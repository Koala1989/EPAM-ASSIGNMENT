# Relationships: REL test cases


### API-REL-003: Move a part to another category with PATCH

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with a different `category` ID moves the part: the response and later reads show the new category. |
| **Requirement** | R-REL-01 ([openapi-parts.yaml#L4122](../../requirements/openapi-parts.yaml#L4122)). Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Part.category`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | State transition (part in category A to category B), Equivalence partitioning (valid class: existing category ID) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: categories `QA-<suffix> Category A` and `QA-<suffix> Category B` (not structural) created with `POST /api/part/category/`; part `QA-<suffix> Part` created in category A with `POST /api/part/`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<part pk>/` as `engineer` | `{"category": <category B pk>}` | `200 OK`. Body is valid against `Part`; `category` equals the category B `pk`; `category_name` is `QA-<suffix> Category B`. |
| 2 | `GET /api/part/` as `engineer` | `category=<category B pk>`, `limit=10` | `200 OK`. The list contains exactly one part, with the `pk` of `QA-<suffix> Part`. |
| 3 | `GET /api/part/` as `engineer` | `category=<category A pk>`, `limit=10` | `200 OK`. `count` is `0`: the part is no longer in category A. |

**Postconditions and cleanup:** One part in category B. As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`), then `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for both categories.

**Notes:** None.

**Duplicate check:** 56 · Review · matches: [API-REL-004](relationships.md) (56)

**Duplicate judgement:** Keep · Differs from API-REL-004 in class and outcome: an existing category ID (part moved to category B) vs `null` (part left uncategorised). · test-case-reviewer, 2026-10-14

### API-REL-004: Remove a part from its category by setting `category` to null

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with `category` `null` is accepted (the field is nullable) and the part has no category afterwards. |
| **Requirement** | R-REL-01 ([openapi-parts.yaml#L4122](../../requirements/openapi-parts.yaml#L4122)). Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Part.category` (`nullable: true`). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: null), State transition (categorised to uncategorised) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Category` (not structural) created with `POST /api/part/category/`; part `QA-<suffix> Part` created in it with `POST /api/part/`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<part pk>/` as `engineer` | `{"category": null}` | `200 OK`. `category` is `null`. |
| 2 | `GET /api/part/<part pk>/` as `engineer` | None | `200 OK`. `category` is `null`; the part is kept. |

**Postconditions and cleanup:** One part with no category. As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`), then `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** The response of an uncategorised part omits `category_name` (test-cases/findings.md#F-11), so do not assert it or a strict `Part` schema match here.

**Duplicate check:** 56 · Review · matches: [API-REL-003](relationships.md) (56), [API-REL-012](relationships.md) (56), [API-REL-044](relationships.md) (54)

**Duplicate judgement:** Keep · Differs from API-REL-003 in class (`null` vs an existing ID), and from API-REL-012 and API-REL-044 in field and rule (`category`, R-REL-01 vs `default_location`, R-REL-03 and `variant_of`, R-REL-10). · test-case-reviewer, 2026-10-14

### API-REL-005: Create a part with a `category` ID that does not exist

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a `category` that refers to no category is not accepted and no part is created. |
| **Requirement** | R-REL-01 ([openapi-parts.yaml#L4122](../../requirements/openapi-parts.yaml#L4122)), response to a missing ID not stated. Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.category`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: ID not found), Error guessing |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: A non-existent category ID: create `QA-<suffix> Gone` with `POST /api/part/category/` as `admin`, delete it (`DELETE /api/part/category/<pk>/` with both flags `false`), and reuse its `pk`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Orphan", "category": <deleted category pk>}` | A part is not created. Not known: depends on open question Q-REL-01 (status code and error body for a category ID that does not exist). |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> Orphan`, `limit=10` | `200 OK`. `count` is `0`: no part with this name exists. |

**Postconditions and cleanup:** None if rejected. If step 1 created a part: As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`).

**Notes:** None.

**Duplicate check:** 67 · Review · matches: [API-REL-045](relationships.md) (67), [API-REL-050](relationships.md) (67), [API-REL-013](relationships.md) (65), [API-REL-007](relationships.md) (56)

**Duplicate judgement:** Keep · Each match uses a different reference field and rule (`variant_of`/`revision_of` R-REL-10, `default_location` R-REL-03, an existing structural category R-REL-02); this case is the missing `category` ID of R-REL-01. · test-case-reviewer, 2026-10-14

### API-REL-006: Move a part to a category ID that does not exist

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with a `category` that refers to no category is not accepted and the part keeps its category. |
| **Requirement** | R-REL-01 ([openapi-parts.yaml#L4122](../../requirements/openapi-parts.yaml#L4122)), response to a missing ID not stated. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Part.category`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: ID not found), State transition (blocked move) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Category` (not structural) created with `POST /api/part/category/`; part `QA-<suffix> Part` created in it; a non-existent category ID obtained by creating and deleting `QA-<suffix> Gone` as `admin` (both delete flags `false`); Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<part pk>/` as `engineer` | `{"category": <deleted category pk>}` | The part is not changed. Not known: depends on open question Q-REL-01 (status code and error body for a category ID that does not exist). |
| 2 | `GET /api/part/<part pk>/` as `engineer` | None | `200 OK`. `category` still equals the pk of `QA-<suffix> Category`. |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`), then `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** None.

**Duplicate check:** 69 · Review · matches: [API-REL-009](relationships.md) (69)

**Duplicate judgement:** Keep · Differs from API-REL-009 in rule and class: a category ID that does not exist (R-REL-01) vs an existing structural category (R-REL-02). · test-case-reviewer, 2026-10-14

### API-REL-007: Create a part directly in a structural category

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with the `category` of a structural category is not accepted: parts may not be assigned directly to it. |
| **Requirement** | R-REL-02 ([openapi-parts.yaml#L3560](../../requirements/openapi-parts.yaml#L3560)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Category.structural`, `components.schemas.Part.category`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Negative (forbidden assignment), Decision table (category structural = true, direct assignment) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Structural` created with `POST /api/part/category/` and `structural` `true`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Direct Part", "category": <structural category pk>}` | The part is not created. Not known: depends on open question Q-REL-02 (status code and error body when a part is assigned to a structural category). |
| 2 | `GET /api/part/` as `engineer` | `category=<structural category pk>`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** None if rejected. If step 1 created a part: As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`). Then `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** None.

**Duplicate check:** 56 · Review · matches: [API-REL-005](relationships.md) (56), [API-REL-013](relationships.md) (54), [API-REL-045](relationships.md) (54), [API-REL-050](relationships.md) (54)

**Duplicate judgement:** Keep · Differs from every match in rule and starting state: an existing category that is structural (R-REL-02) vs a reference ID that does not exist (R-REL-01, R-REL-03, R-REL-10). · test-case-reviewer, 2026-10-14

### API-REL-008: Create a part in a child of a structural category

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with the `category` of a non-structural child of a structural category is accepted. |
| **Requirement** | R-REL-02 ([openapi-parts.yaml#L3560](../../requirements/openapi-parts.yaml#L3560)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Category.structural`, `components.schemas.Category.parent`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Decision table (parent structural = true, child structural = false), Equivalence partitioning (valid class) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Structural` (`structural` `true`), and `QA-<suffix> Child` (`structural` `false`, `parent` = the structural category `pk`), created with `POST /api/part/category/`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Child Part", "category": <child category pk>}` | `201 Created`. Body is valid against `Part`; `category` equals the child category `pk`. |
| 2 | `GET /api/part/` as `engineer` | `category=<child category pk>`, `limit=10` | `200 OK`. The list contains exactly one part, with the `pk` from step 1. |

**Postconditions and cleanup:** One part in the child category. As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`), then `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for the child, then for the structural category.

**Notes:** None.

**Duplicate check:** 50 · Review · matches: [API-REL-011](relationships.md) (50)

**Duplicate judgement:** Keep · Differs from API-REL-011 in rule and starting state: part created in a non-structural child of a structural category (R-REL-02) vs part created with a default location (R-REL-03). · test-case-reviewer, 2026-10-14

### API-REL-009: Move an existing part into a structural category

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with the `category` of a structural category is not accepted and the part keeps its category. |
| **Requirement** | R-REL-02 ([openapi-parts.yaml#L3560](../../requirements/openapi-parts.yaml#L3560)). Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Category.structural`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Negative (forbidden assignment), State transition (blocked move) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Category` (not structural) created with `POST /api/part/category/`, and category `QA-<suffix> Structural` (`structural` `true`); part `QA-<suffix> Part` created in the first one; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<part pk>/` as `engineer` | `{"category": <structural category pk>}` | The part is not moved. Not known: depends on open question Q-REL-02 (status code and error body when a part is assigned to a structural category). |
| 2 | `GET /api/part/<part pk>/` as `engineer` | None | `200 OK`. `category` still equals the pk of `QA-<suffix> Category`. |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`), then `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for both categories.

**Notes:** None.

**Duplicate check:** 69 · Review · matches: [API-REL-006](relationships.md) (69)

**Duplicate judgement:** Keep · Differs from API-REL-006 in rule and class: an existing structural category (R-REL-02, Q-REL-02) vs a category ID that does not exist (R-REL-01, Q-REL-01). · test-case-reviewer, 2026-10-14

### API-REL-010: Make a category that already holds a part structural

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` with `structural` `true` on a category that already contains a part: the outcome for the existing part is checked. |
| **Requirement** | R-REL-02 ([openapi-parts.yaml#L3560](../../requirements/openapi-parts.yaml#L3560)), effect on parts already assigned not stated. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/`, `components.schemas.Category.structural`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | What-if business scenario (category made structural while it holds parts), State transition (non-structural to structural) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Category` (not structural) created with `POST /api/part/category/`; part `QA-<suffix> Part` created in it; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome is not known yet. |
| **Review** | Draft · Open question: Q-REL-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/<category pk>/` as `engineer` | `{"structural": true}` | Not known: depends on open question Q-REL-02 (whether the change is accepted or refused when the category already contains a part, and the status and body if refused). |
| 2 | `GET /api/part/<part pk>/` as `engineer` | None | `200 OK`. The part is kept; `category` still equals the category `pk`. |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`), then `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** None.

### API-REL-011: Create a part with a default location

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `default_location` set to an existing stock location is accepted and the value is returned. |
| **Requirement** | R-REL-03 ([openapi-parts.yaml#L4144](../../requirements/openapi-parts.yaml#L4144)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.default_location`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: existing location ID) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: stock location `QA-<suffix> Location` created with `POST /api/stock/location/` as `admin`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`; create the location with `admin`'s token. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Located Part", "default_location": <location pk>}` | `201 Created`. Body is valid against `Part` (apart from F-11 for a part without category); `default_location` equals the location `pk`. |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `default_location` equals the location `pk`. |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then as `admin` `DELETE /api/stock/location/<pk>/` (`204`; whether a body is needed is not in the schema).

**Notes:** The part has no category, so `category_name` is missing from the response (test-cases/findings.md#F-11).

**Duplicate check:** 50 · Review · matches: [API-REL-008](relationships.md) (50)

**Duplicate judgement:** Keep · Differs from API-REL-008 in rule: part `default_location` (R-REL-03) vs placement in a child of a structural category (R-REL-02). · test-case-reviewer, 2026-10-14

### API-REL-012: Clear a part's default location with null

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with `default_location` `null` is accepted (the field is nullable) and the part has no default location afterwards. |
| **Requirement** | R-REL-03 ([openapi-parts.yaml#L4144](../../requirements/openapi-parts.yaml#L4144)). Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Part.default_location` (`nullable: true`). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: null), State transition (location set to cleared) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: stock location `QA-<suffix> Location` created with `POST /api/stock/location/` as `admin`; part `QA-<suffix> Part` created with `default_location` = that location; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`; create the location with `admin`'s token. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<part pk>/` as `engineer` | `{"default_location": null}` | `200 OK`. `default_location` is `null`. |
| 2 | `GET /api/part/<part pk>/` as `engineer` | None | `200 OK`. `default_location` is `null`. |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then as `admin` `DELETE /api/stock/location/<pk>/` (`204`; whether a body is needed is not in the schema).

**Notes:** None.

**Duplicate check:** 58 · Review · matches: [API-REL-015](relationships.md) (58), [API-REL-004](relationships.md) (56), [API-REL-044](relationships.md) (56)

**Duplicate judgement:** Keep · Differs from API-REL-015 in resource and rule (part `default_location`, R-REL-03 vs category `default_location`, R-REL-04), and from API-REL-004 and API-REL-044 in field and rule (`category`, `variant_of`). · test-case-reviewer, 2026-10-14

### API-REL-013: Create a part with a `default_location` ID that does not exist

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a `default_location` that refers to no stock location is not accepted and no part is created. |
| **Requirement** | R-REL-03 ([openapi-parts.yaml#L4144](../../requirements/openapi-parts.yaml#L4144)), response to a missing ID not stated. Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.default_location`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: ID not found), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: A non-existent location ID: create `QA-<suffix> Gone Location` with `POST /api/stock/location/` as `admin`, delete it with `DELETE /api/stock/location/<pk>/`, and reuse its `pk`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> No Location", "default_location": <deleted location pk>}` | A part is not created. Not known: depends on open question Q-REL-01 (status code and error body for a location ID that does not exist). |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> No Location`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** None if rejected. If step 1 created a part: As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`).

**Notes:** None.

**Duplicate check:** 69 · Review · matches: [API-REL-045](relationships.md) (69), [API-REL-050](relationships.md) (69), [API-REL-005](relationships.md) (65), [API-REL-007](relationships.md) (54)

**Duplicate judgement:** Keep · Differs from every match in the reference field and rule: a stock location ID that does not exist for `default_location` (R-REL-03) vs part or category references (R-REL-10, R-REL-01) and a structural category (R-REL-02). · test-case-reviewer, 2026-10-14

### API-REL-014: Create a category with a default location

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` with `default_location` set to an existing stock location is accepted and the value is returned. |
| **Requirement** | R-REL-04 ([openapi-parts.yaml#L3525](../../requirements/openapi-parts.yaml#L3525)). Schema: `requirements/openapi-parts.yaml POST /api/part/category/`, `components.schemas.Category.default_location`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: existing location ID) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: stock location `QA-<suffix> Location` created with `POST /api/stock/location/` as `admin`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`; create the location with `admin`'s token. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Category", "default_location": <location pk>}` | `201 Created`. Body is valid against `Category`; `default_location` equals the location `pk`. |
| 2 | `GET /api/part/category/<pk from step 1>/` as `engineer` | None | `200 OK`. `default_location` equals the location `pk`. |

**Postconditions and cleanup:** As `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`), then `DELETE /api/stock/location/<pk>/` (`204`; whether a body is needed is not in the schema).

**Notes:** None.

**Duplicate check:** 53 · Review · matches: [API-REL-019](relationships.md) (53), [API-REL-018](relationships.md) (51)

**Duplicate judgement:** Keep · Differs from API-REL-019 and API-REL-018 in field and rule: category `default_location` (R-REL-04) vs category `parent` (R-REL-06). · test-case-reviewer, 2026-10-14

### API-REL-015: Clear a category's default location with null

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` with `default_location` `null` is accepted (the field is nullable) and the category has no default location afterwards. |
| **Requirement** | R-REL-04 ([openapi-parts.yaml#L3525](../../requirements/openapi-parts.yaml#L3525)). Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/`, `components.schemas.Category.default_location` (`nullable: true`). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: null), State transition (location set to cleared) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: stock location `QA-<suffix> Location` created with `POST /api/stock/location/` as `admin`; category `QA-<suffix> Category` created with `default_location` = that location; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`; create the location with `admin`'s token. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/<category pk>/` as `engineer` | `{"default_location": null}` | `200 OK`. `default_location` is `null`. |
| 2 | `GET /api/part/category/<category pk>/` as `engineer` | None | `200 OK`. `default_location` is `null`. |

**Postconditions and cleanup:** As `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`), then `DELETE /api/stock/location/<pk>/` (`204`; whether a body is needed is not in the schema).

**Notes:** None.

**Duplicate check:** 58 · Review · matches: [API-REL-012](relationships.md) (58), [API-REL-021](relationships.md) (50)

**Duplicate judgement:** Keep · Differs from API-REL-012 in resource and rule (category, R-REL-04 vs part, R-REL-03), and from API-REL-021 in field and rule (`default_location` vs `parent`, R-REL-06). · test-case-reviewer, 2026-10-14

### API-REL-016: A part in a category with a default location reports `category_default_location`

| Field | Value |
|---|---|
| **Summary** | A part created without its own `default_location` in a category that has one: `category_default_location` and `default_location` in the part response are checked. |
| **Requirement** | R-REL-04 ([openapi-parts.yaml#L3525](../../requirements/openapi-parts.yaml#L3525)), R-REL-05 ([openapi-parts.yaml#L4294](../../requirements/openapi-parts.yaml#L4294)), meaning not described. Schema: `requirements/openapi-parts.yaml GET /api/part/{id}/`, `components.schemas.Part.category_default_location` (`readOnly`), `components.schemas.Category.default_location`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Decision table (category has default location, part has none), Exploratory (category default applied to parts) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: stock location `QA-<suffix> Location` created with `POST /api/stock/location/` as `admin`; category `QA-<suffix> Category` created with `default_location` = that location; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`; create the location with `admin`'s token. |
| **Automation** | Partial: the expected values are not known yet. |
| **Review** | Draft · Open question: Q-REL-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Part", "category": <category pk>}` | `201 Created`. Body is valid against `Part`. Not known: depends on open question Q-REL-03 (the value of `category_default_location` and whether `default_location` is filled from the category). |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `category_default_location` is an integer or `null` (schema type). Not known: depends on open question Q-REL-03 (the value of `category_default_location` and whether `default_location` is filled from the category). |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then as `admin` `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`), then `DELETE /api/stock/location/<pk>/` (`204`; whether a body is needed is not in the schema).

**Notes:** `category_default_location` is described only as read-only and nullable; its meaning is not stated.

### API-REL-017: A part in a category without a default location reports `category_default_location` null

| Field | Value |
|---|---|
| **Summary** | A part in a category whose `default_location` is `null`: the read-only `category_default_location` is checked. |
| **Requirement** | R-REL-05 ([openapi-parts.yaml#L4294](../../requirements/openapi-parts.yaml#L4294)), meaning not described. Schema: `requirements/openapi-parts.yaml GET /api/part/{id}/`, `components.schemas.Part.category_default_location`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Decision table (category has no default location), Equivalence partitioning (null class) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Category` (not structural) created with `POST /api/part/category/` (no `default_location`); part `QA-<suffix> Part` created in it; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the expected value is not known yet. |
| **Review** | Draft · Open question: Q-REL-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/<part pk>/` as `engineer` | None | `200 OK`. `default_location` is `null`. Not known: depends on open question Q-REL-03 (the value of `category_default_location` when the category has no default location). |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`), then `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** None.

### API-REL-018: Create a child category with `parent`

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` with `parent` set to an existing category creates a child and returns the parent ID. |
| **Requirement** | R-REL-06 ([openapi-parts.yaml#L3537](../../requirements/openapi-parts.yaml#L3537)). Schema: `requirements/openapi-parts.yaml POST /api/part/category/`, `components.schemas.Category.parent`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: existing parent ID) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Parent` (not structural) created with `POST /api/part/category/`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Child", "parent": <parent pk>}` | `201 Created`. Body is valid against `Category`; `parent` equals the parent `pk`. |
| 2 | `GET /api/part/category/` as `engineer` | `parent=<parent pk>`, `limit=10` | `200 OK`. The list contains exactly one category, with the `pk` from step 1. |

**Postconditions and cleanup:** As `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for the child, then for the parent.

**Notes:** None.

**Duplicate check:** 66 · Review · matches: [API-REL-019](relationships.md) (66), [API-REL-014](relationships.md) (51)

**Duplicate judgement:** Keep · Differs from API-REL-019 in class and outcome (existing `parent` given, child created vs `parent` omitted, top-level), and from API-REL-014 in rule (R-REL-06 vs R-REL-04). · test-case-reviewer, 2026-10-14

### API-REL-019: Create a top-level category without `parent`

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` without `parent` creates a top-level category: `parent` is `null` in the response. |
| **Requirement** | R-REL-06 ([openapi-parts.yaml#L3537](../../requirements/openapi-parts.yaml#L3537)). Schema: `requirements/openapi-parts.yaml POST /api/part/category/`, `components.schemas.Category.parent` (`nullable: true`). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: parent omitted) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Top"}` | `201 Created`. Body is valid against `Category`; `parent` is `null`. |
| 2 | `GET /api/part/category/<pk from step 1>/` as `engineer` | None | `200 OK`. `parent` is `null`. |

**Postconditions and cleanup:** As `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** None.

**Duplicate check:** 66 · Review · matches: [API-REL-018](relationships.md) (66), [API-REL-014](relationships.md) (53)

**Duplicate judgement:** Keep · Differs from API-REL-018 in class and outcome (`parent` omitted, top-level vs existing parent, child), and from API-REL-014 in rule (R-REL-06 vs R-REL-04). · test-case-reviewer, 2026-10-14

### API-REL-020: Move a category under another parent with PATCH

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` with a new `parent` moves the category in the hierarchy. |
| **Requirement** | R-REL-06 ([openapi-parts.yaml#L3537](../../requirements/openapi-parts.yaml#L3537)). Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/`, `components.schemas.Category.parent`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | State transition (child of parent A to child of parent B) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: categories `QA-<suffix> Parent A`, `QA-<suffix> Parent B` (top-level), and `QA-<suffix> Child` with `parent` = Parent A, created with `POST /api/part/category/`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/<child pk>/` as `engineer` | `{"parent": <parent B pk>}` | `200 OK`. Body is valid against `Category`; `parent` equals the Parent B `pk`. |
| 2 | `GET /api/part/category/` as `engineer` | `parent=<parent B pk>`, `limit=10` | `200 OK`. The list contains exactly one category, `QA-<suffix> Child`. |
| 3 | `GET /api/part/category/` as `engineer` | `parent=<parent A pk>`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** As `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for the child, then for both parents.

**Notes:** None.

**Duplicate check:** 63 · Review · matches: [API-REL-021](relationships.md) (63)

**Duplicate judgement:** Keep · Differs from API-REL-021 in transition and outcome: moved under another existing parent vs `parent` set to `null` (becomes top-level). · test-case-reviewer, 2026-10-14

### API-REL-021: Make a child category top-level by setting `parent` to null

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` with `parent` `null` is accepted (the field is nullable) and the category becomes top-level. |
| **Requirement** | R-REL-06 ([openapi-parts.yaml#L3537](../../requirements/openapi-parts.yaml#L3537)). Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/`, `components.schemas.Category.parent` (`nullable: true`). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: null), State transition (child to top-level) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Parent` and `QA-<suffix> Child` with `parent` = Parent, created with `POST /api/part/category/`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/<child pk>/` as `engineer` | `{"parent": null}` | `200 OK`. `parent` is `null`. |
| 2 | `GET /api/part/category/` as `engineer` | `parent=<parent pk>`, `limit=10` | `200 OK`. `count` is `0`: the parent has no child. |

**Postconditions and cleanup:** As `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for the child, then for the parent.

**Notes:** None.

**Duplicate check:** 63 · Review · matches: [API-REL-020](relationships.md) (63), [API-REL-015](relationships.md) (50)

**Duplicate judgement:** Keep · Differs from API-REL-020 in class and outcome (`null`, becomes top-level vs another parent), and from API-REL-015 in field and rule (`parent`, R-REL-06 vs `default_location`, R-REL-04). · test-case-reviewer, 2026-10-14

### API-REL-022: Create a category with a `parent` ID that does not exist

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` with a `parent` that refers to no category is not accepted and no category is created. |
| **Requirement** | R-REL-06 ([openapi-parts.yaml#L3537](../../requirements/openapi-parts.yaml#L3537)), response to a missing ID not stated. Schema: `requirements/openapi-parts.yaml POST /api/part/category/`, `components.schemas.Category.parent`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: ID not found), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: A non-existent category ID: create `QA-<suffix> Gone` with `POST /api/part/category/` as `admin`, delete it (both delete flags `false`), and reuse its `pk`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Orphan Child", "parent": <deleted category pk>}` | A category is not created. Not known: depends on open question Q-REL-01 (status code and error body for a parent ID that does not exist). |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix> Orphan Child`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** None if rejected. If step 1 created a category: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** None.

### API-REL-023: Set a category as its own parent

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` with `parent` equal to the category's own `pk` is checked: a circular parent. |
| **Requirement** | R-REL-06 ([openapi-parts.yaml#L3537](../../requirements/openapi-parts.yaml#L3537)), circular parent not stated. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/`, `components.schemas.Category.parent`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Error guessing (self reference), State transition (blocked change) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Category` (top-level) created with `POST /api/part/category/`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome is not known yet. |
| **Review** | Draft · Open question: Q-REL-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/<category pk>/` as `engineer` | `{"parent": <the same category pk>}` | Not known: depends on open question Q-REL-04 (whether a self-parent is rejected, and the status code and error body). |
| 2 | `GET /api/part/category/<category pk>/` as `engineer` | None | `200 OK`. Not known: depends on open question Q-REL-04 (whether `parent` is unchanged after the attempt). |

**Postconditions and cleanup:** As `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** None.

**Duplicate check:** 87 · Duplicate · matches: [API-REL-024](relationships.md) (87)

**Duplicate judgement:** Keep · Differs from API-REL-024 in class and starting state: a direct self-reference on one category vs an indirect cycle through a descendant in a three-level chain; app logic may catch one and not the other. · test-case-reviewer, 2026-10-14

### API-REL-024: Move a category under its own child

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` setting `parent` to one of the category's own descendants is checked: a circular hierarchy. |
| **Requirement** | R-REL-06 ([openapi-parts.yaml#L3537](../../requirements/openapi-parts.yaml#L3537)), circular parent not stated. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/`, `components.schemas.Category.parent`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Error guessing (circular hierarchy), What-if business scenario (category moved into its own subtree) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Top`, `QA-<suffix> Mid` (`parent` = Top) and `QA-<suffix> Leaf` (`parent` = Mid), created with `POST /api/part/category/`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome is not known yet. |
| **Review** | Draft · Open question: Q-REL-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/<Top pk>/` as `engineer` | `{"parent": <Leaf pk>}` | Not known: depends on open question Q-REL-04 (whether a circular parent is rejected, and the status code and error body). |
| 2 | `GET /api/part/category/<Top pk>/` as `engineer` | None | `200 OK`. Not known: depends on open question Q-REL-04 (whether `parent` is unchanged after the attempt). |

**Postconditions and cleanup:** As `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for Leaf, Mid, then Top (if step 1 was accepted, delete in the order that the resulting hierarchy allows).

**Notes:** None.

**Duplicate check:** 87 · Duplicate · matches: [API-REL-023](relationships.md) (87)

**Duplicate judgement:** Keep · Differs from API-REL-023 in class and starting state: an indirect cycle (Top moved under its grandchild Leaf) vs a direct self-reference on a single category. · test-case-reviewer, 2026-10-14

### API-REL-025: `level` and `pathstring` of nested categories follow the hierarchy

| Field | Value |
|---|---|
| **Summary** | In a three-level chain of categories, `level` and `pathstring` are returned for each category and are derived from its position. |
| **Requirement** | R-REL-07 ([openapi-parts.yaml#L3534](../../requirements/openapi-parts.yaml#L3534), [openapi-parts.yaml#L3551](../../requirements/openapi-parts.yaml#L3551)), `pathstring` format not stated. Schema: `requirements/openapi-parts.yaml GET /api/part/category/{id}/`, `components.schemas.Category.level`, `components.schemas.Category.pathstring` (both `readOnly`). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (top, middle, leaf classes), State transition (hierarchy built) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: category `QA-<suffix> Top`, `QA-<suffix> Mid` (`parent` = Top) and `QA-<suffix> Leaf` (`parent` = Mid), created with `POST /api/part/category/`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the expected values are not known yet. |
| **Review** | Draft · Open question: Q-REL-05 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/<Top pk>/` as `engineer` | None | `200 OK`. Body is valid against `Category`; `level` is an integer and `pathstring` a string. Not known: depends on open question Q-REL-05 (the `level` value of a top-level category and the `pathstring` format). |
| 2 | `GET /api/part/category/<Mid pk>/` as `engineer` | None | `200 OK`. Not known: depends on open question Q-REL-05 (the `level` value and `pathstring` of a second-level category). |
| 3 | `GET /api/part/category/<Leaf pk>/` as `engineer` | None | `200 OK`. Not known: depends on open question Q-REL-05 (the `level` value and `pathstring` of a third-level category). |

**Postconditions and cleanup:** As `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for Leaf, Mid, then Top.

**Notes:** Existing API-REL-002 observed `level` `0` for a top-level category after a delete; that is not a documented rule, so it is not used here.

### API-REL-026: `level` and `pathstring` change when a category is moved

| Field | Value |
|---|---|
| **Summary** | After `PATCH /api/part/category/{id}/` moves a category and its child to a new parent, the derived `level` and `pathstring` of both are recomputed. |
| **Requirement** | R-REL-07 ([openapi-parts.yaml#L3534](../../requirements/openapi-parts.yaml#L3534), [openapi-parts.yaml#L3551](../../requirements/openapi-parts.yaml#L3551)), `pathstring` format not stated. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/`, `components.schemas.Category.level`, `components.schemas.Category.pathstring`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | State transition (subtree moved), What-if business scenario (category moved under another parent) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: top-level categories `QA-<suffix> Parent A` and `QA-<suffix> Parent B`; `QA-<suffix> Mid` (`parent` = Parent A) and `QA-<suffix> Leaf` (`parent` = Mid), created with `POST /api/part/category/`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the expected values are not known yet. |
| **Review** | Draft · Open question: Q-REL-05 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/<Mid pk>/` as `engineer` | None | `200 OK`. `level` and `pathstring` are recorded for comparison. Not known: depends on open question Q-REL-05 (the format of `pathstring`). |
| 2 | `PATCH /api/part/category/<Mid pk>/` as `engineer` | `{"parent": <Parent B pk>}` | `200 OK`. `parent` equals the Parent B `pk`. |
| 3 | `GET /api/part/category/<Leaf pk>/` as `engineer` | None | `200 OK`. `parent` is still the Mid `pk`. Not known: depends on open question Q-REL-05 (the new `level` and `pathstring` of the moved child (whether `pathstring` now starts with the Parent B name)). |

**Postconditions and cleanup:** As `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for Leaf, Mid, Parent A and Parent B.

**Notes:** None.

### API-REL-027: Create a supplier part linking a part to a supplier

| Field | Value |
|---|---|
| **Summary** | `POST /api/company/part/` with `part`, `supplier` and `SKU` creates a supplier part and returns it. |
| **Requirement** | R-REL-08 ([openapi-parts.yaml#L185](../../requirements/openapi-parts.yaml#L185), [openapi-parts.yaml#L6029](../../requirements/openapi-parts.yaml#L6029), [openapi-parts.yaml#L6037](../../requirements/openapi-parts.yaml#L6037), [openapi-parts.yaml#L6033](../../requirements/openapi-parts.yaml#L6033)). Schema: `requirements/openapi-parts.yaml POST /api/company/part/`, `components.schemas.SupplierPart` (`required`: `part`, `supplier`, `SKU`). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: all required fields) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); part `QA-<suffix> Part` with `purchaseable` `true` created with `POST /api/part/` (as `admin`); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: depends on how the supplier is created (Q-REL-06). |
| **Review** | Draft · Open question: Q-REL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `admin` | `{"part": <part pk>, "supplier": <supplier pk>, "SKU": "QA-<suffix>-SKU-1"}` | `201 Created`. `part`, `supplier` and `SKU` equal the payload; `pk` is an integer. The body is checked against `SupplierPart` except `availability_updated` (test-cases/findings.md#F-07). |
| 2 | `GET /api/company/part/` as `admin` | `part=<part pk>`, `limit=10` | `200 OK`. The list contains exactly one supplier part, with the `pk` from step 1. |

**Postconditions and cleanup:** One supplier part. As `admin`: `DELETE /api/company/part/<pk>/` (`204`), As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`), and delete the supplier company (endpoint outside the schema slice).

**Notes:** `admin` is used because the operation lists purchase-order scopes beside part scopes (index, Schema issue 1).

### API-REL-028: Create a supplier part without `SKU`

| Field | Value |
|---|---|
| **Summary** | `POST /api/company/part/` without the required `SKU` is not accepted and no supplier part is created. |
| **Requirement** | R-REL-08 ([openapi-parts.yaml#L185](../../requirements/openapi-parts.yaml#L185), [openapi-parts.yaml#L6029](../../requirements/openapi-parts.yaml#L6029), [openapi-parts.yaml#L6037](../../requirements/openapi-parts.yaml#L6037), [openapi-parts.yaml#L6033](../../requirements/openapi-parts.yaml#L6033)). Schema: `requirements/openapi-parts.yaml POST /api/company/part/`, `components.schemas.SupplierPart` (`required` includes `SKU`). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: required field `SKU` missing), Negative |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); part `QA-<suffix> Part` with `purchaseable` `true` created with `POST /api/part/` (as `admin`); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01, Q-REL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `admin` | `{"part": <part pk>, "supplier": <supplier pk>}` | A supplier part is not created. Not known: depends on open question Q-REL-01 (status code and error body for a missing required field `SKU`). |
| 2 | `GET /api/company/part/` as `admin` | `part=<part pk>`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** None if rejected. If step 1 created a supplier part: `DELETE /api/company/part/<pk>/` as `admin` (`204`). As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); delete the supplier company.

**Notes:** None.

**Duplicate check:** 87 · Review · matches: [API-REL-029](relationships.md) (87, test data differs), [API-REL-030](relationships.md) (86, test data differs), [API-REL-033](relationships.md) (78), [API-REL-034](relationships.md) (50)

**Duplicate judgement:** Keep · A different required field is omitted (`SKU`) than in API-REL-029 (`part`) and API-REL-030 (`supplier`), each its own clause of R-REL-08; API-REL-033 is a non-existent ID and API-REL-034 a non-purchaseable part. · test-case-reviewer, 2026-10-14

### API-REL-029: Create a supplier part without `part`

| Field | Value |
|---|---|
| **Summary** | `POST /api/company/part/` without the required `part` is not accepted and no supplier part is created. |
| **Requirement** | R-REL-08 ([openapi-parts.yaml#L185](../../requirements/openapi-parts.yaml#L185), [openapi-parts.yaml#L6029](../../requirements/openapi-parts.yaml#L6029), [openapi-parts.yaml#L6037](../../requirements/openapi-parts.yaml#L6037), [openapi-parts.yaml#L6033](../../requirements/openapi-parts.yaml#L6033)). Schema: `requirements/openapi-parts.yaml POST /api/company/part/`, `components.schemas.SupplierPart` (`required` includes `part`). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: required field `part` missing), Negative |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); part `QA-<suffix> Part` with `purchaseable` `true` created with `POST /api/part/` (as `admin`); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01, Q-REL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `admin` | `{"supplier": <supplier pk>, "SKU": "QA-<suffix>-SKU-2"}` | A supplier part is not created. Not known: depends on open question Q-REL-01 (status code and error body for a missing required field `part`). |
| 2 | `GET /api/company/part/` as `admin` | `part=<part pk>`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** None if rejected. If step 1 created a supplier part: `DELETE /api/company/part/<pk>/` as `admin` (`204`). As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); delete the supplier company.

**Notes:** None.

**Duplicate check:** 92 · Duplicate · matches: [API-REL-030](relationships.md) (92), [API-REL-028](relationships.md) (87, test data differs), [API-REL-033](relationships.md) (81), [API-REL-034](relationships.md) (52)

**Duplicate judgement:** Keep · A different required field is omitted (`part`) than in API-REL-030 (`supplier`) and API-REL-028 (`SKU`); API-REL-033 sends `part` with a non-existent ID (another invalid class) and API-REL-034 a non-purchaseable part. · test-case-reviewer, 2026-10-14

### API-REL-030: Create a supplier part without `supplier`

| Field | Value |
|---|---|
| **Summary** | `POST /api/company/part/` without the required `supplier` is not accepted and no supplier part is created. |
| **Requirement** | R-REL-08 ([openapi-parts.yaml#L185](../../requirements/openapi-parts.yaml#L185), [openapi-parts.yaml#L6029](../../requirements/openapi-parts.yaml#L6029), [openapi-parts.yaml#L6037](../../requirements/openapi-parts.yaml#L6037), [openapi-parts.yaml#L6033](../../requirements/openapi-parts.yaml#L6033)). Schema: `requirements/openapi-parts.yaml POST /api/company/part/`, `components.schemas.SupplierPart` (`required` includes `supplier`). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: required field `supplier` missing), Negative |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); part `QA-<suffix> Part` with `purchaseable` `true` created with `POST /api/part/` (as `admin`); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01, Q-REL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `admin` | `{"part": <part pk>, "SKU": "QA-<suffix>-SKU-2"}` | A supplier part is not created. Not known: depends on open question Q-REL-01 (status code and error body for a missing required field `supplier`). |
| 2 | `GET /api/company/part/` as `admin` | `part=<part pk>`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** None if rejected. If step 1 created a supplier part: `DELETE /api/company/part/<pk>/` as `admin` (`204`). As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); delete the supplier company.

**Notes:** None.

**Duplicate check:** 92 · Duplicate · matches: [API-REL-029](relationships.md) (92), [API-REL-028](relationships.md) (86, test data differs), [API-REL-033](relationships.md) (79), [API-REL-034](relationships.md) (50)

**Duplicate judgement:** Keep · A different required field is omitted (`supplier`) than in API-REL-029 (`part`) and API-REL-028 (`SKU`); API-REL-033 and API-REL-034 concern the `part` value, not a missing `supplier`. · test-case-reviewer, 2026-10-14

### API-REL-031: Create a supplier part with a 100-character `SKU`

| Field | Value |
|---|---|
| **Summary** | `POST /api/company/part/` with a `SKU` of exactly 100 characters (`maxLength`) is accepted and the value is stored as sent. |
| **Requirement** | R-REL-08 ([openapi-parts.yaml#L185](../../requirements/openapi-parts.yaml#L185), [openapi-parts.yaml#L6029](../../requirements/openapi-parts.yaml#L6029), [openapi-parts.yaml#L6037](../../requirements/openapi-parts.yaml#L6037), [openapi-parts.yaml#L6033](../../requirements/openapi-parts.yaml#L6033)). Schema: `requirements/openapi-parts.yaml POST /api/company/part/`, `components.schemas.SupplierPart.SKU` (`maxLength: 100`). |
| **Area** | REL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (SKU maxLength on the limit) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); part `QA-<suffix> Part` with `purchaseable` `true` created with `POST /api/part/` (as `admin`); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: depends on how the supplier is created (Q-REL-06). |
| **Review** | Draft · Open question: Q-REL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `admin` | `{"part": <part pk>, "supplier": <supplier pk>, "SKU": "<100 characters: QA-<suffix>- followed by A to length 100>"}` | `201 Created`. `SKU` equals the 100-character payload value. |

**Postconditions and cleanup:** As `admin`: `DELETE /api/company/part/<pk>/` (`204`), As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); delete the supplier company.

**Notes:** None.

### API-REL-032: Create a supplier part with a 101-character `SKU`

| Field | Value |
|---|---|
| **Summary** | `POST /api/company/part/` with a `SKU` of 101 characters (`maxLength` + 1) is not accepted and no supplier part is created. |
| **Requirement** | R-REL-08 ([openapi-parts.yaml#L185](../../requirements/openapi-parts.yaml#L185), [openapi-parts.yaml#L6029](../../requirements/openapi-parts.yaml#L6029), [openapi-parts.yaml#L6037](../../requirements/openapi-parts.yaml#L6037), [openapi-parts.yaml#L6033](../../requirements/openapi-parts.yaml#L6033)). Schema: `requirements/openapi-parts.yaml POST /api/company/part/`, `components.schemas.SupplierPart.SKU` (`maxLength: 100`). |
| **Area** | REL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (SKU maxLength + 1) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); part `QA-<suffix> Part` with `purchaseable` `true` created with `POST /api/part/` (as `admin`); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01, Q-REL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `admin` | `{"part": <part pk>, "supplier": <supplier pk>, "SKU": "<101 characters>"}` | A supplier part is not created. Not known: depends on open question Q-REL-01 (status code and error body for a value over `maxLength`). |
| 2 | `GET /api/company/part/` as `admin` | `part=<part pk>`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** None if rejected. If step 1 created a supplier part: `DELETE /api/company/part/<pk>/` as `admin`. As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); delete the supplier company.

**Notes:** None.

### API-REL-033: Create a supplier part for a part that does not exist

| Field | Value |
|---|---|
| **Summary** | `POST /api/company/part/` with a `part` that refers to no part is not accepted and no supplier part is created. |
| **Requirement** | R-REL-08 ([openapi-parts.yaml#L185](../../requirements/openapi-parts.yaml#L185), [openapi-parts.yaml#L6029](../../requirements/openapi-parts.yaml#L6029), [openapi-parts.yaml#L6037](../../requirements/openapi-parts.yaml#L6037), [openapi-parts.yaml#L6033](../../requirements/openapi-parts.yaml#L6033)), response to a missing ID not stated. Schema: `requirements/openapi-parts.yaml POST /api/company/part/`, `components.schemas.SupplierPart.part`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: ID not found), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); a non-existent part ID: create `QA-<suffix> Gone Part` with `POST /api/part/`, `PATCH` it inactive, `DELETE` it, and reuse its `pk`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01, Q-REL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `admin` | `{"part": <deleted part pk>, "supplier": <supplier pk>, "SKU": "QA-<suffix>-SKU-3"}` | A supplier part is not created. Not known: depends on open question Q-REL-01 (status code and error body for a part ID that does not exist). |
| 2 | `GET /api/company/part/` as `admin` | `supplier=<supplier pk>`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** None if rejected. If step 1 created a supplier part: `DELETE /api/company/part/<pk>/` as `admin`. Delete the supplier company.

**Notes:** None.

**Duplicate check:** 81 · Duplicate · matches: [API-REL-029](relationships.md) (81), [API-REL-030](relationships.md) (79), [API-REL-028](relationships.md) (78), [API-REL-034](relationships.md) (52)

**Duplicate judgement:** Keep · Differs from API-REL-029 in class: `part` sent with an ID that does not exist vs `part` omitted; API-REL-030/028 omit other fields and API-REL-034 uses an existing non-purchaseable part. · test-case-reviewer, 2026-10-14

### API-REL-034: Create a supplier part for a part that is not purchaseable

| Field | Value |
|---|---|
| **Summary** | `POST /api/company/part/` linking a part with `purchaseable` `false` to a supplier: the outcome is checked. |
| **Requirement** | R-REL-08 ([openapi-parts.yaml#L185](../../requirements/openapi-parts.yaml#L185), [openapi-parts.yaml#L6029](../../requirements/openapi-parts.yaml#L6029), [openapi-parts.yaml#L6037](../../requirements/openapi-parts.yaml#L6037), [openapi-parts.yaml#L6033](../../requirements/openapi-parts.yaml#L6033)), whether the part must be purchaseable is not stated. Schema: `requirements/openapi-parts.yaml POST /api/company/part/`, `components.schemas.Part.purchaseable`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Decision table (part purchaseable = false), What-if business scenario (supplier added to a non-purchaseable part) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); part `QA-<suffix> Part` created with `purchaseable` `false`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome is not known yet. |
| **Review** | Draft · Open question: Q-REL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `admin` | `{"part": <part pk>, "supplier": <supplier pk>, "SKU": "QA-<suffix>-SKU-4"}` | Not known: depends on open question Q-REL-06 (whether the request is accepted for a part that is not purchaseable, and the status and body if refused). |

**Postconditions and cleanup:** If step 1 created a supplier part: `DELETE /api/company/part/<pk>/` as `admin`. As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); delete the supplier company.

**Notes:** None.

**Duplicate check:** 52 · Review · matches: [API-REL-029](relationships.md) (52), [API-REL-033](relationships.md) (52), [API-REL-028](relationships.md) (50), [API-REL-030](relationships.md) (50)

**Duplicate judgement:** Keep · Differs from every match in starting state: a complete, valid payload for an existing part with `purchaseable` `false`, while the matches omit a required field or use a non-existent part. · test-case-reviewer, 2026-10-14

### API-REL-035: Read a supplier part that does not exist

| Field | Value |
|---|---|
| **Summary** | `GET /api/company/part/{id}/` for an ID that does not exist returns `404 Not Found`. |
| **Requirement** | R-REL-08 ([openapi-parts.yaml#L185](../../requirements/openapi-parts.yaml#L185), [openapi-parts.yaml#L6029](../../requirements/openapi-parts.yaml#L6029), [openapi-parts.yaml#L6037](../../requirements/openapi-parts.yaml#L6037), [openapi-parts.yaml#L6033](../../requirements/openapi-parts.yaml#L6033)), operation's own rule. Schema: `requirements/openapi-parts.yaml GET /api/company/part/{id}/`. Standing rule: `references/seed-api-test-case.md` (not found = 404). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Not found (API), Equivalence partitioning (invalid class: ID not found) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: A non-existent supplier part ID: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); part `QA-<suffix> Part` with `purchaseable` `true` created with `POST /api/part/`; create a supplier part with `POST /api/company/part/`, delete it with `DELETE /api/company/part/<pk>/`, and reuse its `pk`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/company/part/<deleted pk>/` as `admin` | None | `404 Not Found`. The body has a `detail` of the form `No <Model> matches the given query.` (the model name for this endpoint was not confirmed). |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); delete the supplier company.

**Notes:** None.

**Duplicate check:** 59 · Review · matches: [API-REL-036](relationships.md) (59)

**Duplicate judgement:** Keep · Differs from API-REL-036 in operation (`GET` vs `DELETE`); the seed's Not found standing rule requires one 404 case per operation. · test-case-reviewer, 2026-10-14

### API-REL-036: Delete a supplier part that does not exist

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/company/part/{id}/` for an ID that does not exist returns `404 Not Found`. |
| **Requirement** | R-REL-08 ([openapi-parts.yaml#L185](../../requirements/openapi-parts.yaml#L185), [openapi-parts.yaml#L6029](../../requirements/openapi-parts.yaml#L6029), [openapi-parts.yaml#L6037](../../requirements/openapi-parts.yaml#L6037), [openapi-parts.yaml#L6033](../../requirements/openapi-parts.yaml#L6033)), operation's own rule. Schema: `requirements/openapi-parts.yaml DELETE /api/company/part/{id}/`. Standing rule: `references/seed-api-test-case.md` (not found = 404). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Not found (API), Equivalence partitioning (invalid class: ID not found) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: A non-existent supplier part ID: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); part `QA-<suffix> Part` with `purchaseable` `true` created with `POST /api/part/`; create a supplier part with `POST /api/company/part/`, delete it with `DELETE /api/company/part/<pk>/`, and reuse its `pk`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/company/part/<deleted pk>/` as `admin` | None | `404 Not Found`. The body has a `detail` of the form `No <Model> matches the given query.` (the model name for this endpoint was not confirmed). |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); delete the supplier company.

**Notes:** None.

**Duplicate check:** 59 · Review · matches: [API-REL-035](relationships.md) (59)

**Duplicate judgement:** Keep · Differs from API-REL-035 in operation (`DELETE` vs `GET`); the seed's Not found standing rule requires one 404 case per operation. · test-case-reviewer, 2026-10-14

### API-REL-037: Create a part with `initial_supplier` supplier and SKU

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `initial_supplier` holding `supplier` and `sku` creates the part and adds supplier information for it. |
| **Requirement** | R-REL-09 ([openapi-parts.yaml#L4354](../../requirements/openapi-parts.yaml#L4354), [openapi-parts.yaml#L3731](../../requirements/openapi-parts.yaml#L3731)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.initial_supplier`, `components.schemas.InitialSupplier`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: supplier and sku given), Decision table (supplier given, manufacturer omitted) |
| **Priority** | P1 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `admin`; Settings: None; Data: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: depends on how the supplier is created (Q-REL-06) and on which fields are required (Q-REL-07). |
| **Review** | Draft · Open question: Q-REL-06, Q-REL-07 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin` | `{"name": "QA-<suffix> Sourced Part", "purchaseable": true, "initial_supplier": {"supplier": <supplier pk>, "sku": "QA-<suffix>-SKU-5"}}` | `201 Created`. `name` equals the payload; `initial_supplier` is not in the response (write-only). |
| 2 | `GET /api/company/part/` as `admin` | `part=<pk from step 1>`, `limit=10` | `200 OK`. Supplier information was added for the part: Not known: depends on open question Q-REL-07 (whether a supplier part with `supplier` and `SKU` equal to the payload is the result). |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); delete any supplier part created in step 1 (`DELETE /api/company/part/<pk>/`) and the supplier company.

**Notes:** None.

**Duplicate check:** 69 · Review · matches: [API-REL-038](relationships.md) (69)

**Duplicate judgement:** Keep · Differs from API-REL-038 in decision-table column and outcome: supplier and SKU only vs supplier plus manufacturer and MPN (a manufacturer part is also expected there). · test-case-reviewer, 2026-10-14

### API-REL-038: Create a part with `initial_supplier` supplier, SKU, manufacturer and MPN

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with all four `initial_supplier` fields adds supplier and manufacturer information for the new part. |
| **Requirement** | R-REL-09 ([openapi-parts.yaml#L4354](../../requirements/openapi-parts.yaml#L4354), [openapi-parts.yaml#L3731](../../requirements/openapi-parts.yaml#L3731)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.InitialSupplier` (`supplier`, `sku`, `manufacturer`, `mpn`). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: all fields given), Decision table (supplier and manufacturer both given) |
| **Priority** | P2 |
| **Tags** | Regression, Cross-functional |
| **Prerequisites** | User: `admin`; Settings: None; Data: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); manufacturer company `QA-<suffix> Manufacturer` created as `admin` (same limits as the supplier); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: depends on Q-REL-06 and Q-REL-07. |
| **Review** | Draft · Open question: Q-REL-06, Q-REL-07 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin` | `{"name": "QA-<suffix> Sourced Part 2", "purchaseable": true, "initial_supplier": {"supplier": <supplier pk>, "sku": "QA-<suffix>-SKU-6", "manufacturer": <manufacturer pk>, "mpn": "QA-<suffix>-MPN-6"}}` | `201 Created`. `name` equals the payload. |
| 2 | `GET /api/company/part/` as `admin` | `part=<pk from step 1>`, `limit=10` | `200 OK`. Not known: depends on open question Q-REL-07 (how the supplier and manufacturer information appears (supplier part `SKU`, `manufacturer_part`, `MPN`)). |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); delete any supplier or manufacturer part created in step 1, then both companies.

**Notes:** None.

**Duplicate check:** 69 · Review · matches: [API-REL-037](relationships.md) (69)

**Duplicate judgement:** Keep · Differs from API-REL-037 in decision-table column and outcome: manufacturer and MPN also given, so manufacturer information is expected besides the supplier part. · test-case-reviewer, 2026-10-14

### API-REL-039: Create a part with `initial_supplier` left blank

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `initial_supplier` holding `supplier` `null` and `manufacturer` `null` skips supplier creation: the part is created and no supplier part exists. |
| **Requirement** | R-REL-09 ([openapi-parts.yaml#L4354](../../requirements/openapi-parts.yaml#L4354), [openapi-parts.yaml#L3731](../../requirements/openapi-parts.yaml#L3731)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.InitialSupplier.supplier` ("leave blank to skip", `nullable`), `components.schemas.InitialSupplier.manufacturer`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: blank supplier and manufacturer), Boundary value analysis (nullable) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> No Supplier", "initial_supplier": {"supplier": null, "manufacturer": null}}` | `201 Created`. `name` equals the payload. |
| 2 | `GET /api/company/part/` as `engineer` | `part=<pk from step 1>`, `limit=10` | `200 OK`. `count` is `0`: no supplier part was created. |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`).

**Notes:** `engineer` has no purchase-order permission (test-cases/findings.md#F-03); if the supplier-part list is refused for `engineer`, run step 2 as `admin`.

### API-REL-040: Create a part with `initial_supplier` for a supplier that does not exist

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with an `initial_supplier.supplier` that refers to no company is checked. |
| **Requirement** | R-REL-09 ([openapi-parts.yaml#L4354](../../requirements/openapi-parts.yaml#L4354), [openapi-parts.yaml#L3731](../../requirements/openapi-parts.yaml#L3731)), response to a missing ID not stated. Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.InitialSupplier.supplier`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: ID not found), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: A non-existent supplier ID: create `QA-<suffix> Gone Supplier` as `admin` (see Q-REL-06), delete it, and reuse its `pk`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome is not known yet. |
| **Review** | Draft · Open question: Q-REL-01, Q-REL-06, Q-REL-07 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin` | `{"name": "QA-<suffix> Bad Supplier", "purchaseable": true, "initial_supplier": {"supplier": <deleted supplier pk>, "sku": "QA-<suffix>-SKU-7"}}` | Not known: depends on open question Q-REL-01 (whether the request is rejected and the status code and error body for an ID that does not exist). |
| 2 | `GET /api/part/` as `admin` | `search=QA-<suffix> Bad Supplier`, `limit=10` | `200 OK`. Not known: depends on open question Q-REL-01 (whether the part exists after a rejected request). |

**Postconditions and cleanup:** If a part exists after step 1: As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`).

**Notes:** None.

### API-REL-041: Create a part with `initial_supplier` SKU but no supplier

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `initial_supplier` holding a `sku` and no `supplier` is checked: which fields are required is not stated. |
| **Requirement** | R-REL-09 ([openapi-parts.yaml#L4354](../../requirements/openapi-parts.yaml#L4354), [openapi-parts.yaml#L3731](../../requirements/openapi-parts.yaml#L3731)), required fields not stated. Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.InitialSupplier` (no `required` list). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: sku without supplier), Decision table (sku given, supplier omitted) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome is not known yet. |
| **Review** | Draft · Open question: Q-REL-07 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Sku Only", "initial_supplier": {"sku": "QA-<suffix>-SKU-8"}}` | Not known: depends on open question Q-REL-07 (whether the part is created, whether the `sku` is ignored, and the status and body if rejected). |

**Postconditions and cleanup:** If a part was created: As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`).

**Notes:** None.

### API-REL-042: Create a part with a 101-character `initial_supplier.sku`

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `initial_supplier.sku` of 101 characters (`maxLength` + 1) is not accepted. |
| **Requirement** | R-REL-09 ([openapi-parts.yaml#L4354](../../requirements/openapi-parts.yaml#L4354), [openapi-parts.yaml#L3731](../../requirements/openapi-parts.yaml#L3731)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.InitialSupplier.sku` (`maxLength: 100`). |
| **Area** | REL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (sku maxLength + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: supplier company `QA-<suffix> Supplier` created as `admin` (the company endpoint is outside the schema slice: the request body is not documented, see Q-REL-06); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01, Q-REL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin` | `{"name": "QA-<suffix> Long Sku", "purchaseable": true, "initial_supplier": {"supplier": <supplier pk>, "sku": "<101 characters>"}}` | No supplier part with a 101-character `SKU` exists. Not known: depends on open question Q-REL-01 (status code and error body for a value over `maxLength`, and whether the part itself is created). |

**Postconditions and cleanup:** If a part was created: As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); delete the supplier company.

**Notes:** None.

### API-REL-043: Create a variant with `variant_of` set to a template part

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `variant_of` set to a template part creates a part that references its template. |
| **Requirement** | R-REL-10 ([openapi-parts.yaml#L4242](../../requirements/openapi-parts.yaml#L4242), [openapi-parts.yaml#L4212](../../requirements/openapi-parts.yaml#L4212)); cross-reference R-Part_Template-03, R-Part_Template-05 (Templates_and_Variants inventory). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.variant_of`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: existing template ID), State transition (template to template with variant) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: template part `QA-<suffix> Template` created with `POST /api/part/` and `is_template` `true`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Variant", "variant_of": <template pk>}` | `201 Created`. `variant_of` equals the template `pk`. |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `variant_of` equals the template `pk`. |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`) for the variant, then for the template.

**Notes:** The response omits `category_name` for a part without category (test-cases/findings.md#F-11).

### API-REL-044: Clear `variant_of` with null

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with `variant_of` `null` is accepted (the field is nullable) and the part is no longer a variant. |
| **Requirement** | R-REL-10 ([openapi-parts.yaml#L4242](../../requirements/openapi-parts.yaml#L4242), [openapi-parts.yaml#L4212](../../requirements/openapi-parts.yaml#L4212)). Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Part.variant_of` (`nullable: true`). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: null), State transition (variant to standalone) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: template part `QA-<suffix> Template` created with `POST /api/part/` and `is_template` `true`; variant `QA-<suffix> Variant` created with `variant_of` = the template `pk`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<variant pk>/` as `engineer` | `{"variant_of": null}` | `200 OK`. `variant_of` is `null`. |
| 2 | `GET /api/part/<variant pk>/` as `engineer` | None | `200 OK`. `variant_of` is `null`. |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`) for the variant, then for the template.

**Notes:** None.

**Duplicate check:** 56 · Review · matches: [API-REL-012](relationships.md) (56), [API-REL-004](relationships.md) (54)

**Duplicate judgement:** Keep · Differs from API-REL-012 and API-REL-004 in field and rule: `variant_of` (R-REL-10) vs `default_location` (R-REL-03) and `category` (R-REL-01), with a template/variant starting state. · test-case-reviewer, 2026-10-14

### API-REL-045: Create a part with a `variant_of` ID that does not exist

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a `variant_of` that refers to no part is not accepted and no part is created. |
| **Requirement** | R-REL-10 ([openapi-parts.yaml#L4242](../../requirements/openapi-parts.yaml#L4242), [openapi-parts.yaml#L4212](../../requirements/openapi-parts.yaml#L4212)), response to a missing ID not stated. Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.variant_of`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: ID not found), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: A non-existent part ID: create `QA-<suffix> Gone Part`, `PATCH` it inactive, `DELETE` it (as `admin`), and reuse its `pk`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Lost Variant", "variant_of": <deleted part pk>}` | A part is not created. Not known: depends on open question Q-REL-01 (status code and error body for a part ID that does not exist). |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> Lost Variant`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** None if rejected. If step 1 created a part: As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`).

**Notes:** None.

**Duplicate check:** 89 · Review · matches: [API-REL-050](relationships.md) (89, test data differs), [API-REL-013](relationships.md) (69), [API-REL-005](relationships.md) (67), [API-REL-007](relationships.md) (54)

**Duplicate judgement:** Keep · Differs from API-REL-050 in clause of R-REL-10 (`variant_of` vs `revision_of`, separate fields with separate restrictions), and from API-REL-013/005/007 in field and rule. · test-case-reviewer, 2026-10-14

### API-REL-046: Create a variant of a part that is not a template

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `variant_of` set to a part whose `is_template` is `false` is checked. |
| **Requirement** | R-REL-10 ([openapi-parts.yaml#L4242](../../requirements/openapi-parts.yaml#L4242), [openapi-parts.yaml#L4212](../../requirements/openapi-parts.yaml#L4212)), restrictions on the link not stated in the schema; cross-reference R-Part_Template-03 (variants only once the Template option is on). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.variant_of`, `components.schemas.Part.is_template`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Decision table (parent is_template = false), State transition (blocked template link) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: part `QA-<suffix> Plain` created with `POST /api/part/` (`is_template` `false`); Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome is not known yet. |
| **Review** | Draft · Open question: Q-REL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Variant Of Plain", "variant_of": <Plain pk>}` | Not known: depends on open question Q-REL-08 (whether the API refuses a variant of a part that is not a template, and the status and body). |

**Postconditions and cleanup:** If step 1 created a part: As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then for `QA-<suffix> Plain`.

**Notes:** The docs say variants can be created once the Template option is on (UI); how the API enforces it is not stated.

### API-REL-047: Set a part as its own variant

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with `variant_of` equal to the part's own `pk` is checked: a circular reference. |
| **Requirement** | R-REL-10 ([openapi-parts.yaml#L4242](../../requirements/openapi-parts.yaml#L4242), [openapi-parts.yaml#L4212](../../requirements/openapi-parts.yaml#L4212)), restrictions on the link not stated. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Part.variant_of`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Error guessing (self reference), State transition (blocked change) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: template part `QA-<suffix> Template` created with `POST /api/part/` and `is_template` `true`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome is not known yet. |
| **Review** | Draft · Open question: Q-REL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<template pk>/` as `engineer` | `{"variant_of": <the same pk>}` | Not known: depends on open question Q-REL-08 (whether a part may reference itself as its template, and the status and body). |
| 2 | `GET /api/part/<template pk>/` as `engineer` | None | `200 OK`. Not known: depends on open question Q-REL-08 (whether `variant_of` is unchanged after the attempt). |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`).

**Notes:** None.

**Duplicate check:** 52 · Review · matches: [API-REL-051](relationships.md) (52)

**Duplicate judgement:** Keep · Differs from API-REL-051 in clause and outcome: `variant_of` self-reference on a template (outcome open, Q-REL-08) vs `revision_of` self-reference, which the docs forbid (R-REV-06). · test-case-reviewer, 2026-10-14

### API-REL-048: Create a part with `revision_of` null

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `revision_of` `null` is accepted (the field is nullable) and the new part is not a revision. |
| **Requirement** | R-REL-10 ([openapi-parts.yaml#L4242](../../requirements/openapi-parts.yaml#L4242), [openapi-parts.yaml#L4212](../../requirements/openapi-parts.yaml#L4212)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.revision_of` (`nullable: true`). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: null) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Original", "revision_of": null}` | `201 Created`. `revision_of` is `null`. |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`).

**Notes:** None.

### API-REL-049: Create a part with `revision_of` set to an existing part

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `revision_of` set to an existing part and a `revision` code: the outcome and the stored reference are checked. |
| **Requirement** | R-REL-10 ([openapi-parts.yaml#L4242](../../requirements/openapi-parts.yaml#L4242), [openapi-parts.yaml#L4212](../../requirements/openapi-parts.yaml#L4212)), conditions for a revision not stated here; cross-reference REV inventory (R-REV-01). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.revision_of`, `components.schemas.Part.revision`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: existing part ID), State transition (original to original with a revision) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer`; Settings: `PART_ENABLE_REVISION` and `PART_REVISION_ASSEMBLY_ONLY`: the settings the docs name but do not render; state them in the run (Q-REL-08); Data: part `QA-<suffix> Original` created with `POST /api/part/` (`assembly` `true`); Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome depends on the revision settings (Q-REL-08). |
| **Review** | Draft · Open question: Q-REL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Original", "revision": "B", "revision_of": <Original pk>}` | Not known: depends on open question Q-REL-08 (whether the request is accepted with the default revision settings, and the status and body if refused). If accepted: `201 Created`, and `revision_of` equals the Original `pk`. |
| 2 | `GET /api/part/<Original pk>/` as `engineer` | None | `200 OK`. `revision_count` is an integer (read-only). Not known: depends on open question Q-REL-08 (the `revision_count` value after the revision is created). |

**Postconditions and cleanup:** Delete both parts as `admin` (`PATCH` inactive, `DELETE`).

**Notes:** Revision settings are unrendered macros in the docs (index, Doc issue 8).

### API-REL-050: Create a part with a `revision_of` ID that does not exist

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a `revision_of` that refers to no part is not accepted and no part is created. |
| **Requirement** | R-REL-10 ([openapi-parts.yaml#L4242](../../requirements/openapi-parts.yaml#L4242), [openapi-parts.yaml#L4212](../../requirements/openapi-parts.yaml#L4212)), response to a missing ID not stated. Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.revision_of`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: ID not found), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: A non-existent part ID: create `QA-<suffix> Gone Part`, `PATCH` it inactive, `DELETE` it (as `admin`), and reuse its `pk`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Lost Revision", "revision": "B", "revision_of": <deleted part pk>}` | A part is not created. Not known: depends on open question Q-REL-01 (status code and error body for a part ID that does not exist). |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> Lost Revision`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** None if rejected. If step 1 created a part: As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`).

**Notes:** None.

**Duplicate check:** 89 · Review · matches: [API-REL-045](relationships.md) (89, test data differs), [API-REL-013](relationships.md) (69), [API-REL-005](relationships.md) (67), [API-REL-007](relationships.md) (54)

**Duplicate judgement:** Keep · Differs from API-REL-045 in clause of R-REL-10 (`revision_of` vs `variant_of`), and from API-REL-013/005/007 in field and rule. · test-case-reviewer, 2026-10-14

### API-REL-051: Set a part as a revision of itself

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with `revision_of` equal to the part's own `pk` is not accepted: a part cannot be a revision of itself. |
| **Requirement** | R-REL-10 ([openapi-parts.yaml#L4242](../../requirements/openapi-parts.yaml#L4242), [openapi-parts.yaml#L4212](../../requirements/openapi-parts.yaml#L4212)); cross-reference R-REV-06 (REV inventory, [part-revision.md#L36](../../requirements/docs/part-revision.md#L36)). Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Part.revision_of`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Negative (forbidden self reference), Error guessing |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer`; Settings: None; Data: part `QA-<suffix> Part` created with `POST /api/part/`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known (R-REV-06: error text not stated). |
| **Review** | Draft · Open question: Q-REL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<part pk>/` as `engineer` | `{"revision_of": <the same pk>}` | The change is not accepted (a part cannot be a revision of itself). Not known: depends on open question Q-REL-08 (status code and error body for a self-referencing `revision_of`). |
| 2 | `GET /api/part/<part pk>/` as `engineer` | None | `200 OK`. `revision_of` is `null`. |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`).

**Notes:** None.

**Duplicate check:** 52 · Review · matches: [API-REL-047](relationships.md) (52)

**Duplicate judgement:** Keep · Differs from API-REL-047 in clause and outcome: `revision_of` self-reference, refused per R-REV-06, vs `variant_of` self-reference with an open outcome. · test-case-reviewer, 2026-10-14

### API-REL-052: Edit a locked part with locking enabled

| Field | Value |
|---|---|
| **Summary** | With `PART_ENABLE_LOCKING` on, `PATCH /api/part/{id}/` on a locked part is not accepted and the part is unchanged. |
| **Requirement** | R-REL-11 ([openapi-parts.yaml#L4185](../../requirements/openapi-parts.yaml#L4185), [part-index.md#L108](../../requirements/docs/part-index.md#L108), [part-index.md#L112](../../requirements/docs/part-index.md#L112)). Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Part.locked`. Docs: [part-index.md#L104-L113](../../requirements/docs/part-index.md#L104). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | State transition (locked part, edit blocked), Decision table (locking setting on, part locked) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Settings-dependent |
| **Prerequisites** | User: `admin`; Settings: `PART_ENABLE_LOCKING` = on (set as `admin`; the settings endpoint is outside the schema slice, default not stated: Q-REL-09); Data: part `QA-<suffix> Locked Part` created with `POST /api/part/` and `locked` `true`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<part pk>/` as `admin` | `{"description": "QA-<suffix> changed"}` | The part is not edited ("Locked parts cannot be edited"). Not known: depends on open question Q-REL-09 (status code and error body for an edit of a locked part). |
| 2 | `GET /api/part/<part pk>/` as `admin` | None | `200 OK`. `description` is unchanged and `locked` is `true`. |

**Postconditions and cleanup:** Set `locked` `false` (see case on unlocking, Q-REL-09), then As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`). Restore `PART_ENABLE_LOCKING` to its starting value.

**Notes:** Locked parts cannot be deleted either (docs); that is the next case.

### API-REL-053: Delete a locked part with locking enabled

| Field | Value |
|---|---|
| **Summary** | With `PART_ENABLE_LOCKING` on, `DELETE /api/part/{id}/` on a locked, inactive part is not accepted and the part still exists. |
| **Requirement** | R-REL-11 ([openapi-parts.yaml#L4185](../../requirements/openapi-parts.yaml#L4185), [part-index.md#L108](../../requirements/docs/part-index.md#L108), [part-index.md#L112](../../requirements/docs/part-index.md#L112)). Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/`. Docs: [part-index.md#L108](../../requirements/docs/part-index.md#L108) ("Locked parts cannot be deleted"). Inactive first: Q-CRUD-02 (answered). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | State transition (locked part, delete blocked), Decision table (locking on, part locked, part inactive) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `admin`; Settings: `PART_ENABLE_LOCKING` = on (set as `admin`; default not stated: Q-REL-09); Data: part `QA-<suffix> Locked Part` created with `POST /api/part/`, then set `active` `false` and `locked` `true` with `PATCH` (as `admin`); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the error status and body are not known yet. |
| **Review** | Draft · Open question: Q-REL-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<part pk>/` as `admin` | None | The part is not deleted. Not known: depends on open question Q-REL-09 (status code and error body for a delete of a locked part). |
| 2 | `GET /api/part/<part pk>/` as `admin` | None | `200 OK`. The part still exists with `locked` `true`. |

**Postconditions and cleanup:** Unlock (Q-REL-09), `DELETE /api/part/<pk>/` (`204`). Restore `PART_ENABLE_LOCKING`.

**Notes:** The part is made inactive first, so the active-part refusal (Q-CRUD-02) is not what blocks the delete.

### API-REL-054: Unlock a locked part with locking enabled

| Field | Value |
|---|---|
| **Summary** | With `PART_ENABLE_LOCKING` on, `PATCH /api/part/{id}/` setting `locked` `false` on a locked part: whether the unlock itself is allowed is checked. |
| **Requirement** | R-REL-11 ([openapi-parts.yaml#L4185](../../requirements/openapi-parts.yaml#L4185), [part-index.md#L108](../../requirements/docs/part-index.md#L108), [part-index.md#L112](../../requirements/docs/part-index.md#L112)), how a part is locked or unlocked is not described (index, Doc issue 12). Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Part.locked`. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | State transition (locked to unlocked), What-if business scenario (unlocking a part in production) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `admin`; Settings: `PART_ENABLE_LOCKING` = on (set as `admin`; default not stated: Q-REL-09); Data: part `QA-<suffix> Locked Part` created with `POST /api/part/`, then set `active` `false` and `locked` `true` with `PATCH` (as `admin`); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome is not known yet. |
| **Review** | Draft · Open question: Q-REL-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<part pk>/` as `admin` | `{"locked": false}` | Not known: depends on open question Q-REL-09 (whether a locked part can be unlocked through the API while locking is on, and the status and body if not). |
| 2 | `GET /api/part/<part pk>/` as `admin` | None | `200 OK`. Not known: depends on open question Q-REL-09 (the value of `locked` after the attempt). |

**Postconditions and cleanup:** Make sure the part is unlocked, then `DELETE /api/part/<pk>/` (`204`). Restore `PART_ENABLE_LOCKING`.

**Notes:** None.

### API-REL-055: Edit a locked part with locking disabled

| Field | Value |
|---|---|
| **Summary** | With `PART_ENABLE_LOCKING` off, the locked state is ignored: `PATCH /api/part/{id}/` on a locked part is accepted. |
| **Requirement** | R-REL-11 ([openapi-parts.yaml#L4185](../../requirements/openapi-parts.yaml#L4185), [part-index.md#L108](../../requirements/docs/part-index.md#L108), [part-index.md#L112](../../requirements/docs/part-index.md#L112)). Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.Part.locked`. Docs: [part-index.md#L112](../../requirements/docs/part-index.md#L112) ("the locked state of a part is ignored and all operations are permitted"). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Decision table (locking setting off, part locked) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `admin`; Settings: `PART_ENABLE_LOCKING` = off (set as `admin`; the settings endpoint is outside the schema slice: Q-REL-09); Data: part `QA-<suffix> Locked Part` created with `POST /api/part/` and `locked` `true`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: depends on how the setting is changed (Q-REL-09). |
| **Review** | Draft · Open question: Q-REL-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<part pk>/` as `admin` | `{"description": "QA-<suffix> changed"}` | `200 OK`. `description` equals the payload; `locked` is still `true`. |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`) (inactivating is an edit and is also allowed while locking is off). Restore `PART_ENABLE_LOCKING`.

**Notes:** None.

### API-REL-056: Delete a locked part with locking disabled

| Field | Value |
|---|---|
| **Summary** | With `PART_ENABLE_LOCKING` off, `DELETE /api/part/{id}/` on a locked, inactive part is accepted. |
| **Requirement** | R-REL-11 ([openapi-parts.yaml#L4185](../../requirements/openapi-parts.yaml#L4185), [part-index.md#L108](../../requirements/docs/part-index.md#L108), [part-index.md#L112](../../requirements/docs/part-index.md#L112)). Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/`. Docs: [part-index.md#L112](../../requirements/docs/part-index.md#L112). Inactive first: Q-CRUD-02 (answered). |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | Decision table (locking setting off, part locked, part inactive) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `admin`; Settings: `PART_ENABLE_LOCKING` = off (set as `admin`; Q-REL-09); Data: part `QA-<suffix> Locked Part` created with `POST /api/part/`, then set `active` `false` and `locked` `true` with `PATCH` (as `admin`); Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: depends on how the setting is changed (Q-REL-09). |
| **Review** | Draft · Open question: Q-REL-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<part pk>/` as `admin` | None | `204 No Content`. The body is empty. |
| 2 | `GET /api/part/<part pk>/` as `admin` | None | `404 Not Found`. |

**Postconditions and cleanup:** None: the part is deleted. Restore `PART_ENABLE_LOCKING`.

**Notes:** None.
