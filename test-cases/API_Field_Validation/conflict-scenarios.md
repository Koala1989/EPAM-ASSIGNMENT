# Conflict scenarios: VAL test cases

### API-VAL-068: Duplicate name, IPN and revision on create is not accepted

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a name, IPN and revision all equal to an existing part is not accepted, and only the first part exists. |
| **Requirement** | R-VAL-01, R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32)). Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name`, `components.schemas.Part.IPN`, `components.schemas.Part.revision`. Index Doc issue 2, Not in schema #2. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: name, IPN and revision all equal), Error guessing (duplicate) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the status code and error body are not known yet. |
| **Review** | Draft · Open question: Q-VAL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Dup Part", "IPN": "QA-<suffix>-IPN-1", "category": <category pk>}` | `201 Created`. Body is valid against `Part`; `name` and `IPN` equal the payload; `revision` is `""`; `pk` is an integer (P1). |
| 2 | `POST /api/part/` as `engineer` | The same payload as step 1. | Proposed, to confirm in Q-VAL-08: the part is not created (the Name is a unique text label, R-Part-13). Open: Q-VAL-08 (status code and error body, and which field carries the error). |
| 3 | `GET /api/part/` as `engineer` | `category=<category pk>`, `limit=50` | `200 OK`. Proposed, to confirm in Q-VAL-08: `count` is `1` and the only result has `pk` P1 (no second part was created). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). One part (P1).

**Notes:** Narrowest reading of "unique": all three values equal, so a rejection is expected under any scope in Doc issue 2. Findings F-04 (the name is not unique on its own).

**Duplicate check:** 52 · Review · matches: [API-VAL-071](conflict-scenarios.md) (52), [API-VAL-072](conflict-scenarios.md) (51)

**Duplicate judgement:** Keep · Exact repeat of name, IPN and revision (expected rejection) vs a letter-case variant (071) and a trailing-space variant (072): different equivalence class and expected outcome · test-case-reviewer, 2026-10-15

### API-VAL-069: Same name with a different IPN on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with the same name as an existing part but a different IPN: whether it is accepted is checked. |
| **Requirement** | R-VAL-01, R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32)). Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name`, `components.schemas.Part.IPN`, `components.schemas.Part.revision`. Index Doc issue 2, Not in schema #2. |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (name equal, IPN differs), Decision table (name equal x IPN differs x revision equal) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; part P1 `QA-<suffix> Dup Part` with IPN `QA-<suffix>-IPN-1` created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: depends on the scope of name uniqueness. |
| **Review** | Draft · Open question: Q-VAL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Dup Part", "IPN": "QA-<suffix>-IPN-2", "category": <category pk>}` | Proposed, to confirm in Q-VAL-08: `201 Created`, body valid against `Part`, `IPN` equals `QA-<suffix>-IPN-2` (name unique together with IPN and revision, not on its own). Open: Q-VAL-08 (if rejected: status code and error body; the docs say the Name is unique, R-Part-13). |
| 2 | `GET /api/part/` as `engineer` | `category=<category pk>`, `limit=50` | Proposed, to confirm in Q-VAL-08: `200 OK`, `count` is `2`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Up to two parts.

**Notes:** Docs (Name is unique) and demo data (findings F-04) disagree. If the app rejects, the architect re-labels the case as Negative.

**Duplicate check:** 58 · Review · matches: [API-VAL-070](conflict-scenarios.md) (58)

**Duplicate judgement:** Keep · Varies the IPN with the revision equal, while API-VAL-070 keeps the IPN and varies the revision: a different decision-table column of the uniqueness scope · test-case-reviewer, 2026-10-15

