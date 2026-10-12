# Requirements inventory: index

Testable rules from `requirements/docs/` (InvenTree 1.5.6 docs), one file per Area. Built by P03 on 2026-10-10; **pending architect review**. Read this file first, then only the Area files a request needs.

Each rule sits in one primary Area; other Areas point to it under "Cross-references". API Areas (`LST`, `VAL`, `REL`, `SEC`) are not here: their rules come from the OpenAPI schema in Phase 2.

## Areas

| Area | Covers | Rules | File |
|---|---|---|---|
| Part | Create Part form, part fields, import from file, update import, supplier import | 41 | [Part/requirements-inventory.md](Part/requirements-inventory.md) |
| Detail_View | Header, image, Stock, Allocated, BOM, Build Orders, Used In, Suppliers, order tabs, Test Templates/Results, Related Parts, Attachments | 70 | [Detail_View/requirements-inventory.md](Detail_View/requirements-inventory.md) |
| Categories | Hierarchy, category part list, filters | 7 | [Categories/requirements-inventory.md](Categories/requirements-inventory.md) |
| ATT | Virtual, Assembly, Component, Testable, Trackable, Purchaseable, Salable, Consumable, Locked, Active | 29 | [ATT/requirements-inventory.md](ATT/requirements-inventory.md) |
| Unit_measure | Part units, supplier part units, unit syntax, custom units, BOM quantities | 18 | [Unit_measure/requirements-inventory.md](Unit_measure/requirements-inventory.md) |
| REV | Revision fields, restrictions, settings, creation, navigation | 15 | [REV/requirements-inventory.md](REV/requirements-inventory.md) |
| Part_Params | Parameters, templates, uniqueness, category defaults, parametric tables, units | 36 | [Part_Params/requirements-inventory.md](Part_Params/requirements-inventory.md) |
| Part_Template | Template flag, variants, serial and stock rules, cascading tests, inherited BOM | 11 | [Part_Template/requirements-inventory.md](Part_Template/requirements-inventory.md) |
| **Total** | | **227** | |

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

## Out of scope or outside the docs set

- Build, sales, purchase, return and transfer order behaviour beyond what the part pages state (R-ATT-06, -07, -16, -17, -22 touch these modules).
- Supplier import plugins (R-Part-39 to R-Part-41): no plugin in the test instance.
- Mobile app and Python library.
- Linked pages not in `requirements/docs/`: `settings/global.md`, `purchasing/supplier.md`, `stock/index.md`, `stock/test.md`, `manufacturing/build.md`, `manufacturing/allocate.md`, `part/pricing.md`, `part/stocktake.md`, `stock/disassemble.md`.
