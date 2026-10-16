# Part field validation on create and update: VAL test cases

### API-VAL-092: Text field maximum lengths on create (description, IPN, keywords)

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` accepts `description` and `keywords` of 250 characters and `IPN` of 100 characters, and does not create a part when the value is one character longer. |
| **Requirement** | R-VAL-02, R-VAL-03, R-VAL-04. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.description` (`maxLength: 250`, [L4148](../../requirements/openapi-parts.yaml#L4148)), `Part.IPN` (`maxLength: 100`, [L4164](../../requirements/openapi-parts.yaml#L4164)), `Part.keywords` (`maxLength: 250`, [L4171](../../requirements/openapi-parts.yaml#L4171)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (maxLength, maxLength + 1 for description, IPN, keywords) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "<row.field>": <row.value>}` | `<row.expected status>`. For a `201`, the body is valid against `Part` and `<row.field>` equals the sent value. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`: a part exists only if step 1 created one. |

**Data sets**

| Row | Class | field | value | tag | expected status | error | count |
|---|---|---|---|---|---|---|---|
| `description on limit` | BVA: maxLength | `description` | 250 × `d` | `len01` | `201 Created` | None | `1` |
| `description over limit` | BVA: maxLength + 1 | `description` | 251 × `d` | `len02` | `Proposed, to confirm in Q-VAL-08: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `0` |
| `IPN on limit` | BVA: maxLength | `IPN` | 100 × `i` | `len03` | `201 Created` | None | `1` |
| `IPN over limit` | BVA: maxLength + 1 | `IPN` | 101 × `i` | `len04` | `Proposed, to confirm in Q-VAL-08: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `0` |
| `keywords on limit` | BVA: maxLength | `keywords` | 250 × `k` | `len05` | `201 Created` | None | `1` |
| `keywords over limit` | BVA: maxLength + 1 | `keywords` | 251 × `k` | `len06` | `Proposed, to confirm in Q-VAL-08: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `0` |

**Postconditions and cleanup:** up to three parts (the `on limit` rows). Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the part name carries the tag, so step 2 finds the part by name. The schema documents no error status (index, Not in schema #1).

**Duplicate check:** 63 · Review · matches: [API-VAL-093](part-field-validation-create-and-update.md) (63), [API-VAL-087](part-name-validation-on-create.md) (58), [API-VAL-095](part-field-validation-create-and-update.md) (56), [API-VAL-096](part-field-validation-create-and-update.md) (54)

**Duplicate judgement:** Keep · Different rules from every match: length limits of description, IPN and keywords (R-VAL-02 to R-VAL-04), versus revision and units (API-VAL-093), name (API-VAL-087), link URI format (API-VAL-095) and the default_expiry numeric range (API-VAL-096). · test-case-reviewer, 2026-10-16

### API-VAL-093: Revision and units length limits on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `revision` of 100 characters or `units` of 20 characters is compared with the same value one character longer, and with a `units` text that is not a unit. |
| **Requirement** | R-VAL-06, R-VAL-07, R-Unit_measure-02. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.revision` (`maxLength: 100`, [L4207](../../requirements/openapi-parts.yaml#L4207)), `Part.units` (`maxLength: 20`, [L4237](../../requirements/openapi-parts.yaml#L4237)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (revision and units maxLength, maxLength + 1), Equivalence partitioning (invalid class: text that is not a unit) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-07, Q-VAL-08, Q-VAL-12 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "<row.field>": <row.value>}` | `<row.expected status>`. For a `201`, the body is valid against `Part` and `<row.field>` equals the sent value. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. |

**Data sets**

| Row | Class | field | value | tag | expected status | error | count |
|---|---|---|---|---|---|---|---|
| `revision on limit` | BVA: maxLength | `revision` | 100 × `r` | `rev01` | `Proposed, to confirm in Q-VAL-07: 201 Created` | None | `Proposed, to confirm in Q-VAL-07: 1` |
| `revision over limit` | BVA: maxLength + 1 | `revision` | 101 × `r` | `rev02` | `Proposed, to confirm in Q-VAL-08: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `0` |
| `units on limit` | BVA: maxLength | `units` | 20 × `u` | `unt01` | `Open: Q-VAL-12 (201 if any text is accepted, 400 if checked against unit definitions)` | `Open: Q-VAL-12 (error body and text)` | `Open: Q-VAL-12 (1 if accepted, 0 if rejected)` |
| `units over limit` | BVA: maxLength + 1 | `units` | 21 × `u` | `unt02` | `Proposed, to confirm in Q-VAL-08: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `0` |
| `units not a unit` | EP invalid: text that is not a unit | `units` | `QA-notaunit` | `unt03` | `Open: Q-VAL-12 (status code)` | `Open: Q-VAL-12 (error body and text)` | `Open: Q-VAL-12 (1 if accepted, 0 if rejected)` |

**Postconditions and cleanup:** normally up to one part per accepted row. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** which unit strings are valid belongs to Unit_measure; only the length limit is stated here. The `revision` rows depend on the revision settings (Doc issue 8).

**Duplicate check:** 63 · Review · matches: [API-VAL-092](part-field-validation-create-and-update.md) (63), [API-VAL-095](part-field-validation-create-and-update.md) (63), [API-VAL-096](part-field-validation-create-and-update.md) (58), [API-VAL-090](part-name-validation-on-create.md) (52)

**Duplicate judgement:** Keep · Different rules and classes: revision and units limits (R-VAL-06, R-VAL-07) plus a not-a-unit class (Q-VAL-12), which no match covers; API-VAL-090 tests name over form content types. · test-case-reviewer, 2026-10-16

### API-VAL-094: Null, empty and whitespace-only values for optional text fields on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` accepts `null` for the nullable fields (`keywords`, `link`, `units`, `revision`) and compares it with `null`, empty and whitespace-only values for the non-nullable `description` and `IPN`. |
| **Requirement** | R-VAL-02, R-VAL-03, R-VAL-04, R-VAL-05, R-VAL-06, R-VAL-07, R-CRUD-12. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.keywords` / `link` / `units` / `revision` (`nullable: true`), `Part.description` / `Part.IPN` (not nullable, [L4148](../../requirements/openapi-parts.yaml#L4148), [L4164](../../requirements/openapi-parts.yaml#L4164)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (valid class: null on a nullable field; invalid classes: null on a non-nullable field), Error guessing (empty string, whitespace-only) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-07, Q-VAL-08, Q-VAL-09 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "<row.field>": <row.value>}` | `<row.expected status>`. For a `201`, the body is valid against `Part`. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. For a `1`, the part's `<row.field>` is `<row.stored value>`. |

**Data sets**

| Row | Class | field | value | tag | expected status | error | count | stored value |
|---|---|---|---|---|---|---|---|---|
| `keywords null` | EP valid: null on nullable field | `keywords` | `null` | `nul01` | `201 Created` | None | `1` | `Proposed, to confirm in Q-VAL-09: null` |
| `link null` | EP valid: null on nullable field | `link` | `null` | `nul02` | `201 Created` | None | `1` | `Proposed, to confirm in Q-VAL-09: null` |
| `units null` | EP valid: null on nullable field | `units` | `null` | `nul03` | `201 Created` | None | `1` | `Proposed, to confirm in Q-VAL-09: null` |
| `revision null` | EP valid: null on nullable field | `revision` | `null` | `nul04` | `Proposed, to confirm in Q-VAL-07: 201 Created` | None | `Proposed, to confirm in Q-VAL-07: 1` | `Open: Q-VAL-09 (null or empty string)` |
| `description null` | EP invalid: null on non-nullable field | `description` | `null` | `nul05` | `Proposed, to confirm in Q-VAL-09: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `Proposed, to confirm in Q-VAL-09: 0` | None |
| `IPN null` | EP invalid: null on non-nullable field | `IPN` | `null` | `nul06` | `Proposed, to confirm in Q-VAL-09: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `Proposed, to confirm in Q-VAL-09: 0` | None |
| `description empty` | Error guessing: empty string | `description` | `""` | `nul07` | `Proposed, to confirm in Q-VAL-09: 201 Created` | None | `Proposed, to confirm in Q-VAL-09: 1` | `Proposed, to confirm in Q-VAL-09: ""` |
| `IPN empty` | Error guessing: empty string (the schema default) | `IPN` | `""` | `nul08` | `Proposed, to confirm in Q-VAL-09: 201 Created` | None | `Proposed, to confirm in Q-VAL-09: 1` | `Proposed, to confirm in Q-VAL-09: ""` |
| `description whitespace` | Error guessing: whitespace-only | `description` | `"   "` (3 spaces) | `nul09` | `Open: Q-VAL-09 (accepted or rejected)` | `Open: Q-VAL-09 (error body and text)` | `Open: Q-VAL-09 (1 if accepted, 0 if rejected)` | `Open: Q-VAL-09 (as sent or trimmed)` |
| `IPN whitespace` | Error guessing: whitespace-only | `IPN` | `"   "` (3 spaces) | `nul10` | `Open: Q-VAL-09 (accepted or rejected)` | `Open: Q-VAL-09 (error body and text)` | `Open: Q-VAL-09 (1 if accepted, 0 if rejected)` | `Open: Q-VAL-09 (as sent or trimmed)` |

**Postconditions and cleanup:** up to ten parts. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** `nullable: true` states that `null` is allowed for those four fields; it says nothing about the returned form, hence the proposed stored values. `description` and `IPN` are not marked nullable; the rejection of `null` is only proposed.

**Duplicate check:** 54 · Review · matches: [API-VAL-097](part-field-validation-create-and-update.md) (54), [API-VAL-098](part-field-validation-create-and-update.md) (54)

**Duplicate judgement:** Keep · Tests null, empty and whitespace-only classes on the text fields and the stored form, versus stock number values (API-VAL-097) and wrong-type reference and flag fields (API-VAL-098): different rules, classes and outcomes. · test-case-reviewer, 2026-10-16

### API-VAL-095: Part link must be a URI of at most 2000 characters, or empty

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` accepts a `link` that is a URI of up to 2000 characters or an empty string, and refuses a text that is not a URI or is longer than 2000 characters. |
| **Requirement** | R-VAL-05, R-Part-17. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.link` (`oneOf` URI `maxLength: 2000` or string `maxLength: 0`, `nullable`, [L4176](../../requirements/openapi-parts.yaml#L4176)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Equivalence partitioning (valid classes: URI, empty string; invalid classes: not a URI, no scheme), Boundary value analysis (link maxLength, maxLength + 1) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-08, Q-VAL-10 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "link": <row.link>}` | `<row.expected status>`. For a `201`, the body is valid against `Part` and `link` equals the sent value. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. |

**Data sets**

| Row | Class | link | tag | expected status | error | count |
|---|---|---|---|---|---|---|
| `valid https URL` | EP valid: URI | `https://example.com/qa` | `lnk01` | `201 Created` | None | `1` |
| `empty string` | EP valid: empty string alternative | `""` | `lnk02` | `201 Created` | None | `1` |
| `on limit` | BVA: maxLength | `https://example.com/` + 1980 × `a`, 2000 characters | `lnk03` | `201 Created` | None | `1` |
| `over limit` | BVA: maxLength + 1 | `https://example.com/` + 1981 × `a`, 2001 characters | `lnk04` | `Proposed, to confirm in Q-VAL-10: 400 Bad Request` | `Open: Q-VAL-10 (error body and text)` | `0` |
| `not a URL` | EP invalid: not a URI | `not a url` | `lnk05` | `Proposed, to confirm in Q-VAL-10: 400 Bad Request` | `Proposed, to confirm in Q-VAL-10: {"link": ["Enter a valid URL."]}` | `0` |
| `no scheme` | EP invalid: URI without scheme | `www.example.com` | `lnk06` | `Proposed, to confirm in Q-VAL-10: 400 Bad Request` | `Proposed, to confirm in Q-VAL-10: {"link": ["Enter a valid URL."]}` | `0` |

**Postconditions and cleanup:** up to four parts (the first three rows). Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the inventory records the text "Enter a valid URL." from the 1.5.6 API (R-Part-17); it is not in the schema, so it stays proposed. The UI label of this field is *Link* (Doc issue 13).

**Duplicate check:** 63 · Review · matches: [API-VAL-093](part-field-validation-create-and-update.md) (63), [API-VAL-096](part-field-validation-create-and-update.md) (57), [API-VAL-092](part-field-validation-create-and-update.md) (56), [API-VAL-090](part-name-validation-on-create.md) (51)

**Duplicate judgement:** Keep · Only case for the link rule (R-VAL-05): URI format classes (not a URI, no scheme, empty-string alternative) and the 2000-character limit, which no match covers. · test-case-reviewer, 2026-10-16

### API-VAL-096: Part default expiry range on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` accepts a `default_expiry` from 0 to 2147483647 and does not create a part for a value below 0, above 2147483647, non-integer or null. |
| **Requirement** | R-VAL-08, R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.default_expiry` (`type: integer`, `minimum: 0`, `maximum: 2147483647`, not nullable, [L4139](../../requirements/openapi-parts.yaml#L4139)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (minimum - 1, minimum, minimum + 1, maximum, maximum + 1), Equivalence partitioning (invalid classes: text, decimal, null) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-11 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "default_expiry": <row.default_expiry>}` | `<row.expected status>`. For a `201`, the body is valid against `Part` and `default_expiry` equals `<row.default_expiry>`. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. |

**Data sets**

| Row | Class | default_expiry | tag | expected status | error | count |
|---|---|---|---|---|---|---|
| `below minimum` | BVA: minimum - 1 | `-1` | `exp01` | `Proposed, to confirm in Q-VAL-11: 400 Bad Request` | `Open: Q-VAL-11 (error body and text)` | `0` |
| `on minimum` | BVA: minimum | `0` | `exp02` | `201 Created` | None | `1` |
| `above minimum` | BVA: minimum + 1 | `1` | `exp03` | `201 Created` | None | `1` |
| `on maximum` | BVA: maximum | `2147483647` | `exp04` | `201 Created` | None | `1` |
| `above maximum` | BVA: maximum + 1 | `2147483648` | `exp05` | `Proposed, to confirm in Q-VAL-11: 400 Bad Request` | `Open: Q-VAL-11 (error body and text)` | `0` |
| `text` | EP invalid: not a number | `"abc"` | `exp06` | `Proposed, to confirm in Q-VAL-11: 400 Bad Request` | `Open: Q-VAL-11 (error body and text)` | `0` |
| `decimal` | EP invalid: not an integer | `1.5` | `exp07` | `Proposed, to confirm in Q-VAL-11: 400 Bad Request` | `Open: Q-VAL-11 (error body and text)` | `0` |
| `null` | EP invalid: null (not nullable) | `null` | `exp08` | `Proposed, to confirm in Q-VAL-11: 400 Bad Request` | `Open: Q-VAL-11 (error body and text)` | `0` |

**Postconditions and cleanup:** three parts (`on minimum`, `above minimum`, `on maximum`). Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the schema states the numeric range; the status code for a value outside it is not documented (index, Not in schema #1).

**Duplicate check:** 58 · Review · matches: [API-VAL-093](part-field-validation-create-and-update.md) (58), [API-VAL-095](part-field-validation-create-and-update.md) (57), [API-VAL-092](part-field-validation-create-and-update.md) (54), [API-VAL-087](part-name-validation-on-create.md) (50)

**Duplicate judgement:** Keep · Integer range of default_expiry (R-VAL-08: minimum and maximum, non-integer, null) versus string length or URI rules in every match. · test-case-reviewer, 2026-10-16

### API-VAL-097: Minimum and maximum stock values on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` accepts numeric `minimum_stock` and `maximum_stock` (default 0) and compares them with non-numeric, null, negative and inverted values. |
| **Requirement** | R-VAL-09, R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.minimum_stock` and `Part.maximum_stock` (`type: number`, `format: double`, `default: 0.0`, [L4188](../../requirements/openapi-parts.yaml#L4188)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (valid classes: zero, decimal; invalid classes: text, null), Boundary value analysis (negative value, minimum above maximum) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-08, Q-VAL-11 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "minimum_stock": <row.min>, "maximum_stock": <row.max>}` | `<row.expected status>`. For a `201`, the body is valid against `Part` and both values equal the payload. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. |

**Data sets**

| Row | Class | min | max | tag | expected status | error | count |
|---|---|---|---|---|---|---|---|
| `zero and zero` | EP valid: default value | `0` | `0` | `stk01` | `201 Created` | None | `1` |
| `decimals` | EP valid: decimal | `2.5` | `10.75` | `stk02` | `201 Created` | None | `1` |
| `min text` | EP invalid: not a number | `"abc"` | `0` | `stk03` | `Proposed, to confirm in Q-VAL-11: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `0` |
| `max null` | EP invalid: null (not nullable) | `0` | `null` | `stk04` | `Proposed, to confirm in Q-VAL-11: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `0` |
| `min negative` | BVA: below zero | `-1` | `0` | `stk05` | `Open: Q-VAL-11 (accepted or rejected; no minimum in the schema)` | `Open: Q-VAL-11 (error body and text)` | `Open: Q-VAL-11 (1 if accepted, 0 if rejected)` |
| `min above max` | BVA: minimum above maximum | `10` | `5` | `stk06` | `Open: Q-VAL-11 (accepted or rejected; no relation stated)` | `Open: Q-VAL-11 (error body and text)` | `Open: Q-VAL-11 (1 if accepted, 0 if rejected)` |

**Postconditions and cleanup:** up to six parts. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the schema gives no lower limit for the stock fields (inventory R-VAL-09), so the `min negative` and `min above max` rows have no proposal.

**Duplicate check:** 60 · Review · matches: [API-VAL-098](part-field-validation-create-and-update.md) (60), [API-VAL-094](part-field-validation-create-and-update.md) (54), [API-VAL-108](part-field-validation-create-and-update.md) (51)

**Duplicate judgement:** Keep · Only case for minimum_stock and maximum_stock (R-VAL-09), with two fields sent together (negative, inverted), versus reference and flag types (API-VAL-098), null text fields (API-VAL-094) and an unknown key (API-VAL-108). · test-case-reviewer, 2026-10-16

### API-VAL-098: Reference and flag fields of the wrong type are refused on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` does not create a part when an integer reference field is text, a decimal or the `pk` of a deleted category, or a boolean flag is not a boolean. |
| **Requirement** | R-VAL-10. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.category` / `variant_of` / `responsible` (`type: integer`, [L4122](../../requirements/openapi-parts.yaml#L4122)), `Part.active` / `assembly` / `trackable` (`type: boolean`, [L4112](../../requirements/openapi-parts.yaml#L4112)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid classes: text, decimal, array, reference to a record that does not exist) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Gone` created with `POST /api/part/category/` as `admin`, then deleted with `DELETE /api/part/category/<pk>/` and body `{"delete_parts": false, "delete_child_categories": false}`; its `pk` is `<deleted category pk>`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-08, Q-VAL-13 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "<row.field>": <row.value>}` | `<row.expected status>`. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. |

**Data sets**

| Row | Class | field | value | tag | expected status | error | count |
|---|---|---|---|---|---|---|---|
| `category text` | EP invalid: text for integer | `category` | `"abc"` | `typ11` | `Proposed, to confirm in Q-VAL-13: 400 Bad Request` | `Open: Q-VAL-13 (error body and text)` | `Proposed, to confirm in Q-VAL-13: 0` |
| `category decimal` | EP invalid: decimal for integer | `category` | `1.5` | `typ12` | `Proposed, to confirm in Q-VAL-13: 400 Bad Request` | `Open: Q-VAL-13 (error body and text)` | `Proposed, to confirm in Q-VAL-13: 0` |
| `category deleted` | EP invalid: reference to a deleted record | `category` | `<deleted category pk>` | `typ13` | `Proposed, to confirm in Q-VAL-13: 400 Bad Request` | `Open: Q-VAL-13 (error body and text)` | `Proposed, to confirm in Q-VAL-13: 0` |
| `variant_of text` | EP invalid: text for integer | `variant_of` | `"abc"` | `typ14` | `Proposed, to confirm in Q-VAL-13: 400 Bad Request` | `Open: Q-VAL-13 (error body and text)` | `Proposed, to confirm in Q-VAL-13: 0` |
| `responsible text` | EP invalid: text for integer | `responsible` | `"abc"` | `typ15` | `Proposed, to confirm in Q-VAL-13: 400 Bad Request` | `Open: Q-VAL-13 (error body and text)` | `Proposed, to confirm in Q-VAL-13: 0` |
| `active text` | EP invalid: text for boolean | `active` | `"maybe"` | `typ16` | `Proposed, to confirm in Q-VAL-13: 400 Bad Request` | `Open: Q-VAL-13 (error body and text)` | `Proposed, to confirm in Q-VAL-13: 0` |
| `assembly text` | EP invalid: text for boolean | `assembly` | `"maybe"` | `typ17` | `Proposed, to confirm in Q-VAL-13: 400 Bad Request` | `Open: Q-VAL-13 (error body and text)` | `Proposed, to confirm in Q-VAL-13: 0` |
| `trackable array` | EP invalid: array for boolean | `trackable` | `[true]` | `typ18` | `Proposed, to confirm in Q-VAL-13: 400 Bad Request` | `Open: Q-VAL-13 (error body and text)` | `Proposed, to confirm in Q-VAL-13: 0` |

**Postconditions and cleanup:** normally no record. If a row creates a part, cleanup as `admin`: find it by the name tag with `GET /api/part/?search=QA-<suffix>&limit=50`, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the schema gives the types; the rejection and status are proposed. The deleted `pk` is taken from a real deleted category, never guessed (standing rule).

**Duplicate check:** 66 · Review · matches: [API-VAL-089](part-name-validation-on-create.md) (66), [API-VAL-097](part-field-validation-create-and-update.md) (60), [API-VAL-094](part-field-validation-create-and-update.md) (54), [API-VAL-108](part-field-validation-create-and-update.md) (53), [API-VAL-099](part-field-validation-create-and-update.md) (52)

**Duplicate judgement:** Keep · Wrong types on integer reference and boolean flag fields, plus a deleted-record reference (R-VAL-10, Q-VAL-13), versus the name field's types (API-VAL-089, R-VAL-01, Q-VAL-06) and the other matches' different rules. · test-case-reviewer, 2026-10-16

### API-VAL-099: Values sent for read-only Part fields on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with values for read-only fields (`pk`, `full_name`, `barcode_hash`, `creation_date`, `in_stock`) shows whether the request is ignored or rejected and that the client value is not stored. |
| **Requirement** | R-VAL-11. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.pk` / `full_name` / `barcode_hash` / `creation_date` / `in_stock` (`readOnly: true`, [L4200](../../requirements/openapi-parts.yaml#L4200), [L4152](../../requirements/openapi-parts.yaml#L4152), [L4118](../../requirements/openapi-parts.yaml#L4118), [L4131](../../requirements/openapi-parts.yaml#L4131), [L4298](../../requirements/openapi-parts.yaml#L4298)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (read-only field set by the client), Error guessing (client sets server-assigned identity and totals) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-14 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "<row.field>": <row.value>}` | `<row.expected status>`. For a `201`, `<row.field>` in the body is not `<row.value>` (R-VAL-11: read-only fields are returned, not set by the client). Open: Q-VAL-14 (ignored or rejected). |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. For a `1`, the stored `<row.field>` is not `<row.value>`. |

**Data sets**

| Row | Class | field | value | tag | expected status | count |
|---|---|---|---|---|---|---|
| `pk` | EP: read-only identity | `pk` | `2147000000` | `rof01` | `Proposed, to confirm in Q-VAL-14: 201 Created` | `Proposed, to confirm in Q-VAL-14: 1` |
| `full_name` | EP: read-only computed text | `full_name` | `QA-<suffix> Forced` | `rof02` | `Proposed, to confirm in Q-VAL-14: 201 Created` | `Proposed, to confirm in Q-VAL-14: 1` |
| `barcode_hash` | EP: read-only hash | `barcode_hash` | `abc123` | `rof03` | `Proposed, to confirm in Q-VAL-14: 201 Created` | `Proposed, to confirm in Q-VAL-14: 1` |
| `creation_date` | EP: read-only date | `creation_date` | `"2000-01-01"` | `rof04` | `Proposed, to confirm in Q-VAL-14: 201 Created` | `Proposed, to confirm in Q-VAL-14: 1` |
| `in_stock` | EP: read-only total | `in_stock` | `500` | `rof05` | `Proposed, to confirm in Q-VAL-14: 201 Created` | `Proposed, to confirm in Q-VAL-14: 1` |

**Postconditions and cleanup:** up to five parts. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the schema marks the fields read-only only; "ignored or rejected" is unanswered (index, Not in schema #5). The `pk` value must not belong to an existing part; if the API accepts it against the proposal, record that as a finding.

**Duplicate check:** 52 · Review · matches: [API-VAL-098](part-field-validation-create-and-update.md) (52)

**Duplicate judgement:** Keep · Read-only fields set by the client (R-VAL-11, proposed ignored and request accepted) versus wrong-type writable fields expected to be refused (API-VAL-098, R-VAL-10). · test-case-reviewer, 2026-10-16

### API-VAL-100: Write-only Part fields are accepted on create and never returned

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `initial_stock` and `copy_category_parameters` returns a part whose body, and a later `GET`, contain none of the write-only fields. |
| **Requirement** | R-VAL-12, R-CRUD-13, R-CRUD-15. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.initial_stock` / `copy_category_parameters` / `duplicate` / `initial_supplier` / `existing_image` (`writeOnly: true`, [L4349](../../requirements/openapi-parts.yaml#L4349), [L4360](../../requirements/openapi-parts.yaml#L4360), [L4160](../../requirements/openapi-parts.yaml#L4160)). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: write-only fields on input), Decision table (write-only field sent or not) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, add stock); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Write only", "copy_category_parameters": false, "initial_stock": {"quantity": "5"}}` | `201 Created`. Body is valid against `Part`; `name` equals the payload; the body has no key `initial_stock`, `copy_category_parameters`, `duplicate`, `initial_supplier` or `existing_image` (R-VAL-12). |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. Body is valid against `Part`; none of the five write-only keys is present (R-VAL-12). |

**Postconditions and cleanup:** one part with initial stock. Cleanup as `admin`: delete its stock item (`GET /api/stock/?part=<pk>`, then `DELETE /api/stock/<pk>/`), `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the stock endpoints are outside the Parts API scope and are used only for cleanup. Whether the stock was created is checked in API-VAL-101.

### API-VAL-101: Initial stock quantity is required and limited on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with `initial_stock` requires `quantity`, adds no stock for a quantity of zero, and refuses a quantity outside the schema pattern. |
| **Requirement** | R-VAL-18, R-CRUD-13. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.InitialStock.quantity` (`required`, `pattern: ^-?\d{0,10}(?:\.\d{0,5})?$`, "If quantity is zero, no stock is added", [L3714](../../requirements/openapi-parts.yaml#L3714)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Equivalence partitioning (invalid classes: quantity absent, text, negative), Boundary value analysis (zero, 10 integer digits, 11 integer digits, 5 decimals, 6 decimals) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts, add stock); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-15 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> <row.tag>", "initial_stock": <row.initial_stock>}` | `<row.expected status>`. For a rejected request, the body is `<row.error>`. |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK`. `count` is `<row.count>`. For a `1`, the part's `stock_item_count` is `<row.stock items>`. |

**Data sets**

| Row | Class | initial_stock | tag | expected status | error | count | stock items |
|---|---|---|---|---|---|---|---|
| `quantity absent` | EP invalid: required key missing (R-VAL-18) | `{"location": null}` | `ini01` | `Proposed, to confirm in Q-VAL-15: 400 Bad Request` | `Open: Q-VAL-15 (error body and text)` | `Proposed, to confirm in Q-VAL-15: 0` | None |
| `quantity zero` | BVA: zero | `{"quantity": "0"}` | `ini02` | `Proposed, to confirm in Q-VAL-15: 201 Created` | None | `Proposed, to confirm in Q-VAL-15: 1` | `0` |
| `quantity five` | EP valid: positive | `{"quantity": "5"}` | `ini03` | `201 Created` | None | `1` | `Proposed, to confirm in Q-VAL-15: 1` |
| `5 decimals` | BVA: pattern, 5 decimals | `{"quantity": "1.12345"}` | `ini04` | `Proposed, to confirm in Q-VAL-15: 201 Created` | None | `Proposed, to confirm in Q-VAL-15: 1` | `Proposed, to confirm in Q-VAL-15: 1` |
| `6 decimals` | BVA: pattern, 6 decimals | `{"quantity": "1.123456"}` | `ini05` | `Proposed, to confirm in Q-VAL-15: 400 Bad Request` | `Open: Q-VAL-15 (error body and text)` | `Proposed, to confirm in Q-VAL-15: 0` | None |
| `10 integer digits` | BVA: pattern, 10 digits | `{"quantity": "9999999999"}` | `ini06` | `Proposed, to confirm in Q-VAL-15: 201 Created` | None | `Proposed, to confirm in Q-VAL-15: 1` | `Proposed, to confirm in Q-VAL-15: 1` |
| `11 integer digits` | BVA: pattern, 11 digits | `{"quantity": "99999999999"}` | `ini07` | `Proposed, to confirm in Q-VAL-15: 400 Bad Request` | `Open: Q-VAL-15 (error body and text)` | `Proposed, to confirm in Q-VAL-15: 0` | None |
| `text` | EP invalid: not a number | `{"quantity": "abc"}` | `ini08` | `Proposed, to confirm in Q-VAL-15: 400 Bad Request` | `Open: Q-VAL-15 (error body and text)` | `Proposed, to confirm in Q-VAL-15: 0` | None |
| `negative` | EP invalid: negative (pattern allows `-`) | `{"quantity": "-1"}` | `ini09` | `Open: Q-VAL-15 (accepted or rejected)` | `Open: Q-VAL-15 (error body and text)` | `Open: Q-VAL-15 (1 if accepted, 0 if rejected)` | `Open: Q-VAL-15 (stock items created)` |

**Postconditions and cleanup:** up to six parts, some with stock. Cleanup as `admin`: find the parts with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, delete its stock items (`GET /api/stock/?part=<pk>`, `DELETE /api/stock/<pk>/`), `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the `quantity zero` row states "no stock is added" (schema description), so `stock_item_count` is `0` as fact; the part creation itself is proposed. The `quantity five` row is `201` and one part per the rule; only the stock item count is proposed. A quantity of 10 digits may still be refused by the stock model; record any such result as a finding.

### API-VAL-102: PATCH changes only the fields sent and needs no required field

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with one field changes only that field, and a body with no fields is compared with it. |
| **Requirement** | R-VAL-16, R-CRUD-04. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([L2767](../../requirements/openapi-parts.yaml#L2767)), `components.schemas.PatchedPart` (no `required` list), response `components.schemas.Part`. |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid classes: one field, no fields), State transition (field value before and after update) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Patch base` with IPN `QA-<suffix>-P`, description `QA-<suffix> original`, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-16 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Patch base", "IPN": "QA-<suffix>-P", "description": "QA-<suffix> original"}` | `201 Created`. Body is valid against `Part`. |
| 2 | `PATCH /api/part/<pk from step 1>/` as `engineer` | `<row.body>` | `<row.expected status>`. Body is valid against `Part`; `description` is `<row.description after>`; `name` is `QA-<suffix> Patch base` and `IPN` is `QA-<suffix>-P`. |
| 3 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `description` is `<row.description after>`; `name` and `IPN` are unchanged. |

**Data sets**

| Row | Class | body | expected status | description after |
|---|---|---|---|---|
| `one field` | EP valid: single field (R-CRUD-04) | `{"description": "QA-<suffix> changed"}` | `200 OK` | `QA-<suffix> changed` |
| `empty body` | EP valid: no fields (R-VAL-16 no required fields) | `{}` | `Proposed, to confirm in Q-VAL-16: 200 OK` | `Proposed, to confirm in Q-VAL-16: QA-<suffix> original` |

**Postconditions and cleanup:** one part per row run. Cleanup as `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the `one field` row states `name` and `IPN` stay as created: the PATCH body updates only the fields sent (R-CRUD-04).

### API-VAL-103: PUT needs the name field, PATCH does not

| Field | Value |
|---|---|
| **Summary** | `PUT /api/part/{id}/` without a valid `name` does not update the part, while a `PUT` with only `name` updates it. |
| **Requirement** | R-VAL-01, R-VAL-16, R-CRUD-03. Schema: `requirements/openapi-parts.yaml PUT /api/part/{id}/` ([L2730](../../requirements/openapi-parts.yaml#L2730)), `components.schemas.Part` `required` including `name` ([L4365](../../requirements/openapi-parts.yaml#L4365)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid classes: name absent, null, empty; valid class: name only), Decision table (PUT versus PATCH required fields) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Put base` with description `QA-<suffix> original`, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01, Q-VAL-02, Q-VAL-08, Q-VAL-16 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Put base", "description": "QA-<suffix> original"}` | `201 Created`. Body is valid against `Part`. |
| 2 | `PUT /api/part/<pk from step 1>/` as `engineer` | `<row.body>` | `<row.expected status>`. For a `200`, the body is valid against `Part` and `name` is `<row.name after>`. For a rejected request, the body is `<row.error>`. |
| 3 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `name` is `<row.name after>`; `description` is `<row.description after>`. |

**Data sets**

| Row | Class | body | expected status | error | name after | description after |
|---|---|---|---|---|---|---|
| `name absent` | EP invalid: required key missing (R-VAL-01) | `{"description": "QA-<suffix> new"}` | `Proposed, to confirm in Q-VAL-16: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `QA-<suffix> Put base` (the part is not updated, R-VAL-01) | `QA-<suffix> original` |
| `name null` | EP invalid: null | `{"name": null}` | `Proposed, to confirm in Q-VAL-01: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `QA-<suffix> Put base` | `QA-<suffix> original` |
| `name empty` | EP invalid: empty string | `{"name": ""}` | `Proposed, to confirm in Q-VAL-02: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `Proposed, to confirm in Q-VAL-02: QA-<suffix> Put base` | `Proposed, to confirm in Q-VAL-02: QA-<suffix> original` |
| `name only` | EP valid: required field only | `{"name": "QA-<suffix> Put renamed"}` | `200 OK` | None | `QA-<suffix> Put renamed` | `Open: Q-VAL-16 (kept or reset to the default)` |

**Postconditions and cleanup:** one part per row run. Cleanup as `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** `name` is in the `Part` `required` list and not read-only, so a `PUT` body needs it; `PATCH` bodies need none (API-VAL-102). The `name only` row is `200 OK` because the full body requires only `name`.

### API-VAL-104: Field limits are enforced on PATCH

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` applies the same limits as create: a value on the limit updates the part, a value one beyond it, or an invalid value, leaves the part as it was. |
| **Requirement** | R-VAL-01, R-VAL-02, R-VAL-03, R-VAL-04, R-VAL-05, R-VAL-08, R-VAL-16. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([L2767](../../requirements/openapi-parts.yaml#L2767)), `components.schemas.PatchedPart` and the matching `Part` fields ([L4105](../../requirements/openapi-parts.yaml#L4105)). |
| **Area** | VAL |
| **Type** | Boundary |
| **Technique** | Boundary value analysis (maxLength, maxLength + 1, minimum - 1), Equivalence partitioning (invalid classes: null, empty, not a URI) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Upd base` with description `QA-<suffix> original`, IPN `QA-<suffix>-ORIG`, keywords `qa`, `default_expiry` 7, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-01, Q-VAL-02, Q-VAL-08, Q-VAL-09, Q-VAL-10, Q-VAL-11 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Upd base", "description": "QA-<suffix> original", "IPN": "QA-<suffix>-ORIG", "keywords": "qa", "default_expiry": 7}` | `201 Created`. Body is valid against `Part`. |
| 2 | `PATCH /api/part/<pk from step 1>/` as `engineer` | `{"<row.field>": <row.value>}` | `<row.expected status>`. For a `200`, the body is valid against `Part` and `<row.field>` equals `<row.after>`. For a rejected request, the body is `<row.error>`. |
| 3 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `<row.field>` is `<row.after>`. |

**Data sets**

| Row | Class | field | value | expected status | error | after |
|---|---|---|---|---|---|---|
| `name on limit` | BVA: maxLength | `name` | `QA-<suffix>` + 89 × `x`, 100 characters | `200 OK` | None | the sent value |
| `name over limit` | BVA: maxLength + 1 | `name` | `QA-<suffix>` + 90 × `x`, 101 characters | `Proposed, to confirm in Q-VAL-01: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `Proposed, to confirm in Q-VAL-01: QA-<suffix> Upd base` |
| `name empty` | EP invalid: empty string | `name` | `""` | `Proposed, to confirm in Q-VAL-02: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `Proposed, to confirm in Q-VAL-02: QA-<suffix> Upd base` |
| `name null` | EP invalid: null | `name` | `null` | `Proposed, to confirm in Q-VAL-01: 400 Bad Request` | `Open: Q-VAL-01 (error body and text)` | `Proposed, to confirm in Q-VAL-01: QA-<suffix> Upd base` |
| `description on limit` | BVA: maxLength | `description` | 250 × `d` | `200 OK` | None | the sent value |
| `description over limit` | BVA: maxLength + 1 | `description` | 251 × `d` | `Proposed, to confirm in Q-VAL-08: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `Proposed, to confirm in Q-VAL-08: QA-<suffix> original` |
| `IPN over limit` | BVA: maxLength + 1 | `IPN` | 101 × `i` | `Proposed, to confirm in Q-VAL-08: 400 Bad Request` | `Open: Q-VAL-08 (error body and text)` | `Proposed, to confirm in Q-VAL-08: QA-<suffix>-ORIG` |
| `keywords null` | EP valid: null on nullable field | `keywords` | `null` | `200 OK` | None | `Proposed, to confirm in Q-VAL-09: null` |
| `link not a URL` | EP invalid: not a URI | `link` | `not a url` | `Proposed, to confirm in Q-VAL-10: 400 Bad Request` | `Proposed, to confirm in Q-VAL-10: {"link": ["Enter a valid URL."]}` | `Proposed, to confirm in Q-VAL-10: the original link (empty)` |
| `default_expiry below minimum` | BVA: minimum - 1 | `default_expiry` | `-1` | `Proposed, to confirm in Q-VAL-11: 400 Bad Request` | `Open: Q-VAL-11 (error body and text)` | `Proposed, to confirm in Q-VAL-11: 7` |

**Postconditions and cleanup:** one part per row run. Cleanup as `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** that a rejected update leaves the part unchanged is proposed, since no source states the error behaviour. The `after` for an accepted row is the sent value.

### API-VAL-105: Values sent for read-only Part fields on update

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with a value for a read-only field (`pk`, `full_name`, `barcode_hash`, `creation_date`, `in_stock`) does not store the client value. |
| **Requirement** | R-VAL-11, R-VAL-16. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([L2767](../../requirements/openapi-parts.yaml#L2767)), `components.schemas.Part.pk` / `full_name` / `barcode_hash` / `creation_date` / `in_stock` (`readOnly: true`, [L4200](../../requirements/openapi-parts.yaml#L4200), [L4152](../../requirements/openapi-parts.yaml#L4152), [L4118](../../requirements/openapi-parts.yaml#L4118), [L4131](../../requirements/openapi-parts.yaml#L4131), [L4298](../../requirements/openapi-parts.yaml#L4298)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (read-only field set by the client), Error guessing (client changes the identity of a record) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Ro base` created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-14 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Ro base"}` | `201 Created`. Body is valid against `Part`; the values of `pk`, `full_name`, `barcode_hash`, `creation_date` and `in_stock` are recorded as `<before>`. |
| 2 | `PATCH /api/part/<pk from step 1>/` as `engineer` | `{"<row.field>": <row.value>}` | `<row.expected status>`. For a `200`, `<row.field>` in the body equals `<before>`, not `<row.value>` (R-VAL-11: read-only fields are returned, not set by the client). |
| 3 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `<row.field>` equals `<before>`; `name` is `QA-<suffix> Ro base`. |

**Data sets**

| Row | Class | field | value | expected status |
|---|---|---|---|---|
| `pk` | EP: read-only identity | `pk` | `2147000000` | `Proposed, to confirm in Q-VAL-14: 200 OK` |
| `full_name` | EP: read-only computed text | `full_name` | `QA-<suffix> Forced` | `Proposed, to confirm in Q-VAL-14: 200 OK` |
| `barcode_hash` | EP: read-only hash | `barcode_hash` | `abc123` | `Proposed, to confirm in Q-VAL-14: 200 OK` |
| `creation_date` | EP: read-only date | `creation_date` | `"2000-01-01"` | `Proposed, to confirm in Q-VAL-14: 200 OK` |
| `in_stock` | EP: read-only total | `in_stock` | `500` | `Proposed, to confirm in Q-VAL-14: 200 OK` |

**Postconditions and cleanup:** one part per row run. Cleanup as `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** if the API rejects the request, the status is still open (Q-VAL-14); the stored value must stay equal to `<before>` either way.

**Duplicate check:** 50 · Review · matches: [API-VAL-106](part-field-validation-create-and-update.md) (50)

**Duplicate judgement:** Keep · Read-only fields on PATCH (R-VAL-11, proposed 200 with value kept) versus wrong-type writable fields on PATCH (API-VAL-106, R-VAL-10, proposed 400). · test-case-reviewer, 2026-10-16

### API-VAL-106: Reference and flag fields of the wrong type are refused on update

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` with `category` as text or the `pk` of a deleted category, or `active` as text, does not change the part. |
| **Requirement** | R-VAL-10, R-VAL-16. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([L2767](../../requirements/openapi-parts.yaml#L2767)), `components.schemas.Part.category` (`type: integer`, [L4122](../../requirements/openapi-parts.yaml#L4122)), `Part.active` (`type: boolean`, [L4112](../../requirements/openapi-parts.yaml#L4112)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Equivalence partitioning (invalid classes: text for integer, reference to a deleted record, text for boolean) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Cat` (the part's category) and category `QA-<suffix> Gone` created with `POST /api/part/category/` as `admin`; `QA-<suffix> Gone` is then deleted with `DELETE /api/part/category/<pk>/` and body `{"delete_parts": false, "delete_child_categories": false}` and its `pk` is `<deleted category pk>`; part `QA-<suffix> Type base` in `QA-<suffix> Cat`, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-08, Q-VAL-13 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Type base", "category": <pk of QA-<suffix> Cat>}` | `201 Created`. Body is valid against `Part`; `category` and `active` (`true`) are recorded. |
| 2 | `PATCH /api/part/<pk from step 1>/` as `engineer` | `{"<row.field>": <row.value>}` | `<row.expected status>`. For a rejected request, the body is `<row.error>`. |
| 3 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. `<row.after>` |

**Data sets**

| Row | Class | field | value | expected status | error | after |
|---|---|---|---|---|---|---|
| `category text` | EP invalid: text for integer | `category` | `"abc"` | `Proposed, to confirm in Q-VAL-13: 400 Bad Request` | `Open: Q-VAL-13 (error body and text)` | `category` is `<pk of QA-<suffix> Cat>` and `active` is `true`: unchanged (R-VAL-10: `category` must be an integer). |
| `category deleted` | EP invalid: reference to a deleted record | `category` | `<deleted category pk>` | `Proposed, to confirm in Q-VAL-13: 400 Bad Request` | `Open: Q-VAL-13 (error body and text)` | Proposed, to confirm in Q-VAL-13: `category` is `<pk of QA-<suffix> Cat>` and `active` is `true` (unchanged). |
| `active text` | EP invalid: text for boolean | `active` | `"maybe"` | `Proposed, to confirm in Q-VAL-13: 400 Bad Request` | `Open: Q-VAL-13 (error body and text)` | `category` is `<pk of QA-<suffix> Cat>` and `active` is `true`: unchanged (R-VAL-10: `active` must be a boolean). |

**Postconditions and cleanup:** one part per row run, in `QA-<suffix> Cat`. Cleanup as `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`), then `DELETE /api/part/category/<pk of QA-<suffix> Cat>/` with `{"delete_parts": false, "delete_child_categories": false}`.

**Notes:** for the `category text` and `active text` rows, the unchanged values in step 3 follow from R-VAL-10 (each field must match its schema type). A deleted category's `pk` is still an integer, so for the `category deleted` row R-VAL-10 states nothing: its rejection and the unchanged `category` are proposed (Q-VAL-13), as in API-VAL-098. The status codes and error bodies are open for every row (Q-VAL-13).

**Duplicate check:** 50 · Review · matches: [API-VAL-105](part-field-validation-create-and-update.md) (50)

**Duplicate judgement:** Keep · Wrong-type reference and flag values on PATCH (R-VAL-10, proposed 400) versus read-only fields on PATCH (API-VAL-105, R-VAL-11, proposed 200). · test-case-reviewer, 2026-10-16

### API-VAL-107: Several invalid fields in one create request

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with an over-long `name`, an over-long `IPN` and a negative `default_expiry` in one body creates no part, and the response shows which fields failed. |
| **Requirement** | R-VAL-01, R-VAL-03, R-VAL-08. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.name` ([L4196](../../requirements/openapi-parts.yaml#L4196)), `Part.IPN` ([L4164](../../requirements/openapi-parts.yaml#L4164)), `Part.default_expiry` ([L4139](../../requirements/openapi-parts.yaml#L4139)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (several invalid fields at once), Equivalence partitioning (invalid classes combined) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix>" + 90 × "x" (101 characters), "IPN": 101 × "i", "default_expiry": -1, "description": "QA-<suffix> multi"}` | No part is created (R-VAL-01). Proposed, to confirm in Q-VAL-08: `400 Bad Request` with one entry each under `name`, `IPN` and `default_expiry`. Open: Q-VAL-08 (status, keys and texts). |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> multi`, `limit=10` | `200 OK`. `count` is `0`. |

**Postconditions and cleanup:** none expected. If a part is created, cleanup as `admin`: find it by the description with `GET /api/part/?search=QA-<suffix>&limit=50`, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** step 2 expects no part because the name alone is over its limit; that outcome is the one rejection the case relies on, with the status proposed.

### API-VAL-108: Unknown key in the create body

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a key that is not a `Part` property creates the part and does not return that key. |
| **Requirement** | R-VAL-10, R-CRUD-01. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), response `components.schemas.Part` ([L4105](../../requirements/openapi-parts.yaml#L4105)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (unknown field in the body) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes |
| **Review** | Draft · Open question: Q-VAL-17 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Unknown key", "qa_unknown": "x"}` | Proposed, to confirm in Q-VAL-17: `201 Created`, body valid against `Part`, with no key `qa_unknown`. Open: Q-VAL-17 (ignored or rejected). |
| 2 | `GET /api/part/` as `engineer` | `search=QA-<suffix> Unknown key`, `limit=10` | `200 OK`. `count` is `Proposed, to confirm in Q-VAL-17: 1`. |

**Postconditions and cleanup:** one part if accepted. Cleanup as `admin`: find it with `GET /api/part/?search=QA-<suffix>&limit=50`, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** the schema defines the properties but not the handling of extra keys.

**Duplicate check:** 53 · Review · matches: [API-VAL-098](part-field-validation-create-and-update.md) (53), [API-VAL-097](part-field-validation-create-and-update.md) (51)

**Duplicate judgement:** Keep · A key that is not a Part property (Q-VAL-17, proposed accepted and not returned) versus wrong values for defined fields (API-VAL-098, API-VAL-097) expected to be refused. · test-case-reviewer, 2026-10-16
