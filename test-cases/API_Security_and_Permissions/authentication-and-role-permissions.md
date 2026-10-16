# Authentication and role permissions: SEC test cases

Conventions used in every case below. "Token" means the user's token from `GET /api/user/me/token/` (basic auth), sent as `Authorization: Token <token>`. "Part P" means part `QA-<suffix> Part`, created as `admin` with `POST /api/part/` and `{"name": "QA-<suffix> Part", "description": "Security test part"}`. "Category C" means category `QA-<suffix> Category`, created as `admin` with `POST /api/part/category/`. "Supplier S" means company `QA-<suffix> Supplier`, created as `admin` with `POST /api/company/` (`is_supplier: true`). Cleanup of a part: as `admin`, `PATCH` `{"active": false}`, then `DELETE`.

### API-SEC-001: List parts without credentials is rejected

| Field | Value |
|---|---|
| **Summary** | `GET /api/part/` with no `Authorization` header is rejected and returns no parts. |
| **Requirement** | `R-SEC-01`. Schema: `requirements/openapi-parts.yaml GET /api/part/` ([#L432](../../requirements/openapi-parts.yaml#L432)), security schemes [#L6112](../../requirements/openapi-parts.yaml#L6112). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: no credentials), Negative |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: none (no Authorization header); Settings: None; Data: None; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` with no `Authorization` header | None | The request is rejected and no part data is returned (R-SEC-01: no operation allows anonymous access). Open: Q-SEC-01 (status code and error body). |

**Postconditions and cleanup:** None.

**Notes:** Proposed status `401`, see Q-SEC-01.

### API-SEC-002: Create a part without credentials is rejected

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with no `Authorization` header is rejected and no part is created. |
| **Requirement** | `R-SEC-01`, `R-SEC-04`. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([#L747](../../requirements/openapi-parts.yaml#L747)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: no credentials), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: none (no Authorization header); Settings: None; Data: None; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` with no `Authorization` header | `{"name": "QA-<suffix> Anonymous Part", "description": "Must not be created"}` | The request is rejected and no part is created (R-SEC-01). Open: Q-SEC-01 (status code and error body). |
| 2 | `GET /api/part/` as `admin` | `search=QA-<suffix> Anonymous Part` | `200 OK`. The list contains no part with that name (R-SEC-01). |

**Postconditions and cleanup:** None expected. If step 2 finds a part, clean it up as `admin` and report a finding.

**Notes:** None.

**Duplicate check:** 51 · Review · matches: [API-SEC-020](authentication-and-role-permissions.md) (51)

**Duplicate judgement:** Keep · Differs from API-SEC-020 in the credential class: no credentials at all (authentication, R-SEC-01, Q-SEC-01) vs an authenticated user without roles (authorisation, Q-SEC-02). · test-case-reviewer, 2026-10-15

### API-SEC-003: List categories without credentials is rejected

| Field | Value |
|---|---|
| **Summary** | `GET /api/part/category/` with no `Authorization` header is rejected and returns no categories. |
| **Requirement** | `R-SEC-01`, `R-SEC-07`. Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([#L848](../../requirements/openapi-parts.yaml#L848)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: no credentials), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: none (no Authorization header); Settings: None; Data: None; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` with no `Authorization` header | None | The request is rejected and no category data is returned (R-SEC-01). Open: Q-SEC-01 (status code and error body). |

**Postconditions and cleanup:** None.

**Notes:** None.

### API-SEC-004: List supplier parts without credentials is rejected

| Field | Value |
|---|---|
| **Summary** | `GET /api/company/part/` with no `Authorization` header is rejected and returns no supplier parts. |
| **Requirement** | `R-SEC-01`. Schema: `requirements/openapi-parts.yaml GET /api/company/part/` ([#L16](../../requirements/openapi-parts.yaml#L16)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: no credentials), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: none (no Authorization header); Settings: None; Data: None; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/company/part/` with no `Authorization` header | None | The request is rejected and no supplier part data is returned (R-SEC-01). Open: Q-SEC-01 (status code and error body). |

**Postconditions and cleanup:** None.

**Notes:** None.

### API-SEC-005: Request with an unknown token is rejected

| Field | Value |
|---|---|
| **Summary** | `GET /api/part/<pk>/` with a well-formed but unknown token is rejected and returns no part data. |
| **Requirement** | `R-SEC-01`. Schema: `requirements/openapi-parts.yaml GET /api/part/{id}/` ([#L2673](../../requirements/openapi-parts.yaml#L2673)), `tokenAuth` [#L6228](../../requirements/openapi-parts.yaml#L6228). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: invalid token), Error guessing |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: none (token is invalid); Settings: None; Data: Part P; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/<Part P pk>/` with header `Authorization: Token 0000000000000000000000000000000000000000` | None | The request is rejected and no part data is returned (R-SEC-01). Open: Q-SEC-01 (status code and error body). |

**Postconditions and cleanup:** Part P: cleanup as `admin`.

**Notes:** None.

### API-SEC-006: Valid token sent with the wrong scheme prefix is rejected

| Field | Value |
|---|---|
| **Summary** | A valid token sent as `Authorization: Bearer <token>` instead of `Token <token>` does not authenticate. |
| **Requirement** | `R-SEC-01`. Schema: `tokenAuth` ("Token-based authentication with required prefix "Token"", [#L6228](../../requirements/openapi-parts.yaml#L6228)), `GET /api/part/`. |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Error guessing (wrong prefix) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: None; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth). |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` with header `Authorization: Bearer <reader token>` | None | The token scheme requires the prefix "Token" (schema), so the call is not authenticated as `reader`. Proposed, to confirm in Q-SEC-01: the request is rejected with the same status as a request without credentials. |

**Postconditions and cleanup:** None.

**Notes:** The schema states the required prefix; the outcome for another prefix is not stated (guardrail 1), hence Proposed.

### API-SEC-007: Basic authentication is accepted

| Field | Value |
|---|---|
| **Summary** | A user with view permission can call `GET /api/part/` with HTTP basic auth. |
| **Requirement** | `R-SEC-01`, `R-SEC-03`. Schema: `requirements/openapi-parts.yaml GET /api/part/` ([#L432](../../requirements/openapi-parts.yaml#L432)), `basicAuth` [#L6113](../../requirements/openapi-parts.yaml#L6113). |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: basic auth) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: None; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` with HTTP basic auth (`reader` / `readonly`) | `limit=5` | `200 OK`, authenticated by basic auth (R-SEC-01). Body is a paginated list valid against `PaginatedPartList`. Open: Q-SEC-03 (whether the Build Orders view role is also needed for `reader`). |

**Postconditions and cleanup:** None.

**Notes:** `limit` is sent because a list without it returns a plain array (Schema issue 8).

**Duplicate check:** 66 · Review · matches: [API-SEC-008](authentication-and-role-permissions.md) (66)

**Duplicate judgement:** Keep · Differs from API-SEC-008 in the valid equivalence class of R-SEC-01: HTTP basic auth (`basicAuth`) vs token auth (`tokenAuth`). · test-case-reviewer, 2026-10-15

### API-SEC-008: Token authentication is accepted

| Field | Value |
|---|---|
| **Summary** | A user with view permission can call `GET /api/part/` with `Authorization: Token <token>`. |
| **Requirement** | `R-SEC-01`, `R-SEC-03`. Schema: `requirements/openapi-parts.yaml GET /api/part/` ([#L432](../../requirements/openapi-parts.yaml#L432)), `tokenAuth` [#L6228](../../requirements/openapi-parts.yaml#L6228). |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: token auth) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `reader` (view only); Settings: None; Data: None; Pre-steps: get `reader`'s token with `GET /api/user/me/token/` (basic auth). |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` with the token | `limit=5` | `200 OK`. Body is valid against `PaginatedPartList` (R-SEC-01). Open: Q-SEC-03 (whether the Build Orders view role is also needed for `reader`). |

**Postconditions and cleanup:** None.

**Notes:** None.

**Duplicate check:** 66 · Review · matches: [API-SEC-007](authentication-and-role-permissions.md) (66), [API-SEC-014](authentication-and-role-permissions.md) (51)

**Duplicate judgement:** Keep · Differs from API-SEC-007 in the auth scheme (token vs basic) and from API-SEC-014 in the rule clause (R-SEC-01 token scheme accepted vs R-SEC-03 view permission, where 014 also asserts Part P is listed). · test-case-reviewer, 2026-10-15

### API-SEC-009: Retrieve the current user's token

| Field | Value |
|---|---|
| **Summary** | An authenticated user can retrieve an API token with `GET /api/user/me/token/`, and the token authenticates later calls. |
| **Requirement** | `R-SEC-02`. Schema: `requirements/openapi-parts.yaml GET /api/user/me/token/` ([#L3463](../../requirements/openapi-parts.yaml#L3463)), response `components.schemas.GetAuthToken`. |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: basic auth credentials) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/user/me/token/` as `engineer` with basic auth | None | `200 OK`. Body is valid against `GetAuthToken`: `token` is a non-empty string, `name` is a string, `expiry` is a date (`format: date`) (R-SEC-02). |
| 2 | `GET /api/part/` as `engineer` with `Authorization: Token <token from step 1>` | `limit=1` | `200 OK`: the token authenticates the user (R-SEC-02: "can be used for auth until it expires"). |

**Postconditions and cleanup:** None. The call issues a new token for `engineer`; earlier tokens of that name may be invalidated.

**Notes:** `GetAuthToken.token` and `expiry` are `readOnly`.

### API-SEC-010: Retrieve a token without credentials is rejected

| Field | Value |
|---|---|
| **Summary** | `GET /api/user/me/token/` with no credentials does not return a token. |
| **Requirement** | `R-SEC-02`, `R-SEC-01`. Schema: `requirements/openapi-parts.yaml GET /api/user/me/token/` ([#L3463](../../requirements/openapi-parts.yaml#L3463)): "Return an API token if the user is authenticated". |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: no credentials), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: none (no Authorization header); Settings: None; Data: None; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/user/me/token/` with no `Authorization` header | None | No token is returned: the token is returned only if the user is authenticated (R-SEC-02). Open: Q-SEC-01 (status code and error body). |

**Postconditions and cleanup:** None.

**Notes:** None.

### API-SEC-011: Retrieve a token with a wrong password is rejected

| Field | Value |
|---|---|
| **Summary** | `GET /api/user/me/token/` with basic auth and a wrong password does not return a token. |
| **Requirement** | `R-SEC-02`, `R-SEC-01`. Schema: `requirements/openapi-parts.yaml GET /api/user/me/token/` ([#L3463](../../requirements/openapi-parts.yaml#L3463)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: wrong password), Error guessing |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/user/me/token/` with basic auth `engineer` / `QA-wrong-password` | None | No token is returned: the user is not authenticated (R-SEC-02). Open: Q-SEC-01 (status code and error body). |

**Postconditions and cleanup:** None.

**Notes:** None.

### API-SEC-012: A new token request replaces the earlier token

| Field | Value |
|---|---|
| **Summary** | A second `GET /api/user/me/token/` deletes the matching earlier token, so the first token stops authenticating. |
| **Requirement** | `R-SEC-02`. Schema: `requirements/openapi-parts.yaml GET /api/user/me/token/` ([#L3463](../../requirements/openapi-parts.yaml#L3463)): "If the user already has a matching token, delete it and create a new one". |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | State transition (token issued, then reissued) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: None; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-01, Q-SEC-05 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/user/me/token/` as `reader` with basic auth | `name=QA-<suffix>-token` | `200 OK`. Body is valid against `GetAuthToken`; `name` is `QA-<suffix>-token`. Keep the token as T1. |
| 2 | `GET /api/user/me/token/` as `reader` with basic auth | `name=QA-<suffix>-token` | `200 OK`. Body is valid against `GetAuthToken`; the returned `token` T2 differs from T1 (R-SEC-02: "Existing tokens are never exposed again"). |
| 3 | `GET /api/part/` with `Authorization: Token <T2>` | `limit=1` | `200 OK`: the new token authenticates. |
| 4 | `GET /api/part/` with `Authorization: Token <T1>` | `limit=1` | The matching token was deleted (R-SEC-02), so T1 does not authenticate. Open: Q-SEC-01 (status code and error body). Open: Q-SEC-05 (whether a call without `name` also counts as matching). |

**Postconditions and cleanup:** `reader` holds the token T2 named `QA-<suffix>-token`; no API call to revoke it is in the slice.

**Notes:** `name` is used so that the case does not depend on the unknown default name.

### API-SEC-013: A user with no permissions retrieves a token

| Field | Value |
|---|---|
| **Summary** | `noaccess` (no role permissions) calls `GET /api/user/me/token/` with basic auth. |
| **Requirement** | `R-SEC-02`. Schema: `requirements/openapi-parts.yaml GET /api/user/me/token/` ([#L3463](../../requirements/openapi-parts.yaml#L3463)), scope `g:read` only. |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Decision table (authenticated, no role), What-if business scenario |
| **Priority** | P3 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: None; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/user/me/token/` as `noaccess` with basic auth | None | The operation lists only the scope `g:read`, no `r:*` role scope (schema). Proposed, to confirm in Q-SEC-04: `200 OK` with a body valid against `GetAuthToken`. |
| 2 | `GET /api/part/` with `Authorization: Token <token from step 1>` | `limit=1` | Not executed if step 1 returned no token. Otherwise the token carries the same permissions as `noaccess` (R-SEC-03 applies): see API-SEC-016. |

**Postconditions and cleanup:** None.

**Notes:** Whether a user without roles may obtain a token is not stated.

### API-SEC-014: View-only user lists parts

| Field | Value |
|---|---|
| **Summary** | A user with view permission on Parts can list parts with `GET /api/part/`. |
| **Requirement** | `R-SEC-03`. Schema: `requirements/openapi-parts.yaml GET /api/part/` ([#L432](../../requirements/openapi-parts.yaml#L432)), scopes `r:view:part` and `r:view:build` ([#L738](../../requirements/openapi-parts.yaml#L738)). |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Decision table (view permission granted) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: Part P; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `reader` | `search=QA-<suffix> Part`, `limit=10` | `200 OK`. Body is valid against `PaginatedPartList` and contains Part P (R-SEC-03). Open: Q-SEC-03 (Build Orders role also needed?). |

**Postconditions and cleanup:** Part P: cleanup as `admin`.

**Notes:** None.

**Duplicate check:** 59 · Review · matches: [API-SEC-015](authentication-and-role-permissions.md) (59), [API-SEC-008](authentication-and-role-permissions.md) (51)

**Duplicate judgement:** Keep · Differs from API-SEC-015 in the operation of R-SEC-03 (list `GET /api/part/` vs detail `GET /api/part/{id}/`) and from API-SEC-008 in the rule tested (R-SEC-03 view permission with Part P present vs R-SEC-01 token scheme). · test-case-reviewer, 2026-10-15

### API-SEC-015: View-only user retrieves a part

| Field | Value |
|---|---|
| **Summary** | A user with view permission on Parts can retrieve one part with `GET /api/part/{id}/`. |
| **Requirement** | `R-SEC-03`. Schema: `requirements/openapi-parts.yaml GET /api/part/{id}/` ([#L2673](../../requirements/openapi-parts.yaml#L2673)), response `components.schemas.Part`. |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Decision table (view permission granted) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: Part P; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/<Part P pk>/` as `reader` | None | `200 OK`. Body is valid against `Part`; `name` is `QA-<suffix> Part` (R-SEC-03). Open: Q-SEC-03 (Build Orders role also needed?). |

**Postconditions and cleanup:** Part P: cleanup as `admin`.

**Notes:** None.

**Duplicate check:** 59 · Review · matches: [API-SEC-014](authentication-and-role-permissions.md) (59)

**Duplicate judgement:** Keep · Differs from API-SEC-014 in the operation: detail `GET /api/part/{id}/` (schema line 2673, `Part`) vs list `GET /api/part/` (`PaginatedPartList`); R-SEC-03 names both. · test-case-reviewer, 2026-10-15

### API-SEC-016: User without view permission cannot list parts

| Field | Value |
|---|---|
| **Summary** | `noaccess` calls `GET /api/part/` and gets no part data. |
| **Requirement** | `R-SEC-03`. Schema: `requirements/openapi-parts.yaml GET /api/part/` ([#L432](../../requirements/openapi-parts.yaml#L432)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (view permission missing), Negative |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: Part P; Pre-steps: get `noaccess`'s token (basic auth). |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/` as `noaccess` | `search=QA-<suffix> Part`, `limit=10` | Part P is not returned: viewing parts needs `r:view:part` (R-SEC-03). Open: Q-SEC-02 (status code and error body, or an empty list). |

**Postconditions and cleanup:** Part P: cleanup as `admin`.

**Notes:** None.

**Duplicate check:** 64 · Review · matches: [API-SEC-017](authentication-and-role-permissions.md) (64)

**Duplicate judgement:** Keep · Differs from API-SEC-017 in the operation (list vs detail) and in the expected outcome, since only the list may answer with an empty list instead of an error (Q-SEC-02). · test-case-reviewer, 2026-10-15

### API-SEC-017: User without view permission cannot retrieve a part

| Field | Value |
|---|---|
| **Summary** | `noaccess` calls `GET /api/part/{id}/` for an existing part and gets no part data. |
| **Requirement** | `R-SEC-03`. Schema: `requirements/openapi-parts.yaml GET /api/part/{id}/` ([#L2673](../../requirements/openapi-parts.yaml#L2673)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (view permission missing), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: Part P; Pre-steps: get `noaccess`'s token (basic auth). |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/<Part P pk>/` as `noaccess` | None | No part data is returned: viewing parts needs `r:view:part` (R-SEC-03). Open: Q-SEC-02 (status code and error body). |

**Postconditions and cleanup:** Part P: cleanup as `admin`.

**Notes:** None.

**Duplicate check:** 64 · Review · matches: [API-SEC-016](authentication-and-role-permissions.md) (64)

**Duplicate judgement:** Keep · Differs from API-SEC-016 in the operation: detail `GET /api/part/{id}/` on an existing part vs the list endpoint. · test-case-reviewer, 2026-10-15

### API-SEC-018: User with part management permission creates a part

| Field | Value |
|---|---|
| **Summary** | `engineer` (manage parts) can create a part with `POST /api/part/`. |
| **Requirement** | `R-SEC-04`. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([#L747](../../requirements/openapi-parts.yaml#L747)), response `components.schemas.Part`. |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Decision table (add permission granted) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-03, Q-SEC-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Engineer Part", "description": "Created by engineer"}` | `201 Created`; body valid against `Part`, `name` equals the payload (R-SEC-04). Open: Q-SEC-03 (Build Orders add role also needed?), Q-SEC-04 (whether `engineer` holds the add permission). |

**Postconditions and cleanup:** one new part. Cleanup as `admin`: `PATCH` `active: false`, `DELETE`.

**Notes:** None.

### API-SEC-019: View-only user cannot create a part

| Field | Value |
|---|---|
| **Summary** | `reader` sends `POST /api/part/` and no part is created. |
| **Requirement** | `R-SEC-04`. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([#L747](../../requirements/openapi-parts.yaml#L747)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (add permission missing), Negative |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: None; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `reader` | `{"name": "QA-<suffix> Reader Part", "description": "Must not be created"}` | The part is not created: creating a part needs `r:add:part` (R-SEC-04). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/` as `admin` | `search=QA-<suffix> Reader Part` | `200 OK`. The list contains no part with that name (R-SEC-04). |

**Postconditions and cleanup:** None expected.

**Notes:** None.

**Duplicate check:** 69 · Review · matches: [API-SEC-020](authentication-and-role-permissions.md) (69)

**Duplicate judgement:** Keep · Differs from API-SEC-020 in the user and decision-table column: `reader` holds Parts view but not add vs `noaccess` with no roles. · test-case-reviewer, 2026-10-15

### API-SEC-020: User without permissions cannot create a part

| Field | Value |
|---|---|
| **Summary** | `noaccess` sends `POST /api/part/` and no part is created. |
| **Requirement** | `R-SEC-04`. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([#L747](../../requirements/openapi-parts.yaml#L747)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (no roles), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: None; Pre-steps: get `noaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `noaccess` | `{"name": "QA-<suffix> Noaccess Part", "description": "Must not be created"}` | The part is not created (R-SEC-04). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/` as `admin` | `search=QA-<suffix> Noaccess Part` | `200 OK`. The list contains no part with that name (R-SEC-04). |

**Postconditions and cleanup:** None expected.

**Notes:** None.

**Duplicate check:** 69 · Review · matches: [API-SEC-019](authentication-and-role-permissions.md) (69), [API-SEC-002](authentication-and-role-permissions.md) (51)

**Duplicate judgement:** Keep · Differs from API-SEC-019 in the user column (no roles vs view-only) and from API-SEC-002 in the credential class (authenticated without roles vs unauthenticated). · test-case-reviewer, 2026-10-15

### API-SEC-021: User with part management permission changes a part with PATCH

| Field | Value |
|---|---|
| **Summary** | `engineer` can change a part's description with `PATCH /api/part/{id}/`. |
| **Requirement** | `R-SEC-05`. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([#L2767](../../requirements/openapi-parts.yaml#L2767)), response `components.schemas.Part`. |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Decision table (change permission granted) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `engineer`; Settings: None; Data: Part P; Pre-steps: get `engineer`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-03, Q-SEC-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<Part P pk>/` as `engineer` | `{"description": "QA-<suffix> changed by engineer"}` | `200 OK`; body valid against `Part`; `description` equals the payload (R-SEC-05). Open: Q-SEC-03, Q-SEC-04 (as in API-SEC-018, for the change permission). |

**Postconditions and cleanup:** Part P changed. Cleanup as `admin`.

**Notes:** None.

### API-SEC-022: View-only user cannot change a part with PATCH

| Field | Value |
|---|---|
| **Summary** | `reader` sends `PATCH /api/part/{id}/` and the part is unchanged. |
| **Requirement** | `R-SEC-05`. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([#L2767](../../requirements/openapi-parts.yaml#L2767)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (change permission missing), Negative |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: Part P; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<Part P pk>/` as `reader` | `{"description": "QA-<suffix> changed by reader"}` | The change is not applied: changing a part needs `r:change:part` (R-SEC-05). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/<Part P pk>/` as `admin` | None | `200 OK`. `description` is still `Security test part` (R-SEC-05). |

**Postconditions and cleanup:** Part P: cleanup as `admin`.

**Notes:** None.

**Duplicate check:** 69 · Review · matches: [API-SEC-024](authentication-and-role-permissions.md) (69), [API-SEC-023](authentication-and-role-permissions.md) (59)

**Duplicate judgement:** Keep · Differs from API-SEC-024 in the user column (`reader` view-only vs `noaccess` no roles) and from API-SEC-023 in the operation (`PATCH` vs `PUT`, both named in R-SEC-05). · test-case-reviewer, 2026-10-15

### API-SEC-023: View-only user cannot change a part with PUT

| Field | Value |
|---|---|
| **Summary** | `reader` sends `PUT /api/part/{id}/` and the part is unchanged. |
| **Requirement** | `R-SEC-05`. Schema: `requirements/openapi-parts.yaml PUT /api/part/{id}/` ([#L2730](../../requirements/openapi-parts.yaml#L2730)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (change permission missing), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: Part P; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PUT /api/part/<Part P pk>/` as `reader` | `{"name": "QA-<suffix> Part", "description": "QA-<suffix> put by reader"}` | The change is not applied (R-SEC-05). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/<Part P pk>/` as `admin` | None | `200 OK`. `description` is still `Security test part` (R-SEC-05). |

**Postconditions and cleanup:** Part P: cleanup as `admin`.

**Notes:** None.

**Duplicate check:** 59 · Review · matches: [API-SEC-022](authentication-and-role-permissions.md) (59)

**Duplicate judgement:** Keep · Differs from API-SEC-022 in the operation: `PUT /api/part/{id}/` (schema line 2730) vs `PATCH` (line 2767), both named in R-SEC-05. · test-case-reviewer, 2026-10-15

### API-SEC-024: User without permissions cannot change a part

| Field | Value |
|---|---|
| **Summary** | `noaccess` sends `PATCH /api/part/{id}/` and the part is unchanged. |
| **Requirement** | `R-SEC-05`. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([#L2767](../../requirements/openapi-parts.yaml#L2767)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (no roles), Negative |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: Part P; Pre-steps: get `noaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<Part P pk>/` as `noaccess` | `{"description": "QA-<suffix> changed by noaccess"}` | The change is not applied (R-SEC-05). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/<Part P pk>/` as `admin` | None | `200 OK`. `description` is still `Security test part` (R-SEC-05). |

**Postconditions and cleanup:** Part P: cleanup as `admin`.

**Notes:** None.

**Duplicate check:** 69 · Review · matches: [API-SEC-022](authentication-and-role-permissions.md) (69)

**Duplicate judgement:** Keep · Differs from API-SEC-022 in the user and decision-table column: `noaccess` (no roles) vs `reader` (view-only). · test-case-reviewer, 2026-10-15

### API-SEC-025: User with delete permission deletes an inactive part

| Field | Value |
|---|---|
| **Summary** | `allaccess` can delete an inactive part with `DELETE /api/part/{id}/`. |
| **Requirement** | `R-SEC-06`. Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/` ([#L2803](../../requirements/openapi-parts.yaml#L2803)). Q-CRUD-02 (answered). |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Decision table (delete permission granted) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: Part P, made inactive as `admin` (`PATCH` `{"active": false}`); Pre-steps: get `allaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<Part P pk>/` as `allaccess` | None | `204 No Content` (R-SEC-06). |
| 2 | `GET /api/part/<Part P pk>/` as `admin` | None | `404 Not Found`, body `{"detail": "No Part matches the given query."}`: the part no longer exists. |

**Postconditions and cleanup:** Part P is deleted; nothing to clean up.

**Notes:** The part is inactive first, per the standing rule on part deletion in the CRUD answers.

### API-SEC-026: View-only user cannot delete a part

| Field | Value |
|---|---|
| **Summary** | `reader` sends `DELETE /api/part/{id}/` for an inactive part and the part still exists. |
| **Requirement** | `R-SEC-06`. Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/` ([#L2803](../../requirements/openapi-parts.yaml#L2803)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (delete permission missing), Negative |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: Part P, made inactive as `admin`; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<Part P pk>/` as `reader` | None | The part is not deleted: deleting a part needs `r:delete:part` (R-SEC-06). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/<Part P pk>/` as `admin` | None | `200 OK`. The part still exists (R-SEC-06). |

**Postconditions and cleanup:** Part P: `DELETE` as `admin`.

**Notes:** None.

**Duplicate check:** 63 · Review · matches: [API-SEC-027](authentication-and-role-permissions.md) (63)

**Duplicate judgement:** Keep · Differs from API-SEC-027 in the user and decision-table column: `reader` (view-only) vs `noaccess` (no roles). · test-case-reviewer, 2026-10-15

### API-SEC-027: User without permissions cannot delete a part

| Field | Value |
|---|---|
| **Summary** | `noaccess` sends `DELETE /api/part/{id}/` for an inactive part and the part still exists. |
| **Requirement** | `R-SEC-06`. Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/` ([#L2803](../../requirements/openapi-parts.yaml#L2803)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (no roles), Negative |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: Part P, made inactive as `admin`; Pre-steps: get `noaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<Part P pk>/` as `noaccess` | None | The part is not deleted (R-SEC-06). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/<Part P pk>/` as `admin` | None | `200 OK`. The part still exists (R-SEC-06). |

**Postconditions and cleanup:** Part P: `DELETE` as `admin`.

**Notes:** None.

**Duplicate check:** 63 · Review · matches: [API-SEC-026](authentication-and-role-permissions.md) (63)

**Duplicate judgement:** Keep · Differs from API-SEC-026 in the user and decision-table column: `noaccess` (no roles) vs `reader` (view-only). · test-case-reviewer, 2026-10-15

### API-SEC-028: Part management user deletes an inactive part

| Field | Value |
|---|---|
| **Summary** | `engineer` sends `DELETE /api/part/{id}/` for an inactive part; the outcome depends on whether `engineer` holds the delete permission. |
| **Requirement** | `R-SEC-06`. Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/` ([#L2803](../../requirements/openapi-parts.yaml#L2803)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (delete permission of a part-management user), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `engineer`; Settings: None; Data: Part P, made inactive as `admin`; Pre-steps: get `engineer`'s token. |
| **Automation** | Partial: expected outcome unknown until Q-SEC-04 is answered. |
| **Review** | Draft · Open question: Q-SEC-02, Q-SEC-03, Q-SEC-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<Part P pk>/` as `engineer` | None | Not known: depends on open question Q-SEC-04 (whether `engineer` holds `r:delete:part`). If it does not, the part is not deleted (R-SEC-06). Open: Q-SEC-02, Q-SEC-03. |
| 2 | `GET /api/part/<Part P pk>/` as `admin` | None | Not known: depends on step 1 and Q-SEC-04. |

**Postconditions and cleanup:** Part P: `DELETE` as `admin` if it still exists.

**Notes:** None.

### API-SEC-029: View-only user lists categories

| Field | Value |
|---|---|
| **Summary** | `reader` can list categories with `GET /api/part/category/`. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([#L848](../../requirements/openapi-parts.yaml#L848)), response `components.schemas.PaginatedCategoryList`. |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Decision table (view permission granted) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: Category C; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-03, Q-SEC-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `reader` | `search=QA-<suffix> Category`, `limit=10` | `200 OK`. Body is valid against `PaginatedCategoryList` and contains Category C (R-SEC-07). Open: Q-SEC-03 (Build Orders role also needed?), Q-SEC-04 (whether `reader` holds Part Categories view). |

**Postconditions and cleanup:** Category C: `DELETE /api/part/category/<pk>/` as `admin` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None.

### API-SEC-030: User without permissions cannot list categories

| Field | Value |
|---|---|
| **Summary** | `noaccess` calls `GET /api/part/category/` and gets no category data. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml GET /api/part/category/` ([#L848](../../requirements/openapi-parts.yaml#L848)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (view permission missing), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: Category C; Pre-steps: get `noaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/` as `noaccess` | `search=QA-<suffix> Category`, `limit=10` | Category C is not returned: viewing categories needs `r:view:part_category` (R-SEC-07). Open: Q-SEC-02 (status code and error body, or an empty list). |

**Postconditions and cleanup:** Category C: cleanup as in API-SEC-029.

**Notes:** None.

**Duplicate check:** 54 · Review · matches: [API-SEC-031](authentication-and-role-permissions.md) (54)

**Duplicate judgement:** Keep · Differs from API-SEC-031 in the operation (category list vs category detail) and in the possible empty-list outcome (Q-SEC-02). · test-case-reviewer, 2026-10-15

### API-SEC-031: User without permissions cannot retrieve a category

| Field | Value |
|---|---|
| **Summary** | `noaccess` calls `GET /api/part/category/{id}/` for an existing category and gets no data. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml GET /api/part/category/{id}/` ([#L1303](../../requirements/openapi-parts.yaml#L1303)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (view permission missing), Negative |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: Category C; Pre-steps: get `noaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/category/<Category C pk>/` as `noaccess` | None | No category data is returned (R-SEC-07). Open: Q-SEC-02 (status code and error body). |

**Postconditions and cleanup:** Category C: cleanup as in API-SEC-029.

**Notes:** None.

**Duplicate check:** 54 · Review · matches: [API-SEC-030](authentication-and-role-permissions.md) (54)

**Duplicate judgement:** Keep · Differs from API-SEC-030 in the operation: `GET /api/part/category/{id}/` (schema line 1303) vs the list endpoint. · test-case-reviewer, 2026-10-15

### API-SEC-032: User with full access creates a category

| Field | Value |
|---|---|
| **Summary** | `allaccess` can create a category with `POST /api/part/category/`. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([#L947](../../requirements/openapi-parts.yaml#L947)), response `components.schemas.Category`. |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Decision table (add permission granted) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: None; Pre-steps: get `allaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `allaccess` | `{"name": "QA-<suffix> Category"}` | `201 Created`; body valid against `Category`; `name` equals the payload (R-SEC-07). |

**Postconditions and cleanup:** one new category. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** None.

### API-SEC-033: View-only user cannot create a category

| Field | Value |
|---|---|
| **Summary** | `reader` sends `POST /api/part/category/` and no category is created. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([#L947](../../requirements/openapi-parts.yaml#L947)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (add permission missing), Negative |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: None; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `reader` | `{"name": "QA-<suffix> Reader Category"}` | The category is not created: creating needs `r:add:part_category` (R-SEC-07). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/category/` as `admin` | `search=QA-<suffix> Reader Category` | `200 OK`. The list contains no category with that name (R-SEC-07). |

**Postconditions and cleanup:** None expected.

**Notes:** None.

**Duplicate check:** 68 · Review · matches: [API-SEC-036](authentication-and-role-permissions.md) (68)

**Duplicate judgement:** Keep · Differs from API-SEC-036 in the user and decision-table column: `reader` (view-only) vs `noaccess` (no roles). · test-case-reviewer, 2026-10-15

### API-SEC-034: User with full access changes a category

| Field | Value |
|---|---|
| **Summary** | `allaccess` can change a category's description with `PATCH /api/part/category/{id}/`. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/` ([#L1370](../../requirements/openapi-parts.yaml#L1370)), response `components.schemas.Category`. |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Decision table (change permission granted) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: Category C; Pre-steps: get `allaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/<Category C pk>/` as `allaccess` | `{"description": "QA-<suffix> changed by allaccess"}` | `200 OK`; body valid against `Category`; `description` equals the payload (R-SEC-07). |

**Postconditions and cleanup:** Category C changed. Cleanup as in API-SEC-029.

**Notes:** None.

### API-SEC-035: View-only user cannot change a category

| Field | Value |
|---|---|
| **Summary** | `reader` sends `PATCH /api/part/category/{id}/` and the category is unchanged. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/` ([#L1370](../../requirements/openapi-parts.yaml#L1370)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (change permission missing), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: Category C (description empty); Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/<Category C pk>/` as `reader` | `{"description": "QA-<suffix> changed by reader"}` | The change is not applied: changing needs `r:change:part_category` (R-SEC-07). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/category/<Category C pk>/` as `admin` | None | `200 OK`. `description` is still empty (R-SEC-07). |

**Postconditions and cleanup:** Category C: cleanup as in API-SEC-029.

**Notes:** None.

### API-SEC-036: User without permissions cannot create a category

| Field | Value |
|---|---|
| **Summary** | `noaccess` sends `POST /api/part/category/` and no category is created. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([#L947](../../requirements/openapi-parts.yaml#L947)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (no roles), Negative |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: None; Pre-steps: get `noaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `noaccess` | `{"name": "QA-<suffix> Noaccess Category"}` | The category is not created (R-SEC-07). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/category/` as `admin` | `search=QA-<suffix> Noaccess Category` | `200 OK`. The list contains no category with that name (R-SEC-07). |

**Postconditions and cleanup:** None expected.

**Notes:** None.

**Duplicate check:** 68 · Review · matches: [API-SEC-033](authentication-and-role-permissions.md) (68)

**Duplicate judgement:** Keep · Differs from API-SEC-033 in the user and decision-table column: `noaccess` (no roles) vs `reader` (view-only). · test-case-reviewer, 2026-10-15

### API-SEC-037: User with full access deletes a category

| Field | Value |
|---|---|
| **Summary** | `allaccess` can delete an empty category with `DELETE /api/part/category/{id}/`. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml DELETE /api/part/category/{id}/` ([#L1406](../../requirements/openapi-parts.yaml#L1406)). Standing rule: both delete flags in the body. |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Decision table (delete permission granted) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: Category C (empty); Pre-steps: get `allaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/category/<Category C pk>/` as `allaccess` | `{"delete_parts": false, "delete_child_categories": false}` | `204 No Content` (R-SEC-07). Open: Q-SEC-03 (the schema lists `r:delete:build`, not only `r:delete:part_category`). |
| 2 | `GET /api/part/category/<Category C pk>/` as `admin` | None | `404 Not Found`, body `{"detail": "No PartCategory matches the given query."}`. |

**Postconditions and cleanup:** Category C is deleted.

**Notes:** The `404` body text is the 1.5.6 pattern `No <Model> matches the given query.`.

### API-SEC-038: View-only user cannot delete a category

| Field | Value |
|---|---|
| **Summary** | `reader` sends `DELETE /api/part/category/{id}/` and the category still exists. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml DELETE /api/part/category/{id}/` ([#L1406](../../requirements/openapi-parts.yaml#L1406)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (delete permission missing), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: Category C; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/category/<Category C pk>/` as `reader` | `{"delete_parts": false, "delete_child_categories": false}` | The category is not deleted: deleting needs `r:delete:part_category` (R-SEC-07). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/category/<Category C pk>/` as `admin` | None | `200 OK`. The category still exists (R-SEC-07). |

**Postconditions and cleanup:** Category C: cleanup as in API-SEC-029.

**Notes:** Both delete flags are sent so that a `400` for a missing body cannot hide the permission check.

**Duplicate check:** 72 · Review · matches: [API-SEC-039](authentication-and-role-permissions.md) (72)

**Duplicate judgement:** Keep · Differs from API-SEC-039 in the user and decision-table column: `reader` (view-only) vs `noaccess` (no roles). · test-case-reviewer, 2026-10-15

### API-SEC-039: User without permissions cannot delete a category

| Field | Value |
|---|---|
| **Summary** | `noaccess` sends `DELETE /api/part/category/{id}/` and the category still exists. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml DELETE /api/part/category/{id}/` ([#L1406](../../requirements/openapi-parts.yaml#L1406)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (no roles), Negative |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: Category C; Pre-steps: get `noaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/category/<Category C pk>/` as `noaccess` | `{"delete_parts": false, "delete_child_categories": false}` | The category is not deleted (R-SEC-07). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/part/category/<Category C pk>/` as `admin` | None | `200 OK`. The category still exists (R-SEC-07). |

**Postconditions and cleanup:** Category C: cleanup as in API-SEC-029.

**Notes:** None.

**Duplicate check:** 72 · Review · matches: [API-SEC-038](authentication-and-role-permissions.md) (72)

**Duplicate judgement:** Keep · Differs from API-SEC-038 in the user and decision-table column: `noaccess` (no roles) vs `reader` (view-only). · test-case-reviewer, 2026-10-15

### API-SEC-040: Part management user creates a category

| Field | Value |
|---|---|
| **Summary** | `engineer` sends `POST /api/part/category/`; the outcome depends on `engineer`'s Part Categories role. |
| **Requirement** | `R-SEC-07`. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([#L947](../../requirements/openapi-parts.yaml#L947)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (Parts role without a stated Part Categories role), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `engineer`; Settings: None; Data: None; Pre-steps: get `engineer`'s token. |
| **Automation** | Partial: expected outcome unknown until Q-SEC-04 is answered. |
| **Review** | Draft · Open question: Q-SEC-02, Q-SEC-03, Q-SEC-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Engineer Category"}` | Not known: depends on open question Q-SEC-04 (whether `engineer` holds `r:add:part_category`). If it does not, the category is not created (R-SEC-07). Open: Q-SEC-02, Q-SEC-03. |

**Postconditions and cleanup:** if a category was created, delete it as `admin` with both delete flags `false`.

**Notes:** Parts and Part Categories are separate roles (R-SEC-09).

### API-SEC-041: User with full access creates a supplier part

| Field | Value |
|---|---|
| **Summary** | `allaccess` can create a supplier part with `POST /api/company/part/`. |
| **Requirement** | `R-SEC-08`. Schema: `requirements/openapi-parts.yaml POST /api/company/part/` ([#L185](../../requirements/openapi-parts.yaml#L185)), response `components.schemas.SupplierPart` (required input: `SKU`, `part`, `supplier`). |
| **Area** | SEC |
| **Type** | Positive |
| **Technique** | Decision table (add Parts and add Purchase Orders granted) |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: Part P, Supplier S; Pre-steps: get `allaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `allaccess` | `{"part": <Part P pk>, "supplier": <Supplier S pk>, "SKU": "QA-<suffix>-SKU-1"}` | `201 Created`; body valid against `SupplierPart`; `part`, `supplier` and `SKU` equal the payload (R-SEC-08). |

**Postconditions and cleanup:** one supplier part. Cleanup as `admin`: `DELETE /api/company/part/<pk>/`, then part P (inactive, delete), then Supplier S.

**Notes:** None.

### API-SEC-042: View-only user cannot create a supplier part

| Field | Value |
|---|---|
| **Summary** | `reader` sends `POST /api/company/part/` and no supplier part is created. |
| **Requirement** | `R-SEC-08`. Schema: `requirements/openapi-parts.yaml POST /api/company/part/` ([#L185](../../requirements/openapi-parts.yaml#L185)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (add permissions missing), Negative |
| **Priority** | P1 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: Part P, Supplier S; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `reader` | `{"part": <Part P pk>, "supplier": <Supplier S pk>, "SKU": "QA-<suffix>-SKU-R"}` | The supplier part is not created: it needs `r:add:part` and `r:add:purchase_order` (R-SEC-08). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/company/part/` as `admin` | `search=QA-<suffix>-SKU-R` | `200 OK`. No supplier part with that SKU (R-SEC-08). |

**Postconditions and cleanup:** None expected; clean up Part P and Supplier S.

**Notes:** None.

**Duplicate check:** 68 · Review · matches: [API-SEC-043](authentication-and-role-permissions.md) (68)

**Duplicate judgement:** Keep · Differs from API-SEC-043 in the user and decision-table column: `reader` (Parts view, no add) vs `noaccess` (no roles). · test-case-reviewer, 2026-10-15

### API-SEC-043: User without permissions cannot create a supplier part

| Field | Value |
|---|---|
| **Summary** | `noaccess` sends `POST /api/company/part/` and no supplier part is created. |
| **Requirement** | `R-SEC-08`. Schema: `requirements/openapi-parts.yaml POST /api/company/part/` ([#L185](../../requirements/openapi-parts.yaml#L185)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (no roles), Negative |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: Part P, Supplier S; Pre-steps: get `noaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `noaccess` | `{"part": <Part P pk>, "supplier": <Supplier S pk>, "SKU": "QA-<suffix>-SKU-N"}` | The supplier part is not created (R-SEC-08). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/company/part/` as `admin` | `search=QA-<suffix>-SKU-N` | `200 OK`. No supplier part with that SKU (R-SEC-08). |

**Postconditions and cleanup:** None expected; clean up Part P and Supplier S.

**Notes:** None.

**Duplicate check:** 68 · Review · matches: [API-SEC-042](authentication-and-role-permissions.md) (68)

**Duplicate judgement:** Keep · Differs from API-SEC-042 in the user and decision-table column: `noaccess` (no roles) vs `reader` (Parts view, no add). · test-case-reviewer, 2026-10-15

### API-SEC-044: Part management user creates a supplier part

| Field | Value |
|---|---|
| **Summary** | `engineer` sends `POST /api/company/part/`; the outcome depends on whether `engineer` holds both the Parts and the Purchase Orders add permissions. |
| **Requirement** | `R-SEC-08`. Schema: `requirements/openapi-parts.yaml POST /api/company/part/` ([#L185](../../requirements/openapi-parts.yaml#L185)). Findings F-03 (engineer cannot view the Suppliers tab). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (add Parts granted, add Purchase Orders unknown), What-if business scenario |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `engineer`; Settings: None; Data: Part P, Supplier S; Pre-steps: get `engineer`'s token. |
| **Automation** | Partial: expected outcome unknown until Q-SEC-04 is answered. |
| **Review** | Draft · Open question: Q-SEC-02, Q-SEC-03, Q-SEC-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/company/part/` as `engineer` | `{"part": <Part P pk>, "supplier": <Supplier S pk>, "SKU": "QA-<suffix>-SKU-E"}` | Not known: depends on open question Q-SEC-04 (whether `engineer` holds `r:add:purchase_order`). If it does not, the supplier part is not created (R-SEC-08: both scopes are needed). Open: Q-SEC-02, Q-SEC-03. |

**Postconditions and cleanup:** if created, delete the supplier part as `admin`; clean up Part P and Supplier S.

**Notes:** The UI found `engineer` can create supplier data but not view the Suppliers tab (F-03); the API may behave differently.

### API-SEC-045: User without permissions cannot list supplier parts

| Field | Value |
|---|---|
| **Summary** | `noaccess` calls `GET /api/company/part/` and gets no supplier part data. |
| **Requirement** | `R-SEC-09`. Schema: `requirements/openapi-parts.yaml GET /api/company/part/` ([#L16](../../requirements/openapi-parts.yaml#L16)), scopes `r:view:part` and `r:view:purchase_order` ([#L176](../../requirements/openapi-parts.yaml#L176)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (view permissions missing), Negative |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `noaccess`; Settings: None; Data: None; Pre-steps: get `noaccess`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/company/part/` as `noaccess` | `limit=5` | No supplier part data is returned: the operation needs the Parts view role (`r:view:part`) (R-SEC-09). Open: Q-SEC-02 (status code and error body, or an empty list). |

**Postconditions and cleanup:** None.

**Notes:** The inventory has no rule for supplier part view, change and delete; R-SEC-09 and the schema scopes are used (see Inventory gaps in the report).

### API-SEC-046: View-only user lists supplier parts

| Field | Value |
|---|---|
| **Summary** | `reader` calls `GET /api/company/part/`; the outcome depends on whether `reader` also holds Purchase Orders view. |
| **Requirement** | `R-SEC-09`. Schema: `requirements/openapi-parts.yaml GET /api/company/part/` ([#L16](../../requirements/openapi-parts.yaml#L16)), scopes [#L176](../../requirements/openapi-parts.yaml#L176). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (view Parts granted, view Purchase Orders unknown) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: None; Pre-steps: get `reader`'s token. |
| **Automation** | Partial: expected outcome unknown until Q-SEC-04 is answered. |
| **Review** | Draft · Open question: Q-SEC-02, Q-SEC-04 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/company/part/` as `reader` | `limit=5` | Not known: depends on open question Q-SEC-04 (whether `reader` holds `r:view:purchase_order`). If it does not, no supplier part data is returned (R-SEC-09: both scopes are listed). Open: Q-SEC-02. |

**Postconditions and cleanup:** None.

**Notes:** None.

### API-SEC-047: View-only user cannot change a supplier part

| Field | Value |
|---|---|
| **Summary** | `reader` sends `PATCH /api/company/part/{id}/` and the supplier part is unchanged. |
| **Requirement** | `R-SEC-09`. Schema: `requirements/openapi-parts.yaml PATCH /api/company/part/{id}/` ([#L360](../../requirements/openapi-parts.yaml#L360)), scopes `r:change:part`, `r:change:purchase_order` ([#L394](../../requirements/openapi-parts.yaml#L394)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (change permissions missing), Negative |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: Part P, Supplier S, supplier part `QA-<suffix>-SKU-1` created as `admin` with `POST /api/company/part/`; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/company/part/<supplier part pk>/` as `reader` | `{"note": "QA-<suffix> changed by reader"}` | The change is not applied: changing needs `r:change:part` and `r:change:purchase_order` (R-SEC-09). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/company/part/<supplier part pk>/` as `admin` | None | `200 OK`. `note` is still empty or absent as created (R-SEC-09). |

**Postconditions and cleanup:** Cleanup as `admin`: delete the supplier part, Part P, Supplier S.

**Notes:** None.

### API-SEC-048: View-only user cannot delete a supplier part

| Field | Value |
|---|---|
| **Summary** | `reader` sends `DELETE /api/company/part/{id}/` and the supplier part still exists. |
| **Requirement** | `R-SEC-09`. Schema: `requirements/openapi-parts.yaml DELETE /api/company/part/{id}/` ([#L403](../../requirements/openapi-parts.yaml#L403)), scopes `r:delete:part`, `r:delete:purchase_order` ([#L426](../../requirements/openapi-parts.yaml#L426)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Decision table (delete permissions missing), Negative |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: Part P, Supplier S, supplier part `QA-<suffix>-SKU-1` created as `admin`; Pre-steps: get `reader`'s token. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/company/part/<supplier part pk>/` as `reader` | None | The supplier part is not deleted: deleting needs `r:delete:part` and `r:delete:purchase_order` (R-SEC-09). Open: Q-SEC-02 (status code and error body). |
| 2 | `GET /api/company/part/<supplier part pk>/` as `admin` | None | `200 OK`. The supplier part still exists (R-SEC-09). |

**Postconditions and cleanup:** as API-SEC-047.

**Notes:** None.

### API-SEC-049: Retrieve a supplier part that does not exist without credentials

| Field | Value |
|---|---|
| **Summary** | `GET /api/company/part/{id}/` for a deleted supplier part, with no `Authorization` header, is rejected for the missing credentials rather than answered with `404`. |
| **Requirement** | `R-SEC-01`. Schema: `requirements/openapi-parts.yaml GET /api/company/part/{id}/` ([#L254](../../requirements/openapi-parts.yaml#L254)). |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid classes: no credentials, unknown id), Error guessing (authentication checked before existence) |
| **Priority** | P2 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: none (no Authorization header); Settings: None; Data: part `QA-<suffix> Part` (Purchaseable) and supplier company `QA-<suffix> Supplier`; a supplier part created with `POST /api/company/part/` and deleted with `DELETE /api/company/part/<pk>/` as `admin`, its `pk` kept; Pre-steps: None. |
| **Automation** | Yes: Phase 2 scope. |
| **Review** | Draft · Open question: Q-SEC-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/company/part/<deleted pk>/` with no `Authorization` header | None | The request is rejected and no supplier part data is returned (R-SEC-01: no operation allows anonymous access). Proposed, to confirm in Q-SEC-01: the status is the one for missing credentials (proposed `401 Unauthorized`), not `404 Not Found`. Open: Q-SEC-01 (status code and error body). |

**Postconditions and cleanup:** As `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/`; delete the supplier company.

**Notes:** The authenticated 404 for this operation is API-REL-035 (REL owns `/api/company/part/`); this case only checks that a missing record is not revealed to an anonymous caller.

**Duplicate check:** 52 · Review · matches: [API-SEC-004](authentication-and-role-permissions.md) (52)

### API-SEC-050: Permission check on an invalid body

| Field | Value |
|---|---|
| **Summary** | `reader` sends `POST /api/part/` with an empty body, which is both unauthorised and invalid. |
| **Requirement** | `R-SEC-04`. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([#L747](../../requirements/openapi-parts.yaml#L747)); `components.schemas.Part.name` is required. |
| **Area** | SEC |
| **Type** | Negative |
| **Technique** | Error guessing (invalid and unauthorised together) |
| **Priority** | P3 |
| **Tags** | Regression, Permissions |
| **Prerequisites** | User: `reader`; Settings: None; Data: None; Pre-steps: get `reader`'s token. |
| **Automation** | Partial: precedence unknown until Q-SEC-06 is answered. |
| **Review** | Draft · Open question: Q-SEC-02, Q-SEC-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `reader` | `{}` | No part is created (R-SEC-04). Proposed, to confirm in Q-SEC-06: the permission error is returned, not a field validation error for `name`. Open: Q-SEC-02 (status code and error body). |

**Postconditions and cleanup:** None.

**Notes:** None.
