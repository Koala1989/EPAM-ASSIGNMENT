# Bill of materials tab editing and validation: Detail_View test cases

### UI-Detail_View-001: The Edit icon switches the BOM tab of an assembly from view mode to editing mode

| Field | Value |
|---|---|
| **Summary** | A user with BOM edit permission opens the *BOM* tab in view mode and switches to editing mode with the *Edit* icon. |
| **Requirement** | `R-Detail_View-59`. Source: [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L124) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (view mode to editing mode) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: category `QA-<suffix> Category`, Assembly part `QA-<suffix> Assembly` (Assembly on), created via `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`. |
| **Automation** | Yes: core BOM flow. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *BOM* tab. | None | The BOM is displayed in "view" mode (R-Detail_View-59). The *Edit* icon is visible at the top of the BOM panel. |
| 2 | Click the *Edit* icon. | None | Editing mode is enabled, which allows adding, adjusting or deleting BOM line items (R-Detail_View-59). Open: Q-Detail_View-02 (which controls appear, and how the user leaves editing mode). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the assembly inactive, delete it, then delete the category.

**Notes:** the docs say the page reloads after the *Edit* click ([manufacturing-bom.md#L137](../../requirements/docs/manufacturing-bom.md#L137)).

---

### UI-Detail_View-002: The BOM tab opens in view mode, without the add control

| Field | Value |
|---|---|
| **Summary** | On first opening, the *BOM* tab is in view mode and does not offer adding, adjusting or deleting lines until the *Edit* icon is used. |
| **Requirement** | `R-Detail_View-59`. Source: [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L124) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (initial state is view mode) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with one BOM line `QA-<suffix> Comp A` quantity 2, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *BOM* tab. | None | The line `QA-<suffix> Comp A` is listed in "view" mode (R-Detail_View-59). The add icon is not shown: the docs say it is clicked after *Edit* (manufacturing-bom.md#L137). Open: Q-Detail_View-02 (which other editing controls are hidden). |
| 2 | Open another tab, then return to the *BOM* tab. | None | Proposed, to confirm in Q-Detail_View-02: the tab is again in view mode. |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: delete the BOM line, set the assembly inactive, delete it and the components, then the category.

**Notes:** None.

---

### UI-Detail_View-003: A user without BOM edit permission does not see the Edit icon

| Field | Value |
|---|---|
| **Summary** | A view-only user opening the *BOM* tab sees the lines but no *Edit* icon, so no editing mode. |
| **Requirement** | `R-Detail_View-60`. Source: [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L127) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (user without edit permission) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `reader` (view-only); Settings: None; Data: Assembly `QA-<suffix> Assembly` with one BOM line `QA-<suffix> Comp A` quantity 2, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *BOM* tab. | None | The BOM lines are listed. The *Edit* icon is not visible (R-Detail_View-60). Open: Q-Detail_View-01 (which permission is missing). |
| 2 | Look for an add icon, a delete control and the *Actions* substitute icon. | None | Proposed, to confirm in Q-Detail_View-01: none is available, as they exist only in editing mode. |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: delete the BOM line, set the assembly inactive and delete it and the components, then the category.

**Notes:** None.

---

### UI-Detail_View-004: A user with no permissions cannot reach the BOM tab

| Field | Value |
|---|---|
| **Summary** | A user with no permissions cannot open the BOM of an assembly. |
| **Requirement** | `R-Detail_View-60`, `R-Detail_View-19`. Source: [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L127), [part-views.md#BOM](../../requirements/docs/part-views.md#L84) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (user with no permissions) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess` (no permissions); Settings: None; Data: Assembly `QA-<suffix> Assembly` created via API as `admin`; Pre-steps: log in through the login form. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part detail page of `QA-<suffix> Assembly` by its URL. | `/web/part/<pk>/` | Proposed, to confirm in Q-Detail_View-01: the part page and its *BOM* tab are not shown and no *Edit* icon is available. |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the assembly inactive, delete it, then delete the category.

**Notes:** no rule states what `noaccess` sees.

---

### UI-Detail_View-005: A BOM line is added with the required fields

| Field | Value |
|---|---|
| **Summary** | In editing mode, the add icon opens the *Create BOM Item* form and *Submit* adds a line to the assembly's BOM. |
| **Requirement** | `R-Detail_View-62`, `R-Detail_View-50`. Source: [manufacturing-bom.md#Add BOM Item](../../requirements/docs/manufacturing-bom.md#L137), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: required fields filled) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A` (Component on), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab. |
| **Automation** | Yes: core BOM flow. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click the *Edit* icon, then, after the page reloads, the add icon. | None | The `Create BOM Item` form is displayed (R-Detail_View-62). Open: Q-Detail_View-03 (which fields are marked required). |
| 2 | Select the component and enter the quantity. | Part: `QA-<suffix> Comp A`<br>Quantity: `2` [open: Q-Detail_View-03, whether Quantity or Raw Amount is entered] | The fields accept the values. |
| 3 | Press *Submit*. | None | The form closes and the BOM item is added to this part's BOM (R-Detail_View-62). |
| 4 | Check the BOM table. | None | A line for `QA-<suffix> Comp A` with quantity `2` is listed (R-Detail_View-50). |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-006: A BOM line is added with every property filled in

| Field | Value |
|---|---|
| **Summary** | A line created with all documented properties shows each value in the BOM table. |
| **Requirement** | `R-Detail_View-50`, `R-Detail_View-62`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23), [manufacturing-bom.md#Add BOM Item](../../requirements/docs/manufacturing-bom.md#L137) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: all optional fields filled) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A` (Component on), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: field labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click the add icon and fill in the form. | Part: `QA-<suffix> Comp A`<br>Reference: `R1`<br>Quantity: `10`<br>Attrition: `2` [open: Q-Detail_View-04, whether `2` or `2%`]<br>Setup Quantity: `5`<br>Rounding Multiple: `10`<br>Consumable: on<br>Inherited: on<br>Optional: on<br>Allow Variants: on [open: Q-Detail_View-05, label and presence]<br>Note: `QA-<suffix> note` | The form accepts the values. Field labels: [open: Q-Detail_View-03, exact labels]. |
| 2 | Press *Submit*. | None | The form closes and the line is added (R-Detail_View-62). |
| 3 | Check the BOM table row. | None | The row shows the part, Reference `R1`, quantity, Attrition, Setup Quantity, Rounding Multiple, and the Consumable, Inherited and Optional flags and the note (R-Detail_View-50). Open: Q-Detail_View-03 (which columns the table shows). |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** Allow Variants is missing from the line property table (index, Doc issue 6).

---

### UI-Detail_View-007: A BOM line cannot be created without a component

| Field | Value |
|---|---|
| **Summary** | Submitting the *Create BOM Item* form with the Part field empty is rejected and no line is added. |
| **Requirement** | `R-Detail_View-62`, `R-Detail_View-50`. Source: [manufacturing-bom.md#Add BOM Item](../../requirements/docs/manufacturing-bom.md#L143), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L25) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty required field) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Leave Part empty, enter only the quantity and press *Submit*. | Quantity: `2` | The BOM item is not added (the docs ask the user to "fill-out the required fields", R-Detail_View-62). Open: Q-Detail_View-03 (which fields are required, the error text and whether the form stays open). |
| 2 | Check the BOM table. | None | No new line is listed. |

**Postconditions and cleanup:** no records created. Cleanup as `admin`: set the assembly inactive, delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-008: Cancelling the Create BOM Item form adds no line

| Field | Value |
|---|---|
| **Summary** | Closing the form after filling it in, without submitting, leaves the BOM unchanged. |
| **Requirement** | `R-Detail_View-62`. Source: [manufacturing-bom.md#Add BOM Item](../../requirements/docs/manufacturing-bom.md#L143) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-form) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Partial: the cancel control label is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Part and Quantity. | Part: `QA-<suffix> Comp A`<br>Quantity: `2` | Fields accept the values. |
| 2 | Close the form without pressing *Submit* [open: Q-Detail_View-03, the cancel or close control]. | None | The form closes. Proposed, to confirm in Q-Detail_View-03: no BOM item is created. |
| 3 | Check the BOM table. | None | No line for `QA-<suffix> Comp A` is listed (R-Detail_View-62: a line is added by *Submit*). |

**Postconditions and cleanup:** no records created. Cleanup as `admin`: set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-009: A BOM line quantity of 0 is submitted

| Field | Value |
|---|---|
| **Summary** | The lower edge of the Quantity field: `0` entered for a new line. |
| **Requirement** | `R-Detail_View-50`, `R-Detail_View-62`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L28), [manufacturing-bom.md#Add BOM Item](../../requirements/docs/manufacturing-bom.md#L143) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (quantity on the lower limit, 0) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the component, enter the quantity and press *Submit*. | Part: `QA-<suffix> Comp A`<br>Quantity: `0` [open: Q-Detail_View-04, lower limit] | Not known: depends on open question Q-Detail_View-04 (whether `0` is accepted or rejected, and the error text). |

**Postconditions and cleanup:** a line may have been created. Cleanup as `admin`: delete it, set the assembly inactive and delete it and the component, then the category.

**Notes:** the docs state no limit for Quantity.

---

### UI-Detail_View-010: A negative BOM line quantity is submitted

| Field | Value |
|---|---|
| **Summary** | A new line with Quantity `-1` is submitted. |
| **Requirement** | `R-Detail_View-50`, `R-Detail_View-62`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L28), [manufacturing-bom.md#Add BOM Item](../../requirements/docs/manufacturing-bom.md#L143) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Boundary value analysis (quantity just below the lower limit, -1) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the component, enter the quantity and press *Submit*. | Part: `QA-<suffix> Comp A`<br>Quantity: `-1` | Proposed, to confirm in Q-Detail_View-04: the line is rejected with a validation error on Quantity and is not added. Open: Q-Detail_View-04 (error text). |

**Postconditions and cleanup:** none expected. Cleanup as `admin`: set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

**Duplicate check:** 77 · Review · matches: [UI-Detail_View-011](bom-tab-editing-and-validation.md) (77)

**Duplicate judgement:** Keep · Different input class from UI-Detail_View-011: a negative numeric quantity (boundary just below 0) versus a non-numeric value (wrong type). · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-011: A non-numeric BOM line quantity is submitted

| Field | Value |
|---|---|
| **Summary** | A new line with a text Quantity is not accepted. |
| **Requirement** | `R-Detail_View-50`, `R-Detail_View-62`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L28), [manufacturing-bom.md#Add BOM Item](../../requirements/docs/manufacturing-bom.md#L143) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the component, enter the quantity and press *Submit*. | Part: `QA-<suffix> Comp A`<br>Quantity: `abc` | Proposed, to confirm in Q-Detail_View-04: the line is rejected with a validation error on Quantity and is not added. Open: Q-Detail_View-04 (whether the field blocks the input or shows an error, and the text). |

**Postconditions and cleanup:** none expected. Cleanup as `admin`: set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

**Duplicate check:** 77 · Review · matches: [UI-Detail_View-010](bom-tab-editing-and-validation.md) (77)

**Duplicate judgement:** Keep · Different input class from UI-Detail_View-010: a non-numeric quantity (wrong type, which the field may block outright) versus a negative number. · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-012: A negative attrition is submitted

| Field | Value |
|---|---|
| **Summary** | A new line with Attrition `-1` is submitted. |
| **Requirement** | `R-Detail_View-51`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L31) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Boundary value analysis (attrition just below 0) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the component, set Quantity, enter Attrition and press *Submit*. | Part: `QA-<suffix> Comp A`<br>Quantity: `2`<br>Attrition: `-1` | Attrition is "a percentage of the base quantity" (R-Detail_View-51). Proposed, to confirm in Q-Detail_View-04: the line is rejected with a validation error on Attrition. Open: Q-Detail_View-04 (limits, error text). |

**Postconditions and cleanup:** none expected. Cleanup as `admin`: set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-013: A BOM line is added with an attrition of 2 percent

| Field | Value |
|---|---|
| **Summary** | The documented example attrition of 2% is accepted and shown on the new line. |
| **Requirement** | `R-Detail_View-51`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L31) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: documented example value) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the component, set Quantity, enter Attrition and press *Submit*. | Part: `QA-<suffix> Comp A`<br>Quantity: `100`<br>Attrition: `2` [open: Q-Detail_View-04, whether `2` or `2%` is typed] | The line is added (R-Detail_View-62). |
| 2 | Check the row. | None | The row shows an attrition of 2%, "expressed as a percentage of the base quantity (e.g. 2%)" (R-Detail_View-51). Open: Q-Detail_View-03 (column label). |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-014: An attrition above 100 percent is submitted

| Field | Value |
|---|---|
| **Summary** | A new line with Attrition `101` is submitted, one above 100% of the base quantity. |
| **Requirement** | `R-Detail_View-51`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L31) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (attrition just above 100) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the component, set Quantity, enter Attrition and press *Submit*. | Part: `QA-<suffix> Comp A`<br>Quantity: `2`<br>Attrition: `101` [open: Q-Detail_View-04, upper limit] | Not known: depends on open question Q-Detail_View-04 (whether a value above 100 is accepted, and the error text). |

**Postconditions and cleanup:** a line may have been created. Cleanup as `admin`: delete it, set the assembly inactive and delete it and the component, then the category.

**Notes:** the docs state no upper limit.

---

### UI-Detail_View-015: A negative setup quantity is submitted

| Field | Value |
|---|---|
| **Summary** | A new line with Setup Quantity `-1` is submitted. |
| **Requirement** | `R-Detail_View-52`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L32) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Boundary value analysis (setup quantity just below 0) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the component, set Quantity, enter Setup Quantity and press *Submit*. | Part: `QA-<suffix> Comp A`<br>Quantity: `2`<br>Setup Quantity: `-1` | Setup Quantity is "added to the base quantity" for fixed setup losses (R-Detail_View-52). Proposed, to confirm in Q-Detail_View-04: the line is rejected with a validation error on Setup Quantity. Open: Q-Detail_View-04 (error text). |

**Postconditions and cleanup:** none expected. Cleanup as `admin`: set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-016: A negative rounding multiple is submitted

| Field | Value |
|---|---|
| **Summary** | A new line with Rounding Multiple `-5` is submitted. |
| **Requirement** | `R-Detail_View-53`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L33) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: negative value) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the component, set Quantity, enter Rounding Multiple and press *Submit*. | Part: `QA-<suffix> Comp A`<br>Quantity: `2`<br>Rounding Multiple: `-5` | The required quantity is rounded up to the nearest multiple of this value (R-Detail_View-53). Proposed, to confirm in Q-Detail_View-04: the line is rejected with a validation error on Rounding Multiple. Open: Q-Detail_View-04 (limits, error text). |

