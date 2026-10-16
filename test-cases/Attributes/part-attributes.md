# Part attributes: ATT test cases

### UI-ATT-001: A part with Assembly on and Component off shows the BOM tab and hides the Used In tab

| Field | Value |
|---|---|
| **Summary** | A part with Assembly on and Component off shows the BOM tab and hides the Used In tab. |
| **Requirement** | `R-ATT-01` [part-index.md#L50](../../requirements/docs/part-index.md#L50); `R-Detail_View-19` [part-views.md#L84](../../requirements/docs/part-views.md#L84); `R-Detail_View-21` [part-views.md#L92](../../requirements/docs/part-views.md#L92) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Decision table (Assembly on, Component on off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Assembly Only` (Assembly on, Component off, all other attributes off) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | Yes: tab visibility check. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the tabs of the part detail page. | None | The *BOM* tab is visible. The *Used In* tab is not visible. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

**Duplicate check:** 78 · Review · matches: [UI-ATT-002](part-attributes.md) (78, test data differs)

**Duplicate judgement:** Keep · Different decision-table column from UI-ATT-002 (Assembly on / Component off vs the reverse) with the opposite expected tab visibility (BOM shown, Used In hidden) · test-case-reviewer, 2026-10-13

### UI-ATT-002: A part with Component on and Assembly off shows the Used In tab and hides the BOM tab

| Field | Value |
|---|---|
| **Summary** | A part with Component on and Assembly off shows the Used In tab and hides the BOM tab. |
| **Requirement** | `R-ATT-01` [part-index.md#L50](../../requirements/docs/part-index.md#L50); `R-Detail_View-19` [part-views.md#L84](../../requirements/docs/part-views.md#L84); `R-Detail_View-21` [part-views.md#L92](../../requirements/docs/part-views.md#L92) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Decision table (Component on, Assembly off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Component Only` (Component on, Assembly off, all other attributes off) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | Yes: tab visibility check. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the tabs of the part detail page. | None | The *Used In* tab is visible. The *BOM* tab is not visible. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

**Duplicate check:** 78 · Review · matches: [UI-ATT-001](part-attributes.md) (78, test data differs)

**Duplicate judgement:** Keep · Different decision-table column from UI-ATT-001 (Component on / Assembly off) with the opposite expected tab visibility (Used In shown, BOM hidden) · test-case-reviewer, 2026-10-13

### UI-ATT-003: A part with Assembly, Component, Purchaseable and Salable all on shows the BOM, Used In, Allocated, Suppliers and Purchase Orders tabs

| Field | Value |
|---|---|
| **Summary** | A part with Assembly, Component, Purchaseable and Salable all on shows the BOM, Used In, Allocated, Suppliers and Purchase Orders tabs. |
| **Requirement** | `R-ATT-01` [part-index.md#L50](../../requirements/docs/part-index.md#L50); `R-Detail_View-17` [part-views.md#L80](../../requirements/docs/part-views.md#L80); `R-Detail_View-19` [part-views.md#L84](../../requirements/docs/part-views.md#L84); `R-Detail_View-21` [part-views.md#L92](../../requirements/docs/part-views.md#L92); `R-Detail_View-23` [part-views.md#L100-L102](../../requirements/docs/part-views.md#L100-L102); `R-Detail_View-24` [part-views.md#L108-L110](../../requirements/docs/part-views.md#L108-L110) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Decision table (all four attributes on) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, so the Suppliers tab is not hidden by missing purchase-order permission); Settings: None; Data: part `QA-<suffix> All Attributes` (Assembly, Component, Purchaseable, Salable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | Yes: tab visibility check. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the tabs of the part detail page. | None | The *BOM*, *Used In*, *Allocated*, *Suppliers* and *Purchase Orders* tabs are all visible. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** In 1.5.6 the *Suppliers* tab is also hidden from users without purchase-order view permission (index doc issue 15), so `allaccess` is used.

**Duplicate check:** 62 · Review · matches: [UI-ATT-004](part-attributes.md) (62)

**Duplicate judgement:** Keep · All-attributes-on column vs UI-ATT-004's all-off column, with the opposite expected outcome (tabs visible vs hidden) · test-case-reviewer, 2026-10-13

### UI-ATT-004: A part with Assembly, Component, Purchaseable, Salable and Testable all off hides the attribute-dependent tabs

| Field | Value |
|---|---|
| **Summary** | A part with Assembly, Component, Purchaseable, Salable and Testable all off hides the attribute-dependent tabs. |
| **Requirement** | `R-ATT-01` [part-index.md#L50](../../requirements/docs/part-index.md#L50); `R-Detail_View-17` [part-views.md#L80](../../requirements/docs/part-views.md#L80); `R-Detail_View-19` [part-views.md#L84](../../requirements/docs/part-views.md#L84); `R-Detail_View-21` [part-views.md#L92](../../requirements/docs/part-views.md#L92); `R-Detail_View-23` [part-views.md#L100-L102](../../requirements/docs/part-views.md#L100-L102); `R-Detail_View-24` [part-views.md#L108-L110](../../requirements/docs/part-views.md#L108-L110); `R-Detail_View-30` [part-views.md#L134](../../requirements/docs/part-views.md#L134) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Decision table (all attributes off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: part `QA-<suffix> No Attributes` (Assembly, Component, Purchaseable, Salable, Testable, Virtual, Trackable off) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | Yes: tab visibility check. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the tabs of the part detail page. | None | The *BOM*, *Used In*, *Allocated*, *Suppliers*, *Purchase Orders* and *Test Results* tabs are not visible. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

**Duplicate check:** 62 · Review · matches: [UI-ATT-003](part-attributes.md) (62)

**Duplicate judgement:** Keep · All-attributes-off column vs UI-ATT-003's all-on column, with the opposite expected outcome (tabs hidden, and Test Results also checked) · test-case-reviewer, 2026-10-13

### UI-ATT-005: Stock cannot be created for a Virtual part

| Field | Value |
|---|---|
| **Summary** | Stock cannot be created for a Virtual part. |
| **Requirement** | `R-ATT-02` [part-virtual.md#L15](../../requirements/docs/part-virtual.md#L15), [part-virtual.md#L27](../../requirements/docs/part-virtual.md#L27) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; Equivalence partitioning (invalid class: Virtual part) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Virtual Stock` (Virtual on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: the blocking mechanism is not known. |
| **Review** | Draft · Open question: Q-ATT-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Start creating a new stock item and choose the part. | Part: `QA-<suffix> Virtual Stock` | No stock item is created for `QA-<suffix> Virtual Stock` (R-ATT-02: a Virtual part cannot have stock items). Open: Q-ATT-08 (whether the part is left out of the part selector or the form is rejected, and the error text). |
| 2 | Submit the form if it can be submitted. | Quantity: `1` | No stock item is created. Error text not known: depends on open question Q-ATT-08 (rejection message). |
| 3 | Open the part's detail page and check its stock. | None | The part has no stock items. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-006: Turning Virtual on for a part that already has stock

| Field | Value |
|---|---|
| **Summary** | Turning Virtual on for a part that already has stock. |
| **Requirement** | `R-ATT-02` [part-virtual.md#L15](../../requirements/docs/part-virtual.md#L15), [part-virtual.md#L27](../../requirements/docs/part-virtual.md#L27) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | State transition (non-Virtual with stock to Virtual); What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: non-virtual part `QA-<suffix> Was Physical` and one stock item of it, via the API as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | No: outcome not known. |
| **Review** | Draft · Open question: Q-ATT-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part's edit form and tick *Virtual*. | None | The *Virtual* checkbox can be ticked. |
| 2 | Submit the form. | None | Proposed, to confirm in Q-ATT-08: the change is rejected, because the part has stock and a Virtual part cannot have stock items (R-ATT-02). Open: Q-ATT-08 (the error text). |
| 3 | Check the stock of the part. | None | Proposed, to confirm in Q-ATT-08: the stock item still exists and the part is not Virtual. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock item first.

**Notes:** The docs only say Virtual parts cannot have stock items; they do not describe a part that already has stock.

### UI-ATT-007: The page of a Virtual part hides the Transfer Orders tab and the stock-related UI elements

| Field | Value |
|---|---|
| **Summary** | The page of a Virtual part hides the Transfer Orders tab and the stock-related UI elements. |
| **Requirement** | `R-ATT-03` [part-virtual.md#L27](../../requirements/docs/part-virtual.md#L27); `R-Detail_View-27` [part-views.md#L122](../../requirements/docs/part-views.md#L122) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Virtual part) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: None; Data: part `QA-<suffix> Virtual View` (Virtual on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | Partial: the list of hidden elements is not known. |
| **Review** | Draft · Open question: Q-ATT-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the tabs and panels of the part detail page. | None | The *Transfer Orders* tab is not visible. Open: Q-ATT-08 (which other stock-related UI elements are hidden; the docs do not list them). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-008: A Virtual part behaves like a regular part: it can be edited and saved

| Field | Value |
|---|---|
| **Summary** | A Virtual part behaves like a regular part: it can be edited and saved. |
| **Requirement** | `R-ATT-04` [part-virtual.md#L23](../../requirements/docs/part-virtual.md#L23) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Virtual part, non-stock action) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Virtual Edit` (Virtual on, description `Before`) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | Yes: edit flow. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part's edit form. | None | The edit form opens. |
| 2 | Change the description and submit. | Description: `After edit` | The form closes and the detail page shows the description `After edit`. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-009: A Virtual part can be added as a BOM sub-component and stays listed in the BOM

| Field | Value |
|---|---|
| **Summary** | A Virtual part can be added as a BOM sub-component and stays listed in the BOM. |
| **Requirement** | `R-ATT-05` [part-virtual.md#L31-L33](../../requirements/docs/part-virtual.md#L31-L33) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Virtual part as BOM line) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Virtual Labor` (Virtual on, Component on) via `POST /api/part/` as `admin`; part `QA-<suffix> Assembly For Virtual` (Assembly on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the assembly's *BOM* tab. |
| **Automation** | Yes: BOM flow. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a BOM line for the Virtual part. | Sub-component: `QA-<suffix> Virtual Labor`<br>Quantity: `1` | The BOM line is saved without error. |
| 2 | Check the BOM table. | None | `QA-<suffix> Virtual Labor` is listed in the BOM. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-010: A Virtual part in a BOM is hidden from the required parts list of a Build Order

| Field | Value |
|---|---|
| **Summary** | A Virtual part in a BOM is hidden from the required parts list of a Build Order. |
| **Requirement** | `R-ATT-06` [part-virtual.md#L37-L39](../../requirements/docs/part-virtual.md#L37-L39) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Virtual BOM line in a build) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, builds); Settings: None; Data: part `QA-<suffix> Virtual Labor B` (Virtual on, Component on) via `POST /api/part/` as `admin`; part `QA-<suffix> Assembly B` (Assembly on) via `POST /api/part/` as `admin`; part `QA-<suffix> Regular Component B` (Component on) via `POST /api/part/` as `admin`; BOM lines for both sub-components on the assembly; one Build Order for the assembly; all via the API as `admin`; Pre-steps: log in through the login form; open the Build Order. |
| **Automation** | Partial: Build Orders module. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the list of required parts of the Build Order. | None | `QA-<suffix> Regular Component B` is listed. `QA-<suffix> Virtual Labor B` is not listed. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Build Order first.

**Notes:** None

### UI-ATT-011: The cost of a Virtual part in a BOM is included in the total cost of the Build Order

| Field | Value |
|---|---|
| **Summary** | The cost of a Virtual part in a BOM is included in the total cost of the Build Order. |
| **Requirement** | `R-ATT-06` [part-virtual.md#L37-L39](../../requirements/docs/part-virtual.md#L37-L39) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Virtual BOM line, cost) |
| **Priority** | P3 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, builds); Settings: None; Data: as the Virtual build case above, with a price on the Virtual part [open: Q-ATT-12, how a price is set]; Pre-steps: log in through the login form; open the Build Order. |
| **Automation** | No: location of the cost not known. |
| **Review** | Draft · Open question: Q-ATT-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Find the total cost of the build. | None | The build total cost includes the cost of the Virtual part (R-ATT-06). Open: Q-ATT-12 (where the build total cost is shown). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Build Order first.

**Notes:** None

### UI-ATT-012: A Virtual part can be added to a Sales Order and no stock is allocated for it

| Field | Value |
|---|---|
| **Summary** | A Virtual part can be added to a Sales Order and no stock is allocated for it. |
| **Requirement** | `R-ATT-07` [part-virtual.md#L43-L47](../../requirements/docs/part-virtual.md#L43-L47) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Virtual part on a sales order) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, sales); Settings: None; Data: part `QA-<suffix> Virtual Service` (Virtual on, Salable on) via `POST /api/part/` as `admin`; a customer company and a Sales Order, via the API as `admin`; Pre-steps: log in through the login form; open the Sales Order. |
| **Automation** | Partial: Sales Orders module. |
| **Review** | Draft · Open question: Q-ATT-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a line item for the Virtual part. | Part: `QA-<suffix> Virtual Service`<br>Quantity: `1` | The line item is added and listed in the order. |
| 2 | Check the allocation of the line item. | None | No stock is allocated for the line item (the Virtual part has no stock). |
| 3 | Check the order total cost. | None | The order total cost includes the Virtual part's line (R-ATT-07). Open: Q-ATT-12 (where the total is shown and how a price is set). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Sales Order and the customer company first.

**Notes:** None

### UI-ATT-013: An Assembly part has a BOM to which a Component part can be added

| Field | Value |
|---|---|
| **Summary** | An Assembly part has a BOM to which a Component part can be added. |
| **Requirement** | `R-ATT-08` [part-index.md#L62](../../requirements/docs/part-index.md#L62); `R-ATT-10` [part-index.md#L68](../../requirements/docs/part-index.md#L68) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Assembly with Component line) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Assembly Main` (Assembly on) via `POST /api/part/` as `admin`; part `QA-<suffix> Component One` (Component on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the assembly's *BOM* tab. |
| **Automation** | Yes: BOM flow. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a BOM line. | Sub-component: `QA-<suffix> Component One`<br>Quantity: `2` | The BOM line is saved without error. |
| 2 | Check the BOM table. | None | `QA-<suffix> Component One` is listed with quantity `2`. |
| 3 | Open the Component part's *Used In* tab. | None | `QA-<suffix> Assembly Main` is listed. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the BOM line first.

**Notes:** None

### UI-ATT-014: A part that is not an Assembly has no BOM tab

| Field | Value |
|---|---|
| **Summary** | A part that is not an Assembly has no BOM tab. |
| **Requirement** | `R-ATT-08` [part-index.md#L62](../../requirements/docs/part-index.md#L62); `R-Detail_View-19` [part-views.md#L84](../../requirements/docs/part-views.md#L84) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; Equivalence partitioning (invalid class: Assembly off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Not Assembly` (Assembly off, Component on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | Yes: tab visibility. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for a *BOM* tab. | None | The *BOM* tab is not visible. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-015: A non-Component part added to an assembly BOM

| Field | Value |
|---|---|
| **Summary** | A non-Component part added to an assembly BOM. |
| **Requirement** | `R-ATT-10` [part-index.md#L68](../../requirements/docs/part-index.md#L68) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: Component off); Negative |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Assembly Target` (Assembly on) via `POST /api/part/` as `admin`; part `QA-<suffix> Not Component` (Component off) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the assembly's *BOM* tab. |
| **Automation** | No: outcome not known. |
| **Review** | Draft · Open question: Q-ATT-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Start a new BOM line and look for the part in the sub-component selector. | Sub-component: `QA-<suffix> Not Component` | Proposed, to confirm in Q-ATT-05: `QA-<suffix> Not Component` is not offered in the sub-component selector; only Component parts are sub-components (R-ATT-10). Open: Q-ATT-05 (the error text if it is blocked on submit instead). |
| 2 | Submit the line if possible. | Quantity: `1` | Proposed, to confirm in Q-ATT-05: no BOM line is saved for `QA-<suffix> Not Component`. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-016: Component turned off for a part that is already used in a BOM

| Field | Value |
|---|---|
| **Summary** | Component turned off for a part that is already used in a BOM. |
| **Requirement** | `R-ATT-10` [part-index.md#L68](../../requirements/docs/part-index.md#L68) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | State transition (Component on to off while used); What-if business scenario |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Assembly Used` (Assembly on) via `POST /api/part/` as `admin`; part `QA-<suffix> Component Used` (Component on) via `POST /api/part/` as `admin`; a BOM line of the component on the assembly, via the API as `admin`; Pre-steps: log in through the login form; open the Component part's detail page. |
| **Automation** | No: outcome not known. |
| **Review** | Draft · Open question: Q-ATT-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the edit form, untick *Component* and submit. | None | Proposed, to confirm in Q-ATT-05: the change is rejected while the part is used in a BOM, as a sub-component must be a Component (R-ATT-10). Open: Q-ATT-05 (the error text). |
| 2 | Open the assembly's *BOM* tab. | None | Proposed, to confirm in Q-ATT-05: the BOM line for the part is still there. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the BOM line first.

**Notes:** None

### UI-ATT-017: An assembled stock item can be broken down into its components

| Field | Value |
|---|---|
| **Summary** | An assembled stock item can be broken down into its components. |
| **Requirement** | `R-ATT-09` [part-index.md#L64](../../requirements/docs/part-index.md#L64) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Exploratory |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: part `QA-<suffix> Assembly Break` (Assembly on) via `POST /api/part/` as `admin` with a BOM and one stock item, via the API as `admin`; Pre-steps: log in through the login form; open the stock item. |
| **Automation** | No: procedure not documented. |
| **Review** | Draft · Open question: Q-ATT-10 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Find the action that breaks the stock item down into its components [open: Q-ATT-10, action name and location]. | None | The stock item is broken down into stock items of its components (R-ATT-09). Open: Q-ATT-10 (the procedure, and the quantities and locations of the resulting items). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-018: A test template can be added to a Testable part

| Field | Value |
|---|---|
| **Summary** | A test template can be added to a Testable part. |
| **Requirement** | `R-ATT-11` [part-index.md#L72](../../requirements/docs/part-index.md#L72) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Testable part) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Testable` (Testable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | Yes: template flow. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab and add a template. | Test name: `QA-<suffix> Visual Check` | The template is saved and listed in the *Test Templates* tab. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** Template fields are covered in Detail_View; this case only checks that a Testable part can have a template.

### UI-ATT-019: A test result can be recorded against a stock item of a Testable part

| Field | Value |
|---|---|
| **Summary** | A test result can be recorded against a stock item of a Testable part. |
| **Requirement** | `R-ATT-11` [part-index.md#L72](../../requirements/docs/part-index.md#L72) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Testable part with template) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: part `QA-<suffix> Testable Result` (Testable on) via `POST /api/part/` as `admin` with test template `QA-<suffix> Visual Check` and one stock item, via the API as `admin`; Pre-steps: log in through the login form; open the stock item. |
| **Automation** | No: the stock test page is not in the docs snapshot. |
| **Review** | Draft · Open question: Q-ATT-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a test result for the template [open: Q-ATT-11, where and how a result is added]. | Result: pass | A `pass` result is recorded against the stock item and shown for it (R-ATT-11). Open: Q-ATT-11 (the form and where the result is shown). |
| 2 | Open the part's *Test Results* tab. | None | The *Test Results* tab is visible. Open: Q-ATT-11 (how the recorded result is shown in the table). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock item first.

**Notes:** None

### UI-ATT-020: A part that is not Testable does not show the Test Results tab

| Field | Value |
|---|---|
| **Summary** | A part that is not Testable does not show the Test Results tab. |
| **Requirement** | `R-ATT-11` [part-index.md#L72](../../requirements/docs/part-index.md#L72); `R-Detail_View-30` [part-views.md#L134](../../requirements/docs/part-views.md#L134) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; Equivalence partitioning (invalid class: Testable off) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Not Testable` (Testable off) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | Yes: tab visibility. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for a *Test Results* tab. | None | The *Test Results* tab is not visible. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-021: A stock item of a Trackable part can be given a batch number

| Field | Value |
|---|---|
| **Summary** | A stock item of a Trackable part can be given a batch number. |
| **Requirement** | `R-ATT-12` [part-index.md#L76](../../requirements/docs/part-index.md#L76) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: batch number) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Batch` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates a stock item for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Batch` | The form opens. |
| 2 | Fill in quantity and batch code. | Quantity: `10`<br>Batch code: `QA-<suffix>-B1` | The fields accept the values. |
| 3 | Submit. | None | The stock item is created and shows batch code `QA-<suffix>-B1`. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock item first.

**Notes:** None

### UI-ATT-022: Single serial number `1` creates one stock item with serial 1

| Field | Value |
|---|---|
| **Summary** | Single serial number `1` creates one stock item with serial 1. |
| **Requirement** | `R-ATT-12` [part-index.md#L76](../../requirements/docs/part-index.md#L76); `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (single) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `1`<br>Serial numbers: `1` | The fields accept the input. |
| 3 | Submit. | None | One stock item is created with serial number `1`. |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 72 · Review · matches: [UI-ATT-025](part-attributes.md) (72), [UI-ATT-023](part-attributes.md) (62), [UI-ATT-024](part-attributes.md) (60), [UI-ATT-026](part-attributes.md) (58), [UI-ATT-027](part-attributes.md) (58), +2 more

**Duplicate judgement:** Keep · Tests the "single SN" row of the R-ATT-14 table; every match tests a different row (next `~`, list, range, start-plus, start-plus-length) with a different expected serial set · test-case-reviewer, 2026-10-13

### UI-ATT-023: List `1,3,5` creates serial numbers 1, 3 and 5

| Field | Value |
|---|---|
| **Summary** | List `1,3,5` creates serial numbers 1, 3 and 5. |
| **Requirement** | `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (list) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `3`<br>Serial numbers: `1,3,5` | The fields accept the input. |
| 3 | Submit. | None | Stock is created with serial numbers `1`, `3` and `5`. |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 81 · Duplicate · matches: [UI-ATT-024](part-attributes.md) (81), [UI-ATT-026](part-attributes.md) (76), [UI-ATT-027](part-attributes.md) (74), [UI-ATT-025](part-attributes.md) (69), [UI-ATT-028](part-attributes.md) (64), +5 more

**Duplicate judgement:** Keep · Tests the comma "list" row of the R-ATT-14 table; the closest match UI-ATT-024 tests the "range" row, and the other matches other rows, each with a different expected serial set · test-case-reviewer, 2026-10-13

### UI-ATT-024: Range `1-5` creates serial numbers 1 to 5

| Field | Value |
|---|---|
| **Summary** | Range `1-5` creates serial numbers 1 to 5. |
| **Requirement** | `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (range) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `5`<br>Serial numbers: `1-5` | The fields accept the input. |
| 3 | Submit. | None | Stock is created with serial numbers `1`, `2`, `3`, `4`, `5`. |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 81 · Duplicate · matches: [UI-ATT-023](part-attributes.md) (81), [UI-ATT-026](part-attributes.md) (75), [UI-ATT-027](part-attributes.md) (75), [UI-ATT-025](part-attributes.md) (68), [UI-ATT-028](part-attributes.md) (64), +5 more

**Duplicate judgement:** Keep · Tests the "range" (`-`) row of the R-ATT-14 table; the closest match UI-ATT-023 tests the "list" row, and the other matches other rows, each with a different expected serial set · test-case-reviewer, 2026-10-13

### UI-ATT-025: `~` gives the next serial number (8)

| Field | Value |
|---|---|
| **Summary** | `~` gives the next serial number (8). |
| **Requirement** | `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (next) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; existing stock item with serial `7` of the same part, via the API as `admin` [open: Q-ATT-09, how the next serial number is determined] (intended: next serial number is 8); Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `1`<br>Serial numbers: `~` | The fields accept the input. |
| 3 | Submit. | None | One stock item is created with serial number `8`. |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 72 · Review · matches: [UI-ATT-022](part-attributes.md) (72), [UI-ATT-023](part-attributes.md) (69), [UI-ATT-026](part-attributes.md) (69), [UI-ATT-027](part-attributes.md) (69), [UI-ATT-024](part-attributes.md) (68), +3 more

**Duplicate judgement:** Keep · Tests the "next SN" (`~`) row of R-ATT-14 with a different starting state (an existing serial 7) than UI-ATT-022's literal single serial; the other matches test other rows · test-case-reviewer, 2026-10-13

### UI-ATT-026: `4+` with 3 numbers needed gives 4, 5, 6

| Field | Value |
|---|---|
| **Summary** | `4+` with 3 numbers needed gives 4, 5, 6. |
| **Requirement** | `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (start-plus) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `3`<br>Serial numbers: `4+` | The fields accept the input. |
| 3 | Submit. | None | Stock is created with serial numbers `4`, `5`, `6`. |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 78 · Review · matches: [UI-ATT-027](part-attributes.md) (78), [UI-ATT-023](part-attributes.md) (76), [UI-ATT-024](part-attributes.md) (75), [UI-ATT-025](part-attributes.md) (69), [UI-ATT-028](part-attributes.md) (64), +5 more

**Duplicate judgement:** Keep · Tests the `<start>+` row (count taken from the quantity) of R-ATT-14; the closest match UI-ATT-027 tests `<start>+<length>` (count given in the input), a different clause · test-case-reviewer, 2026-10-13

### UI-ATT-027: `2+2` gives 2, 3, 4

| Field | Value |
|---|---|
| **Summary** | `2+2` gives 2, 3, 4. |
| **Requirement** | `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (start-plus-length); Boundary value analysis (length 2) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `3`<br>Serial numbers: `2+2` | The fields accept the input. |
| 3 | Submit. | None | Stock is created with serial numbers `2`, `3`, `4`. |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 78 · Review · matches: [UI-ATT-026](part-attributes.md) (78), [UI-ATT-024](part-attributes.md) (75), [UI-ATT-023](part-attributes.md) (74), [UI-ATT-025](part-attributes.md) (69), [UI-ATT-028](part-attributes.md) (69), +5 more

**Duplicate judgement:** Keep · Tests the `<start>+<length>` row of R-ATT-14 (documented example `2+2`); UI-ATT-026 tests `<start>+` and UI-ATT-028 the length-1 boundary with an open outcome · test-case-reviewer, 2026-10-13

### UI-ATT-028: `2+1` (length 1) gives 2 and 3

| Field | Value |
|---|---|
| **Summary** | `2+1` (length 1) gives 2 and 3. |
| **Requirement** | `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Boundary value analysis (length 1, smallest non-zero) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `2`<br>Serial numbers: `2+1` | The fields accept the input. |
| 3 | Submit. | None | Per the rule, `<length>` serial numbers are added to `<start>`: `2` and `3` are expected. Open: Q-ATT-09 (the docs show only the example `2+2`, so length 1 follows from the rule wording, not from an example). |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 69 · Review · matches: [UI-ATT-027](part-attributes.md) (69), [UI-ATT-023](part-attributes.md) (64), [UI-ATT-024](part-attributes.md) (64), [UI-ATT-025](part-attributes.md) (64), [UI-ATT-026](part-attributes.md) (64), +1 more

**Duplicate judgement:** Keep · Boundary value (length 1, smallest non-zero) vs UI-ATT-027's documented example (length 2), with an expected result that depends on Q-ATT-09; the other matches test other R-ATT-14 rows · test-case-reviewer, 2026-10-13

### UI-ATT-029: `2+0` (length 0)

| Field | Value |
|---|---|
| **Summary** | `2+0` (length 0). |
| **Requirement** | `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (length 0) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `1`<br>Serial numbers: `2+0` | The fields accept the input. |
| 3 | Submit. | None | Proposed, to confirm in Q-ATT-09: one stock item with serial number `2` is created, following the rule's pattern (`2+2` gives 2, 3, 4, so `2+0` gives 2) (R-ATT-14). |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

### UI-ATT-030: Mixed rules separated by spaces: `1 3-5 9+2`

| Field | Value |
|---|---|
| **Summary** | Mixed rules separated by spaces: `1 3-5 9+2`. |
| **Requirement** | `R-ATT-15` [part-trackable.md#L38-L42](../../requirements/docs/part-trackable.md#L38-L42) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (space separator, combined rules) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `7`<br>Serial numbers: `1 3-5 9+2` | The fields accept the input. |
| 3 | Submit. | None | Stock is created with serial numbers `1`, `3`, `4`, `5`, `9`, `10`, `11`. |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 95 · Duplicate · matches: [UI-ATT-031](part-attributes.md) (95), [UI-ATT-033](part-attributes.md) (70), [UI-ATT-032](part-attributes.md) (69), [UI-ATT-023](part-attributes.md) (53), [UI-ATT-024](part-attributes.md) (53), +2 more

**Duplicate judgement:** Keep · Whitespace separator vs UI-ATT-031's comma separator: R-ATT-15 names both separators and gives each as its own example, so they are separate clauses; the other matches use `~` or single rules · test-case-reviewer, 2026-10-13

### UI-ATT-031: Mixed rules separated by commas: `1,3-5,9+2`

| Field | Value |
|---|---|
| **Summary** | Mixed rules separated by commas: `1,3-5,9+2`. |
| **Requirement** | `R-ATT-15` [part-trackable.md#L38-L42](../../requirements/docs/part-trackable.md#L38-L42) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (comma separator, combined rules) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `7`<br>Serial numbers: `1,3-5,9+2` | The fields accept the input. |
| 3 | Submit. | None | Stock is created with serial numbers `1`, `3`, `4`, `5`, `9`, `10`, `11`. |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 95 · Duplicate · matches: [UI-ATT-030](part-attributes.md) (95), [UI-ATT-033](part-attributes.md) (70), [UI-ATT-032](part-attributes.md) (69), [UI-ATT-023](part-attributes.md) (53), [UI-ATT-024](part-attributes.md) (53), +2 more

**Duplicate judgement:** Keep · Comma separator vs UI-ATT-030's whitespace separator: R-ATT-15 names both separators and gives each as its own example, so they are separate clauses; the other matches use `~` or single rules · test-case-reviewer, 2026-10-13

### UI-ATT-032: `~+2` with next serial 14 gives 14, 15, 16

| Field | Value |
|---|---|
| **Summary** | `~+2` with next serial 14 gives 14, 15, 16. |
| **Requirement** | `R-ATT-15` [part-trackable.md#L38-L42](../../requirements/docs/part-trackable.md#L38-L42) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (next plus length) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; existing stock item with serial `13` of the same part, via the API as `admin` [open: Q-ATT-09, how the next serial number is determined] (intended: next serial number is 14); Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `3`<br>Serial numbers: `~+2` | The fields accept the input. |
| 3 | Submit. | None | Stock is created with serial numbers `14`, `15`, `16`. |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 86 · Duplicate · matches: [UI-ATT-033](part-attributes.md) (86), [UI-ATT-030](part-attributes.md) (69), [UI-ATT-031](part-attributes.md) (69), [UI-ATT-027](part-attributes.md) (58), [UI-ATT-026](part-attributes.md) (55), +3 more

**Duplicate judgement:** Keep · `~+2` (explicit length, 3 serials) vs UI-ATT-033's `~+` (count taken from the quantity, 2 serials): different clauses of R-ATT-15 with different expected sets · test-case-reviewer, 2026-10-13

### UI-ATT-033: `~+` with next serial 14 and 2 numbers needed gives 14, 15

| Field | Value |
|---|---|
| **Summary** | `~+` with next serial 14 and 2 numbers needed gives 14, 15. |
| **Requirement** | `R-ATT-15` [part-trackable.md#L38-L42](../../requirements/docs/part-trackable.md#L38-L42) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (next plus, count from quantity) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; existing stock item with serial `13` of the same part, via the API as `admin` [open: Q-ATT-09, how the next serial number is determined] (intended: next serial number is 14); Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `2`<br>Serial numbers: `~+` | The fields accept the input. |
| 3 | Submit. | None | Stock is created with serial numbers `14`, `15`. |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 86 · Duplicate · matches: [UI-ATT-032](part-attributes.md) (86), [UI-ATT-030](part-attributes.md) (70), [UI-ATT-031](part-attributes.md) (70), [UI-ATT-026](part-attributes.md) (56), [UI-ATT-027](part-attributes.md) (55), +4 more

**Duplicate judgement:** Keep · `~+` (count taken from the quantity, 2 serials) vs UI-ATT-032's `~+2` (explicit length, 3 serials): different clauses of R-ATT-15 with different expected sets · test-case-reviewer, 2026-10-13

### UI-ATT-034: A duplicate serial number in the input `1,1`

| Field | Value |
|---|---|
| **Summary** | A duplicate serial number in the input `1,1`. |
| **Requirement** | `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate in input); Negative |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `2`<br>Serial numbers: `1,1` | The fields accept the input. |
| 3 | Submit. | None | Proposed, to confirm in Q-ATT-09: the input is rejected and no stock item is created; a serial number cannot appear twice. Open: Q-ATT-09 (the error text). |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 83 · Duplicate · matches: [UI-ATT-038](part-attributes.md) (83), [UI-ATT-037](part-attributes.md) (82), [UI-ATT-036](part-attributes.md) (80), [UI-ATT-035](part-attributes.md) (63)

**Duplicate judgement:** Keep · Invalid class "same serial repeated in one input" (`1,1`) differs from every match: count mismatch (038), non-numeric text (037), reversed range (036), serial already in the database (035) · test-case-reviewer, 2026-10-13

### UI-ATT-035: A serial number that already exists for the part

| Field | Value |
|---|---|
| **Summary** | A serial number that already exists for the part. |
| **Requirement** | `R-ATT-12` [part-index.md#L76](../../requirements/docs/part-index.md#L76); `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Error guessing (existing serial); Negative |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; existing stock item with serial `1` of the same part, via the API as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `1`<br>Serial numbers: `1` | The fields accept the input. |
| 3 | Submit. | None | No second stock item with the same serial number is created; serial numbers uniquely identify a stock item (R-ATT-12, R-ATT-14). Open: Q-ATT-09 (the rejection and its error text). |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 63 · Review · matches: [UI-ATT-034](part-attributes.md) (63), [UI-ATT-037](part-attributes.md) (63), [UI-ATT-038](part-attributes.md) (62), [UI-ATT-036](part-attributes.md) (59)

**Duplicate judgement:** Keep · Different starting state (serial 1 already exists for the part) and a valid input format, vs the matches, which each submit a malformed input against an empty part · test-case-reviewer, 2026-10-13

### UI-ATT-036: A reversed range `5-1`

| Field | Value |
|---|---|
| **Summary** | A reversed range `5-1`. |
| **Requirement** | `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid range); Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `5`<br>Serial numbers: `5-1` | The fields accept the input. |
| 3 | Submit. | None | Proposed, to confirm in Q-ATT-09: the input is rejected and no stock item is created; `5-1` is not a valid range (R-ATT-14). Open: Q-ATT-09 (the error text). |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 80 · Review · matches: [UI-ATT-034](part-attributes.md) (80), [UI-ATT-037](part-attributes.md) (80), [UI-ATT-038](part-attributes.md) (80), [UI-ATT-035](part-attributes.md) (59)

**Duplicate judgement:** Keep · Invalid class "reversed range" (`5-1`) differs from every match: repeated serial (034), non-numeric text (037), count mismatch (038), existing serial (035) · test-case-reviewer, 2026-10-13

### UI-ATT-037: Free text that is not a serial rule: `abc`

| Field | Value |
|---|---|
| **Summary** | Free text that is not a serial rule: `abc`. |
| **Requirement** | `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid format); Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `1`<br>Serial numbers: `abc` | The fields accept the input. |
| 3 | Submit. | None | The input is rejected and no stock item is created: `abc` is none of the accepted serial number formats (R-ATT-14). Open: Q-ATT-09 (the error text). |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 82 · Duplicate · matches: [UI-ATT-034](part-attributes.md) (82), [UI-ATT-038](part-attributes.md) (81), [UI-ATT-036](part-attributes.md) (80), [UI-ATT-035](part-attributes.md) (63)

**Duplicate judgement:** Keep · Invalid class "not a serial rule at all" (`abc`) differs from every match, which use numeric but invalid inputs (repeat, count mismatch, reversed range) or an existing serial · test-case-reviewer, 2026-10-13

### UI-ATT-038: Quantity does not match the number of serial numbers: quantity 3 with `1,3`

| Field | Value |
|---|---|
| **Summary** | Quantity does not match the number of serial numbers: quantity 3 with `1,3`. |
| **Requirement** | `R-ATT-14` [part-trackable.md#L29-L36](../../requirements/docs/part-trackable.md#L29-L36) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Error guessing (count mismatch); Negative |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Serial` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft · Open question: Q-ATT-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates stock items for the part [open: Q-ATT-09, which form and its field labels]. | Part: `QA-<suffix> Trackable Serial` | The form opens. |
| 2 | Enter the quantity and the serial numbers. | Quantity: `3`<br>Serial numbers: `1,3` | The fields accept the input. |
| 3 | Submit. | None | Proposed, to confirm in Q-ATT-09: the input is rejected and no stock item is created; 2 serial numbers do not match quantity 3. Open: Q-ATT-09 (the error text). |
| 4 | Open the part's *Stock* tab. | None | The stock list matches the result of step 3. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock items first.

**Notes:** The stock creation form and the serial number field label are not named in the docs (Q-ATT-09); the rule text is quoted from the serial number table.

**Duplicate check:** 83 · Duplicate · matches: [UI-ATT-034](part-attributes.md) (83), [UI-ATT-037](part-attributes.md) (81), [UI-ATT-036](part-attributes.md) (80), [UI-ATT-035](part-attributes.md) (62)

**Duplicate judgement:** Keep · Invalid class "valid serial list whose count differs from the quantity" differs from every match, where the serial input itself is invalid or already used · test-case-reviewer, 2026-10-13

### UI-ATT-039: Stock of a Trackable part created without a batch or serial number

| Field | Value |
|---|---|
| **Summary** | Stock of a Trackable part created without a batch or serial number. |
| **Requirement** | `R-ATT-13` [part-trackable.md#L19-L21](../../requirements/docs/part-trackable.md#L19-L21) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: neither batch nor serial); Negative |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Trackable Plain` (Trackable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | No: enforcement not known. |
| **Review** | Draft · Open question: Q-ATT-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form that creates a stock item for the part [open: Q-ATT-04, form and labels]. | Part: `QA-<suffix> Trackable Plain` | The form opens. |
| 2 | Enter a quantity only; leave batch code and serial numbers empty, and submit. | Quantity: `5` | Proposed, to confirm in Q-ATT-04: the stock item is created; the docs say a Trackable part's stock should generally have a batch or serial number, not that it must (R-ATT-13). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock item first.

**Notes:** Doc issue 11 in the index: where this is enforced is unclear.

### UI-ATT-040: A build output for a Trackable part is created without serial numbers as one output with the full quantity

| Field | Value |
|---|---|
| **Summary** | A build output for a Trackable part is created without serial numbers as one output with the full quantity. |
| **Requirement** | `R-ATT-16` [part-trackable.md#L51-L53](../../requirements/docs/part-trackable.md#L51-L53) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: no serial numbers) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, builds); Settings: None; Data: part `QA-<suffix> Trackable Assembly` (Trackable on, Assembly on) via `POST /api/part/` as `admin` and a Build Order for it, via the API as `admin`; Pre-steps: log in through the login form; open the Build Order. |
| **Automation** | Partial: Build Orders module. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a build output for the Build Order and leave the serial numbers empty. | Quantity: `5`<br>Serial numbers: empty | The output is created without an error. |
| 2 | Check the list of build outputs. | None | One build output with quantity `5` is listed, not five separate outputs. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Build Order first.

**Notes:** None

### UI-ATT-041: Serial numbers are required for a build output when the BOM has a Trackable sub-component, although the assembly is not Trackable

| Field | Value |
|---|---|
| **Summary** | Serial numbers are required for a build output when the BOM has a Trackable sub-component, although the assembly is not Trackable. |
| **Requirement** | `R-ATT-17` [part-trackable.md#L56](../../requirements/docs/part-trackable.md#L56) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Decision table (assembly Trackable off, tracked BOM line on) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, builds); Settings: None; Data: part `QA-<suffix> Plain Assembly` (Assembly on, Trackable off) via `POST /api/part/` as `admin`; part `QA-<suffix> Tracked Component` (Component on, Trackable on) via `POST /api/part/` as `admin`; a BOM line for it and a Build Order, via the API as `admin`; Pre-steps: log in through the login form; open the Build Order. |
| **Automation** | Partial: Build Orders module. |
| **Review** | Draft · Open question: Q-ATT-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a build output and leave the serial numbers empty. | Quantity: `1`<br>Serial numbers: empty | The output is not created without serial numbers. Open: Q-ATT-13 (the error text and how the form shows it). |
| 2 | Create a build output with serial numbers. | Quantity: `1`<br>Serial numbers: `1` | The output is created with serial number `1`. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Build Order first.

**Notes:** None

### UI-ATT-042: A supplier part can be linked to a Purchaseable part

| Field | Value |
|---|---|
| **Summary** | A supplier part can be linked to a Purchaseable part. |
| **Requirement** | `R-ATT-18` [part-index.md#L82](../../requirements/docs/part-index.md#L82), [part-index.md#L90](../../requirements/docs/part-index.md#L90) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Purchaseable) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access, suppliers); Settings: None; Data: part `QA-<suffix> Purchase Part` (Purchaseable on) via `POST /api/part/` as `admin`; supplier company `QA-<suffix> Supplier`, via the API as `admin`; Pre-steps: log in through the login form; open the part's *Suppliers* tab. |
| **Automation** | Partial. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a supplier part. | Supplier: `QA-<suffix> Supplier`<br>SKU: `QA-<suffix>-SKU` | The supplier part is saved and listed in the *Suppliers* tab. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the supplier part and the supplier company first.

**Notes:** None

### UI-ATT-043: A Purchaseable part can be ordered on a purchase order

| Field | Value |
|---|---|
| **Summary** | A Purchaseable part can be ordered on a purchase order. |
| **Requirement** | `R-ATT-18` [part-index.md#L82](../../requirements/docs/part-index.md#L82), [part-index.md#L90](../../requirements/docs/part-index.md#L90) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Purchaseable on a purchase order) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, purchasing); Settings: None; Data: part `QA-<suffix> Purchase Part PO` (Purchaseable on) via `POST /api/part/` as `admin`; supplier `QA-<suffix> Supplier`, its supplier part for the part, and a Purchase Order for the supplier, via the API as `admin`; Pre-steps: log in through the login form; open the Purchase Order. |
| **Automation** | Partial: Purchase Orders module. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a line item. | Supplier part: `QA-<suffix>-SKU`<br>Quantity: `5` | The line item is added and listed in the order. |
| 2 | Open the part's *Purchase Orders* tab. | None | The Purchase Order is listed. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Purchase Order, supplier part and supplier company first.

**Notes:** None

### UI-ATT-044: A part that is not Purchaseable hides the Suppliers and Purchase Orders tabs

| Field | Value |
|---|---|
| **Summary** | A part that is not Purchaseable hides the Suppliers and Purchase Orders tabs. |
| **Requirement** | `R-ATT-18` [part-index.md#L82](../../requirements/docs/part-index.md#L82), [part-index.md#L90](../../requirements/docs/part-index.md#L90); `R-Detail_View-23` [part-views.md#L100-L102](../../requirements/docs/part-views.md#L100-L102); `R-Detail_View-24` [part-views.md#L108-L110](../../requirements/docs/part-views.md#L108-L110) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; Equivalence partitioning (invalid class: Purchaseable off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: part `QA-<suffix> Not Purchaseable` (Purchaseable off) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | Yes: tab visibility. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for the *Suppliers* and *Purchase Orders* tabs. | None | Neither tab is visible. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-045: A non-Purchaseable part on a purchase order

| Field | Value |
|---|---|
| **Summary** | A non-Purchaseable part on a purchase order. |
| **Requirement** | `R-ATT-18` [part-index.md#L82](../../requirements/docs/part-index.md#L82), [part-index.md#L90](../../requirements/docs/part-index.md#L90) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: Purchaseable off); Negative |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, purchasing); Settings: None; Data: part `QA-<suffix> Not Purchaseable PO` (Purchaseable off) via `POST /api/part/` as `admin`; a supplier and a Purchase Order, via the API as `admin`; Pre-steps: log in through the login form; open the Purchase Order. |
| **Automation** | No: outcome not known. |
| **Review** | Draft · Open question: Q-ATT-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Try to add a line item for the part. | Part: `QA-<suffix> Not Purchaseable PO` | Proposed, to confirm in Q-ATT-06: `QA-<suffix> Not Purchaseable PO` is not offered for the line item; only Purchaseable parts are ordered on purchase orders (R-ATT-18). Open: Q-ATT-06 (the error text if it is blocked on submit instead). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Purchase Order and supplier first.

**Notes:** None

**Duplicate check:** 55 · Review · matches: [UI-ATT-069](part-attributes.md) (55), [UI-ATT-047](part-attributes.md) (52)

**Duplicate judgement:** Keep · Different rule and starting state from UI-ATT-069 (active part with Purchaseable off under R-ATT-18 vs a Purchaseable part made inactive under R-ATT-29), and a different attribute and order type from UI-ATT-047 (Salable, sales order) · test-case-reviewer, 2026-10-13

### UI-ATT-046: A Salable part can be added to a sales order and shows the Allocated tab

| Field | Value |
|---|---|
| **Summary** | A Salable part can be added to a sales order and shows the Allocated tab. |
| **Requirement** | `R-ATT-19` [part-index.md#L98](../../requirements/docs/part-index.md#L98); `R-Detail_View-17` [part-views.md#L80](../../requirements/docs/part-views.md#L80) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Salable) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, sales); Settings: None; Data: part `QA-<suffix> Sale Part` (Salable on) via `POST /api/part/` as `admin`; a customer company and a Sales Order, via the API as `admin`; Pre-steps: log in through the login form; open the Sales Order. |
| **Automation** | Partial: Sales Orders module. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a line item for the part. | Part: `QA-<suffix> Sale Part`<br>Quantity: `1` | The line item is added and listed in the order. |
| 2 | Open the part's detail page. | None | The *Allocated* tab is visible. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Sales Order and the customer first.

**Notes:** None

### UI-ATT-047: A non-Salable part on a sales order

| Field | Value |
|---|---|
| **Summary** | A non-Salable part on a sales order. |
| **Requirement** | `R-ATT-19` [part-index.md#L98](../../requirements/docs/part-index.md#L98) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: Salable off); Negative |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, sales); Settings: None; Data: part `QA-<suffix> Not Salable` (Salable off, Component off) via `POST /api/part/` as `admin`; a customer company and a Sales Order, via the API as `admin`; Pre-steps: log in through the login form; open the Sales Order. |
| **Automation** | No: outcome not known. |
| **Review** | Draft · Open question: Q-ATT-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Try to add a line item for the part. | Part: `QA-<suffix> Not Salable` | Proposed, to confirm in Q-ATT-07: `QA-<suffix> Not Salable` is not offered for the line item; only Salable parts are added to sales orders (R-ATT-19). Open: Q-ATT-07 (the error text if it is blocked on submit instead). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Sales Order and the customer first.

**Notes:** None

**Duplicate check:** 52 · Review · matches: [UI-ATT-045](part-attributes.md) (52)

**Duplicate judgement:** Keep · Different rule (R-ATT-19, Salable off) and order type (sales order) from UI-ATT-045 (R-ATT-18, Purchaseable off, purchase order) · test-case-reviewer, 2026-10-13

### UI-ATT-048: A Consumable part can have stock items, tracked as normal

| Field | Value |
|---|---|
| **Summary** | A Consumable part can have stock items, tracked as normal. |
| **Requirement** | `R-ATT-20` [part-consumable.md#L40](../../requirements/docs/part-consumable.md#L40) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Consumable with stock) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, stock); Settings: None; Data: part `QA-<suffix> Consumable Stock` (Consumable on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the global *Stock* view. |
| **Automation** | Partial: form labels not known. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Create a stock item for the part. | Part: `QA-<suffix> Consumable Stock`<br>Quantity: `20` | The stock item is created. |
| 2 | Open the part's detail page and check the stock. | None | The part shows stock of `20`. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the stock item first.

**Notes:** None

### UI-ATT-049: A Consumable part can be added to a BOM like any other component

| Field | Value |
|---|---|
| **Summary** | A Consumable part can be added to a BOM like any other component. |
| **Requirement** | `R-ATT-21` [part-consumable.md#L44](../../requirements/docs/part-consumable.md#L44) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Consumable as BOM line) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Consumable Glue` (Consumable on, Component on) via `POST /api/part/` as `admin`; part `QA-<suffix> Assembly Glue` (Assembly on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the assembly's *BOM* tab. |
| **Automation** | Yes: BOM flow. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a BOM line. | Sub-component: `QA-<suffix> Consumable Glue`<br>Quantity: `1` | The BOM line is saved without error. |
| 2 | Check the BOM table. | None | `QA-<suffix> Consumable Glue` is listed. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the BOM line first.

**Notes:** None

### UI-ATT-050: A Consumable part is not allocated to a Build Order

| Field | Value |
|---|---|
| **Summary** | A Consumable part is not allocated to a Build Order. |
| **Requirement** | `R-ATT-22` [part-consumable.md#L48-L50](../../requirements/docs/part-consumable.md#L48-L50) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Consumable in a build) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, builds); Settings: None; Data: part `QA-<suffix> Consumable Screw` (Consumable on, Component on) via `POST /api/part/` as `admin` with stock `50`; part `QA-<suffix> Assembly Screw` (Assembly on) via `POST /api/part/` as `admin`; a BOM line and a Build Order, via the API as `admin`; Pre-steps: log in through the login form; open the Build Order. |
| **Automation** | Partial: Build Orders module. |
| **Review** | Draft · Open question: Q-ATT-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the allocation view of the Build Order and look for the Consumable part. | None | The Consumable part is not allocated to the Build Order. Open: Q-ATT-15 (whether it is listed as not requiring allocation or not listed; the docs only say it is not allocated). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Build Order first.

**Notes:** None

### UI-ATT-051: The stock of a Consumable part is not adjusted when a Build Order completes

| Field | Value |
|---|---|
| **Summary** | The stock of a Consumable part is not adjusted when a Build Order completes. |
| **Requirement** | `R-ATT-22` [part-consumable.md#L48-L50](../../requirements/docs/part-consumable.md#L48-L50) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | State transition (build in progress to complete) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, builds); Settings: None; Data: as the previous case, with a build output ready to be completed; Pre-steps: log in through the login form; open the Build Order. |
| **Automation** | Partial: Build Orders module. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Note the stock quantity of the Consumable part. | None | Stock is `50`. |
| 2 | Complete the Build Order. | None | The Build Order status is Complete. |
| 3 | Check the stock quantity of the Consumable part. | None | Stock is still `50`; the build did not adjust it. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Build Order first.

**Notes:** None

### UI-ATT-052: The part-level Consumable flag applies in every BOM that uses the part

| Field | Value |
|---|---|
| **Summary** | The part-level Consumable flag applies in every BOM that uses the part. |
| **Requirement** | `R-ATT-23` [part-consumable.md#L60-L63](../../requirements/docs/part-consumable.md#L60-L63) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (part-level flag) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, builds); Settings: None; Data: part `QA-<suffix> Consumable Everywhere` (Consumable on, Component on) via `POST /api/part/` as `admin`; two assemblies `QA-<suffix> Assembly X` and `QA-<suffix> Assembly Y` each with a BOM line for it (BOM line flag off) and a Build Order each; Pre-steps: log in through the login form; open the Build Order of Assembly X. |
| **Automation** | Partial: Build Orders module. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check allocation on the Build Order of Assembly X. | None | The part is not allocated to the build. |
| 2 | Check allocation on the Build Order of Assembly Y. | None | The part is not allocated to that build either. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Build Orders and BOM lines first.

**Notes:** None

**Duplicate check:** 55 · Review · matches: [UI-ATT-053](part-attributes.md) (55)

**Duplicate judgement:** Keep · Part-level flag clause of R-ATT-23 (flag on the part, not allocated in both builds) vs UI-ATT-053's BOM-line clause (flag on one line only, allocated as normal in the other build) · test-case-reviewer, 2026-10-13

### UI-ATT-053: The BOM-line Consumable flag affects only that BOM

| Field | Value |
|---|---|
| **Summary** | The BOM-line Consumable flag affects only that BOM. |
| **Requirement** | `R-ATT-23` [part-consumable.md#L60-L63](../../requirements/docs/part-consumable.md#L60-L63) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (BOM-line flag only) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, builds); Settings: None; Data: part `QA-<suffix> Fastener` (Consumable off, Component on) via `POST /api/part/` as `admin` with stock; two assemblies X and Y, each with a BOM line for it, flag *Consumable* on only on Assembly X's line, and a Build Order each; Pre-steps: log in through the login form; open the Build Order of Assembly X. |
| **Automation** | Partial: Build Orders module. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check allocation on the Build Order of Assembly X. | None | The part is treated as consumable: it is not allocated. |
| 2 | Check allocation on the Build Order of Assembly Y. | None | The part is required and can be allocated as a regular component. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Build Orders and BOM lines first.

**Notes:** None

**Duplicate check:** 55 · Review · matches: [UI-ATT-052](part-attributes.md) (55)

**Duplicate judgement:** Keep · BOM-line flag clause of R-ATT-23 (part flag off, one line flagged; Assembly Y allocates normally) vs UI-ATT-052's part-level clause, with a different expected outcome in the second build · test-case-reviewer, 2026-10-13

### UI-ATT-054: Setting both the part flag and the BOM-line flag has no extra effect

| Field | Value |
|---|---|
| **Summary** | Setting both the part flag and the BOM-line flag has no extra effect. |
| **Requirement** | `R-ATT-23` [part-consumable.md#L60-L63](../../requirements/docs/part-consumable.md#L60-L63) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Decision table (part flag on, line flag on) |
| **Priority** | P3 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, builds); Settings: None; Data: part `QA-<suffix> Consumable Both` (Consumable on, Component on) via `POST /api/part/` as `admin`; an assembly with a BOM line for it, flag *Consumable* on the line too, and a Build Order; Pre-steps: log in through the login form; open the Build Order. |
| **Automation** | Partial: Build Orders module. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check allocation on the Build Order. | None | The part is not allocated, the same as with only the part flag set; no error or extra behaviour. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Build Order and BOM line first.

**Notes:** None

### UI-ATT-055: A locked part cannot be deleted

| Field | Value |
|---|---|
| **Summary** | A locked part cannot be deleted. |
| **Requirement** | `R-ATT-24` [part-index.md#L108](../../requirements/docs/part-index.md#L108) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; State transition (unlocked to locked, delete blocked) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `admin` (settings and delete); Settings: `PART_ENABLE_LOCKING` = on [open: Q-ATT-02, default and setting label]; Data: part `QA-<suffix> Locked Delete` (Active off) via `POST /api/part/` as `admin`; locking enabled; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | No: lock control not known. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-14, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Lock the part [open: Q-ATT-01, how a part is locked and its label]. | None | The part is now locked. Open: Q-ATT-01 (the lock control and its label). |
| 2 | Try to delete the part. | None | The part is not deleted. Open: Q-ATT-14 (whether the delete action is hidden, disabled, or rejected with a message). |
| 3 | Reload the part's detail page. | None | The part still exists. |

**Postconditions and cleanup:** Cleanup as `admin`: unlock the part, then delete it.

**Notes:** The part must be inactive before it can be deleted; the case sets it inactive in the data so that only the lock blocks deletion.

### UI-ATT-056: A BOM item of a locked assembly cannot be created

| Field | Value |
|---|---|
| **Summary** | A BOM item of a locked assembly cannot be created. |
| **Requirement** | `R-ATT-25` [part-index.md#L109](../../requirements/docs/part-index.md#L109) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; Decision table (locking on, assembly locked, create) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_LOCKING` = on [open: Q-ATT-02, default and setting label]; Data: part `QA-<suffix> Locked Assembly` (Assembly on) via `POST /api/part/` as `admin`; part `QA-<suffix> Component Lock` (Component on) via `POST /api/part/` as `admin`; locking enabled; Pre-steps: log in through the login form; open the assembly's *BOM* tab. |
| **Automation** | No: lock control not known. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-14, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Lock the assembly [open: Q-ATT-01, how a part is locked and its label]. | None | The assembly is now locked. Open: Q-ATT-01 (the lock control and its label). |
| 2 | Try to create a BOM line. | Quantity: `3` | The BOM is not changed. Open: Q-ATT-14 (whether the control is hidden, disabled, or rejected with a message). |
| 3 | Reload the *BOM* tab. | None | The BOM is as before the attempt. |

**Postconditions and cleanup:** Cleanup as `admin`: unlock the assembly, delete BOM lines, make parts inactive and delete them.

**Notes:** None

**Duplicate check:** 88 · Duplicate · matches: [UI-ATT-057](part-attributes.md) (88), [UI-ATT-058](part-attributes.md) (79, test data differs)

**Duplicate judgement:** Keep · "Create" clause of R-ATT-25 on a BOM with no lines, vs UI-ATT-057 ("edit") and UI-ATT-058 ("delete"), which need an existing BOM line and block a different operation · test-case-reviewer, 2026-10-13

### UI-ATT-057: A BOM item of a locked assembly cannot be edited

| Field | Value |
|---|---|
| **Summary** | A BOM item of a locked assembly cannot be edited. |
| **Requirement** | `R-ATT-25` [part-index.md#L109](../../requirements/docs/part-index.md#L109) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; Decision table (locking on, assembly locked, edit) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_LOCKING` = on [open: Q-ATT-02, default and setting label]; Data: part `QA-<suffix> Locked Assembly` (Assembly on) via `POST /api/part/` as `admin`; part `QA-<suffix> Component Lock` (Component on) via `POST /api/part/` as `admin` with one BOM line for `QA-<suffix> Component Lock`; locking enabled; Pre-steps: log in through the login form; open the assembly's *BOM* tab. |
| **Automation** | No: lock control not known. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-14, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Lock the assembly [open: Q-ATT-01, how a part is locked and its label]. | None | The assembly is now locked. Open: Q-ATT-01 (the lock control and its label). |
| 2 | Try to edit the quantity of an existing BOM line. | Quantity: `3` | The BOM is not changed. Open: Q-ATT-14 (whether the control is hidden, disabled, or rejected with a message). |
| 3 | Reload the *BOM* tab. | None | The BOM is as before the attempt. |

**Postconditions and cleanup:** Cleanup as `admin`: unlock the assembly, delete BOM lines, make parts inactive and delete them.

**Notes:** None

**Duplicate check:** 88 · Duplicate · matches: [UI-ATT-056](part-attributes.md) (88), [UI-ATT-058](part-attributes.md) (80, test data differs)

**Duplicate judgement:** Keep · "Edit" clause of R-ATT-25 with an existing BOM line, vs UI-ATT-056 ("create", no line) and UI-ATT-058 ("delete"): each blocks a different operation the rule lists separately · test-case-reviewer, 2026-10-13

### UI-ATT-058: A BOM item of a locked assembly cannot be deleted

| Field | Value |
|---|---|
| **Summary** | A BOM item of a locked assembly cannot be deleted. |
| **Requirement** | `R-ATT-25` [part-index.md#L109](../../requirements/docs/part-index.md#L109) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; Decision table (locking on, assembly locked, delete) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_LOCKING` = on [open: Q-ATT-02, default and setting label]; Data: part `QA-<suffix> Locked Assembly` (Assembly on) via `POST /api/part/` as `admin`; part `QA-<suffix> Component Lock` (Component on) via `POST /api/part/` as `admin` with one BOM line for `QA-<suffix> Component Lock`; locking enabled; Pre-steps: log in through the login form; open the assembly's *BOM* tab. |
| **Automation** | No: lock control not known. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-14, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Lock the assembly [open: Q-ATT-01, how a part is locked and its label]. | None | The assembly is now locked. Open: Q-ATT-01 (the lock control and its label). |
| 2 | Try to delete an existing BOM line. | None | The BOM is not changed. Open: Q-ATT-14 (whether the control is hidden, disabled, or rejected with a message). |
| 3 | Reload the *BOM* tab. | None | The BOM is as before the attempt. |

**Postconditions and cleanup:** Cleanup as `admin`: unlock the assembly, delete BOM lines, make parts inactive and delete them.

**Notes:** None

**Duplicate check:** 80 · Review · matches: [UI-ATT-057](part-attributes.md) (80, test data differs), [UI-ATT-056](part-attributes.md) (79, test data differs)

**Duplicate judgement:** Keep · "Delete" clause of R-ATT-25, vs UI-ATT-057 ("edit") and UI-ATT-056 ("create"): each blocks a different operation the rule lists separately · test-case-reviewer, 2026-10-13

### UI-ATT-059: A parameter of a locked part cannot be created

| Field | Value |
|---|---|
| **Summary** | A parameter of a locked part cannot be created. |
| **Requirement** | `R-ATT-26` [part-index.md#L110](../../requirements/docs/part-index.md#L110) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; Decision table (locking on, part locked, create) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_LOCKING` = on [open: Q-ATT-02, default and setting label]; Data: part `QA-<suffix> Locked Params` (any attributes) via `POST /api/part/` as `admin`; parameter template `QA-<suffix> Param`; locking enabled; Pre-steps: log in through the login form; open the part's *Parameters* tab. |
| **Automation** | No: lock control not known. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-14, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Lock the part [open: Q-ATT-01, how a part is locked and its label]. | None | The part is now locked. Open: Q-ATT-01 (the lock control and its label). |
| 2 | Try to create a parameter. | Value: `7` | The parameters are not changed. Open: Q-ATT-14 (whether the control is hidden, disabled, or rejected with a message). |
| 3 | Reload the *Parameters* tab. | None | The parameters are as before the attempt. |

**Postconditions and cleanup:** Cleanup as `admin`: unlock the part, delete parameters and the template, make the part inactive and delete it.

**Notes:** None

**Duplicate check:** 87 · Duplicate · matches: [UI-ATT-060](part-attributes.md) (87), [UI-ATT-061](part-attributes.md) (78, test data differs)

**Duplicate judgement:** Keep · "Create" clause of R-ATT-26 with no existing parameter, vs UI-ATT-060 ("edit") and UI-ATT-061 ("delete"), which need an existing parameter and block a different operation · test-case-reviewer, 2026-10-13

### UI-ATT-060: A parameter of a locked part cannot be edited

| Field | Value |
|---|---|
| **Summary** | A parameter of a locked part cannot be edited. |
| **Requirement** | `R-ATT-26` [part-index.md#L110](../../requirements/docs/part-index.md#L110) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; Decision table (locking on, part locked, edit) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_LOCKING` = on [open: Q-ATT-02, default and setting label]; Data: part `QA-<suffix> Locked Params` (any attributes) via `POST /api/part/` as `admin` with parameter `QA-<suffix> Param` set to `5`; parameter template `QA-<suffix> Param`; locking enabled; Pre-steps: log in through the login form; open the part's *Parameters* tab. |
| **Automation** | No: lock control not known. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-14, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Lock the part [open: Q-ATT-01, how a part is locked and its label]. | None | The part is now locked. Open: Q-ATT-01 (the lock control and its label). |
| 2 | Try to edit the value of an existing parameter. | Value: `7` | The parameters are not changed. Open: Q-ATT-14 (whether the control is hidden, disabled, or rejected with a message). |
| 3 | Reload the *Parameters* tab. | None | The parameters are as before the attempt. |

**Postconditions and cleanup:** Cleanup as `admin`: unlock the part, delete parameters and the template, make the part inactive and delete it.

**Notes:** None

**Duplicate check:** 87 · Duplicate · matches: [UI-ATT-059](part-attributes.md) (87), [UI-ATT-061](part-attributes.md) (78, test data differs)

**Duplicate judgement:** Keep · "Edit" clause of R-ATT-26 with an existing parameter, vs UI-ATT-059 ("create", none existing) and UI-ATT-061 ("delete"): each blocks a different operation the rule lists separately · test-case-reviewer, 2026-10-13

### UI-ATT-061: A parameter of a locked part cannot be deleted

| Field | Value |
|---|---|
| **Summary** | A parameter of a locked part cannot be deleted. |
| **Requirement** | `R-ATT-26` [part-index.md#L110](../../requirements/docs/part-index.md#L110) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; Decision table (locking on, part locked, delete) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_LOCKING` = on [open: Q-ATT-02, default and setting label]; Data: part `QA-<suffix> Locked Params` (any attributes) via `POST /api/part/` as `admin` with parameter `QA-<suffix> Param` set to `5`; parameter template `QA-<suffix> Param`; locking enabled; Pre-steps: log in through the login form; open the part's *Parameters* tab. |
| **Automation** | No: lock control not known. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-14, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Lock the part [open: Q-ATT-01, how a part is locked and its label]. | None | The part is now locked. Open: Q-ATT-01 (the lock control and its label). |
| 2 | Try to delete an existing parameter. | None | The parameters are not changed. Open: Q-ATT-14 (whether the control is hidden, disabled, or rejected with a message). |
| 3 | Reload the *Parameters* tab. | None | The parameters are as before the attempt. |

**Postconditions and cleanup:** Cleanup as `admin`: unlock the part, delete parameters and the template, make the part inactive and delete it.

**Notes:** None

**Duplicate check:** 78 · Review · matches: [UI-ATT-059](part-attributes.md) (78, test data differs), [UI-ATT-060](part-attributes.md) (78, test data differs)

**Duplicate judgement:** Keep · "Delete" clause of R-ATT-26, vs UI-ATT-059 ("create") and UI-ATT-060 ("edit"): each blocks a different operation the rule lists separately · test-case-reviewer, 2026-10-13

### UI-ATT-062: With locking disabled, a locked part can be deleted

| Field | Value |
|---|---|
| **Summary** | With locking disabled, a locked part can be deleted. |
| **Requirement** | `R-ATT-27` [part-index.md#L112](../../requirements/docs/part-index.md#L112); `R-ATT-24` [part-index.md#L108](../../requirements/docs/part-index.md#L108) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Decision table (locking off, part locked, delete) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `admin` (settings and delete); Settings: `PART_ENABLE_LOCKING` = off [open: Q-ATT-02]; Data: part `QA-<suffix> Locked Setting Off Delete` (Active off, locked) via `POST /api/part/` as `admin` [open: Q-ATT-01, how the part is locked through the API]; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | No: setting label not known. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Turn the Part Locking setting off [open: Q-ATT-02, setting label and location]. | `PART_ENABLE_LOCKING` = off | The setting is saved. |
| 2 | Delete the part. | None | The part is deleted; the locked state is ignored. |

**Postconditions and cleanup:** Restore `PART_ENABLE_LOCKING` to its original value. The part is already deleted.

**Notes:** None

### UI-ATT-063: With locking disabled, a BOM item of a locked assembly can be created

| Field | Value |
|---|---|
| **Summary** | With locking disabled, a BOM item of a locked assembly can be created. |
| **Requirement** | `R-ATT-27` [part-index.md#L112](../../requirements/docs/part-index.md#L112); `R-ATT-25` [part-index.md#L109](../../requirements/docs/part-index.md#L109) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Decision table (locking off, assembly locked, create BOM item) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `admin` (settings and parts); Settings: `PART_ENABLE_LOCKING` = off [open: Q-ATT-02]; Data: part `QA-<suffix> Locked Off Assembly` (Assembly on, locked) via `POST /api/part/` as `admin`; part `QA-<suffix> Component Off` (Component on) via `POST /api/part/` as `admin` [open: Q-ATT-01, how the assembly is locked]; Pre-steps: log in through the login form; open the assembly's *BOM* tab. |
| **Automation** | No: setting label not known. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Turn the Part Locking setting off [open: Q-ATT-02, setting label and location]. | `PART_ENABLE_LOCKING` = off | The setting is saved. |
| 2 | Add a BOM line. | Sub-component: `QA-<suffix> Component Off`<br>Quantity: `1` | The BOM line is saved; the locked state is ignored. |

**Postconditions and cleanup:** Restore `PART_ENABLE_LOCKING`. Delete the BOM line, make parts inactive and delete them.

**Notes:** None

**Duplicate check:** 50 · Review · matches: [UI-ATT-064](part-attributes.md) (50)

**Duplicate judgement:** Keep · Locking-off override of the BOM restriction (R-ATT-25) vs UI-ATT-064's override of the parameter restriction (R-ATT-26): different rule and record type · test-case-reviewer, 2026-10-13

### UI-ATT-064: With locking disabled, a parameter of a locked part can be created

| Field | Value |
|---|---|
| **Summary** | With locking disabled, a parameter of a locked part can be created. |
| **Requirement** | `R-ATT-27` [part-index.md#L112](../../requirements/docs/part-index.md#L112); `R-ATT-26` [part-index.md#L110](../../requirements/docs/part-index.md#L110) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Decision table (locking off, part locked, create parameter) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `admin` (settings and parts); Settings: `PART_ENABLE_LOCKING` = off [open: Q-ATT-02]; Data: part `QA-<suffix> Locked Off Params` (any attributes, locked) via `POST /api/part/` as `admin`; parameter template `QA-<suffix> Param` [open: Q-ATT-01, how the part is locked]; Pre-steps: log in through the login form; open the part's *Parameters* tab. |
| **Automation** | No: setting label not known. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Turn the Part Locking setting off [open: Q-ATT-02, setting label and location]. | `PART_ENABLE_LOCKING` = off | The setting is saved. |
| 2 | Add a parameter. | Template: `QA-<suffix> Param`<br>Value: `5` | The parameter is saved; the locked state is ignored. |

**Postconditions and cleanup:** Restore `PART_ENABLE_LOCKING`. Delete the parameter and template; make the part inactive and delete it.

**Notes:** None

**Duplicate check:** 50 · Review · matches: [UI-ATT-063](part-attributes.md) (50)

**Duplicate judgement:** Keep · Locking-off override of the parameter restriction (R-ATT-26) vs UI-ATT-063's override of the BOM restriction (R-ATT-25): different rule and record type · test-case-reviewer, 2026-10-13

### UI-ATT-065: After a locked part is unlocked, its BOM can be edited again

| Field | Value |
|---|---|
| **Summary** | After a locked part is unlocked, its BOM can be edited again. |
| **Requirement** | `R-ATT-25` [part-index.md#L109](../../requirements/docs/part-index.md#L109); `R-ATT-24` [part-index.md#L108](../../requirements/docs/part-index.md#L108) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | State transition (locked to unlocked) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_LOCKING` = on [open: Q-ATT-02]; Data: part `QA-<suffix> Unlock Assembly` (Assembly on, locked) via `POST /api/part/` as `admin`; part `QA-<suffix> Component Unlock` (Component on) via `POST /api/part/` as `admin`; locking enabled [open: Q-ATT-01, how the assembly is locked]; Pre-steps: log in through the login form; open the assembly's *BOM* tab. |
| **Automation** | No: lock control not known. |
| **Review** | Draft · Open question: Q-ATT-01, Q-ATT-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Unlock the assembly [open: Q-ATT-01, how a part is unlocked and its label]. | None | The assembly is now unlocked. Open: Q-ATT-01 (the unlock control and its label). |
| 2 | Add a BOM line. | Sub-component: `QA-<suffix> Component Unlock`<br>Quantity: `1` | The BOM line is saved without error. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the BOM line, make parts inactive and delete them.

**Notes:** None

### UI-ATT-066: A newly created part is Active by default

| Field | Value |
|---|---|
| **Summary** | A newly created part is Active by default. |
| **Requirement** | `R-ATT-28` [part-index.md#L116](../../requirements/docs/part-index.md#L116) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: default) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: log in through the login form; open the *Parts* view. |
| **Automation** | Yes: default state. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Add Parts* dropdown and select *Create Part*. | None | The *Create Part* form opens. |
| 2 | Fill in the required field only and submit. | Name: `QA-<suffix> Active Default` | The browser goes to the new part's detail page. |
| 3 | Check the part's status. | None | The part is Active. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-067: A part made inactive remains in the database and can still be opened

| Field | Value |
|---|---|
| **Summary** | A part made inactive remains in the database and can still be opened. |
| **Requirement** | `R-ATT-29` [part-index.md#L116](../../requirements/docs/part-index.md#L116) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | State transition (active to inactive) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Inactive Keep` (Active on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the part's detail page. |
| **Automation** | Partial. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the edit form, untick *Active* and submit. | None | The form closes. |
| 2 | Reload the part's detail page. | None | The part's detail page still opens and shows the part as inactive; the part has not been removed. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-068: An inactive part added to a BOM

| Field | Value |
|---|---|
| **Summary** | An inactive part added to a BOM. |
| **Requirement** | `R-ATT-29` [part-index.md#L116](../../requirements/docs/part-index.md#L116) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; What-if business scenario (inactive part in a BOM) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Inactive Component` (Component on, Active off) via `POST /api/part/` as `admin`; part `QA-<suffix> Assembly Inactive` (Assembly on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the assembly's *BOM* tab. |
| **Automation** | No: blocked actions not listed. |
| **Review** | Draft · Open question: Q-ATT-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Start a new BOM line and look for the inactive part. | Sub-component: `QA-<suffix> Inactive Component` | Proposed, to confirm in Q-ATT-03: `QA-<suffix> Inactive Component` is not offered in the sub-component selector; an inactive part is not available for many actions (R-ATT-29). Open: Q-ATT-03 (the error text if it is blocked on submit instead). |
| 2 | Submit the line if possible. | Quantity: `1` | Proposed, to confirm in Q-ATT-03: no BOM line is saved for the inactive part. |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created.

**Notes:** None

### UI-ATT-069: An inactive part added to a purchase order

| Field | Value |
|---|---|
| **Summary** | An inactive part added to a purchase order. |
| **Requirement** | `R-ATT-29` [part-index.md#L116](../../requirements/docs/part-index.md#L116); `R-ATT-18` [part-index.md#L82](../../requirements/docs/part-index.md#L82), [part-index.md#L90](../../requirements/docs/part-index.md#L90) |
| **Area** | ATT |
| **Type** | Negative |
| **Technique** | Negative; What-if business scenario (inactive part on an order) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access, purchasing); Settings: None; Data: part `QA-<suffix> Inactive Purchase` (Purchaseable on, Active off) via `POST /api/part/` as `admin`; supplier, its supplier part and a Purchase Order, via the API as `admin`; Pre-steps: log in through the login form; open the Purchase Order. |
| **Automation** | No: blocked actions not listed. |
| **Review** | Draft · Open question: Q-ATT-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Try to add a line item for the inactive part. | Supplier part: `QA-<suffix>-SKU` | Proposed, to confirm in Q-ATT-03: the inactive part's supplier part is not offered for the line item (R-ATT-29). Open: Q-ATT-03 (the error text if it is blocked on submit instead). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the Purchase Order, supplier part and supplier first.

**Notes:** None

**Duplicate check:** 55 · Review · matches: [UI-ATT-045](part-attributes.md) (55)

**Duplicate judgement:** Keep · Different rule and starting state from UI-ATT-045 (Purchaseable part made inactive, R-ATT-29, vs an active part with Purchaseable off, R-ATT-18) · test-case-reviewer, 2026-10-13

### UI-ATT-070: An inactive part set back to Active becomes available again

| Field | Value |
|---|---|
| **Summary** | An inactive part set back to Active becomes available again. |
| **Requirement** | `R-ATT-29` [part-index.md#L116](../../requirements/docs/part-index.md#L116); `R-ATT-28` [part-index.md#L116](../../requirements/docs/part-index.md#L116) |
| **Area** | ATT |
| **Type** | Positive |
| **Technique** | State transition (inactive to active) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Reactivate` (Active off) via `POST /api/part/` as `admin`; part `QA-<suffix> Assembly Reactivate` (Assembly on) via `POST /api/part/` as `admin`; Pre-steps: log in through the login form; open the assembly's *BOM* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-ATT-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the inactive part's edit form, tick *Active* and submit. | None | The form closes and the part shows as Active. |
| 2 | Open the assembly's *BOM* tab and add the part. | Sub-component: `QA-<suffix> Reactivate`<br>Quantity: `1` | The BOM line is saved without error. Whether this was blocked before is not known: depends on open question Q-ATT-03 (list of blocked actions). |

**Postconditions and cleanup:** Cleanup as `admin`: set each part the case created inactive, then delete it; delete any other record the case created. Delete the BOM line first.

**Notes:** None
