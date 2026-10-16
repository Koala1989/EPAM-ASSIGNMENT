# Cross-functional scenarios: XF test cases

End-to-end flows across Areas on the same records: part creation with parameters and stock (R-XF-01), category default parameters (R-XF-02), templates and variants with stock (R-XF-03), revisions of a stocked part (R-XF-04), BOM lines with units of measure (R-XF-05), locked parts (R-XF-06) and Virtual parts (R-XF-07). Test records are created through the API as `admin` unless a step is under test; each case reuses the open questions of the Areas it composes, plus Q-XF-01 to Q-XF-06 in `open-questions.md`.

---

### UI-XF-001: A part created from the Parts view, with a parameter and a stock item, shows its stock level in the category part list and its parameter value in the parametric view.

| Field | Value |
|---|---|
| **Summary** | A part created from the Parts view, with a parameter and a stock item, shows its stock level in the category part list and its parameter value in the parametric view. |
| **Requirement** | `R-XF-01`, `R-Part-02`, `R-Part-04`, `R-Part-06`, `R-Part_Params-02`, `R-Part_Params-12`, `R-Detail_View-11`, `R-Detail_View-09`, `R-Detail_View-13`, `R-Categories-04`, `R-Categories-06`, `R-Categories-07`, `R-Part_Params-21`. Source: [part-create.md#L17](../../requirements/docs/part-create.md#L17); [part-create.md#L26](../../requirements/docs/part-create.md#L26); [part-create.md#L33](../../requirements/docs/part-create.md#L33); [concepts-parameters.md#L24](../../requirements/docs/concepts-parameters.md#L24); [concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69); [part-views.md#L72](../../requirements/docs/part-views.md#L72); [part-views.md#L58](../../requirements/docs/part-views.md#L58); [part-index.md#L19](../../requirements/docs/part-index.md#L19); [part-index.md#L37-L42](../../requirements/docs/part-index.md#L37-L42); [part-index.md#L46](../../requirements/docs/part-index.md#L46); [part-views.md#L19](../../requirements/docs/part-views.md#L19); [concepts-parameters.md#L112-L114](../../requirements/docs/concepts-parameters.md#L112-L114) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Exploratory (charter: create a part, parameterise it, stock it, find it in the category) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (view, create and edit everything; `engineer` cannot create stock, see [findings.md F-14](../findings.md)); Settings: None; Data: category `QA-<suffix> Category` (non-structural) and parameter template `QA-<suffix> Series` (no Units, no uniqueness), created as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Approved · 2026-10-15 · steps checked in the MCP run of 2026-10-15; agent draft changed first: user `engineer` to `allaccess` (findings.md F-14), control names and the return to the part after creating stock (open questions answered) |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Add Parts* dropdown above the parts table. | None | The dropdown offers the create and import options (R-Part-02). |
| 2 | Select *Create Part*. | None | The part creation form opens (R-Part-04). |
| 3 | Fill in the form. | Name: `QA-<suffix> Resistor`<br>Description: `XF flow part`<br>Category: `QA-<suffix> Category` | The *Add Part* form accepts the values and shows no form errors (R-Part-05); only Name is marked required (open-questions.md Q-REV-05). |
| 4 | Press *Submit*. | None | The browser is redirected to the new part's detail page (R-Part-06). |
| 5 | Open the *Parameters* tab, open the *Add Parameters* menu, select *Create Parameter*, choose the template and enter the data, then press *Submit*. | Template: `QA-<suffix> Series`<br>Data: `E96` | The *Add Parameter* form requires Template and Data (open-questions.md Q-Part_Params-10). The *Parameters* tab lists the parameter `QA-<suffix> Series` with Data `E96` (R-Part_Params-02, R-Part_Params-12). |
| 6 | Open the *Stock* tab, press the add stock item button, enter the quantity and press *Submit*. | Quantity: `25` | A stock item is created for the part (R-Detail_View-11). The *Add Stock Item* dialog opens with the part pre-filled; after *Submit* an alert reads *Stock item created* and the browser shows the new stock item's page (open-questions.md Q-Detail_View-58). |
| 7 | Open `QA-<suffix> Resistor` again and its *Stock* tab. | None | The *Stock* tab lists the item with quantity 25, location and status `OK` (R-Detail_View-09), and the part header shows *In Stock: 25* (R-Detail_View-13; open-questions.md Q-Detail_View-56). |
| 8 | Check the breadcrumb at the top of the part page. | None | It reads `Parts > QA-<suffix> Category` (R-Categories-07; open-questions.md Q-Categories-01). |
| 9 | Click `QA-<suffix> Category` in the breadcrumb, then open the category's *Parts* tab. | None | The table lists `QA-<suffix> Resistor` with Description `XF flow part`, Category `QA-<suffix> Category` and *Total Stock* 25 (R-Categories-04, R-Detail_View-13; open-questions.md Q-Categories-05). |
| 10 | Switch the table to the parametric view with the *Parametric View* toggle above it. | None | The parametric view replaces the table and lists `QA-<suffix> Resistor` with *Total Stock* 25 and `E96` in the `QA-<suffix> Series` column (R-XF-01, R-Part_Params-21; open-questions.md Q-Part_Params-18, Q-Part_Params-19). |
| 11 | Switch back to the table view and click the part name. | None | The Part Detail view of `QA-<suffix> Resistor` opens (R-Categories-06). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part created inactive and delete it, then delete the category (and any parameter template) created for the case. Delete the stock item first if the part cannot be deleted with it.

**Notes:** Steps confirmed in the MCP run of 2026-10-15; the user is `allaccess` because `engineer` cannot create stock (findings.md F-14). In that run, clicking the part name in step 11 opened the detail page on the last tab used; findings.md F-13 records a preview panel for a row click as `reader` and `engineer`.

---

### UI-XF-002: The category part list shows the sum of a part's stock items as its stock level.

| Field | Value |
|---|---|
| **Summary** | The category part list shows the sum of a part's stock items as its stock level. |
| **Requirement** | `R-XF-01`, `R-Detail_View-11`, `R-Detail_View-09`, `R-Detail_View-13`, `R-Categories-04`. Source: [part-views.md#L72](../../requirements/docs/part-views.md#L72); [part-views.md#L58](../../requirements/docs/part-views.md#L58); [part-index.md#L19](../../requirements/docs/part-index.md#L19); [part-index.md#L37-L42](../../requirements/docs/part-index.md#L37-L42) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: part with several stock items) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (view, create and edit everything; `engineer` cannot create stock, see [findings.md F-14](../findings.md)); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Summed` in it, created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open the detail page of `QA-<suffix> Summed`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Stock* tab, press the add stock item button, enter the quantity and press *Submit*. | Quantity: `10` | A stock item is created (R-Detail_View-11). The *Add Stock Item* dialog opens with the part pre-filled; after *Submit* an alert reads *Stock item created* and the browser shows the new stock item's page (open-questions.md Q-Detail_View-58). |
| 2 | Open `QA-<suffix> Summed` again, then its *Stock* tab, press the add stock item button again, enter the quantity and press *Submit*; then open the part's *Stock* tab. | Quantity: `15` | A second stock item is created and the *Stock* tab lists both items with quantity, location and status (R-Detail_View-09). |
| 3 | Check the part's total stock. | None | The part header shows *In Stock: 25*, the sum of both stock items (R-Detail_View-13; open-questions.md Q-Detail_View-56). |
| 4 | Open `QA-<suffix> Category`, then its *Parts* tab, and find the part. | None | The part's *Total Stock* reads 25 (R-Categories-04, R-Detail_View-13; open-questions.md Q-Categories-05). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part created inactive and delete it, then delete the category (and any parameter template) created for the case.

**Notes:** None

---

### UI-XF-003: A stock item added to a part that is already listed in its category changes the stock level shown in the category part list.

| Field | Value |
|---|---|
| **Summary** | A stock item added to a part that is already listed in its category changes the stock level shown in the category part list. |
| **Requirement** | `R-XF-01`, `R-Detail_View-11`, `R-Detail_View-13`, `R-Categories-04`. Source: [part-views.md#L72](../../requirements/docs/part-views.md#L72); [part-index.md#L19](../../requirements/docs/part-index.md#L19); [part-index.md#L37-L42](../../requirements/docs/part-index.md#L37-L42) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | State transition (no stock to stock), What-if business scenario (stock received after the part is listed) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (view, create and edit everything; `engineer` cannot create stock, see [findings.md F-14](../findings.md)); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Late Stock` with no stock items, created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-XF-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> Category` from the *Parts* view, then its *Parts* tab. | None | The category part list shows `QA-<suffix> Late Stock` (R-Categories-02). Open: Q-XF-02 (what the stock level shows for a part with no stock items). |
| 2 | Open the part, then the *Stock* tab, press the add stock item button, enter the quantity and press *Submit*. | Quantity: `5` | A stock item is created (R-Detail_View-11). The *Add Stock Item* dialog opens with the part pre-filled; after *Submit* an alert reads *Stock item created* and the browser shows the new stock item's page (open-questions.md Q-Detail_View-58). |
| 3 | Open `QA-<suffix> Category` again, then its *Parts* tab. | None | The part's *Total Stock* reads 5 (R-Categories-04, R-Detail_View-13; open-questions.md Q-Categories-05). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part created inactive and delete it, then delete the category (and any parameter template) created for the case.

**Notes:** None

---

### UI-XF-004: The Create Part form cannot be submitted with an empty Name, and no part appears in the category.

| Field | Value |
|---|---|
| **Summary** | The Create Part form cannot be submitted with an empty Name, and no part appears in the category. |
| **Requirement** | `R-XF-01`, `R-Part-04`, `R-Part-05`, `R-Part-06`, `R-Categories-02`. Source: [part-create.md#L26](../../requirements/docs/part-create.md#L26); [part-create.md#L31](../../requirements/docs/part-create.md#L31); [part-create.md#L33](../../requirements/docs/part-create.md#L33); [part-index.md#L31](../../requirements/docs/part-index.md#L31) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty Name), Error guessing |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, created as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open *Add Parts*, then *Create Part*. | None | The part creation form opens (R-Part-04). |
| 2 | Select the category and leave Name empty. | Name: empty<br>Category: `QA-<suffix> Category` | Name is not filled. |
| 3 | Press *Submit*. | None | The form cannot be submitted while it shows form errors (R-Part-05); no redirect to a part detail page happens (R-Part-06 applies only after a successful submit). Name is the only required field (open-questions.md Q-REV-05). Open: Q-Part-13 (whether *Submit* is disabled or an error appears, its text and place). |
| 4 | Close the form without saving and open `QA-<suffix> Category`, then its *Parts* tab. | None | The category part list shows no new part (R-Part-05, R-Categories-02). |

**Postconditions and cleanup:** No records are created. Cleanup as `admin`: delete the category.

**Notes:** None

---

### UI-XF-005: A view-only user does not see the Add Parts menu and cannot add a parameter or stock to a listed part.

| Field | Value |
|---|---|
| **Summary** | A view-only user does not see the Add Parts menu and cannot add a parameter or stock to a listed part. |
| **Requirement** | `R-XF-01`, `R-Part-03`, `R-Part_Params-12`, `R-Detail_View-11`, `R-Categories-02`. Source: [part-create.md#L21-L22](../../requirements/docs/part-create.md#L21-L22); [concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69); [part-views.md#L72](../../requirements/docs/part-views.md#L72); [part-index.md#L31](../../requirements/docs/part-index.md#L31) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Negative (action tried by a user who should be blocked), Decision table (permission x action) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Seen` with a parameter from template `QA-<suffix> Series` (Data `E96`) and one stock item (quantity 5), created as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Categories-06, Q-Part_Params-09, Q-Detail_View-60 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for the *Add Parts* dropdown above the parts table. | None | The *Add Parts* menu is not available, as `reader` has no "create" permission for the *Part* group (R-Part-03). |
| 2 | Open `QA-<suffix> Category`. | None | Proposed, to confirm in Q-Categories-06: the category part list shows `QA-<suffix> Seen`, with no create or edit controls. |
| 3 | Open the part and its *Parameters* tab. | None | Proposed, to confirm in Q-Part_Params-09: the parameter is listed and there is no *Add Parameters* menu. |
| 4 | Open the *Stock* tab. | None | Proposed, to confirm in Q-Detail_View-60: the stock item is listed and the add stock item button is not shown (it is not shown to `engineer` either, findings.md F-14). |

**Postconditions and cleanup:** No records are created. Cleanup as `admin`: delete the stock item, set the part inactive and delete it, then the category.

**Notes:** None

---

### UI-XF-006: A user without permissions cannot add parts and sees no parts in the category.

| Field | Value |
|---|---|
| **Summary** | A user without permissions cannot add parts and sees no parts in the category. |
| **Requirement** | `R-XF-01`, `R-Part-03`, `R-Categories-02`. Source: [part-create.md#L21-L22](../../requirements/docs/part-create.md#L21-L22); [part-index.md#L31](../../requirements/docs/part-index.md#L31) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Negative (user with no permissions) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Permissions |
| **Prerequisites** | User: `noaccess` (no permissions); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Hidden` in it, created as `admin`; Pre-steps: log in through the login form. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Categories-06, Q-Detail_View-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Parts* view and look for the *Add Parts* dropdown. | None | The *Add Parts* menu is not available (R-Part-03). |
| 2 | Try to open `QA-<suffix> Category` and its part list. | None | Not known: depends on open question Q-Categories-06 (whether the view is hidden, empty or refused, and the text shown). |
| 3 | Open the part's detail page by its URL. | URL: `/web/part/<pk>/` of `QA-<suffix> Hidden` | Proposed, to confirm in Q-Detail_View-19: no part data is shown and a no-permission or error message appears. |

**Postconditions and cleanup:** No records are created. Cleanup as `admin`: set each part created inactive and delete it, then delete the category (and any parameter template) created for the case.

**Notes:** None

---

### UI-XF-007: A parameter with units incompatible with its template is rejected and does not appear in the parametric view.

| Field | Value |
|---|---|
| **Summary** | A parameter with units incompatible with its template is rejected and does not appear in the parametric view. |
| **Requirement** | `R-XF-01`, `R-Part_Params-12`, `R-Part_Params-31`, `R-Part_Params-21`, `R-Categories-02`. Source: [concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69); [concepts-parameters.md#L183](../../requirements/docs/concepts-parameters.md#L183); [concepts-parameters.md#L112-L114](../../requirements/docs/concepts-parameters.md#L112-L114); [part-index.md#L31](../../requirements/docs/part-index.md#L31) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: incompatible units), Error guessing |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management; may add parameters, open-questions.md Q-Part_Params-09); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Length Part` in it and parameter template `QA-<suffix> Length` with Units `m`, created as `admin`; Pre-steps: log in through the login form, open the part's *Parameters* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Params-07, Q-XF-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Add Parameters* menu, select *Create Parameter*, choose the template and enter a value with an incompatible unit. | Template: `QA-<suffix> Length`<br>Data: `5 kg` | The value is rejected (R-Part_Params-31). Open: Q-Part_Params-07 (error text and where it is shown). |
| 2 | Close the form and check the *Parameters* tab. | None | No parameter for `QA-<suffix> Length` is listed (R-Part_Params-31). |
| 3 | Open `QA-<suffix> Category`, its *Parts* tab, and switch to the parametric view with the *Parametric View* toggle. | None | The part is listed in the category part list (R-Categories-02). Proposed, to confirm in Q-XF-03: it shows no value for `QA-<suffix> Length` in the parametric view. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part created inactive and delete it, then delete the category (and any parameter template) created for the case.

**Notes:** None

---

### UI-XF-008: A numeric parameter filter in the category parametric view shows only the parts that match it.

| Field | Value |
|---|---|
| **Summary** | A numeric parameter filter in the category parametric view shows only the parts that match it. |
| **Requirement** | `R-XF-01`, `R-Part_Params-21`, `R-Part_Params-23`, `R-Part_Params-24`, `R-Part_Params-27`. Source: [concepts-parameters.md#L112-L114](../../requirements/docs/concepts-parameters.md#L112-L114); [concepts-parameters.md#L126-L130](../../requirements/docs/concepts-parameters.md#L126-L130); [concepts-parameters.md#L134](../../requirements/docs/concepts-parameters.md#L134); [concepts-parameters.md#L148-L150](../../requirements/docs/concepts-parameters.md#L148-L150) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (matching, non-matching and no-value parts) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`; parameter template `QA-<suffix> Resistance` with Units `ohm`; parts `QA-<suffix> R1k` (Data `1k`), `QA-<suffix> R10k` (Data `10k`) and `QA-<suffix> RNone` (no parameter), all in the category, created as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Category` and its *Parts* tab. |
| **Automation** | Partial: the filter dialog labels are unconfirmed. |
| **Review** | Draft · Open question: Q-Part_Params-19, Q-Part_Params-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Switch to the parametric view with the *Parametric View* toggle above the table. | None | The parametric view replaces the table (R-Part_Params-21; open-questions.md Q-Part_Params-18). It lists the three parts of the category (R-Categories-02). |
| 2 | Add a filter on the parameter `QA-<suffix> Resistance`. | Operator: greater than (`>`)<br>Value: `5k` | The filter is applied; the filter options depend on the parameter type (R-Part_Params-23). Open: Q-Part_Params-19 (dialog fields and labels), Q-Part_Params-22 (operators offered). |
| 3 | Check the parts shown. | None | Only `QA-<suffix> R10k` is shown, as only parts matching the filter are shown (R-Part_Params-24); a compatible unit prefix such as `k` is accepted in the value (R-Part_Params-27). `QA-<suffix> R1k` and `QA-<suffix> RNone` are not shown (R-Part_Params-24). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part created inactive and delete it, then delete the category (and any parameter template) created for the case.

**Notes:** None

---

### UI-XF-009: A category default parameter is applied to a new part created in a sub-category, and the part is listed in the parent category and its parametric view.

| Field | Value |
|---|---|
| **Summary** | A category default parameter is applied to a new part created in a sub-category, and the part is listed in the parent category and its parametric view. |
| **Requirement** | `R-XF-02`, `R-Part_Params-19`, `R-Part-01`, `R-Part-06`, `R-Part_Params-02`, `R-Categories-02`, `R-Part_Params-21`. Source: [concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104); [part-create.md#L15](../../requirements/docs/part-create.md#L15); [part-create.md#L33](../../requirements/docs/part-create.md#L33); [concepts-parameters.md#L24](../../requirements/docs/concepts-parameters.md#L24); [part-index.md#L31](../../requirements/docs/part-index.md#L31); [concepts-parameters.md#L112-L114](../../requirements/docs/concepts-parameters.md#L112-L114) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: sub-category of the linked category) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: parent category `QA-<suffix> Parent` and its sub-category `QA-<suffix> Child`; parameter template `QA-<suffix> Finish` (no Units, no uniqueness) linked to `QA-<suffix> Parent` with default value `Matte` [open: Q-Part_Params-08, how a template is linked to a category], all set up as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Partial: the category link step is unconfirmed. |
| **Review** | Draft · Open question: Q-Part_Params-08, Q-Part_Params-18 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open *Add Parts*, select *Create Part* and fill in the form. | Name: `QA-<suffix> Knob`<br>Description: `XF default parameter`<br>Category: `QA-<suffix> Child` | The form accepts the values (R-Part-01); only Name is required (open-questions.md Q-REV-05). |
| 2 | Press *Submit*. | None | The browser is redirected to the new part's detail page (R-Part-06). |
| 3 | Open the *Parameters* tab. | None | The tab lists the parameter `QA-<suffix> Finish` with the default value `Matte`, applied to the new part in a sub-category (R-Part_Params-19, R-Part_Params-02). Open: Q-Part_Params-08 (whether the default shows at creation). |
| 4 | Open `QA-<suffix> Parent` from the *Parts* view, then its *Parts* tab. | None | The table lists `QA-<suffix> Knob` with Category `QA-<suffix> Child`, because it lists parts of all sub-categories (R-Categories-02; open-questions.md Q-Categories-05). |
| 5 | Switch to the parametric view with the *Parametric View* toggle. | None | The view lists `QA-<suffix> Knob` with `Matte` in the `QA-<suffix> Finish` column (R-XF-02; open-questions.md Q-Part_Params-19). Open: Q-Part_Params-18 (whether a parent's parametric view includes parts of sub-categories). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part created inactive and delete it, then delete the sub-category, then the parent category (and any parameter template) created for the case.

**Notes:** None

---

### UI-XF-010: A category default is not applied when the template has a uniqueness requirement, and the part is still listed in the parent category.

| Field | Value |
|---|---|
| **Summary** | A category default is not applied when the template has a uniqueness requirement, and the part is still listed in the parent category. |
| **Requirement** | `R-XF-02`, `R-Part_Params-20`, `R-Part_Params-19`, `R-Part-06`, `R-Categories-02`, `R-Part_Params-21`. Source: [concepts-parameters.md#L108](../../requirements/docs/concepts-parameters.md#L108); [concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104); [part-create.md#L33](../../requirements/docs/part-create.md#L33); [part-index.md#L31](../../requirements/docs/part-index.md#L31); [concepts-parameters.md#L112-L114](../../requirements/docs/concepts-parameters.md#L112-L114) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Decision table (template with uniqueness vs without), Negative |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: parent category `QA-<suffix> Parent` and its sub-category `QA-<suffix> Child`; parameter template `QA-<suffix> Tag` with its Unique option set to *Unique for model type* [open: Q-Part_Params-01, form labels], linked to `QA-<suffix> Parent` with default value `T-100` [open: Q-Part_Params-08, how a template is linked], set up as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Partial: the template and link steps are unconfirmed. |
| **Review** | Draft · Open question: Q-Part_Params-01, Q-Part_Params-08, Q-Part_Params-18, Q-XF-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a part in the sub-category through *Add Parts*, *Create Part*. | Name: `QA-<suffix> Plate`<br>Category: `QA-<suffix> Child` | The part is created and the browser goes to its detail page (R-Part-06). |
| 2 | Open the *Parameters* tab. | None | No parameter for `QA-<suffix> Tag` is listed: the category default is not applied for a template with a uniqueness requirement (R-Part_Params-20). |
| 3 | Open `QA-<suffix> Parent`, then its *Parts* tab. | None | The part list shows `QA-<suffix> Plate` (R-Categories-02). |
| 4 | Switch to the parametric view with the *Parametric View* toggle. | None | Proposed, to confirm in Q-XF-03: the part is listed with no value for `QA-<suffix> Tag`. Open: Q-Part_Params-18 (whether a parent's parametric view includes parts of sub-categories). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part created inactive and delete it, then delete the sub-category, then the parent category (and any parameter template) created for the case.

**Notes:** None

---

### UI-XF-011: A category default is not applied to a part created in a category outside the linked category.

| Field | Value |
|---|---|
| **Summary** | A category default is not applied to a part created in a category outside the linked category. |
| **Requirement** | `R-XF-02`, `R-Part_Params-19`, `R-Part-06`. Source: [concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104); [part-create.md#L33](../../requirements/docs/part-create.md#L33) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: category outside the linked subtree), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: parent category `QA-<suffix> Parent` and its sub-category `QA-<suffix> Child` and an unrelated category `QA-<suffix> Other`; parameter template `QA-<suffix> Finish` (no uniqueness) linked to `QA-<suffix> Parent` with default `Matte` [open: Q-Part_Params-08], set up as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Partial: the category link step is unconfirmed. |
| **Review** | Draft · Open question: Q-XF-04, Q-Part_Params-08, Q-Categories-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a part in `QA-<suffix> Other`. | Name: `QA-<suffix> Elsewhere`<br>Category: `QA-<suffix> Other` | The part is created and the browser goes to its detail page (R-Part-06). |
| 2 | Open the *Parameters* tab. | None | Proposed, to confirm in Q-XF-04: no parameter for `QA-<suffix> Finish` is listed, because the default applies only inside the linked category and its sub-categories (R-Part_Params-19 states only the positive case). |
| 3 | Open `QA-<suffix> Parent`, then its *Parts* tab. | None | `QA-<suffix> Elsewhere` is not listed, because the list shows parts of the category and its sub-categories only (R-Categories-02 states the positive case; the opposite is Proposed, to confirm in Q-Categories-05). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part created inactive and delete it, then delete the categories (and any parameter template) created for the case.

**Notes:** None

---

### UI-XF-012: Linking a template to a category with a default does not add the parameter to a part that already exists in it.

| Field | Value |
|---|---|
| **Summary** | Linking a template to a category with a default does not add the parameter to a part that already exists in it. |
| **Requirement** | `R-XF-02`, `R-Part_Params-19`, `R-Part_Params-02`. Source: [concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104); [concepts-parameters.md#L24](../../requirements/docs/concepts-parameters.md#L24) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | What-if business scenario (template linked after parts exist), State transition (no link to link) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); `admin` for the link step; Settings: None; Data: parent category `QA-<suffix> Parent` and its sub-category `QA-<suffix> Child`, part `QA-<suffix> Existing` in the sub-category and template `QA-<suffix> Finish` (no uniqueness), created via the UI and `POST /api/part/` as `admin`, not yet linked; Pre-steps: log in through the login form as `engineer`. |
| **Automation** | Partial: the category link step is unconfirmed. |
| **Review** | Draft · Open question: Q-Part_Params-12, Q-Part_Params-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | As `admin`, link `QA-<suffix> Finish` to `QA-<suffix> Parent` with default `Matte`. | Default: `Matte`<br>Link control: [open: Q-Part_Params-08, where and how] | The link is saved. Open: Q-Part_Params-08. |
| 2 | As `engineer`, open `QA-<suffix> Existing` and its *Parameters* tab. | None | Proposed, to confirm in Q-Part_Params-12: no parameter for `QA-<suffix> Finish` is listed, because the default applies to new parts (R-Part_Params-19). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part created inactive and delete it, then delete the sub-category, then the parent category (and any parameter template) created for the case. Remove the category link first.

**Notes:** None

---

### UI-XF-013: A category default is applied to a part created two levels below the linked category, and the part is listed in the top category.

| Field | Value |
|---|---|
| **Summary** | A category default is applied to a part created two levels below the linked category, and the part is listed in the top category. |
| **Requirement** | `R-XF-02`, `R-Part_Params-19`, `R-Categories-02`, `R-Part-06`, `R-Part_Params-21`. Source: [concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104); [part-index.md#L31](../../requirements/docs/part-index.md#L31); [part-create.md#L33](../../requirements/docs/part-create.md#L33); [concepts-parameters.md#L112-L114](../../requirements/docs/concepts-parameters.md#L112-L114) |
| **Area** | XF |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (nesting depth: category itself, child, grandchild) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: categories `QA-<suffix> Parent`, its sub-category `QA-<suffix> Child` and that category's sub-category `QA-<suffix> Grandchild`; template `QA-<suffix> Finish` (no uniqueness) linked to `QA-<suffix> Parent` with default `Matte` [open: Q-Part_Params-08], set up as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Partial: the category link step is unconfirmed. |
| **Review** | Draft · Open question: Q-XF-04, Q-Part_Params-08, Q-Part_Params-18 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a part in the grandchild category. | Name: `QA-<suffix> Deep`<br>Category: `QA-<suffix> Grandchild` | The part is created and the browser goes to its detail page (R-Part-06). |
| 2 | Open the *Parameters* tab. | None | Proposed, to confirm in Q-XF-04: the parameter `QA-<suffix> Finish` with value `Matte` is listed (R-Part_Params-19 says "a sub-category" without stating a depth). |
| 3 | Open `QA-<suffix> Parent`, then its *Parts* tab. | None | `QA-<suffix> Deep` is listed: any part belonging to a sub-category is displayed (R-Categories-02). |
| 4 | Switch to the parametric view with the *Parametric View* toggle. | None | Proposed, to confirm in Q-XF-04: the part is listed with `Matte`. Open: Q-Part_Params-18. |

**Postconditions and cleanup:** Cleanup as `admin`: set the part inactive and delete it, then delete the grandchild, child and parent categories, and the template.

**Notes:** None

---

### UI-XF-014: A part switched to Template gets a variant from its Variants tab, and the variant is listed.

| Field | Value |
|---|---|
| **Summary** | A part switched to Template gets a variant from its Variants tab, and the variant is listed. |
| **Requirement** | `R-XF-03`, `R-Part_Template-01`, `R-Part_Template-02`, `R-Part_Template-03`, `R-Part_Template-04`, `R-Part_Template-05`, `R-Detail_View-08`. Source: [part-template.md#L32](../../requirements/docs/part-template.md#L32); [part-template.md#L34-L37](../../requirements/docs/part-template.md#L34-L37); [part-template.md#L41](../../requirements/docs/part-template.md#L41); [part-template.md#L43-L44](../../requirements/docs/part-template.md#L43-L44); [part-template.md#L20](../../requirements/docs/part-template.md#L20); [part-views.md#L52](../../requirements/docs/part-views.md#L52) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | State transition (not template to template), Equivalence partitioning (valid class: variant created) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Base` (Template off), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open the detail page of `QA-<suffix> Base`. |
| **Automation** | Partial: the Template toggle location is unconfirmed. |
| **Review** | Draft · Open question: Q-Part_Template-01, Q-Part_Template-02, Q-Part_Template-07, Q-Part_Template-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of `QA-<suffix> Base`. | None | There is no *Variants* tab (R-Detail_View-08). |
| 2 | Switch the Template option on. | Control: [open: Q-Part_Template-01, location and label] | The part is a Template (R-Part_Template-01, R-Part_Template-02) and the *Variants* tab is visible (R-Detail_View-08). |
| 3 | Open the *Variants* tab and press *New Variant*. | None | The `Duplicate Part` form is displayed (R-Part_Template-04). Open: Q-Part_Template-02 (button label, prefilled fields). |
| 4 | Fill in the form and press *Submit*. | Name: `QA-<suffix> Base Red`<br>Other fields: [open: Q-Part_Template-02, required fields] | The variant is created (R-Part_Template-04). Open: Q-Part_Template-02 (navigation after submit). |
| 5 | Check the *Variants* tab of `QA-<suffix> Base`. | None | `QA-<suffix> Base Red` is listed (R-Part_Template-04). Open: Q-Part_Template-07 (columns, row link). |
| 6 | Open the variant's detail page. | None | It references its template part `QA-<suffix> Base` (R-Part_Template-05). Open: Q-Part_Template-09 (field or label and link). |

**Postconditions and cleanup:** Cleanup as `admin`: set the variant and then the template inactive, delete the variant first, then the template, then the category.

**Notes:** None

---

### UI-XF-015: Stock created on a variant counts in the stock of its template part.

| Field | Value |
|---|---|
| **Summary** | Stock created on a variant counts in the stock of its template part. |
| **Requirement** | `R-XF-03`, `R-Detail_View-11`, `R-Detail_View-09`, `R-Detail_View-13`, `R-Part_Template-07`. Source: [part-views.md#L72](../../requirements/docs/part-views.md#L72); [part-views.md#L58](../../requirements/docs/part-views.md#L58); [part-index.md#L19](../../requirements/docs/part-index.md#L19); [part-template.md#L26](../../requirements/docs/part-template.md#L26) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: one variant with stock) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (view, create and edit everything; `engineer` cannot create stock, see [findings.md F-14](../findings.md)); Settings: None; Data: category `QA-<suffix> Category`, template `QA-<suffix> Base` (Template on) and its variant `QA-<suffix> Base Red`, created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open the detail page of `QA-<suffix> Base Red`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Stock* tab, press the add stock item button, enter the quantity and press *Submit*; then open the variant's *Stock* tab again. | Quantity: `30` | A stock item is created for the variant (R-Detail_View-11; open-questions.md Q-Detail_View-58). The tab lists it with quantity, location and status (R-Detail_View-09) and the variant's header shows *In Stock: 30* (R-Detail_View-13; open-questions.md Q-Detail_View-56). |
| 2 | Open the detail page of the template `QA-<suffix> Base` and check its stock. | None | The template's stock includes the variant's 30 units (R-Part_Template-07). Open: Q-Part_Template-06 (where the combined stock is shown). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock item, set the variant and then the template inactive, delete the variant first, then the template, then the category.

**Notes:** None

---

### UI-XF-016: The stock of a template is the sum of the stock of its variants.

| Field | Value |
|---|---|
| **Summary** | The stock of a template is the sum of the stock of its variants. |
| **Requirement** | `R-XF-03`, `R-Detail_View-13`, `R-Part_Template-07`. Source: [part-index.md#L19](../../requirements/docs/part-index.md#L19); [part-template.md#L26](../../requirements/docs/part-template.md#L26) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: several variants with stock) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (view, create and edit everything; `engineer` cannot create stock, see [findings.md F-14](../findings.md)); Settings: None; Data: category `QA-<suffix> Category`, template `QA-<suffix> Base` (Template on) and variants `QA-<suffix> Base Red` and `QA-<suffix> Base Blue`, created as `admin`; Pre-steps: log in through the login form. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | On `QA-<suffix> Base Red`, open the *Stock* tab, press the add stock item button, enter the quantity and press *Submit*. | Quantity: `30` | A stock item is created (R-Detail_View-11). The *Add Stock Item* dialog opens with the part pre-filled; after *Submit* an alert reads *Stock item created* and the browser shows the new stock item's page (open-questions.md Q-Detail_View-58). |
| 2 | On `QA-<suffix> Base Blue`, open the *Stock* tab, press the add stock item button, enter the quantity and press *Submit*. | Quantity: `12` | A stock item is created (R-Detail_View-11). |
| 3 | Open `QA-<suffix> Base` and check its stock. | None | The template's stock is 42, the sum of both variants (R-Part_Template-07, R-Detail_View-13). Open: Q-Part_Template-06 (where it is shown). |
| 4 | Open `QA-<suffix> Base Red` and check its stock. | None | Proposed, to confirm in Q-Part_Template-06: the variant shows only its own 30 units. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock items, set the variants and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-XF-017: A part that is not a Template has no Variants tab, so no variant can be created from it.

| Field | Value |
|---|---|
| **Summary** | A part that is not a Template has no Variants tab, so no variant can be created from it. |
| **Requirement** | `R-XF-03`, `R-Part_Template-03`, `R-Detail_View-08`. Source: [part-template.md#L41](../../requirements/docs/part-template.md#L41); [part-views.md#L52](../../requirements/docs/part-views.md#L52) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Negative (variants only when Template is on), Decision table (Template on/off) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Plain` (Template off), created as `admin`; Pre-steps: log in through the login form, open the detail page of `QA-<suffix> Plain`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-03, Q-Part_Template-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Variants* tab is not visible (R-Detail_View-08), so *New Variant* cannot be used (R-Part_Template-03). |
| 2 | Open the part's page with the variants panel selected by URL. | URL: the part's URL with the variants panel path [open: Q-Part_Template-07, panel path] | Not known: depends on open question Q-Part_Template-07 (page shown when the panel is opened for a non-template part). No variant is created (R-Part_Template-03). |

**Postconditions and cleanup:** No records are created. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None

---

### UI-XF-018: A view-only user cannot create a variant from the Variants tab of a template.

| Field | Value |
|---|---|
| **Summary** | A view-only user cannot create a variant from the Variants tab of a template. |
| **Requirement** | `R-XF-03`, `R-Part_Template-04`, `R-Detail_View-08`. Source: [part-template.md#L43-L44](../../requirements/docs/part-template.md#L43-L44); [part-views.md#L52](../../requirements/docs/part-views.md#L52) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Negative (action tried by a user who should be blocked) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: category `QA-<suffix> Category`, template `QA-<suffix> Base` (Template on) and variant `QA-<suffix> Base Red`, created as `admin`; Pre-steps: log in through the login form, open the detail page of `QA-<suffix> Base`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Variants* tab if it is shown. | None | Not known: depends on open question Q-Part_Template-02 (whether `reader` sees the tab). R-Detail_View-08 states only that the tab is visible only for a Template part. |
| 2 | Look for the *New Variant* button. | None | Proposed, to confirm in Q-Part_Template-02: the button is not available to `reader`, so no variant can be created. |

**Postconditions and cleanup:** No records are created. Cleanup as `admin`: set the variant and then the template inactive, delete the variant first, then the template, then the category.

**Notes:** None

---

### UI-XF-019: A revision created with Duplicate Part from a part with stock is a separate part linked to the original, and the original's stock is unchanged.

| Field | Value |
|---|---|
| **Summary** | A revision created with Duplicate Part from a part with stock is a separate part linked to the original, and the original's stock is unchanged. |
| **Requirement** | `R-XF-04`, `R-REV-01`, `R-REV-02`, `R-REV-11`, `R-REV-12`, `R-REV-13`, `R-Detail_View-09`, `R-Detail_View-13`. Source: [part-revision.md#L23](../../requirements/docs/part-revision.md#L23); [part-revision.md#L19](../../requirements/docs/part-revision.md#L19); [part-revision.md#L43-L48](../../requirements/docs/part-revision.md#L43-L48); [part-revision.md#L53-L64](../../requirements/docs/part-revision.md#L53-L64); [part-revision.md#L66](../../requirements/docs/part-revision.md#L66); [part-views.md#L58](../../requirements/docs/part-views.md#L58); [part-index.md#L19](../../requirements/docs/part-index.md#L19) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Exploratory (charter: revise a stocked part), Equivalence partitioning (valid class: unique revision code) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (part management); Settings: `PART_ENABLE_REVISION` = on [open: Q-REV-01, label and default]; `PART_REVISION_ASSEMBLY_ONLY` [open: Q-REV-01, label and default]; Data: category `QA-<suffix> Category` and assembly part `QA-<suffix> Widget` (Assembly on) with one stock item of quantity 20, created via `POST /api/part/category/`, `POST /api/part/` and the *Stock* tab as `admin`; Pre-steps: log in through the login form, open the detail page of `QA-<suffix> Widget`. |
| **Automation** | Partial: the settings are unconfirmed. |
| **Review** | Draft · Open question: Q-REV-01, Q-REV-02, Q-REV-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu and select *Duplicate Part*. | None | The `Duplicate Part` form opens (R-REV-12). |
| 2 | Set the revision fields. | Revision Of: `QA-<suffix> Widget`<br>Revision: `B`<br>Name: [open: Q-REV-02, whether the Name must change] | The form accepts the values (R-REV-12). Open: Q-REV-02 (Name uniqueness). |
| 3 | Press *Submit*. | None | The user is redirected to the new revision, which shows its link to the original part (R-REV-13, R-REV-01). Open: Q-REV-07 (where and with what label the link is shown). |
| 4 | Open the original `QA-<suffix> Widget`, then its *Stock* tab. | None | The stock item of quantity 20 is still listed and unchanged, and the part header shows *In Stock: 20* (R-REV-02, R-Detail_View-09, R-Detail_View-13; open-questions.md Q-Detail_View-56). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock item, set the revision and the original inactive, delete the revision first, then the original, then the category.

**Notes:** None

---

### UI-XF-020: The revision selector is hidden for a part with a single revision and shows and navigates once several revisions exist.

| Field | Value |
|---|---|
| **Summary** | The revision selector is hidden for a part with a single revision and shows and navigates once several revisions exist. |
| **Requirement** | `R-XF-04`, `R-REV-14`, `R-REV-15`, `R-REV-12`. Source: [part-revision.md#L72](../../requirements/docs/part-revision.md#L72); [part-revision.md#L77](../../requirements/docs/part-revision.md#L77); [part-revision.md#L53-L64](../../requirements/docs/part-revision.md#L53-L64) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | State transition (one part to several revisions) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (part management); Settings: `PART_ENABLE_REVISION` = on [open: Q-REV-01, label and default]; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Widget` (Assembly on) and two revisions `B` and `C` of it (Revision Of the assembly), and a separate assembly `QA-<suffix> Solo` (Assembly on, Revision empty), created via `POST /api/part/` as `admin`; Pre-steps: log in through the login form. |
| **Automation** | Partial: the selector label and the settings are unconfirmed. |
| **Review** | Draft · Open question: Q-REV-01, Q-REV-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> Solo`. | None | The revision selector is not visible, as it is visible only when multiple revisions exist (R-REV-15). |
| 2 | Open `QA-<suffix> Widget`. | None | The *Select Part Revision* drop-down is visible at the top of the page (R-REV-14, R-REV-15). |
| 3 | Open the drop-down and choose revision `C`. | Revision: `C` | The page of revision `C` opens (R-REV-14). |
| 4 | Open the drop-down again and choose the original. | None | The page of `QA-<suffix> Widget` opens (R-REV-14). |

**Postconditions and cleanup:** Cleanup as `admin`: set the revisions and the originals inactive, delete the revisions first, then the originals, then the category.

**Notes:** None

---

### UI-XF-021: The revision selector with exactly one revision besides the original.

| Field | Value |
|---|---|
| **Summary** | The revision selector with exactly one revision besides the original. |
| **Requirement** | `R-XF-04`, `R-REV-14`, `R-REV-15`. Source: [part-revision.md#L72](../../requirements/docs/part-revision.md#L72); [part-revision.md#L77](../../requirements/docs/part-revision.md#L77) |
| **Area** | XF |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (number of revisions: 1, 2 parts in total) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (part management); Settings: `PART_ENABLE_REVISION` = on [open: Q-REV-01, label and default]; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Widget` and one revision `B` of it, created via `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Widget`. |
| **Automation** | Partial: the boundary is unconfirmed. |
| **Review** | Draft · Open question: Q-XF-05, Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the top of the part page for the revision selector. | None | Not known: depends on open question Q-XF-05 (whether an original with one revision counts as "multiple revisions", R-REV-15). Proposed, to confirm in Q-XF-05: the *Select Part Revision* drop-down is visible and lists both parts. |
| 2 | If the selector is visible, choose revision `B`. | Revision: `B` | The page of revision `B` opens (R-REV-14). |

**Postconditions and cleanup:** Cleanup as `admin`: set the revision and the original inactive, delete the revision first, then the original, then the category.

**Notes:** None

---

### UI-XF-022: A second revision with an existing revision code is rejected.

| Field | Value |
|---|---|
| **Summary** | A second revision with an existing revision code is rejected. |
| **Requirement** | `R-XF-04`, `R-REV-07`, `R-REV-12`. Source: [part-revision.md#L37](../../requirements/docs/part-revision.md#L37); [part-revision.md#L53-L64](../../requirements/docs/part-revision.md#L53-L64) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: duplicate revision code), Error guessing |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (part management); Settings: `PART_ENABLE_REVISION` = on [open: Q-REV-01, label and default]; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Widget` and its revision `B` (Revision Of the assembly), created via `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Widget`. |
| **Automation** | Partial: the settings and error text are unconfirmed. |
| **Review** | Draft · Open question: Q-REV-01, Q-REV-02, Q-REV-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu and select *Duplicate Part*. | None | The `Duplicate Part` form opens (R-REV-12). |
| 2 | Set Revision Of and a revision code that already exists. | Revision Of: `QA-<suffix> Widget`<br>Revision: `B`<br>Name: [open: Q-REV-02, whether the Name must change] | The form accepts input. |
| 3 | Press *Submit*. | None | The second revision with code `B` is not created: two revisions of the same part cannot have the same revision code (R-REV-07). Open: Q-REV-06 (error text and place). |
| 4 | Check the revisions of `QA-<suffix> Widget`. | None | Only one revision with code `B` exists (R-REV-07). |

**Postconditions and cleanup:** No new record is created. Cleanup as `admin`: set the revision and the original inactive, delete the revision first, then the original, then the category.

**Notes:** None

---

### UI-XF-023: Stock added to a revision stays on the revision and does not change the stock of the original.

| Field | Value |
|---|---|
| **Summary** | Stock added to a revision stays on the revision and does not change the stock of the original. |
| **Requirement** | `R-XF-04`, `R-REV-01`, `R-REV-02`, `R-Detail_View-11`, `R-Detail_View-13`. Source: [part-revision.md#L23](../../requirements/docs/part-revision.md#L23); [part-revision.md#L19](../../requirements/docs/part-revision.md#L19); [part-views.md#L72](../../requirements/docs/part-views.md#L72); [part-index.md#L19](../../requirements/docs/part-index.md#L19) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: stock on the revision) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `allaccess` (view, create and edit everything; `engineer` cannot create stock, see [findings.md F-14](../findings.md)); Settings: `PART_ENABLE_REVISION` = on [open: Q-REV-01, label and default]; Data: category `QA-<suffix> Category` and assembly part `QA-<suffix> Widget` (Assembly on) with one stock item of quantity 20 and its revision `B` (Revision Of the assembly), created as `admin`; Pre-steps: log in through the login form, open revision `B`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | On revision `B`, open the *Stock* tab, press the add stock item button, enter the quantity and press *Submit*. | Quantity: `7` | A stock item is created for the revision, which has its own stock (R-REV-01, R-Detail_View-11). The *Add Stock Item* dialog opens with the part pre-filled; after *Submit* an alert reads *Stock item created* and the browser shows the new stock item's page (open-questions.md Q-Detail_View-58). |
| 2 | Open revision `B` again and check its stock. | None | The part header shows *In Stock: 7* (R-Detail_View-13; open-questions.md Q-Detail_View-56). |
| 3 | Open `QA-<suffix> Widget` and check its stock. | None | The part header still shows *In Stock: 20* and the original's stock item is unchanged (R-REV-02, R-Detail_View-13). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the stock items, set the revision and the original inactive, delete the revision first, then the original, then the category.

**Notes:** None

---

### UI-XF-024: A revision created with Duplicate Part from a part with stock does not receive the original's stock items.

| Field | Value |
|---|---|
| **Summary** | A revision created with Duplicate Part from a part with stock does not receive the original's stock items. |
| **Requirement** | `R-XF-04`, `R-REV-01`, `R-REV-02`, `R-REV-12`, `R-Detail_View-09`. Source: [part-revision.md#L23](../../requirements/docs/part-revision.md#L23); [part-revision.md#L19](../../requirements/docs/part-revision.md#L19); [part-revision.md#L53-L64](../../requirements/docs/part-revision.md#L53-L64); [part-views.md#L58](../../requirements/docs/part-views.md#L58) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | What-if business scenario (stock on the original when it is duplicated) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (part management); Settings: `PART_ENABLE_REVISION` = on [open: Q-REV-01, label and default]; Data: category `QA-<suffix> Category` and assembly part `QA-<suffix> Widget` (Assembly on) with one stock item of quantity 20, created as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Widget`. |
| **Automation** | Partial: the settings and the outcome are unconfirmed. |
| **Review** | Draft · Open question: Q-XF-01, Q-REV-01, Q-REV-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a revision with *Duplicate Part*. | Revision Of: `QA-<suffix> Widget`<br>Revision: `B`<br>Name: [open: Q-REV-02] | The revision is created (R-REV-12). |
| 2 | Open the revision's *Stock* tab. | None | Proposed, to confirm in Q-XF-01: the tab lists no stock items, as the revision has its own stock (R-REV-01). |
| 3 | Open the original's *Stock* tab. | None | The original's stock item of quantity 20 is still listed (R-REV-02, R-Detail_View-09). |

**Postconditions and cleanup:** Cleanup as `admin`: set the revision and the original inactive, delete the revision first, then the original, then the category.

**Notes:** None

---

### UI-XF-025: With revisions disabled, a revision cannot be created with Duplicate Part.

| Field | Value |
|---|---|
| **Summary** | With revisions disabled, a revision cannot be created with Duplicate Part. |
| **Requirement** | `R-XF-04`, `R-REV-11`, `R-REV-12`. Source: [part-revision.md#L43-L48](../../requirements/docs/part-revision.md#L43-L48); [part-revision.md#L53-L64](../../requirements/docs/part-revision.md#L53-L64) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Decision table (`PART_ENABLE_REVISION` off), State transition (setting on to off) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (part management); `admin` for the setting; Settings: `PART_ENABLE_REVISION` = off [open: Q-REV-01, label, where it is changed and default]; Data: category `QA-<suffix> Category` and assembly part `QA-<suffix> Widget` (Assembly on) with one stock item of quantity 20, created as `admin`; Pre-steps: as `admin` switch revisions off; log in through the login form as `engineer`, open `QA-<suffix> Widget`. |
| **Automation** | Partial: the setting is unconfirmed. |
| **Review** | Draft · Open question: Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu and select *Duplicate Part*. | None | Not known: depends on open question Q-REV-01 (whether the Duplicate action is blocked or still opens when revisions are disabled). |
| 2 | Look for the *Revision Of* field. | None | Proposed, to confirm in Q-REV-01: the *Revision* and *Revision Of* fields are not offered, since revisions are controlled by `PART_ENABLE_REVISION` (R-REV-11). |

**Postconditions and cleanup:** Cleanup as `admin`: restore the setting to its original value, delete the stock item, set the part inactive and delete it, then the category.

**Notes:** None

---

### UI-XF-026: A view-only user cannot create a revision of a part.

| Field | Value |
|---|---|
| **Summary** | A view-only user cannot create a revision of a part. |
| **Requirement** | `R-XF-04`, `R-REV-12`. Source: [part-revision.md#L53-L64](../../requirements/docs/part-revision.md#L53-L64) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Negative (action tried by a user who should be blocked) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional, Permissions, Settings-dependent |
| **Prerequisites** | User: `reader` (view only); Settings: `PART_ENABLE_REVISION` = on [open: Q-REV-01, label and default]; Data: category `QA-<suffix> Category` and assembly part `QA-<suffix> Widget` (Assembly on) with one stock item of quantity 20, created as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Widget`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Categories-03, Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for the part actions menu and the *Duplicate Part* action. | None | Proposed, to confirm in Q-Categories-03: no part actions menu is shown to `reader` (observed on 1.5.6), so no revision can be created. |
| 2 | Check the original's *Stock* tab. | None | The stock item of quantity 20 is listed and unchanged (R-REV-02, R-Detail_View-09). |

**Postconditions and cleanup:** No records are created. Cleanup as `admin`: delete the stock item, set the part inactive and delete it, then the category.

**Notes:** None

---

### UI-XF-027: With the assembly-only revision setting on, a revision of a part that is not an Assembly cannot be created.

| Field | Value |
|---|---|
| **Summary** | With the assembly-only revision setting on, a revision of a part that is not an Assembly cannot be created. |
| **Requirement** | `R-XF-04`, `R-REV-11`, `R-REV-12`. Source: [part-revision.md#L43-L48](../../requirements/docs/part-revision.md#L43-L48); [part-revision.md#L53-L64](../../requirements/docs/part-revision.md#L53-L64) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Decision table (`PART_REVISION_ASSEMBLY_ONLY` on x Assembly off) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (part management); `admin` for the settings; Settings: `PART_ENABLE_REVISION` = on and `PART_REVISION_ASSEMBLY_ONLY` = on [open: Q-REV-01, labels and defaults]; Data: category `QA-<suffix> Category` and part `QA-<suffix> Plain` (Assembly off), created as `admin`; Pre-steps: as `admin` switch both settings on; log in through the login form as `engineer`, open `QA-<suffix> Plain`. |
| **Automation** | Partial: the settings are unconfirmed. |
| **Review** | Draft · Open question: Q-REV-01, Q-REV-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu, select *Duplicate Part* and set Revision Of and Revision. | Revision Of: `QA-<suffix> Plain`<br>Revision: `B` | Not known: depends on open question Q-REV-01 (what `PART_REVISION_ASSEMBLY_ONLY` changes in the UI, and the label of the setting). |
| 2 | Press *Submit* if it is possible. | None | Proposed, to confirm in Q-REV-01: no revision of a non-assembly part is created while the setting is on (R-REV-11). |

**Postconditions and cleanup:** Cleanup as `admin`: restore both settings to their original values, delete any record created, set the part inactive and delete it, then the category.

**Notes:** None

---

### UI-XF-028: A Component part with a unit, added to an Assembly's BOM with a raw amount in a compatible unit, gets a converted quantity, lists the assembly on its Used In tab, and the BOM is not validated.

| Field | Value |
|---|---|
| **Summary** | A Component part with a unit, added to an Assembly's BOM with a raw amount in a compatible unit, gets a converted quantity, lists the assembly on its Used In tab, and the BOM is not validated. |
| **Requirement** | `R-XF-05`, `R-ATT-08`, `R-ATT-10`, `R-Unit_measure-01`, `R-Unit_measure-03`, `R-Unit_measure-06`, `R-Unit_measure-16`, `R-Unit_measure-18`, `R-Detail_View-19`, `R-Detail_View-62`, `R-Detail_View-21`, `R-Detail_View-59`, `R-Detail_View-65`, `R-Detail_View-67`. Source: [part-index.md#L62](../../requirements/docs/part-index.md#L62); [part-index.md#L68](../../requirements/docs/part-index.md#L68); [part-index.md#L120](../../requirements/docs/part-index.md#L120); [part-index.md#L127](../../requirements/docs/part-index.md#L127); [concepts-units.md#L24](../../requirements/docs/concepts-units.md#L24); [manufacturing-bom.md#L29-L30](../../requirements/docs/manufacturing-bom.md#L29-L30); [manufacturing-bom.md#L49](../../requirements/docs/manufacturing-bom.md#L49); [part-views.md#L84](../../requirements/docs/part-views.md#L84); [manufacturing-bom.md#L137-L143](../../requirements/docs/manufacturing-bom.md#L137-L143); [part-views.md#L92](../../requirements/docs/part-views.md#L92); [manufacturing-bom.md#L124](../../requirements/docs/manufacturing-bom.md#L124); [manufacturing-bom.md#L163-L181](../../requirements/docs/manufacturing-bom.md#L163-L181); [manufacturing-bom.md#L187-L191](../../requirements/docs/manufacturing-bom.md#L187-L191) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Exploratory (charter: build a BOM with unit conversion), Equivalence partitioning (valid class: compatible unit) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management) [open: Q-Detail_View-01, whether `engineer` may edit BOMs]; Settings: None; Data: category `QA-<suffix> Category`, component part `QA-<suffix> Flour` (Component on, Units `kg`) and assembly `QA-<suffix> Cake` (Assembly on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open the detail page of `QA-<suffix> Cake`. |
| **Automation** | Partial: the form labels are unconfirmed. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-02, Q-Detail_View-03, Q-Detail_View-06, Q-Unit_measure-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *BOM* tab of the assembly. | None | The tab is visible because the part is an Assembly (R-Detail_View-19). The BOM opens in view mode (R-Detail_View-59). |
| 2 | Press the *Edit* icon. | None | The BOM switches to editing mode (R-Detail_View-59). Open: Q-Detail_View-02. |
| 3 | Press the add icon. | None | The *Create BOM Item* form opens (R-Detail_View-62). |
| 4 | Fill in the form. | Part: `QA-<suffix> Flour`<br>Raw Amount: `500 g` [open: Q-Unit_measure-09, label of the field]<br>Other required fields: [open: Q-Detail_View-03] | The form accepts a raw amount in `g` for a part in `kg`, a compatible unit (R-Unit_measure-16, R-Unit_measure-06). |
| 5 | Press *Submit*. | None | The line is added to the BOM (R-Detail_View-62). |
| 6 | Check the new line's quantity. | None | The quantity is calculated automatically as 0.5 (R-Unit_measure-16, R-Unit_measure-18). Open: Q-Unit_measure-09 (rounding and how the unit is shown). |
| 7 | Check the validation status at the top of the BOM table. | None | The status reads "Not Validated" with a *Validate BOM* button, as adding a line changes the BOM (R-Detail_View-65, R-Detail_View-67). Open: Q-Detail_View-06. |
| 8 | Open the detail page of `QA-<suffix> Flour` and its *Used In* tab. | None | The tab is visible because the part is a Component and lists `QA-<suffix> Cake` (R-Detail_View-21, R-ATT-10). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the BOM line, set both parts inactive and delete them, then the category.

**Notes:** None

---

### UI-XF-029: Raw amounts of 500 g, 0.5 kg and 1/2 kg on a part in kg all give the same quantity of 0.5.

| Field | Value |
|---|---|
| **Summary** | Raw amounts of 500 g, 0.5 kg and 1/2 kg on a part in kg all give the same quantity of 0.5. |
| **Requirement** | `R-XF-05`, `R-Unit_measure-16`, `R-Unit_measure-18`, `R-Detail_View-62`. Source: [manufacturing-bom.md#L29-L30](../../requirements/docs/manufacturing-bom.md#L29-L30); [manufacturing-bom.md#L49](../../requirements/docs/manufacturing-bom.md#L49); [manufacturing-bom.md#L137-L143](../../requirements/docs/manufacturing-bom.md#L137-L143) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (gram input, decimal input, fraction input) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management) [open: Q-Detail_View-01]; Settings: None; Data: category `QA-<suffix> Category`, components `QA-<suffix> Flour G`, `QA-<suffix> Flour K` and `QA-<suffix> Flour F` (each Component on, Units `kg`) and assembly `QA-<suffix> Cake` (Assembly on), created as `admin`; Pre-steps: log in through the login form, open the *BOM* tab of `QA-<suffix> Cake` and switch to editing mode. |
| **Automation** | Partial: the field label is unconfirmed. |
| **Review** | Draft · Open question: Q-Unit_measure-09, Q-Detail_View-01, Q-Detail_View-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a BOM line for the first component. | Part: `QA-<suffix> Flour G`<br>Raw Amount: `500 g` | The line is added (R-Detail_View-62) with quantity 0.5 (R-Unit_measure-18). |
| 2 | Add a BOM line for the second component. | Part: `QA-<suffix> Flour K`<br>Raw Amount: `0.5 kg` | The line is added with quantity 0.5 (R-Unit_measure-18). |
| 3 | Add a BOM line for the third component. | Part: `QA-<suffix> Flour F`<br>Raw Amount: `1/2 kg` | The line is added with quantity 0.5 (R-Unit_measure-18). Open: Q-Unit_measure-09 (field label, rounding and display of the quantity). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the BOM lines, set all parts inactive and delete them, then the category.

**Notes:** None

---

### UI-XF-030: A raw amount with a unit is rejected for a component that has no unit of measure.

| Field | Value |
|---|---|
| **Summary** | A raw amount with a unit is rejected for a component that has no unit of measure. |
| **Requirement** | `R-XF-05`, `R-Unit_measure-17`, `R-Detail_View-62`. Source: [manufacturing-bom.md#L45](../../requirements/docs/manufacturing-bom.md#L45); [manufacturing-bom.md#L137-L143](../../requirements/docs/manufacturing-bom.md#L137-L143) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: unit on a unit-less part) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management) [open: Q-Detail_View-01]; Settings: None; Data: category `QA-<suffix> Category`, component `QA-<suffix> Screw` (Component on, Units empty) and assembly `QA-<suffix> Cake` (Assembly on), created as `admin`; Pre-steps: log in through the login form, open the *BOM* tab of `QA-<suffix> Cake` and switch to editing mode. |
| **Automation** | Partial: the error text is unconfirmed. |
| **Review** | Draft · Open question: Q-Unit_measure-09, Q-Detail_View-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press the add icon and fill in the form with a raw amount that includes a unit. | Part: `QA-<suffix> Screw`<br>Raw Amount: `5 g` | The form opens (R-Detail_View-62). |
| 2 | Press *Submit*. | None | No BOM line is created: if the part has no unit of measure, the raw amount cannot include units (R-Unit_measure-17). Open: Q-Unit_measure-09 (error text and place). |
| 3 | Enter a raw amount without a unit and press *Submit*. | Raw Amount: `5` | Proposed, to confirm in Q-Unit_measure-09: the line is added with quantity 5. |

**Postconditions and cleanup:** Cleanup as `admin`: delete any BOM line created, set both parts inactive and delete them, then the category.

**Notes:** None

---

### UI-XF-031: A raw amount in an incompatible unit is rejected for a component with a unit of measure.

| Field | Value |
|---|---|
| **Summary** | A raw amount in an incompatible unit is rejected for a component with a unit of measure. |
| **Requirement** | `R-XF-05`, `R-Unit_measure-16`, `R-Unit_measure-06`. Source: [manufacturing-bom.md#L29-L30](../../requirements/docs/manufacturing-bom.md#L29-L30); [concepts-units.md#L24](../../requirements/docs/concepts-units.md#L24) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: incompatible unit) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management) [open: Q-Detail_View-01]; Settings: None; Data: category `QA-<suffix> Category`, component part `QA-<suffix> Flour` (Component on, Units `kg`) and assembly `QA-<suffix> Cake` (Assembly on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open the *BOM* tab of `QA-<suffix> Cake` and switch to editing mode. |
| **Automation** | Partial: the outcome and text are unconfirmed. |
| **Review** | Draft · Open question: Q-Unit_measure-09, Q-Detail_View-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press the add icon and fill in the form with a length for a part in kg. | Part: `QA-<suffix> Flour`<br>Raw Amount: `5 m` | The form opens (R-Detail_View-62). |
| 2 | Press *Submit*. | None | Proposed, to confirm in Q-Unit_measure-09: the line is rejected with an error, because the raw amount must be in a unit compatible with the part's unit (R-Unit_measure-16 states the compatible case only). |

**Postconditions and cleanup:** Cleanup as `admin`: delete any BOM line created, set both parts inactive and delete them, then the category.

**Notes:** None

---

### UI-XF-032: Adding a line to a validated BOM marks it Not Validated and shows the Validate BOM button.

| Field | Value |
|---|---|
| **Summary** | Adding a line to a validated BOM marks it Not Validated and shows the Validate BOM button. |
| **Requirement** | `R-XF-05`, `R-Detail_View-65`, `R-Detail_View-66`, `R-Detail_View-67`, `R-Detail_View-62`, `R-Unit_measure-16`. Source: [manufacturing-bom.md#L163-L181](../../requirements/docs/manufacturing-bom.md#L163-L181); [manufacturing-bom.md#L183](../../requirements/docs/manufacturing-bom.md#L183); [manufacturing-bom.md#L187-L191](../../requirements/docs/manufacturing-bom.md#L187-L191); [manufacturing-bom.md#L137-L143](../../requirements/docs/manufacturing-bom.md#L137-L143); [manufacturing-bom.md#L29-L30](../../requirements/docs/manufacturing-bom.md#L29-L30) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | State transition (validated to not validated) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management) [open: Q-Detail_View-01]; Settings: None; Data: category `QA-<suffix> Category`, components `QA-<suffix> Flour` and `QA-<suffix> Sugar` (Component on, Units `kg`), assembly `QA-<suffix> Cake` (Assembly on) with one BOM line for `QA-<suffix> Flour` (quantity 1), created as `admin`; Pre-steps: log in through the login form, open the *BOM* tab of `QA-<suffix> Cake`. |
| **Automation** | Partial: the validated status wording is unconfirmed. |
| **Review** | Draft · Open question: Q-Detail_View-06, Q-Detail_View-01, Q-Detail_View-03, Q-Unit_measure-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *Validate BOM* in the status at the top of the table. | None | The user revalidates the BOM manually (R-Detail_View-66). Open: Q-Detail_View-06 (wording of the validated status, confirmation, message). |
| 2 | Switch to editing mode and add a line. | Part: `QA-<suffix> Sugar`<br>Raw Amount: `200 g` | The line is added (R-Detail_View-62) with quantity 0.2 (R-Unit_measure-16). |
| 3 | Check the validation status at the top of the BOM table. | None | The status reads "Not Validated" with a *Validate BOM* button (R-Detail_View-65, R-Detail_View-67). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the BOM lines, set all parts inactive and delete them, then the category.

**Notes:** None

---

### UI-XF-033: A view-only user does not see the Edit icon on the BOM and cannot add a line.

| Field | Value |
|---|---|
| **Summary** | A view-only user does not see the Edit icon on the BOM and cannot add a line. |
| **Requirement** | `R-XF-05`, `R-Detail_View-60`, `R-Detail_View-59`, `R-Detail_View-19`. Source: [manufacturing-bom.md#L127](../../requirements/docs/manufacturing-bom.md#L127); [manufacturing-bom.md#L124](../../requirements/docs/manufacturing-bom.md#L124); [part-views.md#L84](../../requirements/docs/part-views.md#L84) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Negative (action tried by a user who should be blocked) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: category `QA-<suffix> Category`, component part `QA-<suffix> Flour` (Component on, Units `kg`) and assembly `QA-<suffix> Cake` (Assembly on), created via `POST /api/part/category/` and `POST /api/part/` as `admin` with one BOM line for `QA-<suffix> Flour` (raw amount `500 g`); Pre-steps: log in through the login form, open the detail page of `QA-<suffix> Cake`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *BOM* tab. | None | Proposed, to confirm in Q-Detail_View-01: the tab shows the line, in view mode (R-Detail_View-59). |
| 2 | Look for the *Edit* icon above the BOM table. | None | The *Edit* icon is not shown to a user without permission to edit BOMs (R-Detail_View-60), so no line can be added. Open: Q-Detail_View-01 (which permission `reader` lacks). |

**Postconditions and cleanup:** No records are created. Cleanup as `admin`: delete the BOM line, set both parts inactive and delete them, then the category.

**Notes:** None

---

### UI-XF-034: The BOM and Used In tabs follow the Assembly and Component attributes of four parts.

| Field | Value |
|---|---|
| **Summary** | The BOM and Used In tabs follow the Assembly and Component attributes of four parts. |
| **Requirement** | `R-XF-05`, `R-Detail_View-19`, `R-Detail_View-21`, `R-ATT-08`, `R-ATT-10`. Source: [part-views.md#L84](../../requirements/docs/part-views.md#L84); [part-views.md#L92](../../requirements/docs/part-views.md#L92); [part-index.md#L62](../../requirements/docs/part-index.md#L62); [part-index.md#L68](../../requirements/docs/part-index.md#L68) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Decision table (Assembly x Component: only Component, only Assembly, both, neither) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and four parts created via `POST /api/part/` as `admin`: `QA-<suffix> CompOnly` (Component on, Assembly off), `QA-<suffix> AsmOnly` (Assembly on, Component off), `QA-<suffix> Both` (both on) and `QA-<suffix> Neither` (both off); Pre-steps: log in through the login form. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-XF-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> CompOnly` and check the tabs. | None | The *Used In* tab is visible (R-Detail_View-21); the *BOM* tab is not visible (R-Detail_View-19). |
| 2 | Open `QA-<suffix> AsmOnly` and check the tabs. | None | The *BOM* tab is visible (R-Detail_View-19); the *Used In* tab is not visible (R-Detail_View-21). |
| 3 | Open `QA-<suffix> Both` and check the tabs. | None | Proposed, to confirm in Q-XF-06: both the *BOM* and *Used In* tabs are visible. |
| 4 | Open `QA-<suffix> Neither` and check the tabs. | None | Neither the *BOM* tab nor the *Used In* tab is visible (R-Detail_View-19, R-Detail_View-21). |

**Postconditions and cleanup:** Cleanup as `admin`: set the four parts inactive and delete them, then the category.

**Notes:** None

---

### UI-XF-035: The parameters of a locked part cannot be created, edited or deleted.

| Field | Value |
|---|---|
| **Summary** | The parameters of a locked part cannot be created, edited or deleted. |
| **Requirement** | `R-XF-06`, `R-ATT-24`, `R-ATT-26`, `R-Part_Params-12`. Source: [part-index.md#L108](../../requirements/docs/part-index.md#L108); [part-index.md#L110](../../requirements/docs/part-index.md#L110); [concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Negative (forbidden action on a locked part), State transition (unlocked to locked) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (part management) [open: Q-Part_Params-09, who may change parameters]; Settings: `PART_ENABLE_LOCKING` = on [open: Q-ATT-02, label, location and default]; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Locked` (Assembly on) with one parameter (template `QA-<suffix> Note`, Data `v1`) and one BOM line for component `QA-<suffix> Item` (Component on), created as `admin`; the assembly locked [open: Q-ATT-01, how a part is locked]; Pre-steps: log in through the login form, open the *Parameters* tab of `QA-<suffix> Locked`. |
| **Automation** | Partial: the lock step and the blocked-action behaviour are unconfirmed. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-02, Q-ATT-14, Q-Part_Params-09, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Try to add a parameter with *Add Parameters*, *Create Parameter*. | Template: `QA-<suffix> Note2`<br>Data: `x` | No parameter is created (R-ATT-26). Open: Q-ATT-14 (control hidden, disabled or rejected, and the message). |
| 2 | Try to edit the existing parameter. | Data: `v2` | The parameter keeps the value `v1` (R-ATT-26). Open: Q-ATT-14, Q-Part_Params-19 (label of the edit control). |
| 3 | Try to delete the existing parameter. | None | The parameter is not deleted and is still listed (R-ATT-26). Open: Q-ATT-14. |

**Postconditions and cleanup:** Cleanup as `admin`: unlock the part [open: Q-ATT-01], delete the parameter, the BOM line, set both parts inactive and delete them, then the category and template.

**Notes:** None

---

### UI-XF-036: The BOM lines of a locked assembly cannot be created, edited or deleted.

| Field | Value |
|---|---|
| **Summary** | The BOM lines of a locked assembly cannot be created, edited or deleted. |
| **Requirement** | `R-XF-06`, `R-ATT-25`, `R-Detail_View-59`, `R-Detail_View-62`. Source: [part-index.md#L109](../../requirements/docs/part-index.md#L109); [manufacturing-bom.md#L124](../../requirements/docs/manufacturing-bom.md#L124); [manufacturing-bom.md#L137-L143](../../requirements/docs/manufacturing-bom.md#L137-L143) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Negative (forbidden action on a locked part) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (part management) [open: Q-Detail_View-01]; Settings: `PART_ENABLE_LOCKING` = on [open: Q-ATT-02]; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Locked` (Assembly on) with one parameter (template `QA-<suffix> Note`, Data `v1`) and one BOM line for component `QA-<suffix> Item` (Component on), created as `admin`; the assembly locked [open: Q-ATT-01, how a part is locked] and a second component `QA-<suffix> Item2` (Component on); Pre-steps: log in through the login form, open the *BOM* tab of `QA-<suffix> Locked`. |
| **Automation** | Partial: the lock step and the blocked-action behaviour are unconfirmed. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-02, Q-ATT-14, Q-Detail_View-01, Q-Detail_View-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Switch to editing mode and try to add a line. | Part: `QA-<suffix> Item2` | No BOM line is created (R-ATT-25). Open: Q-ATT-14 (control hidden, disabled or rejected, and the message), Q-Detail_View-02 (editing mode controls). |
| 2 | Try to edit the existing line. | Quantity: `2` | The line keeps its quantity (R-ATT-25). Open: Q-ATT-14, Q-Detail_View-02. |
| 3 | Try to delete the existing line. | None | The line is not deleted (R-ATT-25). Open: Q-ATT-14, Q-Detail_View-02. |

**Postconditions and cleanup:** Cleanup as `admin`: unlock the part [open: Q-ATT-01], delete the BOM line, set the parts inactive and delete them, then the category and template.

**Notes:** None

---

### UI-XF-037: A locked part cannot be deleted.

| Field | Value |
|---|---|
| **Summary** | A locked part cannot be deleted. |
| **Requirement** | `R-XF-06`, `R-ATT-24`. Source: [part-index.md#L108](../../requirements/docs/part-index.md#L108) |
| **Area** | XF |
| **Type** | Negative |
| **Technique** | Negative (forbidden action on a locked part) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `admin` (settings and delete); Settings: `PART_ENABLE_LOCKING` = on [open: Q-ATT-02]; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Locked` (Assembly on) with one parameter (template `QA-<suffix> Note`, Data `v1`) and one BOM line for component `QA-<suffix> Item` (Component on), created as `admin`; the assembly locked [open: Q-ATT-01, how a part is locked]; the part set inactive; Pre-steps: log in through the login form, open the detail page of `QA-<suffix> Locked`. |
| **Automation** | Partial: the lock step and the blocked-action behaviour are unconfirmed. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-02, Q-ATT-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu and select *Delete*. | None | The part is not deleted (R-ATT-24). Open: Q-ATT-14 (control hidden, disabled or rejected, and the message). |
| 2 | Open the part from the category part list. | None | The part still exists and is listed in `QA-<suffix> Category` (R-ATT-24, R-Categories-02). |

**Postconditions and cleanup:** Cleanup as `admin`: unlock the part [open: Q-ATT-01], then delete the BOM line, the parameter and the parts, then the category and template.

**Notes:** The part is set inactive first, as in the seed cleanup order, so that only the lock can block the deletion.

---

### UI-XF-038: With part locking disabled, parameters of a locked part can be created, edited and deleted.

| Field | Value |
|---|---|
| **Summary** | With part locking disabled, parameters of a locked part can be created, edited and deleted. |
| **Requirement** | `R-XF-06`, `R-ATT-27`, `R-ATT-26`, `R-Part_Params-12`. Source: [part-index.md#L112](../../requirements/docs/part-index.md#L112); [part-index.md#L110](../../requirements/docs/part-index.md#L110); [concepts-parameters.md#L65-L69](../../requirements/docs/concepts-parameters.md#L65-L69) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Decision table (`PART_ENABLE_LOCKING` off x locked part), State transition (setting on to off) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (part management) [open: Q-Part_Params-09]; `admin` for the setting; Settings: `PART_ENABLE_LOCKING` = off [open: Q-ATT-02, label, location and default]; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Locked` (Assembly on) with one parameter (template `QA-<suffix> Note`, Data `v1`) and one BOM line for component `QA-<suffix> Item` (Component on), created as `admin`; the assembly locked [open: Q-ATT-01, how a part is locked] and a second template `QA-<suffix> Note2`; Pre-steps: as `admin` switch locking off; log in through the login form as `engineer`, open the *Parameters* tab of `QA-<suffix> Locked`. |
| **Automation** | Partial: the setting and the lock step are unconfirmed. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-02, Q-Part_Params-09, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a parameter with *Add Parameters*, *Create Parameter*. | Template: `QA-<suffix> Note2`<br>Data: `x` | The parameter is created and listed: the locked state is ignored and all operations are permitted (R-ATT-27). |
| 2 | Edit the parameter `QA-<suffix> Note`. | Data: `v2` | The parameter shows `v2` (R-ATT-27). Open: Q-Part_Params-19 (label of the edit control). |
| 3 | Delete the parameter `QA-<suffix> Note2`. | None | The parameter is deleted (R-ATT-27). |

**Postconditions and cleanup:** Cleanup as `admin`: restore the setting to its original value, unlock the part [open: Q-ATT-01], delete the parameter, BOM line and parts, then the category and templates.

**Notes:** None

---

### UI-XF-039: With part locking disabled, BOM lines of a locked assembly can be created, edited and deleted.

| Field | Value |
|---|---|
| **Summary** | With part locking disabled, BOM lines of a locked assembly can be created, edited and deleted. |
| **Requirement** | `R-XF-06`, `R-ATT-27`, `R-ATT-25`, `R-Detail_View-59`, `R-Detail_View-62`. Source: [part-index.md#L112](../../requirements/docs/part-index.md#L112); [part-index.md#L109](../../requirements/docs/part-index.md#L109); [manufacturing-bom.md#L124](../../requirements/docs/manufacturing-bom.md#L124); [manufacturing-bom.md#L137-L143](../../requirements/docs/manufacturing-bom.md#L137-L143) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Decision table (`PART_ENABLE_LOCKING` off x locked part) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `engineer` (part management) [open: Q-Detail_View-01]; `admin` for the setting; Settings: `PART_ENABLE_LOCKING` = off [open: Q-ATT-02]; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Locked` (Assembly on) with one parameter (template `QA-<suffix> Note`, Data `v1`) and one BOM line for component `QA-<suffix> Item` (Component on), created as `admin`; the assembly locked [open: Q-ATT-01, how a part is locked] and a second component `QA-<suffix> Item2` (Component on); Pre-steps: as `admin` switch locking off; log in through the login form as `engineer`, open the *BOM* tab of `QA-<suffix> Locked`. |
| **Automation** | Partial: the setting and the lock step are unconfirmed. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-02, Q-Detail_View-01, Q-Detail_View-02, Q-Detail_View-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Switch to editing mode and add a line. | Part: `QA-<suffix> Item2` | The line is added: the locked state is ignored and all operations are permitted (R-ATT-27, R-Detail_View-62). Open: Q-Detail_View-03 (required fields). |
| 2 | Edit the line of `QA-<suffix> Item`. | Quantity: `2` | The line shows quantity 2 (R-ATT-27). Open: Q-Detail_View-02 (how a line is edited). |
| 3 | Delete the line of `QA-<suffix> Item2`. | None | The line is deleted (R-ATT-27). Open: Q-Detail_View-02. |

**Postconditions and cleanup:** Cleanup as `admin`: restore the setting to its original value, unlock the part [open: Q-ATT-01], delete the BOM lines, the parameter and the parts, then the category and template.

**Notes:** None

---

### UI-XF-040: With part locking disabled, a locked part can be deleted.

| Field | Value |
|---|---|
| **Summary** | With part locking disabled, a locked part can be deleted. |
| **Requirement** | `R-XF-06`, `R-ATT-27`, `R-ATT-24`. Source: [part-index.md#L112](../../requirements/docs/part-index.md#L112); [part-index.md#L108](../../requirements/docs/part-index.md#L108) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Decision table (`PART_ENABLE_LOCKING` off x locked part) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `admin` (settings and delete); Settings: `PART_ENABLE_LOCKING` = off [open: Q-ATT-02]; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Locked` (Assembly on) with one parameter (template `QA-<suffix> Note`, Data `v1`) and one BOM line for component `QA-<suffix> Item` (Component on), created as `admin`; the assembly locked [open: Q-ATT-01, how a part is locked]; the part set inactive; Pre-steps: switch locking off; log in through the login form, open the detail page of `QA-<suffix> Locked`. |
| **Automation** | Partial: the setting and the lock step are unconfirmed. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu and select *Delete*, then confirm. | None | The part is deleted: the locked state is ignored and all operations are permitted (R-ATT-27). Open: Q-ATT-02 (any extra step such as a confirmation, and the page shown afterwards). |
| 2 | Open `QA-<suffix> Category`, then its *Parts* tab. | None | The part is no longer listed (R-ATT-27, R-Categories-02). |

**Postconditions and cleanup:** Cleanup as `admin`: restore the setting to its original value, delete the component, the category and the templates.

**Notes:** The part is set inactive first, as in the seed cleanup order, so that only the lock can block the deletion.

---

### UI-XF-041: A Virtual part has no stock items and its page hides the stock elements.

| Field | Value |
|---|---|
| **Summary** | A Virtual part has no stock items and its page hides the stock elements. |
| **Requirement** | `R-XF-07`, `R-ATT-02`, `R-ATT-03`, `R-ATT-04`. Source: [part-virtual.md#L15](../../requirements/docs/part-virtual.md#L15); [part-virtual.md#L27](../../requirements/docs/part-virtual.md#L27); [part-virtual.md#L23](../../requirements/docs/part-virtual.md#L23) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Virtual part), Negative (stock cannot be added) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Service` (Virtual on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open the detail page of `QA-<suffix> Service`. |
| **Automation** | Partial: the hidden elements are unlisted. |
| **Review** | Draft · Open question: Q-ATT-08, Q-Detail_View-61 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs and the buttons of the part page for stock-related elements. | None | The stock-related user interface elements are hidden (R-ATT-03). Open: Q-ATT-08, Q-Detail_View-61 (which elements are hidden). Proposed, to confirm in Q-Detail_View-61: the *Stock* tab is not listed. |
| 2 | Look for any way to create a stock item for the part. | None | No stock item is created for the part (R-ATT-02); the part has no stock. Open: Q-ATT-08 (how creation is prevented and the error text). |
| 3 | Check the other parts of the page, such as the details panel and the *Parameters* tab. | None | Apart from stock, the part behaves like a regular part (R-ATT-04). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part created inactive and delete it, then delete the category (and any parameter template) created for the case.

**Notes:** None

---

### UI-XF-042: A Virtual part is listed in its category's part list.

| Field | Value |
|---|---|
| **Summary** | A Virtual part is listed in its category's part list. |
| **Requirement** | `R-XF-07`, `R-Categories-02`, `R-Categories-04`, `R-ATT-04`. Source: [part-index.md#L31](../../requirements/docs/part-index.md#L31); [part-index.md#L37-L42](../../requirements/docs/part-index.md#L37-L42); [part-virtual.md#L23](../../requirements/docs/part-virtual.md#L23) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Virtual part in a category) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, Virtual part `QA-<suffix> Service` and regular part `QA-<suffix> Regular` in it, created via `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-XF-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> Category`, then its *Parts* tab. | None | The table lists both parts: it lists every part in the category (R-Categories-02, R-ATT-04; open-questions.md Q-Categories-05). |
| 2 | Check the stock level of `QA-<suffix> Service` in the list. | None | Not known: depends on open question Q-XF-02 (what the stock level shows for a Virtual part). The Virtual part has no stock items (R-ATT-02). |
| 3 | Click the name of `QA-<suffix> Service`. | None | The Part Detail view of the part opens (R-Categories-06). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part created inactive and delete it, then delete the category (and any parameter template) created for the case.

**Notes:** None

---

### UI-XF-043: A Virtual Component part can be added as a line in an Assembly's BOM and stays listed there.

| Field | Value |
|---|---|
| **Summary** | A Virtual Component part can be added as a line in an Assembly's BOM and stays listed there. |
| **Requirement** | `R-XF-07`, `R-ATT-05`, `R-ATT-10`, `R-Detail_View-62`, `R-Detail_View-21`, `R-Detail_View-65`. Source: [part-virtual.md#L31-L33](../../requirements/docs/part-virtual.md#L31-L33); [part-index.md#L68](../../requirements/docs/part-index.md#L68); [manufacturing-bom.md#L137-L143](../../requirements/docs/manufacturing-bom.md#L137-L143); [part-views.md#L92](../../requirements/docs/part-views.md#L92); [manufacturing-bom.md#L163-L181](../../requirements/docs/manufacturing-bom.md#L163-L181) |
| **Area** | XF |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Virtual Component part as BOM line) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management) [open: Q-Detail_View-01]; Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Service` (Virtual on, Component on) and assembly `QA-<suffix> Cake` (Assembly on), created as `admin`; Pre-steps: log in through the login form, open the *BOM* tab of `QA-<suffix> Cake` and switch to editing mode. |
| **Automation** | Partial: the form labels are unconfirmed. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-03, Q-ATT-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press the add icon and fill in the *Create BOM Item* form. | Part: `QA-<suffix> Service`<br>Quantity: `1`<br>Other required fields: [open: Q-Detail_View-03] | The form opens and accepts the part (R-Detail_View-62, R-ATT-05). |
| 2 | Press *Submit*. | None | The line is added and stays listed in the BOM (R-ATT-05). The BOM reads "Not Validated" (R-Detail_View-65). |
| 3 | Open `QA-<suffix> Service` and its *Used In* tab. | None | The tab is visible because the part is a Component and lists `QA-<suffix> Cake` (R-Detail_View-21). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the BOM line, set both parts inactive and delete them, then the category.

**Notes:** None

---
