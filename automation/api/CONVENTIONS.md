# API automation conventions

Rules for the Playwright + TypeScript API suite of the InvenTree Parts module (1.5.6, API 530). Every spec, client, fixture and utility follows them; agents read this file before writing or reviewing code. Lint and type check enforce the parts marked as such (§12).

## 1. Layers

| Layer | Folder | Holds | Never holds |
|---|---|---|---|
| Tests | `tests/<Area>/` | One spec per Approved API case: the case's steps as `test.step`s, and every assertion | Raw `get`/`post`/... calls, paths, hosts, setup logic |
| Clients | `clients/` | One class per REST resource: methods that send a request and return the raw `APIResponse` | Assertions, test data, retries, fixing up the payload |
| Fixtures | `fixtures/` | Authentication per user (`api`, `apiAs`), test data with cleanup (`data`), custom matchers (`expect`) | Business assertions of a case |
| Utilities | `utils/` | Stateless helpers: tokens and request contexts, QA names, the schema validator | State shared between tests |
| Data and config | `data/`, `config/`, `playwright.config.ts` | Demo users, environment values, runner settings | Test logic |

Specs depend on clients and fixtures, never on endpoints or the request context directly.

## 2. Folder layout

```
automation/api/
├── CONVENTIONS.md
├── playwright.config.ts      # projects: api-smoke (setup) -> api
├── config/env.ts             # re-exports ../../shared/config/env.ts (env, users, userNames, credentialsFor)
├── utils/
│   ├── api-context.ts        # tokenFor(user), apiContext(token)
│   ├── schema.ts             # schemaErrors(component, body): Ajv against requirements/openapi-parts.yaml
│   └── names.ts              # QA-<8 hex> names
├── clients/
│   ├── base.client.ts        # ResourceClient: list, create, retrieve, update, partialUpdate, destroy
│   ├── parts.client.ts       # part/
│   ├── categories.client.ts  # part/category/
│   ├── supplier-parts.client.ts  # company/part/
│   ├── auth.client.ts        # user/me/token/
│   └── index.ts              # Clients bundle, clientsFor(context)
├── fixtures/
│   ├── api.fixture.ts        # user option, api, apiAs
│   ├── data.fixture.ts       # TestData: QA records via admin, cleanup
│   ├── expect.ts             # toHaveStatus, toMatchSchema
│   └── index.ts              # merged test + expect: the only import for specs
├── tests/
│   ├── setup/api.setup.ts    # tokens for every demo user, validator self-check
│   └── <Area>/api-<area>-NNN.spec.ts
└── reviews/                  # api-test-reviewer output
```

## 3. Test layer (`tests/`)

- **One spec per Approved case:** `tests/<Area>/<case id in lower case>.spec.ts`, e.g. `tests/CRUD/api-crud-001.spec.ts`. First line: `// case: test-cases/API_<Area>/<file>.md (<case ID>)` (the case folders are `API_`-prefixed; `tests/<Area>/` here is not).
- **Structure:** `import { test, expect } from '../../fixtures';` · `test.use({ user: '<user>' })` from the case's Prerequisites · `test.describe('<functionality>')` · one `test('<case ID>: <case title>', { tag: [...] }, ...)` · prerequisites through `data.*` first · one `test.step('<n>. <request>', ...)` per case step, in order.
- **Every Expected result is asserted, as specifically as the case states it:**
  - **Status first:** `await expect(res).toHaveStatus(201)`. Never `toBeOK()` or a range when the case states a code.
  - **Schema:** `await expect.soft(res).toMatchSchema('<component>')` whenever the case says the body is valid against a schema component. Always `expect.soft`: a schema violation is reported and fails the test, but the step's status, value and business-rule checks still run. Everything else stays a hard `expect`.
  - **Cleanup first:** register a record the request under test creates (`data.trackPart(body.pk)`) right after the status check, before the schema check or any value check, so a failure never leaves it behind.
  - **Values:** each field the case names, with `toBe`/`toEqual` on the parsed body (`const body = await res.json()`). `toMatchObject` only for "contains at least these fields".
  - **Business rule:** a follow-up request that proves it (the record exists, was not created, was changed), when the case states one.
- **Negative cases send exactly the invalid input** the case gives. Never let a client or helper "correct" it.
- **No conditional logic, loops over responses, `try/catch` or `test.only`** in specs. `test.fixme()` only with a `// FINDING:` or `// CASE DEFECT:` comment (§11), and never for a schema violation: that is a soft check and stays in the run.
- **No raw requests** (`.get(`, `.post(`, ...), no `@playwright/test` imports, no hosts or full URLs (lint).

