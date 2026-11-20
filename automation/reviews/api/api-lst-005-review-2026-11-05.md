# Review: API-LST-005 `offset` skips that many results and the page starts at the next one.

| Item | Value |
|---|---|
| Spec | `tests/api/LST/api-lst-005.spec.ts` |
| Case | `test-cases/API_Lists_and_Filters/lists-and-filters.md` (API-LST-005), Review: Approved (2026-11-05, bulk approval; "expected results not yet executed") |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-11-05 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 3 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass (exit 0, no errors) |
| `npx eslint tests/api/LST/api-lst-005.spec.ts clients/base.client.ts clients/parts.client.ts clients/index.ts fixtures/index.ts fixtures/api.fixture.ts fixtures/data.fixture.ts fixtures/expect.ts fixtures/user.fixture.ts utils/names.ts` | Pass (exit 0, no errors or warnings) |
| `npx playwright test tests/api/LST/api-lst-005.spec.ts --list` | 1 test in project `api` (plus the `api-smoke` setup project), title as expected |

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `GET /api/part/` as `reader`, `category=<cat pk>`, `limit=2`, `offset=1`, `ordering=id` | `200 OK` | `1. GET /api/part/ as reader (category=<cat pk>, limit=2, offset=1, ordering=id)` (l.16) | `await expect(res).toHaveStatus(200)` (l.18) | Covered |
| 1 | | Body is valid against `PaginatedPartList` | same | `await expect.soft(res).toMatchSchema('PaginatedPartList')` (l.19) | Covered |
| 1 | | `count` is `3` | same | `expect(body.count).toBe(3)` (l.21) | Covered |
| 1 | | `results` holds `QA-<suffix> P2` then `QA-<suffix> P3` | same | `expect(body.results.map(...)).toEqual([name2, name3])` (l.22): exact length, order and names; proves P1 was skipped | Covered |
| 1 | | `previous` is a non-null string | same | `expect(typeof body.previous).toBe('string')` (l.23): `typeof null` is `'object'`, so null fails | Covered (see Info #1) |

No Extra assertions: `next` (null here) is not stated by the case and is not asserted.

- **Request fidelity:** `api.parts.list({ category: category.pk, limit: 2, offset: 1, ordering: 'id' })` (l.17) sends exactly the case's four parameters, through the inherited `ResourceClient.list`, which passes `params` unchanged. Pass.
- **Order and titles:** one case step, one `test.step`, titled `1. GET /api/part/ as reader` plus the case's parameters. Pass.
- **Prerequisites:** `test.use({ user: 'reader' })` (l.4) matches "User: `reader`"; `reader` exists in `data/users.local.json`. Category `data.name('Page Cat')` and parts `data.name('P1'|'P2'|'P3')` in it are created through `data.*` as admin with `POST part/` (l.8-14), awaited one after another, so pks ascend in the case's order. Token pre-step is handled by the `api` fixture. No settings. Pass.
- **Cleanup:** the request under test is a GET and creates nothing; the category and parts are registered by `data.category` / `data.part` and removed after the test (parts deactivated first). Pass.
- **Schema:** the schema gives `200` -> `#/components/schemas/PaginatedPartList` for `part_list` (openapi-parts.yaml l.740-745); the spec uses that component, as `expect.soft`. Pass.
- **Traceability:** `// case: test-cases/API_Lists_and_Filters/lists-and-filters.md (API-LST-005)` (l.1); title equals the case heading verbatim (l.7); `describe('Lists and filters')` matches the case file's functionality; tags `['@regression']` match Tags "Regression". Not data-driven (no Data sets table). Pass.
- **Review status:** Approved. Pass. (The approval note says the expected results were not yet executed manually; that is a case-process observation, not a spec defect.)
- **Fixme:** none. Pass.

## C. Conventions

- API §3 structure (single import from fixtures, `test.use`, describe, one test, data first, steps in order): pass.
- API §3 status first, soft schema, `toBe`/`toEqual` on parsed values, no `toMatchObject`: pass.
- API §3 no raw requests, no `@playwright/test` import, no URLs or hosts: pass (lint).
- API §4 clients: no new or changed client code (`clients/` has no uncommitted changes); only the inherited `list` is used: pass.
- API §5 fixtures used through `fixtures/index.ts`; only `api` and `data` requested: pass.
- API §7 least-privileged user (`reader`, view only), as the case states: pass.
- API §8 isolation: the `category` filter on a new, unique `QA-` category confines the list to the test's own parts; no demo data: pass.
- API §9 naming (file, title, step, tags): pass.
- API §10 `limit` always sent: pass.

No findings in this section.

## D. SOLID and design

- Single responsibility: one spec, one case; `PartsClient` models one resource: pass.
- Open/closed and Liskov: no client changes; `PartsClient` keeps the `ResourceClient` contract: pass.
- Interface segregation: spec requests only `api` and `data`: pass.
- Dependency inversion: spec depends on clients and fixtures only, no endpoints or request context: pass.
- Duplication: see Info #3 (shared prerequisite block with API-LST-001).

## E. Playwright and TypeScript practice

- Every promise awaited (`data.*`, `test.step`, `api.parts.list`, `toHaveStatus`, `toMatchSchema`, `res.json()`): pass.
- No conditionals, loops over response data (the `map` projects names for one assertion, it does not branch), `try/catch` or `test.only`: pass.
- Unique names (`QA-<8 hex>`), no order dependence: pass.
- `const` throughout, clear names, no non-null assertions: pass.
- Readability: the spec reads like the case step: pass.

See Info #1 and #2.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/api/LST/api-lst-005.spec.ts:23` | Readability of failures (E) | `expect(typeof body.previous).toBe('string')` is correct (null fails), but on failure the report shows only `Received: "object"`, not the value received. | Optionally `expect(body.previous).toEqual(expect.any(String))`: same meaning (rejects null), and a failure shows the actual value. |
| 2 | Info | `tests/api/LST/api-lst-005.spec.ts:22` | TypeScript: no unchecked casts (E) | `(p: { name: string })` puts a type on `any` data from `res.json()` without checking it. It does no harm here: the soft schema check validates the shape, and a missing `name` would make `toEqual` fail. | None needed. If the suite adds typed response helpers later, use them here. |
| 3 | Info | `tests/api/LST/api-lst-005.spec.ts:8-14` | Duplication between specs (D) | The setup (category `Page Cat` plus P1-P3) is the same as in `api-lst-001.spec.ts:8-11`, and the case file gives the same Prerequisites for API-LST-002..006. Today it is a few lines that mirror the case, which is acceptable. | Nothing for this spec. If more LST cases are automated, the architect may consider a shared `data` helper (fixtures are the architect's to change). |

## Outside scope

- None.
