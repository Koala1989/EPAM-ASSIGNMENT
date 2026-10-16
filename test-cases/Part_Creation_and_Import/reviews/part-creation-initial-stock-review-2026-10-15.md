# Review: Part creation initial stock (UI), 2026-10-15

**Cases reviewed:** UI-Part-029, UI-Part-030, UI-Part-031, UI-Part-032, UI-Part-033, UI-Part-034, UI-Part-035, UI-Part-036, UI-Part-037, UI-Part-038, UI-Part-039, UI-Part-040 · **Verdict:** Changes required

No Blockers. The verdict is still Changes required because three Majors (F1, F2, F3) are in what existing cases expect, so they are not covered by "Approve with changes" (that is for Majors such as a missing case). See question 5.

## Coverage

`python tools/coverage_check.py --area Part --area ATT --file test-cases/Part_Creation_and_Import/part-creation-initial-stock.md`: Rules: 70 · covered: 10 · not cited by any case: 60 · exit 0 (every cited rule ID exists; R-ATT-02, -03, -12 and -13 are in `Attributes/requirements-inventory.md`).

| Rule | Cases | Gap / Out of scope / Covered | Depth issues |
|---|---|---|---|
| R-Part-07 (setting on: extra section) | 029, 030, 039, 040 | Covered | On (029), off (030, proposed), on-off-on (040). The section is identified only by Q-Part-08, which 030 and 040 do not mark (F8). In 039 the setting has no effect (F9). |
| R-Part-08 (checking input allows initial stock) | 029, 031-038 | Covered | Checked (031) and unchecked (032). Invalid classes: 0 (033), -1 (034), empty and text (035). No lowest valid value (1) or decimal case (F11). The user without stock permission (Q-Part-12) has no case (question 2). |
| R-Part-03 | 039 | Covered as supporting rule; main coverage is UI-Part-003 (part-creation-flow.md) | Repeats UI-Part-003 (F9). |
| R-Part-04, -05, -06 | 038; 034, 035; 031, 032 | Supporting rules, cited correctly except R-Part-04 in 038 (F7) | None |
| R-ATT-02, R-ATT-03 | 036 | Supporting rules | See F2. |
| R-ATT-12, R-ATT-13 | 037 | Supporting rules | See F3. |
| R-Part-01, -02 | none | Out of scope: Create Part form basics (part-creation-flow.md) | |
| R-Part-09, -10 | none | Out of scope: supplier options | |
| R-Part-11 to R-Part-17 | none | Out of scope: API creation and part fields | |
| R-Part-18 to R-Part-38 | none | Out of scope: import from file and update import | |
| R-Part-39 to R-Part-41 | none | Out of scope: supplier import (plugin) | |
| R-ATT-01, -04 to -11, -14 to -29 | none | Out of scope: Attributes functionality | |

