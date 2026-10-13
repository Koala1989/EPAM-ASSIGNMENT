# Review: API-CRUD-014 Delete an active part

| Item | Value |
|---|---|
| Spec | `tests/CRUD/api-crud-014.spec.ts` |
| Case | `test-cases/API_CRUD/part-and-category-crud.md` (API-CRUD-014), Review: Approved (2026-10-13) |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-10-13 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 2 Info |

## A. Automated checks

- `npm run typecheck`: pass, no errors.
- `npx eslint tests/CRUD/api-crud-014.spec.ts clients/parts.client.ts clients/base.client.ts fixtures/data.fixture.ts fixtures/api.fixture.ts fixtures/expect.ts fixtures/index.ts`: pass, no errors or warnings.
- `npx playwright test tests/CRUD/api-crud-014.spec.ts --list`: 1 test listed in project `api` (`CRUD\api-crud-014.spec.ts:7:7`), plus the `api-smoke` setup.

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `DELETE /api/part/<pk>/` as `admin` | `400`; body is `{"non_field_errors": ["Cannot delete this part as it is still active"]}` | `1. DELETE /api/part/<pk>/ as admin` (l.10) | `toHaveStatus(400)` (l.12); `toEqual` on the whole body (l.13) | Covered |
| 2 | `GET /api/part/<pk>/` as `admin` | `200`; `active` is `true` | `2. GET /api/part/<pk>/ as admin` (l.16) | `toHaveStatus(200)` (l.18); `body.active` `toBe(true)` (l.20) | Covered |

- **Request fidelity:** `api.parts.destroy(part.pk)` sends `DELETE part/<pk>/` with no body (base `destroy` passes no options when `body` is undefined); `api.parts.retrieve` sends `GET part/<pk>/`. Matches the case.
- **Order and titles:** two steps, in order, titled `<n>. <request>`.
- **Prerequisites:** `test.use({ user: 'admin' })` matches User `admin`; the active part is created through `data.part(data.name('Active Delete'), { active: true })`, giving `QA-<suffix> Active Delete` as admin.
- **Cleanup:** the request under test creates nothing. The prerequisite part is tracked by `data.part`; `deletePart` sets `active: false` before `DELETE`, matching the case's Postconditions.
- **Schema:** the case states no schema check. The schema documents only `204` for `part_destroy` (openapi-parts.yaml l.2803-2826), so no component applies to the `400` body; step 2 does not state a schema. No `toMatchSchema` is correct.
- **Traceability:** `// case:` header correct, title `API-CRUD-014: Delete an active part`, `describe('Part and category CRUD')`, tag `@regression` matches Tags `Regression`.
- **Review status:** Approved.
- **Fixme:** none.

## C. Conventions

Pass: §3 structure, imports only from `../../fixtures`, no raw requests or URLs; §4 no new client code (uses inherited `destroy`/`retrieve`); §5 fixtures `api` and `data` only; §8 unique `QA-` name, no demo data; §9 file, title, step and tag naming. See Findings for Info items.

## D. SOLID and design

Pass: spec depends only on clients and fixtures; no new client methods or flags; `PartsClient` keeps the `ResourceClient` contract; only the fixtures used are requested; no duplication.

## E. Playwright and TypeScript practice

Pass: every `expect(res).toHaveStatus` and request awaited; no conditionals, loops, `try/catch` or `test.only`; `const` throughout; no casts or non-null assertions; the spec reads like the case.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/CRUD/api-crud-014.spec.ts:8` | §3 readability | `{ active: true }` is sent explicitly although `active` defaults to `true` on create. It makes the prerequisite ("active part") explicit and is harmless; noted only because it is a field the case's Prerequisites do not list as payload. | None required. |
| 2 | Info | `tests/CRUD/api-crud-014.spec.ts:19-20` | §3 Values | Step 2 checks only `active`, as the case states. The case's business intent ("the part was not deleted") is already proven by the `200`; no extra assertion is needed. | None. |

## Outside scope

None.
