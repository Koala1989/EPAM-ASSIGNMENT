# Automation conventions: UI and API

**Status: UI part approved 2026-10-12; API part 2026-10-13; merged into one project 2026-10-14.** One Playwright + TypeScript project in `automation/` automates the Approved manual cases in `test-cases/` against InvenTree 1.5.6: UI cases through the browser, API cases through the REST API. These conventions apply to people and to every automation agent (`playwright-test-generator`, `playwright-test-healer`, `playwright-test-reviewer`, `api-test-generator`, `api-test-reviewer`).

**How to read it.** *Shared* applies to both suites. Then a UI part and an API part, each with the same twelve sections. References say which part: `Shared §3`, `UI §4`, `API §4`. UI agents read Shared and UI; API agents read Shared and API.

## Shared

### Shared 1. One project, two suites

| Suite | Playwright project | Runs first (dependency) | Tests | Command (from `automation/`) |
|---|---|---|---|---|
| UI | `chromium` | `login-smoke`: every demo user logs in and out through the UI | `tests/ui/` | `npm run test:ui` |
| API | `api` | `api-smoke`: every demo user gets a token; the schema validator self-check | `tests/api/` | `npm run test:api` |

- `npm test` runs both; `npm run test:smoke` runs `@smoke` only; `npx playwright test <spec>` runs one spec with its setup project.
- **Serial (`workers: 1`, `fullyParallel: false`) for both suites:** UI tests change global InvenTree settings that a parallel test would see (UI §8), and concurrent part or category deletes deadlock InvenTree's tree rebuild (API §8).
- The API project opens no browser, so an API-only run needs no browser install.

### Shared 2. Folder layout

```
automation/
├── playwright.config.ts        projects: login-smoke -> chromium (tests/ui), api-smoke -> api (tests/api); reads config/env.ts
├── CONVENTIONS.md
├── package.json, tsconfig.json, eslint.config.mjs   quality gates (UI §12, API §12)
├── config/
│   ├── env.ts                  the only reader of process.env: env, users, userNames, credentialsFor
│   ├── environments/<env>.json base URL, timeouts, users file, demo passwords on/off
│   └── .env.example            template for the gitignored .env.<env> (passwords, overrides)
├── data/
│   ├── users.<env>.json        test users per environment: login name, display name, role (no passwords)
│   └── <Area>/<name>.json      UI input matrices for data-driven tests
├── utils/
│   ├── names.ts                QA-<8 hex> suffix and test record names
│   ├── api-context.ts          tokenFor(user), apiContext(token): authenticated APIRequestContext
│   └── schema.ts               schemaErrors(component, body), KNOWN_DEFECTS: Ajv against requirements/openapi-parts.yaml
├── fixtures/
│   ├── index.ts                the merged `test` and `expect` every spec imports
│   ├── user.fixture.ts         the `user` option both suites share
│   ├── auth.fixture.ts         UI: `page` logs in as `user` through the login form; `switchUser`
│   ├── pages.fixture.ts        UI: page objects injected into tests
│   ├── api.fixture.ts          API: `api` (clients as `user`), `apiAs(caller)`
│   ├── data.fixture.ts         both: `data`, QA test data through the API as admin, cleanup, settings restore
│   └── expect.ts               both: Playwright's expect plus toHaveStatus, toMatchSchema
├── pages/                      UI page objects; components/ for InvenTree widgets (UI §4)
├── clients/                    API clients, one per REST resource (API §4)
├── tests/
│   ├── ui/setup/login.setup.ts, ui/seeds/<user>.seed.spec.ts, ui/<Area>/ui-<area>-NNN.spec.ts
│   └── api/setup/api.setup.ts, api/<Area>/api-<area>-NNN.spec.ts
└── reviews/ui/, reviews/api/   reviewer reports, one per spec per review
```

### Shared 3. Configuration, environments, users and secrets

