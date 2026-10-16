# Review: Category field validation on create and update (API), 2026-10-16

**Cases reviewed:** API-VAL-109, API-VAL-110, API-VAL-111, API-VAL-112, API-VAL-113, API-VAL-114, API-VAL-115, API-VAL-116, API-VAL-117, API-VAL-118, API-VAL-119, API-VAL-120, API-VAL-121, API-VAL-122, API-VAL-123 · **Verdict:** Changes required

All 15 cases are in [category-field-validation-create-and-update.md](../API_Field_Validation/category-field-validation-create-and-update.md), Area `VAL`. They also cite CRUD rules, so coverage was run for `VAL` and `CRUD`.

## Coverage

`python tools/coverage_check.py --area VAL --area CRUD --file test-cases/API_Field_Validation/category-field-validation-create-and-update.md`: Rules: 35 · covered: 9 · not cited by any case: 26 · exit 0 (no unknown rule IDs).

| Rule | Cases | Gap / Out of scope / Covered | Depth issues |
|---|---|---|---|
| R-VAL-13 (Category `name` required, max 100) | 109, 112, 113, 115, 116, 117, 119, 120, 123 | Covered | Create: absent, null, empty, whitespace, 100 and 101 are covered. No 1-character row, although the 109 Summary claims "1 to 100 characters" (finding 9). |
| R-VAL-14 (`description` 250, `default_keywords` nullable 250, `icon` nullable 100) | 110, 111, 116, 120 | Covered | Create: on and over limit for all three. PATCH (120): no `default_keywords on limit` row (finding 6). Create null/empty: no `icon` empty row (finding 12). |
| R-VAL-15 (read-only `pk`, `level`, `pathstring`, `part_count`, `subcategories`, `starred`) | 114, 121 | Covered | `starred` is in the rule and has no row on create or update (finding 5). |
| R-VAL-16 (PATCH bodies have no required fields) | 118, 119, 120, 121, 122 | Covered | None |
| R-VAL-17 (JSON, form-urlencoded, multipart) | 117 | Covered | Covered on create only. No PUT/PATCH with form or multipart bodies; the rule says "create and update" (finding 13). |
| R-VAL-10 (each field matches its schema type) | 113, 116, 122 | Covered | The rule names Part fields only. The Category types are open in Q-VAL-24, and the cases mark it. 122 has no `default_location` row and no decimal or array rows (finding 14). |
| R-CRUD-06 (category create `201`) | 109, 110, 111, 114, 115 | Covered | None |
| R-CRUD-08 (category PUT `200`) | 119 | Covered | None |
| R-CRUD-09 (category PATCH updates only the fields sent) | 118, 120, 122, 123 | Covered | See finding 4 (118 `empty body` row). |
| R-VAL-01 to R-VAL-12, R-VAL-18 | none | Out of scope | Part fields (Part name and Part field validation functionalities). |
| R-CRUD-01 to R-CRUD-05, R-CRUD-11 to R-CRUD-16 | none | Out of scope | Part CRUD (part-and-category CRUD functionality). |
| R-CRUD-07, R-CRUD-10 | none | Out of scope | Category GET and DELETE belong to the CRUD functionality. This functionality has no `{id}` GET or DELETE under test, so the 404 standing rule does not apply here. |
| R-CRUD-17 | none | Out of scope | Bulk updates (CRUD). |

