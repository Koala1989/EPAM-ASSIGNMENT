# Review: UI-Detail_View-086 A part with every conditional attribute off shows none of the conditional tabs

| Item | Value |
|---|---|
| Spec | `tests/ui/Detail_View/ui-detail_view-086.spec.ts` |
| Case | `test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md` (UI-Detail_View-086), Review: Approved · 2026-11-05 |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-11-11 |
| Verdict | Changes required |
| Findings | 1 Blocker, 0 Major, 1 Minor, 4 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass, no errors |
| `npx eslint` on the spec, `pages/part-detail.page.ts`, `pages/base.page.ts`, `pages/components/{actions-menu,select,table,form,notification}.component.ts`, `fixtures/{index,data,pages,auth,user,expect}` | Pass, exit 0, 0 errors, 0 warnings |
| `npx playwright test <spec> --list` | 1 test listed: `Part detail header and tab visibility › UI-Detail_View-086: A part with every conditional attribute off shows none of the conditional tabs` |

## B. Case coverage

The case has one step with one Expected result that names six tabs. The table has one row per tab, because each tab is a separate requirement (R-Detail_View-08, 17, 19, 21, 23, 24).

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-steps: log in through the login form, open `QA-<suffix> AllOff` | None stated | Before the steps: `test.use({ user: 'allaccess' })` L4 (login form via `auth.fixture.ts:17`), `partDetail.open(part.pk)` L20 | L21 `expect(partDetail.title).toContainText(partName)` (checks the right part is open; `open` itself waits for the title, `part-detail.page.ts:75`) | Extra (a guard; acceptable) |
| 1. Read the tab list of the part page. | (sync) | `1. Read the tab list of the part page.` L23 | L25 `expect(partDetail.tab('Part Details')).toBeVisible()`: makes sure the tab list has rendered before the absence checks | Extra (a guard; acceptable) |
| 1 | *Variants* not shown (R-Detail_View-08) | L23 | L26-27 `tab('Variants')` `toBeHidden()` | Covered (no positive spec or run in the repo confirms the app label yet, see finding 2) |
| 1 | *Allocated* not shown (R-Detail_View-17) | L23 | L26-27 `tab('Allocated')` `toBeHidden()` | Uncertain: probably vacuous, see finding 2 |
| 1 | *BOM* not shown (R-Detail_View-19) | L23 | L26-27 `tab('BOM')` `toBeHidden()` | **Missing** (vacuous): the 1.5.6 tab is named *Bill of Materials* (`tests/ui/Detail_View/ui-detail_view-099.spec.ts:15-16`, `tests/ui/Attributes/ui-att-013.spec.ts:15`). An exact-name `tab('BOM')` matches nothing, so `toBeHidden` passes even when the BOM tab is shown. Finding 1 |
| 1 | *Used In* not shown (R-Detail_View-21) | L23 | L26-27 `tab('Used In')` `toBeHidden()` | Covered (label confirmed by `ui-att-013.spec.ts:33` `openTab('Used In')`) |
| 1 | *Suppliers* not shown (R-Detail_View-23) | L23 | L26-27 `tab('Suppliers')` `toBeHidden()` | Covered (label confirmed by `ui-detail_view-110.spec.ts:15`, `ui-part-006.spec.ts:54`) |
| 1 | *Purchase Orders* not shown (R-Detail_View-24) | L23 | L26-27 `tab('Purchase Orders')` `toBeHidden()` | Covered (no positive spec or run in the repo confirms the app label yet, see finding 2) |

Ask the question for the BOM row: if the BOM tab were shown, which line would fail? None. `tab('BOM')` is `getByRole('tablist', { name: 'panel-tabs-part' }).getByRole('tab', { name: 'BOM', exact: true })` (`base.page.ts:71`), and the app has no tab with that name, so the locator resolves to zero elements and `toBeHidden` passes either way. No other line in the test checks for BOM. The same holds for every tab name that differs from the app label.