## 4. Client layer (`clients/`)

- One class per resource, extending `ResourceClient` with its endpoint path relative to `/api/` (`'part/'`). Methods: `list(params)`, `create(body)`, `retrieve(id)`, `update(id, body)` (PUT), `partialUpdate(id, body)` (PATCH), `destroy(id, body?)`.
- **Return the raw `APIResponse`.** The spec decides what status is expected; a client never throws on a 4xx.
- **Send exactly what you are given:** no defaults added, no fields removed, no retries.
- **Never assert** (lint: no `expect` import in `clients/`).
- A request a case needs that no method covers (a sub-endpoint such as `part/{id}/serial-numbers/`, a form-encoded body, a custom header) gets a new, intention-named method on the right client, with a one-line doc comment. A new resource gets a new client, added to `Clients` in `clients/index.ts`.

## 5. Fixtures layer (`fixtures/`)

- Specs import `test` and `expect` only from `fixtures/index.ts` (lint).
- **`user` option and `api`:** `test.use({ user: 'engineer' })` gives `api`, the full set of clients authenticated as that user with an InvenTree API token (`Authorization: Token <key>`, from `GET /api/user/me/token/`, cached per worker). A spec without a `user` fails at once.
- **`apiAs(caller)`:** clients for another caller within the same test: a demo user, `'anonymous'` (no credentials) or `{ token: '<value>' }` (e.g. an invalid token). Use it for permission and authentication cases; contexts are disposed after the test.
- **`data`:** prerequisite records created as admin with `QA-<8 hex>` names (`data.name('Resistor')`), deleted after the test in reverse order: `data.category`, `data.part`, `data.company`, `data.location`, `data.supplierPart`, `data.post`, `data.setSetting` (restored afterwards). A record created by the request under test is registered at once with `data.trackPart(pk)`, `data.trackCategory(pk)` or `data.trackSupplierPart(pk)`.
- **`expect`:** Playwright's `expect` plus `toHaveStatus(code)` (failure message shows the body) and `toMatchSchema(component)` (on a response or a parsed value).

## 6. Utility layer (`utils/`)

- Stateless helpers only. `schemaErrors(component, body)` validates against `components.schemas.<component>` of `requirements/openapi-parts.yaml`, converting OpenAPI `nullable` to JSON Schema. Validation is **strict**: a response that breaks its schema fails, even when the cause is InvenTree itself (findings F-06, F-07).

## 7. Data and configuration layer

