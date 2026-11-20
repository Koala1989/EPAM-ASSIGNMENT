"""ReviewScore: a custom DeepEval metric that turns a reviewer agent's review file into a 0-1 score for the spec.

The reviewers (playwright-test-reviewer, api-test-reviewer) already judge the generated spec against its case and the
conventions, and save that judgement in a fixed format (automation/reviews/<ui|api>/<case>-review-<date>.md). This
metric only reads that format; it makes no LLM call and costs nothing beyond the review itself.

  coverage = Covered / (Covered + Weakened + Missing), over the rows of the "Case coverage" table
  score    = coverage - 0.2 per Major - 0.05 per Minor, capped at 0.3 if there is any Blocker, kept within 0..1
  passed   = score >= 0.7

Rows that are not case steps (pre-steps, postconditions) are skipped. A cell that names several verdicts counts as
the worst one ("Name Covered. Category **Weakened**" is Weakened). Extra rows (asserts what the case does not state)
are left out of coverage: if they matter, the reviewer raises them as findings. A review that cannot be parsed gets no
score (metric.error), not a 0.
"""

import re
from dataclasses import dataclass, field

from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase, SingleTurnParams

PASS_THRESHOLD = 0.7
MAJOR_PENALTY = 0.2
MINOR_PENALTY = 0.05
BLOCKER_CAP = 0.3

VERDICTS = ("Missing", "Weakened", "Covered", "Extra")  # worst first
SEVERITIES = ("Blocker", "Major", "Minor", "Info")


@dataclass
class Review:
    case: str | None
    spec: str | None
    verdict: str | None
    findings: dict[str, int]  # severity -> count
    rows: dict[str, int] = field(default_factory=dict)  # coverage verdict -> count
    unclassified: list[str] = field(default_factory=list)  # case steps whose verdict cell names no verdict
    notes: list[str] = field(default_factory=list)

    @property
    def coverage(self) -> float | None:
        judged = sum(self.rows.get(v, 0) for v in ("Covered", "Weakened", "Missing"))
        return self.rows.get("Covered", 0) / judged if judged else None


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _header(text: str, item: str) -> str | None:
    m = re.search(rf"^\|\s*{item}\s*\|\s*(.+?)\s*\|\s*$", text, re.M)
    return m.group(1) if m else None


def _table(text: str, first_column: str) -> list[list[str]]:
    """Body rows of the first table whose header starts with this column."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(rf"^\|\s*{re.escape(first_column)}\s*\|", line):
            rows = []
            for body in lines[i + 2:]:
                if not body.startswith("|"):
                    break
                rows.append(_cells(body))
            return rows
    return []


def parse_review(text: str) -> Review:
    title = re.search(r"^# Review:\s*(\S+)", text, re.M)
    spec, verdict = _header(text, "Spec"), _header(text, "Verdict")
    review = Review(case=title.group(1) if title else None, spec=spec.strip("`") if spec else None,
                    verdict=verdict.strip("* ") if verdict else None, findings={})

    counts = re.search(r"(\d+) Blocker, (\d+) Major, (\d+) Minor, (\d+) Info", _header(text, "Findings") or "")
    table = [row for row in _table(text, "#") if len(row) > 1 and row[0].isdigit()]
    in_table = {s: sum(row[1].strip("* ") == s for row in table) for s in SEVERITIES}
    if counts:
        review.findings = dict(zip(SEVERITIES, map(int, counts.groups())))
        if any(review.findings[s] != in_table[s] for s in ("Blocker", "Major")) and table:
            review.notes.append(f"header counts {review.findings} differ from the findings table {in_table}")
    elif table:
        review.findings = in_table
        review.notes.append("no Findings line in the header: counted the findings table")

    for row in _table(text, "Case step"):
        if not re.match(r"\d", row[0]):  # pre-steps, postconditions: not case steps
            continue
        named = [v for v in VERDICTS if re.search(rf"\b{v}\b", row[-1], re.I)]
        if named:
            review.rows[named[0]] = review.rows.get(named[0], 0) + 1
        else:
            review.unclassified.append(f"{row[0][:40]}: {row[-1][:60]}")
    return review


class ReviewScoreMetric(BaseMetric):
    """actual_output is the review file's text; input names the spec under review (for the report only)."""

    _required_params = [SingleTurnParams.ACTUAL_OUTPUT]

    def __init__(self, threshold: float = PASS_THRESHOLD):
        self.threshold = threshold
        self.include_reason = True
        self.async_mode = False
        self.evaluation_cost = 0.0
        self.review: Review | None = None

    def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        self.error = None
        self.review = review = parse_review(test_case.actual_output or "")
        missing = [name for name, ok in (("Verdict", review.verdict), ("Findings counts", review.findings),
                                         ("Case coverage rows", review.coverage is not None)) if not ok]
        if missing:
            self.score, self.success = None, False
            self.error = self.reason = f"review not in the reviewer format: no {', '.join(missing)}"
            return self.score

        f = review.findings
        score = review.coverage - MAJOR_PENALTY * f["Major"] - MINOR_PENALTY * f["Minor"]
        if f["Blocker"]:
            score = min(score, BLOCKER_CAP)
        self.score = round(min(1.0, max(0.0, score)), 3)
        self.score_breakdown = {"coverage": round(review.coverage, 3), **f, **review.rows}
        self.success = self.score >= self.threshold

        parts = [f"coverage {review.rows.get('Covered', 0)}/{sum(review.rows.get(v, 0) for v in VERDICTS[:3])}"
                 + "".join(f", {n} {v}" for v, n in review.rows.items() if v != "Covered"),
                 f"{f['Blocker']} Blocker, {f['Major']} Major, {f['Minor']} Minor" + (" (Blocker caps at 0.3)" if f["Blocker"] else ""),
                 f"reviewer verdict: {review.verdict}"]
        expected_verdict = "Changes required" if f["Blocker"] else "Approve with changes" if f["Major"] else None
        if expected_verdict and review.verdict != expected_verdict:
            parts.append(f"verdict does not match the counts (expected {expected_verdict})")
        if review.unclassified:
            parts.append(f"left out, no verdict word: {'; '.join(review.unclassified)}")
        self.reason = ". ".join(parts + review.notes)
        return self.score

    async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return bool(self.success)

    @property
    def __name__(self):
        return "Review Score"
