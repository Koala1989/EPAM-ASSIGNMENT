# Review: API-CRUD-009 Read a part with an ID that does not exist

| Item | Value |
|---|---|
| Spec | `tests/CRUD/api-crud-009.spec.ts` |
| Case | `test-cases/API_CRUD/part-and-category-crud.md` (API-CRUD-009), Review: Approved · 2026-10-13 |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-10-13 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 0 Major, 1 Minor, 3 Info |

## A. Automated checks

- `npm run typecheck`: pass, no errors.
- `npx eslint tests/CRUD/api-crud-009.spec.ts fixtures/index.ts fixtures/api.fixture.ts fixtures/data.fixture.ts fixtures/expect.ts clients/base.client.ts clients/parts.client.ts clients/index.ts`: pass, 0 errors, 0 warnings.
- `npx playwright test tests/CRUD/api-crud-009.spec.ts --list`: 1 test listed in project `api` (plus the `api-smoke` setup).

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| Prerequisite | Create part as `admin`, make inactive, delete, reuse `pk` | (setup) | none (lines 12-15) | `data.part(data.name(...))`; PATCH `active: false` -> `toHaveStatus(200)`; DELETE -> `toHaveStatus(204)` | Covered |
| 1 | `GET /api/part/<deleted pk>/` as `engineer` | `404 Not Found` | `1. GET /api/part/<deleted pk>/ as engineer` (l.17) | `await expect(res).toHaveStatus(404)` (l.19) | Covered |
| 1 | same | Body is `{"detail": "No Part matches the given query."}`; no part is returned | same | `expect(await res.json()).toEqual({ detail: 'No Part matches the given query.' })` (l.20): exact whole-body equality, which also proves no part is returned | Covered |

- **Request fidelity:** `api.parts.retrieve(part.pk)` is `GET part/<pk>/` with no body or parameters (`base.client.ts:28-30`), sent as `engineer`. Matches.
- **Order and titles:** one step, titled as in the case.
- **Prerequisites:** `test.use({ user: 'engineer' })` matches; admin caller obtained through `apiAs('admin')`; part created through `data.part` with `data.name`. No settings.
- **Cleanup:** the request under test creates nothing. The prerequisite part is tracked by `data.part`; the fixture's `deletePart` returns early on 404 (`data.fixture.ts:112`), so the already-deleted part does not fail cleanup.
- **Schema:** the case states no schema component (the operation documents only `200`; 404 rule from Q-CRUD-01). No `toMatchSchema` is correct.
- **Traceability:** `// case:` header correct, title `API-CRUD-009: Read a part with an ID that does not exist`, describe `Part and category CRUD`, tag `@regression` matches Tags `Regression`.
- **Review status:** Approved.
- **Fixme:** none.

## C. Conventions

Passed: §3 structure, import only from `fixtures`, status first, exact value check, no raw requests/URLs; §4 no new client code (`PartsClient` is unchanged and inherits `retrieve`/`partialUpdate`/`destroy`); §5 fixtures through `fixtures/index.ts`, `apiAs` for the second caller; §7 no hosts or credentials; §8 unique QA name, no demo data; §9 file, title, step and tag naming. See finding 1 for the in-spec setup.

## D. SOLID and design

Passed: spec tests one case; no client changes; spec depends only on clients and fixtures, not on endpoints or the request context; no duplication with other specs (no other spec builds a deleted pk today). See finding 1.

## E. Playwright and TypeScript practice

Passed: every call and matcher awaited (l.12-15, 18-20); no conditionals, loops, try/catch or `test.only`; isolation via a freshly created and deleted part (Postgres sequences do not reuse the pk); `const` throughout, no `any`, casts or non-null assertions; readable, with the prerequisite explained in a comment.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Minor | `tests/CRUD/api-crud-009.spec.ts:12-15` | §1 (tests never hold setup logic), §3 (prerequisites through `data.*`) | The prerequisite "a pk that no longer exists" is built in the spec with admin clients and two hard setup assertions. It is correct and fails fast, but it is setup logic in the test layer, and API-CRUD-013/018/021/023/024 (same Q-CRUD-01 pattern) are likely to copy it. | Architect's decision: add a `data` helper (e.g. `data.deletedPartPk()` / `data.deletedCategoryPk()`) that creates, deactivates and deletes as admin, and call it here. Until then the current code is acceptable. |
| 2 | Info | `tests/CRUD/api-crud-009.spec.ts:20` | §3 Values | The detail message is a literal string; it comes verbatim from the case and Q-CRUD-01 / §10 "Not found", so it is traceable, not a magic value. | None. |
| 3 | Info | `fixtures/data.fixture.ts:112` | §8 cleanup | Cleanup of the prerequisite part sends an extra admin `GET part/<pk>/` that returns 404 and exits; harmless, noted only because the spec deletes a tracked record itself. | None. |
| 4 | Info | `requirements/openapi-parts.yaml` GET `/api/part/{id}/` | Schema | The 404 response is not documented in the schema (only `200`); the expected code rests on the architect's rule Q-CRUD-01, as the case states. | None for the spec. |

## Outside scope

- `test-cases/API_CRUD/open-questions.md:5`: Q-CRUD-01 row has Status `Open` in the fourth column while a later column says `Answered`; the architect may want to make the row consistent.
