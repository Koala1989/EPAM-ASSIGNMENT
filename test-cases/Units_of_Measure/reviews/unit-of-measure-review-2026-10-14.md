# Review: Unit_measure (UI), 2026-10-14

**Cases reviewed:** UI-Unit_measure-001 to UI-Unit_measure-029 (29 cases, `test-cases/Units_of_Measure/unit-of-measure.md`) · **Verdict:** Changes required

## Coverage

`coverage_check.py --area Unit_measure --file test-cases/Units_of_Measure/unit-of-measure.md`: Rules: 18 · covered: 18 · not cited by any case: 0 (exit 0; no unknown rule IDs).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Unit_measure-01 | 001 | Covered | None |
| R-Unit_measure-02 | 002, 003 | Covered | Conflict (doc issue 1) correctly marked Q-Unit_measure-01 |
| R-Unit_measure-03 | 004 | Covered | Only litres; metres is covered indirectly by 005 to 008 data. Acceptable. |
| R-Unit_measure-04 | 005, 006, 008 | Covered | None |
| R-Unit_measure-05 | 007, 008 | Covered | Negative present |
| R-Unit_measure-06 | 009, 010 | Covered | None |
| R-Unit_measure-07 | 011 | Covered | None (rule states only valid values) |
| R-Unit_measure-08 | 012 | Covered | None |
| R-Unit_measure-09 | 013 | Covered | Negative present |
| R-Unit_measure-10 | 014, 015 | Covered | Positive and negative present |
| R-Unit_measure-11 | 016, 017 | Covered | Positive and negative present; starting state missing (finding 9) |
| R-Unit_measure-12 | 018 | Covered (shallow) | The rule's values (12, 100, 1000, dimensionless) are not verified by any observable step (finding 6) |
| R-Unit_measure-13 | 019, 020 | Covered (partial) | The "edit" clause (edit an existing custom unit) is tested by no case (finding 4). The blocked-user case (020) is present, with its outcome open. |
| R-Unit_measure-14 | 021 | Covered (partial) | Only the alias class; the classes "new physical quantity" and "link existing units" have no case (finding 3) |
| R-Unit_measure-15 | 022, 023 | Covered | Positive and negative present |
| R-Unit_measure-16 | 024, 025, 026 | Covered | Negative 026 asserts an unstated outcome (finding 1) |
| R-Unit_measure-17 | 027, 028 | Covered | Positive and negative present |
| R-Unit_measure-18 | 029 | Covered | None |

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | UI-Unit_measure-026 | No assumptions | Step 2 expects "The line is not saved" for raw amount `2 m` on a `kg` part. The rule and docs only say that compatible units are allowed; they do not say an incompatible unit is rejected. The case's own Notes admit the failure is "implied, not stated". Q-Unit_measure-09 asks only for the error text, so it presupposes the rejection rather than settling it. | R-Unit_measure-16; manufacturing-bom.md#L41-43 | Edit the case so the outcome is `Not known: depends on open question ...`, and widen Q-Unit_measure-09 (or add a question) to ask whether an incompatible raw amount is rejected. |
| 2 | Major | UI-Unit_measure-007, 013, 015, 017 | No assumptions / Open-question marking | Each case asserts "is not saved" (and 007 step 2 asserts the prior unit is kept). The docs say only "an error will be displayed" (007) or "not valid" / "not supported" (013, 015, 017). For 013, 015 and 017, Q-Unit_measure-03 itself asks "is the form blocked", so the case asserts the answer to an open question. | part-index.md#L138; concepts-units.md#L43, #L52, #L56; Q-Unit_measure-03 | Edit: keep "an error is shown / value is not valid" and mark the saved-or-not part `[open: Q-Unit_measure-03 ...]` (Q-Unit_measure-04 for 007). |
| 3 | Major | R-Unit_measure-14 | Gap (depth) | The rule names three classes: a new physical quantity, a link between existing units, and an alias. Only the alias class has a case (021). | concepts-units.md#L78 | Rerun the creator for the two missing classes, marked with Q-Unit_measure-07. |
| 4 | Major | R-Unit_measure-13, UI-Unit_measure-019 | Gap (depth) / Fidelity | The rule says custom units are viewed, edited and created in the tab. 019's summary claims all three, but its steps only open the tab. 021 and 022 cover creation; no case edits an existing custom unit. | concepts-units.md#L97 | Rerun the creator for an edit-custom-unit case. Optionally narrow 019's summary to what it checks. |
| 5 | Major | UI-Unit_measure-022 | No assumptions | Step 2 expects the unit to appear in the list "as a dimensionless unit". The docs do not say the list shows a unit's dimensionality. | concepts-units.md#L102-104 | Edit: expect "saved and listed", and mark how dimensionless is shown `[open: Q-Unit_measure-06 ...]` or a new question. |
| 6 | Major | UI-Unit_measure-018 | Fidelity / Specific Expected results | Step 2 restates the meanings (12, 100, 1000, dimensionless) but no step observes them. Even if the units are listed, the case does not show `dozen` = 12. | R-Unit_measure-12; concepts-units.md#L87-93 | Edit or rerun: add an observable use of a built-in unit (for example, a part or raw amount in `dozen` with the resulting quantity). The field and outcome are open (Q-Unit_measure-02 / -06). |
| 7 | Major | UI-Unit_measure-003 | Specific Expected results | Step 2's "Quantities are dimensionless pieces" is not observable: no step shows where or how this would be seen. | R-Unit_measure-02; part-index.md#L120 | Edit: state an observable check (for example, the quantity shows no unit), or mark it open under Q-Unit_measure-01. |
| 8 | Major | UI-Unit_measure-008 | Open-question marking | Step 1's Test data uses `[open: Q-Unit_measure-02, label of the units field]`, but the Review field lists only Q-Unit_measure-04 and Q-Unit_measure-05. Q-Unit_measure-02's Affected cases does not list 008 either. Q-Unit_measure-04 (the supplier unit field label or error) is not referenced in any step. | Q-Unit_measure-02, -04, -05 | Edit the Review field to include Q-Unit_measure-02 (or drop the marker, see finding 13). Update Q-Unit_measure-02's Affected cases. |
| 9 | Major | UI-Unit_measure-011, 012, 013, 016, 017 | Specific Expected results (starting state) | The Data field creates `QA-<suffix> Part` without stating its unit. If the field that accepts units is the BOM raw amount (Q-Unit_measure-02 is open), then by R-Unit_measure-17 `1 kg` is rejected on a part with no unit. 016 would then fail, and 017's `1 KG` rejection would not prove case sensitivity. | R-Unit_measure-11, R-Unit_measure-17; concepts-units.md#L56; manufacturing-bom.md#L45 | Edit: state the part's unit in Data (for example, `kg` for 016 and 017), consistent with 009. |
| 10 | Minor | UI-Unit_measure-025 | Specific Expected results | "The quantity is the equivalent in kg" gives no value. The docs give no lb-to-kg factor, so the value is reasonably left open, but the rounding question does not cover the value itself. | manufacturing-bom.md#L41 | Settled if 025 is merged into 024 (see Duplicates); otherwise see question 3. |
| 11 | Minor | UI-Unit_measure-006 | Specific Expected results | Step 3 says "shows the last unit entered" instead of `inches`. | part-index.md#L136 | Edit: expect `inches`. |
| 12 | Minor | UI-Unit_measure-002, 013, 023 | Technique | 002 "State transition (default state)" has no transition. 013 "Boundary value analysis (`1E3` vs `1e3`)" and 023 "(`1` vs `2`)" are equivalence classes, not boundaries. | Seed: Technique field | Edit the technique labels. |
| 13 | Minor | UI-Unit_measure-001, 004, 008 | No assumptions (over-marking) | The part's units field label is marked `[open: Q-Unit_measure-02, label of the units field]`, but the docs name it *Units*. Q-Unit_measure-02 is about which field accepts unit values, not this label. | part-views.md#L44 | Edit: use *Units* and drop the marker where it is the only reason (Q-Unit_measure-02 then may not affect 001). |
| 14 | Minor | UI-Unit_measure-008 | Seed format | Requirement cites R-Unit_measure-05 but links only #L133, with no source link for R-Unit_measure-05 (#L138). | Seed: Requirement field | Edit: add part-index.md#L138. |
| 15 | Minor | UI-Unit_measure-011, 012, 014, 015, 018, 024, 025, 026 | Seed format | The range anchors are written `#L28-32` instead of the inventory's `#L28-L32`, so the links do not resolve to the end line. | Inventory rows R-Unit_measure-07, -08, -10, -12, -16 | Edit the anchors. |
| 16 | Minor | UI-Unit_measure-029, 024 | One behaviour | 029 step 2 (`500 g` gives 0.5 kg) repeats 024 in full. 013 step 1 repeats 012 step 2. The script did not flag these overlaps. | R-Unit_measure-16, -18 | Optional: leave as a setup step, or trim. |
| 17 | Minor | UI-Unit_measure-004, 005, 006 | Seed format (Automation) | Automation says "Yes." while an open question blocks the expected detail. Other cases say "Yes, once Q-... is answered". | Seed: Automation field | Edit for consistency. |
| 18 | Minor | UI-Unit_measure-018 to 023 | Seed format (Prerequisites) | The Pre-steps open the *Parts* view, but the cases work in the settings panel. | Seed: Prerequisites field | Edit the Pre-steps. |

