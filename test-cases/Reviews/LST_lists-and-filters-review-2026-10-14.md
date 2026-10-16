# Review: Lists and filters (API), 2026-10-14

**Cases reviewed:** API-LST-001 to API-LST-072 (72 cases, `test-cases/API_Lists_and_Filters/lists-and-filters.md`) · **Verdict:** Changes required

## Coverage

`python tools/coverage_check.py --area LST --file test-cases/API_Lists_and_Filters/lists-and-filters.md`: Rules: 16 · covered: 16 · not cited by any case: 0 (exit 0, no unknown rule IDs).

Every rule is cited, but three rules are only partly tested (depth gaps below). List endpoints have no `{id}` in their path, so the seed's `404 Not Found` standing rule does not apply. No LST rule is a permission rule (permissions sit in SEC).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-LST-01 | 001, 008, 013 | Covered | None. 013 expects a plain array per Schema issue 8 (answered). |
| R-LST-02 | 001-004, 008-013, 064 | Covered | Boundaries 0 / 1 / count / count + 1 / far above, negative and wrong type are all present. |
| R-LST-03 | 005-008, 064 | Covered | No case below the lower boundary (`offset=-1`). Minor; not in Q-LST-04. |
| R-LST-04 | 026-033, 064 | Covered, **partial** | Only 5 of the 10 searched fields have a case (name, IPN, description, keywords, category name). **No case for** `manufacturer_parts__MPN`, `revision`, `supplier_parts__SKU`, `tags__name`, `tags__slug`. Major. |
| R-LST-05 | 017-022, 064 | Covered | Positive (every `enum` member), `-` prefix and invalid value are present. |
| R-LST-06 | 036-042 | Covered | Numeric, `null`, unknown ID and wrong type are present. |
| R-LST-07 | 037-039 | Covered | On, off and omitted are present. |
| R-LST-08 | 043-046, 062, 063 | Covered | true, false, omitted and invalid are present. |
| R-LST-09 | 047-050 | Covered | None. |
| R-LST-10 | 051-053 | Covered | None. |
| R-LST-11 | 054-059 | Covered | Malformed date tested on `created_after` only. Minor. |
| R-LST-12 | 060, 061, 063 | Covered | All ten flags, true and false. |
| R-LST-13 | 062-064 | Covered | Depends on Q-LST-07; see finding 4. |
| R-LST-14 | 014-016, 023-025 | Covered | Category `ordering` values `pathstring`, `level`, `tree_id`, `lft` are never sent. Minor. |
| R-LST-15 | 065-072 | Covered, **partial** | **No case for `starred`**. Major. `top_level=false` has no case. Minor. |
| R-LST-16 | 034, 035 | Covered, **partial** | **No case for the `description` field**. Major. No category-search no-match case. Minor. |

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | API-LST-028 | No assumptions | The term `QA-<suffix> sprocket` is only part of the description `QA-<suffix> sprocket description`. The case asserts `count` `1` as known, but whether `search` matches part of a value is open in Q-LST-03. The case is not marked. | R-LST-04 note "partial matching not stated"; Q-LST-03; openapi-parts.yaml#L687-L691 | Search the full description, or mark `Draft · Open question: Q-LST-03` and make the result Not known. |
| 2 | Blocker | API-LST-035 | No assumptions | `QA-<suffix> Grand` is expected because its `pathstring` *starts with* the term. That assumes partial matching for category search, which no source states and no open question covers (Q-LST-03 is about the part list only). | R-LST-16; openapi-parts.yaml#L911-L914 | Raise a question on category-search matching, or search Grand's full `pathstring` so the pathstring clause is tested without partial matching. |
| 3 | Blocker | API-LST-040 | No assumptions / Open-question marking | The case states "`QA-<suffix> No Cat` is in the results" as known. It narrows with `search=QA-<suffix>`, a fragment of the name (Q-LST-03), so the result is not known. The case is marked only Q-LST-06 and Q-LST-07. | Q-LST-03; R-LST-04 | Add Q-LST-03 to the Review field and the Not known text, or narrow the list without `search`. |
| 4 | Major | 001-007, 013, 017-019, 026-031, 036, 043, 044, 047-052, 054-056, 060, 061 (systemic) | No assumptions / Open-question marking | Every case scopes the list with `category=<cat pk>`, adds another filter, `search`, `ordering` or pagination, and asserts exact results. That needs filters to combine (R-LST-13), which the inventory says to "confirm before writing cases" and which is open in Q-LST-07. API-LST-062 sends the same request as API-LST-043 but calls the outcome Not known, while 043 asserts `count` `1`. | R-LST-13 note; Q-LST-07 (asks about combining with `search`, `ordering`, `limit` and `offset` too) | Answer Q-LST-07. Then 062-064 can assert results. Otherwise mark the dependent cases. |
| 5 | Major | API-LST-060, API-LST-061 | Postconditions | `QA-<suffix> Only-locked` is locked. Cleanup patches it inactive and deletes it, but a locked part cannot be edited or deleted, so cleanup fails and leaves QA data. | R-REL-11; R-ATT-24 | Add `PATCH /api/part/<pk>/` `{"locked": false}` as `admin` before the cleanup of that part. |
| 6 | Major | API-LST-064 | Open-question marking | `search=QA-<suffix>` is a fragment of every part name (Q-LST-03), but the case is marked only Q-LST-07. | Q-LST-03 | Add Q-LST-03 (also to Q-LST-03's Affected cases). |
| 7 | Major | API-LST-007, API-LST-011, API-LST-045 | No assumptions | Before the Not known clause, each Expected result states an outcome the sources do not give: "`200 OK` is expected for an empty page", "The three parts are expected", "The filter is not applied, so Live and Dead are expected". An automator may assert these. | Q-LST-04, Q-LST-05; Not in schema #1 | Keep only the Not known text (and for 045 the facts that are stated). |
| 8 | Major | R-LST-04 | Coverage (gap) | No case for search on manufacturer MPN, revision, supplier SKU, tag name or tag slug. | openapi-parts.yaml#L690-L691 | Rerun test-case-creator for these five fields. |
| 9 | Major | R-LST-15 | Coverage (gap) | No case for the category `starred` filter. | openapi-parts.yaml#L917-L921 | Rerun the creator (needs a user who stars a category). |
| 10 | Major | R-LST-16 | Coverage (gap) | No case for category search on `description`. | openapi-parts.yaml#L914 | Rerun the creator. |
| 11 | Minor | API-LST-020 | Seed format | Each of the 16 steps makes two calls. The seed says one call per step. | seed-api-test-case.md "One call per step" | Split each step, or accept as an intentional table. |
| 12 | Minor | API-LST-054, API-LST-055 | Technique | Labelled Boundary value analysis, but the dates are far from any boundary. This is equivalence partitioning; the boundaries are 057/058. | R-LST-11 | Relabel. |
| 13 | Minor | API-LST-047 | Technique | "Boundary value analysis (IPN that is a prefix of another)": a prefix is not a boundary. | R-LST-09 | Relabel as Error guessing (prefix trap). |
| 14 | Minor | API-LST-008, API-LST-064 | Technique | "Exploratory" for scripted, fully specified checks. | seed Technique values | Use e.g. Equivalence partitioning / Decision table. |
| 15 | Minor | API-LST-068, API-LST-069, API-LST-070 | Specific Expected results | The category list is not scoped (`limit=100`), so the QA categories are expected on the first 100 rows. That depends on how many categories exist and on the maximum page size (Q-LST-04); 068's note relies on data observed elsewhere. | Q-LST-04 | Scope or order so the QA records are on the first page, or page until found. |
| 16 | Minor | API-LST-050 | Specific Expected results | "with an empty `IPN`" does not say whether `""` or `null` is expected (`IPN` has `default: ''`). | openapi-parts.yaml#L4164-L4167 | State the value. |
| 17 | Minor | API-LST-040 | Prerequisites | Says how `QA-<suffix> No Cat` is created, but not how `QA-<suffix> Cat` and `QA-<suffix> In Cat` are created or by whom. | seed Prerequisites | Complete the Data part. |
| 18 | Minor | 009, 010, 011, 012, 021, 022, 025, 041, 042, 046, 053, 059 | Summary | "handled in a defined way" says nothing checkable. It is acceptable while the outcome is open. | Seed Summary | Reword once the questions are answered. |
| 19 | Minor | R-LST-03, R-LST-11, R-LST-14, R-LST-15, R-LST-16 | Depth | No `offset=-1`; no malformed `created_before`; category ordering on `pathstring`/`level`/`tree_id`/`lft` never sent; no `top_level=false`; no category-search no-match. | see Coverage | Optional extra cases from the creator. |

Checked with no defect: every case has every seed field in order, the three-column Steps table, a rule ID with its source link, and a Review field of `Draft` or `Draft · Open question: ...`. Every case uses `reader` (view-only, the least-privileged demo user that can call a list) and creates its data as `admin`. API-LST-041 follows the standing rule (create, delete, reuse the `pk`). Every category delete sends both flags.

## Duplicates

70 cases scored 50 or more (API-LST-008 and API-LST-025 have no Duplicate check line). Every one has at least one real difference from each of its matches, so all are **Keep**. The verdict and reason are recorded in each case's `**Duplicate judgement:**` line.

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| 001 | 61 | 013 | Keep | `limit` sent (envelope) vs omitted (array) |
| 002 | 69 | 004 | Keep | Different boundary point (1 vs count + 1) |
| 003 | 83 | 004 | Keep | On the boundary (count) vs above it (count + 1) |
| 004 | 83 | 003 | Keep | Above the boundary vs on it |
| 005 | 51 | 001 | Keep | `offset` vs `limit` clause |
| 006 | 58 | 007 | Keep | `offset` 0 vs count |
| 007 | 58 | 006 | Keep | `offset` count vs 0 |
| 009 | 63 | 011 | Keep | `limit` 0 vs far above maximum |
| 010 | 70 | 012 | Keep | Negative vs non-numeric `limit` |
| 011 | 63 | 009 | Keep | Far above vs 0 |
| 012 | 70 | 010 | Keep | Wrong type vs negative |
| 013 | 61 | 001 | Keep | No `limit` vs `limit` |
| 014 | 65 | 016 | Keep | `limit` vs `offset` |
| 015 | 64 | 016 | Keep | No `limit` vs `offset` |
| 016 | 65 | 014 / 023 | Keep | `offset` vs `limit` / ordering |
| 017 | 86 | 018 | Keep | Ascending vs descending |
| 018 | 86 | 017 | Keep | Descending vs ascending |
| 019 | 77 | 017 / 018 | Keep | `id` vs `name` |
| 020 | 55 | 017 / 018 | Keep | All `enum` values accepted vs the order of one field |
| 021 | 76 | 022 | Keep | Non-existent name vs real field outside the whitelist |
| 022 | 76 | 021 | Keep | Real field vs non-existent name |
| 023 | 74 | 024 | Keep | `-name` vs `-part_count` |
| 024 | 74 | 023 | Keep | `-part_count` vs `-name` |
| 026 | 86 | 027 / 028 | Keep | Different searched field |
| 027 | 88 | 028 | Keep | IPN vs description |
| 028 | 88 | 027 | Keep | Description vs IPN |
| 029 | 87 | 027 / 028 | Keep | Keywords vs other fields |
| 030 | 71 | 026 | Keep | Category name (2 results) vs part name |
| 031 | 61 | 052 | Keep | `search` vs `name_regex` no-match |
| 032 | 80 | 033 | Keep | Letter case vs fragment |
| 033 | 80 | 032 | Keep | Fragment vs letter case |
| 034 | 75 | 035 | Keep | `name` vs `pathstring` |
| 035 | 75 | 034 | Keep | `pathstring` vs `name` |
| 036 | 62 | 040 | Keep | Numeric vs `null` |
| 037 | 70 | 038 | Keep | `cascade` true vs false |
| 038 | 70 | 037 | Keep | false vs true |
| 039 | 67 | 037 | Keep | `cascade` omitted vs sent |
| 040 | 62 | 036 | Keep | `null` vs numeric |
| 041 | 70 | 042 | Keep | Unknown ID vs wrong type |
| 042 | 70 | 041 | Keep | Wrong type vs unknown ID |
| 043 | 77 | 044 | Keep | true vs false (see finding 4 on overlap with 062) |
| 044 | 77 | 043 | Keep | false vs true |
| 045 | 64 | 044 | Keep | Omitted vs sent |
| 046 | 58 | 042 / 059 | Keep | Different parameter |
| 047 | 68 | 050 | Keep | `IPN` vs `has_ipn` clause |
| 048 | 68 | 052 | Keep | `IPN` vs `name_regex` no-match |
| 049 | 70 | 050 | Keep | true vs false |
| 050 | 70 | 049 | Keep | false vs true |
| 051 | 53 | 049 / 054 / 055 / 056 | Keep | Only `name_regex` match case |
| 052 | 68 | 048 | Keep | Different parameter |
| 053 | 56 | 052 | Keep | Malformed vs valid regex |
| 054 | 83 | 055 | Keep | `created_after` vs `created_before` |
| 055 | 83 | 054 | Keep | `created_before` vs `created_after` |
| 056 | 78 | 054 | Keep | Range, all returned vs single bound, none |
| 057 | 84 | 058 | Keep | `created_after` vs `created_before` on boundary |
| 058 | 84 | 057 | Keep | `created_before` vs `created_after` on boundary |
| 059 | 59 | 042 | Keep | Different parameter |
| 060 | 79 | 061 | Keep | Flags true vs false |
| 061 | 79 | 060 | Keep | Flags false vs true |
| 062 | 77 | 063 | Keep | `category` x `active` vs `assembly` x `active`. Same request as 043 but with an extra part in another category (finding 4) |
| 063 | 77 | 062 | Keep | Different filter pair |
| 064 | 50 | 062 | Keep | Search/order/paging vs two filters |
| 065 | 71 | 066 | Keep | `cascade` false vs true |
| 066 | 71 | 065 | Keep | true vs false |
| 067 | 66 | 065 / 066 | Keep | Omitted vs sent |
| 068 | 73 | 069 | Keep | `top_level` vs `structural` |
| 069 | 78 | 070 | Keep | `structural` true vs false |
| 070 | 78 | 069 | Keep | false vs true |
| 071 | 60 | 072 | Keep | `depth` vs `name` |
| 072 | 65 | 067 | Keep | `name` vs `parent` |

## Questions for the architect

1. **Q-LST-07 (filters combining)** decides whether about 40 cases can assert exact results (finding 4). Answering it, at least for "`category` plus one more filter or pagination", settles most of them. It also settles whether 062-064 can drop their marking.
2. **Category search matching:** no open question covers whether category `search` (R-LST-16) is case-insensitive or matches part of a value. Should Q-LST-03 be widened to the category list, or a new Q-LST question added? API-LST-035 depends on it.
3. **Q-LST-03 Affected cases** lists only 032 and 033. API-LST-028, API-LST-040 and API-LST-064 also depend on it (and 035, if the question is widened).
4. **Inventory notes look stale:** R-LST-01's note still says the response without `limit` is "not stated (Not in schema #7)", but the index says Schema issue 8 answered it (a plain array). R-LST-13's note says "Confirm before writing cases". Please confirm or update them.
5. **Negative `offset`:** Q-LST-04 does not ask about `offset=-1`. Add it if a below-boundary case is wanted.
