# Seed: manual functional test case

The reference format for every manual UI test case. API cases use `seed-api-test-case.md`, which shares these header fields. Agents copy the template, fill every field, and match the worked example for level of detail. A field that does not apply says `None`; it is never deleted.

---

## Template

### <ID>: <Summary>

| Field | Value |
|---|---|
| **Summary** | One sentence: what is verified, and under which condition. |
| **Requirement** | `R-<Area>-NN` from `test-cases/<Area folder>/requirements-inventory.md`, plus the source link: `[file#heading](../requirements/docs/<file>#L<line>)`. API cases: see `seed-api-test-case.md`. |
| **Area** | UI: `Part` (creation and import) · `Detail_View` (detail view tabs) · `Categories` · `ATT` (attributes) · `Unit_measure` · `REV` (revisions) · `Part_Params` (parameters) · `Part_Template` (templates and variants). API: `CRUD` · `LST` · `VAL` · `REL` · `SEC` (defined in `seed-api-test-case.md`). Each Area's folder: see Area folders below. |
| **Type** | Positive · Negative · Boundary |
| **Technique** | The test design technique(s) that produced the case, comma-separated: `Equivalence partitioning` · `Boundary value analysis` · `State transition` · `Decision table` · `Error guessing` · `Exploratory` · `Negative` · `What-if business scenario`. Add the class, boundary, transition or table column in brackets, e.g. `Boundary value analysis (max length + 1)`. |
| **Priority** | P1 core flow or data integrity · P2 important behaviour · P3 cosmetic or rare edge |
| **Tags** | One or more, comma-separated: `Smoke` (the minimum set that proves the app is usable; run first) · `Regression` (full suite) · plus optional `Cross-functional`, `Permissions`, `Settings-dependent`. Every case has `Regression`; `Smoke` is added on top. |
| **Prerequisites** | One line, semicolon-separated, always in this order: `User: <demo user and role, least-privileged that can do the action>; Settings: <setting = state, or None>; Data: <records that must exist and how they are created, names with the run suffix QA-<8 hex>, or None>; Pre-steps: <actions before step 1 that are not under test, or None>`. |
| **Automation** | Yes / No / Partial, with a reason if not Yes. |
| **Review** | Human review status. Agents write `Draft`, or `Draft · Open question: Q-<Area>-NN` (comma-separated if several) when an open question affects the case, and never change it afterwards. A case with an open question cannot be approved until the question is answered and the case updated. Only the architect sets: `Approved · <date>` (optionally followed by ` · <note on what was changed in the agent draft and why>`), `Changed · <date> · <what was changed and why>` or `Rejected · <date> · <why>`. Only Approved or Changed cases are automated. |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | One user action per step. | Exact values entered. | Observable and specific: a message, a value, a field state, a URL, a status code. Never "works correctly". If an open question leaves part of it unclear, first what the cited rule states, as fact, then the unknown: `No stock item is created for the part (R-ATT-02). Open: Q-ATT-08 (whether the part is left out of the selector or the form is rejected, and the error text).` If no rule states the outcome: `Proposed, to confirm in Q-<Area>-NN: <outcome>.` Only if nothing can be proposed: `Not known: depends on open question Q-<Area>-NN (<what is unknown>).` |

Any other cell that needs a detail an open question leaves unknown: `[open: Q-<Area>-NN, <what is unknown>]`.

**Postconditions and cleanup:** the state left behind, and how to remove the records the case created (for parts: make inactive, then delete).

**Notes:** any trap, mismatch between the docs and the app, or finding reference (`test-cases/findings.md#...`). `None` otherwise.

**Duplicate check:** written by `python tools/dedupe_cases.py --case <ID>` after the case is saved, never by hand, and only when the score is 50 or more: `<score> · <Review / Duplicate> · matches: <links to matching cases with their scores>`. No line means the case is unique (score below 50). 50-80: Review; above 80: Duplicate. Both get a verdict from the `test-case-reviewer` agent; never deleted by an agent.

**Duplicate judgement:** only on cases with a Duplicate check line (score 50 or more), written by the independent `test-case-reviewer` agent (never by the agent that wrote the case) after reading every listed match: `<Keep / Merge into <ID> / Remove / Escalate> · <one-sentence reason> · test-case-reviewer, <date>`. Older lines name `duplicate-judge`, the agent it replaced. The script never overwrites this line. The architect acts on Merge, Remove and Escalate.

