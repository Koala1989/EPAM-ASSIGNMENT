"""Duplicate check for manual test cases, run by the test case creator agent after saving cases."""
import argparse
import glob
import os
import re
import sys
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path

CASE_HEADING = re.compile(r"^###\s+(?P<id>[^:\s]+):\s*(?P<summary>.+?)\s*$")
BLOCK_END = re.compile(r"^(#{1,3}\s|---\s*$)")
CHECK_LINE = re.compile(r"^\*\*Duplicate check:\*\*")
JUDGEMENT_LINE = re.compile(r"^\*\*Duplicate judgement:\*\*")
FIELD_ROW = re.compile(r"^\|\s*\*\*(?P<name>[^*]+)\*\*\s*\|\s*(?P<value>.*?)\s*\|\s*$")
STEP_ROW = re.compile(r"^\|\s*(?P<n>\d+)\s*\|(?P<rest>.*)\|\s*$")
REQ_REF = re.compile(
    r"R-[A-Za-z_]+-\w+|[\w.-]+\.md#L\d+|(?:GET|POST|PUT|PATCH|DELETE)\s+/api/\S+"
)
PLACEHOLDER = re.compile(r"QA-<[^>]*>|<[^>]*>|QA-[0-9a-f]{8}")
TOKEN = re.compile(r"[a-z0-9_]+(?:[./-][a-z0-9_]+)*")
STOPWORDS = set(
    "a an and are as at be by for from in into is it its of on or that the then this to "
    "with without was were will can should must does do not none".split()
)

WEIGHTS = {
    "requirement": 0.20,
    "summary": 0.15,
    "actions": 0.25,
    "expected": 0.25,
    "data": 0.10,
    "user": 0.05,
}
AREA_MISMATCH = 0.8
TYPE_MISMATCH = 0.6
VARIATION_CORE = 0.85
VARIATION_DATA = 0.6
REVIEW_MIN = 50
DUPLICATE_ABOVE = 80
MAX_MATCHES = 5


@dataclass
class Case:
    id: str
    path: Path
    line: int
    summary: str
    fields: dict = field(default_factory=dict)
    actions: list = field(default_factory=list)
    data: list = field(default_factory=list)
    expected: list = field(default_factory=list)


def clean(text):
    text = text.replace("<br>", " ")
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return PLACEHOLDER.sub(" ", text.lower())


def tokens(text):
    words = [w for w in TOKEN.findall(clean(text)) if w not in STOPWORDS]
    return set(words) | {f"{a} {b}" for a, b in zip(words, words[1:])}


def jaccard(a, b):
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def parse_file(path):
    cases, current = [], None
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        heading = CASE_HEADING.match(line)
        if heading:
            current = None
            if not heading["id"].startswith("<"):
                current = Case(heading["id"], path, n, heading["summary"])
                cases.append(current)
            continue
        if BLOCK_END.match(line):
            current = None
            continue
        if current is None:
            continue
        row = FIELD_ROW.match(line)
        if row:
            current.fields[row["name"].strip().lower()] = row["value"]
            continue
        step = STEP_ROW.match(line)
        if step:
            cells = [c.strip() for c in step["rest"].split("|")]
            cells += [""] * (3 - len(cells))
            current.actions.append(cells[0])
            current.data.append(cells[1])
            current.expected.append(cells[2])
    return cases


def features(case):
    requirement = case.fields.get("requirement", "")
    user = re.search(r"User:\s*([^;|]+)", case.fields.get("prerequisites", ""))
    return {
        "requirement": set(REQ_REF.findall(requirement)) or tokens(requirement),
        "summary": tokens(case.fields.get("summary", case.summary)),
        "actions": tokens(" ".join(case.actions)),
        "expected": tokens(" ".join(case.expected)),
        "data": tokens(" ".join(case.data)),
        "user": tokens(user[1] if user else ""),
        "area": case.fields.get("area", "").strip().lower(),
        "type": case.fields.get("type", "").strip().lower(),
    }


def compare(fa, fb):
    parts = {name: jaccard(fa[name], fb[name]) for name in WEIGHTS}
    score = sum(WEIGHTS[n] * parts[n] for n in WEIGHTS)
    core = sum(WEIGHTS[n] * parts[n] for n in WEIGHTS if n != "data") / (1 - WEIGHTS["data"])
    if fa["area"] != fb["area"]:
        score *= AREA_MISMATCH
    if fa["type"] != fb["type"]:
        score *= TYPE_MISMATCH
    data_only = core >= VARIATION_CORE and parts["data"] < VARIATION_DATA
    return round(100 * score), data_only


def status_for(score, data_only):
    # A pair that differs only in test data may be a real boundary variation: a reader decides.
    if score > DUPLICATE_ABOVE and not data_only:
        return "Duplicate"
    return "Review" if score >= REVIEW_MIN else "Unique"


