# BOM tab contents, quantity calculations, multiple substitutes and Excel import: Detail_View test cases

### UI-Detail_View-201: The BOM tab lists each line with its part and quantity

| Field | Value |
|---|---|
| **Summary** | The *BOM* tab of an assembly lists the sub-components and the quantity of each needed to build the assembly. |
| **Requirement** | `R-Detail_View-18`, `R-Detail_View-50`. Source: [part-views.md#BOM](../../requirements/docs/part-views.md#L84), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: BOM with several lines) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, components `QA-<suffix> Comp A`, `QA-<suffix> Comp B`, `QA-<suffix> Comp C` (Component on), BOM lines Comp A quantity 2, Comp B quantity 5, Comp C quantity 1, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`. |
| **Automation** | Partial: column labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-40 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *BOM* tab. | None | The tab lists the sub-components and quantities needed to build the assembly (R-Detail_View-18). Open: Q-Detail_View-40 (column labels). |
| 2 | Read the quantity of each line. | None | Three lines are listed: Comp A quantity `2`, Comp B quantity `5`, Comp C quantity `1` (R-Detail_View-50). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: delete the lines, set the assembly and components inactive and delete them, then delete the category.

**Notes:** None.

---

### UI-Detail_View-202: A line with every property shows its properties in the BOM tab

| Field | Value |
|---|---|
| **Summary** | A line with Reference, Quantity, Attrition, Setup Quantity, Rounding Multiple, Consumable, Inherited, Optional and Note set is displayed with those values. |
| **Requirement** | `R-Detail_View-50`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: every optional property set) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, component `QA-<suffix> Comp A` (Component on), BOM line Comp A with Reference `R1`, Quantity `2`, Attrition `2`, Setup Quantity `5`, Rounding Multiple `10`, Consumable on, Inherited on, Optional on, Note `QA note`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab. |
| **Automation** | Partial: column labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-40 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the line of `QA-<suffix> Comp A`. | None | The line has the properties Part, Reference `R1`, Quantity `2`, Attrition `2`, Setup Quantity `5`, Rounding Multiple `10`, Consumable, Inherited, Optional and Note `QA note` (R-Detail_View-50). Open: Q-Detail_View-40 (which are columns of the table and which only appear in the edit form, and how Attrition is formatted). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: delete the line, set the assembly and component inactive and delete them, then delete the category.

**Notes:** the line is created through the API, so this case checks display only; entry is covered by UI-Detail_View-006.

---

### UI-Detail_View-203: A BOM with no lines shows no line items

