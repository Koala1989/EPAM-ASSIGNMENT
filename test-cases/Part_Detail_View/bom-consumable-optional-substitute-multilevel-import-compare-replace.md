# BOM consumable, optional and substitute lines, multi-level BOMs, import, comparison and component replacement: Detail_View test cases

### UI-Detail_View-038: A line marked Consumable is shown as consumable in the BOM table

| Field | Value |
|---|---|
| **Summary** | A BOM line created with Consumable on keeps the flag and shows it in the BOM table. |
| **Requirement** | `R-Detail_View-54`, `R-Detail_View-50`. Source: [manufacturing-bom.md#Consumable BOM Line Items](../../requirements/docs/manufacturing-bom.md#L53), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Consumable on) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Screw` (Component on), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: the flag display is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click the add icon, fill in the form with Consumable on and press *Submit*. | Part: `QA-<suffix> Screw`<br>Quantity: `12`<br>Consumable: on | The line is added (R-Detail_View-62). |
| 2 | Check the row of `QA-<suffix> Screw`. | None | The row shows the line is consumable (R-Detail_View-50: Consumable is a boolean line property). Open: Q-Detail_View-09 (column label or icon). |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** the docs example is a *Wood Screw* line, 12 per table.

**Duplicate check:** 54 · Review · matches: [UI-Detail_View-043](bom-consumable-optional-substitute-multilevel-import-compare-replace.md) (54)

**Duplicate judgement:** Keep · Tests the Consumable flag (R-Detail_View-54) on its own component, while UI-Detail_View-043 tests the Optional flag (R-Detail_View-56): different rule and different line property. · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-039: The Consumable flag of a BOM line does not change the component part

| Field | Value |
|---|---|
| **Summary** | Marking a line consumable in one assembly's BOM affects only that BOM: the component part and its line in another assembly are unchanged. |
| **Requirement** | `R-Detail_View-55`. Source: [manufacturing-bom.md#Consumable BOM Line Items](../../requirements/docs/manufacturing-bom.md#L61) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (line flag on in BOM 1, off in BOM 2, part flag off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view BOM and part details); Settings: None; Data: category `QA-<suffix> Category`, Assemblies `QA-<suffix> Assembly 1` and `QA-<suffix> Assembly 2`, component `QA-<suffix> Screw` (Component on, Consumable off); `Assembly 1` has a line for the screw with Consumable on, `Assembly 2` has a line for the screw with Consumable off, created via API as `admin`; Pre-steps: log in through the login form. |
| **Automation** | Partial: the flag display is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> Assembly 1`, then its *BOM* tab. | None | The screw line is consumable (R-Detail_View-55). Open: Q-Detail_View-09 (how the flag is shown). |
| 2 | Open `QA-<suffix> Assembly 2`, then its *BOM* tab. | None | The screw line is not consumable: the flag "only affects how the part is treated within *this* particular BOM" (R-Detail_View-55). |
| 3 | Open `QA-<suffix> Screw` and check its details. | None | The part is not marked Consumable: the flag "does not change the underlying part definition" (R-Detail_View-55). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: delete the BOM lines, set the assemblies inactive and delete them and the component, then the category.

**Notes:** the part-level Consumable attribute is covered by Area ATT (R-ATT-23).

---

### UI-Detail_View-040: A consumable BOM line cannot be allocated in the Build Order allocation table

| Field | Value |
|---|---|
| **Summary** | In the allocation table of a Build Order for the assembly, a consumable line is shown as not allocatable. |
| **Requirement** | `R-Detail_View-54`. Source: [manufacturing-bom.md#Consumable BOM Line Items](../../requirements/docs/manufacturing-bom.md#L53), [manufacturing-bom.md#Consumable BOM Line Items](../../requirements/docs/manufacturing-bom.md#L59) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Consumable on: allocation not possible) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full create, edit and delete, including Build Orders); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, components `QA-<suffix> Screw` (stock 100) and `QA-<suffix> Board` (stock 5), BOM lines Screw (quantity 12, Consumable on) and Board (quantity 1, Consumable off), Build Order for 1 `QA-<suffix> Assembly`, created via API as `admin`; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: the allocation table labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the allocation table of the Build Order [open: Q-Detail_View-09, tab name]. | None | The table shows the BOM lines. |
| 2 | Look at the `QA-<suffix> Screw` line. | None | The line "cannot be allocated, as it is *consumable*" (R-Detail_View-54). Open: Q-Detail_View-09 (how this is shown). |

**Postconditions and cleanup:** no stock allocated. Cleanup as `admin`: cancel and delete the Build Order, delete stock and BOM lines, set the assembly and components inactive and delete them, then the category.

**Notes:** the Build Order module is out of scope beyond what the BOM page states ([manufacturing-bom.md#L59](../../requirements/docs/manufacturing-bom.md#L59)).

---

### UI-Detail_View-041: A non-consumable BOM line can be allocated in the Build Order allocation table

| Field | Value |
|---|---|
| **Summary** | The opposite condition of UI-Detail_View-040: a line with Consumable off, in the same Build Order, is allocatable. |
| **Requirement** | `R-Detail_View-54`. Source: [manufacturing-bom.md#Consumable BOM Line Items](../../requirements/docs/manufacturing-bom.md#L59) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Consumable off: allocation possible) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: as UI-Detail_View-040, created via API as `admin`; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: the allocation controls are open. |
| **Review** | Draft · Open question: Q-Detail_View-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the allocation table and look at the `QA-<suffix> Board` line. | None | Proposed, to confirm in Q-Detail_View-09: the line offers allocation, unlike the consumable `QA-<suffix> Screw` line (R-Detail_View-54). |
| 2 | Allocate `QA-<suffix> Board` stock to the line. | Quantity: `1` [open: Q-Detail_View-09, the allocation control] | Proposed, to confirm in Q-Detail_View-09: the allocation is saved and the line shows 1 allocated. |

**Postconditions and cleanup:** one stock allocation exists. Cleanup as in UI-Detail_View-040.

**Notes:** None.

---

### UI-Detail_View-042: A line that is both Consumable and Optional

| Field | Value |
|---|---|
| **Summary** | A line with both flags on: what the BOM and the Build Order allocation table show. |
| **Requirement** | `R-Detail_View-54`, `R-Detail_View-56`. Source: [manufacturing-bom.md#Consumable BOM Line Items](../../requirements/docs/manufacturing-bom.md#L53), [manufacturing-bom.md#Optional BOM Line Items](../../requirements/docs/manufacturing-bom.md#L65) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Consumable on, Optional on), What-if business scenario |
| **Priority** | P3 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, component `QA-<suffix> Screw` (stock 100), BOM line Screw (quantity 2, Consumable on, Optional on), Build Order for 1 assembly, created via API as `admin`; Pre-steps: log in through the login form. |
| **Automation** | Partial: outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the assembly's *BOM* tab and check the line. | None | Both flags are set on the line (R-Detail_View-50). Open: Q-Detail_View-09 (display). |
| 2 | Open the Build Order allocation table and check the line. | None | A consumable line "cannot be allocated" (R-Detail_View-54). Open: Q-Detail_View-09 (interplay with the optional flag). |

**Postconditions and cleanup:** as UI-Detail_View-040.

**Notes:** the docs do not describe the combination.

---

### UI-Detail_View-043: A line marked Optional is shown as optional in the BOM table

| Field | Value |
|---|---|
| **Summary** | A BOM line created with Optional on keeps the flag and shows it in the BOM table. |
| **Requirement** | `R-Detail_View-56`, `R-Detail_View-50`. Source: [manufacturing-bom.md#Optional BOM Line Items](../../requirements/docs/manufacturing-bom.md#L65), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Optional on) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Sticker` (Component on), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: the flag display is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click the add icon, fill in the form with Optional on and press *Submit*. | Part: `QA-<suffix> Sticker`<br>Quantity: `1`<br>Optional: on | The line is added (R-Detail_View-62). |
| 2 | Check the row. | None | The row shows the line is optional (R-Detail_View-50). Open: Q-Detail_View-09 (column label or icon). |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

**Duplicate check:** 54 · Review · matches: [UI-Detail_View-038](bom-consumable-optional-substitute-multilevel-import-compare-replace.md) (54)

**Duplicate judgement:** Keep · Tests the Optional flag (R-Detail_View-56), while UI-Detail_View-038 tests the Consumable flag (R-Detail_View-54): different rule and different line property. · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-044: A build can be completed without allocating an optional line

| Field | Value |
|---|---|
| **Summary** | With the optional items excluded on completion, the Build Order completes although the optional line has no allocation. |
| **Requirement** | `R-Detail_View-56`. Source: [manufacturing-bom.md#Optional BOM Line Items](../../requirements/docs/manufacturing-bom.md#L65) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Optional on, excluded on completion) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, component `QA-<suffix> Board` (stock 5, allocated to the build) and `QA-<suffix> Sticker` (stock 5, not allocated), BOM lines Board (quantity 1) and Sticker (quantity 1, Optional on), Build Order for 1 assembly, created via API as `admin`; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: the completion dialog is open. |
| **Review** | Draft · Open question: Q-Detail_View-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Start completing the build output and exclude the optional items [open: Q-Detail_View-09, control]. | Optional items: excluded | "If optional items are excluded, they will not be allocated to the Build Order" (R-Detail_View-56). |
| 2 | Complete the output and the Build Order. | None | The build "can be completed without them" (R-Detail_View-56). Open: Q-Detail_View-09 (messages). |
| 3 | Check the stock of `QA-<suffix> Sticker`. | None | No Sticker stock was allocated or consumed: quantity still `5` (R-Detail_View-56). |

**Postconditions and cleanup:** a completed Build Order and a built assembly stock item exist. Cleanup as `admin`: delete the produced stock and the Build Order, then BOM lines, set the assembly and components inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-045: Including optional items on completion allocates them to the build

| Field | Value |
|---|---|
| **Summary** | With the optional items included, the optional line is allocated to the Build Order as normal. |
| **Requirement** | `R-Detail_View-56`. Source: [manufacturing-bom.md#Optional BOM Line Items](../../requirements/docs/manufacturing-bom.md#L67) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Optional on, included on completion) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: as UI-Detail_View-044; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: the completion dialog is open. |
| **Review** | Draft · Open question: Q-Detail_View-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Allocate `QA-<suffix> Sticker` stock to the optional line. | Quantity: `1` | "If optional items are included, they will be allocated to the Build Order as normal" (R-Detail_View-56). Open: Q-Detail_View-09 (allocation control). |
| 2 | Complete the output with the optional items included [open: Q-Detail_View-09, control]. | Optional items: included | The optional line is treated like a required line (R-Detail_View-56). Open: Q-Detail_View-09 (messages). |
| 3 | Check the stock of `QA-<suffix> Sticker`. | None | Proposed, to confirm in Q-Detail_View-09: the allocated quantity `1` is consumed, leaving `4`. |

**Postconditions and cleanup:** as UI-Detail_View-044.

**Notes:** None.

---

### UI-Detail_View-046: Optional items included on completion but not allocated

| Field | Value |
|---|---|
| **Summary** | Optional items are included on completion, but the optional line has no allocation. |
| **Requirement** | `R-Detail_View-56`. Source: [manufacturing-bom.md#Optional BOM Line Items](../../requirements/docs/manufacturing-bom.md#L67) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Optional on, included, not allocated), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: as UI-Detail_View-044; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Complete the output with the optional items included and no Sticker allocation [open: Q-Detail_View-09, control]. | Optional items: included | Included optional items "will be allocated ... as normal" (R-Detail_View-56). Proposed, to confirm in Q-Detail_View-09: completion is blocked or warns that the optional line is not fully allocated. |

**Postconditions and cleanup:** the build may be unfinished. Cleanup as UI-Detail_View-044.

**Notes:** None.

---

### UI-Detail_View-047: Stock of a substitute part can be allocated against the BOM line

| Field | Value |
|---|---|
| **Summary** | In the Build Order allocation table, stock of a substitute part is offered for a line whose own component has no stock. |
| **Requirement** | `R-Detail_View-57`. Source: [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L71) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: stock only on a substitute), Exploratory |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, component `QA-<suffix> Comp A` (no stock), component `QA-<suffix> Comp B` (stock 10), BOM line Comp A quantity 1 with substitute Comp B, Build Order for 1 assembly, created via API as `admin`; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: the allocation dialog is open. |
| **Review** | Draft · Open question: Q-Detail_View-10 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the allocation of the `QA-<suffix> Comp A` line [open: Q-Detail_View-10, control]. | None | "Stock items associated with any of the substitute parts may be allocated against the particular line item" (R-Detail_View-57). The stock of `QA-<suffix> Comp B` is offered. |
| 2 | Allocate the Comp B stock. | Quantity: `1` | The allocation is saved against the Comp A line (R-Detail_View-57). Open: Q-Detail_View-10 (how it is shown). |

**Postconditions and cleanup:** one allocation exists. Cleanup as `admin`: delete the Build Order, stock, substitute and line, set the assembly and components inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-048: The available quantity of a line includes the stock of its substitute

| Field | Value |
|---|---|
| **Summary** | A line's *available quantity* counts both the component's stock and the stock of its substitute. |
| **Requirement** | `R-Detail_View-58`. Source: [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L74) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: substitute with stock) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view stock and BOM); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, component `QA-<suffix> Comp A` (stock 5), component `QA-<suffix> Comp B` (stock 7), BOM line Comp A quantity 1, created via API as `admin`; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: the column label is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-10 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Note the available quantity of the Comp A line. | None | The value reflects the stock of Comp A only: `5` [open: Q-Detail_View-10, the column]. |
| 2 | As `admin` add Comp B as a substitute of the line (API), then reload the *BOM* tab. | Substitute: `QA-<suffix> Comp B` | The available quantity includes the substitute's stock (R-Detail_View-58). Proposed, to confirm in Q-Detail_View-10: it reads `12` (5 + 7). |

**Postconditions and cleanup:** the line has one substitute. Cleanup as `admin`: remove the substitute and the line, delete stock, set the assembly and components inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-049: A substitute without stock adds nothing to the available quantity

| Field | Value |
|---|---|
| **Summary** | Boundary of the substitute's stock: 0 units leave the line's available quantity unchanged. |
| **Requirement** | `R-Detail_View-58`. Source: [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L74) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (substitute stock on the lower limit, 0) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view stock and BOM); Settings: None; Data: as UI-Detail_View-048 but `QA-<suffix> Comp B` has stock 0, and Comp B is already a substitute of the line; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: the column label is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-10 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the available quantity of the Comp A line. | None | Stock of the substitute is included in the calculation (R-Detail_View-58), and it is 0. Proposed, to confirm in Q-Detail_View-10: the value is `5`. |

**Postconditions and cleanup:** as UI-Detail_View-048.

**Notes:** None.

---

### UI-Detail_View-050: The available quantity drops when the substitute is removed

| Field | Value |
|---|---|
| **Summary** | After the substitute is removed from the line, its stock no longer counts. |
| **Requirement** | `R-Detail_View-58`, `R-Detail_View-63`. Source: [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L74), [manufacturing-bom.md#Add Substitute for BOM Item](../../requirements/docs/manufacturing-bom.md#L147) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (line with substitute to line without) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: as UI-Detail_View-048 with Comp B already a substitute; Pre-steps: log in through the login form, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: the remove control is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-02, Q-Detail_View-10 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Edit BOM Item Substitutes* form of the Comp A line and remove the substitute `QA-<suffix> Comp B` [open: Q-Detail_View-10, remove control and confirmation]. | None | Proposed, to confirm in Q-Detail_View-10: the substitute `QA-<suffix> Comp B` is removed from the line. Open: Q-Detail_View-10 (the remove control and any confirmation). |
| 2 | Reload and check the available quantity. | None | The stock of Comp B is not counted any more (R-Detail_View-58). Proposed, to confirm in Q-Detail_View-10: the value is `5`. |

**Postconditions and cleanup:** the line has no substitute. Cleanup as `admin`: delete the line, stock, set the assembly and components inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-051: A sub-assembly is used as a BOM component and keeps its own BOM

| Field | Value |
|---|---|
| **Summary** | An assembly that is also a component is a line in a parent BOM, and its own BOM lists its parts. |
| **Requirement** | `R-Detail_View-64`. Source: [manufacturing-bom.md#Multi Level BOMs](../../requirements/docs/manufacturing-bom.md#L157) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: two levels) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Parent`, sub-assembly `QA-<suffix> Sub` (Assembly on, Component on) with BOM line `QA-<suffix> Leaf` (Component on) quantity 4, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Parent`, open the *BOM* tab, click *Edit*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a line for the sub-assembly. | Part: `QA-<suffix> Sub`<br>Quantity: `2` | The line is added (R-Detail_View-62): a BOM "can contain sub-assemblies which themselves have a defined BOM" (R-Detail_View-64). |
| 2 | Open `QA-<suffix> Sub` and its *BOM* tab. | None | The sub-assembly's own BOM lists `QA-<suffix> Leaf` quantity `4` (R-Detail_View-64). Open: Q-Detail_View-11 (whether the parent BOM also expands it). |

**Postconditions and cleanup:** two BOM levels exist. Cleanup as `admin`: delete the lines, set the parts inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-052: A BOM nested four levels deep can be built and opened at every level

| Field | Value |
|---|---|
| **Summary** | Assemblies nested four levels deep each show their own BOM lines; the docs state no depth limit. |
| **Requirement** | `R-Detail_View-64`. Source: [manufacturing-bom.md#Multi Level BOMs](../../requirements/docs/manufacturing-bom.md#L157) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (depth well above two; limit is "unlimited") |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view BOM); Settings: None; Data: category `QA-<suffix> Category`, assemblies `QA-<suffix> L1`, `L2`, `L3` (each Assembly and Component on) and component `QA-<suffix> Leaf`; BOM: L1 contains L2, L2 contains L3, L3 contains Leaf (quantity 1 each), created via API as `admin`; Pre-steps: log in through the login form. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> L1`, then its *BOM* tab. | None | The BOM lists `QA-<suffix> L2` (R-Detail_View-64). |
| 2 | Open `L2`, then `L3` from the BOM tabs. | None | Each BOM lists the next level (R-Detail_View-64). |
| 3 | Open `L3`'s *BOM* tab. | None | It lists `QA-<suffix> Leaf` (R-Detail_View-64: "an unlimited number of levels"). Open: Q-Detail_View-11 (navigation between levels). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: delete the lines, set the parts inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-053: The Used In tab of a sub-assembly lists its parent

| Field | Value |
|---|---|
| **Summary** | The *Used In* tab of a sub-assembly (a Component) lists the parent assembly. |
| **Requirement** | `R-Detail_View-21`, `R-Detail_View-64`. Source: [part-views.md#Used In](../../requirements/docs/part-views.md#L92), [manufacturing-bom.md#Multi Level BOMs](../../requirements/docs/manufacturing-bom.md#L157) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Exploratory (flow across the BOM and Used In tabs) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management; view BOM); Settings: None; Data: as UI-Detail_View-051 with the Parent line for Sub already created; Pre-steps: log in through the login form. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> Sub` and its *Used In* tab. | None | The tab is visible, as the part is a Component (R-Detail_View-21). `QA-<suffix> Parent` is listed as a part this part is used to make (R-Detail_View-21). |

**Postconditions and cleanup:** no records changed. Cleanup as UI-Detail_View-051.

**Notes:** None.

---

### UI-Detail_View-054: An assembly cannot become a component of its own sub-assembly

| Field | Value |
|---|---|
| **Summary** | With Sub in Parent's BOM, adding Parent to Sub's BOM would make a circular BOM. |
| **Requirement** | `R-Detail_View-64`, `R-Detail_View-62`. Source: [manufacturing-bom.md#Multi Level BOMs](../../requirements/docs/manufacturing-bom.md#L157), [manufacturing-bom.md#Add BOM Item](../../requirements/docs/manufacturing-bom.md#L143) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (circular reference) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: as UI-Detail_View-051 with Parent also a Component, and the Parent line for Sub already created; Pre-steps: log in through the login form, open `QA-<suffix> Sub`, open the *BOM* tab, click *Edit*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click the add icon, select `QA-<suffix> Parent` as Part and press *Submit*. | Part: `QA-<suffix> Parent`<br>Quantity: `1` | Not known: depends on open question Q-Detail_View-11 (whether the part is left out of the selector or the form is rejected, and the error text). |

**Postconditions and cleanup:** a line may have been created. Cleanup as UI-Detail_View-051.

**Notes:** the docs state no rule about circular BOMs.

---

### UI-Detail_View-055: Changing a sub-assembly's BOM after the parent BOM is validated

| Field | Value |
|---|---|
| **Summary** | The parent BOM is validated, then a line is added to the sub-assembly's BOM. |
| **Requirement** | `R-Detail_View-64`, `R-Detail_View-65`, `R-Detail_View-67`. Source: [manufacturing-bom.md#Multi Level BOMs](../../requirements/docs/manufacturing-bom.md#L157), [manufacturing-bom.md#BOM Checksum](../../requirements/docs/manufacturing-bom.md#L165) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (validated parent, changed child), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit and validate permission [open: Q-Detail_View-01, whether `engineer` may]); Settings: None; Data: as UI-Detail_View-051 with the Parent line for Sub already created, component `QA-<suffix> Extra`; Pre-steps: log in through the login form, open `QA-<suffix> Parent`, open the *BOM* tab, press *Validate BOM* [open: Q-Detail_View-06, confirmation]. |
| **Automation** | Partial: outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-06, Q-Detail_View-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open `QA-<suffix> Sub`'s *BOM* tab, click *Edit* and add a line. | Part: `QA-<suffix> Extra`<br>Quantity: `1` | The line is added to Sub's BOM (R-Detail_View-62). |
| 2 | Open `QA-<suffix> Parent`'s *BOM* tab and check the validation status. | None | The checksum fields are those of the parent's own lines (R-Detail_View-65). Proposed, to confirm in Q-Detail_View-11: the parent is still validated. |

**Postconditions and cleanup:** as UI-Detail_View-051, plus the added line.

**Notes:** the docs do not say whether a child change reaches the parent's validation.

---

### UI-Detail_View-056: The Import BOM Data icon opens the import dialog

| Field | Value |
|---|---|
| **Summary** | At the top of the *BOM* panel of an assembly, the *Import BOM Data* icon opens the import dialog. |
| **Requirement** | `R-Detail_View-61`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: entry point) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import; docs need staff plus `change` permission]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click the *Import BOM Data* icon at the top of the *BOM* panel. | None | The import dialog opens (R-Detail_View-61). Open: Q-Detail_View-12 (dialog layout and labels). |

**Postconditions and cleanup:** an import session may exist. Cleanup as `admin`: delete the session in the Admin Center, set the assembly inactive and delete it, then the category.

**Notes:** the import follows the general data import process (R-Part-18 to R-Part-34).

---

### UI-Detail_View-057: A CSV row is imported as a BOM line

| Field | Value |
|---|---|
| **Summary** | A CSV file with one valid row is uploaded, mapped and imported, and the line appears in the BOM. |
| **Requirement** | `R-Detail_View-61`, `R-Part-28`, `R-Part-29`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [concepts-data_import.md#Map Data Fields](../../requirements/docs/concepts-data_import.md#L90), [concepts-data_import.md#Process Data](../../requirements/docs/concepts-data_import.md#L104) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: one valid row) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A` (Component on), file `qa-bom.csv` with one data row for `QA-<suffix> Comp A`, quantity 3 [open: Q-Detail_View-12, column names and whether the part is given by ID or name]; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab. |
| **Automation** | Partial: the column mapping is open. |
| **Review** | Draft · Open question: Q-Detail_View-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click *Import BOM Data* and upload the file. | `qa-bom.csv` | The upload is accepted (R-Detail_View-61: CSV or Excel). |
| 2 | Check the field mapping. | None | The server auto-matches file columns to fields, and the user can adjust it (R-Part-28). Open: Q-Detail_View-12 (which columns match). |
| 3 | Process the file, select the row and import it. | None | Each row must be selected and confirmed before it is imported (R-Part-29). The row state becomes Imported (R-Part-31). |
| 4 | Close the session and check the BOM table. | None | A line for `QA-<suffix> Comp A` with quantity `3` is listed (R-Detail_View-61). |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line and the session, set the assembly inactive and delete it and the component, then the category.

**Notes:** bulk upload is non-reversible (R-Part-34).

---

### UI-Detail_View-058: A BOM import row with a non-existing part is in Error state

| Field | Value |
|---|---|
| **Summary** | A row whose part does not exist shows an error and cannot be imported until it is corrected. |
| **Requirement** | `R-Detail_View-61`, `R-Part-30`, `R-Part-31`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [concepts-data_import.md#Process Data](../../requirements/docs/concepts-data_import.md#L104), [concepts-data_import.md#Row States](../../requirements/docs/concepts-data_import.md#L106) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: part not found), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), file `qa-bom-bad.csv` with one row whose part is `QA-<suffix> Missing` (does not exist) [open: Q-Detail_View-12, how the part column is written]; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: error text is open. |
| **Review** | Draft · Open question: Q-Detail_View-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Import the file and map the columns. | `qa-bom-bad.csv` | The file is processed. |
| 2 | Check the row. | None | The row is in *Error* state and "must be corrected before import" (R-Part-31); the row error is displayed (R-Part-30). Open: Q-Detail_View-12 (error text). |
| 3 | Check the BOM table. | None | No line is created for the missing part (R-Part-31). |

**Postconditions and cleanup:** no BOM line. Cleanup as `admin`: delete the session, set the assembly inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-059: A view-only user cannot import BOM data

| Field | Value |
|---|---|
| **Summary** | A user without permission to edit does not get a working BOM import. |
| **Requirement** | `R-Detail_View-60`, `R-Detail_View-61`, `R-Part-19`. Source: [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L127), [concepts-data_import.md#Importing data](../../requirements/docs/concepts-data_import.md#L28) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (user without permission) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view-only); Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for the *Import BOM Data* icon at the top of the *BOM* panel. | None | The user "must be a staff user and have the `change` permission" to import (R-Part-19). Proposed, to confirm in Q-Detail_View-12: the icon is not shown to `reader`. |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the assembly inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-060: A file of an unsupported type is uploaded to the BOM import

| Field | Value |
|---|---|
| **Summary** | A PNG image is uploaded instead of a CSV or Excel file. |
| **Requirement** | `R-Detail_View-61`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong file type) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: Assembly `QA-<suffix> Assembly` (empty BOM), image `qa-image.png`; Pre-steps: log in through the login form, open the *BOM* tab, click *Import BOM Data*. |
| **Automation** | Partial: outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the image. | `qa-image.png` | The docs name "CSV or Excel" files (R-Detail_View-61). Not known: depends on open question Q-Detail_View-12 (whether the file is rejected, and the error text). |

**Postconditions and cleanup:** no session expected. Cleanup as UI-Detail_View-056.

**Notes:** None.

---

### UI-Detail_View-061: Importing a line into a validated BOM marks it Not Validated

| Field | Value |
|---|---|
| **Summary** | After the BOM is validated, an imported line makes the status "Not Validated". |
| **Requirement** | `R-Detail_View-61`, `R-Detail_View-65`, `R-Detail_View-67`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [manufacturing-bom.md#BOM Validation](../../requirements/docs/manufacturing-bom.md#L163), [manufacturing-bom.md#BOM Validation Status](../../requirements/docs/manufacturing-bom.md#L187) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (validated to not validated, line imported), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import, and validate (Q-Detail_View-06)]; Settings: None; Data: Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 2, component `QA-<suffix> Comp B`, file `qa-bom.csv` with one row for Comp B; Pre-steps: log in through the login form, open the *BOM* tab, press *Validate BOM* [open: Q-Detail_View-06, confirmation]. |
| **Automation** | Partial: import mapping is open. |
| **Review** | Draft · Open question: Q-Detail_View-06, Q-Detail_View-12 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Import the file and import its row. | `qa-bom.csv` | The line is added (R-Detail_View-61). |
| 2 | Check the validation status. | None | The status reads "Not Validated" with the *Validate BOM* button: "Whenever a BOM line item is created ... it must be validated again" (R-Detail_View-65, R-Detail_View-67). Open: Q-Detail_View-12 (the import mapping and which demo user may import). |

**Postconditions and cleanup:** two BOM lines, BOM not validated. Cleanup as `admin`: delete the lines and the session, set the assembly inactive and delete it and the components, then the category.

**Notes:** None.

---

### UI-Detail_View-062: The Compare BOM icon opens the comparison view

| Field | Value |
|---|---|
| **Summary** | The *Compare BOM* icon at the top of the BOM table opens a view where a secondary assembly can be selected. |
| **Requirement** | `R-Detail_View-68`. Source: [manufacturing-bom.md#BOM Comparison](../../requirements/docs/manufacturing-bom.md#L197) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: entry point) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view BOM); Settings: None; Data: category `QA-<suffix> Category`, Assemblies `QA-<suffix> Asm A` and `QA-<suffix> Asm B`, each with a BOM; Pre-steps: log in through the login form, open `QA-<suffix> Asm A`. |
| **Automation** | Partial: control labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *BOM* tab and click the *Compare BOM* icon at the top of the BOM table. | None | The BOM comparison view opens (R-Detail_View-68) and "allows you to select a secondary assembly to compare with the primary assembly". Open: Q-Detail_View-13 (selector label). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: delete BOM lines, set the assemblies and components inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-063: Show all parts lists the lines of both assemblies with differences highlighted

| Field | Value |
|---|---|
| **Summary** | In *Show all parts* mode, all lines of both BOMs are shown side by side and differences are red. |
| **Requirement** | `R-Detail_View-68`, `R-Detail_View-69`. Source: [manufacturing-bom.md#BOM Comparison](../../requirements/docs/manufacturing-bom.md#L197), [manufacturing-bom.md#Display Mode](../../requirements/docs/manufacturing-bom.md#L209) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (view mode: show all) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view BOM); Settings: None; Data: category `QA-<suffix> Category`; `Asm A` BOM: `QA-<suffix> Comp A` (qty 1) and `QA-<suffix> Comp B` (qty 1); `Asm B` BOM: `Comp B` (qty 1) and `QA-<suffix> Comp C` (qty 1), created via API as `admin`; Pre-steps: log in through the login form, open `Asm A`, open the *BOM* tab, click *Compare BOM*, select `Asm B`. |
| **Automation** | Partial: highlight check needs the display. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the mode *Show all parts*. | Mode: *Show all parts* | "Display all BOM line items from both assemblies" (R-Detail_View-69): Comp A, Comp B and Comp C are listed. |
| 2 | Check the highlighting. | None | The lines that differ (Comp A and Comp C) are highlighted in red (R-Detail_View-69). The common Comp B line is not. Open: Q-Detail_View-13 (what exactly is highlighted). |

**Postconditions and cleanup:** as UI-Detail_View-062.

**Notes:** None.

---

### UI-Detail_View-064: Show different parts lists only the differing lines

| Field | Value |
|---|---|
| **Summary** | In *Show different parts* mode only the lines that differ between the two BOMs are listed. |
| **Requirement** | `R-Detail_View-69`. Source: [manufacturing-bom.md#Display Mode](../../requirements/docs/manufacturing-bom.md#L209) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (view mode: show different) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view BOM); Settings: None; Data: as UI-Detail_View-063; Pre-steps: log in through the login form, open `Asm A`, open the comparison with `Asm B`. |
| **Automation** | Partial: control labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the mode *Show different parts*. | Mode: *Show different parts* | "Display only the BOM line items which are different" (R-Detail_View-69): Comp A and Comp C are listed, Comp B is not. Differences are in red (R-Detail_View-69). |

**Postconditions and cleanup:** as UI-Detail_View-062.

**Notes:** None.

**Duplicate check:** 59 · Review · matches: [UI-Detail_View-065](bom-consumable-optional-substitute-multilevel-import-compare-replace.md) (59)

**Duplicate judgement:** Keep · Different decision-table column of R-Detail_View-69 (*Show different parts* vs *Show common parts* in UI-Detail_View-065) with the opposite expected outcome (Comp A and Comp C listed, not Comp B). · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-065: Show common parts lists only the lines both BOMs share

| Field | Value |
|---|---|
| **Summary** | In *Show common parts* mode only the lines common to both BOMs are listed. |
| **Requirement** | `R-Detail_View-69`. Source: [manufacturing-bom.md#Display Mode](../../requirements/docs/manufacturing-bom.md#L209) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (view mode: show common) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view BOM); Settings: None; Data: as UI-Detail_View-063; Pre-steps: log in through the login form, open `Asm A`, open the comparison with `Asm B`. |
| **Automation** | Partial: control labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the mode *Show common parts*. | Mode: *Show common parts* | "Display only the BOM line items which are common" (R-Detail_View-69): only Comp B is listed. |

**Postconditions and cleanup:** as UI-Detail_View-062.

**Notes:** None.

**Duplicate check:** 59 · Review · matches: [UI-Detail_View-064](bom-consumable-optional-substitute-multilevel-import-compare-replace.md) (59)

**Duplicate judgement:** Keep · Different decision-table column of R-Detail_View-69 (*Show common parts* vs *Show different parts* in UI-Detail_View-064) with the opposite expected outcome (only Comp B listed). · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-066: Comparing two identical BOMs shows no differences

| Field | Value |
|---|---|
| **Summary** | Two assemblies with identical BOMs: *Show different parts* is empty and *Show common parts* lists every line. |
| **Requirement** | `R-Detail_View-69`. Source: [manufacturing-bom.md#Display Mode](../../requirements/docs/manufacturing-bom.md#L209) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (zero differing lines), Decision table |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view BOM); Settings: None; Data: category `QA-<suffix> Category`; `Asm A` and `Asm B` both with BOM `QA-<suffix> Comp A` (qty 2), created via API as `admin`; Pre-steps: log in through the login form, open `Asm A`, open the comparison with `Asm B`. |
| **Automation** | Partial: empty-list display is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select *Show different parts*. | None | No lines are listed, as none differs (R-Detail_View-69). Open: Q-Detail_View-13 (empty-table text). |
| 2 | Select *Show common parts*. | None | The Comp A line is listed, with no red highlight (R-Detail_View-69). |

**Postconditions and cleanup:** as UI-Detail_View-062.

**Notes:** None.

---

### UI-Detail_View-067: Comparing with an assembly that has an empty BOM

| Field | Value |
|---|---|
| **Summary** | The secondary assembly has no BOM lines. |
| **Requirement** | `R-Detail_View-68`, `R-Detail_View-69`, `R-Detail_View-50`. Source: [manufacturing-bom.md#BOM Comparison](../../requirements/docs/manufacturing-bom.md#L197), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (secondary BOM with zero lines; a BOM has "zero or more" lines) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view BOM); Settings: None; Data: `Asm A` with BOM `QA-<suffix> Comp A` (qty 1), `Asm B` with an empty BOM; Pre-steps: log in through the login form, open `Asm A`, open the comparison, select `Asm B`. |
| **Automation** | Partial: outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select *Show all parts*. | None | The Comp A line of the primary assembly is listed as different (R-Detail_View-69). Open: Q-Detail_View-13 (what is shown on the empty side). |
| 2 | Select *Show common parts*. | None | No line is listed (R-Detail_View-69). |

**Postconditions and cleanup:** as UI-Detail_View-062.

**Notes:** None.

---

### UI-Detail_View-068: An assembly is compared with itself

| Field | Value |
|---|---|
| **Summary** | The same assembly is selected as the secondary assembly. |
| **Requirement** | `R-Detail_View-68`. Source: [manufacturing-bom.md#BOM Comparison](../../requirements/docs/manufacturing-bom.md#L197) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (same assembly on both sides) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view BOM); Settings: None; Data: `Asm A` with BOM `QA-<suffix> Comp A` (qty 1); Pre-steps: log in through the login form, open `Asm A`, open the comparison. |
| **Automation** | Partial: outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select `QA-<suffix> Asm A` as the secondary assembly. | Secondary: `QA-<suffix> Asm A` | Not known: depends on open question Q-Detail_View-13 (whether the part is not offered, rejected, or compared with itself and shown with no differences). |

**Postconditions and cleanup:** as UI-Detail_View-062.

**Notes:** None.

---

### UI-Detail_View-069: A differing quantity on a common component is highlighted

| Field | Value |
|---|---|
| **Summary** | The same component with a different quantity in the two BOMs is flagged as a difference. |
| **Requirement** | `R-Detail_View-68`, `R-Detail_View-69`. Source: [manufacturing-bom.md#BOM Comparison](../../requirements/docs/manufacturing-bom.md#L197), [manufacturing-bom.md#Display Mode](../../requirements/docs/manufacturing-bom.md#L209) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: same part, different property) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view BOM); Settings: None; Data: `Asm A` BOM `QA-<suffix> Comp A` quantity 1, `Asm B` BOM `Comp A` quantity 2; Pre-steps: log in through the login form, open `Asm A`, open the comparison with `Asm B`. |
| **Automation** | Partial: highlight check needs the display. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-13 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select *Show different parts*. | None | The comparison "can highlight different component parts, quantities and other properties" (R-Detail_View-68): the Comp A line is listed with the quantity difference in red (R-Detail_View-69). Open: Q-Detail_View-13 (whether a quantity-only difference counts). |

**Postconditions and cleanup:** as UI-Detail_View-062.

**Notes:** None.

---

### UI-Detail_View-070: The Used In tab is hidden for a part that is not a Component

| Field | Value |
|---|---|
| **Summary** | The entry point of *Replace Component*, the *Used In* tab, is not offered on a part without the Component attribute. |
| **Requirement** | `R-Detail_View-21`, `R-Detail_View-70`. Source: [part-views.md#Used In](../../requirements/docs/part-views.md#L92), [manufacturing-bom.md#Replacing Components](../../requirements/docs/manufacturing-bom.md#L223) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Component off: tab hidden) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> NoComp` (Component off), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> NoComp`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs of the part. | None | The *Used In* tab is not shown: it is visible only if the part is a Component (R-Detail_View-21). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the part inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-071: A component is replaced in the BOM of one selected assembly

| Field | Value |
|---|---|
| **Summary** | From the *Used In* tab of the component, one assembly is selected and the component is replaced by a new part. |
| **Requirement** | `R-Detail_View-70`. Source: [manufacturing-bom.md#Replacing Components](../../requirements/docs/manufacturing-bom.md#L223) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: one assembly selected) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: category `QA-<suffix> Category`, assembly `QA-<suffix> Asm A` with BOM `QA-<suffix> Old` (qty 2), components `QA-<suffix> Old` and `QA-<suffix> New` (Component on), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Old`, open its *Used In* tab. |
| **Automation** | Partial: dialog labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Tick the checkbox next to `QA-<suffix> Asm A`. | None | The row is selected (R-Detail_View-70). |
| 2 | Click the *Replace Component* icon. | None | The "Replace Component" dialog opens, to select a new component part (R-Detail_View-70). Open: Q-Detail_View-14 (fields and buttons). |
| 3 | Select the new part and confirm. | Part: `QA-<suffix> New` | The dialog closes. Open: Q-Detail_View-14 (confirmation and message). |
| 4 | Open `QA-<suffix> Asm A` and its *BOM* tab. | None | The line for `QA-<suffix> New` replaces `QA-<suffix> Old` (R-Detail_View-70). |

**Postconditions and cleanup:** the BOM holds `New`. Cleanup as `admin`: delete the line, set the assembly and components inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-072: A component is replaced only in the selected assemblies

| Field | Value |
|---|---|
| **Summary** | Three assemblies use the component; two are selected, and the third keeps the old component. |
| **Requirement** | `R-Detail_View-70`. Source: [manufacturing-bom.md#Replacing Components](../../requirements/docs/manufacturing-bom.md#L223) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: several assemblies, a subset selected) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: assemblies `QA-<suffix> Asm A`, `Asm B` and `Asm C`, each with BOM `QA-<suffix> Old` (qty 1), component `QA-<suffix> New` (Component on), created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Old`, open its *Used In* tab. |
| **Automation** | Partial: dialog labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Tick `Asm A` and `Asm B`, leave `Asm C` unticked, click *Replace Component*. | None | The dialog opens (R-Detail_View-70). |
| 2 | Select `QA-<suffix> New` and confirm. | Part: `QA-<suffix> New` | The component is replaced "in the BOM of the selected assemblies" (R-Detail_View-70). Open: Q-Detail_View-14 (message). |
| 3 | Open the BOMs of `Asm A`, `Asm B` and `Asm C`. | None | `Asm A` and `Asm B` hold `New`. `Asm C` still holds `Old` (R-Detail_View-70: only the selected assemblies). |

**Postconditions and cleanup:** as UI-Detail_View-071, for three assemblies.

**Notes:** None.

---

### UI-Detail_View-073: Replace Component with no assembly selected

| Field | Value |
|---|---|
| **Summary** | No row is ticked on the *Used In* tab, and the *Replace Component* icon is used. |
| **Requirement** | `R-Detail_View-70`. Source: [manufacturing-bom.md#Replacing Components](../../requirements/docs/manufacturing-bom.md#L223) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty selection) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: as UI-Detail_View-071; Pre-steps: log in through the login form, open `QA-<suffix> Old`, open its *Used In* tab. |
| **Automation** | Partial: outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Without ticking any row, click the *Replace Component* icon. | None | The docs ask the user to select assemblies first (R-Detail_View-70). Proposed, to confirm in Q-Detail_View-14: the icon is disabled and no dialog opens. |

**Postconditions and cleanup:** no records changed. Cleanup as UI-Detail_View-071.

**Notes:** None.

---

### UI-Detail_View-074: A component is replaced by itself

| Field | Value |
|---|---|
| **Summary** | The old component is also chosen as the new component. |
| **Requirement** | `R-Detail_View-70`. Source: [manufacturing-bom.md#Replacing Components](../../requirements/docs/manufacturing-bom.md#L223) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (new equals old) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: as UI-Detail_View-071; Pre-steps: log in through the login form, open `QA-<suffix> Old`, open its *Used In* tab, tick `Asm A`, click *Replace Component*. |
| **Automation** | Partial: outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select `QA-<suffix> Old` as the new part and confirm. | Part: `QA-<suffix> Old` | Not known: depends on open question Q-Detail_View-14 (whether the part is not offered or rejected, and the error text). |

**Postconditions and cleanup:** the BOM is unchanged expected. Cleanup as UI-Detail_View-071.

**Notes:** None.

---

### UI-Detail_View-075: The replacement part is already in a selected BOM

| Field | Value |
|---|---|
| **Summary** | The new component is already a line in the BOM of one of the selected assemblies. |
| **Requirement** | `R-Detail_View-70`. Source: [manufacturing-bom.md#Replacing Components](../../requirements/docs/manufacturing-bom.md#L223) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate line after replacement) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: as UI-Detail_View-071, plus `Asm A` also has BOM line `QA-<suffix> New` (qty 1); Pre-steps: log in through the login form, open `QA-<suffix> Old`, open its *Used In* tab, tick `Asm A`, click *Replace Component*. |
| **Automation** | Partial: outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-04, Q-Detail_View-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select `QA-<suffix> New` and confirm. | Part: `QA-<suffix> New` | Not known: depends on open questions Q-Detail_View-14, Q-Detail_View-04 (whether a duplicate line is created, merged or rejected, and the error text). |

**Postconditions and cleanup:** the BOM may hold two lines. Cleanup as UI-Detail_View-071.

**Notes:** the docs state no uniqueness rule for BOM lines.

---

### UI-Detail_View-076: The properties of the replaced line are kept

| Field | Value |
|---|---|
| **Summary** | A line with Reference, quantity and flags is replaced, and the new line shows the same properties. |
| **Requirement** | `R-Detail_View-70`, `R-Detail_View-50`. Source: [manufacturing-bom.md#Replacing Components](../../requirements/docs/manufacturing-bom.md#L223), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | What-if business scenario (a component is superseded in a configured BOM) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: as UI-Detail_View-071, with the `Old` line in `Asm A` set to Reference `R1`, quantity 10, Optional on, Note `QA-<suffix> note`; Pre-steps: log in through the login form, open `QA-<suffix> Old`, open its *Used In* tab, tick `Asm A`, click *Replace Component*. |
| **Automation** | Partial: dialog labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select `QA-<suffix> New` and confirm. | Part: `QA-<suffix> New` | The component is replaced (R-Detail_View-70). |
| 2 | Open `Asm A`'s *BOM* tab and check the line. | None | Proposed, to confirm in Q-Detail_View-14: the line shows `New` with Reference `R1`, quantity `10`, Optional on and the note unchanged. |

**Postconditions and cleanup:** as UI-Detail_View-071.

**Notes:** None.

---

### UI-Detail_View-077: Replacing a component in a validated BOM marks the BOM Not Validated

| Field | Value |
|---|---|
| **Summary** | The component of a line is a checksum field: after validation, replacing it changes the status to "Not Validated". |
| **Requirement** | `R-Detail_View-70`, `R-Detail_View-65`, `R-Detail_View-67`. Source: [manufacturing-bom.md#Replacing Components](../../requirements/docs/manufacturing-bom.md#L223), [manufacturing-bom.md#BOM Checksum](../../requirements/docs/manufacturing-bom.md#L165), [manufacturing-bom.md#BOM Validation Status](../../requirements/docs/manufacturing-bom.md#L187) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (validated to not validated, component replaced) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit and validate permission [open: Q-Detail_View-01, whether `engineer` may]); Settings: None; Data: as UI-Detail_View-071; Pre-steps: log in through the login form, open `Asm A`, open the *BOM* tab, press *Validate BOM* [open: Q-Detail_View-06, confirmation], then open `QA-<suffix> Old` and its *Used In* tab. |
| **Automation** | Partial: dialog labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-06, Q-Detail_View-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Tick `Asm A`, click *Replace Component*, select `QA-<suffix> New` and confirm. | Part: `QA-<suffix> New` | The component is replaced (R-Detail_View-70). |
| 2 | Open `Asm A`'s *BOM* tab and check the validation status. | None | The status reads "Not Validated" with the *Validate BOM* button: the line's component is a checksum field, so changing it requires validating the BOM again (R-Detail_View-65, R-Detail_View-67). Open: Q-Detail_View-14 (the dialog's confirmation and result message). |

**Postconditions and cleanup:** as UI-Detail_View-071.

**Notes:** None.

---

### UI-Detail_View-078: A view-only user cannot replace a component

| Field | Value |
|---|---|
| **Summary** | A user without permission to edit BOMs is not able to replace a component from the *Used In* tab. |
| **Requirement** | `R-Detail_View-60`, `R-Detail_View-70`. Source: [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L127), [manufacturing-bom.md#Replacing Components](../../requirements/docs/manufacturing-bom.md#L223) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (user without edit permission) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view-only); Settings: None; Data: as UI-Detail_View-071; Pre-steps: log in through the login form, open `QA-<suffix> Old`, open its *Used In* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Tick `Asm A` and look for the *Replace Component* icon. | None | Open: Q-Detail_View-14 (which permission is required). Proposed, to confirm in Q-Detail_View-14: the icon is hidden or disabled, and no BOM is changed. |
| 2 | Open `Asm A`'s *BOM* tab. | None | The line still holds `QA-<suffix> Old`. |

**Postconditions and cleanup:** no records changed. Cleanup as UI-Detail_View-071.

**Notes:** None.

---

### UI-Detail_View-079: Cancelling the Replace Component dialog changes no BOM

| Field | Value |
|---|---|
| **Summary** | The dialog is opened and a new part selected, but the dialog is closed without confirming. |
| **Requirement** | `R-Detail_View-70`. Source: [manufacturing-bom.md#Replacing Components](../../requirements/docs/manufacturing-bom.md#L223) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-form) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: as UI-Detail_View-071; Pre-steps: log in through the login form, open `QA-<suffix> Old`, open its *Used In* tab, tick `Asm A`, click *Replace Component*. |
| **Automation** | Partial: the cancel control is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-14 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the new part, then close the dialog without confirming [open: Q-Detail_View-14, the cancel control]. | Part: `QA-<suffix> New` | The dialog closes. Proposed, to confirm in Q-Detail_View-14: nothing is replaced. |
| 2 | Open `Asm A`'s *BOM* tab. | None | Proposed, to confirm in Q-Detail_View-14: the line still holds `QA-<suffix> Old`; closing the dialog without confirming replaces nothing. |

**Postconditions and cleanup:** no records changed. Cleanup as UI-Detail_View-071.

**Notes:** None.
