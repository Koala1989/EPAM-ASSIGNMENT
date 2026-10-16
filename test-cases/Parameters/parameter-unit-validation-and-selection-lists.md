# Parameter unit validation and selection list administration: Part_Params test cases

### UI-Part_Params-043: With unit validation disabled, a value with incompatible units is accepted.

| Field | Value |
|---|---|
| **Summary** | With unit validation disabled, a parameter value in volts is accepted on a template with base unit `ohm`. |
| **Requirement** | `R-Part_Params-32` ([concepts-parameters.md#L181-L188](../../requirements/docs/concepts-parameters.md#L181-L188)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Decision table (validation off x incompatible unit) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: unit validation = off [open: Q-Part_Params-14, setting name and default]; Data: template `QA-<suffix> Resistance` (Units `ohm`); part `QA-<suffix> Part`; Pre-steps: setting changed by `admin` in the UI [open: Q-Part_Params-14, where the setting is changed] |
| **Automation** | Partial: setting name and location are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a parameter to the part with an incompatible value. | Template: `QA-<suffix> Resistance`<br>Data: `5 V` | The parameter is created: with unit validation disabled any parameter value is accepted (R-Part_Params-32). Open: Q-Part_Params-14 (value as shown in the tab: as entered or altered). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then restore the unit validation setting to its original state.

**Notes:** None

**Duplicate check:** 54 · Review · matches: [UI-Part_Params-044](parameter-unit-validation-and-selection-lists.md) (54), [UI-Part_Params-045](parameter-unit-validation-and-selection-lists.md) (50)

**Duplicate judgement:** Keep · Differs from 044 in input class (parseable value in an incompatible unit, `5 V`, vs unparseable text `abc`) and from 045 in decision-table column (incompatible vs compatible unit with validation off). · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-044: With unit validation disabled, a non-numeric text value is accepted.

| Field | Value |
|---|---|
| **Summary** | With unit validation disabled, plain text with no unit meaning is accepted on a template with base unit `ohm`. |
| **Requirement** | `R-Part_Params-32` ([concepts-parameters.md#L181-L188](../../requirements/docs/concepts-parameters.md#L181-L188)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (validation off, non-numeric class), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: unit validation = off [open: Q-Part_Params-14, setting name and default]; Data: template `QA-<suffix> Resistance` (Units `ohm`); part `QA-<suffix> Part`; Pre-steps: setting changed by `admin` in the UI [open: Q-Part_Params-14, where the setting is changed] |
| **Automation** | Partial: setting name and location are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a parameter with a text value. | Template: `QA-<suffix> Resistance`<br>Data: `abc` | The parameter is created: any parameter value is accepted (R-Part_Params-32). Open: Q-Part_Params-14 (whether `any parameter value` includes non-numeric text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then restore the unit validation setting to its original state.

**Notes:** None

**Duplicate check:** 54 · Review · matches: [UI-Part_Params-043](parameter-unit-validation-and-selection-lists.md) (54)

**Duplicate judgement:** Keep · Different equivalence class from 043: non-numeric text with no unit meaning (`abc`) vs a valid quantity in an incompatible unit (`5 V`). · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-045: With unit validation disabled, a compatible value is still accepted.

| Field | Value |
|---|---|
| **Summary** | Disabling unit validation does not stop a value with compatible units (`4.7k`) being saved. |
| **Requirement** | `R-Part_Params-32` ([concepts-parameters.md#L181-L188](../../requirements/docs/concepts-parameters.md#L181-L188)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Decision table (validation off x compatible unit) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: unit validation = off [open: Q-Part_Params-14, setting name and default]; Data: template `QA-<suffix> Resistance` (Units `ohm`); part `QA-<suffix> Part`; Pre-steps: setting changed by `admin` in the UI [open: Q-Part_Params-14, where the setting is changed] |
| **Automation** | Partial: setting name and location are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a parameter with a compatible value. | Template: `QA-<suffix> Resistance`<br>Data: `4.7k` | The parameter is created (R-Part_Params-32). Open: Q-Part_Params-14 (value shown: as entered or converted). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then restore the unit validation setting to its original state.

**Notes:** None

**Duplicate check:** 50 · Review · matches: [UI-Part_Params-043](parameter-unit-validation-and-selection-lists.md) (50)

**Duplicate judgement:** Keep · Different decision-table column from 043: a compatible unit (`4.7k`) with validation off vs an incompatible one (`5 V`). · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-047: Re-enabling unit validation rejects incompatible values again.

| Field | Value |
|---|---|
| **Summary** | After unit validation is disabled and an incompatible value saved, enabling it again makes the same value rejected for a new parameter. |
| **Requirement** | `R-Part_Params-31` ([concepts-parameters.md#L183](../../requirements/docs/concepts-parameters.md#L183)), `R-Part_Params-32` ([concepts-parameters.md#L187](../../requirements/docs/concepts-parameters.md#L187)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | State transition (off to on) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: unit validation = off, then on [open: Q-Part_Params-14, setting name and default]; Data: template `QA-<suffix> Resistance` (Units `ohm`); part `QA-<suffix> Part`; second part `QA-<suffix> Part 2`; Pre-steps: setting changed by `admin` in the UI [open: Q-Part_Params-14, where the setting is changed] |
| **Automation** | Partial: setting name and location are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-14, Q-Part_Params-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a parameter `5 V` while the setting is off. | Template: `QA-<suffix> Resistance`<br>Data: `5 V` | The parameter is created (R-Part_Params-32). |
| 2 | As `admin`, enable unit validation. | Setting: on [open: Q-Part_Params-14, setting name] | Setting saved. Open: Q-Part_Params-14 (confirmation shown). |
| 3 | As `engineer`, add a parameter on the second part with the same incompatible value. | Part: `QA-<suffix> Part 2`<br>Data: `5 V` | The parameter is not created (R-Part_Params-31). Open: Q-Part_Params-07 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then restore the unit validation setting to its original state.

**Notes:** None

---

### UI-Part_Params-048: A user without admin rights cannot change the unit validation setting.

| Field | Value |
|---|---|
| **Summary** | `reader` and `engineer` cannot change the setting that disables parameter unit validation. |
| **Requirement** | `R-Part_Params-32` ([concepts-parameters.md#L181-L188](../../requirements/docs/concepts-parameters.md#L181-L188)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Negative (blocked role) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions, Settings-dependent |
| **Prerequisites** | User: `reader` (view only); Settings: unit validation [open: Q-Part_Params-14, setting name and default]; Data: None; Pre-steps: log in as `reader` [open: Q-Part_Params-14, where the setting is changed] |
| **Automation** | Partial: location of the setting is an open question. |
| **Review** | Draft · Open question: Q-Part_Params-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Try to open the page that holds the unit validation setting. | [open: Q-Part_Params-14, page] | Proposed, to confirm in Q-Part_Params-14: the page or the setting control is not available to a non-admin user, and the value cannot be changed. |
| 2 | Repeat as `engineer`. | None | Proposed, to confirm in Q-Part_Params-14: same as step 1. |

**Postconditions and cleanup:** None: no records created.

**Notes:** The docs state no permission for the setting.

---

### UI-Part_Params-049: What-if: toggling unit validation does not alter saved parameters.

| Field | Value |
|---|---|
| **Summary** | A parameter saved with a compatible value stays unchanged when unit validation is disabled and enabled again. |
| **Requirement** | `R-Part_Params-32` ([concepts-parameters.md#L181-L188](../../requirements/docs/concepts-parameters.md#L181-L188)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | What-if business scenario |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: unit validation = on [open: Q-Part_Params-14, setting name and default]; Data: template `QA-<suffix> Resistance` (Units `ohm`); part `QA-<suffix> Part`; parameter `4.7k` already saved on the part; Pre-steps: setting changed by `admin` in the UI [open: Q-Part_Params-14, where the setting is changed] |
| **Automation** | Partial: outcome not stated in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | As `admin`, disable then enable unit validation. | Setting off, then on | Both changes saved. Open: Q-Part_Params-14 (setting name). |
| 2 | Open the part's *Parameters* tab. | None | Proposed, to confirm in Q-Part_Params-14: the existing parameter `4.7k` is still listed with the same value. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then restore the unit validation setting to its original state.

**Notes:** None

---

### UI-Part_Params-050: The Admin Center has a Parameter section for selection lists.

| Field | Value |
|---|---|
| **Summary** | An admin can open the Parameter section of the Admin Center and see the selection lists. |
| **Requirement** | `R-Part_Params-36` ([concepts-parameters.md#L195-L202](../../requirements/docs/concepts-parameters.md#L202)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: authorised user) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: selection list `QA-<suffix> Colors` created via API as `admin`; Pre-steps: log in as `admin` |
| **Automation** | Partial: labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-15 (path to it). |
| 2 | Open the *Parameter* section. | None | The section is shown (R-Part_Params-36) and lists `QA-<suffix> Colors`. Open: Q-Part_Params-15 (tab or panel label, columns). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then delete the selection list(s) `QA-<suffix>`.

**Notes:** None

---

### UI-Part_Params-051: An admin creates a selection list with entries.

| Field | Value |
|---|---|
| **Summary** | A selection list with three entries is created in the Admin Center Parameter section. |
| **Requirement** | `R-Part_Params-36` ([concepts-parameters.md#L195-L202](../../requirements/docs/concepts-parameters.md#L202)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: None; Pre-steps: open Admin Center, *Parameter* section |
| **Automation** | Partial: labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Start creating a selection list. | None | A form opens. Open: Q-Part_Params-15 (button and field labels). |
| 2 | Fill in name and entries and submit. | Name: `QA-<suffix> Colors`<br>Entries: `Red`, `Green`, `Blue` | The list is created and shown in the section (R-Part_Params-36). Open: Q-Part_Params-15 (how entries are entered). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then delete the selection list(s) `QA-<suffix>`.

**Notes:** None

---

### UI-Part_Params-052: A selection list cannot be created with an empty or whitespace-only name.

| Field | Value |
|---|---|
| **Summary** | The create form does not accept an empty list name or a name of spaces only. |
| **Requirement** | `R-Part_Params-36` ([concepts-parameters.md#L195-L202](../../requirements/docs/concepts-parameters.md#L202)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty), Error guessing (whitespace-only) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: None; Pre-steps: open the selection list create form |
| **Automation** | Partial: error text is an open question. |
| **Review** | Draft · Open question: Q-Part_Params-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Leave the name empty, enter an entry and submit. | Name: empty<br>Entries: `Red` | Proposed, to confirm in Q-Part_Params-15: the list is not created and an error is shown on the name field. |
| 2 | Enter spaces as the name and submit. | Name: 3 spaces<br>Entries: `Red` | Proposed, to confirm in Q-Part_Params-15: the list is not created and an error is shown. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then delete the selection list(s) `QA-<suffix>`.

**Notes:** Merged with the former UI-Part_Params-053 (whitespace-only name, now step 2) on the architect's decision, 2026-10-15.

---

### UI-Part_Params-054: A second selection list with the same name.

| Field | Value |
|---|---|
| **Summary** | Creating a list with the name of an existing list is tried. |
| **Requirement** | `R-Part_Params-36` ([concepts-parameters.md#L195-L202](../../requirements/docs/concepts-parameters.md#L202)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: selection list `QA-<suffix> Colors`; Pre-steps: open the create form |
| **Automation** | Partial: outcome is an open question. |
| **Review** | Draft · Open question: Q-Part_Params-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a list with the same name. | Name: `QA-<suffix> Colors`<br>Entries: `Red` | Not known: depends on open question Q-Part_Params-15 (whether list names must be unique, and the error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then delete the selection list(s) `QA-<suffix>`.

**Notes:** None

---

### UI-Part_Params-055: A selection list with a special-character and Unicode name.

| Field | Value |
|---|---|
| **Summary** | A list named with special characters and Unicode is created and shown unchanged. |
| **Requirement** | `R-Part_Params-36` ([concepts-parameters.md#L195-L202](../../requirements/docs/concepts-parameters.md#L202)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Error guessing (special characters, Unicode) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: None; Pre-steps: open the create form |
| **Automation** | Partial: labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a list with the special name. | Name: `QA-<suffix> <&> Ω "x"`<br>Entries: `Red` | The list is created (R-Part_Params-36). Proposed, to confirm in Q-Part_Params-15: the name is shown exactly as entered. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then delete the selection list(s) `QA-<suffix>`.

**Notes:** None

---

### UI-Part_Params-056: Entries can be added to an existing selection list.

| Field | Value |
|---|---|
| **Summary** | An entry added to a list in use is accepted as a parameter value on a part. |
| **Requirement** | `R-Part_Params-09` ([concepts-parameters.md#L40](../../requirements/docs/concepts-parameters.md#L40)), `R-Part_Params-36` ([concepts-parameters.md#L195-L202](../../requirements/docs/concepts-parameters.md#L202)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | State transition (list edited, value now valid) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: list `QA-<suffix> Colors` (`Red`,`Green`); template `QA-<suffix> Sel` linked to it; part `QA-<suffix> Part`; Pre-steps: None |
| **Automation** | Partial: labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-15, Q-Part_Params-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Edit the list and add an entry. | Entry: `Blue` | The list saves with three entries (R-Part_Params-36). Open: Q-Part_Params-15 (edit control label). |
| 2 | Add a parameter on the part with the new entry. | Template: `QA-<suffix> Sel`<br>Data: `Blue` | The parameter is created: values come from the selection list (R-Part_Params-09). Open: Q-Part_Params-06 (Data control). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then delete the selection list(s) `QA-<suffix>`.

**Notes:** None

---

### UI-Part_Params-057: What-if: an entry removed from a list already used by a parameter.

| Field | Value |
|---|---|
| **Summary** | A list entry is removed after a part parameter uses it. |
| **Requirement** | `R-Part_Params-09` ([concepts-parameters.md#L40](../../requirements/docs/concepts-parameters.md#L40)), `R-Part_Params-36` ([concepts-parameters.md#L195-L202](../../requirements/docs/concepts-parameters.md#L202)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: list `QA-<suffix> Colors` (`Red`,`Green`); template `QA-<suffix> Sel`; part with parameter `Green`; Pre-steps: None |
| **Automation** | No: outcome unknown. |
| **Review** | Draft · Open question: Q-Part_Params-16 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Remove the entry `Green` from the list. | Entry: `Green` | Not known: depends on open question Q-Part_Params-16 (whether removal is allowed for an entry in use). |
| 2 | Open the part's *Parameters* tab. | None | Not known: depends on open question Q-Part_Params-16 (what the parameter shows). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then delete the selection list(s) `QA-<suffix>`.

**Notes:** None

---

### UI-Part_Params-058: An unused selection list can be deleted.

| Field | Value |
|---|---|
| **Summary** | A list not linked to any template is deleted from the Parameter section. |
| **Requirement** | `R-Part_Params-36` ([concepts-parameters.md#L195-L202](../../requirements/docs/concepts-parameters.md#L202)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | State transition (exists to deleted) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: list `QA-<suffix> Colors`, not used; Pre-steps: open *Parameter* section |
| **Automation** | Partial: labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Delete the list. | None | The list is no longer shown in the section (R-Part_Params-36). Open: Q-Part_Params-15 (delete control and confirmation). |

**Postconditions and cleanup:** None: list deleted by the case.

**Notes:** None

---

### UI-Part_Params-059: What-if: deleting a selection list that a template uses.

| Field | Value |
|---|---|
| **Summary** | A list linked to a template is deleted. |
| **Requirement** | `R-Part_Params-36` ([concepts-parameters.md#L195-L202](../../requirements/docs/concepts-parameters.md#L202)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: list `QA-<suffix> Colors`; template `QA-<suffix> Sel` linked to it; Pre-steps: None |
| **Automation** | No: outcome unknown. |
| **Review** | Draft · Open question: Q-Part_Params-16 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Delete the list. | None | Not known: depends on open question Q-Part_Params-16 (blocked, or template loses the list). |
| 2 | Open the template. | None | Not known: depends on open question Q-Part_Params-16 (template state). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then delete the selection list(s) `QA-<suffix>`.

**Notes:** None

---

### UI-Part_Params-060: A selection list can hold more than the 5000-character Choices limit.

| Field | Value |
|---|---|
| **Summary** | A list with entries totalling over 5000 characters is created and used, where template Choices would be limited. |
| **Requirement** | `R-Part_Params-34` ([concepts-parameters.md#L197](../../requirements/docs/concepts-parameters.md#L197)), `R-Part_Params-36` ([concepts-parameters.md#L195-L202](../../requirements/docs/concepts-parameters.md#L202)) |
| **Area** | Part_Params |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (5001+ characters via list) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: 60 entries of 100 characters (6000 characters in total); Pre-steps: open the create form |
| **Automation** | Partial: entry limits are open. |
| **Review** | Draft · Open question: Q-Part_Params-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create the list with the 60 entries. | Name: `QA-<suffix> Big`<br>Entries: 60 x 100 characters | The list is created: selection lists overcome the 5000-character limit (R-Part_Params-34). Open: Q-Part_Params-15 (limits on entries and entry length). |
| 2 | Add a parameter using the last entry. | Data: entry 60 | The parameter is created (R-Part_Params-09). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then delete the selection list(s) `QA-<suffix>`.

**Notes:** None

---

### UI-Part_Params-061: A value from a template's selection list is accepted on a part.

| Field | Value |
|---|---|
| **Summary** | The positive counterpart of UI-Part_Params-016: an entry in the list is accepted. |
| **Requirement** | `R-Part_Params-09` ([concepts-parameters.md#L40](../../requirements/docs/concepts-parameters.md#L40)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: value in list) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: list `QA-<suffix> List` (`A`,`B`); template `QA-<suffix> Sel` linked to it; part `QA-<suffix> Part`; Pre-steps: None |
| **Automation** | Partial: Data control is an open question. |
| **Review** | Draft · Open question: Q-Part_Params-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a parameter with a listed value. | Template: `QA-<suffix> Sel`<br>Data: `A` | The parameter is created and `A` is shown (R-Part_Params-09). Open: Q-Part_Params-06 (Data control). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the template(s), then delete the selection list(s) `QA-<suffix>`.

**Notes:** None

---

### UI-Part_Params-062: A non-admin user cannot administer selection lists.

| Field | Value |
|---|---|
| **Summary** | `reader` and `engineer` cannot open the selection list section of the Admin Center. |
| **Requirement** | `R-Part_Params-36` ([concepts-parameters.md#L195-L202](../../requirements/docs/concepts-parameters.md#L202)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Negative (blocked role) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: None; Pre-steps: log in as `reader` |
| **Automation** | Partial: outcome is an open question. |
| **Review** | Draft · Open question: Q-Part_Params-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Try to open the Admin Center *Parameter* section. | None | Proposed, to confirm in Q-Part_Params-15: the section is not available and no list can be created, edited or deleted. |
| 2 | Repeat as `engineer`. | None | Proposed, to confirm in Q-Part_Params-15: same as step 1. |

**Postconditions and cleanup:** None: no records created.

**Notes:** The docs name no permission for the Admin Center.

---

### UI-Part_Params-063: A selection list locked by a plugin cannot be changed.

| Field | Value |
|---|---|
| **Summary** | A list locked by a plugin shows as locked, and changes are blocked. |
| **Requirement** | `R-Part_Params-35` ([concepts-parameters.md#L199](../../requirements/docs/concepts-parameters.md#L199)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | State transition (unlocked to plugin-locked) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: list locked by [open: Q-Part_Params-17, plugin and how it locks a list]; Pre-steps: None |
| **Automation** | No: no locking plugin known. |
| **Review** | Draft · Open question: Q-Part_Params-17 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Try to edit and delete the locked list. | None | Plugins can lock selection lists (R-Part_Params-35). Open: Q-Part_Params-17 (what is blocked and how it is shown). |

**Postconditions and cleanup:** None.

**Notes:** No plugin in the test instance is known to lock lists.

---
