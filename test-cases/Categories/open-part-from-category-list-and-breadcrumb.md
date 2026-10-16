# Open part from category list and breadcrumb: Categories test cases

### UI-Categories-001: Open a part by clicking its name in the category part list

| Field | Value |
|---|---|
| **Summary** | Clicking a part name in a category's part list opens that part's detail view. |
| **Requirement** | `R-Categories-06`. Source: [part-index.md#L46](../../requirements/docs/part-index.md#L46) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: part directly in the opened category) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Parent` and part `QA-<suffix> Part A` in it, created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes: core navigation flow. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the category from the *Parts* view. | Category: `QA-<suffix> Parent` | The category page opens and its part list shows `QA-<suffix> Part A`. |
| 2 | Click the part name. | `QA-<suffix> Part A` | A preview panel opens with the part's name, description and category (F-13). |
| 3 | Click the part name at the top of the preview panel. | None | The Part Detail view of `QA-<suffix> Part A` opens (`/web/part/<pk>/`). |
| 4 | Check the detail page header. | None | The header shows the name `QA-<suffix> Part A`. |

**Postconditions and cleanup:** none changed. As `admin`: set the part inactive, delete it, then delete the category.

**Notes:** Steps updated after the MCP run of 2026-10-14: a click in the list opens a preview panel first (F-13).

### UI-Categories-002: Open a part from a parent category's list when the part is in a sub-category

| Field | Value |
|---|---|
| **Summary** | A part that belongs to a sub-category appears in the parent category's part list and can be opened from there. |
| **Requirement** | `R-Categories-02`, `R-Categories-06`. Source: [part-index.md#L31](../../requirements/docs/part-index.md#L31), [part-index.md#L46](../../requirements/docs/part-index.md#L46) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: part in a sub-category), State transition (parent list, then detail view) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Parent`, sub-category `QA-<suffix> Child` under it, part `QA-<suffix> Part B` in `QA-<suffix> Child` only, created via the API as `admin`; Pre-steps: log in, open the *Parts* view. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parent category. | `QA-<suffix> Parent` | The sub-category list shows `QA-<suffix> Child`. The part list shows `QA-<suffix> Part B`, although the part is only in the child. |
| 2 | Click the part name. | `QA-<suffix> Part B` | A preview panel opens with the part's name, description and category (F-13). |
| 3 | Click the part name at the top of the preview panel. | None | The Part Detail view of `QA-<suffix> Part B` opens. |

**Postconditions and cleanup:** as `admin`: set the part inactive, delete it, then delete the child and parent categories.

**Notes:** Steps updated after the MCP run of 2026-10-14: a click in the list opens a preview panel first (F-13).

### UI-Categories-003: A view-only user can open a part from the category list

| Field | Value |
|---|---|
| **Summary** | A user with view-only access can click a part name in the category part list and open the detail view. |
| **Requirement** | `R-Categories-06`. Source: [part-index.md#L46](../../requirements/docs/part-index.md#L46) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: read-only user) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view-only); Settings: None; Data: category `QA-<suffix> Parent` and part `QA-<suffix> Part A` in it, created via the API as `admin`; Pre-steps: log in, open the *Parts* view. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-Categories-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the category. | `QA-<suffix> Parent` | The part list shows `QA-<suffix> Part A`. |
| 2 | Click the part name. | `QA-<suffix> Part A` | A preview panel opens with the part's name, description and category (F-13). |
| 3 | Click the part name at the top of the preview panel. | None | The Part Detail view of `QA-<suffix> Part A` opens. Open: Q-Categories-03 (which controls a view-only user sees; observed on 1.5.6: no *Part actions* menu (Duplicate, Edit, Delete) and a disabled lock icon). |

**Postconditions and cleanup:** as `admin`: set the part inactive, delete it, then delete the category.

**Notes:** Steps updated after the MCP run of 2026-10-14: a click in the list opens a preview panel first (F-13). The docs state no permission condition for the detail view; the controls check waits on Q-Categories-03. For comparison, `engineer` sees the *Part actions* menu and an enabled lock icon.

### UI-Categories-004: Open a part from a filtered category part list

| Field | Value |
|---|---|
| **Summary** | After a filter narrows the category part list, the remaining part name still opens its detail view. |
| **Requirement** | `R-Categories-05`, `R-Categories-06`. Source: [part-index.md#L44](../../requirements/docs/part-index.md#L44), [part-index.md#L46](../../requirements/docs/part-index.md#L46) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Exploratory (filter, then open) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Parent` with active part `QA-<suffix> Part A` and inactive part `QA-<suffix> Part C`, created via the API as `admin`; Pre-steps: log in, open the category. |
| **Automation** | Partial: the available filters are not named in the docs, so the filter choice depends on the app. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the table filter control and add a filter that separates the two parts (for example one on the active state). | Filter: active parts only | The list shows only `QA-<suffix> Part A`. Filter names and values are as the app offers them: the docs do not name them (see index, Not in docs item 6). |
| 2 | Click the part name. | `QA-<suffix> Part A` | A preview panel opens with the part's name, description and category (F-13). |
| 3 | Click the part name at the top of the preview panel. | None | The Part Detail view of `QA-<suffix> Part A` opens. |

**Postconditions and cleanup:** as `admin`: set the parts inactive, delete them, then delete the category. Remove the filter if it persists.

**Notes:** filters are user-configurable; this case does not assert which filters exist. Steps updated after the MCP run of 2026-10-14: a click in the list opens a preview panel first (F-13).

### UI-Categories-005: The part detail breadcrumb shows the part's categories

| Field | Value |
|---|---|
| **Summary** | The part detail page shows the part's categories in the top navigation bar. |
| **Requirement** | `R-Categories-07`. Source: [part-views.md#L17-L21](../../requirements/docs/part-views.md#L17-L21) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: part in a nested category) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: `QA-<suffix> Parent`, sub-category `QA-<suffix> Child`, part `QA-<suffix> Part B` in `QA-<suffix> Child`, created via the API as `admin`; Pre-steps: log in. |
| **Automation** | Partial: breadcrumb structure is not stated. |
| **Review** | Draft · Open question: Q-Categories-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part's detail view. | `QA-<suffix> Part B` | The detail page opens. |
| 2 | Look at the top navigation bar. | None | The breadcrumb shows the part's categories, including `QA-<suffix> Child`. Open: Q-Categories-01 (whether the parent `QA-<suffix> Parent` and a root entry are shown, their order and labels). |

**Postconditions and cleanup:** as `admin`: set the part inactive, delete it, then delete both categories.

**Notes:** the docs say only that "the categories of each part is displayed on the top navigation bar".

### UI-Categories-006: Open the category from the breadcrumb, then open the part from its list

| Field | Value |
|---|---|
| **Summary** | Clicking the part's category in the breadcrumb leads to a category page from which the part can be opened again. |
| **Requirement** | `R-Categories-07`, `R-Categories-06`. Source: [part-views.md#L17-L21](../../requirements/docs/part-views.md#L17-L21), [part-index.md#L46](../../requirements/docs/part-index.md#L46) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Exploratory (round trip: detail, breadcrumb, category list, detail) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Parent` and part `QA-<suffix> Part A` in it, created via the API as `admin`; Pre-steps: log in, open the part's detail view. |
| **Automation** | Partial: click behaviour is not stated. |
| **Review** | Draft · Open question: Q-Categories-01, Q-Categories-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click the entry for the category in the breadcrumb. | `QA-<suffix> Parent` | Proposed, to confirm in Q-Categories-02: the category page of `QA-<suffix> Parent` opens. |
| 2 | Check the category's part list. | None | The list shows `QA-<suffix> Part A`. Open: Q-Categories-02 (that the entry opens the category page). |
| 3 | Click the part name. | `QA-<suffix> Part A` | A preview panel opens with the part's name, description and category (F-13). |
| 4 | Click the part name at the top of the preview panel. | None | The Part Detail view of `QA-<suffix> Part A` opens. |

**Postconditions and cleanup:** as `admin`: set the part inactive, delete it, then delete the category.

**Notes:** the breadcrumb lists categories, not parts, so "opening a part from the breadcrumb" can only be a round trip through the category page (Q-Categories-02). Steps updated after the MCP run of 2026-10-14: a click in the list opens a preview panel first (F-13).

### UI-Categories-007: Open a part from the breadcrumb of a part in a nested category

| Field | Value |
|---|---|
| **Summary** | Clicking a higher-level category in the breadcrumb of a part in a sub-category shows that category's list, which includes the part, and the part can be opened from it. |
| **Requirement** | `R-Categories-07`, `R-Categories-02`, `R-Categories-06`. Source: [part-views.md#L17-L21](../../requirements/docs/part-views.md#L17-L21), [part-index.md#L31](../../requirements/docs/part-index.md#L31), [part-index.md#L46](../../requirements/docs/part-index.md#L46) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Exploratory, Equivalence partitioning (valid class: ancestor category) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: `QA-<suffix> Parent`, `QA-<suffix> Child`, part `QA-<suffix> Part B` in `QA-<suffix> Child` only, created via the API as `admin`; Pre-steps: log in, open the part's detail view. |
| **Automation** | Partial: breadcrumb content and click behaviour are not stated. |
| **Review** | Draft · Open question: Q-Categories-01, Q-Categories-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click the breadcrumb entry for the parent category. | `[open: Q-Categories-01, whether an ancestor entry is shown and its label]` | Proposed, to confirm in Q-Categories-02: the category page of `QA-<suffix> Parent` opens. |
| 2 | Check the part list of the opened category. | None | `QA-<suffix> Part B` is listed, because a category's list includes its sub-categories' parts. Open: Q-Categories-02 (that the entry opens the category page). |
| 3 | Click the part name. | `QA-<suffix> Part B` | A preview panel opens with the part's name, description and category (F-13). |
| 4 | Click the part name at the top of the preview panel. | None | The Part Detail view of `QA-<suffix> Part B` opens. |

**Postconditions and cleanup:** as `admin`: set the part inactive, delete it, then delete both categories.

**Notes:** Steps updated after the MCP run of 2026-10-14: a click in the list opens a preview panel first (F-13).
