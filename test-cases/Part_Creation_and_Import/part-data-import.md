# Part data import: Part test cases

### UI-Part-007: Import from File opens the data import wizard, pre-linked to the Part data type

| Field | Value |
|---|---|
| **Summary** | Selecting *Import from File* in the *Add Parts* menu opens the data import wizard, already linked to the *Part* data type with no model-selection step. |
| **Requirement** | `R-Part-18`, `R-Part-24`. Source: [part-create.md#L55-60](../../requirements/docs/part-create.md#L55-L60), [concepts-data_import.md#L70-73](../../requirements/docs/concepts-data_import.md#L70-L73) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: staff user with import permission starting import from the Parts table) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: None; Pre-steps: log in at `http://localhost/web`, open the *Parts* view. |
| **Automation** | Yes: wizard launch check. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Add Parts* dropdown above the parts table. | None | The menu shows *Create Part* and *Import from File*. |
| 2 | Select *Import from File*. | None | The data import wizard opens. |
| 3 | Check the wizard for a data-type selection step. | None | No data-type selection step is shown; the session is already linked to the *Part* data type (context-sensitive import). |

**Postconditions and cleanup:** no records created; close or cancel the import session. If a session was created on the server, delete it as `admin` from the Admin Center import session list.

**Notes:** None.


---

### UI-Part-008: Import from File availability for a user without staff and change permission

| Field | Value |
|---|---|
| **Summary** | A user who has *Part* create permission but is not a staff user, and/or lacks the `change` permission for the *Part* model, attempts to use *Import from File*. |
| **Requirement** | `R-Part-19`. Source: [concepts-data_import.md#L26-29](../../requirements/docs/concepts-data_import.md#L26-L29) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Negative (user lacking the stated import permissions), Decision table (Part-create permission present, staff/change permission absent) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `engineer` (manage parts, not a staff user); Settings: None; Data: None; Pre-steps: log in at `http://localhost/web`, open the *Parts* view. |
| **Automation** | No: outcome depends on an open question. |
| **Review** | Draft · Open question: Q-Part-01 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Add Parts* dropdown above the parts table. | None | Proposed, to confirm in Q-Part-01: *Import from File* is not shown, because importing needs staff status and the `change` permission (R-Part-19). |
| 2 | If the option is shown, select *Import from File*. | None | The import wizard does not open for this user (R-Part-19: importing needs staff status and the `change` permission). Open: Q-Part-01 (how access is refused). |

**Postconditions and cleanup:** none, no data created.

**Notes:** The docs state two different permission requirements for *Add Parts* (create) and data import (staff + change), with no statement on which one gates this specific wizard entry point (index doc issue 7).


---

### UI-Part-009: Importing parts with the category column mapped to an existing category by name

| Field | Value |
|---|---|
| **Summary** | During *Import from File*, the category column in the uploaded file is mapped to an existing part category using the category's `name` as the natural key. |
| **Requirement** | `R-Part-20`, `R-Part-22`. Source: [concepts-data_import.md#L30-36](../../requirements/docs/concepts-data_import.md#L30-L36), [concepts-data_import.md#L37-45](../../requirements/docs/concepts-data_import.md#L37-L45) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: related record exists and is mapped by natural key), Decision table (natural key available = name) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: non-structural category `QA-<suffix> Category`, created as `admin`; a CSV file with one part row whose category column value is `QA-<suffix> Category`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*, upload the file. |
| **Automation** | Yes: file-based import with column mapping. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the field mapping step for the category column. | None | The category column is available to map; the category field accepts mapping by the `name` natural key. |
| 2 | Map the category column to the Category field using `name`. | Category column value: `QA-<suffix> Category` | The mapping is accepted with no error. |
| 3 | Proceed to load and process the data. | None | The row is loaded and linked to the existing category `QA-<suffix> Category`. |

**Postconditions and cleanup:** one import session and, once processed, one new part in `QA-<suffix> Category`. Cleanup as `admin`: delete the imported part, the import session, and the category.

**Notes:** None.


---

### UI-Part-010: Importing parts with a related field mapped by ID when no natural key is used

| Field | Value |
|---|---|
| **Summary** | During *Import from File*, a related field without a usable natural key is mapped using the record's `ID` (primary key), the default mapping method. |
| **Requirement** | `R-Part-22`. Source: [concepts-data_import.md#L37-45](../../requirements/docs/concepts-data_import.md#L37-L45) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Decision table (natural key not used = ID-only mapping) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: non-structural category `QA-<suffix> Category`, created as `admin`, with its database `ID` noted; a CSV file with one part row whose category column value is that category's `ID`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*, upload the file. |
| **Automation** | Yes: file-based import with ID mapping. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Map the category column to the Category field using `ID`. | Category column value: `<category ID>` | The mapping is accepted with no error. |
| 2 | Proceed to load and process the data. | None | The row is loaded and correctly linked to the category with that `ID`. |

**Postconditions and cleanup:** one import session and, once processed, one new part in `QA-<suffix> Category`. Cleanup as `admin`: delete the imported part, the import session, and the category.

**Notes:** None.


---

### UI-Part-011: A related field whose identifier cannot be determined must be mapped manually

| Field | Value |
|---|---|
| **Summary** | When the uploaded file's category column cannot be auto-matched to an existing category's `ID` or `name`, the import wizard requires the user to map the field manually before the row can be processed. |
| **Requirement** | `R-Part-23`. Source: [concepts-data_import.md#L37-45](../../requirements/docs/concepts-data_import.md#L37-L45) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Error guessing (ambiguous/unmatched category reference in the file) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: a CSV file with one part row whose category column value does not match any existing category by `ID` or `name`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*, upload the file. |
| **Automation** | No: needs a file crafted with an unresolvable reference. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Reach the field mapping step. | None | The category column's unique identifier cannot be auto-determined. |
| 2 | Attempt to proceed without mapping the field manually. | None | The user must manually map the category field to an existing record before the row can be processed. |
| 3 | Manually map the category field to an existing category. | Category: `QA-<suffix> Category` | The mapping is accepted and the row can proceed to processing. |

**Postconditions and cleanup:** one import session. Cleanup as `admin`: delete the import session and any created records.

**Notes:** None.


---

### UI-Part-012: Multi-level import is not supported; one model is imported per session

| Field | Value |
|---|---|
| **Summary** | The *Import from File* wizard imports a single data model (*Part*) per session; there is no option to import related models (such as part categories) in the same session. |
| **Requirement** | `R-Part-21`. Source: [concepts-data_import.md#L30-36](../../requirements/docs/concepts-data_import.md#L30-L36) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: a second, unrelated model in the same session) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: None; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*. |
| **Automation** | Yes: UI control check. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the wizard for any option to add a second model (for example part categories) to the same session. | None | No such option exists; the session is scoped to the single *Part* data type it was opened for. |

**Postconditions and cleanup:** none, no data created; cancel the session.

**Notes:** Related data (such as part categories) must be imported in a separate, earlier session (R-Part-20).


---

### UI-Part-013: An import session persists on the server and can be resumed after navigating away

| Field | Value |
|---|---|
| **Summary** | An in-progress import session remains on the server; the user can leave the import page and return later to find the session and its progress unchanged. |
| **Requirement** | `R-Part-25`. Source: [concepts-data_import.md#L50-55](../../requirements/docs/concepts-data_import.md#L50-L55) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Exploratory (navigate away mid-session and return) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: a CSV file with at least one valid part row; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*, upload the file and complete the field mapping step. |
| **Automation** | No: involves navigation timing. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Note the import session's progress, then navigate away to another page (for example the *Parts* view). | None | The browser leaves the import page without error. |
| 2 | Return to the import session via the Admin Center import session list. | None | The same session is listed, with the same progress as when it was left. |

**Postconditions and cleanup:** one import session. Cleanup as `admin`: delete the import session and any created records.

**Notes:** None.


---

### UI-Part-014: Import sessions are listed in the Admin Center

| Field | Value |
|---|---|
| **Summary** | An import session created from *Import from File* appears in the list of import sessions in the Admin Center. |
| **Requirement** | `R-Part-26`. Source: [concepts-data_import.md#L50-55](../../requirements/docs/concepts-data_import.md#L50-L55) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: session created, then checked in the Admin Center list) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: a CSV file with at least one valid part row; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*, upload the file. |
| **Automation** | Yes: list visibility check. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the Admin Center and find the data import management page. | None | The import session list is shown. |
| 2 | Check the list for the session just created. | None | The session created in step "Pre-steps" is listed. |

**Postconditions and cleanup:** one import session. Cleanup as `admin`: delete the import session and any created records.

**Notes:** None.


---

### UI-Part-015: A general import session from the Admin Center requires selecting the data type first

| Field | Value |
|---|---|
| **Summary** | Starting an import session from the Admin Center (rather than from the Parts table) requires the staff user to first select which data type (model) to import, unlike a context-linked session from *Import from File*. |
| **Requirement** | `R-Part-27`, `R-Part-24`. Source: [concepts-data_import.md#L64-69](../../requirements/docs/concepts-data_import.md#L64-L69), [concepts-data_import.md#L70-73](../../requirements/docs/concepts-data_import.md#L70-L73) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Decision table (import start point: Admin Center = data-type selection required; Parts table = pre-linked, no selection) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: None; Pre-steps: log in at `http://localhost/web`, open the Admin Center. |
| **Automation** | Yes: UI step check. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | From the Admin Center, start a new general import session. | None | The wizard first requires the user to select the type of data (model) to import, for example *Part*. |
| 2 | Select *Part* as the data type and proceed. | None | The session proceeds to file upload, scoped to the selected data type. |

**Postconditions and cleanup:** one import session. Cleanup as `admin`: delete the import session.

**Notes:** Contrast with UI-Part-007, where a session opened from the Parts table skips this selection step.


---

### UI-Part-016: The server auto-matches uploaded columns to part fields, and the mapping can be adjusted

| Field | Value |
|---|---|
| **Summary** | After uploading a file, the server automatically associates file columns with *Part* model fields; the user can manually change a mapping that was matched incorrectly. |
| **Requirement** | `R-Part-28`. Source: [concepts-data_import.md#L84-91](../../requirements/docs/concepts-data_import.md#L84-L91) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: auto-matched column; manually re-mapped column) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: a CSV file with a `name` column and a column header that does not exactly match a field name (for example `part_desc` for Description); Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*, upload the file. |
| **Automation** | Yes: field mapping UI check. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Reach the field mapping step. | None | The `name` column is automatically mapped to the Name field. |
| 2 | Check the mapping for the `part_desc` column. | None | The column is either left unmapped or mapped to a field other than Description; it is not automatically matched. |
| 3 | Manually set `part_desc` to map to the Description field. | None | The mapping is accepted with no error. |

**Postconditions and cleanup:** one import session. Cleanup as `admin`: delete the import session and any created records.

**Notes:** Which columns the server matches automatically beyond an exact name match is not stated; the mismatched header in step 2 is chosen to demonstrate a column the server would not auto-match.


---

### UI-Part-017: A valid row must be selected and confirmed before it is imported

| Field | Value |
|---|---|
| **Summary** | A row with no validation errors is shown as *Pending* after processing, and is only imported into the database once the user selects and confirms it. |
| **Requirement** | `R-Part-29`, `R-Part-31`. Source: [concepts-data_import.md#L98-113](../../requirements/docs/concepts-data_import.md#L98-L113) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | State transition (Pending -> selected and confirmed -> Imported) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: non-structural category `QA-<suffix> Category`, created as `admin`; a CSV file with one valid part row (Name `QA-<suffix> Import Part`, category mapped to `QA-<suffix> Category`); Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*, upload the file, map the fields, and process the data. |
| **Automation** | Yes: core import flow. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the row's status after processing. | None | The row is shown as *Pending* ("contains no errors, and is ready to be imported"). |
| 2 | Select the row and confirm the import. | None | The row is imported into the database. |
| 3 | Check the row's status. | None | The row is shown as *Imported* ("has been successfully imported into the database"). |
| 4 | Open the *Parts* view and search for the new part. | Name: `QA-<suffix> Import Part` | The part exists, in category `QA-<suffix> Category`. |

**Postconditions and cleanup:** one new part. Cleanup as `admin`: set the part inactive, delete it, delete the import session, then delete the category.

**Notes:** None.


---

### UI-Part-018: A row with an error must be corrected and re-processed before it can be imported

| Field | Value |
|---|---|
| **Summary** | A row that fails validation during processing is shown as *Error*; the user corrects the data in the wizard and re-processes the row, which then becomes *Pending* and can be imported. |
| **Requirement** | `R-Part-30`, `R-Part-31`. Source: [concepts-data_import.md#L98-113](../../requirements/docs/concepts-data_import.md#L98-L113) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | State transition (Error -> corrected -> Pending -> Imported), Error guessing (missing required Name value) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: non-structural category `QA-<suffix> Category`, created as `admin`; a CSV file with one part row that has an empty Name column and category mapped to `QA-<suffix> Category`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*, upload the file, map the fields, and process the data. |
| **Automation** | Yes: error-state correction flow. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the row's status after processing. | None | The row is shown as *Error* ("contains an error which must be corrected before it can be imported"); the error is displayed to the user. |
| 2 | Edit the row's Name value in the wizard. | Name: `QA-<suffix> Corrected Part` | The field accepts the value. |
| 3 | Re-process the row. | None | The row's status changes to *Pending*. |
| 4 | Select the row and confirm the import. | None | The row's status changes to *Imported*, and the part is created with the corrected Name. |

**Postconditions and cleanup:** one new part. Cleanup as `admin`: set the part inactive, delete it, delete the import session, then delete the category.

**Notes:** The exact wording of the displayed error message is not stated (R-Part-30 note).


---

### UI-Part-019: An individual row can be removed from the import session instead of being imported

| Field | Value |
|---|---|
| **Summary** | A processed row can be individually removed (deleted) from the import session rather than imported, while the session's other rows are unaffected. |
| **Requirement** | `R-Part-32`. Source: [concepts-data_import.md#L98-113](../../requirements/docs/concepts-data_import.md#L98-L113) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (row action: remove, instead of import) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: non-structural category `QA-<suffix> Category`, created as `admin`; a CSV file with two valid part rows (`QA-<suffix> Keep Part`, `QA-<suffix> Remove Part`), both mapped to `QA-<suffix> Category`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*, upload the file, map the fields, and process the data. |
| **Automation** | Yes: per-row action check. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check both rows are *Pending*. | None | Both rows show *Pending*. |
| 2 | Remove the `QA-<suffix> Remove Part` row. | None | The row is deleted from the import session and no longer listed. |
| 3 | Select and confirm the `QA-<suffix> Keep Part` row. | None | The row is imported; its status becomes *Imported*. |
| 4 | Open the *Parts* view and search for both names. | Names: `QA-<suffix> Keep Part`, `QA-<suffix> Remove Part` | `QA-<suffix> Keep Part` exists. `QA-<suffix> Remove Part` does not exist. |

**Postconditions and cleanup:** one new part (`QA-<suffix> Keep Part`). Cleanup as `admin`: set the part inactive, delete it, delete the import session, then delete the category.

**Notes:** None.


---

### UI-Part-020: The import session is marked complete and can be closed once every row is processed

| Field | Value |
|---|---|
| **Summary** | Once every row in the session has been imported or removed, the session is considered complete and the user can close it. |
| **Requirement** | `R-Part-33`. Source: [concepts-data_import.md#L114-117](../../requirements/docs/concepts-data_import.md#L114-L117) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | State transition (all rows processed -> session complete -> closed) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: non-structural category `QA-<suffix> Category`, created as `admin`; a CSV file with one valid part row mapped to `QA-<suffix> Category`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*, upload the file, map the fields, process the data, then select and confirm the row. |
| **Automation** | Yes: session completion check. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the session status once the only row is *Imported*. | None | The import session is shown as complete. |
| 2 | Close the session. | None | The session closes; the imported record remains stored in the database. |

**Postconditions and cleanup:** one new part. Cleanup as `admin`: set the part inactive, delete it, then delete the category. (The session was already closed in step 2.)

**Notes:** None.


---

### UI-Part-021: Bulk data import is presented as a non-reversible action

| Field | Value |
|---|---|
| **Summary** | Before performing a bulk data import, the user is warned that the action is non-reversible. |
| **Requirement** | `R-Part-34`. Source: [concepts-data_import.md#L13-25](../../requirements/docs/concepts-data_import.md#L13-L25) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Error guessing (user proceeds without noticing a destructive, non-reversible action) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: None; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*. |
| **Automation** | No: outcome depends on an open question. |
| **Review** | Draft · Open question: Q-Part-02 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the import wizard, before uploading a file, for a warning about the action being non-reversible. | None | Proposed, to confirm in Q-Part-02: the wizard shows a warning that the import cannot be undone (R-Part-34: bulk upload is non-reversible). |

**Postconditions and cleanup:** none, no data created.

**Notes:** The docs state this warning as a documentation-page admonition, not as a described UI element (guardrail 9: possible RAG chunk boundary is not the issue here, the text itself is clearly a docs-only admonition box, but whether the app reproduces it is unconfirmed).


---

### UI-Part-022: Updating existing records requires the ID field to be mapped

| Field | Value |
|---|---|
| **Summary** | In an Admin Center import session with *Update Existing Records* selected, the uploaded file's unique-identifier column must be mapped to the `ID` field before the row can be matched to an existing part. |
| **Requirement** | `R-Part-35`, `R-Part-37`. Source: [concepts-data_import.md#L118-130](../../requirements/docs/concepts-data_import.md#L118-L130), [concepts-data_import.md#L140-145](../../requirements/docs/concepts-data_import.md#L140-L145), [concepts-data_import.md#L131-139](../../requirements/docs/concepts-data_import.md#L131-L139) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: ID column correctly mapped) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: an existing part `QA-<suffix> Update Source`, created as `admin`, with its `ID` noted; a CSV file exported/prepared with one row containing that part's `ID`; Pre-steps: log in at `http://localhost/web`, open the Admin Center, start a new import session for the *Part* model with *Update Existing Records* selected, and upload the file. |
| **Automation** | Yes: update-mode mapping check. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Reach the field mapping step. | None | The session is in update mode (*Update Existing Records* was selected when the session was created). |
| 2 | Map the file's identifier column to the `ID` field. | ID column value: `<part ID>` | The mapping is accepted with no error. |
| 3 | Proceed to load and process the data. | None | The row is matched to the existing part `QA-<suffix> Update Source` by `ID`. |

**Postconditions and cleanup:** no new part created. Cleanup as `admin`: delete the import session, then delete the part `QA-<suffix> Update Source`.

**Notes:** None.


---

### UI-Part-023: Import from File (Parts table) does not offer Update Existing Records; only an Admin Center session does

| Field | Value |
|---|---|
| **Summary** | A session started from *Import from File* in the Parts table does not offer an *Update Existing Records* option; that option is only available when creating a general import session from the Admin Center. |
| **Requirement** | `R-Part-37`. Source: [concepts-data_import.md#L131-139](../../requirements/docs/concepts-data_import.md#L131-L139) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Decision table (session start point: Parts table = no update option; Admin Center = update option available) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: None; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*. |
| **Automation** | Yes: UI control check. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the *Import from File* session creation step for an *Update Existing Records* option. | None | No *Update Existing Records* option is offered; the session can only create new *Part* records. |
| 2 | Cancel this session. Open the Admin Center and start a new general import session for the *Part* model. | None | The session creation step offers an *Update Existing Records* option. |

**Postconditions and cleanup:** none, no data created; cancel both sessions.

**Notes:** Contrast with UI-Part-022, which uses the Admin Center session with the option selected.


---

### UI-Part-024: A matching row in an update-mode session updates the existing record's fields

| Field | Value |
|---|---|
| **Summary** | In an update-mode import session, a row whose `ID` matches an existing part updates that part's fields with the values from the file, rather than creating a new part. |
| **Requirement** | `R-Part-38`. Source: [concepts-data_import.md#L146-150](../../requirements/docs/concepts-data_import.md#L146-L150) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | What-if business scenario (a stores user bulk-updates part descriptions via a re-imported, edited export) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: an existing part `QA-<suffix> Update Target` with Description `Original description`, created as `admin`, with its `ID` noted; a CSV file with one row containing that part's `ID` and Description `QA-<suffix> Updated description`; Pre-steps: log in at `http://localhost/web`, open the Admin Center, start a new import session for the *Part* model with *Update Existing Records* selected, upload the file, and map the `ID` and Description columns. |
| **Automation** | Yes: update-mode data check. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Process the data. | None | The row is matched to `QA-<suffix> Update Target` by `ID`, and shown as *Pending*. |
| 2 | Select the row and confirm the import. | None | The row's status becomes *Imported*. |
| 3 | Open the part `QA-<suffix> Update Target` detail page. | None | The Description field reads `QA-<suffix> Updated description`. No new part was created. |

**Postconditions and cleanup:** no new part created; one existing part modified. Cleanup as `admin`: delete the import session, set the part inactive, then delete it.

**Notes:** None.


---

### UI-Part-025: Creating and updating records cannot be mixed in a single import session

| Field | Value |
|---|---|
| **Summary** | In an update-mode import session, a row whose identifier does not match any existing part cannot be used to create a new record in that same session. |
| **Requirement** | `R-Part-36`. Source: [concepts-data_import.md#L118-130](../../requirements/docs/concepts-data_import.md#L118-L130) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Negative (non-matching row in an update-mode session), Error guessing (file mixes a matching and a non-matching row) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: an existing part `QA-<suffix> Update Target`, created as `admin`, with its `ID` noted; a CSV file with two rows: one with that part's `ID`, one with an `ID` value that matches no existing part; Pre-steps: log in at `http://localhost/web`, open the Admin Center, start a new import session for the *Part* model with *Update Existing Records* selected, upload the file, and map the `ID` column. |
| **Automation** | No: outcome depends on an open question. |
| **Review** | Draft · Open question: Q-Part-03 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Process the data. | None | The row with the matching `ID` is shown as *Pending*, matched to `QA-<suffix> Update Target`. Open: Q-Part-03 (the status shown for the row whose `ID` matches no existing part: Error, silently skipped, or something else). |
| 2 | Attempt to proceed with the non-matching row. | None | No new part is created from the non-matching row (R-Part-36: creating and updating cannot be mixed in one import session). Open: Q-Part-03 (whether the session can complete with the row present). |

**Postconditions and cleanup:** cleanup as `admin`: delete the import session, delete any record created from the non-matching row (if the open question is answered to confirm one was created), then delete `QA-<suffix> Update Target`.

**Notes:** None.


---

### UI-Part-026: Uploading a file of an unsupported type or an empty file in the import wizard

| Field | Value |
|---|---|
| **Summary** | Uploading an unsupported file type (a `.txt` file renamed from plain text) or an empty CSV file in the *Import from File* wizard is handled without creating importable rows. |
| **Requirement** | `R-Part-28`, `R-Part-18`. Source: [concepts-data_import.md#L78-83](../../requirements/docs/concepts-data_import.md#L78-L83), [part-create.md#L55-60](../../requirements/docs/part-create.md#L55-L60) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid classes: unsupported file type; empty file), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: file `QA-<suffix>-notes.txt` with plain text; empty file `QA-<suffix>-empty.csv` (0 bytes); Pre-steps: log in at `http://localhost/web`, open the *Parts* view. |
| **Automation** | No: outcome depends on an open question. |
| **Review** | Draft · Open question: Q-Part-04 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open *Add Parts* > *Import from File*. | None | The data import wizard opens at the file upload step. |
| 2 | Upload the unsupported file and submit. | File: `QA-<suffix>-notes.txt` | Proposed, to confirm in Q-Part-04: the file is rejected with an error and no import session is created. Open: Q-Part-04 (the error message). |
| 3 | Restart the wizard and upload the empty file. | File: `QA-<suffix>-empty.csv` | Proposed, to confirm in Q-Part-04: the file is rejected with an error and no rows are imported. Open: Q-Part-04 (the error message). |

**Postconditions and cleanup:** a session may exist, depending on Q-Part-04. Cleanup as `admin`: delete any `QA-<suffix>` import session from the Admin Center.

**Notes:** The docs list no accepted file formats.


---

### UI-Part-027: Update-mode import with the ID field left unmapped

| Field | Value |
|---|---|
| **Summary** | In an Admin Center update-mode import session, leaving the `ID` field unmapped is handled, since updating requires the `ID` field to be mapped. |
| **Requirement** | `R-Part-35`, `R-Part-37`. Source: [concepts-data_import.md#L118-130](../../requirements/docs/concepts-data_import.md#L118-L130), [concepts-data_import.md#L140-145](../../requirements/docs/concepts-data_import.md#L140-L145) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | Negative (required mapping omitted), Equivalence partitioning (invalid class: ID not mapped) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: part `QA-<suffix> Update Target` created as `admin`; CSV with columns `name` and `description` only (no ID column); Pre-steps: log in at `http://localhost/web`, open the Admin Center, start an import session for the *Part* model with *Update Existing Records* selected, upload the file. |
| **Automation** | No: outcome depends on an open question. |
| **Review** | Draft · Open question: Q-Part-05 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | At the mapping step, leave the `ID` field unmapped and proceed. | None | The wizard does not update records while the `ID` field is unmapped (R-Part-35: the `ID` field must be mapped). Open: Q-Part-05 (whether it blocks proceeding or shows an error, and the text). |
| 2 | If processing runs, check the row states. | None | `QA-<suffix> Update Target` is not changed (R-Part-35). Open: Q-Part-05 (the row state). |

**Postconditions and cleanup:** cleanup as `admin`: delete the import session, set the part inactive, then delete it.

**Notes:** None.


---

### UI-Part-028: A row in Error state cannot be imported until corrected

| Field | Value |
|---|---|
| **Summary** | The user attempts to import a row shown as *Error* without correcting it, and the row is not imported. |
| **Requirement** | `R-Part-31`, `R-Part-29`. Source: [concepts-data_import.md#L106-110](../../requirements/docs/concepts-data_import.md#L106-L110), [concepts-data_import.md#L104](../../requirements/docs/concepts-data_import.md#L104) |
| **Area** | Part |
| **Type** | Negative |
| **Technique** | State transition (blocked transition: Error -> Imported without correction), Negative |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin` (staff, full permissions); Settings: None; Data: category `QA-<suffix> Category` created as `admin`; CSV with one row with empty Name and category `QA-<suffix> Category`; Pre-steps: log in at `http://localhost/web`, open *Parts* > *Add Parts* > *Import from File*, upload, map fields, process the data. |
| **Automation** | No: outcome depends on an open question. |
| **Review** | Draft · Open question: Q-Part-06 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Check the row status. | None | The row is shown as *Error*. |
| 2 | Try to select and import the row without editing it. | None | The row is not imported and stays in *Error* state. Open: Q-Part-06 (whether the import control is disabled or hidden, or an error is shown). |
| 3 | Search the *Parts* view for any part created by the row. | Empty name; category `QA-<suffix> Category` | No part is created in `QA-<suffix> Category`. |

**Postconditions and cleanup:** no part created. Cleanup as `admin`: delete the import session, then the category.

**Notes:** Complements UI-Part-018, which covers the correction path.
