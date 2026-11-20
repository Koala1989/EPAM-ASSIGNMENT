# Review: API-REL-001 Delete a category that contains a part

| Item | Value |
|---|---|
| Spec | `tests/api/REL/api-rel-001.spec.ts` |
| Case | `test-cases/API_Relationships/part-and-category-crud.md` (API-REL-001), Review: Approved · 2026-10-13 |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-11-10 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 1 Info |

## A. Automated checks

| Check | Scope | Result |
|---|---|---|
| `npm run typecheck` | whole project | Pass (exit 0, no errors) |
| `npx eslint` | `tests/api/REL/api-rel-001.spec.ts`, `clients/categories.client.ts`, `clients/parts.client.ts`, `clients/base.client.ts`, `clients/index.ts`, `fixtures/index.ts`, `fixtures/api.fixture.ts`, `fixtures/data.fixture.ts`, `fixtures/expect.ts`, `fixtures/user.fixture.ts` | Pass (exit 0, no errors or warnings) |
| `npm run lint` | whole project | Fails, but only on files outside this review: 1 error in `tests/ui/Categories/ui-categories-009.spec.ts:40:59`, warnings in `tests/api/VAL/api-val-087.spec.ts` and `tests/ui/Detail_View/ui-detail_view-088.spec.ts` (see Outside scope). Nothing in this spec or its framework files. |
| `npx playwright test tests/api/REL/api-rel-001.spec.ts --list` | spec | 1 test in project `api` (`Part and category CRUD › API-REL-001: Delete a category that contains a part`), after the `api-smoke` setup |

The tests were not run (reviewer guardrail).

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `DELETE /api/part/category/<category pk>/` as `admin`, `{"delete_parts": false, "delete_child_categories": false}` | `204 No Content`. The body is empty. | `1. DELETE /api/part/category/<category pk>/ as admin` (spec:11) | `await expect(res).toHaveStatus(204)` (spec:13); `expect(await res.text()).toBe('')` (spec:14) | Covered |
| 2 | `GET /api/part/category/<category pk>/` as `admin` | `404 Not Found`. Body is `{"detail": "No PartCategory matches the given query."}`. | `2. GET /api/part/category/<category pk>/ as admin` (spec:17) | `await expect(res).toHaveStatus(404)` (spec:19); `expect(await res.json()).toEqual({ detail: 'No PartCategory matches the given query.' })` (spec:20) | Covered |
| 3 | `GET /api/part/<part pk>/` as `admin` | `200 OK`. The part is kept; `category` is `null`. | `3. GET /api/part/<part pk>/ as admin` (spec:23) | `await expect(res).toHaveStatus(200)` (spec:25); `expect(body.pk).toBe(part.pk)` (spec:27); `expect(body.category).toBeNull()` (spec:28) | Covered |

No Missing, Weakened or Extra rows. The `pk` check at spec:27 is evidence for "the part is kept" (the record returned is the prerequisite part), so it is not Extra.

- **Request fidelity:** step 1 calls `api.categories.destroy(category.pk, { delete_parts: false, delete_child_categories: false })` (spec:12). That is the case's method, endpoint and payload exactly, and `ResourceClient.destroy` (base.client.ts:43-45) sends the body unchanged. Steps 2 and 3 call `retrieve` (spec:18, spec:24) with no parameters, as the case states.
- **Order and titles:** three steps, in the case's order, titled `<n>. <request>` with the case's Request text.
- **Prerequisites:** `test.use({ user: 'admin' })` (spec:4) matches "User: `admin`". The case asks for category `QA-<suffix> Category` and part `QA-<suffix> Child Part` in it, created as admin. The spec creates them with `data.category(data.name('Category'))` (spec:8) and `data.part(data.name('Child Part'), { category: category.pk })` (spec:9). The category has no `parent`, so it is top-level, as step 3's Expected result assumes. Settings: none, and none are changed. The admin token pre-step is done by the `api` fixture.
- **Cleanup:** the request under test creates no record, so no `track*` call is needed. Both prerequisites are registered by the `data` fixture (data.fixture.ts:32-42). Cleanup runs in reverse order. The part goes first, through `deletePart` (made inactive, then deleted, data.fixture.ts:141-153), which matches the case's Postconditions. Then the category: the cleanup DELETE gets `404` because step 1 already removed it, and `remove()` accepts that (data.fixture.ts:137). If step 1 fails, the cleanup still removes both records.
- **Schema:** the case states no schema component. `openapi-parts.yaml` gives `DELETE /api/part/category/{id}/` only `204: No response body` (L1424-1426) and `GET /api/part/category/{id}/` only `200 Category` (L1326-1331), with no `404`. Leaving out `toMatchSchema` is correct.
- **Expected values vs. sources:** the 404 body matches `open-question_CRUD.md` Q-CRUD-01 (answered) and CONVENTIONS API §10 "Not found". The delete flags and the "parts move up, top-level gives `category` `null`" outcome match Q-CRUD-03 (answered) and API §10 "Deleting a category".
- **Traceability:** the first line is `// case: test-cases/API_Relationships/part-and-category-crud.md (API-REL-001)`. The title matches the case heading. `describe('Part and category CRUD')` matches the case file's title. Tags `['@regression']` match "Regression". The case has no Data sets table, so it is not data-driven.
- **Review status:** Approved · 2026-10-13.
- **Fixme:** none.

