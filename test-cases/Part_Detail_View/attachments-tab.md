# Attachments tab: Detail_View test cases

The part *Attachments* tab: listing, uploading files, adding external links, viewing and downloading, thumbnails and the `is_image` flag, renaming, and permissions. Parts are created through the API as `admin`. File names carry the run suffix `QA-<suffix>`. The docs name the buttons "Add attachment" and "Add external link" only; all other labels, form fields and messages are open (Q-Detail_View-50 to Q-Detail_View-53). The `is_image` flag is an API-visible field; where it is shown in the UI is open (Q-Detail_View-52).

---

### UI-Detail_View-401: Open the Attachments tab of a part

| Field | Value |
|---|---|
| **Summary** | A user can open the *Attachments* tab of a part and see the part's attachments table. |
| **Requirement** | `R-Detail_View-42`. Source: [part-views.md#Attachments](../../requirements/docs/part-views.md#L154), [concepts-attachments.md#Attachments Tab](../../requirements/docs/concepts-attachments.md#L22) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: part with no attachments) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-50 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Attachments* tab. | None | The tab opens and displays all attachments associated with the part (R-Detail_View-42); the part has none yet. The *Add attachment* and *Add external link* buttons are available (R-Detail_View-43). Open: Q-Detail_View-50 (table column labels and empty-state text). |

**Postconditions and cleanup:** Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-402: Upload a file with Add attachment

| Field | Value |
|---|---|
| **Summary** | A user can upload a file to a part with the *Add attachment* button, and it is listed in the *Attachments* tab. |
| **Requirement** | `R-Detail_View-43`. Source: [concepts-attachments.md#Adding Attachments](../../requirements/docs/concepts-attachments.md#L55); `R-Detail_View-42`. Source: [part-views.md#Attachments](../../requirements/docs/part-views.md#L154) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: one file upload) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; local file `QA-<suffix>-datasheet.pdf`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-50 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *Add attachment*. | None | A form opens to upload a file (R-Detail_View-43). Open: Q-Detail_View-50 (form title, field labels, required fields). |
| 2 | Select the file and submit. | File: `QA-<suffix>-datasheet.pdf` | The form closes and the file is listed in the *Attachments* tab (R-Detail_View-42). Open: Q-Detail_View-50 (confirmation message, columns shown). |

**Postconditions and cleanup:** One attachment exists on the part. Cleanup as `admin`: delete the attachment [open: Q-Detail_View-50, delete control not described in the docs], set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-403: Add an external link with Add external link

| Field | Value |
|---|---|
| **Summary** | A user can add a URL to a part with the *Add external link* button, and it is listed in the *Attachments* tab. |
| **Requirement** | `R-Detail_View-43`. Source: [concepts-attachments.md#Adding Attachments](../../requirements/docs/concepts-attachments.md#L55) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: valid URL) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-50 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *Add external link*. | None | A form opens to add a link (R-Detail_View-43). Open: Q-Detail_View-50 (form title, field labels, required fields). |
| 2 | Enter the URL and submit. | Link: `https://example.com/QA-<suffix>` | The form closes and the link is listed in the *Attachments* tab (R-Detail_View-43). Open: Q-Detail_View-50 (how the link is displayed). |

**Postconditions and cleanup:** One link attachment exists. Cleanup as `admin`: delete it, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-404: A part can have several attachments

| Field | Value |
|---|---|
| **Summary** | A part can hold several attachments (a file and a link, then a second file) at the same time, all listed. |
| **Requirement** | `R-Detail_View-42`. Source: [part-views.md#Attachments](../../requirements/docs/part-views.md#L154) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Boundary value analysis (more than one attachment) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; local files `QA-<suffix>-datasheet.pdf`, `QA-<suffix>-manual.pdf`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-50 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the first file with *Add attachment*. | File: `QA-<suffix>-datasheet.pdf` | The file is listed (R-Detail_View-42). |
| 2 | Upload the second file with *Add attachment*. | File: `QA-<suffix>-manual.pdf` | Both files are listed; a part can have several attachments (R-Detail_View-42). |
| 3 | Add a link with *Add external link*. | Link: `https://example.com/QA-<suffix>` | Three attachments are listed (R-Detail_View-42). Open: Q-Detail_View-50 (row order). |

**Postconditions and cleanup:** Three attachments exist. Cleanup as `admin`: delete the attachments, set the part inactive and delete it.

**Notes:** The docs state no upper limit on the number of attachments (Q-Detail_View-50).

---

### UI-Detail_View-405: Attachments of one part are not listed on another part

| Field | Value |
|---|---|
| **Summary** | The *Attachments* tab lists only the attachments of the open part. |
| **Requirement** | `R-Detail_View-42`. Source: [part-views.md#Attachments](../../requirements/docs/part-views.md#L154) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Exploratory (two parts, attachment isolation) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: parts `QA-<suffix> Attach A` and `QA-<suffix> Attach B` created via `POST /api/part/` as `admin`; local file `QA-<suffix>-datasheet.pdf`; Pre-steps: log in, open part A's *Attachments* tab. |
| **Automation** | Yes. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file to part A with *Add attachment*. | File: `QA-<suffix>-datasheet.pdf` | The file is listed on part A (R-Detail_View-42). |
| 2 | Open part B and its *Attachments* tab. | None | The tab shows the attachments associated with part B only (R-Detail_View-42); the file of part A is not listed. |

**Postconditions and cleanup:** Cleanup as `admin`: delete part A's attachment, set both parts inactive and delete them.

**Notes:** None.

---

### UI-Detail_View-406: View and download an uploaded file

| Field | Value |
|---|---|
| **Summary** | A user with view access to the part can download or view an uploaded file from the *Attachments* tab. |
| **Requirement** | `R-Detail_View-44`. Source: [concepts-attachments.md#L34](../../requirements/docs/concepts-attachments.md#L34) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: user with permission) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `reader` (view only) [open: Q-Detail_View-51, which permission is "appropriate"]; Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` and the file `QA-<suffix>-datasheet.pdf` attached as `admin`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Partial: the download control is not described in the docs. |
| **Review** | Draft · Open question: Q-Detail_View-51 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Use the attachment's download or view control. | Attachment: `QA-<suffix>-datasheet.pdf` | The file can be downloaded or viewed by a user with the appropriate permissions (R-Detail_View-44). Open: Q-Detail_View-51 (control label, whether the file opens in a new tab or downloads). |
| 2 | Compare the downloaded file with the uploaded one. | None | Proposed, to confirm in Q-Detail_View-51: the content is identical to the uploaded file. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the attachment, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-407: User without any permission cannot view a part's attachments

| Field | Value |
|---|---|
| **Summary** | `noaccess` cannot see or download a part's attachments. |
| **Requirement** | `R-Detail_View-44`. Source: [concepts-attachments.md#L34](../../requirements/docs/concepts-attachments.md#L34) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (user without permission) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess` (no permissions); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` and the file `QA-<suffix>-datasheet.pdf` attached as `admin`; Pre-steps: log in as `noaccess`. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-51 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part's detail page by its URL, then look for the *Attachments* tab. | URL: `/web/part/<pk>/` | Only users with the appropriate permissions can download or view uploaded files (R-Detail_View-44), so the file is not available to `noaccess`. Open: Q-Detail_View-51 (what `noaccess` sees: message text, redirect, hidden tab). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the attachment, set the part inactive and delete it.

**Notes:** Related: Q-Detail_View-19 (`noaccess` opening a part by URL).

---

### UI-Detail_View-408: View-only user does not get the add controls

| Field | Value |
|---|---|
| **Summary** | `reader` opens the *Attachments* tab and cannot add a file or a link. |
| **Requirement** | `R-Detail_View-43`. Source: [concepts-attachments.md#Adding Attachments](../../requirements/docs/concepts-attachments.md#L55); `R-Detail_View-44`. Source: [concepts-attachments.md#L34](../../requirements/docs/concepts-attachments.md#L34) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (view-only user), Decision table (role x action) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-50 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look for the *Add attachment* and *Add external link* buttons. | None | The tab is shown. Proposed, to confirm in Q-Detail_View-50: both buttons are hidden or disabled, so no attachment can be added. |

**Postconditions and cleanup:** Cleanup as `admin`: set the part inactive and delete it.

**Notes:** The docs state no permission for adding attachments.

---

### UI-Detail_View-409: A valid image gets a thumbnail and is_image true

| Field | Value |
|---|---|
| **Summary** | Uploading a valid PNG image creates a thumbnail in the background, and `is_image` is true. |
| **Requirement** | `R-Detail_View-45`. Source: [concepts-attachments.md#Image Thumbnails](../../requirements/docs/concepts-attachments.md#L38-L41); `R-Detail_View-46`. Source: [concepts-attachments.md#L42](../../requirements/docs/concepts-attachments.md#L42) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: valid image) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; local file `QA-<suffix>-image.png` (valid PNG, 800x400 px); Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Partial: thumbnail display in the UI is not described. |
| **Review** | Draft · Open question: Q-Detail_View-52 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the image with *Add attachment*. | File: `QA-<suffix>-image.png` | The file is listed (R-Detail_View-42). |
| 2 | Wait for the background thumbnail generation, then reload the tab. | None | A thumbnail is generated with the original aspect ratio (2:1) (R-Detail_View-45). Open: Q-Detail_View-52 (where the thumbnail is shown in the UI, how long it takes). |
| 3 | Check the `is_image` flag of the attachment [open: Q-Detail_View-52, where the flag is read: UI or API endpoint]. | None | `is_image` is `true` (R-Detail_View-46). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the attachment, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-410: Other Pillow image formats get a thumbnail

| Field | Value |
|---|---|
| **Summary** | JPEG, GIF, BMP and WEBP images are treated as valid images and get a thumbnail. |
| **Requirement** | `R-Detail_View-45`. Source: [concepts-attachments.md#Supported Formats](../../requirements/docs/concepts-attachments.md#L47) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: each supported format) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; valid image files `QA-<suffix>-image.jpg`, `.gif`, `.bmp`, `.webp`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Partial: thumbnail display in the UI is not described. |
| **Review** | Draft · Open question: Q-Detail_View-52 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the JPEG file. | File: `QA-<suffix>-image.jpg` | A thumbnail is generated and `is_image` is true (R-Detail_View-45, R-Detail_View-46). Open: Q-Detail_View-52 (where it is visible). |
| 2 | Upload the GIF file. | File: `QA-<suffix>-image.gif` | A thumbnail is generated and `is_image` is true (R-Detail_View-45). Open: Q-Detail_View-52. |
| 3 | Upload the BMP file. | File: `QA-<suffix>-image.bmp` | A thumbnail is generated and `is_image` is true (R-Detail_View-45). Open: Q-Detail_View-52. |
| 4 | Upload the WEBP file. | File: `QA-<suffix>-image.webp` | A thumbnail is generated and `is_image` is true (R-Detail_View-45). Open: Q-Detail_View-52. |

**Postconditions and cleanup:** Four attachments exist. Cleanup as `admin`: delete them, set the part inactive and delete it.

**Notes:** The docs say "any image format recognised by Pillow (e.g. ...)"; the list is examples.

---

### UI-Detail_View-411: A non-image file gets no thumbnail and is_image false

| Field | Value |
|---|---|
| **Summary** | Uploading a PDF file creates no thumbnail, and `is_image` is false. |
| **Requirement** | `R-Detail_View-46`. Source: [concepts-attachments.md#L42](../../requirements/docs/concepts-attachments.md#L42) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: not an image) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; local file `QA-<suffix>-datasheet.pdf`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Partial: how the flag is read is open. |
| **Review** | Draft · Open question: Q-Detail_View-52 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the PDF with *Add attachment*. | File: `QA-<suffix>-datasheet.pdf` | The file is listed (R-Detail_View-42). |
| 2 | Check the thumbnail and the `is_image` flag as in UI-Detail_View-409 step 3. | None | `is_image` is `false` (R-Detail_View-46). Open: Q-Detail_View-52 (what the UI shows instead of a thumbnail). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the attachment, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-412: A file with an image extension but corrupt data gets no thumbnail

| Field | Value |
|---|---|
| **Summary** | A text file renamed to `.png` is accepted as an attachment but gets no thumbnail, and `is_image` stays false. |
| **Requirement** | `R-Detail_View-47`. Source: [concepts-attachments.md#L43](../../requirements/docs/concepts-attachments.md#L43) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (image extension, invalid content) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; local file `QA-<suffix>-corrupt.png` containing the plain text `not an image`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Partial: how the flag is read is open. |
| **Review** | Draft · Open question: Q-Detail_View-52 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the file with *Add attachment*. | File: `QA-<suffix>-corrupt.png` | No thumbnail is generated and `is_image` remains false (R-Detail_View-47). Open: Q-Detail_View-52 (whether the upload itself is accepted or rejected, and any message). |
| 2 | Check the `is_image` flag as in UI-Detail_View-409 step 3. | None | `is_image` is `false` (R-Detail_View-47). |

**Postconditions and cleanup:** The attachment may exist. Cleanup as `admin`: delete it if listed, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-413: A link attachment never gets a thumbnail

| Field | Value |
|---|---|
| **Summary** | An external link, even one pointing at an image URL, gets no thumbnail. |
| **Requirement** | `R-Detail_View-48`. Source: [concepts-attachments.md#L44](../../requirements/docs/concepts-attachments.md#L44) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (link with an image URL) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Detail_View-52 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a link with *Add external link*. | Link: `https://example.com/QA-<suffix>.png` | The link is listed (R-Detail_View-43). |
| 2 | Look for a thumbnail of the link. | None | No thumbnail is assigned (R-Detail_View-48). Open: Q-Detail_View-52 (what the UI shows for a link row). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the link, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-414: Rename a file attachment with Edit

| Field | Value |
|---|---|
| **Summary** | A user renames an uploaded file with the *Edit* action; the file is not re-uploaded and stays available under the new name. |
| **Requirement** | `R-Detail_View-49`. Source: [concepts-attachments.md#Renaming Attachments](../../requirements/docs/concepts-attachments.md#L59) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (attachment name A to name B) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` and file `QA-<suffix>-datasheet.pdf` attached as `admin`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Partial: the Edit form fields are open. |
| **Review** | Draft · Open question: Q-Detail_View-53 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press the *Edit* action of the attachment. | Attachment: `QA-<suffix>-datasheet.pdf` | An edit form opens (R-Detail_View-49). Open: Q-Detail_View-53 (form title and field labels). |
| 2 | Change the file name and submit. | New name: `QA-<suffix>-datasheet-v2.pdf` | The attachment is listed under the new name without a new upload; the system renames the file on the server and updates the database record (R-Detail_View-49). |
| 3 | Download the renamed attachment. | None | Proposed, to confirm in Q-Detail_View-53: the file downloads with the new name and the original content. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the attachment, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-415: Rename an attachment to an empty name

| Field | Value |
|---|---|
| **Summary** | Clearing the file name in the *Edit* form is not accepted. |
| **Requirement** | `R-Detail_View-49`. Source: [concepts-attachments.md#Renaming Attachments](../../requirements/docs/concepts-attachments.md#L59) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty name), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` and file `QA-<suffix>-datasheet.pdf` attached as `admin`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Detail_View-53 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *Edit*, clear the file name and submit. | Name: empty | Proposed, to confirm in Q-Detail_View-53: the form is not accepted, a field error is shown, and the attachment keeps its name. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the attachment, set the part inactive and delete it.

**Notes:** The docs state nothing about name validation.

---

### UI-Detail_View-416: Rename an attachment to a name with special characters and Unicode

| Field | Value |
|---|---|
| **Summary** | Renaming a file to a name with spaces, Unicode and special characters. |
| **Requirement** | `R-Detail_View-49`. Source: [concepts-attachments.md#Renaming Attachments](../../requirements/docs/concepts-attachments.md#L59) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (special characters, Unicode) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` and file `QA-<suffix>-datasheet.pdf` attached as `admin`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Partial. |
| **Review** | Draft · Open question: Q-Detail_View-53 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *Edit*, enter the new name and submit. | Name: `QA-<suffix> déploy & test #1.pdf` | Not known: depends on open question Q-Detail_View-53 (allowed characters, whether the name is stored as typed or sanitised). |
| 2 | Download the attachment. | None | Not known: depends on open question Q-Detail_View-53 (the name the file is served under). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the attachment, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-417: Add attachment submitted without a file

| Field | Value |
|---|---|
| **Summary** | Submitting the *Add attachment* form with no file selected does not create an attachment. |
| **Requirement** | `R-Detail_View-43`. Source: [concepts-attachments.md#Adding Attachments](../../requirements/docs/concepts-attachments.md#L55) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: no file), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-50 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *Add attachment* and submit without selecting a file. | File: none | Proposed, to confirm in Q-Detail_View-50: the form stays open with an error on the file field, and no attachment is created. |

**Postconditions and cleanup:** No attachment. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** The docs do not name the required fields.

---

### UI-Detail_View-418: Add external link with an empty or invalid URL

| Field | Value |
|---|---|
| **Summary** | An empty link and a text that is not a URL are not accepted by the *Add external link* form. |
| **Requirement** | `R-Detail_View-43`. Source: [concepts-attachments.md#Adding Attachments](../../requirements/docs/concepts-attachments.md#L55) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid classes: empty, not a URL), Error guessing (whitespace-only) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part's *Attachments* tab, press *Add external link*. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-50 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Submit with an empty link. | Link: empty | Proposed, to confirm in Q-Detail_View-50: not accepted, with an error on the link field; no attachment is created. |
| 2 | Submit with spaces only. | Link: 3 spaces | Proposed, to confirm in Q-Detail_View-50: not accepted; no attachment is created. |
| 3 | Submit with text that is not a URL. | Link: `QA-<suffix> not a url` | Proposed, to confirm in Q-Detail_View-50: not accepted, with an error on the link field; no attachment is created. |

**Postconditions and cleanup:** No attachment. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** The docs state no URL validation or error text.

---

### UI-Detail_View-419: Cancel the Add attachment form

| Field | Value |
|---|---|
| **Summary** | Closing the *Add attachment* form with a file selected, without submitting, creates no attachment. |
| **Requirement** | `R-Detail_View-43`. Source: [concepts-attachments.md#Adding Attachments](../../requirements/docs/concepts-attachments.md#L55) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-form) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` as `admin`; local file `QA-<suffix>-datasheet.pdf`; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-50 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Press *Add attachment*, select the file, then close the form without submitting. | File: `QA-<suffix>-datasheet.pdf` | Proposed, to confirm in Q-Detail_View-50: the form closes and the table is unchanged. Open: Q-Detail_View-50 (the cancel control's label). |
| 2 | Reload the tab. | None | Proposed, to confirm in Q-Detail_View-50: no attachment is listed. |

**Postconditions and cleanup:** No attachment. Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-420: Upload the same file twice

| Field | Value |
|---|---|
| **Summary** | Uploading a file with the same name as an existing attachment of the part. |
| **Requirement** | `R-Detail_View-42`. Source: [part-views.md#Attachments](../../requirements/docs/part-views.md#L154); `R-Detail_View-43`. Source: [concepts-attachments.md#Adding Attachments](../../requirements/docs/concepts-attachments.md#L55) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate file name) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Attach` created via `POST /api/part/` and file `QA-<suffix>-datasheet.pdf` attached as `admin`; the same local file; Pre-steps: log in, open the part's *Attachments* tab. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-50 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Upload the same file again with *Add attachment*. | File: `QA-<suffix>-datasheet.pdf` | Not known: depends on open question Q-Detail_View-50 (whether a second attachment is created, the file is renamed, or the upload is rejected, and any message). |

**Postconditions and cleanup:** One or two attachments exist. Cleanup as `admin`: delete them, set the part inactive and delete it.

**Notes:** The docs state no rule for duplicate names.
