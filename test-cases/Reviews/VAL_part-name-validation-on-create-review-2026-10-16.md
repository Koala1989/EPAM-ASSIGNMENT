# Review: Part name validation on create (API), 2026-10-16

**Cases reviewed:** API-VAL-087, API-VAL-088, API-VAL-089, API-VAL-090, API-VAL-091 · **Verdict:** Approve with changes

## Coverage

`coverage_check.py --area VAL --file test-cases/API_Field_Validation/part-name-validation-on-create.md`: Rules: 18 · covered: 5 · not cited by any case: 13 (exit 0; every cited rule ID exists. R-CRUD-01 and R-Part-13, from other Areas, also exist.)

| Rule | Cases | Gap / Out of scope / Covered | Depth issues |
|---|---|---|---|
| R-VAL-01 (Part `name` required, string, max 100) | 087, 088, 089, 090, 091 | Covered | Required: absent and null rows (087). Limit: 99 / 100 / 101 (087), 100 / 101 per form content type (090). Type: 089. No over-limit row for multi-byte text (088 has 100 `Ω` only; Minor, finding 6). |
| R-VAL-03 (IPN max 100, default `''`) | 091 | Out of scope (IPN field limits) | 091 cites it only for the IPN value used in the decision table; its limit is not tested here (finding 8). |
| R-VAL-07 (revision max 100, nullable) | 091 | Out of scope (revision field limits) | As R-VAL-03 (finding 8). |
| R-VAL-10 (each field matches its schema type) | 089 | Covered for `name` only; the rest of the rule (integer IDs, boolean flags) is out of scope | See finding 1. |
| R-VAL-17 (JSON, form-urlencoded, multipart accepted) | 090 (+ JSON in 087) | Covered for `name` on create | None. |
| R-VAL-02, -04, -05, -06, -08, -09 | none | Out of scope: other Part fields (description, keywords, link, units, default_expiry, stock levels) | |
| R-VAL-11, R-VAL-12 | none | Out of scope: read-only and write-only Part fields | |
| R-VAL-13, R-VAL-14, R-VAL-15 | none | Out of scope: Category create and fields | |
| R-VAL-16 | none | Out of scope: PATCH (update), not create | |
| R-VAL-18 | none | Out of scope: `initial_stock` on create | |

