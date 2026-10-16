# Duplicate and uniqueness conflicts: VAL test cases

### API-VAL-124: Duplicate IPN on create with the default setting

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with an `IPN` already used by another part (different `name`) shows whether the duplicate IPN is accepted with the instance's default setting. |
| **Requirement** | R-VAL-03, R-Part-12 ([part-views.md#L30](../../requirements/docs/part-views.md#L30): "The IPN field is not required"; no uniqueness rule for IPN). Index Not in docs #1, Not in schema #2. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.IPN` ([L4164](../../requirements/openapi-parts.yaml#L4164)). Findings F-05. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate IPN), What-if business scenario (two parts given the same part number) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: duplicate-IPN setting at its default [open: Q-VAL-25, the docs name no such setting; findings F-05 observed it on]; Data: part `QA-<suffix> IPN Base` with IPN `QA-<suffix>-IPN`, created in step 1 by `admin`; Pre-steps: get `engineer`'s and `admin`'s tokens with `GET /api/user/me/token/` (basic auth) and send each as `Authorization: Token <token>`. |
| **Automation** | Partial: the expected outcome is only proposed (Q-VAL-25). |
| **Review** | Draft · Open question: Q-VAL-25 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin` | `{"name": "QA-<suffix> IPN Base", "IPN": "QA-<suffix>-IPN", "description": "QA-<suffix> ipn base"}` | `201 Created`. Body is valid against `Part`; `IPN` equals the payload. |
| 2 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> IPN Other", "IPN": "QA-<suffix>-IPN", "description": "QA-<suffix> ipn other"}` | Proposed, to confirm in Q-VAL-25: `201 Created`; the duplicate IPN is accepted (the brief treats it as negative, the docs state no IPN uniqueness, findings F-05 saw it accepted). Open: Q-VAL-25 (whether the API rejects it by default, and the error body). |
| 3 | `GET /api/part/` as `engineer` | `search=QA-<suffix>-IPN`, `limit=10` | `200 OK`. Proposed, to confirm in Q-VAL-25: `count` is `2`. |

**Postconditions and cleanup:** two parts if step 2 was accepted. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** duplicate IPN alone is not the exact-duplicate case of API-VAL-091 (name, IPN and revision all equal). The brief lists duplicate IPN as a negative case; the docs do not.

**Duplicate check:** 69 · Review · matches: [API-VAL-125](duplicate-and-uniqueness-conflicts.md) (69)

**Duplicate judgement:** Keep · Differs from API-VAL-125 in settings and expected outcome: duplicate-IPN setting left at its default (proposed 201, duplicate accepted) versus switched off by `admin` (proposed 400, refused). · test-case-reviewer, 2026-10-16

### API-VAL-125: Duplicate IPN on create with duplicate IPNs disabled

| Field | Value |
|---|---|
| **Summary** | With the instance setting that forbids duplicate IPNs switched off by `admin`, `POST /api/part/` with an IPN already used by another part shows whether it is refused. |
| **Requirement** | R-VAL-03, R-Part-12 ([part-views.md#L30](../../requirements/docs/part-views.md#L30)). Index Not in docs #1, Not in schema #2. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.IPN` ([L4164](../../requirements/openapi-parts.yaml#L4164)). Findings F-05 (setting `PART_ALLOW_DUPLICATE_IPN`). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Decision table (duplicate IPN allowed x IPN already used), Error guessing (duplicate IPN) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: the setting that allows duplicate IPNs = off [open: Q-VAL-25, name and API endpoint not in the docs or the schema slice; findings F-05 names `PART_ALLOW_DUPLICATE_IPN`], changed by `admin`; Data: part `QA-<suffix> IPN Base` with IPN `QA-<suffix>-IPN`, created in step 1 by `admin`; Pre-steps: get `engineer`'s and `admin`'s tokens with `GET /api/user/me/token/` (basic auth) and send each as `Authorization: Token <token>`; switch the setting off as `admin` [open: Q-VAL-25, request]. |
| **Automation** | Partial: the setting endpoint is outside the schema slice and the error is not known. |
| **Review** | Draft · Open question: Q-VAL-25 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin` | `{"name": "QA-<suffix> IPN Base", "IPN": "QA-<suffix>-IPN", "description": "QA-<suffix> ipn base"}` | `201 Created`. Body is valid against `Part`; `IPN` equals the payload. |
| 2 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> IPN Other", "IPN": "QA-<suffix>-IPN", "description": "QA-<suffix> ipn other"}` | Proposed, to confirm in Q-VAL-25: `400 Bad Request`, error under `IPN`; the part is not created. Open: Q-VAL-25 (status code, error key and text). |
| 3 | `GET /api/part/` as `engineer` | `search=QA-<suffix>-IPN`, `limit=10` | `200 OK`. Proposed, to confirm in Q-VAL-25: `count` is `1`. |
| 4 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> IPN Empty", "description": "QA-<suffix> ipn empty"}` (no IPN) | `201 Created`. The IPN is not required (R-Part-12), so the part is created. Open: Q-VAL-25 (whether an empty IPN is exempt from the duplicate check). |

**Postconditions and cleanup:** two or three parts. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`). Restore the setting to its original value as `admin` [open: Q-VAL-25, request].

**Notes:** the setting changes the whole instance; record the original value before changing it and restore it even when the case fails.

**Duplicate check:** 69 · Review · matches: [API-VAL-124](duplicate-and-uniqueness-conflicts.md) (69)

**Duplicate judgement:** Keep · Differs from API-VAL-124 in settings and expected outcome: duplicate IPNs disallowed by `admin` (proposed 400) versus the default setting (proposed 201), and adds the empty-IPN create under the stricter setting. · test-case-reviewer, 2026-10-16

### API-VAL-126: Revision code must be unique among the revisions of one original part on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with a `revision_of` and a `revision` code already used by another revision of the same original is refused; the same code under another original, and a new code, are compared. |
| **Requirement** | R-REV-07 ([part-revision.md#L37](../../requirements/docs/part-revision.md#L37): "A part cannot have two revisions with the same revision number. Each revision (of a given part) must have a unique revision code."), R-REL-10, R-VAL-07. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.revision` ([L4207](../../requirements/openapi-parts.yaml#L4207)), `Part.revision_of` ([L4212](../../requirements/openapi-parts.yaml#L4212)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Decision table (same original or other x same code or new code), Error guessing (letter case of the code) |
| **Priority** | P1 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revision settings (`PART_ENABLE_REVISION`, `PART_REVISION_ASSEMBLY_ONLY`) = [open: Q-REL-08, names and defaults not rendered in the docs, Doc issue 8]; Data: originals `QA-<suffix> Orig A` and `QA-<suffix> Orig C` (`assembly` `true`) and revision `QA-<suffix> Orig A` with `revision` `B` and `revision_of` = Orig A, created in step 1 by `admin`; Pre-steps: get `engineer`'s and `admin`'s tokens with `GET /api/user/me/token/` (basic auth) and send each as `Authorization: Token <token>`. |
| **Automation** | Partial: status code and error body are not known (Q-VAL-26), revision settings open (Q-REL-08). |
| **Review** | Draft · Open question: Q-VAL-26, Q-REL-08, Q-REV-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin`, three times | `{"name": "QA-<suffix> Orig A", "assembly": true}`, `{"name": "QA-<suffix> Orig C", "assembly": true}`, then `{"name": "QA-<suffix> Orig A", "assembly": true, "revision": "B", "revision_of": <pk of Orig A>}` | `201 Created` each, bodies valid against `Part`; the third has `revision` `B` and `revision_of` equal to the Orig A `pk` (R-REV-01). Open: Q-REL-08 (whether the default revision settings allow it). The `pk` of each is recorded. |
| 2 | `POST /api/part/` as `engineer` | `{"name": <row.name>, "assembly": true, "revision": <row.revision>, "revision_of": <row.revision_of>}` | `<row.expected status>`. For a rejected request the body is `<row.error>`. |
| 3 | `GET /api/part/` as `engineer` | `search=QA-<suffix> Orig`, `limit=50` | `200 OK`. `count` is `<row.count>`: the three parts from step 1, plus the step 2 part if one was created. |

**Data sets**

| Row | Class | name | revision | revision_of | expected status | error | count |
|---|---|---|---|---|---|---|---|
| `same code same original` | Decision table: same original, same code | `QA-<suffix> Orig A` | `B` | `<pk of Orig A>` | `Proposed, to confirm in Q-VAL-26: 400 Bad Request` | `Open: Q-VAL-26 (error key and text). The part is not created (R-REV-07).` | `3` |
| `new code same original` | Decision table: same original, new code | `QA-<suffix> Orig A` | `C` | `<pk of Orig A>` | `Proposed, to confirm in Q-VAL-26: 201 Created` | None | `Proposed, to confirm in Q-VAL-26: 4` |
| `same code other original` | Decision table: other original, same code | `QA-<suffix> Orig C` | `B` | `<pk of Orig C>` | `Proposed, to confirm in Q-VAL-26: 201 Created` | None | `Proposed, to confirm in Q-VAL-26: 4` |
| `letter case differs` | Error guessing: `b` against `B` | `QA-<suffix> Orig A` | `b` | `<pk of Orig A>` | `Open: Q-REV-06 (case sensitivity of the comparison)` | `Open: Q-REV-06, Q-VAL-26 (error key and text)` | `Open: Q-REV-06 (count)` |

**Postconditions and cleanup:** three to four parts. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`), revisions first.

**Notes:** each row starts from fresh step 1 data. Only the `same code same original` outcome is stated (R-REV-07); the other rows are not inferred from it (guardrail: never infer the opposite). A revision keeps the name of its original (part-revision.md#L23, a revision is a part); the combined name, IPN and revision rule is Q-VAL-03.

**Duplicate check:** 50 · Review · matches: [API-VAL-127](duplicate-and-uniqueness-conflicts.md) (50)

**Duplicate judgement:** Keep · Differs from API-VAL-127 in operation and starting state: a new revision created with a used code (`POST` with `revision_of`, incl. the other-original and letter-case rows) versus an existing revision relabelled (`PATCH`, incl. the own-code row). · test-case-reviewer, 2026-10-16

### API-VAL-127: Revision code conflict when a revision is edited

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` changing the `revision` of one revision to the code of a sibling revision of the same original shows whether the change is refused, compared with an unused code and with the revision's own code. |
| **Requirement** | R-REV-07 ([part-revision.md#L37](../../requirements/docs/part-revision.md#L37)), R-REL-10. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([L2767](../../requirements/openapi-parts.yaml#L2767)), `components.schemas.PatchedPart.revision`. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Decision table (sibling's code, unused code, own code), State transition (revision code changed), What-if business scenario (a revision relabelled after another exists) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `engineer` (manage parts); Settings: revision settings = [open: Q-REL-08]; Data: original `QA-<suffix> Orig A` (`assembly` `true`) and two revisions of it, `QA-<suffix> Orig A` with `revision` `B` and with `revision` `C`, created in step 1 by `admin`; Pre-steps: get `engineer`'s and `admin`'s tokens with `GET /api/user/me/token/` (basic auth) and send each as `Authorization: Token <token>`. |
| **Automation** | Partial: status code and error body are not known (Q-VAL-26, Q-VAL-27). |
| **Review** | Draft · Open question: Q-VAL-26, Q-VAL-27, Q-REL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin`, three times | `{"name": "QA-<suffix> Orig A", "assembly": true}`, then `{"name": "QA-<suffix> Orig A", "assembly": true, "revision": "B", "revision_of": <pk of Orig A>}` and the same with `"revision": "C"` | `201 Created` each, bodies valid against `Part`. The `pk` of the revisions B and C are recorded. Open: Q-REL-08. |
| 2 | `PATCH /api/part/<pk of revision C>/` as `engineer` | `{"revision": <row.revision>}` | `<row.expected status>`. For a rejected request the body is `<row.error>`. |
| 3 | `GET /api/part/<pk of revision C>/` as `engineer` | None | `200 OK`. `revision` is `<row.revision after>`. |

**Data sets**

| Row | Class | revision | expected status | error | revision after |
|---|---|---|---|---|---|
| `sibling's code` | Decision table: code of another revision of the same original | `B` | `Proposed, to confirm in Q-VAL-26: 400 Bad Request` | `Open: Q-VAL-26 (error key and text). The change is not applied (R-REV-07).` | `C` |
| `unused code` | Decision table: code not used by a sibling | `D` | `Proposed, to confirm in Q-VAL-27: 200 OK` | None | `Proposed, to confirm in Q-VAL-27: D` |
| `own code unchanged` | Decision table: own current code | `C` | `Proposed, to confirm in Q-VAL-27: 200 OK` | None | `Proposed, to confirm in Q-VAL-27: C` |

**Postconditions and cleanup:** three parts. Cleanup as `admin`: for each of the three, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`), revisions first.

**Notes:** each row starts from fresh step 1 data. The own-code row checks that the part is not counted as its own duplicate.

**Duplicate check:** 50 · Review · matches: [API-VAL-126](duplicate-and-uniqueness-conflicts.md) (50)

**Duplicate judgement:** Keep · Differs from API-VAL-126 in operation and starting state: an existing revision's code changed with `PATCH` (sibling's, unused and own code) versus a new revision created with `POST`. · test-case-reviewer, 2026-10-16

### API-VAL-128: Updating a part so that name, IPN and revision match another part

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/{id}/` setting `name` to the name of another part shows whether the update is refused when IPN and revision also match, and accepted when the IPN differs or the value is the part's own. |
| **Requirement** | R-VAL-01, R-VAL-03, R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32): "The Part name is a simple (unique) text label"), R-CRUD-04. Doc issue 2, findings F-04. Schema: `requirements/openapi-parts.yaml PATCH /api/part/{id}/` ([L2767](../../requirements/openapi-parts.yaml#L2767)), `components.schemas.PatchedPart.name`. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Decision table (name equal x IPN equal or different x own value), What-if business scenario (a part renamed to an existing part's name) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: parts `QA-<suffix> Rename Base` (IPN `QA-<suffix>-R1`), `QA-<suffix> Rename Same IPN` (IPN `QA-<suffix>-R1`) and `QA-<suffix> Rename Other IPN` (IPN `QA-<suffix>-R2`), created in step 1 by `admin`; Pre-steps: get `engineer`'s and `admin`'s tokens with `GET /api/user/me/token/` (basic auth) and send each as `Authorization: Token <token>`. |
| **Automation** | Partial: the combined rule, status and body are open (Q-VAL-03, Q-VAL-27). |
| **Review** | Draft · Open question: Q-VAL-03, Q-VAL-27 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin`, three times | `{"name": "QA-<suffix> Rename Base", "IPN": "QA-<suffix>-R1"}`, `{"name": "QA-<suffix> Rename Same IPN", "IPN": "QA-<suffix>-R1"}`, `{"name": "QA-<suffix> Rename Other IPN", "IPN": "QA-<suffix>-R2"}` | `201 Created` each. Bodies are valid against `Part`; the `pk` of each is recorded. Open: Q-VAL-25 (whether the shared IPN of the first two is accepted by default). |
| 2 | `PATCH /api/part/<pk of <row.target>>/` as `engineer` | `{"name": "QA-<suffix> Rename Base"}` | `<row.expected status>`. For a rejected request the body is `<row.error>`. |
| 3 | `GET /api/part/<pk of <row.target>>/` as `engineer` | None | `200 OK`. `name` is `<row.name after>`. |

**Data sets**

| Row | Class | target | expected status | error | name after |
|---|---|---|---|---|---|
| `same name same IPN` | Decision table: name and IPN equal to another part | `Rename Same IPN` | `Proposed, to confirm in Q-VAL-27: 400 Bad Request` | `Open: Q-VAL-27 (error key and text)` | `Proposed, to confirm in Q-VAL-27: QA-<suffix> Rename Same IPN` |
| `same name other IPN` | Decision table: name equal, IPN differs | `Rename Other IPN` | `Proposed, to confirm in Q-VAL-27: 200 OK` | None | `Proposed, to confirm in Q-VAL-27: QA-<suffix> Rename Base` |
| `own name unchanged` | Decision table: the part's own value | `Rename Base` | `Proposed, to confirm in Q-VAL-27: 200 OK` | None | `QA-<suffix> Rename Base` |

**Postconditions and cleanup:** three parts. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix> Rename&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** each row starts from fresh step 1 data. The Expected `name after` of `own name unchanged` is a fact only for the stored value: the part already has that name.

### API-VAL-129: Duplicate action with the name of the original part

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` with the write-only `duplicate` option and the same `name` as the original shows whether the copy is refused when the original has no IPN, and accepted when the original has an IPN that the copy does not take. |
| **Requirement** | R-VAL-12, R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32)), R-CRUD-14, `open-question_CRUD.md Q-CRUD-06` (answered: no field value of the original is copied; IPN takes its default). Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.duplicate` ([L4343](../../requirements/openapi-parts.yaml#L4343)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Decision table (original has IPN or not), What-if business scenario (a user copies a part and forgets to change the name) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: original part created in step 1 by `admin`; Pre-steps: get `engineer`'s and `admin`'s tokens with `GET /api/user/me/token/` (basic auth) and send each as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome depends on the combined rule (Q-VAL-03, Q-VAL-31). |
| **Review** | Draft · Open question: Q-VAL-03, Q-VAL-31 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin` | `{"name": "QA-<suffix> Copy Source", "IPN": <row.original IPN>}` (the `IPN` key is left out when the row says *(left out)*) | `201 Created`. Body is valid against `Part`; the `pk` is recorded. |
| 2 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Copy Source", "duplicate": {"original": <pk from step 1>}}` | `<row.expected status>`. For a rejected request the body is `<row.error>`. For a `201`, the body has no `duplicate` key (Q-CRUD-06) and the original is unchanged. |
| 3 | `GET /api/part/` as `engineer` | `search=QA-<suffix> Copy Source`, `limit=10` | `200 OK`. `count` is `<row.count>`. |

**Data sets**

| Row | Class | original IPN | expected status | error | count |
|---|---|---|---|---|---|
| `original without IPN` | Decision table: name, IPN (both empty) and revision equal | *(left out)* | `Proposed, to confirm in Q-VAL-31: 400 Bad Request` | `Open: Q-VAL-31 (error key and text)` | `Proposed, to confirm in Q-VAL-31: 1` |
| `original with IPN` | Decision table: name equal, copy has an empty IPN (Q-CRUD-06) | `QA-<suffix>-COPY` | `Proposed, to confirm in Q-VAL-03: 201 Created` | None | `Proposed, to confirm in Q-VAL-03: 2` |

**Postconditions and cleanup:** one or two parts. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; for each, `PATCH /api/part/<pk>/` with `{"active": false}`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** each row starts from fresh step 1 data. Whether `duplicate` skips the uniqueness check is not stated (Q-VAL-31).

### API-VAL-130: Create a part with the name, IPN and revision of an inactive part

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/` repeating the name and IPN of a part that was set inactive shows whether an inactive part still counts as a duplicate. |
| **Requirement** | R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32)), R-VAL-01, R-CRUD-11. Doc issue 2. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `components.schemas.Part.active`. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | State transition (active to inactive, then duplicate create), What-if business scenario (a retired part number is reused) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: part `QA-<suffix> Retired` with IPN `QA-<suffix>-RET`, created and set inactive in steps 1 and 2 by `admin`; Pre-steps: get `engineer`'s and `admin`'s tokens with `GET /api/user/me/token/` (basic auth) and send each as `Authorization: Token <token>`. |
| **Automation** | Partial: outcome only proposed (Q-VAL-28). |
| **Review** | Draft · Open question: Q-VAL-28, Q-VAL-03 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin` | `{"name": "QA-<suffix> Retired", "IPN": "QA-<suffix>-RET"}` | `201 Created`. Body is valid against `Part`; `active` is `true` (R-CRUD-11). The `pk` is recorded. |
| 2 | `PATCH /api/part/<pk>/` as `admin` | `{"active": false}` | `200 OK`. `active` is `false`. |
| 3 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Retired", "IPN": "QA-<suffix>-RET"}` | Proposed, to confirm in Q-VAL-28: `400 Bad Request`, the inactive part counts as a duplicate and the part is not created. Open: Q-VAL-28 (whether inactive parts are checked; Q-VAL-03 for the error body). |
| 4 | `GET /api/part/` as `engineer` | `search=QA-<suffix> Retired`, `limit=10`, `active=false` | `200 OK`. `count` is `1`: only the inactive part from steps 1 and 2 is listed, so step 3 created no inactive part. |

**Postconditions and cleanup:** one or two parts. Cleanup as `admin`: find them with `GET /api/part/?search=QA-<suffix>&limit=50`; set every active one inactive with `PATCH`, then `DELETE /api/part/<pk>/` (`204`).

**Notes:** step 4 lists inactive parts only, so a second, active part from step 3 would not be counted; list again without the filter if step 3 returned `201`.

### API-VAL-131: Two identical creates sent at the same time

| Field | Value |
|---|---|
| **Summary** | Two identical `POST` requests sent at the same moment (a double submit) show whether exactly one part or category is created. |
| **Requirement** | R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32)), R-VAL-13, R-CRUD-01, R-CRUD-06. Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)) and `POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)). UI counterpart: Q-Part-20. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (double submit), What-if business scenario (a user clicks twice) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: None; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the outcome is only proposed and a race may be intermittent (Q-VAL-29). |
| **Review** | Draft · Open question: Q-VAL-29 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST <row.endpoint>` as `engineer`, sent twice without waiting for the first response | `<row.payload>` (identical in both requests) | Proposed, to confirm in Q-VAL-29: one response is `<row.accepted status>` and the other is `<row.other status>`. Open: Q-VAL-29 (whether both are accepted, and the error body of the other). |
| 2 | `GET <row.list endpoint>` as `engineer` | `search=<row.search>`, `limit=10` | `200 OK`. Proposed, to confirm in Q-VAL-29: `count` is `1`. |

