# Review: UI-Categories-009 A parent category's part list includes the parts of all its sub-categories

| Item | Value |
|---|---|
| Spec | `tests/ui/Categories/ui-categories-009.spec.ts` |
| Case | `test-cases/Categories/category-hierarchy-and-filtering.md` (UI-Categories-009), Review: Approved (2026-11-05, bulk approval by the architect) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-11-09 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 1 Major, 2 Minor, 2 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass, no errors |
| `npx eslint` on the spec, `pages/category.page.ts`, `pages/parts.page.ts`, `pages/base.page.ts`, `pages/components/table.component.ts`, `fixtures/pages.fixture.ts`, `fixtures/data.fixture.ts`, `fixtures/auth.fixture.ts`, `fixtures/user.fixture.ts`, `fixtures/index.ts` | Pass, no errors or warnings |
| `npx playwright test tests/ui/Categories/ui-categories-009.spec.ts --list` | 1 test: `[chromium] › tests\ui\Categories\ui-categories-009.spec.ts:7:7 › Category hierarchy and filtering › UI-Categories-009: A parent category's part list includes the parts of all its sub-categories` |

The tests were not run (reviewer guardrail).

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Prerequisites: user `engineer`; categories Top > Mid > Leaf > Deep, Sibling and Empty under Top; one part each in Top, Mid, Leaf, Deep, Sibling; via the API as `admin` | n/a | Outside the steps: L4, L9-28 | n/a | Covered |
| Pre-steps: log in through the login form, open the *Parts* view | None stated | Outside the steps: L4 (`auth.fixture.ts:17`, `LoginPage.loginAs`), L30 `partsPage.openCategories()` | None (the page object waits for the categories table, `parts.page.ts:41`) | Covered |
| 1. Open the top category from the *Parts* view (`QA-<suffix> Top`) | The category page opens. | `1. Open the top category from the Parts view` (L32-35) | L34 `expect(categoryPage.partsTab).toBeVisible()` | **Weakened, caught later** (finding 1): L34 is already true before the click. Lines that fail if Top's page does not open: `parts.page.ts:49` (no navigation), `category.page.ts:22-23` (not a category page), spec L40 for `Part Top` (any other category page; `Part Top` is only in Top, which has no parent). |
| 2. Read the category's part list | The list shows `Part Top`, `Part Mid`, `Part Leaf`, `Part Deep` and `Part Sib` (R-Categories-02) | `2. Read the category's part list` (L37-42) | L39-41: `expect(categoryPage.partsTable.row(name)).toBeVisible()` for each of the five names, scoped to the `Parts` tabpanel | Covered |

Other B checks:
- **Order and titles:** two steps in case order, titled `1. Open the top category from the Parts view` and `2. Read the category's part list` (the case wording without italics or the full stop). Pass.
- **Prerequisites:** user `engineer` matches (L4). No settings stated and none set. All six categories are created with the stated parents and all five parts in the stated categories, through `data` (L18-28) with `data.name` names (`QA-<8 hex> <label>`, `utils/names.ts:5`). Pre-steps covered. Pass.
- **Cleanup:** the UI creates no records. Every `data.category`/`data.part` record is registered by the fixture (`data.fixture.ts:34`, `:40`) and removed in reverse order: parts first, then Empty, Sibling, Deep, Leaf, Mid, Top. This matches the case's cleanup (children before parents). Pass.
- **Form checks:** the case has no form. N/A.
- **Absence checks:** the spec has none and the case states none. The case lists five parts but does not say "only", so no count assertion is needed. Pass.
- **Traceability:** the L1 header matches the case file and ID. The title is `UI-Categories-009: <case title>` exactly (L7). The describe is `Category hierarchy and filtering` (the case file's title). Tags `@smoke`, `@regression` match the case's Tags `Smoke, Regression`. Pass.
- **Review status:** Approved, 2026-11-05. Pass.

## C. Conventions

New code: no page object or component member is used by this spec alone. `PartsPage.categoriesTable`, `openCategories`, `openCategoryByName` and `CategoryPage.partsTab`, `openPartsTab`, `partsTable` are also used by `ui-categories-012.spec.ts` and `ui-categories-015.spec.ts` (Grep across `tests/ui/`). The members this spec calls are uncommitted additions: `category.page.ts` is untracked, and the new `PartsPage` members and the `categoryPage` fixture appear in the working-tree diff. They are additions only; no existing member was renamed or changed. They are checked below.

- UI §1 / UI §3 layer boundaries: the spec uses only fixtures and page objects. No `page.locator`/`getBy*`, no direct API calls (setup goes through `data`), no URLs, IDs or credentials (`top.pk` and the others come from `data`). Pass.
- UI §3 structure: import from `fixtures`, `test.use`, describe/test/step layout, and each Expected result asserted in its own step. Pass, except finding 1.
- UI §4: `CategoryPage` extends `BasePage`. Locators are readonly and built in the constructor, using role plus accessible name (`tablist`/`tab`/`tabpanel`/`textbox`/`cell`). The `.first()` at `parts.page.ts:48` has a comment. Methods are named as user intentions. `expect` is used in page objects only to wait. No test data or users. Pass, except finding 3.
- UI §5: fixtures come through `fixtures/index.ts`; `categoryPage` is registered at `pages.fixture.ts:13`, `:24`; login goes through the real form via the `user` option. Pass.
- UI §6 / UI §7: names come from `data.name`; the spec reads no config. Pass.
- UI §8: no `waitForTimeout`, `networkidle` or `force`; actions auto-wait. Pass.
- UI §9: file name, describe, title, tags, step titles, and locator and method names all follow the table. Pass.

Problems: findings 1 and 3.

## D. SOLID and design

- Single responsibility: `CategoryPage` models one category page, `PartsPage` the Parts view and `TableComponent` the table widget. The spec tests one case. Pass.
- Open/closed: new behaviour comes in as new members (`openCategories`, `openCategoryByName`, `CategoryPage`), with no flags added to existing ones. Pass.
- Liskov substitution: neither page overrides `goto`. `openCategories` uses `BasePage.goto`, which keeps the app-shell wait. Pass.
- Interface segregation: the spec requests `partsPage`, `categoryPage` and `data`, and uses all three. Pass.
- Dependency inversion: the spec depends only on page objects and `data`. Pass.

Problems: duplication, findings 2 and 5.

## E. Playwright and TypeScript practice

- Every call is awaited, including inside the `for...of` loop (L39-41). No floating promises. Pass.
- Only web-first assertions. No reads of `textContent()`/`isVisible()`, no sleeps or polling. Pass.
- No conditionals, `try/catch`, `test.only` or `test.fixme`. The loop at L39-41 runs over the case's fixed part names, not over UI state, and a failure names the row in the locator description. Pass.
- Isolation: the test creates all its data with unique `QA-` names and does not rely on demo records or other tests. Pass (finding 4 covers the first-page assumption).
- Locators: `row(name)` matches with substring `hasText`, but the five names are unique and none is a substring of another or of a category name shown in the rows, so there is no strict-mode risk. Pass.
- TypeScript: no `any`, casts or non-null assertions; `const` throughout; `ApiRecord.pk` is typed `number`. Pass.
- Readability: reads like the case. Problem: finding 2.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Major | `tests/ui/Categories/ui-categories-009.spec.ts:34` | Section B (Weakened, caught later); UI §3 (each Expected result is an `expect` in its step, checked after its action) | `await expect(categoryPage.partsTab).toBeVisible()` checks `panelTab('partcategory', 'Parts')` (`category.page.ts:15`). That is the same locator as `PartsPage.partsTab` (`parts.page.ts:20`), and the tab is already shown on the Parts view the step starts from. So the check passes before `openCategoryByName` clicks anything and says nothing about which page opened. In practice, "The category page opens" (for `QA-<suffix> Top`) is only proven by the URL change at `parts.page.ts:49` and by step 2 (`category.page.ts:22-23`, spec L40 for `Part Top`). A failure would be reported at step 2, not step 1. A landing on the top-level Parts index, which lists all parts, would not be guaranteed to fail at all. | After the click, assert something that identifies Top's page. For example, `await expect(categoryPage.breadcrumbs).toContainText([topName])` (`BasePage.breadcrumbs`, `base.page.ts:48-50`), or add a `CategoryPage` locator for the category name in the page header and assert `toHaveText(topName)`. Confirm the element in the live app first. |
| 2 | Minor | `tests/ui/Categories/ui-categories-009.spec.ts:10-16, 24-28` | DRY / readability (Section E) | The five part labels are written twice: in `partNames` (L10-16) and again in the `data.part(data.name('Part ...'))` calls (L24-28). The two lists only agree because `data.name` is deterministic. If one list is edited and the other is not, step 2 looks for parts that were never created. | Name each part once (`const partTop = data.name('Part Top')`, ...) and use those constants in both the `data.part` calls and the list asserted in step 2. |
| 3 | Minor | `pages/parts.page.ts:50` | UI §4 (methods wait for their own result) | After the click, `openCategoryByName` waits for `navigationMenu`. The header is already visible on the Parts view and stays during the in-app route change, so this wait adds nothing. The method really only waits for the URL to change, even though its doc comment (L44) says it "waits for its page". | Wait for an element that only the opened category page has, such as the category name in the breadcrumbs or header, or the `Subcategories` tab. Then the wait proves the category page rendered. The healer may change how an existing method waits (UI §11); re-run 012 and 015 after the change. |
| 4 | Info | `pages/parts.page.ts:45-48` | Test isolation / robustness | `openCategoryByName` clicks the Name cell without searching first, so `QA-<suffix> Top` has to be on the first page of the top-level Part Categories table. Leftover `QA-` top-level categories from aborted runs, or a larger dataset, could push it off that page. The test would then time out: a loud failure, not a false pass. | Optional: call `await this.categoriesTable.search(name)` before the click. |
| 5 | Info | `pages/parts.page.ts:20, 22`; `pages/category.page.ts:15, 17` | DRY (Section D) | `PartsPage.partsTab`/`partsTable` and `CategoryPage.partsTab`/`partsTable` are identical locators, because InvenTree draws the Parts view and a category page with the same `partcategory` panel group. This is why the step-1 check in finding 1 cannot tell the two pages apart. | No change needed for this spec. If more category specs are added, the architect may want one shared component for the `partcategory` panels (Parts tab and table), used by both pages. |

## Outside scope

- `pages/category.page.ts:31-32` (`openSubcategory`, used by 012 and 015, not by this spec): after the click it waits for a URL change and for `subcategoriesTable.searchInput`. That search box is already visible on the parent category page, so, as in finding 3, the wait does not prove the sub-category page rendered.
- `CONVENTIONS.md` UI §5 lists the injected page objects as `app`, `loginPage`, `partsPage`, `partForm`, `partDetail`, but `fixtures/pages.fixture.ts` also injects `categoryPage`, `parameterForm` and `stockItemForm`. The documentation is out of date.
- `fixtures/pages.fixture.ts:9`: a stray blank line separates the `CategoryPage` import from the other imports (cosmetic).
