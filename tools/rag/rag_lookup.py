"""Confirm inventory rules against the docs through the RAG index, by rule ID.

The test-case-creator's lookup for rules that cite the docs (its step 2.4). It replaces a free-form
query_index.py call so the lookup cannot drift: the query is always the rule's own wording from its
requirements inventory, top-k is fixed at 3, and a rule with no match is reported on stdout, where a
discarded stderr cannot hide it. Pass every rule in one call; no shell loop is needed.

Usage:
    tools/rag/.venv/Scripts/python.exe tools/rag/rag_lookup.py R-REV-07 R-Part-03 ...

For each rule, prints the rule, then the top 3 chunks (exact text from the docs), marking the chunk that
holds the line the inventory cites.

Exit codes: 0 every doc rule matched; 2 at least one doc rule has no chunk above the similarity floor
(fall back to requirements/INDEX.md for it, as the agent instructions say); 3 an unknown rule ID.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from query_index import DEFAULT_MIN_SCORE, search  # noqa: E402

TOP_K = 3  # fixed: the rule's section is ranked 1st or 2nd on the golden set (evals/test_retrieval.py)
TEST_CASES = Path(__file__).resolve().parents[2] / "test-cases"
DOC_LINK = re.compile(r"requirements/docs/(?P<file>[\w.-]+\.md)#L(?P<start>\d+)(?:-L?(?P<end>\d+))?")


def load_rules() -> dict[str, tuple[str, str]]:
    """Rule ID -> (rule text, source cell), from every requirements inventory."""
    rules = {}
    for inventory in TEST_CASES.glob("*/requirements-inventory.md"):
        for line in inventory.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.split("|")]
            if len(cells) > 3 and re.fullmatch(r"R-[A-Za-z_]+-\d+", cells[1]):
                rules[cells[1]] = (cells[2], cells[3])
    return rules


def cited_rank(hits: list[dict], source: str) -> int | None:
    """1-based rank of the first chunk that contains a doc line the inventory cites, or None."""
    for rank, hit in enumerate(hits, 1):
        m = re.match(r"docs/([^#]+)#L(\d+)-L(\d+)", hit["citation"])
        for link in DOC_LINK.finditer(source):
            first, last = int(link["start"]), int(link["end"] or link["start"])
            if m and m.group(1) == link["file"] and int(m.group(2)) <= last and first <= int(m.group(3)):
                return rank
    return None


def main() -> int:
    ids = sys.argv[1:]
    if not ids:
        print(__doc__)
        return 3
    rules = load_rules()
    unknown = [r for r in ids if r not in rules]
    if unknown:
        print(f"UNKNOWN RULE ID: {', '.join(unknown)}. Use rule IDs from test-cases/<Area folder>/requirements-inventory.md.")
        return 3

    no_match = []
    for rule_id in ids:
        text, source = rules[rule_id]
        print(f"=== {rule_id}: {text}")
        if not DOC_LINK.search(source):
            print("    Cites no doc line (schema or index rule): RAG does not apply. Use its cited source.\n")
            continue
        hits = search(text, top_k=TOP_K)
        if not hits:
            no_match.append(rule_id)
            print(f"    NO MATCH: no chunk scored >= {DEFAULT_MIN_SCORE:.2f}. Do not treat this as 'no requirement'. "
                  "Fall back to requirements/INDEX.md and read the section the inventory cites.\n")
            continue
        rank = cited_rank(hits, source)
        for i, hit in enumerate(hits, 1):
            mark = "  <- holds the cited line" if i == rank else ""
            print(f"--- {i}. {hit['citation']} (score={hit['score']:.2f}){mark}")
            print(hit["text"])
        if rank is None:
            print("    The cited doc line is not in the top 3 chunks: check the citation, or raise an Open question.")
        print()

    if no_match:
        print(f"NO MATCH for {', '.join(no_match)}: see above.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
