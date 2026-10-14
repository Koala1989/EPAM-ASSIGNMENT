"""Area value -> test-cases folder.

Folders have full names (`Attributes`, `API_Create_Read_Update_Delete`); Area values and IDs stay short (`ATT`,
`CRUD`, `R-ATT-01`). Each folder's requirements-inventory.md declares its Area through its rule IDs, so the
folder is found by reading the inventories: no second mapping table to keep in step with
references/seed-manual-test-case.md ("Area folders").
"""
import re
import sys
from pathlib import Path

TEST_CASES = Path(__file__).resolve().parents[1] / "test-cases"
RULE_ROW = re.compile(r"^\|\s*R-(?P<area>[A-Za-z_]+)-\d+\s*\|", re.M)


def area_folders():
    """{Area value: folder path} for every folder with a requirements inventory."""
    found = {}
    for inventory in sorted(TEST_CASES.glob("*/requirements-inventory.md")):
        m = RULE_ROW.search(inventory.read_text(encoding="utf-8"))
        if m:
            found[m["area"]] = inventory.parent
    return found


def area_folder(area):
    folders = area_folders()
    if area in folders:
        return folders[area]
    if (TEST_CASES / area / "requirements-inventory.md").exists():  # a folder name was given
        return TEST_CASES / area
    sys.exit(f"Unknown Area {area}. Known: {', '.join(f'{a} ({p.name})' for a, p in folders.items())}")
