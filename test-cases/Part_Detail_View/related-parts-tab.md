# Related Parts tab: Detail_View test cases

The part *Related Parts* table: adding relations, how they show on both parts, invalid relations, removal, permissions and the global setting that enables or disables the feature. The docs describe the feature in three sentences (a relationship between two parts, added and shown in a table of the same name, enable or disable in the global part settings); the add form, labels, rules and the setting name are open (Q-Detail_View-54, Q-Detail_View-55). Parts are created through the API as `admin`.

---

### UI-Detail_View-501: Open the Related Parts view of a part with no relations

| Field | Value |
|---|---|
| **Summary** | A user can open the *Related Parts* table of a part that has no related parts. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: no relations) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: part `QA-<suffix> Rel A` created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Related Parts* tab. | None | The *Related Parts* table is shown on the part page (R-Detail_View-40) with no rows. Open: Q-Detail_View-54 (tab versus section, column labels, empty-state text, add control label). |

**Postconditions and cleanup:** Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-502: Add a related part

| Field | Value |
|---|---|
| **Summary** | A user adds a related part to a part, and it is shown in the *Related Parts* table. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: another existing part) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts) [open: Q-Detail_View-54, permission needed]; Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: parts `QA-<suffix> Rel A` and `QA-<suffix> Rel B` created via `POST /api/part/` as `admin`; Pre-steps: log in, open part A's *Related Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Use the add control of the *Related Parts* table. | None | A form opens to add a related part (R-Detail_View-40). Open: Q-Detail_View-54 (control and form labels, required fields). |
| 2 | Select part B and submit. | Related part: `QA-<suffix> Rel B` | The form closes and part B is shown in part A's *Related Parts* table (R-Detail_View-40). Open: Q-Detail_View-54 (columns shown, confirmation message). |

**Postconditions and cleanup:** One relation A-B exists. Cleanup as `admin`: remove the relation [open: Q-Detail_View-54, removal control], set both parts inactive and delete them.

**Notes:** None.

---

### UI-Detail_View-503: A relation shows on the other part as well

| Field | Value |
|---|---|
| **Summary** | After part B is added as related to part A, part A shows in part B's *Related Parts* table. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) (the docs speak of "a relationship between two parts") |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (relation added on one side), Exploratory |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: parts `QA-<suffix> Rel A` and `QA-<suffix> Rel B` created via `POST /api/part/` as `admin`; relation: B added as related of A through the UI as in UI-Detail_View-502; Pre-steps: log in. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open part B's *Related Parts* table. | None | Proposed, to confirm in Q-Detail_View-54: part A is listed in part B's table (the relation is shown on both parts). |

**Postconditions and cleanup:** Cleanup as `admin`: remove the relation, set both parts inactive and delete them.

**Notes:** The docs do not state whether the relation shows on both parts.

---

### UI-Detail_View-504: Add several related parts

| Field | Value |
|---|---|
| **Summary** | A part can have more than one related part, all listed. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Boundary value analysis (more than one relation) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: parts `QA-<suffix> Rel A`, `QA-<suffix> Rel B`, `QA-<suffix> Rel C` created via `POST /api/part/` as `admin`; Pre-steps: log in, open part A's *Related Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add part B as related. | Related part: `QA-<suffix> Rel B` | Part B is listed (R-Detail_View-40). |
| 2 | Add part C as related. | Related part: `QA-<suffix> Rel C` | Parts B and C are both listed (R-Detail_View-40). Open: Q-Detail_View-54 (any limit on the number of relations). |

**Postconditions and cleanup:** Two relations exist. Cleanup as `admin`: remove them, set the parts inactive and delete them.

**Notes:** None.

---

### UI-Detail_View-505: A part cannot be related to itself

| Field | Value |
|---|---|
| **Summary** | Selecting the open part as its own related part is not accepted. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (self-reference) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: part `QA-<suffix> Rel A` created via `POST /api/part/` as `admin`; Pre-steps: log in, open part A's *Related Parts* view, open the add form. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select part A itself and submit. | Related part: `QA-<suffix> Rel A` | Proposed, to confirm in Q-Detail_View-54: the form is rejected with an error (or part A is not offered in the selector), and no relation is created. Open: Q-Detail_View-54 (error text). |

**Postconditions and cleanup:** No relation. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** The docs state no restriction on relations.

---

### UI-Detail_View-506: The same related part cannot be added twice

| Field | Value |
|---|---|
| **Summary** | Adding a part that is already related is not accepted, and the table keeps one row. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate relation) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: parts `QA-<suffix> Rel A` and `QA-<suffix> Rel B` created via `POST /api/part/` as `admin`; relation A-B added as in UI-Detail_View-502; Pre-steps: log in, open part A's *Related Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add part B as related again. | Related part: `QA-<suffix> Rel B` | Proposed, to confirm in Q-Detail_View-54: the form is rejected with an error and part B is still listed once. Open: Q-Detail_View-54 (error text). |
| 2 | Open part B's *Related Parts* table and add part A as related. | Related part: `QA-<suffix> Rel A` | Proposed, to confirm in Q-Detail_View-54: rejected, because the reverse relation already exists. |

