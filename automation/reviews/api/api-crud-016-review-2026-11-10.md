# Review: API-CRUD-016 Create a category

| Item | Value |
|---|---|
| Spec | `tests/api/CRUD/api-crud-016.spec.ts` |
| Case | `test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md` (API-CRUD-016), Review: Approved (2026-10-13, bulk approval; "expected results not yet executed") |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-11-10 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 1 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass (`tsc --noEmit`, exit 0, no errors) |
| `npx eslint tests/api/CRUD/api-crud-016.spec.ts clients/categories.client.ts clients/base.client.ts clients/index.ts fixtures/index.ts fixtures/api.fixture.ts fixtures/data.fixture.ts fixtures/expect.ts fixtures/user.fixture.ts` | Pass (exit 0, no errors or warnings) |
| `npx playwright test tests/api/CRUD/api-crud-016.spec.ts --list` | 1 test in project `api` (`Part and category CRUD › API-CRUD-016: Create a category`), plus the `api-smoke` setup project |

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `POST /api/part/category/` as `engineer` | `201 Created` | `1. POST /api/part/category/ as engineer` (l.11) | `await expect(res).toHaveStatus(201)` (l.13) | Covered |
| 1 | | Body is valid against `Category` | same | `await expect.soft(res).toMatchSchema('Category')` (l.16) | Covered |
| 1 | | `name` equals the payload | same | `expect(body.name).toBe(payload.name)` (l.17) | Covered |
| 1 | | `description` equals the payload | same | `expect(body.description).toBe(payload.description)` (l.18) | Covered |
| 1 | | `structural` equals the payload | same | `expect(body.structural).toBe(payload.structural)` (l.19) | Covered |
| 1 | | `parent` is `null` | same | `expect(body.parent).toBeNull()` (l.20) | Covered |
| 1 | | `pk` is an integer | same | `expect(Number.isInteger(body.pk)).toBe(true)` (l.21) | Covered |
| 2 | `GET /api/part/category/<pk from step 1>/` as `engineer` | `200 OK` | `2. GET /api/part/category/<pk from step 1>/ as engineer` (l.24) | `await expect(res).toHaveStatus(200)` (l.26) | Covered |
| 2 | | `name` and `description` equal the payload | same | `expect(body.name).toBe(payload.name)` (l.28), `expect(body.description).toBe(payload.description)` (l.29) | Covered |

No Extra assertions. Step 2 has no schema check, which is correct: the case's step 2 does not state one.

- **Request fidelity:** payload (l.8) is `{ name: data.name('Category'), description: 'QA API category', structural: false }`; `data.name` gives `QA-<8 hex> Category` (`utils/names.ts:3-5`), so the body equals the case's `{"name": "QA-<suffix> Category", "description": "QA API category", "structural": false}`. Sent through the inherited `ResourceClient.create` (`clients/base.client.ts:23-25`, `POST part/category/` with the body unchanged); step 2 through `ResourceClient.retrieve` (`base.client.ts:28-30`), no parameters, as the case's "None". Pass.
- **Order and titles:** two case steps, two `test.step`s in order, titled `<n>. <request>` verbatim from the case's Request column. Pass.
- **Prerequisites:** `test.use({ user: 'engineer' })` (l.4) matches "User: `engineer`" (`data/users.local.json:4`). Settings: None; Data: None: the spec creates no prerequisite records. The token pre-step is done by the `api` fixture (`fixtures/api.fixture.ts:25-28`). Pass.
- **Cleanup:** the category created by the request under test is registered with `data.trackCategory(body.pk)` (l.15), right after the status check (l.13) and before the schema check (l.16) and every value check. `trackCategory` deletes it as admin with `{ delete_parts: false, delete_child_categories: false }` (`fixtures/data.fixture.ts:103-106`), exactly the case's Postconditions. Pass.
- **Schema:** `part_category_create` (`POST /api/part/category/`, `requirements/openapi-parts.yaml:947-982`) gives `201` -> `#/components/schemas/Category` (l.981). The spec uses `Category` with `expect.soft`. Pass.
- **Traceability:** `// case: test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md (API-CRUD-016)` (l.1); title `API-CRUD-016: Create a category` equals the case heading (case file l.397); `describe('Part and category CRUD')` matches the case file's functionality and the sibling CRUD specs; tags `['@smoke', '@regression']` match Tags "Smoke, Regression". Not data-driven (no Data sets table). Pass.
- **Review status:** Approved. Pass.
- **Fixme:** none. Pass.

## C. Conventions

- API §3 structure (single import from `fixtures`, `test.use`, describe, one test, one step per case step): pass.
- API §3 status first, cleanup first, soft schema, `toBe`/`toBeNull` on the parsed body, no `toMatchObject`, no `toBeOK()`: pass.
- API §3 no raw requests, no `@playwright/test` import, no URLs or hosts: pass (lint).
- API §4 clients: no new client code; `CategoriesClient` (`clients/categories.client.ts`) is unchanged and only the inherited `create` and `retrieve` are used: pass.
- API §5 fixtures through `fixtures/index.ts`; only `api` and `data` requested: pass.
- API §7 user as the case states (`engineer`): pass.
- API §8 isolation: own `QA-` category, no demo records, no order dependence: pass.
- API §9 naming (file, title, step titles, tags): pass.

No findings in this section.

## D. SOLID and design

- Single responsibility: one spec, one case; `CategoriesClient` models one resource: pass.
- Open/closed and Liskov: no client changes; `CategoriesClient` keeps the `ResourceClient` contract (raw response, no assertions, body unchanged): pass.
- Interface segregation: only `api` and `data` requested, both used: pass.
- Dependency inversion: the spec depends on clients and fixtures only, not on paths or the request context: pass.
- Duplication: the create-then-read structure mirrors API-CRUD-001 for parts, but each spec follows its own case and is a few lines: acceptable.

## E. Playwright and TypeScript practice

- Every promise awaited (`test.step`, `api.categories.create`/`retrieve`, `toHaveStatus`, `toMatchSchema`, `res.json()`): pass.
- No conditionals, loops, `try/catch` or `test.only`: pass.
- Unique names (`QA-<8 hex>`), no dependence on other tests: pass.
- `const` everywhere except `let pk` (l.9), which carries the step 1 pk into step 2, as in the sibling specs; no casts or non-null assertions; `body` is Playwright's `any` from `res.json()`, and the soft schema check validates its shape: pass.
- Readability: the expected values come from `payload`, so no literal is repeated; the spec reads like the case: pass.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/api/CRUD/api-crud-016.spec.ts:4,13` | Case Notes, API §11 | The case's Notes say `engineer` is *assumed* to hold the category add role, and its Review says "expected results not yet executed". This review does not run tests, so whether `engineer` gets `201` is unverified here (the users file only says "Manage parts, view stock"). | Nothing for the spec. Check the 3-run result: if InvenTree returns `403`, keep the user and the `201` and mark the test `test.fixme()` with a `// FINDING:` comment, reported under SEC, as the case's Notes say. |

## Outside scope

- `tests/api/CRUD/api-crud-001.spec.ts:22,34`: `toMatchSchema('Part')` is a hard `expect` (API §3 requires `expect.soft`), and at l.22 it runs before `data.trackPart(body.pk)` (l.24), so a schema failure in step 1 leaves the created part behind (API §3 cleanup first). Not reviewed here; worth a re-review of that spec.