**Data sets**

| Row | Class | endpoint | payload | list endpoint | search | accepted status | other status |
|---|---|---|---|---|---|---|---|
| `part` | Error guessing: double submit of a part | `/api/part/` | `{"name": "QA-<suffix> Twice", "description": "QA-<suffix> twice"}` | `/api/part/` | `QA-<suffix> Twice` | `Proposed, to confirm in Q-VAL-29: 201 Created` | `Proposed, to confirm in Q-VAL-29: 400 Bad Request` |
| `category` | Error guessing: double submit of a category | `/api/part/category/` | `{"name": "QA-<suffix> Twice Cat"}` | `/api/part/category/` | `QA-<suffix> Twice Cat` | `Proposed, to confirm in Q-VAL-29: 201 Created` | `Proposed, to confirm in Q-VAL-29: 400 Bad Request` |

**Postconditions and cleanup:** one or two records per row. Cleanup as `admin`: parts by `PATCH` `{"active": false}` then `DELETE /api/part/<pk>/` (`204`); categories by `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** the part duplicate rule itself is unconfirmed (Q-VAL-03), and category name uniqueness is Q-VAL-20; this case depends on both.

### API-VAL-132: Moving a category under a parent that already holds a category with the same name

| Field | Value |
|---|---|
| **Summary** | `PATCH /api/part/category/{id}/` changing `parent` shows whether the move is refused when the target parent (or the top level) already holds a category with the same `name`, and accepted when it does not. |
| **Requirement** | R-VAL-13 (uniqueness among sibling categories not stated), R-REL-06, R-CRUD-09. Schema: `requirements/openapi-parts.yaml PATCH /api/part/category/{id}/` ([L1370](../../requirements/openapi-parts.yaml#L1370)), `components.schemas.PatchedCategory.parent`. |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Decision table (target parent holds same name or not, top level or not), What-if business scenario (a category reorganised into a branch that has its twin) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: categories `QA-<suffix> Parent A`, `QA-<suffix> Parent B`, `QA-<suffix> Parent C` (all top level) and `QA-<suffix> Mover` under A, under B and at the top level, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: depends on the sibling rule (Q-VAL-20, Q-VAL-30). |
| **Review** | Draft · Open question: Q-VAL-20, Q-VAL-30 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer`, six times | Parents A, B and C: `{"name": "QA-<suffix> Parent A"}` and likewise B, C; then `{"name": "QA-<suffix> Mover", "parent": <pk of A>}`, `{"name": "QA-<suffix> Mover", "parent": <pk of B>}` and `{"name": "QA-<suffix> Mover"}` | `201 Created` for the parents and for the first Mover. Bodies are valid against `Category`. The second and third Mover: Proposed, to confirm in Q-VAL-20: `201 Created` (the same name under another parent or at the top level is accepted). The `pk` of each is recorded. |
| 2 | `PATCH /api/part/category/<pk of the Mover under B>/` as `engineer` | `{"parent": <row.parent>}` | `<row.expected status>`. For a rejected request the body is `<row.error>`. |
| 3 | `GET /api/part/category/<pk of the Mover under B>/` as `engineer` | None | `200 OK`. `parent` is `<row.parent after>`. |

