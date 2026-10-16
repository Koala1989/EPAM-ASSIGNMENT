# Review: Part creation with only the required fields (UI), 2026-10-16

**Cases reviewed:** UI-Part-074, UI-Part-075, UI-Part-076, UI-Part-077, UI-Part-078 · **Verdict:** Approve with changes

## Coverage

`python tools/coverage_check.py --area Part --area ATT --area Unit_measure --file test-cases/Part_Creation_and_Import/part-creation-required-fields.md`: exit 0 (every cited rule ID exists). Part: 41 rules, 9 cited by these cases, 32 not cited. R-ATT-28 and R-Unit_measure-02 are cited by UI-Part-077.

| Rule | Cases | Gap / Out of scope / Covered | Depth issues |
|---|---|---|---|
| R-Part-01 | 074, 075 | Covered | None |
| R-Part-04 | 076, 078 | Covered | None |
| R-Part-05 | 074, 076 | Covered (cited) | Neither case tests form errors. The negative case (Name empty, Q-REV-05 says Name is the only required field) exists as UI-Part-042 in `part-creation-form-validation.md`, so no gap. |
| R-Part-06 | 074, 075, 077, 078 | Covered | None |
| R-Part-09 | 077 | Covered (only through the inventory note on the Purchaseable default) | See finding 5. |
| R-Part-12 | 074, 075, 076 | Covered | None |
| R-Part-14 | 076 | Cited, not tested | See finding 6. |
| R-Part-15 | 074, 075, 076 | Covered | None |
| R-Part-16 | 074 | Covered (optional clause only) | Search clause is out of scope here. |
| R-ATT-28 | 077 | Covered | Already covered by UI-ATT-066 (finding 8). |
| R-Unit_measure-02 | 077 | Covered, outcome open (Q-Unit_measure-01) | Already covered by UI-Unit_measure-003 (finding 8). |
| R-Part-02, R-Part-03 | none here | Out of scope: *Add Parts* menu and create permission (UI-Part-002, 003, 039) | None |
| R-Part-07, R-Part-08 | none here | Out of scope: initial stock functionality | None |
| R-Part-10, R-Part-11 | none here | Out of scope: supplier data (outdated rule) and non-UI creation | None |
| R-Part-13, R-Part-17 | none here | Out of scope: form validation (UI-Part-047 to 050, 065 to 069) | None |
| R-Part-18 to R-Part-41 | none here | Out of scope: import from file, update import, supplier import | None |

