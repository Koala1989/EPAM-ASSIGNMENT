# Part detail view header details and tab visibility: Detail_View test cases

Header toggle, creation details and the conditional tabs (Variants, Allocated, BOM, Build Orders, Used In, Suppliers, Purchase Orders). Tabs are checked with parts created through the API as `admin` with exact attribute combinations. `allaccess` is used where the tab may depend on build, sales or purchase order permissions (Q-Detail_View-19, Q-Detail_View-21).

---

### UI-Detail_View-080: The Show Part Details toggle displays the part details in the header panel

| Field | Value |
|---|---|
| **Summary** | A user viewing a part can display the part details in the header panel with the *Show Part Details* toggle. |
| **Requirement** | `R-Detail_View-01`. Source: [part-views.md#Part Details](../../requirements/docs/part-views.md#L24) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (details not displayed to displayed) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Header` (description `Header test part`, IPN `QA-<suffix>-IPN`), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Header`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the header panel of the part detail page. | None | The page shows the part header panel. Open: Q-Detail_View-15 (whether the details are shown or hidden by default). |
| 2 | Set the *Show Part Details* toggle so the details are displayed. | None | The part details are shown in the header panel (R-Detail_View-01). Open: Q-Detail_View-15 (toggle label in 1.5.6 and which fields are listed). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-081: Hiding the part details again with the toggle

| Field | Value |
|---|---|
| **Summary** | With the part details displayed, using the *Show Part Details* toggle again removes them from the header panel. |
| **Requirement** | `R-Detail_View-01`. Source: [part-views.md#Part Details](../../requirements/docs/part-views.md#L24) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (details displayed to not displayed) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Header`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Header`, set the *Show Part Details* toggle so the details are displayed. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Use the *Show Part Details* toggle again. | None | Proposed, to confirm in Q-Detail_View-15: the part details are no longer displayed in the header panel (the docs describe only displaying them). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-082: The details show the creation date and the user who created the part

| Field | Value |
|---|---|
| **Summary** | The part details show the creation date and the user who created the part. |
| **Requirement** | `R-Detail_View-02`. Source: [part-views.md#Part Details](../../requirements/docs/part-views.md#L42) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: part created by a known user on a known day) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Header` created today by `engineer` through the *Create Part* form (or `POST /api/part/` with the `engineer` account); Pre-steps: log in through the login form, open `QA-<suffix> Header`, display the part details with the *Show Part Details* toggle. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Find the creation information in the part details. | None | The details show today's date as the creation date and `engineer` as the user who created the part (R-Detail_View-02). Open: Q-Detail_View-15 (date format, label and position of the user name). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-083: The creator shown is the creating user, not the viewing user

| Field | Value |
|---|---|
| **Summary** | A part created by `admin` and opened by `engineer` shows `admin` as the creator. |
| **Requirement** | `R-Detail_View-02`. Source: [part-views.md#Part Details](../../requirements/docs/part-views.md#L42) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (creator differs from viewer), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Header` created via `POST /api/part/` as `admin`; Pre-steps: log in as `engineer` through the login form, open `QA-<suffix> Header`, display the part details. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-15 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Find the creation information in the part details. | None | The details show `admin`, the user who created the part, not `engineer` (R-Detail_View-02). Open: Q-Detail_View-15 (how the user is displayed: username or full name). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-084: A user with no permissions cannot open the part detail page

| Field | Value |
|---|---|
| **Summary** | `noaccess` cannot view a part's detail page, header or tabs. |
| **Requirement** | `R-Detail_View-03`. Source: [part-views.md#Part Tabs](../../requirements/docs/part-views.md#L48) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (viewing as the user who should be blocked) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess` (no permissions); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Header`, created via API as `admin`; Pre-steps: log in as `noaccess` through the login form. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the detail page of `QA-<suffix> Header` by its URL (`/web/part/<pk>/`). | None | Proposed, to confirm in Q-Detail_View-19: the part header and tabs are not shown, and the user sees a no-permission or error message instead. Open: Q-Detail_View-19 (message text). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-085: A part with every conditional attribute shows all the conditional tabs

| Field | Value |
|---|---|
| **Summary** | A part that is Template, Assembly, Component, Salable and Purchaseable shows the *Variants*, *Allocated*, *BOM*, *Used In*, *Suppliers* and *Purchase Orders* tabs, and each tab opens its panel. |
| **Requirement** | `R-Detail_View-03`, `R-Detail_View-08`, `R-Detail_View-17`, `R-Detail_View-19`, `R-Detail_View-21`, `R-Detail_View-23`, `R-Detail_View-24`. Source: [part-views.md#Part Tabs](../../requirements/docs/part-views.md#L48), [Variants](../../requirements/docs/part-views.md#L52), [Allocations](../../requirements/docs/part-views.md#L80), [BOM](../../requirements/docs/part-views.md#L84), [Used In](../../requirements/docs/part-views.md#L92), [Suppliers](../../requirements/docs/part-views.md#L100), [Purchase Orders](../../requirements/docs/part-views.md#L108) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (all conditions true) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> AllOn` with Template, Assembly, Component, Salable and Purchaseable on, created via `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> AllOn`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the tab list of the part page. | None | The tabs *Variants* (R-Detail_View-08), *Allocated* (R-Detail_View-17), *BOM* (R-Detail_View-19), *Used In* (R-Detail_View-21), *Suppliers* (R-Detail_View-23) and *Purchase Orders* (R-Detail_View-24) are all shown. |
| 2 | Open each of those tabs in turn. | None | Each tab opens its own panel (R-Detail_View-03). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** Whether the *Build Orders* tab shows for this part is covered by UI-Detail_View-104 to UI-Detail_View-106.

---

### UI-Detail_View-086: A part with every conditional attribute off shows none of the conditional tabs

| Field | Value |
|---|---|
| **Summary** | A part that is not Template, Assembly, Component, Salable or Purchaseable shows none of the *Variants*, *Allocated*, *BOM*, *Used In*, *Suppliers* and *Purchase Orders* tabs. |
| **Requirement** | `R-Detail_View-08`, `R-Detail_View-17`, `R-Detail_View-19`, `R-Detail_View-21`, `R-Detail_View-23`, `R-Detail_View-24`. Source: [part-views.md#Part Tabs](../../requirements/docs/part-views.md#L48), [Variants](../../requirements/docs/part-views.md#L52), [Allocations](../../requirements/docs/part-views.md#L80), [BOM](../../requirements/docs/part-views.md#L84), [Used In](../../requirements/docs/part-views.md#L92), [Suppliers](../../requirements/docs/part-views.md#L100), [Purchase Orders](../../requirements/docs/part-views.md#L108) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (all conditions false) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> AllOff` with Template, Assembly, Component, Salable and Purchaseable all off, created via `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> AllOff`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the tab list of the part page. | None | None of the tabs *Variants* (R-Detail_View-08), *Allocated* (R-Detail_View-17), *BOM* (R-Detail_View-19), *Used In* (R-Detail_View-21), *Suppliers* (R-Detail_View-23) or *Purchase Orders* (R-Detail_View-24) is shown. |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** The *Build Orders* tab is left out here: its visibility condition is not stated (UI-Detail_View-105).

---

### UI-Detail_View-087: The Variants tab is visible for a template part

| Field | Value |
|---|---|
| **Summary** | A template part shows the *Variants* tab. |
| **Requirement** | `R-Detail_View-08`. Source: [part-views.md#Variants](../../requirements/docs/part-views.md#L52) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Template on: tab shown) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Template` with Template on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Variants* tab is shown (R-Detail_View-08). |
| 2 | Open the *Variants* tab. | None | The *Variants* panel opens. |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-088: The Variants tab is hidden for a part that is not a template

| Field | Value |
|---|---|
| **Summary** | A part without the Template attribute does not show the *Variants* tab. |
| **Requirement** | `R-Detail_View-08`. Source: [part-views.md#Variants](../../requirements/docs/part-views.md#L52) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Template off: tab hidden) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> NoTemplate` with Template off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> NoTemplate`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Variants* tab is not shown: it is visible only if the part is a Template part (R-Detail_View-08). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-089: Turning the Template attribute off removes the Variants tab

| Field | Value |
|---|---|
| **Summary** | After the Template attribute of a template part is switched off, the part no longer shows the *Variants* tab. |
| **Requirement** | `R-Detail_View-08`. Source: [part-views.md#Variants](../../requirements/docs/part-views.md#L52) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | State transition (template to non-template) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Template` with Template on and no variants, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Partial: depends on the open control name. |
| **Review** | Draft · Open question: Q-Detail_View-20 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Switch the Template attribute off [open: Q-Detail_View-20, the control and label in 1.5.6]. | Template: off | The change is saved. Open: Q-Detail_View-20 (confirmation message, if any). |
| 2 | Check the tabs of the part (reload the page if the tab list has not updated). | None | The *Variants* tab is not shown: it is visible only if the part is a Template part (R-Detail_View-08). Open: Q-Detail_View-20 (whether the tab disappears without a reload). |

**Postconditions and cleanup:** the part is no longer a template. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** The docs describe the toggle in a *Details* tab (index doc issue 9, possibly outdated).

---

### UI-Detail_View-090: Turning the Template attribute on adds the Variants tab

| Field | Value |
|---|---|
| **Summary** | After the Template attribute of an ordinary part is switched on, the part shows the *Variants* tab. |
| **Requirement** | `R-Detail_View-08`. Source: [part-views.md#Variants](../../requirements/docs/part-views.md#L52) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (non-template to template) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> NoTemplate` with Template off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> NoTemplate`. |
| **Automation** | Partial: depends on the open control name. |
| **Review** | Draft · Open question: Q-Detail_View-20 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Switch the Template attribute on [open: Q-Detail_View-20, the control and label in 1.5.6]. | Template: on | The change is saved. Open: Q-Detail_View-20 (confirmation message, if any). |
| 2 | Check the tabs of the part (reload the page if the tab list has not updated). | None | The *Variants* tab is shown (R-Detail_View-08). Open: Q-Detail_View-20 (whether the tab appears without a reload). |

**Postconditions and cleanup:** the part is a template. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** The docs describe the toggle in a *Details* tab (index doc issue 9, possibly outdated).

---

### UI-Detail_View-091: The Allocated tab is visible for a Component part that is not Salable

| Field | Value |
|---|---|
| **Summary** | A part with Component on and Salable off shows the *Allocated* tab. |
| **Requirement** | `R-Detail_View-17`. Source: [part-views.md#Allocations](../../requirements/docs/part-views.md#L80) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Component on, Salable off) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> CompOnly` with Component on, Salable off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> CompOnly`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-24 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | Proposed, to confirm in Q-Detail_View-24: the *Allocated* tab is shown. R-Detail_View-17 says the tab is "only visible if" the part is a Component or Salable, a necessary condition; it does not say Component alone is enough. |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 81 · Review · matches: [UI-Detail_View-092](part-detail-header-and-tab-visibility.md) (81, test data differs), [UI-Detail_View-094](part-detail-header-and-tab-visibility.md) (63), [UI-Detail_View-107](part-detail-header-and-tab-visibility.md) (54)

**Duplicate judgement:** Keep · Different decision-table column of R-Detail_View-17 from 092 (Component on/Salable off vs Salable on/Component off) and 094 (both on), and a different user from 107 (allaccess vs reader) · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-092: The Allocated tab is visible for a Salable part that is not a Component

| Field | Value |
|---|---|
| **Summary** | A part with Salable on and Component off shows the *Allocated* tab. |
| **Requirement** | `R-Detail_View-17`. Source: [part-views.md#Allocations](../../requirements/docs/part-views.md#L80) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Component off, Salable on) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> SalableOnly` with Salable on, Component off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> SalableOnly`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-24 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | Proposed, to confirm in Q-Detail_View-24: the *Allocated* tab is shown. R-Detail_View-17 says the tab is "only visible if" the part is a Component or Salable, a necessary condition; it does not say Salable alone is enough. |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 81 · Review · matches: [UI-Detail_View-091](part-detail-header-and-tab-visibility.md) (81, test data differs), [UI-Detail_View-094](part-detail-header-and-tab-visibility.md) (60), [UI-Detail_View-107](part-detail-header-and-tab-visibility.md) (54)

**Duplicate judgement:** Keep · Salable-only is a distinct decision-table column of R-Detail_View-17 from 091 (Component only) and 094 (both), and 107 uses a different user (reader) on a Component part · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-093: The Allocated tab is hidden for a part that is neither Component nor Salable

| Field | Value |
|---|---|
| **Summary** | A part with Component off and Salable off does not show the *Allocated* tab. |
| **Requirement** | `R-Detail_View-17`. Source: [part-views.md#Allocations](../../requirements/docs/part-views.md#L80) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Component off, Salable off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Neither` with Component off, Salable off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Neither`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Allocated* tab is not shown: it is visible only if the part is a Component or Salable (R-Detail_View-17). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-094: The Allocated tab is visible for a part that is both Component and Salable

| Field | Value |
|---|---|
| **Summary** | A part with Component on and Salable on shows the *Allocated* tab once. |
| **Requirement** | `R-Detail_View-17`. Source: [part-views.md#Allocations](../../requirements/docs/part-views.md#L80) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Component on, Salable on), Error guessing (tab listed only once) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> CompSalable` with Component on, Salable on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> CompSalable`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-24 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | Proposed, to confirm in Q-Detail_View-24: the *Allocated* tab is shown, and appears only once in the tab list. R-Detail_View-17 says the tab is "only visible if" the part is a Component or Salable, a necessary condition; it does not say both together are enough. |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 63 · Review · matches: [UI-Detail_View-091](part-detail-header-and-tab-visibility.md) (63), [UI-Detail_View-092](part-detail-header-and-tab-visibility.md) (60), [UI-Detail_View-107](part-detail-header-and-tab-visibility.md) (51)

**Duplicate judgement:** Keep · Component-and-Salable is the fourth decision-table column of R-Detail_View-17, distinct from 091 and 092 (one attribute on), and 107 differs in user (reader) · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-095: The Allocated tab shows units allocated to a pending build order

| Field | Value |
|---|---|
| **Summary** | A component with stock allocated to a pending build order shows that allocation in its *Allocated* tab. |
| **Requirement** | `R-Detail_View-16`, `R-Detail_View-17`. Source: [part-views.md#Allocations](../../requirements/docs/part-views.md#L80) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: allocation to a pending build order) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Asm` (Assembly on), component `QA-<suffix> Comp` (Component on) with a stock item of 10 units, a BOM line of `QA-<suffix> Asm` using 1 `QA-<suffix> Comp`, and a build order for 5 `QA-<suffix> Asm` in status Pending with 2 units of `QA-<suffix> Comp` stock allocated, all created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Comp`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-18 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Allocated* tab. | None | The tab shows that 2 units of the part are allocated to the pending build order (R-Detail_View-16). Open: Q-Detail_View-18 (table columns and labels, whether a total is shown). |

**Postconditions and cleanup:** one pending build order with an allocation. Cleanup as `admin`: cancel and delete the build order, delete the stock item, set both parts inactive and delete them, then the category.

**Notes:** None.

**Duplicate check:** 75 · Review · matches: [UI-Detail_View-096](part-detail-header-and-tab-visibility.md) (75)

**Duplicate judgement:** Keep · Tests the build-order clause of R-Detail_View-16 (Component part, pending build order), while 096 tests the sales-order clause (Salable part, pending sales order) · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-096: The Allocated tab shows units allocated to a pending sales order

| Field | Value |
|---|---|
| **Summary** | A salable part with stock allocated to a pending sales order shows that allocation in its *Allocated* tab. |
| **Requirement** | `R-Detail_View-16`, `R-Detail_View-17`. Source: [part-views.md#Allocations](../../requirements/docs/part-views.md#L80) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: allocation to a pending sales order) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, customer `QA-<suffix> Customer`, salable part `QA-<suffix> Sale` (Salable on) with a stock item of 10 units, and a sales order for the customer in status Pending with a line of 3 `QA-<suffix> Sale` and 3 units of stock allocated, all created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Sale`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-18 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Allocated* tab. | None | The tab shows that 3 units of the part are allocated to the pending sales order (R-Detail_View-16). Open: Q-Detail_View-18 (table columns and labels, whether a total is shown). |

**Postconditions and cleanup:** one pending sales order with an allocation. Cleanup as `admin`: cancel and delete the sales order, delete the stock item, set the part inactive and delete it, then the customer and the category.

**Notes:** None.

**Duplicate check:** 75 · Review · matches: [UI-Detail_View-095](part-detail-header-and-tab-visibility.md) (75)

**Duplicate judgement:** Keep · Tests the sales-order clause of R-Detail_View-16 (Salable part, pending sales order), while 095 tests the build-order clause · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-097: The Allocated tab of a part with no allocations

| Field | Value |
|---|---|
| **Summary** | A component with stock but no allocations opens its *Allocated* tab without listing any allocation. |
| **Requirement** | `R-Detail_View-16`, `R-Detail_View-17`. Source: [part-views.md#Allocations](../../requirements/docs/part-views.md#L80) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (0 allocations) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> CompOnly` (Component on) with a stock item of 10 units and no build or sales order, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> CompOnly`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-18 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Allocated* tab. | None | Proposed, to confirm in Q-Detail_View-18: the tab opens and lists no allocation (empty table or an empty-state message). Open: Q-Detail_View-18 (empty-state text). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: delete the stock item, set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-098: A cancelled build order no longer counts in the Allocated tab

| Field | Value |
|---|---|
| **Summary** | After the build order holding an allocation is cancelled, the allocation no longer appears in the component's *Allocated* tab, because the tab covers pending orders. |
| **Requirement** | `R-Detail_View-16`. Source: [part-views.md#Allocations](../../requirements/docs/part-views.md#L80) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | State transition (build order Pending to Cancelled), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: as UI-Detail_View-095 (assembly, component with 10 units of stock, pending build order for 5 with 2 units allocated), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Comp`, confirm the *Allocated* tab shows the allocation, then cancel the build order through the build order page. |
| **Automation** | Yes: the build order is cancelled through the API as `admin` in the pre-step. |
| **Review** | Draft · Open question: Q-Detail_View-18 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Return to `QA-<suffix> Comp`, reload the page and open the *Allocated* tab. | None | Proposed, to confirm in Q-Detail_View-18: the cancelled build order's allocation is no longer listed (the docs name only pending orders, R-Detail_View-16). Open: Q-Detail_View-18 (which order statuses count as pending). |

**Postconditions and cleanup:** one cancelled build order. Cleanup as `admin`: delete the build order and the stock item, set both parts inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-099: The BOM tab is visible for an Assembly part

| Field | Value |
|---|---|
| **Summary** | A part with the Assembly attribute shows the *BOM* tab. |
| **Requirement** | `R-Detail_View-19`. Source: [part-views.md#Bill of Materials](../../requirements/docs/part-views.md#L84) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Assembly on: tab shown) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Asm` with Assembly on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Asm`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *BOM* tab is shown (R-Detail_View-19). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-100: The BOM tab is hidden for a part that is not an Assembly

| Field | Value |
|---|---|
| **Summary** | A part without the Assembly attribute does not show the *BOM* tab. |
| **Requirement** | `R-Detail_View-19`. Source: [part-views.md#Bill of Materials](../../requirements/docs/part-views.md#L84) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Assembly off: tab hidden) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> NoAsm` with Assembly off (Component on), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> NoAsm`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *BOM* tab is not shown: it is visible only if the part is an Assembly (R-Detail_View-19). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-101: The Build Orders tab lists the builds of a part with quantity, status and dates

| Field | Value |
|---|---|
| **Summary** | An assembly with one pending build order shows that build in its *Build Orders* tab with quantity, status and creation date. |
| **Requirement** | `R-Detail_View-20`. Source: [part-views.md#Build Orders](../../requirements/docs/part-views.md#L88) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: one pending build) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Asm` (Assembly on) and a build order for 5 `QA-<suffix> Asm` in status Pending, created today via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Asm`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-16, Q-Detail_View-17 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Build Orders* tab is shown. Open: Q-Detail_View-16 (visibility condition not stated). |
| 2 | Open the *Build Orders* tab. | None | The tab lists the build for this part with quantity 5, its status and today's creation date (R-Detail_View-20). Open: Q-Detail_View-17 (column labels, status wording, date format). |

**Postconditions and cleanup:** one pending build order. Cleanup as `admin`: cancel and delete the build order, set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-102: The Build Orders tab of an assembly with no builds

| Field | Value |
|---|---|
| **Summary** | An assembly that has no build order opens its *Build Orders* tab without listing any build. |
| **Requirement** | `R-Detail_View-20`. Source: [part-views.md#Build Orders](../../requirements/docs/part-views.md#L88) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (0 builds) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Asm` (Assembly on) with no build order, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Asm`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-16, Q-Detail_View-17 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Build Orders* tab. | None | Proposed, to confirm in Q-Detail_View-17: the tab opens and lists no build (empty table or an empty-state message). Open: Q-Detail_View-16 (whether the tab is shown for this part), Q-Detail_View-17 (empty-state text). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-103: The Build Orders tab lists a completed and a pending build with their details

| Field | Value |
|---|---|
| **Summary** | With one completed and one pending build order, the *Build Orders* tab lists both with quantity, status and dates, and the completed build shows its completion date. |
| **Requirement** | `R-Detail_View-20`. Source: [part-views.md#Build Orders](../../requirements/docs/part-views.md#L88) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (classes: completed build, pending build) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Asm` (Assembly on) with no BOM lines, a build order for 1 completed today (status Complete) and a second build order for 5 in status Pending, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Asm`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-16, Q-Detail_View-17 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Build Orders* tab and read both rows. | None | Both builds are listed with quantity, status, creation date and completion date (R-Detail_View-20). The completed build shows today's completion date. Open: Q-Detail_View-17 (what the pending build's completion date cell shows, and date format). |

**Postconditions and cleanup:** one completed and one pending build order. Cleanup as `admin`: cancel the pending build, delete both builds and the created stock output, set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-104: The Build Orders tab is visible for an Assembly part

| Field | Value |
|---|---|
| **Summary** | A part with the Assembly attribute shows the *Build Orders* tab. |
| **Requirement** | `R-Detail_View-20`. Source: [part-views.md#Build Orders](../../requirements/docs/part-views.md#L88) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Assembly on, Component off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> AsmOnly` with Assembly on, Component off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> AsmOnly`. |
| **Automation** | Partial: expected result depends on the open question. |
| **Review** | Draft · Open question: Q-Detail_View-16 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | Proposed, to confirm in Q-Detail_View-16: the *Build Orders* tab is shown for an Assembly part. The docs state no visibility condition (R-Detail_View-20). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 50 · Review · matches: [UI-Detail_View-108](part-detail-header-and-tab-visibility.md) (50)

**Duplicate judgement:** Keep · Same Assembly part but a different user: allaccess here vs reader in 108, which tests the permission side of Q-Detail_View-19 · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-105: The Build Orders tab for a part that is neither Assembly nor Component

| Field | Value |
|---|---|
| **Summary** | A part with Assembly off and Component off is opened to check whether the *Build Orders* tab is offered. |
| **Requirement** | `R-Detail_View-20`. Source: [part-views.md#Build Orders](../../requirements/docs/part-views.md#L88) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Assembly off, Component off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Neither` with Assembly off, Component off, Salable off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Neither`. |
| **Automation** | Partial: expected result depends on the open question. |
| **Review** | Draft · Open question: Q-Detail_View-16 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | Proposed, to confirm in Q-Detail_View-16: the *Build Orders* tab is not shown, because the part cannot be built. The docs state no visibility condition (R-Detail_View-20). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 79 · Review · matches: [UI-Detail_View-106](part-detail-header-and-tab-visibility.md) (79, test data differs)

**Duplicate judgement:** Keep · Component off here vs Component on in 106, a separate column while Q-Detail_View-16 leaves open whether Component alone shows the tab · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-106: The Build Orders tab for a Component part that is not an Assembly

| Field | Value |
|---|---|
| **Summary** | A part with Component on and Assembly off is opened to check whether the *Build Orders* tab is offered. |
| **Requirement** | `R-Detail_View-20`. Source: [part-views.md#Build Orders](../../requirements/docs/part-views.md#L88) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Assembly off, Component on) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> CompOnly` with Component on, Assembly off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> CompOnly`. |
| **Automation** | Partial: expected result depends on the open question. |
| **Review** | Draft · Open question: Q-Detail_View-16 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | Proposed, to confirm in Q-Detail_View-16: the *Build Orders* tab is not shown, because the part has no builds of its own. The docs state no visibility condition (R-Detail_View-20). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 79 · Review · matches: [UI-Detail_View-105](part-detail-header-and-tab-visibility.md) (79, test data differs)

**Duplicate judgement:** Keep · Component on here vs off in 105, the column that tells "Assembly only" from "Component too" in Q-Detail_View-16 · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-107: A view-only user sees the Allocated tab of a Component part

| Field | Value |
|---|---|
| **Summary** | `reader` opening a Component part sees the *Allocated* tab, because the tab condition is the part's attributes. |
| **Requirement** | `R-Detail_View-17`. Source: [part-views.md#Allocations](../../requirements/docs/part-views.md#L80) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (role reader x Component on) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> CompOnly` with Component on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> CompOnly`. |
| **Automation** | Partial: expected result depends on the open question. |
| **Review** | Draft · Open question: Q-Detail_View-19, Q-Detail_View-24 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | Proposed, to confirm in Q-Detail_View-24: the *Allocated* tab is shown. R-Detail_View-17 says the tab is "only visible if" the part is a Component or Salable, a necessary condition; it does not say Component alone is enough. Open: Q-Detail_View-19 (whether `reader` also needs build or sales order view permission to see it). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 54 · Review · matches: [UI-Detail_View-091](part-detail-header-and-tab-visibility.md) (54), [UI-Detail_View-092](part-detail-header-and-tab-visibility.md) (54), [UI-Detail_View-094](part-detail-header-and-tab-visibility.md) (51)

**Duplicate judgement:** Keep · Different user (view-only reader vs allaccess in 091, 092 and 094), which is the permission dimension Q-Detail_View-19 asks about · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-108: A view-only user sees the Build Orders tab of an Assembly part

| Field | Value |
|---|---|
| **Summary** | `reader` opening an Assembly part is checked for the *Build Orders* tab. |
| **Requirement** | `R-Detail_View-20`. Source: [part-views.md#Build Orders](../../requirements/docs/part-views.md#L88) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (role reader x Assembly on) |
| **Priority** | P3 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> AsmOnly` with Assembly on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> AsmOnly`. |
| **Automation** | Partial: expected result depends on the open questions. |
| **Review** | Draft · Open question: Q-Detail_View-16, Q-Detail_View-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | Proposed, to confirm in Q-Detail_View-19: the *Build Orders* tab is shown to `reader`. Open: Q-Detail_View-16 (visibility condition), Q-Detail_View-19 (whether build order view permission is needed). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 50 · Review · matches: [UI-Detail_View-104](part-detail-header-and-tab-visibility.md) (50)

**Duplicate judgement:** Keep · Different user (reader vs allaccess in 104) on the same Assembly part; it checks the build-order permission side of Q-Detail_View-19 · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-109: The Used In tab is visible for a Component part

| Field | Value |
|---|---|
| **Summary** | A part with the Component attribute shows the *Used In* tab. |
| **Requirement** | `R-Detail_View-21`. Source: [part-views.md#Used In](../../requirements/docs/part-views.md#L92) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Component on: tab shown) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> CompOnly` with Component on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> CompOnly`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Used In* tab is shown (R-Detail_View-21). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** The hidden case is UI-Detail_View-070.

---

### UI-Detail_View-110: The Suppliers tab is visible for a Purchaseable part

| Field | Value |
|---|---|
| **Summary** | A Purchaseable part shows the *Suppliers* tab to a user with purchase order view permission. |
| **Requirement** | `R-Detail_View-23`. Source: [part-views.md#Suppliers](../../requirements/docs/part-views.md#L100) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Purchaseable on: tab shown) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Buy` with Purchaseable on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Buy`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Suppliers* tab is shown (R-Detail_View-23). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-111: The Suppliers tab is hidden for a part that is not Purchaseable

| Field | Value |
|---|---|
| **Summary** | A part with Purchaseable off does not show the *Suppliers* tab. |
| **Requirement** | `R-Detail_View-23`. Source: [part-views.md#Suppliers](../../requirements/docs/part-views.md#L100) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Purchaseable off: tab hidden) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> NoBuy` with Purchaseable off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> NoBuy`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Suppliers* tab is not shown: it is visible only if the part is Purchaseable (R-Detail_View-23). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 52 · Review · matches: [UI-Detail_View-112](part-detail-header-and-tab-visibility.md) (52)

**Duplicate judgement:** Keep · Purchaseable off with allaccess (attribute condition) vs Purchaseable on with engineer in 112 (permission condition); different starting state and user · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-112: The Suppliers tab is hidden from a user without purchase order view permission

| Field | Value |
|---|---|
| **Summary** | `engineer` opening a Purchaseable part does not see the *Suppliers* tab, although the docs give only the Purchaseable condition. |
| **Requirement** | `R-Detail_View-23`. Source: [part-views.md#Suppliers](../../requirements/docs/part-views.md#L100). Index doc issue 15. |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Purchaseable on x role without purchase order view), Negative |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `engineer` (part management, no purchase order view); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Buy` with Purchaseable on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Buy`. |
| **Automation** | Partial: expected result depends on the open question. |
| **Review** | Draft · Open question: Q-Detail_View-21 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | Proposed, to confirm in Q-Detail_View-21: the *Suppliers* tab is not shown to `engineer`, as observed in 1.5.6 (index doc issue 15). The docs state only the Purchaseable condition (R-Detail_View-23). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** Confirmed in the app in the MCP run of 2026-10-11 (index doc issue 15). Not a finding until the architect answers Q-Detail_View-21.

**Duplicate check:** 52 · Review · matches: [UI-Detail_View-111](part-detail-header-and-tab-visibility.md) (52)

**Duplicate judgement:** Keep · Purchaseable on with engineer, who lacks purchase-order view (permission condition), vs Purchaseable off with allaccess in 111 · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-113: The Purchase Orders tab is visible for a Purchaseable part

| Field | Value |
|---|---|
| **Summary** | A Purchaseable part shows the *Purchase Orders* tab. |
| **Requirement** | `R-Detail_View-24`. Source: [part-views.md#Purchase Orders](../../requirements/docs/part-views.md#L108) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Purchaseable on: tab shown) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Buy` with Purchaseable on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Buy`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Purchase Orders* tab is shown (R-Detail_View-24). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-114: The Purchase Orders tab is hidden for a part that is not Purchaseable

| Field | Value |
|---|---|
| **Summary** | A part with Purchaseable off does not show the *Purchase Orders* tab. |
| **Requirement** | `R-Detail_View-24`. Source: [part-views.md#Purchase Orders](../../requirements/docs/part-views.md#L108) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Purchaseable off: tab hidden) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> NoBuy` with Purchaseable off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> NoBuy`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Purchase Orders* tab is not shown: it is shown only if the part is Purchaseable (R-Detail_View-24). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-115: The Return Orders tab is visible for a Salable part when the return order feature is enabled

| Field | Value |
|---|---|
| **Summary** | A Salable part shows the *Return Orders* tab when the return order feature is enabled. |
| **Requirement** | `R-Detail_View-26`. Source: [part-views.md#Return Orders](../../requirements/docs/part-views.md#L118) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Salable on, feature enabled: tab shown) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `allaccess` (full access); Settings: return order feature = enabled [open: Q-Detail_View-22, setting name and default]; Data: category `QA-<suffix> Category`, part `QA-<suffix> RetSalable` with Salable on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> RetSalable` |
| **Automation** | Partial: the setting step cannot be automated until Q-Detail_View-22 names the setting. |
| **Review** | Draft · Open question: Q-Detail_View-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Return Orders* tab is shown (R-Detail_View-26). Open: Q-Detail_View-22 (setting that enables the feature). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-116: The Return Orders tab is hidden for a part that is not Salable

| Field | Value |
|---|---|
| **Summary** | A part with Salable off does not show the *Return Orders* tab, even with the return order feature enabled. |
| **Requirement** | `R-Detail_View-26`. Source: [part-views.md#Return Orders](../../requirements/docs/part-views.md#L118) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Salable off, feature enabled: tab hidden) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `allaccess` (full access); Settings: return order feature = enabled [open: Q-Detail_View-22, setting name and default]; Data: category `QA-<suffix> Category`, part `QA-<suffix> RetNotSalable` with Salable off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> RetNotSalable` |
| **Automation** | Partial: the setting step cannot be automated until Q-Detail_View-22 names the setting. |
| **Review** | Draft · Open question: Q-Detail_View-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Return Orders* tab is not shown: it is visible only if the part is Salable (R-Detail_View-26). Open: Q-Detail_View-22 (setting that enables the feature). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 71 · Review · matches: [UI-Detail_View-118](part-detail-header-and-tab-visibility.md) (71)

**Duplicate judgement:** Keep · Settings differ from UI-Detail_View-118 (return order feature enabled here, disabled there), a different decision-table column of R-Detail_View-26 · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-117: The Return Orders tab is hidden for a Salable part when the return order feature is disabled

| Field | Value |
|---|---|
| **Summary** | A Salable part does not show the *Return Orders* tab when the return order feature is disabled. |
| **Requirement** | `R-Detail_View-26`. Source: [part-views.md#Return Orders](../../requirements/docs/part-views.md#L118) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Salable on, feature disabled: tab hidden) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `allaccess` (full access); Settings: return order feature = disabled [open: Q-Detail_View-22, setting name and default]; Data: category `QA-<suffix> Category`, part `QA-<suffix> RetSalableOff` with Salable on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> RetSalableOff` after the setting step |
| **Automation** | Partial: the setting step cannot be automated until Q-Detail_View-22 names the setting. |
| **Review** | Draft · Open question: Q-Detail_View-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | As `admin`, disable the return order feature. | [open: Q-Detail_View-22, setting name and where it is changed] | The feature is disabled. Open: Q-Detail_View-22 (setting name and location). |
| 2 | As `allaccess`, check the tabs of the part. | None | The *Return Orders* tab is not shown: it requires the return order feature to be enabled (R-Detail_View-26). Open: Q-Detail_View-22 (setting). |

**Postconditions and cleanup:** the feature setting was changed. Restore it to its original value as `admin`. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 52 · Review · matches: [UI-Detail_View-118](part-detail-header-and-tab-visibility.md) (52), [UI-Detail_View-121](part-detail-header-and-tab-visibility.md) (51)

**Duplicate judgement:** Keep · Starting state differs from UI-Detail_View-118 (Salable on vs off), and UI-Detail_View-121 tests another rule and tab (R-Detail_View-27, Transfer Orders) · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-118: The Return Orders tab is hidden when the part is not Salable and the feature is disabled

| Field | Value |
|---|---|
| **Summary** | A part with Salable off and the return order feature disabled does not show the *Return Orders* tab. |
| **Requirement** | `R-Detail_View-26`. Source: [part-views.md#Return Orders](../../requirements/docs/part-views.md#L118) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Salable off, feature disabled: tab hidden) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `allaccess` (full access); Settings: return order feature = disabled [open: Q-Detail_View-22, setting name and default]; Data: category `QA-<suffix> Category`, part `QA-<suffix> RetNeither` with Salable off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> RetNeither` |
| **Automation** | Partial: the setting step cannot be automated until Q-Detail_View-22 names the setting. |
| **Review** | Draft · Open question: Q-Detail_View-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Return Orders* tab is not shown (R-Detail_View-26). Open: Q-Detail_View-22 (setting). |

**Postconditions and cleanup:** no records changed. Restore the setting as `admin` if it was changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 71 · Review · matches: [UI-Detail_View-116](part-detail-header-and-tab-visibility.md) (71), [UI-Detail_View-117](part-detail-header-and-tab-visibility.md) (52)

**Duplicate judgement:** Keep · Settings differ from UI-Detail_View-116 (feature disabled vs enabled) and starting state differs from UI-Detail_View-117 (Salable off vs on): the both-false column of R-Detail_View-26 · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-119: The Transfer Orders tab is shown for a non-Virtual part when the transfer order feature is enabled

| Field | Value |
|---|---|
| **Summary** | A part with Virtual off shows the *Transfer Orders* tab when the transfer order feature is enabled. |
| **Requirement** | `R-Detail_View-27`. Source: [part-views.md#Transfer Orders](../../requirements/docs/part-views.md#L122) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Virtual off, feature enabled: tab not hidden) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `allaccess` (full access); Settings: transfer order feature = enabled [open: Q-Detail_View-22, setting name and default]; Data: category `QA-<suffix> Category`, part `QA-<suffix> TrNotVirtual` with Virtual off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> TrNotVirtual` |
| **Automation** | Partial: the setting step cannot be automated until Q-Detail_View-22 names the setting. |
| **Review** | Draft · Open question: Q-Detail_View-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | Proposed, to confirm in Q-Detail_View-22: the *Transfer Orders* tab is shown. The docs state only when the tab is hidden (R-Detail_View-27). Open: Q-Detail_View-22 (setting). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-120: The Transfer Orders tab is hidden for a Virtual part

| Field | Value |
|---|---|
| **Summary** | A part with Virtual on does not show the *Transfer Orders* tab, even with the transfer order feature enabled. |
| **Requirement** | `R-Detail_View-27`. Source: [part-views.md#Transfer Orders](../../requirements/docs/part-views.md#L122) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Virtual on, feature enabled: tab hidden) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `allaccess` (full access); Settings: transfer order feature = enabled [open: Q-Detail_View-22, setting name and default]; Data: category `QA-<suffix> Category`, part `QA-<suffix> TrVirtual` with Virtual on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> TrVirtual` |
| **Automation** | Partial: the setting step cannot be automated until Q-Detail_View-22 names the setting. |
| **Review** | Draft · Open question: Q-Detail_View-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Transfer Orders* tab is not shown: it is hidden if the part is Virtual (R-Detail_View-27). Open: Q-Detail_View-22 (setting). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 72 · Review · matches: [UI-Detail_View-122](part-detail-header-and-tab-visibility.md) (72), [UI-Detail_View-121](part-detail-header-and-tab-visibility.md) (51)

**Duplicate judgement:** Keep · Settings differ from UI-Detail_View-122 (transfer order feature enabled vs disabled) and starting state differs from UI-Detail_View-121 (Virtual on vs off) · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-121: The Transfer Orders tab is hidden for a non-Virtual part when the transfer order feature is disabled

| Field | Value |
|---|---|
| **Summary** | A part with Virtual off does not show the *Transfer Orders* tab when the transfer order feature is disabled. |
| **Requirement** | `R-Detail_View-27`. Source: [part-views.md#Transfer Orders](../../requirements/docs/part-views.md#L122) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Virtual off, feature disabled: tab hidden) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `allaccess` (full access); Settings: transfer order feature = disabled [open: Q-Detail_View-22, setting name and default]; Data: category `QA-<suffix> Category`, part `QA-<suffix> TrFeatureOff` with Virtual off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> TrFeatureOff` after the setting step |
| **Automation** | Partial: the setting step cannot be automated until Q-Detail_View-22 names the setting. |
| **Review** | Draft · Open question: Q-Detail_View-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | As `admin`, disable the transfer order feature. | [open: Q-Detail_View-22, setting name and where it is changed] | The feature is disabled. Open: Q-Detail_View-22 (setting name and location). |
| 2 | As `allaccess`, check the tabs of the part. | None | The *Transfer Orders* tab is not shown: it is hidden if the transfer order feature is not enabled (R-Detail_View-27). Open: Q-Detail_View-22 (setting). |

**Postconditions and cleanup:** the feature setting was changed. Restore it to its original value as `admin`. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 51 · Review · matches: [UI-Detail_View-117](part-detail-header-and-tab-visibility.md) (51), [UI-Detail_View-120](part-detail-header-and-tab-visibility.md) (51), [UI-Detail_View-122](part-detail-header-and-tab-visibility.md) (51)

**Duplicate judgement:** Keep · UI-Detail_View-117 tests another rule and tab (R-Detail_View-26), UI-Detail_View-120 has the feature enabled, and UI-Detail_View-122 has Virtual on; this case is the Virtual-off, feature-disabled column · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-122: The Transfer Orders tab is hidden for a Virtual part when the feature is also disabled

| Field | Value |
|---|---|
| **Summary** | A Virtual part with the transfer order feature disabled does not show the *Transfer Orders* tab. |
| **Requirement** | `R-Detail_View-27`. Source: [part-views.md#Transfer Orders](../../requirements/docs/part-views.md#L122) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Virtual on, feature disabled: tab hidden) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `allaccess` (full access); Settings: transfer order feature = disabled [open: Q-Detail_View-22, setting name and default]; Data: category `QA-<suffix> Category`, part `QA-<suffix> TrBoth` with Virtual on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> TrBoth` |
| **Automation** | Partial: the setting step cannot be automated until Q-Detail_View-22 names the setting. |
| **Review** | Draft · Open question: Q-Detail_View-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Transfer Orders* tab is not shown (R-Detail_View-27). Open: Q-Detail_View-22 (setting). |

**Postconditions and cleanup:** no records changed. Restore the setting as `admin` if it was changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

**Duplicate check:** 72 · Review · matches: [UI-Detail_View-120](part-detail-header-and-tab-visibility.md) (72), [UI-Detail_View-121](part-detail-header-and-tab-visibility.md) (51)

**Duplicate judgement:** Keep · Settings differ from UI-Detail_View-120 (feature disabled vs enabled) and starting state differs from UI-Detail_View-121 (Virtual on vs off): the both-conditions column of R-Detail_View-27 · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-123: The Test Results tab is visible for a Testable part

| Field | Value |
|---|---|
| **Summary** | A part with Testable on shows the *Test Results* tab. |
| **Requirement** | `R-Detail_View-30`. Source: [part-views.md#Test Results](../../requirements/docs/part-views.md#L134) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Testable on: tab shown) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Testable` with Testable on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Testable` |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Test Results* tab is shown (R-Detail_View-30). |
| 2 | Open the *Test Results* tab. | None | The tab opens and shows one table of test results for the part's stock items (R-Detail_View-30). The part has no stock, so the table has no rows; the empty-state wording is not stated in the docs and is not asserted. |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-124: The Test Results tab is hidden for a part that is not Testable

| Field | Value |
|---|---|
| **Summary** | A part with Testable off does not show the *Test Results* tab. |
| **Requirement** | `R-Detail_View-30`. Source: [part-views.md#Test Results](../../requirements/docs/part-views.md#L134) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Testable off: tab hidden) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> NotTestable` with Testable off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> NotTestable` |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Test Results* tab is not shown: it is visible only if the part is Testable (R-Detail_View-30). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-125: Turning the Testable attribute off removes the Test Results tab

| Field | Value |
|---|---|
| **Summary** | After Testable is switched off on a part that showed the *Test Results* tab, the tab is no longer shown. |
| **Requirement** | `R-Detail_View-30`. Source: [part-views.md#Test Results](../../requirements/docs/part-views.md#L134) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | State transition (Testable on to off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> TestableOff` with Testable on, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> TestableOff`; confirm the *Test Results* tab is shown |
| **Automation** | Partial: the edit step needs Q-Detail_View-23 answered. |
| **Review** | Draft · Open question: Q-Detail_View-23 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part's edit form and clear the Testable attribute. | Testable: off [open: Q-Detail_View-23, edit control and field label in 1.5.6] | The form accepts the change. Open: Q-Detail_View-23 (control and label). |
| 2 | Save the form and check the tabs of the part. | None | The *Test Results* tab is not shown: it is visible only if the part is Testable (R-Detail_View-30). Open: Q-Detail_View-23 (whether the tab disappears without a reload). |

**Postconditions and cleanup:** the part is no longer Testable. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-126: Turning the Testable attribute on adds the Test Results tab

| Field | Value |
|---|---|
| **Summary** | After Testable is switched on for a part that did not show the *Test Results* tab, the tab is shown. |
| **Requirement** | `R-Detail_View-30`. Source: [part-views.md#Test Results](../../requirements/docs/part-views.md#L134) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (Testable off to on) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> TestableOn` with Testable off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> TestableOn`; confirm the *Test Results* tab is not shown |
| **Automation** | Partial: the edit step needs Q-Detail_View-23 answered. |
| **Review** | Draft · Open question: Q-Detail_View-23 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part's edit form and set the Testable attribute. | Testable: on [open: Q-Detail_View-23, edit control and field label in 1.5.6] | The form accepts the change. Open: Q-Detail_View-23 (control and label). |
| 2 | Save the form and check the tabs of the part. | None | The *Test Results* tab is shown (R-Detail_View-30). Open: Q-Detail_View-23 (whether the tab appears without a reload). |

**Postconditions and cleanup:** the part is Testable. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-127: A view-only user sees the Test Results tab of a Testable part

| Field | Value |
|---|---|
| **Summary** | A user with view-only access (`reader`) sees the *Test Results* tab of a Testable part. |
| **Requirement** | `R-Detail_View-30`. Source: [part-views.md#Test Results](../../requirements/docs/part-views.md#L134) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Negative (view-only user) |
| **Priority** | P3 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> TestableRead` with Testable on, created via API as `admin`; Pre-steps: log in through the login form as `reader`, open `QA-<suffix> TestableRead` |
| **Automation** | Partial: the edit step needs Q-Detail_View-23 answered. |
| **Review** | Draft · Open question: Q-Detail_View-23 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | Proposed, to confirm in Q-Detail_View-23: the *Test Results* tab is shown, because the docs make visibility depend only on the part being Testable (R-Detail_View-30). Open: Q-Detail_View-23 (whether the tab needs stock or test view permission). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---