**Data sets**

| Row | Class | parent | expected status | error | parent after |
|---|---|---|---|---|---|
| `parent holds same name` | Decision table: target holds the same name | `<pk of A>` | `Proposed, to confirm in Q-VAL-30: 400 Bad Request` | `Open: Q-VAL-30 (error key and text)` | `Proposed, to confirm in Q-VAL-30: <pk of B>` |
| `top level holds same name` | Decision table: top level holds the same name | `null` | `Proposed, to confirm in Q-VAL-30: 400 Bad Request` | `Open: Q-VAL-30 (error key and text)` | `Proposed, to confirm in Q-VAL-30: <pk of B>` |
| `parent without same name` | Decision table: no clash | `<pk of C>` | `Proposed, to confirm in Q-VAL-30: 200 OK` | None | `Proposed, to confirm in Q-VAL-30: <pk of C>` |

**Postconditions and cleanup:** six categories. Cleanup as `admin`: find them with `GET /api/part/category/?search=QA-<suffix>&limit=50`; delete the Movers first, then the parents, each with `DELETE /api/part/category/<pk>/` and `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** each row starts from fresh step 1 data. Rename on update is API-VAL-123; this case changes the parent, not the name.

### API-VAL-133: Duplicate top-level category name on create

| Field | Value |
|---|---|
| **Summary** | `POST /api/part/category/` with the `name` of an existing top-level category, with `parent` left out or `null`, shows whether the duplicate is refused. |
| **Requirement** | R-VAL-13 (uniqueness among sibling categories not stated), R-REL-06 (`parent` nullable: top-level), R-CRUD-06. Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `components.schemas.Category.name` ([L3517](../../requirements/openapi-parts.yaml#L3517)), `Category.parent` ([L3537](../../requirements/openapi-parts.yaml#L3537)). |
| **Area** | VAL |
| **Type** | Negative |
| **Technique** | Error guessing (duplicate at top level), Equivalence partitioning (invalid class: duplicate; parent absent, parent null) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: top-level category `QA-<suffix> Top`, created in step 1; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the rule is only proposed (Q-VAL-20, Q-VAL-30). |
| **Review** | Draft · Open question: Q-VAL-20, Q-VAL-30 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Top"}` | `201 Created`. Body is valid against `Category`; `parent` is `null`. |
| 2 | `POST /api/part/category/` as `engineer` | `{"name": "QA-<suffix> Top"}` plus `"parent": null` unless the row says *(left out)* | `<row.expected status>`. For a rejected request the body is `<row.error>`. |
| 3 | `GET /api/part/category/` as `engineer` | `search=QA-<suffix> Top`, `limit=10` | `200 OK`. `count` is `<row.count>`. |

