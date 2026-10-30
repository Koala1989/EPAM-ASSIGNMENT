"""Seed conformance: does a manual case follow references/seed-manual-test-case.md (and the API variant)?

Rule-based, so checked in code (free, exact). Structure S1-S8, requirement linking L1-L4. Wrapped as a DeepEval
custom metric (SeedConformanceMetric) so it reports next to the judged metrics; no LLM is called.
"""

import re
from dataclasses import dataclass

from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

from case_sources import CASES_DIR, DOCS_DIR, REPO, load_rule_texts

FIELDS = ["Summary", "Requirement", "Area", "Type", "Technique", "Priority", "Tags", "Prerequisites", "Automation", "Review"]
TYPES = {"Positive", "Negative", "Boundary"}
PRIORITIES = {"P1", "P2", "P3"}
VAGUE = re.compile(r"works (correctly|as expected|fine)|behaves correctly|as expected\.?\s*\|", re.I)
QUESTION_ID = re.compile(r"\bQ-[A-Za-z_]+-\d+\b")
SCHEMA = REPO / "requirements" / "openapi-parts.yaml"


def _area_folders() -> dict[str, str]:
    """Area value -> folder, from the seed's 'Area folders' table."""
    seed = (REPO / "references" / "seed-manual-test-case.md").read_text(encoding="utf-8")
    return dict(re.findall(r"^\| `([^`]+)`(?: \(API\))? \| `([^`]+)` \|", seed, re.M))


AREA_FOLDERS = _area_folders()
RULES = load_rule_texts()
QUESTIONS = {
    m.group(1)
    for f in (CASES_DIR / "Open_Questions").glob("*.md")
    for m in re.finditer(r"^\| (Q-[A-Za-z_]+-\d+) \|", f.read_text(encoding="utf-8"), re.M)
}
SCHEMA_TEXT = SCHEMA.read_text(encoding="utf-8")
SCHEMA_LINES = SCHEMA_TEXT.count("\n") + 1
DOC_LINES = {p.name: p.read_text(encoding="utf-8").count("\n") + 1 for p in DOCS_DIR.glob("*.md")}


@dataclass
class Check:
    id: str
    ok: bool
    detail: str = ""


def split_cases(text: str) -> list[tuple[str, str, str]]:
    """(case ID, title, block) for every '### <ID>: <title>' case in a case file."""
    parts = re.split(r"^### ((?:UI|API)-[A-Za-z_]+-\d+): (.*)$", text, flags=re.M)
    return [(parts[i], parts[i + 1].strip(), parts[i + 2]) for i in range(1, len(parts), 3)]


