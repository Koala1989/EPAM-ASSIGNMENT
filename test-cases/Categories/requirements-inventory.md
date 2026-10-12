# Requirements inventory: Categories

Rules stated in `requirements/docs/` (InvenTree 1.5.6). Built by P03 on 2026-10-10; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare. Risk values are the agent's proposal.

The docs say little about categories: creating, editing, moving and deleting categories, and structural categories, are not described (see index, Not in docs).

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Categories-01 | Parts are arranged in hierarchical categories, used to organise and filter parts by function. | [part-index.md#L15](../../requirements/docs/part-index.md#L15) | H | |
| R-Categories-02 | A category's part list shows every part in that category and in all its sub-categories. | [part-index.md#L31](../../requirements/docs/part-index.md#L31) | H | |
| R-Categories-03 | A category shows the list of its sub-categories. | [part-index.md#L33](../../requirements/docs/part-index.md#L33) | M | |
| R-Categories-04 | The category part list shows name and description, image thumbnail, category and stock level. | [part-index.md#L37-42](../../requirements/docs/part-index.md#L37-L42) | M | |
| R-Categories-05 | The category part list can be filtered by multiple user-configurable filters. | [part-index.md#L44](../../requirements/docs/part-index.md#L44) | M | Which filters exist is not stated. |
| R-Categories-06 | Clicking a part name in the list opens the Part Detail view. | [part-index.md#L46](../../requirements/docs/part-index.md#L46) | M | |
| R-Categories-07 | The part detail page shows the part's categories in the top navigation bar (breadcrumb). | [part-views.md#L19](../../requirements/docs/part-views.md#L19) | L | |

## Cross-references

| Rule | Primary |
|---|---|
| Category-linked parameter templates and default values | R-Part_Params-19, R-Part_Params-20 |
| Parametric tables (filter and sort parts by parameter) | R-Part_Params-21 to R-Part_Params-29 |
| Import must map parts to existing categories (by ID or name) | R-Part-20, R-Part-22 |
| *Import Part* from the category view (supplier plugin) | R-Part-40 |
