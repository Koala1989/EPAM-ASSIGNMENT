# Category hierarchy and filtering: Categories test cases

### UI-Categories-008: A top-level category shows the list of its sub-categories

| Field | Value |
|---|---|
| **Summary** | The page of a category shows a list of its sub-categories, and a sub-category can be opened from it. |
| **Requirement** | `R-Categories-03`, `R-Categories-01`. Source: [part-index.md#L33](../../requirements/docs/part-index.md#L33), [part-index.md#L15](../../requirements/docs/part-index.md#L15) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: category with sub-categories) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes: core navigation flow. |
| **Review** | Draft · Open question: Q-Categories-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the category from the *Parts* view. | Category: `QA-<suffix> Top` | The category page opens and shows a list of its sub-categories, including `QA-<suffix> Mid` and `QA-<suffix> Sibling` (R-Categories-03). Open: Q-Categories-05 (where the list is shown and its columns). |
| 2 | Open the sub-category from that list. | `QA-<suffix> Mid` | The page of `QA-<suffix> Mid` opens and shows its own sub-category list with `QA-<suffix> Leaf` (R-Categories-03). Open: Q-Categories-05 (the control that navigates). |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** None

---

### UI-Categories-009: A parent category's part list includes the parts of all its sub-categories

| Field | Value |
|---|---|
| **Summary** | The part list of a top-level category shows its own part and the parts of every sub-category below it, at every depth. |
| **Requirement** | `R-Categories-02`, `R-Categories-01`. Source: [part-index.md#L31](../../requirements/docs/part-index.md#L31), [part-index.md#L15](../../requirements/docs/part-index.md#L15) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: parent with parts at several depths) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes: core hierarchy rule. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the top category from the *Parts* view. | Category: `QA-<suffix> Top` | The category page opens. |
| 2 | Read the category's part list. | None | The list shows `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep` and `QA-<suffix> Part Sib`: the parts of the category and of all its sub-categories (R-Categories-02). |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** None

---

### UI-Categories-010: A mid-level category's part list excludes parts of its parent and sibling categories

| Field | Value |
|---|---|
| **Summary** | The part list of a mid-level category shows its own parts and those of its sub-categories only. |
| **Requirement** | `R-Categories-02`. Source: [part-index.md#L31](../../requirements/docs/part-index.md#L31) |
| **Area** | Categories |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: parts outside the category subtree), Negative |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes: hierarchy rule, negative side. |
| **Review** | Draft · Open question: Q-Categories-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the mid-level category. | Category: `QA-<suffix> Mid` (opened through `QA-<suffix> Top`) | The category page opens. |
| 2 | Read the category's part list. | None | The list shows `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf` and `QA-<suffix> Part Deep` (R-Categories-02). Proposed, to confirm in Q-Categories-05: `QA-<suffix> Part Top` and `QA-<suffix> Part Sib` are not listed. |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** None

---

### UI-Categories-011: A category with no parts and no sub-categories shows empty lists

| Field | Value |
|---|---|
| **Summary** | A category that has neither parts nor sub-categories shows an empty part list and an empty sub-category list. |
| **Requirement** | `R-Categories-02`, `R-Categories-03`. Source: [part-index.md#L31](../../requirements/docs/part-index.md#L31), [part-index.md#L33](../../requirements/docs/part-index.md#L33) |
| **Area** | Categories |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (zero parts, zero sub-categories) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Categories-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the empty category. | Category: `QA-<suffix> Empty` (opened through `QA-<suffix> Top`) | The category page opens. |
| 2 | Read the part list and the sub-category list. | None | No part and no sub-category is listed (R-Categories-02, R-Categories-03). Open: Q-Categories-05 (the empty-state text, if any). |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** None

---

### UI-Categories-012: A part in the deepest category appears in the top category's list

| Field | Value |
|---|---|
| **Summary** | A part four levels down appears in the part list of the top category and in the list of its own category. |
| **Requirement** | `R-Categories-02`. Source: [part-index.md#L31](../../requirements/docs/part-index.md#L31) |
| **Area** | Categories |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (deepest level of the hierarchy: level 4) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the top category and read the part list. | Category: `QA-<suffix> Top` | `QA-<suffix> Part Deep`, in the category four levels down, is listed (R-Categories-02). |
| 2 | Open the deepest category through the hierarchy and read the part list. | Category: `QA-<suffix> Deep` | The list shows `QA-<suffix> Part Deep` (R-Categories-02). |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** The docs state no depth limit; the test checks four levels only.

---

### UI-Categories-013: The sub-category list shows only direct children

| Field | Value |
|---|---|
| **Summary** | The sub-category list of the top category shows its direct children, not deeper descendants. |
| **Requirement** | `R-Categories-03`. Source: [part-index.md#L33](../../requirements/docs/part-index.md#L33) |
| **Area** | Categories |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: grandchildren in the list) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Categories-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the top category and read its sub-category list. | Category: `QA-<suffix> Top` | `QA-<suffix> Mid`, `QA-<suffix> Sibling` and `QA-<suffix> Empty` are listed (R-Categories-03). Proposed, to confirm in Q-Categories-05: `QA-<suffix> Leaf` and `QA-<suffix> Deep` are not listed. |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** The rule says only that a category shows the list of its sub-categories.

---

### UI-Categories-014: What-if: a part moved to another category leaves the old list and enters the new one

| Field | Value |
|---|---|
| **Summary** | After a part's category is changed, it is no longer listed under its old category and is listed under the new one and the new category's parents. |
| **Requirement** | `R-Categories-02`, `R-Categories-01`. Source: [part-index.md#L31](../../requirements/docs/part-index.md#L31), [part-index.md#L15](../../requirements/docs/part-index.md#L15) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | What-if business scenario (part moved to another category), State transition (category A to category B) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Partial: depends on how the category is edited. |
| **Review** | Draft · Open question: Q-Categories-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part from the part list of its category. | Category: `QA-<suffix> Leaf`, part `QA-<suffix> Part Leaf` | The part detail view opens. |
| 2 | Change the part's category. | Category: `QA-<suffix> Sibling` [open: Q-Categories-07, the control and field label] | The change is saved. Open: Q-Categories-07 (how the category is edited). |
| 3 | Open `QA-<suffix> Leaf` and read its part list. | Category: `QA-<suffix> Leaf` | `QA-<suffix> Part Leaf` is not listed; `QA-<suffix> Part Deep` is still listed (R-Categories-02). |
| 4 | Open `QA-<suffix> Sibling` and read its part list. | Category: `QA-<suffix> Sibling` | `QA-<suffix> Part Leaf` and `QA-<suffix> Part Sib` are listed (R-Categories-02). |
| 5 | Open `QA-<suffix> Mid` and read its part list. | Category: `QA-<suffix> Mid` | `QA-<suffix> Part Leaf` is not listed (it is no longer below `QA-<suffix> Mid`); `QA-<suffix> Part Mid` and `QA-<suffix> Part Deep` are listed (R-Categories-02). The top category still lists all five parts. |

**Postconditions and cleanup:** `QA-<suffix> Part Leaf` is now in `QA-<suffix> Sibling`. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** None

---

### UI-Categories-015: What-if: a new part created in a sub-category appears in the parent category's list

| Field | Value |
|---|---|
| **Summary** | A part created with a nested category selected is listed in that category and in all its parent categories. |
| **Requirement** | `R-Categories-02`. Source: [part-index.md#L31](../../requirements/docs/part-index.md#L31) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | What-if business scenario (new part in a nested category) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Add Parts* dropdown and select *Create Part*. | None | The *Create Part* form opens. |
| 2 | Fill in the form and submit. | Name: `QA-<suffix> Part New`<br>Description: `New part`<br>Category: `QA-<suffix> Leaf` | The form closes and the new part's detail page opens. |
| 3 | Open `QA-<suffix> Top` and read its part list. | Category: `QA-<suffix> Top` | `QA-<suffix> Part New` is listed (R-Categories-02). |
| 4 | Open `QA-<suffix> Mid` and read its part list. | Category: `QA-<suffix> Mid` | `QA-<suffix> Part New` is listed (R-Categories-02). |

**Postconditions and cleanup:** One new part `QA-<suffix> Part New` exists. As `admin`: set it inactive and delete it, then clean up the rest as in the data list.

**Notes:** None

---

### UI-Categories-016: The category part list shows name, description, thumbnail, category and stock level

| Field | Value |
|---|---|
| **Summary** | The part list of a category shows the columns the docs list, and the category column shows each part's own category. |
| **Requirement** | `R-Categories-04`. Source: [part-index.md#L37-42](../../requirements/docs/part-index.md#L37-L42) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: list with parts from several categories) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Categories-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the top category. | Category: `QA-<suffix> Top` | The category page opens. |
| 2 | Check the columns of the part list. | None | Each part row shows the part name and description, an image thumbnail, the part category and the part stock level (R-Categories-04). Open: Q-Categories-05 (exact column headers). |
| 3 | Check the category cell of one part from a sub-category. | Row: `QA-<suffix> Part Leaf` | The category cell shows the part's own category `QA-<suffix> Leaf` (R-Categories-04). Proposed, to confirm in Q-Categories-05: not the opened category. |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** None

---

### UI-Categories-017: A filter on the parent category's part list also applies to parts of its sub-categories

| Field | Value |
|---|---|
| **Summary** | One filter set on the top category's part list narrows the list across the parts of all sub-categories. |
| **Requirement** | `R-Categories-05`, `R-Categories-02`. Source: [part-index.md#L44](../../requirements/docs/part-index.md#L44), [part-index.md#L31](../../requirements/docs/part-index.md#L31) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: one filter), Decision table (filter on x subtree) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; `QA-<suffix> Part Mid` and `QA-<suffix> Part Deep` set inactive as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Partial: filter control is not named in the docs. |
| **Review** | Draft · Open question: Q-Categories-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the top category. | Category: `QA-<suffix> Top` | The part list shows the five parts (R-Categories-02). |
| 2 | Add one filter that keeps only active parts. | Filter: [open: Q-Categories-04, the filter name and option for active parts] | The part list can be filtered by user-configurable filters (R-Categories-05). Open: Q-Categories-04 (the filter control and its labels). |
| 3 | Read the part list. | None | Proposed, to confirm in Q-Categories-04: only `QA-<suffix> Part Top`, `QA-<suffix> Part Leaf` and `QA-<suffix> Part Sib` are listed, including the one from a sub-category; the inactive `QA-<suffix> Part Mid` and `QA-<suffix> Part Deep` are not. |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** The filters are not named in the docs (index, Not in docs 6). Use the filter that matches the Active state.

**Duplicate check:** 56 · Review · matches: [UI-Categories-019](category-hierarchy-and-filtering.md) (56)

**Duplicate judgement:** Keep · Differs from UI-Categories-019 in what is checked: the filter narrowing the list across sub-category parts (filter applied, specific parts kept and dropped), while 019 checks the filtered-to-unfiltered transition · test-case-reviewer, 2026-10-15

---

### UI-Categories-018: Two filters on the category part list are applied together

| Field | Value |
|---|---|
| **Summary** | With two filters set, the part list shows only parts that satisfy both. |
| **Requirement** | `R-Categories-05`. Source: [part-index.md#L44](../../requirements/docs/part-index.md#L44) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Decision table (filter A on, filter B on) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; `QA-<suffix> Part Mid` and `QA-<suffix> Part Leaf` created with Assembly on; `QA-<suffix> Part Mid` and `QA-<suffix> Part Deep` set inactive as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Partial: filter control is not named in the docs. |
| **Review** | Draft · Open question: Q-Categories-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the top category and add the first filter. | Category: `QA-<suffix> Top`<br>Filter 1: active parts only [open: Q-Categories-04, filter label and value] | The list can be filtered by multiple filters (R-Categories-05). Open: Q-Categories-04 (control labels). |
| 2 | Add a second filter. | Filter 2: Assembly parts only [open: Q-Categories-04, filter label and value] | The list can be filtered by multiple filters (R-Categories-05). Open: Q-Categories-04 (control labels). |
| 3 | Read the part list. | None | Proposed, to confirm in Q-Categories-04: only `QA-<suffix> Part Leaf` is listed (active and Assembly). `QA-<suffix> Part Top` and `QA-<suffix> Part Sib` (active, not Assembly) and `QA-<suffix> Part Mid` (Assembly, inactive) are not; with OR they would be. |

**Postconditions and cleanup:** no records changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** None

---

### UI-Categories-019: Removing the filters restores the full part list

| Field | Value |
|---|---|
| **Summary** | After a filter is removed, the part list shows all parts of the category and its sub-categories again. |
| **Requirement** | `R-Categories-05`, `R-Categories-02`. Source: [part-index.md#L44](../../requirements/docs/part-index.md#L44), [part-index.md#L31](../../requirements/docs/part-index.md#L31) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | State transition (filtered to unfiltered) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; `QA-<suffix> Part Mid` and `QA-<suffix> Part Deep` set inactive as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Partial: filter control is not named in the docs. |
| **Review** | Draft · Open question: Q-Categories-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the top category and add a filter that keeps only active parts. | Category: `QA-<suffix> Top`<br>Filter: [open: Q-Categories-04, the filter name] | The list is filtered (R-Categories-05). Open: Q-Categories-04 (control labels). |
| 2 | Remove the filter. | None | Open: Q-Categories-04 (the remove control). Proposed, to confirm in Q-Categories-04: the part list shows all five parts again (R-Categories-02). |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** None

**Duplicate check:** 56 · Review · matches: [UI-Categories-017](category-hierarchy-and-filtering.md) (56)

**Duplicate judgement:** Keep · Differs from UI-Categories-017 in technique and outcome: a state transition (filter removed) ending with the full five-part list, while 017 ends on the filtered list · test-case-reviewer, 2026-10-15

---

### UI-Categories-020: A filter that matches no part shows an empty part list

| Field | Value |
|---|---|
| **Summary** | A filter that no part of the category subtree satisfies leaves the part list empty. |
| **Requirement** | `R-Categories-05`. Source: [part-index.md#L44](../../requirements/docs/part-index.md#L44) |
| **Area** | Categories |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: filter with no match), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; `QA-<suffix> Part Mid` and `QA-<suffix> Part Deep` set inactive as `admin`; and `QA-<suffix> Part Top`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Sib` set inactive as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Partial: filter control is not named in the docs. |
| **Review** | Draft · Open question: Q-Categories-04, Q-Categories-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the top category and add the filter that keeps only active parts. | Category: `QA-<suffix> Top`<br>Filter: [open: Q-Categories-04, the filter name] | The list is filtered (R-Categories-05). Open: Q-Categories-04 (control labels). |
| 2 | Read the part list. | None | Proposed, to confirm in Q-Categories-04: no part is listed and no error is shown. Open: Q-Categories-05 (the empty-state text). |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** None

---

### UI-Categories-021: A view-only user can browse the hierarchy and filter the part list

| Field | Value |
|---|---|
| **Summary** | A user with view-only access sees the sub-category list and the part list including sub-category parts, and can use filters. |
| **Requirement** | `R-Categories-02`, `R-Categories-03`, `R-Categories-05`. Source: [part-index.md#L31](../../requirements/docs/part-index.md#L31), [part-index.md#L33](../../requirements/docs/part-index.md#L33), [part-index.md#L44](../../requirements/docs/part-index.md#L44) |
| **Area** | Categories |
| **Type** | Positive |
| **Technique** | Negative (reader), Decision table (role x view) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Categories-04, Q-Categories-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the top category from the *Parts* view. | Category: `QA-<suffix> Top` | The page opens, with the sub-category list (R-Categories-03) and the five parts of the subtree (R-Categories-02). Open: Q-Categories-06 (whether a view-only user sees the page in full). |
| 2 | Add a filter to the part list. | Filter: [open: Q-Categories-04, the filter name] | Proposed, to confirm in Q-Categories-06: the filter works for a view-only user (R-Categories-05). |
| 3 | Look for controls that create or edit categories or parts. | None | Proposed, to confirm in Q-Categories-06: none are shown. |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** See also Q-Categories-03 for the Part Detail view.

---

### UI-Categories-022: A user with no permissions cannot see the category hierarchy

| Field | Value |
|---|---|
| **Summary** | A user without any role cannot view categories or their parts. |
| **Requirement** | `R-Categories-01`. Source: [part-index.md#L15](../../requirements/docs/part-index.md#L15) |
| **Area** | Categories |
| **Type** | Negative |
| **Technique** | Negative (noaccess) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess` (no permissions); Settings: None; Data: categories `QA-<suffix> Top` > `QA-<suffix> Mid` > `QA-<suffix> Leaf` > `QA-<suffix> Deep`, plus `QA-<suffix> Sibling` and `QA-<suffix> Empty` under `QA-<suffix> Top`; one part in each of Top, Mid, Leaf, Deep and Sibling, named `QA-<suffix> Part Top`, `QA-<suffix> Part Mid`, `QA-<suffix> Part Leaf`, `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`; all created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Categories-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Parts* view. | None | Not known: depends on open question Q-Categories-06 (whether the view is hidden, empty or refused). |
| 2 | Open the category by its address. | Address: the category page of `QA-<suffix> Top` (`/web/part/category/<pk>/`) | Proposed, to confirm in Q-Categories-06: no category name, sub-category or part is shown. |

**Postconditions and cleanup:** Nothing changed. none changed. As `admin`: set the parts inactive, delete them, then delete the categories (Deep, Leaf, Empty, Sibling, Mid, Top).

**Notes:** The category primary key is read as `admin` beforehand.

---

### UI-Categories-023: Category names with special characters and Unicode are shown as entered

| Field | Value |
|---|---|
| **Summary** | A sub-category whose name has special characters and Unicode letters is listed with its exact name and can be opened. |
| **Requirement** | `R-Categories-03`. Source: [part-index.md#L33](../../requirements/docs/part-index.md#L33) |
| **Area** | Categories |
| **Type** | Boundary |
| **Technique** | Error guessing (special characters, Unicode) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Top` and its sub-category `QA-<suffix> Ünï & <b>Ω'"` created via the API as `admin`; Pre-steps: log in through the login form, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Categories-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the top category and read the sub-category list. | Category: `QA-<suffix> Top` | The sub-category is listed (R-Categories-03). Proposed, to confirm in Q-Categories-05: its name shows exactly as `QA-<suffix> Ünï & <b>Ω'"`, with no markup rendered. |
| 2 | Open the sub-category. | None | Proposed, to confirm in Q-Categories-05: its page opens with the same name. |

**Postconditions and cleanup:** Nothing changed. As `admin`, delete the sub-category, then `QA-<suffix> Top`.

**Notes:** None

---
