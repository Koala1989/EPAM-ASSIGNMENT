# Review: UI-Part-001 Create a part with only the required fields

| Item | Value |
|---|---|
| Spec | `tests/ui/Part/ui-part-001.spec.ts` |
| Case | `test-cases/Part_Creation_and_Import/part-creation-flow.md` (UI-Part-001), Review: Approved (2026-10-11) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-10-15 |
| Verdict | Changes required |
| Findings | 1 Blocker, 0 Major, 3 Minor, 3 Info |

## A. Automated checks

- `npm run typecheck`: pass, no errors.
- `npx eslint` on the spec, `pages/part-form.page.ts`, `pages/part-detail.page.ts`, `pages/parts.page.ts`, `pages/base.page.ts`, `pages/components/form.component.ts`, `select.component.ts`, `actions-menu.component.ts`, `fixtures/data.fixture.ts`, `fixtures/index.ts`, `fixtures/pages.fixture.ts`, `fixtures/auth.fixture.ts`: pass, no errors or warnings.
- `npx playwright test tests/ui/Part/ui-part-001.spec.ts --list`: listed as `[chromium] Part creation flow › UI-Part-001: Create a part with only the required fields` (plus the six `login-smoke` setup tests).

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| 1 Open Add Parts, select Create Part | The part creation form opens | `1. Open the Add Parts dropdown above the parts table and select Create Part` | `partForm.root` `toBeVisible()` (l.16) | Covered |
| 2 Fill required field and category, leave IPN empty | Fields accept the values, no form errors are shown | `2. Fill in the required field and the category only; leave IPN empty` | Name `toHaveValue(partName)` (l.21), Category `toHaveValue(categoryName)` (l.22), IPN `toHaveValue('')` (l.23), `invalidFields` `toHaveCount(0)` (l.24), `formError` `toBeHidden()` (l.25) | Covered |
| 3 Press Submit | The form closes and the browser is redirected to the new part's detail page | `3. Press Submit` | `partForm.root` `toBeHidden()` (l.30); URL wait inside `currentPartId()` (l.31, value discarded); `partDetail.title` `toBeVisible()` (l.32) | Covered across steps 3-4 (form closes, detail page shown; step 4 l.36 proves it is the new part). Within step 3 the "new part" is not asserted (finding 2). |
| 4 Check the part details | Name and category show the values from step 2. IPN is empty. | `4. Check the part details` | Name `toHaveText` (l.36); Category `toContainText` (l.37); IPN row `toHaveCount(0)` (l.39) | Name, IPN Covered. Category **Weakened** (finding 1). |

- **Order and titles:** four `test.step`s in case order, titled `<n>. <case action>`. Pass.
- **Prerequisites:** `test.use({ user: 'engineer' })` matches the case. Settings: none, none set. Data: category via `data.category(data.name('Category'))` (as admin). Part name via `data.name('Resistor 10k')`. Pre-steps: login by fixture, *Parts* view opened by `partsPage.open()` at the start of step 1 (Info 5). Pass.
- **Cleanup:** UI-created part registered with `data.trackPart` (l.11) before it is created; category removed by `data`; reverse order (part, then category) matches the case. Pass.
- **Traceability:** `// case:` header line 1, title `UI-Part-001: Create a part with only the required fields`, describe `Part creation flow` (case file title), tags `@smoke`, `@regression` match "Smoke, Regression". Pass.
- **Review status:** Approved. Pass.

## C. Conventions

Passed: UI §3 one test per case, import from `fixtures`, no raw locators, no setup logic, assertions in the spec; UI §5 only used fixtures requested; UI §7 no hard-coded URLs, IDs, names or credentials in the spec; UI §8 no sleeps, `networkidle` or `force`; UI §9 file, title, step and data names.
New page object member used only by this spec: `PartFormPage.categoryField` (`pages/part-form.page.ts:63-66`). Placement (part form), locator (`getByLabel('tree-field-category')` via `FormComponent.field`, UI §10 pattern), noun naming, no assertion, no change to existing members: pass. Small duplication with `fill()` (Info 6). Problems: findings 1-4.

## D. SOLID and design