Depth: Negative cases present (089, 091; negative rows in 087 and 090). No permission rule in scope (SEC). No `{id}` `GET`/`DELETE` operation in scope (`POST /api/part/` only), so no `404` case is required.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Major | API-VAL-089, rows `array` and `object` | Rule outcome stated | `count` is `Proposed, to confirm in Q-VAL-06: 0`, but the case cites R-VAL-10 ("Each field must match its schema type") and `name` is `type: string`: that an array or object is not accepted is stated by the rule, so `0` should be written as fact, as API-VAL-087 does for its absent, null and over-limit rows. Only the status code and error body are unknown. The value is unchanged; only its marking is wrong. | R-VAL-10; [openapi-parts.yaml#L4196](../../requirements/openapi-parts.yaml#L4196) | Edit 089: set `count` to `0` on `array` and `object`; keep the status `Proposed, to confirm in Q-VAL-06: 400 Bad Request`. |
| 2 | Minor | API-VAL-089 | Fidelity | The title says "is rejected", but the `number` and `boolean` rows have no proposed outcome (they may be converted). The Summary is worded correctly; the title claims more. | Q-VAL-06 | Edit the title, e.g. "Part name of a non-string JSON type on create". |
| 3 | Minor | API-VAL-087, rows `empty` and `whitespace only` | Open-question marking | `error` is `Open: Q-VAL-01 (...)`, but Q-VAL-01 asks about absent, null, over-limit and wrong-type inputs; whether empty and whitespace-only are rejected at all, and with which error, is Q-VAL-02 (whose proposal includes "error under `name`"). | Q-VAL-01, Q-VAL-02 | Edit to `Open: Q-VAL-02 (...)`, or widen Q-VAL-01 to cover blank names. |
| 4 | Minor | API-VAL-087 | Seed format (cleanup) | Postconditions say "up to three parts", but both `empty` and `whitespace only` could be accepted against the proposal, giving up to four. | Data sets rows `empty`, `whitespace only` | Edit to "up to four". |
| 5 | Minor | API-VAL-087, 089, 090, 091 | Specific Expected results | Step 2 or 3 depends on `search` matching `description`; R-LST-04 states it does, so the Note's "if it does not" fallback in 087 is not needed, and the cases do not cite R-LST-04. Partial matching of a multi-word term (`QA-<suffix> chk05`, `QA-<suffix> dup`) is not stated (R-LST-04 note). | R-LST-04 ([openapi-parts.yaml#L687](../../requirements/openapi-parts.yaml#L687)) | Optional: cite R-LST-04 in the Notes; see Question 3. |
| 6 | Minor | API-VAL-088 | Data-driven (boundary row) | The multi-byte boundary has an on-limit row (100 characters) but no over-limit row (101 multi-byte characters). The ASCII over-limit row in 087 covers R-VAL-01's limit itself, so this is optional. | R-VAL-01; Q-VAL-05 | Optional: add a `non-ASCII 101` row (`Proposed, to confirm in Q-VAL-01: 400 Bad Request`, count `0`). |
| 7 | Minor | API-VAL-088, row `padded with spaces` | Open-question marking | `returned name` is `Open: Q-VAL-04 (stored as sent or trimmed)`, though Q-VAL-04 does propose an outcome ("`name` is stored as sent"); the seed prefers `Proposed, to confirm in Q-VAL-04: equals the payload`. | Q-VAL-04 | Edit to the proposed form. |
| 8 | Minor | API-VAL-091 | Fidelity (Requirement) | Cites R-VAL-03 (IPN max 100, default `''`) and R-VAL-07 (revision max 100) although the case tests uniqueness, not those field limits. The rules that drive the case are R-VAL-01, R-Part-13 and (for the revision row) R-REV-07 / Q-VAL-07. | R-VAL-03, R-VAL-07 | Edit the Requirement field, or keep them as context and say so in the Notes. |
| 9 | Minor | API-VAL-091 | Technique | Technique lists "double submit", but no row covers it (`exact duplicate` is a separate create with the same data, not a double submit). | Data sets of 091 | Remove "double submit" from Technique, or add a row if wanted. |

No Blocker. Seed format, users (`engineer` for create, `admin` for setup and cleanup), Review fields (`Draft · Open question: ...`) and API standing rules are otherwise correct in all five cases. The 101-character over-limit rows correctly state `count` `0` as fact (R-VAL-01) with only the status proposed.

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| API-VAL-087 | 58 | API-VAL-088 | Keep | Invalid classes (absent, null, empty, whitespace-only, over limit) and ASCII length boundary, expecting no part; 088 tests valid character-content classes expecting a created part. |
| API-VAL-088 | 58 | API-VAL-087 | Keep | Special, multi-byte and padded text and how `name` is stored; not covered by 087; different open questions (Q-VAL-04, Q-VAL-05). |

## Questions for the architect

1. **R-Part-13 vs the proposals in API-VAL-091.** R-Part-13 (cited by 091) says "The part Name is a unique text label", which on its own would reject any second part with the same name. 091 proposes `201 Created` for `name only, empty IPN` and `other IPN`, based on findings F-04 (demo data shares names with different IPN or revision) and Q-VAL-03's proposal (unique only as name + IPN + revision). The proposals are labelled and Q-VAL-03 is a Conflict, so this is not reported as a defect; answering Q-VAL-03 settles which rows expect `201`.
2. **R-VAL-10 and number/boolean `name` (API-VAL-089).** Does "Each field must match its schema type" forbid a JSON number or boolean being converted to text for a `string` field? If yes, the `number` and `boolean` rows also have count `0` stated by the rule, and only the status stays open; if conversion is allowed, Q-VAL-06 stays as written.
3. **Search used to count created parts.** 087, 089, 090 and 091 count parts with `search=QA-<suffix> <tag>`. R-LST-04 states `search` covers `description` but not whether a multi-word term matches partially or per word. Is this acceptable as a verification step, or should the cases compare `GET /api/part/` counts before and after instead (as 087's Note suggests)?
