# Part parameters tab, parameter templates and category parameters: Part_Params test cases


### UI-Part_Params-001: An admin creates a parameter template with only the required Name; Description and Units stay empty.

| Field | Value |
|---|---|
| **Summary** | An admin creates a parameter template with only the required Name; Description and Units stay empty. |
| **Requirement** | `R-Part_Params-10` ([concepts-parameters.md#L47-L55](../../requirements/docs/concepts-parameters.md#L47-L55)); `R-Part_Params-04` ([concepts-parameters.md#L35](../../requirements/docs/concepts-parameters.md#L35)); `R-Part_Params-05` ([concepts-parameters.md#L36](../../requirements/docs/concepts-parameters.md#L36)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Name only) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: None; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Open the *Parameters* tab and press *New Parameter*. | None | The template form opens with Name (required) and Units (optional) fields (R-Part_Params-10). Open: Q-Part_Params-01 (labels of the other fields). |
| 3 | Enter the name only and press *Submit*. | Name: `QA-<suffix> Tpl` | The form closes and the template appears in the templates list (R-Part_Params-10). Description and Units are accepted empty (R-Part_Params-04, R-Part_Params-05). |
| 4 | Check the new row in the list. | None | The row shows Name `QA-<suffix> Tpl`; Description and Units are empty. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template(s) created (Admin Center, *Parameters* tab) after deleting any parameters that use them.

**Notes:** None

**Duplicate check:** 60 · Review · matches: [UI-Part_Params-002](parameters-tab-templates-and-category-parameters.md) (60)

**Duplicate judgement:** Keep · Different equivalence class: only the required Name with Description and Units left empty (optional clause of R-Part_Params-04/05), vs UI-Part_Params-002 which supplies every field with a valid unit · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-002: An admin creates a template with Name, Description and a valid unit `ohm`.

| Field | Value |
|---|---|
| **Summary** | An admin creates a template with Name, Description and a valid unit `ohm`. |
| **Requirement** | `R-Part_Params-10` ([concepts-parameters.md#L47-L55](../../requirements/docs/concepts-parameters.md#L47-L55)); `R-Part_Params-04` ([concepts-parameters.md#L35](../../requirements/docs/concepts-parameters.md#L35)); `R-Part_Params-05` ([concepts-parameters.md#L36](../../requirements/docs/concepts-parameters.md#L36)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: all fields, valid unit) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: None; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Open the *Parameters* tab and press *New Parameter*. | None | The template form opens with Name (required) and Units (optional) fields (R-Part_Params-10). Open: Q-Part_Params-01 (labels of the other fields). |
| 3 | Fill in the fields and press *Submit*. | Name: `QA-<suffix> Resistance`<br>Description: `Resistance of a part`<br>Units: `ohm` | The form closes and the template is listed with the entered Name, Description and Units (R-Part_Params-04, R-Part_Params-05, R-Part_Params-10). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template(s) created (Admin Center, *Parameters* tab) after deleting any parameters that use them.

**Notes:** None

**Duplicate check:** 60 · Review · matches: [UI-Part_Params-001](parameters-tab-templates-and-category-parameters.md) (60)

**Duplicate judgement:** Keep · Different equivalence class: all fields filled including a valid unit `ohm` (the "valid physical unit if given" clause of R-Part_Params-05), vs UI-Part_Params-001 with optional fields empty · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-003: A template cannot be created with an empty Name.

| Field | Value |
|---|---|
| **Summary** | A template cannot be created with an empty Name. |
| **Requirement** | `R-Part_Params-10` ([concepts-parameters.md#L47-L55](../../requirements/docs/concepts-parameters.md#L47-L55)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty required field) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: None; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Open the *Parameters* tab and press *New Parameter*. | None | The template form opens with Name (required) and Units (optional) fields (R-Part_Params-10). Open: Q-Part_Params-01 (labels of the other fields). |
| 3 | Leave Name empty, enter a Description, press *Submit*. | Name: empty<br>Description: `QA-<suffix> no name` | The template is not created; Name is required (R-Part_Params-10). Open: Q-Part_Params-01 (error text and field highlighting). |

**Postconditions and cleanup:** None; no record is created. Cancel the form if still open.

**Notes:** None

**Duplicate check:** 51 · Review · matches: [UI-Part_Params-004](parameters-tab-templates-and-category-parameters.md) (51)

**Duplicate judgement:** Keep · Empty Name (rejection stated by R-Part_Params-10) vs UI-Part_Params-004's whitespace-only Name, a different invalid class whose outcome is unknown · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-004: A template cannot be created with a Name consisting only of whitespace.

| Field | Value |
|---|---|
| **Summary** | A template cannot be created with a Name consisting only of whitespace. |
| **Requirement** | `R-Part_Params-10` ([concepts-parameters.md#L47-L55](../../requirements/docs/concepts-parameters.md#L47-L55)); `R-Part_Params-03` ([concepts-parameters.md#L34](../../requirements/docs/concepts-parameters.md#L34)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Error guessing (whitespace-only name) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: None; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Open the *Parameters* tab and press *New Parameter*. | None | The template form opens with Name (required) and Units (optional) fields (R-Part_Params-10). Open: Q-Part_Params-01 (labels of the other fields). |
| 3 | Enter spaces only as Name and press *Submit*. | Name: 3 spaces | Not known: depends on open question Q-Part_Params-01 (docs state Name is required but not whether whitespace counts as a value). |

**Postconditions and cleanup:** If a template was created, delete it as `admin`.

**Notes:** None

**Duplicate check:** 52 · Review · matches: [UI-Part_Params-006](parameters-tab-templates-and-category-parameters.md) (52), [UI-Part_Params-003](parameters-tab-templates-and-category-parameters.md) (51)

**Duplicate judgement:** Keep · Whitespace-only Name is a different class from UI-Part_Params-003's empty Name, and tests the required-Name rule rather than UI-Part_Params-006's name-uniqueness case variant · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-005: A second template with exactly the same name is rejected.

| Field | Value |
|---|---|
| **Summary** | A second template with exactly the same name is rejected. |
| **Requirement** | `R-Part_Params-03` ([concepts-parameters.md#L34](../../requirements/docs/concepts-parameters.md#L34)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: duplicate name, same case) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: template `QA-<suffix> Dup`, created via the UI as `admin`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Open the *Parameters* tab and press *New Parameter*. | None | The template form opens with Name (required) and Units (optional) fields (R-Part_Params-10). Open: Q-Part_Params-01 (labels of the other fields). |
| 3 | Enter the name of the existing template and press *Submit*. | Name: `QA-<suffix> Dup` | The template is not created: the name must be unique (R-Part_Params-03). Open: Q-Part_Params-02 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template(s) created (Admin Center, *Parameters* tab) after deleting any parameters that use them.

**Notes:** None

**Duplicate check:** 63 · Review · matches: [UI-Part_Params-006](parameters-tab-templates-and-category-parameters.md) (63)

**Duplicate judgement:** Keep · Exact same-case duplicate name (rejection stated by R-Part_Params-03) vs UI-Part_Params-006's case-differing name, a different class with an unknown outcome · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-006: A template name differing only by letter case from an existing one.

| Field | Value |
|---|---|
| **Summary** | A template name differing only by letter case from an existing one. |
| **Requirement** | `R-Part_Params-03` ([concepts-parameters.md#L34](../../requirements/docs/concepts-parameters.md#L34)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate name, different case) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: template `QA-<suffix> Dup`, created as `admin`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Open the *Parameters* tab and press *New Parameter*. | None | The template form opens with Name (required) and Units (optional) fields (R-Part_Params-10). Open: Q-Part_Params-01 (labels of the other fields). |
| 3 | Enter the name in upper case and press *Submit*. | Name: `QA-<SUFFIX> DUP` (same text, upper case) | Not known: depends on open question Q-Part_Params-02 (the docs state names must be unique but not whether the check is case-sensitive). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template(s) created (Admin Center, *Parameters* tab) after deleting any parameters that use them.

**Notes:** None

**Duplicate check:** 63 · Review · matches: [UI-Part_Params-005](parameters-tab-templates-and-category-parameters.md) (63), [UI-Part_Params-004](parameters-tab-templates-and-category-parameters.md) (52)

**Duplicate judgement:** Keep · Name differing only in letter case is a different class from UI-Part_Params-005's exact duplicate (and its outcome is open in Q-Part_Params-02), and a different rule from UI-Part_Params-004's whitespace Name · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-007: A template with Units that are not a valid physical unit is rejected.

| Field | Value |
|---|---|
| **Summary** | A template with Units that are not a valid physical unit is rejected. |
| **Requirement** | `R-Part_Params-05` ([concepts-parameters.md#L36](../../requirements/docs/concepts-parameters.md#L36)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: unit not a physical unit) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: None; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Open the *Parameters* tab and press *New Parameter*. | None | The template form opens with Name (required) and Units (optional) fields (R-Part_Params-10). Open: Q-Part_Params-01 (labels of the other fields). |
| 3 | Enter a name and an invalid unit, then press *Submit*. | Name: `QA-<suffix> BadUnit`<br>Units: `notaunit` | The template is not saved: units must be a valid physical unit (R-Part_Params-05). Open: Q-Part_Params-03 (error text and whether it is shown on the Units field). |

**Postconditions and cleanup:** None; if the template was created, delete it as `admin`.

**Notes:** None

**Duplicate check:** 60 · Review · matches: [UI-Part_Params-008](parameters-tab-templates-and-category-parameters.md) (60)

**Duplicate judgement:** Keep · A string that is no unit at all (`notaunit`) vs UI-Part_Params-008's wrong-case spelling of a real unit (`OHM`), which falls under unit case sensitivity (R-Unit_measure-11) · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-008: A template Units value in the wrong letter case (`OHM`) is checked against unit syntax.

| Field | Value |
|---|---|
| **Summary** | A template Units value in the wrong letter case (`OHM`) is checked against unit syntax. |
| **Requirement** | `R-Part_Params-05` ([concepts-parameters.md#L36](../../requirements/docs/concepts-parameters.md#L36)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Error guessing (unit case) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: None; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Open the *Parameters* tab and press *New Parameter*. | None | The template form opens with Name (required) and Units (optional) fields (R-Part_Params-10). Open: Q-Part_Params-01 (labels of the other fields). |
| 3 | Enter name and units `OHM`, press *Submit*. | Name: `QA-<suffix> UpperUnit`<br>Units: `OHM` | Not known: depends on open question Q-Part_Params-03 (unit case sensitivity is covered by R-Unit_measure-07 to -11; the outcome for this form is not stated). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template(s) created (Admin Center, *Parameters* tab) after deleting any parameters that use them.

**Notes:** None

**Duplicate check:** 60 · Review · matches: [UI-Part_Params-007](parameters-tab-templates-and-category-parameters.md) (60)

**Duplicate judgement:** Keep · Wrong letter case of a valid unit (case-sensitivity class) vs UI-Part_Params-007's non-unit string: different invalid class and a different governing rule · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-009: A template with a blank Model Type is offered when adding a parameter to a part.

| Field | Value |
|---|---|
| **Summary** | A template with a blank Model Type is offered when adding a parameter to a part. |
| **Requirement** | `R-Part_Params-06` ([concepts-parameters.md#L37](../../requirements/docs/concepts-parameters.md#L37)); `R-Part_Params-12` ([concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: blank Model Type) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); `admin` for setup; Settings: None; Data: template `QA-<suffix> AnyModel` with Model Type blank (created as `admin`); part `QA-<suffix> Part`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `engineer`, open `QA-<suffix> Part`, tab *Parameters*, press *New Parameters*. | None | The *Create Parameter* form opens (R-Part_Params-12). |
| 2 | Open the *Template* selector. | None | `QA-<suffix> AnyModel` is offered: a template with a blank Model Type can be used for any model (R-Part_Params-06). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-010: A template whose Choices are `Red,Green,Blue` accepts the value `Green` on a part.

| Field | Value |
|---|---|
| **Summary** | A template whose Choices are `Red,Green,Blue` accepts the value `Green` on a part. |
| **Requirement** | `R-Part_Params-07` ([concepts-parameters.md#L38](../../requirements/docs/concepts-parameters.md#L38)); `R-Part_Params-12` ([concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: value in choices) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Colour` with Choices `Red,Green,Blue`; part `QA-<suffix> Part` (both created as `admin`); Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part's *Parameters* tab, press *New Parameters*. | None | The *Create Parameter* form opens (R-Part_Params-12). |
| 2 | Select the template and enter the data. | Template: `QA-<suffix> Colour`<br>Data: `Green` | The Data field accepts `Green` (R-Part_Params-07). Open: Q-Part_Params-06 (whether Data is a free field or a choice selector). |
| 3 | Press *Submit*. | None | The parameter `QA-<suffix> Colour` = `Green` is listed on the *Parameters* tab (R-Part_Params-12). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-011: A value that is not in the template's Choices is not accepted.

| Field | Value |
|---|---|
| **Summary** | A value that is not in the template's Choices is not accepted. |
| **Requirement** | `R-Part_Params-07` ([concepts-parameters.md#L38](../../requirements/docs/concepts-parameters.md#L38)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: value outside choices) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Colour` with Choices `Red,Green,Blue`; part `QA-<suffix> Part`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part's *Parameters* tab, press *New Parameters*. | None | The form opens (R-Part_Params-12). |
| 2 | Select the template, enter a value outside the choices and press *Submit*. | Template: `QA-<suffix> Colour`<br>Data: `Purple` | Proposed, to confirm in Q-Part_Params-04: the parameter is not created and an error is shown, because Choices are the valid values (R-Part_Params-07). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-012: A template with Choices of exactly 5000 characters is accepted.

| Field | Value |
|---|---|
| **Summary** | A template with Choices of exactly 5000 characters is accepted. |
| **Requirement** | `R-Part_Params-34` ([concepts-parameters.md#L197](../../requirements/docs/concepts-parameters.md#L197)); `R-Part_Params-07` ([concepts-parameters.md#L38](../../requirements/docs/concepts-parameters.md#L38)) |
| **Area** | Part_Params |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (on the limit: 5000 characters) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: Choices text of exactly 5000 characters, e.g. `v0001,v0002,...` cut to 5000; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Open the *Parameters* tab and press *New Parameter*. | None | The template form opens with Name (required) and Units (optional) fields (R-Part_Params-10). Open: Q-Part_Params-01 (labels of the other fields). |
| 3 | Enter name and Choices of 5000 characters; press *Submit*. | Name: `QA-<suffix> Long5000`<br>Choices: 5000 characters | The template is saved: choices are limited to 5000 characters (R-Part_Params-34). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template(s) created (Admin Center, *Parameters* tab) after deleting any parameters that use them.

**Notes:** None

**Duplicate check:** 62 · Review · matches: [UI-Part_Params-013](parameters-tab-templates-and-category-parameters.md) (62)

**Duplicate judgement:** Keep · On the 5000-character boundary (accepted) vs UI-Part_Params-013 just above it at 5001 (rejected) · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-013: A template with Choices of 5001 characters is not accepted.

| Field | Value |
|---|---|
| **Summary** | A template with Choices of 5001 characters is not accepted. |
| **Requirement** | `R-Part_Params-34` ([concepts-parameters.md#L197](../../requirements/docs/concepts-parameters.md#L197)) |
| **Area** | Part_Params |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (just above the limit: 5001 characters) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: Choices text of exactly 5001 characters; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Open the *Parameters* tab and press *New Parameter*. | None | The template form opens with Name (required) and Units (optional) fields (R-Part_Params-10). Open: Q-Part_Params-01 (labels of the other fields). |
| 3 | Enter name and Choices of 5001 characters; press *Submit*. | Name: `QA-<suffix> Long5001`<br>Choices: 5001 characters | The template is not saved with 5001 characters, as choices are limited to 5000 (R-Part_Params-34). Open: Q-Part_Params-05 (error text; whether the field blocks typing past 5000). |

**Postconditions and cleanup:** None; if the template was created, delete it as `admin`.

**Notes:** None

**Duplicate check:** 62 · Review · matches: [UI-Part_Params-012](parameters-tab-templates-and-category-parameters.md) (62)

**Duplicate judgement:** Keep · Just above the boundary at 5001 characters (not saved) vs UI-Part_Params-012 on the boundary at 5000 (saved) · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-014: A Checkbox template takes the value true on a part.

| Field | Value |
|---|---|
| **Summary** | A Checkbox template takes the value true on a part. |
| **Requirement** | `R-Part_Params-08` ([concepts-parameters.md#L39](../../requirements/docs/concepts-parameters.md#L39)); `R-Part_Params-12` ([concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: checkbox template) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Flag` with Checkbox set; part `QA-<suffix> Part`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part's *Parameters* tab, press *New Parameters* and select the template. | Template: `QA-<suffix> Flag` | The form accepts the template (R-Part_Params-12). Open: Q-Part_Params-06 (what the Data control looks like for a checkbox template). |
| 2 | Set the value to true and press *Submit*. | Data: true | The parameter is created with the value *true* (R-Part_Params-08). Open: Q-Part_Params-06 (displayed text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-015: A Checkbox template does not store a text value such as `maybe`.

| Field | Value |
|---|---|
| **Summary** | A Checkbox template does not store a text value such as `maybe`. |
| **Requirement** | `R-Part_Params-08` ([concepts-parameters.md#L39](../../requirements/docs/concepts-parameters.md#L39)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: non-boolean value) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Flag` with Checkbox set; part `QA-<suffix> Part`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *New Parameters* form and select the template. | Template: `QA-<suffix> Flag` | The form opens (R-Part_Params-12). |
| 2 | Try to enter a non-boolean value and press *Submit*. | Data: `maybe` | Only *true* or *false* can be assigned (R-Part_Params-08), so `maybe` is not stored. Open: Q-Part_Params-06 (whether the control prevents typing or the form returns an error). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-016: A template with a Selection List rejects a value that is not in the list.

| Field | Value |
|---|---|
| **Summary** | A template with a Selection List rejects a value that is not in the list. |
| **Requirement** | `R-Part_Params-09` ([concepts-parameters.md#L40](../../requirements/docs/concepts-parameters.md#L40)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: value outside selection list) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: selection list `QA-<suffix> List` with entries `A`,`B` (created via API as `admin`); template `QA-<suffix> Sel` linked to it; part `QA-<suffix> Part`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *New Parameters* form and select the template. | Template: `QA-<suffix> Sel` | The form opens (R-Part_Params-12). Open: Q-Part_Params-06 (Data control for a selection-list template). |
| 2 | Enter a value not in the list and press *Submit*. | Data: `C` | Only values from the linked selection list can be assigned (R-Part_Params-09), so `C` is not stored. Open: Q-Part_Params-06 (error or prevented input). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s). Delete the selection list via API as `admin`.

**Notes:** None

---

### UI-Part_Params-017: An admin edits an existing template's description with its Edit button.

| Field | Value |
|---|---|
| **Summary** | An admin edits an existing template's description with its Edit button. |
| **Requirement** | `R-Part_Params-11` ([concepts-parameters.md#L57](../../requirements/docs/concepts-parameters.md#L57)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | State transition (template edited) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: template `QA-<suffix> Tpl`, created as `admin`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Open the *Parameters* tab, find `QA-<suffix> Tpl` and press its *Edit* button. | None | The edit form opens with the current values (R-Part_Params-11). Open: Q-Part_Params-01 (tab location). |
| 3 | Change the Description and press *Submit*. | Description: `Edited by QA` | The list row shows the new Description (R-Part_Params-11). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template(s) created (Admin Center, *Parameters* tab) after deleting any parameters that use them.

**Notes:** None

---

### UI-Part_Params-018: Renaming a template to the name of another template is rejected.

| Field | Value |
|---|---|
| **Summary** | Renaming a template to the name of another template is rejected. |
| **Requirement** | `R-Part_Params-11` ([concepts-parameters.md#L57](../../requirements/docs/concepts-parameters.md#L57)); `R-Part_Params-03` ([concepts-parameters.md#L34](../../requirements/docs/concepts-parameters.md#L34)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Error guessing (rename to duplicate) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: templates `QA-<suffix> A` and `QA-<suffix> B`, created as `admin`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `admin` and open the Admin Center. | None | The Admin Center opens. Open: Q-Part_Params-01 (docs say Admin Center at L47 but the *Settings* page at L51). |
| 2 | Edit `QA-<suffix> B` and set its name to that of `QA-<suffix> A`; press *Submit*. | Name: `QA-<suffix> A` | The change is not saved: template names must be unique (R-Part_Params-03). Open: Q-Part_Params-02 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template(s) created (Admin Center, *Parameters* tab) after deleting any parameters that use them.

**Notes:** None

---

### UI-Part_Params-019: A view-only user cannot create templates.

| Field | Value |
|---|---|
| **Summary** | A view-only user cannot create templates. |
| **Requirement** | `R-Part_Params-10` ([concepts-parameters.md#L47-L55](../../requirements/docs/concepts-parameters.md#L47-L55)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Negative (blocked user: `reader`) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: None; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `reader` and try to open the Admin Center. | None | Not known: depends on open question Q-Part_Params-09 (whether the Admin Center entry is hidden or the page refuses access). |
| 2 | If the templates list is reachable, look for *New Parameter*. | None | Proposed, to confirm in Q-Part_Params-09: no *New Parameter* or *Edit* control is available to `reader`. |

**Postconditions and cleanup:** None.

**Notes:** None

---

### UI-Part_Params-020: With no uniqueness (default), the same value can be used on two parts.

| Field | Value |
|---|---|
| **Summary** | With no uniqueness (default), the same value can be used on two parts. |
| **Requirement** | `R-Part_Params-13` ([concepts-parameters.md#L77-L81](../../requirements/docs/concepts-parameters.md#L77-L81)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Decision table (Unique = no uniqueness required) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> U` with Unique = No uniqueness required (default); parts `QA-<suffix> P1` and `QA-<suffix> P2`; P1 already has the parameter `ABC123` (created as `admin`); Pre-steps: None |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> P2`, tab *Parameters*, press *New Parameters*. | None | The form opens (R-Part_Params-12). |
| 2 | Select the template, enter the value and press *Submit*. | Template: `QA-<suffix> U`<br>Data: `ABC123` | The parameter is created: no restriction is placed on parameter values (R-Part_Params-13). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-021: With Unique for model type, the same value on a second part is rejected.

| Field | Value |
|---|---|
| **Summary** | With Unique for model type, the same value on a second part is rejected. |
| **Requirement** | `R-Part_Params-13` ([concepts-parameters.md#L77-L81](../../requirements/docs/concepts-parameters.md#L77-L81)); `R-Part_Params-15` ([concepts-parameters.md#L86](../../requirements/docs/concepts-parameters.md#L86)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Decision table (Unique = unique for model type, duplicate within model) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> U` with Unique = Unique for model type; parts `QA-<suffix> P1` and `QA-<suffix> P2`; P1 already has the parameter `ABC123` (created as `admin`); Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> P2`, tab *Parameters*, press *New Parameters*. | None | The form opens (R-Part_Params-12). |
| 2 | Select the template, enter the value and press *Submit*. | Template: `QA-<suffix> U`<br>Data: `ABC123` | The parameter is not created: the value breaks the uniqueness rule (R-Part_Params-13, R-Part_Params-15). Open: Q-Part_Params-07 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

**Duplicate check:** 93 · Duplicate · matches: [UI-Part_Params-022](parameters-tab-templates-and-category-parameters.md) (93), [UI-Part_Params-023](parameters-tab-templates-and-category-parameters.md) (59), [UI-Part_Params-024](parameters-tab-templates-and-category-parameters.md) (54)

**Duplicate judgement:** Keep · Different decision-table column (template Unique = Unique for model type vs UI-Part_Params-022's Globally unique), and different rules and value classes from UI-Part_Params-023 (case variant) and UI-Part_Params-024 (unit-normalised value) · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-022: With Globally unique, the same value on a second part is rejected.

| Field | Value |
|---|---|
| **Summary** | With Globally unique, the same value on a second part is rejected. |
| **Requirement** | `R-Part_Params-13` ([concepts-parameters.md#L77-L81](../../requirements/docs/concepts-parameters.md#L77-L81)); `R-Part_Params-15` ([concepts-parameters.md#L86](../../requirements/docs/concepts-parameters.md#L86)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Decision table (Unique = globally unique) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> U` with Unique = Globally unique; parts `QA-<suffix> P1` and `QA-<suffix> P2`; P1 already has the parameter `ABC123` (created as `admin`); Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> P2`, tab *Parameters*, press *New Parameters*. | None | The form opens (R-Part_Params-12). |
| 2 | Select the template, enter the value and press *Submit*. | Template: `QA-<suffix> U`<br>Data: `ABC123` | The parameter is not created: the value breaks the uniqueness rule (R-Part_Params-13, R-Part_Params-15). Open: Q-Part_Params-07 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

**Duplicate check:** 93 · Duplicate · matches: [UI-Part_Params-021](parameters-tab-templates-and-category-parameters.md) (93), [UI-Part_Params-023](parameters-tab-templates-and-category-parameters.md) (59), [UI-Part_Params-024](parameters-tab-templates-and-category-parameters.md) (54)

**Duplicate judgement:** Keep · Different decision-table column (template Unique = Globally unique vs UI-Part_Params-021's Unique for model type), and different rules and value classes from UI-Part_Params-023 and UI-Part_Params-024 · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-023: Uniqueness is case-insensitive: `abc123` duplicates `ABC123`.

| Field | Value |
|---|---|
| **Summary** | Uniqueness is case-insensitive: `abc123` duplicates `ABC123`. |
| **Requirement** | `R-Part_Params-14` ([concepts-parameters.md#L84](../../requirements/docs/concepts-parameters.md#L84)); `R-Part_Params-15` ([concepts-parameters.md#L86](../../requirements/docs/concepts-parameters.md#L86)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: duplicate differing in case) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> U` with Unique = Globally unique; parts `QA-<suffix> P1` and `QA-<suffix> P2`; P1 already has the parameter `ABC123` (created as `admin`); Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> P2`, tab *Parameters*, press *New Parameters*. | None | The form opens (R-Part_Params-12). |
| 2 | Select the template, enter the value and press *Submit*. | Template: `QA-<suffix> U`<br>Data: `abc123` | The parameter is not created: `ABC123` and `abc123` are duplicates (R-Part_Params-14, R-Part_Params-15). Open: Q-Part_Params-07 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

**Duplicate check:** 59 · Review · matches: [UI-Part_Params-021](parameters-tab-templates-and-category-parameters.md) (59), [UI-Part_Params-022](parameters-tab-templates-and-category-parameters.md) (59), [UI-Part_Params-024](parameters-tab-templates-and-category-parameters.md) (56)

**Duplicate judgement:** Keep · Tests case-insensitive matching (R-Part_Params-14) with a value differing only in case (`abc123` vs existing `ABC123`), a different rule and value class from the exact duplicates in UI-Part_Params-021/022 and the unit-normalised value in UI-Part_Params-024 · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-024: On a template with units `ohm`, `1k` duplicates an existing `1000`.

| Field | Value |
|---|---|
| **Summary** | On a template with units `ohm`, `1k` duplicates an existing `1000`. |
| **Requirement** | `R-Part_Params-16` ([concepts-parameters.md#L90-L92](../../requirements/docs/concepts-parameters.md#L90-L92)); `R-Part_Params-15` ([concepts-parameters.md#L86](../../requirements/docs/concepts-parameters.md#L86)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: same numeric value, different notation) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> U` with Unique = Globally unique and Units `ohm`; parts `QA-<suffix> P1` and `QA-<suffix> P2`; P1 already has the parameter `1000` (created as `admin`); Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> P2`, tab *Parameters*, press *New Parameters*. | None | The form opens (R-Part_Params-12). |
| 2 | Select the template, enter the value and press *Submit*. | Template: `QA-<suffix> U`<br>Data: `1k` | The parameter is not created: the normalised numeric values are equal (R-Part_Params-16, R-Part_Params-15). Open: Q-Part_Params-07 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

**Duplicate check:** 56 · Review · matches: [UI-Part_Params-023](parameters-tab-templates-and-category-parameters.md) (56), [UI-Part_Params-021](parameters-tab-templates-and-category-parameters.md) (54), [UI-Part_Params-022](parameters-tab-templates-and-category-parameters.md) (54)

**Duplicate judgement:** Keep · Template with units `ohm` and a value equal only after normalisation (`1k` vs `1000`, R-Part_Params-16): different starting state and rule from UI-Part_Params-021/022/023, whose templates have no units · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-025: On a unique template without units, `1k` and `1000` are different text and both accepted.

| Field | Value |
|---|---|
| **Summary** | On a unique template without units, `1k` and `1000` are different text and both accepted. |
| **Requirement** | `R-Part_Params-17` ([concepts-parameters.md#L94](../../requirements/docs/concepts-parameters.md#L94)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: no units, raw text differs) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> U` with Unique = Globally unique (no Units); parts `QA-<suffix> P1` and `QA-<suffix> P2`; P1 already has the parameter `1000` (created as `admin`); Pre-steps: None |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> P2`, tab *Parameters*, press *New Parameters*. | None | The form opens (R-Part_Params-12). |
| 2 | Select the template, enter the value and press *Submit*. | Template: `QA-<suffix> U`<br>Data: `1k` | The parameter is created: without units the raw text is compared, and `1k` differs from `1000` (R-Part_Params-17). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-026: Duplicating a part skips the parameters of unique templates.

| Field | Value |
|---|---|
| **Summary** | Duplicating a part skips the parameters of unique templates. |
| **Requirement** | `R-Part_Params-18` ([concepts-parameters.md#L98-L100](../../requirements/docs/concepts-parameters.md#L98-L100)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | What-if business scenario (duplicate a part that has a unique parameter) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Src` with two parameters: one from a unique template `QA-<suffix> U` (`ABC123`), one from a non-unique template `QA-<suffix> N` (`5`); Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> Src` and start the duplicate-part action. | None | The *Duplicate Part* form opens. Open: Q-Part_Params-13 (action and option labels for copying parameters). |
| 2 | Enable copying of parameters, enter a new name and press *Submit*. | Name: `QA-<suffix> Copy` | The new part is created. |
| 3 | Open the new part's *Parameters* tab. | None | `QA-<suffix> N` = `5` is present; no parameter exists for `QA-<suffix> U`, which can be added manually with a distinct value (R-Part_Params-18). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-027: The Parameters tab lists all parameters of a part.

| Field | Value |
|---|---|
| **Summary** | The Parameters tab lists all parameters of a part. |
| **Requirement** | `R-Part_Params-02` ([concepts-parameters.md#L24](../../requirements/docs/concepts-parameters.md#L24)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: part with several parameters) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: part `QA-<suffix> Part` with parameters from templates `QA-<suffix> T1` (`10`) and `QA-<suffix> T2` (`20`), created as `admin`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `reader`, open `QA-<suffix> Part` and select the *Parameters* tab. | None | The tab lists both parameters, with their template and value (R-Part_Params-02). Open: Q-Part_Params-09 (columns shown). |
| 2 | Look for add, edit and delete controls. | None | Proposed, to confirm in Q-Part_Params-09: none are shown to `reader`. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-028: A part with no parameters shows an empty Parameters tab.

| Field | Value |
|---|---|
| **Summary** | A part with no parameters shows an empty Parameters tab. |
| **Requirement** | `R-Part_Params-02` ([concepts-parameters.md#L24](../../requirements/docs/concepts-parameters.md#L24)) |
| **Area** | Part_Params |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (zero parameters) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Part` with no parameters; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-10 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part and select the *Parameters* tab. | None | The tab opens and lists no parameters (R-Part_Params-02). Open: Q-Part_Params-10 (empty-state text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-029: An engineer adds a parameter to a part from the Parameters tab.

| Field | Value |
|---|---|
| **Summary** | An engineer adds a parameter to a part from the Parameters tab. |
| **Requirement** | `R-Part_Params-12` ([concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: template and data) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`); part `QA-<suffix> Part`; both created as `admin`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-10 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part, tab *Parameters*, press *New Parameters*. | None | The *Create Parameter* form is displayed (R-Part_Params-12). |
| 2 | Select the template and fill the Data field. | Template: `QA-<suffix> Resistance`<br>Data: `100` | Fields accept the values. |
| 3 | Press *Submit*. | None | The form closes and the parameter `QA-<suffix> Resistance` with value `100` appears in the *Parameters* tab (R-Part_Params-12). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-030: The Create Parameter form cannot be submitted without a template.

| Field | Value |
|---|---|
| **Summary** | The Create Parameter form cannot be submitted without a template. |
| **Requirement** | `R-Part_Params-12` ([concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty template) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Part`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-10 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *New Parameters* form, leave Template empty, enter Data and press *Submit*. | Template: empty<br>Data: `5` | Proposed, to confirm in Q-Part_Params-10: the parameter is not created and an error is shown on the Template field. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-031: A view-only user cannot add parameters to a part.

| Field | Value |
|---|---|
| **Summary** | A view-only user cannot add parameters to a part. |
| **Requirement** | `R-Part_Params-12` ([concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Negative (blocked user: `reader`) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: part `QA-<suffix> Part` (created as `admin`); Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `reader`, open the part and select the *Parameters* tab. | None | Proposed, to confirm in Q-Part_Params-09: the *New Parameters* button is not available to `reader`. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-032: A user with no permissions cannot see a part's parameters.

| Field | Value |
|---|---|
| **Summary** | A user with no permissions cannot see a part's parameters. |
| **Requirement** | `R-Part_Params-02` ([concepts-parameters.md#L24](../../requirements/docs/concepts-parameters.md#L24)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Negative (blocked user: `noaccess`) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: part `QA-<suffix> Part` with one parameter (created as `admin`); Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `noaccess` and try to open the part detail page directly. | Part detail URL for the part | Not known: depends on open question Q-Part_Params-09 (redirect, empty page or permission message). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-033: A parameter value in a compatible unit is accepted on a template with base unit `ohm`.

| Field | Value |
|---|---|
| **Summary** | A parameter value in a compatible unit is accepted on a template with base unit `ohm`. |
| **Requirement** | `R-Part_Params-30` ([concepts-parameters.md#L174-L176](../../requirements/docs/concepts-parameters.md#L174-L176)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: compatible unit) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`); part `QA-<suffix> Part`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a parameter with the template and data `4.7k`. | Template: `QA-<suffix> Resistance`<br>Data: `4.7k` | The parameter is created: compatible units are accepted and converted (R-Part_Params-30). Open: Q-Part_Params-11 (value shown in the tab: as entered or converted). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-034: A parameter value with incompatible units is rejected.

| Field | Value |
|---|---|
| **Summary** | A parameter value with incompatible units is rejected. |
| **Requirement** | `R-Part_Params-31` ([concepts-parameters.md#L183](../../requirements/docs/concepts-parameters.md#L183)), `R-Part_Params-32` ([concepts-parameters.md#L187](../../requirements/docs/concepts-parameters.md#L187)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: incompatible unit), Decision table (validation on x incompatible unit) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: unit validation = on [open: Q-Part_Params-14, setting name and default]; Data: template `QA-<suffix> Resistance` (Units `ohm`); part `QA-<suffix> Part`; Pre-steps: setting changed by `admin` in the UI [open: Q-Part_Params-14, where the setting is changed] |
| **Automation** | Partial: setting name, location, error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-07, Q-Part_Params-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a parameter with the template and data in volts. | Template: `QA-<suffix> Resistance`<br>Data: `5 V` | The parameter is not created: units incompatible with the template are rejected (R-Part_Params-31). Open: Q-Part_Params-07 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, delete the template(s), then restore the unit validation setting to its original state.

**Notes:** The setting's name and default are not stated (index doc issue 8); the case sets it explicitly (Q-Part_Params-14). Merged with the former UI-Part_Params-046 (same rule, user, data and outcome) on the architect's decision, 2026-10-15.

---

### UI-Part_Params-035: Parameters cannot be added to a locked part.

| Field | Value |
|---|---|
| **Summary** | Parameters cannot be added to a locked part. |
| **Requirement** | `R-ATT-26` ([part-index.md#L110](../../requirements/docs/part-index.md#L110)); `R-Part_Params-12` ([concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | State transition (unlocked to locked, blocked action) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `Part Locking` enabled [open: Q-ATT-02, setting label and default]; Data: part `QA-<suffix> Part` that is locked; template `QA-<suffix> Tpl`; Pre-steps: [open: Q-ATT-01, how the part is locked] |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-02, Q-ATT-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the locked part, tab *Parameters*. | None | The tab opens (R-Part_Params-02). |
| 2 | Try to add a parameter. | Template: `QA-<suffix> Tpl`<br>Data: `1` | No parameter is created: parameters of a locked part cannot be created (R-ATT-26). Open: Q-ATT-14 (hidden, disabled or rejected, and the message). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** Depends on the open questions Q-ATT-01, Q-ATT-02 (how and with which setting a part is locked).

---

### UI-Part_Params-036: A template is linked to a category with a default value.

| Field | Value |
|---|---|
| **Summary** | A template is linked to a category with a default value. |
| **Requirement** | `R-Part_Params-19` ([concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: template and default value) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: category `QA-<suffix> Cat`; template `QA-<suffix> Tpl`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the category, find where templates are linked, and link the template with a default value. | Template: `QA-<suffix> Tpl`<br>Default value: `42` | The template is linked to the category with its default value (R-Part_Params-19). Open: Q-Part_Params-08 (tab, button and field labels). |

**Postconditions and cleanup:** Cleanup as `admin`: remove the link, delete the category and the template.

**Notes:** None

---

### UI-Part_Params-037: A new part created in the category gets the template's default value.

| Field | Value |
|---|---|
| **Summary** | A new part created in the category gets the template's default value. |
| **Requirement** | `R-Part_Params-19` ([concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: part in the category) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Cat` with template `QA-<suffix> Tpl` linked and default value `42` (linked as `admin`); Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a part in `QA-<suffix> Cat` with the *Create Part* form. | Name: `QA-<suffix> Part`<br>Category: `QA-<suffix> Cat` | The part is created and its detail page opens. |
| 2 | Open the *Parameters* tab. | None | The parameter `QA-<suffix> Tpl` is listed with the value `42` (R-Part_Params-19). Open: Q-Part_Params-08 (whether it is created at once). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

**Duplicate check:** 56 · Review · matches: [UI-Part_Params-038](parameters-tab-templates-and-category-parameters.md) (56)

**Duplicate judgement:** Keep · Part created directly in the linked category vs UI-Part_Params-038's part in a sub-category: separate clauses of R-Part_Params-19 · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-038: A new part created in a sub-category inherits the default value.

| Field | Value |
|---|---|
| **Summary** | A new part created in a sub-category inherits the default value. |
| **Requirement** | `R-Part_Params-19` ([concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104)) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: sub-category) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Cat` with template `QA-<suffix> Tpl` linked and default value `42` (linked as `admin`); sub-category `QA-<suffix> Sub` under it; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a part in `QA-<suffix> Sub`. | Name: `QA-<suffix> SubPart`<br>Category: `QA-<suffix> Sub` | The part is created. |
| 2 | Open the *Parameters* tab. | None | The parameter `QA-<suffix> Tpl` is listed with the value `42`: the default applies to a category or its sub-category (R-Part_Params-19). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

**Duplicate check:** 56 · Review · matches: [UI-Part_Params-037](parameters-tab-templates-and-category-parameters.md) (56)

**Duplicate judgement:** Keep · Part created in a sub-category (inheritance clause "or a sub-category" of R-Part_Params-19) vs UI-Part_Params-037's part in the linked category itself · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-039: A new part in a different category gets no default value.

| Field | Value |
|---|---|
| **Summary** | A new part in a different category gets no default value. |
| **Requirement** | `R-Part_Params-19` ([concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: part outside the category) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Cat` with template `QA-<suffix> Tpl` linked and default value `42` (linked as `admin`); other category `QA-<suffix> Other` with no links; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a part in `QA-<suffix> Other`. | Name: `QA-<suffix> OtherPart`<br>Category: `QA-<suffix> Other` | The part is created. |
| 2 | Open the *Parameters* tab. | None | No parameter `QA-<suffix> Tpl` is listed: the default applies only to parts in the linked category or its sub-categories (R-Part_Params-19). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-040: A part that already exists in the category is not given the default value when the link is added.

| Field | Value |
|---|---|
| **Summary** | A part that already exists in the category is not given the default value when the link is added. |
| **Requirement** | `R-Part_Params-19` ([concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | What-if business scenario (link added after parts exist) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, Admin Center access); Settings: None; Data: category `QA-<suffix> Cat` with existing part `QA-<suffix> Old`; template `QA-<suffix> Tpl`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-08, Q-Part_Params-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the category, find where templates are linked, and link the template with a default value. | Template: `QA-<suffix> Tpl`<br>Default value: `42` | The template is linked to the category with its default value (R-Part_Params-19). Open: Q-Part_Params-08 (tab, button and field labels). |
| 2 | Open `QA-<suffix> Old`, tab *Parameters*. | None | Proposed, to confirm in Q-Part_Params-12: no parameter is added, because the default applies to new parts (R-Part_Params-19). |

**Postconditions and cleanup:** Cleanup as `admin`: remove the link, set the part inactive and delete it, delete the category and the template.

**Notes:** None

---

### UI-Part_Params-041: A category default is not applied for a template that has a uniqueness requirement.

| Field | Value |
|---|---|
| **Summary** | A category default is not applied for a template that has a uniqueness requirement. |
| **Requirement** | `R-Part_Params-20` ([concepts-parameters.md#L108](../../requirements/docs/concepts-parameters.md#L108)); `R-Part_Params-13` ([concepts-parameters.md#L77-L81](../../requirements/docs/concepts-parameters.md#L77-L81)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Decision table (category link x Unique = globally unique) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Cat` with template `QA-<suffix> Uniq` (Unique = globally unique) linked with default `42`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create two parts in the category. | Names: `QA-<suffix> P1`, `QA-<suffix> P2` | Both parts are created; no uniqueness error appears (R-Part_Params-20). |
| 2 | Open the *Parameters* tab of each part. | None | Neither part has a parameter for `QA-<suffix> Uniq`: the default is not applied for a template with a uniqueness requirement (R-Part_Params-20). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the parameters, set the part(s) inactive and delete them, delete the category, then delete the template(s).

**Notes:** None

---

### UI-Part_Params-042: A view-only user cannot link templates to a category.

| Field | Value |
|---|---|
| **Summary** | A view-only user cannot link templates to a category. |
| **Requirement** | `R-Part_Params-19` ([concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104)) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Negative (blocked user: `reader`) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: category `QA-<suffix> Cat`; Pre-steps: None |
| **Automation** | Partial: error texts and control labels are open questions. |
| **Review** | Draft · Open question: Q-Part_Params-08, Q-Part_Params-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `reader` and open the category. | None | The category opens. |
| 2 | Look for the control that links a template to the category. | None | Proposed, to confirm in Q-Part_Params-08: the control is not available to `reader`. Open: Q-Part_Params-09 (read-only view of existing links). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the category.

**Notes:** None

---
