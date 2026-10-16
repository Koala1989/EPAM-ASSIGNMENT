# Part and category CRUD: REL test cases

### API-REL-001: Delete a category that contains a part

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/category/{id}/` on a category that contains a part: with both flags `false`, the category is deleted and the part is kept without a category. |
| **Requirement** | R-CRUD-10 (index, Not in schema #3). Schema: `requirements/openapi-parts.yaml DELETE /api/part/category/{id}/` ([L1406](../../requirements/openapi-parts.yaml#L1406)). Delete behaviour: `open-question_REL.md Q-CRUD-03` (answered). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | What-if business scenario (category removed while parts are assigned), State transition (category with parts to deleted) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: category `QA-<suffix> Category` and part `QA-<suffix> Child Part` in it, created as `admin`; Pre-steps: get `admin`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/category/<category pk>/` as `admin` | `{"delete_parts": false, "delete_child_categories": false}` | `204 No Content`. The body is empty. |
| 2 | `GET /api/part/category/<category pk>/` as `admin` | None | `404 Not Found`. Body is `{"detail": "No PartCategory matches the given query."}`. |
| 3 | `GET /api/part/<part pk>/` as `admin` | None | `200 OK`. The part is kept; `category` is `null` (the deleted category was top-level). |

**Postconditions and cleanup:** the category is deleted; the part remains with no category. As `admin`: `PATCH` the part `active: false`, `DELETE` it (`204`).

**Notes:** the part is created in the category, so no other records are affected. Both flags are required in 1.5.6: without a body the call returns `400` and nothing is deleted. With `delete_parts` `true` the part would be deleted instead (Q-CRUD-03, observed 2026-10-13).

**Duplicate check:** 71 · Review · matches: [API-REL-002](part-and-category-crud.md) (71)

**Duplicate judgement:** Keep · Different starting state: the category holds a part (the outcome checked is the part's survival and its `category` value), whereas API-REL-002 holds a child category (the outcome checked is the child's survival and its `parent` value) · duplicate-judge, 2026-10-13

### API-REL-002: Delete a category that has a child category

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/category/{id}/` on a parent category: with both flags `false`, the parent is deleted and its child is kept and moved up. |
| **Requirement** | R-CRUD-10 (index, Not in schema #3). Schema: `requirements/openapi-parts.yaml DELETE /api/part/category/{id}/` ([L1406](../../requirements/openapi-parts.yaml#L1406)), `components.schemas.Category.parent`. Delete behaviour: `open-question_REL.md Q-CRUD-03` (answered). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | What-if business scenario (parent removed while a child exists), State transition (category with children to deleted) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: category `QA-<suffix> Parent`, and `QA-<suffix> Child` with `parent` set to the parent's `pk`, created as `admin`; Pre-steps: get `admin`'s token. |
| **Automation** | Yes |
| **Review** | Approved · 2026-10-13 · bulk approval by the architect; expected results not yet executed |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/<parent pk>/` as `admin` | None | `200 OK`. `subcategories` is `1`. |
| 2 | `DELETE /api/part/category/<parent pk>/` as `admin` | `{"delete_parts": false, "delete_child_categories": false}` | `204 No Content`. The body is empty. |
| 3 | `GET /api/part/category/<parent pk>/` as `admin` | None | `404 Not Found`. Body is `{"detail": "No PartCategory matches the given query."}`. |
| 4 | `GET /api/part/category/<child pk>/` as `admin` | None | `200 OK`. The child is kept; `parent` is `null` and `level` is `0` (the deleted parent was top-level). |

**Postconditions and cleanup:** the parent is deleted; the child remains as a top-level category. As `admin`: `DELETE` the child with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** both flags are required in 1.5.6; with `delete_child_categories` `true` the child would be deleted instead (Q-CRUD-03, observed 2026-10-13).

**Duplicate check:** 71 · Review · matches: [API-REL-001](part-and-category-crud.md) (71)

**Duplicate judgement:** Keep · Different starting state: the category has a child category (it checks `subcategories` and the child's `parent` after delete), whereas API-REL-001 has a part in the category (it checks the part's `category`) · duplicate-judge, 2026-10-13
