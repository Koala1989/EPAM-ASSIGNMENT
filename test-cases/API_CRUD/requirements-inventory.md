# Requirements inventory: CRUD (create, read, update, delete)

Rules stated in `requirements/openapi-parts.yaml` (InvenTree 1.5.6, API 530), plus `requirements/docs/` where cited. Built on 2026-10-13 from the schema slice; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare. Risk values are the agent's proposal. Expected error status codes are not in the schema (see the index, Not in schema #1).

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-CRUD-01 | `POST /api/part/` creates a part and returns `201` with the new part as a `Part` body. | [openapi-parts.yaml#L747](../../requirements/openapi-parts.yaml#L747) | H | Body accepted as JSON, form-urlencoded or multipart (R-VAL-17). |
| R-CRUD-02 | `GET /api/part/{id}/` returns one part: `200`, `Part` body. | [openapi-parts.yaml#L2673](../../requirements/openapi-parts.yaml#L2673) | H | Response for an unknown `id` not stated (Not in schema #1). |
| R-CRUD-03 | `PUT /api/part/{id}/` updates a part with a full `Part` body: `200`, `Part` body. | [openapi-parts.yaml#L2730](../../requirements/openapi-parts.yaml#L2730) | M | |
| R-CRUD-04 | `PATCH /api/part/{id}/` updates only the fields sent (`PatchedPart`, no required fields): `200`, `Part` body. | [openapi-parts.yaml#L2767](../../requirements/openapi-parts.yaml#L2767) | H | |
| R-CRUD-05 | `DELETE /api/part/{id}/` deletes a part: `204`. | [openapi-parts.yaml#L2803](../../requirements/openapi-parts.yaml#L2803) | H | Whether an active part can be deleted is not stated (Not in schema #4). Locked parts: R-REL-11. |
| R-CRUD-06 | `POST /api/part/category/` creates a category: `201`, `Category` body. | [openapi-parts.yaml#L947](../../requirements/openapi-parts.yaml#L947) | H | |
| R-CRUD-07 | `GET /api/part/category/{id}/` returns one category: `200`, `Category` body. | [openapi-parts.yaml#L1303](../../requirements/openapi-parts.yaml#L1303) | M | |
| R-CRUD-08 | `PUT /api/part/category/{id}/` updates a category with a full `Category` body: `200`. | [openapi-parts.yaml#L1333](../../requirements/openapi-parts.yaml#L1333) | M | |
| R-CRUD-09 | `PATCH /api/part/category/{id}/` updates only the fields sent (`PatchedCategory`, no required fields): `200`. | [openapi-parts.yaml#L1370](../../requirements/openapi-parts.yaml#L1370) | M | |
| R-CRUD-10 | `DELETE /api/part/category/{id}/` deletes a category: `204`. | [openapi-parts.yaml#L1406](../../requirements/openapi-parts.yaml#L1406) | H | What happens to its parts and child categories is not stated (Not in schema #3). |
| R-CRUD-11 | A new part is active by default. | [part-index.md#L116](../../requirements/docs/part-index.md#L116) | M | The schema gives no `default` for `active` ([openapi-parts.yaml#L4112](../../requirements/openapi-parts.yaml#L4112)). |
| R-CRUD-12 | `IPN` and `revision` default to an empty string when not sent. | [openapi-parts.yaml#L4164](../../requirements/openapi-parts.yaml#L4164), [openapi-parts.yaml#L4207](../../requirements/openapi-parts.yaml#L4207) | L | |
| R-CRUD-13 | `initial_stock` (write-only) on create adds an initial stock quantity for the new part; `quantity` is required, `location` optional. | [openapi-parts.yaml#L4349](../../requirements/openapi-parts.yaml#L4349), [openapi-parts.yaml#L3714](../../requirements/openapi-parts.yaml#L3714) | M | Cross-checks the UI rule R-Part-08. |
| R-CRUD-14 | `duplicate` (write-only) on create copies initial data from another part. | [openapi-parts.yaml#L4343](../../requirements/openapi-parts.yaml#L4343) | L | What is copied is in `PartDuplicateOptions`. |
| R-CRUD-15 | `copy_category_parameters` (write-only, default `true`) copies the category's parameter templates to the new part. | [openapi-parts.yaml#L4360](../../requirements/openapi-parts.yaml#L4360) | L | Parameter behaviour: Part_Params. |
| R-CRUD-16 | `full_name` (read-only) is formatted from the part according to the `PART_NAME_FORMAT` setting. | [openapi-parts.yaml#L4152](../../requirements/openapi-parts.yaml#L4152) | L | Format and default not stated. |
| R-CRUD-17 | `PUT` and `PATCH` on `/api/part/` and `/api/part/category/` are bulk updates: `200`. | [openapi-parts.yaml#L778](../../requirements/openapi-parts.yaml#L778), [openapi-parts.yaml#L812](../../requirements/openapi-parts.yaml#L812), [openapi-parts.yaml#L983](../../requirements/openapi-parts.yaml#L983), [openapi-parts.yaml#L1017](../../requirements/openapi-parts.yaml#L1017) | L | How the records to update are chosen is not stated (Not in schema #6). |

## Cross-references

| Rule | Primary |
|---|---|
| Listing parts and categories (pagination, filters, search) | R-LST-01, R-LST-14 |
| Required fields and limits on create and update | R-VAL-01, R-VAL-13 |
| Supplier information on create (`initial_supplier`) | R-REL-09 |
| Who may create, change, view and delete | R-SEC-03 to R-SEC-07 |
