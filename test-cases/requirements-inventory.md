# Requirements inventory: index

Testable rules from `requirements/docs/` (InvenTree 1.5.6 docs), one file per Area. Built by P03 on 2026-10-10; **pending architect review**. Read this file first, then only the Area files a request needs.

Each rule sits in one primary Area; other Areas point to it under "Cross-references". UI Areas take their rules from the docs; API Areas (`CRUD`, `LST`, `VAL`, `REL`, `SEC`) from the OpenAPI schema slice `requirements/openapi-parts.yaml` (built 2026-10-13, also **pending architect review**). For UI rules check the Not in docs and Doc issues tables; for API rules, Not in schema and Schema issues.

## Areas

| Area | Covers | Rules | File |
|---|---|---|---|
| Part | Create Part form, part fields, import from file, update import, supplier import | 41 | [Part_Creation_and_Import/requirements-inventory.md](Part_Creation_and_Import/requirements-inventory.md) |
| Detail_View | Header, image, Stock, Allocated, BOM, Build Orders, Used In, Suppliers, order tabs, Test Templates/Results, Related Parts, Attachments | 70 | [Part_Detail_View/requirements-inventory.md](Part_Detail_View/requirements-inventory.md) |
| Categories | Hierarchy, category part list, filters | 7 | [Categories/requirements-inventory.md](Categories/requirements-inventory.md) |
| ATT | Virtual, Assembly, Component, Testable, Trackable, Purchaseable, Salable, Consumable, Locked, Active | 29 | [Attributes/requirements-inventory.md](Attributes/requirements-inventory.md) |
| Unit_measure | Part units, supplier part units, unit syntax, custom units, BOM quantities | 18 | [Units_of_Measure/requirements-inventory.md](Units_of_Measure/requirements-inventory.md) |
| REV | Revision fields, restrictions, settings, creation, navigation | 15 | [Revisions/requirements-inventory.md](Revisions/requirements-inventory.md) |
| Part_Params | Parameters, templates, uniqueness, category defaults, parametric tables, units | 36 | [Parameters/requirements-inventory.md](Parameters/requirements-inventory.md) |
| Part_Template | Template flag, variants, serial and stock rules, cascading tests, inherited BOM | 11 | [Templates_and_Variants/requirements-inventory.md](Templates_and_Variants/requirements-inventory.md) |
| XF | Cross-functional flows composed of the rules above (no new rules) | 7 | [Cross_Functional_Scenarios/requirements-inventory.md](Cross_Functional_Scenarios/requirements-inventory.md) |
| **Total** | | **227** (+7 XF flows) | |

## API Areas

| Area | Covers | Rules | File |
|---|---|---|---|
| CRUD | Create, read, update, delete on Parts and Part Categories | 17 | [API_Create_Read_Update_Delete/requirements-inventory.md](API_Create_Read_Update_Delete/requirements-inventory.md) |
| LST | Parts and category lists: pagination, filters, ordering, search | 16 | [API_Lists_and_Filters/requirements-inventory.md](API_Lists_and_Filters/requirements-inventory.md) |
| VAL | Field validation: required, max lengths, nullable, read-only, write-only, types | 18 | [API_Field_Validation/requirements-inventory.md](API_Field_Validation/requirements-inventory.md) |
| REL | Category, default location, category hierarchy, supplier links, locked parts | 11 | [API_Relationships/requirements-inventory.md](API_Relationships/requirements-inventory.md) |
| SEC | Authentication, API token, role permissions per operation | 9 | [API_Security_and_Permissions/requirements-inventory.md](API_Security_and_Permissions/requirements-inventory.md) |
| **Total** | | **71** | |

## Not in docs

Items the brief asks us to cover that the docs do not state. Cases for these need an answer in the Area's `open-questions.md` first.