Negative cases are present (113, 114, 115, 116, 119, 121, 122, 123).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | API-VAL-117 | No assumptions / Data-driven | The `form on limit` and `multipart on limit` rows send the same `name` (`QA-<suffix>` + 89 × `x`), both top-level, and both expect `201 Created` as fact. No cleanup runs between rows (cleanup is after the case: "up to two categories"). If Q-VAL-20 is answered as proposed (name unique among siblings), the second on-limit row fails as a duplicate, not because of the limit, and the case misleads. | Q-VAL-20 proposal; [openapi-parts.yaml#L3517](../../requirements/openapi-parts.yaml#L3517) | Edit the case: make the name unique per row (for example, end the padding with the row tag) or delete each row's category before the next row. |
| 2 | Major | API-VAL-115, 118, 119, 120, 121, 122 | Data-driven / Prerequisites | Step 1 creates the same fixed names on every row (`QA-<suffix> Parent A`/`Parent B`/`Twin`, `Patch base`, `Put base`, `Upd base`, `Ro base`, `Type base`), and cleanup is described per case, not per row. Nothing says each row gets a fresh suffix or deletes its records first. Under Q-VAL-20's proposal, step 1 of the second row could be refused as a sibling duplicate, so the outcome would depend on row order. | Q-VAL-20; case Postconditions ("one category per row run") | Edit the cases: state that every row uses its own `QA-<suffix>`, or cleans up before the next row. |
| 3 | Major | API-VAL-116 | Open-question marking | `structural: "maybe"` is a wrong-type value, which is the subject of Q-VAL-24. The proposed outcome expects an error entry under `structural`. The Review field marks only Q-VAL-18, and Q-VAL-24's Affected cases does not list API-VAL-116. | [open-question_VAL.md](../Open_Questions/open-question_VAL.md) Q-VAL-24 | Edit the Review field to `Draft · Open question: Q-VAL-18, Q-VAL-24`. Add API-VAL-116 to Q-VAL-24's Affected cases (architect's file). |
| 4 | Major | API-VAL-118 | Rule outcome stated | `empty body` row: `description after` is `Proposed, to confirm in Q-VAL-23: QA-<suffix> original`. R-CRUD-09 (cited) says PATCH "updates only the fields sent", so when nothing is sent, nothing changes. That is the rule's outcome and should be stated as fact. Only the status code is open in Q-VAL-23. | R-CRUD-09; [openapi-parts.yaml#L1370](../../requirements/openapi-parts.yaml#L1370) | Edit the row: `QA-<suffix> original (R-CRUD-09)`, and keep the status as proposed. |
| 5 | Major | R-VAL-15 / API-VAL-114, API-VAL-121 | Coverage depth | R-VAL-15 lists `starred` as read-only. Neither case has a `starred` row, and both Summaries list only five fields. | R-VAL-15; [openapi-parts.yaml#L3556](../../requirements/openapi-parts.yaml#L3556), [#L5032](../../requirements/openapi-parts.yaml#L5032) | Add a `starred` row (for example `true`) to both cases, or rerun the creator for it. |
| 6 | Major | R-VAL-14 / API-VAL-120 | Coverage depth (boundary) | On PATCH, `default_keywords` has an `over limit` row (251) but no `on limit` row (250). `name`, `description` and `icon` have both. | R-VAL-14; [openapi-parts.yaml#L5003](../../requirements/openapi-parts.yaml#L5003) | Add a `default_keywords on limit` row (250 × `k`, `200 OK`). |
| 7 | Minor | API-VAL-109, 111, 119, 120 | Open-question marking | The `error` column for empty, whitespace or `description null` rows cites `Open: Q-VAL-18`. Q-VAL-18 covers absent, null and over-limit values; empty and whitespace are in Q-VAL-19. The Review fields list both questions, so this is about labels only. | Q-VAL-18, Q-VAL-19 | Optional: cite Q-VAL-19 in those cells, or widen Q-VAL-18 to cover error bodies for every case in this functionality. |
| 8 | Minor | API-VAL-111 | Seed format (Requirement) | The schema links do not line up with the field list. `default_keywords / icon / parent / default_location` is linked to L3525 (default_location), L3529 (default_keywords), L3537 (parent), L3563 (icon). | [openapi-parts.yaml#L3525-L3567](../../requirements/openapi-parts.yaml#L3525) | Reorder the links to match the fields. |
| 9 | Minor | API-VAL-109 | Fidelity (Summary) | The Summary says a category is created "for a `name` of 1 to 100 characters", but no row sends 1 character. The schema gives no `minLength`. | [openapi-parts.yaml#L3517](../../requirements/openapi-parts.yaml#L3517) | Add a `1 character` row (proposed `201`), or reword the Summary to "up to 100". |
| 10 | Minor | API-VAL-112 | Specific Expected results | Step 1 has no branch for a rejected request ("Body is valid against `Category`; `name` is ..."), and step 2 depends on a `pk` from step 1. Every row's status is only proposed, so a rejection leaves steps 1 and 2 undefined. | Q-VAL-22, Q-VAL-19 | Add "For a rejected request, the body is ...; skip step 2", with an `error` column. |
| 11 | Minor | API-VAL-118, API-VAL-119 | Technique / Summary | 118's "State transition" is a before/after value check, not a state transition. 119's title "PUT needs the name field, PATCH does not" names PATCH, but the case does not test PATCH (118 does). | Seed technique list | Relabel 118's technique (for example "Equivalence partitioning"). Retitle 119 to the PUT behaviour only. |
| 12 | Minor | API-VAL-111 | Coverage depth | Q-VAL-19 proposes that empty and whitespace strings are accepted for `icon`. The case has an empty row for `description` and `default_keywords` only, and no `icon` empty row. | Q-VAL-19 | Optional extra row. |
| 13 | Minor | R-VAL-17 / API-VAL-117 | Coverage depth | R-VAL-17 says "create and update bodies". Only create is tested with form-urlencoded and multipart. | R-VAL-17; [openapi-parts.yaml#L1349-L1354](../../requirements/openapi-parts.yaml#L1349), [#L1386-L1391](../../requirements/openapi-parts.yaml#L1386) | Architect's call: add update rows, or accept create-only coverage. |
| 14 | Minor | API-VAL-122 | Coverage depth | The update counterpart of 113 covers only `parent` text and `structural` text. It has no `default_location` row, decimal row or array row. | Q-VAL-24; [openapi-parts.yaml#L4995](../../requirements/openapi-parts.yaml#L4995) | Optional extra rows. |
| 15 | Minor | API-VAL-109, 112, 117 | Specific Expected results | Step 2 (or cleanup) lists categories with `limit=500` and filters by `description` on the client. If the instance has more than 500 categories, results are missed and `count` is wrong. | Seed: no hard limits stated | Page through the results, or use `offset`, or filter by a server-side parameter. |
| 16 | Minor | API-VAL-115 | Wording | The Technique has a typo: "two stores users". The Notes assume search is case-insensitive in step 3 (a fallback is given). | n/a | Fix the wording. |
| 17 | Minor | API-VAL-114, API-VAL-121 | Specific Expected results | No `error` column. If Q-VAL-21 is answered "rejected", the steps have no expected error body. | Q-VAL-21 | Add an `error` column (`Open: Q-VAL-21`). |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| API-VAL-109 | 60 | API-VAL-110 | Keep | Name required and length (R-VAL-13) versus the other fields' limits (R-VAL-14). Also differs from 111, 112 and 117 (classes, channel). |
| API-VAL-110 | 73 | API-VAL-111 | Keep | maxLength boundaries versus null/empty classes. 092 is the Part endpoint. |
| API-VAL-111 | 73 | API-VAL-110 | Keep | Null, empty and whitespace classes on optional fields versus length boundaries. |
| API-VAL-112 | 55 | API-VAL-109 | Keep | Name content classes (special, Unicode, padding) versus presence and length classes. |
| API-VAL-113 | 56 | API-VAL-098 | Keep | Category fields versus Part fields. 116 combines fields. 114 is read-only fields. |
| API-VAL-114 | 50 | API-VAL-113 | Keep | Read-only fields (R-VAL-15, proposed accepted) versus wrong types (R-VAL-10, proposed rejected). |
| API-VAL-116 | 52 | API-VAL-113 | Keep | Several invalid fields reported in one response versus one field per request. |
| API-VAL-117 | 51 | API-VAL-109 | Keep | Form-urlencoded and multipart channels versus JSON. |
| API-VAL-119 | 54 | API-VAL-103 | Keep | Category PUT (R-VAL-13, R-CRUD-08) versus Part PUT (R-VAL-01, R-CRUD-03). |

API-VAL-115, 118, 120, 121, 122 and 123 have no Duplicate check line, so they are unique.

## Questions for the architect

1. **Nullable `parent` and `default_location` (API-VAL-111).** The `parent null` and `default_location null` rows expect `201 Created` as fact from the schema's `nullable: true` ([L3525](../../requirements/openapi-parts.yaml#L3525), [L3537](../../requirements/openapi-parts.yaml#L3537)). The cited R-VAL-14 covers only `description`, `default_keywords` and `icon`, and no VAL rule states that these two are nullable. Should the inventory get a rule for them, or should the rows be proposed under Q-VAL-19?
2. **R-VAL-13 "on create" applied to PUT (API-VAL-119).** R-VAL-13 says `name` is required on create. The case applies it to `PUT` through the schema's `required` list, which the PUT request body shares ([L1348](../../requirements/openapi-parts.yaml#L1348)). Is R-VAL-13 meant to cover full-body updates too, or should the `name absent` row's "not updated" outcome be proposed under Q-VAL-23?
3. **Read-only "not stored" outcome (API-VAL-114, API-VAL-121).** The statement that a client value for a read-only field is never stored comes from the `readOnly` marker and from R-VAL-11's wording, which is about Part fields. R-VAL-15 only lists the fields. Do you accept this as a rule outcome, or should it be proposed under Q-VAL-21?
