# Review: Relationships (API), 2026-10-14

**Cases reviewed:** API-REL-003 to API-REL-056 (54 cases, `test-cases/API_Relationships/relationships.md`) · **Verdict:** Approve with changes

## Coverage

`coverage_check.py --area REL --file test-cases/API_Relationships/relationships.md`: Rules: 11 · covered: 11 · not cited by any case: 0 (exit 0; no unknown rule IDs).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-REL-01 | 003, 004, 005, 006 | Covered | None: valid move, null, non-existent ID on create and on PATCH. |
| R-REL-02 | 007, 008, 009, 010 | Covered | None: direct create (negative), child (positive), move into (negative), category made structural. |
| R-REL-03 | 011, 012, 013 | Covered | None. |
| R-REL-04 | 014, 015, 016 | Covered | Optional: no case for a category `default_location` ID that does not exist (part equivalent is 013). Minor. |
| R-REL-05 | 016, 017 | Covered | None (values open, Q-REL-03). Write attempt on the read-only field belongs to VAL. |
| R-REL-06 | 018 to 024 | Covered | None. |
| R-REL-07 | 025, 026 | Covered | Write attempt on read-only `level`/`pathstring` is R-VAL-15 (VAL), out of scope. |
| R-REL-08 | 027 to 036 | Covered | Required fields (3 negatives), SKU on and over `maxLength`, non-existent part, non-purchaseable part, `GET`/`DELETE` 404. Missing: SKU below the limit (99), a non-existent `supplier` ID. Minor. |
| R-REL-09 | 037 to 042 | Covered | **Major:** `InitialSupplier.sku` has only the over-limit case (042); no on-limit (100) case. `InitialSupplier.mpn` (`maxLength: 100`, [openapi-parts.yaml#L3747-L3750](../../requirements/openapi-parts.yaml#L3747)) has no boundary case at all. |
| R-REL-10 | 043 to 051 | Covered | None for REL; template/revision restrictions are cross-referenced to Part_Template and REV. |
| R-REL-11 | 052 to 056 | Covered | None: edit and delete with locking on (negative) and off (positive), unlock. |

404 standing rule: the only in-scope `{id}` operations with `GET`/`DELETE` that REL owns are `GET` and `DELETE /api/company/part/{id}/`: 035 and 036. `/api/part/{id}/` and `/api/part/category/{id}/` 404s are CRUD cases. No 404 gap.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Major | R-REL-09 | Depth (boundary) | `initial_supplier.sku` has no on-limit (100) case; `initial_supplier.mpn` has no on or over-limit case. | `InitialSupplier.sku` and `.mpn` `maxLength: 100`, [openapi-parts.yaml#L3739-L3750](../../requirements/openapi-parts.yaml#L3739), cited by R-REL-09. | Rerun the creator for these boundary cases (mark Q-REL-01, Q-REL-06 for the over-limit ones). |
| 2 | Major | API-REL-042 | Specific Expected results | Step 1 expects "No supplier part with a 101-character `SKU` exists", but the case has no step that reads supplier parts, so the claim cannot be checked. Summary says "is not accepted" while the Expected result says it is unknown whether the part is created. | Steps table of API-REL-042. | Add a `GET /api/company/part/` step (filter by supplier) and a `GET /api/part/` search step; align the Summary with the open question. |
| 3 | Major | API-REL-026 | No assumptions | The Summary states that `level` and `pathstring` of both categories "are recomputed" after the move; Q-REL-05 asks exactly that. Also Mid's post-move values are never read, and Leaf's pre-move values are never recorded, so the step 1 baseline is unused and the "both" in the Summary is not tested. | R-REL-07 (format not stated); Q-REL-05 ("Are `level` and `pathstring` of descendants recomputed..."). | Reword the Summary to "are checked"; record Leaf before the move and read Mid after it. |
| 4 | Major | API-REL-035, API-REL-036 | Open-question marking | Prerequisites need a supplier company created through an endpoint outside the slice and cite Q-REL-06, yet Review is `Draft` and Automation is `Yes`. Every other case with the same setup (027 to 034) is marked Q-REL-06 and `Partial`. Q-REL-06's Affected cases list omits them. | Prerequisites of 035/036; Q-REL-06 row in `open-question_REL.md`. | Mark both `Draft · Open question: Q-REL-06`, Automation `Partial`; the architect adds them to Q-REL-06's Affected cases. The `404` expectation itself stays (standing rule). |
| 5 | Minor | API-REL-003 | No assumptions | Step 1 expects `category_name` to be `QA-<suffix> Category B`. The schema gives only a read-only string ([openapi-parts.yaml#L4125](../../requirements/openapi-parts.yaml#L4125)); the value is an observation in findings F-11, not a rule. | F-11 (observation). | Accept as observed, or keep only the `category` check. |
| 6 | Minor | API-REL-049 | Seed format | Settings is not in `setting = state` form ("state them in the run"). The new revision uses the same name as the original (`QA-<suffix> Original`), which makes the cleanup and any name search ambiguous. | Seed Prerequisites format. | Give a state per setting (or `default, recorded at run`) and a distinct name such as `QA-<suffix> Original rev B`. |
| 7 | Minor | API-REL-052, 054, 055 | User | Part `PATCH` steps run as `admin`; `engineer` can edit parts (used in 003, 012, 044). `admin` is needed only for the setting change. | Seed: least-privileged user that can make the call. | Run the part steps as `engineer`; keep `admin` for the setting. (053/056 deletes as `admin` match the CRUD cases.) |
| 8 | Minor | API-REL-052, 053, 054 | Seed format (cleanup / data) | Cleanup relies on unlocking the part, which is itself open (054, Q-REL-09), with no fallback. 053/054 Prerequisites set "`active` `false` and `locked` `true` with `PATCH`" without an order; if `locked` is set first, the inactivation may be refused. | Q-REL-09; R-REL-11. | Cleanup: switch `PART_ENABLE_LOCKING` off before unlocking/deleting. Data: one `PATCH` or inactivate first. |
| 9 | Minor | API-REL-039 | User | Step 2 user is conditional ("if refused for `engineer`, run step 2 as `admin`"). | Notes of 039; F-03. | Pick one user for step 2 (`admin`, as in 027 to 036). |
| 10 | Minor | API-REL-016 | Technique | "Exploratory" is not a technique for a scripted case. | Seed Technique list. | Drop it; the decision table suffices. |
| 11 | Minor | API-REL-022 | Seed format | Conditional cleanup does not name the user (`admin`). | Seed: cleanup as `admin`. | Add "As `admin`". |
| 12 | Minor | API-REL-035, 036 | Specific Expected results | The 404 body is written as `No <Model> matches the given query.` with the model "not confirmed". | Seed Not found standing rule. | Architect to confirm the model name (see Questions). |
| 13 | Minor | R-REL-08, R-REL-04 | Depth (optional) | No SKU 99-character case; no non-existent `supplier` ID on supplier-part create; no non-existent category `default_location`. | R-REL-08, R-REL-04 sources. | Optional: rerun the creator if wanted. |

No Blockers. All 54 cases have every seed field in order, the three-column Steps table, a rule ID with source link, and a `Draft` or `Draft · Open question` Review value. Open-question markings match the Affected cases in `open-question_REL.md` except finding 4. Non-existent IDs are created and deleted (no guessed numbers), and every category delete sends both flags.

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| API-REL-003 | 56 | 004 | Keep | Existing ID vs `null`. |
| API-REL-004 | 56 | 003, 012 | Keep | `null` vs ID; other matches are other fields/rules. |
| API-REL-005 | 67 | 045, 050 | Keep | `category` (R-REL-01) vs `variant_of`/`revision_of`/`default_location`. |
| API-REL-006 | 69 | 009 | Keep | Non-existent ID vs structural category. |
| API-REL-007 | 56 | 005 | Keep | Structural category (R-REL-02) vs missing IDs. |
| API-REL-008 | 50 | 011 | Keep | Different rule (R-REL-02 vs R-REL-03). |
| API-REL-009 | 69 | 006 | Keep | Structural vs non-existent. |
| API-REL-011 | 50 | 008 | Keep | Different rule. |
| API-REL-012 | 58 | 015 | Keep | Part vs category `default_location`. |
| API-REL-013 | 69 | 045, 050 | Keep | Different reference field and rule. |
| API-REL-014 | 53 | 019 | Keep | `default_location` (R-REL-04) vs `parent` (R-REL-06). |
| API-REL-015 | 58 | 012 | Keep | Category vs part. |
| API-REL-018 | 66 | 019 | Keep | Parent given vs omitted; different outcome. |
| API-REL-019 | 66 | 018 | Keep | Omitted vs given. |
| API-REL-020 | 63 | 021 | Keep | Another parent vs `null`. |
| API-REL-021 | 63 | 020 | Keep | `null` vs another parent. |
| API-REL-023 | 87 | 024 | Keep | Direct self-reference vs indirect cycle (different class and starting state). |
| API-REL-024 | 87 | 023 | Keep | Indirect cycle vs direct self-reference. |
| API-REL-028 | 87 | 029 | Keep | Different required field omitted (`SKU`). |
| API-REL-029 | 92 | 030 | Keep | `part` omitted vs `supplier` omitted. |
| API-REL-030 | 92 | 029 | Keep | `supplier` omitted vs `part` omitted. |
| API-REL-033 | 81 | 029 | Keep | Non-existent `part` ID vs `part` omitted. |
| API-REL-034 | 52 | 029, 033 | Keep | Valid payload, non-purchaseable part. |
| API-REL-035 | 59 | 036 | Keep | `GET` vs `DELETE`; one 404 case per operation. |
| API-REL-036 | 59 | 035 | Keep | `DELETE` vs `GET`. |
| API-REL-037 | 69 | 038 | Keep | Supplier only vs supplier plus manufacturer. |
| API-REL-038 | 69 | 037 | Keep | Adds manufacturer and MPN. |
| API-REL-044 | 56 | 012 | Keep | `variant_of` vs other fields. |
| API-REL-045 | 89 | 050 | Keep | `variant_of` vs `revision_of` clause. |
| API-REL-047 | 52 | 051 | Keep | `variant_of` self-reference (open) vs `revision_of` self-reference (forbidden by docs). |
| API-REL-050 | 89 | 045 | Keep | `revision_of` vs `variant_of`. |
| API-REL-051 | 52 | 047 | Keep | `revision_of` vs `variant_of`. |

Judgements are recorded in the case file after each `**Duplicate check:**` line.

## Questions for the architect

1. **Scope of R-REL-11 "cannot be edited" (API-REL-052).** The docs list the locked-part restrictions as delete, BOM items and parameters only ([part-index.md#L106-L110](../../requirements/docs/part-index.md#L106)); editing the part's own fields is not in that list. Only the schema field description says "Locked parts cannot be edited" ([openapi-parts.yaml#L4187](../../requirements/openapi-parts.yaml#L4187)). The inventory merges both. Is a `PATCH` of `description` on a locked part meant to be refused? If unsure, API-REL-052's "not edited" becomes an open question.
2. **404 body model name for supplier parts (API-REL-035/036).** The standing rule gives `{"detail": "No <Model> matches the given query."}`. Which model name applies to `/api/company/part/{id}/` (e.g. `SupplierPart`)? The sources do not say.
3. **API-REL-039 and Q-REL-07.** `InitialSupplier` has no `required` list, so by OpenAPI semantics all its fields are optional and 039 (supplier and manufacturer `null`, no `sku`) is written as a plain positive. Q-REL-07 nevertheless asks which fields are required. Should 039 also be marked `Q-REL-07`?