| Field | Value |
|---|---|
| **Summary** | Boundary of the line count: an assembly with zero BOM lines shows an empty BOM table. |
| **Requirement** | `R-Detail_View-50`, `R-Detail_View-19`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23), [part-views.md#BOM](../../requirements/docs/part-views.md#L84) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (line count on the lower limit, 0) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view parts); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` with no BOM lines, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`. |
| **Automation** | Partial: the empty-state text is open. |
| **Review** | Draft · Open question: Q-Detail_View-40 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *BOM* tab. | None | The tab is shown for an Assembly (R-Detail_View-19). A BOM has "zero or more" line items (R-Detail_View-50), so the table lists no line. Open: Q-Detail_View-40 (the empty-table message, if any). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: set the assembly inactive and delete it, then delete the category.

**Notes:** None.

---

### UI-Detail_View-204: Turning the Assembly attribute off removes the BOM tab

| Field | Value |
|---|---|
| **Summary** | After the Assembly attribute of an assembly with no BOM lines is switched off, the *BOM* tab is no longer shown. |
| **Requirement** | `R-Detail_View-19`. Source: [part-views.md#BOM](../../requirements/docs/part-views.md#L84) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (Assembly on to off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Asm` with Assembly on and no BOM lines, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Asm`. |
| **Automation** | Partial: the control that switches the attribute is open. |
| **Review** | Draft · Open question: Q-Detail_View-43 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs. | None | The *BOM* tab is shown (R-Detail_View-19). |
| 2 | Switch Assembly off [open: Q-Detail_View-43, the control and label] and save. | Assembly: off | The change is saved. Open: Q-Detail_View-43 (whether it is accepted without a reload). |
| 3 | Check the tabs again. | None | The *BOM* tab is not shown: it is visible only if the part is an Assembly (R-Detail_View-19). Open: Q-Detail_View-43 (whether a reload is needed). |

**Postconditions and cleanup:** the part is no longer an Assembly. Cleanup as `admin`: set the part inactive, delete it, then delete the category.

**Notes:** the same pattern for the *Variants* tab is UI-Detail_View-089.

---

### UI-Detail_View-205: Turning the Assembly attribute on shows the BOM tab with the existing lines

| Field | Value |
|---|---|
| **Summary** | A part that is not an Assembly but already has BOM lines shows the *BOM* tab after Assembly is switched on, with its lines. |
| **Requirement** | `R-Detail_View-19`, `R-Detail_View-50`. Source: [part-views.md#BOM](../../requirements/docs/part-views.md#L84), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (Assembly off to on), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Asm` that was an Assembly with one BOM line (`QA-<suffix> Comp A`, quantity 2) and then had Assembly switched off, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Asm`. |
| **Automation** | Partial: the control that switches the attribute is open. |
| **Review** | Draft · Open question: Q-Detail_View-43 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the tabs. | None | The *BOM* tab is not shown (R-Detail_View-19). |
| 2 | Switch Assembly on [open: Q-Detail_View-43, the control and label] and save. | Assembly: on | The *BOM* tab is shown (R-Detail_View-19). |
| 3 | Open the *BOM* tab. | None | Proposed, to confirm in Q-Detail_View-43: the line `QA-<suffix> Comp A` with quantity `2` is still listed. |

**Postconditions and cleanup:** the part is an Assembly with one line. Cleanup as `admin`: delete the line, set the part and component inactive and delete them, then delete the category.

**Notes:** the data setup may be refused by the API if the app blocks BOM lines on a non-assembly; if so, record it as a finding in `test-cases/findings.md`.

---

### UI-Detail_View-206: A line without attrition, setup quantity or rounding multiple requires its quantity times the build quantity

| Field | Value |
|---|---|
| **Summary** | Boundary of the calculation inputs: with attrition 0, setup quantity 0 and no rounding multiple, the required quantity is the line quantity for the build. |
| **Requirement** | `R-Detail_View-50`, `R-Detail_View-51`, `R-Detail_View-52`, `R-Detail_View-53`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (attrition and setup on the lower limit, 0; rounding multiple unset) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, component `QA-<suffix> Comp A`, BOM line Comp A quantity `3`, attrition `0`, setup quantity `0`, no rounding multiple, Build Order for `5` assemblies, created via API as `admin`; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: where the required quantity is shown is open. |
| **Review** | Draft · Open question: Q-Detail_View-41 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the required quantity of the Comp A line [open: Q-Detail_View-41, where and under which label]. | None | No attrition, setup or rounding applies (R-Detail_View-51, R-Detail_View-52, R-Detail_View-53). Proposed, to confirm in Q-Detail_View-41: the required quantity is `15` (3 x 5). |

**Postconditions and cleanup:** one Build Order exists. Cleanup as `admin`: delete the Build Order and the line, set the assembly and component inactive and delete them, then delete the category.

**Notes:** None.

---

### UI-Detail_View-207: Attrition is added as a percentage of the base quantity

| Field | Value |
|---|---|
| **Summary** | A line with an attrition of 2 percent requires 2 percent more than its base quantity. |
| **Requirement** | `R-Detail_View-51`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L31) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: attrition above 0) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, component `QA-<suffix> Comp A`, BOM line Comp A quantity `1`, attrition `2` (2%) [open: Q-Detail_View-04, entry format], no setup quantity, no rounding multiple, Build Order for `100` assemblies, created via API as `admin`; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: where the required quantity is shown is open. |
| **Review** | Draft · Open question: Q-Detail_View-04, Q-Detail_View-41 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the required quantity of the Comp A line [open: Q-Detail_View-41, where and under which label]. | None | Attrition is "expressed as a percentage of the base quantity" (R-Detail_View-51), so the base quantity of 100 is increased by 2%. Proposed, to confirm in Q-Detail_View-41: the required quantity is `102`. |

**Postconditions and cleanup:** as UI-Detail_View-206.

**Notes:** the docs give the example "2%" ([manufacturing-bom.md#L31](../../requirements/docs/manufacturing-bom.md#L31)).

---

### UI-Detail_View-208: Setup quantity is added to the base quantity

| Field | Value |
|---|---|
| **Summary** | A line with a setup quantity of 5 requires 5 more than its base quantity. |
| **Requirement** | `R-Detail_View-52`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L32) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: setup quantity above 0) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, component `QA-<suffix> Comp A`, BOM line Comp A quantity `1`, setup quantity `5`, no attrition, no rounding multiple, Build Order for `100` assemblies, created via API as `admin`; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: where the required quantity is shown is open. |
| **Review** | Draft · Open question: Q-Detail_View-41 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the required quantity of the Comp A line [open: Q-Detail_View-41, where and under which label]. | None | The setup quantity "is added to the base quantity of the BOM line item" (R-Detail_View-52). Proposed, to confirm in Q-Detail_View-41: the required quantity is `105` (100 + 5, setup added once per build). |

**Postconditions and cleanup:** as UI-Detail_View-206.

**Notes:** whether the setup quantity is added once per build or per assembly unit is the open part of Q-Detail_View-41.

---

### UI-Detail_View-209: A required quantity just below a rounding multiple is rounded up

| Field | Value |
|---|---|
| **Summary** | Boundary just below a multiple: a required quantity of 9 with a rounding multiple of 5 is rounded up. |
| **Requirement** | `R-Detail_View-53`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L33) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (base quantity just below a multiple: 9 for multiple 5) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, component `QA-<suffix> Comp A`, BOM line Comp A quantity `1`, rounding multiple `5`, no attrition, no setup quantity, Build Order for `9` assemblies, created via API as `admin`; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: where the required quantity is shown is open. |
| **Review** | Draft · Open question: Q-Detail_View-41 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the required quantity of the Comp A line [open: Q-Detail_View-41, where and under which label]. | None | Proposed, to confirm in Q-Detail_View-41: the required quantity is `10`; "the required quantity should be rounded up to the nearest multiple" (R-Detail_View-53), so 9 becomes 10. Open: Q-Detail_View-41 (where it is shown, and the exact formula). |

**Postconditions and cleanup:** as UI-Detail_View-206.

**Notes:** None.

**Duplicate check:** 68 · Review · matches: [UI-Detail_View-211](bom-tab-contents-quantity-calculations-substitutes-excel-import.md) (68), [UI-Detail_View-210](bom-tab-contents-quantity-calculations-substitutes-excel-import.md) (66)

**Duplicate judgement:** Keep · Different boundary of R-Detail_View-53 (just below a multiple, 9 rounded up to 10) from UI-Detail_View-210 (on a multiple, unchanged) and UI-Detail_View-211 (just above, 11 to 15). · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-210: A required quantity exactly on a rounding multiple is not changed

| Field | Value |
|---|---|
| **Summary** | Boundary on a multiple: a required quantity of 10 with a rounding multiple of 5 stays 10. |
| **Requirement** | `R-Detail_View-53`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L33) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (base quantity on a multiple: 10 for multiple 5) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: as UI-Detail_View-209 but Build Order for `10` assemblies; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: where the required quantity is shown is open. |
| **Review** | Draft · Open question: Q-Detail_View-41 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the required quantity of the Comp A line [open: Q-Detail_View-41, where and under which label]. | None | Proposed, to confirm in Q-Detail_View-41: the required quantity stays `10`; it is rounded "up to the nearest multiple" (R-Detail_View-53), and 10 already is a multiple of 5. Open: Q-Detail_View-41 (where it is shown, and the exact formula). |

