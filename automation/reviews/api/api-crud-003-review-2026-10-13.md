# Review: API-CRUD-003 A part created without `active` is active

| Item | Value |
|---|---|
| Spec | `tests/CRUD/api-crud-003.spec.ts` |
| Case | `test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md` (API-CRUD-003), Review: Approved (2026-10-13) |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-10-13 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 3 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass, no errors |
| `npx eslint tests/CRUD/api-crud-003.spec.ts clients/parts.client.ts clients/base.client.ts clients/index.ts fixtures/*.ts` | Pass, 0 errors, 0 warnings |
| `npx playwright test tests/CRUD/api-crud-003.spec.ts --list` | 1 test listed in project `api` (plus `api-smoke` setup) |

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `POST /api/part/` as `engineer`, `{"name": "QA-<suffix> Default Active"}` | `201 Created` | `1. POST /api/part/ as engineer` (l.11) | `await expect(res).toHaveStatus(201)` (l.13) | Covered |
| 1 | | `active` is `true` | same | `expect(body.active).toBe(true)` (l.16) | Covered |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | `200 OK` | `2. GET /api/part/<pk from step 1>/ as engineer` (l.19) | `await expect(res).toHaveStatus(200)` (l.21) | Covered |
| 2 | | `active` is `true` | same | `expect(body.active).toBe(true)` (l.23) | Covered |

- **Request fidelity:** `api.parts.create(payload)` sends `{ name: data.name('Default Active') }` only, with no `active` field, exactly as the case; `PartsClient.create` passes the body unchanged (`base.client.ts:23-25`). Step 2 uses `api.parts.retrieve(pk)` with the pk from step 1.
- **Order and titles:** two steps, in case order, titled `<n>. <request>`.
- **Prerequisites:** `test.use({ user: 'engineer' })` (l.4) matches the case; no data or settings prerequisites, and none are created.
- **Cleanup:** `data.trackPart(body.pk)` (l.15) runs in the creating step, right after the status check and before the business assertion, so a failing `active` check still cleans up.
- **Schema:** the case states no schema check, and the spec correctly adds none.
- **Traceability:** `// case:` header (l.1), title `API-CRUD-003: A part created without \`active\` is active` matches the case heading, `describe('Part and category CRUD')`, tag `@regression` matches Tags: Regression.
- **Review status:** Approved.
- **Fixme:** none.

## C. Conventions

No new client methods (only `create` and `retrieve` from `ResourceClient`); §3 structure, §5 import from `fixtures/index.ts`, §7 no URLs or hosts, §8 unique QA name and cleanup, §9 naming: all pass. No findings.

## D. SOLID and design

Spec tests one case, depends only on `api` and `data` fixtures (no endpoints or request context), requests only the fixtures it uses; no client changes or duplication. No findings.

## E. Playwright and TypeScript practice

All matchers and calls awaited; no conditionals, loops, `try/catch` or `test.only`; no dependence on demo data; `const` everywhere except the cross-step `pk`. See Info 1-3.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/CRUD/api-crud-003.spec.ts:14,22` | TypeScript practice | `res.json()` returns `any`, so `body.pk` and `body.active` are unchecked. Same pattern as API-CRUD-001/002; acceptable as the assertions themselves check the values. | Optional: `const body: ApiRecord = await res.json()`. |
| 2 | Info | `tests/CRUD/api-crud-003.spec.ts:9` | Readability | `let pk = 0` is a sentinel shared across steps; if step 1 failed, step 2 would not run, so 0 is never sent. Same pattern as API-CRUD-001. | None required. |
| 3 | Info | `tests/CRUD/api-crud-003.spec.ts:13-16` | Case coverage | The case Notes say the schema declares no default for `Part.active` (`openapi-parts.yaml` `Part.active`: type boolean, no `default`); the spec relies on the docs' default, as the case does. I did not run the test, so the 1.5.6 behaviour is unverified by me. | None. |

## Outside scope

None.
