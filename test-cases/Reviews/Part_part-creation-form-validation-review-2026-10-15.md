# Review: Part creation form validation (UI), 2026-10-15

**Cases reviewed:** UI-Part-042, UI-Part-043, UI-Part-044, UI-Part-045, UI-Part-046, UI-Part-047, UI-Part-048, UI-Part-049, UI-Part-050, UI-Part-051, UI-Part-052, UI-Part-053, UI-Part-054, UI-Part-055, UI-Part-056, UI-Part-057, UI-Part-058, UI-Part-059, UI-Part-060, UI-Part-061, UI-Part-062, UI-Part-063, UI-Part-064 (all in `test-cases/Part_Creation_and_Import/part-creation-form-validation.md`) · **Verdict:** Changes required

## Coverage

`python tools/coverage_check.py --area Part --area REV --file test-cases/Part_Creation_and_Import/part-creation-form-validation.md`: Rules: 56 · covered: 7 · not cited by any case: 49 · exit code 0 (no unknown rule IDs).

| Rule | Cases | Gap / Out of scope / Covered | Depth issues |
|---|---|---|---|
| R-Part-05 (form errors block submit) | 042, 043, 044, 045, 046, 062, 063, 064 | Covered | Negative (042, 043, 064) and fix-then-submit (062) present. None. |
| R-Part-06 (redirect after submit) | 062 (also asserted in 059, 064) | Covered here; primary coverage in the creation-flow cases | None |
| R-Part-12 (IPN not required) | 048, 054, 055, 056, 057, 058, 064 | Covered | Empty IPN is in UI-Part-001 (outside this set). Boundary 100/101 present. |
| R-Part-13 (Name unique) | 047, 048, 049, 050, 063 | Covered | Negative present (047). No case for a Name that differs from an existing one only by leading/trailing spaces (Q-Part-14 asks about trimming); optional, see Questions. |
| R-Part-14 (Description) | 051, 052, 053 | Covered | Empty, 250, 251 present. |
| R-Part-15 (Revision optional) | 049, 059 | Covered by citation; the empty-Revision case itself is UI-Part-001 / UI-REV (R-REV-05) | 059 cites R-Part-15 but fills Revision (Minor, finding 14). |
| R-REV-03 (Revision any string) | 049, 059, 060, 061 | Covered | 100/101 present. |
| R-Part-01 to R-Part-04 | none | Out of scope: create entry point, menu, permission, opening the form (Part creation flow functionality) | |
| R-Part-07, R-Part-08 | none | Out of scope: initial stock functionality | |
| R-Part-09, R-Part-10 | none | Out of scope: supplier information section | |
| R-Part-11 | none | Out of scope: API / other creation channels | |
| R-Part-16, R-Part-17 | none | Out of scope: Keywords and Link are not named in this functionality (covered by UI-Part-004). See Questions on an invalid-Link negative case. | |
| R-Part-18 to R-Part-41 | none | Out of scope: import from file, update import, supplier import | |
| R-REV-01, R-REV-02, R-REV-04 to R-REV-15 | none | Out of scope: Revisions functionality (R-REV-05 covered in `test-cases/Revisions/part-revisions.md`) | |