The functionality has a Negative case (UI-Part-078). No permission or "visible only if" rule is in scope.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Major | UI-Part-074 step 3 | Specific Expected results | "IPN, Revision and Keywords are not required" is a rule restatement, not something observable on the detail page after submit. The observable fact (the part was created with them empty) is already shown by steps 1-2. | R-Part-12, R-Part-15, R-Part-16 | Edit: drop the sentence or replace it with an observable check (e.g. the detail page loads for the new part); keep the Q-Part-23 marker for how empty fields show. |
| 2 | Major | UI-Part-074, UI-Part-075 | Data-driven | Same rules (R-Part-01, R-Part-06, Q-REV-05), same three steps, differ only in input (Name vs Name + Category) and in the expected category on the detail page. Candidates for one case with a Data sets table (rows: Name only; Name + Category). The only difference is the prerequisite category, which can be created for both rows. | Q-REV-05 answer: "only Name is marked required ... A part is created with Name and Category only" | Architect decides: merge into one data-driven case, or keep two and note why (075 is the case Q-REV-05 observed directly). |
| 3 | Major | UI-Part-077 Prerequisites | User / Settings | Settings: None, but step 1 expects *Purchaseable* checked, which the inventory ties to the `PART_PURCHASEABLE` setting. The expected result depends on an unpinned setting state. (UI cases in `part-creation-flow.md` state `PART_PURCHASEABLE` = on.) | R-Part-09 note: "*Purchaseable* is checked by default (`PART_PURCHASEABLE`)" | Edit: Settings: `PART_PURCHASEABLE` = on (default). |
| 4 | Minor | UI-Part-077 step 4 | Seed format | The Expected result is only "Open: ..." with no stated outcome. Since R-Unit_measure-02 conflicts with part-views.md#L44 (index Doc issue 1), stating it as fact would be wrong, so the seed form is `Not known: depends on open question Q-Unit_measure-01 (...)`. Mixing in Q-Part-23 (other defaults) in a units step is also off-topic. Compare UI-Unit_measure-003 step 2, which states the rule outcome first and then Open. | part-index.md#L120 vs part-views.md#L44 | Edit wording; move the Q-Part-23 remark to step 1 or 3. |
| 5 | Minor | UI-Part-077 step 1 | Fidelity | The cited rule R-Part-09 states the supplier options shown when Purchaseable is marked, not the Purchaseable default; the default comes only from an app observation in the inventory note. | R-Part-09, part-create.md#L47 | Architect: accept the note as the source, or turn the default into a question. |
| 6 | Minor | UI-Part-076 | Fidelity / Requirement | Cites R-Part-05 (form errors block submit) and R-Part-14 (Description is longer-form text), neither of which the case tests; the required markers come from Q-REV-05. | R-Part-05, R-Part-14 | Edit: drop R-Part-05 and R-Part-14 from Requirement, or keep only as context. |
| 7 | Minor | UI-Part-076 Requirement | Seed format | Schema reference `requirements/openapi-parts.yaml components.schemas.Part.name` has no link or line (UI-Part-042 gives L4196-L4199). | Seed: Requirement needs the source link | Edit: add the line link. |
| 8 | Minor | UI-Part-077, UI-Part-074 | One behaviour / overlap | 077 checks three rules from three Areas (Purchaseable default, Active default, unit default). Step 3 repeats UI-ATT-066 (Name only, submit, part is Active); step 4 repeats UI-Unit_measure-003 (no unit, unit shown on details). UI-Part-074 steps 1-2 are also the same as UI-ATT-066 steps 2-3. The dedupe score stayed below 50, so no duplicate verdict is given. | UI-ATT-066, UI-Unit_measure-003 | Architect: decide whether 077 stays as a combined "defaults" case or is reduced to the Purchaseable/attribute defaults only. |
| 9 | Minor | UI-Part-074, UI-Part-077 | Technique | 074 "Boundary value analysis (minimum input set)": there is no numeric or length boundary; it is the valid class only. 077 "State transition (new part to Active)": no transition is exercised, only a default state is read. | Seed Technique list | Edit technique labels. |
| 10 | Minor | UI-Part-077 Requirement | Seed format | The source given for R-Unit_measure-02 is part-views.md#L44 (the conflicting line); the rule's own source is part-index.md#L120. | R-Unit_measure-02 inventory row | Edit: cite part-index.md#L120 and keep #L44 as the conflict. |
| 11 | Minor | Q-Unit_measure-01 | Open-question marking | UI-Part-077 is marked with Q-Unit_measure-01, but the question's Affected cases lists only UI-Unit_measure-002, 003. | Units_of_Measure/open-questions.md row Q-Unit_measure-01 | Architect: add UI-Part-077 to the Affected cases. |

UI-Part-078: no findings. The cancel outcome is correctly written as `Proposed, to confirm in Q-Part-24`, the unknown control is marked `[open: Q-Part-24, ...]`, and the Review field is marked.

Review fields: all five are `Draft` or `Draft · Open question: ...`. Users: `engineer` is the least-privileged demo user that can create parts in each case.

## Duplicates

No case scored 50 or more.

## Questions for the architect

1. Q-Part-18 ("Is Description required on the Create Part form?") is still Open, but the Q-REV-05 answer says Description is optional. UI-Part-076 relies on Q-REV-05 for this. Should Q-Part-18 be answered from Q-REV-05, and UI-Part-051 updated?
2. Q-REV-05 was observed on a form called *Add Part*; these cases (and the docs) call it *Create Part*. Which label does the 1.5.6 menu option and form title use?
3. Should UI-Part-077 stay, given UI-ATT-066 (Active default) and UI-Unit_measure-003 (unit default) already cover two of its three checks (finding 8)?
