# Review: Part detail view Stock tab (UI), 2026-10-15

**Cases reviewed:** UI-Detail_View-601 to UI-Detail_View-624 (24 cases, `test-cases/Part_Detail_View/part-detail-view-stock-tab.md`) · **Verdict:** Approve with changes

## Coverage

`coverage_check.py --area Detail_View --file test-cases/Part_Detail_View/part-detail-view-stock-tab.md`: Rules: 70 · covered: 7 · not cited by any case: 63 · exit 0 (every cited rule ID exists; the cross-Area IDs R-ATT-02 and R-ATT-03 cited by UI-Detail_View-618 are in `Attributes/requirements-inventory.md`).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Detail_View-09 (Stock tab lists all stock items with quantity, location, status) | 601, 602, 604, 609, 616, 617, 618 | Covered | Positive, empty, permission (reader, noaccess) and Virtual cases present. No case checks that stock items of another part are not listed ("for the part"), or what a template part's tab shows for its variants' stock (finding 13, question 1). |
| R-Detail_View-10 (Export: options dialog, file with all the part's stock items) | 605, 606, 607 | Covered | Positive, cancel and zero-item cases present. File content is not checked for exclusion of another part's stock (finding 13). |
| R-Detail_View-11 (New Stock Item opens a dialog to create a stock item) | 608, 609, 610, 611, 612, 613, 616, 624 | Covered | Positive, empty, cancel, negative and non-numeric cases, plus reader. No case for quantity `0`, the on-boundary value next to 612's `-1` (finding 12). The rule states no limit, so this is not a required boundary set. |
| R-Detail_View-12 (Stock actions enabled when items are selected) | 614, 615, 616 | Covered | Selected, none selected and cleared selection cases present. |
| R-Detail_View-13 (Total stock is the sum of all stock items) | 603, 604, 609, 624 | Covered | Several items, an added item, a single item and an increase are covered. A total of 0 for a part with no stock is not checked (602 opens the tab only) (finding 11). |
| R-Detail_View-14 (below minimum: "low stock") | 619, 620, 621, 624 | Covered | Below (15/16), on (15/15, open Q-63) and above (15/10) are present, plus the flag clearing (624). |
| R-Detail_View-15 (exceeds maximum: "overstocked") | 621, 622, 623 | Covered | Above (15/14), on (15/15, open Q-63) and below (15/20) are present. |
| R-Detail_View-01 to R-Detail_View-08 | none | Out of scope | Header and details, image, notes, Variants tab (header and tab visibility functionality). |
| R-Detail_View-16 to R-Detail_View-28 | none | Out of scope | Allocated, BOM, Build Orders, Used In, Pricing, Suppliers, order tabs, Stock History: other tabs. R-Detail_View-28 (*Stock History*) is a separate tab, not the *Stock* tab. |
| R-Detail_View-29 to R-Detail_View-39 | none | Out of scope | Test Templates and Test Results tabs. |
| R-Detail_View-40 to R-Detail_View-49 | none | Out of scope | Related Parts and Attachments tabs. |
| R-Detail_View-50 to R-Detail_View-70 | none | Out of scope | BOM tab. |

No rule in scope is uncovered. Negative cases are present (606, 610, 611, 613, 615, 616, 617, 618, 621). There are no API `{id}` operations in this UI scope.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Major | UI-Detail_View-624 | Open-question marking | Step 3 expects "The total stock is 20" on the detail page. Where the total is shown and under which label is open in Q-Detail_View-56, but the case is marked only Q-58 and Q-62. 603, 604 and 609 mark Q-56 for the same check. Q-56's Affected cases column does not list 624 either. | R-Detail_View-13; Q-Detail_View-56 ("Where is the part's total stock shown on the detail page (label)") | Add Q-Detail_View-56 to 624's Review field and to step 3 (`Open: Q-Detail_View-56 (where the total is shown)`). Add 624 to Q-56's Affected cases. |
| 2 | Minor | UI-Detail_View-604 | Seed format | Step 3 cites R-Detail_View-09, but the Requirement field gives only R-Detail_View-13. | Steps table, step 3 | Add R-Detail_View-09 and its source link to Requirement. |
| 3 | Minor | UI-Detail_View-624 | Seed format | Step 2 cites R-Detail_View-11, but the Requirement field gives only R-14 and R-13. | Steps table, step 2 | Add R-Detail_View-11 and its source link to Requirement. |
| 4 | Minor | UI-Detail_View-604 | Specific Expected results | Step 1 is a setup action through the API (`POST /api/stock/` as `admin`) with the vague expected result "The item is created." It is not a UI behaviour under test. | Seed: Expected results are "observable and specific" | Move the stock creation into the step as a stated pre-condition, or state the observable result (the new item's quantity 7 returned). |
| 5 | Minor | UI-Detail_View-601 | Specific Expected results | The test data does not name the status of either stock item (item 2 has only "a different status"), so steps 2 and 3 expect "the item's status" without a value to check. The wording can stay open (Q-56), but the status set at creation should be named. | R-Detail_View-09 ("status of each Stock Item", part-views.md#L58) | Name the status of each item in Prerequisites (for example the default status for item 1 and one other status for item 2). In steps 2 and 3, expect that status, with the wording left open in Q-56. |
| 6 | Minor | UI-Detail_View-602 | Rule outcome stated | The only expected result is a `Proposed` outcome. R-Detail_View-09 does state the outcome for zero items: the tab lists all (here, no) stock items. The Summary states "shows no stock rows" as fact. | R-Detail_View-09 | Expected: "No stock item rows are listed (R-Detail_View-09). Open: Q-Detail_View-56 (empty-state text)." |
| 7 | Minor | UI-Detail_View-616, UI-Detail_View-617 | No assumptions | The Summaries state permission behaviour as fact ("has no working *New Stock Item* or stock actions", "cannot see the part's stock items"), but every expected result is `Proposed` under Q-Detail_View-60. No source states the permission. | Q-Detail_View-60 (Open) | Reword the Summaries as checks ("... is checked for ..."), or mark them proposed. |
| 8 | Minor | UI-Detail_View-616 | Open-question marking | Step 2 looks for *New Stock Item*, whose label is open in Q-Detail_View-58 (other cases mark `[open: Q-Detail_View-58, control label]`). The case is marked only Q-60. | Q-Detail_View-58 | Add the `[open: Q-Detail_View-58, control label]` marker in step 2 and add Q-58 to the Review field. |
| 9 | Minor | UI-Detail_View-618 | Fidelity, Technique | The case cites R-ATT-02 (a Virtual part cannot have stock items) but never tries to create stock. Step 1 restates the rule as an expected result that looking at the tabs cannot show. The Technique says "State transition (Virtual flag on)", but the part is created Virtual and no transition happens. | R-ATT-02, R-ATT-03 (part-virtual.md#L27) | Drop R-ATT-02 from Requirement and step 1 (it is covered in the Attributes Area), or add a step that checks it. Change the Technique to Decision table only, or add a step that switches the Virtual flag on. |
| 10 | Minor | UI-Detail_View-609, UI-Detail_View-610 | Technique, Seed format | 609's "Exploratory (tab and total)" does not describe a scripted end-to-end check. 610 step 1 gives both `Not known: ...` and a `Proposed` outcome; the seed allows `Not known` only when nothing can be proposed. | Seed, Technique and Expected result rules | 609: use "What-if business scenario" or drop the second technique. 610: keep only the `Proposed` outcome plus `Open: Q-Detail_View-58 (...)`. |
| 11 | Minor | R-Detail_View-13 | Depth | No case checks the total for a part with no stock (0). | part-index.md#L19 | Optional: add a step to 602 or a new case (rerun the creator). |
| 12 | Minor | R-Detail_View-11 / UI-Detail_View-612 | Depth, Technique | 612 is labelled boundary "just below zero" but has no on-boundary partner (quantity `0`). The minimum quantity is open (Q-58). | Q-Detail_View-58 | After Q-58 is answered, add the boundary set (`0`, and the minimum allowed value) by rerunning the creator. |
| 13 | Minor | R-Detail_View-09, R-Detail_View-10 | Depth | "for the part" / "all stock items for this Part": no case puts a second part's stock item next to the part under test to show it is excluded from the tab and the export. | part-views.md#L58, #L68 | Optional: add a stock item of another part to the data of 601 and 605 and expect it to be absent. |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Detail_View-619 | 52 | UI-Detail_View-622 | Keep | Different rule (R-14 vs R-15), setting (minimum vs maximum) and expected flag ("low stock" vs "overstocked"). |
| UI-Detail_View-620 | 55 | UI-Detail_View-623 | Keep | Total equal to the minimum (R-14) vs equal to the maximum (R-15); a different flag. |
| UI-Detail_View-622 | 52 | UI-Detail_View-619 | Keep | Mirror of 619: R-15 above the maximum vs R-14 below the minimum. |
| UI-Detail_View-623 | 55 | UI-Detail_View-620 | Keep | Mirror of 620: equal to the maximum vs equal to the minimum. |

## Questions for the architect

1. R-Detail_View-09 says the *Stock* tab lists "all the stock items for the selected Part". For a Template part, does the tab (and the total stock, R-Detail_View-13) include its variants' stock items? The docs do not say. This may need a new open question in `Part_Detail_View/open-questions.md` and a case.
2. Finding 1 also needs Q-Detail_View-56's Affected cases column updated to include UI-Detail_View-624. Only the architect edits question files.