| # | Brief item | What the docs say | Area |
|---|---|---|---|
| 1 | Duplicate IPN is a negative case | Only that IPN is not required ([part-views.md#L30](../requirements/docs/part-views.md#L30)). No uniqueness rule for IPN. | Part |
| 2 | Revision-of-revision prevention | Nothing. Restrictions listed are self-reference, unique codes, templates, variant template references ([part-revision.md#L36-39](../requirements/docs/part-revision.md#L36-L39)). | REV |
| 3 | Inactive part restrictions | Only "not available for many actions" ([part-index.md#L116](../requirements/docs/part-index.md#L116)); no list of actions. | ATT |
| 4 | Unique codes (name, IPN and revision together) | Name is "(unique)" ([part-views.md#L32](../requirements/docs/part-views.md#L32)); revision codes unique per part ([part-revision.md#L37](../requirements/docs/part-revision.md#L37)). No combined rule. | Part, REV |
| 5 | Category hierarchy management | Creating, editing, moving and deleting categories, and structural categories, are not described. | Categories |
| 6 | Category filtering | "Multiple user-configurable filters" ([part-index.md#L44](../requirements/docs/part-index.md#L44)); the filters are not named. | Categories |
| 7 | *Revisions* tab | No tab described; a revision selector drop-down instead ([part-revision.md#L72](../requirements/docs/part-revision.md#L72)). | REV |
| 8 | *Build Orders* tab | Columns listed; visibility condition and actions not stated ([part-views.md#L88](../requirements/docs/part-views.md#L88)). | Detail_View |
| 9 | Required fields and limits on the Create Part form | "Fill out the required attributes" ([part-create.md#L31](../requirements/docs/part-create.md#L31)); which fields are required and any max lengths are not stated. | Part |
| 10 | Units of measure configuration | Only that custom units are managed in the *Physical Units* settings tab ([concepts-units.md#L97](../requirements/docs/concepts-units.md#L97)); form fields and validation not described. | Unit_measure |

## Doc issues to review

Contradictions, ambiguities and missing details found while building the inventory. Settle each before cases are written for the rules it affects.

| # | Kind | Issue | Doc lines | Affects |
|---|---|---|---|---|
| 1 | Conflict | Default unit of measure: "blank ... dimensionless pieces" vs "The default is 'pcs'". | [part-index.md#L120](../requirements/docs/part-index.md#L120), [part-views.md#L44](../requirements/docs/part-views.md#L44) | R-Unit_measure-02 |
| 2 | Ambiguous | Name is "(unique)", but a revision is a separate part of the same item: is the name unique globally, or with revision (and IPN)? | [part-views.md#L32](../requirements/docs/part-views.md#L32), [part-revision.md#L23](../requirements/docs/part-revision.md#L23) | R-Part-13, R-REV-12 |
| 3 | Conflict | Test key "consists only of lowercase alphanumeric characters", but the example key `_100percenttest` has an underscore. | [part-test.md#L31](../requirements/docs/part-test.md#L31), [#L43](../requirements/docs/part-test.md#L43) | R-Detail_View-32, R-Detail_View-33 |
| 4 | Ambiguous | Test name "unique for a given part (or across a set of part variants)": can a variant reuse a name defined on its template? | [part-test.md#L27](../requirements/docs/part-test.md#L27) | R-Detail_View-31 |
| 5 | Conflict | Parameter templates are created in the "Admin Center", but the steps say the "Settings" page. | [concepts-parameters.md#L47](../requirements/docs/concepts-parameters.md#L47), [#L51](../requirements/docs/concepts-parameters.md#L51) | R-Part_Params-10 |
| 6 | Gap | BOM checksum includes "Allow Variants", which is missing from the BOM line item property table. | [manufacturing-bom.md#L179](../requirements/docs/manufacturing-bom.md#L179), [#L25-37](../requirements/docs/manufacturing-bom.md#L25-L37) | R-Detail_View-50, R-Detail_View-65 |
| 7 | Ambiguous | *Add Parts* menu needs "create" permission; data import needs staff plus "change" permission. Which applies to *Import from File*? | [part-create.md#L21-22](../requirements/docs/part-create.md#L21-L22), [concepts-data_import.md#L28](../requirements/docs/concepts-data_import.md#L28) | R-Part-03, R-Part-19 |
| 8 | Gap | Setting names or defaults missing: `PART_ENABLE_REVISION` and `PART_REVISION_ASSEMBLY_ONLY` (unrendered macro), *Create Initial Stock*, Related Parts, unit validation, `PART_ENABLE_LOCKING` default, return and transfer order features. | [part-revision.md#L47-48](../requirements/docs/part-revision.md#L47-L48), [part-create.md#L37](../requirements/docs/part-create.md#L37), [part-views.md#L144](../requirements/docs/part-views.md#L144), [concepts-parameters.md#L187](../requirements/docs/concepts-parameters.md#L187), [part-index.md#L112](../requirements/docs/part-index.md#L112) | R-REV-11, R-Part-07, R-Detail_View-41, R-Part_Params-32, R-ATT-27, R-Detail_View-26, R-Detail_View-27 |
| 9 | Possibly outdated | Template is toggled via a "Details" tab and a slider on the right-hand side; this may describe an older UI. | [part-template.md#L34-37](../requirements/docs/part-template.md#L34-L37) | R-Part_Template-02 |
| 10 | Doc error | The attachments page says "Parameters can be associated with various InvenTree models" (copy error; no rule taken from it). | [concepts-attachments.md#L20](../requirements/docs/concepts-attachments.md#L20) | None |
| 11 | Ambiguous | Trackable stock "should" have a batch or serial number, "not strictly enforced" for build outputs: where is it enforced? | [part-trackable.md#L19-21](../requirements/docs/part-trackable.md#L19-L21) | R-ATT-13 |
| 12 | Gap | How a part is locked or unlocked is not described. | [part-index.md#L104-112](../requirements/docs/part-index.md#L104-L112) | R-ATT-24 to R-ATT-27 |
| 13 | Outdated (confirmed in app) | The docs call the field *External Link*; the 1.5.6 form and detail page label it *Link*. Found in the MCP run of 2026-10-11. | [part-views.md#L40](../requirements/docs/part-views.md#L40) | R-Part-17 |
| 14 | Outdated (confirmed in app) | The docs describe an *Add Supplier Data* option on the Create Part form; 1.5.6 has none. Supplier and manufacturer fields sit in a *Supplier Information* section shown while *Purchaseable* is checked (default on). Found in the MCP run of 2026-10-11. | [part-create.md#L47-51](../requirements/docs/part-create.md#L47-L51) | R-Part-09, R-Part-10 |
| 15 | Gap (confirmed in app) | The *Suppliers* tab is hidden from users without purchase-order view permission; the docs give only the Purchaseable condition. Found in the MCP run of 2026-10-11. | [part-views.md#L100-102](../requirements/docs/part-views.md#L100-L102) | R-Detail_View-23 |

## Not in schema (API)

Items the brief or the API rules need that the schema does not state. Cases for these need an answer in the Area's `open-questions.md` first, or are written with the outcome marked not known.

| # | Item | What the schema says | Area |
|---|---|---|---|
| 1 | Error responses: status codes for invalid data, missing or invalid credentials, missing permission, unknown ID; error body format | Only the success code of each operation (`200`, `201`, `204`), e.g. [openapi-parts.yaml#L747](../requirements/openapi-parts.yaml#L747). The brief requires status-code assertions on negative cases. | VAL, SEC, REL, CRUD |
| 2 | Uniqueness of name, IPN and revision (brief: duplicate IPN is a negative case; "conflicts") | Nothing. The app allows duplicate IPN by default and enforces name + IPN + revision together ([findings F-04, F-05](findings.md)). | VAL, REL |
| 3 | Deleting a category that has parts or child categories | `DELETE` takes only the `id`; no options or outcome stated ([openapi-parts.yaml#L1406](../requirements/openapi-parts.yaml#L1406)). | CRUD, REL |
| 4 | Whether an active part can be deleted | Nothing; `DELETE` documents only `204` ([openapi-parts.yaml#L2803](../requirements/openapi-parts.yaml#L2803)). | CRUD |
| 5 | Values sent for read-only fields: ignored or rejected | Fields are marked `readOnly` only. | VAL |
| 6 | Bulk `PUT`/`PATCH` on list endpoints: how records are selected | The body is a plain `Part` or `Category` ([openapi-parts.yaml#L778](../requirements/openapi-parts.yaml#L778), [openapi-parts.yaml#L983](../requirements/openapi-parts.yaml#L983)). | CRUD |
| 7 | List response when `limit` is not sent; default and maximum page size | The response is always documented as paginated ([openapi-parts.yaml#L432](../requirements/openapi-parts.yaml#L432)). | LST |

Answered on 2026-10-13 (details in `API_Create_Read_Update_Delete/open-questions.md`): item 3 by Q-CRUD-03, item 4 by Q-CRUD-02, item 6 by Q-CRUD-04, and the unknown-ID part of item 1 by Q-CRUD-01 (`404 Not Found` for a `GET` or `DELETE` of a resource that does not exist; other error codes remain open). Item 7 is answered by Schema issue 8: a list without `limit` returns a plain array.

## Schema issues to review (API)

| # | Kind | Issue | Schema lines | Affects |
|---|---|---|---|---|
| 1 | Ambiguous | Each Parts and Category operation lists two OAuth2 scopes, e.g. `r:add:part` **and** `r:add:build`; supplier parts list `r:add:part` and `r:add:purchase_order`. In OpenAPI a scope list means all are needed: does a user need the Build role too, or either one? | [openapi-parts.yaml#L747](../requirements/openapi-parts.yaml#L747), [openapi-parts.yaml#L185](../requirements/openapi-parts.yaml#L185) | R-SEC-03 to R-SEC-08 |
| 2 | Description error | `created_after` and `created_before` are described as "Updated after/before", but filter on the creation date. | [openapi-parts.yaml#L491](../requirements/openapi-parts.yaml#L491), [openapi-parts.yaml#L497](../requirements/openapi-parts.yaml#L497) | R-LST-11 |
| 3 | Type mismatch | The `category` list filter is typed `integer`, but its description accepts the literal `null`. | [openapi-parts.yaml#L469](../requirements/openapi-parts.yaml#L469) | R-LST-06 |
| 4 | Ambiguous | One schema serves request and response, so `required` includes read-only fields (`Part`: `pk`, `full_name`, `barcode_hash`, `thumbnail`...). Input-required = required and not `readOnly`: `name` only, for both `Part` and `Category`. | [openapi-parts.yaml#L4365](../requirements/openapi-parts.yaml#L4365), [openapi-parts.yaml#L3572](../requirements/openapi-parts.yaml#L3572) | R-VAL-01, R-VAL-13 |
| 5 | Schema vs app (confirmed) | `Part.image` is declared `format: uri`; the app returns site-relative paths (`/media/...`). Findings F-06. | [openapi-parts.yaml#L4156](../requirements/openapi-parts.yaml#L4156) | R-VAL-11 |
| 6 | Schema vs app (confirmed) | `SupplierPart.availability_updated` is declared `format: date-time`; the app returns `YYYY-MM-DD HH:MM`. Findings F-07. | [openapi-parts.yaml#L5815](../requirements/openapi-parts.yaml#L5815) | R-REL-08 |
| 7 | Schema vs app (confirmed) | `DELETE /api/part/category/{id}/` documents no request body; 1.5.6 requires `delete_parts` and `delete_child_categories`, else `400`. Findings F-08. | [openapi-parts.yaml#L1406](../requirements/openapi-parts.yaml#L1406) | R-CRUD-10 |
| 8 | Schema vs app (confirmed) | List endpoints are documented as paginated but return a plain array unless `limit` is sent. Findings F-09. | [openapi-parts.yaml#L432](../requirements/openapi-parts.yaml#L432), [openapi-parts.yaml#L848](../requirements/openapi-parts.yaml#L848) | R-LST-01, R-LST-14 |
| 9 | Schema vs app (confirmed) | Bulk `PUT`/`PATCH` are documented as returning `Part`/`Category`; 1.5.6 returns `{"success", "items"}`, and the part entries lack `category_name`. Findings F-10. | [openapi-parts.yaml#L778](../requirements/openapi-parts.yaml#L778), [openapi-parts.yaml#L812](../requirements/openapi-parts.yaml#L812), [openapi-parts.yaml#L983](../requirements/openapi-parts.yaml#L983), [openapi-parts.yaml#L1017](../requirements/openapi-parts.yaml#L1017) | R-CRUD-17 |

## Out of scope or outside the docs set

- Build, sales, purchase, return and transfer order behaviour beyond what the part pages state (R-ATT-06, -07, -16, -17, -22 touch these modules).
- Supplier import plugins (R-Part-39 to R-Part-41): no plugin in the test instance.
- Mobile app and Python library.
- Linked pages not in `requirements/docs/`: `settings/global.md`, `purchasing/supplier.md`, `stock/index.md`, `stock/test.md`, `manufacturing/build.md`, `manufacturing/allocate.md`, `part/pricing.md`, `part/stocktake.md`, `stock/disassemble.md`.
- API endpoints in the schema slice but outside the brief's API scope: pricing, internal and sale prices, BOM copy and validation, stocktake, test templates, related parts, thumbnails, serial numbers, requirements, category parameter templates. The slice keeps them for reference; no API rules are inventoried for them.
