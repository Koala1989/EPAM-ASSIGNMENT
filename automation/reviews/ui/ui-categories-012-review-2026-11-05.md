# Review: UI-Categories-012 A part in the deepest category appears in the top category's list

| Item | Value |
|---|---|
| Spec | `tests/ui/Categories/ui-categories-012.spec.ts` |
| Case | `test-cases/Categories/category-hierarchy-and-filtering.md` (UI-Categories-012), Review: Approved (2026-11-05, bulk approval) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-11-05 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 2 Major, 2 Minor, 3 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass (exit 0, no output) |
| `npx eslint` on the spec, `pages/category.page.ts`, `pages/parts.page.ts`, `pages/base.page.ts`, `pages/components/table.component.ts`, `fixtures/pages.fixture.ts`, `fixtures/data.fixture.ts`, `fixtures/index.ts` | Pass (exit 0, no errors, no warnings) |
| `npx playwright test <spec> --list` | 1 test: `[chromium] › ... › Category hierarchy and filtering › UI-Categories-012: A part in the deepest category appears in the top category's list` |

Tests were not run (reviewer guardrail).

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-steps: log in, open the *Parts* view | None stated | `auth` fixture (`test.use({ user: 'engineer' })`, L4); `partsPage.openCategories()` (L27) | None (page-object wait for the categories table) | Covered |
| 1. Open the top category and read the part list (`QA-<suffix> Top`) | `QA-<suffix> Part Deep`, in the category four levels down, is listed | `1. Open the top category and read the part list` (L29-33) | `expect(categoryPage.partsTable.row(partName)).toBeVisible()` (L32) | Covered |
| 2. Open the deepest category through the hierarchy and read the part list (`QA-<suffix> Deep`) | The list shows `QA-<suffix> Part Deep` | `2. Open the deepest category through the hierarchy and read the part list` (L35-42) | `expect(categoryPage.partsTable.row(partName)).toBeVisible()` (L41) | Covered |

Both Expected results state presence only, and the spec asserts presence of a uniquely named row. The assertion is as specific as the case. Both assertions would also pass on the global Parts list and on every ancestor of Deep, so proof that the right list is read depends on the navigation waits in the page objects (finding 4).

