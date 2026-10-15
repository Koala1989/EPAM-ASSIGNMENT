# Review: Return Orders, Transfer Orders and Test Results tab visibility (UI), 2026-10-15

**Cases reviewed:** UI-Detail_View-115 to UI-Detail_View-127 (13 cases, `test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md`) · **Verdict:** Approve with changes

## Coverage

`python tools/coverage_check.py --area Detail_View --file test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md`: Rules: 70 · covered: 14 · not cited by any case: 56 · exit 0 (every cited rule ID exists).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Detail_View-26 (Return Orders tab visible only if Salable and feature enabled) | 115, 116, 117, 118 | Covered | All four decision-table columns present. None. |
| R-Detail_View-27 (Transfer Orders tab hidden if Virtual or feature disabled) | 119, 120, 121, 122 | Covered | All four columns present. None. |
| R-Detail_View-30 (Test Results tab shows results of all stock items in one table; visible only if Testable) | 123, 124, 125, 126, 127 | Covered | Visibility: shown, hidden and both transitions present. **Content clause not tested:** no case has test results on two or more stock items and checks they appear together in one table (123 only opens the tab on a part with no stock). See finding 2. |
| R-Detail_View-29 (Testable part: tests can be defined; Test Templates tab) | none | Out of scope | Test templates functionality, not this tab-visibility request. |
| R-Detail_View-01 to -25, -28, -31 to -70 | 080 to 114 or none | Out of scope | Header, other tabs, test templates, related parts, attachments, stock and BOM functionalities of the same Area. |

No functionality-level Negative gap: 116, 117, 118, 120, 121, 122, 124, 125 are Negative.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Major | UI-Detail_View-115 to 127 | Open-question marking | `Q-Detail_View-22` and `Q-Detail_View-23` are each defined **twice** in `open-questions.md`: rows 26-27 (BOM tab contents / quantity calculations) and rows 31-32 (this functionality). The cases' `Draft · Open question: Q-Detail_View-22/23` marks and every inline `Open: Q-Detail_View-22/23` are therefore ambiguous. Rows 26-27 also list UI-Detail_View-115 to 117 and 120 to 127 as affected by BOM-table and BOM-quantity questions that have nothing to do with these cases. Rows 28-30 (Q-24 to Q-26) likewise cite UI-Detail_View-118, 119, 130 to 148, i.e. IDs that are either these tab cases or do not exist (the Area has cases 001 to 127 only). | `test-cases/Part_Detail_View/open-questions.md` rows Q-Detail_View-22/23 (lines 26-27 and 31-32) | Architect: renumber one pair of the duplicate questions (and correct the Affected cases column); then update the Review field and inline `Open:` references of the affected cases to the new IDs (rerun the creator or edit). |
| 2 | Major | R-Detail_View-30 | Coverage depth | The first clause, "shows results from all the part's stock items in one table", has no case with real data. 123 checks an empty table only. Missing: a Testable part with two stock items, a test result recorded on each, and both results listed in the single *Test Results* table. | [part-views.md#L134](../../../requirements/docs/part-views.md#L134), R-Detail_View-30 | Rerun the creator for this case. |
| 3 | Minor | UI-Detail_View-127 | Technique / Automation | Technique is `Negative (view-only user)` but the case is Type Positive and expects the tab shown; it is an equivalence class of user (e.g. `Equivalence partitioning (view-only user class)`). Automation says "the edit step needs Q-Detail_View-23 answered" but the case has no edit step; the partial reason is the Proposed outcome. | Case 127 fields | Edit Technique and Automation reason. |
| 4 | Minor | UI-Detail_View-118, UI-Detail_View-122 | Seed format (prerequisites/postconditions) | Prerequisites require the feature disabled but no step or pre-step disables it (117 and 121 do it in step 1); Postconditions say "no records changed" and then "Restore the setting as `admin` if it was changed", which is contradictory. | Cases 118, 122 | Add the disabling action as a pre-step (as `admin`) and state the restore in Postconditions unconditionally. |
| 5 | Minor | UI-Detail_View-115 to 126 | User | `allaccess` is not the least-privileged user. For 123 to 126 (Testable tab, editing a part) `engineer` is the seed's default Parts user and can edit parts. For 115 to 122 `allaccess` may be deliberate (the Return/Transfer Orders tabs may need order view permission, as the *Suppliers* tab does in 1.5.6, index doc issue 15), but the cases do not say so. | Seed "Demo users"; index doc issue 15 | Use `engineer` for 123 to 126, or note why `allaccess`; see question 3 for 115 to 122. |

No Blocker. Expected results are specific to what the rules state; unknowns (setting names, edit control, reload behaviour) are marked with `Open:` / `[open: ...]` after the rule's outcome. The Proposed outcome in 119 and 127 is labelled.

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Detail_View-116 | 71 | UI-Detail_View-118 | Keep | Settings differ (feature enabled vs disabled). |
| UI-Detail_View-117 | 52 | UI-Detail_View-118 | Keep | Starting state differs (Salable on vs off); 121 is another rule and tab. |
| UI-Detail_View-118 | 71 | UI-Detail_View-116 | Keep | Settings differ from 116; Salable state differs from 117. |
| UI-Detail_View-120 | 72 | UI-Detail_View-122 | Keep | Settings differ (feature enabled vs disabled); Virtual state differs from 121. |
| UI-Detail_View-121 | 51 | UI-Detail_View-120 / 122 | Keep | Feature setting differs from 120, Virtual state from 122; 117 is another rule. |
| UI-Detail_View-122 | 72 | UI-Detail_View-120 | Keep | Settings differ from 120; Virtual state differs from 121. |

Judgement lines written to the case file. Note: 118 and 122 (both conditions false) add little over the single-condition cases; they are real decision-table columns, so Keep, but the architect may drop them by priority (both are P3).

## Questions for the architect

1. **Duplicate question IDs** (finding 1): which pair of Q-Detail_View-22/23 keeps its ID? Do BOM-tab-contents cases with IDs UI-Detail_View-115 to 148 exist anywhere (they are cited by Q-22 to Q-26, rows 26-30, but no such cases are saved apart from the tab-visibility cases reviewed here)? If they were never saved or were overwritten, that functionality needs a rerun with new IDs.
2. **"Only if" as a positive outcome:** 115, 123 and 126 state "the tab is shown" as fact from "visible only if ...", while 119 marks the parallel inference from "hidden if ..." as Proposed. Strictly, neither wording states when the tab is shown. Should all four be stated as fact (common reading), or all marked Proposed?
3. **Permission dependency of Return Orders and Transfer Orders tabs:** like the *Suppliers* tab (doc issue 15), do they need return order or transfer order view permission? No case covers a user without that permission; the docs do not state one, so this is not a gap, but Q-Detail_View-22 (this functionality's row) could ask it.
4. **List content of Return/Transfer Orders tabs:** the doc lines (part-views.md L118, L122) also say the tabs list the return/transfer orders that reference the part. R-Detail_View-26 and -27 keep only the visibility clause, so no case checks the list. Add the clause to the inventory if it should be tested.