def analyse(cases):
    feats = [features(c) for c in cases]
    matches = [[] for _ in cases]
    for (i, a), (j, b) in combinations(enumerate(cases), 2):
        score, data_only = compare(feats[i], feats[j])
        matches[i].append((score, j, data_only))
        matches[j].append((score, i, data_only))
    results = []
    for i, case in enumerate(cases):
        ranked = sorted(matches[i], key=lambda m: -m[0])
        top = ranked[0] if ranked else (0, None, False)
        results.append({
            "case": case,
            "score": top[0],
            "status": status_for(top[0], top[2]),
            "matches": [(s, cases[j], d) for s, j, d in ranked if s >= REVIEW_MIN],
        })
    return results


def check_line(result):
    case = result["case"]
    shown = []
    for score, other, data_only in result["matches"][:MAX_MATCHES]:
        link = os.path.relpath(other.path, case.path.parent).replace("\\", "/")
        note = ", test data differs" if data_only else ""
        shown.append(f"[{other.id}]({link}) ({score}{note})")
    extra = len(result["matches"]) - MAX_MATCHES
    if extra > 0:
        shown.append(f"+{extra} more")
    return (f"**Duplicate check:** {result['score']} · {result['status']} · "
            f"matches: {', '.join(shown) if shown else 'none'}")


def write_back(path, by_line):
    out, current, start = [], None, 0

    def close():
        if current is None or current["status"] == "Unique":
            return
        had_trailing = False
        while out and not out[-1].strip():
            out.pop()
            had_trailing = True
        # The check line goes before an existing judgement line (seed order: check, then judgement).
        judged = next((i for i in range(len(out) - 1, start - 1, -1) if JUDGEMENT_LINE.match(out[i])), None)
        if judged is None:
            out.extend(["", check_line(current)])
        else:
            while judged > start and not out[judged - 1].strip():
                del out[judged - 1]
                judged -= 1
            out[judged:judged] = ["", check_line(current), ""]
        if had_trailing:
            out.append("")

    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        heading = CASE_HEADING.match(line)
        if heading or BLOCK_END.match(line):
            close()
            current = by_line.get(n) if heading else None
            start = len(out)
        elif current is not None and CHECK_LINE.match(line):
            continue
        out.append(line)
    close()
    while out and not out[-1].strip():
        out.pop()
    newline = "\r\n" if b"\r\n" in path.read_bytes() else "\n"
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline=newline)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=f"Score = highest similarity to any other case (0-100). Above {DUPLICATE_ABOVE}: Duplicate. "
               f"{REVIEW_MIN}-{DUPLICATE_ABOVE}: Review (LLM assesses the listed matches). "
               f"Below {REVIEW_MIN}: Unique. Review and Duplicate are saved as the last line of the case; "
               f"a Unique case gets no line, and any old line is removed.",
    )
    parser.add_argument("files", nargs="*", default=["test-cases/**/*.md"],
                        help="case files or globs (default: every case under test-cases/, all Area folders)")
    parser.add_argument("--case", action="append", metavar="ID",
                        help="save the check only for this case ID (repeatable); it is still compared with all cases")
    parser.add_argument("--dry-run", action="store_true", help="print the report without saving")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    paths = sorted({Path(p) for pattern in args.files for p in glob.glob(pattern, recursive=True)
                    if Path(p).name != "requirements-inventory.md"
                    and not {"Open_Questions", "Reviews", "Runs"} & set(Path(p).parts)})
    if not paths:
        sys.exit(f"No files match: {' '.join(args.files)}")
    cases = [c for p in paths for c in parse_file(p)]
    if not cases:
        sys.exit(f"No test cases found in: {' '.join(map(str, paths))}")

    results = analyse(cases)
    if args.case:
        missing = set(args.case) - {c.id for c in cases}
        if missing:
            sys.exit(f"Case IDs not found: {', '.join(sorted(missing))}")
        results = [r for r in results if r["case"].id in args.case]

    seen = {}
    for c in cases:
        seen.setdefault(c.id, []).append(f"{c.path.name}:{c.line}")
    for case_id, places in seen.items():
        if len(places) > 1:
            print(f"Duplicate ID {case_id}: {', '.join(places)}")

    print("| ID | Score | Status | Matches |")
    print("|---|---|---|---|")
    for r in sorted(results, key=lambda r: -r["score"]):
        print(f"| {r['case'].id} | {r['score']} | {r['status']} | {check_line(r).split(' · matches: ')[1]} |")

    if not args.dry_run:
        by_path = {}
        for r in results:
            by_path.setdefault(r["case"].path, {})[r["case"].line] = r
        for path, by_line in by_path.items():
            write_back(path, by_line)
        print(f"Saved the duplicate check for {len(results)} case(s).")


if __name__ == "__main__":
    main()