**Postconditions and cleanup:** as UI-Detail_View-206.

**Notes:** None.

**Duplicate check:** 66 · Review · matches: [UI-Detail_View-209](bom-tab-contents-quantity-calculations-substitutes-excel-import.md) (66), [UI-Detail_View-211](bom-tab-contents-quantity-calculations-substitutes-excel-import.md) (66)

**Duplicate judgement:** Keep · On-the-boundary value of R-Detail_View-53 (10 is already a multiple, no rounding) differs from UI-Detail_View-209 (below, rounded up) and UI-Detail_View-211 (above, rounded to the next multiple). · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-211: A required quantity just above a rounding multiple is rounded up to the next multiple

| Field | Value |
|---|---|
| **Summary** | Boundary just above a multiple: a required quantity of 11 with a rounding multiple of 5 is rounded up to 15. |
| **Requirement** | `R-Detail_View-53`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L33) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (base quantity just above a multiple: 11 for multiple 5) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: as UI-Detail_View-209 but Build Order for `11` assemblies; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: where the required quantity is shown is open. |
| **Review** | Draft · Open question: Q-Detail_View-41 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the required quantity of the Comp A line [open: Q-Detail_View-41, where and under which label]. | None | Proposed, to confirm in Q-Detail_View-41: the required quantity is `15`; 11 is rounded up to the nearest multiple of 5 (R-Detail_View-53). Open: Q-Detail_View-41 (where it is shown, and the exact formula). |

**Postconditions and cleanup:** as UI-Detail_View-206.

**Notes:** None.

**Duplicate check:** 68 · Review · matches: [UI-Detail_View-209](bom-tab-contents-quantity-calculations-substitutes-excel-import.md) (68), [UI-Detail_View-210](bom-tab-contents-quantity-calculations-substitutes-excel-import.md) (66)

**Duplicate judgement:** Keep · Just-above boundary of R-Detail_View-53 (11 rounded to the next multiple, 15) differs in class and expected value from UI-Detail_View-209 (9 to 10) and UI-Detail_View-210 (10 unchanged). · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-212: Attrition, setup quantity and rounding multiple combine in one required quantity

| Field | Value |
|---|---|
| **Summary** | A line with attrition 2%, setup quantity 5 and rounding multiple 10 requires the base quantity with all three applied. |
| **Requirement** | `R-Detail_View-51`, `R-Detail_View-52`, `R-Detail_View-53`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L31) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (attrition on, setup on, rounding on) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, component `QA-<suffix> Comp A`, BOM line Comp A quantity `1`, attrition `2`, setup quantity `5`, rounding multiple `10`, Build Order for `100` assemblies, created via API as `admin`; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: where the required quantity is shown is open. |
| **Review** | Draft · Open question: Q-Detail_View-04, Q-Detail_View-41 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the required quantity of the Comp A line [open: Q-Detail_View-41, where and under which label]. | None | Attrition is a percentage of the base quantity (R-Detail_View-51), setup quantity is added (R-Detail_View-52) and the result is rounded up to the nearest multiple (R-Detail_View-53). Proposed, to confirm in Q-Detail_View-41: `110` (100 + 2% = 102, + 5 = 107, rounded up to a multiple of 10). Open: Q-Detail_View-41 (order of the three steps; both orders give 110 for these data). |

**Postconditions and cleanup:** as UI-Detail_View-206.

**Notes:** the data are chosen so that either order of attrition and setup gives 110.

---

### UI-Detail_View-213: Changing the attrition of a line changes the required quantity

| Field | Value |
|---|---|
| **Summary** | After the attrition of a line is raised from 0 to 2 percent in the BOM, a new Build Order requires more of the component. |
| **Requirement** | `R-Detail_View-51`, `R-Detail_View-59`. Source: [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L31), [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L124) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (attrition 0 to 2), What-if business scenario |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, component `QA-<suffix> Comp A`, BOM line Comp A quantity `1`, attrition `0`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: edit control and required quantity location are open. |
| **Review** | Draft · Open question: Q-Detail_View-02, Q-Detail_View-04, Q-Detail_View-41 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Change the attrition of the Comp A line and save [open: Q-Detail_View-02, edit control]. | Attrition: `2` | The line is saved with the new attrition (R-Detail_View-59). Open: Q-Detail_View-04 (entry format). |
| 2 | As `admin` create a Build Order for `100` assemblies (API), open it and read the required quantity of the Comp A line. | Build quantity: `100` | Attrition is a percentage of the base quantity (R-Detail_View-51). Proposed, to confirm in Q-Detail_View-41: the required quantity is `102`. |

**Postconditions and cleanup:** as UI-Detail_View-206.

**Notes:** whether a Build Order created before the change follows it is part of Q-Detail_View-41; this case uses a new Build Order.

---

### UI-Detail_View-214: The available quantity of a line includes the stock of two substitutes

| Field | Value |
|---|---|
| **Summary** | A line with two substitutes counts the stock of the component and of both substitutes in its available quantity. |
| **Requirement** | `R-Detail_View-57`, `R-Detail_View-58`. Source: [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L71), [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L74) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: several substitutes with stock), Boundary value analysis (more than one substitute) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view stock and BOM); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, components `QA-<suffix> Comp A` (stock 5), `QA-<suffix> Comp B` (stock 7), `QA-<suffix> Comp C` (stock 3), BOM line Comp A quantity 1 with substitutes Comp B and Comp C, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab. |
| **Automation** | Partial: the column label is open. |
| **Review** | Draft · Open question: Q-Detail_View-10, Q-Detail_View-40 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the available quantity of the Comp A line [open: Q-Detail_View-40, column label]. | None | "Stock quantities associated with substitute parts are included in the calculation" (R-Detail_View-58). Proposed, to confirm in Q-Detail_View-10: `15` (5 + 7 + 3). |