Other B checks:
- **Order and titles:** one `test.step` for the one case step, titled `1. Read the tab list of the part page.`, the same as the case action. Pass.
- **Prerequisites:** user `allaccess` (L4) matches the case. Settings: None, and none are set. Data: category `QA-<suffix> Category` (L9) and part `QA-<suffix> AllOff` (L10-19) are created through `data` with `data.name`, and Template, Assembly, Component, Salable and Purchaseable are all `false` (L14-18). Setting them explicitly matters, because InvenTree turns some of them on by default. Pre-step "open" is L20. Pass, except the extra `description` (finding 4).
- **Cleanup:** nothing is created through the UI. `data.category`/`data.part` register both records (`data.fixture.ts:34`, `:40`). Pass.
- **Form checks:** no form. N/A.
- **Absence checks:** the absences are stated by the Expected result. They run after `open` (title visible, `part-detail.page.ts:75`), after the title shows this part's name (L21, so the part record has loaded) and after the tab list has rendered (L25). They do not run before the action that would show the tabs. Pass for timing. Finding 1 is about the names, not the timing.
- **Traceability:** the first-line `// case:` header is correct (L1). The test title matches `<case ID>: <case title>` (L7). The tag `@regression` matches Tags "Regression". The `describe` paraphrases the case file title (finding 5). Pass otherwise.
- **Review status:** Approved · 2026-11-05. Pass.
- **Case notes:** *Build Orders* is left out, as the case's Notes say. Pass.

## C. Conventions

- UI §1 / §3: the spec uses only fixtures and page objects. It has no raw locators, API calls, URLs, IDs or credentials, and its assertions are in the test. Pass.
- UI §4: the spec uses `PartDetailPage.open`, `title` and `tab`. All three already exist and other specs use them (Grep: 088, 099, 110, 111, 405, XF-001, REV-001, ATT-008, ATT-013, Part-006, Part-074). The generator added no page object members for this spec. `tab()` is role-based and scoped to the `panel-tabs-part` tab list (UI §10). Pass.
- UI §5 / §7: `user`, `data` and `partDetail` come through `fixtures/index.ts`, and names come from `data.name`. Pass.
- UI §8: no sleeps, `networkidle` or `force`. Pass.
- UI §9: file name, test title and tag follow the naming table. Pass.
- Problems: findings 1, 3, 5, 6.

## D. SOLID and design

- Single responsibility: one spec covers one case. `tab()` only returns a locator. Pass.
- Open/closed: no flags or special-casing are added to page objects. Pass.
- Liskov: `PartDetailPage.open` calls `BasePage.goto` (which waits for the app shell) and then waits for the title. Pass.
- Interface segregation: the spec requests only `partDetail` and `data`, and uses both. Pass.
- Dependency inversion: the spec depends on the page object and fixtures. However, the tab labels are inline strings in the spec rather than names owned by the page object, and this is how the wrong label got in unnoticed. See finding 6.
- DRY: the spec reuses existing members. Pass.

## E. Playwright and TypeScript practice

