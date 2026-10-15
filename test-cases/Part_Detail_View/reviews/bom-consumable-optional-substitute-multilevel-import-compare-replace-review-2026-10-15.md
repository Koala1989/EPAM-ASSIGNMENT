# Review: BOM consumable, optional and substitute lines, multi-level BOMs, BOM import, comparison and component replacement (UI), 2026-10-15

**Cases reviewed:** UI-Detail_View-038 to UI-Detail_View-079 (42 cases) · **Verdict:** Changes required

There is no Blocker. The verdict is still Changes required because several Majors (F3, F4, F5, F6) mean the architect has to edit the Expected results of existing cases. "Approve with changes" covers only Majors that leave existing expectations as they are.

## Coverage

`python tools/coverage_check.py --area Detail_View --file test-cases/Part_Detail_View/bom-consumable-optional-substitute-multilevel-import-compare-replace.md`: Rules: 70 · covered: 17 · not cited by any case: 53 · exit 0 (every cited rule ID exists; the cited `R-Part-19`, `R-Part-28` to `R-Part-31` exist in `Part_Creation_and_Import/requirements-inventory.md`).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Detail_View-54 | 038, 040, 041, 042 | Covered | None: the consumable case (040) and the non-consumable case (041) are both present. |
| R-Detail_View-55 | 039 | Covered | None |
| R-Detail_View-56 | 042, 043, 044, 045, 046 | Covered | None: include, exclude and included-but-not-allocated are all present. |
| R-Detail_View-57 | 047 | Covered | **Major (F1):** the rule says a line "may have multiple substitute parts". Every case uses exactly one substitute. |
| R-Detail_View-58 | 048, 049, 050 | Covered | Same gap as F1: the available quantity is never checked with two or more substitutes. |
| R-Detail_View-61 | 056 to 061 | Covered | **Major (F2):** the rule names "CSV or Excel". Only CSV is imported, so the Excel valid class has no case. The blocked user (`reader`, 059) is covered. |
| R-Detail_View-64 | 051 to 055 | Covered | None. Circular BOM (054) and a deep nesting (052) are present. |
| R-Detail_View-68 | 062, 063, 067, 068, 069 | Covered | None |
| R-Detail_View-69 | 063 to 067, 069 | Covered | None: all three view modes, zero differences (066) and an empty BOM (067). |
| R-Detail_View-70 | 070 to 079 | Covered | None: several assemblies, an empty selection, new = old, a duplicate line, cancel, a blocked user (078) and validation. |
| R-Detail_View-21 | 053, 070 | Covered (supporting) | Both the visible case (053) and the hidden case (070) are present. |
| R-Detail_View-50, -60, -62, -63, -65, -67 | various | Covered (supporting) | Primary home is the functionality "BOM tab editing and validation" (UI-Detail_View-001 to 037). |
| R-Detail_View-51, -52, -53, -59, -66 | none | Out of scope | Belong to "BOM tab editing and validation". |
| R-Detail_View-01 to -20, -22 to -49 | none | Out of scope | Header, image, other tabs, test templates, related parts and attachments functionalities. |