**Postconditions and cleanup:** none expected. Cleanup as `admin`: set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-017: The same component cannot be added twice to one BOM

| Field | Value |
|---|---|
| **Summary** | Adding a component that is already a line of the BOM is tried a second time. |
| **Requirement** | `R-Detail_View-50`, `R-Detail_View-62`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23), [manufacturing-bom.md#Add BOM Item](../../requirements/docs/manufacturing-bom.md#L143) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate line) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with one BOM line `QA-<suffix> Comp A` quantity 2, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the same component, enter Quantity and press *Submit*. | Part: `QA-<suffix> Comp A`<br>Quantity: `3` | Not known: depends on open question Q-Detail_View-04 (whether a second line for the same component is rejected or allowed, and the error text). |

**Postconditions and cleanup:** one or two lines may exist. Cleanup as `admin`: delete the lines, set the assembly inactive and delete it and the component, then the category.

**Notes:** the docs do not state a uniqueness rule for BOM lines.

---

### UI-Detail_View-018: An assembly cannot be added to its own BOM

| Field | Value |
|---|---|
| **Summary** | Selecting the assembly itself as the component of one of its BOM lines. |
| **Requirement** | `R-Detail_View-50`, `R-Detail_View-62`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L25), [manufacturing-bom.md#Add BOM Item](../../requirements/docs/manufacturing-bom.md#L143) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (self-reference) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with Component on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the assembly itself as Part, enter Quantity and press *Submit*. | Part: `QA-<suffix> Assembly`<br>Quantity: `1` | Not known: depends on open question Q-Detail_View-04 (whether the assembly is offered in the selector or the form is rejected, and the error text). |

**Postconditions and cleanup:** a line may have been created. Cleanup as `admin`: delete it, set the assembly inactive and delete it, then the category.

**Notes:** the docs state no self-reference rule for BOMs (revision self-reference is a different rule, R-REV).

---

### UI-Detail_View-019: A BOM line reference with special characters and Unicode is accepted

| Field | Value |
|---|---|
| **Summary** | The optional Reference field takes a part-designator-like value with special characters and Unicode. |
| **Requirement** | `R-Detail_View-50`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L28) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Error guessing (special characters and Unicode) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the component, set Quantity, enter Reference and press *Submit*. | Part: `QA-<suffix> Comp A`<br>Quantity: `1`<br>Reference: `R1/<>&"é-測試` | Reference is an optional free field "to describe the BOM Line Item, e.g. part designator" (R-Detail_View-50). Proposed, to confirm in Q-Detail_View-04: the line is added and the row shows the reference exactly as typed, unescaped. |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-020: A whitespace-only reference is submitted

