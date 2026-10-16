# Review: Security and permissions: authentication and role permissions on parts, categories and supplier parts (API), 2026-10-15

**Cases reviewed:** API-SEC-001 to API-SEC-050 (50 cases, `test-cases/API_Security_and_Permissions/authentication-and-role-permissions.md`) · **Verdict:** Changes required

## Coverage

`python tools/coverage_check.py --area SEC --file test-cases/API_Security_and_Permissions/authentication-and-role-permissions.md`: Rules: 9 · covered: 9 · not cited by any case: 0 (exit 0, no unknown rule IDs).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-SEC-01 | 001-008, 010, 011 | Covered | Anonymous access is tested only on `GET /api/part/`, `POST /api/part/`, `GET /api/part/category/`, `GET /api/company/part/` and the token endpoint; no anonymous `PATCH`/`PUT`/`DELETE` and no anonymous category write. Positive cases exist for basic and token auth only; session cookie and OAuth2 (both named in the rule) have none (Minor, see Questions). |
| R-SEC-02 | 009-013 | Covered | Good depth (positive, no credentials, wrong password, reissue, user without roles). 012 relies on an undefined "matching" (finding 4). |
| R-SEC-03 | 007, 008, 014-017 | Covered | List and detail, granted and blocked: complete. |
| R-SEC-04 | 002, 018-020, 050 | Covered | Positive only with `engineer`, whose add permission is open (Q-SEC-04); no unconditional positive (e.g. `allaccess`). Minor. |
| R-SEC-05 | 021-024 | Covered | No positive `PUT` (only `PATCH` 021); negatives cover both methods. Minor. |
| R-SEC-06 | 025-028 | Covered | Complete (granted, view-only, no roles, engineer unknown). |
| R-SEC-07 | 003, 029-040 | Covered | No positive category detail `GET /api/part/category/{id}/`; no category `PUT` case (positive or negative). Minor. |
| R-SEC-08 | 041-044 | Covered | The column that matters for "both scopes" (Parts add granted, Purchase Orders add missing) is only 044, whose outcome is Not known. Part P is not made purchaseable (finding 1). |
| R-SEC-09 | 045-049 | Covered | Used as a stand-in rule for supplier part view, change and delete, which have no inventory rule (finding 3). 049 is a 404 case, not a scope mapping (finding 2). |

