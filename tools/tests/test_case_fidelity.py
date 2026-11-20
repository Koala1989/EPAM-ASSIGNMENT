"""Tests for tools/case_fidelity.py, against the repo's real cases. Run from the repo root:
  python -m unittest discover -s tools/tests -v

The mutation tests change a spec that matches its case (ui-part-006) and expect each change to be reported. The draft
test is the playwright-test-generator's first UI-Categories-009 spec of 2026-11-09, which the gate refused: it named
its parts through an array (`partNames[0]`), which the check could not read, so it reported five parts as missing
and missed the real defect (`Part Sib` in an extra category, `Sibling 2`, instead of the case's `Sibling`).
"""

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from case_fidelity import REPO, check  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
SPEC_009 = "automation/tests/ui/Categories/ui-categories-009.spec.ts"
SPEC_006 = "automation/tests/ui/Part/ui-part-006.spec.ts"


def problems(text: str, path: str) -> list[str]:
    return [str(p) for p in check(text, path).problems]


class DraftWithArrayNames(unittest.TestCase):
    draft = (FIXTURES / "ui-categories-009.draft1.spec.ts.txt").read_text(encoding="utf-8")

    def test_reports_the_real_defect_only(self):
        found = problems(self.draft, SPEC_009)
        self.assertEqual(len(found), 1, found)
        self.assertIn('part "Part Sib" is created in "Sibling 2"', found[0])
        self.assertIn('put it in "Sibling"', found[0])

    def test_no_part_reported_missing(self):
        self.assertFalse([p for p in problems(self.draft, SPEC_009) if "the spec does not" in p])

    def test_mapped_string_array_resolves_too(self):
        mapped = re.sub(r"const partNames = \[.*?\];",
                        "const partNames = ['Part Top', 'Part Mid', 'Part Leaf', 'Part Deep', 'Part Sib']"
                        ".map((label) => data.name(label));", self.draft, flags=re.S)
        self.assertNotEqual(mapped, self.draft)
        found = problems(mapped, SPEC_009)
        self.assertEqual(len(found), 1, found)
        self.assertIn('"Part Sib" is created in "Sibling 2"', found[0])

    def test_fixed_draft_passes(self):
        fixed = self.draft.replace("data.name('Sibling 2')", "data.name('Sibling')").replace(
            "    await data.category(data.name('Sibling'), { parent: top.pk });\n", "", 1)
        self.assertEqual(problems(fixed, SPEC_009), [])


class Mutations(unittest.TestCase):
    base = (REPO / SPEC_006).read_text(encoding="utf-8")

    def assertCaught(self, mutated: str, path: str = SPEC_006):
        self.assertNotEqual(mutated, self.base, "the mutation changed nothing")
        self.assertTrue(problems(mutated, path), "the mutation was not reported")

    def test_base_matches(self):
        self.assertEqual(problems(self.base, SPEC_006), [])

    def test_dropped_tag(self):
        self.assertCaught(self.base.replace("'@cross-functional', ", "", 1))

    def test_wrong_title(self):
        self.assertCaught(self.base.replace("UI-Part-006: Create a part", "UI-Part-006: Make a part", 1))

    def test_renumbered_step(self):
        self.assertCaught(self.base.replace("'2. Enter", "'3. Enter", 1))

    def test_dropped_step(self):
        self.assertCaught(re.sub(r"await test\.step\('4\..*", "", self.base, flags=re.S) + "\n}); });")

    def test_step_without_expect(self):
        self.assertCaught(re.sub(r"(test\.step\('3\. Press Submit'.*?)(?=await test\.step\('4)",
                                 lambda m: re.sub(r"await expect\(.*?;\n", "", m.group(1), flags=re.S),
                                 self.base, flags=re.S))

    def test_missing_prerequisite(self):
        self.assertCaught(re.sub(r"await data\.company\(data\.name\('Manufacturer'\).*?\);", "({ pk: 0 });",
                                 self.base, flags=re.S))

    def test_wrong_record_kind(self):
        self.assertCaught(self.base.replace("await data.company(data.name('Supplier')", "await data.part(data.name('Supplier')"))

    def test_unused_test_data_name(self):
        self.assertCaught(self.base.replace("data.trackPart(data.name('Connector'))", "data.trackPart('fixed name')"))

    def test_broken_case_line(self):
        self.assertCaught(self.base.replace("(UI-Part-006)", "(UI-Part-999)", 1))

    def test_wrong_file_name(self):
        self.assertTrue(problems(self.base, "automation/tests/ui/Part/ui-part-007.spec.ts"))

    def test_wrong_category_link(self):
        spec_012 = "automation/tests/ui/Categories/ui-categories-012.spec.ts"
        text = (REPO / spec_012).read_text(encoding="utf-8")
        mutated = text.replace("data.name('Part Leaf'), { category: leaf.pk }", "data.name('Part Leaf'), { category: mid.pk }")
        self.assertNotEqual(mutated, text)
        self.assertTrue([p for p in problems(mutated, spec_012) if '"Part Leaf" is created in "Mid"' in p])


if __name__ == "__main__":
    unittest.main()