### API-VAL-070: Same name and IPN with a different revision on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with the same name and IPN as an existing part but a different revision: whether it is accepted is checked. |
| **Requirement** | R-VAL-01, R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32)). Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name`, `components.schemas.Part.IPN`, `components.schemas.Part.revision`. Index Doc issue 2, Not in schema #2. Revision: R-VAL-07 ([openapi-parts.yaml#L4207](../../requirements/openapi-parts.yaml#L4207)). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (name and IPN equal, revision differs), Decision table (revision differs) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revision settings (`PART_ENABLE_REVISION`, `PART_REVISION_ASSEMBLY_ONLY`) = [open: Q-REL-08, names and defaults not rendered in the docs, Doc issue 8]; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; part P1 `QA-<suffix> Dup Part` with IPN `QA-<suffix>-IPN-1` and no revision created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: depends on the scope of name uniqueness and the revision settings. |
| **Review** | Draft · Open question: Q-VAL-08, Q-VAL-06, Q-REL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Dup Part", "IPN": "QA-<suffix>-IPN-1", "revision": "B", "category": <category pk>}` | Proposed, to confirm in Q-VAL-08: `201 Created`, `revision` equals `B` (a revision is a separate part of the same item, part-revision.md#L23). Open: Q-VAL-06 and Q-REL-08 (whether a `revision` is accepted without `revision_of` under the default revision settings); Q-VAL-08 (if rejected: status code and error body). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Up to two parts.

**Notes:** `revision_of` is not sent here; the revision-code rule with `revision_of` is in API-VAL-078 to API-VAL-081.

**Duplicate check:** 58 · Review · matches: [API-VAL-069](conflict-scenarios.md) (58)

**Duplicate judgement:** Keep · Varies the revision with name and IPN equal (and depends on the revision settings), while API-VAL-069 varies the IPN: a different decision-table column · test-case-reviewer, 2026-10-15

### API-VAL-071: Name differing only in letter case on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a name that differs from an existing part only in letter case, with the same IPN and revision: whether it counts as a duplicate is checked. |
| **Requirement** | R-VAL-01, R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32)). Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name`, `components.schemas.Part.IPN`, `components.schemas.Part.revision`. Index Doc issue 2, Not in schema #2. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (case variant of a duplicate), Equivalence partitioning |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; part P1 `QA-<suffix> Dup Part` with IPN `QA-<suffix>-IPN-1` created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: comparison rules not stated. |
| **Review** | Draft · Open question: Q-VAL-08, Q-VAL-10 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> DUP PART", "IPN": "QA-<suffix>-IPN-1", "category": <category pk>}` | Proposed, to confirm in Q-VAL-10: `201 Created` (a value differing only in case is a distinct value). Open: Q-VAL-10 (case sensitivity of the comparison); Q-VAL-08 (if rejected: status code and error body). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Up to two parts.

**Notes:** None

**Duplicate check:** 75 · Review · matches: [API-VAL-072](conflict-scenarios.md) (75), [API-VAL-068](conflict-scenarios.md) (52), [API-VAL-081](conflict-scenarios.md) (50)

**Duplicate judgement:** Keep · Letter-case variant of the name, unlike the trailing-space variant (072), the exact repeat (068) and the revision-code case variant under R-REV-07 (081) · test-case-reviewer, 2026-10-15

### API-VAL-072: Name with a trailing space on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a name equal to an existing part's name plus a trailing space, same IPN and revision: whether it counts as a duplicate is checked. |
| **Requirement** | R-VAL-01, R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32)). Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name`, `components.schemas.Part.IPN`, `components.schemas.Part.revision`. Index Doc issue 2, Not in schema #2. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (whitespace variant of a duplicate) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; part P1 `QA-<suffix> Dup Part` with IPN `QA-<suffix>-IPN-1` created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: trimming rules not stated. |
| **Review** | Draft · Open question: Q-VAL-10 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Dup Part ", "IPN": "QA-<suffix>-IPN-1", "category": <category pk>}` (one trailing space in the name) | Proposed, to confirm in Q-VAL-10: `201 Created` (the trailing space makes a distinct value). Open: Q-VAL-10 (whether text is trimmed before comparison, and the stored `name`); if rejected: status code and error body. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Up to two parts.

**Notes:** The schema has no `minLength` or trimming rule (see Q-VAL-04).

**Duplicate check:** 75 · Review · matches: [API-VAL-071](conflict-scenarios.md) (75), [API-VAL-068](conflict-scenarios.md) (51)

