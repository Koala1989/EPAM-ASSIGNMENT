# Review: Part Import (UI), 2026-10-13

**Cases reviewed:** UI-Part-026, UI-Part-027, UI-Part-028 · **Verdict:** Approve with changes

Coverage was checked against every case in `test-cases/Part_Creation_and_Import/part-data-import.md` (UI-Part-007 to UI-Part-028), because the three new cases add to the existing Part Import set. The case-by-case checks cover only UI-Part-026 to UI-Part-028.

## Coverage

`coverage_check.py --area Part --file test-cases/Part_Creation_and_Import/part-data-import.md`: Rules: 41 · covered: 21 · not cited by any case: 20 (exit 0, no unknown rule IDs).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Part-01 to R-Part-17 | none | Out of scope (Create Part form and Part fields functionality) | |
| R-Part-18 | UI-Part-007, UI-Part-026 | Covered | |
| R-Part-19 | UI-Part-008 | Covered | Permission depth: only the non-staff user (`engineer`) is tested. No case covers the other blocked combination, a staff user without the Part `change` permission (rule says staff **and** `change`). See finding 5. |
| R-Part-20 | UI-Part-009 | Covered | |
| R-Part-21 | UI-Part-012 | Covered | |
| R-Part-22 | UI-Part-009, UI-Part-010 | Covered | |
| R-Part-23 | UI-Part-011 | Covered | |
| R-Part-24 | UI-Part-007, UI-Part-015 | Covered | |
| R-Part-25 | UI-Part-013 | Covered | |
| R-Part-26 | UI-Part-014 | Covered | |
| R-Part-27 | UI-Part-015 | Covered | |
| R-Part-28 | UI-Part-016, UI-Part-026 | Covered (by UI-Part-016 only; UI-Part-026 does not test this rule, finding 1) | |
| R-Part-29 | UI-Part-017, UI-Part-028 | Covered | Negative missing: no case checks that a *Pending* row is **not** in the database before it is selected and confirmed (UI-Part-017 never checks the Parts list before step 2; UI-Part-028 is about an *Error* row). See finding 4. |
| R-Part-30 | UI-Part-018 | Covered | |
| R-Part-31 | UI-Part-017, UI-Part-018, UI-Part-028 | Covered | |
| R-Part-32 | UI-Part-019 | Covered | |
| R-Part-33 | UI-Part-020 | Covered | |
| R-Part-34 | UI-Part-021 | Covered | |
| R-Part-35 | UI-Part-022, UI-Part-027 | Covered | |
| R-Part-36 | UI-Part-025 | Covered | |
| R-Part-37 | UI-Part-022, UI-Part-023, UI-Part-027 | Covered | |
| R-Part-38 | UI-Part-024 | Covered | |
| R-Part-39 to R-Part-41 | none | Out of scope (Import from Supplier functionality; index "Out of scope": no supplier plugin in the test instance) | |

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Major | UI-Part-026 | Fidelity | Cites `R-Part-28` (server auto-matches columns, user can adjust the mapping), but the case never reaches the mapping step; it tests file-type and empty-file handling at upload, which no inventory rule states. Coverage then counts R-Part-28 as covered by a case that does not test it. Q-Part-04 carries the same rule link. | R-Part-28 = [concepts-data_import.md#L90](../../requirements/docs/concepts-data_import.md#L90); upload step is L78-83 and states no formats. | Cite only `R-Part-18` (the wizard opens) and record "accepted file formats" as a Not in docs item. The architect decides whether to add a rule to the inventory. |
| 2 | Major | UI-Part-026 | No assumptions | The Summary states an outcome ("is handled without creating importable rows"), but the docs do not say this and every step leaves the result as Not known (Q-Part-04). | [concepts-data_import.md#L78-83](../../requirements/docs/concepts-data_import.md#L78-L83) | Reword the Summary so it does not state an outcome, e.g. "...the wizard's response is checked". |
| 3 | Minor | UI-Part-026 | One behaviour | Two invalid classes (unsupported type, empty file) in one case; their outcomes may differ, and a failure in step 2 hides step 3. The test-data wording "a `.txt` file renamed from plain text" is also unclear. | Seed: one behaviour per case. | Split into two cases once Q-Part-04 is answered; describe the file plainly ("plain-text `.txt` file"). |
| 4 | Major | R-Part-29 | Coverage (negative) | Gap: the "must be selected and confirmed" rule has no negative case showing that a *Pending* row is not yet imported. | [concepts-data_import.md#L104](../../requirements/docs/concepts-data_import.md#L104) | Rerun the creator for this negative, or add a step to UI-Part-017 before step 2 that checks the part does not exist yet. |
| 5 | Major | R-Part-19 | Coverage (permission) | Gap: no case for a staff user without the Part `change` permission being refused import. | [concepts-data_import.md#L28](../../requirements/docs/concepts-data_import.md#L28) | Rerun the creator once a suitable demo user is confirmed (see questions). The outcome for the Parts-table entry depends on Q-Part-01; the Admin Center entry does not. |
| 6 | Minor | UI-Part-027 | Seed format / Fidelity | Cites `R-Part-37` without its source link (only L118-130 and L140-145 are linked; R-Part-37 is L134-136). R-Part-37 is only the precondition here (Admin Center update session), not what the case tests. | [concepts-data_import.md#L134-136](../../requirements/docs/concepts-data_import.md#L134-L136) | Drop R-Part-37 or add its link. |
| 7 | Minor | UI-Part-027 | Specific test data | The CSV content is not given (Test data "None"). To check whether `QA-<suffix> Update Target` "is changed", the file needs a row with values that would change it (e.g. the target's name and a new description). The case also conflates "ID column absent from the file" (prerequisite) with "ID column present but left unmapped" (Summary, step 1); these are two classes. | R-Part-35 (L120: file must contain an identifier; L142: `ID` must be mapped) | State the row values. Choose one class, or include an ID column and leave it unmapped so that the case matches its Summary. |
| 8 | Minor | UI-Part-027 | Postconditions | Cleanup does not cover parts that may be created from the rows if the session does not block (the outcome is unknown under Q-Part-05). | Q-Part-05 | Add "delete any `QA-<suffix>` part created from the rows". |
| 9 | Minor | UI-Part-028 | Steps | Step 3 says "Search the *Parts* view" using an empty name, which cannot be searched for. The Expected result checks the category instead. | n/a | Change the action to "Open `QA-<suffix> Category` and check its part list". |
| 10 | Minor | UI-Part-028 | Fidelity | `R-Part-29` is cited, but the case tests the Error-state clause of R-Part-31. Select and confirm is only the action used. | R-Part-31 = [concepts-data_import.md#L108](../../requirements/docs/concepts-data_import.md#L108) | Keep R-Part-31 as the primary rule; R-Part-29 is optional. |

Checks passed for all three cases: seed field order and Steps columns; Review field `Draft · Open question: Q-Part-0N` correct and each question lists the case; Not known parts marked in the right format; Type and Technique labels fit; `admin` is defensible as the user while Q-Part-01 (which user may import) is open.

## Duplicates

No case scored 50 or more (none of UI-Part-026, -027, -028 has a `**Duplicate check:**` line).

## Questions for the architect

1. UI-Part-028 step 1 (and the already approved UI-Part-018) expect an empty Name to put the row in *Error*. The docs do not state which part fields are required (index "Not in docs" item 9). Only the API schema makes `name` input-required (Schema issue 4). Do you accept the schema as the source for this UI expectation, or should it become an open question?
2. Is there a demo user who is staff but lacks the Part `change` permission (perhaps `steven`, "Staff, some admin pages")? Finding 5 needs one.
3. Accepted import file formats (UI-Part-026, Q-Part-04): should this go into the index "Not in docs" table, since no inventory rule covers it?
