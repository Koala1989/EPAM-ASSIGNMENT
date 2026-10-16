# Review: Part parameters tab, parameter templates and category parameters (UI), 2026-10-15

**Cases reviewed:** UI-Part_Params-001 to UI-Part_Params-042 (42 cases, `test-cases/Parameters/parameters-tab-templates-and-category-parameters.md`) · **Verdict:** Approve with changes

No Blocker. The Majors are mostly gaps and missing depth cases (new cases needed). Three Majors also need edits to existing cases: UI-Part_Params-008 (Expected result), UI-Part_Params-034 (Prerequisites, open question) and the Review field of seven cases that use Q-Part_Params-01 but do not list it (F1). None of these makes an existing Expected result wrong.

## Coverage

`coverage_check.py --area Part_Params`: Rules: 36 · covered: 22 · not cited by any case: 14 (exit 0, no unknown rule IDs). UI-Part_Params-035 also cites `R-ATT-26` (Attributes Area), which exists.

| Rule | Cases | Gap / Out of scope / Covered | Depth issues |
|---|---|---|---|
| R-Part_Params-01 | none | Question (see Q1) | Informational ("not used for any core business logic"); no observable behaviour to test |
| R-Part_Params-02 | 027, 028, 032 | Covered | None |
| R-Part_Params-03 | 004, 005, 006, 018 | Covered | None (004 cites it wrongly, see F7) |
| R-Part_Params-04 | 001, 002 | Covered | None |
| R-Part_Params-05 | 001, 002, 007, 008 | Covered | None |
| R-Part_Params-06 | 009 | Covered | **Missing hidden case:** no case checks that a template whose Model Type is set to another model (e.g. Company) is *not* offered on a part (F3) |
| R-Part_Params-07 | 010, 011, 012 | Covered | None |
| R-Part_Params-08 | 014, 015 | Covered | Minor: the other valid value (*false*) is not tested |
| R-Part_Params-09 | 016 | Covered | **Missing positive case:** no case assigns a value that *is* in the selection list (F4) |
| R-Part_Params-10 | 001, 002, 003, 004, 019 | Covered | None |
| R-Part_Params-11 | 017, 018 | Covered | None |
| R-Part_Params-12 | 009, 010, 014, 029, 030, 031, 035 | Covered | None |
| R-Part_Params-13 | 020, 021, 022, 041 | Covered | **Missing distinguishing case:** "Unique for model type" vs "Globally unique" differ only when the same value is used on a different model type; 021 and 022 run the same Part-to-Part scenario with the same outcome, so the difference between the two options is never tested (F5) |
| R-Part_Params-14 | 023 | Covered | None |
| R-Part_Params-15 | 021, 022, 023, 024 | Covered | None |
| R-Part_Params-16 | 024 | Covered | None |
| R-Part_Params-17 | 025 | Covered | None |
| R-Part_Params-18 | 026 | Covered | None |
| R-Part_Params-19 | 036 to 040, 042 | Covered | None |
| R-Part_Params-20 | 041 | Covered | None |
| R-Part_Params-21 to R-Part_Params-29 | none | Out of scope | Parametric tables (Parametric View, sorting, filtering, operators): a separate functionality of the Part_Params Area |
| R-Part_Params-30 | 033 | Covered | None |
| R-Part_Params-31 | 034 | Covered | None |
| R-Part_Params-32 | none | **Gap** | Unit validation disabled, so an incompatible value is accepted: the "can be disabled" clause of the incompatible-units behaviour that 034 tests. Setting name and default are not stated (index doc issue 8), so the case needs an open question (F2) |
| R-Part_Params-33 | none | Out of scope | Sorting by parameter belongs to parametric tables |
| R-Part_Params-34 | 012, 013 | Covered | Minor: the "selection lists overcome this" clause has no case |
| R-Part_Params-35 | none | Out of scope | Plugin behaviour; no plugin that locks selection lists in the test instance |
| R-Part_Params-36 | none | **Gap** (see Q2) | Selection-list administration in the Admin Center *Parameter* section: listed under "Parameter templates" in the inventory, and R-Part_Params-09 depends on it; UI-Part_Params-016 only sets a list up through the API |