**Duplicate judgement:** Keep · Tests whitespace trimming before comparison, a different equivalence class from the letter-case variant (071) and the exact repeat (068) · test-case-reviewer, 2026-10-15

### API-VAL-073: Rename a part to a duplicate name with PATCH

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` renaming a part to the name of another part with the same IPN and revision is not accepted, and the part keeps its name. |
| **Requirement** | R-VAL-01, R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32)). Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name`, `components.schemas.Part.IPN`, `components.schemas.Part.revision`. Index Doc issue 2, Not in schema #2. Update: R-CRUD-04 (`PATCH /api/part/{id}/`, [L2767](../../requirements/openapi-parts.yaml#L2767)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | State transition (unique to duplicate by update), Error guessing (duplicate) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; part P1 `QA-<suffix> Dup Part` and part P2 `QA-<suffix> Other Part`, both with IPN `QA-<suffix>-IPN-1`, created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the status code and error body are not known yet. |
| **Review** | Draft · Open question: Q-VAL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<P2 pk>/` as `engineer` | `{"name": "QA-<suffix> Dup Part"}` | Proposed, to confirm in Q-VAL-08: the update is not accepted (the Name is a unique text label, R-Part-13). Open: Q-VAL-08 (status code and error body). |
| 2 | `GET /api/part/<P2 pk>/` as `engineer` | None | `200 OK`. Proposed, to confirm in Q-VAL-08: `name` is still `QA-<suffix> Other Part`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Two parts.

**Notes:** None

**Duplicate check:** 50 · Review · matches: [API-VAL-076](conflict-scenarios.md) (50)

**Duplicate judgement:** Keep · Renames to a duplicate name (R-Part-13, Q-VAL-08), while API-VAL-076 changes the IPN under the duplicate-IPN setting (R-VAL-03, Q-VAL-09): different rule, field and setting · test-case-reviewer, 2026-10-15

### API-VAL-074: Duplicate IPN on create with duplicates allowed

| Field | Value |
|---|---|
| **Summary** | With duplicate IPNs allowed, `POST /api/part/` with an IPN already used by another part is accepted. |
| **Requirement** | R-VAL-03 ([openapi-parts.yaml#L4164](../../requirements/openapi-parts.yaml#L4164)); index Not in docs #1 ([part-views.md#L30](../../requirements/docs/part-views.md#L30)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.IPN`. |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Decision table (duplicate IPN allowed on x IPN equal), Equivalence partitioning |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: duplicate IPN allowed [open: Q-VAL-09, setting name and endpoint; findings F-05 reports `PART_ALLOW_DUPLICATE_IPN`], set as `admin`; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; part P1 `QA-<suffix> IPN Part A` with IPN `QA-<suffix>-IPN-1` created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the setting endpoint is outside the schema slice. |
| **Review** | Draft · Open question: Q-VAL-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> IPN Part B", "IPN": "QA-<suffix>-IPN-1", "category": <category pk>}` | Proposed, to confirm in Q-VAL-09: `201 Created`, body valid against `Part`, `IPN` equals `QA-<suffix>-IPN-1`. Open: Q-VAL-09 (the setting that allows duplicates and its default; the docs do not say a duplicate IPN is rejected). |
| 2 | `GET /api/part/` as `engineer` | `IPN=QA-<suffix>-IPN-1`, `limit=50` | Proposed, to confirm in Q-VAL-09: `200 OK`, `count` is `2`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Two parts. Restore the duplicate-IPN setting to its starting value.

**Notes:** Findings F-05: the demo data already shares IPNs. Names differ here so the name rule (Q-VAL-08) is not triggered.

### API-VAL-075: Duplicate IPN on create with duplicates not allowed

