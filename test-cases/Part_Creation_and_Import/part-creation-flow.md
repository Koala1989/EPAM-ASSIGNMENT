# Part creation flow: Part test cases

### UI-Part-002: Add Parts dropdown offers create and import options

| Field | Value |
|---|---|
| **Summary** | The *Add Parts* dropdown above the parts table in the *Parts* view shows the create and import options for a user with create permission. |
| **Requirement** | `R-Part-02`. Source: [part-create.md#L17](../../requirements/docs/part-create.md#L17) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: user with create permission) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in at `http://localhost/web`. |
| **Automation** | Yes: simple visibility check. |
| **Review** | Approved · 2026-10-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Parts* view. | None | The parts table is shown with the *Add Parts* dropdown above it. |
| 2 | Open the *Add Parts* dropdown. | None | The menu lists *Create Part* and *Import from File*. |

**Postconditions and cleanup:** none, no data created.

**Notes:** the docs name *Create Part* and *Import from File* as the options; whether further options appear (for example supplier import with a plugin) is not stated.

---

### UI-Part-003: Add Parts menu is not available without create permission

| Field | Value |
|---|---|
| **Summary** | A user without "create" permission for the *Part* permission group does not see the *Add Parts* menu. |
| **Requirement** | `R-Part-03`. Source: [part-create.md#L21-22](../../requirements/docs/part-create.md#L21-L22) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Negative (user without create permission), Decision table (permission: create absent) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view-only); Settings: None; Data: None; Pre-steps: log in at `http://localhost/web`. |
| **Automation** | Yes: permission check. |
| **Review** | Approved · 2026-10-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Parts* view. | None | The parts table is shown. |
| 2 | Look above the parts table for the *Add Parts* dropdown. | None | The *Add Parts* menu is not available. |

**Postconditions and cleanup:** none, no data created.

**Notes:** `reader` is assumed by the seed to have no create rights; confirm in the user's permission groups if the menu is shown.

---

### UI-Part-004: Create a part with optional IPN, Keywords and Link filled

| Field | Value |
|---|---|
| **Summary** | A part can be created with the optional IPN, Keywords and Link fields filled, and the values show on the detail page. |
| **Requirement** | `R-Part-12`, `R-Part-16`, `R-Part-17`, `R-Part-06`. Source: [part-views.md#L30](../../requirements/docs/part-views.md#L30), [part-views.md#L38](../../requirements/docs/part-views.md#L38), [part-views.md#L40](../../requirements/docs/part-views.md#L40), [part-create.md#L33](../../requirements/docs/part-create.md#L33) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: all optional text fields filled with valid values) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: non-structural category `QA-<suffix> Category`, created as `admin`; Pre-steps: log in at `http://localhost/web`, open the *Parts* view, open *Add Parts* > *Create Part*. |
| **Automation** | Yes: form fill and detail check. |
| **Review** | Approved · 2026-10-11 · passed the MCP re-run; agent draft changed first: the docs call the field *External Link* (part-views.md#L40) but the 1.5.6 form and detail page label it *Link*, so it is renamed to *Link* throughout; removed the `[confirm in app: required fields]` placeholder. |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name, Category and the optional fields. | Name: `QA-<suffix> Capacitor 100n`<br>Category: `QA-<suffix> Category`<br>IPN: `QA-<suffix>-IPN1`<br>Keywords: `qa<suffix>cap ceramic`<br>Link: `https://example.com/datasheet` | Fields accept the values, no form errors are shown. |
| 2 | Press *Submit*. | None | The browser is redirected to the new part's detail page. |
| 3 | Check the part details. | None | IPN, Keywords and Link show the values from step 1. |

**Postconditions and cleanup:** one new part. Cleanup as `admin`: set the part inactive, delete it, then delete the category.

**Notes:** the docs name this field *External Link*; the 1.5.6 UI label is *Link* (index doc issue 13). An invalid URL or one without a scheme is rejected with "Enter a valid URL." (confirmed in the InvenTree 1.5.6 API, 2026-10-11).

---

### UI-Part-005: Supplier Information section shows only while Purchaseable is checked

| Field | Value |
|---|---|
| **Summary** | In the *Create Part* form, the *Supplier Information* section is shown while *Purchaseable* is checked (the default), hidden when it is unchecked, and shown again when it is re-checked. |
| **Requirement** | `R-Part-09`. Source: [part-create.md#L47](../../requirements/docs/part-create.md#L47) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | State transition (Purchaseable checked → unchecked → checked) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_PURCHASEABLE` = on (new parts Purchaseable by default), `PART_CREATE_SUPPLIER` = on (Initial Supplier Data); Data: None; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes: form field visibility. |
| **Review** | Approved · 2026-10-11 · passed the MCP re-run; agent draft changed first: (1) the docs' *Add Supplier Data* option (part-create.md#L51) does not exist in 1.5.6, the fields are in a *Supplier Information* section; (2) *Purchaseable* is checked by default, so "set to checked" first tested nothing. Reordered to default → unchecked → re-checked and added the two settings. |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the *Purchaseable* option and the form sections. | None | *Purchaseable* is checked. The *Supplier Information* section is shown with the fields *Supplier*, *SKU*, *Manufacturer* and *MPN*. |
| 2 | Uncheck *Purchaseable*. | None | The *Supplier Information* section is no longer shown. |
| 3 | Check *Purchaseable* again. | None | The *Supplier Information* section is shown again. |

**Postconditions and cleanup:** none, the form is closed without submitting (Cancel).

**Notes:** the docs describe an older form with an *Add Supplier Data* option (index doc issue 14).

---

### UI-Part-006: Create a part with supplier and manufacturer data from the Supplier Information section

| Field | Value |
|---|---|
| **Summary** | Supplier part and manufacturer part data entered in the *Supplier Information* section of the *Create Part* form is saved with the new part and listed on its *Suppliers* tab. |
| **Requirement** | `R-Part-09`, `R-Part-10`, `R-Part-06`, `R-Detail_View-23`. Source: [part-create.md#L47](../../requirements/docs/part-create.md#L47), [part-create.md#L51](../../requirements/docs/part-create.md#L51), [part-create.md#L33](../../requirements/docs/part-create.md#L33), [part-views.md#L100-102](../../requirements/docs/part-views.md#L100-L102) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Decision table (Purchaseable = checked, supplier and manufacturer data entered) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (steps 1-3: manage parts), `allaccess` (step 4: needs purchase-order view to see the *Suppliers* tab); Settings: `PART_PURCHASEABLE` = on, `PART_CREATE_SUPPLIER` = on; Data: non-structural category `QA-<suffix> Category`, supplier company `QA-<suffix> Supplier` and manufacturer company `QA-<suffix> Manufacturer`, created as `admin`; Pre-steps: log in as `engineer` at `http://localhost/web`, open *Parts* > *Add Parts* > *Create Part*. |
| **Automation** | Yes: form fill, then a second user for the tab check. |
| **Review** | Approved · 2026-10-11 · passed the MCP re-run; agent draft changed first: (1) *Add Supplier Data* does not exist in 1.5.6, so that step is removed; (2) `engineer` has no purchase-order permission and cannot see the *Suppliers* tab, so step 4 now uses `allaccess`. The agent's original step 5 was inferred, not documented. |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Fill in Name and Category; leave *Purchaseable* checked. | Name: `QA-<suffix> Connector`<br>Category: `QA-<suffix> Category` | The *Supplier Information* section is shown. |
| 2 | Enter the supplier and manufacturer data in *Supplier Information*. | Supplier: `QA-<suffix> Supplier`<br>SKU: `QA-<suffix>-SKU1`<br>Manufacturer: `QA-<suffix> Manufacturer`<br>MPN: `QA-<suffix>-MPN1` | Fields accept the values, no form errors are shown. |
| 3 | Press *Submit*. | None | The browser is redirected to the new part's detail page. |
| 4 | Log out, log in as `allaccess`, open the new part and its *Suppliers* tab. | None | The supplier part (`QA-<suffix> Supplier`, SKU `QA-<suffix>-SKU1`) is listed, and the tab's *Manufacturers* section lists the manufacturer part (`QA-<suffix> Manufacturer`, MPN `QA-<suffix>-MPN1`). |

**Postconditions and cleanup:** one new part with a supplier part and a manufacturer part. Cleanup as `admin`: delete the supplier part and manufacturer part, set the part inactive, delete it, then delete the category and companies.

**Notes:** `engineer` can create the supplier and manufacturer parts through this form but cannot see them afterwards (F-03 in `test-cases/findings.md`). The *Suppliers* tab permission is not in the docs (index doc issue 15).