- Every call is awaited, and the assertions are web-first. There is no `try/catch`, `test.only` or `fixme`, and no conditionals. Pass.
- The test is isolated: it creates its own category and part and does not depend on demo data. Pass.
- TypeScript: no `any`, casts or `!`, and `const` throughout. Pass.
- Problems: finding 3 (the loop of hard assertions).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Blocker | `tests/ui/Detail_View/ui-detail_view-086.spec.ts:26-27` | Reviewer B (Expected result Missing); UI §3 "Each Expected result of the case is at least one `expect`"; CLAUDE.md "An app/case mismatch is a finding, not a fix" | `tab('BOM')` uses the case wording, but InvenTree 1.5.6 names the tab *Bill of Materials*. The sibling spec `ui-detail_view-099.spec.ts:15-16` says so ("The app names the BOM tab 'Bill of Materials'") and asserts `tab('Bill of Materials')` visible, and `ui-att-013.spec.ts:15` opens it by that name. `tab()` matches the exact name (`base.page.ts:71`), so `tab('BOM')` resolves to no element and `toBeHidden()` always passes. R-Detail_View-19 is not tested: the test stays green if the BOM tab is shown for this part. | Assert `partDetail.tab('Bill of Materials')` with a one-line comment that the app uses this label, as in 099. Report the wording gap to the architect: the case and R-Detail_View-19 say *BOM*, 1.5.6 shows *Bill of Materials*. Before re-running, check every one of the six labels in the live app (see finding 2). |
| 2 | Info | `tests/ui/Detail_View/ui-detail_view-086.spec.ts:26` | Reviewer B; unsure, so marked Info | *Allocated* is probably not the app label either. The docs' body text says "*Allocated* tab" (`requirements/docs/part-views.md:80`), but the section heading is *Allocations* (`:78`). For BOM, the heading (*Bill of Materials*, `:82`) is the one that matched the app, not the body text (`:84`, "*BOM* tab"). As far as I know, InvenTree's part page labels this panel "Allocations". Nothing in this repo confirms either name. *Variants* and *Purchase Orders* are not confirmed by any positive spec or run either. Only *Used In* (`ui-att-013.spec.ts:33`) and *Suppliers* (`ui-detail_view-110.spec.ts:15`) are. If *Allocated* is wrong, its row is Missing and the severity is the same as finding 1. | Check the six labels in the live 1.5.6 tab list (Playwright MCP snapshot of a part with every attribute on, i.e. UI-Detail_View-085's data). Use the app labels, with a comment wherever a label differs from the case, and report the differences to the architect. |
| 3 | Minor | `tests/ui/Detail_View/ui-detail_view-086.spec.ts:26-28` | UI §3 "Tests read like the manual case"; reviewer E (readability) | The six checks run as a `for` loop of hard `expect`s over inline strings. The first tab that is shown stops the step, so one run reports only one of the six requirements. The loop also hides which label is the case's word and which is the app's, which is how finding 1 slipped in. | Write six explicit assertions, one per tab, in the case's order, each with its requirement ID as a short comment, and the app label where it differs. |
| 4 | Info | `tests/ui/Detail_View/ui-detail_view-086.spec.ts:12` | UI §3 "No setup logic" beyond the case's Prerequisites | `description: partName` is set although the case's Data names no description. It does not affect the tabs under test, and the sibling specs (088, 099, 110, 111) do the same. | No change needed. Drop it if 1.5.6 does not require a description on create. |
| 5 | Info | `tests/ui/Detail_View/ui-detail_view-086.spec.ts:6` | UI §3 "a `test.describe` per functionality (the case file's title)" | The `describe` is `'Part detail header and tab visibility'`. The case file title is "Part detail view header details and tab visibility". It matches the sibling specs 088, 099, 110 and 111, so the report groups them together. | No change in this spec alone. If the architect wants the exact title, rename it in all five specs together. |
| 6 | Info | `pages/part-detail.page.ts:96-98` | Reviewer D (dependency inversion); UI §4 (page objects own the UI's names) | `tab(name: string)` accepts any string. Because a wrong name gives a locator that matches nothing, every absence check on a misspelled or case-worded tab passes silently. The page object already types its menu items (`PartAction`, `part-detail.page.ts:7`). Changing an existing member's signature is the architect's decision (UI §11). | Suggestion for the architect: type the tab names, e.g. `type PartTab = 'Part Details' \| 'Variants' \| 'Bill of Materials' \| ...` as confirmed in the app. Then `tab('BOM')` becomes a type error and the absence specs (086, 088, 093, 100, ...) cannot use a name that does not exist. |

## Outside scope

- `tests/ui/Detail_View/ui-detail_view-088.spec.ts:15` asserts `tab('Variants')` `not.toBeVisible()` without first waiting for the tab list (086:25 and 111:16 do wait). It has the same exposure as finding 6, and it can also pass before the tab list renders.
- The case wording *BOM* and *Allocated* comes from the docs' body text and is used across the Detail_View and Attributes cases (e.g. UI-Detail_View-085, 091-100 and UI-ATT-003, 046). Every spec automated from them will hit the same label gap, so it is worth recording once for the architect (a findings entry or case-wording note) rather than per spec.
- `pages/part-detail.page.ts:96` `tab(name)` has no doc comment, unlike its neighbours (existing code).
