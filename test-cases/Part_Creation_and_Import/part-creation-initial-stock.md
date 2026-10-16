# Part creation initial stock: Part test cases

### UI-Part-029: Initial stock section is shown when Create Initial Stock is enabled

| Field | Value |
|---|---|
| **Summary** | With the *Create Initial Stock* setting enabled, the *Create Part* form has an extra section for creating initial stock. |
| **Requirement** | `R-Part-07`, `R-Part-08`. Source: [part-create.md#L37](../../requirements/docs/part-create.md#L37), [part-create.md#L43](../../requirements/docs/part-create.md#L43) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Decision table (setting = on) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Part-12, whether stock-create permission is also needed]; Settings: *Create Initial Stock* = on [open: Q-Part-07, setting key and where it is changed]; Data: None; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes: form section visibility. |
| **Review** | Draft · Open question: Q-Part-07, Q-Part-08, Q-Part-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the sections of the open *Create Part* form. | None | An extra section for creating initial stock is available in the form (R-Part-07). Open: Q-Part-08 (section title and field labels). |
| 2 | Look for the *Create Initial Stock* input in the form. | None | A *Create Initial Stock* form input is present (R-Part-08). Open: Q-Part-08 (input type, default state, and whether checking it reveals more fields). |
| 3 | Press *Cancel*. | None | The form closes and no part is created. |

**Postconditions and cleanup:** none, the form is closed without submitting. Restore the setting as `admin`.

**Notes:** The setting key, default and the form labels are not in the docs (index doc issue 8); the docs show the section only as an image.

---

### UI-Part-030: Initial stock section is not shown when Create Initial Stock is disabled

| Field | Value |
|---|---|
| **Summary** | With the *Create Initial Stock* setting disabled, the *Create Part* form has no initial stock section. |
| **Requirement** | `R-Part-07`. Source: [part-create.md#L37](../../requirements/docs/part-create.md#L37) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Decision table (setting = off), Negative (opposite of a positively worded rule) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Part-12, whether stock-create permission is also needed]; Settings: *Create Initial Stock* = off [open: Q-Part-07, setting key, default and where it is changed]; Data: None; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes: form section visibility. |
| **Review** | Draft · Open question: Q-Part-07, Q-Part-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the sections of the open *Create Part* form. | None | Proposed, to confirm in Q-Part-09: no initial stock section and no *Create Initial Stock* input are shown. Open: Q-Part-07 (setting key and how to disable it). |
| 2 | Press *Cancel*. | None | The form closes and no part is created. |

**Postconditions and cleanup:** none. Restore the setting as `admin`.

**Notes:** The docs state only the enabled case (part-create.md#L37); the disabled outcome is proposed.

---

### UI-Part-031: Create a part with initial stock

| Field | Value |
|---|---|
| **Summary** | Checking *Create Initial Stock* and entering a quantity creates the part and an initial stock item of that quantity. |
| **Requirement** | `R-Part-08`, `R-Part-06`. Source: [part-create.md#L43](../../requirements/docs/part-create.md#L43), [part-create.md#L33](../../requirements/docs/part-create.md#L33) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Create Initial Stock checked, valid quantity) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Part-12, whether stock-create permission is also needed]; Settings: *Create Initial Stock* = on [open: Q-Part-07, setting key and where it is changed]; Data: non-structural category `QA-<suffix> Category`, created via `POST /api/part/category/` as `admin`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes: core flow. |
| **Review** | Draft · Open question: Q-Part-07, Q-Part-08, Q-Part-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the part fields. | Name: `QA-<suffix> Stocked Part`<br>Category: `QA-<suffix> Category` | Fields accept the values, no form errors. |
| 2 | Check *Create Initial Stock* and enter the stock data. | Quantity: `10`<br>Location: [open: Q-Part-08, whether a location is required and its label] | An initial quantity of stock can be created for the new part (R-Part-08). Open: Q-Part-08 (field labels). |
| 3 | Press *Submit*. | None | The browser is redirected to the new part's detail page (R-Part-06). |
| 4 | Open the *Stock* tab of the new part. | None | A stock item with quantity `10` is listed for the part (R-Part-08). Open: Q-Part-08 (the stock item's location and status). |

**Postconditions and cleanup:** one new part `QA-<suffix> Stocked Part` with a stock item. Cleanup as `admin`: delete the stock item, set the part inactive, delete it, delete the category, and restore the setting.

**Notes:** The setting key, default and the form labels are not in the docs (index doc issue 8); the docs show the section only as an image.

---

### UI-Part-032: Create a part with Create Initial Stock left unchecked creates no stock

| Field | Value |
|---|---|
| **Summary** | With the setting enabled but the *Create Initial Stock* input left unchecked, the part is created without a stock item. |
| **Requirement** | `R-Part-08`, `R-Part-06`. Source: [part-create.md#L43](../../requirements/docs/part-create.md#L43), [part-create.md#L33](../../requirements/docs/part-create.md#L33) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | State transition (Create Initial Stock unchecked), Negative (opposite of a positively worded rule) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Part-12, whether stock-create permission is also needed]; Settings: *Create Initial Stock* = on [open: Q-Part-07, setting key and where it is changed]; Data: non-structural category `QA-<suffix> Category`, created via `POST /api/part/category/` as `admin`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part-07, Q-Part-08, Q-Part-09, Q-Part-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the part fields. Leave *Create Initial Stock* unchecked. | Name: `QA-<suffix> No Stock Part`<br>Category: `QA-<suffix> Category` | Fields accept the values. Open: Q-Part-08 (whether the input is unchecked by default). |
| 2 | Press *Submit*. | None | The browser is redirected to the new part's detail page (R-Part-06). |
| 3 | Open the *Stock* tab. | None | Proposed, to confirm in Q-Part-09: the part has no stock items. |

**Postconditions and cleanup:** one new part `QA-<suffix> No Stock Part`. Cleanup as `admin`: set the part inactive, delete it, delete the category, restore the setting.

**Notes:** The setting key, default and the form labels are not in the docs (index doc issue 8); the docs show the section only as an image.

---

### UI-Part-033: Initial stock quantity zero

| Field | Value |
|---|---|
| **Summary** | With *Create Initial Stock* checked, a quantity of 0 is handled at the lower boundary. |
| **Requirement** | `R-Part-08`. Source: [part-create.md#L43](../../requirements/docs/part-create.md#L43) |
| **Area** | Part |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (quantity = 0) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Part-12, whether stock-create permission is also needed]; Settings: *Create Initial Stock* = on [open: Q-Part-07, setting key and where it is changed]; Data: non-structural category `QA-<suffix> Category`, created via `POST /api/part/category/` as `admin`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part-07, Q-Part-08, Q-Part-09, Q-Part-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the part fields, check *Create Initial Stock* and enter quantity 0. | Name: `QA-<suffix> Zero Stock`<br>Category: `QA-<suffix> Category`<br>Quantity: `0` | Fields accept the entry. Open: Q-Part-08 (quantity field label). |
| 2 | Press *Submit*. | None | Not known: depends on open question Q-Part-09 (whether quantity 0 is rejected with an error, or the part is created without a stock item). |
| 3 | If the part was created, open its *Stock* tab. | None | Not known: depends on open question Q-Part-09 (whether a zero-quantity stock item exists). |

**Postconditions and cleanup:** a part may exist. Cleanup as `admin`: delete any stock item, set the part inactive, delete it, delete the category, restore the setting.

**Notes:** The setting key, default and the form labels are not in the docs (index doc issue 8); the docs show the section only as an image.

---

### UI-Part-034: Initial stock quantity negative is rejected

| Field | Value |
|---|---|
| **Summary** | With *Create Initial Stock* checked, a negative quantity is not accepted. |
| **Requirement** | `R-Part-08`, `R-Part-05`. Source: [part-create.md#L43](../../requirements/docs/part-create.md#L43), [part-create.md#L31](../../requirements/docs/part-create.md#L31) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: negative quantity), Boundary value analysis (quantity = -1) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Part-12, whether stock-create permission is also needed]; Settings: *Create Initial Stock* = on [open: Q-Part-07, setting key and where it is changed]; Data: non-structural category `QA-<suffix> Category`, created via `POST /api/part/category/` as `admin`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part-07, Q-Part-08, Q-Part-09, Q-Part-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the part fields, check *Create Initial Stock* and enter quantity -1. | Name: `QA-<suffix> Negative Stock`<br>Category: `QA-<suffix> Category`<br>Quantity: `-1` | Open: Q-Part-08 (quantity field label). |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Part-09: the form shows an error on the quantity field and stays open. A form that shows errors cannot be submitted (R-Part-05). Open: Q-Part-09 (error text). |
| 3 | Search the *Parts* view for the name. | `QA-<suffix> Negative Stock` | Proposed, to confirm in Q-Part-09: no part is created. |

**Postconditions and cleanup:** no part created. Cleanup as `admin`: delete the category and restore the setting.

**Notes:** The setting key, default and the form labels are not in the docs (index doc issue 8); the docs show the section only as an image.

**Duplicate check:** 61 · Review · matches: [UI-Part-035](part-creation-initial-stock.md) (61)

**Duplicate judgement:** Keep · Negative quantity (-1, invalid numeric class just below the 0 boundary); UI-Part-035 covers the empty and non-numeric invalid classes, different equivalence classes of the quantity input. · test-case-reviewer, 2026-10-15

---

### UI-Part-035: Initial stock quantity left empty is rejected

| Field | Value |
|---|---|
| **Summary** | With *Create Initial Stock* checked, an empty quantity is not accepted. |
| **Requirement** | `R-Part-08`, `R-Part-05`. Source: [part-create.md#L43](../../requirements/docs/part-create.md#L43), [part-create.md#L31](../../requirements/docs/part-create.md#L31) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Part-12, whether stock-create permission is also needed]; Settings: *Create Initial Stock* = on [open: Q-Part-07, setting key and where it is changed]; Data: non-structural category `QA-<suffix> Category`, created via `POST /api/part/category/` as `admin`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part-07, Q-Part-08, Q-Part-09, Q-Part-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the part fields, check *Create Initial Stock*, leave the quantity empty and press *Submit*. | Name: `QA-<suffix> Blank Qty`<br>Category: `QA-<suffix> Category`<br>Quantity: empty | Proposed, to confirm in Q-Part-09: an error is shown and the form stays open. Open: Q-Part-09 (error text, and whether an empty quantity is rejected or ignored). |
| 2 | Search the *Parts* view for the name. | `QA-<suffix> Blank Qty` | Proposed, to confirm in Q-Part-09: no part is created. |

**Postconditions and cleanup:** no part created. Cleanup as `admin`: delete the category and restore the setting.

**Notes:** The non-numeric quantity is UI-Part-041. The setting key, default and the form labels are not in the docs (index doc issue 8); the docs show the section only as an image.

**Duplicate check:** 61 · Review · matches: [UI-Part-034](part-creation-initial-stock.md) (61)

**Duplicate judgement:** Keep · Empty and non-numeric quantity (invalid non-number classes); UI-Part-034 sends a negative number, a different invalid class next to the 0 boundary. · test-case-reviewer, 2026-10-15

---

### UI-Part-036: Initial stock for a Virtual part

| Field | Value |
|---|---|
| **Summary** | A Virtual part cannot have stock, so creating a Virtual part with *Create Initial Stock* checked must not give it a stock item. |
| **Requirement** | `R-Part-08`, `R-ATT-02`. Source: [part-create.md#L43](../../requirements/docs/part-create.md#L43), [part-virtual.md#L15](../../requirements/docs/part-virtual.md#L15) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Decision table (Virtual = checked x Create Initial Stock = checked), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Part-12, whether stock-create permission is also needed]; Settings: *Create Initial Stock* = on [open: Q-Part-07, setting key and where it is changed]; Data: non-structural category `QA-<suffix> Category`, created via `POST /api/part/category/` as `admin`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-ATT-08, Q-Part-07, Q-Part-08, Q-Part-10, Q-Part-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the part fields and check *Virtual*. | Name: `QA-<suffix> Virtual Stock`<br>Category: `QA-<suffix> Category` | Open: Q-Part-10 (whether the initial stock section is hidden or disabled once *Virtual* is checked). |
| 2 | Check *Create Initial Stock* if it is available, enter a quantity and press *Submit*. | Quantity: `5` | No stock item is created for the part (R-ATT-02). Open: Q-Part-10 (whether the form is rejected with an error, or the part is created without stock, and the error text), Q-ATT-08 (how stock creation for a Virtual part is prevented). |
| 3 | Open the global *Stock* view and search for the part name. | `QA-<suffix> Virtual Stock` | No stock item of `QA-<suffix> Virtual Stock` is listed (R-ATT-02: a Virtual part cannot have stock items). |

**Postconditions and cleanup:** a Virtual part may exist. Cleanup as `admin`: set it inactive, delete it, delete the category, restore the setting.

**Notes:** Step 3 uses the global *Stock* view because a Virtual part's own page hides stock elements (R-ATT-03, covered by UI-ATT-007). The setting key, default and the form labels are not in the docs (index doc issue 8); the docs show the section only as an image.

---

### UI-Part-037: Initial stock for a Trackable part

| Field | Value |
|---|---|
| **Summary** | Creating a Trackable part with initial stock: what the form needs for batch or serial numbers. |
| **Requirement** | `R-Part-08`, `R-ATT-12`, `R-ATT-13`. Source: [part-create.md#L43](../../requirements/docs/part-create.md#L43), [part-index.md#L76](../../requirements/docs/part-index.md#L76), [part-trackable.md#L19-21](../../requirements/docs/part-trackable.md#L19-L21) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Decision table (Trackable = checked x Create Initial Stock = checked), What-if business scenario |
| **Priority** | P3 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Part-12, whether stock-create permission is also needed]; Settings: *Create Initial Stock* = on [open: Q-Part-07, setting key and where it is changed]; Data: non-structural category `QA-<suffix> Category`, created via `POST /api/part/category/` as `admin`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Partial: depends on the answer to Q-Part-11. |
| **Review** | Draft · Open question: Q-Part-07, Q-Part-08, Q-Part-11, Q-Part-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the part fields and check *Trackable*. | Name: `QA-<suffix> Tracked Stock`<br>Category: `QA-<suffix> Category` | Fields accept the values. |
| 2 | Check *Create Initial Stock*, enter the quantity and the serial numbers, and press *Submit*. | Quantity: `3`<br>Serial numbers: `1, 2, 3` [open: Q-Part-11, whether the form offers the field and its label] | Proposed, to confirm in Q-Part-11: the part `QA-<suffix> Tracked Stock` is created and the form closes. A Trackable part's stock items can be assigned serial numbers (R-ATT-12). Open: Q-Part-11 (whether the initial stock section takes serial numbers). |
| 3 | Open the *Stock* tab of `QA-<suffix> Tracked Stock`. | None | Proposed, to confirm in Q-Part-11: three stock items are listed, each of quantity 1, with serial numbers `1`, `2` and `3`. Open: Q-Part-11 (whether one item of quantity 3 is created instead). |

**Postconditions and cleanup:** one new part, possibly with stock. Cleanup as `admin`: delete stock items, set the part inactive, delete it, delete the category, restore the setting.

**Notes:** The setting key, default and the form labels are not in the docs (index doc issue 8); the docs show the section only as an image.

---

### UI-Part-038: Cancel the form after filling initial stock creates nothing

| Field | Value |
|---|---|
| **Summary** | Cancelling the *Create Part* form after checking *Create Initial Stock* and entering a quantity creates no part and no stock. |
| **Requirement** | `R-Part-08`, `R-Part-04`. Source: [part-create.md#L43](../../requirements/docs/part-create.md#L43), [part-create.md#L26](../../requirements/docs/part-create.md#L26) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-form) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Part-12, whether stock-create permission is also needed]; Settings: *Create Initial Stock* = on [open: Q-Part-07, setting key and where it is changed]; Data: non-structural category `QA-<suffix> Category`, created via `POST /api/part/category/` as `admin`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part-07, Q-Part-08, Q-Part-09, Q-Part-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the part fields, check *Create Initial Stock* and enter a quantity. | Name: `QA-<suffix> Cancelled`<br>Category: `QA-<suffix> Category`<br>Quantity: `10` | Open: Q-Part-08 (field labels). |
| 2 | Press *Cancel*. | None | The form closes. Proposed, to confirm in Q-Part-09: no part and no stock item is created. |
| 3 | Search the *Parts* view and the category for the name. | `QA-<suffix> Cancelled` | Proposed, to confirm in Q-Part-09: no part is found. |

**Postconditions and cleanup:** no part created. Cleanup as `admin`: delete the category and restore the setting.

**Notes:** The setting key, default and the form labels are not in the docs (index doc issue 8); the docs show the section only as an image.

---

### UI-Part-039: Add Parts menu is not available to a view-only user when the setting is on

| Field | Value |
|---|---|
| **Summary** | A user without part create permission does not see the *Add Parts* menu, so cannot reach the form with the initial stock section, whatever the setting. |
| **Requirement** | `R-Part-03`, `R-Part-07`. Source: [part-create.md#L21-22](../../requirements/docs/part-create.md#L21-L22), [part-create.md#L37](../../requirements/docs/part-create.md#L37) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Negative (permission), Decision table (setting = on x user without create permission) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions, Settings-dependent |
| **Prerequisites** | User: `reader` (view only); Settings: *Create Initial Stock* = on [open: Q-Part-07, setting key and where it is changed]; Data: None; Pre-steps: log in at `http://localhost/web`, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for the *Add Parts* menu above the parts table. | None | The *Add Parts* menu is not shown (R-Part-03). |

**Postconditions and cleanup:** none. Restore the setting as `admin`.

**Notes:** The *Create Part* form has no documented direct route, so no second step is written.

---

### UI-Part-040: Initial stock section follows the setting after it is changed

| Field | Value |
|---|---|
| **Summary** | After an administrator turns *Create Initial Stock* off, a new *Create Part* form no longer shows the initial stock section, and turning it on shows it again. |
| **Requirement** | `R-Part-07`. Source: [part-create.md#L37](../../requirements/docs/part-create.md#L37) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | State transition (setting on, off, on) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent, Cross-functional |
| **Prerequisites** | User: `admin` (changes the setting), `engineer` (opens the form); Settings: *Create Initial Stock* = on at the start [open: Q-Part-07, setting key and where it is changed]; Data: None; Pre-steps: log in as `engineer` at `http://localhost/web`. |
| **Automation** | Partial: setting change location unknown. |
| **Review** | Draft · Open question: Q-Part-07, Q-Part-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | As `engineer`, open *Parts* > *Add Parts* > *Create Part*, note the sections, then cancel. | None | The initial stock section is shown (R-Part-07). |
| 2 | As `admin`, set *Create Initial Stock* off. | [open: Q-Part-07, setting location] | The setting is saved. |
| 3 | As `engineer`, reload and open the *Create Part* form again. | None | Proposed, to confirm in Q-Part-09: the initial stock section is not shown. |
| 4 | As `admin`, set *Create Initial Stock* on again, then as `engineer` open the form. | None | The initial stock section is shown again (R-Part-07). |

**Postconditions and cleanup:** no records. Setting back to its starting value.

**Notes:** The setting key, default and the form labels are not in the docs (index doc issue 8); the docs show the section only as an image.

---

### UI-Part-041: Initial stock quantity that is not a number is rejected

| Field | Value |
|---|---|
| **Summary** | With *Create Initial Stock* checked, a text quantity is not accepted. |
| **Requirement** | `R-Part-08`, `R-Part-05`. Source: [part-create.md#L43](../../requirements/docs/part-create.md#L43), [part-create.md#L31](../../requirements/docs/part-create.md#L31) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: non-numeric), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Part-12, whether stock-create permission is also needed]; Settings: *Create Initial Stock* = on [open: Q-Part-07, setting key and where it is changed]; Data: non-structural category `QA-<suffix> Category`, created via `POST /api/part/category/` as `admin`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part-07, Q-Part-08, Q-Part-09, Q-Part-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in the part fields, check *Create Initial Stock*, enter text as the quantity and press *Submit*. | Name: `QA-<suffix> Text Qty`<br>Category: `QA-<suffix> Category`<br>Quantity: `abc` | Proposed, to confirm in Q-Part-09: an error is shown on the quantity field and the form stays open. Open: Q-Part-09 (error text). |
| 2 | Search the *Parts* view for the name. | `QA-<suffix> Text Qty` | Proposed, to confirm in Q-Part-09: no part is created. |

**Postconditions and cleanup:** no part created. Cleanup as `admin`: delete the category and restore the setting.

**Notes:** Split from UI-Part-035 (the empty quantity). The setting key, default and the form labels are not in the docs (index doc issue 8); the docs show the section only as an image.

**Duplicate check:** 71 · Review · matches: [UI-Part-035](part-creation-initial-stock.md) (71), [UI-Part-034](part-creation-initial-stock.md) (69)

---
