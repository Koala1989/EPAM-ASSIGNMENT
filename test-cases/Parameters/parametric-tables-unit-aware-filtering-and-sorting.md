# Parametric tables with unit-aware filtering and sorting: Part_Params test cases

### UI-Part_Params-064: The category part list has a Parametric View button

| Field | Value |
|---|---|
| **Summary** | The category's part list has a *Parametric View* button above the table, and pressing it opens the parametric table. |
| **Requirement** | `R-Part_Params-21`. Source: [concepts-parameters.md#L112-114](../../requirements/docs/concepts-parameters.md#L112-L114) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: table that supports parametric view) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look above the category's part list. | None | A *Parametric View* button is shown above the table (R-Part_Params-21). Open: Q-Part_Params-18 (whether the category part list is one of the tables that support it). |
| 2 | Press the button. | None | The parametric table opens (R-Part_Params-21). Open: Q-Part_Params-18 (how the table replaces or extends the list). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

---

### UI-Part_Params-065: The parametric table gathers the parameters of all listed parts

| Field | Value |
|---|---|
| **Summary** | The parametric table shows each listed part with its value of the template's parameter in a parameter column. |
| **Requirement** | `R-Part_Params-21`. Source: [concepts-parameters.md#L112-114](../../requirements/docs/concepts-parameters.md#L112-L114) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: parts with a parameter) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-21 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Read the parameter column. | None | The six parts show a value in the `QA-<suffix> Resistance` column: `500`, `4.7k`, `10k`, `47k`, `100k` and `1000 kohm` (R-Part_Params-21). Open: Q-Part_Params-21 (whether values show as entered or converted). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

---

### UI-Part_Params-066: A table that does not support parametric filtering has no Parametric View button

| Field | Value |
|---|---|
| **Summary** | A table without parametric support does not offer the *Parametric View* button. |
| **Requirement** | `R-Part_Params-21`. Source: [concepts-parameters.md#L112-114](../../requirements/docs/concepts-parameters.md#L112-L114) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Negative (opposite condition of 'tables which support') |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. Open a table that does not hold parts, for example a stock table [open: Q-Part_Params-18, which tables lack support]. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the table named in the prerequisites. | None | The table opens. |
| 2 | Look above the table for the button. | None | Proposed, to confirm in Q-Part_Params-18: no *Parametric View* button is shown above this table. R-Part_Params-21 names the button only for tables that support parametric filtering and sorting; it does not say other tables lack it. Open: Q-Part_Params-18 (which tables lack support). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** The docs do not list the tables that support parametric view.

---

### UI-Part_Params-067: Clicking a parameter column header sorts parts by that parameter

| Field | Value |
|---|---|
| **Summary** | One click on the parameter column header sorts the listed parts by their parameter value. |
| **Requirement** | `R-Part_Params-22`. Source: [concepts-parameters.md#L120](../../requirements/docs/concepts-parameters.md#L120) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: numeric parameter), State transition (unsorted to sorted) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-21 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Click the header of the Resistance column. | None | The parts are sorted by that parameter (R-Part_Params-22). Open: Q-Part_Params-21 (the direction of the first sort and its indicator). |
| 3 | Read the order of the parts. | None | Proposed, to confirm in Q-Part_Params-21: ascending, in the order `QA-<suffix> R-500`, `QA-<suffix> R-4k7`, `QA-<suffix> R-10k`, `QA-<suffix> R-47k`, `QA-<suffix> R-100k`, `QA-<suffix> R-1000k`. |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 76 · Review · matches: [UI-Part_Params-068](parametric-tables-unit-aware-filtering-and-sorting.md) (76), [UI-Part_Params-069](parametric-tables-unit-aware-filtering-and-sorting.md) (54)

**Duplicate judgement:** Keep · Differs from UI-Part_Params-068 in the transition (unsorted to first sort vs first to second click, expected order reversed) and from UI-Part_Params-069 in rule and data (R-Part_Params-22 on prefix values vs R-Part_Params-33 on explicit mixed units) · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-068: A second click on the column header reverses the sort

| Field | Value |
|---|---|
| **Summary** | Clicking the same parameter header twice reverses the order of the parts. |
| **Requirement** | `R-Part_Params-22`. Source: [concepts-parameters.md#L120](../../requirements/docs/concepts-parameters.md#L120) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | State transition (ascending to descending) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-21 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Click the header of the Resistance column twice. | None | The parts are sorted by that parameter (R-Part_Params-22). Open: Q-Part_Params-21 (the effect of a second click). |
| 3 | Read the order of the parts. | None | Proposed, to confirm in Q-Part_Params-21: descending, in the order `QA-<suffix> R-1000k`, `QA-<suffix> R-100k`, `QA-<suffix> R-47k`, `QA-<suffix> R-10k`, `QA-<suffix> R-4k7`, `QA-<suffix> R-500`. |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 76 · Review · matches: [UI-Part_Params-067](parametric-tables-unit-aware-filtering-and-sorting.md) (76)

**Duplicate judgement:** Keep · Differs from UI-Part_Params-067 in the state transition (second click, ascending to descending) and the expected order (reversed) · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-069: Sorting by a parameter with mixed units follows the converted value

| Field | Value |
|---|---|
| **Summary** | Values entered in different compatible units sort by their converted numeric value, not by their text. |
| **Requirement** | `R-Part_Params-33`, `R-Part_Params-22`, `R-Part_Params-30`. Source: [concepts-parameters.md#L191](../../requirements/docs/concepts-parameters.md#L191), [concepts-parameters.md#L120](../../requirements/docs/concepts-parameters.md#L120), [concepts-parameters.md#L174-176](../../requirements/docs/concepts-parameters.md#L174-L176) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: compatible units mixed), Error guessing (text order differs from numeric order) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`); category `QA-<suffix> Sorting`; four parts with a `QA-<suffix> Resistance` parameter: `QA-<suffix> S-900` = `900 ohm`, `QA-<suffix> S-1500` = `1500 ohm`, `QA-<suffix> S-2k` = `2 kohm`, `QA-<suffix> S-3000` = `0.003 Mohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Sorting`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-21 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Click the header of the Resistance column. | None | Sorting takes unit conversion into account, so values in different but compatible units are sorted correctly (R-Part_Params-33). Open: Q-Part_Params-21 (the direction of the first sort). |
| 3 | Read the order of the parts. | None | The parts are ordered by converted value: `QA-<suffix> S-900` (900 ohm), `QA-<suffix> S-1500` (1500 ohm), `QA-<suffix> S-2k` (2000 ohm), `QA-<suffix> S-3000` (3000 ohm), or the exact reverse (R-Part_Params-33). Open: Q-Part_Params-21 (which direction). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** Sorting by the entered text would give S-3000, S-1500, S-2k, S-900. A wrong order is a finding.

**Duplicate check:** 54 · Review · matches: [UI-Part_Params-067](parametric-tables-unit-aware-filtering-and-sorting.md) (54)

**Duplicate judgement:** Keep · Differs from UI-Part_Params-067 in rule (R-Part_Params-33 unit-aware sorting) and input class (values in explicit, different compatible units whose text order differs from numeric order) · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-070: What-if: parts without the parameter when sorting by it

| Field | Value |
|---|---|
| **Summary** | Checks whether, and where, a part that has no value for the parameter is listed when the table is sorted by that parameter (open: Q-Part_Params-21). |
| **Requirement** | `R-Part_Params-22`. Source: [concepts-parameters.md#L120](../../requirements/docs/concepts-parameters.md#L120) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | What-if business scenario (part without the parameter), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; extra part `QA-<suffix> R-none` in the category with no parameter; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-21 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Click the header of the Resistance column. | None | The parts are sorted by that parameter (R-Part_Params-22). |
| 3 | Find the part without a value. | Part: `QA-<suffix> R-none` | Proposed, to confirm in Q-Part_Params-21: `QA-<suffix> R-none` is still listed, after all parts that have a value. Open: Q-Part_Params-21 (whether it is placed first or last). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

---

### UI-Part_Params-071: Filter `>` (greater than) on a parameter with units

| Field | Value |
|---|---|
| **Summary** | A numeric filter with the operator `>` and the value `10k` keeps only the parts whose converted value satisfies it. |
| **Requirement** | `R-Part_Params-29`, `R-Part_Params-23`. Source: [concepts-parameters.md#L164-170](../../requirements/docs/concepts-parameters.md#L164-L170), [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) |
| **Area** | Part_Params |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (on the limit: 10000 ohm excluded), Equivalence partitioning (operator `>`) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Read the parts shown. | None | `>` means greater than (R-Part_Params-29). The table shows `QA-<suffix> R-47k`, `QA-<suffix> R-100k`, `QA-<suffix> R-1000k`; `QA-<suffix> R-500`, `QA-<suffix> R-4k7`, `QA-<suffix> R-10k` are not shown, `QA-<suffix> R-10k` being on the boundary (R-Part_Params-23). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 96 · Duplicate · matches: [UI-Part_Params-072](parametric-tables-unit-aware-filtering-and-sorting.md) (96), [UI-Part_Params-073](parametric-tables-unit-aware-filtering-and-sorting.md) (95), [UI-Part_Params-074](parametric-tables-unit-aware-filtering-and-sorting.md) (93), [UI-Part_Params-087](parametric-tables-unit-aware-filtering-and-sorting.md) (55), [UI-Part_Params-075](parametric-tables-unit-aware-filtering-and-sorting.md) (54), +1 more

**Duplicate judgement:** Keep · Every listed match differs in operator class and expected set: `>` excludes the 10k boundary part (072 `>=` includes it, 073/074 select the lower side, 075 `=` keeps only it, 087 combines two filters under R-Part_Params-26); the unlisted "+1 more" match was not visible to the reviewer · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-072: Filter `>=` (greater than or equal to) on a parameter with units

| Field | Value |
|---|---|
| **Summary** | A numeric filter with the operator `>=` and the value `10k` keeps only the parts whose converted value satisfies it. |
| **Requirement** | `R-Part_Params-29`, `R-Part_Params-23`. Source: [concepts-parameters.md#L164-170](../../requirements/docs/concepts-parameters.md#L164-L170), [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) |
| **Area** | Part_Params |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (on the limit: 10000 ohm included) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>=`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Read the parts shown. | None | `>=` means greater than or equal to (R-Part_Params-29). The table shows `QA-<suffix> R-10k`, `QA-<suffix> R-47k`, `QA-<suffix> R-100k`, `QA-<suffix> R-1000k`; `QA-<suffix> R-500`, `QA-<suffix> R-4k7` are not shown (R-Part_Params-23). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 96 · Duplicate · matches: [UI-Part_Params-071](parametric-tables-unit-aware-filtering-and-sorting.md) (96), [UI-Part_Params-074](parametric-tables-unit-aware-filtering-and-sorting.md) (94), [UI-Part_Params-073](parametric-tables-unit-aware-filtering-and-sorting.md) (92), [UI-Part_Params-075](parametric-tables-unit-aware-filtering-and-sorting.md) (55), [UI-Part_Params-087](parametric-tables-unit-aware-filtering-and-sorting.md) (55), +1 more

**Duplicate judgement:** Keep · Differs from every listed match in operator class and expected set: `>=` includes the 10k boundary part (071 `>` excludes it, 073/074 select the lower side, 075 `=` keeps only it, 087 is a two-filter range under R-Part_Params-26); the unlisted "+1 more" match was not visible to the reviewer · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-073: Filter `<` (less than) on a parameter with units

| Field | Value |
|---|---|
| **Summary** | A numeric filter with the operator `<` and the value `10k` keeps only the parts whose converted value satisfies it. |
| **Requirement** | `R-Part_Params-29`, `R-Part_Params-23`. Source: [concepts-parameters.md#L164-170](../../requirements/docs/concepts-parameters.md#L164-L170), [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) |
| **Area** | Part_Params |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (on the limit: 10000 ohm excluded) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `<`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Read the parts shown. | None | `<` means less than (R-Part_Params-29). The table shows `QA-<suffix> R-500`, `QA-<suffix> R-4k7`; `QA-<suffix> R-10k`, `QA-<suffix> R-47k`, `QA-<suffix> R-100k`, `QA-<suffix> R-1000k` are not shown, `QA-<suffix> R-10k` being on the boundary (R-Part_Params-23). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 98 · Duplicate · matches: [UI-Part_Params-074](parametric-tables-unit-aware-filtering-and-sorting.md) (98), [UI-Part_Params-071](parametric-tables-unit-aware-filtering-and-sorting.md) (95), [UI-Part_Params-072](parametric-tables-unit-aware-filtering-and-sorting.md) (92), [UI-Part_Params-087](parametric-tables-unit-aware-filtering-and-sorting.md) (57), [UI-Part_Params-075](parametric-tables-unit-aware-filtering-and-sorting.md) (53), +1 more

**Duplicate judgement:** Keep · Differs from every listed match in operator class and expected set: `<` excludes the 10k boundary part (074 `<=` includes it, 071/072 select the upper side, 075 `=` keeps only it, 087 is a two-filter range under R-Part_Params-26); the unlisted "+1 more" match was not visible to the reviewer · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-074: Filter `<=` (less than or equal to) on a parameter with units

| Field | Value |
|---|---|
| **Summary** | A numeric filter with the operator `<=` and the value `10k` keeps only the parts whose converted value satisfies it. |
| **Requirement** | `R-Part_Params-29`, `R-Part_Params-23`. Source: [concepts-parameters.md#L164-170](../../requirements/docs/concepts-parameters.md#L164-L170), [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) |
| **Area** | Part_Params |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (on the limit: 10000 ohm included) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `<=`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Read the parts shown. | None | `<=` means less than or equal to (R-Part_Params-29). The table shows `QA-<suffix> R-500`, `QA-<suffix> R-4k7`, `QA-<suffix> R-10k`; `QA-<suffix> R-47k`, `QA-<suffix> R-100k`, `QA-<suffix> R-1000k` are not shown (R-Part_Params-23). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 98 · Duplicate · matches: [UI-Part_Params-073](parametric-tables-unit-aware-filtering-and-sorting.md) (98), [UI-Part_Params-072](parametric-tables-unit-aware-filtering-and-sorting.md) (94), [UI-Part_Params-071](parametric-tables-unit-aware-filtering-and-sorting.md) (93), [UI-Part_Params-087](parametric-tables-unit-aware-filtering-and-sorting.md) (57), [UI-Part_Params-075](parametric-tables-unit-aware-filtering-and-sorting.md) (54), +1 more

**Duplicate judgement:** Keep · Differs from every listed match in operator class and expected set: `<=` includes the 10k boundary part (073 `<` excludes it, 071/072 select the upper side, 075 `=` keeps only it, 087 is a two-filter range under R-Part_Params-26); the unlisted "+1 more" match was not visible to the reviewer · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-075: Filter `=` (equal to) on a parameter with units

| Field | Value |
|---|---|
| **Summary** | A numeric filter with the operator `=` and the value `10k` keeps only the parts whose converted value satisfies it. |
| **Requirement** | `R-Part_Params-29`, `R-Part_Params-23`. Source: [concepts-parameters.md#L164-170](../../requirements/docs/concepts-parameters.md#L164-L170), [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (operator `=`) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `=`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Read the parts shown. | None | `=` means equal to (R-Part_Params-29). The table shows `QA-<suffix> R-10k`; the other five parts are not shown (R-Part_Params-23). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 83 · Duplicate · matches: [UI-Part_Params-076](parametric-tables-unit-aware-filtering-and-sorting.md) (83), [UI-Part_Params-077](parametric-tables-unit-aware-filtering-and-sorting.md) (70), [UI-Part_Params-072](parametric-tables-unit-aware-filtering-and-sorting.md) (55), [UI-Part_Params-071](parametric-tables-unit-aware-filtering-and-sorting.md) (54), [UI-Part_Params-074](parametric-tables-unit-aware-filtering-and-sorting.md) (54), +2 more

**Duplicate judgement:** Keep · Differs from every listed match: `=` keeps only the 10k part, the complement of 076 `!=`; 077 is a text parameter with `~`; 071, 072 and 074 are range operators with other expected sets; the two unlisted "+2 more" matches were not visible to the reviewer · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-076: Filter `!=` (not equal to) on a parameter with units

| Field | Value |
|---|---|
| **Summary** | A numeric filter with `!=` and the value `10k` removes the part whose converted value is 10000 ohm. |
| **Requirement** | `R-Part_Params-29`, `R-Part_Params-23`. Source: [concepts-parameters.md#L164-170](../../requirements/docs/concepts-parameters.md#L164-L170), [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (operator `!=`) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `!=`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Read the parts shown. | None | `!=` means not equal to (R-Part_Params-29). The table shows `QA-<suffix> R-500`, `QA-<suffix> R-4k7`, `QA-<suffix> R-47k`, `QA-<suffix> R-100k`, `QA-<suffix> R-1000k`; `QA-<suffix> R-10k` is not shown (R-Part_Params-23). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 83 · Duplicate · matches: [UI-Part_Params-075](parametric-tables-unit-aware-filtering-and-sorting.md) (83), [UI-Part_Params-077](parametric-tables-unit-aware-filtering-and-sorting.md) (65), [UI-Part_Params-072](parametric-tables-unit-aware-filtering-and-sorting.md) (52), [UI-Part_Params-071](parametric-tables-unit-aware-filtering-and-sorting.md) (51), [UI-Part_Params-074](parametric-tables-unit-aware-filtering-and-sorting.md) (51), +2 more

**Duplicate judgement:** Keep · Differs from every listed match: `!=` drops only the 10k part, the complement of 075 `=`; 077 is a text parameter with `~`; 071, 072 and 074 are range operators with other expected sets; the two unlisted "+2 more" matches were not visible to the reviewer · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-077: Filter `~` (contains) on a text parameter

| Field | Value |
|---|---|
| **Summary** | The contains operator on a text parameter keeps only parts whose value contains the entered text. |
| **Requirement** | `R-Part_Params-29`, `R-Part_Params-23`. Source: [concepts-parameters.md#L164-170](../../requirements/docs/concepts-parameters.md#L164-L170), [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: text parameter, operator `~`) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Series` (no Units, Model Type blank); category `QA-<suffix> Series Cat`; three parts with a `QA-<suffix> Series` parameter: `QA-<suffix> T-1` = `Alpha-100`, `QA-<suffix> T-2` = `Beta-200`, `QA-<suffix> T-3` = `Gamma-300`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Series Cat`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19, Q-Part_Params-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Series` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Series column. | Operator: `~`<br>Value: `-2` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Read the parts shown. | None | `~` means contains, for text parameters (R-Part_Params-29). The table shows `QA-<suffix> T-2` (`Beta-200`); `QA-<suffix> T-1` and `QA-<suffix> T-3` are not shown. Open: Q-Part_Params-22 (case sensitivity of `~`). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Series`.

**Notes:** None

**Duplicate check:** 70 · Review · matches: [UI-Part_Params-075](parametric-tables-unit-aware-filtering-and-sorting.md) (70), [UI-Part_Params-076](parametric-tables-unit-aware-filtering-and-sorting.md) (65)

**Duplicate judgement:** Keep · Differs from UI-Part_Params-075 and UI-Part_Params-076 in parameter type (text template with no units vs ohm template) and operator (`~` contains vs `=`/`!=`), with different data and expected parts · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-078: The `~` operator is only for text parameters

| Field | Value |
|---|---|
| **Summary** | A filter on a numeric parameter with units does not offer the contains operator. |
| **Requirement** | `R-Part_Params-29`, `R-Part_Params-23`. Source: [concepts-parameters.md#L164-170](../../requirements/docs/concepts-parameters.md#L164-L170), [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Negative (operator not valid for the parameter type), Decision table (type x operator) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19, Q-Part_Params-22 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Open the filter dialog of the Resistance column and look at the operators. | None | `~` is available for text parameters (R-Part_Params-29). Open: Q-Part_Params-19 (the dialog). Proposed, to confirm in Q-Part_Params-22: `~` is not offered for a numeric parameter. |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

---

### UI-Part_Params-079: Unit-aware filter: `10k` and `10000` give the same result

| Field | Value |
|---|---|
| **Summary** | On a parameter with unit ohm, a filter value of `10k` and one of `10000` are both read as 10000 ohm. |
| **Requirement** | `R-Part_Params-27`. Source: [concepts-parameters.md#L148-150](../../requirements/docs/concepts-parameters.md#L148-L150) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: same quantity in two notations) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Read the parts shown. | None | The table shows `QA-<suffix> R-47k`, `QA-<suffix> R-100k`, `QA-<suffix> R-1000k` (R-Part_Params-27). |
| 4 | Remove the filter and add the same filter with the plain number. | Operator: `>`<br>Value: `10000` | The filter is added. Open: Q-Part_Params-19 (the remove and filter controls). |
| 5 | Read the parts shown. | None | The same three parts are shown: `10k` and `10000` are both read as 10,000 ohms (R-Part_Params-27). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 51 · Review · matches: [UI-Part_Params-080](parametric-tables-unit-aware-filtering-and-sorting.md) (51)

**Duplicate judgement:** Keep · Differs from UI-Part_Params-080 in input class and operator: SI-prefix shorthand `10k` against the plain base-unit number `10000` with `>`, while 080 uses an explicit compatible unit `10 kohm` with `=` · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-080: Unit-aware filter: a value with an explicit compatible unit is converted

| Field | Value |
|---|---|
| **Summary** | A filter value written with a different, compatible unit (`10 kohm`) is converted to the template's base unit ohm. |
| **Requirement** | `R-Part_Params-27`, `R-Part_Params-30`. Source: [concepts-parameters.md#L148-150](../../requirements/docs/concepts-parameters.md#L148-L150), [concepts-parameters.md#L174-176](../../requirements/docs/concepts-parameters.md#L174-L176) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: explicit compatible unit) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `=`<br>Value: `10 kohm` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Read the parts shown. | None | The table shows only `QA-<suffix> R-10k`: the system converts the value to the base unit defined for the template (R-Part_Params-27). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 52 · Review · matches: [UI-Part_Params-075](parametric-tables-unit-aware-filtering-and-sorting.md) (52), [UI-Part_Params-076](parametric-tables-unit-aware-filtering-and-sorting.md) (51), [UI-Part_Params-079](parametric-tables-unit-aware-filtering-and-sorting.md) (51)

**Duplicate judgement:** Keep · Closest is UI-Part_Params-075 (same operator `=` and same expected part), but the input class differs: an explicit compatible unit `10 kohm` that must be converted to ohm (R-Part_Params-27) vs the prefix shorthand `10k`; 076 and 079 differ in operator and input · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-081: A filter value with a unit incompatible with the template is not accepted

| Field | Value |
|---|---|
| **Summary** | A filter value in an unrelated unit (`10 kg`) on an ohm parameter is not applied as a normal filter. |
| **Requirement** | `R-Part_Params-27`. Source: [concepts-parameters.md#L148-150](../../requirements/docs/concepts-parameters.md#L148-L150) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: incompatible unit) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19, Q-Part_Params-20 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `=`<br>Value: `10 kg` | The value is entered in the filter field. Open: Q-Part_Params-19 (the filter button, dialog and field labels), Q-Part_Params-20 (whether the value is refused here or when the filter is applied). |
| 3 | Read the table and any message. | None | Filters accept any compatible unit (R-Part_Params-27). Proposed, to confirm in Q-Part_Params-20: the filter is not applied and an error is shown. Open: Q-Part_Params-20 (the error text). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 73 · Review · matches: [UI-Part_Params-082](parametric-tables-unit-aware-filtering-and-sorting.md) (73)

**Duplicate judgement:** Keep · Differs from UI-Part_Params-082 in invalid class: a numeric value with an incompatible unit (`10 kg`) vs a non-numeric value (`abc`) · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-082: A non-numeric filter value on a parameter with units is not accepted

| Field | Value |
|---|---|
| **Summary** | A text filter value (`abc`) on a numeric ohm parameter is not applied as a normal filter. |
| **Requirement** | `R-Part_Params-27`, `R-Part_Params-29`. Source: [concepts-parameters.md#L148-150](../../requirements/docs/concepts-parameters.md#L148-L150), [concepts-parameters.md#L164-170](../../requirements/docs/concepts-parameters.md#L164-L170) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19, Q-Part_Params-20 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `=`<br>Value: `abc` | The value is entered in the filter field. Open: Q-Part_Params-19 (the filter button, dialog and field labels), Q-Part_Params-20 (whether the value is refused here or when the filter is applied). |
| 3 | Read the table and any message. | None | Proposed, to confirm in Q-Part_Params-20: the filter is not applied and an error is shown. Open: Q-Part_Params-20 (the error text). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 73 · Review · matches: [UI-Part_Params-081](parametric-tables-unit-aware-filtering-and-sorting.md) (73)

**Duplicate judgement:** Keep · Differs from UI-Part_Params-081 in invalid class: a non-numeric value (`abc`) vs a numeric value with an incompatible unit (`10 kg`) · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-083: A filter with an empty value is not applied

| Field | Value |
|---|---|
| **Summary** | Submitting a numeric filter with no value does not change the table. |
| **Requirement** | `R-Part_Params-23`. Source: [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty), Error guessing (whitespace-only) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19, Q-Part_Params-20 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column with an empty value, then with a single space. | Operator: `>`<br>Value: empty, then ` ` | Open: Q-Part_Params-19 (the dialog). |
| 3 | Read the table and any message. | None | Proposed, to confirm in Q-Part_Params-20: the filter is not applied, the six parts stay listed, and an error is shown. Open: Q-Part_Params-20 (the error text). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

---

### UI-Part_Params-084: A parameter with a limited set of choices is filtered by those choices

| Field | Value |
|---|---|
| **Summary** | The filter on a parameter with Choices offers those choices, and selecting one keeps only matching parts. |
| **Requirement** | `R-Part_Params-23`. Source: [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: choices parameter), Decision table (parameter type x filter options) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Colour` (no Units, Choices `Red,Green,Blue`); category `QA-<suffix> Colour Cat`; three parts with a `QA-<suffix> Colour` parameter: `QA-<suffix> C-1` = `Red`, `QA-<suffix> C-2` = `Green`, `QA-<suffix> C-3` = `Blue`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Colour Cat`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Colour` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Open the filter of the Colour column. | None | A parameter with a limited set of choices allows filtering by those choices (R-Part_Params-23). Open: Q-Part_Params-19 (how the choices are presented). |
| 3 | Select one choice and apply. | Choice: `Green` | Only `QA-<suffix> C-2` is shown (R-Part_Params-23). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Colour`.

**Notes:** None

---

### UI-Part_Params-085: Filters on two different parameters show only parts that match both

| Field | Value |
|---|---|
| **Summary** | A filter on Resistance and a filter on Tolerance leave only parts that satisfy both. |
| **Requirement** | `R-Part_Params-24`. Source: [concepts-parameters.md#L134](../../requirements/docs/concepts-parameters.md#L134) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Decision table (filter A on, filter B on) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; second template `QA-<suffix> Tolerance` (Units `percent`) with a value on each part: `QA-<suffix> R-500` = `10`, `QA-<suffix> R-4k7` = `5`, `QA-<suffix> R-10k` = `1`, `QA-<suffix> R-47k` = `1`, `QA-<suffix> R-100k` = `5`, `QA-<suffix> R-1000k` = `10`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Add a filter on the Tolerance column. | Operator: `=`<br>Value: `1` | A new filter is added for the second parameter (R-Part_Params-24). Open: Q-Part_Params-19 (the filter controls). |
| 4 | Read the parts shown. | None | Only parts that match all filters are shown: `QA-<suffix> R-47k` (47k ohm, 1). `QA-<suffix> R-100k` and `QA-<suffix> R-1000k` (greater than 10k but not 1) and `QA-<suffix> R-10k` (1 but not greater than 10k) are not shown (R-Part_Params-24). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and both templates.

**Notes:** None

---

### UI-Part_Params-086: Each parameter column shows whether a filter is applied

| Field | Value |
|---|---|
| **Summary** | A column with an active filter shows an indicator, and a column without a filter does not. |
| **Requirement** | `R-Part_Params-25`. Source: [concepts-parameters.md#L136](../../requirements/docs/concepts-parameters.md#L136) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | State transition (no filter to filter applied), Decision table (column with / without filter) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; second template `QA-<suffix> Tolerance` (Units `percent`) with a value on each part: `QA-<suffix> R-500` = `10`, `QA-<suffix> R-4k7` = `5`, `QA-<suffix> R-10k` = `1`, `QA-<suffix> R-47k` = `1`, `QA-<suffix> R-100k` = `5`, `QA-<suffix> R-1000k` = `10`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Compare the Resistance and Tolerance column headers. | None | The Resistance column indicates that a filter is applied; the Tolerance column does not (R-Part_Params-25). Open: Q-Part_Params-19 (how the indication looks). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and both templates.

**Notes:** None

---

### UI-Part_Params-087: Two filters on the same parameter give a range

| Field | Value |
|---|---|
| **Summary** | Greater than 10k and less than 100k on the same parameter keep only the parts between the limits. |
| **Requirement** | `R-Part_Params-26`, `R-Part_Params-29`. Source: [concepts-parameters.md#L142](../../requirements/docs/concepts-parameters.md#L142), [concepts-parameters.md#L164-170](../../requirements/docs/concepts-parameters.md#L164-L170) |
| **Area** | Part_Params |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (both limits excluded: 10k and 100k), Equivalence partitioning (range inside) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Add a second filter on the same column. | Operator: `<`<br>Value: `100k` | Several filters can be applied to the same parameter (R-Part_Params-26). Open: Q-Part_Params-19 (the controls). |
| 4 | Read the parts shown. | None | Only `QA-<suffix> R-47k` is shown; `QA-<suffix> R-10k` and `QA-<suffix> R-100k` are on the limits and excluded, and `QA-<suffix> R-500`, `QA-<suffix> R-4k7`, `QA-<suffix> R-1000k` are outside (R-Part_Params-26). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 57 · Review · matches: [UI-Part_Params-073](parametric-tables-unit-aware-filtering-and-sorting.md) (57), [UI-Part_Params-074](parametric-tables-unit-aware-filtering-and-sorting.md) (57), [UI-Part_Params-071](parametric-tables-unit-aware-filtering-and-sorting.md) (55), [UI-Part_Params-072](parametric-tables-unit-aware-filtering-and-sorting.md) (55)

**Duplicate judgement:** Keep · Differs from UI-Part_Params-071 to 074 in rule and outcome: two filters on the same parameter (R-Part_Params-26) combining into a range that keeps only the 47k part, while each match applies a single operator · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-088: Contradictory filters on the same parameter leave an empty table

| Field | Value |
|---|---|
| **Summary** | Greater than 100k and less than 10k on the same parameter match no part. |
| **Requirement** | `R-Part_Params-26`. Source: [concepts-parameters.md#L142](../../requirements/docs/concepts-parameters.md#L142) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Error guessing (contradictory filters) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>`<br>Value: `100k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Add a second filter on the same column. | Operator: `<`<br>Value: `10k` | Several filters can be applied to the same parameter (R-Part_Params-26). Open: Q-Part_Params-19 (the controls). |
| 4 | Read the table. | None | No part is shown, because only parts matching all filters are shown (R-Part_Params-24, R-Part_Params-26). Open: Q-Part_Params-19 (the empty-state text). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

---

### UI-Part_Params-089: Removing one of two filters on a parameter keeps the other

| Field | Value |
|---|---|
| **Summary** | With a range filter on one parameter, removing the upper limit leaves the lower limit in force. |
| **Requirement** | `R-Part_Params-28`, `R-Part_Params-26`. Source: [concepts-parameters.md#L156](../../requirements/docs/concepts-parameters.md#L156), [concepts-parameters.md#L142](../../requirements/docs/concepts-parameters.md#L142) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | State transition (two filters to one filter) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Add a second filter on the same column. | Operator: `<`<br>Value: `100k` | Only `QA-<suffix> R-47k` is shown (R-Part_Params-26). |
| 4 | Remove the `<` `100k` filter with its remove button. | None | A filter is removed with its remove button (R-Part_Params-28). Open: Q-Part_Params-19 (the button, an icon not rendered in the docs). |
| 5 | Read the parts shown. | None | The `>` `10k` filter is still applied: `QA-<suffix> R-47k`, `QA-<suffix> R-100k`, `QA-<suffix> R-1000k` are shown (R-Part_Params-26). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 53 · Review · matches: [UI-Part_Params-090](parametric-tables-unit-aware-filtering-and-sorting.md) (53)

**Duplicate judgement:** Keep · Differs from UI-Part_Params-090 in starting state and outcome: two filters to one, with the remaining `>` 10k filter still applied, while 090 goes from one filter to none and the full table · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-090: Removing the only filter restores the full table

| Field | Value |
|---|---|
| **Summary** | After the single filter is removed, all six parts are listed again. |
| **Requirement** | `R-Part_Params-28`. Source: [concepts-parameters.md#L156](../../requirements/docs/concepts-parameters.md#L156) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | State transition (filtered to unfiltered) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Remove the filter with its remove button. | None | A filter is removed with its remove button (R-Part_Params-28). Open: Q-Part_Params-19 (the button). |
| 4 | Read the parts shown and the column header. | None | All six parts are listed again. Proposed, to confirm in Q-Part_Params-19: the column no longer indicates a filter (R-Part_Params-25). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

**Duplicate check:** 53 · Review · matches: [UI-Part_Params-089](parametric-tables-unit-aware-filtering-and-sorting.md) (53)

**Duplicate judgement:** Keep · Differs from UI-Part_Params-089 in starting state and outcome: one filter to none, with all six parts restored and the column indicator cleared, while 089 keeps one of two filters in force · test-case-reviewer, 2026-10-15

---

### UI-Part_Params-091: A filtered table can be sorted by converted value

| Field | Value |
|---|---|
| **Summary** | A filter and a sort on the same parameter work together: the filtered parts are ordered by converted value. |
| **Requirement** | `R-Part_Params-23`, `R-Part_Params-33`, `R-Part_Params-27`. Source: [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130), [concepts-parameters.md#L191](../../requirements/docs/concepts-parameters.md#L191), [concepts-parameters.md#L148-150](../../requirements/docs/concepts-parameters.md#L148-L150) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Decision table (filter on x sort on) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`); category `QA-<suffix> Sorting`; four parts with a `QA-<suffix> Resistance` parameter: `QA-<suffix> S-900` = `900 ohm`, `QA-<suffix> S-1500` = `1500 ohm`, `QA-<suffix> S-2k` = `2 kohm`, `QA-<suffix> S-3000` = `0.003 Mohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Sorting`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19, Q-Part_Params-21 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>`<br>Value: `1 kohm` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Click the header of the Resistance column. | None | Sorting takes unit conversion into account (R-Part_Params-33). Open: Q-Part_Params-21 (the direction). |
| 4 | Read the parts shown. | None | Only `QA-<suffix> S-1500`, `QA-<suffix> S-2k` and `QA-<suffix> S-3000` are shown (R-Part_Params-27); `QA-<suffix> S-900` is not. They are ordered by converted value 1500, 2000, 3000 ohm, or the exact reverse (R-Part_Params-33). Open: Q-Part_Params-21 (which direction). |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

---

### UI-Part_Params-092: What-if: a parameter value edited while a filter is applied

| Field | Value |
|---|---|
| **Summary** | After a part's value is changed so that it passes the filter, the part appears in the filtered table. |
| **Requirement** | `R-Part_Params-23`, `R-Part_Params-27`. Source: [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130), [concepts-parameters.md#L148-150](../../requirements/docs/concepts-parameters.md#L148-L150) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | What-if business scenario (value edited after the filter), State transition (excluded to included) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Open the part `QA-<suffix> R-4k7`, change its `QA-<suffix> Resistance` parameter to `22k` on the Parameters tab [open: Q-Part_Params-19, the edit control], and save. | Value: `22k` | Proposed, to confirm in Q-Part_Params-19: the new value `22k` is saved. No rule describes editing a parameter value. |
| 4 | Return to the category and reopen the parametric view with the same filter. | Operator: `>`<br>Value: `10k` | `QA-<suffix> R-4k7` (now 22000 ohm) is shown with `QA-<suffix> R-47k`, `QA-<suffix> R-100k`, `QA-<suffix> R-1000k` (R-Part_Params-23). Open: Q-Part_Params-19 (whether the filter is kept when the user returns). |

**Postconditions and cleanup:** the `QA-<suffix> Resistance` value of `QA-<suffix> R-4k7` is now `22k`. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** editing an existing parameter value is not described in the docs (Q-Part_Params-19 asks whether it can be done from the Parameters tab).

---

### UI-Part_Params-093: The parametric view of a parent category includes parts of its sub-categories

| Field | Value |
|---|---|
| **Summary** | The parametric table of a parent category lists the parts of its sub-categories as the category part list does. |
| **Requirement** | `R-Part_Params-21`, `R-Categories-02`. Source: [concepts-parameters.md#L112-114](../../requirements/docs/concepts-parameters.md#L112-L114), [part-index.md#L31](../../requirements/docs/part-index.md#L31) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Exploratory (charter: parametric view across the category tree) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`); categories `QA-<suffix> Resistors` > `QA-<suffix> Resistors Sub`; `QA-<suffix> R-10k` = `10k` in `QA-<suffix> Resistors`, `QA-<suffix> R-47k` = `47k` in `QA-<suffix> Resistors Sub`; created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the category's normal part list. | None | `QA-<suffix> R-10k` and `QA-<suffix> R-47k` are listed (R-Categories-02). |
| 2 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 3 | Read the parts in the parametric table. | None | Proposed, to confirm in Q-Part_Params-18: `QA-<suffix> R-10k` and `QA-<suffix> R-47k` are both listed with their Resistance values. |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete both categories and the template `QA-<suffix> Resistance`.

**Notes:** None

---

### UI-Part_Params-094: A view-only user can use the parametric view

| Field | Value |
|---|---|
| **Summary** | A user with view-only access can open the parametric view, filter and sort. |
| **Requirement** | `R-Part_Params-21`, `R-Part_Params-22`, `R-Part_Params-23`. Source: [concepts-parameters.md#L112-114](../../requirements/docs/concepts-parameters.md#L112-L114), [concepts-parameters.md#L120](../../requirements/docs/concepts-parameters.md#L120), [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) |
| **Area** | Part_Params |
| **Type** | Positive |
| **Technique** | Negative (reader), Decision table (role x action) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-18, Q-Part_Params-19, Q-Part_Params-23 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the parametric view of the category's part list. | Press the *Parametric View* button | The parametric parts table opens with a column for the parameter `QA-<suffix> Resistance` (R-Part_Params-21). Open: Q-Part_Params-18 (the button's label and location). |
| 2 | Add a filter on the Resistance column. | Operator: `>`<br>Value: `10k` | The filter is added (R-Part_Params-23). Open: Q-Part_Params-19 (the filter button, dialog and field labels). |
| 3 | Click the header of the Resistance column. | None | Proposed, to confirm in Q-Part_Params-23: the filter and the sort work for a view-only user (R-Part_Params-22, R-Part_Params-23). |
| 4 | Look for controls that change parameters. | None | Proposed, to confirm in Q-Part_Params-23: none are shown. |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

---

### UI-Part_Params-095: A user with no permissions cannot use the parametric view

| Field | Value |
|---|---|
| **Summary** | A user without any role cannot reach the parametric table of parts. |
| **Requirement** | `R-Part_Params-21`. Source: [concepts-parameters.md#L112-114](../../requirements/docs/concepts-parameters.md#L112-L114) |
| **Area** | Part_Params |
| **Type** | Negative |
| **Technique** | Negative (noaccess) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess` (no permissions); Settings: None; Data: template `QA-<suffix> Resistance` (Units `ohm`, no uniqueness); category `QA-<suffix> Resistors`; six parts in it, each with a `QA-<suffix> Resistance` parameter: `QA-<suffix> R-500` = `500`, `QA-<suffix> R-4k7` = `4.7k`, `QA-<suffix> R-10k` = `10k`, `QA-<suffix> R-47k` = `47k`, `QA-<suffix> R-100k` = `100k`, `QA-<suffix> R-1000k` = `1000 kohm`; all created as `admin`; Pre-steps: log in through the login form, open the *Parts* view, open the category `QA-<suffix> Resistors`. The category address is read as `admin` beforehand. |
| **Automation** | Partial: the filter controls are not named in the docs. |
| **Review** | Draft · Open question: Q-Part_Params-23 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Parts* view. | None | Not known: depends on open question Q-Part_Params-23 (whether the view is hidden, empty or refused). |
| 2 | Open the category by its address. | Address: the category page of `QA-<suffix> Resistors` | Proposed, to confirm in Q-Part_Params-23: no part, parameter value or *Parametric View* button is shown. |

**Postconditions and cleanup:** Nothing changed. Cleanup as `admin`: set the parts inactive and delete them, then delete the category and the template `QA-<suffix> Resistance`.

**Notes:** None

---
