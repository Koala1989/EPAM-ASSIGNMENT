# Part creation form validation: Part test cases

### UI-Part-042: Submit is blocked when Name is empty

| Field | Value |
|---|---|
| **Summary** | Submitting the *Create Part* form with the Name field empty is blocked by a form error and no part is created. |
| **Requirement** | `R-Part-05`. Source: [part-create.md#L31](../../requirements/docs/part-create.md#L31). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: required field empty), Negative |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: core form validation. |
| **Review** | Draft · Open question: Q-Part-13, Q-REV-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Leave Name empty and fill the Description. | Name: empty<br>Description: `QA-<suffix> description` | No value in Name. |
| 2 | Press *Submit*. | None | The form cannot be submitted: it stays open on the same page (R-Part-05). No part is created (R-Part-05). Open: Q-Part-13 (the error text, where it is shown, and whether *Submit* is disabled or the error appears on submit). |
| 3 | Search the *Parts* view for `QA-<suffix> description`. | None | No part with that description exists. |

**Postconditions and cleanup:** no part is created. Check by searching the *Parts* view for `QA-<suffix> description`: no result. Nothing to clean up.

**Notes:** Name is the only input-required field per the schema (index Schema issue 4); the docs do not list required fields (index Not in docs 9, Q-REV-05).

---

### UI-Part-043: Whitespace-only Name is not accepted

| Field | Value |
|---|---|
| **Summary** | A Name made only of spaces is treated like an empty Name when the form is submitted. |
| **Requirement** | `R-Part-05`. Source: [part-create.md#L31](../../requirements/docs/part-create.md#L31). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Error guessing (whitespace-only text) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: simple form check. |
| **Review** | Draft · Open question: Q-Part-14, Q-Part-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter spaces only in Name. | Name: 5 space characters | The field shows the spaces. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-14: the form is not submitted and no part is created. Open: Q-Part-13 (the error text, where it is shown, and whether *Submit* is disabled or the error appears on submit). |

**Postconditions and cleanup:** no part is created (proposed). If a part with a blank Name was created, cleanup as `admin`: set it inactive, then delete it.

**Notes:** The docs do not say whether whitespace-only text is trimmed or rejected.

---

### UI-Part-044: Name of exactly 100 characters is accepted

| Field | Value |
|---|---|
| **Summary** | A Name on the maximum length limit (100 characters) can be submitted. |
| **Requirement** | `R-Part-05`. Source: [part-create.md#L31](../../requirements/docs/part-create.md#L31). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (max length) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: boundary check. |
| **Review** | Draft · Open question: Q-Part-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name. | Name: 100 characters (`QA-<suffix>-` followed by `N` characters up to a total of 100) | The field accepts the value. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-15: the form closes and the browser goes to the new part's detail page; the schema allows up to 100 characters. |
| 3 | Check the detail page header. | None | Proposed, to confirm in Q-Part-15: the Name shows all 100 characters. |

**Postconditions and cleanup:** one new part `with the 100-character name` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** The limit comes from the schema, not from the UI docs (Q-Part-15).

**Duplicate check:** 50 · Review · matches: [UI-Part-045](part-creation-form-validation.md) (50), [UI-Part-054](part-creation-form-validation.md) (50)

**Duplicate judgement:** Keep · Differs from UI-Part-045 by boundary side (on the 100 limit, accepted, vs 101, rejected) and from UI-Part-054 by field (Name vs IPN, different rule R-Part-05/13 vs R-Part-12) · test-case-reviewer, 2026-10-15

---

### UI-Part-045: Name of 101 characters is not accepted

| Field | Value |
|---|---|
| **Summary** | A Name one character over the maximum length (101 characters) is not saved. |
| **Requirement** | `R-Part-05`. Source: [part-create.md#L31](../../requirements/docs/part-create.md#L31). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (max length + 1) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: boundary check. |
| **Review** | Draft · Open question: Q-Part-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name. | Name: 101 characters (`QA-<suffix>-` followed by `N` characters up to a total of 101) | Proposed, to confirm in Q-Part-15: the field accepts the input, or blocks typing beyond 100 characters. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-15: the form shows an error on Name, stays open, and no part is created. The API schema limits Name to 100 characters (`maxLength 100`); a form that shows errors cannot be submitted (R-Part-05). No doc states how the form handles a longer value. Open: Q-Part-15 (the error text, or whether the field stops input at 100 characters, in which case a part is created with the first 100 characters). |

**Postconditions and cleanup:** Proposed (Q-Part-15): no part is created. Check by searching the *Parts* view for `QA-<suffix>-`. If a part was created (input cut at the limit), cleanup as `admin`: set it inactive, then delete it.

**Notes:** The limit comes from the schema, not from the UI docs (Q-Part-15).

**Duplicate check:** 55 · Review · matches: [UI-Part-055](part-creation-form-validation.md) (55), [UI-Part-044](part-creation-form-validation.md) (50)

**Duplicate judgement:** Keep · Differs from UI-Part-055 by field and rule (Name, R-Part-05, vs IPN, R-Part-12) and from UI-Part-044 by boundary side and outcome (101 rejected vs 100 accepted) · test-case-reviewer, 2026-10-15

---

### UI-Part-046: Name with special characters and Unicode is accepted

| Field | Value |
|---|---|
| **Summary** | A Name containing punctuation, symbols and non-ASCII letters is saved and shown unchanged. |
| **Requirement** | `R-Part-05`. Source: [part-create.md#L31](../../requirements/docs/part-create.md#L31). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Error guessing (special characters, Unicode) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: simple form check. |
| **Review** | Draft · Open question: Q-Part-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name. | Name: `QA-<suffix> Ø10 ±5% <R&D> "x" é 抵抗` | The field accepts the value. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-14: the form closes and the browser goes to the new part's detail page. |
| 3 | Check the detail page header. | None | Proposed, to confirm in Q-Part-14: the Name shows exactly the text entered, with no escaped or stripped characters. |

**Postconditions and cleanup:** one new part `QA-<suffix> Ø10 ...` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** None.

---

### UI-Part-047: A second part with the same Name, IPN and Revision is not created

| Field | Value |
|---|---|
| **Summary** | Creating a part whose Name, IPN and Revision all equal those of an existing part is blocked. |
| **Requirement** | `R-Part-13`. Source: [part-views.md#L32](../../requirements/docs/part-views.md#L32). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: duplicate), Negative |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Existing` with IPN `QA-<suffix>-IPN1` and no Revision, created as `admin` via `POST /api/part/`; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: data integrity check. |
| **Review** | Draft · Open question: Q-Part-16 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the form with the same Name and IPN as the existing part. | Name: `QA-<suffix> Existing`<br>IPN: `QA-<suffix>-IPN1` | The fields accept the values. |
| 2 | Press *Submit*. | None | The part is not created: the Name is unique (R-Part-13). Open: Q-Part-16 (error text, which field shows it, and whether the form stays open). |

**Postconditions and cleanup:** only `QA-<suffix> Existing` exists. Cleanup as `admin`: set it inactive, then delete it.

**Notes:** Doc issue 2: the scope of 'unique' is unclear. The case uses identical Name, IPN and Revision so any reading of the rule rejects it. Finding F-04 shows the app treats Name together with IPN and Revision as the key (an app observation, not a requirement).

---

### UI-Part-048: A part with an existing Name but a different IPN

| Field | Value |
|---|---|
| **Summary** | Creating a part with the same Name as an existing part but a different IPN: the outcome depends on the scope of Name uniqueness. |
| **Requirement** | `R-Part-13`, `R-Part-12`. Source: [part-views.md#L32](../../requirements/docs/part-views.md#L32), [part-views.md#L30](../../requirements/docs/part-views.md#L30). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Decision table (Name same, IPN different), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Existing` with IPN `QA-<suffix>-IPN1`, created as `admin` via `POST /api/part/`; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: after Q-Part-16 is answered. |
| **Review** | Draft · Open question: Q-Part-16 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the form with the existing Name and a new IPN. | Name: `QA-<suffix> Existing`<br>IPN: `QA-<suffix>-IPN2` | The fields accept the values. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-16: the part is created and the browser goes to its detail page. Open: Q-Part-16 (if Name is globally unique per R-Part-13, the part is not created, error text unknown). |

**Postconditions and cleanup:** the part `QA-<suffix> Existing` exists and, if created, a second part with the same Name. Cleanup as `admin`: set each part created by this case inactive, then delete it.

**Notes:** Doc issue 2 (Conflict). Finding F-04 suggests acceptance in 1.5.6 (app observation, not a requirement).

---

### UI-Part-049: A part with an existing Name and IPN but a different Revision

| Field | Value |
|---|---|
| **Summary** | Creating a part with the same Name and IPN as an existing part but a different Revision: the outcome depends on the scope of Name uniqueness. |
| **Requirement** | `R-Part-13`, `R-Part-15`, `R-REV-03`. Source: [part-views.md#L32](../../requirements/docs/part-views.md#L32), [part-views.md#L36](../../requirements/docs/part-views.md#L36), [part-revision.md#L29](../../requirements/docs/part-revision.md#L29). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199); requirements/openapi-parts.yaml `components.schemas.Part.revision` (nullable, maxLength 100, L4207-L4211) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Decision table (Name and IPN same, Revision different), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revisions enabled [open: Q-REV-01, setting name and state]; Data: part `QA-<suffix> Existing` with IPN `QA-<suffix>-IPN1` and Revision `A`, created as `admin` via `POST /api/part/`; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: after Q-Part-16 is answered. |
| **Review** | Draft · Open question: Q-Part-16, Q-Part-19, Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Find the Revision field. | None | The form shows a Revision field [open: Q-Part-19, whether the Create Part form has a Revision field and its label]. |
| 2 | Fill in the form with the existing Name and IPN and a new Revision. | Name: `QA-<suffix> Existing`<br>IPN: `QA-<suffix>-IPN1`<br>Revision: `B` | The Revision field accepts any string value (R-REV-03). |
| 3 | Press *Submit*. | None | Proposed, to confirm in Q-Part-16: the part is created and the browser goes to its detail page. Open: Q-Part-16 (if Name is globally unique per R-Part-13, the part is not created). |

**Postconditions and cleanup:** the part `QA-<suffix> Existing` exists with Revision `A`, plus the new part if created. Cleanup as `admin`: set each part created by this case inactive, then delete it.

**Notes:** Doc issue 2. Finding F-04: demo data has parts sharing Name and IPN with different revisions (app observation).

---

### UI-Part-050: A Name differing only in letter case from an existing Name

| Field | Value |
|---|---|
| **Summary** | Creating a part whose Name differs from an existing Name only by upper or lower case: the outcome depends on the case sensitivity of the uniqueness check. |
| **Requirement** | `R-Part-13`. Source: [part-views.md#L32](../../requirements/docs/part-views.md#L32). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Error guessing (case variant), Equivalence partitioning |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Existing` with IPN `QA-<suffix>-IPN1`, created as `admin` via `POST /api/part/`; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: after Q-Part-16 is answered. |
| **Review** | Draft · Open question: Q-Part-16 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the form with the existing Name in upper case and the same IPN. | Name: `QA-<SUFFIX> EXISTING`<br>IPN: `QA-<suffix>-IPN1` | The fields accept the values. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-16: the part is not created, as the Name is unique (R-Part-13). Open: Q-Part-16 (whether the check is case-sensitive). |

**Postconditions and cleanup:** the part `QA-<suffix> Existing` exists and, if created, the upper-case part. Cleanup as `admin`: set each part created by this case inactive, then delete it.

**Notes:** None.

---

### UI-Part-051: Part is created with an empty Description

| Field | Value |
|---|---|
| **Summary** | The Description field left empty does not block the submit. |
| **Requirement** | `R-Part-14`. Source: [part-views.md#L34](../../requirements/docs/part-views.md#L34). Schema: requirements/openapi-parts.yaml `components.schemas.Part.description` (optional, maxLength 250, L4148-L4151) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: optional field empty) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: simple form check. |
| **Review** | Draft · Open question: Q-Part-18 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name only; leave Description empty. | Name: `QA-<suffix> NoDesc`<br>Description: empty | No form error is shown on Description [open: Q-Part-18, whether Description is required on the form]. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-18: the form closes and the browser goes to the new part's detail page; Description is empty. |

**Postconditions and cleanup:** one new part `QA-<suffix> NoDesc` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** The docs do not state if Description is required (R-Part-14 note). The schema marks it optional.

---

### UI-Part-052: Description of exactly 250 characters is accepted

| Field | Value |
|---|---|
| **Summary** | A Description on the maximum length limit (250 characters) can be submitted. |
| **Requirement** | `R-Part-14`. Source: [part-views.md#L34](../../requirements/docs/part-views.md#L34). Schema: requirements/openapi-parts.yaml `components.schemas.Part.description` (optional, maxLength 250, L4148-L4151) |
| **Area** | Part |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (max length) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: boundary check. |
| **Review** | Draft · Open question: Q-Part-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and Description. | Name: `QA-<suffix> Desc250`<br>Description: 250 characters | The fields accept the values. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-15: the form closes and the browser goes to the new part's detail page. |
| 3 | Check the detail page. | None | Proposed, to confirm in Q-Part-15: Description shows all 250 characters. |

**Postconditions and cleanup:** one new part `QA-<suffix> Desc250` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** The limit comes from the schema (Q-Part-15).

---

### UI-Part-053: Description of 251 characters is not accepted

| Field | Value |
|---|---|
| **Summary** | A Description one character over the maximum length (251 characters) is not saved. |
| **Requirement** | `R-Part-14`. Source: [part-views.md#L34](../../requirements/docs/part-views.md#L34). Schema: requirements/openapi-parts.yaml `components.schemas.Part.description` (optional, maxLength 250, L4148-L4151) |
| **Area** | Part |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (max length + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: boundary check. |
| **Review** | Draft · Open question: Q-Part-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and Description. | Name: `QA-<suffix> Desc251`<br>Description: 251 characters | Proposed, to confirm in Q-Part-15: the field accepts the input, or blocks typing beyond 250 characters. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-15: the form shows an error on Description, stays open, and no part is created. The API schema limits Description to 250 characters (`maxLength 250`); a form that shows errors cannot be submitted (R-Part-05). No doc states how the form handles a longer value. Open: Q-Part-15 (the error text, or whether the field stops input at 250 characters, in which case a part is created with the first 250 characters). |

**Postconditions and cleanup:** Proposed (Q-Part-15): no part is created. Check by searching the *Parts* view for `QA-<suffix> Desc251`. If a part was created (input cut at the limit), cleanup as `admin`: set it inactive, then delete it.

**Notes:** The limit comes from the schema (Q-Part-15).

---

### UI-Part-054: IPN of exactly 100 characters is accepted

| Field | Value |
|---|---|
| **Summary** | An IPN on the maximum length limit (100 characters) can be submitted. |
| **Requirement** | `R-Part-12`. Source: [part-views.md#L30](../../requirements/docs/part-views.md#L30). Schema: requirements/openapi-parts.yaml `components.schemas.Part.IPN` (maxLength 100, L4164-L4167) |
| **Area** | Part |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (max length) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: boundary check. |
| **Review** | Draft · Open question: Q-Part-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and IPN. | Name: `QA-<suffix> Ipn100`<br>IPN: 100 characters (`QA-<suffix>-` then `I` characters up to a total of 100) | The fields accept the values. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-15: the form closes and the browser goes to the new part's detail page. |
| 3 | Check the detail page. | None | Proposed, to confirm in Q-Part-15: IPN shows all 100 characters. |

**Postconditions and cleanup:** one new part `QA-<suffix> Ipn100` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** The limit comes from the schema (Q-Part-15). An empty IPN is covered by UI-Part-001.

**Duplicate check:** 51 · Review · matches: [UI-Part-055](part-creation-form-validation.md) (51), [UI-Part-044](part-creation-form-validation.md) (50)

**Duplicate judgement:** Keep · Differs from UI-Part-055 by boundary side and outcome (100 accepted vs 101 rejected) and from UI-Part-044 by field and rule (IPN, R-Part-12, vs Name, R-Part-05) · test-case-reviewer, 2026-10-15

---

### UI-Part-055: IPN of 101 characters is not accepted

| Field | Value |
|---|---|
| **Summary** | An IPN one character over the maximum length (101 characters) is not saved. |
| **Requirement** | `R-Part-12`. Source: [part-views.md#L30](../../requirements/docs/part-views.md#L30). Schema: requirements/openapi-parts.yaml `components.schemas.Part.IPN` (maxLength 100, L4164-L4167) |
| **Area** | Part |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (max length + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: boundary check. |
| **Review** | Draft · Open question: Q-Part-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and IPN. | Name: `QA-<suffix> Ipn101`<br>IPN: 101 characters (`QA-<suffix>-` then `I` characters up to a total of 101) | Proposed, to confirm in Q-Part-15: the field accepts the input, or blocks typing beyond 100 characters. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-15: the form shows an error on IPN, stays open, and no part is created. The API schema limits IPN to 100 characters (`maxLength 100`); a form that shows errors cannot be submitted (R-Part-05). No doc states how the form handles a longer value. Open: Q-Part-15 (the error text, or whether the field stops input at 100 characters, in which case a part is created with the first 100 characters). |

**Postconditions and cleanup:** Proposed (Q-Part-15): no part is created. Check by searching the *Parts* view for `QA-<suffix> Ipn101`. If a part was created (input cut at the limit), cleanup as `admin`: set it inactive, then delete it.

**Notes:** The limit comes from the schema (Q-Part-15).

**Duplicate check:** 55 · Review · matches: [UI-Part-045](part-creation-form-validation.md) (55), [UI-Part-054](part-creation-form-validation.md) (51)

**Duplicate judgement:** Keep · Differs from UI-Part-045 by field and rule (IPN, R-Part-12, vs Name, R-Part-05) and from UI-Part-054 by boundary side and outcome (101 rejected vs 100 accepted) · test-case-reviewer, 2026-10-15

---

### UI-Part-056: IPN with special characters is accepted

| Field | Value |
|---|---|
| **Summary** | An IPN containing separators and symbols is saved and shown unchanged. |
| **Requirement** | `R-Part-12`. Source: [part-views.md#L30](../../requirements/docs/part-views.md#L30). Schema: requirements/openapi-parts.yaml `components.schemas.Part.IPN` (maxLength 100, L4164-L4167) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Error guessing (special characters) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: simple form check. |
| **Review** | Draft · Open question: Q-Part-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and IPN. | Name: `QA-<suffix> IpnSpecial`<br>IPN: `QA-<suffix>/10.5-A_#é` | The fields accept the values. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-14: the form closes and the browser goes to the new part's detail page. |
| 3 | Check the detail page. | None | Proposed, to confirm in Q-Part-14: IPN shows exactly the text entered. |

**Postconditions and cleanup:** one new part `QA-<suffix> IpnSpecial` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** The docs state no IPN format (R-Part-12: a code for any numbering system).

---

### UI-Part-057: Whitespace-only IPN

| Field | Value |
|---|---|
| **Summary** | An IPN made only of spaces is submitted: the IPN is not required, so the outcome depends on whether the value is trimmed. |
| **Requirement** | `R-Part-12`. Source: [part-views.md#L30](../../requirements/docs/part-views.md#L30). Schema: requirements/openapi-parts.yaml `components.schemas.Part.IPN` (maxLength 100, L4164-L4167) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Error guessing (whitespace-only text) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: simple form check. |
| **Review** | Draft · Open question: Q-Part-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and enter spaces only in IPN. | Name: `QA-<suffix> IpnBlank`<br>IPN: 5 space characters | The field shows the spaces. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-14: the value is trimmed to empty and the part is created with an empty IPN (the IPN is not required, R-Part-12). Open: Q-Part-14 (or the form rejects the value). |

**Postconditions and cleanup:** if created, cleanup as `admin`: set the part `QA-<suffix> IpnBlank` inactive, then delete it.

**Notes:** None.

---

### UI-Part-058: A second part with the same IPN and a different Name

| Field | Value |
|---|---|
| **Summary** | Creating a part whose IPN equals the IPN of an existing part (different Name): the brief treats this as a negative case, the docs state no IPN uniqueness rule. |
| **Requirement** | `R-Part-12`. Source: [part-views.md#L30](../../requirements/docs/part-views.md#L30). Schema: requirements/openapi-parts.yaml `components.schemas.Part.IPN` (maxLength 100, L4164-L4167) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: duplicate IPN), Negative |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Existing` with IPN `QA-<suffix>-IPN1`, created as `admin` via `POST /api/part/`; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: after Q-Part-17 is answered. |
| **Review** | Draft · Open question: Q-Part-17 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in a new Name and the existing IPN. | Name: `QA-<suffix> Second`<br>IPN: `QA-<suffix>-IPN1` | The fields accept the values. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-17: the part is not created and an error is shown on the IPN field. Open: Q-Part-17 (whether a duplicate IPN is rejected or accepted, the setting that controls it, and the error text). |

**Postconditions and cleanup:** only `QA-<suffix> Existing` exists (if rejected). If `QA-<suffix> Second` was created, cleanup as `admin`: set it inactive, then delete it; then delete the existing part the same way.

**Notes:** Index Not in docs 1: no IPN uniqueness rule in the docs. Finding F-05 (app observation, not a requirement): 1.5.6 accepted duplicate IPNs (`PART_ALLOW_DUPLICATE_IPN` on). If the app accepts, record a finding; do not change the case.

---

### UI-Part-059: Revision accepts any string value

| Field | Value |
|---|---|
| **Summary** | A free-form Revision value (letters, digits, symbols) is accepted on the Create Part form. |
| **Requirement** | `R-Part-15`, `R-REV-03`. Source: [part-views.md#L36](../../requirements/docs/part-views.md#L36), [part-revision.md#L29](../../requirements/docs/part-revision.md#L29). Schema: requirements/openapi-parts.yaml `components.schemas.Part.revision` (nullable, maxLength 100, L4207-L4211) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: arbitrary string) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revisions enabled [open: Q-REV-01, setting name and state]; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: after Q-Part-19 is answered. |
| **Review** | Draft · Open question: Q-Part-19, Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Find the Revision field. | None | The form shows a Revision field [open: Q-Part-19, whether the Create Part form has a Revision field and its label]. |
| 2 | Fill in Name and Revision. | Name: `QA-<suffix> Rev`<br>Revision: `v2.1-rc#A` | The Revision field accepts any string value (R-REV-03). |
| 3 | Press *Submit*. | None | The form closes and the browser goes to the new part's detail page (R-Part-06). |
| 4 | Check the detail page. | None | Proposed, to confirm in Q-Part-19: Revision shows `v2.1-rc#A`. |

**Postconditions and cleanup:** one new part `QA-<suffix> Rev` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** A part with the Revision left empty is covered by UI-Part-001.

---

### UI-Part-060: Revision of exactly 100 characters is accepted

| Field | Value |
|---|---|
| **Summary** | A Revision on the maximum length limit (100 characters) can be submitted. |
| **Requirement** | `R-REV-03`. Source: [part-revision.md#L29](../../requirements/docs/part-revision.md#L29). Schema: requirements/openapi-parts.yaml `components.schemas.Part.revision` (nullable, maxLength 100, L4207-L4211) |
| **Area** | Part |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (max length) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revisions enabled [open: Q-REV-01, setting name and state]; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: after Q-Part-19 is answered. |
| **Review** | Draft · Open question: Q-Part-15, Q-Part-19, Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Find the Revision field. | None | [open: Q-Part-19, whether the Create Part form has a Revision field] |
| 2 | Fill in Name and Revision. | Name: `QA-<suffix> Rev100`<br>Revision: 100 characters | The fields accept the values. |
| 3 | Press *Submit*. | None | Proposed, to confirm in Q-Part-15: the form closes and the browser goes to the new part's detail page. |

**Postconditions and cleanup:** one new part `QA-<suffix> Rev100` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** R-REV-03 states no maximum length; the limit comes from the schema.

**Duplicate check:** 63 · Review · matches: [UI-Part-061](part-creation-form-validation.md) (63)

**Duplicate judgement:** Keep · Differs from UI-Part-061 by boundary side and expected outcome (Revision of 100 characters accepted vs 101 rejected) · test-case-reviewer, 2026-10-15

---

### UI-Part-061: Revision of 101 characters is not accepted

| Field | Value |
|---|---|
| **Summary** | A Revision one character over the maximum length (101 characters) is not saved. |
| **Requirement** | `R-REV-03`. Source: [part-revision.md#L29](../../requirements/docs/part-revision.md#L29). Schema: requirements/openapi-parts.yaml `components.schemas.Part.revision` (nullable, maxLength 100, L4207-L4211) |
| **Area** | Part |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (max length + 1) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revisions enabled [open: Q-REV-01, setting name and state]; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: after Q-Part-19 is answered. |
| **Review** | Draft · Open question: Q-Part-15, Q-Part-19, Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Find the Revision field. | None | [open: Q-Part-19, whether the Create Part form has a Revision field] |
| 2 | Fill in Name and Revision. | Name: `QA-<suffix> Rev101`<br>Revision: 101 characters | Proposed, to confirm in Q-Part-15: the field accepts the input, or blocks typing beyond 100 characters. |
| 3 | Press *Submit*. | None | Proposed, to confirm in Q-Part-15: the form shows an error on Revision, stays open, and no part is created. The API schema limits Revision to 100 characters (`maxLength 100`); a form that shows errors cannot be submitted (R-Part-05). No doc states how the form handles a longer value. Open: Q-Part-15 (the error text, or whether the field stops input at 100 characters, in which case a part is created with the first 100 characters). |

**Postconditions and cleanup:** Proposed (Q-Part-15): no part is created. Check by searching the *Parts* view for `QA-<suffix> Rev101`. If a part was created (input cut at the limit), cleanup as `admin`: set it inactive, then delete it.

**Notes:** The limit comes from the schema (Q-Part-15).

**Duplicate check:** 63 · Review · matches: [UI-Part-060](part-creation-form-validation.md) (63)

**Duplicate judgement:** Keep · Differs from UI-Part-060 by boundary side and expected outcome (Revision of 101 characters rejected vs 100 accepted) · test-case-reviewer, 2026-10-15

---

### UI-Part-062: Fixing a form error lets the same form be submitted

| Field | Value |
|---|---|
| **Summary** | After a submit is blocked by a form error, correcting the field lets the same open form be submitted and creates the part. |
| **Requirement** | `R-Part-05`, `R-Part-06`. Source: [part-create.md#L31](../../requirements/docs/part-create.md#L31), [part-create.md#L33](../../requirements/docs/part-create.md#L33). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | State transition (form with error to valid form to submitted) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: core form flow. |
| **Review** | Draft · Open question: Q-Part-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Description only and press *Submit*. | Description: `QA-<suffix> fix` | The form cannot be submitted (R-Part-05). No part is created (R-Part-05). Open: Q-Part-13 (the error text, where it is shown, and whether *Submit* is disabled or the error appears on submit). |
| 2 | Fill in Name in the same open form. | Name: `QA-<suffix> Fixed` | [open: Q-Part-13, whether and when the error on Name clears] |
| 3 | Press *Submit*. | None | The form closes and the browser goes to the new part's detail page (R-Part-05, R-Part-06). |
| 4 | Check the detail page. | None | Name `QA-<suffix> Fixed` and Description `QA-<suffix> fix` show. |

**Postconditions and cleanup:** one new part `QA-<suffix> Fixed` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** None.

---

### UI-Part-063: Double-clicking Submit creates only one part

| Field | Value |
|---|---|
| **Summary** | Pressing *Submit* twice quickly on a valid form creates one part, not two. |
| **Requirement** | `R-Part-05`, `R-Part-13`. Source: [part-create.md#L31](../../requirements/docs/part-create.md#L31), [part-views.md#L32](../../requirements/docs/part-views.md#L32). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Error guessing (double submit) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Partial: the timing of a double click is hard to make stable. |
| **Review** | Draft · Open question: Q-Part-20 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name. | Name: `QA-<suffix> Double` | The field accepts the value. |
| 2 | Double-click *Submit*. | None | Proposed, to confirm in Q-Part-20: one part is created and the browser goes to its detail page; no second part is created. |
| 3 | Search the *Parts* view for `QA-<suffix> Double`. | None | Proposed, to confirm in Q-Part-20: exactly one part is listed. |

**Postconditions and cleanup:** one new part `QA-<suffix> Double` exists. Cleanup as `admin`: set the part inactive, then delete it. If two parts were created, clean up both.

**Notes:** None.

---

### UI-Part-064: Several invalid fields are all reported and block the submit

| Field | Value |
|---|---|
| **Summary** | With Name empty and IPN over the limit at the same time, the form shows errors and nothing is created until both are fixed. |
| **Requirement** | `R-Part-05`, `R-Part-12`. Source: [part-create.md#L31](../../requirements/docs/part-create.md#L31), [part-views.md#L30](../../requirements/docs/part-views.md#L30). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199); requirements/openapi-parts.yaml `components.schemas.Part.IPN` (maxLength 100, L4164-L4167) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Decision table (Name empty and IPN too long) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: simple form check. |
| **Review** | Draft · Open question: Q-Part-13, Q-Part-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Leave Name empty and enter an IPN over the limit. | Name: empty<br>IPN: 101 characters (`QA-<suffix>-` then `I` up to 101) | The fields show the values. |
| 2 | Press *Submit*. | None | The form cannot be submitted (R-Part-05). No part is created (R-Part-05). Open: Q-Part-13 (whether both errors are shown together, and their texts), Q-Part-15 (the IPN length error). |
| 3 | Fix only Name, then press *Submit*. | Name: `QA-<suffix> TwoErr` | Proposed, to confirm in Q-Part-15: the form is still not submitted while the IPN error remains (R-Part-05 states a form with errors cannot be submitted). No part is created (R-Part-05). |
| 4 | Shorten IPN to 100 characters and press *Submit*. | IPN: 100 characters | The form closes and the browser goes to the new part's detail page (R-Part-05, R-Part-06). |

**Postconditions and cleanup:** one new part `QA-<suffix> TwoErr` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** None.

---
### UI-Part-065: Link without a scheme is not accepted

| Field | Value |
|---|---|
| **Summary** | A Link value that looks like a host name but has no scheme (`http://` or `https://`) is rejected. |
| **Requirement** | `R-Part-17`, `R-Part-05`. Source: [part-views.md#L40](../../requirements/docs/part-views.md#L40), [part-create.md#L31](../../requirements/docs/part-create.md#L31). Schema: requirements/openapi-parts.yaml `components.schemas.Part.link` (nullable, format uri, maxLength 2000) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: URL without scheme) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: simple form check. |
| **Review** | Draft · Open question: Q-Part-21 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and an invalid Link. | Name: `QA-<suffix> L065`<br>Link: `www.example.com/datasheet` | The fields show the values. |
| 2 | Press *Submit*. | None | The form is not submitted and no part is created (R-Part-05, R-Part-17). The error "Enter a valid URL." is stated for an invalid URL (R-Part-17). Open: Q-Part-21 (whether the text is shown on the *Link* field or in a form-level message, and whether the check runs before or on submit). |
| 3 | Search the *Parts* view for the Name. | `QA-<suffix> L065` | No part with that Name exists (R-Part-17). |

**Postconditions and cleanup:** No part is created. Nothing to clean up.

**Notes:** The docs call the field *External Link*; 1.5.6 labels it *Link* (findings F-01, index doc issue 13). The error text comes from an app observation recorded in R-Part-17, not from the docs.

**Duplicate check:** 79 · Review · matches: [UI-Part-066](part-creation-form-validation.md) (79, test data differs)

**Duplicate judgement:** Keep · Tests a different clause of R-Part-17 than UI-Part-066 (the inventory note names "one without a scheme" separately from "an invalid URL"): a host-like value missing only the scheme vs plain text that is not a URL at all · test-case-reviewer, 2026-10-15

---

### UI-Part-066: Link that is plain text with spaces is not accepted

| Field | Value |
|---|---|
| **Summary** | A Link value that is ordinary text, not a URL, is rejected. |
| **Requirement** | `R-Part-17`, `R-Part-05`. Source: [part-views.md#L40](../../requirements/docs/part-views.md#L40), [part-create.md#L31](../../requirements/docs/part-create.md#L31). Schema: requirements/openapi-parts.yaml `components.schemas.Part.link` (nullable, format uri, maxLength 2000) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: not a URL) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: simple form check. |
| **Review** | Draft · Open question: Q-Part-21 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and an invalid Link. | Name: `QA-<suffix> L066`<br>Link: `not a valid url` | The fields show the values. |
| 2 | Press *Submit*. | None | The form is not submitted and no part is created (R-Part-05, R-Part-17). The error "Enter a valid URL." is stated for an invalid URL (R-Part-17). Open: Q-Part-21 (whether the text is shown on the *Link* field or in a form-level message, and whether the check runs before or on submit). |
| 3 | Search the *Parts* view for the Name. | `QA-<suffix> L066` | No part with that Name exists (R-Part-17). |

**Postconditions and cleanup:** No part is created. Nothing to clean up.

**Notes:** The docs call the field *External Link*; 1.5.6 labels it *Link* (findings F-01, index doc issue 13). The error text comes from an app observation recorded in R-Part-17, not from the docs.

**Duplicate check:** 79 · Review · matches: [UI-Part-065](part-creation-form-validation.md) (79, test data differs)

**Duplicate judgement:** Keep · Tests the "invalid URL" clause of R-Part-17 (plain text with spaces, no URL structure), while UI-Part-065 tests the separate "without a scheme" clause · test-case-reviewer, 2026-10-15

---

### UI-Part-067: Link of exactly 2000 characters is accepted

| Field | Value |
|---|---|
| **Summary** | A valid URL on the maximum Link length (2000 characters) can be submitted. |
| **Requirement** | `R-Part-17`. Source: [part-views.md#L40](../../requirements/docs/part-views.md#L40). Schema: requirements/openapi-parts.yaml `components.schemas.Part.link` (nullable, format uri, maxLength 2000) |
| **Area** | Part |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (max length) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: boundary check. |
| **Review** | Draft · Open question: Q-Part-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and Link. | Name: `QA-<suffix> Link2000`<br>Link: `https://example.com/` followed by `a` characters up to a total of 2000 | The fields accept the values. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-22: the form closes and the browser goes to the new part's detail page; the schema allows up to 2000 characters. |
| 3 | Check the detail page. | None | Proposed, to confirm in Q-Part-22: Link shows the full 2000-character URL. |

**Postconditions and cleanup:** One new part `QA-<suffix> Link2000` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** The limit comes from the schema, not from the docs (Q-Part-22).

---

### UI-Part-068: Link of 2001 characters is not accepted

| Field | Value |
|---|---|
| **Summary** | A valid-looking URL one character over the maximum Link length (2001 characters) is not saved. |
| **Requirement** | `R-Part-17`, `R-Part-05`. Source: [part-views.md#L40](../../requirements/docs/part-views.md#L40), [part-create.md#L31](../../requirements/docs/part-create.md#L31). Schema: requirements/openapi-parts.yaml `components.schemas.Part.link` (nullable, format uri, maxLength 2000) |
| **Area** | Part |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (max length + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: boundary check. |
| **Review** | Draft · Open question: Q-Part-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and Link. | Name: `QA-<suffix> Link2001`<br>Link: `https://example.com/` followed by `a` characters up to a total of 2001 | Proposed, to confirm in Q-Part-22: the field accepts the input, or blocks typing beyond 2000 characters. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-22: the form shows an error on Link, stays open, and no part is created. A form that shows errors cannot be submitted (R-Part-05). Open: Q-Part-22 (the error text, or whether the field stops input at 2000 characters, in which case a part is created with the first 2000 characters). |

**Postconditions and cleanup:** Proposed (Q-Part-22): no part is created. Check by searching the *Parts* view for `QA-<suffix> Link2001`. If a part was created (input cut at the limit), cleanup as `admin`: set it inactive, then delete it.

**Notes:** The limit comes from the schema (Q-Part-22).

**Duplicate check:** 51 · Review · matches: [UI-Part-045](part-creation-form-validation.md) (51)

**Duplicate judgement:** Keep · Different field, rule and limit from UI-Part-045 (Link, R-Part-17, schema maxLength 2000 vs Name, R-Part-05, maxLength 100) and a different open question (Q-Part-22 vs Q-Part-15) · test-case-reviewer, 2026-10-15

---

### UI-Part-069: Whitespace-only Link

| Field | Value |
|---|---|
| **Summary** | A Link made only of spaces is submitted: the outcome depends on whether the value is trimmed to empty or checked as a URL. |
| **Requirement** | `R-Part-17`. Source: [part-views.md#L40](../../requirements/docs/part-views.md#L40). Schema: requirements/openapi-parts.yaml `components.schemas.Part.link` (nullable, format uri, maxLength 2000) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Error guessing (whitespace-only text) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: simple form check. |
| **Review** | Draft · Open question: Q-Part-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and enter spaces only in Link. | Name: `QA-<suffix> LinkBlank`<br>Link: 5 space characters | The field shows the spaces. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-22: the value is trimmed to empty and the part is created with an empty Link. Open: Q-Part-22 (or the form rejects the value with "Enter a valid URL.", which R-Part-17 states for an invalid URL). |

**Postconditions and cleanup:** If created, cleanup as `admin`: set the part `QA-<suffix> LinkBlank` inactive, then delete it.

**Notes:** The docs do not say whether whitespace is trimmed. Compare UI-Part-057 (IPN).

---

### UI-Part-070: Name with leading and trailing spaces

| Field | Value |
|---|---|
| **Summary** | A Name typed with spaces before and after the text is submitted: the outcome depends on whether the form trims the value. |
| **Requirement** | `R-Part-13`. Source: [part-views.md#L32](../../requirements/docs/part-views.md#L32). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Error guessing (leading and trailing whitespace) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: simple form check. |
| **Review** | Draft · Open question: Q-Part-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name with two spaces before and two after the text. | Name: `  QA-<suffix> Padded  ` (2 leading and 2 trailing spaces) | The field shows the value. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-14: the form closes and the browser goes to the new part's detail page. Open: Q-Part-14 (or the form rejects the value). |
| 3 | Check the detail page header. | None | Proposed, to confirm in Q-Part-14: the Name shows `QA-<suffix> Padded` with the surrounding spaces removed. Open: Q-Part-14 (or the spaces are kept). |

**Postconditions and cleanup:** If created, one new part `QA-<suffix> Padded` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** The docs do not say whether whitespace is trimmed (Q-Part-14).

---

### UI-Part-071: Name that differs from an existing Name only by trailing space

| Field | Value |
|---|---|
| **Summary** | A Name equal to an existing part's Name plus a trailing space, with the same IPN, is submitted: the outcome depends on trimming and on the scope of Name uniqueness. |
| **Requirement** | `R-Part-13`. Source: [part-views.md#L32](../../requirements/docs/part-views.md#L32). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` (required, maxLength 100, L4196-L4199) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | What-if business scenario, Error guessing (trailing whitespace on a duplicate) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Existing` with IPN `QA-<suffix>-IPN1`, created as `admin` via `POST /api/part/`; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: after Q-Part-14 and Q-Part-16 are answered. |
| **Review** | Draft · Open question: Q-Part-14, Q-Part-16 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the existing Name followed by one space, and the same IPN. | Name: `QA-<suffix> Existing ` (1 trailing space)<br>IPN: `QA-<suffix>-IPN1` | The fields show the values. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-14 and Q-Part-16: the value is trimmed, equals the existing Name, IPN and Revision, and the part is not created (the Name is unique, R-Part-13). Open: Q-Part-16 (error text, and whether an untrimmed duplicate is accepted). |

**Postconditions and cleanup:** Only `QA-<suffix> Existing` exists if rejected. If a second part was created, cleanup as `admin`: set each part created by this case inactive, then delete it.

**Notes:** Doc issue 2: the scope of 'unique' is unclear. Compare UI-Part-047 (identical Name).

---

### UI-Part-072: Whitespace-only Revision

| Field | Value |
|---|---|
| **Summary** | A Revision made only of spaces is submitted: Revision is optional, so the outcome depends on whether the value is trimmed to empty. |
| **Requirement** | `R-Part-15`, `R-REV-03`. Source: [part-views.md#L36](../../requirements/docs/part-views.md#L36), [part-revision.md#L29](../../requirements/docs/part-revision.md#L29). Schema: requirements/openapi-parts.yaml `components.schemas.Part.revision` (nullable, maxLength 100, L4207-L4211) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Error guessing (whitespace-only text) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revisions enabled [open: Q-REV-01, setting name and state]; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: after Q-Part-19 is answered. |
| **Review** | Draft · Open question: Q-Part-14, Q-Part-19, Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Find the Revision field. | None | The form shows a Revision field [open: Q-Part-19, whether the Create Part form has a Revision field and its label]. |
| 2 | Fill in Name and enter spaces only in Revision. | Name: `QA-<suffix> RevBlank`<br>Revision: 5 space characters | The field shows the spaces. |
| 3 | Press *Submit*. | None | Proposed, to confirm in Q-Part-14: the value is trimmed to empty and the part is created with no Revision (Revision is optional, R-Part-15). Open: Q-Part-14 (or the form rejects the value). |
| 4 | Check the detail page. | None | Proposed, to confirm in Q-Part-14: no Revision value is shown. Open: Q-Part-19 (what the detail page shows for an empty Revision). |

**Postconditions and cleanup:** If created, cleanup as `admin`: set the part `QA-<suffix> RevBlank` inactive, then delete it.

**Notes:** R-REV-03 says any string value is allowed; whether spaces count as a value is not stated. Compare UI-Part-057 (IPN).

---

### UI-Part-073: Whitespace-only Description

| Field | Value |
|---|---|
| **Summary** | A Description made only of spaces is submitted: the outcome depends on whether the value is trimmed to empty and on whether Description is required. |
| **Requirement** | `R-Part-14`. Source: [part-views.md#L34](../../requirements/docs/part-views.md#L34). Schema: requirements/openapi-parts.yaml `components.schemas.Part.description` (optional, maxLength 250, L4148-L4151) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Error guessing (whitespace-only text) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: simple form check. |
| **Review** | Draft · Open question: Q-Part-14, Q-Part-18 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and enter spaces only in Description. | Name: `QA-<suffix> DescBlank`<br>Description: 5 space characters | The field shows the spaces. |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-14 and Q-Part-18: the value is trimmed to empty and the part is created with an empty Description (the schema marks Description optional). Open: Q-Part-18 (whether Description is required, in which case the form is rejected like an empty Description), Q-Part-14 (trimming). |

**Postconditions and cleanup:** If created, cleanup as `admin`: set the part `QA-<suffix> DescBlank` inactive, then delete it.

**Notes:** Compare UI-Part-051 (empty Description).

---
