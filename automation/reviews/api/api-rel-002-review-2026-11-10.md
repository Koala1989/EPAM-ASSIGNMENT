# Review: API-REL-002 Delete a category that has a child category

| Item | Value |
|---|---|
| Spec | `tests/api/REL/api-rel-002.spec.ts` |
| Case | `test-cases/API_Relationships/part-and-category-crud.md` (API-REL-002), Review: Approved · 2026-10-13 |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-11-10 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 1 Info |

## A. Automated checks

| Check | Scope | Result |
|---|---|---|
| `npm run typecheck` | whole project | Pass (exit 0, no errors) |
| `npx eslint` | `tests/api/REL/api-rel-002.spec.ts`, `clients/categories.client.ts`, `clients/base.client.ts`, `clients/index.ts`, `fixtures/index.ts`, `fixtures/api.fixture.ts`, `fixtures/data.fixture.ts`, `fixtures/expect.ts`, `fixtures/user.fixture.ts` | Pass (exit 0, no errors or warnings) |
| `npm run lint` | whole project | Fails (exit 1), only on files outside this review: 1 error at `tests/ui/Categories/ui-categories-009.spec.ts:40:59`, plus warnings in `tests/api/VAL/api-val-087.spec.ts` and `tests/ui/Detail_View/ui-detail_view-088.spec.ts` (see Outside scope). This spec and its framework files have none. |
| `npx playwright test tests/api/REL/api-rel-002.spec.ts --list` | spec | 1 test in project `api` (`Part and category CRUD › API-REL-002: Delete a category that has a child category`), after the `api-smoke` setup |

The tests were not run (reviewer guardrail).

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `GET /api/part/category/<parent pk>/` as `admin` | `200 OK`. `subcategories` is `1`. | `1. GET /api/part/category/<parent pk>/ as admin` (spec:11) | `await expect(res).toHaveStatus(200)` (spec:13); `expect(body.subcategories).toBe(1)` (spec:15) | Covered |
| 2 | `DELETE /api/part/category/<parent pk>/` as `admin`, `{"delete_parts": false, "delete_child_categories": false}` | `204 No Content`. The body is empty. | `2. DELETE /api/part/category/<parent pk>/ as admin` (spec:18) | `await expect(res).toHaveStatus(204)` (spec:20); `expect(await res.text()).toBe('')` (spec:21) | Covered |
| 3 | `GET /api/part/category/<parent pk>/` as `admin` | `404 Not Found`. Body is `{"detail": "No PartCategory matches the given query."}`. | `3. GET /api/part/category/<parent pk>/ as admin` (spec:24) | `await expect(res).toHaveStatus(404)` (spec:26); `expect(await res.json()).toEqual({ detail: 'No PartCategory matches the given query.' })` (spec:27) | Covered |
| 4 | `GET /api/part/category/<child pk>/` as `admin` | `200 OK`. The child is kept; `parent` is `null` and `level` is `0`. | `4. GET /api/part/category/<child pk>/ as admin` (spec:30) | `await expect(res).toHaveStatus(200)` (spec:32); `expect(body.parent).toBeNull()` (spec:34); `expect(body.level).toBe(0)` (spec:35) | Covered (see finding 1 on the source of the `level` value) |

No Missing, Weakened or Extra rows. For "the child is kept", the `200` on `retrieve(child.pk)` (spec:31-32) is enough proof: a deleted category returns `404` (step 3). A `pk` check like the one in api-rel-001.spec.ts:27 would add nothing.

- **Request fidelity:** step 2 calls `api.categories.destroy(parent.pk, { delete_parts: false, delete_child_categories: false })` (spec:19), which is the case's method, endpoint and payload exactly. `ResourceClient.destroy` (base.client.ts:43-45) sends the body unchanged. Steps 1, 3 and 4 call `retrieve` with no parameters (spec:12, :25, :31), as the case states, against the parent, the parent and the child.
- **Order and titles:** four steps in the case's order, each titled `<n>. <request>` with the case's Request text, word for word.
- **Prerequisites:** `test.use({ user: 'admin' })` (spec:4) matches "User: `admin`". The case's data, `QA-<suffix> Parent` and `QA-<suffix> Child` with `parent` set to the parent's `pk`, is created as admin with `data.category(data.name('Parent'))` (spec:8) and `data.category(data.name('Child'), { parent: parent.pk })` (spec:9). The parent has no `parent`, so it is top-level, which step 4's Expected result requires. The case changes no settings and the spec changes none. The `api` fixture does the admin token pre-step.
- **Cleanup:** the request under test creates nothing, so no `track*` call is needed. `data.category` registers both prerequisites (data.fixture.ts:32-36). Cleanup runs in reverse order (data.fixture.ts:125). First the child is deleted with both flags `false` (data.fixture.ts:104), which is the case's Postconditions exactly. Then the parent's cleanup DELETE gets `404`, because step 2 already removed it, and `remove()` accepts that (data.fixture.ts:137). If step 2 fails, both records are still removed, child first.
- **Schema:** no step states a schema component, so leaving out `toMatchSchema` is correct. `openapi-parts.yaml` gives `GET /api/part/category/{id}/` only `200 Category` (L1326-1331) and `DELETE` only `204: No response body` (L1424-1426), with no `404` response. The asserted fields agree with `Category`: `subcategories` is an integer, read-only and nullable (L3547-3550), `level` is a read-only integer (L3534-3536), and `parent` is a nullable integer (L3537-3541), so `null` is a valid value.
- **Expected values vs. sources:** the delete flags and "children move up; under a top-level parent they get `parent` `null`" match Q-CRUD-03 (answered, `open-question_CRUD.md:7`) and CONVENTIONS API §10 "Deleting a category". The 404 body matches API §10 "Not found" (Q-CRUD-01). No answered question or inventory rule backs the `level` `0` value (finding 1).
- **Traceability:** the first line is `// case: test-cases/API_Relationships/part-and-category-crud.md (API-REL-002)`. The test title matches the case heading. `describe('Part and category CRUD')` matches the case file's title and the sibling api-rel-001.spec.ts. Tags `['@regression']` match "Regression". The case has no Data sets table, so it is not data-driven.
- **Review status:** Approved · 2026-10-13.
- **Fixme:** none.