Negative cases exist (003, 005, 007, 011, 013, 015, 016, 018, 019, 021 to 024, 030 to 032, 034, 035, 039 to 042). The blocked-user cases exist for templates (019), adding parameters (031), viewing (032) and category links (042).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| F1 | Major | UI-Part_Params-005, 006, 007, 008, 012, 013, 018 | Open-question marking | Steps 1 and 2 (step 1 in 018) carry `Open: Q-Part_Params-01` (where templates live and their labels), but the Review field lists only Q-Part_Params-02, -03 or -05. Q-Part_Params-01's "Affected cases" also leaves them out. Under the seed, each case stays approvable after the other question is answered even though the navigation is still unknown. | Seed, Review field: "`Draft · Open question: Q-<Area>-NN` (comma-separated if several) when an open question affects the case"; [concepts-parameters.md#L47-L55](../../requirements/docs/concepts-parameters.md#L47-L55) | Add Q-Part_Params-01 to these Review fields and to the question's Affected cases list (architect's edit, or rerun the creator) |
| F2 | Major | R-Part_Params-32 | Coverage (gap) | No case for "unit validation can be disabled so that any value is accepted". | [concepts-parameters.md#L187](../../requirements/docs/concepts-parameters.md#L187); index doc issue 8 | Rerun the creator for R-Part_Params-32; it needs a new open question for the setting name and default |
| F3 | Major | R-Part_Params-06 | Coverage (depth) | Only the blank Model Type case (009) exists. No case checks that a template set to another model type is left out of a part's Template selector. | [concepts-parameters.md#L37](../../requirements/docs/concepts-parameters.md#L37): "The InvenTree model to which this parameter template applies" | Rerun the creator for the restricted Model Type case (the selector outcome would need a proposal or an open question) |
| F4 | Major | R-Part_Params-09 | Coverage (depth) | Only the negative case (016) exists. No case checks that a value from the linked selection list is accepted. | [concepts-parameters.md#L40](../../requirements/docs/concepts-parameters.md#L40) | Rerun the creator for the valid-class case |
| F5 | Major | R-Part_Params-13 / UI-Part_Params-021, 022 | Coverage (depth) | Both cases test a repeated value on a second **Part**, which both options reject, so the doc's distinguishing example is untested: a value reused on a different model type (e.g. a Company) is allowed by "Unique for model type" and rejected by "Globally unique". | [concepts-parameters.md#L80-L81](../../requirements/docs/concepts-parameters.md#L80-L81) | Decide whether a cross-model check (Company parameter) is in scope for the Parts module (Q3); if so, rerun the creator |
| F6 | Major | R-Part_Params-36 | Coverage (gap) | No case manages a selection list in the Admin Center *Parameter* section. | [concepts-parameters.md#L202](../../requirements/docs/concepts-parameters.md#L202) | See Q2; if in scope, rerun the creator |
| F7 | Major | UI-Part_Params-008 | Rule outcome stated | Expected result is only `Not known`, but the outcome follows from inventoried rules: R-Unit_measure-11 says units are case-sensitive (`kg` valid, `KG` not), and R-Part_Params-05 says template units must be a valid physical unit. So `OHM` should be rejected, with only the error text open. The case does not cite R-Unit_measure-11 and names it only in the Expected cell. The Summary ("is checked against unit syntax") is vague too. | `test-cases/Units_of_Measure/requirements-inventory.md` R-Unit_measure-11 ([concepts-units.md#L56](../../requirements/docs/concepts-units.md#L56)); [concepts-parameters.md#L36](../../requirements/docs/concepts-parameters.md#L36) | Edit 008: add R-Unit_measure-11 to Requirement, state "The template is not saved: units are case-sensitive and `OHM` is not a valid unit (R-Unit_measure-11, R-Part_Params-05)", then `Open: Q-Part_Params-03 (error text)`; sharpen the Summary |
| F8 | Major | UI-Part_Params-034 | No assumptions / Open-question marking / Seed format | Prerequisites say `Settings: None`, but the case is tagged `Settings-dependent` and the Notes say it "Assumes unit validation is on". The docs give neither the setting name nor its default (index doc issue 8), and no open question covers this. | [concepts-parameters.md#L187](../../requirements/docs/concepts-parameters.md#L187); index doc issue 8 | Raise an open question for the unit-validation setting (name, default), put `Settings: unit validation on [open: Q-Part_Params-NN, setting name and default]` and add it to the Review field. The same question serves F2 |
| F9 | Major | UI-Part_Params-035 | Duplicate (cross-Area) | Same rule (R-ATT-26, "create" clause), user (`engineer`), starting state (locked part) and outcome (no parameter created) as **UI-ATT-059** in `test-cases/Attributes/part-attributes.md`. The inventory's Cross-references table makes R-ATT-26 the primary for this rule. `dedupe_cases.py` did not compare across Areas, so the case has no Duplicate check line. | `test-cases/Parameters/requirements-inventory.md` Cross-references; UI-ATT-059 | Architect: consider Remove (nothing to carry over except the template name in Test data). Q-ATT-14 does not list 035 as an affected case either |
| F10 | Minor | UI-Part_Params-004 | Fidelity | Cites R-Part_Params-03 (name uniqueness), which a whitespace-only Name does not test. | [concepts-parameters.md#L34](../../requirements/docs/concepts-parameters.md#L34) | Remove R-Part_Params-03 from Requirement |
| F11 | Minor | UI-Part_Params-012 | Open-question marking | Marked with Q-Part_Params-05, which asks only about 5001 characters; the 5000-character outcome is stated by R-Part_Params-34. (It is affected by Q-Part_Params-01, see F1.) | [concepts-parameters.md#L197](../../requirements/docs/concepts-parameters.md#L197) | Replace Q-Part_Params-05 with Q-Part_Params-01 in the Review field |
| F12 | Minor | UI-Part_Params-029 | Open-question marking | Data `100` on an `ohm` template: whether the tab shows `100` or a unit-annotated or converted value is the same unknown as Q-Part_Params-11. The case is marked with Q-Part_Params-10 (required fields, empty state), which does not affect its steps. | Q-Part_Params-11 | Mark with Q-Part_Params-11 (or use a template without units) |
| F13 | Minor | UI-Part_Params-009 | Open-question marking | Marked Q-Part_Params-01, but no step depends on it. Only the setup (blank Model Type) might, and that can be done via the API. | n/a | Architect: keep only if the setup is done through the UI |
| F14 | Minor | UI-Part_Params-006, 008 | Technique / Type | Type `Negative`, but the outcome is unknown (006) or wrongly given as unknown (008, see F7). | Seed Type field | Revisit Type once Q-Part_Params-02 is answered |
| F15 | Minor | UI-Part_Params-017 | Technique | "State transition (template edited)": editing a description is not a state transition. | Seed Technique field | Equivalence partitioning (valid class: edit an optional field) |
| F16 | Minor | UI-Part_Params-027 | One behaviour | Step 2 (reader sees no add, edit or delete controls) is a permission check that repeats UI-Part_Params-031. The case is also missing the `Permissions` tag. | n/a | Drop step 2 or tag it `Permissions` |
| F17 | Minor | UI-Part_Params-026 | Fidelity | Step 3 Expected adds "which can be added manually with a distinct value", but no step checks it. | [concepts-parameters.md#L100](../../requirements/docs/concepts-parameters.md#L100) | Add a step or drop the clause |
| F18 | Minor | UI-Part_Params-020, 035 | Seed format | Step Expected results cite rules not in the Requirement field (R-Part_Params-12 in 020, R-Part_Params-02 in 035). | n/a | Add them to Requirement or drop the citations |
| F19 | Minor | 009 to 016, 020 to 026, 028 to 030, 033 to 035, 037 to 041 | Seed format | Cleanup text is boilerplate: "delete the category" where the case creates no category. Several cases also have no login step and say `Pre-steps: None` (e.g. 010, 014, 020 to 025, 029, 033, 034). | Seed Prerequisites/Postconditions | Tidy when editing |
| F20 | Minor | UI-Part_Params-001 to 008, 012, 013, 017, 018, 036, 040 | User | `admin` (superuser) is used for template and category-link actions. The least-privileged user (e.g. staff `steven`) is not known: Q-Part_Params-09 asks this. | Seed: least-privileged demo user | Revisit after Q-Part_Params-09 |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Part_Params-001 | 60 | UI-Part_Params-002 | Keep | Name only with optional fields empty vs all fields with a valid unit |
| UI-Part_Params-002 | 60 | UI-Part_Params-001 | Keep | Same difference, from the other side |
| UI-Part_Params-003 | 51 | UI-Part_Params-004 | Keep | Empty vs whitespace-only Name (different invalid class) |
| UI-Part_Params-004 | 52 | UI-Part_Params-006 | Keep | Whitespace Name (required-field rule) vs name case variant (uniqueness); vs 003, different class |
| UI-Part_Params-005 | 63 | UI-Part_Params-006 | Keep | Exact duplicate (rejected) vs case-differing name (unknown) |
| UI-Part_Params-006 | 63 | UI-Part_Params-005 | Keep | Case-differing name vs exact duplicate |
| UI-Part_Params-007 | 60 | UI-Part_Params-008 | Keep | Non-unit string vs wrong-case real unit (R-Unit_measure-11) |
| UI-Part_Params-008 | 60 | UI-Part_Params-007 | Keep | Same difference, from the other side |
| UI-Part_Params-012 | 62 | UI-Part_Params-013 | Keep | On the boundary (5000) vs just above it (5001) |
| UI-Part_Params-013 | 62 | UI-Part_Params-012 | Keep | Just above the boundary vs on it |
| UI-Part_Params-021 | 93 | UI-Part_Params-022 | Keep | Decision-table column: Unique for model type vs Globally unique (see F5 for the depth gap) |
| UI-Part_Params-022 | 93 | UI-Part_Params-021 | Keep | Globally unique vs Unique for model type |
| UI-Part_Params-023 | 59 | UI-Part_Params-021/022 | Keep | Case-insensitive match (R-Part_Params-14), a different value class |
| UI-Part_Params-024 | 56 | UI-Part_Params-023 | Keep | Template with units, normalised numeric match (R-Part_Params-16) |
| UI-Part_Params-037 | 56 | UI-Part_Params-038 | Keep | Linked category vs sub-category clause |
| UI-Part_Params-038 | 56 | UI-Part_Params-037 | Keep | Sub-category vs linked category clause |

Not scored by the tool: UI-Part_Params-035 duplicates UI-ATT-059 across Areas (F9). No judgement line was written because 035 has no Duplicate check line.

## Questions for the architect

1. **R-Part_Params-01** ("Parameters are metadata only and are not used in core business logic") has no case. It describes something the system does *not* do, and nothing observable follows from it. Should it count as non-testable, or do you want a case (and if so, what should it check)?
2. **R-Part_Params-36** (selection-list administration in the Admin Center): is it part of this functionality, which covers templates and needs a selection list for R-Part_Params-09, or a separate functionality? Q-Part_Params-06 already asks how a selection list is created in the UI. This review counts it as a gap (F6).
3. **R-Part_Params-13 across model types** (F5): only "Unique for model type" vs "Globally unique" separates the two options, and seeing that needs a parameter on a non-Part model (e.g. a Company). Is a Company parameter inside the Parts-module scope of this assignment?
4. **UI-Part_Params-035 vs UI-ATT-059** (F9): should the Part_Params folder hold cases whose primary rule belongs to another Area (here R-ATT-26), or should they live only in the primary Area?