**Data sets**

| Row | Class | parent | expected status | error | count |
|---|---|---|---|---|---|
| `parent left out` | EP invalid: duplicate, parent absent | *(left out)* | `Proposed, to confirm in Q-VAL-30: 400 Bad Request` | `Open: Q-VAL-30 (error key and text)` | `Proposed, to confirm in Q-VAL-30: 1` |
| `parent null` | EP invalid: duplicate, parent null | `null` | `Proposed, to confirm in Q-VAL-30: 400 Bad Request` | `Open: Q-VAL-30 (error key and text)` | `Proposed, to confirm in Q-VAL-30: 1` |

**Postconditions and cleanup:** one to two categories. Cleanup as `admin`: find them with `GET /api/part/category/?search=QA-<suffix>&limit=50`; `DELETE /api/part/category/<pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`) for each.

**Notes:** API-VAL-115 covers duplicates under a named parent; this case covers the top level, where `parent` is empty.

**Duplicate check:** 53 · Review · matches: [API-VAL-115](category-field-validation-create-and-update.md) (53), [API-VAL-113](category-field-validation-create-and-update.md) (50)

**Duplicate judgement:** Keep · Differs from API-VAL-115 in starting state (duplicate at the top level with `parent` absent or `null`, Q-VAL-30, versus under a named parent, Q-VAL-20) and from API-VAL-113 in rule and outcome (name uniqueness versus wrong-type fields). · test-case-reviewer, 2026-10-16

