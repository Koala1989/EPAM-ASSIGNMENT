# Review: API-LST-001 A part list request with `limit` returns the paginated envelope with `count`, `results`, `next` and `previous`.

| Item | Value |
|---|---|
| Spec | `tests/api/LST/api-lst-001.spec.ts` |
| Case | `test-cases/API_Lists_and_Filters/lists-and-filters.md` (API-LST-001), Review: Approved (2026-11-05, bulk approval by the architect; expected results not yet executed) |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-11-05 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 0 Major, 2 Minor, 1 Info |

## A. Automated checks

- `npm run typecheck` (`tsc --noEmit`): pass (exit 0), no errors.
- `npx eslint tests/api/LST/api-lst-001.spec.ts clients/parts.client.ts clients/base.client.ts clients/index.ts fixtures/index.ts fixtures/api.fixture.ts fixtures/data.fixture.ts fixtures/expect.ts fixtures/user.fixture.ts utils/schema.ts`: pass (exit 0), no errors or warnings.
- `npx playwright test tests/api/LST/api-lst-001.spec.ts --list`: lists `[api] › tests\api\LST\api-lst-001.spec.ts:7:7 › Lists and filters › API-LST-001: ...` plus the 7 `api-smoke` setup tests (including `token for reader`).

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `GET /api/part/` as `reader`, `category=<cat pk>`, `limit=2` | `200 OK` | `1. GET /api/part/ as reader (category=<cat pk>, limit=2)` (L13) | `await expect(res).toHaveStatus(200)` (L15) | Covered |
| 1 | | Body valid against `PaginatedPartList` | | `await expect.soft(res).toMatchSchema('PaginatedPartList')` (L16) | Covered |
| 1 | | `count` is `3` | | `expect(body.count).toBe(3)` (L18) | Covered |
| 1 | | `results` has exactly 2 items | | `expect(body.results).toHaveLength(2)` (L19) | Covered |
| 1 | | `next` is a non-null string | | `expect(typeof body.next).toBe('string')` (L20); `typeof null` is `'object'`, so null fails | Covered (see Finding 2 on the failure message) |
| 1 | | `previous` is `null` | | `expect(body.previous).toBeNull()` (L21) | Covered |

- **Request fidelity:** pass. `api.parts.list({ category: category.pk, limit: 2 })` (L14) -> `ResourceClient.list` sends `GET part/` with exactly these query parameters (`clients/base.client.ts:18-20`), as `reader`. No extra parameters (no `ordering`, `offset`); none stated by the case. `limit` is the parameter the schema marks `required: true` (`openapi-parts.yaml` L578-583); `category` is an integer filter (L468-472).
- **Order and titles:** one step for the case's one step, numbered `1.`. The title adds the parameters to the request (Finding 1).
- **Prerequisites:** pass. `test.use({ user: 'reader' })` (L4) matches "User: `reader`"; token pre-step done by the `api` fixture (`tokenFor`, `Authorization: Token`). Category `QA-<suffix> Page Cat` (L8) and parts `QA-<suffix> P1`, `P2`, `P3` in it (L9-11) are created as admin through `data.category` / `data.part` with `data.name`, awaited one after another, so creation order and ascending pks match the case. Settings: None, none changed.
- **Cleanup:** pass. The request under test is a `GET` and creates nothing. The category and parts are registered by `data.category` / `data.part` (`fixtures/data.fixture.ts:32-42`) and removed in reverse order: parts deactivated and deleted first, then the category with `delete_parts: false, delete_child_categories: false`, as the case's Postconditions state.
- **Schema:** pass. `part_list` `200` response is `#/components/schemas/PaginatedPartList` (`openapi-parts.yaml` L741-745; component L3944-3966). The check is `expect.soft` and awaited.
- **Traceability:** pass. L1 `// case: test-cases/API_Lists_and_Filters/lists-and-filters.md (API-LST-001)`; title equals `<case ID>: <case title>` character for character (including the closing period); `describe('Lists and filters')` from the case file title; tags `['@smoke', '@regression']` match Tags "Smoke, Regression". Not a data-driven case (no Data sets table).
- **Review status:** Approved. Pass.
- **Fixme:** none used; none needed.
- **Isolation of the count:** `count` 3 is deterministic: the filter targets a category created in this test with no child categories, so the default `cascade` behaviour and demo data cannot change it.

