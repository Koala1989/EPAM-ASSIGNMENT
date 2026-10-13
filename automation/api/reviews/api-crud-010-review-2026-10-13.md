# Review: API-CRUD-010 Update a part with PUT

| Item | Value |
|---|---|
| Spec | `tests/CRUD/api-crud-010.spec.ts` |
| Case | `test-cases/API_CRUD/part-and-category-crud.md` (API-CRUD-010), Review: Approved (2026-10-13, bulk approval) |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-10-13 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 2 Info |

## A. Automated checks

- `npm run typecheck`: pass, no errors.
- `npx eslint tests/CRUD/api-crud-010.spec.ts clients/base.client.ts clients/parts.client.ts clients/index.ts fixtures/index.ts fixtures/api.fixture.ts fixtures/data.fixture.ts fixtures/expect.ts`: pass, no errors or warnings.
- `npx playwright test tests/CRUD/api-crud-010.spec.ts --list`: lists `[api] CRUD\api-crud-010.spec.ts:7:7 Part and category CRUD > API-CRUD-010: Update a part with PUT`. Tests were not run (reviewer guardrail).

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `PUT /api/part/<pk>/` as `engineer`, payload `{name: "QA-<suffix> Put Done", description: "QA after", category: <category pk>, active: true}` | `200 OK` | `1. PUT /api/part/<pk>/ as engineer` (L17) | `toHaveStatus(200)` (L19) | Covered |
| 1 | | Body valid against `Part` | same | `expect.soft(res).toMatchSchema('Part')` (L20) | Covered |
| 1 | | `name`, `description`, `category` equal the payload | same | `toBe(payload.name/description/category)` (L22-24) | Covered |
| 2 | `GET /api/part/<pk>/` as `engineer` | `200 OK` | `2. GET /api/part/<pk>/ as engineer` (L27) | `toHaveStatus(200)` (L29) | Covered |
| 2 | | `name`, `description`, `category` equal step 1 payload | same | `toBe(...)` (L31-33) | Covered |

- **Request fidelity:** `api.parts.update` is `ResourceClient.update` = PUT `part/<pk>/` with the body unchanged (base.client.ts:33-35); `api.parts.retrieve` = GET. Payload keys and values match the case exactly (L10-15); names share the test's single suffix (`TestData.suffix`), as `QA-<suffix>` in the case requires.
- **Order and titles:** two steps, in order, titled `<n>. <request>`.
- **Prerequisites:** `test.use({ user: 'engineer' })` matches; part `QA-<suffix> Put Me` with description `QA before` and category `QA-<suffix> Category` created through `data.*` as admin with `data.name`. No settings.
- **Cleanup:** the request under test creates nothing; prerequisites are tracked by `data.part`/`data.category` and removed in reverse order (part deactivated and deleted, then category with both flags `false`), matching the case's Postconditions.
- **Schema:** PUT `/api/part/{id}/` 200 response is `#/components/schemas/Part` (openapi-parts.yaml L2759-2764); check is soft. Step 2 has no schema check, and the case states none.
- **Traceability:** `// case:` header correct; title `API-CRUD-010: Update a part with PUT`; describe `Part and category CRUD` consistent with the other CRUD specs; tag `@regression` matches Tags `Regression`.
- **Review status:** Approved.
- **Fixme:** none.

## C. Conventions

Passed: §3 structure and import from `../../fixtures`; status first, soft schema, `toBe` values; no raw requests, URLs or `@playwright/test` imports; §4 no new client code (uses existing `update`/`retrieve`); §5 fixtures through `fixtures/index.ts`; §7 no hosts or credentials; §8 unique QA names, no demo data; §9 file, title, step and tag naming. No findings.

## D. SOLID and design

Passed: spec tests one case; depends only on `api` and `data` fixtures (interface segregation, dependency inversion); no client changes, so open/closed and Liskov are untouched; no duplication with existing client methods. No findings.

## E. Playwright and TypeScript practice

Passed: every `expect(res)` matcher and request awaited; no conditionals, loops, `try/catch` or `test.only`; isolated data; `const` throughout; no casts or non-null assertions; reads like the case. See Info #1.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/CRUD/api-crud-010.spec.ts:21`, `:30` | E. TypeScript practice | `const body = await res.json()` is implicitly `any`, so field access is untyped. This is the suite-wide pattern and not a defect of this spec. | None required; a typed response helper would be a framework-level decision for the architect. |
| 2 | Info | `tests/CRUD/api-crud-010.spec.ts:14` | B. Fidelity | `active: true` is sent (as the case's payload states) but not asserted; the case does not name it in the Expected result, so not asserting it is correct. Noted only so it is not read as a gap. | None. |

## Outside scope

None.
