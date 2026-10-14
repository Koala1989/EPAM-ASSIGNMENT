# Requirements inventory: ATT (attributes)

Rules stated in `requirements/docs/` (InvenTree 1.5.6). Built by P03 on 2026-10-10; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare. Risk values are the agent's proposal.

The docs describe three attributes the brief does not list: Testable, Consumable and Locked. They are included here.

## General

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-ATT-01 | A part's attributes determine which functions can be performed on or with it. | [part-index.md#L50](../../requirements/docs/part-index.md#L50) | M | |

## Virtual

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-ATT-02 | A Virtual part cannot have stock items. | [part-virtual.md#L15](../../requirements/docs/part-virtual.md#L15), [#L27](../../requirements/docs/part-virtual.md#L27) | H | |
| R-ATT-03 | Stock-related UI elements are hidden on a Virtual part's page. | [part-virtual.md#L27](../../requirements/docs/part-virtual.md#L27) | H | Which elements is not listed; Transfer Orders tab is one (R-Detail_View-27). |
| R-ATT-04 | Apart from stock, a Virtual part behaves like a regular part. | [part-virtual.md#L23](../../requirements/docs/part-virtual.md#L23) | M | |
| R-ATT-05 | A Virtual part can be a BOM sub-component; it stays listed in the BOM and in cost calculations but is not allocated in builds. | [part-virtual.md#L31-33](../../requirements/docs/part-virtual.md#L31-L33) | M | |
| R-ATT-06 | In a Build Order, Virtual parts are hidden from the required parts list; their cost is included in the build total. | [part-virtual.md#L37-39](../../requirements/docs/part-virtual.md#L37-L39) | M | Exercises the Build Orders module. |
| R-ATT-07 | A Virtual part can be added to a Sales Order; it is not allocated from stock but is included in the order and total cost. | [part-virtual.md#L43-47](../../requirements/docs/part-virtual.md#L43-L47) | M | Exercises the Sales Orders module. |

## Assembly and Component

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-ATT-08 | An Assembly part can be built from component parts and has a Bill of Materials. | [part-index.md#L62](../../requirements/docs/part-index.md#L62) | H | BOM rules are in Detail_View. |
| R-ATT-09 | An assembled stock item can be broken down into its components (disassembly). | [part-index.md#L64](../../requirements/docs/part-index.md#L64) | L | Disassembly page not in `requirements/docs/`. |
| R-ATT-10 | A Component part can be used as a sub-component of an Assembly. | [part-index.md#L68](../../requirements/docs/part-index.md#L68) | H | Whether a non-Component can be added to a BOM is not stated. |

## Testable

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-ATT-11 | A Testable part can have test templates, and test results can be recorded against its stock items. | [part-index.md#L72](../../requirements/docs/part-index.md#L72), [part-test.md#L15](../../requirements/docs/part-test.md#L15) | M | Test template rules are in Detail_View. |

## Trackable

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-ATT-12 | A Trackable part's stock items can be assigned batch numbers or serial numbers. | [part-index.md#L76](../../requirements/docs/part-index.md#L76) | H | |
| R-ATT-13 | A Trackable part's stock item should generally have a batch or serial number, including stock from purchase or build orders. | [part-trackable.md#L19-21](../../requirements/docs/part-trackable.md#L19-L21) | M | "Should" and "not strictly enforced": which cases are enforced is unclear (index, doc issue 11). |
| R-ATT-14 | Serial number input accepts: single (`1`), list (`1,3,5`), range (`1-5`), next (`~`), start-plus (`4+` with count needed), start-plus-length (`2+2` gives 2,3,4). | [part-trackable.md#L29-36](../../requirements/docs/part-trackable.md#L29-L36) | H | Equivalence partitions and boundaries for serial input. |
| R-ATT-15 | Serial rules can be combined, separated by spaces or commas: `1 3-5 9+2` and `1,3-5,9+2` give 1,3,4,5,9,10,11; `~+2` (next 14) gives 14,15,16; `~+` (next 14, 2 needed) gives 14,15. | [part-trackable.md#L38-42](../../requirements/docs/part-trackable.md#L38-L42) | M | |
| R-ATT-16 | A build output for a Trackable part can be created without serial numbers, as one output with the full quantity, to be serialised or split later. | [part-trackable.md#L51-53](../../requirements/docs/part-trackable.md#L51-L53) | M | Exercises the Build Orders module. |
| R-ATT-17 | If the BOM contains Trackable sub-components, serial numbers are required when creating build outputs, whether or not the assembly is Trackable. | [part-trackable.md#L56](../../requirements/docs/part-trackable.md#L56) | M | Exercises the Build Orders module. |

## Purchaseable and Salable

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-ATT-18 | A Purchaseable part can be bought from external suppliers: it can be linked to supplier parts and ordered on purchase orders. | [part-index.md#L82](../../requirements/docs/part-index.md#L82), [#L90](../../requirements/docs/part-index.md#L90) | H | Whether a non-Purchaseable part is blocked from purchase orders is not stated. |
| R-ATT-19 | A Salable part can be sold: it can be added to sales orders. | [part-index.md#L98](../../requirements/docs/part-index.md#L98) | H | Whether a non-Salable part is blocked from sales orders is not stated. |

## Consumable

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-ATT-20 | A Consumable part can have stock items, tracked as normal. | [part-consumable.md#L40](../../requirements/docs/part-consumable.md#L40) | M | |
| R-ATT-21 | A Consumable part can be a BOM sub-component like any other component. | [part-consumable.md#L44](../../requirements/docs/part-consumable.md#L44) | M | |
| R-ATT-22 | A Consumable part is not allocated to a Build Order, and its stock is not adjusted when the build completes. | [part-consumable.md#L48-50](../../requirements/docs/part-consumable.md#L48-L50) | M | Exercises the Build Orders module. |
| R-ATT-23 | The part-level Consumable flag applies everywhere; the BOM-line flag applies to that BOM only; setting both has no extra effect. | [part-consumable.md#L60-63](../../requirements/docs/part-consumable.md#L60-L63) | M | |

## Locked

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-ATT-24 | A locked part cannot be deleted. | [part-index.md#L108](../../requirements/docs/part-index.md#L108) | H | How a part is locked is not described. |
| R-ATT-25 | BOM items of a locked assembly cannot be created, edited or deleted. | [part-index.md#L109](../../requirements/docs/part-index.md#L109) | H | |
| R-ATT-26 | Parameters of a locked part cannot be created, edited or deleted. | [part-index.md#L110](../../requirements/docs/part-index.md#L110) | H | |
| R-ATT-27 | With `PART_ENABLE_LOCKING` disabled, the locked state is ignored and all operations are permitted. | [part-index.md#L112](../../requirements/docs/part-index.md#L112) | H | Default value not stated. |

## Active and Inactive

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-ATT-28 | All parts are Active by default. | [part-index.md#L116](../../requirements/docs/part-index.md#L116) | H | |
| R-ATT-29 | An inactive part is not available for many actions but remains in the database. | [part-index.md#L116](../../requirements/docs/part-index.md#L116) | H | Which actions are blocked is not stated (index, Not in docs). |

## Cross-references

| Rule | Primary |
|---|---|
| Template attribute and variants | R-Part_Template-01 to R-Part_Template-04 |
| Allocated, BOM, Used In, Suppliers, Purchase Orders, Return Orders, Transfer Orders, Test Results tab visibility by attribute | R-Detail_View-17 to R-Detail_View-30 |