- `config/env.ts` re-exports `automation/shared/config/env.ts`, shared with the UI suite and the only reader of `process.env` (lint). `TEST_ENV` (default `local`) selects `automation/shared/environments/<env>.json` (base URL, timeouts, users file); `INVENTREE_URL` and the timeout variables override it. `credentialsFor(user)` gives the login name and password (`INVENTREE_<USER>_PASSWORD`, or the demo dataset's published passwords for `local` only). Put them in the gitignored `automation/shared/.env.<env>` (template `.env.example`); variables already set win over the file.
- No hosts, ports, full URLs, passwords or tokens anywhere else (lint for URLs). Clients use paths relative to `/api/`.
- `automation/shared/data/users.<env>.json`: the test users (login name, display name, role) for the environment, same keys in every environment. Pick the least-privileged user that can make the call, as the case says.

## 8. Test data and isolation

- Each test creates what it needs and cleans it up; never depend on demo records, other tests or test order.
- Specs run serially (`workers: 1`). InvenTree 1.5.6 rebuilds the whole part or category tree on every delete, and two cleanups at once deadlock in PostgreSQL (HTTP 500). Never re-enable parallel runs.
- Names are unique per test (`QA-<8 hex>`), so runs never collide on data.
- Never delete records the test did not create. Report `QA-` leftovers.
- Settings changed with `data.setSetting` are restored after the test; a case that changes a global setting is tagged `@settings`.

## 9. Naming

| Item | Pattern | Example |
|---|---|---|
| Spec file | `tests/<Area>/<case id lower>.spec.ts` | `tests/VAL/api-val-003.spec.ts` |
| Test title | `<case ID>: <case title>` | `API-VAL-003: Part name longer than 100 characters is rejected` |
| Step title | `<n>. <request as in the case>` | `1. POST /api/part/ as engineer` |
| Client | `<Resource>Client` in `<resource>.client.ts` | `CategoriesClient` |
| Client method | intention, camelCase | `serialNumbers(id)` |
| Tags | from the case's Tags | `@smoke`, `@regression`, `@permissions`, `@settings`, `@cross-functional` |

## 10. InvenTree API patterns observed (1.5.6)

| Pattern | Detail |
|---|---|
| Authentication | Every operation needs credentials; the suite uses token auth. Tokens come from `GET /api/user/me/token/` with basic auth; every demo user, including `noaccess`, can get one. |
| Lists | Paginated with `limit`/`offset`: `{ count, next, previous, results }` (R-LST-01) **only when `limit` is sent**; without it the response is a plain array of every record (F-09). Always send `limit`. |
| Required on input | `required` in the schema includes read-only response fields; only fields that are required and not `readOnly` must be sent (schema issue 4). |
| Deleting a part | A part must be inactive before it can be deleted; `data` handles this for cleanup. |
| Deleting a category | Needs a JSON body with both `delete_parts` and `delete_child_categories`; without them `400`, before the ID is looked up (not in the schema, F-08). Both `false` moves the category's parts and child categories up to its parent. |
| Deleting a stock location | Needs a JSON body with both `delete_stock_items` and `delete_sub_locations`, else `400` (not in the schema). `data` sends both `false`. |
| Not found | `GET`, `PATCH` and `DELETE` of a part or category that does not exist return `404` with `{"detail": "No Part matches the given query."}` (`PartCategory` for categories). Architect's rule for `GET` and `DELETE` (Q-CRUD-01). |
| Deleting an active part | `400` `{"non_field_errors": ["Cannot delete this part as it is still active"]}`. |
| Bulk update | `PATCH`/`PUT` on a list endpoint with `{ "items": [pk, ...], <fields> }` returns `200` `{ "success", "items" }` (F-10); without `items` `400`. Never `?all=true`. |
| Schema deviations | `Part.image` is a relative path, not a URI (F-06); `SupplierPart.availability_updated` is not RFC 3339 (F-07); list without `limit` (F-09); bulk response shape (F-10); `Part.category_name` missing when the part has no category (F-11); `Part.pricing_updated` not RFC 3339 once the part has stock (F-12). None of these is suppressed: a soft `toMatchSchema` that hits one fails the test, and its message labels each error with the finding (`[F-11]`) or `[NEW]`. The labels come from `KNOWN_DEFECTS` in `utils/schema.ts`; the architect adds an entry when a new schema defect is recorded. |

## 11. Agents

- **`api-test-generator`** writes one spec per Approved API case, runs it, and fixes how it runs until it passes three times in a row. It may add client methods or clients (additions only, §4) and never changes what a spec asserts. A schema violation is never a fixme: the soft check reports it (§5). When InvenTree's status code or values differ from the case, it marks the test `test.fixme()` with `// FINDING: case <ID> step <n> expects <X>; InvenTree 1.5.6 returns <Y>.` (or `// CASE DEFECT:` when the case looks wrong) and reports it.
- **Client changes by agents are additions only:** new methods or clients. Renaming, removing or changing an existing method is the architect's decision.
- **`api-test-reviewer`** (a stronger model than the generator) reviews a spec independently, without the generator's reasoning: conventions, coverage of every case step and Expected result, SOLID design, Playwright and TypeScript practice. It runs lint and type check, never runs the tests or edits code, and saves `reviews/<case id>-review-<date>.md` with a verdict.

## 12. Quality gates

- `npm run typecheck` and `npm run lint` pass. Lint enforces: no raw requests or `@playwright/test` imports in specs (§3, §5), no `expect` in clients (§4), no hosts or full URLs outside `config/env.ts` (§7), no `process.env` outside `config/env.ts` and `playwright.config.ts` (§7).
- `npm test` runs `api-smoke` then all specs; `npm run test:smoke` runs `@smoke` only.
- A spec counts as done only when three runs in a row (`npx playwright test <spec> --project=api --repeat-each=3`) all pass, or all fail only on known product defects: a run whose only failures are soft `toMatchSchema` errors all labelled with a recorded finding (`Known product defects only: F-..`). It also needs an `api-test-reviewer` verdict of Approve or Approve with changes. A `[NEW]` schema error is a new finding for the architect, not done.
