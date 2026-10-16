# Review: Parameter unit validation setting and selection list administration (UI), 2026-10-15

**Cases reviewed:** UI-Part_Params-043 to UI-Part_Params-063 (21 cases, all in `test-cases/Parameters/parameter-unit-validation-and-selection-lists.md`) · **Verdict:** Approve with changes

## Coverage

`coverage_check.py --area Part_Params --file test-cases/Parameters/parameter-unit-validation-and-selection-lists.md`: Rules: 36 · covered: 6 · not cited by any case: 30 · exit 0 (no unknown rule IDs).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Part_Params-32 (unit validation can be disabled, any value accepted) | 043, 044, 045, 046, 047, 048, 049 | Covered | Off x incompatible, off x non-numeric, off x compatible, on x incompatible, off-to-on transition, blocked user, toggle with existing data. Adequate. |
| R-Part_Params-31 (incompatible units rejected) | 046, 047 | Covered (baseline; primary coverage is UI-Part_Params-034 in the other functionality) | None. |
| R-Part_Params-36 (selection lists administered in Admin Center *Parameter* section or API) | 050-060, 062 | Covered | View, create, edit (add entry), delete unused, delete used, empty / whitespace / duplicate / special names, blocked users (062). The "or via the API" clause is not exercised; out of scope for a UI functionality. |
| R-Part_Params-09 (selection-list template accepts only list values) | 056, 057, 061 (and 060 step 2 without citing it) | Covered | Negative counterpart is UI-Part_Params-016 (other functionality). |
| R-Part_Params-34 (Choices limited to 5000; selection lists overcome it) | 060 | Covered | The 5000/5001 Choices boundary is in UI-Part_Params-012/013 (other functionality); 060 tests the "overcome" clause with 6000 characters. See finding 4. |
| R-Part_Params-35 (plugins can lock selection lists) | 063 | Covered | Not executable until Q-Part_Params-17 is answered. |
| R-Part_Params-01 to -08, -10 to -30 (except those above), -33 | None | Out of scope | Parameters tab, templates, Choices/Checkbox, uniqueness, category parameters, parametric tables, unit conversion and sorting: functionality "Part parameters tab, parameter templates and category parameters" (`parameters-tab-templates-and-category-parameters.md`). |

