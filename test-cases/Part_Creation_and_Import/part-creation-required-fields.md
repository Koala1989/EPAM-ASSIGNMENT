# Part creation with only the required fields: Part test cases

### UI-Part-074: Create a part with Name only

| Field | Value |
|---|---|
| **Summary** | A part is created from the *Create Part* form with only Name filled and every other field left at its default, and the browser goes to the new part's detail page. |
| **Requirement** | `R-Part-01`, `R-Part-05`, `R-Part-06`, `R-Part-12`, `R-Part-15`, `R-Part-16`. Source: [part-create.md#L31](../../requirements/docs/part-create.md#L31), [part-create.md#L33](../../requirements/docs/part-create.md#L33), [part-views.md#L30](../../requirements/docs/part-views.md#L30), [part-views.md#L36](../../requirements/docs/part-views.md#L36), [part-views.md#L38](../../requirements/docs/part-views.md#L38). Answered: `Revisions/open-questions.md Q-REV-05` (only Name is marked required) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: only the required field filled), Boundary value analysis (minimum input set) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: core create flow. |
| **Review** | Approved · Open question: Q-Part-23 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name only. Leave Category, IPN, Description, Revision, Keywords and Link empty. | Name: `QA-<suffix> MinPart` | The field accepts the value. No form error is shown (R-Part-05, Q-REV-05). |
| 2 | Press *Submit*. | None | The form closes and the browser goes to the new part's detail page (R-Part-06). |
| 3 | Check the detail page header and details. | None | Name shows `QA-<suffix> MinPart`. IPN, Revision and Keywords are not required (R-Part-12, R-Part-15, R-Part-16). Open: Q-Part-23 (how the detail page shows an empty Category, IPN, Revision, Keywords, Link and Description). |

**Postconditions and cleanup:** one new part `QA-<suffix> MinPart` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** Category is optional on the 1.5.6 form per Q-REV-05 (observed and confirmed by the architect 2026-10-15). Compare UI-Part-075 (Name and Category).

---

### UI-Part-075: Create a part with Name and Category only

| Field | Value |
|---|---|
| **Summary** | A part is created with Name and Category filled and all other fields left empty, and the detail page shows both values. |
| **Requirement** | `R-Part-01`, `R-Part-06`, `R-Part-12`, `R-Part-15`. Source: [part-create.md#L33](../../requirements/docs/part-create.md#L33), [part-views.md#L30](../../requirements/docs/part-views.md#L30), [part-views.md#L36](../../requirements/docs/part-views.md#L36). Answered: `Revisions/open-questions.md Q-REV-05` (a part is created with Name and Category only, Revision empty) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: required field plus Category) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: non-structural category `QA-<suffix> Category`, created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: core create flow. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and Category. Leave IPN, Description, Revision, Keywords and Link empty. | Name: `QA-<suffix> MinCat`<br>Category: `QA-<suffix> Category` | Fields accept the values. No form error is shown (Q-REV-05). |
| 2 | Press *Submit*. | None | The browser goes to the new part's detail page (R-Part-06). |
| 3 | Check the header and details. | None | Name shows `QA-<suffix> MinCat` and the category shows `QA-<suffix> Category`. |

**Postconditions and cleanup:** one new part exists in `QA-<suffix> Category`. Cleanup as `admin`: set the part inactive, delete it, then delete the category.

**Notes:** None.

---

### UI-Part-076: Only Name is marked required on the Create Part form

| Field | Value |
|---|---|
| **Summary** | On the *Create Part* form only Name carries the required marker; Category, IPN, Description, Revision and the other fields do not. |
| **Requirement** | `R-Part-04`, `R-Part-05`, `R-Part-12`, `R-Part-14`, `R-Part-15`. Source: [part-create.md#L26](../../requirements/docs/part-create.md#L26), [part-create.md#L31](../../requirements/docs/part-create.md#L31). Answered: `Revisions/open-questions.md Q-REV-05` (only Name is marked required with `*`). Schema: requirements/openapi-parts.yaml `components.schemas.Part.name` |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Decision table (field x required marker) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes: form check. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open *Add Parts* > *Create Part*. | None | The *Create Part* form opens (R-Part-04). |
| 2 | Check the required marker (`*`) on Name. | None | Name is marked required (Q-REV-05). |
| 3 | Check the marker on Category, IPN, Description, Revision, Keywords and Link. | None | None of these fields is marked required (Q-REV-05). |

**Postconditions and cleanup:** none, no data created.

**Notes:** Fields further down the form (attribute checkboxes, *Supplier Information*) are not covered by Q-REV-05; they are not checked here.

---

### UI-Part-077: Attribute defaults of a part created with Name only

| Field | Value |
|---|---|
| **Summary** | A part created with only Name filled is Active and has the form's default attributes, which show on the detail page. |
| **Requirement** | `R-ATT-28`, `R-Part-09`, `R-Part-06`, `R-Unit_measure-02`. Source: [part-index.md#L116](../../requirements/docs/part-index.md#L116), [part-create.md#L47](../../requirements/docs/part-create.md#L47), [part-create.md#L33](../../requirements/docs/part-create.md#L33), [part-views.md#L44](../../requirements/docs/part-views.md#L44) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: all defaults), State transition (new part to Active) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Partial: the attribute defaults other than Active are not stated. |
| **Review** | Draft · Open question: Q-Part-23, Q-Unit_measure-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Without changing anything, read the state of the attribute checkboxes. | None | *Purchaseable* is checked (R-Part-09, inventory note on `PART_PURCHASEABLE`). Open: Q-Part-23 (default state of the other attribute checkboxes). |
| 2 | Fill in Name only and press *Submit*. | Name: `QA-<suffix> Defaults` | The browser goes to the new part's detail page (R-Part-06). |
| 3 | Check the part status on the detail page. | None | The part is Active (R-ATT-28). |
| 4 | Check the units of the part. | None | Open: Q-Unit_measure-01 (blank dimensionless or `pcs`; docs conflict, index Doc issue 1). Open: Q-Part-23 (how the other defaults show on the detail page). |

**Postconditions and cleanup:** one new part `QA-<suffix> Defaults` exists. Cleanup as `admin`: set the part inactive, then delete it.

**Notes:** Index Doc issue 1 (R-Unit_measure-02).

---

### UI-Part-078: Cancelling the form with only Name entered creates no part

| Field | Value |
|---|---|
| **Summary** | Closing the *Create Part* form without submitting, after entering only Name, leaves no part behind. |
| **Requirement** | `R-Part-04`, `R-Part-06`. Source: [part-create.md#L26](../../requirements/docs/part-create.md#L26), [part-create.md#L33](../../requirements/docs/part-create.md#L33) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-form) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: form check. |
| **Review** | Draft · Open question: Q-Part-24 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter Name only. | Name: `QA-<suffix> Cancelled` | The field accepts the value. |
| 2 | Close the form without pressing *Submit*. | [open: Q-Part-24, label of the cancel or close control] | Proposed, to confirm in Q-Part-24: the form closes, the browser stays on the *Parts* view and no part is created. |
| 3 | Search the *Parts* view for `QA-<suffix> Cancelled`. | None | Proposed, to confirm in Q-Part-24: no part with that name exists. |

**Postconditions and cleanup:** no part is created. Nothing to clean up.

**Notes:** The docs describe only the successful submit (R-Part-06); the cancel outcome is not stated.