## C. Conventions

- API §3: file path and name, the one-line header, the single fixtures import, `test.use`, `describe`, one test, `data.*` first, one step per case step, status first, values checked with `toBe`/`toEqual`/`toBeNull`, follow-up GETs to prove the business rule. All pass.
- API §4: no new client code. The spec uses only the inherited `retrieve` and `destroy` on the existing `CategoriesClient` (categories.client.ts:5-9, constructor and endpoint only), which is unchanged.
- API §5: `api` and `data` come through `fixtures/index.ts`. The case has one caller, so `apiAs` is not needed.
- API §7 and Shared §3: no hosts, URLs, hard-coded IDs or credentials. The pks come from the created records.
- API §8: no demo data, unique `QA-` names, and both records are registered for cleanup.
- API §9: file, title, step titles and tags are named correctly.

No findings (see Findings).

## D. SOLID and design

- Single responsibility: one spec for one case, and `CategoriesClient` models one resource.
- Open/closed and Liskov substitution: no client was changed. `ResourceClient` keeps its contract: raw response, no assertions, payload unchanged.
- Interface segregation: the spec requests only `api` and `data`, and uses both.
- Dependency inversion: the spec depends only on clients and fixtures. It has no endpoint strings and no request context.
- Duplication: steps 2-3 (spec:18-28) repeat api-rel-001.spec.ts:11-21 almost line for line. That comes from the two cases, which state the same delete and 404 check. The assertions belong in each spec (API §3), so there is no shared logic to extract.

No findings (see Findings).

## E. Playwright and TypeScript practice

- Every promise is awaited (spec:8, 9, 11, 12, 13, 14, 18, 19, 20, 21, 24, 25, 26, 27, 30, 31, 32, 33). The synchronous `expect`s (spec:15, 34, 35) check values that are already parsed.
- No conditionals, loops, `try/catch` or `test.only`.
- Isolation: the test creates its own two categories and does not depend on demo data, other tests or test order.
- TypeScript: `const` only, no casts, no non-null assertions. `parent.pk` and `child.pk` are typed `number` through `ApiRecord`. `body` (spec:14, :33) is Playwright's untyped `res.json()`, the pattern API §3 prescribes.
- Readability: the spec reads like the case. The flags, the 404 message, `1`, `null` and `0` are all the case's own values, so there are no unexplained magic values.

No findings (see Findings).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/api/REL/api-rel-002.spec.ts:35` | CLAUDE.md "Never assume a requirement"; reviewer guardrail 4 (the case is the yardstick) | `expect(body.level).toBe(0)` checks the case's step 4 value, `level` is `0`, faithfully, but no documented source backs that value. R-CRUD-10 (`API_Create_Read_Update_Delete/requirements-inventory.md:16`) says nothing about child categories. The answered Q-CRUD-03 (`open-question_CRUD.md:7`) states only that children get `parent` `null`. Q-REL-05 (`open-question_REL.md:9`), which asks exactly whether a top-level category's `level` is 0 or 1, is still **Open**. API-REL-025's Notes (`relationships.md:674`) say that API-REL-002's `level` `0` "is not a documented rule". The spec matches the Approved case, so this is not a spec defect. Removing the assertion would make step 4 Weakened. | No spec change. The architect decides: answer Q-REL-05, which would back `level` `0`, or change API-REL-002 step 4. If the case value changes, the spec follows. |

## Outside scope

- `test-cases/API_Relationships/part-and-category-crud.md:39` (the case's Requirement field) cites `open-question_REL.md Q-CRUD-03`, but Q-CRUD-03 is in `test-cases/Open_Questions/open-question_CRUD.md:7`. API-REL-001 at `:8` has the same wrong reference.
- API-REL-002 (Approved) asserts `level` `0` while Q-REL-05, which asks for that value, is Open, and the Draft case API-REL-025 relies on that open question (finding 1). The case set needs to agree on one source for the value.
- `npm run lint` fails for the project because of other specs: `tests/ui/Categories/ui-categories-009.spec.ts:40:59` has the error `playwright/valid-expect` ("Matchers must be called to assert"). There are warnings `playwright/no-conditional-in-test` and `no-conditional-expect` in `tests/api/VAL/api-val-087.spec.ts:16-32`, and `playwright/no-useless-not` in `tests/ui/Detail_View/ui-detail_view-088.spec.ts:15:50`.
- No problems noticed in the framework code this spec uses (`clients/base.client.ts`, `clients/categories.client.ts`, `clients/index.ts`, `fixtures/api.fixture.ts`, `fixtures/data.fixture.ts`, `fixtures/expect.ts`, `fixtures/index.ts`, `fixtures/user.fixture.ts`).
