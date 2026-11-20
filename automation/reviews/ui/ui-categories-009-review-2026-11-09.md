# Review: UI-Categories-009 A parent category's part list includes the parts of all its sub-categories

| Item | Value |
|---|---|
| Spec | `tests/ui/Categories/ui-categories-009.spec.ts` |
| Case | `test-cases/Categories/category-hierarchy-and-filtering.md` (UI-Categories-009), Review: Approved (2026-11-05) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-11-09 |
| Verdict | Changes required |
| Findings | 1 Blocker, 0 Major, 2 Minor, 4 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass (exit 0, no errors) |
| `npx eslint` on the spec and every framework file it uses (`pages/category.page.ts`, `pages/parts.page.ts`, `pages/base.page.ts`, `pages/login.page.ts`, `pages/components/table.component.ts`, `actions-menu.component.ts`, `form.component.ts`, `notification.component.ts`, `fixtures/index.ts`, `pages.fixture.ts`, `data.fixture.ts`, `auth.fixture.ts`, `user.fixture.ts`, `utils/names.ts`, `utils/api-context.ts`) | Pass (exit 0, no errors or warnings) |
| `npx playwright test <spec> --list` | 1 test listed: `[chromium] › ui-categories-009.spec.ts:7:7 › Category hierarchy and filtering › UI-Categories-009: ...` |

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-steps: log in through the login form, open the *Parts* view | None stated | Outside the steps: `test.use({ user: 'engineer' })` (L4, `auth.fixture.ts` logs in through `LoginPage.loginAs`); `partsPage.openCategories()` (L30, `/web/part/`) | None (page object waits for the categories table) | Covered |
| 1. Open the top category from the *Parts* view (`QA-<suffix> Top`) | The category page opens. | `1. Open the top category from the Parts view` (L32-35) | `expect(categoryPage.partsTab).toBeVisible()` (L34) | **Weakened**: the locator is the same tab the starting Parts view already shows, so the check passes before the click (finding 1) |
| 2. Read the category's part list | The list shows `Part Top`, `Part Mid`, `Part Leaf`, `Part Deep` and `Part Sib` (R-Categories-02) | `2. Read the category's part list` (L37-42) | `expect(categoryPage.partsTable.row(name)).toBeVisible()` for each of the five names (L39-41), scoped to the `Parts` tabpanel | Covered |

Other B checks:
- **Order and titles:** two `test.step`s, in case order, titled `<n>. <case action>` word for word. Pass.
- **Prerequisites, user:** `engineer` (L4) matches the case; no user change in the steps. Pass.
- **Prerequisites, settings:** None stated, none set. Pass.
- **Prerequisites, data:** Top > Mid > Leaf > Deep, plus Sibling and Empty under Top (L18-23); one part each in Top, Mid, Leaf, Deep and Sibling (L24-28, `Part Sib` correctly in `sibling.pk`); all through `data` as admin, names via `data.name`. Pass.
- **Cleanup:** the test creates nothing through the UI; every API record is registered by `data.category`/`data.part` and removed in reverse order (parts first, then categories). The fixture's category order (Empty, Sibling, Deep, Leaf, Mid, Top) differs from the case's (Deep, Leaf, Empty, Sibling, Mid, Top), but parts are deleted first and `trackCategory` moves children up, so the end state is the same. Pass.
- **Form checks:** no form in this case. N/A.
- **Absence checks:** none in the spec. Pass.
- **Traceability:** first-line `// case:` header correct; title `UI-Categories-009: <case title>` exact; `describe('Category hierarchy and filtering')` matches the case file's functionality; tags `@smoke`, `@regression` match Tags *Smoke, Regression*. Pass.
- **Review status:** Approved. Pass.
- **Row specificity:** `TableComponent.row` filters by substring. The five part names are not substrings of one another or of the category names, so each locator matches exactly one row. A second match would be a loud strict-mode failure, not a false pass.

## C. Conventions

No page object or component member is used by this spec alone: `PartsPage.openCategories`, `openCategoryByName`, `categoriesTable` and `CategoryPage.partsTab`, `openPartsTab`, `partsTable` are also used by `ui-categories-012.spec.ts` and `ui-categories-015.spec.ts` (Grep across `tests/ui/`). So there is no new code to review as this spec's own. The shared members it relies on were checked against UI §4 and UI §8.

- UI §1 layers: the spec uses only fixtures and page objects, with no `page`, API calls or DOM. Pass.
- UI §3: one test, file name, title, header, tags and steps correct; assertions are in the spec, not in page objects; no setup logic beyond `data` calls. Pass, except finding 1.
- UI §4: locators use role plus accessible name (`tablist`/`tab`/`tabpanel`/`textbox`/`cell`); `.first()` in `openCategoryByName` has a comment; methods are named as user intentions; `expect` in page objects is used only for waits. Pass, except finding 2.
- UI §5: imports from `fixtures/index.ts`; real login through the `user` fixture; `categoryPage` registered in `pages.fixture.ts`. Pass.
- UI §7: no URLs, IDs or credentials in the spec. Pass.
- UI §8: no sleeps, `networkidle` or `force`. Pass.
- UI §9: names follow the table. Pass.

Problems: findings 1 and 2.

## D. SOLID and design

- Single responsibility: the spec tests one case; `CategoryPage` models one category page and `PartsPage` the Parts view. Pass.
- Open/closed: no flags or special cases added to existing members. Pass.
- Liskov: `CategoryPage` and `PartsPage` extend `BasePage` without overriding `goto`. Pass.
- Interface segregation: the spec requests `partsPage`, `categoryPage` and `data`, and uses all three. Pass.
- Dependency inversion: the spec depends only on page objects and fixtures. Pass.

