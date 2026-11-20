# Review: API-CRUD-021 Delete an empty category

| Item | Value |
|---|---|
| Spec | `tests/api/CRUD/api-crud-021.spec.ts` |
| Case | `test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md` (API-CRUD-021), Review: Approved · 2026-10-13 |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-11-10 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 0 Info |

## A. Automated checks

| Check | Scope | Result |
|---|---|---|
| `npm run typecheck` | whole project | Pass (exit 0, no errors) |
| `npx eslint` | `tests/api/CRUD/api-crud-021.spec.ts`, `clients/categories.client.ts`, `clients/base.client.ts`, `clients/index.ts`, `fixtures/index.ts`, `fixtures/api.fixture.ts`, `fixtures/data.fixture.ts`, `fixtures/expect.ts`, `fixtures/user.fixture.ts` | Pass (exit 0, no errors or warnings) |
| `npx playwright test tests/api/CRUD/api-crud-021.spec.ts --list` | spec | 1 test in project `api` (`Part and category CRUD › API-CRUD-021: Delete an empty category`), after the `api-smoke` setup |

The tests were not run (reviewer guardrail).

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `DELETE /api/part/category/<pk>/` as `admin`, `{"delete_parts": false, "delete_child_categories": false}` | `204 No Content`. The body is empty. | `1. DELETE /api/part/category/<pk>/ as admin` (spec:10) | `await expect(res).toHaveStatus(204)` (spec:12); `expect(await res.text()).toBe('')` (spec:13) | Covered |
| 2 | `GET /api/part/category/<pk>/` as `admin` | `404 Not Found`. Body is `{"detail": "No PartCategory matches the given query."}`. | `2. GET /api/part/category/<pk>/ as admin` (spec:16) | `await expect(res).toHaveStatus(404)` (spec:18); `expect(await res.json()).toEqual({ detail: 'No PartCategory matches the given query.' })` (spec:19) | Covered |

No Missing, Weakened or Extra rows.

- **Request fidelity:** step 1 calls `api.categories.destroy(category.pk, { delete_parts: false, delete_child_categories: false })` (spec:11), which is the case's method, endpoint and payload exactly; `ResourceClient.destroy` (base.client.ts:43-45) sends the body unchanged. Step 2 calls `api.categories.retrieve(category.pk)` (spec:17) with no parameters, as the case states.
- **Order and titles:** two steps, in the case's order, titled `<n>. <request>` with the case's Request text.
- **Prerequisites:** `test.use({ user: 'admin' })` (spec:4) matches "User: `admin`". The category comes from `data.category(data.name('Delete Category'))` (spec:8), which gives `QA-<suffix> Delete Category` posted to `part/category/` as admin, as the case states. Settings: none, and none are changed. The admin token pre-step is handled by the `api` fixture.
- **Cleanup:** the request under test creates no record. The prerequisite category is registered by `data.category` through `trackCategory` (data.fixture.ts:32-36, 103-106). If step 1 fails, cleanup still removes it; if step 1 passes, the cleanup DELETE gets `404`, which `remove()` accepts (data.fixture.ts:137). This matches the case's "Postconditions and cleanup: none, the category is deleted."
- **Schema:** the case states no schema component. `openapi-parts.yaml` gives `DELETE /api/part/category/{id}/` only `204: No response body` (L1424-1426) and `GET` only `200 Category` (L1326-1331), with no `404`. A missing `toMatchSchema` is correct here.
- **Expected values vs. sources:** the 404 body matches `open-question_CRUD.md` Q-CRUD-01 (answered) and CONVENTIONS API §10 "Not found". The required delete flags match Q-CRUD-03 and API §10 "Deleting a category".
- **Traceability:** the first line is `// case: test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md (API-CRUD-021)`. The title `API-CRUD-021: Delete an empty category` matches the case heading. The `describe('Part and category CRUD')` matches the case file's title. Tags `['@smoke', '@regression']` match "Smoke, Regression". This is not a data-driven case (no Data sets table).
- **Review status:** Approved · 2026-10-13.
- **Fixme:** none.

## C. Conventions

- API §3: the file path and name, one-line header, single fixtures import, `test.use`, `describe`, a single test, `data.*` first, one step per case step, status first, values with `toEqual`/`toBe`, follow-up GET as the business-rule proof. All pass.
- API §4: there is no new client code. The spec uses only the inherited `ResourceClient.destroy` and `retrieve` on the existing `CategoriesClient`, which is unchanged (a constructor with the `part/category/` endpoint only).
- API §5: `api` and `data` come through `fixtures/index.ts`. No `apiAs` is needed because the case has a single caller.
- API §7 and Shared §3: no hosts, URLs, IDs or credentials. The pk comes from the created record.
- API §8: no demo data, a unique `QA-` name, and the record is registered for cleanup.
- API §9: naming of the file, title, step titles and tags. All pass.

No findings (see Findings).

## D. SOLID and design

- Single responsibility: one spec for one case. `CategoriesClient` models one resource.
- Open/closed and Liskov substitution: no client was changed. `ResourceClient` keeps its contract: it returns the raw response, makes no assertions and sends the payload unchanged.
- Interface segregation: the spec requests only `api` and `data`, and uses both.
- Dependency inversion: the spec depends on clients and fixtures only, with no endpoint strings or request context.
- Duplication: nothing duplicated. This is the only spec that calls `categories.destroy` (Grep over `tests/api/`). The 404 pattern matches `api-crud-009.spec.ts:19-20`.

No findings (see Findings).

## E. Playwright and TypeScript practice

- Every promise is awaited (spec:8, 10, 11, 12, 13, 16, 17, 18, 19).
- No conditionals, loops, `try/catch` or `test.only`.
- Isolation: the test creates its own category and does not depend on other tests or on order.
- TypeScript: `const` only, no `any`, no casts, no non-null assertions. `category.pk` is typed `number` through `ApiRecord`.
- Readability: the spec reads like the case. It has no magic values: the 404 message is the case's literal Expected result, and the flags are the case's literal payload.

No findings (see Findings).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| - | - | - | - | None | - |

## Outside scope

None noticed in the framework code this spec uses (`clients/base.client.ts`, `clients/categories.client.ts`, `clients/index.ts`, `fixtures/api.fixture.ts`, `fixtures/data.fixture.ts`, `fixtures/expect.ts`, `fixtures/index.ts`).