The functionality has Negative cases (046, 054, 058, 059, 060, 068, 070, 073, 074, 075, 078, 079).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| F1 | Major | R-Detail_View-57, R-Detail_View-58 | Coverage depth | No case gives a line two or more substitutes. Nothing checks that stock of *any* substitute can be allocated, or that the available quantity counts every substitute. | manufacturing-bom.md#L71 ("may have multiple substitute parts ... any of the substitute parts"), #L74 ("substitute parts" plural) | Rerun the creator for a line with two substitutes (allocation from the second one, and the available quantity = component + both substitutes, Proposed under Q-Detail_View-10). |
| F2 | Major | R-Detail_View-61 | Coverage depth | Only a CSV file is imported. The Excel class named by the rule has no positive case. | manufacturing-bom.md#L131 ("such as CSV or Excel") | Rerun the creator for an Excel (`.xlsx`) BOM import case. |
| F3 | Major | UI-Detail_View-061 step 2 | Rule outcome stated | "Not Validated" is written as `Proposed`, but the rules state it: creating a line requires revalidation, and an invalid BOM shows "Not Validated" with *Validate BOM*. The rule outcome should come first as fact, then `Open: Q-Detail_View-12` for anything import-specific. | manufacturing-bom.md#L163 ("Whenever a BOM line item is created ... must be validated"), #L181, #L191; R-Detail_View-65, R-Detail_View-67 | Edit step 2: the status reads "Not Validated" and *Validate BOM* is shown (R-Detail_View-65, R-Detail_View-67). Open: Q-Detail_View-12. |
| F4 | Major | UI-Detail_View-077 step 2 | Rule outcome stated | Same problem as F3. *Component ID* is a checksum field, and a changed checksum field marks the assembly "not validated". The case gives this outcome only as `Proposed`. | manufacturing-bom.md#L170, #L181, #L191; R-Detail_View-65, R-Detail_View-67 | Edit step 2 to state "Not Validated" as fact (R-Detail_View-65, R-Detail_View-67), then Open: Q-Detail_View-14 only for the replacement path. |
| F5 | Major | UI-Detail_View-079 step 2 | No assumptions | Says the line still holds `Old` because "R-Detail_View-70: the replacement happens on confirmation". R-Detail_View-70 and the docs say nothing about confirming or cancelling. Step 1 of the same case labels "nothing is replaced" as Proposed, so the two steps contradict each other. | manufacturing-bom.md#L221-231 (no confirm or cancel stated); R-Detail_View-70 | Edit step 2 to `Proposed, to confirm in Q-Detail_View-14: ...` and drop the rule attribution. |
| F6 | Major | UI-Detail_View-050 step 1 | No assumptions | "The substitute is removed from the line" is written as fact. No rule states that a substitute can be removed: R-Detail_View-63 covers only adding one. | manufacturing-bom.md#L147-153; R-Detail_View-63 | Edit step 1 to `Proposed, to confirm in Q-Detail_View-10: ...`. Also drop R-Detail_View-63 from the Requirement, or note that it supports only the form name. |
| F7 | Major | 038, 039, 043, 048 to 051, 053 to 055, 059, 062 to 079 vs `open-questions.md` | Open-question marking | (a) View-only cases are marked with Q-Detail_View-01, which is about *editing and validating* BOMs: 039, 048, 049, 053, 062 to 069, 070. Q-01 does not affect them. (b) Cases that do depend on Q-01, Q-02, Q-04 or Q-06 are missing from those rows' "Affected cases" columns, which list only 001 to 037. Examples: Q-01 for 038, 043, 050, 051, 054, 055, 071 to 079; Q-02 for 050; Q-04 for 075; Q-06 for 055, 061, 077. Q-02 on 050 is also doubtful: Q-02 asks about line edit and delete, while substitute removal is in Q-10. | open-questions.md rows Q-Detail_View-01, -02, -04, -06 | Architect: remove Q-01 from the view-only cases (and Q-02 from 050). Extend the Affected cases of Q-01, Q-04 and Q-06 (the architect owns that file). |
| F8 | Minor | UI-Detail_View-044 step 3 | No assumptions | "Quantity still `5`" is attributed to R-Detail_View-56 as fact. The rule says only that excluded items are not allocated; it says nothing about stock consumption. UI-Detail_View-045 step 3 labels the matching consumption outcome as Proposed, so the two cases are inconsistent. | manufacturing-bom.md#L67 | Mark as `Proposed, to confirm in Q-Detail_View-09`. |
| F9 | Minor | UI-Detail_View-045 step 1 | Fidelity | The step allocates stock manually, but the Expected result quotes the rule about what happens *on completion when optional items are included*. The quoted outcome does not follow from this action. | manufacturing-bom.md#L67 | Move the quote to step 2. Step 1 expects only that the allocation is saved. |
| F10 | Minor | UI-Detail_View-054 | Rule outcome stated | Uses `Not known`, but Q-Detail_View-11 proposes an outcome ("circular BOMs are rejected"). The seed allows `Not known` only when nothing can be proposed. | seed-manual-test-case.md L28; open-questions.md Q-Detail_View-11 | Change to `Proposed, to confirm in Q-Detail_View-11: the form is rejected (or Parent is not offered)`. |
| F11 | Minor | UI-Detail_View-038, -043, -051, -055 | Seed format | Expected results cite R-Detail_View-62, which is not in the Requirement field. The same happens in 057, which cites R-Part-31 (step 3) without listing it. | Requirement fields of those cases | Add the cited rule IDs to Requirement, with source links. |
| F12 | Minor | UI-Detail_View-057, -058, -061, -062, -066 to -069 | Seed format | The Data part of Prerequisites leaves out how the records are created ("created via API as `admin`") and, in 058, 061 and 067 to 069, the category. 062 says only "each with a BOM", without lines or quantities. | seed-manual-test-case.md L20 | Fill in the data and how it is created. |
| F13 | Minor | UI-Detail_View-052 | Technique | Labelled `Boundary value analysis` and Type Boundary, but "unlimited" has no boundary. The title says four levels, while the data has three nested BOMs (L1, L2, L3, then Leaf). | manufacturing-bom.md#L157 | Relabel as Equivalence partitioning (valid class: multi-level, three BOM levels) and Type Positive, or align the title. |
| F14 | Minor | UI-Detail_View-074 | Seed format | Postconditions read "the BOM is unchanged expected", which states an outcome the case marks Not known. | Case text | Reword to "the BOM may or may not be changed; ...". |
| F15 | Minor | UI-Detail_View-048 step 1 | Specific / no assumptions | The value `5` for the available quantity before any substitute is stated as fact, while the column itself is open. | R-Detail_View-58; Q-Detail_View-10 | Prefix with `Proposed, to confirm in Q-Detail_View-10`, or keep it and accept it as the obvious base case (architect's call). |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Detail_View-038 | 54 | UI-Detail_View-043 | Keep | Consumable flag (R-Detail_View-54) vs Optional flag (R-Detail_View-56) |
| UI-Detail_View-043 | 54 | UI-Detail_View-038 | Keep | Optional flag (R-Detail_View-56) vs Consumable flag (R-Detail_View-54) |
| UI-Detail_View-064 | 59 | UI-Detail_View-065 | Keep | *Show different parts* vs *Show common parts*, opposite listed lines |
| UI-Detail_View-065 | 59 | UI-Detail_View-064 | Keep | *Show common parts* vs *Show different parts*, opposite listed lines |

## Questions for the architect

1. R-Part-19 requires *staff* **and** the `change` permission. UI-Detail_View-059 checks only `reader` (neither). Should there be a case for a user who has `change` but is not staff (possibly `engineer`, depending on Q-Detail_View-12)? I cannot tell from the docs which demo user fits.
2. UI-Detail_View-055: manufacturing-bom.md#L163 says "any assemblies which are associated with that BOM must be validated". Is a parent assembly "associated" with a sub-assembly's BOM? The case correctly leaves this as Proposed under Q-Detail_View-11. Please confirm that wording when you answer Q-11.
3. UI-Detail_View-069 cites R-Detail_View-68 ("can highlight ... quantities") but still opens whether a quantity-only difference counts. Should R-Detail_View-68 be taken as settling this, so the Open part covers only the display?