No gap among the rules in scope. The functionality has Negative cases (042, 043, 045, 047, 053, 055, 057, 058, 061, 063, 064).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | UI-Part-045 step 2 | No assumptions / Rule outcome stated | "No part is created (R-Part-05)" is written as fact. R-Part-05 says only that a form with errors cannot be submitted; it does not say a 101-character Name is an error. The docs state no length limit, and Q-Part-15 itself lists "one over is rejected" as a *Proposed* outcome. The sibling UI-Part-044 correctly labels its outcome Proposed. | R-Part-05 ([part-create.md#L31](../../requirements/docs/part-create.md#L31)); index Not in docs 9; Q-Part-15 ("Proposed: exactly the limit is accepted, one over is rejected") | Edit to `Proposed, to confirm in Q-Part-15: no part is created. Open: Q-Part-15 (...)`. |
| 2 | Blocker | UI-Part-053 step 2 | No assumptions / Rule outcome stated | Same as #1 for Description at 251 characters. Also cites R-Part-05, which is not in the case's Requirement field (R-Part-14 only). R-Part-14 inventory note: "max length, not stated". | R-Part-14 note; Q-Part-15 | Relabel as Proposed (Q-Part-15); add R-Part-05 to Requirement or drop the citation. |
| 3 | Blocker | UI-Part-055 step 2 | No assumptions / Rule outcome stated | Same as #1 for IPN at 101 characters; R-Part-05 cited in the Expected result but not in the Requirement field (R-Part-12 only). | R-Part-12 ([part-views.md#L30](../../requirements/docs/part-views.md#L30)); Q-Part-15 | Relabel as Proposed (Q-Part-15); align the Requirement field. |
| 4 | Blocker | UI-Part-061 step 3 | No assumptions / Rule outcome stated | Same as #1 for Revision at 101 characters. R-REV-03 says the Revision "can be any string" and its inventory note says "Max length not stated"; R-Part-05 is cited but not in the Requirement field. | R-REV-03 ([part-revision.md#L29](../../requirements/docs/part-revision.md#L29)) and note; Q-Part-15 | Relabel as Proposed (Q-Part-15); align the Requirement field. |
| 5 | Minor | UI-Part-045, 053, 055, 061 Summary and title | Fidelity | Titles and Summaries state "is not accepted / is not saved" as fact, while the outcome is a proposal under Q-Part-15. Same for UI-Part-043 ("Whitespace-only Name is not accepted", Q-Part-14 proposal). | Q-Part-14, Q-Part-15 | Optional rewording once the questions are answered. |
| 6 | Minor | UI-Part-048, UI-Part-049 | Technique / Type | Type is Positive, but the outcome depends on Q-Part-16, and the literal rule ("Name is a simple (unique) text label") would reject the case. The Proposed acceptance is backed in the Notes by finding F-04, an app observation. Correctly labelled Proposed, so not a defect of marking; see Questions. | R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32)); index doc issue 2; Q-Part-16 | Architect decides the reading in Q-Part-16; then fix Type. |
| 7 | Minor | UI-Part-050 | Technique / Type | Type Positive, but the Proposed outcome is that the part is not created (a negative outcome). | Q-Part-16 | Set Type to Negative, or align with the Q-Part-16 answer. |
| 8 | Minor | UI-Part-057 | Technique / Type | Type Negative, but the Proposed outcome is that the part is created with an empty IPN (a positive outcome). | Q-Part-14 | Set Type to match the proposal or the answer. |
| 9 | Minor | UI-Part-058 | Fidelity | Cites R-Part-12 ("IPN is not required"), which says nothing about IPN uniqueness; the behaviour under test has no rule (index Not in docs 1). Correctly marked Proposed with Q-Part-17. The note "If the app accepts, record a finding" presumes the proposal is the requirement; with no rule, acceptance is an answer to Q-Part-17, not a finding, until the architect decides. | R-Part-12; index Not in docs 1; Q-Part-17 | Reword the note after Q-Part-17 is answered. |
| 10 | Minor | UI-Part-046 | Fidelity | Cites R-Part-05 (form errors) for a "special characters accepted" check; the nearer rule is R-Part-13 (Name is a text label). | R-Part-05, R-Part-13 | Adjust the Requirement field. |
| 11 | Minor | UI-Part-060 step 1, UI-Part-061 step 1 | Specific Expected results | Expected result is only an `[open: ...]` marker, with no observable outcome; UI-Part-059 step 1 states "The form shows a Revision field [open: Q-Part-19 ...]". UI-Part-060 also has no detail-page check that all 100 characters were saved, unlike UI-Part-044/052/054. | Q-Part-19 | Align with UI-Part-059 step 1; add a detail-page check step to UI-Part-060. |
| 12 | Minor | UI-Part-064 step 1 | Open-question marking | "The fields show the values" for a 101-character IPN, but Q-Part-15 asks whether input is limited to 100 characters (UI-Part-045/055 step 1 mark this). If input is truncated, step 3's outcome changes too. | Q-Part-15 | Add the Q-Part-15 proposal to step 1. |
| 13 | Minor | UI-Part-042 step 3, Postconditions | No assumptions | Checks that no part exists by searching the *Parts* view for the Description text. The docs do not state that Parts search matches Description. | none in docs | Search by a unique Name the case would have used, or mark the search scope as open. |
| 14 | Minor | UI-Part-059 | Fidelity | Cites R-Part-15 ("Revision is optional") but fills Revision; optionality is not tested here (Notes point to UI-Part-001, which does not assert an empty Revision). | R-Part-15; UI-Part-001 in `part-creation-flow.md` | Drop R-Part-15 from 059, or rely on UI-REV coverage of R-REV-05. |
| 15 | Minor | UI-Part-044 Postconditions | Seed format | "one new part `with the 100-character name` exists": code formatting around prose. | Seed | Cosmetic edit. |
| 16 | Minor | UI-Part-047 to 050, 042 to 064 Requirement | Seed format | Every case cites `components.schemas.Part.name` in the Requirement field even where the rule is about Description, IPN or uniqueness only (e.g. 047, 050, 063); harmless but noisy. | Seed Requirement field | Optional cleanup. |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Part-044 | 50 | UI-Part-045 / UI-Part-054 | Keep | Boundary side differs from 045 (100 accepted vs 101 rejected); field and rule differ from 054 (Name vs IPN). |
| UI-Part-045 | 55 | UI-Part-055 | Keep | Field and rule differ (Name, R-Part-05 vs IPN, R-Part-12); boundary side differs from 044. |
| UI-Part-054 | 51 | UI-Part-055 | Keep | Boundary side and outcome differ (100 accepted vs 101 rejected); field differs from 044. |
| UI-Part-055 | 55 | UI-Part-045 | Keep | Field and rule differ (IPN vs Name); boundary side differs from 054. |
| UI-Part-060 | 63 | UI-Part-061 | Keep | Boundary side and outcome differ (100 accepted vs 101 rejected). |
| UI-Part-061 | 63 | UI-Part-060 | Keep | Boundary side and outcome differ (101 rejected vs 100 accepted). |

