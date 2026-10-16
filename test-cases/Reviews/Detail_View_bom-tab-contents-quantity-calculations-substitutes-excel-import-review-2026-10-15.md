# Review: BOM tab contents and visibility, quantity calculations, multiple substitutes and Excel import (UI), 2026-10-15

**Cases reviewed:** UI-Detail_View-201 to UI-Detail_View-234 (34 cases, `test-cases/Part_Detail_View/bom-tab-contents-quantity-calculations-substitutes-excel-import.md`) · **Verdict:** Changes required

## Coverage

`coverage_check.py --area Detail_View --file .../bom-tab-contents-quantity-calculations-substitutes-excel-import.md`: Rules: 70 · covered: 12 · not cited by any case: 58 · exit code 0 (every cited rule ID exists; the R-Part-* IDs cited are in `Part_Creation_and_Import/requirements-inventory.md`).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Detail_View-18 | 201 | Covered | None |
| R-Detail_View-19 | 203, 204, 205 | Covered | Hidden case present (204 step 3, 205 step 1). None |
| R-Detail_View-50 | 201, 202, 203, 205, 206, 222, 226, 233, 234 | Covered | Zero-line boundary present (203). 202 omits the Raw Amount property (Minor, F-12) |
| R-Detail_View-51 | 206, 207, 212, 213, 227 | Covered | Lower limit 0 (206) and above 0 (207). Upper limit / invalid attrition belongs to the editing and validation functionality (Q-Detail_View-04, UI-Detail_View-009 to 020) |
| R-Detail_View-52 | 206, 208, 212, 227 | Covered | 0 and above 0. None |
| R-Detail_View-53 | 206, 209, 210, 211, 212, 227 | Covered | Below / on / above a multiple present (209 / 210 / 211); unset (206). None |
| R-Detail_View-57 | 214, 215, 216, 220 | Covered | Several substitutes, stock only on the second, split allocation, shared substitute. None |
| R-Detail_View-58 | 214, 216, 217, 218 | Covered | None (zero-stock substitute is UI-Detail_View-049) |
| R-Detail_View-59 | 213 | Covered (incidental) | Out of the functionality's core; editing mode is the editing functionality |
| R-Detail_View-60 | 219 | Covered | Blocked user (`reader`) present |
| R-Detail_View-61 | 221 to 234 | Covered | Valid, several rows, manual mapping, mixed valid/invalid, removed row, booleans, numerics, .xls, empty, multi-sheet, corrupt, bad quantity, duplicate, Unicode. Import permission (R-Part-19) blocked case is UI-Detail_View-059 (CSV functionality); no gap |
| R-Detail_View-63 | 217, 219, 220 | Covered | None |
| R-Detail_View-01 to 17, 20 to 49 | none | Out of scope | Header, Variants, Stock, Allocated, Build Orders, Used In, Suppliers, order tabs, tests, related parts, attachments: other Detail_View functionalities |
| R-Detail_View-54, 55, 56 | none | Out of scope | Consumable / Optional lines: "BOM consumable, optional, substitute, multi-level, import, comparison and replacement" (UI-Detail_View-038 to 046) |
| R-Detail_View-62, 65, 66, 67 | none | Out of scope | Adding lines and BOM validation: "BOM tab editing and validation" |
| R-Detail_View-64, 68, 69, 70 | none | Out of scope | Multi-level BOM, comparison, Replace Component: the consumable/optional/multi-level/compare/replace functionality |

