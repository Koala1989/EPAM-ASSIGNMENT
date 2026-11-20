# Review: UI-Categories-015 What-if: a new part created in a sub-category appears in the parent category's list

| Item | Value |
|---|---|
| Spec | `tests/ui/Categories/ui-categories-015.spec.ts` |
| Case | `test-cases/Categories/category-hierarchy-and-filtering.md` (UI-Categories-015), Review: Approved (2026-11-05, bulk approval) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-11-05 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 2 Major, 3 Minor, 5 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass (exit 0, no output) |
| `npx eslint` on the spec, `pages/category.page.ts`, `pages/parts.page.ts`, `pages/part-form.page.ts`, `pages/part-detail.page.ts`, `pages/base.page.ts`, `pages/components/table.component.ts`, `pages/components/form.component.ts`, `pages/components/select.component.ts`, `pages/components/actions-menu.component.ts`, `fixtures/pages.fixture.ts`, `fixtures/data.fixture.ts`, `fixtures/auth.fixture.ts`, `fixtures/index.ts`, `utils/names.ts` | Pass (exit 0, no errors, no warnings) |
| `npx playwright test <spec> --list` | 1 test: `[chromium] › tests\ui\Categories\ui-categories-015.spec.ts:7:7 › Category hierarchy and filtering › UI-Categories-015: What-if: a new part created in a sub-category appears in the parent category's list` |

Tests were not run (reviewer guardrail). No run artefacts for this spec were found under `test-results/`.

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-steps: log in through the login form, open the *Parts* view | None stated | `auth` fixture (`test.use({ user: 'engineer' })`, L4); `partsPage.open()` (L24) | None (page-object wait for the parts table) | Covered |
| 1. Open the *Add Parts* dropdown and select *Create Part* | The *Create Part* form opens | `1. Open the Add Parts dropdown and select Create Part` (L26-29) | `expect(partForm.root).toBeVisible()` (L28) | Covered (same assertion as the CONVENTIONS.md UI §3 example for this step) |
| 2. Fill in the form and submit (Name `QA-<suffix> Part New`, Description `New part`, Category `QA-<suffix> Leaf`) | The form closes and the new part's detail page opens | `2. Fill in the form and submit` (L31-39) | Filled fields: `textField('name')` `toHaveValue(partName)` (L33), `textField('description')` `toHaveValue('New part')` (L34), `categoryField` `toHaveValue(/(^\|\/)<leaf>$/)` (L35). After submit: `partForm.root` `toBeHidden()` (L37), `partDetail.detail('Name')` `toHaveText(partName)` (L38) | Covered (the category check hedges, see finding 4) |
| 3. Open `QA-<suffix> Top` and read its part list | `QA-<suffix> Part New` is listed (R-Categories-02) | `3. Open Top and read its part list` (L41-46) | `expect(categoryPage.partsTable.row(partName)).toBeVisible()` (L45) | Covered |
| 4. Open `QA-<suffix> Mid` and read its part list | `QA-<suffix> Part New` is listed (R-Categories-02) | `4. Open Mid and read its part list` (L48-53) | `expect(categoryPage.partsTable.row(partName)).toBeVisible()` (L52) | Covered |

Steps 3 and 4 only ask for presence, and the spec checks presence of a row with a unique `QA-` name. That is as specific as the case. The same assertion would also pass on the global Parts list and on Top's list (Part New is in both). So the proof that step 4 reads Mid's list, and not Top's, rests on the navigation waits in the page objects (finding 5).

