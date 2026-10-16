# Review: Part field validation on create and update (API), 2026-10-16

**Cases reviewed:** API-VAL-092, API-VAL-093, API-VAL-094, API-VAL-095, API-VAL-096, API-VAL-097, API-VAL-098, API-VAL-099, API-VAL-100, API-VAL-101, API-VAL-102, API-VAL-103, API-VAL-104, API-VAL-105, API-VAL-106, API-VAL-107, API-VAL-108 (all in [part-field-validation-create-and-update.md](../API_Field_Validation/part-field-validation-create-and-update.md)) · **Verdict:** Changes required

## Coverage

`coverage_check.py --area VAL --file test-cases/API_Field_Validation/part-field-validation-create-and-update.md`: Rules: 18 · covered: 14 · not cited by any case: 4 (R-VAL-13, R-VAL-14, R-VAL-15, R-VAL-17). Exit 0: no unknown rule ID.

| Rule | Cases | Gap / Out of scope / Covered | Depth issues |
|---|---|---|---|
| R-VAL-01 | 103, 104, 107 | Covered (create depth is in API-VAL-087 to 091, name functionality) | PUT/PATCH rows reuse Q-VAL-01/02, which ask about `POST` only (Q4). |
| R-VAL-02 | 092, 094, 104 | Covered | No `maxLength - 1` row (F5). |
| R-VAL-03 | 092, 094, 104, 107 | Covered | No `maxLength - 1` row (F5); default `''` when not sent is not tested (R-CRUD-12 is cited by 094 but no row omits the key) (F6). On PATCH: no IPN on-limit row (F12). |
| R-VAL-04 | 092, 094, 104 | Covered | No `maxLength - 1` row; no keywords length row on PATCH (F5, F12). |
| R-VAL-05 | 094, 095, 104 | Covered | No 1999-character row (F5). Inventory-stated rejection text kept as proposed (F8). |
| R-VAL-06 | 093, 094 | Covered | The on-limit row (`20 × u`) is not a unit, so the limit cannot be judged apart from Q-VAL-12 (F9). |
| R-VAL-07 | 093, 094 | Covered | No `maxLength - 1` row (F5). |
| R-VAL-08 | 096, 104, 107 | Covered | No `maximum - 1` row (F5). |
| R-VAL-09 | 097 | Covered | "Default 0" is not tested: no row leaves the fields out (F6). |
| R-VAL-10 | 096, 097, 098, 106, 108 | Covered | `default_location` and `revision_of`, named in the rule, have no row (F7). |
| R-VAL-11 | 099, 105 | Covered | `category_name`, `starred`, `thumbnail` and pricing figures not exercised (Minor, F20). |
| R-VAL-12 | 100 | Covered | Only two of five write-only fields are sent (Minor, F19). |
| R-VAL-13 | none | Out of scope: Category create validation (separate Category functionality). | |
| R-VAL-14 | none | Out of scope: Category field limits. | |
| R-VAL-15 | none | Out of scope: Category read-only fields. | |
| R-VAL-16 | 102, 103, 104, 105, 106 | Covered (`PatchedPart` half; `PatchedCategory` half out of scope) | |
| R-VAL-17 | none here; API-VAL-090 covers create (name functionality) | **Gap** for update: no `PUT`/`PATCH /api/part/{id}/` case with `application/x-www-form-urlencoded` or `multipart/form-data` (F1). | |
| R-VAL-18 | 101 | Covered | |