## C. Conventions

- API §3: file path and name, one-line header, single fixtures import, `test.use`, `describe`, one test, `data.*` first, one step per case step, status first, values with `toEqual`/`toBe`/`toBeNull`, follow-up GETs as the business-rule proof. All pass.
- API §4: there is no new client code. The spec uses only the inherited `destroy` and `retrieve` on the existing `CategoriesClient` and `PartsClient`, which are unchanged (each is a constructor with its endpoint only).
- API §5: `api` and `data` come through `fixtures/index.ts`. No `apiAs` is needed because the case has a single caller.
- API §7 and Shared §3: no hosts, URLs, IDs or credentials. The pks come from the created records.
- API §8: no demo data, unique `QA-` names, and both records are registered for cleanup.
- API §9: naming of the file, title, step titles and tags. All pass.

No findings (see Findings).

## D. SOLID and design

- Single responsibility: one spec for one case. Each client models one resource.
- Open/closed and Liskov substitution: no client was changed. `ResourceClient` keeps its contract: it returns the raw response, makes no assertions and sends the payload unchanged.
- Interface segregation: the spec requests only `api` and `data`, and uses both.
- Dependency inversion: the spec depends on clients and fixtures only, with no endpoint strings or request context.
- Duplication: steps 1-2 repeat `api-crud-021.spec.ts:10-20` almost line for line. That follows from the two cases, which state the same two steps. The assertions belong in the specs (API §3), so this is not shared logic to extract.

No findings (see Findings).

## E. Playwright and TypeScript practice

- Every promise is awaited (spec:8, 9, 11, 12, 13, 14, 17, 18, 19, 20, 23, 24, 25, 26).
- No conditionals, loops, `try/catch` or `test.only`.
- Isolation: the test creates its own category and part, and does not depend on demo data, other tests or order.
- TypeScript: `const` only, no casts, no non-null assertions. `category.pk` and `part.pk` are typed `number` through `ApiRecord`. `body` (spec:26) is Playwright's untyped `res.json()`, which is the pattern API §3 prescribes.
- Readability: the spec reads like the case. The 404 message and the flags are the case's own values, so there are no magic values.

No findings (see Findings).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/api/REL/api-rel-001.spec.ts:9`, `:28` | Business rule proven by a follow-up request (API §3) | Nothing confirms that the part is in the category before the delete. `data.part` checks only that the POST succeeded, not the `category` it returned. If InvenTree ignored the `category` field on create, step 3's `expect(body.category).toBeNull()` would still pass, even though the delete moved nothing. The case does not ask for a pre-check (its sibling API-REL-002 has one: step 1 checks `subcategories` is `1`), so adding one now would be Extra. The spec is faithful to the case as written. | No spec change. Ask the architect whether to add a step to the case before the delete (`GET /api/part/<part pk>/`, `200`, `category` equals `<category pk>`), as API-REL-002 does. If the case changes, the spec gets that step. |

## Outside scope

- `test-cases/API_Relationships/part-and-category-crud.md:8` (case Requirement field, also API-REL-002 at :39) cites `open-question_REL.md Q-CRUD-03`, but Q-CRUD-03 is in `test-cases/Open_Questions/open-question_CRUD.md:7`. `open-question_REL.md` has only Q-REL-01..11. The architect should fix the reference; it does not affect the spec.
- `npm run lint` fails for the project because of other specs: `tests/ui/Categories/ui-categories-009.spec.ts:40:59` error `playwright/valid-expect` ("Matchers must be called to assert"); warnings `playwright/no-conditional-in-test` / `no-conditional-expect` in `tests/api/VAL/api-val-087.spec.ts:16-32` and `playwright/no-useless-not` in `tests/ui/Detail_View/ui-detail_view-088.spec.ts:15:50`.
- No problems noticed in the framework code this spec uses (`clients/base.client.ts`, `clients/categories.client.ts`, `clients/parts.client.ts`, `clients/index.ts`, `fixtures/api.fixture.ts`, `fixtures/data.fixture.ts`, `fixtures/expect.ts`, `fixtures/index.ts`, `fixtures/user.fixture.ts`).
