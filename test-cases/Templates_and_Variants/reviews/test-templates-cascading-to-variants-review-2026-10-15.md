# Review: Test templates cascading from a template part to its variants' stock items (UI), 2026-10-15

**Cases reviewed:** UI-Part_Template-036, UI-Part_Template-037, UI-Part_Template-038, UI-Part_Template-039, UI-Part_Template-040, UI-Part_Template-041, UI-Part_Template-042, UI-Part_Template-043, UI-Part_Template-044 · **Verdict:** Changes required

## Coverage

`coverage_check.py --area Part_Template --file test-cases/Templates_and_Variants/template-parts-and-variants-tab.md`: Rules: 11 · covered: 11 · not cited by any case: 0 (exit 0). The cases also cite R-Detail_View-29, R-Detail_View-30 and R-Detail_View-39, which exist in `Part_Detail_View/requirements-inventory.md`.

| Rule | Cases (this batch) | Status | Depth issues |
|---|---|---|---|
| R-Part_Template-08 (test templates cascade to variants and their stock items) | 036, 037, 038, 039, 040, 041, 042, 043, 044 (also 028, UI-Detail_View-330 to 333) | Covered | Both clauses covered: variants (036, 039) and variants' stock items (040). Negative direction covered (038; master side also in UI-Detail_View-332). Blocked user covered (043). No rule states a limit, so no boundary case is required. |
| R-Detail_View-30 (Test Results tab shows results of all the part's stock items) | 040 | Covered (in a cross-functional step) | Outcome written as Proposed although the rule states it (finding 5). |
| R-Detail_View-39 (deleting a template deletes its results) | 041 | Covered | 041 has no result in its data, so the "results deleted" clause is not observable (finding 8). |
| R-Detail_View-29 | 044 | Covered | None. |
| R-Detail_View-31 (test name unique across a set of variants; Part_Template cross-reference) | None in this batch | Out of scope: Detail_View, covered by UI-Detail_View-313 | None. |
| R-Part_Template-09 (Inherited BOM lines) | 037 (cited) | Out of scope: BOM inheritance functionality (cases 029 to 035) | 037 cites it, but does not test it (finding 2). |
| R-Part_Template-04 | 039 (cited, as the way the variant is created) | Out of scope: Variants tab functionality (cases 008 to 018) | None. |
| R-Part_Template-01 to 03, 05 to 07, 10, 11 | None in this batch | Out of scope: template flag, Variants tab, serials, stock and BOM functionalities | None. |

No gap. The batch includes Negative cases (038, 041, 043, 044).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | UI-Part_Template-040 | User | The Prerequisites give `engineer` "(part management, view and change stock)", and step 2 adds a stock test result. The project's user data gives `engineer` "Manage parts, view stock" only. Run as written, step 2 would probably fail for permission reasons and look like an app finding. | `automation/data/users.local.json` (engineer role); seed "Demo users" (engineer = part management) | Use the least-privileged user that can change stock (for example `allaccess`), or raise an open question on which demo user can add stock test results. |
| 2 | Major | UI-Part_Template-037 | Fidelity | Cites `R-Part_Template-09` (Inherited BOM lines in variants and sub-variants) in Requirement. The case tests only test templates, so R-09 is not tested. The coverage report wrongly counts 037 as covering R-09. The sub-variant wording in R-09 is context for the proposal, not a requirement of this case. | R-Part_Template-09 ([manufacturing-bom.md#L80](../../../requirements/docs/manufacturing-bom.md#L80)) vs [part-test.md#L19](../../../requirements/docs/part-test.md#L19) | Keep only `R-Part_Template-08` in Requirement and move the R-09 reference to Notes. |
| 3 | Major | UI-Part_Template-037 | Open-question marking | The prerequisite data makes `Variant A` a template (Template on) with its own sub-variant. Q-Part_Template-03 (may a variant become a template with its own sub-variants?) and Q-Part_Template-07 (are sub-variants allowed?) leave this open, but the case is not marked with either. | [open-questions.md](../open-questions.md) rows Q-Part_Template-03, Q-Part_Template-07 | Add Q-Part_Template-03 (and Q-Part_Template-07) to Review, with an `[open: ...]` marker on the sub-variant data. Add 037 to those questions' Affected cases. |
| 4 | Major | UI-Part_Template-039 | Open-question marking | Steps 1 and 2 send "whether the new variant is Testable (so the tab is shown)" to Q-Part_Template-02. That question asks about the New Variant button and form fields, prefill, errors and navigation, not whether Testable is copied. No open question covers this unknown. Review also lists Q-Part_Template-07, but no step uses it. | Q-Part_Template-02 and Q-Part_Template-07 question text | Raise a question (or extend Q-Part_Template-02) on whether *Duplicate Part* copies Testable to the variant. Remove Q-Part_Template-07, or point a step at it. |
| 5 | Major | UI-Part_Template-040 | Rule outcome stated | Step 3 is written as "Proposed, to confirm in Q-Part_Template-10: the new result is listed". R-Detail_View-30 states the outcome: the *Test Results* tab shows results from all the part's stock items in one table, and the variant is Testable. | R-Detail_View-30, [part-views.md#L134](../../../requirements/docs/part-views.md#L134) | State the outcome as fact (R-Detail_View-30) first, then `Open: Q-Part_Template-10 (labels)`. Step 3 depends on step 2 succeeding. |
| 6 | Minor | UI-Part_Template-040, 041, 042, 043, 044 | Seed format (Data) | The Prerequisites say "Testable variant `QA-<suffix> Variant A`" but omit `variant_of` = the template, which 036 to 038 state. The cases depend on this link. | Seed: Data must name the records and how they are created | Add `variant_of` = the template to each Data clause. |
| 7 | Minor | UI-Part_Template-036 | Technique / Type | Type Boundary and "Boundary value analysis (count of variants = 2)". R-08 states no limit on the number of variants. The doc only says "multiple variants". Two variants is an equivalence class (several variants), not a boundary. | [part-test.md#L19](../../../requirements/docs/part-test.md#L19) | Change to Positive and Equivalence partitioning (class: master with several variants). |
| 8 | Minor | UI-Part_Template-041 | Specific Expected results | Step 1 expects "The template and its test results are deleted (R-Detail_View-39)", but the data creates no test result, so the results clause cannot be observed. | R-Detail_View-39 | Either drop the results clause from step 1, or add a result on a variant stock item to the data and check it is gone. That would also test that R-Detail_View-39 reaches results recorded on a variant. |
| 9 | Minor | UI-Part_Template-038 | One behaviour | Step 1 checks the sibling variant and step 2 checks the master. Step 2 repeats UI-Detail_View-332 (a variant's own template is not on the master). | UI-Detail_View-332 | Consider dropping step 2 and leaving the master direction to UI-Detail_View-332. |
| 10 | Minor | UI-Part_Template-044 | Expected result wording | Step 1 is "Not known" although Q-Detail_View-48 has a proposal (templates are kept when Testable is switched off). The seed allows "Not known" only when nothing can be proposed. Testable is an ATT attribute, so whether `engineer` can switch it off depends on the ATT questions, which are not referenced. | Seed Expected result rule; Q-Detail_View-48 Proposed text | Write `Proposed, to confirm in Q-Detail_View-48: the change is saved and the template part's test templates are kept.` |
| 11 | Minor | UI-Part_Template-036 | Overlap (no Duplicate check line) | Step 1 is the same check as UI-Part_Template-028 (and UI-Detail_View-330). Only step 2 (the second variant) is new. | UI-Part_Template-028 | Consider merging the second-variant step into 028, or keeping 036 as the Smoke case and 028 as its subset. |
| 12 | Minor | Open-question rows | Open-question marking | The Affected cases columns do not list the new cases that cite these questions: Q-Detail_View-45 (036, 041, 042, 043), Q-Detail_View-48 (041, 042, 044), Q-Detail_View-49 (036, 037, 038, 039, 043), Q-Part_Template-02 (039), Q-Part_Template-10 (040 is listed; fine). | `Part_Detail_View/open-questions.md` rows 45 to 49; `Templates_and_Variants/open-questions.md` row 02 | The architect updates the Affected cases columns (the reviewer does not edit question files). |

## Duplicates

No case scored 50 or more (none of 036 to 044 has a `**Duplicate check:**` line). Overlaps without a score line are noted in findings 9 and 11.

## Questions for the architect

1. Which demo user may add a test result to a stock item in 1.5.6? `engineer` is documented as "view stock" only (finding 1).
2. Does the *Duplicate Part* form (New Variant) copy Testable to the new variant? No open question covers this, and UI-Part_Template-039 depends on it (finding 4).
3. Can a variant edit or delete an inherited test template on its own *Test Templates* tab (as `engineer`)? Q-Detail_View-49 asks whether inherited templates are read-only, but no case in this batch tests the editable/read-only state for a permitted user. 043 covers only `reader`. Decide whether a case is wanted once Q-Detail_View-49 is answered.
4. Does a disabled (Enabled = false) template on the master still cascade to variants and their stock items? No source states this. Decide whether to add a question and a case (R-Detail_View-38 with R-Part_Template-08).