Passed: single responsibility (one spec, one case); open/closed (the new member is an addition, no flags); dependency inversion (spec depends on page objects and `data`, not on DOM or endpoints); interface segregation (only `partsPage`, `partForm`, `partDetail`, `data`). `PartDetailPage` and `PartsPage` keep the `BasePage.goto` contract. `PartFormPage` not extending `BasePage`: see Outside scope.

## E. Playwright and TypeScript practice

Passed: every call awaited; web-first assertions only; no conditionals, loops, `try/catch`, `test.only` or `fixme`; isolated (own category, unique names, no demo records); no `any` or `!` in the spec; `const` throughout. Problems: findings 3, 4.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Blocker | tests/ui/Part/ui-part-001.spec.ts:37 | Checklist B (Weakened: `toContainText` where the case states the value); UI §3 | Case step 4: "Name and category show the values from step 2." Name is asserted exactly (`toHaveText`, l.36), Category only with `toContainText(categoryName)`, which also passes for `Parent/QA-… Category` or a cell with extra text. No comment explains why exact text cannot be used. Low practical risk (unique, top-level name), but the Expected result is asserted less specifically than stated. | `await expect(partDetail.detail('Category')).toHaveText(categoryName);`. If the cell genuinely holds more than the name (icon text, path), add a `PartDetailPage` accessor for the category link and assert `toHaveText` on it, or keep `toContainText` with a comment stating what else the cell contains, confirmed in the app. |
| 2 | Minor | tests/ui/Part/ui-part-001.spec.ts:31-32 | UI §3 (each Expected result is an `expect` in its step) | Step 3 expects a redirect to the **new** part's detail page. The spec checks only that some part page is shown: `currentPartId()` is called for its URL wait and its value thrown away, and `title` `toBeVisible()` matches any part. The new part is first identified in step 4. | `await expect(partDetail.title).toContainText(partName);` in step 3 (or compare `await partDetail.currentPartId()` with the pk from `data.findParts(partName)`). |
| 3 | Minor | tests/ui/Part/ui-part-001.spec.ts:31 | Checklist E (readability) | `await partDetail.currentPartId();` reads as an action whose result is unused; its only purpose is the hidden URL wait. | Use the returned ID (see finding 2) or rely on a web-first assertion on the title. |
| 4 | Minor | tests/ui/Part/ui-part-001.spec.ts:9-10 | Checklist E (no unchecked casts; readability) | `String(category.name)` converts an optional field (`name?: string`); an undefined name would silently become `"undefined"`. The name is already known before the call. | `const categoryName = data.name('Category'); await data.category(categoryName);` |
| 5 | Info | tests/ui/Part/ui-part-001.spec.ts:14 | Checklist B (pre-steps) | The case pre-step "open the *Parts* view" runs inside step 1 (`partsPage.open()`). Acceptable, as the step needs the view; noted for traceability. | None. |
| 6 | Info | pages/part-form.page.ts:64-66, 82 | DRY | New `categoryField` returns `form.field('tree', 'category')`; `fill()` builds the same locator again through `form.select('tree', 'category')`. Harmless. Its doc comment ("input value is the selected category's name") is a UI behaviour claim not listed in UI §10; it is exercised by l.22, so the runs confirm it. | Optionally add a `category` getter returning `SelectComponent` and use it in both places. |
| 7 | Info | tests/ui/Part/ui-part-001.spec.ts:38-39 | Checklist B | "IPN is empty" asserted as the IPN row being absent (comment l.38). The negative check runs after the Name row has rendered (l.36), and the same `detail('IPN')` locator resolves positively in UI-Part-004 l.39, so it cannot pass only because the locator is wrong. | None. |

## Outside scope

- `pages/part-form.page.ts:44`: `PartFormPage` does not extend `BasePage` (UI §4 "Every page object extends it"); it behaves like a component wrapping `FormComponent`. Architect's decision: extend `BasePage` or move it to `components/`.
- `pages/parts.page.ts:35-37`: `addParts()` does not wait for the form to open (UI §4 "Methods wait for their own result"); `PartFormPage.waitUntilOpen()` exists but is unused. Same for `FormComponent.submit()` (no wait for the dialog to close).
- `pages/components/form.component.ts:25`: `invalidFields` uses CSS `[aria-invalid="true"]` without the comment UI §4 requires.
- `pages/part-detail.page.ts:39`: non-null assertion `!` in `currentPartId()`; safe after `toHaveURL`, but an explicit throw would be clearer.
