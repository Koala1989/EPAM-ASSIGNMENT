# Lists and filters: LST test cases

### API-LST-001: A part list request with `limit` returns the paginated envelope with `count`, `results`, `next` and `previous`.

| Field | Value |
|---|---|
| **Summary** | A part list request with `limit` returns the paginated envelope with `count`, `results`, `next` and `previous`. |
| **Requirement** | `R-LST-01` ([L432](../../requirements/openapi-parts.yaml#L432), [L3944](../../requirements/openapi-parts.yaml#L3944)), `R-LST-02` ([L578](../../requirements/openapi-parts.yaml#L578)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: limit smaller than the number of matching parts) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=2` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `3`; `results` has exactly 2 items; `next` is a non-null string; `previous` is `null`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 61 · Review · matches: [API-LST-013](lists-and-filters.md) (61), [API-LST-005](lists-and-filters.md) (51)

**Duplicate judgement:** Keep · Differs from API-LST-013 in class (`limit` sent, paginated envelope, vs `limit` omitted, plain array) and from API-LST-005 in rule clause (`limit` vs `offset`). · test-case-reviewer, 2026-10-14

### API-LST-002: `limit=1`, the smallest page, returns one part and a `next` link.

| Field | Value |
|---|---|
| **Summary** | `limit=1`, the smallest page, returns one part and a `next` link. |
| **Requirement** | `R-LST-02` ([L578](../../requirements/openapi-parts.yaml#L578)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (limit = 1) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=1`, `ordering=id` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `3`; `results` has exactly 1 item, `QA-<suffix> P1`; `next` is a non-null string. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 69 · Review · matches: [API-LST-004](lists-and-filters.md) (69), [API-LST-003](lists-and-filters.md) (68), [API-LST-009](lists-and-filters.md) (54), [API-LST-011](lists-and-filters.md) (53)

**Duplicate judgement:** Keep · `limit=1` is the lowest valid boundary; API-LST-003 (= count), API-LST-004 (count + 1), API-LST-009 (0) and API-LST-011 (far above) are different boundary points. · test-case-reviewer, 2026-10-14

### API-LST-003: A `limit` equal to the number of matching parts returns all of them on one page, with `next` null.

| Field | Value |
|---|---|
| **Summary** | A `limit` equal to the number of matching parts returns all of them on one page, with `next` null. |
| **Requirement** | `R-LST-02` ([L578](../../requirements/openapi-parts.yaml#L578)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (limit = count) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=3`, `ordering=id` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `3`; `results` has 3 items (P1, P2, P3); `next` is `null`; `previous` is `null`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 83 · Review · matches: [API-LST-004](lists-and-filters.md) (83, test data differs), [API-LST-002](lists-and-filters.md) (68), [API-LST-009](lists-and-filters.md) (54), [API-LST-011](lists-and-filters.md) (53), [API-LST-006](lists-and-filters.md) (50)

**Duplicate judgement:** Keep · On the boundary (`limit` = count) vs API-LST-004 above it (count + 1); API-LST-002/009/011 are other boundary points and API-LST-006 tests `offset`. · test-case-reviewer, 2026-10-14

### API-LST-004: A `limit` larger than the number of matching parts returns all of them on one page, with `next` null.

| Field | Value |
|---|---|
| **Summary** | A `limit` larger than the number of matching parts returns all of them on one page, with `next` null. |
| **Requirement** | `R-LST-02` ([L578](../../requirements/openapi-parts.yaml#L578)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (limit = count + 1) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=4`, `ordering=id` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `3`; `results` has 3 items; `next` is `null`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 83 · Review · matches: [API-LST-003](lists-and-filters.md) (83, test data differs), [API-LST-002](lists-and-filters.md) (69), [API-LST-009](lists-and-filters.md) (54), [API-LST-011](lists-and-filters.md) (53)

**Duplicate judgement:** Keep · Above the boundary (`limit` = count + 1) vs API-LST-003 on it; API-LST-002/009/011 are other boundary points. · test-case-reviewer, 2026-10-14

### API-LST-005: `offset` skips that many results and the page starts at the next one.

| Field | Value |
|---|---|
| **Summary** | `offset` skips that many results and the page starts at the next one. |
| **Requirement** | `R-LST-03` ([L604](../../requirements/openapi-parts.yaml#L604)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: offset inside the result set) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=2`, `offset=1`, `ordering=id` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `3`; `results` holds `QA-<suffix> P2` then `QA-<suffix> P3`; `previous` is a non-null string. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 51 · Review · matches: [API-LST-001](lists-and-filters.md) (51)

**Duplicate judgement:** Keep · Tests `offset` (R-LST-03) inside the result set; API-LST-001 tests `limit` and the envelope with no offset. · test-case-reviewer, 2026-10-14

### API-LST-006: `offset=0` starts at the first result, the same page as no offset.

| Field | Value |
|---|---|
| **Summary** | `offset=0` starts at the first result, the same page as no offset. |
| **Requirement** | `R-LST-03` ([L604](../../requirements/openapi-parts.yaml#L604)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (offset = 0) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=2`, `offset=0`, `ordering=id` | `200 OK`. Body is valid against `PaginatedPartList`. `results` holds `QA-<suffix> P1` then `QA-<suffix> P2`; `previous` is `null`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 58 · Review · matches: [API-LST-007](lists-and-filters.md) (58), [API-LST-003](lists-and-filters.md) (50)

**Duplicate judgement:** Keep · `offset=0` (lower boundary) vs API-LST-007 `offset` = count (upper boundary); API-LST-003 tests `limit`. · test-case-reviewer, 2026-10-14

### API-LST-007: An `offset` equal to `count` (one past the last result) returns an empty page.

| Field | Value |
|---|---|
| **Summary** | An `offset` equal to `count` (one past the last result) returns an empty page. |
| **Requirement** | `R-LST-03` ([L604](../../requirements/openapi-parts.yaml#L604)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (offset = count) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=2`, `offset=3` | `200 OK` is expected for an empty page, but the schema does not state it. Not known: depends on open question Q-LST-04 (status and body for an offset at or beyond `count`; `count` itself is `3`). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 58 · Review · matches: [API-LST-006](lists-and-filters.md) (58)

**Duplicate judgement:** Keep · `offset` = count (upper boundary, empty page) vs API-LST-006 `offset=0` (lower boundary, first page). · test-case-reviewer, 2026-10-14

### API-LST-008: Following `next` returns the second page and its `previous` link points back.

| Field | Value |
|---|---|
| **Summary** | Following `next` returns the second page and its `previous` link points back. |
| **Requirement** | `R-LST-01` ([L432](../../requirements/openapi-parts.yaml#L432), [L3944](../../requirements/openapi-parts.yaml#L3944)), `R-LST-02` ([L578](../../requirements/openapi-parts.yaml#L578)), `R-LST-03` ([L604](../../requirements/openapi-parts.yaml#L604)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Exploratory (page through a result set with the `next` link) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=2`, `ordering=id` | `200 OK`. `results` holds P1, P2; `next` is non-null. |
| 2 | `GET` the path and query of the `next` value from step 1 as `reader` | None (use the `next` value as returned, without its host) | `200 OK`. Body is valid against `PaginatedPartList`. `results` holds only `QA-<suffix> P3`; `next` is `null`; `previous` is non-null; `count` is `3`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

### API-LST-009: `limit=0` is handled in a defined way.

| Field | Value |
|---|---|
| **Summary** | `limit=0` is handled in a defined way. |
| **Requirement** | `R-LST-02` ([L578](../../requirements/openapi-parts.yaml#L578)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (limit = 0, just below the smallest useful page) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=0` | Not known: depends on open question Q-LST-04 (status and body for `limit=0`: error, empty page, or all parts). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 63 · Review · matches: [API-LST-011](lists-and-filters.md) (63), [API-LST-002](lists-and-filters.md) (54), [API-LST-003](lists-and-filters.md) (54), [API-LST-004](lists-and-filters.md) (54)

**Duplicate judgement:** Keep · `limit=0` sits below the lowest valid page size; API-LST-011 is far above any maximum and API-LST-002/003/004 are valid boundary points. · test-case-reviewer, 2026-10-14

### API-LST-010: A negative `limit` is handled in a defined way.

| Field | Value |
|---|---|
| **Summary** | A negative `limit` is handled in a defined way. |
| **Requirement** | `R-LST-02` ([L578](../../requirements/openapi-parts.yaml#L578)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: negative integer), Boundary value analysis (limit = -1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=-1` | Not known: depends on open question Q-LST-04 (status and body for a negative `limit`). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 70 · Review · matches: [API-LST-012](lists-and-filters.md) (70), [API-LST-041](lists-and-filters.md) (53), [API-LST-042](lists-and-filters.md) (53), [API-LST-046](lists-and-filters.md) (53), [API-LST-059](lists-and-filters.md) (53), +1 more

**Duplicate judgement:** Keep · Negative integer `limit` vs API-LST-012 non-numeric `limit` (different invalid class); API-LST-041/042/046/059 test other parameters. · test-case-reviewer, 2026-10-14

### API-LST-011: A very large `limit` is accepted or capped in a defined way.

| Field | Value |
|---|---|
| **Summary** | A very large `limit` is accepted or capped in a defined way. |
| **Requirement** | `R-LST-02` ([L578](../../requirements/openapi-parts.yaml#L578)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (limit far above any stated maximum) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=100000` | The three parts are expected, but the schema states no maximum page size. Not known: depends on open question Q-LST-04 (maximum `limit` and whether a larger value is rejected or capped). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 63 · Review · matches: [API-LST-009](lists-and-filters.md) (63), [API-LST-002](lists-and-filters.md) (53), [API-LST-003](lists-and-filters.md) (53), [API-LST-004](lists-and-filters.md) (53)

**Duplicate judgement:** Keep · `limit` far above any maximum vs API-LST-009 `limit=0`; API-LST-002/003/004 are boundaries around the record count, not the page-size maximum. · test-case-reviewer, 2026-10-14

### API-LST-012: A non-integer `limit` is rejected or ignored in a defined way.

| Field | Value |
|---|---|
| **Summary** | A non-integer `limit` is rejected or ignored in a defined way. |
| **Requirement** | `R-LST-02` ([L578](../../requirements/openapi-parts.yaml#L578)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type, non-numeric string) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=abc` | Not known: depends on open question Q-LST-09 (status and body for a non-integer `limit`). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 70 · Review · matches: [API-LST-010](lists-and-filters.md) (70), [API-LST-042](lists-and-filters.md) (57), [API-LST-059](lists-and-filters.md) (56), [API-LST-046](lists-and-filters.md) (55), [API-LST-041](lists-and-filters.md) (53)

**Duplicate judgement:** Keep · Wrong type (non-numeric) `limit` vs API-LST-010 negative integer; API-LST-041/042/046/059 send invalid values to other parameters. · test-case-reviewer, 2026-10-14

### API-LST-013: Without `limit` the part list is a plain JSON array of all matching parts, not the paginated envelope.

| Field | Value |
|---|---|
| **Summary** | Without `limit` the part list is a plain JSON array of all matching parts, not the paginated envelope. |
| **Requirement** | `R-LST-01` ([L432](../../requirements/openapi-parts.yaml#L432), [L3944](../../requirements/openapi-parts.yaml#L3944)), `R-LST-02` ([L578](../../requirements/openapi-parts.yaml#L578)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: no `limit`; observed behaviour, Schema issue 8) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>` (no `limit`) | `200 OK`. Body is a JSON array (not an object) with 3 items, each valid against `Part`: P1, P2, P3. It is not valid against `PaginatedPartList`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** Documented as paginated, returned as an array: `test-cases/findings.md#F-09`, index Schema issue 8 (answered).

**Duplicate check:** 61 · Review · matches: [API-LST-001](lists-and-filters.md) (61)

**Duplicate judgement:** Keep · `limit` omitted (plain array) vs API-LST-001 `limit` sent (paginated envelope): different class and expected outcome. · test-case-reviewer, 2026-10-14

### API-LST-014: A category list request with `limit` returns the paginated envelope.

| Field | Value |
|---|---|
| **Summary** | A category list request with `limit` returns the paginated envelope. |
| **Requirement** | `R-LST-14` ([L848](../../requirements/openapi-parts.yaml#L848)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: limit smaller than the number of matching categories) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Root` and its children `QA-<suffix> Cat Two` (2 parts), `QA-<suffix> Cat One` (1 part) and `QA-<suffix> Cat Zero` (no parts), created with `POST /api/part/category/` and `POST /api/part/` as `admin` (parts named `QA-<suffix> CP1` to `CP3`); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `parent=<Root pk>`, `limit=2` | `200 OK`. Body is valid against `PaginatedCategoryList`. `count` is `3`; `results` has exactly 2 items; `next` is a non-null string; `previous` is `null`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 65 · Review · matches: [API-LST-016](lists-and-filters.md) (65), [API-LST-015](lists-and-filters.md) (61), [API-LST-024](lists-and-filters.md) (59), [API-LST-023](lists-and-filters.md) (58)

**Duplicate judgement:** Keep · Category list with `limit` only (envelope) vs API-LST-016 `offset`, API-LST-015 no `limit` (array) and API-LST-023/024 `ordering`. · test-case-reviewer, 2026-10-14

### API-LST-015: Without `limit` the category list is a plain JSON array.

| Field | Value |
|---|---|
| **Summary** | Without `limit` the category list is a plain JSON array. |
| **Requirement** | `R-LST-14` ([L848](../../requirements/openapi-parts.yaml#L848)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: no `limit`; observed behaviour, Schema issue 8) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Root` and its children `QA-<suffix> Cat Two` (2 parts), `QA-<suffix> Cat One` (1 part) and `QA-<suffix> Cat Zero` (no parts), created with `POST /api/part/category/` and `POST /api/part/` as `admin` (parts named `QA-<suffix> CP1` to `CP3`); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `parent=<Root pk>` (no `limit`) | `200 OK`. Body is a JSON array with 3 items (Cat Two, Cat One, Cat Zero), each valid against `Category`. It is not valid against `PaginatedCategoryList`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** `test-cases/findings.md#F-09`, index Schema issue 8 (answered).

**Duplicate check:** 64 · Review · matches: [API-LST-016](lists-and-filters.md) (64), [API-LST-014](lists-and-filters.md) (61), [API-LST-023](lists-and-filters.md) (61), [API-LST-024](lists-and-filters.md) (60)

**Duplicate judgement:** Keep · Category list without `limit` (plain array) vs API-LST-014/016 with `limit` (envelope) and API-LST-023/024 `ordering`. · test-case-reviewer, 2026-10-14

### API-LST-016: `offset` works on the category list.

| Field | Value |
|---|---|
| **Summary** | `offset` works on the category list. |
| **Requirement** | `R-LST-14` ([L848](../../requirements/openapi-parts.yaml#L848)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: offset inside the result set) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Root` and its children `QA-<suffix> Cat Two` (2 parts), `QA-<suffix> Cat One` (1 part) and `QA-<suffix> Cat Zero` (no parts), created with `POST /api/part/category/` and `POST /api/part/` as `admin` (parts named `QA-<suffix> CP1` to `CP3`); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `parent=<Root pk>`, `limit=2`, `offset=2`, `ordering=name` | `200 OK`. Body is valid against `PaginatedCategoryList`. `count` is `3`; `results` has 1 item, `QA-<suffix> Cat Zero` (the third by name: Cat One, Cat Two, Cat Zero). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 65 · Review · matches: [API-LST-014](lists-and-filters.md) (65), [API-LST-023](lists-and-filters.md) (65), [API-LST-015](lists-and-filters.md) (64), [API-LST-024](lists-and-filters.md) (63)

**Duplicate judgement:** Keep · Category `offset` vs API-LST-014 `limit` only, API-LST-015 no `limit`, and API-LST-023/024 ordering checks. · test-case-reviewer, 2026-10-14

### API-LST-017: `ordering=name` sorts parts by name ascending.

| Field | Value |
|---|---|
| **Summary** | `ordering=name` sorts parts by name ascending. |
| **Requirement** | `R-LST-05` ([L615](../../requirements/openapi-parts.yaml#L615)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: ascending value) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Order Cat` and three parts `QA-<suffix> Banana`, `QA-<suffix> Apple`, `QA-<suffix> Cherry` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=name` | `200 OK`. Body is valid against `PaginatedPartList`. `results` names, in order: `QA-<suffix> Apple`, `QA-<suffix> Banana`, `QA-<suffix> Cherry`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 86 · Duplicate · matches: [API-LST-018](lists-and-filters.md) (86), [API-LST-019](lists-and-filters.md) (77), [API-LST-020](lists-and-filters.md) (55), [API-LST-036](lists-and-filters.md) (50)

**Duplicate judgement:** Keep · Ascending `name` vs API-LST-018 descending (`-` prefix clause of R-LST-05), API-LST-019 a different field (`-id`), API-LST-020 status-only sweep, API-LST-036 a different rule (`category`). · test-case-reviewer, 2026-10-14

### API-LST-018: `ordering=-name` reverses the order to descending.

| Field | Value |
|---|---|
| **Summary** | `ordering=-name` reverses the order to descending. |
| **Requirement** | `R-LST-05` ([L615](../../requirements/openapi-parts.yaml#L615)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: `-` prefix) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Order Cat` and three parts `QA-<suffix> Banana`, `QA-<suffix> Apple`, `QA-<suffix> Cherry` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=-name` | `200 OK`. Body is valid against `PaginatedPartList`. `results` names, in order: `QA-<suffix> Cherry`, `QA-<suffix> Banana`, `QA-<suffix> Apple`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 86 · Duplicate · matches: [API-LST-017](lists-and-filters.md) (86), [API-LST-019](lists-and-filters.md) (77), [API-LST-020](lists-and-filters.md) (55)

**Duplicate judgement:** Keep · Descending (`-` prefix clause of R-LST-05) vs API-LST-017 ascending; API-LST-019 orders by `id`; API-LST-020 checks status only, not order. · test-case-reviewer, 2026-10-14

### API-LST-019: `ordering=-id` lists the newest part first.

| Field | Value |
|---|---|
| **Summary** | `ordering=-id` lists the newest part first. |
| **Requirement** | `R-LST-05` ([L615](../../requirements/openapi-parts.yaml#L615)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: `-id`) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Order Cat` and three parts `QA-<suffix> Banana`, `QA-<suffix> Apple`, `QA-<suffix> Cherry` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=-id` | `200 OK`. Body is valid against `PaginatedPartList`. `results` names, in order: `QA-<suffix> Cherry`, `QA-<suffix> Apple`, `QA-<suffix> Banana` (reverse creation order). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 77 · Review · matches: [API-LST-017](lists-and-filters.md) (77), [API-LST-018](lists-and-filters.md) (77), [API-LST-020](lists-and-filters.md) (54)

**Duplicate judgement:** Keep · Orders by `id` (creation order, differs from name order in the data) vs API-LST-017/018 by `name`; API-LST-020 does not assert order. · test-case-reviewer, 2026-10-14

### API-LST-020: Every `ordering` value listed in the schema, with and without the `-` prefix, is accepted.

| Field | Value |
|---|---|
| **Summary** | Every `ordering` value listed in the schema, with and without the `-` prefix, is accepted. |
| **Requirement** | `R-LST-05` ([L615](../../requirements/openapi-parts.yaml#L615)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (each `enum` member), Decision table (value x prefix) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Order Cat` and three parts `QA-<suffix> Banana`, `QA-<suffix> Apple`, `QA-<suffix> Cherry` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=id` then `ordering=-id` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 2 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=name` then `ordering=-name` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 3 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=creation_date` then `ordering=-creation_date` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 4 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=IPN` then `ordering=-IPN` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 5 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=ordering` then `ordering=-ordering` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 6 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=in_stock` then `ordering=-in_stock` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 7 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=total_in_stock` then `ordering=-total_in_stock` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 8 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=unallocated_stock` then `ordering=-unallocated_stock` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 9 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=category` then `ordering=-category` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 10 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=default_location` then `ordering=-default_location` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 11 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=units` then `ordering=-units` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 12 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=pricing_min` then `ordering=-pricing_min` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 13 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=pricing_max` then `ordering=-pricing_max` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 14 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=pricing_updated` then `ordering=-pricing_updated` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 15 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=revision` then `ordering=-revision` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |
| 16 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=revision_count` then `ordering=-revision_count` (two calls) | `200 OK` for both calls. Body is valid against `PaginatedPartList`; `count` is `3`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** Sixteen steps, one per field. Only the status and envelope are checked: the sort order of fields with no stored values is not asserted.

**Duplicate check:** 55 · Review · matches: [API-LST-017](lists-and-filters.md) (55), [API-LST-018](lists-and-filters.md) (55), [API-LST-019](lists-and-filters.md) (54), [API-LST-056](lists-and-filters.md) (50)

**Duplicate judgement:** Keep · Checks that every `enum` value and its `-` form is accepted (status and envelope) vs API-LST-017/018/019, which assert the order of one field; API-LST-056 is a different rule (dates). · test-case-reviewer, 2026-10-14

### API-LST-021: An `ordering` value that is not in the schema's list is handled in a defined way.

| Field | Value |
|---|---|
| **Summary** | An `ordering` value that is not in the schema's list is handled in a defined way. |
| **Requirement** | `R-LST-05` ([L615](../../requirements/openapi-parts.yaml#L615)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: value outside the `enum`) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Order Cat` and three parts `QA-<suffix> Banana`, `QA-<suffix> Apple`, `QA-<suffix> Cherry` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=notafield` | Not known: depends on open question Q-LST-01 (status and body for an `ordering` value outside the `enum`: error, or ignored with the default order). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 76 · Review · matches: [API-LST-022](lists-and-filters.md) (76), [API-LST-041](lists-and-filters.md) (52), [API-LST-046](lists-and-filters.md) (51), [API-LST-010](lists-and-filters.md) (50), [API-LST-042](lists-and-filters.md) (50), +1 more

**Duplicate judgement:** Keep · A name that is no field at all vs API-LST-022 a real `Part` field outside the whitelist (Q-LST-01 asks about both separately); API-LST-010/041/042/046 test other parameters. · test-case-reviewer, 2026-10-14

### API-LST-022: A real part field that is not in the `ordering` list (`description`) is handled like any other unlisted value.

| Field | Value |
|---|---|
| **Summary** | A real part field that is not in the `ordering` list (`description`) is handled like any other unlisted value. |
| **Requirement** | `R-LST-05` ([L615](../../requirements/openapi-parts.yaml#L615)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Error guessing (valid field name, not in the `enum`) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Order Cat` and three parts `QA-<suffix> Banana`, `QA-<suffix> Apple`, `QA-<suffix> Cherry` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `ordering=description` | Not known: depends on open question Q-LST-01 (status and body for an `ordering` value outside the `enum`). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 76 · Review · matches: [API-LST-021](lists-and-filters.md) (76), [API-LST-042](lists-and-filters.md) (50), [API-LST-046](lists-and-filters.md) (50)

**Duplicate judgement:** Keep · A real `Part` field outside the `enum` (checks the whitelist is enforced) vs API-LST-021 a non-existent name; API-LST-042/046 test other parameters. · test-case-reviewer, 2026-10-14

### API-LST-023: `ordering=-name` sorts categories by name descending.

| Field | Value |
|---|---|
| **Summary** | `ordering=-name` sorts categories by name descending. |
| **Requirement** | `R-LST-14` ([L848](../../requirements/openapi-parts.yaml#L848)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: `-` prefix on a category field) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Root` and its children `QA-<suffix> Cat Two` (2 parts), `QA-<suffix> Cat One` (1 part) and `QA-<suffix> Cat Zero` (no parts), created with `POST /api/part/category/` and `POST /api/part/` as `admin` (parts named `QA-<suffix> CP1` to `CP3`); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `parent=<Root pk>`, `limit=10`, `ordering=-name` | `200 OK`. Body is valid against `PaginatedCategoryList`. `results` names, in order: `QA-<suffix> Cat Zero`, `QA-<suffix> Cat Two`, `QA-<suffix> Cat One`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 74 · Review · matches: [API-LST-024](lists-and-filters.md) (74), [API-LST-016](lists-and-filters.md) (65), [API-LST-015](lists-and-filters.md) (61), [API-LST-014](lists-and-filters.md) (58), [API-LST-034](lists-and-filters.md) (50)

**Duplicate judgement:** Keep · Orders categories by `-name` vs API-LST-024 by `-part_count` (different order expected); API-LST-014/015/016 test pagination and API-LST-034 search. · test-case-reviewer, 2026-10-14

### API-LST-024: `ordering=-part_count` lists the category with the most parts first.

| Field | Value |
|---|---|
| **Summary** | `ordering=-part_count` lists the category with the most parts first. |
| **Requirement** | `R-LST-14` ([L848](../../requirements/openapi-parts.yaml#L848)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: `part_count`, descending) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Root` and its children `QA-<suffix> Cat Two` (2 parts), `QA-<suffix> Cat One` (1 part) and `QA-<suffix> Cat Zero` (no parts), created with `POST /api/part/category/` and `POST /api/part/` as `admin` (parts named `QA-<suffix> CP1` to `CP3`); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `parent=<Root pk>`, `limit=10`, `ordering=-part_count` | `200 OK`. Body is valid against `PaginatedCategoryList`. `results` names, in order: `QA-<suffix> Cat Two` (`part_count` 2), `QA-<suffix> Cat One` (1), `QA-<suffix> Cat Zero` (0). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 74 · Review · matches: [API-LST-023](lists-and-filters.md) (74), [API-LST-016](lists-and-filters.md) (63), [API-LST-015](lists-and-filters.md) (60), [API-LST-014](lists-and-filters.md) (59)

**Duplicate judgement:** Keep · Orders by `-part_count` (Two, One, Zero) vs API-LST-023 by `-name` (Zero, Two, One); API-LST-014/015/016 test pagination. · test-case-reviewer, 2026-10-14

### API-LST-025: A category `ordering` value outside the schema's list is handled in a defined way.

| Field | Value |
|---|---|
| **Summary** | A category `ordering` value outside the schema's list is handled in a defined way. |
| **Requirement** | `R-LST-14` ([L848](../../requirements/openapi-parts.yaml#L848)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: value outside the `enum`) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Root` and its children `QA-<suffix> Cat Two` (2 parts), `QA-<suffix> Cat One` (1 part) and `QA-<suffix> Cat Zero` (no parts), created with `POST /api/part/category/` and `POST /api/part/` as `admin` (parts named `QA-<suffix> CP1` to `CP3`); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `parent=<Root pk>`, `limit=10`, `ordering=notafield` | Not known: depends on open question Q-LST-01 (status and body for an `ordering` value outside the `enum`). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

### API-LST-026: `search` matches the part name.

| Field | Value |
|---|---|
| **Summary** | `search` matches the part name. |
| **Requirement** | `R-LST-04` ([L687](../../requirements/openapi-parts.yaml#L687)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: term matches the field) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Search Cat`; part `QA-<suffix> Widget Alpha` (IPN `QA-<suffix>-W1`, description `QA-<suffix> sprocket description`, keywords `qakeyword<suffix>`) and part `QA-<suffix> Other Beta` (no IPN, description `plain`) in it, created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `search=QA-<suffix> Widget Alpha` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `1`; the only result is `QA-<suffix> Widget Alpha`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 86 · Duplicate · matches: [API-LST-027](lists-and-filters.md) (86), [API-LST-028](lists-and-filters.md) (86), [API-LST-029](lists-and-filters.md) (85, test data differs), [API-LST-030](lists-and-filters.md) (71), [API-LST-032](lists-and-filters.md) (66), +11 more

**Duplicate judgement:** Keep · Searches the `name` field; API-LST-027/028/029/030 each search a different field listed in R-LST-04 (IPN, description, keywords, category name) and API-LST-032 tests letter case. · test-case-reviewer, 2026-10-14

### API-LST-027: `search` matches the IPN.

| Field | Value |
|---|---|
| **Summary** | `search` matches the IPN. |
| **Requirement** | `R-LST-04` ([L687](../../requirements/openapi-parts.yaml#L687)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: term matches the field) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Search Cat`; part `QA-<suffix> Widget Alpha` (IPN `QA-<suffix>-W1`, description `QA-<suffix> sprocket description`, keywords `qakeyword<suffix>`) and part `QA-<suffix> Other Beta` (no IPN, description `plain`) in it, created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `search=QA-<suffix>-W1` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `1`; the only result is `QA-<suffix> Widget Alpha`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 88 · Duplicate · matches: [API-LST-028](lists-and-filters.md) (88), [API-LST-029](lists-and-filters.md) (87, test data differs), [API-LST-026](lists-and-filters.md) (86), [API-LST-030](lists-and-filters.md) (69), [API-LST-032](lists-and-filters.md) (60), +11 more

**Duplicate judgement:** Keep · Searches the `IPN` field; API-LST-026/028/029/030 search other fields of R-LST-04 and API-LST-032 tests letter case. · test-case-reviewer, 2026-10-14

### API-LST-028: `search` matches the description.

| Field | Value |
|---|---|
| **Summary** | `search` matches the description. |
| **Requirement** | `R-LST-04` ([L687](../../requirements/openapi-parts.yaml#L687)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: term matches the field) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Search Cat`; part `QA-<suffix> Widget Alpha` (IPN `QA-<suffix>-W1`, description `QA-<suffix> sprocket description`, keywords `qakeyword<suffix>`) and part `QA-<suffix> Other Beta` (no IPN, description `plain`) in it, created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `search=QA-<suffix> sprocket` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `1`; the only result is `QA-<suffix> Widget Alpha`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 88 · Duplicate · matches: [API-LST-027](lists-and-filters.md) (88), [API-LST-029](lists-and-filters.md) (87, test data differs), [API-LST-026](lists-and-filters.md) (86), [API-LST-030](lists-and-filters.md) (69), [API-LST-032](lists-and-filters.md) (60), +11 more

**Duplicate judgement:** Keep · Searches the `description` field; API-LST-026/027/029/030 search other fields of R-LST-04 and API-LST-032 tests letter case. · test-case-reviewer, 2026-10-14

### API-LST-029: `search` matches the keywords.

| Field | Value |
|---|---|
| **Summary** | `search` matches the keywords. |
| **Requirement** | `R-LST-04` ([L687](../../requirements/openapi-parts.yaml#L687)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: term matches the field) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Search Cat`; part `QA-<suffix> Widget Alpha` (IPN `QA-<suffix>-W1`, description `QA-<suffix> sprocket description`, keywords `qakeyword<suffix>`) and part `QA-<suffix> Other Beta` (no IPN, description `plain`) in it, created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `search=qakeyword<suffix>` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `1`; the only result is `QA-<suffix> Widget Alpha`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 87 · Review · matches: [API-LST-027](lists-and-filters.md) (87, test data differs), [API-LST-028](lists-and-filters.md) (87, test data differs), [API-LST-026](lists-and-filters.md) (85, test data differs), [API-LST-030](lists-and-filters.md) (68), [API-LST-033](lists-and-filters.md) (61), +11 more

**Duplicate judgement:** Keep · Searches the `keywords` field; API-LST-026/027/028/030 search other fields of R-LST-04 and API-LST-033 tests a word fragment. · test-case-reviewer, 2026-10-14

### API-LST-030: `search` matches the name of the part's category.

| Field | Value |
|---|---|
| **Summary** | `search` matches the name of the part's category. |
| **Requirement** | `R-LST-04` ([L687](../../requirements/openapi-parts.yaml#L687)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: term matches `category__name`) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Search Cat`; part `QA-<suffix> Widget Alpha` (IPN `QA-<suffix>-W1`, description `QA-<suffix> sprocket description`, keywords `qakeyword<suffix>`) and part `QA-<suffix> Other Beta` (no IPN, description `plain`) in it, created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `search=QA-<suffix> Search Cat` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `2`; results are `QA-<suffix> Widget Alpha` and `QA-<suffix> Other Beta`, both found through their category name. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 71 · Review · matches: [API-LST-026](lists-and-filters.md) (71), [API-LST-027](lists-and-filters.md) (69), [API-LST-028](lists-and-filters.md) (69), [API-LST-029](lists-and-filters.md) (68), [API-LST-032](lists-and-filters.md) (60), +2 more

**Duplicate judgement:** Keep · Searches the related `category__name` field and expects both parts; API-LST-026/027/028/029 search the part's own fields and expect one part. · test-case-reviewer, 2026-10-14

### API-LST-031: `search` with a term that matches nothing returns an empty page.

| Field | Value |
|---|---|
| **Summary** | `search` with a term that matches nothing returns an empty page. |
| **Requirement** | `R-LST-04` ([L687](../../requirements/openapi-parts.yaml#L687)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: no match) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Search Cat`; part `QA-<suffix> Widget Alpha` (IPN `QA-<suffix>-W1`, description `QA-<suffix> sprocket description`, keywords `qakeyword<suffix>`) and part `QA-<suffix> Other Beta` (no IPN, description `plain`) in it, created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `search=QA-<suffix>-nomatch-zzz` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `0`; `results` is an empty array; `next` and `previous` are `null`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 61 · Review · matches: [API-LST-052](lists-and-filters.md) (61), [API-LST-048](lists-and-filters.md) (60)

**Duplicate judgement:** Keep · No-match `search` (R-LST-04) vs API-LST-052 no-match `name_regex` (R-LST-10) and API-LST-048 no-match `IPN` (R-LST-09): different parameters and rules. · test-case-reviewer, 2026-10-14

### API-LST-032: `search` finds a part with a lower-case version of its name.

| Field | Value |
|---|---|
| **Summary** | `search` finds a part with a lower-case version of its name. |
| **Requirement** | `R-LST-04` ([L687](../../requirements/openapi-parts.yaml#L687)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Error guessing (letter case) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Search Cat`; part `QA-<suffix> Widget Alpha` (IPN `QA-<suffix>-W1`, description `QA-<suffix> sprocket description`, keywords `qakeyword<suffix>`) and part `QA-<suffix> Other Beta` (no IPN, description `plain`) in it, created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `search=qa-<suffix> widget alpha` | Not known: depends on open question Q-LST-03 (whether `search` is case-insensitive; `QA-<suffix> Widget Alpha` is expected only if it is). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 80 · Review · matches: [API-LST-033](lists-and-filters.md) (80), [API-LST-026](lists-and-filters.md) (66), [API-LST-027](lists-and-filters.md) (60), [API-LST-028](lists-and-filters.md) (60), [API-LST-030](lists-and-filters.md) (60), +1 more

**Duplicate judgement:** Keep · Letter case of the term vs API-LST-033 a word fragment (separate parts of Q-LST-03); API-LST-026/027/028/030 use exact terms. · test-case-reviewer, 2026-10-14

### API-LST-033: `search` finds a part with a fragment of its name.

| Field | Value |
|---|---|
| **Summary** | `search` finds a part with a fragment of its name. |
| **Requirement** | `R-LST-04` ([L687](../../requirements/openapi-parts.yaml#L687)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Error guessing (partial term) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Search Cat`; part `QA-<suffix> Widget Alpha` (IPN `QA-<suffix>-W1`, description `QA-<suffix> sprocket description`, keywords `qakeyword<suffix>`) and part `QA-<suffix> Other Beta` (no IPN, description `plain`) in it, created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10`, `search=Widget` | Not known: depends on open question Q-LST-03 (whether `search` matches part of a word; `QA-<suffix> Widget Alpha` is expected only if it does). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 80 · Review · matches: [API-LST-032](lists-and-filters.md) (80), [API-LST-026](lists-and-filters.md) (62), [API-LST-029](lists-and-filters.md) (61), [API-LST-027](lists-and-filters.md) (60), [API-LST-028](lists-and-filters.md) (60), +1 more

**Duplicate judgement:** Keep · Word fragment vs API-LST-032 letter case (separate parts of Q-LST-03); API-LST-026/027/028/029 use whole terms. · test-case-reviewer, 2026-10-14

### API-LST-034: A category `search` matches the name.

| Field | Value |
|---|---|
| **Summary** | A category `search` matches the name. |
| **Requirement** | `R-LST-16` ([L911](../../requirements/openapi-parts.yaml#L911)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: term matches `name`) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Root`, `QA-<suffix> Child` (parent Root) and `QA-<suffix> Grand` (parent Child), created with `POST /api/part/category/` as `admin`; parts `QA-<suffix> PR` (in Root), `QA-<suffix> PC` (in Child) and `QA-<suffix> PG` (in Grand), created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `limit=10`, `search=QA-<suffix> Grand` | `200 OK`. Body is valid against `PaginatedCategoryList`. `results` contains `QA-<suffix> Grand`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 75 · Review · matches: [API-LST-035](lists-and-filters.md) (75), [API-LST-066](lists-and-filters.md) (52), [API-LST-023](lists-and-filters.md) (50)

**Duplicate judgement:** Keep · Category search on `name` vs API-LST-035 on `pathstring` (different field of R-LST-16); API-LST-066 is the `parent` filter and API-LST-023 ordering. · test-case-reviewer, 2026-10-14

### API-LST-035: A category `search` matches the path string, so a term from a parent's name finds its sub-categories.

| Field | Value |
|---|---|
| **Summary** | A category `search` matches the path string, so a term from a parent's name finds its sub-categories. |
| **Requirement** | `R-LST-16` ([L911](../../requirements/openapi-parts.yaml#L911)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: term matches `pathstring`) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Root`, `QA-<suffix> Child` (parent Root) and `QA-<suffix> Grand` (parent Child), created with `POST /api/part/category/` as `admin`; parts `QA-<suffix> PR` (in Root), `QA-<suffix> PC` (in Child) and `QA-<suffix> PG` (in Grand), created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `limit=10`, `search=QA-<suffix> Root/QA-<suffix> Child` | `200 OK`. Body is valid against `PaginatedCategoryList`. `results` contains `QA-<suffix> Child` and `QA-<suffix> Grand` (their `pathstring` starts with the term). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** Read `pathstring` from the `POST` response of the category in the setup and use it as the term.

**Duplicate check:** 75 · Review · matches: [API-LST-034](lists-and-filters.md) (75), [API-LST-066](lists-and-filters.md) (51)

**Duplicate judgement:** Keep · Category search on `pathstring` vs API-LST-034 on `name`; API-LST-066 reaches descendants through the `parent` filter, not `search`. · test-case-reviewer, 2026-10-14

### API-LST-036: `category=<pk>` returns the parts in that category.

| Field | Value |
|---|---|
| **Summary** | `category=<pk>` returns the parts in that category. |
| **Requirement** | `R-LST-06` ([L469](../../requirements/openapi-parts.yaml#L469)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: existing category ID, no child categories) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Order Cat` and three parts `QA-<suffix> Banana`, `QA-<suffix> Apple`, `QA-<suffix> Cherry` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `3`; every result has `category` equal to `<cat pk>`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 62 · Review · matches: [API-LST-040](lists-and-filters.md) (62), [API-LST-037](lists-and-filters.md) (61), [API-LST-039](lists-and-filters.md) (61), [API-LST-038](lists-and-filters.md) (60), [API-LST-056](lists-and-filters.md) (57), +13 more

**Duplicate judgement:** Keep · Numeric category ID with no child categories vs API-LST-040 literal `null`, API-LST-037/038/039 a category tree with `cascade` on, off or omitted, and API-LST-056 a date filter. · test-case-reviewer, 2026-10-14

### API-LST-037: `category=<pk>&cascade=true` also returns parts in child and grandchild categories.

| Field | Value |
|---|---|
| **Summary** | `category=<pk>&cascade=true` also returns parts in child and grandchild categories. |
| **Requirement** | `R-LST-06` ([L469](../../requirements/openapi-parts.yaml#L469)), `R-LST-07` ([L464](../../requirements/openapi-parts.yaml#L464)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: cascade on) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Root`, `QA-<suffix> Child` (parent Root) and `QA-<suffix> Grand` (parent Child), created with `POST /api/part/category/` as `admin`; parts `QA-<suffix> PR` (in Root), `QA-<suffix> PC` (in Child) and `QA-<suffix> PG` (in Grand), created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<Root pk>`, `cascade=true`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `3`; results are `QA-<suffix> PR`, `QA-<suffix> PC` and `QA-<suffix> PG`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 70 · Review · matches: [API-LST-038](lists-and-filters.md) (70), [API-LST-039](lists-and-filters.md) (67), [API-LST-036](lists-and-filters.md) (61), [API-LST-040](lists-and-filters.md) (53), [API-LST-056](lists-and-filters.md) (53), +5 more

**Duplicate judgement:** Keep · `cascade=true` (3 parts) vs API-LST-038 `cascade=false` (1 part) and API-LST-039 `cascade` omitted; API-LST-036/040/056 are other filters. · test-case-reviewer, 2026-10-14

### API-LST-038: `category=<pk>&cascade=false` returns only the parts directly in the category.

| Field | Value |
|---|---|
| **Summary** | `category=<pk>&cascade=false` returns only the parts directly in the category. |
| **Requirement** | `R-LST-06` ([L469](../../requirements/openapi-parts.yaml#L469)), `R-LST-07` ([L464](../../requirements/openapi-parts.yaml#L464)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: cascade off) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Root`, `QA-<suffix> Child` (parent Root) and `QA-<suffix> Grand` (parent Child), created with `POST /api/part/category/` as `admin`; parts `QA-<suffix> PR` (in Root), `QA-<suffix> PC` (in Child) and `QA-<suffix> PG` (in Grand), created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<Root pk>`, `cascade=false`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `1`; the only result is `QA-<suffix> PR`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 70 · Review · matches: [API-LST-037](lists-and-filters.md) (70), [API-LST-039](lists-and-filters.md) (64), [API-LST-050](lists-and-filters.md) (64), [API-LST-044](lists-and-filters.md) (63), [API-LST-036](lists-and-filters.md) (60), +11 more

**Duplicate judgement:** Keep · `cascade=false` vs API-LST-037 `cascade=true` and API-LST-039 omitted; API-LST-050/044 are other filters and API-LST-036 has no child categories. · test-case-reviewer, 2026-10-14

### API-LST-039: `category=<pk>` without `cascade` returns child-category parts or not, by the default.

| Field | Value |
|---|---|
| **Summary** | `category=<pk>` without `cascade` returns child-category parts or not, by the default. |
| **Requirement** | `R-LST-06` ([L469](../../requirements/openapi-parts.yaml#L469)), `R-LST-07` ([L464](../../requirements/openapi-parts.yaml#L464)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Decision table (cascade omitted) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Root`, `QA-<suffix> Child` (parent Root) and `QA-<suffix> Grand` (parent Child), created with `POST /api/part/category/` as `admin`; parts `QA-<suffix> PR` (in Root), `QA-<suffix> PC` (in Child) and `QA-<suffix> PG` (in Grand), created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-05 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<Root pk>`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> PR` is in the results. Not known: depends on open question Q-LST-05 (default of `cascade`: whether `QA-<suffix> PC` and `QA-<suffix> PG` are also returned). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 67 · Review · matches: [API-LST-037](lists-and-filters.md) (67), [API-LST-038](lists-and-filters.md) (64), [API-LST-036](lists-and-filters.md) (61), [API-LST-040](lists-and-filters.md) (57), [API-LST-045](lists-and-filters.md) (53)

**Duplicate judgement:** Keep · `cascade` omitted (default under Q-LST-05) vs API-LST-037/038 with `cascade` sent; API-LST-036/040/045 are other classes or filters. · test-case-reviewer, 2026-10-14

### API-LST-040: `category=null` returns parts that have no category.

| Field | Value |
|---|---|
| **Summary** | `category=null` returns parts that have no category. |
| **Requirement** | `R-LST-06` ([L469](../../requirements/openapi-parts.yaml#L469)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: literal `null`) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Cat` with part `QA-<suffix> In Cat`; part `QA-<suffix> No Cat` created without a category with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-06, Q-LST-07 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=null`, `search=QA-<suffix>`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> No Cat` is in the results. Not known: depends on open question Q-LST-06 (whether the literal `null` is accepted although the parameter is typed `integer`; `QA-<suffix> In Cat` is expected to be absent only if it is). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** Schema issue 3. `search` is added only to narrow the list, which depends on filters combining (Q-LST-07).

**Duplicate check:** 62 · Review · matches: [API-LST-036](lists-and-filters.md) (62), [API-LST-039](lists-and-filters.md) (57), [API-LST-037](lists-and-filters.md) (53), [API-LST-038](lists-and-filters.md) (53)

**Duplicate judgement:** Keep · Literal `null` (parts with no category) vs API-LST-036 a numeric ID and API-LST-037/038/039 `cascade` on a category tree. · test-case-reviewer, 2026-10-14

### API-LST-041: `category=<pk>` of a category that does not exist is handled in a defined way.

| Field | Value |
|---|---|
| **Summary** | `category=<pk>` of a category that does not exist is handled in a defined way. |
| **Requirement** | `R-LST-06` ([L469](../../requirements/openapi-parts.yaml#L469)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: well-formed ID of no category) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Gone` created and deleted with `DELETE /api/part/category/<pk>/` as `admin` (body flags both `false`); its `pk` is reused; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<deleted category pk>`, `limit=10` | Not known: depends on open question Q-LST-09 (status and body for a category ID that matches no category: empty page or a validation error). |

**Postconditions and cleanup:** None beyond the setup: the category is already deleted.

**Notes:** None

**Duplicate check:** 70 · Review · matches: [API-LST-042](lists-and-filters.md) (70), [API-LST-046](lists-and-filters.md) (54), [API-LST-059](lists-and-filters.md) (54), [API-LST-010](lists-and-filters.md) (53), [API-LST-012](lists-and-filters.md) (53), +2 more

**Duplicate judgement:** Keep · Well-formed ID of a deleted category vs API-LST-042 a non-numeric value (different invalid class); API-LST-046/059/010/012 test other parameters. · test-case-reviewer, 2026-10-14

### API-LST-042: A non-numeric `category` value other than `null` is handled in a defined way.

| Field | Value |
|---|---|
| **Summary** | A non-numeric `category` value other than `null` is handled in a defined way. |
| **Requirement** | `R-LST-06` ([L469](../../requirements/openapi-parts.yaml#L469)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: None; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=abc`, `limit=10` | Not known: depends on open question Q-LST-09 (status and body for a non-numeric `category`). |

**Postconditions and cleanup:** None: no data created.

**Notes:** None

**Duplicate check:** 70 · Review · matches: [API-LST-041](lists-and-filters.md) (70), [API-LST-059](lists-and-filters.md) (59), [API-LST-046](lists-and-filters.md) (58), [API-LST-012](lists-and-filters.md) (57), [API-LST-010](lists-and-filters.md) (53), +2 more

**Duplicate judgement:** Keep · Non-numeric `category` (wrong type) vs API-LST-041 a well-formed but unknown ID; API-LST-059/046/012/010 test other parameters. · test-case-reviewer, 2026-10-14

### API-LST-043: `active=true` returns only active parts.

| Field | Value |
|---|---|
| **Summary** | `active=true` returns only active parts. |
| **Requirement** | `R-LST-08` ([L447](../../requirements/openapi-parts.yaml#L447)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: true) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Active Cat` with part `QA-<suffix> Live` (active) and part `QA-<suffix> Dead` (created, then `PATCH` `active: false`), created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `active=true`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `1`; the only result is `QA-<suffix> Live`, with `active` `true`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 77 · Review · matches: [API-LST-044](lists-and-filters.md) (77), [API-LST-062](lists-and-filters.md) (64), [API-LST-045](lists-and-filters.md) (62), [API-LST-038](lists-and-filters.md) (59), [API-LST-050](lists-and-filters.md) (59), +13 more

**Duplicate judgement:** Keep · `active=true` vs API-LST-044 `false` and API-LST-045 omitted; API-LST-062 sends the same request but cites R-LST-13 and adds an active part in another category (see review finding on the overlap). · test-case-reviewer, 2026-10-14

### API-LST-044: `active=false` returns only inactive parts.

| Field | Value |
|---|---|
| **Summary** | `active=false` returns only inactive parts. |
| **Requirement** | `R-LST-08` ([L447](../../requirements/openapi-parts.yaml#L447)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: false) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Active Cat` with part `QA-<suffix> Live` (active) and part `QA-<suffix> Dead` (created, then `PATCH` `active: false`), created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `active=false`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `1`; the only result is `QA-<suffix> Dead`, with `active` `false`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 77 · Review · matches: [API-LST-043](lists-and-filters.md) (77), [API-LST-045](lists-and-filters.md) (64), [API-LST-038](lists-and-filters.md) (63), [API-LST-050](lists-and-filters.md) (63), [API-LST-026](lists-and-filters.md) (56), +12 more

**Duplicate judgement:** Keep · `active=false` (returns Dead) vs API-LST-043 `true` (returns Live) and API-LST-045 omitted; the other matches test other filters. · test-case-reviewer, 2026-10-14

### API-LST-045: Without `active`, the list contains both active and inactive parts.

| Field | Value |
|---|---|
| **Summary** | Without `active`, the list contains both active and inactive parts. |
| **Requirement** | `R-LST-08` ([L447](../../requirements/openapi-parts.yaml#L447)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Decision table (filter omitted) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Active Cat` with part `QA-<suffix> Live` (active) and part `QA-<suffix> Dead` (created, then `PATCH` `active: false`), created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-05 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. The filter is not applied, so `QA-<suffix> Live` and `QA-<suffix> Dead` are expected. Not known: depends on open question Q-LST-05 (the schema states no default for `active`; if inactive parts are hidden by default the count is `1`). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 64 · Review · matches: [API-LST-044](lists-and-filters.md) (64), [API-LST-043](lists-and-filters.md) (62), [API-LST-062](lists-and-filters.md) (56), [API-LST-039](lists-and-filters.md) (53), [API-LST-036](lists-and-filters.md) (52), +1 more

**Duplicate judgement:** Keep · `active` omitted (default under Q-LST-05) vs API-LST-043/044 with a value sent; API-LST-062/039/036 test other filters. · test-case-reviewer, 2026-10-14

### API-LST-046: A non-boolean `active` value is handled in a defined way.

| Field | Value |
|---|---|
| **Summary** | A non-boolean `active` value is handled in a defined way. |
| **Requirement** | `R-LST-08` ([L447](../../requirements/openapi-parts.yaml#L447)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Active Cat` with part `QA-<suffix> Live` (active) and part `QA-<suffix> Dead` (created, then `PATCH` `active: false`), created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `active=maybe`, `limit=10` | Not known: depends on open question Q-LST-09 (status and body for a non-boolean filter value). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 58 · Review · matches: [API-LST-042](lists-and-filters.md) (58), [API-LST-059](lists-and-filters.md) (58), [API-LST-012](lists-and-filters.md) (55), [API-LST-041](lists-and-filters.md) (54), [API-LST-010](lists-and-filters.md) (53), +3 more

**Duplicate judgement:** Keep · Invalid value on the boolean `active` (R-LST-08) vs invalid values on `category`, `created_after` and `limit` in the matches (different parameters and rules). · test-case-reviewer, 2026-10-14

### API-LST-047: `IPN` filters by the exact IPN, so a longer IPN that starts with it is not returned.

| Field | Value |
|---|---|
| **Summary** | `IPN` filters by the exact IPN, so a longer IPN that starts with it is not returned. |
| **Requirement** | `R-LST-09` ([L437](../../requirements/openapi-parts.yaml#L437), [L531](../../requirements/openapi-parts.yaml#L531)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: exact match), Boundary value analysis (IPN that is a prefix of another) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> IPN Cat` with parts `QA-<suffix> A` (IPN `QA-<suffix>-A1`), `QA-<suffix> B` (no IPN) and `QA-<suffix> C` (IPN `QA-<suffix>-A10`), created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `IPN=QA-<suffix>-A1`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `1`; the only result is `QA-<suffix> A`; `QA-<suffix> C` (IPN `QA-<suffix>-A10`) is not returned. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 68 · Review · matches: [API-LST-050](lists-and-filters.md) (68), [API-LST-049](lists-and-filters.md) (64), [API-LST-027](lists-and-filters.md) (55), [API-LST-028](lists-and-filters.md) (55), [API-LST-026](lists-and-filters.md) (54), +4 more

**Duplicate judgement:** Keep · Exact `IPN` filter with a prefix-sharing IPN vs API-LST-049/050 `has_ipn` (other clause of R-LST-09) and API-LST-026/027/028 `search` (R-LST-04). · test-case-reviewer, 2026-10-14

### API-LST-048: `IPN` with a value no part has returns an empty page.

| Field | Value |
|---|---|
| **Summary** | `IPN` with a value no part has returns an empty page. |
| **Requirement** | `R-LST-09` ([L437](../../requirements/openapi-parts.yaml#L437), [L531](../../requirements/openapi-parts.yaml#L531)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: no match) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> IPN Cat` with parts `QA-<suffix> A` (IPN `QA-<suffix>-A1`), `QA-<suffix> B` (no IPN) and `QA-<suffix> C` (IPN `QA-<suffix>-A10`), created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `IPN=QA-<suffix>-ZZ`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `0`; `results` is empty. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 68 · Review · matches: [API-LST-052](lists-and-filters.md) (68), [API-LST-031](lists-and-filters.md) (60)

**Duplicate judgement:** Keep · No-match `IPN` (R-LST-09) vs API-LST-052 no-match `name_regex` (R-LST-10) and API-LST-031 no-match `search` (R-LST-04). · test-case-reviewer, 2026-10-14

### API-LST-049: `has_ipn=true` returns only parts that have an IPN.

| Field | Value |
|---|---|
| **Summary** | `has_ipn=true` returns only parts that have an IPN. |
| **Requirement** | `R-LST-09` ([L437](../../requirements/openapi-parts.yaml#L437), [L531](../../requirements/openapi-parts.yaml#L531)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: true) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> IPN Cat` with parts `QA-<suffix> A` (IPN `QA-<suffix>-A1`), `QA-<suffix> B` (no IPN) and `QA-<suffix> C` (IPN `QA-<suffix>-A10`), created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `has_ipn=true`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `2`; results are `QA-<suffix> A` and `QA-<suffix> C`; every result has a non-empty `IPN`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 70 · Review · matches: [API-LST-050](lists-and-filters.md) (70), [API-LST-047](lists-and-filters.md) (64), [API-LST-043](lists-and-filters.md) (55), [API-LST-036](lists-and-filters.md) (54), [API-LST-051](lists-and-filters.md) (53), +6 more

**Duplicate judgement:** Keep · `has_ipn=true` (A and C) vs API-LST-050 `false` (B) and API-LST-047 the exact `IPN` clause; the other matches test other filters. · test-case-reviewer, 2026-10-14

### API-LST-050: `has_ipn=false` returns only parts without an IPN.

| Field | Value |
|---|---|
| **Summary** | `has_ipn=false` returns only parts without an IPN. |
| **Requirement** | `R-LST-09` ([L437](../../requirements/openapi-parts.yaml#L437), [L531](../../requirements/openapi-parts.yaml#L531)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: false) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> IPN Cat` with parts `QA-<suffix> A` (IPN `QA-<suffix>-A1`), `QA-<suffix> B` (no IPN) and `QA-<suffix> C` (IPN `QA-<suffix>-A10`), created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `has_ipn=false`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `1`; the only result is `QA-<suffix> B`, with an empty `IPN`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 70 · Review · matches: [API-LST-049](lists-and-filters.md) (70), [API-LST-047](lists-and-filters.md) (68), [API-LST-038](lists-and-filters.md) (64), [API-LST-044](lists-and-filters.md) (63), [API-LST-043](lists-and-filters.md) (59), +9 more

**Duplicate judgement:** Keep · `has_ipn=false` (B) vs API-LST-049 `true` (A, C) and API-LST-047 the exact `IPN` clause; the other matches test other filters. · test-case-reviewer, 2026-10-14

### API-LST-051: `name_regex` returns the parts whose name matches the regular expression.

| Field | Value |
|---|---|
| **Summary** | `name_regex` returns the parts whose name matches the regular expression. |
| **Requirement** | `R-LST-10` ([L600](../../requirements/openapi-parts.yaml#L600)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: valid regex) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Reg Cat` with parts `QA-<suffix> Reg-A`, `QA-<suffix> Reg-B` and `QA-<suffix> Reg-C`, created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `name_regex=Reg-[AB]$`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `2`; results are `QA-<suffix> Reg-A` and `QA-<suffix> Reg-B`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 53 · Review · matches: [API-LST-049](lists-and-filters.md) (53), [API-LST-054](lists-and-filters.md) (53), [API-LST-055](lists-and-filters.md) (53), [API-LST-056](lists-and-filters.md) (53), [API-LST-036](lists-and-filters.md) (52), +9 more

**Duplicate judgement:** Keep · Only case that exercises `name_regex` with a matching expression (R-LST-10); every match tests a different filter and rule. · test-case-reviewer, 2026-10-14

### API-LST-052: `name_regex` with a regex that matches no name returns an empty page.

| Field | Value |
|---|---|
| **Summary** | `name_regex` with a regex that matches no name returns an empty page. |
| **Requirement** | `R-LST-10` ([L600](../../requirements/openapi-parts.yaml#L600)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (valid regex, no match) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Reg Cat` with parts `QA-<suffix> Reg-A`, `QA-<suffix> Reg-B` and `QA-<suffix> Reg-C`, created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `name_regex=^Reg-Z$`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `0`; `results` is empty. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 68 · Review · matches: [API-LST-048](lists-and-filters.md) (68), [API-LST-031](lists-and-filters.md) (61), [API-LST-053](lists-and-filters.md) (56)

**Duplicate judgement:** Keep · Valid regex with no match vs API-LST-053 malformed regex; API-LST-048 (`IPN`) and API-LST-031 (`search`) are other parameters. · test-case-reviewer, 2026-10-14

### API-LST-053: `name_regex` with an invalid regular expression is handled in a defined way.

| Field | Value |
|---|---|
| **Summary** | `name_regex` with an invalid regular expression is handled in a defined way. |
| **Requirement** | `R-LST-10` ([L600](../../requirements/openapi-parts.yaml#L600)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: malformed regex), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Reg Cat` with parts `QA-<suffix> Reg-A`, `QA-<suffix> Reg-B` and `QA-<suffix> Reg-C`, created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `name_regex=[`, `limit=10` (the `[` is URL-encoded as `%5B`) | Not known: depends on open question Q-LST-02 (status and body for an invalid regular expression: validation error, empty page, or server error). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 56 · Review · matches: [API-LST-052](lists-and-filters.md) (56), [API-LST-041](lists-and-filters.md) (53), [API-LST-046](lists-and-filters.md) (50)

**Duplicate judgement:** Keep · Malformed regex (invalid class) vs API-LST-052 valid regex with no match; API-LST-041/046 send invalid values to other parameters. · test-case-reviewer, 2026-10-14

### API-LST-054: `created_after` with a date in the future returns no parts.

| Field | Value |
|---|---|
| **Summary** | `created_after` with a date in the future returns no parts. |
| **Requirement** | `R-LST-11` ([L491](../../requirements/openapi-parts.yaml#L491), [L497](../../requirements/openapi-parts.yaml#L497)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Boundary value analysis (date far after any creation) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `created_after=2999-12-31`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `0`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** Schema issue 2: the description says "Updated after"; the filter is on the creation date.

**Duplicate check:** 83 · Review · matches: [API-LST-055](lists-and-filters.md) (83, test data differs), [API-LST-056](lists-and-filters.md) (78), [API-LST-036](lists-and-filters.md) (55), [API-LST-051](lists-and-filters.md) (53), [API-LST-029](lists-and-filters.md) (52), +9 more

**Duplicate judgement:** Keep · Tests the `created_after` parameter vs API-LST-055 `created_before` (other parameter of R-LST-11) and API-LST-056 both bounds with all parts returned. · test-case-reviewer, 2026-10-14

### API-LST-055: `created_before` with a date long ago returns no parts.

| Field | Value |
|---|---|
| **Summary** | `created_before` with a date long ago returns no parts. |
| **Requirement** | `R-LST-11` ([L491](../../requirements/openapi-parts.yaml#L491), [L497](../../requirements/openapi-parts.yaml#L497)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Boundary value analysis (date far before any creation) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `created_before=2000-01-01`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `0`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** Schema issue 2.

**Duplicate check:** 83 · Review · matches: [API-LST-054](lists-and-filters.md) (83, test data differs), [API-LST-056](lists-and-filters.md) (75), [API-LST-036](lists-and-filters.md) (54), [API-LST-051](lists-and-filters.md) (53), [API-LST-029](lists-and-filters.md) (52), +9 more

**Duplicate judgement:** Keep · Tests the `created_before` parameter vs API-LST-054 `created_after` and API-LST-056 both bounds with all parts returned. · test-case-reviewer, 2026-10-14

### API-LST-056: A range with `created_after` in the past and `created_before` in the future returns the parts created today.

| Field | Value |
|---|---|
| **Summary** | A range with `created_after` in the past and `created_before` in the future returns the parts created today. |
| **Requirement** | `R-LST-11` ([L491](../../requirements/openapi-parts.yaml#L491), [L497](../../requirements/openapi-parts.yaml#L497)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: date range around creation) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `created_after=2000-01-01`, `created_before=2999-12-31`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. `count` is `3`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** Schema issue 2.

**Duplicate check:** 78 · Review · matches: [API-LST-054](lists-and-filters.md) (78), [API-LST-055](lists-and-filters.md) (75), [API-LST-036](lists-and-filters.md) (57), [API-LST-037](lists-and-filters.md) (53), [API-LST-051](lists-and-filters.md) (53), +10 more

**Duplicate judgement:** Keep · Both date bounds around creation, all 3 parts returned, vs API-LST-054/055 a single bound returning none (different class and outcome). · test-case-reviewer, 2026-10-14

### API-LST-057: `created_after` set to the day the parts were created includes or excludes them, by the boundary rule.

| Field | Value |
|---|---|
| **Summary** | `created_after` set to the day the parts were created includes or excludes them, by the boundary rule. |
| **Requirement** | `R-LST-11` ([L491](../../requirements/openapi-parts.yaml#L491), [L497](../../requirements/openapi-parts.yaml#L497)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (date = creation date) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `created_after=<creation_date of P1>`, `limit=10` | Not known: depends on open question Q-LST-08 (whether `created_after` is inclusive of the given day). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** Schema issue 2. Take the date from `creation_date` in the `POST` response.

**Duplicate check:** 84 · Review · matches: [API-LST-058](lists-and-filters.md) (84, test data differs)

**Duplicate judgement:** Keep · On-boundary date for `created_after` vs API-LST-058 for `created_before`: different parameter, and inclusiveness may differ per parameter (Q-LST-08). · test-case-reviewer, 2026-10-14

### API-LST-058: `created_before` set to the day the parts were created includes or excludes them, by the boundary rule.

| Field | Value |
|---|---|
| **Summary** | `created_before` set to the day the parts were created includes or excludes them, by the boundary rule. |
| **Requirement** | `R-LST-11` ([L491](../../requirements/openapi-parts.yaml#L491), [L497](../../requirements/openapi-parts.yaml#L497)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (date = creation date) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `created_before=<creation_date of P1>`, `limit=10` | Not known: depends on open question Q-LST-08 (whether `created_before` is inclusive of the given day). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** Schema issue 2.

**Duplicate check:** 84 · Review · matches: [API-LST-057](lists-and-filters.md) (84, test data differs)

**Duplicate judgement:** Keep · On-boundary date for `created_before` vs API-LST-057 for `created_after`: different parameter, and inclusiveness may differ per parameter (Q-LST-08). · test-case-reviewer, 2026-10-14

### API-LST-059: A `created_after` value that is not a date in `YYYY-MM-DD` format is handled in a defined way.

| Field | Value |
|---|---|
| **Summary** | A `created_after` value that is not a date in `YYYY-MM-DD` format is handled in a defined way. |
| **Requirement** | `R-LST-11` ([L491](../../requirements/openapi-parts.yaml#L491), [L497](../../requirements/openapi-parts.yaml#L497)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong `format: date`) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Page Cat` and three parts `QA-<suffix> P1`, `QA-<suffix> P2`, `QA-<suffix> P3` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `created_after=31/12/2025`, `limit=10` | Not known: depends on open question Q-LST-09 (status and body for a malformed date). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 59 · Review · matches: [API-LST-042](lists-and-filters.md) (59), [API-LST-046](lists-and-filters.md) (58), [API-LST-012](lists-and-filters.md) (56), [API-LST-041](lists-and-filters.md) (54), [API-LST-010](lists-and-filters.md) (53), +1 more

**Duplicate judgement:** Keep · Malformed date on `created_after` (R-LST-11, `format: date`) vs invalid values on `category`, `active` and `limit` in the matches. · test-case-reviewer, 2026-10-14

### API-LST-060: Each boolean attribute filter set to `true` returns only parts with that attribute on.

| Field | Value |
|---|---|
| **Summary** | Each boolean attribute filter set to `true` returns only parts with that attribute on. |
| **Requirement** | `R-LST-12` ([L455](../../requirements/openapi-parts.yaml#L455), [L479](../../requirements/openapi-parts.yaml#L479), [L483](../../requirements/openapi-parts.yaml#L483), [L570](../../requirements/openapi-parts.yaml#L570), [L591](../../requirements/openapi-parts.yaml#L591), [L671](../../requirements/openapi-parts.yaml#L671), [L684](../../requirements/openapi-parts.yaml#L684), [L710](../../requirements/openapi-parts.yaml#L710), [L714](../../requirements/openapi-parts.yaml#L714), [L728](../../requirements/openapi-parts.yaml#L728)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: true), Decision table (one column per attribute) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Flag Cat`; part `QA-<suffix> Base` with all ten flags (`assembly`, `component`, `consumable`, `is_template`, `locked`, `purchaseable`, `salable`, `testable`, `trackable`, `virtual`) `false`; and for each flag X a part `QA-<suffix> Only-X` that is `Base` except X `true`, all created as `admin` (`locked` set with `PATCH` after creation); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `assembly=true`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Only-assembly` is in the results; `QA-<suffix> Base` is not; every result has `assembly` `true`. |
| 2 | `GET /api/part/` as `reader` | `category=<cat pk>`, `component=true`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Only-component` is in the results; `QA-<suffix> Base` is not; every result has `component` `true`. |
| 3 | `GET /api/part/` as `reader` | `category=<cat pk>`, `consumable=true`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Only-consumable` is in the results; `QA-<suffix> Base` is not; every result has `consumable` `true`. |
| 4 | `GET /api/part/` as `reader` | `category=<cat pk>`, `is_template=true`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Only-is_template` is in the results; `QA-<suffix> Base` is not; every result has `is_template` `true`. |
| 5 | `GET /api/part/` as `reader` | `category=<cat pk>`, `locked=true`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Only-locked` is in the results; `QA-<suffix> Base` is not; every result has `locked` `true`. |
| 6 | `GET /api/part/` as `reader` | `category=<cat pk>`, `purchaseable=true`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Only-purchaseable` is in the results; `QA-<suffix> Base` is not; every result has `purchaseable` `true`. |
| 7 | `GET /api/part/` as `reader` | `category=<cat pk>`, `salable=true`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Only-salable` is in the results; `QA-<suffix> Base` is not; every result has `salable` `true`. |
| 8 | `GET /api/part/` as `reader` | `category=<cat pk>`, `testable=true`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Only-testable` is in the results; `QA-<suffix> Base` is not; every result has `testable` `true`. |
| 9 | `GET /api/part/` as `reader` | `category=<cat pk>`, `trackable=true`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Only-trackable` is in the results; `QA-<suffix> Base` is not; every result has `trackable` `true`. |
| 10 | `GET /api/part/` as `reader` | `category=<cat pk>`, `virtual=true`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Only-virtual` is in the results; `QA-<suffix> Base` is not; every result has `virtual` `true`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** Ten steps, one per attribute.

**Duplicate check:** 79 · Review · matches: [API-LST-061](lists-and-filters.md) (79)

**Duplicate judgement:** Keep · Each flag `true` (Only-X returned, Base excluded) vs API-LST-061 each flag `false` (opposite class and outcome). · test-case-reviewer, 2026-10-14

### API-LST-061: Each boolean attribute filter set to `false` returns only parts with that attribute off.

| Field | Value |
|---|---|
| **Summary** | Each boolean attribute filter set to `false` returns only parts with that attribute off. |
| **Requirement** | `R-LST-12` ([L455](../../requirements/openapi-parts.yaml#L455), [L479](../../requirements/openapi-parts.yaml#L479), [L483](../../requirements/openapi-parts.yaml#L483), [L570](../../requirements/openapi-parts.yaml#L570), [L591](../../requirements/openapi-parts.yaml#L591), [L671](../../requirements/openapi-parts.yaml#L671), [L684](../../requirements/openapi-parts.yaml#L684), [L710](../../requirements/openapi-parts.yaml#L710), [L714](../../requirements/openapi-parts.yaml#L714), [L728](../../requirements/openapi-parts.yaml#L728)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: false), Decision table (one column per attribute) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Flag Cat`; part `QA-<suffix> Base` with all ten flags (`assembly`, `component`, `consumable`, `is_template`, `locked`, `purchaseable`, `salable`, `testable`, `trackable`, `virtual`) `false`; and for each flag X a part `QA-<suffix> Only-X` that is `Base` except X `true`, all created as `admin` (`locked` set with `PATCH` after creation); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `assembly=false`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Base` is in the results; `QA-<suffix> Only-assembly` is not; every result has `assembly` `false`. |
| 2 | `GET /api/part/` as `reader` | `category=<cat pk>`, `component=false`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Base` is in the results; `QA-<suffix> Only-component` is not; every result has `component` `false`. |
| 3 | `GET /api/part/` as `reader` | `category=<cat pk>`, `consumable=false`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Base` is in the results; `QA-<suffix> Only-consumable` is not; every result has `consumable` `false`. |
| 4 | `GET /api/part/` as `reader` | `category=<cat pk>`, `is_template=false`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Base` is in the results; `QA-<suffix> Only-is_template` is not; every result has `is_template` `false`. |
| 5 | `GET /api/part/` as `reader` | `category=<cat pk>`, `locked=false`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Base` is in the results; `QA-<suffix> Only-locked` is not; every result has `locked` `false`. |
| 6 | `GET /api/part/` as `reader` | `category=<cat pk>`, `purchaseable=false`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Base` is in the results; `QA-<suffix> Only-purchaseable` is not; every result has `purchaseable` `false`. |
| 7 | `GET /api/part/` as `reader` | `category=<cat pk>`, `salable=false`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Base` is in the results; `QA-<suffix> Only-salable` is not; every result has `salable` `false`. |
| 8 | `GET /api/part/` as `reader` | `category=<cat pk>`, `testable=false`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Base` is in the results; `QA-<suffix> Only-testable` is not; every result has `testable` `false`. |
| 9 | `GET /api/part/` as `reader` | `category=<cat pk>`, `trackable=false`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Base` is in the results; `QA-<suffix> Only-trackable` is not; every result has `trackable` `false`. |
| 10 | `GET /api/part/` as `reader` | `category=<cat pk>`, `virtual=false`, `limit=20` | `200 OK`. Body is valid against `PaginatedPartList`. `QA-<suffix> Base` is in the results; `QA-<suffix> Only-virtual` is not; every result has `virtual` `false`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** Ten steps, one per attribute.

**Duplicate check:** 79 · Review · matches: [API-LST-060](lists-and-filters.md) (79)

**Duplicate judgement:** Keep · Each flag `false` (Base returned, Only-X excluded) vs API-LST-060 each flag `true`. · test-case-reviewer, 2026-10-14

### API-LST-062: `category` and `active` together return only the active parts of that category.

| Field | Value |
|---|---|
| **Summary** | `category` and `active` together return only the active parts of that category. |
| **Requirement** | `R-LST-13` ([L432](../../requirements/openapi-parts.yaml#L432)), `R-LST-08` ([L447](../../requirements/openapi-parts.yaml#L447)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Decision table (category set, active true) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Active Cat` with part `QA-<suffix> Live` (active) and part `QA-<suffix> Dead` (created, then `PATCH` `active: false`), created as `admin`; part `QA-<suffix> Elsewhere` (active) in a second category `QA-<suffix> Other Cat`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-07 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<Active Cat pk>`, `active=true`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. Not known: depends on open question Q-LST-07 (that all filters sent must match is implied, not stated; `QA-<suffix> Live` only is expected if they do). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 77 · Review · matches: [API-LST-063](lists-and-filters.md) (77), [API-LST-043](lists-and-filters.md) (64), [API-LST-044](lists-and-filters.md) (56), [API-LST-045](lists-and-filters.md) (56), [API-LST-064](lists-and-filters.md) (50)

**Duplicate judgement:** Keep · Combination `category` x `active` vs API-LST-063 `assembly` x `active`; vs API-LST-043 (same request) it cites R-LST-13 and adds an active part in another category, a different starting state (see review finding on the overlap). · test-case-reviewer, 2026-10-14

### API-LST-063: Two attribute filters together return only parts matching both.

| Field | Value |
|---|---|
| **Summary** | Two attribute filters together return only parts matching both. |
| **Requirement** | `R-LST-13` ([L432](../../requirements/openapi-parts.yaml#L432)), `R-LST-12` ([L455](../../requirements/openapi-parts.yaml#L455), [L479](../../requirements/openapi-parts.yaml#L479), [L483](../../requirements/openapi-parts.yaml#L483), [L570](../../requirements/openapi-parts.yaml#L570), [L591](../../requirements/openapi-parts.yaml#L591), [L671](../../requirements/openapi-parts.yaml#L671), [L684](../../requirements/openapi-parts.yaml#L684), [L710](../../requirements/openapi-parts.yaml#L710), [L714](../../requirements/openapi-parts.yaml#L714), [L728](../../requirements/openapi-parts.yaml#L728)), `R-LST-08` ([L447](../../requirements/openapi-parts.yaml#L447)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Decision table (assembly x active) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Combo Cat` with parts `QA-<suffix> X1` (assembly, active), `QA-<suffix> X2` (assembly, inactive) and `QA-<suffix> X3` (not assembly, active), created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-07 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `assembly=true`, `active=true`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList`. Not known: depends on open question Q-LST-07 (that all filters sent must match is implied, not stated; `QA-<suffix> X1` only is expected if they do). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 77 · Review · matches: [API-LST-062](lists-and-filters.md) (77), [API-LST-043](lists-and-filters.md) (53), [API-LST-045](lists-and-filters.md) (51), [API-LST-044](lists-and-filters.md) (50)

**Duplicate judgement:** Keep · Combination `assembly` x `active` (data with one part failing each filter) vs API-LST-062 `category` x `active`; API-LST-043/044/045 use `active` alone. · test-case-reviewer, 2026-10-14

### API-LST-064: `search`, `ordering`, `limit` and `offset` work together.

| Field | Value |
|---|---|
| **Summary** | `search`, `ordering`, `limit` and `offset` work together. |
| **Requirement** | `R-LST-13` ([L432](../../requirements/openapi-parts.yaml#L432)), `R-LST-04` ([L687](../../requirements/openapi-parts.yaml#L687)), `R-LST-05` ([L615](../../requirements/openapi-parts.yaml#L615)), `R-LST-02` ([L578](../../requirements/openapi-parts.yaml#L578)), `R-LST-03` ([L604](../../requirements/openapi-parts.yaml#L604)). Schema: `requirements/openapi-parts.yaml GET /api/part/` ([L432](../../requirements/openapi-parts.yaml#L432)), response `components.schemas.PaginatedPartList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Exploratory (all list parameters in one request) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: category `QA-<suffix> Order Cat` and three parts `QA-<suffix> Banana`, `QA-<suffix> Apple`, `QA-<suffix> Cherry` in it, created in this order with `POST /api/part/` as `admin` (pks ascending); Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-07 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `category=<cat pk>`, `search=QA-<suffix>`, `ordering=-name`, `limit=1`, `offset=1` | `200 OK`. Body is valid against `PaginatedPartList`. Not known: depends on open question Q-LST-07 (that all parameters apply together is implied, not stated; `count` `3` and the single result `QA-<suffix> Banana` are expected if they do). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 50 · Review · matches: [API-LST-062](lists-and-filters.md) (50)

**Duplicate judgement:** Keep · Combines `search`, `ordering`, `limit` and `offset` vs API-LST-062 two filters (`category`, `active`): different parameters and rules. · test-case-reviewer, 2026-10-14

### API-LST-065: `parent=<pk>&cascade=false` returns only the direct children.

| Field | Value |
|---|---|
| **Summary** | `parent=<pk>&cascade=false` returns only the direct children. |
| **Requirement** | `R-LST-15` ([L902](../../requirements/openapi-parts.yaml#L902), [L853](../../requirements/openapi-parts.yaml#L853), [L923](../../requirements/openapi-parts.yaml#L923)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: parent, cascade off) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Root`, `QA-<suffix> Child` (parent Root) and `QA-<suffix> Grand` (parent Child), created with `POST /api/part/category/` as `admin`; parts `QA-<suffix> PR` (in Root), `QA-<suffix> PC` (in Child) and `QA-<suffix> PG` (in Grand), created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `parent=<Root pk>`, `cascade=false`, `limit=10` | `200 OK`. Body is valid against `PaginatedCategoryList`. `count` is `1`; the only result is `QA-<suffix> Child`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 71 · Review · matches: [API-LST-066](lists-and-filters.md) (71), [API-LST-067](lists-and-filters.md) (66), [API-LST-070](lists-and-filters.md) (65), [API-LST-068](lists-and-filters.md) (63), [API-LST-069](lists-and-filters.md) (61), +2 more

**Duplicate judgement:** Keep · `parent` with `cascade=false` (Child only) vs API-LST-066 `cascade=true` (Child, Grand) and API-LST-067 omitted; API-LST-068/069/070 are other filters. · test-case-reviewer, 2026-10-14

### API-LST-066: `parent=<pk>&cascade=true` also returns grandchildren.

| Field | Value |
|---|---|
| **Summary** | `parent=<pk>&cascade=true` also returns grandchildren. |
| **Requirement** | `R-LST-15` ([L902](../../requirements/openapi-parts.yaml#L902), [L853](../../requirements/openapi-parts.yaml#L853), [L923](../../requirements/openapi-parts.yaml#L923)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: parent, cascade on) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Root`, `QA-<suffix> Child` (parent Root) and `QA-<suffix> Grand` (parent Child), created with `POST /api/part/category/` as `admin`; parts `QA-<suffix> PR` (in Root), `QA-<suffix> PC` (in Child) and `QA-<suffix> PG` (in Grand), created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `parent=<Root pk>`, `cascade=true`, `limit=10` | `200 OK`. Body is valid against `PaginatedCategoryList`. `count` is `2`; results are `QA-<suffix> Child` and `QA-<suffix> Grand`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 71 · Review · matches: [API-LST-065](lists-and-filters.md) (71), [API-LST-068](lists-and-filters.md) (67), [API-LST-067](lists-and-filters.md) (66), [API-LST-069](lists-and-filters.md) (63), [API-LST-070](lists-and-filters.md) (60), +4 more

**Duplicate judgement:** Keep · `parent` with `cascade=true` (Child, Grand) vs API-LST-065 `false` and API-LST-067 omitted; API-LST-068/069/070 are other filters. · test-case-reviewer, 2026-10-14

### API-LST-067: `parent=<pk>` without `cascade` returns direct children, or all descendants, by the default.

| Field | Value |
|---|---|
| **Summary** | `parent=<pk>` without `cascade` returns direct children, or all descendants, by the default. |
| **Requirement** | `R-LST-15` ([L902](../../requirements/openapi-parts.yaml#L902), [L853](../../requirements/openapi-parts.yaml#L853), [L923](../../requirements/openapi-parts.yaml#L923)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Decision table (cascade omitted) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Root`, `QA-<suffix> Child` (parent Root) and `QA-<suffix> Grand` (parent Child), created with `POST /api/part/category/` as `admin`; parts `QA-<suffix> PR` (in Root), `QA-<suffix> PC` (in Child) and `QA-<suffix> PG` (in Grand), created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-05 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `parent=<Root pk>`, `limit=10` | `200 OK`. Body is valid against `PaginatedCategoryList`. `QA-<suffix> Child` is in the results. Not known: depends on open question Q-LST-05 (default of `cascade`: whether `QA-<suffix> Grand` is also returned). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 66 · Review · matches: [API-LST-065](lists-and-filters.md) (66), [API-LST-066](lists-and-filters.md) (66), [API-LST-072](lists-and-filters.md) (65), [API-LST-068](lists-and-filters.md) (60), [API-LST-069](lists-and-filters.md) (58), +2 more

**Duplicate judgement:** Keep · `parent` with `cascade` omitted (default under Q-LST-05) vs API-LST-065/066 with it sent; API-LST-072/068/069 are other filters. · test-case-reviewer, 2026-10-14

### API-LST-068: `top_level=true` returns only categories without a parent.

| Field | Value |
|---|---|
| **Summary** | `top_level=true` returns only categories without a parent. |
| **Requirement** | `R-LST-15` ([L902](../../requirements/openapi-parts.yaml#L902), [L853](../../requirements/openapi-parts.yaml#L853), [L923](../../requirements/openapi-parts.yaml#L923)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: true) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Root`, `QA-<suffix> Child` (parent Root) and `QA-<suffix> Grand` (parent Child), created with `POST /api/part/category/` as `admin`; parts `QA-<suffix> PR` (in Root), `QA-<suffix> PC` (in Child) and `QA-<suffix> PG` (in Grand), created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `top_level=true`, `limit=100` | `200 OK`. Body is valid against `PaginatedCategoryList`. `QA-<suffix> Root` is in the results; `QA-<suffix> Child` and `QA-<suffix> Grand` are not; every result has `parent` `null`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** `limit=100` is above the 28 categories observed on the demo data (`test-cases/findings.md#F-09`); the maximum page size is not stated (Q-LST-04).

**Duplicate check:** 73 · Review · matches: [API-LST-069](lists-and-filters.md) (73), [API-LST-070](lists-and-filters.md) (68), [API-LST-066](lists-and-filters.md) (67), [API-LST-065](lists-and-filters.md) (63), [API-LST-067](lists-and-filters.md) (60), +2 more

**Duplicate judgement:** Keep · `top_level` filter vs API-LST-069/070 `structural` and API-LST-065/066/067 `parent`: different filters of R-LST-15. · test-case-reviewer, 2026-10-14

### API-LST-069: `structural=true` returns only structural categories.

| Field | Value |
|---|---|
| **Summary** | `structural=true` returns only structural categories. |
| **Requirement** | `R-LST-15` ([L902](../../requirements/openapi-parts.yaml#L902), [L853](../../requirements/openapi-parts.yaml#L853), [L923](../../requirements/openapi-parts.yaml#L923)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: true) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Structural` (`structural` `true`) and `QA-<suffix> Normal` (`structural` `false`), created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `structural=true`, `limit=100` | `200 OK`. Body is valid against `PaginatedCategoryList`. `QA-<suffix> Structural` is in the results; `QA-<suffix> Normal` is not; every result has `structural` `true`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 78 · Review · matches: [API-LST-070](lists-and-filters.md) (78), [API-LST-068](lists-and-filters.md) (73), [API-LST-066](lists-and-filters.md) (63), [API-LST-065](lists-and-filters.md) (61), [API-LST-067](lists-and-filters.md) (58), +2 more

**Duplicate judgement:** Keep · `structural=true` vs API-LST-070 `structural=false` (opposite class and outcome); API-LST-068 and API-LST-065/066/067 are other filters. · test-case-reviewer, 2026-10-14

### API-LST-070: `structural=false` returns only non-structural categories.

| Field | Value |
|---|---|
| **Summary** | `structural=false` returns only non-structural categories. |
| **Requirement** | `R-LST-15` ([L902](../../requirements/openapi-parts.yaml#L902), [L853](../../requirements/openapi-parts.yaml#L853), [L923](../../requirements/openapi-parts.yaml#L923)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: false) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Structural` (`structural` `true`) and `QA-<suffix> Normal` (`structural` `false`), created as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `structural=false`, `limit=100` | `200 OK`. Body is valid against `PaginatedCategoryList`. `QA-<suffix> Normal` is in the results; `QA-<suffix> Structural` is not; every result has `structural` `false`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 78 · Review · matches: [API-LST-069](lists-and-filters.md) (78), [API-LST-068](lists-and-filters.md) (68), [API-LST-065](lists-and-filters.md) (65), [API-LST-066](lists-and-filters.md) (60), [API-LST-067](lists-and-filters.md) (58), +2 more

**Duplicate judgement:** Keep · `structural=false` vs API-LST-069 `structural=true`; API-LST-068 and API-LST-065/066/067 are other filters. · test-case-reviewer, 2026-10-14

### API-LST-071: `depth` filters categories by their level in the tree.

| Field | Value |
|---|---|
| **Summary** | `depth` filters categories by their level in the tree. |
| **Requirement** | `R-LST-15` ([L902](../../requirements/openapi-parts.yaml#L902), [L853](../../requirements/openapi-parts.yaml#L853), [L923](../../requirements/openapi-parts.yaml#L923)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: depth of an existing level) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Root`, `QA-<suffix> Child` (parent Root) and `QA-<suffix> Grand` (parent Child), created with `POST /api/part/category/` as `admin`; parts `QA-<suffix> PR` (in Root), `QA-<suffix> PC` (in Child) and `QA-<suffix> PG` (in Grand), created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-10 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `depth=1`, `limit=100` | `200 OK`. Body is valid against `PaginatedCategoryList`. Not known: depends on open question Q-LST-10 (whether the top level is depth 0 or 1, and whether `depth` means exactly that level or up to it). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 60 · Review · matches: [API-LST-072](lists-and-filters.md) (60), [API-LST-067](lists-and-filters.md) (58), [API-LST-068](lists-and-filters.md) (58), [API-LST-069](lists-and-filters.md) (58), [API-LST-070](lists-and-filters.md) (58), +2 more

**Duplicate judgement:** Keep · `depth` filter vs API-LST-072 `name`, API-LST-067 `parent`, API-LST-068 `top_level` and API-LST-069/070 `structural`: different filters of R-LST-15. · test-case-reviewer, 2026-10-14

### API-LST-072: `name` filters categories by name.

| Field | Value |
|---|---|
| **Summary** | `name` filters categories by name. |
| **Requirement** | `R-LST-15` ([L902](../../requirements/openapi-parts.yaml#L902), [L853](../../requirements/openapi-parts.yaml#L853), [L923](../../requirements/openapi-parts.yaml#L923)). Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | LST |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: full name of one category) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `reader` (view access); Settings: None; Data: categories `QA-<suffix> Root`, `QA-<suffix> Child` (parent Root) and `QA-<suffix> Grand` (parent Child), created with `POST /api/part/category/` as `admin`; parts `QA-<suffix> PR` (in Root), `QA-<suffix> PC` (in Child) and `QA-<suffix> PG` (in Grand), created with `POST /api/part/` as `admin`; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-LST-11 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `name=QA-<suffix> Child`, `limit=10` | `200 OK`. Body is valid against `PaginatedCategoryList`. `QA-<suffix> Child` is in the results. Not known: depends on open question Q-LST-11 (whether `name` is an exact or a partial, case-insensitive match, so whether `QA-<suffix> Grand` could also appear). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part `PATCH /api/part/<pk>/` with `{"active": false}` and `DELETE /api/part/<pk>/` (`204`); then for each category, children first, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None

**Duplicate check:** 65 · Review · matches: [API-LST-067](lists-and-filters.md) (65), [API-LST-071](lists-and-filters.md) (60), [API-LST-066](lists-and-filters.md) (59), [API-LST-065](lists-and-filters.md) (58), [API-LST-068](lists-and-filters.md) (58), +2 more

**Duplicate judgement:** Keep · `name` filter vs API-LST-067/066/065 `parent`, API-LST-071 `depth` and API-LST-068 `top_level`: different filters of R-LST-15. · test-case-reviewer, 2026-10-14
