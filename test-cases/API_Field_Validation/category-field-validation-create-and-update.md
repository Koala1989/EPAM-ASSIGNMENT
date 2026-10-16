# Category field validation on create and update: VAL test cases

### API-VAL-109: Category name is validated on create (absent, null, blank, length boundaries)

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` creates a category for a `name` of 1 to 100 characters, and does not create one when `name` is absent, null, empty, whitespace-only or 101 characters. |
| **Requirement** | R-VAL-13, R-CRUD-06. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name` (`maxLength: 100`, [L3517](../../requirements/openapi-parts.yaml#L3517)) and the `required` list ([L3572](../../requirements/openapi-parts.yaml#L3572)), response `components.schemas.Category`. |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Equivalence partitioning (invalid classes: absent, null, empty, whitespace-only), Boundary value analysis (name maxLength, maxLength + 1) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-18, Q-VAL-19 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": <row.name>, "description": "QA-<suffix> catname"}` (the `name` key is left out when the row's name is *absent*) | `<row.expected status>`. For a `201`, the body is valid against `Category` and `name` equals the sent value. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/category/` as `engineer` | `limit=500` | `200 OK`. The number of results whose `description` is `QA-<suffix> catname` is `<row.count>`: a category exists only if step 1 created one. |

**Data sets**

| Row | Class | name | expected status | error | count |
|---|---|---|---|---|---|
| `absent` | EP invalid: required key missing (R-VAL-13) | *(key left out)* | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `0` |
| `null` | EP invalid: null (not `nullable`) | `null` | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `Proposed, to confirm in Q-VAL-18: 0` |
| `empty` | EP invalid: empty string | `""` | `Proposed, to confirm in Q-VAL-19: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `Proposed, to confirm in Q-VAL-19: 0` |
| `whitespace only` | EP invalid: whitespace-only | `"   "` (3 spaces) | `Proposed, to confirm in Q-VAL-19: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `Proposed, to confirm in Q-VAL-19: 0` |
| `on limit` | BVA: maxLength | `QA-<suffix>` + 89 × `x`, 100 characters | `201 Created` | None | `1` |
| `over limit` | BVA: maxLength + 1 | `QA-<suffix>` + 90 × `x`, 101 characters | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `0` |

**Postconditions and cleanup:** up to one category per row (the `on limit` row for certain). Cleanup as `admin`: `GET /api/part/category/?limit=500`, pick the results whose `description` is `QA-<suffix> catname`; for each, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** the rows without a name leave `name` out of the list search, so step 2 identifies categories by the description marker. `name` is in the `Category` `required` list and not read-only (index, Schema issue 4), so the absent row creates nothing as fact; the status code is proposed (Not in schema #1).

**Duplicate check:** 60 · Review · matches: [API-VAL-110](category-field-validation-create-and-update.md) (60), [API-VAL-112](category-field-validation-create-and-update.md) (55), [API-VAL-111](category-field-validation-create-and-update.md) (51), [API-VAL-117](category-field-validation-create-and-update.md) (51)

**Duplicate judgement:** Keep · Differs from every match: name required and length classes (R-VAL-13) versus the other text fields' limits (API-VAL-110, R-VAL-14), name character content (API-VAL-112), null/empty on optional fields (API-VAL-111) and form-urlencoded/multipart channels (API-VAL-117). · test-case-reviewer, 2026-10-16

### API-VAL-110: Category text field maximum lengths on create (description, default_keywords, icon)

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` accepts `description` and `default_keywords` of 250 characters and `icon` of 100 characters, and does not create a category when the value is one character longer. |
| **Requirement** | R-VAL-14, R-CRUD-06. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.description` (`maxLength: 250`, [L3521](../../requirements/openapi-parts.yaml#L3521)), `Category.default_keywords` (`maxLength: 250`, [L3529](../../requirements/openapi-parts.yaml#L3529)), `Category.icon` (`maxLength: 100`, [L3563](../../requirements/openapi-parts.yaml#L3563)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (maxLength, maxLength + 1 for description, default_keywords, icon) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-18 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "<row.field>": <row.value>}` | `<row.expected status>`. For a `201`, the body is valid against `Category` and `<row.field>` equals the sent value. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`: a category exists only if step 1 created one. |

**Data sets**

| Row | Class | field | value | tag | expected status | error | count |
|---|---|---|---|---|---|---|---|
| `description on limit` | BVA: maxLength | `description` | 250 × `d` | `clen01` | `201 Created` | None | `1` |
| `description over limit` | BVA: maxLength + 1 | `description` | 251 × `d` | `clen02` | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `0` |
| `default_keywords on limit` | BVA: maxLength | `default_keywords` | 250 × `k` | `clen03` | `201 Created` | None | `1` |
| `default_keywords over limit` | BVA: maxLength + 1 | `default_keywords` | 251 × `k` | `clen04` | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `0` |
| `icon on limit` | BVA: maxLength | `icon` | 100 × `i` | `clen05` | `201 Created` | None | `1` |
| `icon over limit` | BVA: maxLength + 1 | `icon` | 101 × `i` | `clen06` | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `0` |

**Postconditions and cleanup:** up to three categories (the `on limit` rows). Cleanup as `admin`: find them with `GET /api/part/category/?search=QA-<suffix>&limit=50`; for each, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** the category name carries the tag, so step 2 finds it by name. The schema documents no error status (index, Not in schema #1). A 100-character `icon` is accepted by length only; whether the app validates icon content is not stated.

**Duplicate check:** 73 · Review · matches: [API-VAL-111](category-field-validation-create-and-update.md) (73), [API-VAL-109](category-field-validation-create-and-update.md) (60), [API-VAL-092](part-field-validation-create-and-update.md) (50)

**Duplicate judgement:** Keep · Differs from every match: maxLength boundaries of description, default_keywords and icon (R-VAL-14) versus null/empty classes (API-VAL-111), the name field (API-VAL-109) and Part fields on a different endpoint (API-VAL-092). · test-case-reviewer, 2026-10-16

### API-VAL-111: Null, empty and whitespace-only values for optional category fields on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` accepts `null` for the nullable fields (`default_keywords`, `icon`, `parent`, `default_location`) and compares it with `null`, empty and whitespace-only values for the non-nullable `description`. |
| **Requirement** | R-VAL-14, R-CRUD-06. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.default_keywords` / `icon` / `parent` / `default_location` (`nullable: true`, [L3525](../../requirements/openapi-parts.yaml#L3525), [L3529](../../requirements/openapi-parts.yaml#L3529), [L3537](../../requirements/openapi-parts.yaml#L3537), [L3563](../../requirements/openapi-parts.yaml#L3563)), `Category.description` (not nullable, [L3521](../../requirements/openapi-parts.yaml#L3521)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Equivalence partitioning (valid class: null on a nullable field; invalid class: null on a non-nullable field), Error guessing (empty and whitespace-only text) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-18, Q-VAL-19 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "<row.field>": <row.value>}` | `<row.expected status>`. For a `201`, the body is valid against `Category`. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. For a `1`, `<row.field>` of the result is `<row.stored>`. |

**Data sets**

| Row | Class | field | value | tag | expected status | error | count | stored |
|---|---|---|---|---|---|---|---|---|
| `default_keywords null` | EP valid: null on nullable | `default_keywords` | `null` | `nul01` | `201 Created` | None | `1` | `Proposed, to confirm in Q-VAL-19: null` |
| `icon null` | EP valid: null on nullable | `icon` | `null` | `nul02` | `201 Created` | None | `1` | `Proposed, to confirm in Q-VAL-19: null` |
| `parent null` | EP valid: null on nullable | `parent` | `null` | `nul03` | `201 Created` | None | `1` | `Proposed, to confirm in Q-VAL-19: null` |
| `default_location null` | EP valid: null on nullable | `default_location` | `null` | `nul04` | `201 Created` | None | `1` | `Proposed, to confirm in Q-VAL-19: null` |
| `description null` | EP invalid: null on non-nullable | `description` | `null` | `nul05` | `Proposed, to confirm in Q-VAL-19: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `Proposed, to confirm in Q-VAL-19: 0` | `None (no category)` |
| `description empty` | EP: empty string | `description` | `""` | `nul06` | `Proposed, to confirm in Q-VAL-19: 201 Created` | None | `Proposed, to confirm in Q-VAL-19: 1` | `Proposed, to confirm in Q-VAL-19: ""` |
| `description whitespace only` | Error guessing: whitespace-only | `description` | `"   "` (3 spaces) | `nul07` | `Proposed, to confirm in Q-VAL-19: 201 Created` | None | `Proposed, to confirm in Q-VAL-19: 1` | `Proposed, to confirm in Q-VAL-19: 3 spaces, as sent` |
| `default_keywords empty` | EP: empty string on nullable | `default_keywords` | `""` | `nul08` | `Proposed, to confirm in Q-VAL-19: 201 Created` | None | `Proposed, to confirm in Q-VAL-19: 1` | `Proposed, to confirm in Q-VAL-19: ""` |

**Postconditions and cleanup:** up to eight categories. Cleanup as `admin`: find them with `GET /api/part/category/?search=QA-<suffix>&limit=50`; for each, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** the four `null` rows on nullable fields are `201` because the schema marks the fields `nullable`; what the response holds for them is proposed. A `parent` of `null` makes a top-level category; hierarchy rules are REL.

**Duplicate check:** 73 · Review · matches: [API-VAL-110](category-field-validation-create-and-update.md) (73), [API-VAL-109](category-field-validation-create-and-update.md) (51)

**Duplicate judgement:** Keep · Different classes from both matches: null, empty and whitespace values on optional fields (nullable vs non-nullable) versus maxLength boundaries (API-VAL-110) and the required name field (API-VAL-109). · test-case-reviewer, 2026-10-16

### API-VAL-112: Category name with special, non-ASCII and padded text on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` with a `name` holding special characters, non-ASCII characters, 100 multi-byte characters or leading and trailing spaces shows what is stored and returned. |
| **Requirement** | R-VAL-13. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name` (`type: string`, `maxLength: 100`, [L3517](../../requirements/openapi-parts.yaml#L3517)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Error guessing (special characters, Unicode, padding), Boundary value analysis (100 multi-byte characters on the maxLength) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-19, Q-VAL-22 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": <row.name>, "description": "QA-<suffix> <row.tag>"}` | `<row.expected status>`. Body is valid against `Category`; `name` is `<row.returned name>`. |
| 2 | `GET /api/part/category/<pk from step 1>/` as `engineer` | None | `200 OK`. `name` equals the step 1 value. |

**Data sets**

| Row | Class | name | tag | expected status | returned name |
|---|---|---|---|---|---|
| `special characters` | Error guessing: markup and quote characters | `QA-<suffix> <&>"'/` | `spc01` | `Proposed, to confirm in Q-VAL-22: 201 Created` | `Proposed, to confirm in Q-VAL-22: as sent` |
| `non-ASCII` | Error guessing: Unicode | `QA-<suffix> Ünïcödé 部品` | `spc02` | `Proposed, to confirm in Q-VAL-22: 201 Created` | `Proposed, to confirm in Q-VAL-22: as sent` |
| `100 multi-byte` | BVA: maxLength counted in characters | `QA-<suffix>` + 89 × `é`, 100 characters | `spc03` | `Proposed, to confirm in Q-VAL-22: 201 Created` | `Proposed, to confirm in Q-VAL-22: as sent` |
| `padded with spaces` | Error guessing: leading and trailing spaces | `"  QA-<suffix> padded  "` | `spc04` | `Proposed, to confirm in Q-VAL-19: 201 Created` | `Proposed, to confirm in Q-VAL-19: as sent, spaces kept` |

**Postconditions and cleanup:** up to four categories. Cleanup as `admin`: find them with `GET /api/part/category/?limit=500`, pick the results whose `description` starts with `QA-<suffix> spc`; for each, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** the docs list no allowed characters for a category name. If the API trims or alters the value, record the actual result as a finding against Q-VAL-19 or Q-VAL-22.

**Duplicate check:** 55 · Review · matches: [API-VAL-109](category-field-validation-create-and-update.md) (55)

**Duplicate judgement:** Keep · Tests name content classes (special characters, Unicode, multi-byte length, padding; Q-VAL-22, Q-VAL-19) whereas API-VAL-109 tests presence and length classes of the same field. · test-case-reviewer, 2026-10-16

### API-VAL-113: Reference and flag fields of the wrong type are refused on category create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` does not create a category when `parent` or `default_location` is text or a decimal, or `structural` is not a boolean. |
| **Requirement** | R-VAL-10 (each field matches its schema type), R-VAL-13. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.parent` / `default_location` (`type: integer`, [L3537](../../requirements/openapi-parts.yaml#L3537), [L3525](../../requirements/openapi-parts.yaml#L3525)), `Category.structural` (`type: boolean`, [L3560](../../requirements/openapi-parts.yaml#L3560)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid classes: text for integer, decimal for integer, text for boolean, array for boolean) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-24 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "<row.field>": <row.value>}` | `<row.expected status>`. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. |

**Data sets**

| Row | Class | field | value | tag | expected status | error | count |
|---|---|---|---|---|---|---|---|
| `parent text` | EP invalid: text for integer | `parent` | `"abc"` | `typ01` | `Proposed, to confirm in Q-VAL-24: 400 Bad Request` | `Open: Q-VAL-24 (error body and text)` | `Proposed, to confirm in Q-VAL-24: 0` |
| `parent decimal` | EP invalid: decimal for integer | `parent` | `1.5` | `typ02` | `Proposed, to confirm in Q-VAL-24: 400 Bad Request` | `Open: Q-VAL-24 (error body and text)` | `Proposed, to confirm in Q-VAL-24: 0` |
| `default_location text` | EP invalid: text for integer | `default_location` | `"abc"` | `typ03` | `Proposed, to confirm in Q-VAL-24: 400 Bad Request` | `Open: Q-VAL-24 (error body and text)` | `Proposed, to confirm in Q-VAL-24: 0` |
| `structural text` | EP invalid: text for boolean | `structural` | `"maybe"` | `typ04` | `Proposed, to confirm in Q-VAL-24: 400 Bad Request` | `Open: Q-VAL-24 (error body and text)` | `Proposed, to confirm in Q-VAL-24: 0` |
| `structural array` | EP invalid: array for boolean | `structural` | `[true]` | `typ05` | `Proposed, to confirm in Q-VAL-24: 400 Bad Request` | `Open: Q-VAL-24 (error body and text)` | `Proposed, to confirm in Q-VAL-24: 0` |

**Postconditions and cleanup:** normally no record. If a row creates a category, cleanup as `admin`: find it with `GET /api/part/category/?search=QA-<suffix>&limit=50`, then `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** a `parent` or `default_location` that is an integer for a record that does not exist is a relationship rule (REL, Q-REL-01), not covered here.

**Duplicate check:** 56 · Review · matches: [API-VAL-098](part-field-validation-create-and-update.md) (56), [API-VAL-116](category-field-validation-create-and-update.md) (52), [API-VAL-114](category-field-validation-create-and-update.md) (50)

**Duplicate judgement:** Keep · Differs from every match: Category endpoint and fields versus Part fields (API-VAL-098), one wrong-type field per request versus several invalid fields reported together (API-VAL-116), and type errors versus read-only fields (API-VAL-114). · test-case-reviewer, 2026-10-16

### API-VAL-114: Values sent for read-only Category fields on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` with a value for a read-only field (`pk`, `level`, `pathstring`, `part_count`, `subcategories`, `starred`) shows whether the request is ignored or rejected and that the client value is not stored. |
| **Requirement** | R-VAL-15, R-CRUD-06. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.pk` / `level` / `pathstring` / `part_count` / `subcategories` (`readOnly: true`, [L3513](../../requirements/openapi-parts.yaml#L3513), [L3534](../../requirements/openapi-parts.yaml#L3534), [L3551](../../requirements/openapi-parts.yaml#L3551), [L3542](../../requirements/openapi-parts.yaml#L3542), [L3547](../../requirements/openapi-parts.yaml#L3547)), `Category.starred` (`readOnly: true`, [L3556](../../requirements/openapi-parts.yaml#L3556)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (read-only field set by the client), Error guessing (client sets server-assigned identity, depth and totals) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-21 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "<row.field>": <row.value>}` | `<row.expected status>`. For a `201`, `<row.field>` in the body is not `<row.value>` (read-only fields are not set by the client, R-VAL-15). Open: Q-VAL-21 (ignored or rejected). |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. For a `1`, the stored `<row.field>` is not `<row.value>`. |

**Data sets**

| Row | Class | field | value | tag | expected status | count |
|---|---|---|---|---|---|---|
| `pk` | EP: read-only identity | `pk` | `2147000000` | `rof01` | `Proposed, to confirm in Q-VAL-21: 201 Created` | `Proposed, to confirm in Q-VAL-21: 1` |
| `level` | EP: read-only depth | `level` | `7` | `rof02` | `Proposed, to confirm in Q-VAL-21: 201 Created` | `Proposed, to confirm in Q-VAL-21: 1` |
| `pathstring` | EP: read-only computed text | `pathstring` | `QA-<suffix> Forced/Path` | `rof03` | `Proposed, to confirm in Q-VAL-21: 201 Created` | `Proposed, to confirm in Q-VAL-21: 1` |
| `part_count` | EP: read-only total | `part_count` | `500` | `rof04` | `Proposed, to confirm in Q-VAL-21: 201 Created` | `Proposed, to confirm in Q-VAL-21: 1` |
| `subcategories` | EP: read-only total | `subcategories` | `500` | `rof05` | `Proposed, to confirm in Q-VAL-21: 201 Created` | `Proposed, to confirm in Q-VAL-21: 1` |
| `starred` | EP: read-only per-user flag | `starred` | `true` | `rof06` | `Proposed, to confirm in Q-VAL-21: 201 Created` | `Proposed, to confirm in Q-VAL-21: 1` |

**Postconditions and cleanup:** up to six categories. Cleanup as `admin`: find them with `GET /api/part/category/?search=QA-<suffix>&limit=50`; for each, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** the schema marks the fields read-only only; "ignored or rejected" is unanswered (index, Not in schema #5). The `pk` value must not belong to an existing category; if the API accepts it against the proposal, record that as a finding. The R-VAL-15 rule lists the fields without stating the client-value behaviour, so the statement that the client value is not stored comes from the `readOnly` marker (the inventory's R-VAL-11 wording for Part fields).

**Duplicate check:** 50 · Review · matches: [API-VAL-113](category-field-validation-create-and-update.md) (50)

**Duplicate judgement:** Keep · Different rule and outcome from API-VAL-113: read-only fields (R-VAL-15, proposed accepted with the client value not stored) versus wrong-type writable fields (R-VAL-10, proposed rejected). · test-case-reviewer, 2026-10-16

### API-VAL-115: Duplicate category name under the same parent on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` with a `name` and `parent` already used by a sibling category shows whether the duplicate is rejected, and compares it with the same name under a different parent. |
| **Requirement** | R-VAL-13 (uniqueness among sibling categories not stated), R-CRUD-06. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name` ([L3517](../../requirements/openapi-parts.yaml#L3517)), `Category.parent` ([L3537](../../requirements/openapi-parts.yaml#L3537)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate), Decision table (same or different name × same or different parent), What-if business scenario (two stores users create the same category) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: parent categories `QA-<suffix> Parent A` and `QA-<suffix> Parent B` and a child `QA-<suffix> Twin` under `QA-<suffix> Parent A`, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-20 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer`, three times | `{"name": "QA-<suffix> Parent A"}`, `{"name": "QA-<suffix> Parent B"}`, then `{"name": "QA-<suffix> Twin", "parent": <pk of Parent A>}` | `201 Created` each. Bodies are valid against `Category`; the `pk` of each is recorded. |
| 2 | `POST /api/part/category/` as `engineer` | `{"name": <row.name>, "parent": <row.parent>}` | `<row.expected status>`. For a rejected request, the body is `<row.error>`. |
| 3 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix> Twin`, `limit=10` | `200 OK`. `count` is `<row.count>`. |

**Data sets**

| Row | Class | name | parent | expected status | error | count |
|---|---|---|---|---|---|---|
| `same name same parent` | Decision table: name equal, parent equal | `QA-<suffix> Twin` | `<pk of Parent A>` | `Proposed, to confirm in Q-VAL-20: 400 Bad Request` | `Open: Q-VAL-20 (error body and text)` | `Proposed, to confirm in Q-VAL-20: 1` |
| `same name other parent` | Decision table: name equal, parent differs | `QA-<suffix> Twin` | `<pk of Parent B>` | `Proposed, to confirm in Q-VAL-20: 201 Created` | None | `Proposed, to confirm in Q-VAL-20: 2` |
| `other case same parent` | Error guessing: letter case differs | `qa-<suffix> twin` | `<pk of Parent A>` | `Open: Q-VAL-20 (whether the check is case-sensitive)` | `Open: Q-VAL-20 (error body and text)` | `Open: Q-VAL-20 (count)` |

**Postconditions and cleanup:** Each row runs on its own with a new `QA-<suffix>`, so no two rows create the same name, and the row's categories are deleted when the row ends. Each row leaves three or four categories. Cleanup as `admin`: find them with `GET /api/part/category/?search=QA-<suffix>&limit=50`; delete the children first, then the parents, each with `DELETE /api/part/category/<pk>/` and `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** the schema and docs state no uniqueness for category names; findings F-04 and F-05 (name + IPN + revision) concern parts. Search is assumed case-insensitive in step 3 only to count the twins; use the `pk` list if it is not.

### API-VAL-116: Several invalid fields in one category create request

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` with an over-long `name`, an over-long `description` and `structural` as text in one body creates no category, and the response shows which fields failed. |
| **Requirement** | R-VAL-13, R-VAL-14, R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name` ([L3517](../../requirements/openapi-parts.yaml#L3517)), `Category.description` ([L3521](../../requirements/openapi-parts.yaml#L3521)), `Category.structural` ([L3560](../../requirements/openapi-parts.yaml#L3560)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (several invalid fields at once), Equivalence partitioning (invalid classes combined) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-18, Q-VAL-24 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix>" + 90 × "x" (101 characters), "description": 251 × "d", "structural": "maybe"}` | No category is created (R-VAL-13: `name` over its limit). Proposed, to confirm in Q-VAL-18 and Q-VAL-24: `400 Bad Request` with one entry each under `name`, `description` and `structural`. Open: Q-VAL-18 (status, keys and texts), Q-VAL-24 (error for `structural` as text). |
| 2 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix>`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** none expected. If a category is created, cleanup as `admin`: find it with `GET /api/part/category/?search=QA-<suffix>&limit=50`, then `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** step 2 expects no category because the name alone is over its limit; the other two invalid fields are expected to be reported in the same response (proposed).

**Duplicate check:** 52 · Review · matches: [API-VAL-113](category-field-validation-create-and-update.md) (52)

**Duplicate judgement:** Keep · Different expected outcome from API-VAL-113: several invalid fields in one body and whether all are reported in one error response, versus one wrong-type field per request. · test-case-reviewer, 2026-10-16

### API-VAL-117: Category name limit is enforced for form-urlencoded and multipart bodies

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` applies the 100-character `name` limit to `application/x-www-form-urlencoded` and `multipart/form-data` bodies the same way as to JSON. |
| **Requirement** | R-VAL-17, R-VAL-13. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` request bodies ([L957](../../requirements/openapi-parts.yaml#L957)), `components.schemas.Category.name` (`maxLength: 100`, [L3517](../../requirements/openapi-parts.yaml#L3517)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (name maxLength, maxLength + 1), Equivalence partitioning (content types: form-urlencoded, multipart) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-18 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` with `Content-Type: <row.content type>` | field `name` = `<row.name>`, field `description` = `QA-<suffix> <row.tag>` | `<row.expected status>`. For a `201`, the body is valid against `Category` and `name` equals the sent value. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/category/` as `engineer` | `limit=500` | `200 OK`. The number of results whose `description` is `QA-<suffix> <row.tag>` is `<row.count>`. |

**Data sets**

| Row | Class | content type | name | tag | expected status | error | count |
|---|---|---|---|---|---|---|---|
| `form on limit` | BVA: maxLength, form-urlencoded | `application/x-www-form-urlencoded` | `QA-<suffix>` + `f` + 88 × `x`, 100 characters | `frm01` | `201 Created` | None | `1` |
| `form over limit` | BVA: maxLength + 1, form-urlencoded | `application/x-www-form-urlencoded` | `QA-<suffix>` + `f` + 89 × `x`, 101 characters | `frm02` | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `0` |
| `multipart on limit` | BVA: maxLength, multipart | `multipart/form-data` | `QA-<suffix>` + `m` + 88 × `x`, 100 characters | `mpt01` | `201 Created` | None | `1` |
| `multipart over limit` | BVA: maxLength + 1, multipart | `multipart/form-data` | `QA-<suffix>` + `m` + 89 × `x`, 101 characters | `mpt02` | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `0` |

**Postconditions and cleanup:** up to two categories (the `on limit` rows). Cleanup as `admin`: `GET /api/part/category/?limit=500`, pick the results whose `description` starts with `QA-<suffix> frm` or `QA-<suffix> mpt`; for each, `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** R-VAL-17 states the three accepted content types; that the limit applies to them is the `Category` schema, shared by all three. The `on limit` rows are `201` because the content type is accepted (R-VAL-17) and the value is within `maxLength`. Each row's name has its own marker (`f` or `m`, the same length), so the two `on limit` rows never send the same top-level name and their result does not depend on whether sibling names must be unique (Q-VAL-20).

**Duplicate check:** 51 · Review · matches: [API-VAL-109](category-field-validation-create-and-update.md) (51)

**Duplicate judgement:** Keep · Different channel from API-VAL-109: form-urlencoded and multipart bodies (R-VAL-17) versus JSON. · test-case-reviewer, 2026-10-16

### API-VAL-118: Category PATCH changes only the fields sent and needs no required field

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` with one field changes only that field, and a body with no fields is compared with it. |
| **Requirement** | R-VAL-16, R-CRUD-09. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/` ([L1370](../../requirements/openapi-parts.yaml#L1370)), `components.schemas.PatchedCategory` (no `required` list, [L4979](../../requirements/openapi-parts.yaml#L4979)), response `components.schemas.Category`. |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid classes: one field, no fields), State transition (field value before and after update) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Patch base` with description `QA-<suffix> original` and `default_keywords` `qa`, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-23 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Patch base", "description": "QA-<suffix> original", "default_keywords": "qa"}` | `201 Created`. Body is valid against `Category`. |
| 2 | `PATCH /api/part/category/<pk from step 1>/` as `engineer` | `<row.body>` | `<row.expected status>`. Body is valid against `Category`; `description` is `<row.description after>`; `name` is `QA-<suffix> Patch base` and `default_keywords` is `qa`. |
| 3 | `GET /api/part/category/<pk from step 1>/` as `engineer` | None | `200 OK`. `description` is `<row.description after>`; `name` and `default_keywords` are unchanged. |

**Data sets**

| Row | Class | body | expected status | description after |
|---|---|---|---|---|
| `one field` | EP valid: single field (R-CRUD-09) | `{"description": "QA-<suffix> changed"}` | `200 OK` | `QA-<suffix> changed` |
| `empty body` | EP valid: no fields (R-VAL-16 no required fields) | `{}` | `Proposed, to confirm in Q-VAL-23: 200 OK` | `QA-<suffix> original` (R-CRUD-09: only the fields sent are updated) |

**Postconditions and cleanup:** Each row runs on its own with a new `QA-<suffix>`, so no two rows create the same name, and the row's categories are deleted when the row ends. Each row leaves one category. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** for the `empty body` row only the status is open (Q-VAL-23); that nothing changes is R-CRUD-09. The `one field` row states `name` and `default_keywords` stay as created: a PATCH updates only the fields sent (R-CRUD-09).

### API-VAL-119: Category PUT needs the name field, PATCH does not

| Field | Value |
|---|---|
| **Summary** | `PUT /api/part/category/{id}/` without a valid `name` does not update the category, while a `PUT` with only `name` updates it. |
| **Requirement** | R-VAL-13, R-VAL-16, R-CRUD-08. Schema: `requirements/openapi-parts.yaml PUT /api/part/category/{id}/` ([L1333](../../requirements/openapi-parts.yaml#L1333)), `components.schemas.Category` `required` including `name` ([L3572](../../requirements/openapi-parts.yaml#L3572)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid classes: name absent, null, empty; valid class: name only), Decision table (PUT versus PATCH required fields) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Put base` with description `QA-<suffix> original`, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-18, Q-VAL-19, Q-VAL-23 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Put base", "description": "QA-<suffix> original"}` | `201 Created`. Body is valid against `Category`. |
| 2 | `PUT /api/part/category/<pk from step 1>/` as `engineer` | `<row.body>` | `<row.expected status>`. For a `200`, the body is valid against `Category` and `name` is `<row.name after>`. For a rejected request, the body is `<row.error>`. |
| 3 | `GET /api/part/category/<pk from step 1>/` as `engineer` | None | `200 OK`. `name` is `<row.name after>`; `description` is `<row.description after>`. |

**Data sets**

| Row | Class | body | expected status | error | name after | description after |
|---|---|---|---|---|---|---|
| `name absent` | EP invalid: required key missing (R-VAL-13) | `{"description": "QA-<suffix> new"}` | `Proposed, to confirm in Q-VAL-23: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `QA-<suffix> Put base` (the category is not updated, R-VAL-13) | `QA-<suffix> original` |
| `name null` | EP invalid: null | `{"name": null}` | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `QA-<suffix> Put base` | `QA-<suffix> original` |
| `name empty` | EP invalid: empty string | `{"name": ""}` | `Proposed, to confirm in Q-VAL-19: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `Proposed, to confirm in Q-VAL-19: QA-<suffix> Put base` | `Proposed, to confirm in Q-VAL-19: QA-<suffix> original` |
| `name only` | EP valid: required field only | `{"name": "QA-<suffix> Put renamed"}` | `200 OK` | None | `QA-<suffix> Put renamed` | `Open: Q-VAL-23 (kept or reset to the default)` |

**Postconditions and cleanup:** Each row runs on its own with a new `QA-<suffix>`, so no two rows create the same name, and the row's categories are deleted when the row ends. Each row leaves one category. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** `name` is in the `Category` `required` list and not read-only, so a `PUT` body needs it; `PATCH` bodies need none (API-VAL-118). The `name only` row is `200 OK` because the full body requires only `name`.

**Duplicate check:** 54 · Review · matches: [API-VAL-103](part-field-validation-create-and-update.md) (54)

**Duplicate judgement:** Keep · Different resource and rule from API-VAL-103: `PUT /api/part/category/{id}/` and R-VAL-13/R-CRUD-08 versus `PUT /api/part/{id}/` and R-VAL-01/R-CRUD-03. · test-case-reviewer, 2026-10-16

### API-VAL-120: Category field limits are enforced on PATCH

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` applies the same limits as create: a value on the limit updates the category, a value one beyond it, or an invalid value, leaves the category as it was. |
| **Requirement** | R-VAL-13, R-VAL-14, R-VAL-16, R-CRUD-09. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/` ([L1370](../../requirements/openapi-parts.yaml#L1370)), `components.schemas.PatchedCategory` and the matching `Category` fields ([L3517](../../requirements/openapi-parts.yaml#L3517), [L3521](../../requirements/openapi-parts.yaml#L3521), [L3529](../../requirements/openapi-parts.yaml#L3529), [L3563](../../requirements/openapi-parts.yaml#L3563)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (maxLength, maxLength + 1), Equivalence partitioning (invalid classes: null, empty) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Upd base` with description `QA-<suffix> original`, `default_keywords` `qa`, `icon` `qa-icon`, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-18, Q-VAL-19 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Upd base", "description": "QA-<suffix> original", "default_keywords": "qa", "icon": "qa-icon"}` | `201 Created`. Body is valid against `Category`. |
| 2 | `PATCH /api/part/category/<pk from step 1>/` as `engineer` | `{"<row.field>": <row.value>}` | `<row.expected status>`. For a `200`, the body is valid against `Category` and `<row.field>` equals `<row.after>`. For a rejected request, the body is `<row.error>`. |
| 3 | `GET /api/part/category/<pk from step 1>/` as `engineer` | None | `200 OK`. `<row.field>` is `<row.after>`. |

**Data sets**

| Row | Class | field | value | expected status | error | after |
|---|---|---|---|---|---|---|
| `name on limit` | BVA: maxLength | `name` | `QA-<suffix>` + 89 × `x`, 100 characters | `200 OK` | None | the sent value |
| `name over limit` | BVA: maxLength + 1 | `name` | `QA-<suffix>` + 90 × `x`, 101 characters | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `Proposed, to confirm in Q-VAL-18: QA-<suffix> Upd base` |
| `name empty` | EP invalid: empty string | `name` | `""` | `Proposed, to confirm in Q-VAL-19: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `Proposed, to confirm in Q-VAL-19: QA-<suffix> Upd base` |
| `name null` | EP invalid: null | `name` | `null` | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `Proposed, to confirm in Q-VAL-18: QA-<suffix> Upd base` |
| `description on limit` | BVA: maxLength | `description` | 250 × `d` | `200 OK` | None | the sent value |
| `description over limit` | BVA: maxLength + 1 | `description` | 251 × `d` | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `Proposed, to confirm in Q-VAL-18: QA-<suffix> original` |
| `default_keywords on limit` | BVA: maxLength | `default_keywords` | 250 × `k` | `200 OK` | None | the sent value |
| `default_keywords over limit` | BVA: maxLength + 1 | `default_keywords` | 251 × `k` | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `Proposed, to confirm in Q-VAL-18: qa` |
| `default_keywords null` | EP valid: null on nullable field | `default_keywords` | `null` | `200 OK` | None | `Proposed, to confirm in Q-VAL-19: null` |
| `icon on limit` | BVA: maxLength | `icon` | 100 × `i` | `200 OK` | None | the sent value |
| `icon over limit` | BVA: maxLength + 1 | `icon` | 101 × `i` | `Proposed, to confirm in Q-VAL-18: 400 Bad Request` | `Open: Q-VAL-18 (error body and text)` | `Proposed, to confirm in Q-VAL-18: qa-icon` |

**Postconditions and cleanup:** Each row runs on its own with a new `QA-<suffix>`, so no two rows create the same name, and the row's categories are deleted when the row ends. Each row leaves one category. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** that a rejected update leaves the category unchanged is proposed, since no source states the error behaviour. The `after` for an accepted row is the sent value.

### API-VAL-121: Values sent for read-only Category fields on update

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` with a value for a read-only field (`pk`, `level`, `pathstring`, `part_count`, `subcategories`, `starred`) does not store the client value. |
| **Requirement** | R-VAL-15, R-VAL-16. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/` ([L1370](../../requirements/openapi-parts.yaml#L1370)), `components.schemas.PatchedCategory.pk` / `level` / `pathstring` / `part_count` / `subcategories` (`readOnly: true`, [L4983](../../requirements/openapi-parts.yaml#L4983), [L5004](../../requirements/openapi-parts.yaml#L5004), [L5021](../../requirements/openapi-parts.yaml#L5021), [L5012](../../requirements/openapi-parts.yaml#L5012), [L5017](../../requirements/openapi-parts.yaml#L5017)), `PatchedCategory.starred` (`readOnly: true`, [L5032](../../requirements/openapi-parts.yaml#L5032)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (read-only field set by the client), Error guessing (client changes the identity of a record) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Ro base` created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-21 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Ro base"}` | `201 Created`. Body is valid against `Category`; the values of `pk`, `level`, `pathstring`, `part_count`, `subcategories` and `starred` are recorded as `<before>`. |
| 2 | `PATCH /api/part/category/<pk from step 1>/` as `engineer` | `{"<row.field>": <row.value>}` | `<row.expected status>`. For a `200`, `<row.field>` in the body equals `<before>`, not `<row.value>` (read-only fields are not set by the client, R-VAL-15). |
| 3 | `GET /api/part/category/<pk from step 1>/` as `engineer` | None | `200 OK`. `<row.field>` equals `<before>`; `name` is `QA-<suffix> Ro base`. |

**Data sets**

| Row | Class | field | value | expected status |
|---|---|---|---|---|
| `pk` | EP: read-only identity | `pk` | `2147000000` | `Proposed, to confirm in Q-VAL-21: 200 OK` |
| `level` | EP: read-only depth | `level` | `7` | `Proposed, to confirm in Q-VAL-21: 200 OK` |
| `pathstring` | EP: read-only computed text | `pathstring` | `QA-<suffix> Forced/Path` | `Proposed, to confirm in Q-VAL-21: 200 OK` |
| `part_count` | EP: read-only total | `part_count` | `500` | `Proposed, to confirm in Q-VAL-21: 200 OK` |
| `subcategories` | EP: read-only total | `subcategories` | `500` | `Proposed, to confirm in Q-VAL-21: 200 OK` |
| `starred` | EP: read-only per-user flag | `starred` | `true` | `Proposed, to confirm in Q-VAL-21: 200 OK` |

**Postconditions and cleanup:** Each row runs on its own with a new `QA-<suffix>`, so no two rows create the same name, and the row's categories are deleted when the row ends. Each row leaves one category. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** if the API rejects the request, the status is still open (Q-VAL-21); the stored value must stay equal to `<before>` either way.

### API-VAL-122: Reference and flag fields of the wrong type are refused on category update

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` with `parent` as text or `structural` as text does not change the category. |
| **Requirement** | R-VAL-10 (each field matches its schema type), R-VAL-16, R-CRUD-09. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/` ([L1370](../../requirements/openapi-parts.yaml#L1370)), `components.schemas.PatchedCategory.parent` (`type: integer`, [L5007](../../requirements/openapi-parts.yaml#L5007)), `PatchedCategory.structural` (`type: boolean`, [L5036](../../requirements/openapi-parts.yaml#L5036)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid classes: text for integer, text for boolean) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Type base` with `structural` false and no parent, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-24 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Type base", "structural": false}` | `201 Created`. Body is valid against `Category`; `parent` is `null` and `structural` is `false`. |
| 2 | `PATCH /api/part/category/<pk from step 1>/` as `engineer` | `{"<row.field>": <row.value>}` | `<row.expected status>`. For a rejected request, the body is `<row.error>`. |
| 3 | `GET /api/part/category/<pk from step 1>/` as `engineer` | None | `200 OK`. `parent` is `null` and `structural` is `false`: unchanged (`Proposed, to confirm in Q-VAL-24` for the rejected rows). |

**Data sets**

| Row | Class | field | value | expected status | error |
|---|---|---|---|---|---|
| `parent text` | EP invalid: text for integer | `parent` | `"abc"` | `Proposed, to confirm in Q-VAL-24: 400 Bad Request` | `Open: Q-VAL-24 (error body and text)` |
| `structural text` | EP invalid: text for boolean | `structural` | `"maybe"` | `Proposed, to confirm in Q-VAL-24: 400 Bad Request` | `Open: Q-VAL-24 (error body and text)` |

**Postconditions and cleanup:** Each row runs on its own with a new `QA-<suffix>`, so no two rows create the same name, and the row's categories are deleted when the row ends. Each row leaves one category. Cleanup as `admin`: `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** the type rule R-VAL-10 names Part fields; the Category types come from the schema only, hence the proposal (Q-VAL-24).

### API-VAL-123: Renaming a category to a sibling's name on update

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` renaming a category to the `name` of a sibling under the same parent shows whether the rename is rejected and the category keeps its name. |
| **Requirement** | R-VAL-13 (uniqueness among sibling categories not stated), R-CRUD-09. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/` ([L1370](../../requirements/openapi-parts.yaml#L1370)), `components.schemas.PatchedCategory.name` ([L4987](../../requirements/openapi-parts.yaml#L4987)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate on rename), What-if business scenario (a category renamed to an existing sibling name) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: parent `QA-<suffix> Parent` and two child categories `QA-<suffix> Sibling One` and `QA-<suffix> Sibling Two` under it, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-20 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer`, three times | `{"name": "QA-<suffix> Parent"}`, then `{"name": "QA-<suffix> Sibling One", "parent": <pk of Parent>}` and `{"name": "QA-<suffix> Sibling Two", "parent": <pk of Parent>}` | `201 Created` each. Bodies are valid against `Category`; the `pk` of each is recorded. |
| 2 | `PATCH /api/part/category/<pk of Sibling Two>/` as `engineer` | `{"name": "QA-<suffix> Sibling One"}` | Proposed, to confirm in Q-VAL-20: `400 Bad Request`, category not renamed. Open: Q-VAL-20 (error body and text, or whether the rename is accepted). |
| 3 | `GET /api/part/category/<pk of Sibling Two>/` as `engineer` | None | `200 OK`. `name` is `Proposed, to confirm in Q-VAL-20: QA-<suffix> Sibling Two`. |

**Postconditions and cleanup:** three categories. Cleanup as `admin`: delete the two children, then the parent, each with `DELETE /api/part/category/<pk>/` and `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** the schema and docs state no uniqueness for category names; the same open question covers create (API-VAL-115).
