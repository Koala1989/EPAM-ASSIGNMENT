# Part detail view Stock tab: Detail_View test cases

The part *Stock* tab: the stock item table, *Export*, *New Stock Item*, *Stock Actions*, the part's total stock, the low stock and overstocked flags, and the tab on Virtual parts. The docs describe the tab in a few sentences (columns, button labels, dialog contents, flag display and permissions are not stated), so most outcomes beyond the cited rules are open (Q-Detail_View-56 to Q-Detail_View-63). Parts, locations and stock items are created through the API as `admin`; the minimum and maximum stock levels are set on the part as `admin`.

---

### UI-Detail_View-601: Stock tab lists the part's stock items with quantity, location and status

| Field | Value |
|---|---|
| **Summary** | The *Stock* tab of a part with several stock items lists each item with its quantity, location and status. |
| **Requirement** | `R-Detail_View-09`. Source: [part-views.md#Stock](../../requirements/docs/part-views.md#L58) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: part with several stock items in different locations) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock A`, locations `QA-<suffix> Loc 1` and `QA-<suffix> Loc 2`, stock item 1 (quantity 10, `Loc 1`) and stock item 2 (quantity 5, `Loc 2`, a different status [open: Q-Detail_View-56, status wording]) created via the API as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-56 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Stock* tab. | None | The table lists both stock items (R-Detail_View-09). Open: Q-Detail_View-56 (column labels, default filters). |
| 2 | Check the row of stock item 1. | Quantity 10, `QA-<suffix> Loc 1` | The row shows quantity 10, location `QA-<suffix> Loc 1` and the item's status (R-Detail_View-09). |
| 3 | Check the row of stock item 2. | Quantity 5, `QA-<suffix> Loc 2` | The row shows quantity 5, location `QA-<suffix> Loc 2` and its status (R-Detail_View-09). Open: Q-Detail_View-56 (status wording). |

**Postconditions and cleanup:** Two stock items exist. Cleanup as `admin`: delete the stock items, set the part inactive, delete it, then delete the locations.

**Notes:** None.

---

### UI-Detail_View-602: Stock tab of a part with no stock items

| Field | Value |
|---|---|
| **Summary** | The *Stock* tab of a part that has no stock items opens and shows no stock rows. |
| **Requirement** | `R-Detail_View-09`. Source: [part-views.md#Stock](../../requirements/docs/part-views.md#L58) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (zero stock items), Equivalence partitioning (empty class) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock B` with no stock items, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-56 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Stock* tab. | None | Proposed, to confirm in Q-Detail_View-56: the table is empty (an empty-state message or no rows) and no error is shown. |

**Postconditions and cleanup:** None created by the case. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-603: Total stock is the sum of the part's stock items

| Field | Value |
|---|---|
| **Summary** | A part with stock items of 10 and 5 shows a total stock of 15. |
| **Requirement** | `R-Detail_View-13`. Source: [part-index.md#Total stock](../../requirements/docs/part-index.md#L19) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: several stock items) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock C` with stock items of quantity 10 and 5 (same status) created via the API as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-56 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for the part's total stock on the detail page [open: Q-Detail_View-56, where and under which label it is shown]. | None | The total stock is 15, the sum of all its stock items (R-Detail_View-13). Open: Q-Detail_View-56 (location and label, and whether items with other statuses are included). |
| 2 | Open the *Stock* tab and add up the quantities. | Quantities 10 and 5 | The rows sum to the total shown in step 1 (R-Detail_View-13). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock items, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-604: Total stock follows a stock item added after the page was opened

| Field | Value |
|---|---|
| **Summary** | After another stock item is added to a part, the part's total stock shows the new sum. |
| **Requirement** | `R-Detail_View-13`. Source: [part-index.md#Total stock](../../requirements/docs/part-index.md#L19) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | What-if business scenario (stock received while the page is open), State transition (total 15 to 22) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock D` with stock items of quantity 10 and 5 created via the API as `admin`; Pre-steps: log in, open the part detail page and note the total stock (15). |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-56 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | In a second session, add a stock item of quantity 7 to the part via `POST /api/stock/` as `admin`. | Quantity: `7` | The item is created. |
| 2 | Reload the part detail page. | None | The total stock is 22, the sum of the three items (R-Detail_View-13). Open: Q-Detail_View-56 (where the total is shown). |
| 3 | Open the *Stock* tab. | None | Three rows are listed (R-Detail_View-09). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock items, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-605: Export the part's stock items

| Field | Value |
|---|---|
| **Summary** | *Export* opens an options dialog, then downloads a file with all the part's stock items. |
| **Requirement** | `R-Detail_View-10`. Source: [part-views.md#Export](../../requirements/docs/part-views.md#L68) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: part with stock items) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock) [open: Q-Detail_View-57, permission needed]; Settings: None; Data: part `QA-<suffix> Stock E` with stock items of quantity 10 and 5 created via the API as `admin`; Pre-steps: log in, open the part's *Stock* tab. |
| **Automation** | Partial: the file content check depends on Q-Detail_View-57. |
| **Review** | Draft · Open question: Q-Detail_View-57 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *Export* [open: Q-Detail_View-57, control label]. | None | A dialog to select export options opens (R-Detail_View-10). Open: Q-Detail_View-57 (options and their defaults). |
| 2 | Confirm the dialog with the default options. | None | A file is downloaded containing data for all stock items of this part (R-Detail_View-10). Open: Q-Detail_View-57 (file format, name and columns). |
| 3 | Open the downloaded file. | None | It has data for both stock items (quantities 10 and 5) (R-Detail_View-10). |

**Postconditions and cleanup:** A file is in the browser's download folder; remove it. Cleanup as `admin`: delete the stock items, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-606: Cancel the export dialog

| Field | Value |
|---|---|
| **Summary** | Closing the *Export* options dialog without confirming downloads no file. |
| **Requirement** | `R-Detail_View-10`. Source: [part-views.md#Export](../../requirements/docs/part-views.md#L68) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-flow) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock F` with one stock item of quantity 10 created via the API as `admin`; Pre-steps: log in, open the part's *Stock* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-57 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *Export* [open: Q-Detail_View-57, control label]. | None | The options dialog opens (R-Detail_View-10). |
| 2 | Close the dialog without confirming [open: Q-Detail_View-57, cancel or close control]. | None | Proposed, to confirm in Q-Detail_View-57: the dialog closes, no file is downloaded and the table is unchanged. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock item, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-607: Export for a part with no stock items

| Field | Value |
|---|---|
| **Summary** | *Export* on a part without stock items is handled without an error. |
| **Requirement** | `R-Detail_View-10`. Source: [part-views.md#Export](../../requirements/docs/part-views.md#L68) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (zero stock items), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock G` with no stock items, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part's *Stock* tab. |
| **Automation** | Partial: depends on Q-Detail_View-57. |
| **Review** | Draft · Open question: Q-Detail_View-57 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *Export* [open: Q-Detail_View-57, control label] and confirm the dialog. | None | Proposed, to confirm in Q-Detail_View-57: a file with no stock rows is downloaded, or a message says there is nothing to export; no error page is shown. |

**Postconditions and cleanup:** Remove any downloaded file. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-608: New Stock Item opens a dialog for the part

| Field | Value |
|---|---|
| **Summary** | *New Stock Item* opens a dialog to create a stock item for the selected part. |
| **Requirement** | `R-Detail_View-11`. Source: [part-views.md#New Stock Item](../../requirements/docs/part-views.md#L72) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: user who can create stock) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `allaccess` (full create, edit and delete; the least privileged user that can create stock is not stated [open: Q-Detail_View-58]); Settings: None; Data: part `QA-<suffix> Stock H` created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part's *Stock* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-58 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *New Stock Item* [open: Q-Detail_View-58, control label]. | None | A dialog opens to create a new stock item for the selected part (R-Detail_View-11). Open: Q-Detail_View-58 (title, fields, whether the part is pre-filled). |

**Postconditions and cleanup:** None created. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-609: Create a stock item from the Stock tab

| Field | Value |
|---|---|
| **Summary** | A stock item created with *New Stock Item* appears in the part's *Stock* tab and in its total stock. |
| **Requirement** | `R-Detail_View-11`, `R-Detail_View-09`, `R-Detail_View-13`. Source: [part-views.md#New Stock Item](../../requirements/docs/part-views.md#L72), [part-views.md#Stock](../../requirements/docs/part-views.md#L58), [part-index.md#Total stock](../../requirements/docs/part-index.md#L19) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: all required fields filled), Exploratory (tab and total) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` [open: Q-Detail_View-58, least privileged user]; Settings: None; Data: part `QA-<suffix> Stock I` with no stock and location `QA-<suffix> Loc 1`, created via the API as `admin`; Pre-steps: log in, open the part's *Stock* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-58, Q-Detail_View-56 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *New Stock Item* [open: Q-Detail_View-58, control label]. | None | The dialog opens (R-Detail_View-11). |
| 2 | Fill in the fields [open: Q-Detail_View-58, field labels and required fields]. | Quantity: `10`<br>Location: `QA-<suffix> Loc 1` | The fields accept the values with no validation errors. |
| 3 | Submit the dialog. | None | The dialog closes and the new stock item is listed in the *Stock* tab with quantity 10 and location `QA-<suffix> Loc 1` (R-Detail_View-11, R-Detail_View-09). Open: Q-Detail_View-58 (confirmation message, whether the browser goes to the stock item). |
| 4 | Check the part's total stock. | None | The total stock is 10 (R-Detail_View-13). Open: Q-Detail_View-56 (where the total is shown). |

**Postconditions and cleanup:** One stock item exists. Cleanup as `admin`: delete the stock item, set the part inactive, delete it, then delete the location.

**Notes:** None.

---

### UI-Detail_View-610: New stock item with no values entered

| Field | Value |
|---|---|
| **Summary** | Submitting the *New Stock Item* dialog without filling the required fields creates no stock item. |
| **Requirement** | `R-Detail_View-11`. Source: [part-views.md#New Stock Item](../../requirements/docs/part-views.md#L72) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: required fields empty), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` [open: Q-Detail_View-58, least privileged user]; Settings: None; Data: part `QA-<suffix> Stock J` with no stock, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part's *Stock* tab. |
| **Automation** | Partial: error text and required fields depend on Q-Detail_View-58. |
| **Review** | Draft · Open question: Q-Detail_View-58 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *New Stock Item*, clear any pre-filled required fields and submit. | Quantity: empty | Not known: depends on open question Q-Detail_View-58 (which fields are required, the error text, and whether a default quantity is pre-filled). Proposed, to confirm in Q-Detail_View-58: the dialog stays open with a field error and no stock item is created. |
| 2 | Close the dialog and check the *Stock* tab. | None | Proposed, to confirm in Q-Detail_View-58: no row is listed. |

**Postconditions and cleanup:** None created. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-611: Cancel the New Stock Item dialog

| Field | Value |
|---|---|
| **Summary** | Closing the *New Stock Item* dialog after entering values creates no stock item. |
| **Requirement** | `R-Detail_View-11`. Source: [part-views.md#New Stock Item](../../requirements/docs/part-views.md#L72) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-form) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` [open: Q-Detail_View-58, least privileged user]; Settings: None; Data: part `QA-<suffix> Stock K` with no stock, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part's *Stock* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-58 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *New Stock Item* and enter a quantity. | Quantity: `10` | The dialog is open with the value entered. |
| 2 | Close the dialog without submitting [open: Q-Detail_View-58, cancel control]. | None | Proposed, to confirm in Q-Detail_View-58: the dialog closes and no stock item is created. |
| 3 | Check the *Stock* tab. | None | Proposed, to confirm in Q-Detail_View-58: the table has no rows. |

**Postconditions and cleanup:** None created. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-612: New stock item with a negative quantity

| Field | Value |
|---|---|
| **Summary** | A negative quantity of `-1` entered in the *New Stock Item* dialog is not accepted. |
| **Requirement** | `R-Detail_View-11`. Source: [part-views.md#New Stock Item](../../requirements/docs/part-views.md#L72) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (quantity just below zero; limit [open: Q-Detail_View-58]) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` [open: Q-Detail_View-58, least privileged user]; Settings: None; Data: part `QA-<suffix> Stock L` with no stock, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part's *Stock* tab. |
| **Automation** | Partial: depends on Q-Detail_View-58. |
| **Review** | Draft · Open question: Q-Detail_View-58 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open *New Stock Item*, enter the quantity and submit. | Quantity: `-1` | Proposed, to confirm in Q-Detail_View-58: the dialog stays open with a field error and no stock item is created. Open: Q-Detail_View-58 (minimum quantity and error text). |

**Postconditions and cleanup:** None created. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-613: New stock item with a non-numeric quantity

| Field | Value |
|---|---|
| **Summary** | A text quantity `abc` entered in the *New Stock Item* dialog is not accepted. |
| **Requirement** | `R-Detail_View-11`. Source: [part-views.md#New Stock Item](../../requirements/docs/part-views.md#L72) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` [open: Q-Detail_View-58, least privileged user]; Settings: None; Data: part `QA-<suffix> Stock M` with no stock, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part's *Stock* tab. |
| **Automation** | Partial: depends on Q-Detail_View-58. |
| **Review** | Draft · Open question: Q-Detail_View-58 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open *New Stock Item*, enter the quantity and submit. | Quantity: `abc` | Proposed, to confirm in Q-Detail_View-58: the value is not accepted (the field refuses the text or shows a field error) and no stock item is created. Open: Q-Detail_View-58 (error text). |

**Postconditions and cleanup:** None created. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-614: Stock actions are enabled when stock items are selected

| Field | Value |
|---|---|
| **Summary** | Selecting a stock item in the *Stock* table enables the stock actions drop-down. |
| **Requirement** | `R-Detail_View-12`. Source: [part-views.md#Stock Actions](../../requirements/docs/part-views.md#L76) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (nothing selected to one item selected), Decision table (selection: some) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` [open: Q-Detail_View-59, least privileged user]; Settings: None; Data: part `QA-<suffix> Stock N` with stock items of quantity 10 and 5 created via the API as `admin`; Pre-steps: log in, open the part's *Stock* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-59 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the row of the stock item with quantity 10. | Row: quantity 10 | The row is selected [open: Q-Detail_View-59, selection control]. |
| 2 | Open the stock actions drop-down [open: Q-Detail_View-59, control label]. | None | The stock actions are enabled via the drop-down menu (R-Detail_View-12). Open: Q-Detail_View-59 (which actions are listed). |
| 3 | Select both rows and open the drop-down again. | Both rows | The stock actions are enabled (R-Detail_View-12). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock items, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-615: Stock actions with no stock item selected

| Field | Value |
|---|---|
| **Summary** | With no row selected, the stock actions drop-down is not enabled; clearing the selection disables it again. |
| **Requirement** | `R-Detail_View-12`. Source: [part-views.md#Stock Actions](../../requirements/docs/part-views.md#L76) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (selection: none), State transition (selected to cleared) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` [open: Q-Detail_View-59, least privileged user]; Settings: None; Data: part `QA-<suffix> Stock O` with a stock item of quantity 10 created via the API as `admin`; Pre-steps: log in, open the part's *Stock* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-59 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the stock actions drop-down with no row selected [open: Q-Detail_View-59, control label]. | None | Proposed, to confirm in Q-Detail_View-59: the drop-down is disabled (the docs state only that it is enabled when items are selected, R-Detail_View-12). |
| 2 | Select the row, then clear the selection. | Row: quantity 10 | The drop-down is enabled while the row is selected (R-Detail_View-12). Proposed, to confirm in Q-Detail_View-59: it is disabled again after the selection is cleared. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock item, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-616: Reader cannot create or change stock from the Stock tab

| Field | Value |
|---|---|
| **Summary** | A view-only user sees the stock items but has no working *New Stock Item* or stock actions. |
| **Requirement** | `R-Detail_View-09`, `R-Detail_View-11`, `R-Detail_View-12`. Source: [part-views.md#Stock](../../requirements/docs/part-views.md#L58), [part-views.md#New Stock Item](../../requirements/docs/part-views.md#L72), [part-views.md#Stock Actions](../../requirements/docs/part-views.md#L76) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (permission), Decision table (role: view only) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: part `QA-<suffix> Stock P` with a stock item of quantity 10 created via the API as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-60 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Stock* tab. | None | Proposed, to confirm in Q-Detail_View-60: the stock item is listed (the docs do not state the permission needed to view the tab). |
| 2 | Look for *New Stock Item*. | None | Proposed, to confirm in Q-Detail_View-60: the control is hidden or disabled. |
| 3 | Select the row and look at the stock actions drop-down. | Row: quantity 10 | Proposed, to confirm in Q-Detail_View-60: no stock action that changes stock can be started. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock item, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-617: User without permissions opens a part page

| Field | Value |
|---|---|
| **Summary** | A user with no permissions cannot see the part's stock items. |
| **Requirement** | `R-Detail_View-09`. Source: [part-views.md#Stock](../../requirements/docs/part-views.md#L58) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (permission), Error guessing (open by URL) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: part `QA-<suffix> Stock Q` with a stock item of quantity 10 created via the API as `admin` (note its `pk`); Pre-steps: log in as `noaccess`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-60 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part's detail page by its URL, `/web/part/<pk>/stock`. | `<pk>` of `QA-<suffix> Stock Q` | Proposed, to confirm in Q-Detail_View-60: no stock rows are shown, and a no-permission or error message is displayed. Open: Q-Detail_View-60 (message text, redirect). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock item, set the part inactive and delete it.

**Notes:** The `/web/part/<pk>/stock` path is the web UI's tab URL pattern, not stated in the docs; confirm it in the app and use the tab URL the app shows.

---

### UI-Detail_View-618: Virtual part has no stock UI

| Field | Value |
|---|---|
| **Summary** | On a Virtual part, the stock-related UI elements, including the *Stock* tab and *New Stock Item*, are hidden. |
| **Requirement** | `R-ATT-02`, `R-ATT-03`, `R-Detail_View-09`. Source: [part-virtual.md#Stock Items](../../requirements/docs/part-virtual.md#L27) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Virtual: yes), State transition (Virtual flag on) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock R` with Virtual on, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-61 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the tabs of the part page. | None | User interface elements related to stock items are hidden (R-ATT-03). Virtual parts cannot have stock items (R-ATT-02). Open: Q-Detail_View-61 (which elements are meant). Proposed, to confirm in Q-Detail_View-61: the *Stock* tab is not listed. |
| 2 | Try the Stock tab URL directly. | `/web/part/<pk>/stock` | Not known: depends on open question Q-Detail_View-61 (page shown for a hidden tab). |

**Postconditions and cleanup:** Cleanup as `admin`: set the part inactive and delete it.

**Notes:** The Transfer Orders tab is also hidden for Virtual parts (R-Detail_View-27), covered in the tab visibility cases.

---

### UI-Detail_View-619: Part below its minimum stock is flagged low stock

| Field | Value |
|---|---|
| **Summary** | A part whose total stock (15) is just below its minimum stock level (16) is flagged "low stock". |
| **Requirement** | `R-Detail_View-14`. Source: [part-index.md#Minimum Stock](../../requirements/docs/part-index.md#L23) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Boundary value analysis (total just below the minimum) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock S` with minimum stock 16 (set as `admin` [open: Q-Detail_View-62, field label]) and stock items of quantity 10 and 5 created via the API as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Partial: the flag's markup depends on Q-Detail_View-62. |
| **Review** | Draft · Open question: Q-Detail_View-62 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the part's stock information on the detail page. | Total 15, minimum 16 | The part is flagged "low stock" and can be identified in the interface (R-Detail_View-14). Open: Q-Detail_View-62 (where and how the flag is shown). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock items, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 52 · Review · matches: [UI-Detail_View-622](part-detail-view-stock-tab.md) (52)

**Duplicate judgement:** Keep · Different rule and outcome: R-Detail_View-14 (total 15 just below a minimum of 16, "low stock" flag) vs UI-Detail_View-622's R-Detail_View-15 (total 15 just above a maximum of 14, "overstocked" flag) · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-620: Total stock equal to the minimum stock level

| Field | Value |
|---|---|
| **Summary** | A part whose total stock (15) equals its minimum stock level (15) is checked for the low stock flag. |
| **Requirement** | `R-Detail_View-14`. Source: [part-index.md#Minimum Stock](../../requirements/docs/part-index.md#L23) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (total on the minimum) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock T` with minimum stock 15 (set as `admin` [open: Q-Detail_View-62, field label]) and stock items of quantity 10 and 5 created via the API as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Partial: depends on Q-Detail_View-63. |
| **Review** | Draft · Open question: Q-Detail_View-62, Q-Detail_View-63 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the part's stock information on the detail page. | Total 15, minimum 15 | Proposed, to confirm in Q-Detail_View-63: the part is not flagged "low stock" (the docs flag a part only when the total "falls below" the minimum; behaviour at equality is not stated). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock items, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 55 · Review · matches: [UI-Detail_View-623](part-detail-view-stock-tab.md) (55)

**Duplicate judgement:** Keep · Different rule and setting: total equal to the minimum stock level (R-Detail_View-14, "low stock" flag) vs UI-Detail_View-623's total equal to the maximum (R-Detail_View-15, "overstocked" flag) · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-621: Total stock between the minimum and maximum levels

| Field | Value |
|---|---|
| **Summary** | A part whose total stock (15) lies between its minimum (10) and maximum (20) stock levels shows neither flag. |
| **Requirement** | `R-Detail_View-14`, `R-Detail_View-15`. Source: [part-index.md#Minimum Stock](../../requirements/docs/part-index.md#L23), [part-index.md#Maximum Stock](../../requirements/docs/part-index.md#L27) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (valid class: inside the range), Decision table (below min: no, above max: no) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock U` with minimum stock 10 and maximum stock 20 (set as `admin` [open: Q-Detail_View-62, field labels]) and stock items of quantity 10 and 5 created via the API as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Partial: depends on Q-Detail_View-62. |
| **Review** | Draft · Open question: Q-Detail_View-62 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the part's stock information on the detail page. | Total 15, minimum 10, maximum 20 | Proposed, to confirm in Q-Detail_View-62: neither the "low stock" nor the "overstocked" flag is shown (the docs state only the conditions that set each flag). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock items, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-622: Part above its maximum stock is flagged overstocked

| Field | Value |
|---|---|
| **Summary** | A part whose total stock (15) is just above its maximum stock level (14) is flagged "overstocked". |
| **Requirement** | `R-Detail_View-15`. Source: [part-index.md#Maximum Stock](../../requirements/docs/part-index.md#L27) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Boundary value analysis (total just above the maximum) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock V` with maximum stock 14 (set as `admin` [open: Q-Detail_View-62, field label]) and stock items of quantity 10 and 5 created via the API as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Partial: the flag's markup depends on Q-Detail_View-62. |
| **Review** | Draft · Open question: Q-Detail_View-62 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the part's stock information on the detail page. | Total 15, maximum 14 | The part is flagged "overstocked" and can be identified in the interface (R-Detail_View-15). Open: Q-Detail_View-62 (where and how the flag is shown). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock items, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 52 · Review · matches: [UI-Detail_View-619](part-detail-view-stock-tab.md) (52)

**Duplicate judgement:** Keep · Different rule and outcome: R-Detail_View-15 (total 15 just above a maximum of 14, "overstocked" flag) vs UI-Detail_View-619's R-Detail_View-14 (total 15 just below a minimum of 16, "low stock" flag) · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-623: Total stock equal to the maximum stock level

| Field | Value |
|---|---|
| **Summary** | A part whose total stock (15) equals its maximum stock level (15) is checked for the overstocked flag. |
| **Requirement** | `R-Detail_View-15`. Source: [part-index.md#Maximum Stock](../../requirements/docs/part-index.md#L27) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (total on the maximum) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Stock W` with maximum stock 15 (set as `admin` [open: Q-Detail_View-62, field label]) and stock items of quantity 10 and 5 created via the API as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Partial: depends on Q-Detail_View-63. |
| **Review** | Draft · Open question: Q-Detail_View-62, Q-Detail_View-63 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the part's stock information on the detail page. | Total 15, maximum 15 | Proposed, to confirm in Q-Detail_View-63: the part is not flagged "overstocked" (the docs flag a part only when the total "exceeds" the maximum; behaviour at equality is not stated). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock items, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 55 · Review · matches: [UI-Detail_View-620](part-detail-view-stock-tab.md) (55)

**Duplicate judgement:** Keep · Different rule and setting: total equal to the maximum stock level (R-Detail_View-15, "overstocked" flag) vs UI-Detail_View-620's total equal to the minimum (R-Detail_View-14, "low stock" flag) · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-624: Low stock flag clears when stock is added

| Field | Value |
|---|---|
| **Summary** | After a new stock item lifts the total from 15 to 20, above the minimum level of 16, the "low stock" flag is no longer shown. |
| **Requirement** | `R-Detail_View-14`, `R-Detail_View-13`. Source: [part-index.md#Minimum Stock](../../requirements/docs/part-index.md#L23), [part-index.md#Total stock](../../requirements/docs/part-index.md#L19) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (low stock to not low stock), What-if business scenario (goods received) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` [open: Q-Detail_View-58, least privileged user]; Settings: None; Data: part `QA-<suffix> Stock X` with minimum stock 16 (set as `admin` [open: Q-Detail_View-62, field label]), stock items of quantity 10 and 5 and location `QA-<suffix> Loc 1` created via the API as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Partial: depends on Q-Detail_View-62. |
| **Review** | Draft · Open question: Q-Detail_View-58, Q-Detail_View-62 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the part's stock information. | Total 15, minimum 16 | The part is flagged "low stock" (R-Detail_View-14). |
| 2 | Open the *Stock* tab and create a stock item with *New Stock Item* [open: Q-Detail_View-58, form fields]. | Quantity: `5`<br>Location: `QA-<suffix> Loc 1` | The item is created and listed (R-Detail_View-11). |
| 3 | Return to the part's stock information. | Total 20, minimum 16 | The total stock is 20 (R-Detail_View-13). Proposed, to confirm in Q-Detail_View-62: the "low stock" flag is no longer shown. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock items, set the part inactive, delete it, then delete the location.

**Notes:** None.
