# Test templates tab: Detail_View test cases

Test template management on the part *Test Templates* tab: creating, key generation, name uniqueness, flags, enabling, deleting, cascade to variants and permissions. Testable parts are created through the API as `admin`. Result-related cases use the stock item test results, which are documented in `stock/test.md` (not in `requirements/docs/`); the UI path there is marked open.

---

### UI-Detail_View-301: Open the Test Templates tab of a Testable part

| Field | Value |
|---|---|
| **Summary** | A user can open the *Test Templates* tab of a Testable part and see its test templates. |
| **Requirement** | `R-Detail_View-29`. Source: [part-views.md#Test Templates](../../requirements/docs/part-views.md#L130), [part-test.md#L15](../../requirements/docs/part-test.md#L15) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: Testable part) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-302: Add a test template with only a name

| Field | Value |
|---|---|
| **Summary** | A user can define a test template by entering only a name. |
| **Requirement** | `R-Detail_View-29`. Source: [part-views.md#Test Templates](../../requirements/docs/part-views.md#L130), [part-test.md#L15](../../requirements/docs/part-test.md#L15); `R-Detail_View-32`. Source: [part-test.md#Test Key](../../requirements/docs/part-test.md#L31) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: name only) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter the name and submit. | Name: `QA-<suffix> Voltage Check` | The form closes and the template appears in the table (R-Detail_View-29). Its key is `qa<suffix>voltagecheck`: the name in lowercase, with only alphanumeric characters (R-Detail_View-32). Open: Q-Detail_View-45 (whether other fields are required), Q-Detail_View-46 (where the key is shown). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 53 · Review · matches: [UI-Detail_View-304](test-templates-tab.md) (53), [UI-Detail_View-306](test-templates-tab.md) (53), [UI-Detail_View-305](test-templates-tab.md) (51), [UI-Detail_View-307](test-templates-tab.md) (50)

**Duplicate judgement:** Keep · Different requirement clause from every match: this is the R-Detail_View-29 name-only creation smoke case (name with a hyphen and run suffix), while 304 to 307 assert the specific R-Detail_View-33 key mappings · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-303: Add a test template with every field set

| Field | Value |
|---|---|
| **Summary** | All template fields (description, Required, Requires Value, Requires Attachment, Enabled) are saved as entered. |
| **Requirement** | `R-Detail_View-34`. Source: [part-test.md#Test Description](../../requirements/docs/part-test.md#L48); `R-Detail_View-35`. Source: [part-test.md#Required](../../requirements/docs/part-test.md#L52); `R-Detail_View-36`. Source: [part-test.md#Requires Value](../../requirements/docs/part-test.md#L56); `R-Detail_View-37`. Source: [part-test.md#Requires Attachment](../../requirements/docs/part-test.md#L60); `R-Detail_View-38`. Source: [part-test.md#Enabled](../../requirements/docs/part-test.md#L64) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: all fields set) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-47 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Fill in all fields and submit. | Name: `QA-<suffix> Full Test`<br>Description: `Checks the supply voltage`<br>Required: on<br>Requires Value: on<br>Requires Attachment: on<br>Enabled: on | The template is created. Open: Q-Detail_View-45 (field labels and defaults). |
| 4 | Open the template for editing. | None | The form shows description `Checks the supply voltage` and the Required, Requires Value, Requires Attachment and Enabled flags as set (R-Detail_View-34 to R-Detail_View-38). Open: Q-Detail_View-45 (edit control label), Q-Detail_View-47 (where the flags show in the table). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-304: Test key generated from a name with a space

| Field | Value |
|---|---|
| **Summary** | A test template named `Firmware Version` is saved and its generated key is `firmwareversion`. |
| **Requirement** | `R-Detail_View-32`. Source: [part-test.md#Test Key](../../requirements/docs/part-test.md#L31); `R-Detail_View-33`. Source: [part-test.md#Examples](../../requirements/docs/part-test.md#L41-L44) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (key generation example from the docs) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter the name and submit. | Name: `Firmware Version` | The template is created and listed (R-Detail_View-29). Its test key is `firmwareversion` (R-Detail_View-33). Open: Q-Detail_View-46 (where the key is shown in the UI). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 81 · Review · matches: [UI-Detail_View-306](test-templates-tab.md) (81, test data differs), [UI-Detail_View-305](test-templates-tab.md) (76), [UI-Detail_View-307](test-templates-tab.md) (74), [UI-Detail_View-302](test-templates-tab.md) (53)

**Duplicate judgement:** Keep · Baseline R-Detail_View-33 example (inner space and capitals only, no trimming) with a different expected key from each match: 305 adds leading/trailing and repeated spaces, 306 digits, 307 a leading digit, 302 asserts no specific key · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-305: Test key generated from a name with extra spaces and capitals

| Field | Value |
|---|---|
| **Summary** | A test template named ` My NEW T E sT ` is saved and its generated key is `mynewtest`. |
| **Requirement** | `R-Detail_View-32`. Source: [part-test.md#Test Key](../../requirements/docs/part-test.md#L31); `R-Detail_View-33`. Source: [part-test.md#Examples](../../requirements/docs/part-test.md#L41-L44) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (key generation example from the docs) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter the name and submit. | Name: ` My NEW T E sT ` | The template is created and listed (R-Detail_View-29). Its test key is `mynewtest` (R-Detail_View-33). Open: Q-Detail_View-46 (where the key is shown in the UI). Spaces are removed and capitals lowercased (R-Detail_View-33). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 76 · Review · matches: [UI-Detail_View-304](test-templates-tab.md) (76), [UI-Detail_View-306](test-templates-tab.md) (76), [UI-Detail_View-307](test-templates-tab.md) (71), [UI-Detail_View-302](test-templates-tab.md) (51)

**Duplicate judgement:** Keep · Only case for the trimming class (leading, trailing and repeated inner spaces, mixed case) of R-Detail_View-33, with its own expected key `mynewtest` · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-306: Test key generated from a name with digits

| Field | Value |
|---|---|
| **Summary** | A test template named `Test 123` is saved and its generated key is `test123`. |
| **Requirement** | `R-Detail_View-32`. Source: [part-test.md#Test Key](../../requirements/docs/part-test.md#L31); `R-Detail_View-33`. Source: [part-test.md#Examples](../../requirements/docs/part-test.md#L41-L44) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (key generation example from the docs) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter the name and submit. | Name: `Test 123` | The template is created and listed (R-Detail_View-29). Its test key is `test123` (R-Detail_View-33). Open: Q-Detail_View-46 (where the key is shown in the UI). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 81 · Review · matches: [UI-Detail_View-304](test-templates-tab.md) (81, test data differs), [UI-Detail_View-305](test-templates-tab.md) (76), [UI-Detail_View-307](test-templates-tab.md) (76), [UI-Detail_View-302](test-templates-tab.md) (53)

**Duplicate judgement:** Keep · Only case where digits are kept inside the key (`test123`), a different R-Detail_View-33 class from the letters-only (304, 305) and leading-digit (307) examples · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-307: Test key generated from a name starting with a digit

| Field | Value |
|---|---|
| **Summary** | A test template named `100 Percent Test` is saved and its generated key is `_100percenttest`. |
| **Requirement** | `R-Detail_View-32`. Source: [part-test.md#Test Key](../../requirements/docs/part-test.md#L31); `R-Detail_View-33`. Source: [part-test.md#Examples](../../requirements/docs/part-test.md#L41-L44) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (key generation example from the docs) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter the name and submit. | Name: `100 Percent Test` | The template is created and listed (R-Detail_View-29). Its test key is `_100percenttest` (R-Detail_View-33). Open: Q-Detail_View-46 (where the key is shown in the UI). Open: Q-Detail_View-46 (the key has a leading underscore, which contradicts 'only lowercase alphanumeric'; index doc issue 3). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 76 · Review · matches: [UI-Detail_View-306](test-templates-tab.md) (76), [UI-Detail_View-304](test-templates-tab.md) (74), [UI-Detail_View-305](test-templates-tab.md) (71), [UI-Detail_View-302](test-templates-tab.md) (50)

**Duplicate judgement:** Keep · Only case for a name starting with a digit, where the expected key gets a leading underscore (`_100percenttest`, index doc issue 3); no match covers that clause · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-308: Test key is regenerated when the template is renamed

| Field | Value |
|---|---|
| **Summary** | When a template is saved with a new name, its key is generated again from the new name. |
| **Requirement** | `R-Detail_View-32`. Source: [part-test.md#Test Key](../../requirements/docs/part-test.md#L31) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (name changed, template saved again) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `Firmware Version` created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46, Q-Detail_View-48 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Edit the template and change its name. | New name: `Hardware Revision` | The template is saved under the new name. Open: Q-Detail_View-45 (edit control label). |
| 3 | Check the template's key. | None | The key is `hardwarerevision`, generated again when the template is saved (R-Detail_View-32). Open: Q-Detail_View-46 (where the key is shown in the UI). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-309: Test key from a name with special characters and Unicode

| Field | Value |
|---|---|
| **Summary** | A name with symbols and non-ASCII characters is handled and any key contains only lowercase alphanumeric characters. |
| **Requirement** | `R-Detail_View-32`. Source: [part-test.md#Test Key](../../requirements/docs/part-test.md#L31) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Error guessing (special characters, Unicode) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter the name and submit. | Name: `QA-<suffix> Voltage @ 5V (±5%) Ünit` | The key contains only lowercase alphanumeric characters (R-Detail_View-32). Proposed, to confirm in Q-Detail_View-46: the name is accepted, and the spaces, symbols and brackets are left out of the key. Open: Q-Detail_View-46 (where the key is shown, and whether `Ü` counts as alphanumeric). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-310: Duplicate test name on the same part is rejected

| Field | Value |
|---|---|
| **Summary** | A second template with the same name on the same part is not created. |
| **Requirement** | `R-Detail_View-31`. Source: [part-test.md#Test Name](../../requirements/docs/part-test.md#L27) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate), Equivalence partitioning (invalid class: name already used on the part) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Voltage Check` created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter the same name and submit. | Name: `QA-<suffix> Voltage Check` | The template is not created; the table still lists one template with that name (R-Detail_View-31). Open: Q-Detail_View-46 (error text and where it is shown). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 63 · Review · matches: [UI-Detail_View-311](test-templates-tab.md) (63), [UI-Detail_View-340](test-templates-tab.md) (61), [UI-Detail_View-313](test-templates-tab.md) (56), [UI-Detail_View-314](test-templates-tab.md) (51)

**Duplicate judgement:** Keep · Exact same name on the same part; 311 uses a different spelling with the same key, 340 starts with no template (double submit), 313 is the cross-variant clause and 314 the empty-name class · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-311: Test name differing only in case and spaces is rejected

| Field | Value |
|---|---|
| **Summary** | A name that gives the same key as an existing template on the part is not accepted as a separate template. |
| **Requirement** | `R-Detail_View-31`. Source: [part-test.md#Test Name](../../requirements/docs/part-test.md#L27); `R-Detail_View-32`. Source: [part-test.md#Test Key](../../requirements/docs/part-test.md#L31) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (same key, different spelling) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Voltage Check` created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter the name and submit. | Name: ` qa-<suffix>  voltage check ` | Proposed, to confirm in Q-Detail_View-46: the template is not created, because its key equals the existing key (R-Detail_View-32). Open: Q-Detail_View-46 (whether uniqueness compares names or keys; error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 63 · Review · matches: [UI-Detail_View-310](test-templates-tab.md) (63), [UI-Detail_View-314](test-templates-tab.md) (61), [UI-Detail_View-315](test-templates-tab.md) (55), [UI-Detail_View-340](test-templates-tab.md) (51)

**Duplicate judgement:** Keep · Different invalid class from every match: a different name that gives the same key (case and spacing), versus the exact same name (310), empty (314), whitespace-only (315) and double submit (340) · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-312: Same test name on an unrelated part is accepted

| Field | Value |
|---|---|
| **Summary** | The same test name can be used on a different part that is not a variant of the first. |
| **Requirement** | `R-Detail_View-31`. Source: [part-test.md#Test Name](../../requirements/docs/part-test.md#L27) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: name unique within its own part) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and a second unrelated Testable part `QA-<suffix> Testable B`; template `QA-<suffix> Voltage Check` on the first part; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open part `QA-<suffix> Testable B` and its *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter the same name and submit. | Name: `QA-<suffix> Voltage Check` | The template is created; the name is unique for this part (R-Detail_View-31). Open: Q-Detail_View-46 (confirmation that uniqueness is per part). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the second part too.

**Notes:** None.

---

### UI-Detail_View-313: Variant reuses a test name defined on its template part

| Field | Value |
|---|---|
| **Summary** | A variant defines a template with a name already defined on its template part. |
| **Requirement** | `R-Detail_View-31`. Source: [part-test.md#Test Name](../../requirements/docs/part-test.md#L27); `R-Part_Template-08`. Source: [part-test.md#L19](../../requirements/docs/part-test.md#L19) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: name used across a set of variants) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and variant `QA-<suffix> Variant` of the part (the part is a template); template `QA-<suffix> Voltage Check` on the template part; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46, Q-Detail_View-49 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the variant's *Test Templates* tab. | None | The tab lists the template inherited from the template part (R-Part_Template-08). Open: Q-Detail_View-49 (how inherited templates are marked). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter the same name and submit. | Name: `QA-<suffix> Voltage Check` | Proposed, to confirm in Q-Detail_View-46: the template is rejected with an error, and the variant's tab still lists only the inherited `QA-<suffix> Voltage Check`. A test name must be unique "for a part (or across a set of variants)" (R-Detail_View-31), but the scope is ambiguous (doc issue 4). Open: Q-Detail_View-46 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the variant first.

**Notes:** None.

**Duplicate check:** 56 · Review · matches: [UI-Detail_View-310](test-templates-tab.md) (56)

**Duplicate judgement:** Keep · Different starting state and clause from 310: the name is defined on the template part and reused on its variant (the "across a set of part variants" clause of R-Detail_View-31), not on the same part · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-314: Empty test name is rejected

| Field | Value |
|---|---|
| **Summary** | A template cannot be saved with an empty name. |
| **Requirement** | `R-Detail_View-31`. Source: [part-test.md#Test Name](../../requirements/docs/part-test.md#L27); `R-Detail_View-32`. Source: [part-test.md#Test Key](../../requirements/docs/part-test.md#L31) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Leave the name empty and submit. | Name: empty | Proposed, to confirm in Q-Detail_View-46: the form stays open and no template is created. Open: Q-Detail_View-46 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 61 · Review · matches: [UI-Detail_View-311](test-templates-tab.md) (61), [UI-Detail_View-315](test-templates-tab.md) (54), [UI-Detail_View-310](test-templates-tab.md) (51)

**Duplicate judgement:** Keep · Empty-name invalid class, different from the same-key (311), whitespace-only (315) and exact-duplicate (310) classes · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-315: Whitespace-only test name is rejected

| Field | Value |
|---|---|
| **Summary** | A template whose name is only spaces is not created. |
| **Requirement** | `R-Detail_View-32`. Source: [part-test.md#Test Key](../../requirements/docs/part-test.md#L31) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (whitespace-only) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter spaces as the name and submit. | Name: 5 space characters | Proposed, to confirm in Q-Detail_View-46: no template is created (a key made from spaces would be empty, R-Detail_View-32). Open: Q-Detail_View-46 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 55 · Review · matches: [UI-Detail_View-311](test-templates-tab.md) (55), [UI-Detail_View-314](test-templates-tab.md) (54)

**Duplicate judgement:** Keep · Whitespace-only class (non-empty input whose key would be empty) differs from the empty class (314) and the same-key class (311) · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-316: Test name length boundary

| Field | Value |
|---|---|
| **Summary** | A test name just below, at and just above the maximum length is handled. |
| **Requirement** | `R-Detail_View-31`. Source: [part-test.md#Test Name](../../requirements/docs/part-test.md#L27) |
| **Area** | Detail_View |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (max - 1, max, max + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Submit a name of maximum length minus 1. | Name: [open: Q-Detail_View-46, max length - 1] characters | Not known: depends on open question Q-Detail_View-46 (maximum length). Proposed: the template is created. |
| 4 | Submit a name of maximum length. | Name: [open: Q-Detail_View-46, max length] characters | Not known: depends on open question Q-Detail_View-46 (maximum length). Proposed: the template is created. |
| 5 | Submit a name of maximum length plus 1. | Name: [open: Q-Detail_View-46, max length + 1] characters | Not known: depends on open question Q-Detail_View-46 (maximum length, error text). Proposed: the template is not created. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete every template created.

**Notes:** None.

---

### UI-Detail_View-317: Test description is saved

| Field | Value |
|---|---|
| **Summary** | The description entered for a template is stored; it is information only and not used by the testing framework. |
| **Requirement** | `R-Detail_View-34`. Source: [part-test.md#Test Description](../../requirements/docs/part-test.md#L48) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: description entered) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter name and description, then submit. | Name: `QA-<suffix> Desc Test`<br>Description: `Information only` | The template is created. Open: Q-Detail_View-45 (whether the description is a table column). |
| 4 | Open the template for editing. | None | The description `Information only` is stored. The description is not used by the InvenTree testing framework (R-Detail_View-34), so it does not change test behaviour. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-318: Required flag is saved on a template

| Field | Value |
|---|---|
| **Summary** | A template saved with *Required* on keeps the flag, marking the test as crucial for acceptance of a stock item. |
| **Requirement** | `R-Detail_View-35`. Source: [part-test.md#Required](../../requirements/docs/part-test.md#L52) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (flag on) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-47 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Set Required on and submit. | Name: `QA-<suffix> Required Test`<br>Required: on | The template is created. Open: Q-Detail_View-45 (flag label). |
| 4 | Check the template's Required state. | None | The flag is on: the test is crucial for the acceptance of a stock item (R-Detail_View-35). Open: Q-Detail_View-47 (where it is shown and what it changes for a stock item). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-319: Test result without a value is rejected when Requires Value is on

| Field | Value |
|---|---|
| **Summary** | A result recorded against a template with *Requires Value* must set the value, so a result without one is not saved. |
| **Requirement** | `R-Detail_View-36`. Source: [part-test.md#Requires Value](../../requirements/docs/part-test.md#L56) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Requires Value on, value empty) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Value Test` with Requires Value on, and a stock item of the part, created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-47 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the stock item's test results and add a result for `QA-<suffix> Value Test` without a value. | Value: empty | The result is not saved without a value (R-Detail_View-36). Open: Q-Detail_View-47 (UI path on the stock page, error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the stock item first.

**Notes:** None.

---

### UI-Detail_View-320: Test result with a value is accepted when Requires Value is on

| Field | Value |
|---|---|
| **Summary** | A result with the value set is saved against a *Requires Value* template. |
| **Requirement** | `R-Detail_View-36`. Source: [part-test.md#Requires Value](../../requirements/docs/part-test.md#L56) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Requires Value on, value set) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Value Test` with Requires Value on, and a stock item of the part, created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-47 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a result for `QA-<suffix> Value Test` with a value. | Value: `5.0` | The result is saved (R-Detail_View-36). Open: Q-Detail_View-47 (UI path on the stock page). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the stock item first.

**Notes:** None.

---

### UI-Detail_View-321: Test result without a file is rejected when Requires Attachment is on

| Field | Value |
|---|---|
| **Summary** | A result against a *Requires Attachment* template must include an uploaded file, so a result without one is not saved. |
| **Requirement** | `R-Detail_View-37`. Source: [part-test.md#Requires Attachment](../../requirements/docs/part-test.md#L60) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Requires Attachment on, no file) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Attach Test` with Requires Attachment on, a stock item of the part, and a small file `qa-result.txt`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-47 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a result for `QA-<suffix> Attach Test` without a file. | Attachment: none | The result is not saved without a file (R-Detail_View-37). Open: Q-Detail_View-47 (UI path on the stock page, error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the stock item first.

**Notes:** None.

---

### UI-Detail_View-322: Test result with a file is accepted when Requires Attachment is on

| Field | Value |
|---|---|
| **Summary** | A result with an uploaded file is saved against a *Requires Attachment* template. |
| **Requirement** | `R-Detail_View-37`. Source: [part-test.md#Requires Attachment](../../requirements/docs/part-test.md#L60) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Decision table (Requires Attachment on, file uploaded) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Attach Test` with Requires Attachment on, a stock item of the part, and a small file `qa-result.txt`; Pre-steps: log in, open the part detail page. |
| **Automation** | Partial: file upload needs a fixture. |
| **Review** | Draft · Open question: Q-Detail_View-47 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Add a result for `QA-<suffix> Attach Test` and upload the file. | Attachment: `qa-result.txt` | The result is saved with the file (R-Detail_View-37). Open: Q-Detail_View-47 (UI path on the stock page). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the stock item first.

**Notes:** None.

---

### UI-Detail_View-323: Disable a test template while keeping it

| Field | Value |
|---|---|
| **Summary** | Setting *Enabled* off keeps the template in the table. |
| **Requirement** | `R-Detail_View-38`. Source: [part-test.md#Enabled](../../requirements/docs/part-test.md#L64) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (enabled to disabled) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and enabled template `QA-<suffix> Disable Test` created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-47, Q-Detail_View-48 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Edit the template and set Enabled off, then submit. | Enabled: off | The template is saved and stays listed; it is retained (R-Detail_View-38). Open: Q-Detail_View-47 (how a disabled test is shown), Q-Detail_View-45 (edit control label). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 63 · Review · matches: [UI-Detail_View-324](test-templates-tab.md) (63)

**Duplicate judgement:** Keep · Different transition and starting state from 324: enabled to disabled here, disabled to enabled there · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-324: Re-enable a disabled test template

| Field | Value |
|---|---|
| **Summary** | A disabled template can be enabled again. |
| **Requirement** | `R-Detail_View-38`. Source: [part-test.md#Enabled](../../requirements/docs/part-test.md#L64) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (disabled to enabled) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and disabled template `QA-<suffix> Disable Test` created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-47, Q-Detail_View-48 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Edit the template and set Enabled on, then submit. | Enabled: on | Proposed, to confirm in Q-Detail_View-48: the template is saved as enabled again. Open: Q-Detail_View-47 (how an enabled test is shown). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 63 · Review · matches: [UI-Detail_View-323](test-templates-tab.md) (63)

**Duplicate judgement:** Keep · Different transition and starting state from 323: disabled to enabled here, enabled to disabled there · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-325: Delete a test template that has no results

| Field | Value |
|---|---|
| **Summary** | A template with no results is removed from the table. |
| **Requirement** | `R-Detail_View-39`. Source: [part-test.md#Enabled](../../requirements/docs/part-test.md#L64) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: no results) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Delete Test` created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-48 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Delete the template. | None | After confirming, the template is no longer listed (R-Detail_View-39). Open: Q-Detail_View-48 (confirmation dialog text), Q-Detail_View-45 (delete control label). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-326: Deleting a test template deletes its test results

| Field | Value |
|---|---|
| **Summary** | Deleting a template also deletes the test results recorded against it. |
| **Requirement** | `R-Detail_View-39`. Source: [part-test.md#Enabled](../../requirements/docs/part-test.md#L64) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (template with results to deleted) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Delete Test`, a stock item of the part and one result for the template, created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-47, Q-Detail_View-48 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the stock item's test results. | None | One result for `QA-<suffix> Delete Test` is listed. Open: Q-Detail_View-47 (UI path on the stock page). |
| 2 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 3 | Delete the template and confirm. | None | The template is removed (R-Detail_View-39). Open: Q-Detail_View-48 (confirmation text). |
| 4 | Open the stock item's test results again. | None | The result for the deleted template is gone (R-Detail_View-39). Open: Q-Detail_View-47 (UI path on the stock page). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the stock item first.

**Notes:** None.

---

### UI-Detail_View-327: Cancel deleting a test template

| Field | Value |
|---|---|
| **Summary** | Cancelling the delete leaves the template unchanged. |
| **Requirement** | `R-Detail_View-39`. Source: [part-test.md#Enabled](../../requirements/docs/part-test.md#L64) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-action) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Delete Test` created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-48 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start deleting the template, then cancel. | None | The template stays listed. Proposed, to confirm in Q-Detail_View-48: deleting asks for confirmation, so it can be cancelled. Open: Q-Detail_View-48 (cancel control label). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-328: Cancel adding a test template

| Field | Value |
|---|---|
| **Summary** | Closing the add form without submitting creates no template. |
| **Requirement** | `R-Detail_View-29`. Source: [part-views.md#Test Templates](../../requirements/docs/part-views.md#L130), [part-test.md#L15](../../requirements/docs/part-test.md#L15) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (cancel mid-form) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter a name, then cancel the form. | Name: `QA-<suffix> Cancelled` | The form closes and no template named `QA-<suffix> Cancelled` is listed. Proposed, to confirm in Q-Detail_View-45: cancelling discards the entry. Open: Q-Detail_View-45 (cancel control label). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-329: Rename a test template after results exist

| Field | Value |
|---|---|
| **Summary** | A template that already has a result is renamed; the result stays linked to it. |
| **Requirement** | `R-Detail_View-32`. Source: [part-test.md#Test Key](../../requirements/docs/part-test.md#L31) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | What-if business scenario (template renamed after results exist) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Rename Test`, a stock item of the part and one result for it, created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-46, Q-Detail_View-48 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Edit the template and rename it. | New name: `QA-<suffix> Renamed Test` | The key is generated again from the new name when the template is saved (R-Detail_View-32). |
| 3 | Open the stock item's test results. | None | The key is used to match test results to the template (R-Detail_View-32). Not known: depends on open question Q-Detail_View-48 (whether the result stays linked after the key changes). Proposed, to confirm in Q-Detail_View-48: the result stays linked. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the stock item first.

**Notes:** None.

---

### UI-Detail_View-330: Test templates cascade from a master part to its variant

| Field | Value |
|---|---|
| **Summary** | A test template defined on the master part is assigned to its variants. |
| **Requirement** | `R-Part_Template-08`. Source: [part-test.md#L19](../../requirements/docs/part-test.md#L19) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: variant of a master part) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and variant `QA-<suffix> Variant` of the part (the part is a template), created as `admin`; template `QA-<suffix> Master Test` on the master part; Pre-steps: log in, open the variant's detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-49 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the variant's *Test Templates* tab. | None | The template `QA-<suffix> Master Test` is listed for the variant (R-Part_Template-08). Open: Q-Detail_View-49 (how it is marked as inherited). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the variant first.

**Notes:** None.

**Duplicate check:** 51 · Review · matches: [UI-Detail_View-331](test-templates-tab.md) (51)

**Duplicate judgement:** Escalate · The prerequisites do not say whether the master's template exists before the variant is created; if it does, the starting state differs from 331 (Keep), if it is created after the variant, the case repeats 331 · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-331: Template added to the master after a variant exists reaches the variant

| Field | Value |
|---|---|
| **Summary** | A test template added to the master part later also appears on an existing variant. |
| **Requirement** | `R-Part_Template-08`. Source: [part-test.md#L19](../../requirements/docs/part-test.md#L19) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | What-if business scenario (template added after variants exist) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and variant `QA-<suffix> Variant` of the part (the part is a template), created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-49 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the master part's *Test Templates* tab and add a template. | Name: `QA-<suffix> Late Test` | The template is created on the master. Open: Q-Detail_View-45 (add control label). |
| 2 | Open the variant's *Test Templates* tab. | None | The template `QA-<suffix> Late Test` is listed for the variant (R-Part_Template-08). Open: Q-Detail_View-49 (inherited marker). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the variant first.

**Notes:** None.

**Duplicate check:** 51 · Review · matches: [UI-Detail_View-330](test-templates-tab.md) (51)

**Duplicate judgement:** Keep · Explicit starting state of a variant that exists before the template is added to the master (added through the UI); 330 does not fix that order, see its Escalate verdict · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-332: Variant's own test template does not appear on the master

| Field | Value |
|---|---|
| **Summary** | A template defined on the variant is not shown on the master part. |
| **Requirement** | `R-Part_Template-08`. Source: [part-test.md#L19](../../requirements/docs/part-test.md#L19) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (cascade is master to variant only) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and variant `QA-<suffix> Variant` of the part (the part is a template), created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-49 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the variant's *Test Templates* tab and add a template. | Name: `QA-<suffix> Variant Test` | Open: Q-Detail_View-49 (whether a variant can add its own template). |
| 2 | Open the master part's *Test Templates* tab. | None | Proposed, to confirm in Q-Detail_View-49: `QA-<suffix> Variant Test` is not listed, because templates cascade down from the master (R-Part_Template-08). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the variant first.

**Notes:** None.

---

### UI-Detail_View-333: Stock item of a variant has the master's test templates

| Field | Value |
|---|---|
| **Summary** | Stock items of a variant part have the same test templates as the master. |
| **Requirement** | `R-Part_Template-08`. Source: [part-test.md#L19](../../requirements/docs/part-test.md#L19) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Exploratory (flow across part and stock pages) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and variant `QA-<suffix> Variant` of the part (the part is a template), created as `admin`; template `QA-<suffix> Master Test` on the master part; a stock item of the variant; Pre-steps: log in. |
| **Automation** | Partial: stock page path unknown. |
| **Review** | Draft · Open question: Q-Detail_View-49 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the variant's stock item and its test results. | None | The stock item has the template `QA-<suffix> Master Test` associated with it (R-Part_Template-08). Open: Q-Detail_View-49 (UI path on the stock page, not in `requirements/docs/`). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it. Delete the stock item and the variant first.

**Notes:** None.

---

### UI-Detail_View-334: Test Templates tab for a part that is not Testable

| Field | Value |
|---|---|
| **Summary** | The tab is checked on a part with Testable off. |
| **Requirement** | `R-Detail_View-29`. Source: [part-views.md#Test Templates](../../requirements/docs/part-views.md#L130), [part-test.md#L15](../../requirements/docs/part-test.md#L15) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Decision table (Testable off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Plain` with testable = false created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Look at the tabs on the part detail page. | None | Proposed, to confirm in Q-Detail_View-45: no *Test Templates* tab is shown, because tests are defined for a Testable part (R-Detail_View-29). Open: Q-Detail_View-45 (the docs do not say the tab is hidden). |

**Postconditions and cleanup:** Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-335: Test Templates tab appears when Testable is switched on

| Field | Value |
|---|---|
| **Summary** | After Testable is set on a part, the tab becomes available. |
| **Requirement** | `R-Detail_View-29`. Source: [part-views.md#Test Templates](../../requirements/docs/part-views.md#L130), [part-test.md#L15](../../requirements/docs/part-test.md#L15) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | State transition (Testable off to on) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Plain` with testable = false created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-23 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Edit the part and set Testable on. | Testable: on | The part is saved. Open: Q-Detail_View-23 (edit form control label). |
| 2 | Look at the tabs on the part detail page. | None | Proposed, to confirm in Q-Detail_View-45: the *Test Templates* tab is shown, because the part is now Testable (R-Detail_View-29). Open: Q-Detail_View-23 (whether a reload is needed). |

**Postconditions and cleanup:** Cleanup as `admin`: set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-336: Existing templates when Testable is switched off and on

| Field | Value |
|---|---|
| **Summary** | A part with templates is made not Testable and Testable again; the templates are not lost. |
| **Requirement** | `R-Detail_View-29`. Source: [part-views.md#Test Templates](../../requirements/docs/part-views.md#L130), [part-test.md#L15](../../requirements/docs/part-test.md#L15) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | What-if business scenario (Testable switched off after templates exist) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Kept Test` created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-48 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Edit the part and set Testable off. | Testable: off | The part is saved. |
| 2 | Edit the part and set Testable on again, then open the *Test Templates* tab. | Testable: on | Not known: depends on open question Q-Detail_View-48 (whether the templates are kept). Proposed, to confirm in Q-Detail_View-48: `QA-<suffix> Kept Test` is still listed. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-337: Add, edit and delete controls are hidden from a view-only user

| Field | Value |
|---|---|
| **Summary** | `reader` cannot add, edit or delete test templates. |
| **Requirement** | `R-Detail_View-29`. Source: [part-views.md#Test Templates](../../requirements/docs/part-views.md#L130), [part-test.md#L15](../../requirements/docs/part-test.md#L15) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (blocked role) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Read Test` created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | Proposed, to confirm in Q-Detail_View-45: the tab opens for `reader`. Open: Q-Detail_View-45 (whether the tab is visible to `reader`). |
| 2 | Look for controls to add, edit and delete a template. | None | Proposed, to confirm in Q-Detail_View-45: no add, edit or delete control is available to `reader`. |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-338: A view-only user can see the test templates

| Field | Value |
|---|---|
| **Summary** | `reader` sees the table with the existing templates. |
| **Requirement** | `R-Detail_View-29`. Source: [part-views.md#Test Templates](../../requirements/docs/part-views.md#L130), [part-test.md#L15](../../requirements/docs/part-test.md#L15) |
| **Area** | Detail_View |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: view role) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Read Test` created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | Proposed, to confirm in Q-Detail_View-45: the table lists `QA-<suffix> Read Test`, because `reader` can view the tab (R-Detail_View-29). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-339: A user without permissions cannot see test templates

| Field | Value |
|---|---|
| **Summary** | `noaccess` opening the part page by URL gets no part data. |
| **Requirement** | `R-Detail_View-29`. Source: [part-views.md#Test Templates](../../requirements/docs/part-views.md#L130), [part-test.md#L15](../../requirements/docs/part-test.md#L15) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Negative (blocked role) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess` (no permissions); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Yes. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-19 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the part detail page by its URL. | None | Proposed, to confirm in Q-Detail_View-45: no test templates are shown. Open: Q-Detail_View-19 (message text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

---

### UI-Detail_View-340: Double submit of the add form creates one template

| Field | Value |
|---|---|
| **Summary** | Pressing the submit button twice quickly creates a single template. |
| **Requirement** | `R-Detail_View-31`. Source: [part-test.md#Test Name](../../requirements/docs/part-test.md#L27) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (double submit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Partial: timing. |
| **Review** | Draft · Open question: Q-Detail_View-45 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | Start adding a test template [open: Q-Detail_View-45, add control label]. | None | A form to define a test template opens. Open: Q-Detail_View-45 (form title, field labels, which fields are required). |
| 3 | Enter a name and double-click the submit button. | Name: `QA-<suffix> Double` | Exactly one template `QA-<suffix> Double` is listed, because a name must be unique for a part (R-Detail_View-31). Open: Q-Detail_View-45 (whether the second submit shows an error). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** None.

**Duplicate check:** 61 · Review · matches: [UI-Detail_View-310](test-templates-tab.md) (61), [UI-Detail_View-311](test-templates-tab.md) (51)

**Duplicate judgement:** Keep · Different starting state and technique from 310 and 311: no template exists and one name is submitted twice quickly (double submit), instead of a second submission against an existing template · test-case-reviewer, 2026-10-15

---

### UI-Detail_View-341: Edit a template another user has deleted

| Field | Value |
|---|---|
| **Summary** | A page left open still shows a template that `admin` has deleted; saving an edit is handled. |
| **Requirement** | `R-Detail_View-29`. Source: [part-views.md#Test Templates](../../requirements/docs/part-views.md#L130), [part-test.md#L15](../../requirements/docs/part-test.md#L15) |
| **Area** | Detail_View |
| **Type** | Negative |
| **Technique** | Error guessing (stale page after another user's change) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: Testable part `QA-<suffix> Testable` (testable = true) created via `POST /api/part/` as `admin` and template `QA-<suffix> Stale Test` created as `admin`; Pre-steps: log in, open the part detail page. |
| **Automation** | Partial: needs two sessions. |
| **Review** | Draft · Open question: Q-Detail_View-45, Q-Detail_View-48 |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Test Templates* tab. | None | The tab opens and lists the part's test templates (R-Detail_View-29). Open: Q-Detail_View-45 (tab and column labels, empty-state text). |
| 2 | As `admin` in another session, delete the template. | None | The template is deleted. |
| 3 | In the first session, edit the template and save. | Name: `QA-<suffix> Stale Renamed` | Proposed, to confirm in Q-Detail_View-48: the save fails with an error and no template with the new name exists. No rule covers editing a template that no longer exists. Open: Q-Detail_View-48 (error text). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the template if it exists, set the part inactive and delete it.

**Notes:** error-guessing case; no rule states the outcome, so it is Proposed under Q-Detail_View-48.

---
