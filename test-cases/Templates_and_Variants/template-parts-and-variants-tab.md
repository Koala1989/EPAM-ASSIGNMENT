# Template parts and the Variants tab: Part_Template test cases

Template option, creating variants from the *Variants* tab, serial number and stock rules across variants, test template cascading and inherited BOM lines. Data is created through the API as `admin`; the variant rules about revisions are in `Revisions` (R-REV-08 to R-REV-10).

---

### UI-Part_Template-001: A user can switch the Template option on for a part that is not a template.

| Field | Value |
|---|---|
| **Summary** | A user can switch the Template option on for a part that is not a template. |
| **Requirement** | `R-Part_Template-01`, `R-Part_Template-02`. Source: [part-template.md#Enable Template Part](../../requirements/docs/part-template.md#L32); [part-template.md#Enable Template Part](../../requirements/docs/part-template.md#L34-L37) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | State transition (not template to template) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Plain` (Template off), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Plain`. |
| **Automation** | Partial: the toggle location is unconfirmed. |
| **Review** | Draft · Open question: Q-Part_Template-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part detail page of `QA-<suffix> Plain`. | None | The page shows no *Variants* tab (R-Detail_View-08). |
| 2 | Locate the part options where the Template option is toggled. | None | The Template option is shown off. Open: Q-Part_Template-01 (the docs say the *Details* tab, part options on the right-hand side; the 1.5.6 location and label may differ). |
| 3 | Switch the Template option on. | None | The option shows on (green, slider to the right) (R-Part_Template-02). Open: Q-Part_Template-01 (whether a form or a confirmation is involved, and the save step). |
| 4 | Reload the part detail page. | None | The Template option is still on (R-Part_Template-01) and the *Variants* tab is visible (R-Detail_View-08). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** Doc issue 9 in the index: the described UI path may be outdated. Related: Q-Detail_View-20.

---

### UI-Part_Template-002: A part created as a Template shows the Variants tab on its detail page.

| Field | Value |
|---|---|
| **Summary** | A part created as a Template shows the Variants tab on its detail page. |
| **Requirement** | `R-Part_Template-01`, `R-Detail_View-08`. Source: [part-template.md#Enable Template Part](../../requirements/docs/part-template.md#L32); [part-views.md#Variants](../../requirements/docs/part-views.md#L52) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: part with Template on) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part detail page of `QA-<suffix> Template`. | None | The *Variants* tab is visible (R-Detail_View-08, R-Part_Template-01). |
| 2 | Select the *Variants* tab. | None | The tab opens and shows the variants panel of the template. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-003: A part that is not a Template has no Variants tab.

| Field | Value |
|---|---|
| **Summary** | A part that is not a Template has no Variants tab. |
| **Requirement** | `R-Detail_View-08`. Source: [part-views.md#Variants](../../requirements/docs/part-views.md#L52) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Negative (tab visible only if Template) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Plain` (Template off), created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Plain`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part detail page of `QA-<suffix> Plain`. | None | The *Variants* tab is not in the tab list (R-Detail_View-08: visible only if the part is a Template part). |
| 2 | Edit the URL to the Variants panel of the part, if the browser URL names the panel. | Panel name as shown in the URL of the template's *Variants* tab | The panel is not shown for this part. Proposed, to confirm in Q-Part_Template-07: the page falls back to the default tab. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-004: The Template option is off by default for a part created without it.

| Field | Value |
|---|---|
| **Summary** | The Template option is off by default for a part created without it. |
| **Requirement** | `R-Part_Template-01`. Source: [part-template.md#Enable Template Part](../../requirements/docs/part-template.md#L32) |
| **Area** | Part_Template |
| **Type** | Boundary |
| **Technique** | Equivalence partitioning (class: Template not set) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Plain` (no Template value sent), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Plain`. |
| **Automation** | Partial: toggle location unconfirmed. |
| **Review** | Draft · Open question: Q-Part_Template-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part detail page of `QA-<suffix> Plain`. | None | No *Variants* tab is shown (R-Detail_View-08). |
| 2 | Look at the Template option in the part options. | None | Proposed, to confirm in Q-Part_Template-01: the option is off. Open: Q-Part_Template-01 (location and label). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** The docs do not state a default for Template, so the default is proposed.

---

### UI-Part_Template-005: A user with view-only access cannot switch the Template option.

| Field | Value |
|---|---|
| **Summary** | A user with view-only access cannot switch the Template option. |
| **Requirement** | `R-Part_Template-02`. Source: [part-template.md#Enable Template Part](../../requirements/docs/part-template.md#L34-L37) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Negative (blocked user) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Plain` (Template off), created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Plain`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part detail page of `QA-<suffix> Plain`. | None | The page opens. No *Variants* tab is shown (R-Detail_View-08). |
| 2 | Look for the control that toggles the Template option. | None | Proposed, to confirm in Q-Part_Template-01: the control is hidden or disabled, and the part cannot be changed to a Template by `reader`. Open: Q-Part_Template-01 (control location). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-006: Switching the Template option off, on a template with no variants, removes the Variants tab.

| Field | Value |
|---|---|
| **Summary** | Switching the Template option off, on a template with no variants, removes the Variants tab. |
| **Requirement** | `R-Part_Template-01`, `R-Part_Template-02`, `R-Detail_View-08`. Source: [part-template.md#Enable Template Part](../../requirements/docs/part-template.md#L32); [part-template.md#Enable Template Part](../../requirements/docs/part-template.md#L34-L37); [part-views.md#Variants](../../requirements/docs/part-views.md#L52) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | State transition (template to not template) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part detail page of `QA-<suffix> Template`. | None | The *Variants* tab is visible (R-Detail_View-08). |
| 2 | Switch the Template option off. | None | The option shows off. Open: Q-Part_Template-01 (location, label, save step). |
| 3 | Reload the part detail page. | None | The *Variants* tab is not in the tab list (R-Detail_View-08: visible only if the part is a Template part). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-007: Switching the Template option off on a template that already has a variant.

| Field | Value |
|---|---|
| **Summary** | Switching the Template option off on a template that already has a variant. |
| **Requirement** | `R-Part_Template-01`, `R-Part_Template-05`. Source: [part-template.md#Enable Template Part](../../requirements/docs/part-template.md#L32); [part-template.md#Part Templates](../../requirements/docs/part-template.md#L20) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | What-if business scenario (template switched off after variants exist) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`, plus variant `QA-<suffix> Variant A` (`variant_of` = the template); Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-01, Q-Part_Template-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part detail page of `QA-<suffix> Template` and switch the Template option off. | None | Proposed, to confirm in Q-Part_Template-04: the change is blocked with an error while a variant exists, and the Template option stays on. Open: Q-Part_Template-04 (the error text), Q-Part_Template-01 (control location). |
| 2 | Reload the page and open the detail page of `QA-<suffix> Variant A`. | None | Proposed, to confirm in Q-Part_Template-04: `QA-<suffix> Variant A` still exists and still references `QA-<suffix> Template` as its template. No rule states what happens to a variant when its template's option is switched off; Q-Part_Template-04 lists keeping or deleting the variants as possible outcomes. |
| 3 | Look at the tab list of `QA-<suffix> Template`. | None | Proposed, to confirm in Q-Part_Template-04: the *Variants* tab is still shown, because the option stayed on. If the option was switched off, the tab is hidden (R-Detail_View-08: visible only if the part is a Template). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** Q-Detail_View-20 asks a similar question for the tab; this case adds the effect on existing variants.

---

### UI-Part_Template-008: A variant is created from the Variants tab with New Variant and the Duplicate Part form.

| Field | Value |
|---|---|
| **Summary** | A variant is created from the Variants tab with New Variant and the Duplicate Part form. |
| **Requirement** | `R-Part_Template-04`, `R-Part_Template-05`. Source: [part-template.md#Create Variant](../../requirements/docs/part-template.md#L43-L44); [part-template.md#Part Templates](../../requirements/docs/part-template.md#L20) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: all required fields filled) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`, select the *Variants* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-02, Q-Part_Template-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the *New Variant* button on the *Variants* tab. | None | The *Duplicate Part* form opens (R-Part_Template-04). Open: Q-Part_Template-02 (which fields are prefilled from the template, and whether *Variant Of* is set). |
| 2 | Fill in the form. | Name: `QA-<suffix> Variant A`<br>Description: `Variant test part` | Fields accept the values. Open: Q-Part_Template-02 (which fields are required). |
| 3 | Press *Submit*. | None | The variant is created (R-Part_Template-04). Open: Q-Part_Template-02 (whether the browser goes to the new part's page or stays on the template). |
| 4 | Look at the *Variants* tab of the template. | None | `QA-<suffix> Variant A` is listed (R-Part_Template-04). Open: Q-Part_Template-07 (column layout). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-009: A variant created from a template references the template part.

| Field | Value |
|---|---|
| **Summary** | A variant created from a template references the template part. |
| **Requirement** | `R-Part_Template-05`, `R-Part_Template-04`. Source: [part-template.md#Part Templates](../../requirements/docs/part-template.md#L20); [part-template.md#Create Variant](../../requirements/docs/part-template.md#L43-L44) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: variant created through the form) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`, create `QA-<suffix> Variant A` with *New Variant* and *Submit*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-02, Q-Part_Template-09 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the detail page of `QA-<suffix> Variant A`. | None | The page opens. Open: Q-Part_Template-02 (navigation after Submit). |
| 2 | Look for the reference to the template part on the detail page. | None | The variant references `QA-<suffix> Template` (R-Part_Template-05: variant parts reference the template part, creating and showing a direct relationship). Open: Q-Part_Template-09 (the label and where it is shown). |
| 3 | Follow the reference. | None | The detail page of `QA-<suffix> Template` opens. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-010: A template with no variants shows an empty Variants tab.

| Field | Value |
|---|---|
| **Summary** | A template with no variants shows an empty Variants tab. |
| **Requirement** | `R-Part_Template-04`, `R-Detail_View-08`. Source: [part-template.md#Create Variant](../../requirements/docs/part-template.md#L43-L44); [part-views.md#Variants](../../requirements/docs/part-views.md#L52) |
| **Area** | Part_Template |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (count of variants = 0) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the *Variants* tab. | None | The tab opens with no variant row. The *New Variant* button is available (R-Part_Template-04). Open: Q-Part_Template-07 (empty-state text). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-011: The Variants tab lists several variants of the template.

| Field | Value |
|---|---|
| **Summary** | The Variants tab lists several variants of the template. |
| **Requirement** | `R-Part_Template-04`, `R-Part_Template-05`. Source: [part-template.md#Create Variant](../../requirements/docs/part-template.md#L43-L44); [part-template.md#Part Templates](../../requirements/docs/part-template.md#L20) |
| **Area** | Part_Template |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (count of variants = 2) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`, plus variant `QA-<suffix> Variant A` (`variant_of` = the template) and `QA-<suffix> Variant B`; Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select the *Variants* tab. | None | Both `QA-<suffix> Variant A` and `QA-<suffix> Variant B` are listed (R-Part_Template-05). Open: Q-Part_Template-07 (columns shown). |
| 2 | Select the row of `QA-<suffix> Variant B`. | None | The detail page of `QA-<suffix> Variant B` opens. Proposed, to confirm in Q-Part_Template-07: rows link to the variant. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-012: The Duplicate Part form rejects an empty name.

| Field | Value |
|---|---|
| **Summary** | The Duplicate Part form rejects an empty name. |
| **Requirement** | `R-Part_Template-04`. Source: [part-template.md#Create Variant](../../requirements/docs/part-template.md#L43-L44) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty required field) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`, select the *Variants* tab and *New Variant*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Clear the Name field and press *Submit*. | Name: empty | Proposed, to confirm in Q-Part_Template-02: the form stays open, shows an error on Name, and no variant is created. Open: Q-Part_Template-02 (which fields are required, error text). |
| 2 | Close the form and look at the *Variants* tab. | None | No new variant row is listed. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

**Duplicate check:** 68 · Review · matches: [UI-Part_Template-013](template-parts-and-variants-tab.md) (68)

**Duplicate judgement:** Keep · An empty name (missing value) is a different invalid class from the whitespace-only name of UI-Part_Template-013, which tests trimming of a non-empty value. · test-case-reviewer, 2026-10-15

---

### UI-Part_Template-013: The Duplicate Part form rejects a whitespace-only name.

| Field | Value |
|---|---|
| **Summary** | The Duplicate Part form rejects a whitespace-only name. |
| **Requirement** | `R-Part_Template-04`. Source: [part-template.md#Create Variant](../../requirements/docs/part-template.md#L43-L44) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Error guessing (whitespace-only text) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`, select the *Variants* tab and *New Variant*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Enter spaces in Name and press *Submit*. | Name: 3 spaces | Proposed, to confirm in Q-Part_Template-02: the form stays open with an error on Name and no variant is created. Open: Q-Part_Template-02 (error text). |
| 2 | Close the form and look at the *Variants* tab. | None | No new variant row is listed. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

**Duplicate check:** 68 · Review · matches: [UI-Part_Template-012](template-parts-and-variants-tab.md) (68)

**Duplicate judgement:** Keep · A whitespace-only name is a different invalid class from the empty name of UI-Part_Template-012: it passes a plain not-empty check and tests trimming. · test-case-reviewer, 2026-10-15

---

### UI-Part_Template-014: Cancelling the Duplicate Part form creates no variant.

| Field | Value |
|---|---|
| **Summary** | Cancelling the Duplicate Part form creates no variant. |
| **Requirement** | `R-Part_Template-04`. Source: [part-template.md#Create Variant](../../requirements/docs/part-template.md#L43-L44) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-form) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`, select the *Variants* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select *New Variant* and enter a name. | Name: `QA-<suffix> Cancelled` | The *Duplicate Part* form shows the name. Open: Q-Part_Template-02 (form layout). |
| 2 | Close the form without pressing *Submit*. | None | Proposed, to confirm in Q-Part_Template-02: the form closes and no part is created. |
| 3 | Look at the *Variants* tab. | None | No variant `QA-<suffix> Cancelled` is listed. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-015: A user with view-only access cannot create a variant.

| Field | Value |
|---|---|
| **Summary** | A user with view-only access cannot create a variant. |
| **Requirement** | `R-Part_Template-04`. Source: [part-template.md#Create Variant](../../requirements/docs/part-template.md#L43-L44) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Negative (blocked user) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`, plus variant `QA-<suffix> Variant A` (`variant_of` = the template); Pre-steps: log in through the login form, open `QA-<suffix> Template`, select the *Variants* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-02, Q-Part_Template-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the *Variants* tab. | None | `QA-<suffix> Variant A` is listed (R-Part_Template-05). Open: Q-Part_Template-07 (columns). |
| 2 | Look for the *New Variant* button. | None | Proposed, to confirm in Q-Part_Template-02: the *New Variant* button is hidden or disabled for `reader`, and no variant can be created. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-016: A user with no permissions cannot open a template part.

| Field | Value |
|---|---|
| **Summary** | A user with no permissions cannot open a template part. |
| **Requirement** | `R-Part_Template-04`. Source: [part-template.md#Create Variant](../../requirements/docs/part-template.md#L43-L44) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Negative (blocked user) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess` (no permissions); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; Pre-steps: log in through the login form, log in as `noaccess`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Part_Template-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the detail page of `QA-<suffix> Template` by its URL (`/web/part/<pk>/`). | pk of the template | Proposed, to confirm in Q-Part_Template-02: the page content is not shown and no *Variants* tab or *New Variant* button is available. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-017: A variant cannot be made of a part that is not a Template.

| Field | Value |
|---|---|
| **Summary** | A variant cannot be made of a part that is not a Template. |
| **Requirement** | `R-Part_Template-03`. Source: [part-template.md#Create Variant](../../requirements/docs/part-template.md#L41) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Negative (only once the Template option is on) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, part `QA-<suffix> Plain` (Template off) and part `QA-<suffix> Other` (Template off), created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Other`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the detail page of `QA-<suffix> Plain`. | None | No *Variants* tab and no *New Variant* button (R-Detail_View-08). A variant cannot be created from it (R-Part_Template-03). |
| 2 | Open the edit form of `QA-<suffix> Other` and look at the field that sets the template of a part. | None | Variants can be created only once the Template option is on (R-Part_Template-03). Open: Q-Part_Template-03 (the field's label in 1.5.6, and whether `QA-<suffix> Plain` is offered). |
| 3 | Select `QA-<suffix> Plain` in that field and save. | None | `QA-<suffix> Other` does not become a variant of a non-template part (R-Part_Template-03). Open: Q-Part_Template-03 (whether the part is left out of the selector or the form is rejected, and the error text). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-018: A variant of a variant (sub-variant) can be created once the variant is a Template.

| Field | Value |
|---|---|
| **Summary** | A variant of a variant (sub-variant) can be created once the variant is a Template. |
| **Requirement** | `R-Part_Template-03`, `R-Part_Template-04`, `R-Part_Template-05`. Source: [part-template.md#Create Variant](../../requirements/docs/part-template.md#L41); [part-template.md#Create Variant](../../requirements/docs/part-template.md#L43-L44); [part-template.md#Part Templates](../../requirements/docs/part-template.md#L20) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | State transition (variant switched to template, then sub-variant created) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`, plus variant `QA-<suffix> Variant A` (`variant_of` = the template); Pre-steps: log in through the login form, open `QA-<suffix> Variant A`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-01, Q-Part_Template-03, Q-Part_Template-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the tab list of `QA-<suffix> Variant A`. | None | The *Variants* tab is hidden while the variant's Template option is off (R-Detail_View-08). |
| 2 | Switch the Template option on for `QA-<suffix> Variant A`. | None | The option shows on (R-Part_Template-02). Open: Q-Part_Template-01 (location). |
| 3 | Select *Variants*, then *New Variant*, fill in a name and press *Submit*. | Name: `QA-<suffix> Sub Variant` | Proposed, to confirm in Q-Part_Template-03: the sub-variant is created and references `QA-<suffix> Variant A`. Open: Q-Part_Template-07 (whether sub-variants are allowed). |
| 4 | Open `QA-<suffix> Variant A` *Variants* tab. | None | `QA-<suffix> Sub Variant` is listed. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** The docs mention sub-variants only in the BOM page (manufacturing-bom.md#L80).

---

### UI-Part_Template-019: A template part with variants can be set inactive and deleted only after its variants are handled.

| Field | Value |
|---|---|
| **Summary** | A template part with variants can be set inactive and deleted only after its variants are handled. |
| **Requirement** | `R-Part_Template-05`. Source: [part-template.md#Part Templates](../../requirements/docs/part-template.md#L20) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | What-if business scenario (template deleted while variants exist) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `admin`; Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`, plus variant `QA-<suffix> Variant A` (`variant_of` = the template); Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Set `QA-<suffix> Template` inactive and try to delete it. | None | Not known: depends on open question Q-Part_Template-04 (deletion blocked, variants deleted too, or variants left without a template). |
| 2 | Open `QA-<suffix> Variant A` by its URL. | pk of the variant | Open: Q-Part_Template-04 (whether the variant still exists, and what its template reference shows). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** Cleanup is part of the test: delete variants before the template to avoid the unknown outcome.

---

### UI-Part_Template-020: A serial number already used on one variant is rejected on a sibling variant.

| Field | Value |
|---|---|
| **Summary** | A serial number already used on one variant is rejected on a sibling variant. |
| **Requirement** | `R-Part_Template-06`. Source: [part-template.md#Part Templates](../../requirements/docs/part-template.md#L24) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: duplicate serial across variants) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, Trackable template `QA-<suffix> Template` (Template on, Trackable on), Trackable variants `QA-<suffix> Variant A` and `QA-<suffix> Variant B` (`variant_of` = the template), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; location `QA-<suffix> Location`; Pre-steps: log in through the login form, open `QA-<suffix> Variant A`, *Stock* tab. |
| **Automation** | Partial: error text unknown. |
| **Review** | Draft · Open question: Q-Part_Template-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | On `QA-<suffix> Variant A`, add a stock item with a serial number. | Quantity: 1<br>Serial: `QA100` | The stock item is created with serial `QA100`. Open: Q-Part_Template-05 (the add-stock form and its labels; Trackable parts need a serial or batch). |
| 2 | Open `QA-<suffix> Variant B` and add a stock item with the same serial. | Quantity: 1<br>Serial: `QA100` | No stock item with serial `QA100` is created for `QA-<suffix> Variant B` (R-Part_Template-06: serial numbers must be unique across a template and its variants). Open: Q-Part_Template-05 (error text and where it is shown). |
| 3 | Look at the *Stock* tab of `QA-<suffix> Variant B`. | None | No stock item with serial `QA100` is listed. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

**Duplicate check:** 57 · Review · matches: [UI-Part_Template-021](template-parts-and-variants-tab.md) (57)

**Duplicate judgement:** Keep · Duplicate serial between two sibling variants, whereas UI-Part_Template-021 checks a variant against its template (a different pair in the template / variant set). · test-case-reviewer, 2026-10-15

---

### UI-Part_Template-021: A serial number used on a variant is rejected on its template.

| Field | Value |
|---|---|
| **Summary** | A serial number used on a variant is rejected on its template. |
| **Requirement** | `R-Part_Template-06`. Source: [part-template.md#Part Templates](../../requirements/docs/part-template.md#L24) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: duplicate serial template vs variant) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, Trackable template `QA-<suffix> Template` (Template on, Trackable on), Trackable variants `QA-<suffix> Variant A` and `QA-<suffix> Variant B` (`variant_of` = the template), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; location `QA-<suffix> Location`; Pre-steps: log in through the login form, open `QA-<suffix> Variant A`, *Stock* tab. |
| **Automation** | Partial: error text unknown. |
| **Review** | Draft · Open question: Q-Part_Template-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | On `QA-<suffix> Variant A`, add a stock item with a serial number. | Quantity: 1<br>Serial: `QA200` | The stock item is created. Open: Q-Part_Template-05 (form labels). |
| 2 | Open `QA-<suffix> Template` and add a stock item with the same serial. | Quantity: 1<br>Serial: `QA200` | No stock item with serial `QA200` is created for the template (R-Part_Template-06). Open: Q-Part_Template-05 (error text; whether a template can hold stock directly). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

**Duplicate check:** 57 · Review · matches: [UI-Part_Template-020](template-parts-and-variants-tab.md) (57)

**Duplicate judgement:** Keep · Duplicate serial between a variant and its template, whereas UI-Part_Template-020 checks two sibling variants; it also exercises stock held directly on the template. · test-case-reviewer, 2026-10-15

---

### UI-Part_Template-022: Different serial numbers on a template and its variants are accepted.

| Field | Value |
|---|---|
| **Summary** | Different serial numbers on a template and its variants are accepted. |
| **Requirement** | `R-Part_Template-06`. Source: [part-template.md#Part Templates](../../requirements/docs/part-template.md#L24) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: distinct serials) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, Trackable template `QA-<suffix> Template` (Template on, Trackable on), Trackable variants `QA-<suffix> Variant A` and `QA-<suffix> Variant B` (`variant_of` = the template), created via `POST /api/part/category/` and `POST /api/part/` as `admin`; location `QA-<suffix> Location`; Pre-steps: log in through the login form, open `QA-<suffix> Variant A`, *Stock* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | On `QA-<suffix> Variant A`, add a stock item. | Quantity: 1<br>Serial: `QA300` | The stock item is created. Open: Q-Part_Template-05 (form labels). |
| 2 | On `QA-<suffix> Variant B`, add a stock item. | Quantity: 1<br>Serial: `QA301` | Proposed, to confirm in Q-Part_Template-05: the stock item is created, because the serial is unique across the variants. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-023: The same serial number is accepted on two parts that are not template and variant.

| Field | Value |
|---|---|
| **Summary** | The same serial number is accepted on two parts that are not template and variant. |
| **Requirement** | `R-Part_Template-06`. Source: [part-template.md#Part Templates](../../requirements/docs/part-template.md#L24) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Decision table (columns: related parts / unrelated parts) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, two Trackable parts `QA-<suffix> Solo 1` and `QA-<suffix> Solo 2` (no template relation), location `QA-<suffix> Location`, created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Solo 1`, *Stock* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | On `QA-<suffix> Solo 1`, add a stock item. | Quantity: 1<br>Serial: `QA400` | The stock item is created. Open: Q-Part_Template-05 (form labels). |
| 2 | On `QA-<suffix> Solo 2`, add a stock item with the same serial. | Quantity: 1<br>Serial: `QA400` | Proposed, to confirm in Q-Part_Template-05: the stock item is created. The docs state uniqueness only for template and variant parts (R-Part_Template-06). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** The opposite of the rule is proposed, not stated (guardrail 1).

---

### UI-Part_Template-024: A template's stock includes the stock of its variants.

| Field | Value |
|---|---|
| **Summary** | A template's stock includes the stock of its variants. |
| **Requirement** | `R-Part_Template-07`. Source: [part-template.md#Part Templates](../../requirements/docs/part-template.md#L26) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: stock on variants only) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`, variants `QA-<suffix> Variant A` and `QA-<suffix> Variant B`; stock 5 on A and 7 on B via `POST /api/stock/` as `admin`; template has no stock of its own; Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the detail page of `QA-<suffix> Template`. | None | The page opens. Open: Q-Part_Template-06 (where the stock figure is shown). |
| 2 | Read the stock quantity of the template. | None | The stock of the template includes the stock of all its variants: 12 (5 + 7) (R-Part_Template-07). Open: Q-Part_Template-06 (the label and the tab or field that shows it). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

**Duplicate check:** 53 · Review · matches: [UI-Part_Template-026](template-parts-and-variants-tab.md) (53), [UI-Part_Template-025](template-parts-and-variants-tab.md) (51)

**Duplicate judgement:** Keep · Stock only on two direct variants (template has none), whereas UI-Part_Template-026 has stock only on a sub-variant and UI-Part_Template-025 adds the template's own stock. · test-case-reviewer, 2026-10-15

---

### UI-Part_Template-025: A template's stock adds its own stock to the stock of its variants.

| Field | Value |
|---|---|
| **Summary** | A template's stock adds its own stock to the stock of its variants. |
| **Requirement** | `R-Part_Template-07`. Source: [part-template.md#Part Templates](../../requirements/docs/part-template.md#L26) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Decision table (columns: template stock present / variant stock present) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`, variant `QA-<suffix> Variant A`; stock 3 on the template and 5 on A via `POST /api/stock/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the stock quantity of `QA-<suffix> Template`. | None | The stock of the template includes the stock for all variants: 8 (3 + 5) (R-Part_Template-07). Open: Q-Part_Template-06 (label and location of the figure). |
| 2 | Read the stock quantity of `QA-<suffix> Variant A`. | None | Proposed, to confirm in Q-Part_Template-06: 5, the variant's own stock only. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

**Duplicate check:** 56 · Review · matches: [UI-Part_Template-026](template-parts-and-variants-tab.md) (56), [UI-Part_Template-024](template-parts-and-variants-tab.md) (51)

**Duplicate judgement:** Keep · Template holds its own stock plus a direct variant's (a different decision-table column from UI-Part_Template-024 and from the sub-variant-only stock of UI-Part_Template-026), and it also checks the variant's own figure. · test-case-reviewer, 2026-10-15

---

### UI-Part_Template-026: A template's stock includes the stock of a sub-variant.

| Field | Value |
|---|---|
| **Summary** | A template's stock includes the stock of a sub-variant. |
| **Requirement** | `R-Part_Template-07`. Source: [part-template.md#Part Templates](../../requirements/docs/part-template.md#L26) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (class: variant of a variant) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`, plus variant `QA-<suffix> Variant A` (`variant_of` = the template) and sub-variant `QA-<suffix> Sub Variant` (`variant_of` = Variant A, Variant A has Template on); stock 4 on the sub-variant; Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-06, Q-Part_Template-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the stock quantity of `QA-<suffix> Template`. | None | Proposed, to confirm in Q-Part_Template-06: 4, because the stock of the template includes the stock for all variants under that part (R-Part_Template-07). Open: Q-Part_Template-06 (whether sub-variants count as variants). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

**Duplicate check:** 56 · Review · matches: [UI-Part_Template-025](template-parts-and-variants-tab.md) (56), [UI-Part_Template-024](template-parts-and-variants-tab.md) (53)

**Duplicate judgement:** Keep · Stock sits only on a sub-variant (two levels down), a different starting state from the direct-variant stock of UI-Part_Template-024 and UI-Part_Template-025. · test-case-reviewer, 2026-10-15

---

### UI-Part_Template-027: An inactive variant's stock and the template's stock figure.

| Field | Value |
|---|---|
| **Summary** | An inactive variant's stock and the template's stock figure. |
| **Requirement** | `R-Part_Template-07`. Source: [part-template.md#Part Templates](../../requirements/docs/part-template.md#L26) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | What-if business scenario (variant made inactive) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and template part `QA-<suffix> Template` (Template on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`, variant `QA-<suffix> Variant A` (Inactive) with stock 5; Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Read the stock quantity of `QA-<suffix> Template`. | None | Not known: depends on open question Q-Part_Template-06 (whether an inactive variant's stock is included; the docs say all variants). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-028: A test template defined on the template part also applies to its variant.

| Field | Value |
|---|---|
| **Summary** | A test template defined on the template part also applies to its variant. |
| **Requirement** | `R-Part_Template-08`. Source: [part-test.md#Test Templates](../../requirements/docs/part-test.md#L19) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: master part with a test template) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category` and Testable template part `QA-<suffix> Template` (Template on, Testable on), created via `POST /api/part/category/` and `POST /api/part/` as `admin`, plus Testable variant `QA-<suffix> Variant A` (`variant_of` = the template); test template `QA-<suffix> Visual` on the template via `POST /api/part/test-template/`; Pre-steps: log in through the login form, open `QA-<suffix> Variant A`, *Test Templates* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Detail_View-49 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab of `QA-<suffix> Variant A`. | None | Test templates of the master part cascade to its variants (R-Part_Template-08): `QA-<suffix> Visual` is listed. Open: Q-Detail_View-49 (how inherited templates are marked). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** Q-Detail_View-49 is an earlier Open question; the cases in the Detail_View folder cover the tab in depth.

---

### UI-Part_Template-029: An Inherited BOM line of the template appears in the variant's BOM.

| Field | Value |
|---|---|
| **Summary** | An Inherited BOM line of the template appears in the variant's BOM. |
| **Requirement** | `R-Part_Template-09`. Source: [manufacturing-bom.md#Inherited BOM Line Items](../../requirements/docs/manufacturing-bom.md#L80), [#L88-107](../../requirements/docs/manufacturing-bom.md#L88-L107) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Decision table (column: inherited line, variant) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`; Assembly template `QA-<suffix> Template` (Template on), variant `QA-<suffix> Variant A` (`variant_of` = template), components `QA-<suffix> Comp A1` and `QA-<suffix> Comp A2`; BOM lines on the template: `Comp A1` (Inherited on) and `Comp A2` (Inherited off), created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Variant A`, *Bill of Materials* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Bill of Materials* tab of `QA-<suffix> Variant A`. | None | `QA-<suffix> Comp A1` is included in the BOM of the variant (R-Part_Template-09). Open: Q-Part_Template-08 (how an inherited line is marked on the variant's BOM table). |
| 2 | Open the *Bill of Materials* tab of `QA-<suffix> Template`. | None | `QA-<suffix> Comp A1` and `QA-<suffix> Comp A2` are both listed. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

**Duplicate check:** 55 · Review · matches: [UI-Part_Template-031](template-parts-and-variants-tab.md) (55)

**Duplicate judgement:** Keep · Checks the inherited line on a direct variant, whereas UI-Part_Template-031 checks the "sub-variant" clause of the same rule two levels down. · test-case-reviewer, 2026-10-15

---

### UI-Part_Template-030: A BOM line that is not Inherited stays on the template only.

| Field | Value |
|---|---|
| **Summary** | A BOM line that is not Inherited stays on the template only. |
| **Requirement** | `R-Part_Template-09`. Source: [manufacturing-bom.md#Inherited BOM Line Items](../../requirements/docs/manufacturing-bom.md#L80), [#L88-107](../../requirements/docs/manufacturing-bom.md#L88-L107) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Decision table (column: non-inherited line, variant) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`; Assembly template `QA-<suffix> Template` (Template on), variant `QA-<suffix> Variant A` (`variant_of` = template), components `QA-<suffix> Comp A1` and `QA-<suffix> Comp A2`; BOM lines on the template: `Comp A1` (Inherited on) and `Comp A2` (Inherited off), created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Variant A`, *Bill of Materials* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the BOM table of `QA-<suffix> Variant A`. | None | `QA-<suffix> Comp A2` is not listed: a line that is not inherited is only included in the BOM of the template (manufacturing-bom.md worked example, A2) (R-Part_Template-09). Open: Q-Part_Template-08 (none beyond the table layout). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-031: An Inherited BOM line of the template appears in the BOM of a sub-variant.

| Field | Value |
|---|---|
| **Summary** | An Inherited BOM line of the template appears in the BOM of a sub-variant. |
| **Requirement** | `R-Part_Template-09`. Source: [manufacturing-bom.md#Inherited BOM Line Items](../../requirements/docs/manufacturing-bom.md#L80), [#L88-107](../../requirements/docs/manufacturing-bom.md#L88-L107) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Decision table (column: inherited line, sub-variant) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`; Assembly template `QA-<suffix> Template` (Template on), variant `QA-<suffix> Variant A` (`variant_of` = template), components `QA-<suffix> Comp A1` and `QA-<suffix> Comp A2`; BOM lines on the template: `Comp A1` (Inherited on) and `Comp A2` (Inherited off), created via the API as `admin`; sub-variant `QA-<suffix> Sub Variant` (`variant_of` = Variant A, Variant A Template on); Pre-steps: log in through the login form, open `QA-<suffix> Sub Variant`, *Bill of Materials* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Bill of Materials* tab of `QA-<suffix> Sub Variant`. | None | `QA-<suffix> Comp A1` is included, as the line is inherited by any variant or sub-variant of the template (R-Part_Template-09). Open: Q-Part_Template-08 (row marking). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

**Duplicate check:** 55 · Review · matches: [UI-Part_Template-029](template-parts-and-variants-tab.md) (55)

**Duplicate judgement:** Keep · Checks the "sub-variant" clause of R-Part_Template-09 (variant of a variant), whereas UI-Part_Template-029 checks a direct variant. · test-case-reviewer, 2026-10-15

---

### UI-Part_Template-032: A line inherited from a variant reaches its sub-variant but not a sibling variant.

| Field | Value |
|---|---|
| **Summary** | A line inherited from a variant reaches its sub-variant but not a sibling variant. |
| **Requirement** | `R-Part_Template-09`. Source: [manufacturing-bom.md#Inherited BOM Line Items](../../requirements/docs/manufacturing-bom.md#L80), [#L88-107](../../requirements/docs/manufacturing-bom.md#L88-L107) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Decision table (columns: sub-variant of defining variant / sibling variant) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`; Assembly template `QA-<suffix> Template` (Template on), variant `QA-<suffix> Variant A` (`variant_of` = template), components `QA-<suffix> Comp A1` and `QA-<suffix> Comp A2`; BOM lines on the template: `Comp A1` (Inherited on) and `Comp A2` (Inherited off), created via the API as `admin`; variant `QA-<suffix> Variant B` (sibling); Variant A has Template on, sub-variant `QA-<suffix> Sub Variant`; BOM line `QA-<suffix> Comp B1` (Inherited on) on Variant A; Pre-steps: log in through the login form, open `QA-<suffix> Sub Variant`, *Bill of Materials* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the BOM table of `QA-<suffix> Sub Variant`. | None | `Comp A1` and `Comp B1` are both included (R-Part_Template-09, worked example: D has A1 from A and B1 from B). Open: Q-Part_Template-08 (row marking). |
| 2 | Look at the BOM table of `QA-<suffix> Variant B`. | None | `Comp A1` is included. `Comp B1` is not shown here: it is defined on Variant A and flows downwards only (R-Part_Template-10). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-033: An Inherited BOM line defined on a variant does not appear in the template's BOM.

| Field | Value |
|---|---|
| **Summary** | An Inherited BOM line defined on a variant does not appear in the template's BOM. |
| **Requirement** | `R-Part_Template-10`. Source: [manufacturing-bom.md#Inherited BOM Line Items](../../requirements/docs/manufacturing-bom.md#L113) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Negative (inheritance flows downwards only) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`; Assembly template `QA-<suffix> Template` (Template on), variant `QA-<suffix> Variant A` (`variant_of` = template), components `QA-<suffix> Comp A1` and `QA-<suffix> Comp A2`; BOM lines on the template: `Comp A1` (Inherited on) and `Comp A2` (Inherited off), created via the API as `admin`; BOM line `QA-<suffix> Comp B1` (Inherited on) on `QA-<suffix> Variant A`; Pre-steps: log in through the login form, open `QA-<suffix> Template`, *Bill of Materials* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the BOM table of `QA-<suffix> Template`. | None | `QA-<suffix> Comp B1` is not listed: a part higher up the variant chain cannot inherit BOM items from child parts (R-Part_Template-10). |
| 2 | Look at the BOM table of `QA-<suffix> Variant A`. | None | `Comp B1` is listed as its own line. Open: Q-Part_Template-08 (row marking). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-034: Editing an Inherited BOM line on the template updates the variant's BOM.

| Field | Value |
|---|---|
| **Summary** | Editing an Inherited BOM line on the template updates the variant's BOM. |
| **Requirement** | `R-Part_Template-11`. Source: [manufacturing-bom.md#Inherited BOM Line Items](../../requirements/docs/manufacturing-bom.md#L116) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | State transition (quantity changed on the template) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`; Assembly template `QA-<suffix> Template` (Template on), variant `QA-<suffix> Variant A` (`variant_of` = template), components `QA-<suffix> Comp A1` and `QA-<suffix> Comp A2`; BOM lines on the template: `Comp A1` (Inherited on) and `Comp A2` (Inherited off), created via the API as `admin` (line `Comp A1` quantity 2); Pre-steps: log in through the login form, open `QA-<suffix> Template`, *Bill of Materials* tab, editing mode. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-08, Q-Detail_View-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Edit the `QA-<suffix> Comp A1` line of the template and change its quantity. | Quantity: 5 | The change is saved on the template. Open: Q-Detail_View-02 (how a line is edited), Q-Part_Template-08 (permissions). |
| 2 | Open the *Bill of Materials* tab of `QA-<suffix> Variant A`. | None | The `Comp A1` line shows quantity 5 (R-Part_Template-11: changes to an inherited line are reflected in the BOM of variant parts). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-035: An Inherited BOM line that is switched off on the template leaves the variant's BOM.

| Field | Value |
|---|---|
| **Summary** | An Inherited BOM line that is switched off on the template leaves the variant's BOM. |
| **Requirement** | `R-Part_Template-09`, `R-Part_Template-11`. Source: [manufacturing-bom.md#Inherited BOM Line Items](../../requirements/docs/manufacturing-bom.md#L80), [#L88-107](../../requirements/docs/manufacturing-bom.md#L88-L107); [manufacturing-bom.md#Inherited BOM Line Items](../../requirements/docs/manufacturing-bom.md#L116) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | What-if business scenario (Inherited flag turned off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`; Assembly template `QA-<suffix> Template` (Template on), variant `QA-<suffix> Variant A` (`variant_of` = template), components `QA-<suffix> Comp A1` and `QA-<suffix> Comp A2`; BOM lines on the template: `Comp A1` (Inherited on) and `Comp A2` (Inherited off), created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`, *Bill of Materials* tab, editing mode. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-08 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Edit the `Comp A1` line of the template and turn *Inherited* off. | Inherited: off | The change is saved. Open: Q-Part_Template-08 (the field label *Inherited* and how it is edited). |
| 2 | Open the *Bill of Materials* tab of `QA-<suffix> Variant A`. | None | Proposed, to confirm in Q-Part_Template-08: `Comp A1` is no longer in the variant's BOM, as only Inherited lines are included (R-Part_Template-09). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** The docs state that inherited lines are included in variants; the effect of turning the flag off is proposed.

---

### UI-Part_Template-036: A test template of the template part is listed on two variants.

| Field | Value |
|---|---|
| **Summary** | A test template defined on the template part is assigned to every one of its variants, here two direct variants. |
| **Requirement** | `R-Part_Template-08`. Source: [part-test.md#Part Test Templates](../../requirements/docs/part-test.md#L19) |
| **Area** | Part_Template |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (count of variants = 2) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, Testable template part `QA-<suffix> Template` (Template on, Testable on), Testable variants `QA-<suffix> Variant A` and `QA-<suffix> Variant B` (`variant_of` = the template), test template `QA-<suffix> Visual` on the template, created via `POST /api/part/category/`, `POST /api/part/` and `POST /api/part/test-template/` as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Variant A`. |
| **Automation** | Partial: tab labels unconfirmed. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-49 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab of `QA-<suffix> Variant A`. | None | `QA-<suffix> Visual` is listed: any test template defined for the master part is assigned to its variants (R-Part_Template-08). Open: Q-Detail_View-45 (tab and column labels), Q-Detail_View-49 (how an inherited template is marked). |
| 2 | Open the *Test Templates* tab of `QA-<suffix> Variant B`. | None | `QA-<suffix> Visual` is listed (R-Part_Template-08). Open: Q-Detail_View-49 (marker). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: delete the test template, set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** Detail_View covers a single variant (UI-Detail_View-330); this case checks that every variant receives the template.

---

### UI-Part_Template-037: A test template of the template part is listed on a sub-variant.

| Field | Value |
|---|---|
| **Summary** | A test template defined on the template part also reaches a variant of a variant (sub-variant). |
| **Requirement** | `R-Part_Template-08`, `R-Part_Template-09`. Source: [part-test.md#Part Test Templates](../../requirements/docs/part-test.md#L19); [manufacturing-bom.md#Inherited BOM Line Items](../../requirements/docs/manufacturing-bom.md#L80) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (class: variant of a variant) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, Testable template part `QA-<suffix> Template` (Template on, Testable on), Testable variant `QA-<suffix> Variant A` (`variant_of` = the template, Template on), Testable sub-variant `QA-<suffix> Sub Variant` (`variant_of` = Variant A), test template `QA-<suffix> Visual` on the template, created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Sub Variant`. |
| **Automation** | Partial: tab labels unconfirmed. |
| **Review** | Draft · Open question: Q-Part_Template-11, Q-Detail_View-49 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab of `QA-<suffix> Sub Variant`. | None | Proposed, to confirm in Q-Part_Template-11: `QA-<suffix> Visual` is listed. The test docs state the cascade for the variants of a master part (R-Part_Template-08) and mention sub-variants only for the BOM (R-Part_Template-09). Open: Q-Detail_View-49 (marker). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: delete the test template, set the sub-variant, the variant and the template inactive, delete them in that order, then the category.

**Notes:** None

---

### UI-Part_Template-038: A test template defined on one variant is not listed on a sibling variant.

| Field | Value |
|---|---|
| **Summary** | A test template defined on `Variant A` does not reach the sibling `Variant B` or the master, because the cascade runs from the master part down. |
| **Requirement** | `R-Part_Template-08`. Source: [part-test.md#Part Test Templates](../../requirements/docs/part-test.md#L19) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Negative (cascade is downwards only), Decision table (columns: master / own variant / sibling) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, Testable template part `QA-<suffix> Template` (Template on, Testable on), Testable variants `QA-<suffix> Variant A` and `QA-<suffix> Variant B` (`variant_of` = the template), test template `QA-<suffix> A Only` on `Variant A`, created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Variant B`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Detail_View-49, Q-Part_Template-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab of `QA-<suffix> Variant B`. | None | Proposed, to confirm in Q-Part_Template-11: `QA-<suffix> A Only` is not listed. No rule states the sibling case; the docs state only that templates of the master part cascade to its variants (R-Part_Template-08). |
| 2 | Open the *Test Templates* tab of `QA-<suffix> Template`. | None | Proposed, to confirm in Q-Part_Template-11: `QA-<suffix> A Only` is not listed on the master. Open: Q-Detail_View-49. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: delete the test template, set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** Whether a variant can define its own test template is Q-Detail_View-49; the data is created through the API.

---

### UI-Part_Template-039: A variant created with New Variant receives the template part's test templates.

| Field | Value |
|---|---|
| **Summary** | A variant created from the *Variants* tab after the template part already has a test template lists that test template. |
| **Requirement** | `R-Part_Template-08`, `R-Part_Template-04`. Source: [part-test.md#Part Test Templates](../../requirements/docs/part-test.md#L19); [part-template.md#Create Variant](../../requirements/docs/part-template.md#L43-L44) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | State transition (variant created after the test template exists), Exploratory |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, Testable template part `QA-<suffix> Template` (Template on, Testable on), test template `QA-<suffix> Visual` on the template, created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`, select the *Variants* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Part_Template-02, Q-Part_Template-07, Q-Detail_View-49 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select *New Variant*, fill in the *Duplicate Part* form and press *Submit*. | Name: `QA-<suffix> Variant A`<br>Description: `Variant test part` | The variant is created (R-Part_Template-04). Open: Q-Part_Template-02 (prefilled fields and navigation after Submit; whether the new variant is Testable depends on the form). |
| 2 | Open the *Test Templates* tab of `QA-<suffix> Variant A`. | None | `QA-<suffix> Visual` is listed (R-Part_Template-08: templates of the master part are assigned to its variants). Open: Q-Part_Template-02 (whether the new variant is Testable, so that the tab is shown), Q-Detail_View-49 (marker). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: delete the test template, set the variant and then the template inactive, delete the variant first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-040: A result recorded on a variant stock item against an inherited test template.

| Field | Value |
|---|---|
| **Summary** | A test result can be recorded on a stock item of a variant against a test template defined on the template part. |
| **Requirement** | `R-Part_Template-08`, `R-Detail_View-30`. Source: [part-test.md#Part Test Templates](../../requirements/docs/part-test.md#L19); [part-views.md#Test Results](../../requirements/docs/part-views.md#L134) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | Exploratory (flow across part, stock and test results) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `allaccess` (view, create and edit everything; step 2 adds a stock test result, which `engineer`, with view-only stock access, cannot do); Settings: None; Data: category `QA-<suffix> Category`, location `QA-<suffix> Location`, Testable template part `QA-<suffix> Template` (Template on, Testable on), Testable variant `QA-<suffix> Variant A`, test template `QA-<suffix> Visual` on the template, stock item of quantity 1 on `Variant A`, created via the API as `admin`; Pre-steps: log in through the login form, open the variant's stock item. |
| **Automation** | Partial: the stock pages are not in `requirements/docs/`. |
| **Review** | Draft · Open question: Q-Part_Template-10, Q-Detail_View-47 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the test results of the stock item. | None | Any stock item of a variant part has the same test templates associated with it (R-Part_Template-08): `QA-<suffix> Visual` is listed. Open: Q-Part_Template-10 (tab and table labels on the stock item). |
| 2 | Add a test result for `QA-<suffix> Visual` and save. | Result: pass | Proposed, to confirm in Q-Part_Template-10: the result is saved and listed against `QA-<suffix> Visual`. Open: Q-Part_Template-10 (form labels), Q-Detail_View-47 (value and attachment requirements). |
| 3 | Open the *Test Results* tab of `QA-<suffix> Variant A`. | None | Proposed, to confirm in Q-Part_Template-10: the new result is listed. The tab shows results from all the part's stock items in one table (R-Detail_View-30). |

**Postconditions and cleanup:** the stock item, its result, the variant and the template remain. Cleanup as `admin`: delete the stock item and the test template, then follow the usual order for variants, template and category.

**Notes:** Goes beyond UI-Detail_View-333, which only checks that the template is listed.

---

### UI-Part_Template-041: Deleting the template part's test template removes it from the variant.

| Field | Value |
|---|---|
| **Summary** | After a test template is deleted from the template part, it is no longer listed on the variant. |
| **Requirement** | `R-Part_Template-08`, `R-Detail_View-39`. Source: [part-test.md#Part Test Templates](../../requirements/docs/part-test.md#L19); [part-test.md#Enabled](../../requirements/docs/part-test.md#L64) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | What-if business scenario (master's test template deleted while variants exist), State transition (listed to removed) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, Testable template part `QA-<suffix> Template` (Template on, Testable on), Testable variant `QA-<suffix> Variant A`, test template `QA-<suffix> Visual` on the template, created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`, *Test Templates* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-48, Q-Part_Template-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Delete the test template `QA-<suffix> Visual` from the template part. | None | The template and its test results are deleted (R-Detail_View-39). Open: Q-Detail_View-45 (delete control), Q-Detail_View-48 (confirmation). |
| 2 | Open the *Test Templates* tab of `QA-<suffix> Variant A`. | None | Proposed, to confirm in Q-Part_Template-11: `QA-<suffix> Visual` is no longer listed, because the variant only receives the master's templates (R-Part_Template-08). |

**Postconditions and cleanup:** no test template is left. Cleanup as `admin`: set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-042: Renaming the template part's test template changes its name on the variant.

| Field | Value |
|---|---|
| **Summary** | After a test template of the template part is renamed, the variant lists it under the new name. |
| **Requirement** | `R-Part_Template-08`. Source: [part-test.md#Part Test Templates](../../requirements/docs/part-test.md#L19) |
| **Area** | Part_Template |
| **Type** | Positive |
| **Technique** | State transition (template renamed), What-if business scenario |
| **Priority** | P3 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, Testable template part `QA-<suffix> Template` (Template on, Testable on), Testable variant `QA-<suffix> Variant A`, test template `QA-<suffix> Visual` on the template, created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`, *Test Templates* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-48, Q-Part_Template-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Edit the test template and change its name. | Name: `QA-<suffix> Visual Renamed` | The template is saved. Open: Q-Detail_View-45 (edit control), Q-Detail_View-48 (key regeneration after a rename). |
| 2 | Open the *Test Templates* tab of `QA-<suffix> Variant A`. | None | Proposed, to confirm in Q-Part_Template-11: `QA-<suffix> Visual Renamed` is listed and `QA-<suffix> Visual` is not, because the variant is assigned the master's template itself (R-Part_Template-08). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: delete the test template, set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-043: A view-only user cannot edit an inherited test template on the variant.

| Field | Value |
|---|---|
| **Summary** | A user with view-only access sees the inherited test template on the variant but has no add, edit or delete control. |
| **Requirement** | `R-Part_Template-08`. Source: [part-test.md#Part Test Templates](../../requirements/docs/part-test.md#L19) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | Negative (blocked user) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: category `QA-<suffix> Category`, Testable template part `QA-<suffix> Template` (Template on, Testable on), Testable variant `QA-<suffix> Variant A`, test template `QA-<suffix> Visual` on the template, created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Variant A`, *Test Templates* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-49 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the *Test Templates* tab. | None | `QA-<suffix> Visual` is listed (R-Part_Template-08). Open: Q-Detail_View-49 (marker). |
| 2 | Look for controls to add, edit or delete a test template. | None | Proposed, to confirm in Q-Detail_View-45: no add, edit or delete control is available to `reader`. |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: delete the test template, set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None

---

### UI-Part_Template-044: Test templates on a variant after the template part is made not Testable.

| Field | Value |
|---|---|
| **Summary** | After the template part is made not Testable, check which test templates its still Testable variant shows. |
| **Requirement** | `R-Part_Template-08`, `R-Detail_View-29`. Source: [part-test.md#Part Test Templates](../../requirements/docs/part-test.md#L19); [part-views.md#Test Templates](../../requirements/docs/part-views.md#L130) |
| **Area** | Part_Template |
| **Type** | Negative |
| **Technique** | What-if business scenario (master no longer Testable), State transition (Testable to not Testable) |
| **Priority** | P3 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (part management); Settings: None; Data: category `QA-<suffix> Category`, Testable template part `QA-<suffix> Template` (Template on, Testable on), Testable variant `QA-<suffix> Variant A`, test template `QA-<suffix> Visual` on the template, created via the API as `admin`; Pre-steps: log in through the login form, open `QA-<suffix> Template`. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Detail_View-48, Q-Part_Template-11 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Switch the Testable attribute of `QA-<suffix> Template` off. | None | Not known: depends on open question Q-Detail_View-48 (how Testable is switched off in 1.5.6, and whether the templates are kept). |
| 2 | Open the *Test Templates* tab of `QA-<suffix> Variant A`, which is still Testable. | None | Not known: depends on open question Q-Part_Template-11 (whether `QA-<suffix> Visual` is still listed on the variant when its master is not Testable). |

**Postconditions and cleanup:** records created by the case remain. Cleanup as `admin`: delete the test template, set each variant and then the template inactive, delete the variants first, then the template, then the category.

**Notes:** None