## Questions for the architect

1. **Is the schema's `required` on `name` a requirement for UI cases?** UI-Part-042, 062 step 1 and 064 step 2 state as fact (citing R-Part-05) that an empty Name blocks submit. R-Part-05 does not say which fields are required (inventory note; index Not in docs 9; Q-REV-05 still open), but the cases also cite the schema (Schema issue 4: `name` is the only input-required field). If schema-required counts for UI, these are fine; if not, they need the same Proposed relabel as findings 1 to 4. The same decision bears on whether the schema's maxLength values can be stated as fact (findings 1 to 4).
2. **Q-Part-16 / doc issue 2:** the proposed reading (uniqueness on Name+IPN+Revision, so UI-Part-048 and 049 are accepted) comes from app observation F-04 and contradicts the literal doc text "Name ... (unique)". Which reading do you adopt? It decides the Expected results and Type of UI-Part-048, 049, 050.
3. **Invalid Link:** the inventory note on R-Part-17 records that an invalid URL is rejected with "Enter a valid URL.", which is a form error that blocks submit. No case anywhere tests it. Should it be added to this functionality (form errors) or to the Part fields functionality?
4. **Leading/trailing whitespace:** Q-Part-14 asks about trimming in Name, IPN, Description and Revision, but only whitespace-only Name and IPN have cases. Do you want a case for a Name equal to an existing Name plus a trailing space (a uniqueness bypass risk), and for whitespace-only Revision/Description?
