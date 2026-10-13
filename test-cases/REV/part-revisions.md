# Part revisions: REV test cases

### UI-REV-001: A template part cannot have a revision

| Field | Value |
|---|---|
| **Summary** | When duplicating a template part, the *Revision Of* field does not offer the template part, so a revision of a template cannot be created. |
| **Requirement** | `R-REV-08`. Source: [part-revision.md#L38](../../requirements/docs/part-revision.md#L38) |
| **Area** | REV |
| **Type** | Negative |
| **Technique** | Negative, State transition (template part: blocked revision) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` ("Part Revisions") = on, which is the default on this instance; Data: template part `QA-<suffix> Template` (Template and Assembly checked), created via `POST /api/part/` as `admin`; Pre-steps: log in at `http://localhost/web`, open the detail page of `QA-<suffix> Template`. |
| **Automation** | Yes: field option check. |
| **Review** | Approved · 2026-10-11 · agent draft changed first: the draft expected a validation error on Submit after choosing the template in *Revision Of*; in 1.5.6 template parts are not offered in the *Revision Of* field at all, so the block happens before Submit. Steps rewritten to check the field options; removed the `[confirm in app]` placeholders. |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu (three vertical dots, top right) and select *Duplicate Part*. | None | The *Duplicate Part* form opens. |
| 2 | Open the *Revision Of* field and search for the template part. | Search: `QA-<suffix> Template` | The template part is not offered as an option in *Revision Of*. |
| 3 | Cancel the form. | None | The form closes and no new part is created. |
| 4 | Open the *Parts* view and search for the template's name. | `QA-<suffix> Template` | Only the template itself is listed. |

**Postconditions and cleanup:** only the template exists. Cleanup as `admin`: make `QA-<suffix> Template` inactive, then delete it.

**Notes:** the block is applied in the *Revision Of* field, which does not list template parts. The server also enforces it: a revision of a template sent through the API is rejected with "Cannot make a revision of a template part" (InvenTree 1.5.6 API, 2026-10-11); cover that in an API case.

### UI-REV-002: A duplicate revision code for the same part is rejected

| Field | Value |
|---|---|
| **Summary** | Creating a second revision of a part with a revision code already used by another revision of that part is rejected. |
| **Requirement** | `R-REV-07`. Source: [part-revision.md#L37](../../requirements/docs/part-revision.md#L37) |
| **Area** | REV |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: revision code already used), Error guessing (repeat of the same code) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = enabled [confirm in app: Q-REV-01]; Data: assembly part `QA-<suffix> Assembly` and its revision `QA-<suffix> Assembly B` (Revision `B`, Revision Of the assembly), both created via `POST /api/part/` as `admin`; Pre-steps: log in, open the detail page of `QA-<suffix> Assembly`. |
| **Automation** | Yes: stable form validation. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu and select *Duplicate Part*. | None | The *Duplicate Part* form opens. |
| 2 | Set *Revision Of* to the original and *Revision* to the code already used. Make Name distinct. | Revision Of: `QA-<suffix> Assembly`<br>Revision: `B`<br>Name: `QA-<suffix> Assembly Second B` | Fields accept the values. |
| 3 | Press *Submit*. | None | The form stays open with a validation error [confirm in app: error text and field]. No part is created. |
| 4 | Change *Revision* to an unused code and press *Submit*. | Revision: `C` | The form closes and the browser opens the new part, showing its link to `QA-<suffix> Assembly`. |

**Postconditions and cleanup:** the original, revision B and revision C exist. Cleanup as `admin`: make each of the three parts inactive, then delete them (revisions first).

**Notes:** case sensitivity of the comparison is open (Q-REV-06). Step 4 shows the only blocker was the code.

### UI-REV-003: A variant part can have a revision

| Field | Value |
|---|---|
| **Summary** | Duplicating a variant part with *Revision Of* set to the variant, a unique code and the same template is accepted. |
| **Requirement** | `R-REV-09`. Source: [part-revision.md#L38](../../requirements/docs/part-revision.md#L38) |
| **Area** | REV |
| **Type** | Positive |
| **Technique** | State transition (variant part: allowed revision) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = enabled [confirm in app: Q-REV-01]; Data: template `QA-<suffix> Template` and its variant `QA-<suffix> Variant` (Variant Of the template, Assembly checked), created via `POST /api/part/` as `admin`; Pre-steps: log in, open the detail page of `QA-<suffix> Variant`. |
| **Automation** | Yes. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu and select *Duplicate Part*. | None | The *Duplicate Part* form opens. |
| 2 | Set *Revision Of* and *Revision*. Make Name distinct; leave the template reference as copied. | Revision Of: `QA-<suffix> Variant`<br>Revision: `B`<br>Name: `QA-<suffix> Variant Rev B` | Fields accept the values with no validation errors. |
| 3 | Press *Submit*. | None | The form closes and the browser opens the new part, which links to `QA-<suffix> Variant`. |

**Postconditions and cleanup:** template, variant and revision exist. Cleanup as `admin`: make the revision, variant and template inactive, then delete them in that order.

**Notes:** the assembly flag is set because the effect of `PART_REVISION_ASSEMBLY_ONLY` is unknown (Q-REV-01).

### UI-REV-004: The revision selector navigates between revisions

| Field | Value |
|---|---|
| **Summary** | When multiple revisions exist, the *Select Part Revision* drop-down at the top of the part page navigates between them. |
| **Requirement** | `R-REV-14`. Source: [part-revision.md#L72](../../requirements/docs/part-revision.md#L72) |
| **Area** | REV |
| **Type** | Positive |
| **Technique** | State transition (revision A to revision B) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression, Settings-dependent |
| **Prerequisites** | User: `reader` (view only); Settings: `PART_ENABLE_REVISION` = enabled [confirm in app: Q-REV-01]; Data: assembly `QA-<suffix> Assembly` (Revision `A`) and `QA-<suffix> Assembly B` (Revision `B`, Revision Of the first), created via `POST /api/part/` as `admin`; Pre-steps: log in, open the detail page of `QA-<suffix> Assembly`. |
| **Automation** | Yes. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Find the *Select Part Revision* drop-down at the top of the part page. | None | The drop-down is visible. |
| 2 | Open the drop-down. | None | Both revisions are listed [confirm in app: option label format]. |
| 3 | Select revision `B`. | Revision: `B` | The browser opens the detail page of `QA-<suffix> Assembly B`. |
| 4 | Select revision `A` in the drop-down. | Revision: `A` | The browser returns to the detail page of `QA-<suffix> Assembly`. |

**Postconditions and cleanup:** no change. Cleanup as `admin`: make both parts inactive, then delete the revision and the original.

**Notes:** None

### UI-REV-005: The revision selector is hidden when no other revision exists

| Field | Value |
|---|---|
| **Summary** | A part with no revisions shows no *Select Part Revision* drop-down. |
| **Requirement** | `R-REV-15`. Source: [part-revision.md#L77](../../requirements/docs/part-revision.md#L77) |
| **Area** | REV |
| **Type** | Negative |
| **Technique** | State transition (single part: selector hidden), Decision table (revisions exist = no) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `reader` (view only); Settings: `PART_ENABLE_REVISION` = enabled [confirm in app: Q-REV-01]; Data: assembly `QA-<suffix> Solo`, no revisions, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the detail page of `QA-<suffix> Solo`. |
| **Automation** | Yes. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the top of the part page. | None | No *Select Part Revision* drop-down is shown. |
| 2 | As `admin`, create a revision of the part via `POST /api/part/` (Revision `B`, Revision Of the part) and reload the page. | Revision: `B` | The *Select Part Revision* drop-down now appears. |

**Postconditions and cleanup:** the part and one revision exist. Cleanup as `admin`: make both inactive, then delete the revision and the part.

**Notes:** step 2 proves the selector appears once the condition changes.

### UI-REV-006: The Revision field accepts any string

| Field | Value |
|---|---|
| **Summary** | A revision code containing spaces, symbols and Unicode is accepted when creating a revision. |
| **Requirement** | `R-REV-03`. Source: [part-revision.md#L29](../../requirements/docs/part-revision.md#L29) |
| **Area** | REV |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: non-alphanumeric string), Error guessing (special characters, Unicode) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = enabled [confirm in app: Q-REV-01]; Data: assembly `QA-<suffix> Assembly`, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the detail page of the part. |
| **Automation** | Yes. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu and select *Duplicate Part*. | None | The *Duplicate Part* form opens. |
| 2 | Enter the revision values and a distinct Name. | Revision Of: `QA-<suffix> Assembly`<br>Revision: `Rev Ä-1 #2`<br>Name: `QA-<suffix> Assembly Unicode` | Fields accept the values. |
| 3 | Press *Submit*. | None | The form closes and the new part opens. |
| 4 | Check the revision on the detail page. | None | Revision shows `Rev Ä-1 #2` exactly. |

**Postconditions and cleanup:** original and revision exist. Cleanup as `admin`: make both inactive, then delete revision and original.

**Notes:** maximum length is not stated, so no boundary case is written.

### UI-REV-007: Creating a revision leaves the original part's data unchanged

| Field | Value |
|---|---|
| **Summary** | After a revision is created, stock recorded against the original part stays on the original and is not moved to the revision. |
| **Requirement** | `R-REV-01`, `R-REV-02`. Source: [part-revision.md#L19](../../requirements/docs/part-revision.md#L19), [part-revision.md#L23](../../requirements/docs/part-revision.md#L23) |
| **Area** | REV |
| **Type** | Positive |
| **Technique** | What-if business scenario (revision created after stock exists) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional, Settings-dependent |
| **Prerequisites** | User: `allaccess` (create and edit parts and stock); Settings: `PART_ENABLE_REVISION` = enabled [confirm in app: Q-REV-01]; Data: assembly `QA-<suffix> Assembly` with one stock item of quantity 10, created via `POST /api/part/` and `POST /api/stock/` as `admin`; Pre-steps: log in, open the part's *Stock* tab and note the item and quantity. |
| **Automation** | Yes. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Stock* tab of the original. | None | One stock item of quantity 10 is listed. |
| 2 | Use *Duplicate Part* from the actions menu; set revision values and a distinct Name; press *Submit*. | Revision Of: `QA-<suffix> Assembly`<br>Revision: `B`<br>Name: `QA-<suffix> Assembly B` | The revision's detail page opens. |
| 3 | Open the revision's *Stock* tab. | None | The original's stock item is not listed (the revision has its own stock). |
| 4 | Return to the original and open its *Stock* tab. | None | The same stock item, quantity 10, is still listed. |

**Postconditions and cleanup:** original with stock, and revision. Cleanup as `admin`: delete the stock item, make both parts inactive, then delete the revision and the original.

**Notes:** the Name-uniqueness ambiguity is avoided with a distinct Name (Q-REV-02).

### UI-REV-008: Create a revision with Duplicate Part using the documented steps

| Field | Value |
|---|---|
| **Summary** | Duplicating a part and changing only *Revision Of* and *Revision* creates the revision and redirects to it. |
| **Requirement** | `R-REV-12`, `R-REV-13`. Source: [part-revision.md#L53-64](../../requirements/docs/part-revision.md#L53-L64), [part-revision.md#L66](../../requirements/docs/part-revision.md#L66) |
| **Area** | REV |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: documented minimal changes), What-if business scenario (Name left unchanged) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = enabled [open: Q-REV-01, default and label]; Data: assembly `QA-<suffix> Assembly`, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the detail page of `QA-<suffix> Assembly`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-REV-01, Q-REV-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu (three vertical dots, top right) and select *Duplicate Part*. | None | The *Duplicate Part* form opens. |
| 2 | Set *Revision Of* to the original and *Revision* to a new code. Change no other field. | Revision Of: `QA-<suffix> Assembly`<br>Revision: `B` | Fields accept the values. |
| 3 | Press *Submit*. | None | Not known: depends on open question Q-REV-02 (whether the unchanged Name, which the docs call unique, is accepted). If accepted: the form closes and the browser opens the new part. |

**Postconditions and cleanup:** original, and revision if created. Cleanup as `admin`: make each part inactive, then delete the revision and the original.

**Notes:** if the app requires a different Name, record it as the answer to Q-REV-02; UI-REV-003 and UI-REV-007 use a distinct Name.

### UI-REV-009: The revision page shows a link to the original part

| Field | Value |
|---|---|
| **Summary** | The detail page of a revision shows its link to the original part, and the link opens the original. |
| **Requirement** | `R-REV-04`, `R-REV-13`. Source: [part-revision.md#L30](../../requirements/docs/part-revision.md#L30), [part-revision.md#L66](../../requirements/docs/part-revision.md#L66) |
| **Area** | REV |
| **Type** | Positive |
| **Technique** | State transition (revision page to original page) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `reader` (view only); Settings: `PART_ENABLE_REVISION` = enabled [open: Q-REV-01, default and label]; Data: assembly `QA-<suffix> Assembly` and `QA-<suffix> Assembly B` (Revision `B`, Revision Of the first), created via `POST /api/part/` as `admin`; Pre-steps: log in, open the detail page of `QA-<suffix> Assembly B`. |
| **Automation** | Partial: link location is not known. |
| **Review** | Draft · Open question: Q-REV-01, Q-REV-07 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for the link to the original part on the revision page. | None | A link to `QA-<suffix> Assembly` is shown at [open: Q-REV-07, location and label]. |
| 2 | Open the link. | None | Not known: depends on open question Q-REV-07 (whether the link opens the original's detail page). |

**Postconditions and cleanup:** no change. Cleanup as `admin`: make both parts inactive, then delete the revision and the original.

**Notes:** None

### UI-REV-010: A part can be created with the Revision field empty

| Field | Value |
|---|---|
| **Summary** | The Revision field is optional: a part is created with it left empty. |
| **Requirement** | `R-REV-05`. Source: [part-views.md#L36](../../requirements/docs/part-views.md#L36) |
| **Area** | REV |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: optional field empty) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: non-structural category `QA-<suffix> Category`, created via `POST /api/part/category/` as `admin`; Pre-steps: log in, open the *Parts* view. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-REV-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open *Add Parts* and select *Create Part*. | None | The *Create Part* form opens. |
| 2 | Fill in the fields and leave *Revision* empty. | Name: `QA-<suffix> NoRev`<br>Description: `No revision`<br>Category: `QA-<suffix> Category`<br>Revision: empty<br>Other required fields: [open: Q-REV-05, which fields are required] | No validation error is shown on *Revision*. |
| 3 | Press *Submit*. | None | The form closes and the browser opens the new part's detail page. |
| 4 | Check the part's details. | None | No revision value is shown. |

**Postconditions and cleanup:** one part. Cleanup as `admin`: make it inactive, delete it, then delete the category.

**Notes:** None

### UI-REV-011: A part cannot be made a revision of itself

| Field | Value |
|---|---|
| **Summary** | Setting *Revision Of* of an existing part to the part itself is rejected. |
| **Requirement** | `R-REV-06`. Source: [part-revision.md#L36](../../requirements/docs/part-revision.md#L36) |
| **Area** | REV |
| **Type** | Negative |
| **Technique** | Negative (circular reference), Error guessing (self-reference) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = enabled [open: Q-REV-01, default and label]; Data: assembly `QA-<suffix> Assembly`, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the detail page of the part. |
| **Automation** | Partial: the form location is not known. |
| **Review** | Draft · Open question: Q-REV-01, Q-REV-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the form where *Revision Of* can be set on this part [open: Q-REV-03, form, for example *Edit Part*]. | None | The form opens. |
| 2 | Try to set *Revision Of* to the part itself and a revision code. | Revision Of: `QA-<suffix> Assembly`<br>Revision: `B` | Not known: depends on open question Q-REV-03 (whether the part is offered in the field or rejected on Submit). |
| 3 | Submit if possible. | None | The part is not saved as a revision of itself. Error text not known: depends on open question Q-REV-03. |
| 4 | Reopen the part's details. | None | *Revision Of* is empty and the revision is unchanged. |

**Postconditions and cleanup:** the original unchanged. Cleanup as `admin`: make inactive, then delete.

**Notes:** None

### UI-REV-012: A revision of a variant cannot point to a different template

| Field | Value |
|---|---|
| **Summary** | Creating a revision of a variant while the template reference points to a different template is rejected. |
| **Requirement** | `R-REV-10`. Source: [part-revision.md#L39](../../requirements/docs/part-revision.md#L39) |
| **Area** | REV |
| **Type** | Negative |
| **Technique** | Decision table (original is variant, template differs), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = enabled [open: Q-REV-01, default and label]; Data: templates `QA-<suffix> Template A` and `QA-<suffix> Template B`, variant `QA-<suffix> Variant` (Variant Of Template A, Assembly checked), created via `POST /api/part/` as `admin`; Pre-steps: log in, open the detail page of `QA-<suffix> Variant`. |
| **Automation** | Partial: depends on form fields. |
| **Review** | Draft · Open question: Q-REV-01, Q-REV-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu and select *Duplicate Part*. | None | The *Duplicate Part* form opens. |
| 2 | Set the revision fields and a distinct Name. Set the template reference to the other template if the form allows it [open: Q-REV-04, which field]. | Revision Of: `QA-<suffix> Variant`<br>Revision: `B`<br>Name: `QA-<suffix> Variant Rev B`<br>Template: `QA-<suffix> Template B` | Not known: depends on open question Q-REV-04 (whether the form lets the template be changed). |
| 3 | Press *Submit*. | None | No revision is created. Error text not known: depends on open question Q-REV-04. |

**Postconditions and cleanup:** two templates and the variant. Cleanup as `admin`: make all inactive, then delete the variant and the templates.

**Notes:** the positive same-template case is UI-REV-003.

### UI-REV-013: With revisions disabled, revision fields are not available

| Field | Value |
|---|---|
| **Summary** | With `PART_ENABLE_REVISION` off, revisions cannot be created. |
| **Requirement** | `R-REV-11`. Source: [part-revision.md#L43-48](../../requirements/docs/part-revision.md#L43-L48) |
| **Area** | REV |
| **Type** | Negative |
| **Technique** | Decision table (setting off), State transition (enabled to disabled) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = off [open: Q-REV-01, setting label]; Data: assembly `QA-<suffix> Assembly`, created via `POST /api/part/` as `admin`; Pre-steps: as `admin` switch the setting off; log in as `engineer`, open the part detail page. |
| **Automation** | Partial: depends on the setting's effect. |
| **Review** | Draft · Open question: Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part actions menu and select *Duplicate Part*. | None | Not known: depends on open question Q-REV-01 (what the disabled state changes; the form opens or the action is unavailable). |
| 2 | Look for the *Revision* and *Revision Of* fields. | None | Not known: depends on open question Q-REV-01 (whether the fields are hidden). |

**Postconditions and cleanup:** restore the setting as `admin`. Make the part inactive, then delete it.

**Notes:** None

### UI-REV-014: With assembly-only on, a revision of a non-assembly part is rejected

| Field | Value |
|---|---|
| **Summary** | With `PART_REVISION_ASSEMBLY_ONLY` on, a revision of a part that is not an assembly is not created. |
| **Requirement** | `R-REV-11`. Source: [part-revision.md#L43-48](../../requirements/docs/part-revision.md#L43-L48) |
| **Area** | REV |
| **Type** | Negative |
| **Technique** | Decision table (assembly-only on, Assembly off) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = on, `PART_REVISION_ASSEMBLY_ONLY` = on [open: Q-REV-01, labels]; Data: non-assembly part `QA-<suffix> Plain` (Assembly unchecked), created via `POST /api/part/` as `admin`; Pre-steps: as `admin` set the settings; log in, open the part detail page. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select *Duplicate Part* from the actions menu. | None | Not known: depends on open question Q-REV-01 (the form opens or the action is unavailable). |
| 2 | Set revision fields and a distinct Name; press *Submit*. | Revision Of: `QA-<suffix> Plain`<br>Revision: `B`<br>Name: `QA-<suffix> Plain B` | No revision is created. Error text not known: depends on open question Q-REV-01. |

**Postconditions and cleanup:** restore both settings as `admin`. Make the part inactive, then delete it.

**Notes:** None

### UI-REV-015: With assembly-only off, a revision of a non-assembly part is accepted

| Field | Value |
|---|---|
| **Summary** | With `PART_REVISION_ASSEMBLY_ONLY` off, a non-assembly part can have a revision. |
| **Requirement** | `R-REV-11`. Source: [part-revision.md#L43-48](../../requirements/docs/part-revision.md#L43-L48) |
| **Area** | REV |
| **Type** | Positive |
| **Technique** | Decision table (assembly-only off, Assembly off) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = on, `PART_REVISION_ASSEMBLY_ONLY` = off [open: Q-REV-01, labels]; Data: non-assembly part `QA-<suffix> Plain`, created via `POST /api/part/` as `admin`; Pre-steps: as `admin` set the settings; log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select *Duplicate Part* from the actions menu. | None | The *Duplicate Part* form opens. |
| 2 | Set revision fields and a distinct Name; press *Submit*. | Revision Of: `QA-<suffix> Plain`<br>Revision: `B`<br>Name: `QA-<suffix> Plain B` | Not known: depends on open question Q-REV-01 (the setting description is missing). Expected: the revision is created and its page opens. |

**Postconditions and cleanup:** restore the settings as `admin`. Make both parts inactive, then delete the revision and the original.

**Notes:** None

### UI-REV-016: A revision code differing only by letter case

| Field | Value |
|---|---|
| **Summary** | Creating a second revision whose code differs from an existing code only in letter case. |
| **Requirement** | `R-REV-07`. Source: [part-revision.md#L37](../../requirements/docs/part-revision.md#L37) |
| **Area** | REV |
| **Type** | Boundary |
| **Technique** | Error guessing (case variant), Equivalence partitioning (near-duplicate code) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = enabled [open: Q-REV-01, default and label]; Data: assembly `QA-<suffix> Assembly` and its revision `QA-<suffix> Assembly B` (Revision `B`), created via `POST /api/part/` as `admin`; Pre-steps: log in, open the original's detail page. |
| **Automation** | Yes once answered. |
| **Review** | Draft · Open question: Q-REV-01, Q-REV-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select *Duplicate Part* from the actions menu. | None | The form opens. |
| 2 | Set the revision fields with a lowercase code and a distinct Name. | Revision Of: `QA-<suffix> Assembly`<br>Revision: `b`<br>Name: `QA-<suffix> Assembly lower b` | Fields accept the values. |
| 3 | Press *Submit*. | None | Not known: depends on open question Q-REV-06 (whether `b` and `B` are the same code). |

**Postconditions and cleanup:** original, revision B, and a second revision if created. Cleanup as `admin`: make all inactive, then delete revisions first.

**Notes:** None

### UI-REV-017: A revision of a revision

| Field | Value |
|---|---|
| **Summary** | Duplicating a revision with *Revision Of* set to that revision. |
| **Requirement** | `R-REV-04`, `R-REV-07`. Source: [part-revision.md#L30](../../requirements/docs/part-revision.md#L30), [part-revision.md#L37](../../requirements/docs/part-revision.md#L37) |
| **Area** | REV |
| **Type** | Negative |
| **Technique** | Exploratory (chained revisions), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = enabled [open: Q-REV-01, default and label]; Data: assembly `QA-<suffix> Assembly` and its revision `QA-<suffix> Assembly B` (Revision `B`), created via `POST /api/part/` as `admin`; Pre-steps: log in, open the detail page of `QA-<suffix> Assembly B`. |
| **Automation** | Yes once answered. |
| **Review** | Draft · Open question: Q-REV-01, Q-REV-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select *Duplicate Part* from the actions menu. | None | The form opens. |
| 2 | Set *Revision Of* to the revision, a new code and a distinct Name; press *Submit*. | Revision Of: `QA-<suffix> Assembly B`<br>Revision: `C`<br>Name: `QA-<suffix> Assembly C` | Not known: depends on open question Q-REV-06 (whether a revision of a revision is allowed, and where the new part appears in the revision selector). |

**Postconditions and cleanup:** original, B, and C if created. Cleanup as `admin`: make all inactive, then delete newest first.

**Notes:** None

### UI-REV-018: The same revision code is allowed on revisions of different parts

| Field | Value |
|---|---|
| **Summary** | Revision code uniqueness applies per part, so code `B` can be used for revisions of two different parts. |
| **Requirement** | `R-REV-07`. Source: [part-revision.md#L37](../../requirements/docs/part-revision.md#L37) |
| **Area** | REV |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: same code, different original) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = enabled [open: Q-REV-01, default and label]; Data: assemblies `QA-<suffix> Assembly X` and `QA-<suffix> Assembly Y`, plus `QA-<suffix> X B` (Revision `B`, Revision Of X), created via `POST /api/part/` as `admin`; Pre-steps: log in, open the detail page of `QA-<suffix> Assembly Y`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select *Duplicate Part* from the actions menu. | None | The form opens. |
| 2 | Set revision fields and a distinct Name. | Revision Of: `QA-<suffix> Assembly Y`<br>Revision: `B`<br>Name: `QA-<suffix> Y B` | Fields accept the values. |
| 3 | Press *Submit*. | None | The form closes and the new part opens, linked to `QA-<suffix> Assembly Y`, with no uniqueness error. |

**Postconditions and cleanup:** two originals and two revisions. Cleanup as `admin`: make all inactive, then delete revisions first.

**Notes:** None

### UI-REV-019: Cancelling the Duplicate Part form creates no revision

| Field | Value |
|---|---|
| **Summary** | Closing the *Duplicate Part* form after entering revision values creates nothing. |
| **Requirement** | `R-REV-12`. Source: [part-revision.md#L53-64](../../requirements/docs/part-revision.md#L53-L64) |
| **Area** | REV |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-form) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: `PART_ENABLE_REVISION` = enabled [open: Q-REV-01, default and label]; Data: assembly `QA-<suffix> Assembly`, created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-REV-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Select *Duplicate Part* from the actions menu. | None | The form opens. |
| 2 | Enter revision values and a distinct Name. | Revision Of: `QA-<suffix> Assembly`<br>Revision: `B`<br>Name: `QA-<suffix> Assembly B` | Fields accept the values. |
| 3 | Close the form without submitting. | None | The form closes and the browser stays on the original part. |
| 4 | Search the *Parts* view. | `QA-<suffix> Assembly` | Only the original is listed, and no revision selector is shown. |

**Postconditions and cleanup:** original only. Cleanup as `admin`: make inactive, then delete.

**Notes:** None
