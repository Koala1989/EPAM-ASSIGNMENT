# Part name validation on create: VAL test cases

### API-VAL-087: Part name is validated on create (absent, null, blank, length boundaries)

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` accepts a `name` of up to 100 characters and does not create a part when `name` is absent, null, over 100 characters, empty or whitespace-only. |
| **Requirement** | R-VAL-01, R-CRUD-01. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name` (`type: string`, `maxLength: 100`, [L4196](../../requirements/openapi-parts.yaml#L4196)), in the `required` list and not `readOnly` ([L4365](../../requirements/openapi-parts.yaml#L4365)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Equivalence partitioning (invalid classes: absent, null, empty, whitespace-only; valid class: name within limit), Boundary value analysis (name maxLength - 1, maxLength, maxLength + 1) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Approved · Open question: Q-VAL-01, Q-VAL-02 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": <row.name>, "description": "QA-<suffix> <row.tag>"}` (the `name` key is left out when the row is *absent*) | `<row.expected status>`. For a `201`, the body is valid against `Part`, `name` equals the payload and `pk` is an integer. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`: a part exists only if step 1 created one. |

**Data sets**

| Row | Class | name | tag | expected status | error | count |
|---|---|---|---|---|---|---|
| `absent` | EP invalid: absent (required, R-VAL-01) | *(key left out)* | `chk01` | `Proposed, to confirm in Q-VAL-01: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `0` |
| `null` | EP invalid: null (not nullable) | `null` | `chk02` | `Proposed, to confirm in Q-VAL-01: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `0` |
| `empty` | EP invalid: empty string | `""` | `chk03` | `Proposed, to confirm in Q-VAL-02: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `Proposed, to confirm in Q-VAL-02: 0` |
| `whitespace only` | EP invalid: whitespace-only | `"   "` (3 spaces) | `chk04` | `Proposed, to confirm in Q-VAL-02: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `Proposed, to confirm in Q-VAL-02: 0` |
| `below limit` | BVA: maxLength - 1 | `QA-<suffix>` + 88 × `x`, 99 characters | `chk05` | `201 Created` | None | `1` |
| `on limit` | BVA: maxLength | `QA-<suffix>` + 89 × `x`, 100 characters | `chk06` | `201 Created` | None | `1` |
| `over limit` | BVA: maxLength + 1 | `QA-<suffix>` + 90 × `x`, 101 characters | `chk07` | `Proposed, to confirm in Q-VAL-01: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `0` |

**Postconditions and cleanup:** up to three parts (`below limit`, `on limit`, and any row the API accepts against the proposal). Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** `QA-<suffix>` is 11 characters (`QA-` and 8 hex). A part accepted with a blank or whitespace name carries only the description tag; find it by the tag. The check in step 2 relies on `search` also matching `description`; if it does not, compare the `count` of `GET /api/part/` with `limit=1` before and after step 1. Whether a minimum length applies is not stated (no `minLength`); it is covered by the `empty` row.

**Duplicate check:** 58 · Review · matches: [API-VAL-088](part-name-validation-on-create.md) (58)

**Duplicate judgement:** Keep · Different classes and outcome from API-VAL-088: invalid inputs (absent, null, empty, whitespace-only, over limit) and the ASCII length boundary expecting no part, versus API-VAL-088's valid character-content classes (special, multi-byte, padded) expecting a created part. · test-case-reviewer, 2026-10-16

### API-VAL-088: Part name with special, non-ASCII and padded text on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` creates a part whose `name` holds special characters, 100 non-ASCII characters, or leading and trailing spaces, and the response returns `name` as stored. |
| **Requirement** | R-VAL-01, R-CRUD-01. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name` ([L4196](../../requirements/openapi-parts.yaml#L4196)). Docs: [part-views.md#Part Details](../../requirements/docs/part-views.md#L32) ("simple (unique) text label"). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Error guessing (special characters, Unicode, leading and trailing whitespace), Boundary value analysis (maxLength counted in characters) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-04, Q-VAL-05 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": <row.name>, "description": "QA-<suffix> <row.tag>"}` | `<row.expected status>`. For a `201`, the body is valid against `Part` and `name` is `<row.returned name>`. |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. Body is valid against `Part`; `name` equals the step 1 response. (Skip when step 1 created no part.) |

**Data sets**

| Row | Class | name | tag | expected status | returned name |
|---|---|---|---|---|---|
| `special characters` | EP valid: special characters | `QA-<suffix> <b>R&D "10k" 'x'/y</b>` | `spc01` | `Proposed, to confirm in Q-VAL-05: 201 Created` | `Proposed, to confirm in Q-VAL-05: equals the payload` |
| `non-ASCII 100` | BVA: maxLength in characters, multi-byte | `QA-<suffix>` + 89 × `Ω`, 100 characters | `spc02` | `Proposed, to confirm in Q-VAL-05: 201 Created` | `Proposed, to confirm in Q-VAL-05: equals the payload` |
| `padded with spaces` | Error guessing: leading and trailing whitespace | `"  QA-<suffix> Padded  "` | `spc03` | `Proposed, to confirm in Q-VAL-04: 201 Created` | `Open: Q-VAL-04 (stored as sent or trimmed)` |

**Postconditions and cleanup:** up to three parts. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the docs list no restricted characters; every expected outcome is therefore proposed, not stated. The leading spaces in the `padded` row sit before `QA-`: search by the description tag.

**Duplicate check:** 58 · Review · matches: [API-VAL-087](part-name-validation-on-create.md) (58)

**Duplicate judgement:** Keep · Tests valid character-content classes (special characters, 100 multi-byte characters, leading and trailing spaces) and how `name` is stored and returned, which API-VAL-087's required, blank and ASCII length rows do not cover; different open questions (Q-VAL-04, Q-VAL-05). · test-case-reviewer, 2026-10-16

### API-VAL-089: Part name of the wrong type is rejected on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a `name` that is a JSON number, boolean, array or object does not create a part with that value as it was sent. |
| **Requirement** | R-VAL-01, R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name` (`type: string`, [L4196](../../requirements/openapi-parts.yaml#L4196)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid classes: number, boolean, array, object) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01, Q-VAL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer`, `Content-Type: application/json` | `{"name": <row.name>, "description": "QA-<suffix> <row.tag>"}` | `<row.expected status>`. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. |

**Data sets**

| Row | Class | name | tag | expected status | error | count |
|---|---|---|---|---|---|---|
| `number` | EP invalid: number | `12345` | `typ01` | `Open: Q-VAL-06 (status code; number may be converted to text)` | `Open: Q-VAL-06 (error body)` | `Open: Q-VAL-06 (0 if rejected, 1 if converted)` |
| `boolean` | EP invalid: boolean | `true` | `typ02` | `Open: Q-VAL-06 (status code; boolean may be converted to text)` | `Open: Q-VAL-06 (error body)` | `Open: Q-VAL-06 (0 if rejected, 1 if converted)` |
| `array` | EP invalid: array | `["QA-<suffix> A"]` | `typ03` | `Proposed, to confirm in Q-VAL-06: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `Proposed, to confirm in Q-VAL-06: 0` |
| `object` | EP invalid: object | `{"a": "QA-<suffix> B"}` | `typ04` | `Proposed, to confirm in Q-VAL-06: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `Proposed, to confirm in Q-VAL-06: 0` |

**Postconditions and cleanup:** normally no record. If a row creates a part, cleanup as `admin`: find it by the description tag with `GET /api/part/?search=QA-<suffix>&limit=50`, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the `number` and `boolean` rows have no proposed outcome: the schema gives the type but not the conversion rule. The part may be created without the `QA-` name prefix if converted; find it by tag.

### API-VAL-090: Part name limit is enforced for form-urlencoded and multipart bodies

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` accepts a 100-character `name` and refuses a 101-character one when the body is sent as `application/x-www-form-urlencoded` or `multipart/form-data`. |
| **Requirement** | R-VAL-01, R-VAL-17. Schema: `requirements/openapi-parts.yaml POST /api/part/` request bodies ([L752](../../requirements/openapi-parts.yaml#L752)), `components.schemas.Part.name` ([L4196](../../requirements/openapi-parts.yaml#L4196)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Equivalence partitioning (content types: form-urlencoded, multipart), Boundary value analysis (name maxLength, maxLength + 1) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer`, `Content-Type: <row.content type>` | Form fields `name=<row.name>`, `description=QA-<suffix> <row.tag>` | `<row.expected status>`. For a `201`, the body is valid against `Part` and `name` equals the sent value. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. |

**Data sets**

| Row | Class | content type | name | tag | expected status | error | count |
|---|---|---|---|---|---|---|---|
| `urlencoded on limit` | BVA: maxLength, form-urlencoded | `application/x-www-form-urlencoded` | `QA-<suffix>` + 89 × `x`, 100 characters | `frm01` | `201 Created` | None | `1` |
| `urlencoded over limit` | BVA: maxLength + 1, form-urlencoded | `application/x-www-form-urlencoded` | `QA-<suffix>` + 90 × `x`, 101 characters | `frm02` | `Proposed, to confirm in Q-VAL-01: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `0` |
| `multipart on limit` | BVA: maxLength, multipart | `multipart/form-data` | `QA-<suffix>` + 89 × `x`, 100 characters | `frm03` | `201 Created` | None | `1` |
| `multipart over limit` | BVA: maxLength + 1, multipart | `multipart/form-data` | `QA-<suffix>` + 90 × `x`, 101 characters | `frm04` | `Proposed, to confirm in Q-VAL-01: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `0` |

**Postconditions and cleanup:** two parts (`urlencoded on limit`, `multipart on limit`). Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the three content types are stated as accepted (R-VAL-17); rejection of any other content type is not stated and is not tested here.

### API-VAL-091: Duplicate part name on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a `name` already used by another part is accepted or refused depending on whether the IPN and the revision also match. |
| **Requirement** | R-VAL-01, R-VAL-03, R-VAL-07, R-Part-13. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name` ([L4196](../../requirements/openapi-parts.yaml#L4196)). Docs: [part-views.md#Part Details](../../requirements/docs/part-views.md#L32) ("The Part name is a simple (unique) text label"), [part-revision.md#L23](../../requirements/docs/part-revision.md#L23). Findings F-04. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Decision table (name, IPN, revision equal or different), Error guessing (duplicate, letter case, trailing space, double submit) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Dup` with IPN `QA-<suffix>-IPN` and no revision, created in step 1 by `admin`; Pre-steps: get `engineer`'s and `admin`'s tokens with `GET /api/user/me/token/` (basic auth). |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01, Q-VAL-03, Q-VAL-04, Q-VAL-07 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin` | `{"name": "QA-<suffix> Dup", "IPN": "QA-<suffix>-IPN", "description": "QA-<suffix> dup base"}` | `201 Created`. Body is valid against `Part`; `name` and `IPN` equal the payload. |
| 2 | `POST /api/part/` as `engineer` | `{"name": <row.name>, "IPN": <row.IPN>, "revision": <row.revision>, "description": "QA-<suffix> <row.tag>"}` (a key shown as *(left out)* is not sent) | `<row.expected status>`. For a `201`, the body is valid against `Part` and `name` equals the payload. For a rejected request, the body is `<row.error>`. |
| 3 | `GET /api/part/` as `engineer` | `search=QA-<suffix> dup`, `limit=10` | `200 OK`. `count` is `<row.count>`: the base part from step 1, plus the step 2 part if one was created. |

**Data sets**

| Row | Class | name | IPN | revision | tag | expected status | error | count |
|---|---|---|---|---|---|---|---|---|
| `exact duplicate` | Decision table: name, IPN, revision all equal | `QA-<suffix> Dup` | `QA-<suffix>-IPN` | *(left out)* | `dup01` | `Proposed, to confirm in Q-VAL-03: 400 Bad Request` | `Open: Q-VAL-03 (error body, key and text)` | `1` |
| `name only, empty IPN` | Decision table: name equal, IPN different (empty) | `QA-<suffix> Dup` | *(left out)* | *(left out)* | `dup02` | `Proposed, to confirm in Q-VAL-03: 201 Created` | None | `Proposed, to confirm in Q-VAL-03: 2` |
| `other IPN` | Decision table: name equal, IPN different | `QA-<suffix> Dup` | `QA-<suffix>-IPN2` | *(left out)* | `dup03` | `Proposed, to confirm in Q-VAL-03: 201 Created` | None | `Proposed, to confirm in Q-VAL-03: 2` |
| `other revision` | Decision table: name and IPN equal, revision different | `QA-<suffix> Dup` | `QA-<suffix>-IPN` | `B` | `dup04` | `Proposed, to confirm in Q-VAL-07: 201 Created` | None | `Proposed, to confirm in Q-VAL-07: 2` |
| `letter case differs` | Error guessing: letter case | `qa-<suffix> dup` | `QA-<suffix>-IPN` | *(left out)* | `dup05` | `Proposed, to confirm in Q-VAL-04: 201 Created` | None | `Proposed, to confirm in Q-VAL-04: 2` |
| `trailing space` | Error guessing: trailing whitespace | `QA-<suffix> Dup ` | `QA-<suffix>-IPN` | *(left out)* | `dup06` | `Proposed, to confirm in Q-VAL-04: 201 Created` | None | `Proposed, to confirm in Q-VAL-04: 2` |

**Postconditions and cleanup:** the base part and any part step 2 created. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the docs call the Name "(unique)" (R-Part-13) but findings F-04 shows the demo data holds parts with one name and different IPN or revision (Doc issue 2); the combined rule is only proposed. `exact duplicate` is the case the docs' wording most directly covers, yet its status and body are not stated. Empty IPN and revision are the schema defaults (R-CRUD-12), so `name only, empty IPN` differs from the base part by IPN only. Duplicate IPN alone is outside this case (findings F-05).