404 standing rule: the six `{id}` operations with `GET`/`DELETE` touched here (`/api/part/{id}/`, `/api/part/category/{id}/`, `/api/company/part/{id}/`) already have their 404 cases in other Areas: API-CRUD-009, API-CRUD-023, API-CRUD-018, API-CRUD-024, API-REL-035, API-REL-036. No 404 gap. Negative cases exist (most of the set).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Major | API-SEC-041 (and the Part P setup of 042, 043, 044, 047, 048, 049) | No assumptions / Fidelity | Part P is created with only `name` and `description`; `purchaseable` is not set and the schema gives no default. If Part P is not purchaseable, the `allaccess` create in 041 may be rejected for a reason unrelated to permissions (API-REL-034 proposes exactly that, Q-REL-06), and the negative cases could pass for the wrong reason. | `Part.purchaseable` has no `default` ([openapi-parts.yaml#L4204](../../../requirements/openapi-parts.yaml#L4204)); API-REL-034, Q-REL-06 | Edit the supplier-part cases' Data to create Part P with `"purchaseable": true`, or rerun the creator for these cases. |
| 2 | Blocker | API-SEC-049 | Fidelity / No assumptions / Duplicate | (a) Cites R-SEC-09 (how scopes read), which says nothing about not-found; the case is not a security case. (b) Expected body `{"detail": "No SupplierPart matches the given query."}` is stated as fact, but the model name for this endpoint is unconfirmed (its own Notes say "confirm on first run"; API-REL-035 says "the model name for this endpoint was not confirmed"). (c) Same operation, same expected `404` as API-REL-035; only the user differs (`allaccess` vs `admin`), which is not a real difference for a not-found check. (No `Duplicate check` line, so the dedupe run did not compare across files.) | R-SEC-09 ([openapi-parts.yaml#L6112](../../../requirements/openapi-parts.yaml#L6112)); seed standing rule "Not found"; API-REL-035 | Reject API-SEC-049 as a duplicate of API-REL-035 (architect decision), or at minimum drop the model name from the body assertion and re-cite. |
| 3 | Major | API-SEC-045, 046, 047, 048 (and 049) | Fidelity | They cite R-SEC-09, a scope-reading rule, as the requirement that supplier part view, change and delete need `r:*:part` and `r:*:purchase_order`. That requirement is stated only by the schema scopes; no inventory rule holds it (R-SEC-08 covers create only). The case Notes admit the gap. | [openapi-parts.yaml#L176-L177](../../../requirements/openapi-parts.yaml#L176), [#L307-L308](../../../requirements/openapi-parts.yaml#L307), [#L394-L395](../../../requirements/openapi-parts.yaml#L394), [#L426-L427](../../../requirements/openapi-parts.yaml#L426) | Architect: add inventory rules for supplier part view/change/delete permissions (see Questions), then have the cases cite them. |
| 4 | Major | API-SEC-012 | No assumptions / Open-question marking | Step 4 states as fact that a second call with the same `name` deletes T1 ("The matching token was deleted"). The schema does not define "matching"; same-name matching is assumed. The Open note points Q-SEC-05 at the no-`name` variant, which this case does not exercise, so the actual unknown is unmarked. | [openapi-parts.yaml#L3468](../../../requirements/openapi-parts.yaml#L3468); Q-SEC-05 | Edit step 4: state the rule ("a matching token is deleted"), then `Open: Q-SEC-05 (whether a token with the same name counts as matching)`; widen Q-SEC-05 accordingly. |
| 5 | Major | API-SEC-047 | Specific Expected results | Step 2: "`note` is still empty or absent as created": two allowed outcomes, no exact value. `SupplierPart.note` is `nullable`, so the created value may be `null` or `""`. | `SupplierPart.note` ([openapi-parts.yaml#L6003](../../../requirements/openapi-parts.yaml#L6003)) | Edit: "`note` equals the value returned when `admin` created the supplier part (Data)". |
| 6 | Major | API-SEC-013 step 2 | Specific Expected results | Expected result is conditional ("Not executed if step 1 returned no token") and only a cross-reference ("see API-SEC-016"), with no status or check of its own. | Seed: "Never 'succeeds'"; each step states its outcome | Edit step 2 to state its outcome (Part P not returned, `Open: Q-SEC-02`) or drop the step, since API-SEC-016 covers it. |
| 7 | Major | API-SEC-025, 032, 034, 037, 041 | Open-question marking | Inconsistent: 037 (`allaccess` deletes a category) is marked Q-SEC-03 because the schema also lists `r:delete:build`, but 025, 032, 034 and 041 (`allaccess`, same dual-scope situation) are not. Either the Build role is a question for `allaccess` (all five) or it is not (none). Also Q-SEC-04 asks which roles `allaccess` holds, yet no `allaccess` case is marked with it. | Q-SEC-03, Q-SEC-04; scopes [#L2819-L2820](../../../requirements/openapi-parts.yaml#L2819), [#L974-L975](../../../requirements/openapi-parts.yaml#L974), [#L1397-L1398](../../../requirements/openapi-parts.yaml#L1397), [#L1422-L1423](../../../requirements/openapi-parts.yaml#L1422) | Architect: decide whether `allaccess` role holdings are settled by the seed's demo user table ("Full create, edit and delete"); then align the markings. |
| 8 | Minor | API-SEC-006 | Rule outcome stated | The rejection is labelled "Proposed", but R-SEC-01 (no anonymous access) plus the required "Token" prefix already state it: a request not authenticated is rejected. Only the status code is unknown. | [openapi-parts.yaml#L6232](../../../requirements/openapi-parts.yaml#L6232); R-SEC-01 | Edit: "The request is rejected (R-SEC-01). Open: Q-SEC-01 (status code and error body)." |
| 9 | Minor | API-SEC-009 | User | `engineer` is not the least-privileged user that can retrieve a token; `reader` would do (`noaccess` is open, Q-SEC-04). The unnamed reissue may also invalidate `engineer` tokens held by other tests running in parallel (Q-SEC-05). | R-SEC-02; seed Prerequisites rule | Edit user to `reader` with a `name` parameter, or note the side effect. |
| 10 | Minor | API-SEC-035 | Specific Expected results | "`description` is still empty" assumes Category C's default description; Category C is created with no stated payload. | Conventions block of the case file | Edit: compare with the `description` returned at creation. |
| 11 | Minor | API-SEC-049 | Technique | `Not found (API)` is not one of the seed's techniques. | `seed-manual-test-case.md` line 17 | Covered by finding 2. |
| 12 | Minor | R-SEC-01 | Depth | Anonymous access is not checked on any write method on `{id}` (`PATCH`, `PUT`, `DELETE`) or on category writes; session cookie and OAuth2 have no positive case. | R-SEC-01 | Architect: decide whether to add (rerun the creator) or accept the sample. |
| 13 | Minor | R-SEC-04, R-SEC-05, R-SEC-07 | Depth | No unconditional positive part create (only `engineer`, open); no positive part `PUT`; no positive category detail `GET`; no category `PUT` case. | R-SEC-04, R-SEC-05, R-SEC-07 | Rerun the creator for these optional depth cases if wanted. |
| 14 | Minor | API-SEC-007 | Format | The `reader` password is written in the case (`reader` / `readonly`). The seed's demo user table holds it too, but CLAUDE.md keeps credentials to `automation/config/` and `automation/data/`. | CLAUDE.md hard rules | Edit to "basic auth with `reader`'s credentials from the users file". |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| API-SEC-002 | 51 | API-SEC-020 | Keep | Unauthenticated (Q-SEC-01) vs authenticated without roles (Q-SEC-02). |
| API-SEC-007 | 66 | API-SEC-008 | Keep | Basic auth vs token auth. |
| API-SEC-008 | 66 | API-SEC-007 | Keep | Token vs basic; vs 014 a different rule (R-SEC-01 vs R-SEC-03). |
| API-SEC-014 | 59 | API-SEC-015 | Keep | List vs detail operation; vs 008 a different rule. |
| API-SEC-015 | 59 | API-SEC-014 | Keep | Detail vs list operation. |
| API-SEC-016 | 64 | API-SEC-017 | Keep | List vs detail; the list may return an empty list. |
| API-SEC-017 | 64 | API-SEC-016 | Keep | Detail vs list. |
| API-SEC-019 | 69 | API-SEC-020 | Keep | `reader` (view, no add) vs `noaccess` (no roles). |
| API-SEC-020 | 69 | API-SEC-019 | Keep | No roles vs view-only; vs 002 authenticated vs anonymous. |
| API-SEC-022 | 69 | API-SEC-024 | Keep | View-only vs no roles; vs 023 `PATCH` vs `PUT`. |
| API-SEC-023 | 59 | API-SEC-022 | Keep | `PUT` vs `PATCH`. |
| API-SEC-024 | 69 | API-SEC-022 | Keep | No roles vs view-only. |
| API-SEC-026 | 63 | API-SEC-027 | Keep | View-only vs no roles. |
| API-SEC-027 | 63 | API-SEC-026 | Keep | No roles vs view-only. |
| API-SEC-030 | 54 | API-SEC-031 | Keep | Category list vs detail. |
| API-SEC-031 | 54 | API-SEC-030 | Keep | Category detail vs list. |
| API-SEC-033 | 68 | API-SEC-036 | Keep | View-only vs no roles. |
| API-SEC-036 | 68 | API-SEC-033 | Keep | No roles vs view-only. |
| API-SEC-038 | 72 | API-SEC-039 | Keep | View-only vs no roles. |
| API-SEC-039 | 72 | API-SEC-038 | Keep | No roles vs view-only. |
| API-SEC-042 | 68 | API-SEC-043 | Keep | View-only vs no roles. |
| API-SEC-043 | 68 | API-SEC-042 | Keep | No roles vs view-only. |

Not scored (no `Duplicate check` line) but a cross-Area duplicate found while reading: API-SEC-049 vs API-REL-035 (finding 2).

## Questions for the architect

1. Supplier part view, change and delete permissions (schema scopes at L176, L307, L394, L426) have no inventory rule. Should rules be added (e.g. R-SEC-10 to R-SEC-12) so that API-SEC-045 to 048 can cite them instead of R-SEC-09?
2. Does the seed's demo user table ("allaccess: Full create, edit and delete", "engineer: Part management", "reader: View-only", "noaccess: No permissions") settle part of Q-SEC-04, in particular for `allaccess`? This decides whether the `allaccess` positives need Q-SEC-03/Q-SEC-04 marking (finding 7).
3. Are session cookie and OAuth2 authentication in scope for R-SEC-01 positive cases, or is basic plus token enough?
4. Q-SEC-05 asks about calls without `name`; should it also ask whether a call with the same `name` counts as "matching" (API-SEC-012)?
5. Should Part P in the supplier-part cases be created with `purchaseable: true` (finding 1), given Q-REL-06 is open?