Other B checks:
- **Order and titles:** four `test.step`s in case order, titled `<n>. <case action>`. Step 3 and 4 shorten `QA-<suffix> Top`/`Mid` to `Top`/`Mid`, which is acceptable. Pass.
- **Prerequisites, user:** `engineer`, as the case states. No user change. Pass.
- **Prerequisites, settings:** None stated, none set. Pass.
- **Prerequisites, data:** all six categories are created through `data` with `data.name` names, and the hierarchy is correct (Top > Mid > Leaf > Deep, with Sibling and Empty under Top). But only three of the five stated parts exist: `Part Deep` and `Part Sib` are missing (finding 1).
- **Cleanup:** the UI-created part is registered by name before creation (`data.trackPart(data.name('Part New'))`, L12). The prerequisite records are removed by `data`. Pass. The cleanup order differs from the case's postconditions (finding 6, Info).
- **Form checks:** step 2 fills Name, Description and Category, and all three are asserted. The step leaves no field untouched that is asserted. Pass (with finding 4 on how the category is asserted).
- **Absence checks:** one only, `partForm.root` `toBeHidden()` (L37). The Expected result states it ("The form closes"), and it runs after *Submit*. Pass.
- **Traceability:** the first-line `// case:` header matches the file and ID. The test title is `<case ID>: <case title>` word for word. `describe` is `Category hierarchy and filtering` (the case file's title). Tags `@regression`, `@cross-functional` match Tags: Regression, Cross-functional. Pass.
- **Review status:** Approved. Pass.

## C. Conventions

No page object or component member is used by this spec alone. Every `CategoryPage` member it calls, and `PartsPage.openCategories`/`openCategoryByName`, is also used by `tests/ui/Categories/ui-categories-012.spec.ts`. `PartFormPage.categoryField` is also used by `tests/ui/XF/ui-xf-001.spec.ts`. So there is no new code to review as this spec's own. The shared members it relies on were checked against UI §4 and UI §8 below.

- Imports from `fixtures/index.ts` only; `test.use({ user })`; no `page.locator`/`getBy*`, CSS, URLs, IDs or credentials in the spec; prerequisites only through `data`; names through `data.name`. Pass.
- Assertions are only in the spec. Page objects use `expect` only to wait. Pass.
- Naming (UI §9): spec file, step titles, locator nouns, verb methods. Pass.
- Layer boundaries (UI §1): the spec uses only fixtures and page objects. Page objects use `BasePage` and components. Pass.
- Locator priority (UI §4): `getByRole`/`getByLabel` throughout the members used; `.first()` and `.nth(1)` carry comments. Pass.
- Problems: findings 2, 3, 5, 8, 9.

## D. SOLID and design

- Single responsibility: the spec tests one case, and each page-object method does one thing. Pass. But two classes model the same screen (finding 2).
- Open/closed: no flags or caller-specific branches in the methods used. Pass.
- Liskov: `CategoryPage` and `PartsPage` keep `BasePage.goto` (app-shell wait), and `PartDetailPage` too. Pass.
- Interface segregation: the spec requests `partsPage`, `partForm`, `partDetail`, `categoryPage` and `data`, and uses all five. Pass.
- Dependency inversion: the spec depends on page objects and fixtures, not on the DOM, CSS or endpoints. Pass.
- DRY: problem, see finding 2.

## E. Playwright and TypeScript practice

- Every Playwright call and promise is awaited. Pass.
- Web-first assertions only; no `textContent()`/`isVisible()` reads, no polling or sleeps. Pass.
- No conditionals, loops, `try/catch`, `test.only` or `test.fixme`. Pass.
- Isolation: the test uses only records it creates, with unique `QA-` names. Pass.
- Locators: `row(partName)` matches one uniquely named row. Pass.
- TypeScript: no `any`, casts or `!`; `const` throughout; `pk` types come from `ApiRecord`. Pass.
- Readability: the spec reads like the case, except L35 (finding 4).
- Problems: findings 3, 4.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Major | `tests/ui/Categories/ui-categories-015.spec.ts:17-22` | Checklist B (Prerequisites, data); case Prerequisites ("one part in each of Top, Mid, Leaf, Deep and Sibling, named ... `QA-<suffix> Part Deep`, `QA-<suffix> Part Sib`") | The spec creates `Part Top`, `Part Mid` and `Part Leaf` only. `Part Deep` (in Deep) and `Part Sib` (in Sibling) are never created, and the Deep and Sibling records are thrown away (L17-18), so they cannot hold a part. The spec does not build the data set the case states, and nothing in the spec says it leaves them out on purpose. Neither Expected result can change because of it (both only ask whether Part New is listed), so this is not a Blocker. | `const deep = await data.category(data.name('Deep'), { parent: leaf.pk });`, `const sibling = await data.category(data.name('Sibling'), { parent: top.pk });`, then `await data.part(data.name('Part Deep'), { category: deep.pk });` and `await data.part(data.name('Part Sib'), { category: sibling.pk });`. |
| 2 | Major | `pages/category.page.ts:8,15` (`partsTab`), `:10,17` (`partsTable`), `:27-33` (`openSubcategory`); duplicates `pages/parts.page.ts:10,20`, `:12,22`, `:45-51` | DRY; UI §4 (one class per page); single responsibility | The Parts view and a category page are the same InvenTree screen (panel group `partcategory`). `CategoryPage.partsTab`/`partsTable` are the same locators as `PartsPage.partsTab`/`partsTable`. `openSubcategory` repeats the body of `openCategoryByName`. The spec shows the cost directly: it opens Top with `partsPage.openCategoryByName` (L43) and then reads Top's list through `categoryPage.partsTable` (L45), on the same screen. A locator fix for this screen has to be made in two classes. This is the same root cause as finding 2 of the UI-Categories-012 review, and one fix covers both. | Decide which class owns the category screen (architect, UI §11). Keep in the second class only what the first lacks. Put "click the Name cell and wait for the next category page" in one helper. |
| 3 | Minor | `tests/ui/Categories/ui-categories-015.spec.ts:49` | UI §4 (page objects hold every UI action; methods wait for their own result) | `await categoryPage.subcategoriesTab.click();` is a UI action in the spec, and it waits for nothing. The same page object has `openPartsTab()`, which clicks and waits for the table, so the two tabs are handled differently. `openSubcategory` then reads `page.url()` as its "before" URL right after this click. If the tab switch ever updated the URL after that read, the method's "URL changed" wait would be met by the tab switch and not by opening Mid. I think this is unlikely in practice. Not a lint error. | Add `CategoryPage.openSubcategoriesTab()` (click, then wait for `subcategoriesTable.searchInput`) and call it here, as `openPartsTab()` is called on L44 and L51. |
| 4 | Minor | `tests/ui/Categories/ui-categories-015.spec.ts:35`; `pages/part-form.page.ts:63` | UI §3 (assert as specifically as possible; readable spec); UI §4 (doc comments describe UI behaviour) | ``toHaveValue(new RegExp(`(^\|/)${leafName}$`))`` accepts two different displays, the bare name *or* any path ending in `/<leaf>`. So the spec does not pin what InvenTree shows for a nested category. This conflicts with the `categoryField` doc comment ("its input value is the selected category's name"), which `ui-xf-001.spec.ts:36` relies on with an exact match. The regex also interpolates a name without escaping it. That is safe for today's `QA-<hex> Leaf` names, but it breaks silently if `data.name` ever produces regex metacharacters. And the line has no comment explaining it. Its end anchor does have value: it rejects a wrong pick of the child `Deep` (see finding 7). | Confirm in the app what the tree field shows for a nested category. Then assert that exact string: ``${topName}/${midName}/${leafName}`` (as a template literal) if it is the path, or `leafName` if it is the name. Correct the `categoryField` doc comment if the value is the path. |
| 5 | Minor | `pages/parts.page.ts:50`; `pages/category.page.ts:32` | UI §4 (methods wait for their own result); UI §8 | In `openCategoryByName` and `openSubcategory`, the second wait is already true before the click: `navigationMenu` is visible on every screen, and on Top's Subcategories panel `subcategoriesTable.searchInput` is already visible. The only real wait is "the URL changed", and nothing confirms that the page shown is the named category. Here this matters more than usual: step 4's assertion (L52) is identical to step 3's (L45), and it passes on Top's list, which the test has just read. | Wait for something that only exists on the target category's page, e.g. the last breadcrumb reading the category name (confirm in the app). Keep it as a page-object wait. The case does not ask for a "page opened" assertion in the spec. |
| 6 | Info | `tests/ui/Categories/ui-categories-015.spec.ts:12`; `fixtures/data.fixture.ts:125` | Case Postconditions ("set it inactive and delete it, then clean up the rest") | `trackPart` is registered first, and cleanups run in reverse, so Part New is deleted last. By then Leaf, Mid and Top are deleted (`delete_parts: false`), and the part has moved up to the top level. Cleanup still finds it by its unique name and deletes it, so the result is the same. The order differs from the case. | None needed. To match the case, register `trackPart` after the `data.*` prerequisites (still before *Submit*). |
| 7 | Info | `pages/components/select.component.ts:32-35` | Locators: text matching that can hit several elements | `select(leafName)` clicks the first option whose text *contains* `QA-<suffix> Leaf`. If the category picker shows paths, the child `Deep` (`.../Leaf/Deep`) also matches, and the pick depends on option order. I am unsure how 1.5.6 renders these options. L35's `$` anchor would catch a wrong pick (a loud failure). | None for this spec. If the options show paths, consider an exact or end-anchored option match in `SelectComponent`. |
| 8 | Info | `pages/parts.page.ts:53-55` | UI §4 (methods wait for their own result, e.g. the form opened) | `addParts` clicks the menu item and does not wait for the form. `PartFormPage.waitUntilOpen()` exists. The spec's own L28 assertion covers it here, so there is no flakiness. | Optionally wait for `form().submitButton` in `addParts`, like `PartDetailPage.addParameter`. |
| 9 | Info | `pages/parts.page.ts:45-48` | Robustness | `openCategoryByName` clicks Top's Name cell without searching, so Top must be on the first page of the Part Categories table. Leftover `QA-` categories could push it to a later page. The test would then time out (a loud failure, not a false pass). | Optionally `categoriesTable.search(name)` before the click. |
| 10 | Info | case `category-hierarchy-and-filtering.md:205`, `:222-223` | Case precision | The Summary says the part "is listed in that category and in all its parent categories", but no step reads Leaf's own list. The spec correctly follows the steps (Top and Mid only), and adding a Leaf check would be Extra. | Architect may add a Leaf step or narrow the Summary to the parent categories. |

## Outside scope

- `CONVENTIONS.md` UI §5 lists the injected page objects as `app`, `loginPage`, `partsPage`, `partForm`, `partDetail`. `fixtures/pages.fixture.ts` also injects `categoryPage`, `parameterForm` and `stockItemForm`.
- `BasePage.openBreadcrumb` (`pages/base.page.ts:57`) has the same no-op `navigationMenu` wait after its URL check as finding 5.