- **`config/env.ts`** is the single place that reads `process.env` (lint). Tests, fixtures, page objects, clients and utilities import from it.
- **Environments:** `local` (default: the pinned 1.5.6 Docker instance) and `demo-web` (demo.inventree.org, 1.6.0 dev, run only by the architect). `TEST_ENV` selects `config/environments/<env>.json`: base URL, timeouts, users file, and whether the demo passwords apply. `INVENTREE_URL`, `TEST_TIMEOUT_MS` and `EXPECT_TIMEOUT_MS` override it. Run another environment with `$env:TEST_ENV='<env>'; npm test` (PowerShell).
- **Secrets** come only from environment variables or the gitignored `config/.env.<env>` (template `config/.env.example`); variables already set win over the file. The demo dataset's passwords are defaults only for `local`; any other environment sets `INVENTREE_<USER>_PASSWORD`. `credentialsFor(user)` returns the login name and password.
- **Users:** `data/users.<env>.json` maps each user key specs use (`engineer`, `reader`, ...) to its login name, display name (the accessible name of the UI's user menu, used to log out), role and purpose. No passwords. Every environment defines the same keys as `users.local.json`.
- **No hosts, ports, full URLs or credentials** outside `config/` and `data/`. Lint rejects full URLs in API specs, clients, page objects, fixtures and utilities; UI specs may contain a URL only as test data typed into a field.

### Shared 4. Shared fixtures

- **One import for every spec:** `import { test, expect } from '../../../fixtures';` (lint). `fixtures/index.ts` merges all fixture files with `mergeTests`; fixtures are lazy, so a UI spec builds no API clients it does not use and an API spec opens no browser.
- **`user`** (`user.fixture.ts`): `test.use({ user: 'engineer' })`, the user from the case's Prerequisites. UI: `page` logs in as this user through the real login form (UI §5). API: `api` sends requests as this user (API §5).
- **`data`** (`data.fixture.ts`): prerequisite records created through the API as `admin` with unique `QA-<8 hex>` names (`data.name('Resistor')`) and removed after the test in reverse order: `category`, `part`, `company`, `location`, `supplierPart`, `stockItem`, `post`; `setSetting` restores the setting afterwards. A record the test itself creates is registered at once: API `data.trackPart(pk)` (also `trackCategory`, `trackSupplierPart`), UI `data.trackPart(name)`; `data.findParts(name)` finds parts by exact name. A cleanup error fails the test with the records that could not be removed.
- **`expect`** (`expect.ts`): Playwright's `expect` plus `toHaveStatus(code)` and `toMatchSchema(component)` (API §5).

## UI part

**Status: approved 2026-10-12.** Conventions for the UI suite (`tests/ui/`, `pages/`), which automates the Approved manual cases in `test-cases/<Area folder>/` against InvenTree 1.5.6. They apply to people, to the `playwright-test-generator` and `playwright-test-healer` agents, and to Copilot.

### UI 1. Layers

The suite has five layers. Each layer may only use the layers below it.

```
Tests            tests/ui/<Area>/*.spec.ts           what is tested: workflow + assertions
  ↓ uses
Fixtures         fixtures/                         setup, teardown, users, injected page objects, test data
  ↓ uses
Page objects     pages/                            locators + actions per page and per InvenTree widget
  ↓ uses
Utilities        utils/                            stateless helpers
Data & config    data/, config/, playwright.config.ts   environment values, users, input matrices (Shared §3)
```

| Layer | May import | Must not |
|---|---|---|
| Tests | fixtures, data | use `page.locator`/`getBy*` directly, call the API directly, hard-code URLs, IDs or credentials |
| Fixtures | pages, utils, data, config | contain assertions about the feature under test |
| Page objects | utils, config, other page objects and components | contain `expect` about business outcomes, create test data, know which user is logged in |
| Utilities | config | hold state, import Playwright test fixtures |
| Data & config | nothing | contain code beyond reading environment variables |

### UI 2. Folder layout

UI code lives in `tests/ui/`, `pages/` and `reviews/ui/`; fixtures, utilities, data and config are shared (Shared §2).

### UI 3. Test layer (`tests/`)

Tests read like the manual case: the workflow and the checks, nothing else.

- **One test per Approved manual case.** File `tests/ui/<Area>/<case id in lower case>.spec.ts`; title `<case ID>: <case title>`; a `test.describe` per functionality (the case file's title).
- **Traceability.** First line: `// case: test-cases/<Area folder>/<file>.md (<case ID>)`. Tags from the case's Tags field: `{ tag: ['@smoke', '@regression'] }`.
- **One `test.step` per case step**, titled `<n>. <case action>`, so the HTML report and trace show the case's steps.
- **Assertions live in tests.** Each Expected result of the case is at least one `expect` in its step. Use web-first assertions (`toBeVisible`, `toHaveText`, `toHaveURL`, `toHaveValue`). Page objects return locators or values; the test asserts on them.
- **No raw DOM access.** No `page.locator`, `page.getBy*`, CSS or XPath in a test. If a page object lacks what the step needs, add it to the page object.
- **No setup logic.** Prerequisite records, users and settings come from fixtures.
- **Data-driven tests** loop over a matrix from `data/` and create one `test` per row, with the row's label in the title.

```ts
// case: test-cases/Part_Creation_and_Import/part-creation-flow.md (UI-Part-001)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Part creation flow', () => {
  test('UI-Part-001: Create a part with only the required fields', { tag: ['@smoke', '@regression'] },
    async ({ partsPage, partForm, partDetail, data }) => {
      const category = await data.category(data.name('Category'));
      const partName = data.trackPart(data.name('Resistor 10k'));

      await test.step('1. Open Add Parts and select Create Part', async () => {
        await partsPage.open();
        await partsPage.addParts('Create Part');
        await expect(partForm.root).toBeVisible();
      });

      await test.step('2. Fill in the required field and the category only', async () => {
        await partForm.fill({ name: partName, category: String(category.name) });
        await expect(partForm.form.invalidFields).toHaveCount(0);
      });

      await test.step('3. Submit', async () => {
        await partForm.submit();
        await expect(partDetail.detail('Name')).toHaveText(partName);
      });
    });
});
```

### UI 4. Page object layer (`pages/`)

Page objects hold every locator and every UI action. Tests and fixtures never touch the DOM.

- **One class per page or form**, named `<Name>Page` in `<name>.page.ts`. Reusable InvenTree widgets are **components** (`<Name>Component` in `components/<name>.component.ts`), composed into pages, not inherited.
- **`BasePage`** holds what every screen has: the navigation menu, global search, notifications, and helpers to get the shared components. Every page object extends it.
- **Constructor** takes the Playwright `Page` (and a root locator for components). Locators are `readonly` properties defined in the constructor; actions are `async` methods.
- **Locator priority:** `getByRole` with the accessible name → `getByLabel` → `getByPlaceholder` → `getByText` → `getByTestId`. InvenTree exposes many `aria-label`s (e.g. `navigation-menu`, `login-username`); reach them through `getByRole(role, { name })`. CSS or XPath only when nothing else identifies the element, with a comment saying why. No `nth()` without a comment.
- **Methods are user intentions**, named as verbs in the UI's language: `addParts('Create Part')`, `openTab('Suppliers')`, `selectRevision('B')`. Not `clickButton3()`.
- **Methods wait for their own result** (the form opened, the page navigated) with web-first checks, so tests never need sleeps. They do not assert business outcomes; that is the test's job.
- **Methods return** `void`, a locator, a value read from the UI, or the next page object when the action navigates.
- **No test data, no users, no API calls** in page objects.

### UI 5. Fixtures layer (`fixtures/`)

Fixtures prepare what a test needs and clean it up afterwards.

- **Import path.** Every spec imports `test` and `expect` from `fixtures/index.ts` (Shared §4). Never import `test` from `@playwright/test` in a spec.
- **Real login, like a user.** `test.use({ user: 'engineer' })` makes the fixture log in through the login form (`LoginPage.loginAs`) before the test body; no saved sessions or cookies are used. Without it the test's `page` starts logged out. A case that changes user ("log out, log in as allaccess") calls `switchUser('allaccess')`: it logs out through the user menu and logs in as the other user in the same page, so the test continues with the same page objects.
- **Login smoke check.** The `login-smoke` project (`tests/ui/setup/login.setup.ts`) runs first and checks that every demo user can log in and out; the other tests depend on it, so a broken login stops the run early instead of failing every test. Single-spec agent runs skip it (`--no-deps`, or `SKIP_LOGIN_SMOKE=1`, which `.mcp.json` sets for the playwright-test MCP server); the full suites keep it.
- **`data`** creates prerequisite records through the API as `admin` with unique `QA-<8 hex>` names, and removes them after the test in reverse order, including stock, supplier and manufacturer parts. Records the test creates through the UI are registered with `data.trackPart(name)` (returns the name) so they are removed too. `data` is shared with the API suite (Shared §4). `data.setSetting(key, value)` changes a global setting and restores it after the test.
- **Page objects** are injected per test by `fixtures/pages.fixture.ts`: `app` (a `BasePage`), `loginPage`, `partsPage`, `partForm`, `partDetail`, built on the test's `page`.
- **Finding records the UI created:** `data.findParts(name)` returns the parts with that exact name (e.g. to get the ID of a part made through the form).
- **Worker-scoped** fixtures only for expensive, read-only things (the admin API context). Everything else is test-scoped, so tests stay independent.
- **Cleanup must not hide failures**: a cleanup error fails the test with the list of records that could not be removed.

### UI 6. Utility layer (`utils/`)

Shared with the API suite (Shared §2). For UI work: `names.ts` (`qaSuffix()`, `qaName(suffix, label)`, `slug(label)`, menu labels to InvenTree's aria-label form). Add a helper only when two or more callers need it. No business assertions here.

### UI 7. Data and configuration layer (`data/`, `config/`, `playwright.config.ts`)

- **Configuration, environments, users and secrets:** Shared §3. `LoginPage` gets the login name and password through `credentialsFor(user)`; specs never contain them.
- **`data/<Area>/<name>.json`** holds UI test inputs as JSON (or CSV) matrices, e.g. boundary values for a field, one row per case variant with a `label` used in the test title: `data/Part/name-boundaries.json`.

### UI 8. Waiting, timing and stability

- No `page.waitForTimeout`, no `waitForLoadState('networkidle')`, no `force: true` (all lint errors). If an overlay covers an element, the page object waits for the overlay to go away.
- Rely on auto-waiting actions and web-first assertions. A page object method that triggers navigation or a form waits for the resulting state.
- One worker (`workers: 1`, Shared §1): some tests change global InvenTree settings, which every parallel test would see.
- A test that fails because InvenTree differs from the case is marked `test.fixme()` with `// FINDING: ...` above the failing step, never "fixed" by changing the assertion.

### UI 9. Naming

| Item | Convention | Example |
|---|---|---|
| Spec file | `<case id lower>.spec.ts` in `tests/ui/<Area>/` | `tests/ui/Part/ui-part-001.spec.ts` |
| Page object | `<name>.page.ts`, class `<Name>Page` | `part-detail.page.ts`, `PartDetailPage` |
| Component | `components/<name>.component.ts`, class `<Name>Component` | `FormComponent` |
| Fixture file | `<name>.fixture.ts` | `data.fixture.ts` |
| Locator property | noun, camelCase, what the user sees | `addPartsButton`, `revisionSelect` |
| Action method | verb phrase in the UI's words | `addParts('Create Part')` |
| Test data names | `data.name('<label>')` → `QA-<8 hex> <label>` | `QA-1A2B3C4D Resistor 10k` |
| Tags | `@smoke`, `@regression`, `@permissions`, `@cross-functional`, `@settings` | |

### UI 10. InvenTree UI patterns observed (1.5.6)

Known behaviour, verified in the app (Playwright MCP exploration and runs, 2026-10-11 and 2026-10-12) and encoded once in pages and components.

**Accessible names.** InvenTree labels its controls consistently; page objects build locators from these patterns:

| Control | Accessible name pattern | Example |
|---|---|---|
| Form field | `<kind>-field-<api field name>` (kind: text, number, boolean, related, tree, tags) | `text-field-name`, `boolean-field-purchaseable`, `related-field-revision_of`, `tree-field-category` |
| Actions menu / item | `action-menu-<menu>` / `action-menu-<menu>-<item>` | `action-menu-add-parts` → `action-menu-add-parts-create-part` |
| Action button | `action-button-<name>` | `action-button-add-part-category` |
| Panel tabs | tab list `panel-tabs-<page>`, tabs by visible name | `panel-tabs-part` → *Suppliers* |
| Table | `table-search-input`, `table-refresh`, `table-select-filters`, `row-action-menu-<n>` | |
| Header | `navigation-menu`, `open-search`, `open-spotlight`, `open-notifications` | |
| Login | `login-username`, `login-password`, button *Log In* | |
| Revision selector | combobox `part-revision-select` | |

**Behaviour:**

| Pattern | Where it belongs |
|---|---|
| Login form re-renders after server info loads: it can clear typed values, and a click on *Log In* during the re-render sends nothing | `LoginPage.loginAs` retries the whole login, with short per-action timeouts, until the app shell appears |
| Header user menu: a button named by the user's display name (no aria-label); menu items *User Settings*, *Change Color Mode*, *About InvenTree*, *Logout*; Logout returns to `/web/login` | `BasePage.userMenu()` / `BasePage.logout()` |
| `/web/part/` lands on the *Part Categories* panel; the parts table and *Add Parts* menu are on the *Parts* panel (`/web/part/category/index/parts`) | `PartsPage.open()` |
| Part detail URL is `/web/part/<id>/details`; header reads `Part: <IPN> \| <name> \| <revision>` | `PartDetailPage` |
| Part Details rows are three cells: label, value, copy button | `PartDetailPage.detail(label)` takes the second cell |
| Related fields search on the server only on real key presses (`fill` does not trigger it); options have no accessible name, so they are matched by visible text (name plus description) | `SelectComponent.search()` / `select()` |
| Tree fields (category, location) filter as you type; options matched by visible text | `SelectComponent.select()` |
| Read-only dropdowns (revision selector) have a hidden dummy input that cannot be clicked; open with focus + ArrowDown | `SelectComponent.choose()` |
| Escape closes the whole modal form, not just an open dropdown | Never press Escape inside a form to close a dropdown |
| Invalid field: `aria-invalid="true"`, error text in its accessible description ("This field is required."); plus a *Form Error* alert in the form | `FormComponent.formError`, assert with `toHaveAccessibleDescription` |
| Pop-up notification after actions, e.g. "Login successful" | `NotificationComponent` |
| Create Part form: *Purchaseable* on by default shows a *Supplier Information* section (Supplier, SKU, Manufacturer, MPN); the URL field is labelled *Link* | `PartFormPage` |
| *Revision Of* in the Duplicate Part form does not offer template parts | `PartFormPage.revisionOf` |
| *Suppliers* tab hidden without purchase-order view permission | test prerequisites (user choice), not the page object |

### UI 11. Agents

- **`playwright-test-generator`** writes specs and, when a step needs a locator, action, component or page the framework lacks, adds it to `pages/` (registering new pages in `fixtures/pages.fixture.ts`). It never queries the DOM in a spec.
- **`playwright-test-healer`** may fix page objects, components and fixtures (a broken locator is fixed once, in the page object, not in every spec), add missing page object members, and change the *how* of a spec. It never changes what a spec asserts.
- **Page object changes by agents are additions only**: new locators, methods, components or pages, each confirmed in the live app and following UI §4. Renaming, removing or changing the behaviour of an existing member is the architect's decision (the healer may change *how* a method works, not what it does). Agents list every page object change in their report; `playwright-test-reviewer` reviews them with the spec.
- **`playwright-test-reviewer`** (a stronger model than the generator and healer) reviews a spec independently, without the writers' reasoning: conventions, coverage of every case step and Expected result, SOLID design, Playwright and TypeScript practice. It runs lint and type check, never edits code, and saves `reviews/ui/<case id>-review-<date>.md` with a verdict. A spec counts as done only with an Approve or Approve-with-changes review and three green runs.
- After an agent changes page objects, the main session runs `npm run lint`, `npm run typecheck` and the full suite, so an addition cannot break other specs unnoticed.

### UI 12. Quality gates

- `npm run typecheck` (TypeScript, no emit) and `npm run lint` (ESLint with `eslint-plugin-playwright`) must pass before a spec is committed. The lint configuration enforces these conventions: raw locators or `@playwright/test` imports in a spec (UI §3, UI §5), `process.env` outside `config/env.ts` and `playwright.config.ts` (Shared §3), and `waitForTimeout`, `networkidle` or `force` (UI §8) are errors.
- `npm run test:ui` runs the UI suite (`--project=chromium`, after `login-smoke`); `npm test` runs both suites; `npm run test:smoke` runs `@smoke` only.
- A new or changed spec passes three runs in a row and has a `playwright-test-reviewer` verdict of Approve or Approve with changes before it counts as done.

## API part

Rules for the Playwright + TypeScript API suite of the InvenTree Parts module (1.5.6, API 530). Every spec, client, fixture and utility follows them; agents read this file before writing or reviewing code. Lint and type check enforce the parts marked as such (API §12).

### API 1. Layers

| Layer | Folder | Holds | Never holds |
|---|---|---|---|
| Tests | `tests/api/<Area>/` | One spec per Approved API case: the case's steps as `test.step`s, and every assertion | Raw `get`/`post`/... calls, paths, hosts, setup logic |
| Clients | `clients/` | One class per REST resource: methods that send a request and return the raw `APIResponse` | Assertions, test data, retries, fixing up the payload |
| Fixtures | `fixtures/` | Authentication per user (`api`, `apiAs`), test data with cleanup (`data`), custom matchers (`expect`) | Business assertions of a case |
| Utilities | `utils/` | Stateless helpers: tokens and request contexts, QA names, the schema validator | State shared between tests |
| Data and config | `data/`, `config/`, `playwright.config.ts` | Demo users, environment values, runner settings | Test logic |

Specs depend on clients and fixtures, never on endpoints or the request context directly.

### API 2. Folder layout

API code lives in `tests/api/`, `clients/` and `reviews/api/`; fixtures, utilities, data and config are shared (Shared §2).

### API 3. Test layer (`tests/`)

- **One spec per Approved case:** `tests/api/<Area>/<case id in lower case>.spec.ts`, e.g. `tests/api/CRUD/api-crud-001.spec.ts`. First line: `// case: test-cases/<Area folder>/<file>.md (<case ID>)` (case folders have full names, e.g. `API_Create_Read_Update_Delete`; spec folders use the short Area value, `tests/api/CRUD/`).
- **Structure:** `import { test, expect } from '../../../fixtures';` · `test.use({ user: '<user>' })` from the case's Prerequisites · `test.describe('<functionality>')` · one `test('<case ID>: <case title>', { tag: [...] }, ...)` · prerequisites through `data.*` first · one `test.step('<n>. <request>', ...)` per case step, in order.
- **Every Expected result is asserted, as specifically as the case states it:**
  - **Status first:** `await expect(res).toHaveStatus(201)`. Never `toBeOK()` or a range when the case states a code.
  - **Schema:** `await expect.soft(res).toMatchSchema('<component>')` whenever the case says the body is valid against a schema component. Always `expect.soft`: a schema violation is reported and fails the test, but the step's status, value and business-rule checks still run. Everything else stays a hard `expect`.
  - **Cleanup first:** register a record the request under test creates (`data.trackPart(body.pk)`) right after the status check, before the schema check or any value check, so a failure never leaves it behind.
  - **Values:** each field the case names, with `toBe`/`toEqual` on the parsed body (`const body = await res.json()`). `toMatchObject` only for "contains at least these fields".
  - **Business rule:** a follow-up request that proves it (the record exists, was not created, was changed), when the case states one.
- **Negative cases send exactly the invalid input** the case gives. Never let a client or helper "correct" it.
- **No conditional logic, loops over responses, `try/catch` or `test.only`** in specs. `test.fixme()` only with a `// FINDING:` or `// CASE DEFECT:` comment (API §11), and never for a schema violation: that is a soft check and stays in the run.
- **No raw requests** (`.get(`, `.post(`, ...), no `@playwright/test` imports, no hosts or full URLs (lint).

### API 4. Client layer (`clients/`)

- One class per resource, extending `ResourceClient` with its endpoint path relative to `/api/` (`'part/'`). Methods: `list(params)`, `create(body)`, `retrieve(id)`, `update(id, body)` (PUT), `partialUpdate(id, body)` (PATCH), `destroy(id, body?)`.
- **Return the raw `APIResponse`.** The spec decides what status is expected; a client never throws on a 4xx.
- **Send exactly what you are given:** no defaults added, no fields removed, no retries.
- **Never assert** (lint: no `expect` import in `clients/`).
- A request a case needs that no method covers (a sub-endpoint such as `part/{id}/serial-numbers/`, a form-encoded body, a custom header) gets a new, intention-named method on the right client, with a one-line doc comment. A new resource gets a new client, added to `Clients` in `clients/index.ts`.

### API 5. Fixtures layer (`fixtures/`)

- Specs import `test` and `expect` only from `fixtures/index.ts` (lint; Shared §4).
- **`user` option and `api`:** `test.use({ user: 'engineer' })` gives `api`, the full set of clients authenticated as that user with an InvenTree API token (`Authorization: Token <key>`, from `GET /api/user/me/token/`, cached per worker). A spec without a `user` fails at once.
- **`apiAs(caller)`:** clients for another caller within the same test: a demo user, `'anonymous'` (no credentials) or `{ token: '<value>' }` (e.g. an invalid token). Use it for permission and authentication cases; contexts are disposed after the test.
- **`data`** (shared with the UI suite, Shared §4): prerequisite records created as admin with `QA-<8 hex>` names (`data.name('Resistor')`), deleted after the test in reverse order: `data.category`, `data.part`, `data.company`, `data.location`, `data.supplierPart`, `data.post`, `data.setSetting` (restored afterwards). A record created by the request under test is registered at once with `data.trackPart(pk)`, `data.trackCategory(pk)` or `data.trackSupplierPart(pk)`.
- **`expect`:** Playwright's `expect` plus `toHaveStatus(code)` (failure message shows the body) and `toMatchSchema(component)` (on a response or a parsed value).

### API 6. Utility layer (`utils/`)

- Stateless helpers only. `schemaErrors(component, body)` validates against `components.schemas.<component>` of `requirements/openapi-parts.yaml`, converting OpenAPI `nullable` to JSON Schema. Validation is **strict**: a response that breaks its schema fails, even when the cause is InvenTree itself (findings F-06, F-07).

### API 7. Data and configuration layer

- Configuration, environments, users and secrets: Shared §3. No hosts, ports, full URLs, passwords or tokens anywhere else (lint for URLs). Clients use paths relative to `/api/`.
- Pick the least-privileged user that can make the call, as the case says.

### API 8. Test data and isolation

- Each test creates what it needs and cleans it up; never depend on demo records, other tests or test order.
- Specs run serially (`workers: 1`, Shared §1). InvenTree 1.5.6 rebuilds the whole part or category tree on every delete, and two cleanups at once deadlock in PostgreSQL (HTTP 500). Never re-enable parallel runs.
- Names are unique per test (`QA-<8 hex>`), so runs never collide on data.
- Never delete records the test did not create. Report `QA-` leftovers.
- Settings changed with `data.setSetting` are restored after the test; a case that changes a global setting is tagged `@settings`.

### API 9. Naming

| Item | Pattern | Example |
|---|---|---|
| Spec file | `tests/api/<Area>/<case id lower>.spec.ts` | `tests/api/VAL/api-val-003.spec.ts` |
| Test title | `<case ID>: <case title>` | `API-VAL-003: Part name longer than 100 characters is rejected` |
| Step title | `<n>. <request as in the case>` | `1. POST /api/part/ as engineer` |
| Client | `<Resource>Client` in `<resource>.client.ts` | `CategoriesClient` |
| Client method | intention, camelCase | `serialNumbers(id)` |
| Tags | from the case's Tags | `@smoke`, `@regression`, `@permissions`, `@settings`, `@cross-functional` |

### API 10. InvenTree API patterns observed (1.5.6)

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

### API 11. Agents

- **`api-test-generator`** writes one spec per Approved API case, runs it, and fixes how it runs until it passes three times in a row. It may add client methods or clients (additions only, API §4) and never changes what a spec asserts. A schema violation is never a fixme: the soft check reports it (API §5). When InvenTree's status code or values differ from the case, it marks the test `test.fixme()` with `// FINDING: case <ID> step <n> expects <X>; InvenTree 1.5.6 returns <Y>.` (or `// CASE DEFECT:` when the case looks wrong) and reports it.
- **Client changes by agents are additions only:** new methods or clients. Renaming, removing or changing an existing method is the architect's decision.
- **`api-test-reviewer`** (a stronger model than the generator) reviews a spec independently, without the generator's reasoning: conventions, coverage of every case step and Expected result, SOLID design, Playwright and TypeScript practice. It runs lint and type check, never runs the tests or edits code, and saves `reviews/api/<case id>-review-<date>.md` with a verdict.

### API 12. Quality gates

- `npm run typecheck` and `npm run lint` pass. Lint enforces: no raw requests or `@playwright/test` imports in specs (API §3, API §5), no `expect` in clients (API §4), no hosts or full URLs outside `config/` (Shared §3), no `process.env` outside `config/env.ts` and `playwright.config.ts` (Shared §3).
- `npm run test:api` runs the API suite (`--project=api`, after `api-smoke`); `npm test` runs both suites; `npm run test:smoke` runs `@smoke` only.
- A spec counts as done only when three runs in a row (`npx playwright test <spec> --project=api --repeat-each=3`) all pass, or all fail only on known product defects: a run whose only failures are soft `toMatchSchema` errors all labelled with a recorded finding (`Known product defects only: F-..`). It also needs an `api-test-reviewer` verdict of Approve or Approve with changes. A `[NEW]` schema error is a new finding for the architect, not done.