**Postconditions and cleanup:** the line has two substitutes. Cleanup as `admin`: remove the substitutes and the line, delete stock, set the assembly and components inactive and delete them, then the category.

**Notes:** one substitute is UI-Detail_View-048.

**Duplicate check:** 51 · Review · matches: [UI-Detail_View-218](bom-tab-contents-quantity-calculations-substitutes-excel-import.md) (51)

**Duplicate judgement:** Keep · Starting state differs from UI-Detail_View-218 (all substitutes active here, Comp B inactive there) and so does the expected outcome (15 here, open 15-or-8 there). · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-215: Stock of the second substitute alone can be allocated to the line

| Field | Value |
|---|---|
| **Summary** | When the component and the first substitute have no stock, stock of the second substitute is offered and can be allocated in the Build Order. |
| **Requirement** | `R-Detail_View-57`. Source: [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L71) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: stock only on the second substitute) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, components `QA-<suffix> Comp A` (no stock), `QA-<suffix> Comp B` (no stock), `QA-<suffix> Comp C` (stock 4), BOM line Comp A quantity 1 with substitutes Comp B and Comp C, Build Order for 1 assembly, created via API as `admin`; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: the allocation dialog is open. |
| **Review** | Draft · Open question: Q-Detail_View-10 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the allocation of the Comp A line [open: Q-Detail_View-10, control]. | None | Stock items of "any of the substitute parts may be allocated against the particular line item" (R-Detail_View-57): the Comp C stock is offered. |
| 2 | Allocate the Comp C stock. | Quantity: `1` | The allocation is saved against the Comp A line (R-Detail_View-57). Open: Q-Detail_View-10 (how it is shown). |

**Postconditions and cleanup:** one allocation exists. Cleanup as `admin`: delete the Build Order, stock, substitutes and line, set the assembly and components inactive and delete them, then the category.

**Notes:** None.

**Duplicate check:** 67 · Review · matches: [UI-Detail_View-047](bom-consumable-optional-substitute-multilevel-import-compare-replace.md) (67)

**Duplicate judgement:** Keep · Different clause of R-Detail_View-57 and starting state from UI-Detail_View-047: the line has several substitutes and only the second one has stock ("any of the substitute parts"), whereas 047 has a single substitute. · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-216: One line is allocated from the component and two substitutes

| Field | Value |
|---|---|
| **Summary** | A build needing more than any single stock is allocated across the component and two substitutes. |
| **Requirement** | `R-Detail_View-57`, `R-Detail_View-58`. Source: [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L71), [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L74) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Exploratory (allocation across the component and several substitutes) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (full access); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly`, components `QA-<suffix> Comp A` (stock 5), `QA-<suffix> Comp B` (stock 7), `QA-<suffix> Comp C` (stock 3), BOM line Comp A quantity 1 with substitutes Comp B and Comp C, Build Order for 12 assemblies, created via API as `admin`; Pre-steps: log in through the login form, open the Build Order. |
| **Automation** | Partial: the allocation dialog is open. |
| **Review** | Draft · Open question: Q-Detail_View-10, Q-Detail_View-44 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Allocate the Comp A stock to the Comp A line [open: Q-Detail_View-10, control]. | Quantity: `5` | The allocation is saved (R-Detail_View-57). |
| 2 | Allocate the Comp B stock to the same line. | Quantity: `7` | Proposed, to confirm in Q-Detail_View-44: the allocation is saved alongside the Comp A allocation. Substitute stock may be allocated against the line (R-Detail_View-57); whether one line's allocation can be split across the component and substitutes is open (Q-Detail_View-44). |
| 3 | Check the line's allocation. | None | Proposed, to confirm in Q-Detail_View-44: the line shows `12` of `12` allocated; the Comp C stock (3) remains unallocated. |

**Postconditions and cleanup:** two allocations exist. Cleanup as `admin`: delete the Build Order, stock, substitutes and line, set the assembly and components inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-217: Removing one of two substitutes keeps the other counted in the available quantity

| Field | Value |
|---|---|
| **Summary** | After one of two substitutes is removed from the line, only the component and the remaining substitute count. |
| **Requirement** | `R-Detail_View-58`, `R-Detail_View-63`. Source: [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L74), [manufacturing-bom.md#Add Substitute for BOM Item](../../requirements/docs/manufacturing-bom.md#L147) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (two substitutes to one) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: as UI-Detail_View-214 (Comp A stock 5, Comp B stock 7, Comp C stock 3, both substitutes on the line); Pre-steps: log in through the login form, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: the remove control is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-02, Q-Detail_View-10, Q-Detail_View-40 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Edit BOM Item Substitutes* form of the Comp A line and remove the substitute `QA-<suffix> Comp B` [open: Q-Detail_View-10, remove control and confirmation]. | None | Proposed, to confirm in Q-Detail_View-10: the substitute Comp B is removed and Comp C stays. Open: Q-Detail_View-10 (the control and any confirmation). |
| 2 | Reload and read the available quantity of the Comp A line [open: Q-Detail_View-40, column label]. | None | The stock of the remaining substitute is still counted (R-Detail_View-58), the removed one is not. Proposed, to confirm in Q-Detail_View-10: `8` (5 + 3). |

**Postconditions and cleanup:** the line has one substitute. Cleanup as `admin`: remove the substitute and the line, delete stock, set the assembly and components inactive and delete them, then the category.

**Notes:** one substitute removed is UI-Detail_View-050.

**Duplicate check:** 55 · Review · matches: [UI-Detail_View-050](bom-consumable-optional-substitute-multilevel-import-compare-replace.md) (55)

**Duplicate judgement:** Keep · Different transition from UI-Detail_View-050 (two substitutes to one, not one to none) and a different expected outcome: the remaining substitute's stock is still counted (8, not 5). · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-218: The stock of an inactive substitute and the available quantity

| Field | Value |
|---|---|
| **Summary** | A substitute part that is made inactive while it still has stock: effect on the line's available quantity. |
| **Requirement** | `R-Detail_View-58`. Source: [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L74) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | What-if business scenario (substitute made inactive), State transition (active to inactive) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; view stock and BOM); Settings: None; Data: as UI-Detail_View-214 but `QA-<suffix> Comp B` is set inactive via API as `admin`; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: the column label and the outcome are open. |
| **Review** | Draft · Open question: Q-Detail_View-40, Q-Detail_View-44 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the available quantity of the Comp A line [open: Q-Detail_View-40, column label]. | None | "Stock quantities associated with substitute parts are included in the calculation" (R-Detail_View-58). Open: Q-Detail_View-44 (whether the stock of an inactive substitute, 7, is counted: `15`, or not: `8`). |

**Postconditions and cleanup:** as UI-Detail_View-214; Comp B is already inactive.

**Notes:** the docs say only that inactive parts are "not available for many actions" ([part-index.md#L116](../../requirements/docs/part-index.md#L116), index Not in docs 3).

**Duplicate check:** 51 · Review · matches: [UI-Detail_View-214](bom-tab-contents-quantity-calculations-substitutes-excel-import.md) (51)

**Duplicate judgement:** Keep · Starting state differs from UI-Detail_View-214 (one substitute is inactive), which asks a different question (Q-Detail_View-44) and can give a different available quantity. · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-219: A view-only user cannot add a substitute to a line

| Field | Value |
|---|---|
| **Summary** | A user without BOM edit permission cannot open the substitute form of a line. |
| **Requirement** | `R-Detail_View-60`, `R-Detail_View-63`. Source: [manufacturing-bom.md#Editing Mode](../../requirements/docs/manufacturing-bom.md#L127), [manufacturing-bom.md#Add Substitute for BOM Item](../../requirements/docs/manufacturing-bom.md#L147) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (view-only user blocked) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` with BOM line `QA-<suffix> Comp A` quantity 1 and substitute `QA-<suffix> Comp B`, created via API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for the *Edit* icon at the top of the BOM panel. | None | The *Edit* icon is not shown to users without permission to edit BOMs (R-Detail_View-60). Open: Q-Detail_View-01 (which permission, and whether `reader` lacks it). |
| 2 | Look for the substitute icon in the *Actions* column. | None | Proposed, to confirm in Q-Detail_View-01: no *Actions* column or substitute icon is shown, so the *Edit BOM Item Substitutes* form cannot be opened (it is reached in editing mode, R-Detail_View-63). |

