# UI automation conventions

**Status: approved 2026-10-12.** Conventions for the Playwright UI suite in `automation/ui/`, which automates the Approved manual cases in `test-cases/<Area>/` against InvenTree 1.5.6. They apply to people, to the `playwright-test-generator` and `playwright-test-healer` agents, and to Copilot.

## 1. Layers

The suite has five layers. Each layer may only use the layers below it.

```
Tests            tests/<Area>/*.spec.ts           what is tested: workflow + assertions
  ↓ uses
Fixtures         fixtures/                         setup, teardown, users, injected page objects, test data
  ↓ uses
Page objects     pages/                            locators + actions per page and per InvenTree widget
  ↓ uses
Utilities        utils/                            stateless helpers
Data & config    data/, config/, playwright.config.ts   environment values, users, input matrices
```

| Layer | May import | Must not |
|---|---|---|
| Tests | fixtures, data | use `page.locator`/`getBy*` directly, call the API directly, hard-code URLs, IDs or credentials |
| Fixtures | pages, utils, data, config | contain assertions about the feature under test |
| Page objects | utils, config, other page objects and components | contain `expect` about business outcomes, create test data, know which user is logged in |
| Utilities | config | hold state, import Playwright test fixtures |
| Data & config | nothing | contain code beyond reading environment variables |

## 2. Folder layout

```
automation/ui/
├── playwright.config.ts        runner settings: projects, reporters, retries, workers; reads config/env.ts
├── CONVENTIONS.md
├── tsconfig.json, eslint.config.mjs   quality gates (§12)
├── .env.example                every environment variable, with its default
├── config/
│   └── env.ts                  baseURL, apiURL, timeouts, credentials from process.env with defaults
├── data/
│   ├── users.json              demo users: username, role, what they may do (no passwords)
│   └── <Area>/<name>.json      input matrices for data-driven tests
├── utils/
│   ├── names.ts                QA-<8 hex> suffix and test record names
│   └── api-client.ts           creates an authenticated APIRequestContext
├── fixtures/
│   ├── index.ts                the merged `test` and `expect` every spec imports
│   ├── auth.fixture.ts         `user` option (real UI login before the test), `switchUser`
│   ├── data.fixture.ts         `data`: API test data with cleanup, setting changes with restore
│   └── pages.fixture.ts        page objects injected into tests
├── pages/
│   ├── base.page.ts            BasePage: navigation, notifications, shared components
│   ├── components/             InvenTree widgets reused across pages
│   │   ├── form.component.ts           modal forms: fields, Submit, Cancel, field errors
│   │   ├── select.component.ts         dropdown fields: searchable (related/tree) and read-only
│   │   ├── table.component.ts          table search, rows, row actions
│   │   ├── actions-menu.component.ts   the three-dot actions menu
│   │   └── notification.component.ts   pop-up notifications
│   ├── login.page.ts           login screen: real login through the form
│   ├── parts.page.ts           Parts view: Categories and Parts panels, Add Parts menu
│   ├── part-detail.page.ts     part detail: header, tabs, revision selector
│   └── part-form.page.ts       Create Part and Duplicate Part forms
├── reviews/                    review reports from playwright-test-reviewer, one per spec per review
└── tests/
    ├── setup/login.setup.ts    login smoke check: every demo user logs in and out (saves nothing)
    ├── seeds/<user>.seed.spec.ts   starting point for the generator agent
    └── <Area>/<case id>.spec.ts    one test per Approved manual case
```

## 3. Test layer (`tests/`)

Tests read like the manual case: the workflow and the checks, nothing else.