## C. Conventions

- API §3 structure (single fixtures import, `test.use`, describe, one test, `data.*` prerequisites first, status first, soft schema, `toBe` on the parsed body, no raw requests or URLs): pass. Step title: Finding 1.
- API §4 no new client methods or clients; `PartsClient` (`clients/parts.client.ts`) and `ResourceClient` unchanged, return the raw response, send what they are given: pass.
- API §5 fixtures through `fixtures/index.ts`; only `api` and `data` requested, both used: pass.
- API §6/§7 no hosts, ports, credentials, `process.env` or tokens in the spec (lint confirms); least-privileged user `reader` as the case states: pass.
- API §8 unique `QA-<8 hex>` names, no demo-record or order dependence: pass.
- API §9 file name, test title, tags: pass. Step title: Finding 1.

## D. SOLID and design

- Single responsibility (one case per spec, `PartsClient` models `/api/part/` only), open/closed (no flags added), Liskov (`PartsClient` keeps the `ResourceClient` contract), interface segregation (`api`, `data` only), dependency inversion (spec uses clients and fixtures, no endpoints or request context), no duplication with other specs or client methods (only LST spec so far): pass.

## E. Playwright and TypeScript practice

- `toHaveStatus` and `toMatchSchema` awaited; no conditionals, loops, `try/catch` or `test.only`; isolated data; `const` throughout; no casts, `any` annotations or non-null assertions; the literal `2` and `3` are the case's own values: pass. See Findings 2 and 3.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Minor | `tests/api/LST/api-lst-001.spec.ts:13` | API §9 step title `<n>. <request as in the case>`; API §3 | Title is `'1. GET /api/part/ as reader (category=<cat pk>, limit=2)'`. The case's Request column is `` `GET /api/part/` as `reader` ``; the parameters belong to the Payload column. Every other API spec uses the request only (e.g. `tests/api/CRUD/api-crud-001.spec.ts:19`, `tests/api/VAL/api-val-087.spec.ts:37`), so the report reads differently from the case and from the rest of the suite. | `test.step('1. GET /api/part/ as reader', ...)`. |
| 2 | Minor | `tests/api/LST/api-lst-001.spec.ts:20` | E readability / diagnostics | `expect(typeof body.next).toBe('string')` is correct (null gives `'object'`), but on failure the message shows only `Expected: "string" Received: "object"` (or `"undefined"`), not the actual `next` value, so you cannot tell a `null` from a missing key or a number from the report. The suite already uses the idiomatic form in `tests/api/setup/api.setup.ts:11`. | `expect(body.next).toEqual(expect.any(String));` (matches string primitives, rejects `null` and `undefined`, and prints the received value). |
| 3 | Info | `tests/api/LST/api-lst-001.spec.ts:17-21` | E TypeScript | `const body = await res.json()` is implicitly `any`, so `body.count`, `body.results`, `body.next` and `body.previous` are not type-checked. At run time a missing envelope (e.g. a plain array, F-09) still fails the hard `toBe(3)` with a clear message, so this is a static-typing note only, and the same pattern is used across the API suite. | None required. If the suite later adds a typed helper or a `PaginatedList<T>` type, use it here. |

## Outside scope

- None found in the framework code read (`clients/base.client.ts`, `clients/parts.client.ts`, `clients/index.ts`, `fixtures/index.ts`, `fixtures/api.fixture.ts`, `fixtures/data.fixture.ts`, `fixtures/expect.ts`, `fixtures/user.fixture.ts`, `utils/schema.ts`, `utils/names.ts`).