| Field | Value |
|---|---|
| **Summary** | Reference containing only spaces is submitted on a new line. |
| **Requirement** | `R-Detail_View-50`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L28) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (whitespace-only text) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, click the add icon. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the component, set Quantity, enter Reference and press *Submit*. | Part: `QA-<suffix> Comp A`<br>Quantity: `1`<br>Reference: three spaces | Reference is optional (R-Detail_View-50). Proposed, to confirm in Q-Detail_View-04: the line is added with an empty reference (spaces trimmed). Open: Q-Detail_View-04. |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-021: The quantity of an existing BOM line is changed in editing mode

| Field | Value |
|---|---|
| **Summary** | In editing mode, an existing line's Quantity is adjusted and the new value is shown. |
| **Requirement** | `R-Detail_View-59`. Source: [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L124) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (editing mode, line adjusted) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with one BOM line `QA-<suffix> Comp A` quantity 2, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: the edit control is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the edit action of the `QA-<suffix> Comp A` row [open: Q-Detail_View-02, control and label]. | None | The line becomes editable, as editing mode allows adjusting lines (R-Detail_View-59). Open: Q-Detail_View-02 (form or inline). |
| 2 | Change Quantity and save. | Quantity: `5` | The change is saved. The row shows quantity `5` (R-Detail_View-59). |
| 3 | Reload the page and open the *BOM* tab. | None | The row still shows quantity `5`. |