404 standing rule: the `{id}` operations under test are `PUT` and `PATCH`; `GET`/`DELETE` of `/api/part/{id}/` are used only as checks, and their 404 cases exist in CRUD (API-CRUD-009, API-CRUD-023). Negative cases exist.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| F1 | Major | R-VAL-17 | Coverage (gap) | Update bodies as form-urlencoded and multipart are stated as accepted, but no case sends `PUT` or `PATCH` in those formats. API-VAL-090 covers `POST` only. | R-VAL-17; [openapi-parts.yaml#L2741-L2751](../../requirements/openapi-parts.yaml#L2741), [#L2778-L2788](../../requirements/openapi-parts.yaml#L2778) | Rerun the creator for R-VAL-17 on update (data-driven, content type as a column). |
| F2 | **Blocker** | API-VAL-106 | No assumptions | Step 3 states as fact that `category` and `active` are unchanged for every row, including `category deleted`. A deleted category's `pk` is still an integer, so R-VAL-10 (type) does not state its rejection; Q-VAL-13 proposes it. The case's own Notes say step 3 is proposed, contradicting the step. API-VAL-098 correctly marks the same row as proposed. | R-VAL-10; Q-VAL-13; Notes of API-VAL-106 | Edit step 3: for the `category deleted` row, `Proposed, to confirm in Q-VAL-13: unchanged` (add an `after` column), keep the type-mismatch rows as fact, and align the Notes. |
| F3 | Major | API-VAL-098 | Rule outcome stated | `count` is `Proposed, to confirm in Q-VAL-13: 0` on the text, decimal and wrong-boolean rows, although R-VAL-10 says each field "must match its schema type", so "no part created" is the rule's outcome (as API-VAL-096 and API-VAL-097 treat it). Only the `category deleted` row is truly proposed. | R-VAL-10; [openapi-parts.yaml#L4122](../../requirements/openapi-parts.yaml#L4122), [#L4112](../../requirements/openapi-parts.yaml#L4112) | Edit: `count` `0` as fact on the type rows; keep proposed on `category deleted`. |
| F4 | Major | API-VAL-104 | Rule outcome stated | `after` on the rejected rows (`name over limit`, `description over limit`, `IPN over limit`, `link not a URL`, `default_expiry below minimum`) is only `Proposed`; the cited rules state the limits (max 100/250/100, URI, minimum 0), so the out-of-limit value is not stored. API-VAL-092/096 state `count 0` as fact for the same limits on create. The Notes call it proposed "since no source states the error behaviour"; the status and body are open, the stored value is not. `name empty`/`name null` (Q-VAL-02, Q-VAL-01) are rightly proposed. | R-VAL-01, R-VAL-02, R-VAL-03, R-VAL-05, R-VAL-08 | Edit: the rule outcome first (`after` is the original value, as fact), then `Open: Q-VAL-08 (status and error body)`. |
| F5 | Major | API-VAL-092, 093, 095, 096 (R-VAL-02 to R-VAL-08) | Depth (boundary) | Length limits have only on-limit and over-limit rows; the below-limit row (`maxLength - 1`) is missing, and API-VAL-096 has no `maximum - 1`. API-VAL-087 shows the full set for `name`. | R-VAL-02 to R-VAL-08; schema L4148, L4164, L4171, L4176, L4207, L4237, L4139 | Add rows to the Data sets (architect edit or creator rerun). |
| F6 | Major | R-VAL-09, R-VAL-03 (API-VAL-097, API-VAL-094) | Depth / Fidelity | R-VAL-09 states "default 0" and R-VAL-03 "default `''`", but no row leaves the field out to see the default. The `zero and zero` row is labelled "EP valid: default value" but sends `0` explicitly. API-VAL-094 cites R-CRUD-12 (default when not sent) without testing it. | R-VAL-09, R-VAL-03, R-CRUD-12; [openapi-parts.yaml#L4166](../../requirements/openapi-parts.yaml#L4166), [#L4191](../../requirements/openapi-parts.yaml#L4191) | Add a "fields left out" row (expected `0.0` / `''` as fact), or remove the R-CRUD-12 citation if CRUD covers it. |
| F7 | Major | API-VAL-098 | Data-driven (class with no row) | R-VAL-10 names `default_location` and `revision_of` as integer ID fields; neither has a row. | R-VAL-10; [openapi-parts.yaml#L4144](../../requirements/openapi-parts.yaml#L4144), [#L4212](../../requirements/openapi-parts.yaml#L4212) | Add `default_location text` and `revision_of text` rows. |
| F8 | Major | API-VAL-095, API-VAL-104 | Rule outcome stated | The `not a URL` and `no scheme` rows keep the rejection text as `Proposed`, but R-Part-17 (cited by 095) records the 1.5.6 API rejecting an invalid URL "or one without a scheme" with "Enter a valid URL." (also R-VAL-05 note). The case's Notes say "not in the schema, so it stays proposed", but the inventory is a requirement source. The status code and the `{"link": [...]}` key are still unstated. | R-Part-17 (Part inventory), R-VAL-05 Notes | Edit: text `Enter a valid URL.` as fact, key and status `Proposed, to confirm in Q-VAL-10`. Or, if the architect does not accept the inventory note as a rule, say so in Q-VAL-10 (Q2). |
| F9 | Major | API-VAL-093 | Depth (boundary) / Data-driven | The `units on limit` row sends `20 × u`, which is unlikely to be a valid unit, so its outcome depends on Q-VAL-12 and the 20-character limit itself is never shown to be accepted. | R-VAL-06; Q-VAL-12 | Use a valid unit expression of exactly 20 characters for the on-limit row (keep `QA-notaunit` as the unit-validity row). |
| F10 | Major | API-VAL-093 | Fidelity (wrong rule cited) | Cites R-Unit_measure-02 ("by default a part's unit of measure is blank"), which no row tests; the `units not a unit` row is about unit validity, which no inventory rule states (Q-VAL-12). | R-Unit_measure-02 (Units_of_Measure inventory) | Remove the R-Unit_measure-02 citation; Q-VAL-12 marks the unit-validity row. |
| F11 | Major | API-VAL-102 | Rule outcome stated | `empty body` row: `description after` is `Proposed, to confirm in Q-VAL-16`, but R-CRUD-04 (cited) says PATCH "updates only the fields sent", so with `{}` nothing changes. Step 2 already states `name` and `IPN` unchanged as fact for every row, which is inconsistent with the proposed description. The status (`200`) of `{}` may stay proposed under Q-VAL-16. | R-CRUD-04, R-VAL-16 | Edit: `description after` `QA-<suffix> original` as fact; status keeps `Proposed, to confirm in Q-VAL-16`. |
| F12 | Major | API-VAL-104 | Data-driven (class with no row) | "Field limits are enforced on PATCH" cites R-VAL-02 to R-VAL-05 and R-VAL-08, but has no `IPN on limit`, no `keywords` length row (only `null`), no `link` length rows, no `default_expiry` on-minimum, on-maximum or above-maximum rows. | R-VAL-02 to R-VAL-05, R-VAL-08 | Add the missing on/over rows, or narrow Summary and Requirement to what the rows test. |
| F13 | Major | API-VAL-103, API-VAL-104 | Open-question marking | The `name` rows on PUT and PATCH are marked with Q-VAL-01 and Q-VAL-02, whose questions are about `POST /api/part/` only. No question asks for the error status and body of `name` on PUT/PATCH (Q-VAL-16 covers only a PUT without `name`). In 103 the `name absent` error is marked Q-VAL-08, which is about fields other than `name`. | Q-VAL-01, Q-VAL-02, Q-VAL-08, Q-VAL-16 | Architect: widen Q-VAL-01/02 to PUT and PATCH (or add a question), then fix the markings. |
| F14 | Minor | API-VAL-103 | Fidelity | `name absent` says "the part is not updated, R-VAL-01", but R-VAL-01 is "required on create"; the requirement for PUT comes from R-CRUD-03 (full `Part` body) and Schema issue 4. The title also says "PATCH does not", but no step sends a PATCH (covered in API-VAL-102). | R-VAL-01, R-CRUD-03; index Schema issue 4 | Cite R-CRUD-03 and Schema issue 4 for that row; reword the title. |
| F15 | Minor | API-VAL-097 | Technique | "Boundary value analysis (negative value, minimum above maximum)": R-VAL-09 states no limit, so these are error-guessing or decision rows, not boundaries. | R-VAL-09 | Relabel. |
| F16 | Minor | API-VAL-100 | Technique | "Decision table (write-only field sent or not)", but there is no "not sent" column. R-CRUD-15 (category parameters copied) is cited but not exercised (`false`, no category). | R-VAL-12, R-CRUD-15 | Relabel; drop or justify the R-CRUD-15 citation. |
| F17 | Minor | API-VAL-101 | Data set label | `negative` is classed "EP invalid" though the schema pattern allows `-`; the row is open. `quantity five`: R-CRUD-13 states the stock is added, so a fact check (e.g. `in_stock` is `5`) could stand next to the proposed `stock_item_count`. | R-CRUD-13, [openapi-parts.yaml#L3721](../../requirements/openapi-parts.yaml#L3721) | Relabel; consider a factual stock assertion. |
| F18 | Minor | API-VAL-098 | Seed format (evidence) | `variant_of`/`responsible` linked to L4122 (category) and `assembly`/`trackable` to L4112 (active). Actual lines: L4242, L4269, L4115, L4234. | schema | Fix links. |
| F19 | Minor | API-VAL-100 | Depth | Only `initial_stock` and `copy_category_parameters` are sent; "accepted on input" is not shown for `duplicate`, `initial_supplier`, `existing_image`. | R-VAL-12 | Optional extra rows or a note. |
| F20 | Minor | API-VAL-099, API-VAL-105 | Data-driven | No `error` column for the alternative where the API rejects read-only values (Q-VAL-14); `category_name` (named in Q-VAL-14) has no row. | R-VAL-11, Q-VAL-14 | Add an `error` column (`Open: Q-VAL-14`) and a `category_name` row. |
| F21 | Minor | API-VAL-108 | Fidelity / Type | Cites R-VAL-10 (types), which says nothing about unknown keys; Type is Negative while the proposed outcome is acceptance. | R-VAL-10, Q-VAL-17 | Cite only R-CRUD-01 and Q-VAL-17; consider Type Positive or leave it to the answer. |
| F22 | Minor | API-VAL-095 | Wording | Cleanup says "up to four parts (the first three rows)". | | Fix the count. |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| API-VAL-092 | 63 | API-VAL-093 | Keep | Different rules (R-VAL-02 to 04 vs R-VAL-06/07). |
| API-VAL-093 | 63 | API-VAL-092 / API-VAL-095 | Keep | Revision and units limits plus a unit-validity class. |
| API-VAL-094 | 54 | API-VAL-097 | Keep | Null, empty and whitespace classes on text fields. |
| API-VAL-095 | 63 | API-VAL-093 | Keep | Only link URI and 2000-character case. |
| API-VAL-096 | 58 | API-VAL-093 | Keep | Integer range rule R-VAL-08. |
| API-VAL-097 | 60 | API-VAL-098 | Keep | Stock number fields R-VAL-09. |
| API-VAL-098 | 66 | API-VAL-089 | Keep | Reference and flag fields vs the name field's types. |
| API-VAL-099 | 52 | API-VAL-098 | Keep | Read-only fields (R-VAL-11), proposed accepted. |
| API-VAL-105 | 50 | API-VAL-106 | Keep | Read-only (R-VAL-11) vs wrong type (R-VAL-10) on PATCH. |
| API-VAL-106 | 50 | API-VAL-105 | Keep | Wrong type (R-VAL-10) vs read-only (R-VAL-11) on PATCH. |
| API-VAL-108 | 53 | API-VAL-098 | Keep | Unknown key vs wrong values for defined fields. |

## Questions for the architect

1. **Q1, `engineer` and initial stock (API-VAL-100, API-VAL-101).** Both cases give `engineer` "manage parts, add stock", but the demo-user table lists `engineer` only as "Part management". The sources do not say whether `engineer` can create stock through `initial_stock`. If it cannot, the cases need another user (e.g. `allaccess`), or the outcome is a permission matter (SEC).
2. **Q2, R-Part-17 note as a requirement (API-VAL-095, API-VAL-104, F8).** Does the observed 1.5.6 text "Enter a valid URL." in the inventory notes count as a stated outcome for the API? This review treats it as stated.
3. **Q3, open-question "Affected cases" lists are out of date.** Q-VAL-01 and Q-VAL-02 do not list API-VAL-103/104; Q-VAL-07 does not list API-VAL-093/094; Q-VAL-09 does not list API-VAL-094's `revision null` row's dependency on Q-VAL-07. Only the architect edits the question file.
4. **Q4, scope of Q-VAL-01/02 (F13).** Should they be widened to `PUT`/`PATCH`, or should a new question cover `name` validation on update?