Problems: findings 3, 6 and 7 (duplication).

## E. Playwright and TypeScript practice

- Every call is awaited; no floating promises. Pass.
- Web-first assertions only; no values read with `textContent()` or `isVisible()`. Pass.
- No conditionals, `try/catch`, `test.only` or `fixme`. The one loop goes over a static list of expected names, not UI state (finding 4, Info). Pass.
- Isolation: the test creates all its own data. Pass, except finding 5 (Info).
- TypeScript: no `any`, casts or `!`; `const` throughout. Pass.

Problems: findings 3, 4 and 5.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Blocker | `tests/ui/Categories/ui-categories-009.spec.ts:34` | UI §3 (each Expected result is asserted in its step); review B (Weakened) | Step 1's Expected result, "The category page opens", is asserted only with `expect(categoryPage.partsTab).toBeVisible()`. `CategoryPage.partsTab` (`pages/category.page.ts:15`) is the same locator as `PartsPage.partsTab` (`pages/parts.page.ts:20`): `panelTab('partcategory', 'Parts')`. The Parts view the step starts on already shows that tab (`PartsPage.open` lands on its Parts panel, `parts.page.ts:28`, and `ui-xf-001.spec.ts:92-93` clicks the same locator on a category page). So the check is already true before the click. It does not show that a category page opened, or that it is Top's. Only the page object's internal `not.toHaveURL(before)` wait stands in for the Expected result. | After the click, assert something only `QA-<suffix> Top`'s page shows. For example, `await expect(categoryPage.breadcrumbs).toHaveText(['Parts', topName])` (an existing `BasePage` member, the pattern of `ui-xf-001.spec.ts:88`; confirm the trail in the live app), or add a `CategoryPage` locator for the category's title and assert `toHaveText(topName)`. |
| 2 | Minor | `pages/parts.page.ts:49-50` | UI §4 (methods wait for their own result) | `openCategoryByName` waits for the URL to change, then for `navigationMenu`. The header was already visible before the click, so the second wait is a no-op, and the method never waits for the category page itself. The spec then clicks a tab that exists on both views (`openPartsTab`). This leaves a small window where the click can land before the category route has rendered. | Wait for something only a category page has, e.g. the `Subcategories` tab (the Parts view labels that panel `Part Categories`, see `parts.page.ts:21` vs `category.page.ts:14`), or return a `CategoryPage` that has waited for itself. This changes how an existing member works, so a healer may do it (UI §11); anything beyond that is the architect's decision. |
| 3 | Minor | `tests/ui/Categories/ui-categories-009.spec.ts:10-16, 24-28` | DRY / readability (review E) | Each part name is built twice: once in `partNames` (L10-16) and again in each `data.part(data.name('Part ...'))` (L24-28). The two only match because `data.name` is deterministic within one test (`utils/names.ts:5`). If one label is edited and not the other, step 2 looks for a part that was never created. | Build each name once, e.g. `const partTop = data.name('Part Top')` and so on. Pass those constants to `data.part(...)` and use the same constants in the step 2 list. |
| 4 | Info | `tests/ui/Categories/ui-categories-009.spec.ts:39-41` | Review E (loops) | A loop over a static list of five expected names. This is acceptable (not a loop over UI state). A hard `expect` stops at the first missing part, so a run reports one missing part at a time. | Optional: write five explicit `expect`s (reads closer to the case's list), or use `expect.soft` so one run reports every missing part. |
| 5 | Info | `pages/parts.page.ts:45-48` | Isolation / robustness | `openCategoryByName` clicks Top's Name cell without searching, so Top must be on the first page of the top-level Part Categories table. Leftover `QA-` categories from aborted runs, or a larger dataset, could push it to a later page. The test would then time out (a loud failure, not a false pass). | Optional: `await this.categoriesTable.search(name)` before the click. |
| 6 | Info | `tests/ui/Categories/ui-categories-009.spec.ts:18-28` | DRY | The same seven-category, five-part hierarchy from the case file's shared Prerequisites is built inline here, in `ui-categories-012.spec.ts:15-25` and in `ui-categories-015.spec.ts:14-22`. Cases 010, 011 and 013 share it too. The copies have already drifted (see Outside scope). | Consider a single builder on `data` (e.g. `data.categoryHierarchy()` returning the names and pks). Fixture changes are the architect's decision. |
| 7 | Info | `pages/category.page.ts:15,17` vs `pages/parts.page.ts:20,22` | Design (DRY, single source of a locator) | `CategoryPage.partsTab`/`partsTable` duplicate `PartsPage.partsTab`/`partsTable` exactly, because InvenTree uses one panel group (`panel-tabs-partcategory`) for the Parts view and for every category page. With two page objects for one panel group, it is easy to pick a locator that cannot tell the two pages apart, which is the root of finding 1. | Architect's decision: e.g. one shared component for the category panel group, with each page object exposing only what differs (`Part Categories` vs `Subcategories`, the category's title). |

## Outside scope

- `tests/ui/Categories/ui-categories-012.spec.ts:25` creates `QA-<suffix> Part Sib` in `top.pk`, but the case's Prerequisites (`category-hierarchy-and-filtering.md:126`) put it in `QA-<suffix> Sibling`. The `Sibling` category (L19) is created but left empty. The spec still passes its own Expected results, but its data does not match the case.
