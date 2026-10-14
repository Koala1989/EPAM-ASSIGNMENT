# Unit_measure: Unit_measure test cases


### UI-Unit_measure-001: A user can set a part's unit of measure to `kg`, and the unit is saved and shown on the part

| Field | Value |
|---|---|
| **Summary** | A user can set a part's unit of measure to `kg`, and the unit is saved and shown on the part. |
| **Requirement** | R-Unit_measure-01, [part-index.md#L120](../../requirements/docs/part-index.md#L120) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: compatible physical unit) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: category `QA-<suffix> Category` created via `POST /api/part/category/` as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes: core flow. |
| **Review** | Draft · Open question: Q-Unit_measure-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Create Part* form. | None | The form opens. |
| 2 | Fill in name, category and the unit field. | Name: `QA-<suffix> Wire`<br>Description: `Unit test part`<br>Category: `QA-<suffix> Category`<br>Unit: `kg` (field [open: Q-Unit_measure-02, label of the units field]) | The field accepts `kg` with no validation error. |
| 3 | Press *Submit*. | None | The part is created and the detail page opens. |
| 4 | Check the part details. | None | The part's unit of measure shows `kg`. Exact detail-page label [open: Q-Unit_measure-02, label of the units field]. |

**Postconditions and cleanup:** One part `QA-<suffix> Wire`. Cleanup as `admin`: set inactive, delete, then delete the category.

**Notes:** None


### UI-Unit_measure-002: The unit field of a new part has the documented default when the *Create Part* form opens

| Field | Value |
|---|---|
| **Summary** | The unit field of a new part has the documented default when the *Create Part* form opens. |
| **Requirement** | R-Unit_measure-02, [part-index.md#L120](../../requirements/docs/part-index.md#L120), [part-views.md#L44](../../requirements/docs/part-views.md#L44) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: no unit given), State transition (default state) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: None; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-01 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Create Part* form. | None | The form opens. |
| 2 | Read the value of the unit field before typing. | None | Not known: depends on open question Q-Unit_measure-01 (blank per part-index.md#L120, or `pcs` per part-views.md#L44). |

**Postconditions and cleanup:** No record created. Close the form.

**Notes:** Docs conflict (index doc issue 1).


### UI-Unit_measure-003: A part saved without a unit is tracked in dimensionless pieces

| Field | Value |
|---|---|
| **Summary** | A part saved without a unit is tracked in dimensionless pieces. |
| **Requirement** | R-Unit_measure-02, [part-index.md#L120](../../requirements/docs/part-index.md#L120) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: no unit) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: category `QA-<suffix> Category` created via `POST /api/part/category/` as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-01 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a part and leave the unit field untouched. | Name: `QA-<suffix> Piece Part`<br>Description: `No unit`<br>Category: `QA-<suffix> Category` | The part is created. |
| 2 | Check the part details. | None | Not known: depends on open question Q-Unit_measure-01 (the unit shown is blank per part-index.md#L120, or `pcs` per part-views.md#L44). Quantities are dimensionless pieces. |

**Postconditions and cleanup:** One part. Cleanup as `admin`: set inactive, delete, then delete the category.

**Notes:** None


### UI-Unit_measure-004: A part can be set to a litre unit to track a volume quantity

| Field | Value |
|---|---|
| **Summary** | A part can be set to a litre unit to track a volume quantity. |
| **Requirement** | R-Unit_measure-03, [part-index.md#L127](../../requirements/docs/part-index.md#L127) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: volume unit) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: category `QA-<suffix> Category` created via `POST /api/part/category/` as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Unit_measure-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Create Part* form and fill it in with a litre unit. | Name: `QA-<suffix> Solvent`<br>Description: `Tracked in litres`<br>Category: `QA-<suffix> Category`<br>Unit: `litres` (field [open: Q-Unit_measure-02, label of the units field]) | The field accepts the value with no validation error. |
| 2 | Press *Submit* and check the details. | None | The part is created and its unit shows `litres` (or an equivalent form [open: Q-Unit_measure-02, display form of the unit]). |

**Postconditions and cleanup:** One part. Cleanup as `admin`: set inactive, delete, then delete the category.

**Notes:** None


### UI-Unit_measure-005: A new supplier part takes the unit of its base part by default

| Field | Value |
|---|---|
| **Summary** | A new supplier part takes the unit of its base part by default. |
| **Requirement** | R-Unit_measure-04, [part-index.md#L133](../../requirements/docs/part-index.md#L133) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: default unit) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: allaccess (full create, edit); Settings: None; Data: `QA-<suffix> Cable` (unit `metres`), supplier `QA-<suffix> Supplier`; created via the UI or API as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Unit_measure-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the base part's *Suppliers* tab and start adding a supplier part. | Supplier: `QA-<suffix> Supplier`<br>SKU: `QA-<suffix>-SKU1` | The supplier part form opens. |
| 2 | Read the supplier part unit field [open: Q-Unit_measure-04, label of the supplier part unit field]. | None | The field shows `metres`, the base part's unit. |
| 3 | Submit the form. | None | The supplier part is created with unit `metres`. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the supplier part, make the part inactive and delete it, then delete the supplier.

**Notes:** None


### UI-Unit_measure-006: A supplier part's unit can be changed to the compatible units `feet`, `cm` and `inches` for a base part in `metres`

| Field | Value |
|---|---|
| **Summary** | A supplier part's unit can be changed to the compatible units `feet`, `cm` and `inches` for a base part in `metres`. |
| **Requirement** | R-Unit_measure-04, [part-index.md#L133](../../requirements/docs/part-index.md#L133) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: compatible length units) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: allaccess (full create, edit); Settings: None; Data: `QA-<suffix> Cable` (unit `metres`), supplier `QA-<suffix> Supplier`; created via the UI or API as `admin`; supplier part `QA-<suffix>-SKU1` exists; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Unit_measure-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Edit the supplier part and set its unit. | Unit: `feet` [open: Q-Unit_measure-04, label of the supplier part unit field] | The change is accepted and saved. |
| 2 | Edit again and set the unit. | Unit: `cm` | The change is accepted and saved. |
| 3 | Edit again and set the unit. | Unit: `inches` | The change is accepted and saved. The supplier part shows the last unit entered. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the supplier part, make the part inactive and delete it, then delete the supplier.

**Notes:** None


### UI-Unit_measure-007: A supplier part unit incompatible with the base part's unit is rejected with an error

| Field | Value |
|---|---|
| **Summary** | A supplier part unit incompatible with the base part's unit is rejected with an error. |
| **Requirement** | R-Unit_measure-05, [part-index.md#L138](../../requirements/docs/part-index.md#L138) |
| **Area** | Unit_measure |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: incompatible unit type), Negative |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: allaccess (full create, edit); Settings: None; Data: `QA-<suffix> Cable` (unit `metres`), supplier `QA-<suffix> Supplier`; created via the UI or API as `admin`; supplier part `QA-<suffix>-SKU1` exists; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-04 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Edit the supplier part and set an incompatible unit. | Unit: `kg` [open: Q-Unit_measure-04, label of the supplier part unit field] | The change is not saved. An error is displayed on the form. Error text not known: depends on open question Q-Unit_measure-04 (error text for an incompatible unit). |
| 2 | Close the form and reopen the supplier part. | None | The unit is still the value from before the attempt. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the supplier part, make the part inactive and delete it, then delete the supplier.

**Notes:** The docs show the error only as an image (`part_units_invalid.png`).


### UI-Unit_measure-008: Changing the base part's unit after a supplier part exists leads to a defined outcome for the supplier part

| Field | Value |
|---|---|
| **Summary** | Changing the base part's unit after a supplier part exists leads to a defined outcome for the supplier part. |
| **Requirement** | R-Unit_measure-04, R-Unit_measure-05, [part-index.md#L133](../../requirements/docs/part-index.md#L133) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | What-if business scenario (base unit changed to an incompatible unit) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: allaccess (full create, edit); Settings: None; Data: `QA-<suffix> Cable` (unit `metres`), supplier `QA-<suffix> Supplier`; created via the UI or API as `admin`; supplier part `QA-<suffix>-SKU1` exists in `metres`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | No: outcome unknown. |
| **Review** | Draft · Open question: Q-Unit_measure-04, Q-Unit_measure-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Edit the base part and change its unit. | Unit: `kg` (field [open: Q-Unit_measure-02, label of the units field]) | Not known: depends on open question Q-Unit_measure-05 (change rejected, supplier part unit reset, or left as is). |
| 2 | Open the supplier part `QA-<suffix>-SKU1`. | None | Not known: depends on open question Q-Unit_measure-05 (the unit the supplier part shows). |

**Postconditions and cleanup:** Restore the base part's unit if changed. Cleanup as `admin`: delete the supplier part, make the part inactive and delete it, then delete the supplier.

**Notes:** None


### UI-Unit_measure-009: A value is converted between compatible mass units

| Field | Value |
|---|---|
| **Summary** | A value is converted between compatible mass units. |
| **Requirement** | R-Unit_measure-06, [concepts-units.md#L24](../../requirements/docs/concepts-units.md#L24) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: mass units) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: `QA-<suffix> Part`, created via the *Create Part* form or `POST /api/part/` as `admin` with unit `kg`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-02 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter a mass value in a compatible unit in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `500 g` | The value is accepted. |
| 2 | Check the resulting quantity. | None | The quantity is `0.5` kg. Where it is displayed [open: Q-Unit_measure-02, location of the converted value]. |

**Postconditions and cleanup:** Remove or revert any data entered, as `admin`.

**Notes:** None

**Duplicate check:** 70 · Review · matches: [UI-Unit_measure-010](unit-of-measure.md) (70)

**Duplicate judgement:** Keep · R-Unit_measure-06 names mass and length as separate unit dimensions, and this case uses a different class and starting state (part in `kg`, value `500 g`) from UI-Unit_measure-010 (part in `metres`, value `100 cm`) · test-case-reviewer, 2026-10-14

### UI-Unit_measure-010: A value is converted between compatible length units

| Field | Value |
|---|---|
| **Summary** | A value is converted between compatible length units. |
| **Requirement** | R-Unit_measure-06, [concepts-units.md#L24](../../requirements/docs/concepts-units.md#L24) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: length units) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: `QA-<suffix> Part`, created via the *Create Part* form or `POST /api/part/` as `admin` with unit `metres`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-02 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter a length value in a compatible unit in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `100 cm` | The value is accepted. |
| 2 | Check the resulting quantity. | None | The quantity is `1` metre. Where it is displayed [open: Q-Unit_measure-02, location of the converted value]. |

**Postconditions and cleanup:** Remove or revert any data entered, as `admin`.

**Notes:** None

**Duplicate check:** 70 · Review · matches: [UI-Unit_measure-009](unit-of-measure.md) (70)

**Duplicate judgement:** Keep · Length is a separate unit dimension named by R-Unit_measure-06, and the part's starting unit (`metres` vs `kg`) and the value class differ from UI-Unit_measure-009 · test-case-reviewer, 2026-10-14

### UI-Unit_measure-011: Engineering notation values `10k3`, `10M3` and `3n02` are accepted and read as the documented numbers

| Field | Value |
|---|---|
| **Summary** | Engineering notation values `10k3`, `10M3` and `3n02` are accepted and read as the documented numbers. |
| **Requirement** | R-Unit_measure-07, [concepts-units.md#L28-32](../../requirements/docs/concepts-units.md#L28-32) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: engineering notation) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: `QA-<suffix> Part`, created via the *Create Part* form or `POST /api/part/` as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-02 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter the value in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `10k3` | Accepted as valid, equal to 10,300. |
| 2 | Enter the value in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `10M3` | Accepted as valid, equal to 10,000,000. |
| 3 | Enter the value in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `3n02` | Accepted as valid, equal to 0.00000000302. |

**Postconditions and cleanup:** Remove or revert any data entered, as `admin`.

**Notes:** None


### UI-Unit_measure-012: Scientific notation values `1E-3`, `1E3` and `-123.45E-3` are accepted and read as the documented numbers

| Field | Value |
|---|---|
| **Summary** | Scientific notation values `1E-3`, `1E3` and `-123.45E-3` are accepted and read as the documented numbers. |
| **Requirement** | R-Unit_measure-08, [concepts-units.md#L36-40](../../requirements/docs/concepts-units.md#L36-40) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: scientific notation) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: `QA-<suffix> Part`, created via the *Create Part* form or `POST /api/part/` as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-02 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter the value in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `1E-3` | Accepted as valid, equal to 0.001. |
| 2 | Enter the value in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `1E3` | Accepted as valid, equal to 1000. |
| 3 | Enter the value in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `-123.45E-3` | Accepted as valid, equal to -0.12345. |

**Postconditions and cleanup:** Remove or revert any data entered, as `admin`.

**Notes:** None


### UI-Unit_measure-013: Scientific notation is case-sensitive: lowercase `1e3` is not valid

| Field | Value |
|---|---|
| **Summary** | Scientific notation is case-sensitive: lowercase `1e3` is not valid. |
| **Requirement** | R-Unit_measure-09, [concepts-units.md#L43](../../requirements/docs/concepts-units.md#L43) |
| **Area** | Unit_measure |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: lowercase exponent), Boundary value analysis (`1E3` valid vs `1e3` invalid) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: `QA-<suffix> Part`, created via the *Create Part* form or `POST /api/part/` as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-03 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-02, Q-Unit_measure-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter the valid form in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `1E3` | Accepted, equal to 1000. |
| 2 | Replace it with the lowercase form. | Value: `1e3` | The value is not valid and is not saved. Error text not known: depends on open question Q-Unit_measure-03 (error text and whether the form is blocked). |

**Postconditions and cleanup:** Remove or revert any data entered, as `admin`.

**Notes:** None


### UI-Unit_measure-014: Feet and inches shorthand `3'` and `6"` is accepted

| Field | Value |
|---|---|
| **Summary** | Feet and inches shorthand `3'` and `6"` is accepted. |
| **Requirement** | R-Unit_measure-10, [concepts-units.md#L49-52](../../requirements/docs/concepts-units.md#L49-52) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: shorthand) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: `QA-<suffix> Part`, created via the *Create Part* form or `POST /api/part/` as `admin` with a length unit; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-02 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter the feet shorthand in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `3'` | Accepted, equal to 3 feet. |
| 2 | Enter the inches shorthand. | Value: `6"` | Accepted, equal to 6 inches. |

**Postconditions and cleanup:** Remove or revert any data entered, as `admin`.

**Notes:** None


### UI-Unit_measure-015: A compound feet and inches value `3'6"` is not supported

| Field | Value |
|---|---|
| **Summary** | A compound feet and inches value `3'6"` is not supported. |
| **Requirement** | R-Unit_measure-10, [concepts-units.md#L49-52](../../requirements/docs/concepts-units.md#L49-52) |
| **Area** | Unit_measure |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: compound measurement) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: `QA-<suffix> Part`, created via the *Create Part* form or `POST /api/part/` as `admin` with a length unit; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-03 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-02, Q-Unit_measure-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter the compound value in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `3'6"` | The value is not supported and is not saved. Error text not known: depends on open question Q-Unit_measure-03 (error text and whether the form is blocked). |

**Postconditions and cleanup:** Remove or revert any data entered, as `admin`.

**Notes:** None


### UI-Unit_measure-016: The unit `kg` in lowercase is accepted

| Field | Value |
|---|---|
| **Summary** | The unit `kg` in lowercase is accepted. |
| **Requirement** | R-Unit_measure-11, [concepts-units.md#L56](../../requirements/docs/concepts-units.md#L56) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: correct case) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: `QA-<suffix> Part`, created via the *Create Part* form or `POST /api/part/` as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-02 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter a value with the unit in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `1 kg` | Accepted as one kilogram. |

**Postconditions and cleanup:** Remove or revert any data entered, as `admin`.

**Notes:** None


### UI-Unit_measure-017: The unit `KG` in uppercase is not valid because units are case-sensitive

| Field | Value |
|---|---|
| **Summary** | The unit `KG` in uppercase is not valid because units are case-sensitive. |
| **Requirement** | R-Unit_measure-11, [concepts-units.md#L56](../../requirements/docs/concepts-units.md#L56) |
| **Area** | Unit_measure |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong case), Error guessing (case of the unit) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts, view stock); Settings: None; Data: `QA-<suffix> Part`, created via the *Create Part* form or `POST /api/part/` as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-03 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-02, Q-Unit_measure-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter a value with the uppercase unit in the field that accepts units [open: Q-Unit_measure-02, field] | Value: `1 KG` | The value is not valid and is not saved. Error text not known: depends on open question Q-Unit_measure-03 (error text and whether the form is blocked). |

**Postconditions and cleanup:** Remove or revert any data entered, as `admin`.

**Notes:** None


### UI-Unit_measure-018: The built-in custom units `piece`, `each`, `dozen`, `hundred` and `thousand` exist and are dimensionless

| Field | Value |
|---|---|
| **Summary** | The built-in custom units `piece`, `each`, `dozen`, `hundred` and `thousand` exist and are dimensionless. |
| **Requirement** | R-Unit_measure-12, [concepts-units.md#L87-93](../../requirements/docs/concepts-units.md#L87-93) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: each built-in unit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: admin; Settings: None; Data: None; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Partial: depends on Q-Unit_measure-06. |
| **Review** | Draft · Open question: Q-Unit_measure-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the settings panel and select the *Physical Units* tab. | None | The tab opens. |
| 2 | Look for the built-in units. | None | Not known: depends on open question Q-Unit_measure-06 (whether `piece`, `each`, `dozen`, `hundred`, `thousand` are listed in the tab). Their meanings are one item, one item, 12, 100 and 1000, all dimensionless. |

**Postconditions and cleanup:** None.

**Notes:** None


### UI-Unit_measure-019: An admin can open the *Physical Units* tab in the settings panel to view, edit and create custom units

| Field | Value |
|---|---|
| **Summary** | An admin can open the *Physical Units* tab in the settings panel to view, edit and create custom units. |
| **Requirement** | R-Unit_measure-13, [concepts-units.md#L97](../../requirements/docs/concepts-units.md#L97) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: authorised user) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: admin; Settings: None; Data: None; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Unit_measure-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the settings panel. | None | The settings panel opens. |
| 2 | Select the *Physical Units* tab. | None | The tab opens and shows the custom units with controls to add and edit a unit. Exact control labels [open: Q-Unit_measure-06, fields and labels]. |

**Postconditions and cleanup:** None.

**Notes:** None


### UI-Unit_measure-020: Users without the required permission cannot manage custom units in the *Physical Units* tab

| Field | Value |
|---|---|
| **Summary** | Users without the required permission cannot manage custom units in the *Physical Units* tab. |
| **Requirement** | R-Unit_measure-13, [concepts-units.md#L97](../../requirements/docs/concepts-units.md#L97) |
| **Area** | Unit_measure |
| **Type** | Negative |
| **Technique** | Negative (blocked users), Decision table (role column: reader, noaccess) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: reader, then noaccess; Settings: None; Data: None; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | No: expected outcome unknown. |
| **Review** | Draft · Open question: Q-Unit_measure-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Log in as `reader` and try to open the settings panel and the *Physical Units* tab. | None | Not known: depends on open question Q-Unit_measure-06 (permission required, and whether the tab is hidden or read-only). |
| 2 | Log out, log in as `noaccess` and repeat. | None | Not known: depends on open question Q-Unit_measure-06 (same). |

**Postconditions and cleanup:** None.

**Notes:** Docs do not state a permission (Not in docs item 10).


### UI-Unit_measure-021: A custom unit can be created as an alias of an existing unit

| Field | Value |
|---|---|
| **Summary** | A custom unit can be created as an alias of an existing unit. |
| **Requirement** | R-Unit_measure-14, [concepts-units.md#L78](../../requirements/docs/concepts-units.md#L78) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: alias) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: admin; Settings: None; Data: None; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Partial: depends on Q-Unit_measure-07. |
| **Review** | Draft · Open question: Q-Unit_measure-06, Q-Unit_measure-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Physical Units* tab and start creating a unit. | None | The create form opens. Fields [open: Q-Unit_measure-06, fields and labels]. |
| 2 | Enter a name and a definition that aliases an existing unit. | Name: `qa<suffix>unit`<br>Definition: [open: Q-Unit_measure-07, definition syntax for an alias of `metre`] | The unit is saved and appears in the list. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the custom unit `qa<suffix>unit`.

**Notes:** None

**Duplicate check:** 52 · Review · matches: [UI-Unit_measure-022](unit-of-measure.md) (52)

**Duplicate judgement:** Keep · This case tests R-Unit_measure-14 (an alias of an existing unit), while UI-Unit_measure-022 tests R-Unit_measure-15 (a dimensionless unit defined as `1`) · test-case-reviewer, 2026-10-14

### UI-Unit_measure-022: A custom dimensionless unit is created with the literal `1` as its definition

| Field | Value |
|---|---|
| **Summary** | A custom dimensionless unit is created with the literal `1` as its definition. |
| **Requirement** | R-Unit_measure-15, [concepts-units.md#L104](../../requirements/docs/concepts-units.md#L104) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: definition `1`) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: admin; Settings: None; Data: None; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Partial: depends on Q-Unit_measure-06. |
| **Review** | Draft · Open question: Q-Unit_measure-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Physical Units* tab and start creating a unit. | None | The create form opens. Fields [open: Q-Unit_measure-06, fields and labels]. |
| 2 | Enter the name and the definition. | Name: `qa<suffix>box`<br>Definition: `1` | The unit is saved and appears in the list as a dimensionless unit. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the custom unit `qa<suffix>box`.

**Notes:** None

**Duplicate check:** 52 · Review · matches: [UI-Unit_measure-021](unit-of-measure.md) (52)

**Duplicate judgement:** Keep · This case tests R-Unit_measure-15 (a dimensionless definition `1`), a different rule and definition class from the alias in UI-Unit_measure-021 (R-Unit_measure-14) · test-case-reviewer, 2026-10-14

### UI-Unit_measure-023: A custom dimensionless unit with a definition other than `1` does not give a valid dimensionless unit

| Field | Value |
|---|---|
| **Summary** | A custom dimensionless unit with a definition other than `1` does not give a valid dimensionless unit. |
| **Requirement** | R-Unit_measure-15, [concepts-units.md#L104](../../requirements/docs/concepts-units.md#L104) |
| **Area** | Unit_measure |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: definition not `1`), Boundary value analysis (`1` vs `2`) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: admin; Settings: None; Data: None; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | No: outcome unknown. |
| **Review** | Draft · Open question: Q-Unit_measure-06, Q-Unit_measure-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Physical Units* tab and start creating a unit. | None | The create form opens. Fields [open: Q-Unit_measure-06, fields and labels]. |
| 2 | Enter the name and a definition other than `1`. | Name: `qa<suffix>bad`<br>Definition: `2` | Not known: depends on open question Q-Unit_measure-08 (rejection, message, or the unit is saved with a different meaning). |

**Postconditions and cleanup:** If saved, delete the unit as `admin`.

**Notes:** None


### UI-Unit_measure-024: A BOM line's raw amount in grams is accepted for a part in kilograms, and the quantity is calculated in kilograms

| Field | Value |
|---|---|
| **Summary** | A BOM line's raw amount in grams is accepted for a part in kilograms, and the quantity is calculated in kilograms. |
| **Requirement** | R-Unit_measure-16, [manufacturing-bom.md#L29-30](../../requirements/docs/manufacturing-bom.md#L29-30), [manufacturing-bom.md#L41-43](../../requirements/docs/manufacturing-bom.md#L41-43) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: compatible smaller unit) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: engineer (manage parts); Settings: None; Data: assembly `QA-<suffix> Assembly` and component `QA-<suffix> Flour` (unit `kg`), created as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-09 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the assembly's *BOM* tab and start adding a BOM line. | Component: `QA-<suffix> Flour` | The BOM line form opens. |
| 2 | Enter the raw amount and submit. | Raw amount [open: Q-Unit_measure-09, label of the raw amount field]: `500 g` | The line is saved with no error. |
| 3 | Check the BOM line quantity. | None | The quantity is `0.5` kg. Rounding and format [open: Q-Unit_measure-09, rounding of the calculated quantity]. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the BOM line, make the parts inactive and delete them.

**Notes:** None

**Duplicate check:** 72 · Review · matches: [UI-Unit_measure-025](unit-of-measure.md) (72)

**Duplicate judgement:** Keep · This is the merge target for UI-Unit_measure-025: it has the same rule, user and starting state, and it carries the documented exact outcome (`500 g` gives `0.5` kg, manufacturing-bom.md#L49), which 025 does not · test-case-reviewer, 2026-10-14

### UI-Unit_measure-025: A BOM line's raw amount in pounds is accepted for a part in kilograms

| Field | Value |
|---|---|
| **Summary** | A BOM line's raw amount in pounds is accepted for a part in kilograms. |
| **Requirement** | R-Unit_measure-16, [manufacturing-bom.md#L41-43](../../requirements/docs/manufacturing-bom.md#L41-43) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: compatible imperial unit) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts); Settings: None; Data: assembly `QA-<suffix> Assembly` and component `QA-<suffix> Flour` (unit `kg`), created as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-09 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the assembly's *BOM* tab and start adding a BOM line. | Component: `QA-<suffix> Flour` | The BOM line form opens. |
| 2 | Enter the raw amount and submit. | Raw amount [open: Q-Unit_measure-09, label of the raw amount field]: `1 lb` | The line is saved with no error. |
| 3 | Check the BOM line quantity. | None | The quantity is the equivalent in kg. Value and rounding not known: depends on open question Q-Unit_measure-09 (rounding of the calculated quantity). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the BOM line, make the parts inactive and delete them.

**Notes:** None

**Duplicate check:** 72 · Review · matches: [UI-Unit_measure-024](unit-of-measure.md) (72)

**Duplicate judgement:** Merge into UI-Unit_measure-024 · This case has the same rule (R-Unit_measure-16), user, starting state (component in `kg`) and outcome (saved, quantity in kg), and `1 lb` is another value from the same compatible-unit class; carry `1 lb` over as an extra step in 024 · test-case-reviewer, 2026-10-14

### UI-Unit_measure-026: A BOM line's raw amount in an incompatible unit is not accepted for a part in kilograms

| Field | Value |
|---|---|
| **Summary** | A BOM line's raw amount in an incompatible unit is not accepted for a part in kilograms. |
| **Requirement** | R-Unit_measure-16, [manufacturing-bom.md#L41-43](../../requirements/docs/manufacturing-bom.md#L41-43) |
| **Area** | Unit_measure |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: incompatible unit type) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts); Settings: None; Data: assembly `QA-<suffix> Assembly` and component `QA-<suffix> Flour` (unit `kg`), created as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-09 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the assembly's *BOM* tab and start adding a BOM line. | Component: `QA-<suffix> Flour` | The BOM line form opens. |
| 2 | Enter the raw amount and submit. | Raw amount [open: Q-Unit_measure-09, label of the raw amount field]: `2 m` | The line is not saved. Error text not known: depends on open question Q-Unit_measure-09 (error text). The docs state only that units must be compatible. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the BOM line, make the parts inactive and delete them.

**Notes:** Docs say the amount can be given in any compatible unit; the failure for incompatible units is implied, not stated.

**Duplicate check:** 54 · Review · matches: [UI-Unit_measure-027](unit-of-measure.md) (54)

**Duplicate judgement:** Keep · The rule (R-Unit_measure-16 vs R-Unit_measure-17) and the starting state (component in `kg` vs no unit) both differ from UI-Unit_measure-027 · test-case-reviewer, 2026-10-14

### UI-Unit_measure-027: A BOM line's raw amount with a unit is not allowed when the component has no unit of measure

| Field | Value |
|---|---|
| **Summary** | A BOM line's raw amount with a unit is not allowed when the component has no unit of measure. |
| **Requirement** | R-Unit_measure-17, [manufacturing-bom.md#L45](../../requirements/docs/manufacturing-bom.md#L45) |
| **Area** | Unit_measure |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: unit on a unitless part) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts); Settings: None; Data: assembly `QA-<suffix> Assembly` and component `QA-<suffix> Screw` with no unit of measure, created as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-09 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the assembly's *BOM* tab and start adding a BOM line. | Component: `QA-<suffix> Screw` | The BOM line form opens. |
| 2 | Enter a raw amount with a unit and submit. | Raw amount [open: Q-Unit_measure-09, label of the raw amount field]: `5 g` | The line is not saved. Error text not known: depends on open question Q-Unit_measure-09 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the BOM line, make the parts inactive and delete them.

**Notes:** None

**Duplicate check:** 54 · Review · matches: [UI-Unit_measure-026](unit-of-measure.md) (54)

**Duplicate judgement:** Keep · The rule (R-Unit_measure-17 vs R-Unit_measure-16) and the starting state (component with no unit vs in `kg`) both differ from UI-Unit_measure-026 · test-case-reviewer, 2026-10-14

### UI-Unit_measure-028: A plain numeric raw amount is accepted for a component with no unit of measure, and the quantity equals the number

| Field | Value |
|---|---|
| **Summary** | A plain numeric raw amount is accepted for a component with no unit of measure, and the quantity equals the number. |
| **Requirement** | R-Unit_measure-17, [manufacturing-bom.md#L45](../../requirements/docs/manufacturing-bom.md#L45) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: number without unit on unitless part) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts); Settings: None; Data: assembly `QA-<suffix> Assembly` and component `QA-<suffix> Screw` with no unit of measure, created as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-09 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the assembly's *BOM* tab and start adding a BOM line. | Component: `QA-<suffix> Screw` | The BOM line form opens. |
| 2 | Enter a raw amount without a unit and submit. | Raw amount [open: Q-Unit_measure-09, label of the raw amount field]: `5` | The line is saved. |
| 3 | Check the BOM line quantity. | None | The quantity is `5`. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the BOM line, make the parts inactive and delete them.

**Notes:** None


### UI-Unit_measure-029: Raw amounts `500 g`, `0.5 kg` and `1/2 kg` all give a quantity of 0.5 kg

| Field | Value |
|---|---|
| **Summary** | Raw amounts `500 g`, `0.5 kg` and `1/2 kg` all give a quantity of 0.5 kg. |
| **Requirement** | R-Unit_measure-18, [manufacturing-bom.md#L49](../../requirements/docs/manufacturing-bom.md#L49) |
| **Area** | Unit_measure |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid classes: gram form, decimal form, fraction form) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: engineer (manage parts); Settings: None; Data: assembly `QA-<suffix> Assembly` and component `QA-<suffix> Flour` (unit `kg`), created as `admin`; Pre-steps: log in through the login form and open the *Parts* view. |
| **Automation** | Yes, once Q-Unit_measure-09 is answered. |
| **Review** | Draft · Open question: Q-Unit_measure-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the assembly's *BOM* tab and start adding a BOM line. | Component: `QA-<suffix> Flour` | The BOM line form opens. |
| 2 | Enter the raw amount and submit. | Raw amount [open: Q-Unit_measure-09, label of the raw amount field]: `500 g` | The line is saved. Quantity is `0.5` kg. |
| 3 | Edit the line and change the raw amount. | Raw amount: `0.5 kg` | The line is saved. Quantity is still `0.5` kg. |
| 4 | Edit the line and change the raw amount. | Raw amount: `1/2 kg` | The line is saved. Quantity is still `0.5` kg. Display format [open: Q-Unit_measure-09, rounding of the calculated quantity]. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the BOM line, make the parts inactive and delete them.

**Notes:** None