Seed format, Review fields (all `Draft` or `Draft · Open question: ...`) and the users chosen are otherwise correct. `allaccess` for supplier parts matches doc issue 15. `admin` for the settings tab is left open by Q-Unit_measure-06.

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Unit_measure-009 | 70 | UI-Unit_measure-010 | Keep | Mass vs length: separate dimensions named by R-Unit_measure-06, with different part units. |
| UI-Unit_measure-010 | 70 | UI-Unit_measure-009 | Keep | Same as above. |
| UI-Unit_measure-021 | 52 | UI-Unit_measure-022 | Keep | Different rule (R-14 alias vs R-15 dimensionless). |
| UI-Unit_measure-022 | 52 | UI-Unit_measure-021 | Keep | Different rule. |
| UI-Unit_measure-024 | 72 | UI-Unit_measure-025 | Keep | Merge target; carries the documented exact outcome (0.5 kg). |
| UI-Unit_measure-025 | 72 | UI-Unit_measure-024 | Merge into UI-Unit_measure-024 | Same rule, user, state and outcome; `1 lb` is another value of the compatible-unit class. Carry `1 lb` over as a step in 024. |
| UI-Unit_measure-026 | 54 | UI-Unit_measure-027 | Keep | Different rule (R-16 vs R-17) and starting state (kg vs no unit). |
| UI-Unit_measure-027 | 54 | UI-Unit_measure-026 | Keep | Same as above. |

## Questions for the architect

1. **Incompatible BOM raw amount (finding 1):** is a raw amount in a unit incompatible with the part's unit (`2 m` for a `kg` part) rejected? The docs state only that compatible units are allowed. Q-Unit_measure-09 presupposes an error.
2. **Built-in custom units in the UI (finding 6):** where can the meaning of `dozen`, `hundred` and `thousand` be observed (part units, BOM raw amount), and does a dimensionless built-in unit count as "having a unit" for R-Unit_measure-17?
3. **Expected value for `1 lb` (finding 10, only if 025 is kept):** may the case state the standard conversion (1 lb = 0.45359237 kg) when the docs do not give it, or must the value stay open?
4. **Q-Unit_measure-02 scope:** the docs give the part field label (*Units*, part-views.md#L44). Should Q-Unit_measure-02 be narrowed to "which field accepts values with units and where the converted value is shown", and its Affected cases updated (add 008, possibly drop 001)?
