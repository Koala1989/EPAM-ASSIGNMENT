# Requirements inventory: VAL (field validation)

Rules stated in `requirements/openapi-parts.yaml` (InvenTree 1.5.6, API 530), plus `requirements/docs/` where cited. Built on 2026-10-13 from the schema slice; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare. Risk values are the agent's proposal. Expected error status codes are not in the schema (see the index, Not in schema #1). A field is required on input only if it is in the schema's `required` list **and** not `readOnly` (schema issue #4).

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-VAL-01 | Part `name` is required on create; string, max 100 characters. | [openapi-parts.yaml#L4196](../../requirements/openapi-parts.yaml#L4196), [openapi-parts.yaml#L4365](../../requirements/openapi-parts.yaml#L4365) | H | Uniqueness not stated (Not in schema #2). |
| R-VAL-02 | Part `description`: optional string, max 250. | [openapi-parts.yaml#L4148](../../requirements/openapi-parts.yaml#L4148) | M | |
| R-VAL-03 | Part `IPN`: optional string, max 100, default `''`. | [openapi-parts.yaml#L4164](../../requirements/openapi-parts.yaml#L4164) | M | |
| R-VAL-04 | Part `keywords`: nullable string, max 250. | [openapi-parts.yaml#L4171](../../requirements/openapi-parts.yaml#L4171) | L | |
| R-VAL-05 | Part `link`: nullable; a URI of at most 2000 characters, or an empty string. | [openapi-parts.yaml#L4176](../../requirements/openapi-parts.yaml#L4176) | M | The UI found an invalid URL rejected with "Enter a valid URL." (R-Part-17). |
| R-VAL-06 | Part `units`: nullable string, max 20. | [openapi-parts.yaml#L4237](../../requirements/openapi-parts.yaml#L4237) | L | Which unit strings are valid: Unit_measure. |
| R-VAL-07 | Part `revision`: nullable string, max 100. | [openapi-parts.yaml#L4207](../../requirements/openapi-parts.yaml#L4207) | L | Revision rules: REV. |
| R-VAL-08 | Part `default_expiry`: integer from 0 to 2147483647 (days). | [openapi-parts.yaml#L4139](../../requirements/openapi-parts.yaml#L4139) | M | |
| R-VAL-09 | Part `minimum_stock` and `maximum_stock`: numbers, default 0. | [openapi-parts.yaml#L4188](../../requirements/openapi-parts.yaml#L4188) | L | Negative values, and minimum above maximum, not stated. |
| R-VAL-10 | Each field must match its schema type: integer IDs for `category`, `default_location`, `variant_of`, `revision_of`, `responsible`; booleans for the attribute flags. | [openapi-parts.yaml#L4122](../../requirements/openapi-parts.yaml#L4122), [openapi-parts.yaml#L4112](../../requirements/openapi-parts.yaml#L4112) | M | |
| R-VAL-11 | Read-only Part fields (`pk`, `full_name`, `barcode_hash`, `creation_date`, `category_name`, `starred`, `thumbnail`, stock and pricing figures) are returned, not set by the client. | [openapi-parts.yaml#L4200](../../requirements/openapi-parts.yaml#L4200), [openapi-parts.yaml#L4152](../../requirements/openapi-parts.yaml#L4152), [openapi-parts.yaml#L4118](../../requirements/openapi-parts.yaml#L4118), [openapi-parts.yaml#L4131](../../requirements/openapi-parts.yaml#L4131) | M | Whether values sent for them are ignored or rejected is not stated (Not in schema #5). |
| R-VAL-12 | Write-only Part fields (`existing_image`, `duplicate`, `initial_stock`, `initial_supplier`, `copy_category_parameters`) are accepted on input and never returned. | [openapi-parts.yaml#L4160](../../requirements/openapi-parts.yaml#L4160), [openapi-parts.yaml#L4343](../../requirements/openapi-parts.yaml#L4343), [openapi-parts.yaml#L4349](../../requirements/openapi-parts.yaml#L4349), [openapi-parts.yaml#L4354](../../requirements/openapi-parts.yaml#L4354), [openapi-parts.yaml#L4360](../../requirements/openapi-parts.yaml#L4360) | L | |
| R-VAL-13 | Category `name` is required on create; string, max 100. | [openapi-parts.yaml#L3517](../../requirements/openapi-parts.yaml#L3517), [openapi-parts.yaml#L3572](../../requirements/openapi-parts.yaml#L3572) | H | Uniqueness among sibling categories not stated. |
| R-VAL-14 | Category `description` max 250; `default_keywords` nullable, max 250; `icon` nullable, max 100. | [openapi-parts.yaml#L3521](../../requirements/openapi-parts.yaml#L3521), [openapi-parts.yaml#L3529](../../requirements/openapi-parts.yaml#L3529), [openapi-parts.yaml#L3563](../../requirements/openapi-parts.yaml#L3563) | L | |
| R-VAL-15 | Read-only Category fields: `pk`, `level`, `pathstring`, `part_count`, `subcategories`, `starred`. | [openapi-parts.yaml#L3534](../../requirements/openapi-parts.yaml#L3534), [openapi-parts.yaml#L3551](../../requirements/openapi-parts.yaml#L3551), [openapi-parts.yaml#L3542](../../requirements/openapi-parts.yaml#L3542) | L | |
| R-VAL-16 | `PATCH` bodies (`PatchedPart`, `PatchedCategory`) have no required fields. | [openapi-parts.yaml#L2767](../../requirements/openapi-parts.yaml#L2767), [openapi-parts.yaml#L1370](../../requirements/openapi-parts.yaml#L1370) | M | |
| R-VAL-17 | Create and update bodies are accepted as `application/json`, `application/x-www-form-urlencoded` and `multipart/form-data`. | [openapi-parts.yaml#L747](../../requirements/openapi-parts.yaml#L747) | L | |
| R-VAL-18 | `initial_stock.quantity` is required when `initial_stock` is sent. | [openapi-parts.yaml#L3714](../../requirements/openapi-parts.yaml#L3714) | M | Lower limit (0, negative) not stated. |

## Cross-references

| Rule | Primary |
|---|---|
| A structural category rejects direct part assignment | R-REL-02 |
| A supplier part needs `part`, `supplier` and `SKU` | R-REL-08 |
