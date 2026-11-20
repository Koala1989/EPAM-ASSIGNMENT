# Review: UI-Categories-009 A parent category's part list includes the parts of all its sub-categories

| Item | Value |
|---|---|
| Spec | `tests/ui/Categories/ui-categories-009.spec.ts` |
| Case | `test-cases/Categories/category-hierarchy-and-filtering.md` (UI-Categories-009), Review: Approved (2026-11-05, bulk approval) |
| Reviewer | playwright-test-reviewer (Sonnet 5.5), 2026-11-11 |
| Verdict | Changes required |
| Findings | 1 Blocker, 0 Major, 3 Minor, 1 Info |

## A. Automated checks

- `npm run typecheck`: pass.
- `npx eslint` on the spec, `pages/category.page.ts`, `pages/parts.page.ts`, `fixtures/data.fixture.ts`, `fixtures/pages.fixture.ts`: **1 error**, `ui-categories-009.spec.ts:40:59 playwright/valid-expect` ("Matchers must be called to assert").

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| 1. Open the top category from the Parts view | The category page opens. | `1. Open the top category from the Parts view` (l.32) | `openCategoryByName` waits for the URL to change and the nav menu (parts.page.ts:45-51); `expect(categoryPage.partsTab).toBeVisible()` (l.34) | Covered (see finding 3) |
| 2. Read the category's part list | The list shows Part Top, Part Mid, Part Leaf, Part Deep and Part Sib | `2. Read the category's part list` (l.37) | l.40 `expect(...row(name)).toBeVisible;` is never called, so nothing is asserted. `openPartsTab` (category.page.ts:21-24) only waits for the table search box. | **Missing** |

If this Expected result were false (a part absent from the list), no line fails: the search-box wait passes, the property reference on l.40 is a no-op, and the test ends green. No later assertion can catch it.

Other B checks:
- Order and titles: two steps, in order, titled `<n>. <case action>`. Pass.
- Prerequisites: `test.use({ user: 'engineer' })` matches; no settings required; all categories (Top, Mid, Leaf, Deep, Sibling, Empty) and five parts created via `data.category` / `data.part` with `data.name` and the right parents. Pass.
- Cleanup: the test creates no records through the UI. Pass.
- Form checks: no form. Absence checks: none.
- Traceability: `// case:` header, title `UI-Categories-009: <case title>`, describe "Category hierarchy and filtering", tags `@smoke`, `@regression` match Smoke, Regression. Pass.
- Review status: Approved. Pass.

## C. Conventions

Passed: no raw locators in the spec, imports from `../../../fixtures`, no hard-coded URLs or credentials, setup through `data`, page object methods named as intentions, `CategoryPage` extends `BasePage`, locator priority (role, then label) in new members, locator `.first()` uses carry a comment, no assertions about business outcomes in page objects. Problems: see findings 1 and 3.

New or spec-only members (only this spec and 012/015 use them): `CategoryPage` (`pages/category.page.ts`) and `PartsPage.openCategories` / `openCategoryByName`. Placement is right, waits are web-first, no existing member renamed (not verifiable beyond what was read; git shows `parts.page.ts` modified).

## D. SOLID and design

Passed: single responsibility (one page object per page), specs depend on page objects and fixtures rather than the DOM. See finding 4 for a small DRY note.

## E. Playwright and TypeScript practice

Passed: every call awaited, no `any`, no `!`, no sleeps, no `test.only`, no `try/catch`, no `nth()`, test creates its own data. Problems: findings 1 and 2.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Blocker | `tests/ui/Categories/ui-categories-009.spec.ts:40` | UI §3 (each Expected result asserted); UI §12 (lint must pass); case step 2 | `toBeVisible` is referenced, not called. No assertion runs, so the case's only substantive Expected result (all five parts listed) is Missing, and lint fails with `playwright/valid-expect`. The test can pass while the behaviour is wrong. | Call the matcher: `await expect(categoryPage.partsTable.row(name)).toBeVisible();`. Re-run lint and typecheck. |
| 2 | Minor | `ui-categories-009.spec.ts:39-41` | UI §3 readability; spec should read like the case | A loop over `partNames` inside the step, and the five names are built twice (l.10-16 and l.24-28 via separate `data.name` calls). | Define each name once (`const partTop = data.name('Part Top')` ...), pass it to `data.part` and assert each part with its own `expect` line, or build the parts from one list. |
| 3 | Minor | `ui-categories-009.spec.ts:34` | UI §3 (assert what the case asks) | Step 1 asserts `partsTab` visible. The same tab exists on the Parts index page, so it does not show the Top category opened. The URL-change wait in `openCategoryByName` carries most of the check. | Optionally assert a locator that names the open category (for example the category header/breadcrumb in `CategoryPage`), if the page exposes one. |
| 4 | Minor | `pages/category.page.ts:15` and `pages/parts.page.ts:20` | DRY | `partsTab` (`panelTab('partcategory', 'Parts')`) and the `partsTable` are defined in both `CategoryPage` and `PartsPage`. | Consider sharing through a component or one page; no change needed to pass. |
| 5 | Info | `pages/category.page.ts:21-24` | Not checked by running | Whether the Parts panel of Top shows sub-category parts by default (R-Categories-02) is not verified, because tests are not run in review. After fixing finding 1, the green run is the evidence; if a part is missing it is a `FINDING` for `test.fixme`, not a weakened assertion. | Run the spec after the fix. |

## Outside scope

- `CategoryPage.openSubcategory` is not used by this spec (used by Categories-008 type cases); no problem noted.