---

## Worked example

### UI-Part-001: Create a part manually with the required fields

| Field | Value |
|---|---|
| **Summary** | A user with part create permission can create a part through the *Create Part* form, and is redirected to the new part's detail page. |
| **Requirement** | `R-Part-TBD` (assigned in the P03 inventory). Source: [part-create.md#Create Part Form](../requirements/docs/part-create.md#L24), [part-create.md#Part Creation](../requirements/docs/part-create.md#L13) |
| **Area** | Part |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: all required fields filled with valid values) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts, view stock); Settings: *Create Initial Stock* off (check the 1.5.6 default); Data: non-structural category `QA-<suffix> Category`, created via `POST /api/part/category/` as `admin`; Pre-steps: log in at `http://localhost/web`, open the *Parts* view. |
| **Automation** | Yes: core CRUD, part of the Phase 3 scope. |
| **Review** | Draft |

**Steps**

| # | Action | Test data | Expected result |
|---|---|---|---|
| 1 | Open the *Add Parts* dropdown above the parts table. | None | The menu shows *Create Part* and *Import from File*. |
| 2 | Select *Create Part*. | None | The *Create Part* form opens. Required fields are marked. |
| 3 | Fill in the fields. | Name: `QA-<suffix> Resistor 10k`<br>Description: `Seed test part`<br>Category: `QA-<suffix> Category` | Fields accept the values, with no validation errors shown. |
| 4 | Press *Submit*. | None | The form closes and the browser goes to the new part's detail page (`/web/part/<pk>/`). |
| 5 | Check the detail page header and details. | None | Name, description and category show the values from step 3. The part is Active. |
| 6 | Open the category `QA-<suffix> Category` from the *Parts* view. | None | The new part appears in the category's part list. |

**Postconditions and cleanup:** one new part exists in `QA-<suffix> Category`. Cleanup as `admin`: set the part inactive, delete it, then delete the category.

**Notes:** check the required fields against the `Part` schema in `requirements/openapi-parts.yaml` before writing negative cases for this form.
---

## Area folders

Each Area has a short value, used in the Area field and in every ID (`UI-ATT-001`, `R-ATT-01`, `Q-ATT-01`), and a folder under `test-cases/` with a full name. Paths in agents and docs write the folder as `test-cases/<Area folder>/`.

| Area | Folder | Covers |
|---|---|---|
| `Part` | `Part_Creation_and_Import` | Create Part form, part fields, import from file |
| `Detail_View` | `Part_Detail_View` | Detail view header and tabs |
| `Categories` | `Categories` | Category hierarchy, category part list, filters |
| `ATT` | `Attributes` | Virtual, Assembly, Component, Testable, Trackable, Purchaseable, Salable, Locked, Active |
| `Unit_measure` | `Units_of_Measure` | Part and supplier part units |
| `REV` | `Revisions` | Revisions |
| `Part_Params` | `Parameters` | Parameters and templates |
| `Part_Template` | `Templates_and_Variants` | Template parts and variants |
| `CRUD` (API) | `API_Create_Read_Update_Delete` | Create, read, update, delete on parts and categories |
| `LST` (API) | `API_Lists_and_Filters` | Lists: pagination, filters, ordering, search |
| `VAL` (API) | `API_Field_Validation` | Field validation |
| `REL` (API) | `API_Relationships` | Category, location, supplier links |
| `SEC` (API) | `API_Security_and_Permissions` | Authentication and role permissions |

A new Area gets a row here and a folder with a `requirements-inventory.md`; the tools find the folder from the inventory's rule IDs (`tools/areas.py`).

---

## Demo users

| Username | Password | Use for |
|---|---|---|
| admin | inventree | Setup, cleanup, settings changes |
| allaccess | nolimits | Full create, edit and delete |
| engineer | partsonly | Part management (default for Parts UI cases) |
| reader | readonly | View-only checks: create and edit controls hidden |
| noaccess | youshallnotpass | No permissions |
| steven | wizardstaff | Staff, some admin pages |
