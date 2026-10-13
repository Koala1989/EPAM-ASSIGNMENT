# Review: API-CRUD-001 Create a part with name, description and category

| Item | Value |
|---|---|
| Spec | `tests/CRUD/api-crud-001.spec.ts` |
| Case | `test-cases/API_CRUD/part-and-category-crud.md` (API-CRUD-001), Review: Approved (2026-10-13) |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-10-13 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 2 Info |

## A. Automated checks

- `npm run typecheck` (`tsc --noEmit`): pass, no errors.
- `npx eslint tests/CRUD/api-crud-001.spec.ts clients/base.client.ts clients/parts.client.ts clients/index.ts fixtures/index.ts fixtures/api.fixture.ts fixtures/data.fixture.ts fixtures/expect.ts`: pass, no errors or warnings.
- `npx playwright test tests/CRUD/api-crud-001.spec.ts --list`: lists `[api] › CRUD\api-crud-001.spec.ts:7:7 › Part and category CRUD › API-CRUD-001: Create a part with name, description and category` (plus the `api-smoke` setup project).

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `POST /api/part/` as `engineer`, `{"name": "QA-<suffix> Resistor 10k", "description": "QA API part", "category": <category pk>}` | `201 Created` | `1. POST /api/part/ as engineer` (L19) | `toHaveStatus(201)` (L21) | Covered |
| 1 | | Body valid against `Part` | | `toMatchSchema('Part')` (L22) | Covered |
| 1 | | `name`, `description`, `category` equal the payload | | `toBe(payload.name/description/category)` (L25-27) | Covered |
| 1 | | `pk` is an integer | | `expect(Number.isInteger(body.pk)).toBe(true)` (L28) | Covered |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | `200 OK` | `2. GET /api/part/<pk from step 1>/ as engineer` (L31) | `toHaveStatus(200)` (L33) | Covered |
| 2 | | Body valid against `Part` | | `toMatchSchema('Part')` (L34) | Covered |
| 2 | | `name`, `description`, `category` equal the payload of step 1 | | `toBe(payload.*)` (L36-38) | Covered |

- **Request fidelity:** pass. `api.parts.create(payload)` -> `ResourceClient.create` posts the body unchanged to `part/`; payload fields and values match the case (`data.name('Resistor 10k')` yields `QA-<8 hex> Resistor 10k`; description literal `'QA API part'`; `category.pk`). `api.parts.retrieve(pk)` -> `GET part/<pk>/`.
- **Order and titles:** pass. Two steps, in case order, titled `<n>. <request>`.
- **Prerequisites:** pass. `test.use({ user: 'engineer' })` (L4) matches the case; token pre-step is done by the `api` fixture (`tokenFor`); category `QA-<suffix> Category` created as admin through `data.category(data.name('Category'))` (L11). No settings.
- **Cleanup:** pass. `data.trackPart(body.pk)` (L24) in the step that creates the part; the category is tracked by `data.category`. Reverse-order disposal deletes the part (deactivate then delete) before the category (`delete_parts: false, delete_child_categories: false`), matching the case's Postconditions.
- **Schema:** pass. `requirements/openapi-parts.yaml` `part_create` `201` -> `#/components/schemas/Part` (L771-776); `GET /api/part/{id}/` `200` -> `#/components/schemas/Part` (L2724-2728).
- **Traceability:** pass. Header L1 `// case: test-cases/API_CRUD/part-and-category-crud.md (API-CRUD-001)`; title equals `<case ID>: <case title>`; `describe('Part and category CRUD')`; tags `@smoke`, `@regression` match Tags "Smoke, Regression".
- **Review status:** Approved.
- **Fixme:** none used; not needed.

## C. Conventions

- §3 structure, first line, import from `../../fixtures`, `test.use`, describe, single test, `data.*` prerequisites first, status-first assertions, `toBe` on parsed body: pass.
- §4 no new client methods or clients; `PartsClient` and `ResourceClient` unchanged and return raw responses: pass.
- §5 fixtures used through `fixtures/index.ts`; only `api` and `data` requested: pass.
- §6/§7 no hosts, URLs, credentials, `process.env` or raw requests in the spec: pass (lint confirms).
- §8 unique `QA-` names, no demo-record dependence: pass.
- §9 file name, test title, step titles, tags: pass.
- See Findings for Info items.

## D. SOLID and design

- Single responsibility (one resource per client, one case per spec), open/closed (no flags added), Liskov (`PartsClient` keeps `ResourceClient` contract), interface segregation (only `api`, `data`), dependency inversion (spec uses clients/fixtures only), no duplication: pass.

## E. Playwright and TypeScript practice

- All `toHaveStatus`/`toMatchSchema` awaited; no conditionals, loops, `try/catch`, `test.only`; isolated data; no `any` annotations, casts or non-null assertions; `const` except the cross-step `pk`: pass. See Findings for Info items.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/CRUD/api-crud-001.spec.ts:17` | §E readability, `const` by default | `let pk = 0;` is a mutable sentinel shared between steps. This is the usual Playwright way to pass a value from one `test.step` to the next, and step 2 cannot run if step 1 fails, so there is no functional problem. | Optional: return the pk from step 1 (`const pk = await test.step('1. ...', async () => { ...; return body.pk; })`) to keep it `const`. |
| 2 | Info | `tests/CRUD/api-crud-001.spec.ts:23-28` | §E TypeScript | `const body = await res.json()` is implicitly `any`, so `body.pk` passed to `trackPart(pk: number)` is not type-checked. The `toMatchSchema('Part')` assertion on L22 runs first and guarantees `pk` is an integer at run time, so this is only a static-typing note. | None required. |

## Outside scope

- None found in the framework code read (`clients/base.client.ts`, `clients/parts.client.ts`, `clients/index.ts`, `fixtures/*.ts`, `utils/names.ts`).