- **One test per Approved manual case.** File `tests/<Area>/<case id in lower case>.spec.ts`; title `<case ID>: <case title>`; a `test.describe` per functionality (the case file's title).
- **Traceability.** First line: `// case: test-cases/<Area>/<file>.md (<case ID>)`. Tags from the case's Tags field: `{ tag: ['@smoke', '@regression'] }`.
- **One `test.step` per case step**, titled `<n>. <case action>`, so the HTML report and trace show the case's steps.
- **Assertions live in tests.** Each Expected result of the case is at least one `expect` in its step. Use web-first assertions (`toBeVisible`, `toHaveText`, `toHaveURL`, `toHaveValue`). Page objects return locators or values; the test asserts on them.
- **No raw DOM access.** No `page.locator`, `page.getBy*`, CSS or XPath in a test. If a page object lacks what the step needs, add it to the page object.
- **No setup logic.** Prerequisite records, users and settings come from fixtures.
- **Data-driven tests** loop over a matrix from `data/` and create one `test` per row, with the row's label in the title.

```ts
// case: test-cases/Part/part-creation-flow.md (UI-Part-001)
import { test, expect } from '../../fixtures';

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

## 4. Page object layer (`pages/`)

Page objects hold every locator and every UI action. Tests and fixtures never touch the DOM.

- **One class per page or form**, named `<Name>Page` in `<name>.page.ts`. Reusable InvenTree widgets are **components** (`<Name>Component` in `components/<name>.component.ts`), composed into pages, not inherited.
- **`BasePage`** holds what every screen has: the navigation menu, global search, notifications, and helpers to get the shared components. Every page object extends it.
- **Constructor** takes the Playwright `Page` (and a root locator for components). Locators are `readonly` properties defined in the constructor; actions are `async` methods.
- **Locator priority:** `getByRole` with the accessible name → `getByLabel` → `getByPlaceholder` → `getByText` → `getByTestId`. InvenTree exposes many `aria-label`s (e.g. `navigation-menu`, `login-username`); reach them through `getByRole(role, { name })`. CSS or XPath only when nothing else identifies the element, with a comment saying why. No `nth()` without a comment.
- **Methods are user intentions**, named as verbs in the UI's language: `addParts('Create Part')`, `openTab('Suppliers')`, `selectRevision('B')`. Not `clickButton3()`.
- **Methods wait for their own result** (the form opened, the page navigated) with web-first checks, so tests never need sleeps. They do not assert business outcomes; that is the test's job.
- **Methods return** `void`, a locator, a value read from the UI, or the next page object when the action navigates.
- **No test data, no users, no API calls** in page objects.

## 5. Fixtures layer (`fixtures/`)

Fixtures prepare what a test needs and clean it up afterwards.

- **Import path.** Every spec imports `test` and `expect` from `fixtures/index.ts`, which merges the fixture files with `mergeTests`. Never import `test` from `@playwright/test` in a spec.
- **Real login, like a user.** `test.use({ user: 'engineer' })` makes the fixture log in through the login form (`LoginPage.loginAs`) before the test body; no saved sessions or cookies are used. Without it the test's `page` starts logged out. A case that changes user ("log out, log in as allaccess") calls `switchUser('allaccess')`: it logs out through the user menu and logs in as the other user in the same page, so the test continues with the same page objects.
- **Login smoke check.** The `login-smoke` project (`tests/setup/login.setup.ts`) runs first and checks that every demo user can log in and out; the other tests depend on it, so a broken login stops the run early instead of failing every test.
- **`data`** creates prerequisite records through the API as `admin` with unique `QA-<8 hex>` names, and removes them after the test in reverse order, including stock, supplier and manufacturer parts. Records the test creates through the UI are registered with `data.trackPart(name)` (returns the name) so they are removed too. `data.setSetting(key, value)` changes a global setting and restores it after the test.
- **Page objects** are injected per test: `app` (a `BasePage`), `loginPage`, `partsPage`, `partForm`, `partDetail`, built on the test's `page`.
- **Finding records the UI created:** `data.findParts(name)` returns the parts with that exact name (e.g. to get the ID of a part made through the form).
- **Worker-scoped** fixtures only for expensive, read-only things (the admin API context). Everything else is test-scoped, so tests stay independent.
- **Cleanup must not hide failures**: a cleanup error fails the test with the list of records that could not be removed.

## 6. Utility layer (`utils/`)

Stateless helpers with no Playwright test fixtures: pure functions and small factories.

- `names.ts`: `qaSuffix()`, `qaName(suffix, label)`, `slug(label)` (menu item labels to InvenTree's aria-label form).
- `api-client.ts`: `createApiContext(baseURL, credentials)` returns an `APIRequestContext` authenticated with an InvenTree token.
- Add a helper only when two or more callers need it. No business assertions here.

## 7. Data and configuration layer (`data/`, `config/`, `playwright.config.ts`)

- **`playwright.config.ts`** holds runner settings only: test directory, projects (`setup`, `chromium`), reporters, retries, workers, trace and screenshot policy. It reads environment values from `config/env.ts`.
- **`config/env.ts`** is the single place that reads `process.env`. It exports typed values with defaults for the local Docker instance: `INVENTREE_URL` (default `http://localhost`), timeouts, and user credentials. Tests, fixtures and page objects import from it; nothing else reads `process.env`.
- **Secrets** come only from environment variables (or an untracked `.env`). The demo users' passwords are the documented defaults for the local demo dataset; any other environment sets them through `INVENTREE_<USER>_PASSWORD`. `.env.example` lists every variable. `LoginPage` reads passwords through `passwordFor()`; specs never contain them.
- **`data/users.json`** lists each demo user's display name (the accessible name of the header user menu, used to log out), role and purpose. No passwords.
- **`data/`** holds test inputs as JSON (or CSV) matrices, e.g. boundary values for a field, one row per case variant with a `label` used in the test title. Files are named by Area and purpose: `data/Part/name-boundaries.json`.

## 8. Waiting, timing and stability

- No `page.waitForTimeout`, no `waitForLoadState('networkidle')`, no `force: true` (all lint errors). If an overlay covers an element, the page object waits for the overlay to go away.
- Rely on auto-waiting actions and web-first assertions. A page object method that triggers navigation or a form waits for the resulting state.
- One worker (`workers: 1`): some tests change global InvenTree settings, which every parallel test would see.
- A test that fails because InvenTree differs from the case is marked `test.fixme()` with `// FINDING: ...` above the failing step, never "fixed" by changing the assertion.

## 9. Naming

| Item | Convention | Example |
|---|---|---|
| Spec file | `<case id lower>.spec.ts` in `tests/<Area>/` | `tests/Part/ui-part-001.spec.ts` |
| Page object | `<name>.page.ts`, class `<Name>Page` | `part-detail.page.ts`, `PartDetailPage` |
| Component | `components/<name>.component.ts`, class `<Name>Component` | `FormComponent` |
| Fixture file | `<name>.fixture.ts` | `data.fixture.ts` |
| Locator property | noun, camelCase, what the user sees | `addPartsButton`, `revisionSelect` |
| Action method | verb phrase in the UI's words | `addParts('Create Part')` |
| Test data names | `data.name('<label>')` → `QA-<8 hex> <label>` | `QA-1A2B3C4D Resistor 10k` |
| Tags | `@smoke`, `@regression`, `@permissions`, `@cross-functional`, `@settings` | |

## 10. InvenTree UI patterns observed (1.5.6)

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

## 11. Agents

- **`playwright-test-generator`** writes specs and, when a step needs a locator, action, component or page the framework lacks, adds it to `pages/` (registering new pages in `fixtures/pages.fixture.ts`). It never queries the DOM in a spec.
- **`playwright-test-healer`** may fix page objects, components and fixtures (a broken locator is fixed once, in the page object, not in every spec), add missing page object members, and change the *how* of a spec. It never changes what a spec asserts.
- **Page object changes by agents are additions only**: new locators, methods, components or pages, each confirmed in the live app and following §4. Renaming, removing or changing the behaviour of an existing member is the architect's decision (the healer may change *how* a method works, not what it does). Agents list every page object change in their report; `playwright-test-reviewer` reviews them with the spec.
- **`playwright-test-reviewer`** (a stronger model than the generator and healer) reviews a spec independently, without the writers' reasoning: conventions, coverage of every case step and Expected result, SOLID design, Playwright and TypeScript practice. It runs lint and type check, never edits code, and saves `reviews/<case id>-review-<date>.md` with a verdict. A spec counts as done only with an Approve or Approve-with-changes review and three green runs.
- After an agent changes page objects, the main session runs `npm run lint`, `npm run typecheck` and the full suite, so an addition cannot break other specs unnoticed.

## 12. Quality gates

- `npm run typecheck` (TypeScript, no emit) and `npm run lint` (ESLint with `eslint-plugin-playwright`) must pass before a spec is committed. The lint configuration enforces these conventions: raw locators or `@playwright/test` imports in a spec (§3, §5), `process.env` outside `config/env.ts` and `playwright.config.ts` (§7), and `waitForTimeout`, `networkidle` or `force` (§8) are errors.
- `npm test` runs the suite; `npm run test:smoke` runs `@smoke` only.
- A new or changed spec passes three runs in a row and has a `playwright-test-reviewer` verdict of Approve or Approve with changes before it counts as done.