No gap. Negative cases exist (046, 047, 048, 052, 053, 054, 057, 059, 062, 063); permission cases exist for both the setting (048) and selection-list administration (062).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Major | UI-Part_Params-060 | Seed format / Open-question marking | Step 2 adds a parameter "using the last entry", but Prerequisites list no template linked to `QA-<suffix> Big` and no part, and step 2 Test data gives no template. Step 2's Expected result cites R-Part_Params-09, which is not in the Requirement field, and the Data control for a selection-list template (Q-Part_Params-06) is not marked in the Review field. The step cannot be run as written. | Case lines: Prerequisites "Data: 60 entries of 100 characters"; step 2 "Data: entry 60"; R-Part_Params-09 ([concepts-parameters.md#L40](../../requirements/docs/concepts-parameters.md#L40)) | Edit the case: add the template linked to the list and the part to Prerequisites, the template to step 2 Test data, R-Part_Params-09 to Requirement, Q-Part_Params-06 to Review; or move step 2 into a separate case. |
| 2 | Major | UI-Part_Params-063 | Specific Expected results | The only Expected result is "Plugins can lock selection lists (R-Part_Params-35)", which restates the rule and is not an observable outcome of "Try to edit and delete the locked list". The Summary and title state "changes are blocked", which the Expected result does not. | R-Part_Params-35 ([concepts-parameters.md#L199](../../requirements/docs/concepts-parameters.md#L199): "lock selection lists to ensure a known state") | Edit step 1's Expected result to an observable outcome, e.g. `Proposed, to confirm in Q-Part_Params-17: the list cannot be edited or deleted, and is shown as locked.` Consider splitting edit and delete into two steps. |
| 3 | Minor | UI-Part_Params-050 to 060, 062 | Seed format | Requirement link text says `#L195-L202` but the link target is `#L202`. | All cited R-Part_Params-36 links | Make the label and anchor agree (inventory source is L202). |
| 4 | Minor | UI-Part_Params-060 | Technique | Technique says `Boundary value analysis (5001+ characters via list)` but data is 6000 characters, not on or just above the boundary; this is a representative value of the "over limit" class. | R-Part_Params-34 | Relabel as `Equivalence partitioning (over 5000 characters via list)`, or use 5001 characters if the boundary is intended. |
| 5 | Minor | UI-Part_Params-044 | Open-question marking | Expected result opens "whether `any parameter value` includes non-numeric text" against Q-Part_Params-14, but Q-Part_Params-14 does not ask this, and R-Part_Params-32 says any value is accepted. | R-Part_Params-32 ([concepts-parameters.md#L187](../../requirements/docs/concepts-parameters.md#L187)); Q-Part_Params-14 text | Drop that open note, or add the sub-question to Q-Part_Params-14. |
| 6 | Minor | UI-Part_Params-056 | User | Prerequisite user is `admin` for the whole case, but step 2 (adding a part parameter) can be done by `engineer`. | Seed: least-privileged user | Run step 1 as `admin` and step 2 as `engineer` (as 047 does). |
| 7 | Minor | UI-Part_Params-061 | Seed format | Data `list QA-<suffix> List (A,B)` and the linked template do not say how they are created (016 says "via API as `admin`"). Cleanup does mention the list. | Seed: Data "how they are created" | Add "created via API as `admin`". |
| 8 | Minor | UI-Part_Params-051 | No assumptions | Step 1 "A form opens" is stated as fact; the docs only say lists are administered in the section. Low risk; the labels are already marked open. | R-Part_Params-36 | Optionally phrase as Proposed under Q-Part_Params-15. |
| 9 | Minor | UI-Part_Params-046 | One behaviour / duplicate | Same check as UI-Part_Params-034 and as UI-Part_Params-047 step 3. See Duplicates. | R-Part_Params-31 | Act on the Merge verdict. |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Part_Params-043 | 54 | UI-Part_Params-044 | Keep | Incompatible unit (`5 V`) vs unparseable text (`abc`); vs 045, incompatible vs compatible unit. |
| UI-Part_Params-044 | 54 | UI-Part_Params-043 | Keep | Non-numeric text class vs valid quantity in an incompatible unit. |
| UI-Part_Params-045 | 50 | UI-Part_Params-043 | Keep | Compatible-unit column vs incompatible-unit column with validation off. |
| UI-Part_Params-046 | 56 | UI-Part_Params-034 | Merge into UI-Part_Params-034 | Same rule, user, data and rejection outcome with validation on in both; carry over the explicit `unit validation = on` prerequisite, the R-Part_Params-32 citation and the setting-restore cleanup. |
| UI-Part_Params-052 | 53 | UI-Part_Params-053 | Keep | Empty name vs whitespace-only name. |
| UI-Part_Params-053 | 53 | UI-Part_Params-052 | Keep | Whitespace-only name vs empty name. |

## Questions for the architect

1. UI-Part_Params-048 and 062 test `reader` and `engineer` as blocked users. The demo user `steven` is staff with "some admin pages"; should `steven` also be checked for the unit validation setting and the Admin Center *Parameter* section? The docs state no permission for either (Q-Part_Params-14, Q-Part_Params-15).
2. No case links a template to a selection list through the UI (all cases do it in Prerequisites). Q-Part_Params-15 already asks for the template's link label. Should a UI case for setting a template's Selection List be added once that is answered, and in which functionality?
3. The default state of the unit validation setting is unknown (index doc issue 8, Q-Part_Params-14). If it defaults to off, UI-Part_Params-034 (which assumes on with `Settings: None`) would fail; this is why the Merge of 046 into 034 should carry the explicit setting over.