**Postconditions and cleanup:** the line has quantity 5. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-022: An existing BOM line cannot be saved with an empty quantity

| Field | Value |
|---|---|
| **Summary** | Clearing Quantity of an existing line and saving is rejected, and the stored value is unchanged. |
| **Requirement** | `R-Detail_View-59`, `R-Detail_View-50`. Source: [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L124), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L28) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty value on edit) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with one BOM line `QA-<suffix> Comp A` quantity 2, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: the edit control is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-02, Q-Detail_View-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the edit action of the row [open: Q-Detail_View-02, control and label], clear Quantity and save. | Quantity: empty | Open: Q-Detail_View-04 (error text, whether the form stays open). Proposed, to confirm in Q-Detail_View-04: the change is rejected. |
| 2 | Reload the page and open the *BOM* tab. | None | Proposed, to confirm in Q-Detail_View-04: the row still shows quantity `2`. |

**Postconditions and cleanup:** the line is unchanged. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-023: A BOM line is deleted in editing mode

| Field | Value |
|---|---|
| **Summary** | In editing mode, an existing line is deleted and no longer listed. |
| **Requirement** | `R-Detail_View-59`. Source: [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L124) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (editing mode, line deleted) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM lines `QA-<suffix> Comp A` and `QA-<suffix> Comp B`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: the delete control is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Use the delete action of the `QA-<suffix> Comp A` row [open: Q-Detail_View-02, control and label], and confirm if asked. | None | The line is deleted (R-Detail_View-59). Open: Q-Detail_View-02 (confirmation dialog and message). |
| 2 | Reload the page and open the *BOM* tab. | None | `QA-<suffix> Comp A` is not listed. `QA-<suffix> Comp B` is still listed. |