**Postconditions and cleanup:** One relation A-B. Cleanup as `admin`: remove it, set both parts inactive and delete them.

**Notes:** None.

---

### UI-Detail_View-507: Add related part submitted without a part

| Field | Value |
|---|---|
| **Summary** | Submitting the add form with no related part selected creates no relation. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: part `QA-<suffix> Rel A` created via `POST /api/part/` as `admin`; Pre-steps: log in, open part A's *Related Parts* view, open the add form. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Submit the form without selecting a part. | Related part: empty | Proposed, to confirm in Q-Detail_View-54: the form stays open with an error on the part field; no relation is created. |

**Postconditions and cleanup:** No relation. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-508: Cancel the add related part form

| Field | Value |
|---|---|
| **Summary** | Closing the add form after selecting a part, without submitting, creates no relation. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-form) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: parts `QA-<suffix> Rel A` and `QA-<suffix> Rel B` created via `POST /api/part/` as `admin`; Pre-steps: log in, open part A's *Related Parts* view, open the add form. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select part B, then close the form without submitting. | Related part: `QA-<suffix> Rel B` | Proposed, to confirm in Q-Detail_View-54: the form closes and part B is not listed. Open: Q-Detail_View-54 (cancel control label). |

**Postconditions and cleanup:** No relation. Cleanup as `admin`: set both parts inactive and delete them.

**Notes:** None.

---

### UI-Detail_View-509: Remove a related part

| Field | Value |
|---|---|
| **Summary** | A user removes an existing relation from the *Related Parts* table. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | What-if business scenario (relation entered by mistake), State transition (related to not related) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: parts `QA-<suffix> Rel A` and `QA-<suffix> Rel B` created via `POST /api/part/` as `admin`; relation A-B added as in UI-Detail_View-502; Pre-steps: log in, open part A's *Related Parts* view. |
| **Automation** | Partial: the removal control is not described. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Remove part B from the table [open: Q-Detail_View-54, removal control and confirmation]. | Related part: `QA-<suffix> Rel B` | Proposed, to confirm in Q-Detail_View-54: part B is no longer listed on part A. |
| 2 | Open part B's *Related Parts* table. | None | Proposed, to confirm in Q-Detail_View-54: part A is no longer listed on part B. |

**Postconditions and cleanup:** No relation. Cleanup as `admin`: set both parts inactive and delete them.

**Notes:** The docs state only that related parts can be added, not removed.

---

### UI-Detail_View-510: View-only user cannot add a related part

| Field | Value |
|---|---|
| **Summary** | `reader` opens the *Related Parts* view and has no way to add a related part. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (view-only user), Decision table (role x action) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: parts `QA-<suffix> Rel A` and `QA-<suffix> Rel B` created via `POST /api/part/` as `admin`; relation A-B added as `admin`; Pre-steps: log in, open part A's *Related Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the *Related Parts* table. | None | Proposed, to confirm in Q-Detail_View-54: the related part B is listed, and the add and remove controls are hidden or disabled. |

**Postconditions and cleanup:** Cleanup as `admin`: remove the relation, set both parts inactive and delete them.

**Notes:** The docs state no permission for related parts.

---

### UI-Detail_View-511: User without any permission cannot open a part to see related parts