**Postconditions and cleanup:** no records changed. Cleanup as `admin`: remove the substitute and the line, set the assembly and components inactive and delete them, then the category.

**Notes:** the *Edit* icon alone is UI-Detail_View-003.

---

### UI-Detail_View-220: The same part as a substitute on two lines of one BOM

| Field | Value |
|---|---|
| **Summary** | One part is added as a substitute to two different lines of the same BOM. |
| **Requirement** | `R-Detail_View-57`, `R-Detail_View-63`. Source: [manufacturing-bom.md#Substitute BOM Line Items](../../requirements/docs/manufacturing-bom.md#L71), [manufacturing-bom.md#Add Substitute for BOM Item](../../requirements/docs/manufacturing-bom.md#L147) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | What-if business scenario (shared substitute), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management; BOM edit permission [open: Q-Detail_View-01, whether `engineer` may edit BOMs]); Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` with BOM lines `QA-<suffix> Comp A` and `QA-<suffix> Comp B` (quantity 1 each), component `QA-<suffix> Comp C` (Component on), created via API as `admin`; Pre-steps: log in through the login form, open the *BOM* tab, click *Edit*. |
| **Automation** | Partial: the substitute display is open. |
| **Review** | Draft · Open question: Q-Detail_View-01, Q-Detail_View-08, Q-Detail_View-44 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add `QA-<suffix> Comp C` as a substitute of the Comp A line. | Part: `QA-<suffix> Comp C` | The substitute is added (R-Detail_View-63). Open: Q-Detail_View-08 (where it is shown). |
| 2 | Add `QA-<suffix> Comp C` as a substitute of the Comp B line. | Part: `QA-<suffix> Comp C` | Proposed, to confirm in Q-Detail_View-44: the substitute is added to the second line as well. Open: Q-Detail_View-44 (whether the app refuses it, and the error text). |

**Postconditions and cleanup:** up to two substitute links exist. Cleanup as `admin`: remove the substitutes and lines, set the assembly and components inactive and delete them, then the category.

**Notes:** the same substitute twice on one line is UI-Detail_View-037.

---

### UI-Detail_View-221: An Excel file with one valid row is imported as a BOM line

| Field | Value |
|---|---|
| **Summary** | An `.xlsx` file with one valid row is uploaded, mapped and imported, and the line appears in the BOM. |
| **Requirement** | `R-Detail_View-61`, `R-Part-28`, `R-Part-29`, `R-Part-31`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [concepts-data_import.md#Map Data Fields](../../requirements/docs/concepts-data_import.md#L90), [concepts-data_import.md#Process Data](../../requirements/docs/concepts-data_import.md#L104), [concepts-data_import.md#Row States](../../requirements/docs/concepts-data_import.md#L106) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Excel file, one valid row) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A` (Component on), file `qa-bom.xlsx` with one worksheet, a header row and one data row for `QA-<suffix> Comp A`, quantity 3 [open: Q-Detail_View-12, column names and whether the part is given by ID or name]; Pre-steps: log in through the login form, open `QA-<suffix> Assembly`, open the *BOM* tab. |
| **Automation** | Partial: the column mapping is open. |
| **Review** | Draft · Open question: Q-Detail_View-12, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click *Import BOM Data* and upload the file. | `qa-bom.xlsx` | BOM data "can be imported from an existing file (such as CSV or Excel)" (R-Detail_View-61): the upload is accepted. Open: Q-Detail_View-42 (accepted extensions). |
| 2 | Check the field mapping. | None | The server auto-matches file columns to fields, and the user can adjust it (R-Part-28). Open: Q-Detail_View-42 (which headers match). |
| 3 | Process the file, select the row and import it. | None | Each row must be selected and confirmed before it is imported (R-Part-29). The row state becomes Imported (R-Part-31). |
| 4 | Close the session and check the BOM table. | None | A line for `QA-<suffix> Comp A` with quantity `3` is listed (R-Detail_View-61). |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line and the session, set the assembly inactive and delete it and the component, then the category.

**Notes:** bulk upload is non-reversible (R-Part-34). The CSV equivalent is UI-Detail_View-057.

**Duplicate check:** 74 · Review · matches: [UI-Detail_View-057](bom-consumable-optional-substitute-multilevel-import-compare-replace.md) (74)

**Duplicate judgement:** Keep · Different input class of R-Detail_View-61 from UI-Detail_View-057: an Excel (.xlsx) file instead of CSV ("CSV or Excel" are separate clauses), with the Excel-specific question Q-Detail_View-42. · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-222: An Excel file with three rows creates three BOM lines with their values

| Field | Value |
|---|---|
| **Summary** | Three data rows with Reference, Quantity and Note are all imported, and each line keeps its own values. |
| **Requirement** | `R-Detail_View-61`, `R-Detail_View-50`, `R-Part-29`, `R-Part-32`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23), [concepts-data_import.md#Process Data](../../requirements/docs/concepts-data_import.md#L104), [concepts-data_import.md#Row States](../../requirements/docs/concepts-data_import.md#L112) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: several valid rows) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), components `QA-<suffix> Comp A`, `QA-<suffix> Comp B`, `QA-<suffix> Comp C` (Component on), file `qa-bom-3.xlsx` with rows: Comp A, quantity 2, reference `R1`, note `first`; Comp B, quantity 5, reference `R2`, note `second`; Comp C, quantity 1, reference `R3`, note `third` [open: Q-Detail_View-12, column names]; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: the column mapping is open. |
| **Review** | Draft · Open question: Q-Detail_View-12, Q-Detail_View-40, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file and process it. | `qa-bom-3.xlsx` | Three rows are shown in state Pending (R-Part-31). Open: Q-Detail_View-42 (header matching). |
| 2 | Select all rows and import them. | None | All three rows become Imported (R-Part-29, R-Part-32). |
| 3 | Close the session and check the BOM table. | None | Three lines are listed with the values of the file: Comp A `2` / `R1` / `first`, Comp B `5` / `R2` / `second`, Comp C `1` / `R3` / `third` (R-Detail_View-50, R-Detail_View-61). Open: Q-Detail_View-40 (column labels). |

**Postconditions and cleanup:** three BOM lines exist. Cleanup as `admin`: delete the lines and the session, set the assembly and components inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-223: Excel columns with other header names are mapped by hand

| Field | Value |
|---|---|
| **Summary** | A workbook whose headers do not match the field names is imported after the user adjusts the field mapping. |
| **Requirement** | `R-Detail_View-61`, `R-Part-28`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [concepts-data_import.md#Map Data Fields](../../requirements/docs/concepts-data_import.md#L90) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: headers not auto-matched), Decision table (auto-match off, manual mapping on) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A` (Component on), file `qa-bom-headers.xlsx` with headers `Component` and `Amount` and one row (`QA-<suffix> Comp A`, `4`); Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: mapping controls are open. |
| **Review** | Draft · Open question: Q-Detail_View-12, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file and open the mapping step. | `qa-bom-headers.xlsx` | The server tries to match the columns automatically (R-Part-28). Open: Q-Detail_View-42 (whether `Component` and `Amount` match). |
| 2 | Map `Component` to the part field and `Amount` to the quantity field [open: Q-Detail_View-12, field names]. | Mapping: `Component` to Part, `Amount` to Quantity | The mapping is accepted: the user can adjust the mapping the server proposed (R-Part-28). |
| 3 | Process, select and import the row, then check the BOM table. | None | A line for `QA-<suffix> Comp A` with quantity `4` is listed (R-Detail_View-61). |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line and the session, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-224: A valid Excel row is imported while an invalid row stays in Error state

| Field | Value |
|---|---|
| **Summary** | A workbook with one row for an existing part and one for a part that does not exist: the second row cannot be imported, the first can. |
| **Requirement** | `R-Detail_View-61`, `R-Part-30`, `R-Part-31`, `R-Part-32`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [concepts-data_import.md#Process Data](../../requirements/docs/concepts-data_import.md#L104), [concepts-data_import.md#Row States](../../requirements/docs/concepts-data_import.md#L106) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: part not found, mixed with a valid row), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, file `qa-bom-mixed.xlsx` with row 1 for `QA-<suffix> Comp A` quantity 2 and row 2 for `QA-<suffix> Missing` (does not exist) quantity 1 [open: Q-Detail_View-12, how the part column is written]; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: error text is open. |
| **Review** | Draft · Open question: Q-Detail_View-12, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file and process it. | `qa-bom-mixed.xlsx` | Row 1 is Pending (ready to import); row 2 is in Error state and must be corrected before import (R-Part-31). The row errors are displayed (R-Part-30). Open: Q-Detail_View-12 (error text). |
| 2 | Select row 1 and import it. | None | Each row can be imported individually (R-Part-32); row 1 becomes Imported. |
| 3 | Try to import row 2. | None | Row 2 is not imported while it is in Error state (R-Part-31). Open: Q-Detail_View-12 (whether the import control is disabled or an error is shown). |
| 4 | Check the BOM table. | None | Only the line for `QA-<suffix> Comp A` quantity `2` exists; no line for `QA-<suffix> Missing` (R-Part-31). |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line and the session, set the assembly inactive and delete it and the component, then the category.

**Notes:** the CSV equivalent with only an invalid row is UI-Detail_View-058.

---

### UI-Detail_View-225: One row of an Excel import is removed before the others are imported

| Field | Value |
|---|---|
| **Summary** | A row is removed from the import session, and only the remaining rows become BOM lines. |
| **Requirement** | `R-Detail_View-61`, `R-Part-32`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [concepts-data_import.md#Row States](../../requirements/docs/concepts-data_import.md#L112) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: row removed), State transition (row Pending to removed) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: as UI-Detail_View-222 (file `qa-bom-3.xlsx`); Pre-steps: log in through the login form, open the *BOM* tab, upload and process the file. |
| **Automation** | Partial: the remove control is open. |
| **Review** | Draft · Open question: Q-Detail_View-12, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Remove the row of `QA-<suffix> Comp B`. | None | "Each row can be imported or removed individually" (R-Part-32): the row is removed from the session. |
| 2 | Select the other two rows and import them. | None | Both rows become Imported (R-Part-32). |
| 3 | Check the BOM table. | None | Lines for Comp A and Comp C exist; there is no line for Comp B (R-Part-32). |

**Postconditions and cleanup:** two BOM lines exist. Cleanup as `admin`: delete the lines and the session, set the assembly and components inactive and delete them, then the category.

**Notes:** None.

---

### UI-Detail_View-226: Excel TRUE cells set the Consumable and Optional flags of the imported line

| Field | Value |
|---|---|
| **Summary** | A row with TRUE in the Consumable and Optional columns creates a line with both flags on. |
| **Requirement** | `R-Detail_View-61`, `R-Detail_View-50`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: boolean columns set), Decision table (Consumable on, Optional on) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, file `qa-bom-flags.xlsx` with one row (Comp A, quantity 1, Consumable cell TRUE, Optional cell TRUE) [open: Q-Detail_View-42, how boolean cells are read]; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: flag display is open. |
| **Review** | Draft · Open question: Q-Detail_View-12, Q-Detail_View-40, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file, map the flag columns and import the row. | `qa-bom-flags.xlsx` | The row is imported (R-Detail_View-61). Open: Q-Detail_View-42 (whether boolean cells are accepted). |
| 2 | Open the imported line's flags in the BOM table. | None | Proposed, to confirm in Q-Detail_View-42: the line is Consumable and Optional. Open: Q-Detail_View-40 (how the flags are shown). |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line and the session, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-227: Excel numeric cells set attrition, setup quantity and rounding multiple

| Field | Value |
|---|---|
| **Summary** | Numeric cells for Attrition, Setup Quantity and Rounding Multiple are imported into the line. |
| **Requirement** | `R-Detail_View-61`, `R-Detail_View-51`, `R-Detail_View-52`, `R-Detail_View-53`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L31) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: numeric property cells) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, file `qa-bom-calc.xlsx` with one row (Comp A, quantity 1, attrition `2`, setup quantity `5`, rounding multiple `10`) [open: Q-Detail_View-04, attrition format]; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: column labels are open. |
| **Review** | Draft · Open question: Q-Detail_View-04, Q-Detail_View-12, Q-Detail_View-40, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file, map the columns and import the row. | `qa-bom-calc.xlsx` | The row is imported (R-Detail_View-61). Open: Q-Detail_View-42 (how numeric cells are read). |
| 2 | Read the imported line. | None | Proposed, to confirm in Q-Detail_View-42: Attrition `2`, Setup Quantity `5` and Rounding Multiple `10` are stored on the line (R-Detail_View-51, R-Detail_View-52, R-Detail_View-53). Open: Q-Detail_View-40 (labels). |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line and the session, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-228: A legacy .xls workbook is uploaded to the BOM import

| Field | Value |
|---|---|
| **Summary** | A workbook in the older `.xls` format with one valid row is uploaded. |
| **Requirement** | `R-Detail_View-61`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (file-format class: legacy Excel) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, file `qa-bom.xls` with one data row for Comp A quantity 3; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: the outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-12, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click *Import BOM Data* and upload the file. | `qa-bom.xls` | The docs name "CSV or Excel" files (R-Detail_View-61). Proposed, to confirm in Q-Detail_View-42: the file is accepted and its row is shown for mapping. Open: Q-Detail_View-42 (whether `.xls` is accepted, and the error text if not). |

**Postconditions and cleanup:** an import session may exist. Cleanup as `admin`: delete the session, set the assembly inactive and delete it and the component, then the category.

**Notes:** None.

---

### UI-Detail_View-229: An Excel file with only a header row creates no BOM line

| Field | Value |
|---|---|
| **Summary** | A workbook with headers and no data rows is uploaded. |
| **Requirement** | `R-Detail_View-61`, `R-Part-30`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [concepts-data_import.md#Process Data](../../requirements/docs/concepts-data_import.md#L104) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Boundary value analysis (row count on the lower limit, 0), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), file `qa-bom-empty.xlsx` with a header row only; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: the outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-12, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file and process it. | `qa-bom-empty.xlsx` | Proposed, to confirm in Q-Detail_View-42: no row is offered for import. Open: Q-Detail_View-42 (whether the upload is refused, and the message). |
| 2 | Close the session and check the BOM table. | None | Proposed, to confirm in Q-Detail_View-42: the BOM still has no lines. |

**Postconditions and cleanup:** an import session may exist. Cleanup as `admin`: delete the session, set the assembly inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-230: A workbook with several worksheets is uploaded

| Field | Value |
|---|---|
| **Summary** | A workbook with two worksheets, BOM data only on the second one: which sheet is imported. |
| **Requirement** | `R-Detail_View-61`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (multi-sheet workbook), What-if business scenario |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, file `qa-bom-sheets.xlsx` whose first sheet `Notes` holds free text and whose second sheet `BOM` holds a header and one row for Comp A quantity 2; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: the outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-12, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file and process it. | `qa-bom-sheets.xlsx` | Not known: depends on open question Q-Detail_View-42 (which worksheet is read, whether the user can choose, and what is shown for the sheet that is not read). |

**Postconditions and cleanup:** an import session may exist. Cleanup as `admin`: delete any imported line and the session, set the assembly inactive and delete it and the component, then the category.

**Notes:** the docs do not describe worksheets at all.

---

### UI-Detail_View-231: An Excel file with corrupt content is rejected

| Field | Value |
|---|---|
| **Summary** | A file named `.xlsx` whose content is not a valid workbook is uploaded to the BOM import. |
| **Requirement** | `R-Detail_View-61`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (valid extension, invalid content), Equivalence partitioning (invalid class: unreadable file) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), file `qa-bom-corrupt.xlsx` containing plain text `not a workbook`; Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: the error text is open. |
| **Review** | Draft · Open question: Q-Detail_View-12, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Click *Import BOM Data* and upload the file. | `qa-bom-corrupt.xlsx` | Proposed, to confirm in Q-Detail_View-42: the file is rejected with an error and no rows are offered. Open: Q-Detail_View-42 (error text). |
| 2 | Check the BOM table. | None | Proposed, to confirm in Q-Detail_View-42: the BOM still has no lines. |

**Postconditions and cleanup:** an import session may exist. Cleanup as `admin`: delete the session, set the assembly inactive and delete it, then the category.

**Notes:** None.

---

### UI-Detail_View-232: A text value in an Excel quantity cell puts the row in Error state

| Field | Value |
|---|---|
| **Summary** | A row whose quantity cell holds text instead of a number cannot be imported until it is corrected. |
| **Requirement** | `R-Detail_View-61`, `R-Part-30`, `R-Part-31`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [concepts-data_import.md#Process Data](../../requirements/docs/concepts-data_import.md#L104), [concepts-data_import.md#Row States](../../requirements/docs/concepts-data_import.md#L106) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: non-numeric quantity), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, file `qa-bom-badqty.xlsx` with one row (Comp A, quantity cell `abc`); Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: the error text is open. |
| **Review** | Draft · Open question: Q-Detail_View-04, Q-Detail_View-12, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file and process it. | `qa-bom-badqty.xlsx` | Row errors are displayed (R-Part-30). Proposed, to confirm in Q-Detail_View-42: the row is in Error state, which must be corrected before import (R-Part-31). Open: Q-Detail_View-12 (error text). |
| 2 | Try to import the row. | None | The row is not imported while it is in Error state (R-Part-31). |
| 3 | Check the BOM table. | None | No line for `QA-<suffix> Comp A` exists (R-Part-31). |

**Postconditions and cleanup:** no BOM line. Cleanup as `admin`: delete the session, set the assembly inactive and delete it and the component, then the category.

**Notes:** UI-Detail_View-011 covers the same input in the form.

---

### UI-Detail_View-233: The same part in two Excel rows

| Field | Value |
|---|---|
| **Summary** | A workbook lists one component in two rows; checks how the import handles the same component twice in one BOM (open: Q-Detail_View-04). |
| **Requirement** | `R-Detail_View-61`, `R-Detail_View-50`, `R-Part-31`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23), [concepts-data_import.md#Row States](../../requirements/docs/concepts-data_import.md#L106) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate rows), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, file `qa-bom-dup.xlsx` with two rows for Comp A (quantity 2 and quantity 3); Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: the outcome is open. |
| **Review** | Draft · Open question: Q-Detail_View-04, Q-Detail_View-12, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file, process it, select both rows and import them. | `qa-bom-dup.xlsx` | Proposed, to confirm in Q-Detail_View-04: the first row is imported and the second row fails or stays in Error state. Open: Q-Detail_View-04 (whether a duplicate component in one BOM is rejected, and the error text). |
| 2 | Check the BOM table. | None | Proposed, to confirm in Q-Detail_View-04: one line for `QA-<suffix> Comp A` exists, quantity `2`. |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line and the session, set the assembly inactive and delete it and the component, then the category.

**Notes:** no source states whether a component may appear more than once in a BOM; Q-Detail_View-04 asks it. UI-Detail_View-017 asks the same through the form.

---

### UI-Detail_View-234: Special characters and Unicode in Excel reference and note cells are kept

| Field | Value |
|---|---|
| **Summary** | A row with Unicode and special characters in Reference and Note is imported and shown unchanged. |
| **Requirement** | `R-Detail_View-61`, `R-Detail_View-50`. Source: [manufacturing-bom.md#Importing a BOM](../../requirements/docs/manufacturing-bom.md#L131), [manufacturing-bom.md#BOM Line Items](../../requirements/docs/manufacturing-bom.md#L23) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Error guessing (special characters and Unicode) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `steven` (staff) [open: Q-Detail_View-12, which demo user may import]; Settings: None; Data: category `QA-<suffix> Category`, Assembly `QA-<suffix> Assembly` (empty BOM), component `QA-<suffix> Comp A`, file `qa-bom-unicode.xlsx` with one row (Comp A, quantity 1, reference `Ω-R1/é & <b>`, note `Überprüfung "ok" 部品`); Pre-steps: log in through the login form, open the *BOM* tab. |
| **Automation** | Partial: the column mapping is open. |
| **Review** | Draft · Open question: Q-Detail_View-04, Q-Detail_View-12, Q-Detail_View-42 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file, map the columns and import the row. | `qa-bom-unicode.xlsx` | The row is imported (R-Detail_View-61). Open: Q-Detail_View-04 (limits and allowed characters of Reference). |
| 2 | Read the imported line in the BOM table. | None | Proposed, to confirm in Q-Detail_View-04: Reference `Ω-R1/é & <b>` and Note `Überprüfung "ok" 部品` are shown exactly as in the file, with no markup interpreted. |

**Postconditions and cleanup:** one BOM line exists. Cleanup as `admin`: delete the line and the session, set the assembly inactive and delete it and the component, then the category.

**Notes:** the same input in the form is UI-Detail_View-019.