**Postconditions and cleanup:** one BOM line remains. Cleanup as `admin`: delete the remaining line, set the assembly inactive and delete it and the components, then the category.

**Notes:** None.

---

### UI-Detail_View-024: Adding a line to a validated BOM marks the BOM Not Validated

| Field | Value |
|---|---|
| **Summary** | After a BOM is validated, creating a line changes its status to "Not Validated" and shows the *Validate BOM* button. |
| **Requirement** | `R-Detail_View-65`, `R-Detail_View-67`. Source: [manufacturing-bom.md#BOM Validation](../../requirements/docs/manufacturing-bom.md#L163), [manufacturing-bom.md#BOM Validation Status](../../requirements/docs/manufacturing-bom.md#L187) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (validated to not validated, line created) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit and validate permission [open: Q-Detail_View-01, whether `engineer` may]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, component `QA-<suffix> Comp B`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, press *Validate BOM* [open: Q-Detail_View-06, confirmation], click *Edit*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-Detail_View-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the validation status at the top of the BOM table. | None | The BOM is validated: no "Not Validated" status and no *Validate BOM* button (R-Detail_View-67). Open: Q-Detail_View-06 (the status text when valid). |
| 2 | Click the add icon, add a line and press *Submit*. | Part: `QA-<suffix> Comp B`<br>Quantity: `1` | The line is added (R-Detail_View-62). |
| 3 | Check the validation status. | None | The status reads "Not Validated" and the *Validate BOM* button is displayed at the top of the BOM table (R-Detail_View-65, R-Detail_View-67: creating a line requires the assembly to be validated again). |

**Postconditions and cleanup:** two BOM lines, BOM not validated. Cleanup as `admin`: delete the lines, set the assembly inactive and delete it and the components, then the category.

**Notes:** R-Detail_View-65 lists the checksum fields; the create outcome comes from "Whenever a BOM line item is created, adjusted or deleted ... must be validated" ([manufacturing-bom.md#L164](../../requirements/docs/manufacturing-bom.md#L164)).

---

### UI-Detail_View-025: Changing the quantity of a line in a validated BOM marks the BOM Not Validated

| Field | Value |
|---|---|
| **Summary** | After validation, editing the Quantity of a line changes the status to "Not Validated". |
| **Requirement** | `R-Detail_View-65`, `R-Detail_View-67`. Source: [manufacturing-bom.md#BOM Checksum](../../requirements/docs/manufacturing-bom.md#L165), [manufacturing-bom.md#BOM Validation Status](../../requirements/docs/manufacturing-bom.md#L187) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (validated to not validated, quantity changed) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit and validate permission [open: Q-Detail_View-01, whether `engineer` may]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, press *Validate BOM* [open: Q-Detail_View-06, confirmation], click *Edit*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the validation status. | None | The BOM is validated: no "Not Validated" status and no *Validate BOM* button (R-Detail_View-67). Open: Q-Detail_View-06 (status text when valid). |
| 2 | Change Quantity of the line and save. | Quantity: `3` | The change is saved. |
| 3 | Check the validation status. | None | The status reads "Not Validated" and the *Validate BOM* button is displayed (R-Detail_View-65: Quantity is a checksum field; R-Detail_View-67). |

**Postconditions and cleanup:** BOM not validated. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-026: Deleting a line of a validated BOM marks the BOM Not Validated

| Field | Value |
|---|---|
| **Summary** | After validation, deleting a line changes the status to "Not Validated". |
| **Requirement** | `R-Detail_View-65`, `R-Detail_View-67`. Source: [manufacturing-bom.md#BOM Validation](../../requirements/docs/manufacturing-bom.md#L163), [manufacturing-bom.md#BOM Validation Status](../../requirements/docs/manufacturing-bom.md#L187) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (validated to not validated, line deleted) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit and validate permission [open: Q-Detail_View-01, whether `engineer` may]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM lines `QA-<suffix> Comp A` and `QA-<suffix> Comp B`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, press *Validate BOM* [open: Q-Detail_View-06, confirmation], click *Edit*. |
| **Automation** | Partial: the delete control is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-02, Q-Detail_View-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Delete the `QA-<suffix> Comp A` row [open: Q-Detail_View-02, control and confirmation]. | None | The line is deleted. |
| 2 | Check the validation status. | None | The status reads "Not Validated" and the *Validate BOM* button is displayed (R-Detail_View-65: deleting a line requires the assembly to be validated again, manufacturing-bom.md#L164; R-Detail_View-67). |

**Postconditions and cleanup:** one BOM line, BOM not validated. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the components, then the category.

**Notes:** None.

---

### UI-Detail_View-027: Changing each other checksum field of a line marks the BOM Not Validated

| Field | Value |
|---|---|
| **Summary** | For each checksum field (Reference, Attrition, Setup Quantity, Rounding Multiple, Consumable, Inherited, Optional), a change after validation gives "Not Validated". |
| **Requirement** | `R-Detail_View-65`, `R-Detail_View-66`, `R-Detail_View-67`. Source: [manufacturing-bom.md#BOM Checksum](../../requirements/docs/manufacturing-bom.md#L165), [manufacturing-bom.md#BOM Validation Status](../../requirements/docs/manufacturing-bom.md#L187) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (one column per checksum field) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit and validate permission [open: Q-Detail_View-01, whether `engineer` may]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2 (Reference empty, Attrition 0, Setup Quantity 0, Rounding Multiple empty, flags off), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: edit control and labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *Validate BOM* [open: Q-Detail_View-06, confirmation]. | None | The *Validate BOM* button is no longer displayed (R-Detail_View-67). |
| 2 | Edit the line: set Reference. | Reference: `R1` | The status reads "Not Validated" (R-Detail_View-65). |
| 3 | Press *Validate BOM*, then edit the line: set Attrition. | Attrition: `2` | The status reads "Not Validated" (R-Detail_View-65). |
| 4 | Press *Validate BOM*, then edit the line: set Setup Quantity. | Setup Quantity: `5` | The status reads "Not Validated" (R-Detail_View-65). |
| 5 | Press *Validate BOM*, then edit the line: set Rounding Multiple. | Rounding Multiple: `10` | The status reads "Not Validated" (R-Detail_View-65). |
| 6 | Press *Validate BOM*, then edit the line: turn Consumable on. | Consumable: on | The status reads "Not Validated" (R-Detail_View-65). |
| 7 | Press *Validate BOM*, then edit the line: turn Inherited on. | Inherited: on | The status reads "Not Validated" (R-Detail_View-65). |
| 8 | Press *Validate BOM*, then edit the line: turn Optional on. | Optional: on | The status reads "Not Validated" (R-Detail_View-65). |

**Postconditions and cleanup:** the line has all changed values. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** the component (Assembly ID and Component ID) checksum fields are not tested by editing; changing the component is a different action. Allow Variants has its own case (UI-Detail_View-028).

---

### UI-Detail_View-028: Changing Allow Variants of a line in a validated BOM

| Field | Value |
|---|---|
| **Summary** | Allow Variants is in the BOM checksum list but missing from the line property table; this case checks the effect of changing it. |
| **Requirement** | `R-Detail_View-65`. Source: [manufacturing-bom.md#BOM Checksum](../../requirements/docs/manufacturing-bom.md#L179), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L25) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (checksum field: Allow Variants) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit and validate permission [open: Q-Detail_View-01, whether `engineer` may]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, press *Validate BOM* [open: Q-Detail_View-06, confirmation], click *Edit*. |
| **Automation** | Partial: the field label is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-05, Q-Detail_View-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Edit the line and toggle Allow Variants [open: Q-Detail_View-05, label, current state and whether the form has it]. | Allow Variants: toggled | The status reads "Not Validated" and the *Validate BOM* button is displayed (R-Detail_View-65: "Allow Variants" is in the checksum list, manufacturing-bom.md#L179). Open: Q-Detail_View-05 (whether the field exists on the form). |

**Postconditions and cleanup:** the line is changed. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** Doc issue 6 in `test-cases/requirements-inventory.md`.

---

### UI-Detail_View-029: Changing only the note of a line leaves a validated BOM validated

| Field | Value |
|---|---|
| **Summary** | Note is not in the checksum field list, so editing it should not invalidate the BOM. |
| **Requirement** | `R-Detail_View-65`. Source: [manufacturing-bom.md#BOM Checksum](../../requirements/docs/manufacturing-bom.md#L165) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (non-checksum field: Note) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit and validate permission [open: Q-Detail_View-01, whether `engineer` may]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, press *Validate BOM* [open: Q-Detail_View-06, confirmation], click *Edit*. |
| **Automation** | Partial: the edit control is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-06, Q-Detail_View-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Edit the line: set Note, save. | Note: `QA-<suffix> note` | The note is saved. |
| 2 | Check the validation status. | None | Proposed, to confirm in Q-Detail_View-07: the BOM stays validated, with no "Not Validated" status and no *Validate BOM* button, because Note is not a checksum field (R-Detail_View-65 lists the fields that change the checksum). |

**Postconditions and cleanup:** the line has a note. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-030: Adding a substitute to a line of a validated BOM

| Field | Value |
|---|---|
| **Summary** | Substitutes are not in the checksum list; this case checks the validation status after adding one. |
| **Requirement** | `R-Detail_View-65`, `R-Detail_View-63`. Source: [manufacturing-bom.md#BOM Checksum](../../requirements/docs/manufacturing-bom.md#L165), [manufacturing-bom.md#Add Substitute for BOM Item](../../requirements/docs/manufacturing-bom.md#L147) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | What-if business scenario (substitute added after validation) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit and validate permission [open: Q-Detail_View-01, whether `engineer` may]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, component `QA-<suffix> Comp B` (Component on), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, press *Validate BOM* [open: Q-Detail_View-06, confirmation], click *Edit*. |
| **Automation** | Partial: the substitute form is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-06, Q-Detail_View-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click the substitute icon in the *Actions* column of the line, select `QA-<suffix> Comp B` and click *Add Substitute*. | Substitute: `QA-<suffix> Comp B` | The substitute is added (R-Detail_View-63). |
| 2 | Close the form and check the validation status. | None | Proposed, to confirm in Q-Detail_View-07: the BOM stays validated, because substitutes are not in the checksum field list (R-Detail_View-65). |

**Postconditions and cleanup:** the line has one substitute. Cleanup as `admin`: remove the substitute, delete the line, set the assembly inactive and delete it and the components, then the category.

**Notes:** None.

---

### UI-Detail_View-031: Saving a line without changing it leaves a validated BOM validated

| Field | Value |
|---|---|
| **Summary** | Submitting the edit of a line with unchanged values must not recalculate the checksum to a different value. |
| **Requirement** | `R-Detail_View-65`. Source: [manufacturing-bom.md#BOM Checksum](../../requirements/docs/manufacturing-bom.md#L165) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Error guessing (save without change) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit and validate permission [open: Q-Detail_View-01, whether `engineer` may]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, press *Validate BOM* [open: Q-Detail_View-06, confirmation], click *Edit*. |
| **Automation** | Partial: the edit control is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-06, Q-Detail_View-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the line for editing and save without changing any value. | None | The form closes. |
| 2 | Check the validation status. | None | Proposed, to confirm in Q-Detail_View-07: the BOM stays validated; the checksum is a hash of the field values (R-Detail_View-65), which are unchanged. |

**Postconditions and cleanup:** no change. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-032: Validate BOM revalidates a BOM that is Not Validated

| Field | Value |
|---|---|
| **Summary** | After a change, the user revalidates the BOM manually with the *Validate BOM* button. |
| **Requirement** | `R-Detail_View-66`, `R-Detail_View-67`. Source: [manufacturing-bom.md#BOM Checksum](../../requirements/docs/manufacturing-bom.md#L183), [manufacturing-bom.md#BOM Validation Status](../../requirements/docs/manufacturing-bom.md#L187) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (not validated to validated) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit and validate permission [open: Q-Detail_View-01, whether `engineer` may]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, press *Validate BOM* [open: Q-Detail_View-06, confirmation], click *Edit*, change Quantity to `3` and save. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the top of the BOM table. | None | The status reads "Not Validated" and the *Validate BOM* button is displayed (R-Detail_View-67). |
| 2 | Press *Validate BOM* and confirm if asked. | None | The BOM is revalidated (R-Detail_View-66, R-Detail_View-67). Open: Q-Detail_View-06 (confirmation and message). |
| 3 | Check the top of the BOM table. | None | The status no longer reads "Not Validated". Open: Q-Detail_View-06 (the status text when valid, and whether the button is hidden). |
| 4 | Reload the page and open the *BOM* tab. | None | The BOM is still shown as validated. |

**Postconditions and cleanup:** BOM validated. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-033: A view-only user cannot revalidate a BOM that is Not Validated

| Field | Value |
|---|---|
| **Summary** | A user without edit permission opening a "Not Validated" BOM cannot revalidate it. |
| **Requirement** | `R-Detail_View-60`, `R-Detail_View-66`, `R-Detail_View-67`. Source: [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L127), [manufacturing-bom.md#BOM Validation Status](../../requirements/docs/manufacturing-bom.md#L187) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (user without permission, Validate BOM) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view-only); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, changed after validation so it is Not Validated (validate and edit the quantity via API as `admin`); Pre-steps: log in through the login form, open `QA-<suffix> Assembly`. |
| **Automation** | Partial: the permission is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *BOM* tab. | None | The status reads "Not Validated" (R-Detail_View-67). Open: Q-Detail_View-06 (whether `reader` sees the *Validate BOM* button). |
| 2 | If a *Validate BOM* button is shown, press it. | None | Proposed, to confirm in Q-Detail_View-06: the button is hidden for `reader`, or the action is refused with a permission error; the BOM stays "Not Validated". |

**Postconditions and cleanup:** no change. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-034: A substitute is added to a BOM line

| Field | Value |
|---|---|
| **Summary** | In editing mode, the *Actions* column icon opens the *Edit BOM Item Substitutes* form and *Add Substitute* assigns a substitute part. |
| **Requirement** | `R-Detail_View-63`, `R-Detail_View-57`. Source: [manufacturing-bom.md#Add Substitute for BOM Item](../../requirements/docs/manufacturing-bom.md#L147), [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L71) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: a different Component part) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, component `QA-<suffix> Comp B` (Component on), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: the substitute display is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click the substitute icon in the *Actions* column of the `QA-<suffix> Comp A` row. | None | The `Edit BOM Item Substitutes` form is displayed (R-Detail_View-63). |
| 2 | Select a part in the list and click *Add Substitute*. | Part: `QA-<suffix> Comp B` | The substitute is added to the line (R-Detail_View-63, R-Detail_View-57). Open: Q-Detail_View-08 (where it is shown afterwards). |

**Postconditions and cleanup:** the line has one substitute. Cleanup as `admin`: remove the substitute, delete the line, set the assembly inactive and delete it and the components, then the category.

**Notes:** None.

---

### UI-Detail_View-035: A BOM line can have several substitutes

| Field | Value |
|---|---|
| **Summary** | Two different substitute parts are assigned to the same BOM line. |
| **Requirement** | `R-Detail_View-57`, `R-Detail_View-63`. Source: [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L71), [manufacturing-bom.md#Add Substitute for BOM Item](../../requirements/docs/manufacturing-bom.md#L147) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: several substitutes) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, components `QA-<suffix> Comp B` and `QA-<suffix> Comp C` (Component on), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, open the *Edit BOM Item Substitutes* form of the line. |
| **Automation** | Partial: the substitute display is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select a part and click *Add Substitute*. | Part: `QA-<suffix> Comp B` | The substitute is added (R-Detail_View-63). |
| 2 | Select another part and click *Add Substitute*. | Part: `QA-<suffix> Comp C` | A second substitute is added: "a particular line item may have multiple substitute parts assigned to it" (R-Detail_View-57). Open: Q-Detail_View-08 (where both are shown). |

**Postconditions and cleanup:** the line has two substitutes. Cleanup as `admin`: remove the substitutes, delete the line, set the assembly inactive and delete it and the components, then the category.

**Notes:** None.

---

### UI-Detail_View-036: The component of the line cannot be added as its own substitute

| Field | Value |
|---|---|
| **Summary** | In the *Edit BOM Item Substitutes* form, the line's own component is chosen as the substitute. |
| **Requirement** | `R-Detail_View-63`, `R-Detail_View-57`. Source: [manufacturing-bom.md#Add Substitute for BOM Item](../../requirements/docs/manufacturing-bom.md#L147), [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L71) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (substitute equals the component) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, open the *Edit BOM Item Substitutes* form of the line. |
| **Automation** | Partial: the outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the line's own component and click *Add Substitute*. | Part: `QA-<suffix> Comp A` | Not known: depends on open question Q-Detail_View-08 (whether the part is left out of the list or the form is rejected, and the error text). |

**Postconditions and cleanup:** no substitute expected. Cleanup as `admin`: remove any substitute, delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** the docs state no restriction on substitutes.

**Duplicate check:** 53 · Review · matches: [UI-Detail_View-037](bom-tab-editing-and-validation.md) (53)

**Duplicate judgement:** Keep · Different class and starting state from UI-Detail_View-037: the line's own component is used as the substitute, on a line that has no substitutes, versus an existing substitute added again. · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-037: The same substitute cannot be added twice to one line

| Field | Value |
|---|---|
| **Summary** | A substitute already assigned to a line is added a second time. |
| **Requirement** | `R-Detail_View-63`, `R-Detail_View-57`. Source: [manufacturing-bom.md#Add Substitute for BOM Item](../../requirements/docs/manufacturing-bom.md#L147), [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L71) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate substitute) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2 and substitute `QA-<suffix> Comp B` on that line, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*, open the *Edit BOM Item Substitutes* form of the line. |
| **Automation** | Partial: the outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the same substitute and click *Add Substitute*. | Part: `QA-<suffix> Comp B` | Not known: depends on open question Q-Detail_View-08 (whether the duplicate is rejected or the part is not offered, and the error text). |

**Postconditions and cleanup:** one substitute expected. Cleanup as `admin`: remove the substitute, delete the line, set the assembly inactive and delete it and the components, then the category.

**Notes:** the docs state no uniqueness rule for substitutes.

**Duplicate check:** 53 · Review · matches: [UI-Detail_View-036](bom-tab-editing-and-validation.md) (53)

**Duplicate judgement:** Keep · Different starting state and class from UI-Detail_View-036: the line already has substitute Comp B, which is added again (a duplicate substitute), versus the line's own component. · test-case-reviewer, 2026-10-15