Other B checks:
- **Order and titles:** two `test.step`s, in case order, titled `<n>. <case action>` word for word. Pass.
- **Prerequisites, user:** `engineer`, as the case states. No user change. Pass.
- **Prerequisites, settings:** None stated, none set. Pass.
- **Prerequisites, data:** all six categories and five parts are created through `data` with `data.name` names, and the hierarchy Top > Mid > Leaf > Deep is correct. But `Part Sib` goes into Top, not Sibling (finding 1).
- **Cleanup:** the test creates no records through the UI, so nothing needs `trackPart`. `data` deletes in reverse creation order: the parts first, then Empty, Sibling, Deep, Leaf, Mid, Top. The case lists Deep, Leaf, Empty, Sibling, Mid, Top. Both orders delete children before their parents, so the result is the same. Pass.
- **Form checks:** no form in this case. N/A.
- **Absence checks:** none in the spec, none in the case. Pass.
- **Traceability:** the first-line `// case:` header matches the file and ID, the test title is `<case ID>: <case title>`, `describe` is `Category hierarchy and filtering` (the case file's title), and the tag `@regression` matches Tags: Regression. Pass.
- **Review status:** Approved. Pass.

## C. Conventions

Code only this spec uses (Grep across `tests/ui/`), reviewed as new code: all of `pages/category.page.ts` (`CategoryPage`: `subcategoriesTab`, `partsTab`, `subcategoriesTable`, `partsTable`, `openPartsTab`, `openSubcategory`), its registration in `fixtures/pages.fixture.ts`, and in `PartsPage` the members `categoriesTable`, `openCategories`, `openCategoryByName`.

- Import from `fixtures/index.ts` only; `test.use({ user })`; no `page.locator`/`getBy*`, URLs, IDs or credentials in the spec; prerequisites only through `data`. Pass.
- Naming (UI §9): spec file, page object file and class, locator nouns, verb methods. Pass.
- Page objects (UI §4): `CategoryPage` extends `BasePage`; locators are `readonly` and built in the constructor with `getByRole` (via `panelTab`/`panel`/`TableComponent`); `.first()` carries a comment; `expect` is used only for waits, never for business outcomes; no test data, users or API calls. Pass.
- Layer boundaries (UI §1): the spec uses fixtures and page objects only; page objects use components and `BasePage`. Pass.
- Existing members: `partsTab`, `partsTable`, `open`, `openCategory` are still used by other specs with their documented behaviour. I found no sign of a renamed or changed member. I could not see a diff, because git is outside the reviewer's allowed commands.
- Problems: findings 2, 3 and 4.

## D. SOLID and design

- Single responsibility: the spec tests one case, and each method does one thing. Pass. But two page objects now model the same InvenTree screen (finding 2).
- Open/closed: no flags or caller-specific branches. Pass.
- Liskov: `CategoryPage` does not override `goto`, and `PartsPage.openCategories` uses `BasePage.goto`, which keeps the app-shell wait. Pass.
- Interface segregation: the spec requests `partsPage`, `categoryPage` and `data`, and uses all three. Pass.
- Dependency inversion: the spec depends on page objects and fixtures only, not on the DOM or the API. Pass.
- DRY: problem, see finding 2.

## E. Playwright and TypeScript practice

- Every call is awaited, with no floating promises. Pass.
- Assertions are web-first (`await expect(locator).toBeVisible()`), with no value reads, polling or sleeps. Pass.
- No conditionals, loops, `try/catch`, `test.only` or `test.fixme`. Pass.
- Isolation: the test uses only records it creates itself, with unique names. Pass.
- Locators: by role, scoped to the panel; `row(partName)` matches a unique `QA-` name. Pass.
- TypeScript: no `any`, casts or `!`; `const` throughout; the `ApiRecord.pk` types flow from `data`. Pass.
- Readability: the spec reads like the case. Pass.
- Problems: finding 3 (a UI action in the spec).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Major | `tests/ui/Categories/ui-categories-012.spec.ts:19`, `:25` | Checklist B (Prerequisites, data); case Prerequisites ("one part in each of Top, Mid, Leaf, Deep and Sibling ... `QA-<suffix> Part Sib`") | `await data.part(data.name('Part Sib'), { category: top.pk });` puts *Part Sib* in **Top**, and the Sibling category's record is thrown away (L19), so Sibling has no part. The spec does not build the data the case states. Neither Expected result can change because of it (cascade lists the part in Top either way), so this is not a Blocker. But the setup is wrong, and the same prerequisite block is shared by UI-Categories-008 to 013 and is likely to be copied. | `const sibling = await data.category(data.name('Sibling'), { parent: top.pk });` and `await data.part(data.name('Part Sib'), { category: sibling.pk });`. |
| 2 | Major | `pages/category.page.ts:8,15` (`partsTab`), `:10,17` (`partsTable`), `:27-33` (`openSubcategory`); duplicates `pages/parts.page.ts:10,20`, `:12,22`, `:45-51` | DRY; UI §4 (one class per page); single responsibility | The Parts view and a category page are the same InvenTree screen (panel group `partcategory`). `PartsPage` already models a category's page: `openCategory(categoryId)` opens `/web/part/category/<id>/parts`, and `ui-xf-001.spec.ts:93-98` uses `partsPage.partsTab`/`partsTable` on a category page. `CategoryPage.partsTab` and `partsTable` are identical locators (`panelTab('partcategory', 'Parts')`, `TableComponent(this.panel('Parts'))`). `openSubcategory` repeats the body of `openCategoryByName` (click `cell(name, name).first()`, wait for the URL to change). A locator fix for this screen now has to be made in two classes. | Additions only (UI §11): keep in `CategoryPage` only what `PartsPage` lacks (`subcategoriesTab`, `subcategoriesTable`, `openSubcategory`, a tab-opening method), and have the spec use `partsPage.partsTab`/`partsTable`, or the reverse. Put the shared "click the Name cell and wait for the next page" in one place, e.g. a `TableComponent` method that returns the cell, with the navigation wait in one helper. Which class owns the category screen is the architect's decision. |
| 3 | Minor | `tests/ui/Categories/ui-categories-012.spec.ts:36` | UI §4 (page objects hold every UI action; methods wait for their own result) | `await categoryPage.subcategoriesTab.click();` performs a UI action in the spec and waits for nothing. The same page object offers `openPartsTab()`, which clicks and waits for the table, so the two tabs are handled differently. This is not a lint error. The same pattern was rated Minor in the UI-Part-002 review (finding 1). | Add `CategoryPage.openSubcategoriesTab()` (click the tab, then wait for `subcategoriesTable.searchInput`) and call it here. |
| 4 | Minor | `pages/parts.page.ts:50`; `pages/category.page.ts:32` | UI §4 (methods wait for their own result); UI §8 | In both methods the second wait is already true before the click. `navigationMenu` is visible on every screen, and on the parent's Subcategories panel `subcategoriesTable.searchInput` is already visible. So the only real wait is "the URL changed", and nothing confirms that the page shown is the named category. That matters here because both spec assertions (`partsTable.row(partName)` visible) also pass on the global Parts list and on every ancestor of Deep. The spec's proof that it reads Top's list and then Deep's list rests entirely on these waits. | Wait for something that only exists on the target page, e.g. `await expect(this.breadcrumbs.last()).toHaveText(name)` (confirm in the app that the last breadcrumb is the open category), or a URL pattern for a category ID. Keep it as a page-object wait. The case does not ask for a "page opened" assertion in the spec. |
| 5 | Info | `pages/parts.page.ts:45-48` | Robustness | `openCategoryByName` clicks the Name cell without searching, so `QA-<suffix> Top` must be on the first page of the Part Categories table. On the local demo data this holds, but leftover `QA-` categories or a larger dataset could push it to a later page. The test would then time out (a loud failure, not a false pass). | Optionally type the name into `categoriesTable.search(name)` before the click. |
| 6 | Info | `pages/category.page.ts:29` | UI §4 (`nth()`/`.first()` with a reason) | The comment says the Path cell of a top-level row repeats the name. Rows in a Subcategories list are not top-level (their Path is `Top/Mid`), so the stated reason may not apply here. `.first()` is still correct and harmless. I am unsure how InvenTree 1.5.6 renders Path in this table. | Reword the comment to the real reason for subcategory rows, or say it is a guard. |
| 7 | Info | case `category-hierarchy-and-filtering.md:119`, `:134` | Case precision | The case says Part Deep is "in the category four levels down", but Deep is three levels below Top (level 4 of the hierarchy, as the Technique field says). The spec builds the hierarchy exactly as Prerequisites state, so the spec is right. | Architect may reword to "at level 4" or "three levels below". |

## Outside scope

- `CONVENTIONS.md` UI §5 lists the injected page objects as `app`, `loginPage`, `partsPage`, `partForm`, `partDetail`. `fixtures/pages.fixture.ts` now also injects `categoryPage`, `parameterForm` and `stockItemForm`.
- `BasePage.openBreadcrumb` (`pages/base.page.ts:57`) has the same no-op `navigationMenu` wait after its URL check as finding 4.
- `PartsPage.openPart` (`pages/parts.page.ts:69-71`) clicks the part name and does not wait for the detail page (UI §4).
