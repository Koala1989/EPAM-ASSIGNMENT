# Requirements inventory: Detail_View (part detail view and tabs)

Rules stated in `requirements/docs/` (InvenTree 1.5.6). Built by P03 on 2026-10-10; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare. Risk values are the agent's proposal.

Tab rules that belong to another Area (Parameters, Variants, Revisions) are listed under Cross-references, not repeated. The brief's "Revisions" tab is not described in the docs; they describe a revision selector instead (R-REV-14).

## Header and details

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Detail_View-01 | Part details are shown in the header panel with the *Show Part Details* toggle. | [part-views.md#L24](../../requirements/docs/part-views.md#L24) | L | Toggle label to confirm in the app. |
| R-Detail_View-02 | The details show the creation date and the user who created the part. | [part-views.md#L42](../../requirements/docs/part-views.md#L42) | L | |
| R-Detail_View-03 | Part data is organised in tabs, each with its own function. | [part-views.md#L48](../../requirements/docs/part-views.md#L48) | L | |
| R-Detail_View-04 | A part can have an image, shown on its detail page. | [part-index.md#L144](../../requirements/docs/part-index.md#L144) | L | |
| R-Detail_View-05 | A thumbnail is generated automatically when a part image is uploaded. | [part-index.md#L150](../../requirements/docs/part-index.md#L150) | L | |
| R-Detail_View-06 | Hovering over the part image offers: upload new image, select from existing images, delete image. | [part-index.md#L156-164](../../requirements/docs/part-index.md#L156-L164) | M | |
| R-Detail_View-07 | Part notes support Markdown formatting. | [part-views.md#L160](../../requirements/docs/part-views.md#L160) | L | |

## Variants tab

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Detail_View-08 | The *Variants* tab is visible only if the part is a Template part. | [part-views.md#L52](../../requirements/docs/part-views.md#L52) | M | |

## Stock tab

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Detail_View-09 | The *Stock* tab lists all stock items for the part with quantity, location and status. | [part-views.md#L58](../../requirements/docs/part-views.md#L58) | M | |
| R-Detail_View-10 | *Export* opens an options dialog, then downloads a file with all the part's stock items. | [part-views.md#L68](../../requirements/docs/part-views.md#L68) | M | |
| R-Detail_View-11 | *New Stock Item* opens a dialog to create a stock item for the part. | [part-views.md#L72](../../requirements/docs/part-views.md#L72) | H | Used by the cross-functional flow. |
| R-Detail_View-12 | Stock actions in the drop-down are enabled when stock items are selected. | [part-views.md#L76](../../requirements/docs/part-views.md#L76) | M | |
| R-Detail_View-13 | A part's total stock is the sum of all its stock items. | [part-index.md#L19](../../requirements/docs/part-index.md#L19) | H | |
| R-Detail_View-14 | A part whose total stock is below its minimum stock level is flagged "low stock". | [part-index.md#L23](../../requirements/docs/part-index.md#L23) | M | Behaviour exactly at the minimum is not stated. |
| R-Detail_View-15 | A part whose total stock exceeds its maximum stock level is flagged "overstocked". | [part-index.md#L27](../../requirements/docs/part-index.md#L27) | M | Behaviour exactly at the maximum is not stated. |

## Other tabs

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Detail_View-16 | The *Allocated* tab shows how many units are allocated to pending build orders and sales orders. | [part-views.md#L80](../../requirements/docs/part-views.md#L80) | M | |
| R-Detail_View-17 | The *Allocated* tab is visible only if the part is a Component or Salable. | [part-views.md#L80](../../requirements/docs/part-views.md#L80) | M | |
| R-Detail_View-18 | The *BOM* tab lists the sub-components and quantities needed to build the assembly. | [part-views.md#L84](../../requirements/docs/part-views.md#L84) | M | |
| R-Detail_View-19 | The *BOM* tab is visible only if the part is an Assembly. | [part-views.md#L84](../../requirements/docs/part-views.md#L84) | M | |
| R-Detail_View-20 | The *Build Orders* tab lists the part's builds with quantity, status, creation and completion dates. | [part-views.md#L88](../../requirements/docs/part-views.md#L88) | M | Visibility condition not stated. |
| R-Detail_View-21 | The *Used In* tab lists parts this part is used to make, and is visible only if the part is a Component. | [part-views.md#L92](../../requirements/docs/part-views.md#L92) | M | |
| R-Detail_View-22 | The *Part Pricing* tab shows pricing aggregated from several sources. | [part-views.md#L96](../../requirements/docs/part-views.md#L96) | L | Not in the brief's tab list; pricing page not in `requirements/docs/`. |
| R-Detail_View-23 | The *Suppliers* tab lists suppliers and manufacturers, and is visible only if the part is Purchaseable. | [part-views.md#L100-102](../../requirements/docs/part-views.md#L100-L102) | M | In 1.5.6 the tab is also hidden from users without purchase-order view permission (e.g. `engineer`), which the docs do not state (index doc issue 15). Manufacturer parts show in the tab's *Manufacturers* section. |
| R-Detail_View-24 | The *Purchase Orders* tab lists the part's purchase orders, and is shown only if the part is Purchaseable. | [part-views.md#L108-110](../../requirements/docs/part-views.md#L108-L110) | M | |
| R-Detail_View-25 | The *Sales Orders* tab lists the part's sales orders with customer, status, creation and shipment dates. | [part-views.md#L114](../../requirements/docs/part-views.md#L114) | L | Visibility condition not stated. |
| R-Detail_View-26 | The *Return Orders* tab is visible only if the part is Salable and the return order feature is enabled. | [part-views.md#L118](../../requirements/docs/part-views.md#L118) | L | Feature setting not named. |
| R-Detail_View-27 | The *Transfer Orders* tab is hidden if the part is Virtual or the transfer order feature is disabled. | [part-views.md#L122](../../requirements/docs/part-views.md#L122) | L | Feature setting not named. |
| R-Detail_View-28 | The *Stock History* tab shows historical stock levels. | [part-views.md#L126](../../requirements/docs/part-views.md#L126) | L | |

## Test Templates and Test Results tabs

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Detail_View-29 | For a Testable part, the user can define tests to be performed on its stock items. | [part-views.md#L130](../../requirements/docs/part-views.md#L130), [part-test.md#L15](../../requirements/docs/part-test.md#L15) | M | Whether the *Test Templates* tab is hidden for non-Testable parts is not stated. |
| R-Detail_View-30 | The *Test Results* tab shows results from all the part's stock items in one table, and is visible only if the part is Testable. | [part-views.md#L134](../../requirements/docs/part-views.md#L134) | M | |
| R-Detail_View-31 | A test name must be unique for a part (or across a set of variants). | [part-test.md#L27](../../requirements/docs/part-test.md#L27) | H | Scope across variants is ambiguous (index, doc issue 4). |
| R-Detail_View-32 | A test key is generated from the test name whenever the template is saved, using only lowercase alphanumeric characters. | [part-test.md#L31](../../requirements/docs/part-test.md#L31) | M | Contradicted by the `_100percenttest` example (index, doc issue 3). |
| R-Detail_View-33 | Key examples: "Firmware Version" → `firmwareversion`; " My NEW T E sT " → `mynewtest`; "100 Percent Test" → `_100percenttest`; "Test 123" → `test123`. | [part-test.md#L41-44](../../requirements/docs/part-test.md#L41-L44) | M | Ready-made test data. |
| R-Detail_View-34 | The test description is not used by the testing framework. | [part-test.md#L48](../../requirements/docs/part-test.md#L48) | L | |
| R-Detail_View-35 | The *Required* flag marks a test as crucial for accepting a stock item. | [part-test.md#L52](../../requirements/docs/part-test.md#L52) | M | |
| R-Detail_View-36 | With *Requires Value*, a test result must set a value. | [part-test.md#L56](../../requirements/docs/part-test.md#L56) | H | |
| R-Detail_View-37 | With *Requires Attachment*, a test result must include an uploaded file. | [part-test.md#L60](../../requirements/docs/part-test.md#L60) | H | |
| R-Detail_View-38 | A test can be disabled (Enabled = false) while keeping the template. | [part-test.md#L64](../../requirements/docs/part-test.md#L64) | M | |
| R-Detail_View-39 | Deleting a test template also deletes its test results. | [part-test.md#L64](../../requirements/docs/part-test.md#L64) | H | |

## Related Parts tab

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Detail_View-40 | Related parts can be added, and are shown in the *Related Parts* table on the part page. | [part-views.md#L138-140](../../requirements/docs/part-views.md#L138-L140) | M | Whether the relation shows on both parts is not stated. |
| R-Detail_View-41 | The Related Parts feature can be enabled or disabled in the global part settings. | [part-views.md#L144](../../requirements/docs/part-views.md#L144) | M | Setting name and default not stated. |

## Attachments tab

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Detail_View-42 | The *Attachments* tab lists the part's file attachments; a part can have several. | [part-views.md#L154](../../requirements/docs/part-views.md#L154) | M | |
| R-Detail_View-43 | *Add attachment* uploads a file; *Add external link* adds a URL. | [concepts-attachments.md#L55](../../requirements/docs/concepts-attachments.md#L55) | M | |
| R-Detail_View-44 | Uploaded files can be downloaded or viewed by users with the appropriate permissions. | [concepts-attachments.md#L34](../../requirements/docs/concepts-attachments.md#L34) | M | Which permission is not stated. |
| R-Detail_View-45 | For a valid image, a thumbnail is generated in the background with the original aspect ratio. | [concepts-attachments.md#L38-41](../../requirements/docs/concepts-attachments.md#L38-L41) | L | Formats: any Pillow format, e.g. PNG, JPEG, GIF, BMP, WEBP (L47). |
| R-Detail_View-46 | `is_image` is true for valid images and false for other files. | [concepts-attachments.md#L42](../../requirements/docs/concepts-attachments.md#L42) | M | API-visible field. |
| R-Detail_View-47 | A file with an image extension but corrupt data gets no thumbnail and `is_image` stays false. | [concepts-attachments.md#L43](../../requirements/docs/concepts-attachments.md#L43) | M | Error-guessing case stated by the docs. |
| R-Detail_View-48 | Link attachments never get a thumbnail. | [concepts-attachments.md#L44](../../requirements/docs/concepts-attachments.md#L44) | L | |
| R-Detail_View-49 | A file attachment can be renamed with *Edit* without re-uploading it. | [concepts-attachments.md#L59](../../requirements/docs/concepts-attachments.md#L59) | M | |

## BOM tab

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Detail_View-50 | A BOM has zero or more line items: Part, Reference, Raw Amount, Quantity, Attrition, Setup Quantity, Rounding Multiple, Consumable, Inherited, Optional, Note. | [manufacturing-bom.md#L23-37](../../requirements/docs/manufacturing-bom.md#L23-L37) | M | Required fields not stated. |
| R-Detail_View-51 | Attrition is a percentage of the base quantity. | [manufacturing-bom.md#L31](../../requirements/docs/manufacturing-bom.md#L31) | M | |
| R-Detail_View-52 | Setup Quantity is added to the base quantity. | [manufacturing-bom.md#L32](../../requirements/docs/manufacturing-bom.md#L32) | M | |
| R-Detail_View-53 | The required quantity is rounded up to the nearest Rounding Multiple. | [manufacturing-bom.md#L33](../../requirements/docs/manufacturing-bom.md#L33) | M | |
| R-Detail_View-54 | A Consumable BOM line is not allocated to a Build Order and cannot be allocated in its allocation table. | [manufacturing-bom.md#L53](../../requirements/docs/manufacturing-bom.md#L53), [#L59](../../requirements/docs/manufacturing-bom.md#L59) | M | |
| R-Detail_View-55 | The BOM-line Consumable flag applies to that BOM only and does not change the part. | [manufacturing-bom.md#L61](../../requirements/docs/manufacturing-bom.md#L61) | M | |
| R-Detail_View-56 | An Optional BOM line need not be allocated; when completing a build the user chooses to include or exclude optional items. | [manufacturing-bom.md#L65-67](../../requirements/docs/manufacturing-bom.md#L65-L67) | M | |
| R-Detail_View-57 | A BOM line can have several substitute parts, whose stock can be allocated against it. | [manufacturing-bom.md#L71](../../requirements/docs/manufacturing-bom.md#L71) | M | |
| R-Detail_View-58 | A line's available quantity includes the stock of its substitutes. | [manufacturing-bom.md#L74](../../requirements/docs/manufacturing-bom.md#L74) | M | |
| R-Detail_View-59 | The BOM opens in view mode; the *Edit* icon switches to editing mode to add, adjust or delete lines. | [manufacturing-bom.md#L124](../../requirements/docs/manufacturing-bom.md#L124) | M | |
| R-Detail_View-60 | Users without permission to edit BOMs do not see the *Edit* icon. | [manufacturing-bom.md#L127](../../requirements/docs/manufacturing-bom.md#L127) | H | Which permission is not stated. |
| R-Detail_View-61 | BOM data can be imported from a CSV or Excel file with the *Import BOM Data* icon. | [manufacturing-bom.md#L131-133](../../requirements/docs/manufacturing-bom.md#L131-L133) | M | Uses the data import rules in Part (R-Part-18 to R-Part-34). |
| R-Detail_View-62 | A BOM line is added in editing mode via the add icon, which opens the *Create BOM Item* form; Submit adds it. | [manufacturing-bom.md#L137-143](../../requirements/docs/manufacturing-bom.md#L137-L143) | M | |
| R-Detail_View-63 | A substitute is added with the *Actions* column icon, *Edit BOM Item Substitutes* form, *Add Substitute*. | [manufacturing-bom.md#L147-153](../../requirements/docs/manufacturing-bom.md#L147-L153) | M | |
| R-Detail_View-64 | Multi-level BOMs (sub-assemblies with their own BOM) are supported to any depth. | [manufacturing-bom.md#L157](../../requirements/docs/manufacturing-bom.md#L157) | M | |
| R-Detail_View-65 | Changing any checksum field of a BOM line (assembly, component, reference, quantity, attrition, setup quantity, rounding multiple, consumable, inherited, optional, allow variants) marks the assembly "not validated". | [manufacturing-bom.md#L163-181](../../requirements/docs/manufacturing-bom.md#L163-L181) | H | "Allow Variants" is not in the line item table (index, doc issue 6). |
| R-Detail_View-66 | The user must revalidate the BOM manually. | [manufacturing-bom.md#L183](../../requirements/docs/manufacturing-bom.md#L183) | M | |
| R-Detail_View-67 | Validation status shows at the top of the BOM table; when invalid it reads "Not Validated" with a *Validate BOM* button. | [manufacturing-bom.md#L187-191](../../requirements/docs/manufacturing-bom.md#L187-L191) | M | |
| R-Detail_View-68 | A BOM can be compared side by side with another assembly's BOM, with differences highlighted. | [manufacturing-bom.md#L197-205](../../requirements/docs/manufacturing-bom.md#L197-L205) | L | |
| R-Detail_View-69 | Comparison modes: show all, show different, show common; differences in red. | [manufacturing-bom.md#L209-217](../../requirements/docs/manufacturing-bom.md#L209-L217) | L | |
| R-Detail_View-70 | *Replace Component* on the component's *Used In* tab replaces it in the selected assemblies' BOMs. | [manufacturing-bom.md#L221-231](../../requirements/docs/manufacturing-bom.md#L221-L231) | M | |

## Cross-references

| Rule | Primary |
|---|---|
| *Parameters* tab and adding parameters | R-Part_Params-02, R-Part_Params-12 |
| Revision selector (the brief's "Revisions" tab) | R-REV-14, R-REV-15 |
| Inherited BOM lines across variants | R-Part_Template-09 to R-Part_Template-11 |
| Test templates cascade to variants | R-Part_Template-08 |
| BOM raw amount and units | R-Unit_measure-16 to R-Unit_measure-18 |
| Locked part: BOM and parameter restrictions, no delete | R-ATT-24 to R-ATT-27 |
| Virtual part: no stock, stock UI hidden | R-ATT-02, R-ATT-03 |