### API-VAL-134: Reuse a part name and IPN after the part is deleted

| Field | Value |
|---|---|
| **Summary** | After a part is set inactive and deleted, `POST /api/part/` with the same name and IPN shows whether the combination is free again. |
| **Requirement** | R-Part-13 ([part-views.md#L32](../../requirements/docs/part-views.md#L32)), R-CRUD-05, `open-question_CRUD.md Q-CRUD-02` (answered: inactive first, then `204`), `Q-CRUD-01` (deleted part returns `404`). Schema: `requirements/openapi-parts.yaml POST /api/part/` ([L747](../../requirements/openapi-parts.yaml#L747)), `DELETE /api/part/{id}/` ([L2803](../../requirements/openapi-parts.yaml#L2803)). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | State transition (created, deleted, created again), What-if business scenario (a part removed by mistake is recreated) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: None; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the final step is only proposed (Q-VAL-28). |
| **Review** | Draft · Open question: Q-VAL-28 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `admin` | `{"name": "QA-<suffix> Reborn", "IPN": "QA-<suffix>-RB"}` | `201 Created`. Body is valid against `Part`; the `pk` is recorded. |
| 2 | `PATCH /api/part/<pk>/` as `admin` | `{"active": false}` | `200 OK`. `active` is `false`. |
| 3 | `DELETE /api/part/<pk>/` as `admin` | None | `204 No Content`. The body is empty (Q-CRUD-02). |
| 4 | `GET /api/part/<pk>/` as `admin` | None | `404 Not Found`. Body is `{"detail": "No Part matches the given query."}` (Q-CRUD-01). |
| 5 | `POST /api/part/` as `admin` | `{"name": "QA-<suffix> Reborn", "IPN": "QA-<suffix>-RB"}` | Proposed, to confirm in Q-VAL-28: `201 Created`; a deleted part does not count as a duplicate. Body is valid against `Part` with a new `pk`. Open: Q-VAL-28 (whether deleted parts are excluded). |

**Postconditions and cleanup:** one part. Cleanup as `admin`: `PATCH /api/part/<new pk>/` with `{"active": false}`, `DELETE /api/part/<new pk>/` (`204`).

**Notes:** a deleted record is removed, but the docs and the schema do not state that the name becomes free.

### API-VAL-135: Reuse a category name after the category is deleted

| Field | Value |
|---|---|
| **Summary** | After a category is deleted, `POST /api/part/category/` with the same `name` and `parent` shows whether the name is free again. |
| **Requirement** | R-VAL-13 (uniqueness among sibling categories not stated), R-CRUD-10, `open-question_CRUD.md Q-CRUD-03` (answered: both flags required; `204`), `Q-CRUD-01` (deleted category returns `404`). Schema: `requirements/openapi-parts.yaml POST /api/part/category/` ([L947](../../requirements/openapi-parts.yaml#L947)), `DELETE /api/part/category/{id}/` ([L1406](../../requirements/openapi-parts.yaml#L1406)). |
| **Area** | VAL |
| **Type** | Positive |
| **Technique** | State transition (created, deleted, created again), What-if business scenario (a category removed by mistake is recreated) |
| **Priority** | P3 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: None; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the final step is only proposed (Q-VAL-30). |
| **Review** | Draft · Open question: Q-VAL-30 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/category/` as `admin` | `{"name": "QA-<suffix> Reborn Cat"}` | `201 Created`. Body is valid against `Category`; the `pk` is recorded. |
| 2 | `DELETE /api/part/category/<pk>/` as `admin` | `{"delete_parts": false, "delete_child_categories": false}` | `204 No Content` (Q-CRUD-03). |
| 3 | `GET /api/part/category/<pk>/` as `admin` | None | `404 Not Found`. Body is `{"detail": "No PartCategory matches the given query."}` (Q-CRUD-01). |
| 4 | `POST /api/part/category/` as `admin` | `{"name": "QA-<suffix> Reborn Cat"}` | Proposed, to confirm in Q-VAL-30: `201 Created`; a deleted category does not block the name. Body is valid against `Category` with a new `pk`. Open: Q-VAL-30 (whether deleted categories are excluded). |

**Postconditions and cleanup:** one category. Cleanup as `admin`: `DELETE /api/part/category/<new pk>/` with `{"delete_parts": false, "delete_child_categories": false}` (`204`).

**Notes:** None
