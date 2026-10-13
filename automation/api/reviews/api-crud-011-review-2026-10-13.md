# Review: API-CRUD-011 Update one field of a part with PATCH

| Item | Value |
|---|---|
| Spec | `tests/CRUD/api-crud-011.spec.ts` |
| Case | `test-cases/API_CRUD/part-and-category-crud.md` (API-CRUD-011), Review: Approved (2026-10-13) |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-10-13 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 2 Info |

## A. Automated checks

- `npm run typecheck`: pass, no errors.
- `npx eslint tests/CRUD/api-crud-011.spec.ts clients/parts.client.ts clients/base.client.ts clients/index.ts fixtures/*.ts`: pass, no errors or warnings.
- `npx playwright test tests/CRUD/api-crud-011.spec.ts --list`: lists `[api] › CRUD\api-crud-011.spec.ts:7:7 › Part and category CRUD › API-CRUD-011: Update one field of a part with PATCH`.

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `PATCH /api/part/<pk>/` as `engineer`, `{"description": "QA changed"}` | `200 OK` | `1. PATCH /api/part/<pk>/ as engineer` (L12) | `await expect(res).toHaveStatus(200)` (L14) | Covered |
| 1 | | Body valid against `Part` | L12 | `await expect.soft(res).toMatchSchema('Part')` (L15) | Covered |
| 1 | | `description` is `QA changed` | L12 | `expect(body.description).toBe('QA changed')` (L17) | Covered |
| 1 | | `name` is `QA-<suffix> Patch Me` | L12 | `expect(body.name).toBe(name)` (L18), `name = data.name('Patch Me')` = `QA-<8 hex> Patch Me` | Covered |
| 1 | | `IPN` is `QA-<suffix>-P` | L12 | `expect(body.IPN).toBe(IPN)` (L19), `IPN = \`${data.suffix}-P\`` = `QA-<8 hex>-P` | Covered |
| 2 | `GET /api/part/<pk>/` as `engineer` | `200 OK` | `2. GET /api/part/<pk>/ as engineer` (L22) | `await expect(res).toHaveStatus(200)` (L24) | Covered |
| 2 | | `description` is `QA changed` | L22 | `toBe('QA changed')` (L26) | Covered |
| 2 | | `name` and `IPN` unchanged | L22 | `toBe(name)`, `toBe(IPN)` against the prerequisite values (L27-L28) | Covered |

- **Request fidelity:** `api.parts.partialUpdate(part.pk, { description: 'QA changed' })` sends PATCH to `part/<pk>/` with exactly the case payload (`base.client.ts:38-40`); step 2 uses `retrieve` (GET). Pass.
- **Order and titles:** two steps, in case order, titled `<n>. <request>`. Pass.
- **Prerequisites:** `test.use({ user: 'engineer' })` matches; the part is created as admin through `data.part(name, { description: 'QA keep', IPN })` with `data.name`, matching the case's name, description and IPN. Pass.
- **Cleanup:** the request under test creates no record; the prerequisite part is tracked by `data.part` (`data.fixture.ts:38-42`) and deleted (inactivated first) after the test, matching the case's Postconditions. Pass.
- **Schema:** the case and `openapi-parts.yaml` L2767-L2802 give response `Part` for `200` of `part_partial_update`; the spec checks `Part` with `expect.soft`. Pass. Step 2 has no schema check, and the case does not state one. Pass (no Extra).
- **Traceability:** `// case:` header correct, title `API-CRUD-011: Update one field of a part with PATCH` matches, `describe('Part and category CRUD')`, tags `@smoke`, `@regression` match the case's Tags (Smoke, Regression). Pass.
- **Review status:** Approved. Pass.
- **Fixme:** none. Pass.

## C. Conventions

Passed: no new client code (uses `ResourceClient.partialUpdate`/`retrieve` via `PartsClient`); imports only from `../../fixtures` (§5); no raw requests, paths or URLs in the spec (§3, §7); prerequisites through `data.*` (§8); file, title, step and tag naming (§9); status first, soft schema, `toBe` values (§3). No findings.

## D. SOLID and design

Passed: spec tests one case through clients and fixtures only (DIP); requests only `api` and `data` (ISP); no client changes or duplication (OCP, LSP). No findings.

## E. Playwright and TypeScript practice

Passed: every request and matcher awaited (`toHaveStatus`, `toMatchSchema`, `res.json()`); no conditionals, loops, `try/catch` or `test.only`; no demo-data dependence, unique `QA-` names; `const` throughout, no casts or non-null assertions; the spec reads like the case. See Info items 1-2.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/CRUD/api-crud-011.spec.ts:10`, `:15` | §10 Schema deviations (F-11) | The prerequisite part has no category (the case states none), so the soft `toMatchSchema('Part')` is expected to report `Part.category_name` missing, labelled `[F-11]`. This is a recorded known product defect, not a spec defect; the 3-run gate counts it as "Known product defects only" (§12). | None. Do not add a category to dodge the check, since the case does not state one. |
| 2 | Info | `tests/CRUD/api-crud-011.spec.ts:16`, `:25` | §E TypeScript | `await res.json()` is typed `any`, so `body.description` etc. are unchecked property accesses. This is the suite-wide pattern and acceptable for value assertions. | Optional, suite-wide: a typed helper or `as Record<string, unknown>` if the architect wants stricter typing. |

## Outside scope

None.