| Field | Value |
|---|---|
| **Summary** | `noaccess` does not get part data, including related parts. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (user without permission) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess` (no permissions); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: parts `QA-<suffix> Rel A` and `QA-<suffix> Rel B` created via `POST /api/part/` and related as `admin`; Pre-steps: log in as `noaccess`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open part A's page by its URL. | URL: `/web/part/<pk>/` | Proposed, to confirm in Q-Detail_View-54: no part data and no *Related Parts* table are shown; a no-permission or error message appears. Open: Q-Detail_View-54 (message text; see also Q-Detail_View-19). |

**Postconditions and cleanup:** Cleanup as `admin`: remove the relation, set both parts inactive and delete them.

**Notes:** None.

---

### UI-Detail_View-512: Related Parts feature disabled in the global part settings

| Field | Value |
|---|---|
| **Summary** | With the Related Parts feature disabled, the part page does not offer related parts. |
| **Requirement** | `R-Detail_View-41`. Source: [part-views.md#L144](../../requirements/docs/part-views.md#L144) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (setting off), State transition (enabled to disabled) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = disabled [open: Q-Detail_View-55, setting name, location and default]; Data: part `QA-<suffix> Rel A` created via `POST /api/part/` as `admin`; Pre-steps: as `admin` disable the setting; log in as `engineer`, open the part detail page. |
| **Automation** | Partial: setting name is open. |
| **Review** | Draft · Open question: Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for the *Related Parts* tab or table on the part page. | None | The feature is disabled, so related parts are not offered (R-Detail_View-41). Open: Q-Detail_View-55 (whether the tab or table is hidden, or shown with a message; the docs state only that the feature can be disabled). |

**Postconditions and cleanup:** Cleanup as `admin`: restore the setting to its original value [open: Q-Detail_View-55], set the part inactive and delete it.

**Notes:** Record the setting's original value before changing it.

---

### UI-Detail_View-513: Related Parts feature enabled in the global part settings

| Field | Value |
|---|---|
| **Summary** | With the Related Parts feature enabled, the part page offers related parts. |
| **Requirement** | `R-Detail_View-41`. Source: [part-views.md#L144](../../requirements/docs/part-views.md#L144) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (setting on), State transition (disabled to enabled) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name, location and default]; Data: part `QA-<suffix> Rel A` created via `POST /api/part/` as `admin`; Pre-steps: as `admin` disable the setting, then enable it; log in as `engineer`, open the part detail page. |
| **Automation** | Partial: setting name is open. |
| **Review** | Draft · Open question: Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Related Parts* tab or table. | None | Related parts can be added and are shown in the *Related Parts* table (R-Detail_View-40). Open: Q-Detail_View-55 (whether a page reload is needed after the setting changes). |

**Postconditions and cleanup:** Cleanup as `admin`: restore the setting to its original value, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-514: Existing relations after the feature is disabled and enabled again

| Field | Value |
|---|---|
| **Summary** | A relation created while the feature is enabled is still listed after the feature is disabled and enabled again. |
| **Requirement** | `R-Detail_View-41`. Source: [part-views.md#L144](../../requirements/docs/part-views.md#L144); `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | What-if business scenario (setting switched off for a while), State transition |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled, then toggled [open: Q-Detail_View-55, setting name and location]; Data: parts `QA-<suffix> Rel A` and `QA-<suffix> Rel B` created via `POST /api/part/` as `admin`; relation A-B added as in UI-Detail_View-502; Pre-steps: log in. |
| **Automation** | Partial: setting name is open. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | As `admin`, disable the setting, then reload part A's page as `engineer`. | None | Related parts are not offered (R-Detail_View-41). Open: Q-Detail_View-55 (what is shown). |
| 2 | As `admin`, enable the setting, then open part A's *Related Parts* view. | None | Proposed, to confirm in Q-Detail_View-55: part B is still listed, since disabling only hides the feature. |

**Postconditions and cleanup:** Cleanup as `admin`: restore the setting, remove the relation, set both parts inactive and delete them.

**Notes:** The docs do not say whether disabling the feature deletes relations.

---

### UI-Detail_View-515: A related part is made inactive

| Field | Value |
|---|---|
| **Summary** | A related part that is set inactive after the relation was created. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | What-if business scenario (related part retired), State transition (active to inactive) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: parts `QA-<suffix> Rel A` and `QA-<suffix> Rel B` created via `POST /api/part/` as `admin`; relation A-B added as in UI-Detail_View-502; Pre-steps: as `admin` set part B inactive; log in as `engineer`, open part A's *Related Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the *Related Parts* table of part A. | None | Not known: depends on open question Q-Detail_View-54 (whether an inactive related part is still listed, and how it is marked). |

**Postconditions and cleanup:** Cleanup as `admin`: remove the relation, delete both parts (part B is already inactive; set A inactive first).

**Notes:** The docs state no rule on inactive related parts.

---

### UI-Detail_View-516: Open a related part from the table

| Field | Value |
|---|---|
| **Summary** | A user opens a listed related part's detail page from the *Related Parts* table. |
| **Requirement** | `R-Detail_View-40`. Source: [part-views.md#Related Parts](../../requirements/docs/part-views.md#L138-L140) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Exploratory (navigation across parts) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: Related Parts feature = enabled [open: Q-Detail_View-55, setting name and default]; Data: parts `QA-<suffix> Rel A` and `QA-<suffix> Rel B` created via `POST /api/part/` as `admin`; relation A-B added as in UI-Detail_View-502; Pre-steps: log in, open part A's *Related Parts* view. |
| **Automation** | Partial: the navigation control is not described. |
| **Review** | Draft · Open question: Q-Detail_View-54, Q-Detail_View-55 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click the row of part B. | None | Proposed, to confirm in Q-Detail_View-54: the browser goes to part B's detail page (`/web/part/<pk>/`). |

**Postconditions and cleanup:** Cleanup as `admin`: remove the relation, set both parts inactive and delete them.

**Notes:** The docs do not describe row navigation.
