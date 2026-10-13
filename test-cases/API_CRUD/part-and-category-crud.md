# Part and category CRUD: CRUD test cases

### API-CRUD-001: Create a part with name, description and category

| Field | Value |
|---|---|
| **Summary** | A user with part create permission can create a part with `POST /api/part/`, and the response returns the new part with the values sent. |
| **Requirement** | R-CRUD-01. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), response `components.schemas.Part`. |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: required `name` plus optional fields with valid values) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes: core CRUD. |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Resistor 10k", "description": "QA API part", "category": <category pk>}` | `201 Created`. Body is valid against `Part`; `name`, `description` and `category` equal the payload; `pk` is an integer. |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. Body is valid against `Part`; `name`, `description` and `category` equal the payload of step 1. |

**Postconditions and cleanup:** one new part in `QA-<suffix> Category`. Cleanup as `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`), then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** only `name` is input-required (index, Schema issues #4).

### API-CRUD-002: Create a part with only the name: IPN and revision default to empty strings

| Field | Value |
|---|---|
| **Summary** | A part created with only `name` is accepted and `IPN` and `revision` default to an empty string. |
| **Requirement** | R-CRUD-12 (also R-CRUD-01). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.IPN` ([L4164](../../requirements/openapi-parts.yaml#L4164)), `components.schemas.Part.revision` ([L4207](../../requirements/openapi-parts.yaml#L4207)). |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: minimum payload), Boundary value analysis (only required fields sent) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth). |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Name Only"}` | `201 Created`. Body is valid against `Part`; `name` equals the payload; `IPN` is `""`; `revision` is `""`. |

**Postconditions and cleanup:** one new part. Cleanup as `admin`: `PATCH` `active: false`, `DELETE /api/part/<pk>/` (`204`).

**Notes:** `revision` is `nullable` in the schema; the check is for the empty string, as the default states.

### API-CRUD-003: A part created without `active` is active

| Field | Value |
|---|---|
| **Summary** | A part created without the `active` field is active in the response and when read back. |
| **Requirement** | R-CRUD-11. Source: [part-index.md#L114-L117](../../requirements/docs/part-index.md#L114). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.active` ([L4112](../../requirements/openapi-parts.yaml#L4112), no `default` declared). |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | State transition (initial state: Active), Equivalence partitioning (field omitted) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Default Active"}` | `201 Created`. `active` is `true`. |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `active` is `true`. |

**Postconditions and cleanup:** one new part. Cleanup as `admin`: `PATCH` `active: false`, `DELETE` (`204`).

**Notes:** the docs state the default; the schema does not declare it.

### API-CRUD-004: Create a part with initial stock

| Field | Value |
|---|---|
| **Summary** | Sending the write-only `initial_stock` with a quantity and location on create adds that stock for the new part. |
| **Requirement** | R-CRUD-13. Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.initial_stock` ([L4349](../../requirements/openapi-parts.yaml#L4349)), `components.schemas.InitialStock` ([L3714](../../requirements/openapi-parts.yaml#L3714)). |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: quantity above zero with a location) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `engineer` (manage parts and stock); Settings: None; Data: stock location `QA-<suffix> Location` created as `admin` with `POST /api/stock/location/`; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Initial Stock", "initial_stock": {"quantity": "10", "location": <location pk>}}` | `201 Created`. Body is valid against `Part`; it has no `initial_stock` key (write-only). |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `total_in_stock` is `10`; `stock_item_count` is `1`. |

**Postconditions and cleanup:** one part with one stock item of 10. Cleanup as `admin`: delete the stock item (`DELETE /api/stock/<pk>/`), `PATCH` the part `active: false`, `DELETE` it, then delete the location.

**Notes:** the stock endpoints are outside the Parts slice and are used for setup and cleanup only.

### API-CRUD-005: Create a part with initial stock quantity zero adds no stock

| Field | Value |
|---|---|
| **Summary** | With `initial_stock.quantity` of `"0"` the part is created and no stock is added. |
| **Requirement** | R-CRUD-13. Schema: `components.schemas.InitialStock.quantity` ([L3718](../../requirements/openapi-parts.yaml#L3718)): "If quantity is zero, no stock is added." |
| **Area** | CRUD |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (quantity = 0, on the limit between "no stock" and "stock added") |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Zero Stock", "initial_stock": {"quantity": "0"}}` | `201 Created`. Body is valid against `Part`. |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `total_in_stock` is not greater than `0` (`0` or `null`); `stock_item_count` is not greater than `0`. |

**Postconditions and cleanup:** one part, no stock. Cleanup as `admin`: `PATCH` `active: false`, `DELETE` (`204`).

**Notes:** `quantity` is a decimal string (`pattern ^-?\d{0,10}(?:\.\d{0,5})?$`). Whether `0` is reported as `0` or `null` is not stated, so both are accepted.

### API-CRUD-006: Create a part by duplicating another part

| Field | Value |
|---|---|
| **Summary** | Sending `duplicate` with the `pk` of an existing part creates a new, separate part and leaves the original unchanged. |
| **Requirement** | R-CRUD-14. Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.duplicate` ([L4343](../../requirements/openapi-parts.yaml#L4343)), `components.schemas.PartDuplicateOptions` ([L4440](../../requirements/openapi-parts.yaml#L4440)). Fields copied: `open-questions.md Q-CRUD-06` (answered). |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: `original` only, copy options at their defaults) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: part `QA-<suffix> Original` created with `POST /api/part/` as `admin` (description `QA original`); Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Copy", "duplicate": {"original": <original pk>}}` | `201 Created`. Body is valid against `Part`; `name` equals `QA-<suffix> Copy`; `pk` differs from the original's; no `duplicate` key in the body (write-only). `description` is `""`: values of fields not sent are not copied from the original. |
| 2 | `GET /api/part/<original pk>/` as `engineer` | None | `200 OK`. `name` is still `QA-<suffix> Original`; `description` is `QA original`. |

**Postconditions and cleanup:** two new parts. Cleanup as `admin`: for each, `PATCH` `active: false`, `DELETE` (`204`).

**Notes:** in 1.5.6 the API sets only the fields sent: no field value of the original (description, category, IPN, keywords, units, flags, stock limits) is copied (Q-CRUD-06, observed 2026-10-13). The `copy_*` options act on related data (image, BOM, notes, tests, parameters), which this case does not exercise. Option defaults per `PartDuplicateOptions`: `copy_image` false, `copy_bom` false, `copy_notes` true, `copy_tests` false, `copy_parameters` true.

### API-CRUD-007: The read-only full_name is returned for a created part

| Field | Value |
|---|---|
| **Summary** | The `full_name` of a part is a read-only string returned on create and read, and a value sent for it is not used as the name. |
| **Requirement** | R-CRUD-16. Schema: `components.schemas.Part.full_name` ([L4152](../../requirements/openapi-parts.yaml#L4152)), `readOnly`. Default format: `open-questions.md Q-CRUD-05` (answered). |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (read-only derived field) |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer`; Settings: `PART_NAME_FORMAT` at its default (see Notes); Data: None; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Full Name", "IPN": "QA-<suffix>-IPN"}` | `201 Created`. `full_name` is `QA-<suffix>-IPN \| QA-<suffix> Full Name`. |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `full_name` equals the value from step 1. |

**Postconditions and cleanup:** one new part. Cleanup as `admin`: `PATCH` `active: false`, `DELETE` (`204`).

**Notes:** In the table, `\|` stands for a literal `|`. The default `PART_NAME_FORMAT` in 1.5.6 is `{{ part.IPN if part.IPN }}{{ ' \| ' if part.IPN }}{{ part.name }}{{ ' \| ' if part.revision }}{{ part.revision if part.revision }}`, so `full_name` is the IPN, a vertical bar, the name, and (with a revision) a vertical bar and the revision; with no IPN it is the name alone (Q-CRUD-05, observed 2026-10-13). Read-only handling of values sent for it is VAL scope (Not in schema #5).

### API-CRUD-008: Read a part by ID

| Field | Value |
|---|---|
| **Summary** | `GET /api/part/{id}/` returns the part with that ID. |
| **Requirement** | R-CRUD-02. Schema: `requirements/openapi-parts.yaml GET /api/part/{id}/` ([L2673](../../requirements/openapi-parts.yaml#L2673)), response `components.schemas.Part`. |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: existing ID) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: part `QA-<suffix> Read Me` (description `QA read`) created with `POST /api/part/` as `admin`; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/<pk>/` as `engineer` | None | `200 OK`. Body is valid against `Part`; `pk` equals the requested ID; `name` is `QA-<suffix> Read Me`; `description` is `QA read`. |

**Postconditions and cleanup:** none beyond the setup part. Cleanup as `admin`: `PATCH` `active: false`, `DELETE` (`204`).

**Notes:** None.

### API-CRUD-009: Read a part with an ID that does not exist

| Field | Value |
|---|---|
| **Summary** | `GET /api/part/{id}/` for a non-existent ID returns `404 Not Found`. |
| **Requirement** | R-CRUD-02. Schema: `requirements/openapi-parts.yaml GET /api/part/{id}/` ([L2673](../../requirements/openapi-parts.yaml#L2673)); only `200` is documented. Not found: `open-questions.md Q-CRUD-01` (answered). |
| **Area** | CRUD |
| **Type** | Negative |
| **Technique** | Error guessing (unknown ID), Equivalence partitioning (invalid class: not found) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: an ID that does not exist: create a part as `admin`, make it inactive, delete it, and reuse its `pk`; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/<deleted pk>/` as `engineer` | None | `404 Not Found`. Body is `{"detail": "No Part matches the given query."}`; no part is returned. |

**Postconditions and cleanup:** none.

**Notes:** 404 Not Found for a part or category that does not exist is the architect's rule (Q-CRUD-01, answered), confirmed on 1.5.6 on 2026-10-13.

### API-CRUD-010: Update a part with PUT

| Field | Value |
|---|---|
| **Summary** | `PUT /api/part/{id}/` with a full body replaces the writable values and returns the updated part. |
| **Requirement** | R-CRUD-03. Schema: `requirements/openapi-parts.yaml PUT /api/part/{id}/` ([L2730](../../requirements/openapi-parts.yaml#L2730)), request and response `components.schemas.Part`. |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: full body) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: part `QA-<suffix> Put Me` created with `POST /api/part/` as `admin` (description `QA before`), category `QA-<suffix> Category` created as `admin`; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PUT /api/part/<pk>/` as `engineer` | `{"name": "QA-<suffix> Put Done", "description": "QA after", "category": <category pk>, "active": true}` | `200 OK`. Body is valid against `Part`; `name`, `description` and `category` equal the payload. |
| 2 | `GET /api/part/<pk>/` as `engineer` | None | `200 OK`. `name`, `description` and `category` equal the step 1 payload. |

**Postconditions and cleanup:** the part is renamed and moved. Cleanup as `admin`: `PATCH` `active: false`, `DELETE` the part (`204`), then the category (`DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}`, `204`).

**Notes:** values of writable fields omitted from a `PUT` are not stated and not asserted.

### API-CRUD-011: Update one field of a part with PATCH

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with one field changes that field only. |
| **Requirement** | R-CRUD-04. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([L2767](../../requirements/openapi-parts.yaml#L2767)), request `components.schemas.PatchedPart`, response `components.schemas.Part`. |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: partial body) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: part `QA-<suffix> Patch Me` (description `QA keep`, IPN `QA-<suffix>-P`) created with `POST /api/part/` as `admin`; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<pk>/` as `engineer` | `{"description": "QA changed"}` | `200 OK`. Body is valid against `Part`; `description` is `QA changed`; `name` is `QA-<suffix> Patch Me`; `IPN` is `QA-<suffix>-P`. |
| 2 | `GET /api/part/<pk>/` as `engineer` | None | `200 OK`. `description` is `QA changed`; `name` and `IPN` are unchanged. |

**Postconditions and cleanup:** description changed. Cleanup as `admin`: `PATCH` `active: false`, `DELETE` (`204`).

**Notes:** None.

### API-CRUD-012: Make a part inactive with PATCH

| Field | Value |
|---|---|
| **Summary** | `PATCH` with `active: false` moves an active part to inactive and the part remains readable. |
| **Requirement** | R-CRUD-04, R-CRUD-11. Source: [part-index.md#L114-L117](../../requirements/docs/part-index.md#L114) ("the part remains in the database"). Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Part.active`. |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | State transition (Active to Inactive) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: active part `QA-<suffix> Deactivate` created with `POST /api/part/` as `admin`; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<pk>/` as `engineer` | `{"active": false}` | `200 OK`. Body is valid against `Part`; `active` is `false`. |
| 2 | `GET /api/part/<pk>/` as `engineer` | None | `200 OK`. `active` is `false`; `name` is unchanged. |

**Postconditions and cleanup:** inactive part. Cleanup as `admin`: `DELETE /api/part/<pk>/` (`204`).

**Notes:** which actions are blocked for an inactive part is not documented (index, Not in docs #3) and is not tested here.

### API-CRUD-013: Delete an inactive part

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/{id}/` on an inactive part removes it, and it can no longer be read. |
| **Requirement** | R-CRUD-05. Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/` ([L2803](../../requirements/openapi-parts.yaml#L2803)). Not found: `open-questions.md Q-CRUD-01` (answered). |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | State transition (Inactive to deleted) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: part `QA-<suffix> Delete Me` created with `POST /api/part/` as `admin` and made inactive with `PATCH` `{"active": false}`; Pre-steps: get `admin`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<pk>/` as `admin` | None | `204 No Content`. The body is empty. |
| 2 | `GET /api/part/<pk>/` as `admin` | None | `404 Not Found`. Body is `{"detail": "No Part matches the given query."}`. |
| 3 | `GET /api/part/` as `admin` | `search=QA-<suffix> Delete Me` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** none, the part is deleted.

**Notes:** `admin` is used because the roles needed to delete are not stated (Schema issues #1). 404 Not Found for a part or category that does not exist is the architect's rule (Q-CRUD-01, answered), confirmed on 1.5.6 on 2026-10-13.

### API-CRUD-014: Delete an active part

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/{id}/` on a part that is still active. |
| **Requirement** | R-CRUD-05. Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/` ([L2803](../../requirements/openapi-parts.yaml#L2803)). Source: [part-index.md#L116](../../requirements/docs/part-index.md#L116) (inactive recommended "rather than deleting"). Refusal: `open-questions.md Q-CRUD-02` (answered). |
| **Area** | CRUD |
| **Type** | Negative |
| **Technique** | State transition (blocked or allowed: Active to deleted), What-if business scenario (user deletes instead of deactivating) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: active part `QA-<suffix> Active Delete` created with `POST /api/part/` as `admin`; Pre-steps: get `admin`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<pk>/` as `admin` | None | `400 Bad Request`. Body is `{"non_field_errors": ["Cannot delete this part as it is still active"]}`. |
| 2 | `GET /api/part/<pk>/` as `admin` | None | `200 OK`. `active` is `true`: the part was not deleted. |

**Postconditions and cleanup:** the active part remains. Cleanup as `admin`: `PATCH` `active: false`, `DELETE` (`204`).

**Notes:** an active part cannot be deleted in 1.5.6; it must be made inactive first (Q-CRUD-02, observed 2026-10-13). The schema documents only `204`.

### API-CRUD-015: Bulk PATCH on the parts list

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/` with an `items` list of part IDs updates exactly those parts and no others. |
| **Requirement** | R-CRUD-17. Schema: `requirements/openapi-parts.yaml PATCH /api/part/` ([L812](../../requirements/openapi-parts.yaml#L812)), request `components.schemas.PatchedPart`; the 1.5.6 response is `{"success", "items"}`, not `Part` (findings F-10). Selection: `open-questions.md Q-CRUD-04` (answered). |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: bulk update with `items`) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: two parts `QA-<suffix> Bulk A` and `QA-<suffix> Bulk B` and one control part `QA-<suffix> Bulk Control`, all created as `admin` with description `QA before`; Pre-steps: get `admin`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/` as `admin` | `{"items": [<Bulk A pk>, <Bulk B pk>], "description": "QA bulk"}` | `200 OK`. `success` is `Updated multiple items`; `items` has 2 entries, the parts Bulk A and Bulk B by `pk`, each with `description` `QA bulk`. |
| 2 | `GET /api/part/<Bulk A pk>/` as `admin` | None | `200 OK`. `description` is `QA bulk`. |
| 3 | `GET /api/part/<Bulk B pk>/` as `admin` | None | `200 OK`. `description` is `QA bulk`. |
| 4 | `GET /api/part/<Bulk Control pk>/` as `admin` | None | `200 OK`. `description` is `QA before`: the control part was not updated. |

**Postconditions and cleanup:** three parts. Cleanup as `admin`: for each, `PATCH` `active: false`, `DELETE` (`204`).

**Notes:** records are selected only by `items` (a list of primary keys) in the body; a body without `items` returns `400` (Q-CRUD-04, observed 2026-10-13). Never send `?all=true`: it updates every record, including ones this run did not create.

**Duplicate check:** 51 · Review · matches: [API-CRUD-022](part-and-category-crud.md) (51)

**Duplicate judgement:** Keep · Targets a different endpoint and resource (`PATCH /api/part/` with `PatchedPart` on parts, inactive-then-delete cleanup) than API-CRUD-022 (`PATCH /api/part/category/` with `PatchedCategory` on categories), so a bulk-update defect in one list would not be caught by the other · duplicate-judge, 2026-10-13

### API-CRUD-016: Create a category

| Field | Value |
|---|---|
| **Summary** | A user with category create permission can create a category with `POST /api/part/category/`, and the response returns it with the values sent. |
| **Requirement** | R-CRUD-06. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), response `components.schemas.Category`. |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: `name` plus optional fields) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Category", "description": "QA API category", "structural": false}` | `201 Created`. Body is valid against `Category`; `name`, `description` and `structural` equal the payload; `parent` is `null`; `pk` is an integer. |
| 2 | `GET /api/part/category/<pk from step 1>/` as `engineer` | None | `200 OK`. `name` and `description` equal the payload. |

**Postconditions and cleanup:** one new category. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** `engineer` is assumed to hold the category add role; if the call is refused, report it under SEC rather than changing the user.

### API-CRUD-017: Read a category by ID

| Field | Value |
|---|---|
| **Summary** | `GET /api/part/category/{id}/` returns the category with that ID. |
| **Requirement** | R-CRUD-07. Schema: `requirements/openapi-parts.yaml GET /api/part/category/{id}/` ([L1303](../../requirements/openapi-parts.yaml#L1303)), response `components.schemas.Category`. |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: existing ID) |
| **Priority** | P2 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Read Category` (description `QA read`) created with `POST /api/part/category/` as `admin`; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/<pk>/` as `engineer` | None | `200 OK`. Body is valid against `Category`; `pk` equals the requested ID; `name` is `QA-<suffix> Read Category`; `description` is `QA read`; `part_count` is `0`. |

**Postconditions and cleanup:** cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** None.

### API-CRUD-018: Read a category with an ID that does not exist

| Field | Value |
|---|---|
| **Summary** | `GET /api/part/category/{id}/` for a non-existent ID returns `404 Not Found`. |
| **Requirement** | R-CRUD-07. Schema: `requirements/openapi-parts.yaml GET /api/part/category/{id}/` ([L1303](../../requirements/openapi-parts.yaml#L1303)); only `200` is documented. Not found: `open-questions.md Q-CRUD-01` (answered). |
| **Area** | CRUD |
| **Type** | Negative |
| **Technique** | Error guessing (unknown ID), Equivalence partitioning (invalid class: not found) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: an ID that does not exist: create a category as `admin`, delete it, and reuse its `pk`; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/<deleted pk>/` as `engineer` | None | `404 Not Found`. Body is `{"detail": "No PartCategory matches the given query."}`; no category is returned. |

**Postconditions and cleanup:** none.

**Notes:** 404 Not Found for a part or category that does not exist is the architect's rule (Q-CRUD-01, answered), confirmed on 1.5.6 on 2026-10-13.

### API-CRUD-019: Update a category with PUT

| Field | Value |
|---|---|
| **Summary** | `PUT /api/part/category/{id}/` with a full body updates the category and returns it. |
| **Requirement** | R-CRUD-08. Schema: `requirements/openapi-parts.yaml PUT /api/part/category/{id}/` ([L1333](../../requirements/openapi-parts.yaml#L1333)), request and response `components.schemas.Category`. |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: full body) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Put Category` (description `QA before`) created with `POST /api/part/category/` as `admin`; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PUT /api/part/category/<pk>/` as `engineer` | `{"name": "QA-<suffix> Put Category Done", "description": "QA after", "parent": null, "structural": false}` | `200 OK`. Body is valid against `Category`; `name`, `description`, `parent` and `structural` equal the payload. |
| 2 | `GET /api/part/category/<pk>/` as `engineer` | None | `200 OK`. `name` and `description` equal the step 1 payload. |

**Postconditions and cleanup:** cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** None.

### API-CRUD-020: Update one field of a category with PATCH

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` with one field changes that field only. |
| **Requirement** | R-CRUD-09. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/` ([L1370](../../requirements/openapi-parts.yaml#L1370)), request `components.schemas.PatchedCategory`, response `components.schemas.Category`. |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: partial body) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Patch Category` (description `QA keep`) created with `POST /api/part/category/` as `admin`; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/<pk>/` as `engineer` | `{"description": "QA changed"}` | `200 OK`. Body is valid against `Category`; `description` is `QA changed`; `name` is `QA-<suffix> Patch Category`. |
| 2 | `GET /api/part/category/<pk>/` as `engineer` | None | `200 OK`. `description` is `QA changed`; `name` is unchanged. |

**Postconditions and cleanup:** cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** None.

### API-CRUD-021: Delete an empty category

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/category/{id}/` on a category with no parts and no child categories removes it. |
| **Requirement** | R-CRUD-10. Schema: `requirements/openapi-parts.yaml DELETE /api/part/category/{id}/` ([L1406](../../requirements/openapi-parts.yaml#L1406)). Not found: `open-questions.md Q-CRUD-01` (answered). |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: empty category) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: category `QA-<suffix> Delete Category` created with `POST /api/part/category/` as `admin`; Pre-steps: get `admin`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/category/<pk>/` as `admin` | `{"delete_parts": false, "delete_child_categories": false}` | `204 No Content`. The body is empty. |
| 2 | `GET /api/part/category/<pk>/` as `admin` | None | `404 Not Found`. Body is `{"detail": "No PartCategory matches the given query."}`. |

**Postconditions and cleanup:** none, the category is deleted.

**Notes:** `admin` is used because the roles needed to delete are not stated (Schema issues #1). 404 Not Found for a part or category that does not exist is the architect's rule (Q-CRUD-01, answered), confirmed on 1.5.6 on 2026-10-13. Both flags are required in 1.5.6: without a body the call returns `400` (Q-CRUD-03).

### API-CRUD-022: Bulk PATCH on the categories list

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/` with an `items` list of category IDs updates exactly those categories and no others. |
| **Requirement** | R-CRUD-17. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/` ([L1017](../../requirements/openapi-parts.yaml#L1017)), request `components.schemas.PatchedCategory`; the 1.5.6 response is `{"success", "items"}`, not `Category` (findings F-10). Selection: `open-questions.md Q-CRUD-04` (answered). |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: bulk update with `items`) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: two categories `QA-<suffix> Bulk Cat A` and `QA-<suffix> Bulk Cat B` and one control category `QA-<suffix> Bulk Cat Control`, all created as `admin` with description `QA before`; Pre-steps: get `admin`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/` as `admin` | `{"items": [<Bulk Cat A pk>, <Bulk Cat B pk>], "description": "QA bulk"}` | `200 OK`. `success` is `Updated multiple items`; `items` has 2 entries, each valid against `Category`, the categories Bulk Cat A and Bulk Cat B by `pk`, each with `description` `QA bulk`. |
| 2 | `GET /api/part/category/<Bulk Cat A pk>/` as `admin` | None | `200 OK`. `description` is `QA bulk`. |
| 3 | `GET /api/part/category/<Bulk Cat B pk>/` as `admin` | None | `200 OK`. `description` is `QA bulk`. |
| 4 | `GET /api/part/category/<control pk>/` as `admin` | None | `200 OK`. `description` is `QA before`: the control category was not updated. |

**Postconditions and cleanup:** three categories. Cleanup as `admin`: `DELETE` each with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** records are selected only by `items` (a list of primary keys) in the body; a body without `items` returns `400` (Q-CRUD-04, observed 2026-10-13). Never send `?all=true`: it updates every record, including ones this run did not create.

**Duplicate check:** 51 · Review · matches: [API-CRUD-015](part-and-category-crud.md) (51)

**Duplicate judgement:** Keep · Targets the categories list endpoint (`PATCH /api/part/category/`, `PatchedCategory`) rather than the parts list endpoint of API-CRUD-015, a separate resource and schema under R-CRUD-17 · duplicate-judge, 2026-10-13

### API-CRUD-023: Delete a part with an ID that does not exist

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/{id}/` for a non-existent ID returns `404 Not Found` and deletes nothing. |
| **Requirement** | R-CRUD-05. Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/` ([L2803](../../requirements/openapi-parts.yaml#L2803)). Not found: `open-questions.md Q-CRUD-01` (answered). |
| **Area** | CRUD |
| **Type** | Negative |
| **Technique** | Error guessing (unknown ID), Equivalence partitioning (invalid class: not found) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: an ID that does not exist: create a part as `admin`, make it inactive, delete it, and reuse its `pk`; Pre-steps: get `admin`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<deleted pk>/` as `admin` | None | `404 Not Found`. Body is `{"detail": "No Part matches the given query."}`. |

**Postconditions and cleanup:** none.

**Notes:** 404 Not Found for a part or category that does not exist is the architect's rule (Q-CRUD-01, answered), confirmed on 1.5.6 on 2026-10-13.

### API-CRUD-024: Delete a category with an ID that does not exist

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/category/{id}/` for a non-existent ID returns `404 Not Found` and deletes nothing. |
| **Requirement** | R-CRUD-10. Schema: `requirements/openapi-parts.yaml DELETE /api/part/category/{id}/` ([L1406](../../requirements/openapi-parts.yaml#L1406)). Not found: `open-questions.md Q-CRUD-01` (answered). |
| **Area** | CRUD |
| **Type** | Negative |
| **Technique** | Error guessing (unknown ID), Equivalence partitioning (invalid class: not found) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: an ID that does not exist: create a category as `admin`, delete it, and reuse its `pk`; Pre-steps: get `admin`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/category/<deleted pk>/` as `admin` | `{"delete_parts": false, "delete_child_categories": false}` | `404 Not Found`. Body is `{"detail": "No PartCategory matches the given query."}`. |

**Postconditions and cleanup:** none.

**Notes:** 404 Not Found for a part or category that does not exist is the architect's rule (Q-CRUD-01, answered), confirmed on 1.5.6 on 2026-10-13. The two flags are sent because 1.5.6 requires them on every category delete: without a body the call returns `400` before the lookup (observed 2026-10-13, not in the schema).