| Field | Value |
|---|---|
| **Summary** | With duplicate IPNs not allowed, `POST /api/part/` with an IPN already used by another part is not accepted. |
| **Requirement** | R-VAL-03 ([openapi-parts.yaml#L4164](../../requirements/openapi-parts.yaml#L4164)); index Not in docs #1 ([part-views.md#L30](../../requirements/docs/part-views.md#L30)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.IPN`. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Decision table (duplicate IPN allowed off x IPN equal), Error guessing (duplicate) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: duplicate IPN not allowed [open: Q-VAL-09, setting name and endpoint; findings F-05 reports `PART_ALLOW_DUPLICATE_IPN`], set as `admin`; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; part P1 `QA-<suffix> IPN Part A` with IPN `QA-<suffix>-IPN-1` created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the setting endpoint and error body are not known. |
| **Review** | Draft · Open question: Q-VAL-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> IPN Part B", "IPN": "QA-<suffix>-IPN-1", "category": <category pk>}` | Proposed, to confirm in Q-VAL-09: the part is not created; the error is reported on `IPN`. Open: Q-VAL-09 (status code and error body). |
| 2 | `GET /api/part/` as `engineer` | `IPN=QA-<suffix>-IPN-1`, `limit=50` | `200 OK`. Proposed, to confirm in Q-VAL-09: `count` is `1` and the only result has the `pk` of P1. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). One part. Restore the duplicate-IPN setting to its starting value.

**Notes:** Findings F-05 asks for this second case (setting off).

### API-VAL-076: Change a part's IPN to a duplicate with PATCH, duplicates not allowed

| Field | Value |
|---|---|
| **Summary** | With duplicate IPNs not allowed, `PATCH /api/part/{id}/` setting a part's IPN to one used by another part is not accepted, and the IPN is unchanged. |
| **Requirement** | R-VAL-03 ([openapi-parts.yaml#L4164](../../requirements/openapi-parts.yaml#L4164)), R-CRUD-04. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/`, `components.schemas.PatchedPart.IPN`. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | State transition (unique to duplicate by update), Decision table (setting off) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: duplicate IPN not allowed [open: Q-VAL-09, setting name and endpoint], set as `admin`; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; part P1 `QA-<suffix> IPN Part A` with IPN `QA-<suffix>-IPN-1` and part P2 `QA-<suffix> IPN Part B` with IPN `QA-<suffix>-IPN-2`, created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the setting endpoint and error body are not known. |
| **Review** | Draft · Open question: Q-VAL-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<P2 pk>/` as `engineer` | `{"IPN": "QA-<suffix>-IPN-1"}` | Proposed, to confirm in Q-VAL-09: the update is not accepted. Open: Q-VAL-09 (status code and error body). |
| 2 | `GET /api/part/<P2 pk>/` as `engineer` | None | `200 OK`. Proposed, to confirm in Q-VAL-09: `IPN` is still `QA-<suffix>-IPN-2`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Two parts. Restore the setting.

**Notes:** None

**Duplicate check:** 50 · Review · matches: [API-VAL-073](conflict-scenarios.md) (50)

**Duplicate judgement:** Keep · Changes the IPN with duplicate IPNs not allowed (R-VAL-03, Q-VAL-09), while API-VAL-073 renames to a duplicate name (R-Part-13): different rule, field and setting · test-case-reviewer, 2026-10-15

### API-VAL-077: Two parts with an empty IPN, duplicates not allowed

| Field | Value |
|---|---|
| **Summary** | With duplicate IPNs not allowed, two parts that both have an empty IPN are accepted. |
| **Requirement** | R-VAL-03, R-CRUD-12 (`IPN` defaults to `''`, [openapi-parts.yaml#L4164](../../requirements/openapi-parts.yaml#L4164)); index Not in docs #1. Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.IPN`. |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Boundary value analysis (IPN empty, the minimum), Decision table (setting off x IPN empty) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: duplicate IPN not allowed [open: Q-VAL-09, setting name and endpoint], set as `admin`; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the setting endpoint is outside the schema slice. |
| **Review** | Draft · Open question: Q-VAL-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> No IPN A", "category": <category pk>}` (no `IPN`) | `201 Created`. `IPN` is `""` (R-CRUD-12). |
| 2 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> No IPN B", "category": <category pk>}` (no `IPN`) | Proposed, to confirm in Q-VAL-09: `201 Created`, `IPN` is `""` (empty values are not duplicates of each other). Open: Q-VAL-09 (status code and error body if rejected). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Two parts. Restore the setting.

**Notes:** None

### API-VAL-078: Duplicate revision code under the same original on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a `revision` already used by another revision of the same original part is not accepted. |
| **Requirement** | R-REV-07 ([part-revision.md#L37](../../requirements/docs/part-revision.md#L37)), R-REL-10 (`revision_of`), R-VAL-07 ([openapi-parts.yaml#L4207](../../requirements/openapi-parts.yaml#L4207)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.revision`, `components.schemas.Part.revision_of`. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: revision code equal under the same revision_of), Error guessing (duplicate) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revision settings (`PART_ENABLE_REVISION`, `PART_REVISION_ASSEMBLY_ONLY`) = [open: Q-REL-08, names and defaults not rendered in the docs, Doc issue 8]; Data: category `QA-<suffix> Category` created as `admin`; original part P1 `QA-<suffix> Original` (flags needed for revisions [open: Q-REL-08, e.g. whether it must be an assembly]) and revision P2 `QA-<suffix> Original B` with `revision_of` P1 and `revision` `B`, created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the status code and error body are not known yet. |
| **Review** | Draft · Open question: Q-VAL-11, Q-REL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Original B2", "revision_of": <P1 pk>, "revision": "B", "category": <category pk>}` | The part is not created: a part cannot have two revisions with the same revision number (R-REV-07). Open: Q-VAL-11 (status code and error body, and which field carries the error). |
| 2 | `GET /api/part/` as `engineer` | `revision_of=<P1 pk>`, `limit=50` | `200 OK`. `count` is `1`; the only result is P2 (R-REV-07). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Two parts (P1, P2).

**Notes:** The name differs from P2's so the name rule (Q-VAL-08) is not what blocks the request.

**Duplicate check:** 52 · Review · matches: [API-VAL-080](conflict-scenarios.md) (52), [API-VAL-081](conflict-scenarios.md) (51)

**Duplicate judgement:** Keep · Duplicate revision code on create, while API-VAL-080 reaches it by PATCH (different operation and transition) and API-VAL-081 uses a letter-case variant (different class and expected outcome) · test-case-reviewer, 2026-10-15

### API-VAL-079: Same revision code under a different original on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a `revision` equal to one used by a revision of a different original part is checked. |
| **Requirement** | R-REV-07 ([part-revision.md#L37](../../requirements/docs/part-revision.md#L37)), R-REL-10 (`revision_of`), R-VAL-07 ([openapi-parts.yaml#L4207](../../requirements/openapi-parts.yaml#L4207)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.revision`, `components.schemas.Part.revision_of`. |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: same revision code, different revision_of), Decision table (revision equal x revision_of differs) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revision settings (`PART_ENABLE_REVISION`, `PART_REVISION_ASSEMBLY_ONLY`) = [open: Q-REL-08, names and defaults not rendered in the docs, Doc issue 8]; Data: category `QA-<suffix> Category` created as `admin`; original part P1 `QA-<suffix> Original` (flags needed for revisions [open: Q-REL-08, e.g. whether it must be an assembly]) and revision P2 `QA-<suffix> Original B` with `revision_of` P1 and `revision` `B`, created as `engineer`, and a second original part P3 `QA-<suffix> Other Original` (same flags) created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: depends on the revision settings and Q-VAL-11. |
| **Review** | Draft · Open question: Q-VAL-11, Q-REL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Other Original B", "revision_of": <P3 pk>, "revision": "B", "category": <category pk>}` | Proposed, to confirm in Q-VAL-11: `201 Created`, `revision_of` equals the P3 `pk`, `revision` is `B`. Open: Q-REL-08 (whether the settings allow the revision). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Four parts.

**Notes:** Opposite of API-VAL-078: R-REV-07 forbids a repeated code only for revisions "of a given part" (part-revision.md#L37), so the outcome for a different original is proposed, not stated.

### API-VAL-080: Change a revision's code to a sibling's code with PATCH

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` changing a revision's code to one already used by a sibling revision is not accepted, and the code is unchanged. |
| **Requirement** | R-REV-07 ([part-revision.md#L37](../../requirements/docs/part-revision.md#L37)), R-REL-10 (`revision_of`), R-VAL-07 ([openapi-parts.yaml#L4207](../../requirements/openapi-parts.yaml#L4207)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.revision`, `components.schemas.Part.revision_of`. Update: R-CRUD-04. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | State transition (unique to duplicate revision by update), Error guessing (duplicate) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revision settings (`PART_ENABLE_REVISION`, `PART_REVISION_ASSEMBLY_ONLY`) = [open: Q-REL-08, names and defaults not rendered in the docs, Doc issue 8]; Data: category `QA-<suffix> Category` created as `admin`; original part P1 `QA-<suffix> Original` (flags needed for revisions [open: Q-REL-08, e.g. whether it must be an assembly]) and revision P2 `QA-<suffix> Original B` with `revision_of` P1 and `revision` `B`, created as `engineer`, and a second revision P4 `QA-<suffix> Original C` with `revision_of` P1 and `revision` `C`, created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the status code and error body are not known yet. |
| **Review** | Draft · Open question: Q-VAL-11, Q-REL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<P4 pk>/` as `engineer` | `{"revision": "B"}` | The update is not accepted: a part cannot have two revisions with the same revision number (R-REV-07). Open: Q-VAL-11 (status code and error body). |
| 2 | `GET /api/part/<P4 pk>/` as `engineer` | None | `200 OK`. Proposed, to confirm in Q-VAL-11: `revision` is still `C`. |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Three parts (P1, P2, P4).

**Notes:** None

**Duplicate check:** 52 · Review · matches: [API-VAL-078](conflict-scenarios.md) (52)

**Duplicate judgement:** Keep · Reaches the duplicate revision code by PATCH on an existing sibling (unique to duplicate transition, code must stay unchanged), while API-VAL-078 does it on create · test-case-reviewer, 2026-10-15

### API-VAL-081: Revision code differing only in letter case on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a `revision` that differs from a sibling revision's code only in letter case: whether it counts as a duplicate is checked. |
| **Requirement** | R-REV-07 ([part-revision.md#L37](../../requirements/docs/part-revision.md#L37)), R-REL-10 (`revision_of`), R-VAL-07 ([openapi-parts.yaml#L4207](../../requirements/openapi-parts.yaml#L4207)). Schema: `requirements/openapi-parts.yaml POST /api/part/`, `components.schemas.Part.revision`, `components.schemas.Part.revision_of`. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (case variant of a duplicate), Equivalence partitioning |
| **Priority** | P3 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revision settings (`PART_ENABLE_REVISION`, `PART_REVISION_ASSEMBLY_ONLY`) = [open: Q-REL-08, names and defaults not rendered in the docs, Doc issue 8]; Data: category `QA-<suffix> Category` created as `admin`; original part P1 `QA-<suffix> Original` (flags needed for revisions [open: Q-REL-08, e.g. whether it must be an assembly]) and revision P2 `QA-<suffix> Original B` with `revision_of` P1 and `revision` `B`, created as `engineer`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: case sensitivity not stated. |
| **Review** | Draft · Open question: Q-VAL-10, Q-VAL-11, Q-REL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Original b", "revision_of": <P1 pk>, "revision": "b", "category": <category pk>}` | Proposed, to confirm in Q-VAL-10: `201 Created` (`b` is distinct from `B`). Open: Q-VAL-10 (case sensitivity of the comparison; the R-REV-07 note says it is not stated); Q-VAL-11 (if rejected: status code and error body). |

**Postconditions and cleanup:** Cleanup as `admin`: for each part created, `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`); then `DELETE /api/part/category/<category pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`). Up to three parts.

**Notes:** None

**Duplicate check:** 51 · Review · matches: [API-VAL-078](conflict-scenarios.md) (51), [API-VAL-071](conflict-scenarios.md) (50)

**Duplicate judgement:** Keep · Letter-case variant of a revision code (proposed accepted) vs the exact duplicate code (078, rejected by R-REV-07) and the name case variant (071, different field and rule) · test-case-reviewer, 2026-10-15

### API-VAL-082: Duplicate category name under the same parent on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` with a name already used by another category under the same parent is checked. |
| **Requirement** | R-VAL-13 ([openapi-parts.yaml#L3517](../../requirements/openapi-parts.yaml#L3517)), R-REL-06 (`parent`). Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name`, `components.schemas.Category.parent`. Index: uniqueness among sibling categories not stated. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: same name, same parent), Error guessing (duplicate) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `allaccess` (full create, edit and delete); Settings: None; Data: parent category `QA-<suffix> Parent` and child `QA-<suffix> Dup Cat` (`parent` = parent pk) created as `allaccess`; Pre-steps: get `allaccess`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the status code and error body are not known yet. |
| **Review** | Draft · Open question: Q-VAL-12 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `allaccess` | `{"name": "QA-<suffix> Dup Cat", "parent": <parent pk>}` | Proposed, to confirm in Q-VAL-12: the category is not created (sibling categories are unique by name). Open: Q-VAL-12 (status code and error body). |
| 2 | `GET /api/part/category/` as `allaccess` | `parent=<parent pk>`, `limit=50` | `200 OK`. Proposed, to confirm in Q-VAL-12: `count` is `1`. |

**Postconditions and cleanup:** Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": true}` (`204`) for each top-level category created (Q-CRUD-03).

**Notes:** None

**Duplicate check:** 79 · Review · matches: [API-VAL-084](conflict-scenarios.md) (79)

**Duplicate judgement:** Keep · Siblings under a set parent, while API-VAL-084 covers top-level categories (`parent` null): a different starting state and class of the R-REL-06 `parent` value · test-case-reviewer, 2026-10-15

### API-VAL-083: Same category name under a different parent on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` with a name used by a category under a different parent is checked. |
| **Requirement** | R-VAL-13 ([openapi-parts.yaml#L3517](../../requirements/openapi-parts.yaml#L3517)), R-REL-06 (`parent`). Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name`, `components.schemas.Category.parent`. Index: uniqueness among sibling categories not stated. |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: same name, different parent), Decision table (name equal x parent differs) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: parents `QA-<suffix> Parent A` and `QA-<suffix> Parent B`, and child `QA-<suffix> Dup Cat` under Parent A, created as `allaccess`; Pre-steps: get `allaccess`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: depends on the uniqueness scope. |
| **Review** | Draft · Open question: Q-VAL-12 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `allaccess` | `{"name": "QA-<suffix> Dup Cat", "parent": <Parent B pk>}` | Proposed, to confirm in Q-VAL-12: `201 Created`, body valid against `Category`, `parent` equals the Parent B `pk`, `name` equals the payload. Open: Q-VAL-12 (if rejected: status code and error body). |

**Postconditions and cleanup:** Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": true}` (`204`) for each top-level category created (Q-CRUD-03).

**Notes:** Opposite of API-VAL-082; the schema states no uniqueness, so the outcome is proposed.

### API-VAL-084: Duplicate top-level category name on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` with a name already used by another top-level category (`parent` null) is checked. |
| **Requirement** | R-VAL-13 ([openapi-parts.yaml#L3517](../../requirements/openapi-parts.yaml#L3517)), R-REL-06 (`parent`). Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name`, `components.schemas.Category.parent`. Index: uniqueness among sibling categories not stated. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid class: same name, parent null), Error guessing (duplicate) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: top-level category `QA-<suffix> Dup Top` created as `allaccess`; Pre-steps: get `allaccess`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the status code and error body are not known yet. |
| **Review** | Draft · Open question: Q-VAL-12 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `allaccess` | `{"name": "QA-<suffix> Dup Top"}` (no `parent`) | Proposed, to confirm in Q-VAL-12: the category is not created (top-level categories are unique by name). Open: Q-VAL-12 (status code and error body). |
| 2 | `GET /api/part/category/` as `allaccess` | `name=QA-<suffix> Dup Top`, `limit=50` | `200 OK`. Proposed, to confirm in Q-VAL-12: `count` is `1`. |

**Postconditions and cleanup:** Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": true}` (`204`) for each top-level category created (Q-CRUD-03).

**Notes:** None

**Duplicate check:** 79 · Review · matches: [API-VAL-082](conflict-scenarios.md) (79)

**Duplicate judgement:** Keep · Top-level categories (`parent` null), while API-VAL-082 uses siblings under a set parent: a different starting state and class of the `parent` value · test-case-reviewer, 2026-10-15

### API-VAL-085: Rename a category to a sibling's name with PATCH

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` renaming a category to the name of a sibling is checked, and the category keeps its name if refused. |
| **Requirement** | R-VAL-13 ([openapi-parts.yaml#L3517](../../requirements/openapi-parts.yaml#L3517)), R-REL-06 (`parent`). Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name`, `components.schemas.Category.parent`. Index: uniqueness among sibling categories not stated. Update: R-CRUD-09 (`PATCH /api/part/category/{id}/`, [L1370](../../requirements/openapi-parts.yaml#L1370)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | State transition (unique to duplicate by rename), Error guessing (duplicate) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: parent `QA-<suffix> Parent`, children `QA-<suffix> Cat One` and `QA-<suffix> Cat Two` (both `parent` = parent pk), created as `allaccess`; Pre-steps: get `allaccess`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the status code and error body are not known yet. |
| **Review** | Draft · Open question: Q-VAL-12 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/<Cat Two pk>/` as `allaccess` | `{"name": "QA-<suffix> Cat One"}` | Proposed, to confirm in Q-VAL-12: the update is not accepted. Open: Q-VAL-12 (status code and error body). |
| 2 | `GET /api/part/category/<Cat Two pk>/` as `allaccess` | None | `200 OK`. Proposed, to confirm in Q-VAL-12: `name` is still `QA-<suffix> Cat Two`. |

**Postconditions and cleanup:** Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": true}` (`204`) for each top-level category created (Q-CRUD-03).

**Notes:** None

**Duplicate check:** 59 · Review · matches: [API-VAL-086](conflict-scenarios.md) (59)

**Duplicate judgement:** Keep · Creates the conflict by changing `name`, while API-VAL-086 creates it by changing `parent` (a move): a different field and transition · test-case-reviewer, 2026-10-15

### API-VAL-086: Move a category under a parent that holds the same name with PATCH

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` moving a category under a parent that already has a child of the same name is checked. |
| **Requirement** | R-VAL-13 ([openapi-parts.yaml#L3517](../../requirements/openapi-parts.yaml#L3517)), R-REL-06 (`parent`). Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name`, `components.schemas.Category.parent`. Index: uniqueness among sibling categories not stated. Update: R-CRUD-09; moving a category: R-REL-06. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | State transition (move into a name conflict), What-if business scenario (category moved under a parent holding the same name) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `allaccess`; Settings: None; Data: parents `QA-<suffix> Parent A` and `QA-<suffix> Parent B`, child `QA-<suffix> Dup Cat` under each, created as `allaccess`; Pre-steps: get `allaccess`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the status code and error body are not known yet. |
| **Review** | Draft · Open question: Q-VAL-12 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/category/<Parent B's Dup Cat pk>/` as `allaccess` | `{"parent": <Parent A pk>}` | Proposed, to confirm in Q-VAL-12: the move is not accepted (Parent A already has a child of that name). Open: Q-VAL-12 (status code and error body). |
| 2 | `GET /api/part/category/<Parent B's Dup Cat pk>/` as `allaccess` | None | `200 OK`. Proposed, to confirm in Q-VAL-12: `parent` is still the Parent B `pk`. |

**Postconditions and cleanup:** Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": true}` (`204`) for each top-level category created (Q-CRUD-03).

**Notes:** None

**Duplicate check:** 59 · Review · matches: [API-VAL-085](conflict-scenarios.md) (59)

**Duplicate judgement:** Keep · Creates the conflict by moving the category (`parent` change), while API-VAL-085 renames it (`name` change): a different field and transition · test-case-reviewer, 2026-10-15
