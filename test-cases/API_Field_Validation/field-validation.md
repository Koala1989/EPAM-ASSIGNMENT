# Field validation: VAL test cases

### API-VAL-001: Create a part without `name` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part without `name` is rejected. |
| **Requirement** | R-VAL-01. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name` ([L4365](../../requirements/openapi-parts.yaml#L4365)) (in the `required` list, not `readOnly`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: required field missing) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"description": "QA-<suffix> no name"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** Only `name` is input-required (index, Schema issues #4). The rejected payload has no searchable name, so step 2 relies on `search` also matching `description`; if it does not, compare `count` of `GET /api/part/` with `limit=1` before and after.

**Duplicate check:** 90 · Review · matches: [API-VAL-004](field-validation.md) (90, test data differs), [API-VAL-003](field-validation.md) (88, test data differs), [API-VAL-008](field-validation.md) (70), [API-VAL-010](field-validation.md) (70), [API-VAL-012](field-validation.md) (70), +18 more

**Duplicate judgement:** Keep · Missing `name` is its own invalid class (required field absent); API-VAL-004 sends `null` and API-VAL-003 tests the maxLength + 1 boundary, and the others are other fields or rules. · test-case-reviewer, 2026-10-14

### API-VAL-002: Create a part with a 100-character name is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with a 100-character name is accepted. |
| **Requirement** | R-VAL-01. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name` ([L4196](../../requirements/openapi-parts.yaml#L4196)) (`maxLength: 100`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (name maxLength, on the limit) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> + padding, 100 characters"}` | `201 Created`. Body is valid against `Part`; `name` equals the payload and has 100 characters. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 70 · Review · matches: [API-VAL-009](field-validation.md) (70), [API-VAL-007](field-validation.md) (58), [API-VAL-011](field-validation.md) (58), [API-VAL-018](field-validation.md) (58), [API-VAL-021](field-validation.md) (55), +3 more

**Duplicate judgement:** Keep · On-limit boundary of Part `name` (R-VAL-01); every match is the on-limit boundary of a different field and rule (IPN R-VAL-03, description R-VAL-02, keywords, link, units). · test-case-reviewer, 2026-10-14

### API-VAL-003: Create a part with a 101-character name is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a 101-character name is rejected. |
| **Requirement** | R-VAL-01. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name` ([L4196](../../requirements/openapi-parts.yaml#L4196)) (`maxLength: 100`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (name maxLength + 1) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> + padding, 101 characters"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 88 · Review · matches: [API-VAL-001](field-validation.md) (88, test data differs), [API-VAL-004](field-validation.md) (84, test data differs), [API-VAL-010](field-validation.md) (77), [API-VAL-024](field-validation.md) (75), [API-VAL-008](field-validation.md) (71), +18 more

**Duplicate judgement:** Keep · Part `name` maxLength + 1 boundary; API-VAL-001 (missing) and API-VAL-004 (null) are other invalid classes of the same field, the rest are other fields' limits. · test-case-reviewer, 2026-10-14

### API-VAL-004: Create a part with `name` null is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with `name` null is rejected. |
| **Requirement** | R-VAL-01. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name` ([L4196](../../requirements/openapi-parts.yaml#L4196)) (`type: string`, not `nullable`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: null for a non-nullable field) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": null, "description": "QA-<suffix> null name"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** `name` is not `nullable` in the schema. The rejected payload has no searchable name, so step 2 relies on `search` also matching `description`; if it does not, compare `count` of `GET /api/part/` with `limit=1` before and after.

**Duplicate check:** 90 · Review · matches: [API-VAL-001](field-validation.md) (90, test data differs), [API-VAL-003](field-validation.md) (84, test data differs), [API-VAL-008](field-validation.md) (69), [API-VAL-010](field-validation.md) (69), [API-VAL-012](field-validation.md) (69), +17 more

**Duplicate judgement:** Keep · `null` for a non-nullable field is a different invalid class from the absent field (API-VAL-001) and from the 101-character boundary (API-VAL-003). · test-case-reviewer, 2026-10-14

### API-VAL-005: Create a part with an empty `name`

| Field | Value |
|---|---|
| **Summary** | Create a part with an empty `name`. |
| **Requirement** | R-VAL-01. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name` ([L4196](../../requirements/openapi-parts.yaml#L4196)) (no `minLength` stated). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty string), Error guessing (empty required text) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01, Q-VAL-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "", "description": "QA-<suffix> empty name"}` | Not known: depends on open questions Q-VAL-01, Q-VAL-04 (whether an empty `name` is rejected, and the status and error body). |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | Not known: depends on open question Q-VAL-04 (`count` is `0` if the request is rejected, `1` if it is accepted). |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** The rejected payload has no searchable name, so step 2 relies on `search` also matching `description`; if it does not, compare `count` of `GET /api/part/` with `limit=1` before and after.

**Duplicate check:** 81 · Duplicate · matches: [API-VAL-006](field-validation.md) (81), [API-VAL-001](field-validation.md) (68), [API-VAL-004](field-validation.md) (66), [API-VAL-003](field-validation.md) (64), [API-VAL-047](field-validation.md) (54), +1 more

**Duplicate judgement:** Keep · Empty string is a different class from the whitespace-only name of API-VAL-006 (which also asks about trimming, Q-VAL-04) and from the absent, null and over-limit names; API-VAL-047 is the category rule R-VAL-13. · test-case-reviewer, 2026-10-14

### API-VAL-006: Create a part with a whitespace-only `name`

| Field | Value |
|---|---|
| **Summary** | Create a part with a whitespace-only `name`. |
| **Requirement** | R-VAL-01. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name` ([L4196](../../requirements/openapi-parts.yaml#L4196)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (whitespace-only text) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01, Q-VAL-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "   ", "description": "QA-<suffix> blank name"}` | Not known: depends on open questions Q-VAL-01, Q-VAL-04 (whether a whitespace-only `name` is rejected, stored trimmed or stored as is, and the status and error body). |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | Not known: depends on open question Q-VAL-04 (`count` is `0` if the request is rejected, `1` if it is accepted). |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** The rejected payload has no searchable name, so step 2 relies on `search` also matching `description`; if it does not, compare `count` of `GET /api/part/` with `limit=1` before and after.

**Duplicate check:** 81 · Duplicate · matches: [API-VAL-005](field-validation.md) (81), [API-VAL-001](field-validation.md) (67), [API-VAL-004](field-validation.md) (66), [API-VAL-003](field-validation.md) (64)

**Duplicate judgement:** Keep · Whitespace-only is a different class from the empty string of API-VAL-005: it can be stored as is, trimmed or rejected (Q-VAL-04), so the expected outcome can differ. · test-case-reviewer, 2026-10-14

### API-VAL-007: Create a part with a 250-character description is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with a 250-character description is accepted. |
| **Requirement** | R-VAL-02. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.description` ([L4148](../../requirements/openapi-parts.yaml#L4148)) (`maxLength: 250`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (description maxLength, on the limit) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Desc 250", "description": "250 characters"}` | `201 Created`. Body is valid against `Part`; `description` equals the payload and has 250 characters. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 67 · Review · matches: [API-VAL-011](field-validation.md) (67), [API-VAL-002](field-validation.md) (58), [API-VAL-009](field-validation.md) (57), [API-VAL-018](field-validation.md) (57), [API-VAL-021](field-validation.md) (54), +2 more

**Duplicate judgement:** Keep · On-limit boundary of Part `description` (R-VAL-02); each match is the on-limit boundary of a different field and rule (keywords R-VAL-04, name, IPN, link, units). · test-case-reviewer, 2026-10-14

### API-VAL-008: Create a part with a 251-character description is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a 251-character description is rejected. |
| **Requirement** | R-VAL-02. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.description` ([L4148](../../requirements/openapi-parts.yaml#L4148)) (`maxLength: 250`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (description maxLength + 1) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Desc 251", "description": "251 characters"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 75 · Review · matches: [API-VAL-012](field-validation.md) (75), [API-VAL-003](field-validation.md) (71), [API-VAL-001](field-validation.md) (70), [API-VAL-010](field-validation.md) (70), [API-VAL-022](field-validation.md) (70), +17 more

**Duplicate judgement:** Keep · maxLength + 1 of Part `description` (R-VAL-02); the matches are over-limit or invalid cases of other fields and rules (keywords R-VAL-04, name, IPN, units). · test-case-reviewer, 2026-10-14

### API-VAL-009: Create a part with a 100-character IPN is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with a 100-character IPN is accepted. |
| **Requirement** | R-VAL-03. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.IPN` ([L4164](../../requirements/openapi-parts.yaml#L4164)) (`maxLength: 100`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (IPN maxLength, on the limit) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> IPN 100", "IPN": "QA-<suffix> + padding, 100 characters"}` | `201 Created`. Body is valid against `Part`; `IPN` equals the payload and has 100 characters. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** The IPN carries the run suffix, so it is unique even if `PART_ALLOW_DUPLICATE_IPN` is off.

**Duplicate check:** 70 · Review · matches: [API-VAL-002](field-validation.md) (70), [API-VAL-011](field-validation.md) (58), [API-VAL-007](field-validation.md) (57), [API-VAL-018](field-validation.md) (57), [API-VAL-021](field-validation.md) (54), +3 more

**Duplicate judgement:** Keep · On-limit boundary of `IPN` (R-VAL-03); API-VAL-002 is the same limit value on `name` (R-VAL-01), a different field and rule, and the rest are other fields. · test-case-reviewer, 2026-10-14

### API-VAL-010: Create a part with a 101-character IPN is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a 101-character IPN is rejected. |
| **Requirement** | R-VAL-03. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.IPN` ([L4164](../../requirements/openapi-parts.yaml#L4164)) (`maxLength: 100`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (IPN maxLength + 1) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> IPN 101", "IPN": "QA-<suffix> + padding, 101 characters"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 77 · Review · matches: [API-VAL-003](field-validation.md) (77), [API-VAL-024](field-validation.md) (74), [API-VAL-001](field-validation.md) (70), [API-VAL-008](field-validation.md) (70), [API-VAL-012](field-validation.md) (70), +15 more

**Duplicate judgement:** Keep · maxLength + 1 of `IPN` (R-VAL-03); API-VAL-003 and API-VAL-024 test the same limit on `name` (R-VAL-01) and `revision` (R-VAL-07), different fields and rules. · test-case-reviewer, 2026-10-14

### API-VAL-011: Create a part with 250-character keywords is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with 250-character keywords is accepted. |
| **Requirement** | R-VAL-04. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.keywords` ([L4171](../../requirements/openapi-parts.yaml#L4171)) (`maxLength: 250`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (keywords maxLength, on the limit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Keywords 250", "keywords": "250 characters"}` | `201 Created`. Body is valid against `Part`; `keywords` equals the payload and has 250 characters. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 67 · Review · matches: [API-VAL-007](field-validation.md) (67), [API-VAL-002](field-validation.md) (58), [API-VAL-009](field-validation.md) (58), [API-VAL-018](field-validation.md) (57), [API-VAL-021](field-validation.md) (55), +2 more

**Duplicate judgement:** Keep · On-limit boundary of `keywords` (R-VAL-04); API-VAL-007 is the same 250 limit on `description` (R-VAL-02), a different field and rule. · test-case-reviewer, 2026-10-14

### API-VAL-012: Create a part with 251-character keywords is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with 251-character keywords is rejected. |
| **Requirement** | R-VAL-04. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.keywords` ([L4171](../../requirements/openapi-parts.yaml#L4171)) (`maxLength: 250`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (keywords maxLength + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Keywords 251", "keywords": "251 characters"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 75 · Review · matches: [API-VAL-008](field-validation.md) (75), [API-VAL-003](field-validation.md) (71), [API-VAL-001](field-validation.md) (70), [API-VAL-010](field-validation.md) (70), [API-VAL-017](field-validation.md) (70), +15 more

**Duplicate judgement:** Keep · maxLength + 1 of `keywords` (R-VAL-04); API-VAL-008 is the same limit on `description` (R-VAL-02), and the rest are other fields or classes. · test-case-reviewer, 2026-10-14

### API-VAL-013: Create a part with `keywords` null is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with `keywords` null is accepted. |
| **Requirement** | R-VAL-04. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.keywords` ([L4171](../../requirements/openapi-parts.yaml#L4171)) (`nullable: true`). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: null for a nullable field) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Keywords null", "keywords": null}` | `201 Created`. Body is valid against `Part`; `keywords` is `null`. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 64 · Review · matches: [API-VAL-016](field-validation.md) (64), [API-VAL-020](field-validation.md) (64), [API-VAL-039](field-validation.md) (64), [API-VAL-014](field-validation.md) (55), [API-VAL-030](field-validation.md) (53), +2 more

**Duplicate judgement:** Keep · `null` for nullable `keywords` (R-VAL-04); the matches send `null` to other nullable fields under other rules (`link` R-VAL-05, `units` R-VAL-06, `category` R-VAL-10). · test-case-reviewer, 2026-10-14

### API-VAL-014: Create a part with a valid URI in `link` is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with a valid URI in `link` is accepted. |
| **Requirement** | R-VAL-05. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.link` ([L4176](../../requirements/openapi-parts.yaml#L4176)) (`oneOf` URI or empty string, `nullable`). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: URI) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Link URI", "link": "https://example.org/qa-<suffix>"}` | `201 Created`. Body is valid against `Part`; `link` equals the payload. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 75 · Review · matches: [API-VAL-016](field-validation.md) (75), [API-VAL-015](field-validation.md) (68), [API-VAL-013](field-validation.md) (55), [API-VAL-020](field-validation.md) (55), [API-VAL-039](field-validation.md) (55), +2 more

**Duplicate judgement:** Keep · The valid-URI class of `link` (R-VAL-05); API-VAL-016 sends `null` and API-VAL-015 the empty string, the two other valid branches, with a different expected `link` value. · test-case-reviewer, 2026-10-14

### API-VAL-015: Create a part with an empty string in `link` is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with an empty string in `link` is accepted. |
| **Requirement** | R-VAL-05. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.link` ([L4176](../../requirements/openapi-parts.yaml#L4176)) (second `oneOf` branch, `maxLength: 0`). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: empty string) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-07 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Link empty", "link": ""}` | `201 Created`. Body is valid against `Part`. Not known: depends on open question Q-VAL-07 (whether the response `link` is `""` or `null`). |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 71 · Review · matches: [API-VAL-016](field-validation.md) (71), [API-VAL-014](field-validation.md) (68), [API-VAL-013](field-validation.md) (52), [API-VAL-020](field-validation.md) (52), [API-VAL-039](field-validation.md) (52)

**Duplicate judgement:** Keep · The empty-string branch of `link` (`maxLength: 0`, R-VAL-05) is a different valid class from `null` (API-VAL-016) and a URI (API-VAL-014), and its returned value is open (Q-VAL-07). · test-case-reviewer, 2026-10-14

### API-VAL-016: Create a part with `link` null is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with `link` null is accepted. |
| **Requirement** | R-VAL-05. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.link` ([L4176](../../requirements/openapi-parts.yaml#L4176)) (`nullable: true`). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: null) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Link null", "link": null}` | `201 Created`. Body is valid against `Part`; `link` is `null`. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 75 · Review · matches: [API-VAL-014](field-validation.md) (75), [API-VAL-015](field-validation.md) (71), [API-VAL-013](field-validation.md) (64), [API-VAL-020](field-validation.md) (64), [API-VAL-039](field-validation.md) (64), +2 more

**Duplicate judgement:** Keep · `null` for `link` is a different valid class from a URI (API-VAL-014) and the empty string (API-VAL-015); the other matches are `null` on other fields and rules. · test-case-reviewer, 2026-10-14

### API-VAL-017: Create a part with a `link` that is not a URI is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a `link` that is not a URI is rejected. |
| **Requirement** | R-VAL-05. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.link` ([L4176](../../requirements/openapi-parts.yaml#L4176)) (`format: uri`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong format) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Link bad", "link": "not a url"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** The UI shows "Enter a valid URL." for an invalid link (R-Part-17); the API message is not stated.

**Duplicate check:** 84 · Review · matches: [API-VAL-019](field-validation.md) (84, test data differs), [API-VAL-001](field-validation.md) (70), [API-VAL-003](field-validation.md) (70), [API-VAL-012](field-validation.md) (70), [API-VAL-026](field-validation.md) (70), +15 more

**Duplicate judgement:** Keep · Breaks the `format: uri` constraint of `link`; API-VAL-019 breaks the `maxLength: 2000` constraint with a well-formed URI, a different clause of R-VAL-05. · test-case-reviewer, 2026-10-14

### API-VAL-018: Create a part with a 2000-character `link` is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with a 2000-character `link` is accepted. |
| **Requirement** | R-VAL-05. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.link` ([L4176](../../requirements/openapi-parts.yaml#L4176)) (`maxLength: 2000`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (link maxLength, on the limit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Link 2000", "link": "https://example.org/ + path padding, 2000 characters in total"}` | `201 Created`. Body is valid against `Part`; `link` equals the payload and has 2000 characters. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 58 · Review · matches: [API-VAL-002](field-validation.md) (58), [API-VAL-007](field-validation.md) (57), [API-VAL-009](field-validation.md) (57), [API-VAL-011](field-validation.md) (57), [API-VAL-021](field-validation.md) (54), +2 more

**Duplicate judgement:** Keep · On-limit boundary of `link` (2000, R-VAL-05); every match is the on-limit boundary of a different field and rule. · test-case-reviewer, 2026-10-14

### API-VAL-019: Create a part with a 2001-character `link` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a 2001-character `link` is rejected. |
| **Requirement** | R-VAL-05. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.link` ([L4176](../../requirements/openapi-parts.yaml#L4176)) (`maxLength: 2000`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (link maxLength + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Link 2001", "link": "https://example.org/ + path padding, 2001 characters in total"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 84 · Review · matches: [API-VAL-017](field-validation.md) (84, test data differs), [API-VAL-001](field-validation.md) (69), [API-VAL-003](field-validation.md) (69), [API-VAL-008](field-validation.md) (69), [API-VAL-010](field-validation.md) (69), +15 more

**Duplicate judgement:** Keep · maxLength + 1 of `link` with a well-formed URI; API-VAL-017 sends a short non-URI (format clause of R-VAL-05), and the rest are other fields. · test-case-reviewer, 2026-10-14

### API-VAL-020: Create a part with `units` null is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with `units` null is accepted. |
| **Requirement** | R-VAL-06. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.units` ([L4237](../../requirements/openapi-parts.yaml#L4237)) (`nullable: true`). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: null for a nullable field) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Units null", "units": null}` | `201 Created`. Body is valid against `Part`; `units` is `null`. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 64 · Review · matches: [API-VAL-013](field-validation.md) (64), [API-VAL-016](field-validation.md) (64), [API-VAL-039](field-validation.md) (64), [API-VAL-014](field-validation.md) (55), [API-VAL-030](field-validation.md) (53), +2 more

**Duplicate judgement:** Keep · `null` for nullable `units` (R-VAL-06); the matches send `null` to other fields under other rules (`keywords`, `link`, `category`). · test-case-reviewer, 2026-10-14

### API-VAL-021: Create a part with a 20-character `units` value

| Field | Value |
|---|---|
| **Summary** | Create a part with a 20-character `units` value. |
| **Requirement** | R-VAL-06. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.units` ([L4237](../../requirements/openapi-parts.yaml#L4237)) (`maxLength: 20`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (units maxLength, on the limit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-05 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Units 20", "units": "[open: Q-VAL-05, a valid unit string of exactly 20 characters]"}` | `201 Created`. Body is valid against `Part`; `units` equals the payload. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** Unit strings are also checked against the unit rules (Unit_measure), so a 20-character value may be rejected for that reason.

**Duplicate check:** 55 · Review · matches: [API-VAL-002](field-validation.md) (55), [API-VAL-011](field-validation.md) (55), [API-VAL-007](field-validation.md) (54), [API-VAL-009](field-validation.md) (54), [API-VAL-018](field-validation.md) (54), +2 more

**Duplicate judgement:** Keep · On-limit boundary of `units` (20, R-VAL-06), which also depends on the unit check (Q-VAL-05); every match is another field and rule. · test-case-reviewer, 2026-10-14

### API-VAL-022: Create a part with a 21-character `units` value is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a 21-character `units` value is rejected. |
| **Requirement** | R-VAL-06. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.units` ([L4237](../../requirements/openapi-parts.yaml#L4237)) (`maxLength: 20`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (units maxLength + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Units 21", "units": "21 characters"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** A 21-character string is also not a known unit, so the rejection may come from the unit check; the rule under test is the length limit.

**Duplicate check:** 70 · Review · matches: [API-VAL-003](field-validation.md) (70), [API-VAL-008](field-validation.md) (70), [API-VAL-012](field-validation.md) (70), [API-VAL-024](field-validation.md) (70), [API-VAL-001](field-validation.md) (69), +15 more

**Duplicate judgement:** Keep · maxLength + 1 of `units` (R-VAL-06); the matches are over-limit or invalid cases of other fields and rules. · test-case-reviewer, 2026-10-14

### API-VAL-023: Create a part with a 100-character `revision`

| Field | Value |
|---|---|
| **Summary** | Create a part with a 100-character `revision`. |
| **Requirement** | R-VAL-07. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.revision` ([L4207](../../requirements/openapi-parts.yaml#L4207)) (`maxLength: 100`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (revision maxLength, on the limit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Rev 100", "revision": "100 characters"}` | Not known: depends on open question Q-VAL-06 (whether the revision settings allow a `revision` on a part that is not a revision of another part). If created: `201 Created`, body valid against `Part`, `revision` equals the payload. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** Revision settings (REV) may affect whether a revision is accepted on create.

**Duplicate check:** 54 · Review · matches: [API-VAL-002](field-validation.md) (54), [API-VAL-009](field-validation.md) (53)

**Duplicate judgement:** Keep · On-limit boundary of `revision` (R-VAL-07), subject to the revision settings (Q-VAL-06); API-VAL-002 and API-VAL-009 are the same limit on `name` and `IPN`, other rules. · test-case-reviewer, 2026-10-14

### API-VAL-024: Create a part with a 101-character `revision` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a 101-character `revision` is rejected. |
| **Requirement** | R-VAL-07. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.revision` ([L4207](../../requirements/openapi-parts.yaml#L4207)) (`maxLength: 100`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (revision maxLength + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Rev 101", "revision": "101 characters"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 75 · Review · matches: [API-VAL-003](field-validation.md) (75), [API-VAL-010](field-validation.md) (74), [API-VAL-001](field-validation.md) (70), [API-VAL-008](field-validation.md) (70), [API-VAL-012](field-validation.md) (70), +15 more

**Duplicate judgement:** Keep · maxLength + 1 of `revision` (R-VAL-07); API-VAL-003 and API-VAL-010 test the same limit on `name` (R-VAL-01) and `IPN` (R-VAL-03). · test-case-reviewer, 2026-10-14

### API-VAL-025: Create a part with `default_expiry` 0 is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with `default_expiry` 0 is accepted. |
| **Requirement** | R-VAL-08. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.default_expiry` ([L4139](../../requirements/openapi-parts.yaml#L4139)) (`minimum: 0`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (default_expiry minimum, on the limit) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Expiry 0", "default_expiry": 0}` | `201 Created`. Body is valid against `Part`; `default_expiry` is `0`. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 81 · Review · matches: [API-VAL-027](field-validation.md) (81, test data differs), [API-VAL-021](field-validation.md) (54), [API-VAL-002](field-validation.md) (53), [API-VAL-007](field-validation.md) (53), [API-VAL-009](field-validation.md) (53), +2 more

**Duplicate judgement:** Keep · On the `minimum: 0` boundary of `default_expiry`; API-VAL-027 is on the `maximum` boundary, a different boundary of R-VAL-08. · test-case-reviewer, 2026-10-14

### API-VAL-026: Create a part with `default_expiry` -1 is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with `default_expiry` -1 is rejected. |
| **Requirement** | R-VAL-08. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.default_expiry` ([L4139](../../requirements/openapi-parts.yaml#L4139)) (`minimum: 0`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (default_expiry minimum - 1) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Expiry -1", "default_expiry": -1}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 89 · Duplicate · matches: [API-VAL-028](field-validation.md) (89), [API-VAL-029](field-validation.md) (79), [API-VAL-001](field-validation.md) (70), [API-VAL-003](field-validation.md) (70), [API-VAL-012](field-validation.md) (70), +15 more

**Duplicate judgement:** Keep · Below the `minimum: 0` boundary (-1); API-VAL-028 is above the `maximum` boundary and API-VAL-029 a wrong type, different boundaries and classes of R-VAL-08. · test-case-reviewer, 2026-10-14

### API-VAL-027: Create a part with `default_expiry` 2147483647 is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with `default_expiry` 2147483647 is accepted. |
| **Requirement** | R-VAL-08. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.default_expiry` ([L4139](../../requirements/openapi-parts.yaml#L4139)) (`maximum: 2147483647`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (default_expiry maximum, on the limit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Expiry max", "default_expiry": 2147483647}` | `201 Created`. Body is valid against `Part`; `default_expiry` is `2147483647`. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 81 · Review · matches: [API-VAL-025](field-validation.md) (81, test data differs), [API-VAL-021](field-validation.md) (54), [API-VAL-002](field-validation.md) (53), [API-VAL-007](field-validation.md) (53), [API-VAL-009](field-validation.md) (53), +2 more

**Duplicate judgement:** Keep · On the `maximum: 2147483647` boundary of `default_expiry`; API-VAL-025 is on the `minimum` boundary, a different boundary of R-VAL-08. · test-case-reviewer, 2026-10-14

### API-VAL-028: Create a part with `default_expiry` 2147483648 is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with `default_expiry` 2147483648 is rejected. |
| **Requirement** | R-VAL-08. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.default_expiry` ([L4139](../../requirements/openapi-parts.yaml#L4139)) (`maximum: 2147483647`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (default_expiry maximum + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Expiry max+1", "default_expiry": 2147483648}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 89 · Duplicate · matches: [API-VAL-026](field-validation.md) (89), [API-VAL-029](field-validation.md) (79), [API-VAL-001](field-validation.md) (70), [API-VAL-003](field-validation.md) (69), [API-VAL-004](field-validation.md) (69), +15 more

**Duplicate judgement:** Keep · Above the `maximum` boundary (2147483648); API-VAL-026 is below the `minimum` boundary and API-VAL-029 a wrong type, different boundaries and classes of R-VAL-08. · test-case-reviewer, 2026-10-14

### API-VAL-029: Create a part with a non-numeric `default_expiry` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a non-numeric `default_expiry` is rejected. |
| **Requirement** | R-VAL-08, R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.default_expiry` ([L4139](../../requirements/openapi-parts.yaml#L4139)) (`type: integer`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Expiry text", "default_expiry": "abc"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 79 · Review · matches: [API-VAL-026](field-validation.md) (79), [API-VAL-028](field-validation.md) (79), [API-VAL-032](field-validation.md) (78), [API-VAL-035](field-validation.md) (78), [API-VAL-036](field-validation.md) (78), +15 more

**Duplicate judgement:** Keep · Wrong type (text) for `default_expiry`; API-VAL-026 and API-VAL-028 are out-of-range integers, and API-VAL-032, 035 and 036 send text to other fields (`minimum_stock` R-VAL-09, `category`, `default_location`). · test-case-reviewer, 2026-10-14

### API-VAL-030: Create a part without stock limits: `minimum_stock` and `maximum_stock` default to 0

| Field | Value |
|---|---|
| **Summary** | Create a part without stock limits: `minimum_stock` and `maximum_stock` default to 0. |
| **Requirement** | R-VAL-09. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.minimum_stock` ([L4188](../../requirements/openapi-parts.yaml#L4188)) (`default: 0.0`). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: field omitted, default applies) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Stock default"}` | `201 Created`. Body is valid against `Part`; `minimum_stock` and `maximum_stock` equal `0`. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 73 · Review · matches: [API-VAL-031](field-validation.md) (73), [API-VAL-013](field-validation.md) (53), [API-VAL-016](field-validation.md) (53), [API-VAL-020](field-validation.md) (53), [API-VAL-039](field-validation.md) (53), +1 more

**Duplicate judgement:** Keep · Tests the `default: 0` clause of R-VAL-09 with the fields omitted; API-VAL-031 sends explicit decimal values (the type clause), with a different expected value. · test-case-reviewer, 2026-10-14

### API-VAL-031: Create a part with decimal `minimum_stock` and `maximum_stock`

| Field | Value |
|---|---|
| **Summary** | Create a part with decimal `minimum_stock` and `maximum_stock`. |
| **Requirement** | R-VAL-09. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.minimum_stock` ([L4188](../../requirements/openapi-parts.yaml#L4188)) (`type: number`). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: decimal numbers) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Stock decimal", "minimum_stock": 10.5, "maximum_stock": 100.25}` | `201 Created`. Body is valid against `Part`; `minimum_stock` is `10.5` and `maximum_stock` is `100.25`. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 73 · Review · matches: [API-VAL-030](field-validation.md) (73), [API-VAL-013](field-validation.md) (53), [API-VAL-016](field-validation.md) (53), [API-VAL-020](field-validation.md) (53), [API-VAL-039](field-validation.md) (53), +1 more

**Duplicate judgement:** Keep · Explicit decimal values (the `type: number` clause of R-VAL-09); API-VAL-030 omits the fields to check the default, a different class and expected value. · test-case-reviewer, 2026-10-14

### API-VAL-032: Create a part with a non-numeric `minimum_stock` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a non-numeric `minimum_stock` is rejected. |
| **Requirement** | R-VAL-09, R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.minimum_stock` ([L4188](../../requirements/openapi-parts.yaml#L4188)) (`type: number`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Stock text", "minimum_stock": "abc"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 78 · Review · matches: [API-VAL-029](field-validation.md) (78), [API-VAL-035](field-validation.md) (78), [API-VAL-036](field-validation.md) (78), [API-VAL-037](field-validation.md) (78), [API-VAL-038](field-validation.md) (76), +15 more

**Duplicate judgement:** Keep · Wrong type for `minimum_stock` (R-VAL-09, a number); the matches send the wrong type to other fields under other rules (`default_expiry` R-VAL-08, FK integers and a boolean under R-VAL-10). · test-case-reviewer, 2026-10-14

### API-VAL-033: Create a part with a negative `minimum_stock`

| Field | Value |
|---|---|
| **Summary** | Create a part with a negative `minimum_stock`. |
| **Requirement** | R-VAL-09. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.minimum_stock` ([L4188](../../requirements/openapi-parts.yaml#L4188)) (no `minimum` stated). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (below zero, limit not stated) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Stock negative", "minimum_stock": -1}` | Not known: depends on open question Q-VAL-03 (whether a negative `minimum_stock` is accepted, and the status and body if rejected). |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 62 · Review · matches: [API-VAL-067](field-validation.md) (62)

**Duplicate judgement:** Keep · Negative `minimum_stock` on the Part (R-VAL-09); API-VAL-067 sends a negative `initial_stock.quantity`, a different field, schema component and rule (R-VAL-18). · test-case-reviewer, 2026-10-14

### API-VAL-034: Create a part whose `minimum_stock` is above `maximum_stock`

| Field | Value |
|---|---|
| **Summary** | Create a part whose `minimum_stock` is above `maximum_stock`. |
| **Requirement** | R-VAL-09. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.minimum_stock` ([L4188](../../requirements/openapi-parts.yaml#L4188)), `components.schemas.Part.maximum_stock` ([L4192](../../requirements/openapi-parts.yaml#L4192)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Decision table (minimum above maximum), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Stock min>max", "minimum_stock": 100, "maximum_stock": 10}` | Not known: depends on open question Q-VAL-03 (whether `minimum_stock` greater than `maximum_stock` is accepted or rejected, and the status and body). |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

### API-VAL-035: Create a part with a non-integer `category` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a non-integer `category` is rejected. |
| **Requirement** | R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.category` ([L4122](../../requirements/openapi-parts.yaml#L4122)) (`type: integer`, `nullable`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type, text for an integer ID) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Category text", "category": "abc"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 88 · Review · matches: [API-VAL-036](field-validation.md) (88, test data differs), [API-VAL-037](field-validation.md) (88, test data differs), [API-VAL-038](field-validation.md) (83, test data differs), [API-VAL-029](field-validation.md) (78), [API-VAL-032](field-validation.md) (78), +15 more

**Duplicate judgement:** Keep · Wrong type for `category`, one of the fields R-VAL-10 names; API-VAL-036 and API-VAL-037 cover the separately named `default_location` and `variant_of` clauses, and API-VAL-038 a boolean. · test-case-reviewer, 2026-10-14

### API-VAL-036: Create a part with a non-integer `default_location` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a non-integer `default_location` is rejected. |
| **Requirement** | R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.default_location` ([L4142](../../requirements/openapi-parts.yaml#L4142)) (`type: integer`, `nullable`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Location text", "default_location": "abc"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 88 · Review · matches: [API-VAL-035](field-validation.md) (88, test data differs), [API-VAL-037](field-validation.md) (88, test data differs), [API-VAL-038](field-validation.md) (83, test data differs), [API-VAL-029](field-validation.md) (78), [API-VAL-032](field-validation.md) (78), +15 more

**Duplicate judgement:** Keep · Wrong type for `default_location`, a field R-VAL-10 names separately; API-VAL-035 and API-VAL-037 cover the `category` and `variant_of` clauses, API-VAL-038 a boolean. · test-case-reviewer, 2026-10-14

### API-VAL-037: Create a part with a non-integer `variant_of` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a non-integer `variant_of` is rejected. |
| **Requirement** | R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.variant_of` (`type: integer`, `nullable`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Variant text", "variant_of": "abc"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 88 · Review · matches: [API-VAL-035](field-validation.md) (88, test data differs), [API-VAL-036](field-validation.md) (88, test data differs), [API-VAL-038](field-validation.md) (83, test data differs), [API-VAL-029](field-validation.md) (78), [API-VAL-032](field-validation.md) (78), +15 more

**Duplicate judgement:** Keep · Wrong type for `variant_of`, a field R-VAL-10 names separately; API-VAL-035 and API-VAL-036 cover the `category` and `default_location` clauses, API-VAL-038 a boolean. · test-case-reviewer, 2026-10-14

### API-VAL-038: Create a part with a non-boolean `virtual` flag is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a non-boolean `virtual` flag is rejected. |
| **Requirement** | R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.virtual` (`type: boolean`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong type, text for a boolean) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Virtual text", "virtual": "maybe"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 83 · Review · matches: [API-VAL-035](field-validation.md) (83, test data differs), [API-VAL-036](field-validation.md) (83, test data differs), [API-VAL-037](field-validation.md) (83, test data differs), [API-VAL-029](field-validation.md) (76), [API-VAL-032](field-validation.md) (76), +15 more

**Duplicate judgement:** Keep · The boolean clause of R-VAL-10 (text for a flag); API-VAL-035 to 037 are the integer-ID clause and API-VAL-029 and 032 numeric fields. · test-case-reviewer, 2026-10-14

### API-VAL-039: Create a part with `category` null is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with `category` null is accepted. |
| **Requirement** | R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.category` ([L4122](../../requirements/openapi-parts.yaml#L4122)) (`nullable: true`). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: null for a nullable integer) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Category null", "category": null}` | `201 Created`. Body is valid against `Part`; `category` is `null`. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** Known finding F-11 (`test-cases/findings.md`): a part with no category has no `category_name` key, so the check against `Part` fails on that key; assert the other fields.

**Duplicate check:** 64 · Review · matches: [API-VAL-013](field-validation.md) (64), [API-VAL-016](field-validation.md) (64), [API-VAL-020](field-validation.md) (64), [API-VAL-014](field-validation.md) (55), [API-VAL-030](field-validation.md) (53), +2 more

**Duplicate judgement:** Keep · `null` for the nullable integer `category` (R-VAL-10), which also changes the response (`category_name` absent, F-11); the matches are `null` on text fields under other rules. · test-case-reviewer, 2026-10-14

### API-VAL-040: Create a part sending the read-only `pk`: the sent value is not used

| Field | Value |
|---|---|
| **Summary** | Create a part sending the read-only `pk`: the sent value is not used. |
| **Requirement** | R-VAL-11. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.pk` ([L4200](../../requirements/openapi-parts.yaml#L4200), `readOnly: true`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: read-only field sent), Error guessing |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> ReadOnly pk", "pk": 999999}` | Not known: depends on open question Q-VAL-02 (whether the request is accepted with the read-only value ignored, or rejected, and the status and body). If a part is created, its `pk` is not `999999`. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 78 · Review · matches: [API-VAL-042](field-validation.md) (78)

**Duplicate judgement:** Keep · Sends the identity key `pk`; API-VAL-042 sends the derived `category_name`, needs a category as starting state and expects a different value check. · test-case-reviewer, 2026-10-14

### API-VAL-041: Update a part sending the read-only `full_name`: the stored value is not changed

| Field | Value |
|---|---|
| **Summary** | Update a part sending the read-only `full_name`: the stored value is not changed. |
| **Requirement** | R-VAL-11. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([L2767](../../requirements/openapi-parts.yaml#L2767)), `components.schemas.Part.full_name` ([L4152](../../requirements/openapi-parts.yaml#L4152), `readOnly: true`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: read-only field sent) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> ReadOnly full_name"}` | `201 Created`. Body is valid against `Part`; `full_name` is `QA-<suffix> ReadOnly full_name` (name only, so the default `PART_NAME_FORMAT` gives the name; Q-CRUD-05). |
| 2 | `PATCH /api/part/<pk from step 1>/` as `engineer` | `{"full_name": "QA-<suffix> Forged name"}` | Not known: depends on open question Q-VAL-02 (whether the request is accepted with the read-only field ignored, or rejected, and the status and body). |
| 3 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `full_name` is still `QA-<suffix> ReadOnly full_name` and `name` is unchanged. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

### API-VAL-042: Create a part sending the read-only `category_name`: the sent value is not used

| Field | Value |
|---|---|
| **Summary** | Create a part sending the read-only `category_name`: the sent value is not used. |
| **Requirement** | R-VAL-11. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.category_name` ([L4125](../../requirements/openapi-parts.yaml#L4125), `readOnly: true`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: read-only field sent) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> ReadOnly category_name", "category": "<category pk>", "category_name": "QA-<suffix> Forged category"}` | Not known: depends on open question Q-VAL-02 (whether the request is accepted with the read-only field ignored, or rejected, and the status and body). If a part is created, `category_name` is `QA-<suffix> Category`, not the value sent. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`); then delete the category with `DELETE /api/part/category/<pk>/` and both flags `false`.

**Notes:** None

**Duplicate check:** 78 · Review · matches: [API-VAL-040](field-validation.md) (78)

**Duplicate judgement:** Keep · Sends the derived `category_name` with an existing category (different starting state) and expects it to hold the category's name; API-VAL-040 sends the identity key `pk`. · test-case-reviewer, 2026-10-14

### API-VAL-043: Write-only fields sent on create are not returned

| Field | Value |
|---|---|
| **Summary** | Write-only fields sent on create are not returned. |
| **Requirement** | R-VAL-12. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.duplicate` ([L4343](../../requirements/openapi-parts.yaml#L4343)), `initial_stock` ([L4349](../../requirements/openapi-parts.yaml#L4349)), `copy_category_parameters` ([L4360](../../requirements/openapi-parts.yaml#L4360)), all `writeOnly: true`. |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: write-only fields sent) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Original"}` | `201 Created`. Body is valid against `Part`; `pk` is an integer (the original part). |
| 2 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> WriteOnly", "duplicate": {"original": "<pk from step 1>"}, "initial_stock": {"quantity": "5"}, "copy_category_parameters": false}` | `201 Created`. The body does not contain the keys `duplicate`, `initial_stock` or `copy_category_parameters`. |
| 3 | `GET /api/part/<pk from step 2>/` as `engineer` | None | `200 OK`. The body does not contain the keys `duplicate`, `initial_stock` or `copy_category_parameters`. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** `existing_image` and `initial_supplier` (also write-only, R-VAL-12) are not covered: `existing_image` needs a known image file name and `initial_supplier` needs supplier data (REL).

### API-VAL-044: Create a category without `name` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a category without `name` is rejected. |
| **Requirement** | R-VAL-13. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name` ([L3517](../../requirements/openapi-parts.yaml#L3517)) (in the `required` list, not `readOnly`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: required field missing) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"description": "QA-<suffix> no name"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the category is not created or changed. |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no category was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** Only `name` is input-required for a category (index, Schema issues #4). Step 2 relies on `search` also matching `description`; if it does not, compare `count` of `GET /api/part/category/` before and after.

**Duplicate check:** 88 · Review · matches: [API-VAL-046](field-validation.md) (88, test data differs), [API-VAL-049](field-validation.md) (70), [API-VAL-051](field-validation.md) (70), [API-VAL-054](field-validation.md) (70), [API-VAL-047](field-validation.md) (68), +1 more

**Duplicate judgement:** Keep · Category `name` absent (required clause of R-VAL-13); API-VAL-046 is the maxLength + 1 boundary and API-VAL-047 the empty string, and the rest are other fields (R-VAL-14). · test-case-reviewer, 2026-10-14

### API-VAL-045: Create a category with a 100-character name is accepted

| Field | Value |
|---|---|
| **Summary** | Create a category with a 100-character name is accepted. |
| **Requirement** | R-VAL-13. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name` ([L3517](../../requirements/openapi-parts.yaml#L3517)) (`maxLength: 100`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (name maxLength, on the limit) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> + padding, 100 characters"}` | `201 Created`. Body is valid against `Category`; `name` equals the payload and has 100 characters. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** None

**Duplicate check:** 67 · Review · matches: [API-VAL-053](field-validation.md) (67), [API-VAL-048](field-validation.md) (58), [API-VAL-050](field-validation.md) (58)

**Duplicate judgement:** Keep · On-limit boundary of Category `name` (R-VAL-13); API-VAL-053 is the same 100 limit on `icon` (R-VAL-14), and the others are 250-limit fields. · test-case-reviewer, 2026-10-14

### API-VAL-046: Create a category with a 101-character name is rejected

| Field | Value |
|---|---|
| **Summary** | Create a category with a 101-character name is rejected. |
| **Requirement** | R-VAL-13. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name` ([L3517](../../requirements/openapi-parts.yaml#L3517)) (`maxLength: 100`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (name maxLength + 1) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> + padding, 101 characters"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the category is not created or changed. |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no category was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** None

**Duplicate check:** 88 · Review · matches: [API-VAL-044](field-validation.md) (88, test data differs), [API-VAL-054](field-validation.md) (75), [API-VAL-049](field-validation.md) (70), [API-VAL-051](field-validation.md) (70), [API-VAL-047](field-validation.md) (64), +1 more

**Duplicate judgement:** Keep · maxLength + 1 of Category `name` (R-VAL-13); API-VAL-044 omits the name (required clause) and API-VAL-054 is the same limit on `icon` (R-VAL-14). · test-case-reviewer, 2026-10-14

### API-VAL-047: Create a category with an empty `name`

| Field | Value |
|---|---|
| **Summary** | Create a category with an empty `name`. |
| **Requirement** | R-VAL-13. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name` ([L3517](../../requirements/openapi-parts.yaml#L3517)) (no `minLength` stated). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: empty string), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01, Q-VAL-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "", "description": "QA-<suffix> empty name"}` | Not known: depends on open questions Q-VAL-01, Q-VAL-04 (whether an empty `name` is rejected, and the status and error body). |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix>`, `limit=10` | Not known: depends on open question Q-VAL-04 (`count` is `0` if the request is rejected, `1` if it is accepted). |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** Step 2 relies on `search` also matching `description`.

**Duplicate check:** 68 · Review · matches: [API-VAL-044](field-validation.md) (68), [API-VAL-046](field-validation.md) (64), [API-VAL-005](field-validation.md) (54)

**Duplicate judgement:** Keep · Empty Category `name` (an open outcome, Q-VAL-04); API-VAL-044 and 046 are the absent and over-limit classes, and API-VAL-005 is the Part rule R-VAL-01 on another endpoint. · test-case-reviewer, 2026-10-14

### API-VAL-048: Create a category with a 250-character description is accepted

| Field | Value |
|---|---|
| **Summary** | Create a category with a 250-character description is accepted. |
| **Requirement** | R-VAL-14. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.description` ([L3521](../../requirements/openapi-parts.yaml#L3521)) (`maxLength: 250`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (description maxLength, on the limit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Cat Desc 250", "description": "250 characters"}` | `201 Created`. Body is valid against `Category`; `description` equals the payload and has 250 characters. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** None

**Duplicate check:** 81 · Review · matches: [API-VAL-050](field-validation.md) (81, test data differs), [API-VAL-053](field-validation.md) (72), [API-VAL-045](field-validation.md) (58)

**Duplicate judgement:** Keep · On-limit boundary of Category `description`; API-VAL-050 is the same limit on `default_keywords`, a separately stated clause of R-VAL-14 on a different field. · test-case-reviewer, 2026-10-14

### API-VAL-049: Create a category with a 251-character description is rejected

| Field | Value |
|---|---|
| **Summary** | Create a category with a 251-character description is rejected. |
| **Requirement** | R-VAL-14. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.description` ([L3521](../../requirements/openapi-parts.yaml#L3521)) (`maxLength: 250`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (description maxLength + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Cat Desc 251", "description": "251 characters"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the category is not created or changed. |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no category was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** None

**Duplicate check:** 88 · Review · matches: [API-VAL-051](field-validation.md) (88, test data differs), [API-VAL-054](field-validation.md) (84, test data differs), [API-VAL-044](field-validation.md) (70), [API-VAL-046](field-validation.md) (70), [API-VAL-008](field-validation.md) (50)

**Duplicate judgement:** Keep · maxLength + 1 of Category `description`; API-VAL-051 and API-VAL-054 are the over-limit clauses for `default_keywords` and `icon`, separately stated in R-VAL-14. · test-case-reviewer, 2026-10-14

### API-VAL-050: Create a category with 250-character `default_keywords` is accepted

| Field | Value |
|---|---|
| **Summary** | Create a category with 250-character `default_keywords` is accepted. |
| **Requirement** | R-VAL-14. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.default_keywords` ([L3529](../../requirements/openapi-parts.yaml#L3529)) (`maxLength: 250`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (default_keywords maxLength, on the limit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Cat Keywords 250", "default_keywords": "250 characters"}` | `201 Created`. Body is valid against `Category`; `default_keywords` equals the payload and has 250 characters. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** None

**Duplicate check:** 81 · Review · matches: [API-VAL-048](field-validation.md) (81, test data differs), [API-VAL-053](field-validation.md) (72), [API-VAL-045](field-validation.md) (58)

**Duplicate judgement:** Keep · On-limit boundary of `default_keywords`; API-VAL-048 is the same limit on `description`, a separately stated clause of R-VAL-14 on a different field. · test-case-reviewer, 2026-10-14

### API-VAL-051: Create a category with 251-character `default_keywords` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a category with 251-character `default_keywords` is rejected. |
| **Requirement** | R-VAL-14. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.default_keywords` ([L3529](../../requirements/openapi-parts.yaml#L3529)) (`maxLength: 250`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (default_keywords maxLength + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Cat Keywords 251", "default_keywords": "251 characters"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the category is not created or changed. |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no category was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** None

**Duplicate check:** 88 · Review · matches: [API-VAL-049](field-validation.md) (88, test data differs), [API-VAL-054](field-validation.md) (84, test data differs), [API-VAL-044](field-validation.md) (70), [API-VAL-046](field-validation.md) (70)

**Duplicate judgement:** Keep · maxLength + 1 of `default_keywords`; API-VAL-049 and API-VAL-054 are the over-limit clauses for `description` and `icon`, separately stated in R-VAL-14. · test-case-reviewer, 2026-10-14

### API-VAL-052: Create a category with `default_keywords` null is accepted

| Field | Value |
|---|---|
| **Summary** | Create a category with `default_keywords` null is accepted. |
| **Requirement** | R-VAL-14. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.default_keywords` ([L3529](../../requirements/openapi-parts.yaml#L3529)) (`nullable: true`). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: null for a nullable field) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Cat Keywords null", "default_keywords": null}` | `201 Created`. Body is valid against `Category`; `default_keywords` is `null`. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** None

### API-VAL-053: Create a category with a 100-character `icon` is accepted

| Field | Value |
|---|---|
| **Summary** | Create a category with a 100-character `icon` is accepted. |
| **Requirement** | R-VAL-14. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.icon` ([L3563](../../requirements/openapi-parts.yaml#L3563)) (`maxLength: 100`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (icon maxLength, on the limit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Cat Icon 100", "icon": "100 characters"}` | `201 Created`. Body is valid against `Category`; `icon` equals the payload and has 100 characters. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** The schema does not describe the `icon` value format; the check is the length limit only.

**Duplicate check:** 72 · Review · matches: [API-VAL-048](field-validation.md) (72), [API-VAL-050](field-validation.md) (72), [API-VAL-045](field-validation.md) (67)

**Duplicate judgement:** Keep · On-limit boundary of `icon` (100); API-VAL-048 and 050 are 250-limit fields and API-VAL-045 is Category `name` (R-VAL-13). · test-case-reviewer, 2026-10-14

### API-VAL-054: Create a category with a 101-character `icon` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a category with a 101-character `icon` is rejected. |
| **Requirement** | R-VAL-14. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.icon` ([L3563](../../requirements/openapi-parts.yaml#L3563)) (`maxLength: 100`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (icon maxLength + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Cat Icon 101", "icon": "101 characters"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the category is not created or changed. |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no category was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** None

**Duplicate check:** 84 · Review · matches: [API-VAL-049](field-validation.md) (84, test data differs), [API-VAL-051](field-validation.md) (84, test data differs), [API-VAL-046](field-validation.md) (75), [API-VAL-044](field-validation.md) (70)

**Duplicate judgement:** Keep · maxLength + 1 of `icon` (101); API-VAL-049 and 051 are other R-VAL-14 fields with a 250 limit, API-VAL-046 is Category `name` (R-VAL-13). · test-case-reviewer, 2026-10-14

### API-VAL-055: Update a category sending the read-only `level` and `pathstring`: the stored values are not changed

| Field | Value |
|---|---|
| **Summary** | Update a category sending the read-only `level` and `pathstring`: the stored values are not changed. |
| **Requirement** | R-VAL-15. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/` ([L1370](../../requirements/openapi-parts.yaml#L1370)), `components.schemas.Category.level` ([L3542](../../requirements/openapi-parts.yaml#L3542)), `pathstring` ([L3551](../../requirements/openapi-parts.yaml#L3551)), both `readOnly: true`. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: read-only fields sent) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> RO Category"}` | `201 Created`. Body is valid against `Category`; `pathstring` is `QA-<suffix> RO Category`. Record the returned `level`. |
| 2 | `PATCH /api/part/category/<pk from step 1>/` as `engineer` | `{"level": 5, "pathstring": "QA-<suffix>/Forged"}` | Not known: depends on open question Q-VAL-02 (whether the request is accepted with the read-only fields ignored, or rejected, and the status and body). |
| 3 | `GET /api/part/category/<pk from step 1>/` as `engineer` | None | `200 OK`. `level` equals the value recorded in step 1 and `pathstring` is still `QA-<suffix> RO Category`. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** None

### API-VAL-056: PATCH a part with an empty body changes nothing

| Field | Value |
|---|---|
| **Summary** | PATCH a part with an empty body changes nothing. |
| **Requirement** | R-VAL-16. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([L2767](../../requirements/openapi-parts.yaml#L2767)), `components.schemas.PatchedPart` (no `required` list). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: no fields), Boundary value analysis (minimum payload) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Patch Empty", "description": "QA original"}` | `201 Created`. Body is valid against `Part`. |
| 2 | `PATCH /api/part/<pk from step 1>/` as `engineer` | `{}` | `200 OK`. `name` is `QA-<suffix> Patch Empty` and `description` is `QA original`. |
| 3 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `name` and `description` equal the step 1 values. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 56 · Review · matches: [API-VAL-058](field-validation.md) (56)

**Duplicate judgement:** Keep · Empty PATCH on a Part (`PatchedPart`); API-VAL-058 is the `PatchedCategory` clause of R-VAL-16 on a different endpoint and resource. · test-case-reviewer, 2026-10-14

### API-VAL-057: PATCH a part with a name over 100 characters is rejected

| Field | Value |
|---|---|
| **Summary** | PATCH a part with a name over 100 characters is rejected. |
| **Requirement** | R-VAL-16, R-VAL-01. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([L2767](../../requirements/openapi-parts.yaml#L2767)), `components.schemas.Part.name` ([L4196](../../requirements/openapi-parts.yaml#L4196)) (`maxLength: 100`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Boundary value analysis (name maxLength + 1 on update), Equivalence partitioning (partial update still validates) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Patch Long"}` | `201 Created`. Body is valid against `Part`. |
| 2 | `PATCH /api/part/<pk from step 1>/` as `engineer` | `{"name": "QA-<suffix> + padding, 101 characters"}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 3 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `name` is still `QA-<suffix> Patch Long`. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

### API-VAL-058: PATCH a category with an empty body changes nothing

| Field | Value |
|---|---|
| **Summary** | PATCH a category with an empty body changes nothing. |
| **Requirement** | R-VAL-16. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/` ([L1370](../../requirements/openapi-parts.yaml#L1370)), `components.schemas.PatchedCategory` (no `required` list). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: no fields), Boundary value analysis (minimum payload) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Patch Empty Cat", "description": "QA original"}` | `201 Created`. Body is valid against `Category`. |
| 2 | `PATCH /api/part/category/<pk from step 1>/` as `engineer` | `{}` | `200 OK`. `name` is `QA-<suffix> Patch Empty Cat` and `description` is `QA original`. |
| 3 | `GET /api/part/category/<pk from step 1>/` as `engineer` | None | `200 OK`. `name` and `description` equal the step 1 values. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each category the case created.

**Notes:** None

**Duplicate check:** 56 · Review · matches: [API-VAL-056](field-validation.md) (56)

**Duplicate judgement:** Keep · Empty PATCH on a Category (`PatchedCategory`); API-VAL-056 is the `PatchedPart` clause of R-VAL-16 on a different endpoint and resource. · test-case-reviewer, 2026-10-14

### API-VAL-059: Create a part with a form-urlencoded body is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with a form-urlencoded body is accepted. |
| **Requirement** | R-VAL-17. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), request body `application/x-www-form-urlencoded` ([L747](../../requirements/openapi-parts.yaml#L747)). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: second listed content type) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer`, `Content-Type: application/x-www-form-urlencoded` | `name=QA-<suffix> Form&description=QA form body` | `201 Created`. Body is valid against `Part`; `name` and `description` equal the sent values. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 78 · Review · matches: [API-VAL-060](field-validation.md) (78)

**Duplicate judgement:** Keep · `application/x-www-form-urlencoded` body; API-VAL-060 sends `multipart/form-data`, a separately listed content type (a different valid class of R-VAL-17). · test-case-reviewer, 2026-10-14

### API-VAL-060: Create a part with a multipart body is accepted

| Field | Value |
|---|---|
| **Summary** | Create a part with a multipart body is accepted. |
| **Requirement** | R-VAL-17. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), request body `multipart/form-data` ([L747](../../requirements/openapi-parts.yaml#L747)). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: third listed content type) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer`, `Content-Type: multipart/form-data` | Form fields `name` = `QA-<suffix> Multipart`, `description` = `QA multipart body` | `201 Created`. Body is valid against `Part`; `name` and `description` equal the sent values. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 78 · Review · matches: [API-VAL-059](field-validation.md) (78)

**Duplicate judgement:** Keep · `multipart/form-data` body; API-VAL-059 sends `application/x-www-form-urlencoded`, a separately listed content type (a different valid class of R-VAL-17). · test-case-reviewer, 2026-10-14

### API-VAL-061: Create a part with a content type the schema does not list

| Field | Value |
|---|---|
| **Summary** | Create a part with a content type the schema does not list. |
| **Requirement** | R-VAL-17. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), request body content types ([L747](../../requirements/openapi-parts.yaml#L747)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: unlisted content type), Error guessing |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer`, `Content-Type: text/plain` | Body `name=QA-<suffix> Plain` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 57 · Review · matches: [API-VAL-001](field-validation.md) (57), [API-VAL-003](field-validation.md) (57), [API-VAL-008](field-validation.md) (57), [API-VAL-012](field-validation.md) (57), [API-VAL-017](field-validation.md) (57), +15 more

**Duplicate judgement:** Keep · An unlisted content type (R-VAL-17); every match is an invalid field value in a JSON body under a field rule. · test-case-reviewer, 2026-10-14

### API-VAL-062: Create a part with `initial_stock` but no `quantity` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with `initial_stock` but no `quantity` is rejected. |
| **Requirement** | R-VAL-18. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.InitialStock.quantity` ([L3714](../../requirements/openapi-parts.yaml#L3714), in the `required` list). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: required field missing in a nested object) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Stock no qty", "initial_stock": {}}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 83 · Review · matches: [API-VAL-063](field-validation.md) (83, test data differs), [API-VAL-001](field-validation.md) (69), [API-VAL-003](field-validation.md) (69), [API-VAL-004](field-validation.md) (68), [API-VAL-008](field-validation.md) (68), +15 more

**Duplicate judgement:** Keep · `quantity` absent from `initial_stock` (the required clause of R-VAL-18); API-VAL-063 sends a non-numeric quantity, a different invalid class. · test-case-reviewer, 2026-10-14

### API-VAL-063: Create a part with a non-numeric `initial_stock.quantity` is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with a non-numeric `initial_stock.quantity` is rejected. |
| **Requirement** | R-VAL-18. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.InitialStock.quantity` ([L3714](../../requirements/openapi-parts.yaml#L3714), `format: decimal`, pattern `^-?\d{0,10}(?:\.\d{0,5})?$`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong format) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Stock qty text", "initial_stock": {"quantity": "abc"}}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 83 · Review · matches: [API-VAL-062](field-validation.md) (83, test data differs), [API-VAL-032](field-validation.md) (73), [API-VAL-029](field-validation.md) (72), [API-VAL-001](field-validation.md) (70), [API-VAL-035](field-validation.md) (70), +17 more

**Duplicate judgement:** Keep · Non-numeric `initial_stock.quantity` (decimal pattern); API-VAL-062 omits the quantity, and API-VAL-032 and 029 send text to Part fields under other rules. · test-case-reviewer, 2026-10-14

### API-VAL-064: Create a part with an `initial_stock.quantity` of 10 integer digits

| Field | Value |
|---|---|
| **Summary** | Create a part with an `initial_stock.quantity` of 10 integer digits. |
| **Requirement** | R-VAL-18. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.InitialStock.quantity` ([L3714](../../requirements/openapi-parts.yaml#L3714), pattern allows up to 10 integer digits). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (quantity integer digits, on the limit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Stock qty 10 digits", "initial_stock": {"quantity": "9999999999"}}` | Not known: depends on open question Q-VAL-03 (the largest stock quantity the app stores; the schema pattern allows 10 integer digits). If created: `201 Created`, body valid against `Part`, `name` equals the payload. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 64 · Review · matches: [API-VAL-067](field-validation.md) (64), [API-VAL-065](field-validation.md) (56), [API-VAL-066](field-validation.md) (51)

**Duplicate judgement:** Keep · On the 10-integer-digit limit of `quantity`; API-VAL-065 is one digit over it, API-VAL-066 the decimal-places limit and API-VAL-067 a negative value. · test-case-reviewer, 2026-10-14

### API-VAL-065: Create a part with an `initial_stock.quantity` of 11 integer digits is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with an `initial_stock.quantity` of 11 integer digits is rejected. |
| **Requirement** | R-VAL-18. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.InitialStock.quantity` ([L3714](../../requirements/openapi-parts.yaml#L3714), pattern allows up to 10 integer digits). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (quantity integer digits + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Stock qty 11 digits", "initial_stock": {"quantity": "99999999999"}}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 84 · Review · matches: [API-VAL-066](field-validation.md) (84, test data differs), [API-VAL-064](field-validation.md) (56), [API-VAL-063](field-validation.md) (51, test data differs), [API-VAL-067](field-validation.md) (51)

**Duplicate judgement:** Keep · One over the integer-digit limit of `quantity` (11 digits); API-VAL-066 is over the separate decimal-places limit, a different boundary of the pattern. · test-case-reviewer, 2026-10-14

### API-VAL-066: Create a part with an `initial_stock.quantity` of 6 decimal places is rejected

| Field | Value |
|---|---|
| **Summary** | Create a part with an `initial_stock.quantity` of 6 decimal places is rejected. |
| **Requirement** | R-VAL-18. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.InitialStock.quantity` ([L3714](../../requirements/openapi-parts.yaml#L3714), pattern allows up to 5 decimal places). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (quantity decimal places + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Stock qty 6 decimals", "initial_stock": {"quantity": "1.123456"}}` | Not known: depends on open question Q-VAL-01 (status code and error body for a request that fails field validation). Known: the part is not created or changed. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0` and `results` is empty: no part was created. |

**Postconditions and cleanup:** No record is created if the request is rejected; if the API accepts it, the record it creates is cleaned up. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 84 · Review · matches: [API-VAL-065](field-validation.md) (84, test data differs), [API-VAL-063](field-validation.md) (51, test data differs), [API-VAL-064](field-validation.md) (51), [API-VAL-067](field-validation.md) (51)

**Duplicate judgement:** Keep · One over the decimal-places limit of `quantity` (6 places); API-VAL-065 is over the separate integer-digit limit, a different boundary of the pattern. · test-case-reviewer, 2026-10-14

### API-VAL-067: Create a part with a negative `initial_stock.quantity`

| Field | Value |
|---|---|
| **Summary** | Create a part with a negative `initial_stock.quantity`. |
| **Requirement** | R-VAL-18. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.InitialStock.quantity` ([L3714](../../requirements/openapi-parts.yaml#L3714), pattern allows a leading `-`). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (below zero, lower limit not stated) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Stock qty negative", "initial_stock": {"quantity": "-1"}}` | Not known: depends on open question Q-VAL-03 (whether a negative initial quantity is accepted, and the status and body if rejected). The pattern allows a leading `-`, which does not decide it. |

**Postconditions and cleanup:** The records created by the steps. Cleanup as `admin`: for each part the case created, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** None

**Duplicate check:** 64 · Review · matches: [API-VAL-064](field-validation.md) (64), [API-VAL-033](field-validation.md) (62), [API-VAL-065](field-validation.md) (51), [API-VAL-066](field-validation.md) (51)

**Duplicate judgement:** Keep · Negative `initial_stock.quantity` (below zero); API-VAL-064 is the upper digit limit and API-VAL-033 a negative `minimum_stock`, another field and rule (R-VAL-09). · test-case-reviewer, 2026-10-14
