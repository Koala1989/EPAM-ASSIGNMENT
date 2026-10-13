# Requirements inventory: REL (relational integrity)

Rules stated in `requirements/openapi-parts.yaml` (InvenTree 1.5.6, API 530), plus `requirements/docs/` where cited. Built on 2026-10-13 from the schema slice; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare. Risk values are the agent's proposal. Expected error status codes are not in the schema (see the index, Not in schema #1).

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-REL-01 | Part `category` references a category by ID and is nullable: a part can have no category. | [openapi-parts.yaml#L4122](../../requirements/openapi-parts.yaml#L4122) | H | Response to an ID that does not exist not stated. |
| R-REL-02 | Parts may not be assigned directly to a structural category, but may be assigned to its child categories. | [openapi-parts.yaml#L3560](../../requirements/openapi-parts.yaml#L3560) | H | |
| R-REL-03 | Part `default_location` references a stock location (where the part is normally stored); nullable. | [openapi-parts.yaml#L4144](../../requirements/openapi-parts.yaml#L4144) | M | |
| R-REL-04 | Category `default_location` is the default location for parts in that category. | [openapi-parts.yaml#L3525](../../requirements/openapi-parts.yaml#L3525) | M | How it applies to parts is not stated; see R-REL-05. |
| R-REL-05 | Part responses include `category_default_location` (read-only). | [openapi-parts.yaml#L4294](../../requirements/openapi-parts.yaml#L4294) | L | Meaning not described; presumably the category's default location. Confirm before writing cases. |
| R-REL-06 | Category `parent` references the parent category; nullable (a top-level category). | [openapi-parts.yaml#L3537](../../requirements/openapi-parts.yaml#L3537) | H | A circular parent (a category under its own child) is not stated. |
| R-REL-07 | Category `level` and `pathstring` are read-only and derived from the hierarchy. | [openapi-parts.yaml#L3534](../../requirements/openapi-parts.yaml#L3534), [openapi-parts.yaml#L3551](../../requirements/openapi-parts.yaml#L3551) | M | Exact format of `pathstring` not stated. |
| R-REL-08 | `POST /api/company/part/` creates a supplier part linking a part to a supplier; `part`, `supplier` and `SKU` are required: `201`. | [openapi-parts.yaml#L185](../../requirements/openapi-parts.yaml#L185), [openapi-parts.yaml#L6029](../../requirements/openapi-parts.yaml#L6029), [openapi-parts.yaml#L6037](../../requirements/openapi-parts.yaml#L6037), [openapi-parts.yaml#L6033](../../requirements/openapi-parts.yaml#L6033), [openapi-parts.yaml#L6044](../../requirements/openapi-parts.yaml#L6044) | H | Whether the part must be purchaseable is not stated. |
| R-REL-09 | `initial_supplier` on part create adds supplier and manufacturer information (`supplier`, `sku`, `manufacturer`, `mpn`) for the new part. | [openapi-parts.yaml#L4354](../../requirements/openapi-parts.yaml#L4354), [openapi-parts.yaml#L3731](../../requirements/openapi-parts.yaml#L3731) | M | Which of its fields are required is not stated. Cross-checks the UI rule R-Part-09. |
| R-REL-10 | Part `variant_of` and `revision_of` reference other parts by ID; both nullable. | [openapi-parts.yaml#L4242](../../requirements/openapi-parts.yaml#L4242), [openapi-parts.yaml#L4212](../../requirements/openapi-parts.yaml#L4212) | M | Restrictions on these links: Part_Template and REV. |
| R-REL-11 | A locked part cannot be edited or deleted; when `PART_ENABLE_LOCKING` is disabled, the locked state is ignored. | [openapi-parts.yaml#L4185](../../requirements/openapi-parts.yaml#L4185), [part-index.md#L108](../../requirements/docs/part-index.md#L108), [part-index.md#L112](../../requirements/docs/part-index.md#L112) | H | Setting default not stated. Locking itself: ATT. |

## Cross-references

| Rule | Primary |
|---|---|
| A revision cannot reference itself; template parts cannot have revisions | REV inventory |
| Variant and template relationships | Part_Template inventory |
| Locked and active states in the UI | ATT inventory |
