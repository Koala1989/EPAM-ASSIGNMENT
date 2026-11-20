# Review: API-CRUD-008 Read a part by ID

| Item | Value |
|---|---|
| Spec | `tests/api/CRUD/api-crud-008.spec.ts` |
| Case | `test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md` (API-CRUD-008), Review: Approved (2026-10-13, bulk approval; "expected results not yet executed") |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-11-10 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 2 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass (`tsc --noEmit`, no errors) |
| `npx eslint tests/api/CRUD/api-crud-008.spec.ts clients/parts.client.ts clients/base.client.ts clients/index.ts fixtures/index.ts fixtures/api.fixture.ts fixtures/data.fixture.ts fixtures/expect.ts fixtures/user.fixture.ts` | Pass (exit 0, no errors or warnings) |
| `npx playwright test tests/api/CRUD/api-crud-008.spec.ts --list` | 1 test in project `api` (`Part and category CRUD › API-CRUD-008: Read a part by ID`), plus the `api-smoke` setup project |

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `GET /api/part/<pk>/` as `engineer` | `200 OK` | `1. GET /api/part/<pk>/ as engineer` (l.11) | `await expect(res).toHaveStatus(200)` (l.13) | Covered |
| 1 | | Body is valid against `Part` | same | `await expect.soft(res).toMatchSchema('Part')` (l.14) | Covered (see Info #1) |
| 1 | | `pk` equals the requested ID | same | `expect(body.pk).toBe(part.pk)` (l.16); `part.pk` is the ID passed to `retrieve` (l.12) | Covered |
| 1 | | `name` is `QA-<suffix> Read Me` | same | `expect(body.name).toBe(name)` (l.17), `name = data.name('Read Me')` (l.8) gives `QA-<8 hex> Read Me` (`utils/names.ts:5`) | Covered |
| 1 | | `description` is `QA read` | same | `expect(body.description).toBe('QA read')` (l.18) | Covered |

No Extra assertions: only the fields the Expected result names are checked.

- **Request fidelity:** `api.parts.retrieve(part.pk)` (l.12) is `GET part/<pk>/` through the inherited `ResourceClient.retrieve` (`clients/base.client.ts:28-30`), no query parameters, as the case's "Payload / parameters: None". Pass.
- **Order and titles:** one case step, one `test.step`, titled `1. GET /api/part/<pk>/ as engineer`, verbatim from the case's Request column. Pass.
- **Prerequisites:** `test.use({ user: 'engineer' })` (l.4) matches "User: `engineer`"; `engineer` exists in `data/users.local.json:4`. The part `QA-<suffix> Read Me` with description `QA read` is created by `data.part(name, { description: 'QA read' })` (l.9), which is `POST part/` as admin (`fixtures/data.fixture.ts:38-42`), as the case states. Settings: none. The token pre-step is done by the `api` fixture (`fixtures/api.fixture.ts:25-28`). Pass.
- **Cleanup:** the request under test is a GET and creates nothing. The setup part is registered inside `data.part` and deleted after the test (made inactive first, `data.fixture.ts:141-153`), matching the case's Postconditions. Pass.
- **Schema:** `part_retrieve` (`GET /api/part/{id}/`, `requirements/openapi-parts.yaml:2672-2729`) gives `200` -> `#/components/schemas/Part` (l.2728). The spec uses `Part` and `expect.soft`. Pass.
- **Traceability:** `// case: test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md (API-CRUD-008)` (l.1); title `API-CRUD-008: Read a part by ID` equals the case heading (l.7); `describe('Part and category CRUD')` matches the case file's functionality and the sibling CRUD specs; tags `['@smoke', '@regression']` match Tags "Smoke, Regression". Not data-driven (no Data sets table). Pass.
- **Review status:** Approved. Pass.
- **Fixme:** none. Pass.

## C. Conventions

- API §3 structure (single import from `fixtures`, `test.use`, describe, one test, data first, one step): pass.
- API §3 status first, soft schema, `toBe` on the parsed body, no `toMatchObject`, no `toBeOK()`: pass.
- API §3 no raw requests, no `@playwright/test` import, no URLs or hosts: pass (lint).
- API §4 clients: no new or changed client code (`clients/` has no uncommitted changes; only the inherited `retrieve` is used): pass.
- API §5 fixtures through `fixtures/index.ts`; only `api` and `data` requested: pass.
- API §7 user as the case states (`engineer`): pass.
- API §8 isolation: own `QA-` part, no demo records, no order dependence: pass.
- API §9 naming (file, title, step, tags): pass.

No findings in this section.

## D. SOLID and design

- Single responsibility: one spec, one case; `PartsClient` models one resource: pass.
- Open/closed and Liskov: no client changes; `PartsClient` keeps the `ResourceClient` contract (raw response, no assertions): pass.
- Interface segregation: only `api` and `data` requested, both used: pass.
- Dependency inversion: the spec depends on clients and fixtures only: pass.
- Duplication: the GET-by-pk step resembles step 2 of API-CRUD-001/010, but each belongs to its own case and is three or four lines that mirror the case: acceptable.

## E. Playwright and TypeScript practice

- Every promise awaited (`data.part`, `test.step`, `api.parts.retrieve`, `toHaveStatus`, `toMatchSchema`, `res.json()`): pass.
- No conditionals, loops, `try/catch` or `test.only`: pass.
- Unique names (`QA-<8 hex>`), no dependence on other tests: pass.
- `const` throughout, no casts or non-null assertions; `body` is Playwright's `any` from `res.json()`, as in every sibling spec, and the soft schema check validates its shape: pass.
- Readability: the spec reads like the case step: pass (see Info #2).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/api/CRUD/api-crud-008.spec.ts:9,14` | API §3 Schema, API §10 Schema deviations, API §12 | The case's setup part has no category, so `Part.category_name` is missing from the response (F-11, `test-cases/findings.md`, which already lists API-CRUD-008). The soft `toMatchSchema('Part')` will fail on every run with `[F-11]`, while status, `pk`, `name` and `description` still run. This is the intended behaviour (not a fixme, not suppressed). | Nothing for the spec. The 3-run check should show "Known product defects only: F-11"; any `[NEW]` label is a new finding for the architect. |
| 2 | Info | `tests/api/CRUD/api-crud-008.spec.ts:9,18` | Readability (E) | The name is held in a `const` and reused, but the description literal `'QA read'` is written twice (setup and assertion). Harmless: a mismatch would fail the test, not hide anything, and the literal mirrors the case. | Optional: `const description = 'QA read'` and use it in both places, as the spec already does for `name`. |

## Outside scope

- None.
