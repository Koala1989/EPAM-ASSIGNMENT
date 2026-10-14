# Review: API-CRUD-012 Make a part inactive with PATCH

| Item | Value |
|---|---|
| Spec | `tests/CRUD/api-crud-012.spec.ts` |
| Case | `test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md` (API-CRUD-012), Review: Approved (2026-10-13) |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-10-13 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 0 Major, 1 Minor, 2 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass, no errors |
| `npx eslint tests/CRUD/api-crud-012.spec.ts clients/base.client.ts clients/parts.client.ts clients/index.ts fixtures/index.ts fixtures/data.fixture.ts fixtures/api.fixture.ts fixtures/expect.ts` | Pass, no errors or warnings |
| `npx playwright test tests/CRUD/api-crud-012.spec.ts --list` | Lists 1 test in project `api` (plus `api-smoke` setup) |

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `PATCH /api/part/<pk>/` as `engineer`, `{"active": false}` | `200 OK` | `1. PATCH /api/part/<pk>/ as engineer` (L11) | `await expect(res).toHaveStatus(200)` (L13) | Covered |
| 1 | | Body valid against `Part` | L11 | `await expect.soft(res).toMatchSchema('Part')` (L14) | Covered |
| 1 | | `active` is `false` | L11 | `expect(body.active).toBe(false)` (L16) | Covered |
| 2 | `GET /api/part/<pk>/` as `engineer` | `200 OK` | `2. GET /api/part/<pk>/ as engineer` (L19) | `await expect(res).toHaveStatus(200)` (L21) | Covered |
| 2 | | `active` is `false` | L19 | `expect(body.active).toBe(false)` (L23) | Covered |
| 2 | | `name` is unchanged | L19 | `expect(body.name).toBe(name)` (L24) | Covered |

- **Request fidelity:** `api.parts.partialUpdate(part.pk, { active: false })` sends PATCH to `part/<pk>/` with exactly the case's payload; `retrieve` sends GET. Pass.
- **Order and titles:** two steps, in case order, titled `<n>. <request>`. Pass.
- **Prerequisites:** `test.use({ user: 'engineer' })` matches; the part is created as admin through `data.part` with a `data.name('Deactivate')` name (`QA-<8 hex> Deactivate`, as the case states). The part's initial `active` state is not established or checked (finding 1). The extra `description: 'Seed API part'` is not in the case (finding 2).
- **Cleanup:** the request under test creates no record; the prerequisite part is registered by `data.part` (`trackPart`) and deleted after the test. Pass.
- **Schema:** the schema's `PATCH /api/part/{id}/` `200` response is `$ref: '#/components/schemas/Part'` (`openapi-parts.yaml` L2797-L2801); the spec uses `'Part'` with `expect.soft`. Pass. The case states no schema for step 2, and none is checked. Pass.
- **Traceability:** `// case:` header, title `API-CRUD-012: Make a part inactive with PATCH`, describe `Part and category CRUD`, tag `@regression` matching Tags `Regression`. Pass.
- **Review status:** Approved. Pass.
- **Fixme:** none. Pass.

## C. Conventions

No new client methods or clients (uses `ResourceClient.partialUpdate` and `retrieve`, unchanged). Imports only from `../../fixtures` (§5); no raw requests, paths or URLs (§3, §7); data through `data.*` (§8); file, title, step and tag naming per §9. All pass; see findings table.

## D. SOLID and design

Spec tests one case; depends only on `api` and `data` fixtures (dependency inversion, interface segregation); no client changes, so open/closed and Liskov are unaffected; no duplication with existing client methods. All pass.

## E. Playwright and TypeScript practice

Every request and `toHaveStatus`/`toMatchSchema` awaited; no conditionals, loops, `try/catch` or `test.only`; `const` throughout; no `any` annotations, casts or non-null assertions; unique QA name, no demo data or order dependence. All pass; see findings table.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Minor | `tests/CRUD/api-crud-012.spec.ts:9` | Case Prerequisites ("active part"), Technique "State transition (Active to Inactive)" | The start state of the transition is implicit: the part is created without `active` and the spec never confirms it is active, so the test would still pass if InvenTree created it inactive (the schema gives `Part.active` no default, `openapi-parts.yaml` L4112). | Create it with `data.part(name, { ..., active: true })` so the prerequisite is explicit, or assert `part.active` is `true` before step 1. |
| 2 | Info | `tests/CRUD/api-crud-012.spec.ts:9` | Case Prerequisites | `description: 'Seed API part'` is not stated by the case. Harmless setup data (other CRUD specs use the same seed), not part of the request under test. | None required; drop it if InvenTree does not need it to create a part. |
| 3 | Info | `tests/CRUD/api-crud-012.spec.ts:14` | §10 Schema deviations (F-11) | The part has no category, so the soft `toMatchSchema('Part')` can fail on the known defect F-11 (`category_name` missing). This is correct behaviour per §10/§12 (known-defect-only failure), not a spec problem; noted so the 3-run result is read accordingly. | None. |

## Outside scope

None.
