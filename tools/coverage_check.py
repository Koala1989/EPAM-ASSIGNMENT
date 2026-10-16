"""Rule coverage of manual test cases, for the test-case-reviewer agent.

For each Area given, maps every rule in its requirements inventory to the cases that cite it in their
Requirement field, and lists rules no case cites and rule IDs cases cite that the inventory does not have.
Exact matching on rule IDs only: whether an uncovered rule belongs to the functionality is the reviewer's call.

Usage:
    python tools/coverage_check.py --area CRUD [--area REL ...] [--file <case file> ...]

--area takes the Area value (`Part`, `REV`, `CRUD`, ...); its folder (`test-cases/Revisions/`, ...) is looked up
by tools/areas.py.
--file limits the cases counted to those files (e.g. the functionality under review); default: every case
file in the Area folder.
"""
import argparse
import re
import sys
from pathlib import Path

from areas import area_folder

ROOT = Path(__file__).resolve().parents[1] / "test-cases"
SKIP = {"requirements-inventory.md"}
RULE_ROW = re.compile(r"^\|\s*(?P<id>R-[A-Za-z_]+-\d+)\s*\|\s*(?P<text>[^|]*)\|")
CASE_HEADING = re.compile(r"^###\s+(?P<id>(?:UI|API)-[A-Za-z_]+-\d+):")
REQUIREMENT = re.compile(r"^\|\s*\*\*Requirement\*\*\s*\|(?P<value>.*)\|\s*$")
RULE_REF = re.compile(r"R-[A-Za-z_]+-\d+")


def rules_in(folder):
    rules = {}
    for line in (folder / "requirements-inventory.md").read_text(encoding="utf-8").splitlines():
        m = RULE_ROW.match(line)
        if m:
            rules[m["id"]] = m["text"].strip()
    return rules


def citations(files):
    """{rule ID: [case IDs]} from each case's Requirement field."""
    cited = {}
    for path in files:
        case = None
        for line in path.read_text(encoding="utf-8").splitlines():
            heading = CASE_HEADING.match(line)
            if heading:
                case = heading["id"]
                continue
            req = REQUIREMENT.match(line)
            if case and req:
                for rule in dict.fromkeys(RULE_REF.findall(req["value"])):
                    cited.setdefault(rule, []).append(case)
    return cited


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--area", action="append", required=True, help="Area value; repeatable")
    parser.add_argument("--file", action="append", default=[], help="case file to count; repeatable")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    folders = [area_folder(a) for a in args.area]
    files = [Path(f).resolve() for f in args.file] or sorted(
        p for folder in folders for p in folder.glob("*.md") if p.name not in SKIP)
    missing = [str(f) for f in files if not f.exists()]
    if missing:
        sys.exit(f"Not found: {', '.join(missing)}")

    rules = {rid: (folder.name, text) for folder in folders for rid, text in rules_in(folder).items()}
    cited = citations(files)
    all_rules = {rid for folder in ROOT.iterdir() if (folder / "requirements-inventory.md").exists()
                 for rid in rules_in(folder)}

    print(f"Cases counted from: {', '.join(str(f.relative_to(ROOT.parent)) for f in files)}\n")
    print("| Rule | Area folder | Cases citing it | Rule text |")
    print("|---|---|---|---|")
    for rid, (folder, text) in rules.items():
        cases = ", ".join(cited.get(rid, [])) or "**none**"
        print(f"| {rid} | {folder} | {cases} | {text[:90]} |")

    uncovered = [rid for rid in rules if rid not in cited]
    unknown = sorted(rid for rid in cited if rid not in all_rules)
    print(f"\nRules: {len(rules)} · covered: {len(rules) - len(uncovered)} · not cited by any case: {len(uncovered)}")
    if uncovered:
        print("Not cited: " + ", ".join(uncovered))
    if unknown:
        print("Cited but not in any inventory: " + ", ".join(f"{r} ({', '.join(cited[r])})" for r in unknown))
    sys.exit(1 if unknown else 0)


if __name__ == "__main__":
    main()
