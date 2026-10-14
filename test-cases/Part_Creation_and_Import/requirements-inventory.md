# Requirements inventory: Part (creation and import)

Rules stated in `requirements/docs/` (InvenTree 1.5.6). Built by P03 on 2026-10-10; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare. Risk values are the agent's proposal.

## Create Part form

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part-01 | New parts can be created manually via the web interface. | [part-create.md#L15](../../requirements/docs/part-create.md#L15) | H | |
| R-Part-02 | Create and import options are in the *Add Parts* dropdown above the parts table in the *Parts* view. | [part-create.md#L17](../../requirements/docs/part-create.md#L17) | M | |
| R-Part-03 | A user without "create" permission for the *Part* permission group does not see the *Add Parts* menu. | [part-create.md#L21-22](../../requirements/docs/part-create.md#L21-L22) | H | |
| R-Part-04 | Selecting *Create Part* opens the part creation form. | [part-create.md#L26](../../requirements/docs/part-create.md#L26) | M | |
| R-Part-05 | The form cannot be submitted while it shows form errors; the errors must be fixed first. | [part-create.md#L31](../../requirements/docs/part-create.md#L31) | H | Which fields are required is not stated. |
| R-Part-06 | After a successful submit, the browser is redirected to the new part's detail page. | [part-create.md#L33](../../requirements/docs/part-create.md#L33) | H | |
| R-Part-07 | If the *Create Initial Stock* setting is enabled, the form has an extra section for creating initial stock. | [part-create.md#L37](../../requirements/docs/part-create.md#L37) | M | Setting key and default not stated. |
| R-Part-08 | Checking the *Create Initial Stock* input allows an initial quantity of stock to be created for the new part. | [part-create.md#L43](../../requirements/docs/part-create.md#L43) | M | |
| R-Part-09 | If the part is marked *Purchaseable*, the form offers options to add manufacturer and/or supplier information. | [part-create.md#L47](../../requirements/docs/part-create.md#L47) | M | In 1.5.6 (MCP run 2026-10-11): a *Supplier Information* section (Supplier, SKU, Manufacturer, MPN), shown while *Purchaseable* is checked. *Purchaseable* is checked by default (`PART_PURCHASEABLE`); the section also needs `PART_CREATE_SUPPLIER` on. Index doc issue 14. |
| R-Part-10 | If *Add Supplier Data* is checked, supplier part and manufacturer part information can be added to the new part. | [part-create.md#L51](../../requirements/docs/part-create.md#L51) | M | **Outdated for 1.5.6:** there is no *Add Supplier Data* option; the data is entered in the *Supplier Information* section (see R-Part-09). Index doc issue 14. |
| R-Part-11 | Parts can also be created via the REST API, the Python library and the database admin interface. | [part-create.md#L92-96](../../requirements/docs/part-create.md#L92-L96) | L | API creation is covered in Phase 2 from the schema. |

## Part fields

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part-12 | The IPN field is not required. | [part-views.md#L30](../../requirements/docs/part-views.md#L30) | M | IPN uniqueness is not stated (see index, Not in docs). |
| R-Part-13 | The part Name is a unique text label. | [part-views.md#L32](../../requirements/docs/part-views.md#L32) | H | Scope of "unique" is unclear given revisions are separate parts (index, doc issue 2). |
| R-Part-14 | Description is a longer-form text field. | [part-views.md#L34](../../requirements/docs/part-views.md#L34) | L | Required or not, and max length, not stated. |
| R-Part-15 | Revision is optional. | [part-views.md#L36](../../requirements/docs/part-views.md#L36) | M | Revision rules are in REV. |
| R-Part-16 | Keywords are optional and make part search more efficient. | [part-views.md#L38](../../requirements/docs/part-views.md#L38) | M | Testable as: a part is found by searching one of its keywords. |
| R-Part-17 | External Link holds a URL to an external page. | [part-views.md#L40](../../requirements/docs/part-views.md#L40) | L | The 1.5.6 UI labels this field *Link*, not *External Link* (index doc issue 13). An invalid URL or one without a scheme is rejected: "Enter a valid URL." (1.5.6 API, 2026-10-11). |

## Import from file (data import wizard)

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part-18 | *Import from File* in the *Add Parts* menu opens the data import wizard. | [part-create.md#L57-59](../../requirements/docs/part-create.md#L57-L59) | M | |
| R-Part-19 | To import data, the user must be a staff user and have the `change` permission for the model. | [concepts-data_import.md#L28](../../requirements/docs/concepts-data_import.md#L28) | H | Unclear how this combines with R-Part-03 (create permission) for *Import from File* (index, doc issue 7). |
| R-Part-20 | Related data must already exist; for parts, part categories must exist and the category column must be mapped to them. | [concepts-data_import.md#L32](../../requirements/docs/concepts-data_import.md#L32) | M | |
| R-Part-21 | Multi-level imports are not supported: one model per import. | [concepts-data_import.md#L35](../../requirements/docs/concepts-data_import.md#L35) | M | |
| R-Part-22 | Related fields map by `ID` by default; some models allow a natural key, such as `name` for part categories. | [concepts-data_import.md#L39-41](../../requirements/docs/concepts-data_import.md#L39-L41) | M | |
| R-Part-23 | If a related field's unique identifier cannot be determined, the user must map it manually during import. | [concepts-data_import.md#L44](../../requirements/docs/concepts-data_import.md#L44) | M | |
| R-Part-24 | An import started from a data table is linked automatically to that table's data type. | [concepts-data_import.md#L58](../../requirements/docs/concepts-data_import.md#L58), [#L72](../../requirements/docs/concepts-data_import.md#L72) | M | |
| R-Part-25 | Import sessions are stored on the server; the user can leave the page and return to check progress. | [concepts-data_import.md#L52](../../requirements/docs/concepts-data_import.md#L52), [#L96](../../requirements/docs/concepts-data_import.md#L96) | M | |
| R-Part-26 | Import sessions are listed in the Admin Center. | [concepts-data_import.md#L54](../../requirements/docs/concepts-data_import.md#L54) | L | |
| R-Part-27 | A general import from the Admin Center (staff users) requires selecting the data type. | [concepts-data_import.md#L66](../../requirements/docs/concepts-data_import.md#L66) | L | |
| R-Part-28 | The server auto-matches file columns to fields; the user can adjust the mapping. | [concepts-data_import.md#L90](../../requirements/docs/concepts-data_import.md#L90) | M | |
| R-Part-29 | Each row must be selected and confirmed before it is imported. | [concepts-data_import.md#L104](../../requirements/docs/concepts-data_import.md#L104) | H | |
| R-Part-30 | Row errors are displayed; the user can correct the data and re-process it. | [concepts-data_import.md#L104](../../requirements/docs/concepts-data_import.md#L104) | H | Error texts not stated. |
| R-Part-31 | Row states are Error (must be corrected before import), Pending (ready) and Imported. | [concepts-data_import.md#L106-110](../../requirements/docs/concepts-data_import.md#L106-L110) | M | |
| R-Part-32 | Each row can be imported or removed individually. | [concepts-data_import.md#L112](../../requirements/docs/concepts-data_import.md#L112) | M | |
| R-Part-33 | The session is complete once all rows are processed, and can then be closed. | [concepts-data_import.md#L112-116](../../requirements/docs/concepts-data_import.md#L112-L116) | L | |
| R-Part-34 | Bulk upload is non-reversible. | [concepts-data_import.md#L18](../../requirements/docs/concepts-data_import.md#L18) | L | Warning; implies no undo. |

## Import to update existing records

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part-35 | Updating existing records needs a unique identifier per record; the `ID` field must be mapped. | [concepts-data_import.md#L120](../../requirements/docs/concepts-data_import.md#L120), [#L142](../../requirements/docs/concepts-data_import.md#L142) | M | |
| R-Part-36 | Creating and updating records cannot be mixed in one import session. | [concepts-data_import.md#L129](../../requirements/docs/concepts-data_import.md#L129) | M | |
| R-Part-37 | Updating is only possible from an Admin Center session with *Update Existing Records* selected. | [concepts-data_import.md#L134-136](../../requirements/docs/concepts-data_import.md#L134-L136) | M | |
| R-Part-38 | In update mode, each row matching an existing record updates that record. | [concepts-data_import.md#L148](../../requirements/docs/concepts-data_import.md#L148) | H | |

## Import from supplier

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part-39 | Importing parts from a supplier requires a plugin for that supplier. | [part-create.md#L65-66](../../requirements/docs/part-create.md#L65-L66) | L | No supplier plugin in the test instance: likely untestable. |
| R-Part-40 | *Import Part* in the Part Category view runs a wizard: confirm category, select parameters, create initial stock. | [part-create.md#L75-79](../../requirements/docs/part-create.md#L75-L79) | L | Needs a supplier plugin. |
| R-Part-41 | For an existing part, a supplier part and its manufacturer part can be imported from the supplier panel (*Import supplier part*). | [part-create.md#L85](../../requirements/docs/part-create.md#L85) | L | Needs a supplier plugin. |