No gap: both in-scope rules (R-Part-07, R-Part-08) have positive and negative cases. Neither rule is a permission or "visible only if" rule, and neither states a limit. The functionality has Negative cases (030, 032, 034, 035, 036, 038, 039).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| F1 | Major | UI-Part-035 | One behaviour | The case tests two invalid classes (empty, then `abc`) on one form, and step 2 only works if step 1 keeps the form open. Step 1 itself leaves open "whether an empty quantity is rejected or ignored". If the empty quantity is ignored, the part is created and the form closes, so steps 2 and 3 cannot run as written. | Q-Part-09; R-Part-05 [part-create.md#L31](../../../requirements/docs/part-create.md#L31) | Edit: split into an empty-quantity case and a non-numeric case, each with its own submit and its own no-part check. |
| F2 | Major | UI-Part-036 step 3 | Specific Expected results / Open-question marking | "Stock-related UI elements are hidden" names no element. R-ATT-03 does not list them, and Q-ATT-08 (and Q-Detail_View-61) ask which ones, but the case is not marked with Q-ATT-08. Also, checking "no stock items" on a page that hides stock elements cannot be observed. This same defect was raised as F11 for UI-ATT-005 in the Attributes review. Step 3 also re-tests R-ATT-03, which UI-ATT-007 already covers. | [part-virtual.md#L27](../../../requirements/docs/part-virtual.md#L27); `Attributes/open-questions.md` Q-ATT-08 | Edit: check for no stock in the global stock list filtered by the part (or drop the step), remove or narrow the R-ATT-03 assertion, and add Q-ATT-08 to Review if it stays. |
| F3 | Major | UI-Part-037 step 2 | Specific Expected results | The Expected result for pressing *Submit* only restates R-ATT-12 ("stock items can be assigned batch or serial numbers"). It does not say whether the part is created, whether the browser is redirected (R-Part-06), or what stock exists. Step 3 is `Not known`. The case has no outcome that can pass or fail. | [part-index.md#L76](../../../requirements/docs/part-index.md#L76), [part-trackable.md#L19-21](../../../requirements/docs/part-trackable.md#L19-L21) | Edit: write step 2 as `Not known: depends on Q-Part-11 (...)` or a `Proposed` outcome, and keep R-ATT-12 for the field check (are batch/serial inputs offered). Consider Type Boundary/Negative, not Positive, while the outcome is open. |
| F4 | Minor | UI-Part-033 steps 2-3 | Rule outcome stated | Both steps are `Not known`, but a cited source proposes an outcome. The InitialStock schema says "If quantity is zero, no stock is added." This is cited by inventory rule R-CRUD-13 and asserted in the approved API-CRUD-005. Under the seed rule, `Not known` is only for cases where nothing can be proposed. | [openapi-parts.yaml#L3723](../../../requirements/openapi-parts.yaml#L3723); `API_Create_Read_Update_Delete/requirements-inventory.md` R-CRUD-13 | Edit, if the architect agrees the schema applies to the UI form (question 1): `Proposed, to confirm in Q-Part-09: the part is created and no stock item is added.` |
| F5 | Minor | UI-Part-033 step 1 | No assumptions | "Fields accept the entry" for quantity 0 asserts that there is no inline validation. That outcome is exactly what Q-Part-09 leaves open. | Q-Part-09 | Edit: drop the assertion or mark it with Q-Part-09. |
| F6 | Minor | UI-Part-029 step 3, UI-Part-030 step 2, UI-Part-038 step 2 | No assumptions | "The form closes and no part is created" on *Cancel* is stated as fact in 029 and 030. No rule states it, and 038 treats the same outcome as `Proposed` under Q-Part-09. The cases are inconsistent. | No rule on Cancel in [part-create.md#L24-33](../../../requirements/docs/part-create.md#L24-L33) | Edit: use the same `Proposed (Q-Part-09)` form in all three, or treat Cancel in 029/030 as cleanup with no Expected result. |
| F7 | Minor | UI-Part-038 Requirement | Fidelity | R-Part-04 ("Selecting *Create Part* opens the form") is not what the case tests. The case tests that cancelling creates nothing, and no rule covers that, so it rests only on Q-Part-09. | [part-create.md#L26](../../../requirements/docs/part-create.md#L26) | Edit: keep R-Part-08 only (or note that no rule states the outcome). |
| F8 | Minor | UI-Part-030, UI-Part-040 Review | Open-question marking | Both cases check whether "the initial stock section" is present. Its title and labels are unknown (Q-Part-08), which 029 marks for the same check. 030 also cites `[open: Q-Part-12]` in Prerequisites, but with the setting off no stock is created, so Q-Part-12 does not affect it (Q-Part-12 does not list 030 either). | Q-Part-08, Q-Part-12 | Edit: add Q-Part-08 to 030 and 040 Review; remove the Q-Part-12 marker from 030. |
| F9 | Minor | UI-Part-039 | One behaviour / Fidelity | R-Part-03 does not depend on the setting. The case repeats the approved UI-Part-003 with only the setting changed, and the setting cannot change the outcome. The Summary says "whatever the setting" but only "on" is run. Citing R-Part-07 adds nothing that is tested. The dedupe score was under 50, so this is not a duplicate verdict. | [part-create.md#L21-22](../../../requirements/docs/part-create.md#L21-L22); UI-Part-003 | Architect: consider removing it, or keeping it only as a setting-on regression of UI-Part-003. |
| F10 | Minor | UI-Part-032 Technique | Technique | "State transition (Create Initial Stock unchecked)" is a decision-table column (setting on x input unchecked), not a transition. | | Edit: `Decision table (setting = on, input = unchecked)`. |
| F11 | Minor | R-Part-08 depth | Coverage depth | The boundary set has 0 (on) and -1 (below) but no lowest valid value (1) and no decimal quantity. The rule states no limit, so this is optional. The API-side limits (10 digits, 5 decimals, R-VAL-18) are API cases. | [openapi-parts.yaml#L3721](../../../requirements/openapi-parts.yaml#L3721) | Optional: rerun the creator for a quantity 1 case. |
| F12 | Minor | UI-Part-034 step 1, UI-Part-036 step 1, UI-Part-038 step 1 | Specific Expected results | The Expected result is only `Open: Q-...` with no observable outcome and no `Not known`/`Proposed` label, as the seed requires. | Seed, Steps column rule | Edit: add the observable outcome (e.g. "the quantity field holds -1") or use `Not known: depends on Q-Part-10 (...)` in 036. |
| F13 | Minor | UI-Part-031 step 2 | Specific Expected results | "An initial quantity of stock can be created" restates the rule. It does not say what is observed after entering the data (fields accept the values, no errors). The actual check is in step 4. | R-Part-08 | Edit: "Fields accept the values, no form errors (R-Part-08). Open: Q-Part-08 (labels)." |

Checked and fine: the seed field order and Steps columns in all 12 cases; Review is `Draft · Open question: ...` throughout; the Requirement fields carry rule IDs and doc links; `Proposed` outcomes are labelled (030, 032, 034, 035, 038, 040); `engineer` with the Q-Part-12 marker is used for stock creation, `reader` for the blocked user (039), and `admin` only for the setting change (040).

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Part-034 | 61 | UI-Part-035 | Keep | Negative quantity (-1, numeric class below the 0 boundary) vs empty and non-numeric classes. |
| UI-Part-035 | 61 | UI-Part-034 | Keep | Empty and non-numeric classes vs a negative number. Splitting 035 (F1) does not change this. |

## Questions for the architect

1. **Quantity 0 (UI-Part-033):** The InitialStock schema says "If quantity is zero, no stock is added" ([openapi-parts.yaml#L3723](../../../requirements/openapi-parts.yaml#L3723)), and the approved API-CRUD-005 relies on it. Does this statement apply to the UI *Create Part* form (which presumably submits the same `initial_stock` object), so that 033 can use it as the proposed outcome? Answering in Q-Part-09 would settle it.
2. **Stock permission (Q-Part-12):** No case covers a user who can create parts but cannot add stock, with the setting on. Should a case be written (marked `Not known`) once Q-Part-12 says whether such a user sees the section, or does the architect consider this out of scope? The same question is open on the API side (Field validation review 2026-10-14, question 1).
3. **Location (Q-Part-08):** R-CRUD-13 and the schema state that `location` is optional (`nullable`) for `initial_stock` ([openapi-parts.yaml#L3724-3728](../../../requirements/openapi-parts.yaml#L3724-L3728)). Can that answer the "is a location required" part of Q-Part-08 for the UI form, or must it be confirmed in the UI?
4. **UI-Part-039:** Keep it next to UI-Part-003 or remove it (F9)?
5. **Verdict rule:** The reviewer's verdict scale has no level for "Majors in existing cases, no Blocker". This review uses Changes required for that situation. Please confirm, or say if Approve with changes was meant.