No rule in scope is without a case, and every in-scope limit, "only" and permission rule has its boundary, hidden or blocked case. A Negative case exists (219, 224, 229 to 233).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| F-01 | Blocker | UI-Detail_View-233 | No assumptions | The Summary states as a requirement "the BOM may contain a component once", and the Notes call it "the same rule" as UI-Detail_View-017. No cited source states that a component may appear only once; Q-Detail_View-04 asks exactly this ("Is a duplicate component in the same BOM ... rejected"). The Expected results are correctly labelled Proposed, but the Summary would steer an automator to assert a rejection. | R-Detail_View-50 (manufacturing-bom.md#L23-37) lists line properties only; R-Part-31 (concepts-data_import.md#L106-110) defines row states only; Q-Detail_View-04 | Edit the Summary to describe the scenario without the restriction (e.g. "a workbook lists one component in two rows: whether the second row is accepted"), and drop "rule" from the Notes. Step 1 also puts `Open:` before `Proposed`; reorder to seed order (Minor). |
| F-02 | Major | UI-Detail_View-209, 210, 211 | Rule outcome stated / No assumptions | The required quantities `10`, `10`, `15` are written as fact. R-Detail_View-53 states only that the required quantity is rounded up to the multiple; that the required quantity before rounding is line quantity x build quantity (9, 10, 11) is the formula Q-Detail_View-41 asks for ("what is the exact formula"). The sibling cases 206, 207, 208, 212 label the same kind of derived value "Proposed, to confirm in Q-Detail_View-41". | manufacturing-bom.md#L33; Q-Detail_View-41 | Keep the rounding fact (R-Detail_View-53), and write the number as `Proposed, to confirm in Q-Detail_View-41: 10` (resp. `10`, `15`). |
| F-03 | Major | UI-Detail_View-216 | Rule outcome stated | Step 2 states "The allocation is saved" as fact, but whether one line's allocation can be split across the component and a substitute is the open part of Q-Detail_View-44 (Proposed there: it can). | manufacturing-bom.md#L71 (substitute stock "may be allocated against the particular line item"; splitting not stated); Q-Detail_View-44 | Write step 2's outcome as `Proposed, to confirm in Q-Detail_View-44: the allocation is saved`, keeping the R-Detail_View-57 fact that substitute stock may be allocated. |
| F-04 | Major | UI-Detail_View-223 | Fidelity | Step 2 cites R-Part-23 ("the user must map it manually" when a related field's unique identifier cannot be determined) as the rule for mapping file column headers. R-Part-23 is about mapping related-record identifiers (e.g. a part given by name rather than `ID`) to existing records, not header-to-field mapping, which is R-Part-28. | concepts-data_import.md#L44 vs #L90 | Drop R-Part-23 from the Requirement and step 2 (R-Part-28 alone covers the step), or, if the intent is related-record mapping, rewrite the step to map the `Component` values to the existing part and mark Q-Detail_View-12 (part by ID or name). |
| F-05 | Minor | UI-Detail_View-204 | Rule outcome stated | Step 2 "The change is saved" is not stated by any cited rule (Q-Detail_View-43 asks whether switching Assembly off is allowed; Proposed: allowed). Low risk here because the part has no BOM lines. | Q-Detail_View-43 | Label as `Proposed, to confirm in Q-Detail_View-43`. |
| F-06 | Minor | UI-Detail_View-205 | Notes | The Note says a refused data setup should be recorded as a finding; the docs are silent on it, so a refusal answers Q-Detail_View-43 ("is switching it off blocked when the part has BOM lines"), not an app/doc mismatch. | Q-Detail_View-43 | Point the Note at Q-Detail_View-43 instead of `findings.md`. |
| F-07 | Minor | UI-Detail_View-216 | Fidelity | Title and Summary say the line is allocated "from the component and two substitutes", but the steps allocate from Comp A and Comp B only (Comp C stays unallocated). R-Detail_View-58 is cited but no step checks the available quantity. | Steps 1-3 | Reword the title/Summary to "the component and one of two substitutes", and drop R-Detail_View-58 or add an available-quantity check. |
| F-08 | Minor | UI-Detail_View-217 | Fidelity | Cites R-Detail_View-63, which covers adding a substitute; the case removes one. | manufacturing-bom.md#L147-153 | Keep R-Detail_View-58 only, or note that removal is under Q-Detail_View-10. |
| F-09 | Minor | UI-Detail_View-227 | Fidelity | Cites R-Detail_View-51, 52, 53 (calculation semantics) but only checks that the imported values are stored; the stored properties are R-Detail_View-50. | manufacturing-bom.md#L23-37 | Cite R-Detail_View-50 and R-Detail_View-61; drop 51 to 53 or note they are not exercised. |
| F-10 | Minor | UI-Detail_View-222 | Seed format | Step 1 cites R-Part-31 (Pending state), which is not in the Requirement field. Same pattern in 221 is fine (R-Part-31 is listed there). | Requirement field vs step 1 | Add R-Part-31 to the Requirement. |
| F-11 | Minor | UI-Detail_View-232 | Rule outcome stated | Step 1 opens with "Row errors are displayed (R-Part-30)" as fact, then proposes that the row is in Error state; whether `abc` is an error at all is the proposed part (quantity format is Q-Detail_View-04). Steps 2-3 follow from the proposed Error state. | concepts-data_import.md#L104-108; Q-Detail_View-04 | Put the Proposed error state first; keep steps 2-3 as "if in Error state" facts. |
| F-12 | Minor | UI-Detail_View-202 | Fidelity | Summary says "every property" but omits Raw Amount, one of the properties R-Detail_View-50 lists. | manufacturing-bom.md#L29 | Add Raw Amount or say it is covered under Unit_measure (R-Unit_measure-16 to 18). |
| F-13 | Minor | UI-Detail_View-214 | Technique | "Boundary value analysis (more than one substitute)" is not a boundary (no limit is stated; Q-Detail_View-44 asks if there is one). | manufacturing-bom.md#L71 | Keep Equivalence partitioning only. |
| F-14 | Minor | UI-Detail_View-204, 205 | User | `allaccess` is used to switch the Assembly attribute; `engineer` (part management) is the least-privileged demo user for part edits. | Seed "Demo users" | Use `engineer`, or state why `allaccess` is needed. |
| F-15 | Minor | UI-Detail_View-201, 202, 203, 214, 218 | User | View-only checks use `engineer`; the seed names `reader` for view-only checks. Whether `reader` sees the BOM tab and available quantity is not stated, so this is a choice for the architect (see Questions). | Seed "Demo users" | Use `reader` if the architect confirms it can view BOMs. |
| F-16 | Minor | UI-Detail_View-223, 226, 227, 228, 230, 232, 233, 234 | Open-question marking | The file data give the part by name, but R-Part-22 says related fields map by `ID` by default; unlike 221, 222 and 224, these cases do not mark `[open: Q-Detail_View-12, whether the part is given by ID or name]` in Prerequisites. Q-Detail_View-12 is already on their Review field. | concepts-data_import.md#L39-41 | Add the in-cell marker. |
| F-17 | Minor | UI-Detail_View-229 | Fidelity | Cites R-Part-30 (row errors displayed) for a file with no rows; no step checks a row error. | concepts-data_import.md#L104 | Drop R-Part-30 or tie it to an expected message under Q-Detail_View-42. |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Detail_View-209 | 68 | UI-Detail_View-211 | Keep | Just below a multiple vs just above (and 210 on it); different boundary and expected value. |
| UI-Detail_View-210 | 66 | UI-Detail_View-209 / 211 | Keep | On the multiple (no rounding) vs below / above. |
| UI-Detail_View-211 | 68 | UI-Detail_View-209 | Keep | Just above (11 to 15) vs just below (9 to 10). |
| UI-Detail_View-214 | 51 | UI-Detail_View-218 | Keep | All substitutes active vs one inactive; different expected outcome. |
| UI-Detail_View-215 | 67 | UI-Detail_View-047 | Keep | Several substitutes with stock only on the second ("any of the substitute parts") vs a single substitute. |
| UI-Detail_View-217 | 55 | UI-Detail_View-050 | Keep | Two substitutes to one (remaining still counted, 8) vs one to none (5). |
| UI-Detail_View-218 | 51 | UI-Detail_View-214 | Keep | Inactive substitute starting state; different question (Q-Detail_View-44). |
| UI-Detail_View-221 | 74 | UI-Detail_View-057 | Keep | Excel vs CSV input class of R-Detail_View-61. |

Judgement lines written after each case's Duplicate check line.

## Questions for the architect

1. Can the demo user `reader` view the *BOM* tab and a line's available quantity? If yes, the view-only cases (201, 202, 203, 214, 218) could use `reader` (F-15); the docs give no permission for viewing BOMs.
2. Which least-privileged demo user can view a Build Order's required quantities (206 to 212) and allocate stock (215, 216)? The cases use `allaccess`; `engineer` ("partsonly") presumably lacks build permissions, but the docs do not say.
3. For R-Detail_View-53 (F-02): do you read "the required quantity" as the build total (line quantity x build quantity, then rounded), so that 209 to 211 may state `10`/`10`/`15` as fact? If so, F-02 can be closed by answering Q-Detail_View-41.
