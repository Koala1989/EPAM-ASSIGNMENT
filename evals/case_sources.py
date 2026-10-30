"""Reads the project's own sources for the evals: inventory rules, manual test cases, and doc sections.

Shared by test_retrieval.py (rule texts) and test_agent_cases.py (cases and the doc text they cite).
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CASES_DIR = REPO / "test-cases"
DOCS_DIR = REPO / "requirements" / "docs"

sys.path.insert(0, str(REPO / "tools" / "rag"))
from build_index import chunk_file  # noqa: E402  (the same sections the RAG index stores)

# A doc link in a case or inventory: ../../requirements/docs/<file>#L<start>[-[L]<end>]
DOC_LINK = re.compile(r"requirements/docs/(?P<file>[\w.-]+\.md)#L(?P<start>\d+)(?:-L?(?P<end>\d+))?")
RULE_ID = re.compile(r"\bR-[A-Za-z_]+-\d+\b")


def load_rule_texts() -> dict[str, str]:
    """Rule ID -> rule text, from every requirements inventory table row (| R-xx-NN | text | source | ...)."""
    rules = {}
    for inventory in CASES_DIR.glob("*/requirements-inventory.md"):
        for line in inventory.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.split("|")]
            if len(cells) > 2 and cells[1].startswith("R-"):
                rules[cells[1]] = cells[2]
    return rules


def load_rule_risks() -> dict[str, str]:
    """Rule ID -> Risk (H, M or L), from the inventories' Risk column (| R-xx-NN | text | source | risk | ...)."""
    risks = {}
    for inventory in CASES_DIR.glob("*/requirements-inventory.md"):
        for line in inventory.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.split("|")]
            if len(cells) > 4 and cells[1].startswith("R-") and cells[4] in ("H", "M", "L"):
                risks[cells[1]] = cells[4]
    return risks


def find_case(case_id: str) -> dict:
    """Parse one manual case (### <ID>: <title> block) into its fields and step rows."""
    header = re.compile(rf"^### {re.escape(case_id)}: (?P<title>.+)$", re.M)
    for path in CASES_DIR.glob("*/*.md"):
        text = path.read_text(encoding="utf-8")
        m = header.search(text)
        if not m:
            continue
        nxt = re.search(r"^### ", text[m.end():], re.M)
        block = text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]
        fields = dict(re.findall(r"^\| \*\*(.+?)\*\* \| (.*) \|$", block, re.M))
        steps = []
        for row in re.findall(r"^\| (\d+) \| (.*) \|$", block, re.M):
            cells = [c.strip() for c in row[1].split(" | ")]
            steps.append({"n": int(row[0]), "action": cells[0], "data": cells[1], "expected": cells[-1]})
        return {"id": case_id, "title": m["title"], "file": str(path.relative_to(REPO)), "fields": fields, "steps": steps}
    raise KeyError(f"{case_id} not found under {CASES_DIR}")


def doc_sections(text: str) -> list[str]:
    """The doc sections (heading to next heading) that contain each doc line cited in `text`, deduplicated."""
    sections = []
    for link in DOC_LINK.finditer(text):
        first = int(link["start"])
        last = int(link["end"] or first)
        for _title, start, end, body in chunk_file(DOCS_DIR / link["file"]):
            if start <= last and first <= end:
                labelled = f"[{link['file']}#L{start}-L{end}]\n{body}"
                if labelled not in sections:
                    sections.append(labelled)
    return sections