def check_case(case_id: str, block: str, folder: str) -> list[Check]:
    kind, area = case_id.split("-")[0], case_id.split("-", 1)[1].rsplit("-", 1)[0]
    fields = dict(re.findall(r"^\| \*\*(.+?)\*\* \| (.*) \|$", block, re.M))
    order = [f for f in re.findall(r"^\| \*\*(.+?)\*\* \|", block, re.M) if f in FIELDS]
    checks = []

    # S1 ID, Area field and folder agree
    expected_folder = AREA_FOLDERS.get(area)
    s1 = fields.get("Area", "").strip("` ") == area and expected_folder == folder
    checks.append(Check("S1 id-area-folder", s1, f"ID Area {area}, Area field {fields.get('Area')!r}, folder {folder} (expected {expected_folder})"))

    # S2 all ten fields, in the seed's order
    missing = [f for f in FIELDS if f not in fields]
    checks.append(Check("S2 fields", not missing and order == FIELDS, f"missing {missing}" if missing else f"order {order}"))

    # S3 allowed values
    bad = []
    if fields.get("Type", "").strip() not in TYPES:
        bad.append(f"Type {fields.get('Type')!r}")
    if fields.get("Priority", "").strip() not in PRIORITIES:
        bad.append(f"Priority {fields.get('Priority')!r}")
    if not re.search(r"\b(Smoke|Regression)\b", fields.get("Tags", "")):
        bad.append(f"Tags {fields.get('Tags')!r} (needs Smoke or Regression)")
    automation = fields.get("Automation", "")
    if not re.match(r"(Yes|No|Partial)\b", automation):
        bad.append(f"Automation {automation!r}")
    elif not automation.startswith("Yes") and len(automation.split()) < 3:
        bad.append(f"Automation {automation!r} (no reason)")
    if not re.match(r"(Draft|Approved|Changed|Rejected)\b", fields.get("Review", "")):
        bad.append(f"Review {fields.get('Review')!r}")
    checks.append(Check("S3 allowed values", not bad, "; ".join(bad)))

    # S4 prerequisites: one line, User; Settings; Data; Pre-steps in order
    pre = fields.get("Prerequisites", "")
    positions = [pre.find(p) for p in ("User:", "Settings:", "Data:", "Pre-steps:")]
    checks.append(Check("S4 prerequisites order", -1 not in positions and positions == sorted(positions), pre[:80]))

    # S5 steps table: right columns, rows numbered 1..n
    header = "| # | Request | Payload / parameters | Expected result |" if kind == "API" else "| # | Action | Test data | Expected result |"
    rows = [int(n) for n in re.findall(r"^\| (\d+) \|", block.split("**Data sets**")[0], re.M)]
    checks.append(Check("S5 steps table", header in block and rows == list(range(1, len(rows) + 1)) and bool(rows), f"rows {rows}"))

    # S6 postconditions and notes
    checks.append(Check("S6 postconditions and notes", "**Postconditions and cleanup:**" in block and "**Notes:**" in block))

    # S7 no vague expected results
    vague = VAGUE.search(block)
    checks.append(Check("S7 no vague results", not vague, vague.group(0) if vague else ""))

    # S8 API data sets carry an expected status column
    if kind == "API" and "**Data sets**" in block:
        sets = block.split("**Data sets**", 1)[1]
        checks.append(Check("S8 data sets expected status", "expected status" in sets.split("\n\n")[0] or "| expected status |" in sets))

    # L1 every cited rule exists in an inventory
    requirement = fields.get("Requirement", "")
    rule_ids = re.findall(r"\bR-[A-Za-z_]+-\d+\b", requirement)
    unknown = [r for r in rule_ids if r not in RULES]
    checks.append(Check("L1 rules exist", bool(rule_ids) and not unknown, f"unknown {unknown}" if unknown else ("no rule cited" if not rule_ids else "")))

    # L2 source links resolve: doc file and line exist (UI); schema operation or line exists (API)
    broken = []
    for doc, line in re.findall(r"requirements/docs/([\w.-]+\.md)#L(\d+)", requirement):
        if doc not in DOC_LINES or int(line) > DOC_LINES[doc]:
            broken.append(f"{doc}#L{line}")
    for line in re.findall(r"openapi-parts\.yaml#L(\d+)", requirement):
        if int(line) > SCHEMA_LINES:
            broken.append(f"openapi-parts.yaml#L{line}")
    for method, path in re.findall(r"openapi-parts\.yaml (GET|POST|PUT|PATCH|DELETE) (/\S+?)`", requirement):
        if f"\n  {path}:" not in SCHEMA_TEXT:
            broken.append(f"{method} {path}")
    has_source = re.search(r"requirements/docs/|openapi-parts\.yaml", requirement)
    checks.append(Check("L2 sources resolve", bool(has_source) and not broken, f"broken {broken}" if broken else ("no source link" if not has_source else "")))

    # L3 every cited open question exists
    cited = set(QUESTION_ID.findall(block.replace(fields.get("Review", ""), "")))
    review_qs = set(QUESTION_ID.findall(fields.get("Review", "")))
    missing_q = sorted((cited | review_qs) - QUESTIONS)
    checks.append(Check("L3 open questions exist", not missing_q, f"not found {missing_q}" if missing_q else ""))

    # L4 a Draft case that cites open questions in its body names them in Review
    review = fields.get("Review", "")
    if review.startswith("Draft") and cited:
        unlisted = sorted(cited - review_qs)
        checks.append(Check("L4 review lists open questions", not unlisted, f"cited but not in Review {unlisted}" if unlisted else ""))
    return checks


def case_blocks(case_ids: list[str] | None = None) -> list[tuple[str, str, str]]:
    """(case ID, block, folder) for every case in test-cases/ (case_ids None), or only the given IDs.
    An empty list returns no cases: it must never widen to all of them."""
    if case_ids is not None and not case_ids:
        return []
    wanted = set(case_ids) if case_ids is not None else None
    found = []
    for path in sorted(CASES_DIR.glob("*/*.md")):
        if path.parent.name in ("Open_Questions", "Reviews", "Runs") or path.name == "requirements-inventory.md":
            continue
        for case_id, _title, block in split_cases(path.read_text(encoding="utf-8")):
            if wanted is None or case_id in wanted:
                found.append((case_id, block, path.parent.name))
    return found


class SeedConformanceMetric(BaseMetric):
    """Share of seed checks passed across the cases in test_case.metadata['cases'] ((id, block, folder) tuples).
    A custom DeepEval metric with no LLM: measure() runs the checks in code."""

    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.async_mode = False
        self.include_reason = True
        self.strict_mode = False
        self.evaluation_model = None
        self.evaluation_cost = 0

    def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        failures, total, passed = [], 0, 0
        for case_id, block, folder in test_case.metadata["cases"]:
            for check in check_case(case_id, block, folder):
                total += 1
                passed += check.ok
                if not check.ok:
                    failures.append(f"{case_id} {check.id}: {check.detail}")
        self.score = passed / total if total else 0.0
        self.success = self.score >= self.threshold
        self.failures = failures
        self.reason = f"{passed}/{total} checks passed" + ("; " + " | ".join(failures[:15]) if failures else "")
        return self.score

    async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return bool(getattr(self, "success", False))

    @property
    def __name__(self):
        return "Seed conformance"
