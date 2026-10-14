# Review: FIELD_Validation (API), 2026-10-14

**Cases reviewed:** API-VAL-001 to API-VAL-067 (67 cases, `test-cases/API_Field_Validation/field-validation.md`) · **Verdict:** Changes required

## Coverage

`python tools/coverage_check.py --area VAL --file test-cases/API_Field_Validation/field-validation.md`: Rules: 18 · covered: 18 · not cited by any case: 0 (exit 0, no unknown rule IDs).

| Rule | Cases | Gap / Out of scope / Covered | Depth issues |
|---|---|---|---|
| R-VAL-01 | 001-006, 057 | Covered | None: missing, null, empty, whitespace, 100, 101 (create and PATCH). |
| R-VAL-02 | 007, 008 | Covered | None (250 / 251). |
| R-VAL-03 | 009, 010 | Covered | Minor: the `default: ''` clause has no case (create without `IPN`, expect `IPN` `""`). |
| R-VAL-04 | 011-013 | Covered | None (250 / 251 / null). |
| R-VAL-05 | 014-019 | Covered | None (URI, empty, null, non-URI, 2000, 2001). |
| R-VAL-06 | 020-022 | Covered | On-limit case blocked by Q-VAL-05 (correctly marked). |
| R-VAL-07 | 023, 024 | Covered | Minor: the `nullable` clause has no case (`revision: null`); other nullable fields have one. |
| R-VAL-08 | 025-029 | Covered | None (0, -1, max, max + 1, wrong type). |
| R-VAL-09 | 030-034 | Covered | Minor: no wrong-type case for `maximum_stock` (only `minimum_stock`, 032). |
| R-VAL-10 | 029, 032, 035-039 | Covered (partial) | **Major:** the rule names five integer-ID fields; `revision_of` and `responsible` have no wrong-type case. |
| R-VAL-11 | 040-042 | Covered | None (create and update, three representative fields). |
| R-VAL-12 | 043 | Covered (partial) | Minor: `existing_image` and `initial_supplier` not covered (acknowledged in the case's Notes). |
| R-VAL-13 | 044-047 | Covered | None (missing, 100, 101, empty). |
| R-VAL-14 | 048-054 | Covered | Minor: the `icon` `nullable` clause has no case. |
| R-VAL-15 | 055 | Covered | None. |
| R-VAL-16 | 056-058 | Covered | None. |
| R-VAL-17 | 059-061 | Covered (partial) | **Major:** the rule says "create **and update** bodies"; no `PUT`/`PATCH` case sends form-urlencoded or multipart. Category endpoints also untested (Minor). |
| R-VAL-18 | 062-067 | Covered | **Major:** decimal places have only the over-limit case (066, 6 places); the on-limit case (5 places, e.g. `"1.12345"`) is missing. |

No API standing-rule gaps: no case in this set does a `GET` or `DELETE` on an `{id}` as the action under test (the `404` cases belong to CRUD), and every category cleanup sends both delete flags.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | API-VAL-061 | No assumptions | Step 1 says "Known: the part is not created" and step 2 expects `count` `0`. R-VAL-17 says only that the three listed types are accepted. It does not say ("only", "must") that other types are rejected, and Q-VAL-01 covers only the status and body. | R-VAL-17; [openapi-parts.yaml#L752-L763](../../../requirements/openapi-parts.yaml#L752) | Make both outcomes Not known (extend Q-VAL-01 or raise a new question on whether an unlisted content type is rejected), or confirm the rule. |
| 2 | Major | R-VAL-10 | Coverage (gap) | No wrong-type case for `revision_of` or `responsible`, both named in the rule. | R-VAL-10; [openapi-parts.yaml#L4212](../../../requirements/openapi-parts.yaml#L4212), [#L4269](../../../requirements/openapi-parts.yaml#L4269) | Rerun test-case-creator for the two missing cases. |
| 3 | Major | R-VAL-18 | Coverage (boundary) | Decimal places: 6 places is tested (066) but 5 places, on the pattern limit, is not. | `pattern: ^-?\d{0,10}(?:\.\d{0,5})?$`, [openapi-parts.yaml#L3721](../../../requirements/openapi-parts.yaml#L3721) | Rerun the creator for an on-limit case (`"quantity": "1.12345"`). |
| 4 | Major | R-VAL-17 | Coverage (gap) | The "update" half of the rule has no case: no `PATCH`/`PUT` with `application/x-www-form-urlencoded` or `multipart/form-data`. | R-VAL-17; `PATCH /api/part/{id}/` content types, [openapi-parts.yaml#L2767](../../../requirements/openapi-parts.yaml#L2767) | Rerun the creator for update cases (and, optionally, one category create). |
| 5 | Major | API-VAL-043, 062, 063, 064, 065, 066, 067 | User / Settings / Open-question marking | Every case sends `initial_stock` with Settings `None` and user `engineer`. The docs tie initial stock to the *Create Initial Stock* setting. The seed gives `engineer` "manage parts, view stock", and creating initial stock creates a stock item. No question records whether the setting or the stock permission changes how the API handles `initial_stock`. | [part-create.md#L37](../../../requirements/docs/part-create.md#L37); `references/seed-manual-test-case.md` L55, L105 | Answer the question below; then set Settings (and the user if needed) in these cases, or mark them with the new question. |
| 6 | Major | API-VAL-055 | No assumptions | Step 1 expects `pathstring` to be `QA-<suffix> RO Category` and step 3 expects it to be "still" that value. The schema says only `title: Path`, and no rule states the `pathstring` of a top-level category. | [openapi-parts.yaml#L3551-L3555](../../../requirements/openapi-parts.yaml#L3551) | Record the returned `pathstring` in step 1 (as is done for `level`) and compare in step 3. |
| 7 | Minor | API-VAL-001, 003, 004, 008, 010, 012, 017, 019, 022, 024, 026, 028, 029, 032, 035-038, 044, 046, 049, 051, 054, 061-063, 065, 066 | Fidelity (verification step) | Step 2 searches `QA-<suffix>` and expects `count` `0`. That holds only if no other record has the same suffix at that moment, but the seed calls it "the run suffix". | `references/seed-api-test-case.md` L40 | Search on the case's own unique name, or compare counts before and after; see the question below. |
| 8 | Minor | API-VAL-024 | Open-question marking | A rejection may come from the revision settings (Q-VAL-06) rather than from `maxLength`. API-VAL-022 notes the same kind of confound for `units`; this case does not. | Q-VAL-06 | Add a note (or add Q-VAL-06 to the marking). |
| 9 | Minor | Positive part-create cases without a category (e.g. 002, 007, 009, 011, 013-016, 018, 020, 025, 027, 030, 031, 056, 059, 060) | Specific Expected results | They expect "Body is valid against `Part`". Known finding F-11 says that check fails for any uncategorised part, but only API-VAL-039 mentions it. | `test-cases/findings.md` F-11 | Add the F-11 note, or create these parts in a QA category so the field rule is tested in isolation. |
| 10 | Minor | API-VAL-042, API-VAL-043 | Fidelity | Integer fields are sent as quoted strings (`"category": "<category pk>"`, `"original": "<pk from step 1>"`), which overlaps the wrong-type class of API-VAL-035. | `Part.category` `type: integer` L4122; `PartDuplicateOptions.original` `type: integer` L4449 | Send the pk as a JSON integer. |
| 11 | Minor | API-VAL-065, API-VAL-066 | Seed format (Type) | Typed Boundary, while every other over-limit case (003, 008, 010, ...) is Negative. | Seed Type field | Align the Type. |
| 12 | Minor | API-VAL-041, 055, 057 | Wording | The postconditions say "No record is created if the request is rejected", but step 1 creates one. API-VAL-057 step 2 says "not created or changed" for a `PATCH`. | Cases | Reword the postconditions to name the step 1 record; use "not changed" for the PATCH. |
| 13 | Minor | API-VAL-030, 037, 038, 056, 058 | Seed format (Requirement) | API-VAL-030 checks `maximum_stock` but cites only `minimum_stock`. API-VAL-037, 038, 056 and 058 cite components with no line link. | `Part.maximum_stock` L4192, `variant_of` L4242, `virtual` L4246 | Add the missing component and line links. |
| 14 | Minor | R-VAL-18 (inventory) | Fidelity | Cases 063-067 test the decimal `pattern`, but the rule text states only "quantity required". The pattern comes from the cited schema line, not from the rule wording. | R-VAL-18; L3721 | Architect: consider extending R-VAL-18 to state the pattern. |
| 15 | Minor | R-VAL-03, R-VAL-07, R-VAL-09, R-VAL-14 | Coverage (depth) | Valid or invalid classes stated in these rules have no case: `IPN` default `''`, `revision: null`, wrong type for `maximum_stock`, `icon: null`. | Rules as listed | Optional: rerun the creator for these. |

## Duplicates

All 61 cases scoring 50 or more were judged **Keep**. Each one differs from every match in at least one real dimension: a different field or rule clause, a different boundary (on, under or over; minimum or maximum; integer digits or decimal places), a different equivalence class (absent, null, empty, whitespace, wrong type, wrong format), a different resource or schema component (Part or Category; `PatchedPart` or `PatchedCategory`), or a different content type. The verdicts are recorded in the case file.

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| API-VAL-001 | 90 | API-VAL-004 | Keep | Absent vs `null` (different invalid class). |
| API-VAL-002 | 70 | API-VAL-009 | Keep | `name` (R-VAL-01) vs `IPN` (R-VAL-03). |
| API-VAL-003 | 88 | API-VAL-001 | Keep | maxLength + 1 vs absent. |
| API-VAL-004 | 90 | API-VAL-001 | Keep | `null` vs absent. |
| API-VAL-005 | 81 | API-VAL-006 | Keep | Empty vs whitespace-only (trimming, Q-VAL-04). |
| API-VAL-006 | 81 | API-VAL-005 | Keep | Whitespace-only vs empty. |
| API-VAL-007 | 67 | API-VAL-011 | Keep | `description` (R-VAL-02) vs `keywords` (R-VAL-04). |
| API-VAL-008 | 75 | API-VAL-012 | Keep | `description` vs `keywords`. |
| API-VAL-009 | 70 | API-VAL-002 | Keep | `IPN` vs `name`. |
| API-VAL-010 | 77 | API-VAL-003 | Keep | `IPN` vs `name`. |
| API-VAL-011 | 67 | API-VAL-007 | Keep | `keywords` vs `description`. |
| API-VAL-012 | 75 | API-VAL-008 | Keep | `keywords` vs `description`. |
| API-VAL-013 | 64 | API-VAL-016 | Keep | `keywords` null vs `link` null (different rules). |
| API-VAL-014 | 75 | API-VAL-016 | Keep | URI vs `null` (different valid class). |
| API-VAL-015 | 71 | API-VAL-016 | Keep | Empty string vs `null`. |
| API-VAL-016 | 75 | API-VAL-014 | Keep | `null` vs URI. |
| API-VAL-017 | 84 | API-VAL-019 | Keep | Format clause vs maxLength clause. |
| API-VAL-018 | 58 | API-VAL-002 | Keep | `link` vs `name`. |
| API-VAL-019 | 84 | API-VAL-017 | Keep | maxLength clause vs format clause. |
| API-VAL-020 | 64 | API-VAL-013 | Keep | `units` vs `keywords`. |
| API-VAL-021 | 55 | API-VAL-002 | Keep | `units` vs `name`. |
| API-VAL-022 | 70 | API-VAL-003 | Keep | `units` vs `name`. |
| API-VAL-023 | 54 | API-VAL-002 | Keep | `revision` vs `name`. |
| API-VAL-024 | 75 | API-VAL-003 | Keep | `revision` vs `name`. |
| API-VAL-025 | 81 | API-VAL-027 | Keep | Minimum vs maximum boundary. |
| API-VAL-026 | 89 | API-VAL-028 | Keep | Below minimum vs above maximum. |
| API-VAL-027 | 81 | API-VAL-025 | Keep | Maximum vs minimum boundary. |
| API-VAL-028 | 89 | API-VAL-026 | Keep | Above maximum vs below minimum. |
| API-VAL-029 | 79 | API-VAL-026 | Keep | Wrong type vs out of range. |
| API-VAL-030 | 73 | API-VAL-031 | Keep | Default (omitted) vs explicit decimals. |
| API-VAL-031 | 73 | API-VAL-030 | Keep | Explicit decimals vs default. |
| API-VAL-032 | 78 | API-VAL-029 | Keep | `minimum_stock` (R-VAL-09) vs `default_expiry` (R-VAL-08). |
| API-VAL-033 | 62 | API-VAL-067 | Keep | Part field vs `InitialStock` field (different rules). |
| API-VAL-035 | 88 | API-VAL-036 | Keep | `category` vs `default_location` (separately named in R-VAL-10). |
| API-VAL-036 | 88 | API-VAL-035 | Keep | `default_location` vs `category`. |
| API-VAL-037 | 88 | API-VAL-035 | Keep | `variant_of` vs `category`. |
| API-VAL-038 | 83 | API-VAL-035 | Keep | Boolean clause vs integer-ID clause. |
| API-VAL-039 | 64 | API-VAL-013 | Keep | `category` (integer, R-VAL-10) vs `keywords`. |
| API-VAL-040 | 78 | API-VAL-042 | Keep | `pk` vs derived `category_name` (different starting state and check). |
| API-VAL-042 | 78 | API-VAL-040 | Keep | `category_name` with a category vs `pk`. |
| API-VAL-044 | 88 | API-VAL-046 | Keep | Absent vs maxLength + 1. |
| API-VAL-045 | 67 | API-VAL-053 | Keep | Category `name` (R-VAL-13) vs `icon` (R-VAL-14). |
| API-VAL-046 | 88 | API-VAL-044 | Keep | maxLength + 1 vs absent. |
| API-VAL-047 | 68 | API-VAL-044 | Keep | Empty vs absent. |
| API-VAL-048 | 81 | API-VAL-050 | Keep | `description` vs `default_keywords` (separate clauses). |
| API-VAL-049 | 88 | API-VAL-051 | Keep | `description` vs `default_keywords`. |
| API-VAL-050 | 81 | API-VAL-048 | Keep | `default_keywords` vs `description`. |
| API-VAL-051 | 88 | API-VAL-049 | Keep | `default_keywords` vs `description`. |
| API-VAL-053 | 72 | API-VAL-048 | Keep | `icon` (100) vs `description` (250). |
| API-VAL-054 | 84 | API-VAL-049 | Keep | `icon` vs `description`. |
| API-VAL-056 | 56 | API-VAL-058 | Keep | `PatchedPart` vs `PatchedCategory`. |
| API-VAL-058 | 56 | API-VAL-056 | Keep | `PatchedCategory` vs `PatchedPart`. |
| API-VAL-059 | 78 | API-VAL-060 | Keep | form-urlencoded vs multipart. |
| API-VAL-060 | 78 | API-VAL-059 | Keep | multipart vs form-urlencoded. |
| API-VAL-061 | 57 | API-VAL-001 | Keep | Content type vs field value. |
| API-VAL-062 | 83 | API-VAL-063 | Keep | Quantity absent vs non-numeric. |
| API-VAL-063 | 83 | API-VAL-062 | Keep | Non-numeric vs absent. |
| API-VAL-064 | 64 | API-VAL-067 | Keep | Upper digit limit vs negative. |
| API-VAL-065 | 84 | API-VAL-066 | Keep | Integer-digit limit vs decimal-places limit. |
| API-VAL-066 | 84 | API-VAL-065 | Keep | Decimal-places limit vs integer-digit limit. |
| API-VAL-067 | 64 | API-VAL-064 | Keep | Negative vs upper digit limit. |

Not judged (no duplicate-check line; scored under 50): API-VAL-034, 041, 043, 052, 055, 057.

## Questions for the architect

1. **Initial stock (API-VAL-043, 062-067):** The docs say the *Create Initial Stock* setting controls the initial-stock section of the create form ([part-create.md#L37](../../../requirements/docs/part-create.md#L37)). Does this setting also decide whether `POST /api/part/` accepts or validates `initial_stock`? Can `engineer` (manage parts, view stock) create the initial stock item, or is a user with stock add permission needed?
2. **Unlisted content type (API-VAL-061):** R-VAL-17 lists the accepted types but does not say other types are rejected. Should a `text/plain` body be treated as rejected (the part is not created), or should that also be an open question?
3. **Run suffix (step 2 of the negative create cases):** Is `QA-<suffix>` unique per case or shared by a whole run? If it is shared, `search=QA-<suffix>` with `count` `0` can fail when other cases run in parallel.
4. **Category `pathstring` (API-VAL-055):** Should the `pathstring` of a top-level category equal its `name`? No rule or schema line states this.
