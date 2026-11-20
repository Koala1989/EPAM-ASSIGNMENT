# Review: UI-Detail_View-099 The BOM tab is visible for an Assembly part

| Item | Value |
|---|---|
| Spec | `tests/ui/Detail_View/ui-detail_view-099.spec.ts` |
| Case | `test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md` (UI-Detail_View-099), Review: Approved · 2026-11-05 |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-11-05 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 0 Major, 1 Minor, 2 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass, no errors |
| `npx eslint` on the spec, `pages/part-detail.page.ts`, `pages/base.page.ts`, `fixtures/index.ts`, `fixtures/data.fixture.ts`, `fixtures/pages.fixture.ts` | Pass, 0 errors, 0 warnings |
| `npx playwright test <spec> --list` | 1 test listed: `UI-Detail_View-099: The BOM tab is visible for an Assembly part` |

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| 1. Check the tabs of the part. | The *BOM* tab is shown (R-Detail_View-19). | `1. Check the tabs of the part.` (line 14) | `expect(partDetail.tab('Bill of Materials')).toBeVisible()` (line 16); exact-name tab in tab list `panel-tabs-part` | Covered (label differs from the case wording, see finding 1) |

- **Order and titles:** one step, titled `1. Check the tabs of the part.`, matching the case action. Pass.
- **Prerequisites:** user `engineer` via `test.use` (line 4) matches the case. Settings: none, none set. Data: category `QA-<suffix> Category` and part `QA-<suffix> Asm` with `assembly: true` created through `data` as admin with `data.name` (lines 9-11). Pre-step "open `QA-<suffix> Asm`" done with `partDetail.open(part.pk)` before step 1 (line 12); login through the form by the `user` fixture. Pass.
- **Cleanup:** no records created through the UI; `data.category` / `data.part` register both records for reverse-order cleanup. Pass.
- **Form checks:** no form in this case. N/A.
- **Absence checks:** none. Pass.
- **Traceability:** first-line `// case:` header correct; title `UI-Detail_View-099: The BOM tab is visible for an Assembly part` matches; `describe('Part detail header and tab visibility')` matches the case file's functionality; tags `@smoke`, `@regression` match Tags "Smoke, Regression". Pass.
- **Review status:** Approved. Pass.

## C. Conventions

- Layer boundaries (UI §1): spec uses only fixtures and page objects; no raw locators, API calls, URLs, IDs or credentials. Pass.
- UI §3: one test per case, one `test.step` per case step, assertion in the test, imports from `fixtures`. Pass.
- UI §4: `PartDetailPage.tab(name)` and `BasePage.panelTab` are existing members (also used by 088, 110, 111), not added for this spec; locator is `getByRole('tablist', { name: 'panel-tabs-part' }).getByRole('tab', { name, exact: true })`, matching the UI §10 panel-tab pattern. `open(partId)` waits for the header title. No new page object code from this spec (the uncommitted diff of `part-detail.page.ts` is attachment members used by other specs). Pass.
- UI §5 / §7: `user`, `data`, `partDetail` used through `fixtures/index.ts`; names via `data.name`. Pass.
- UI §8: no sleeps, `networkidle` or `force`. Pass.
- UI §9: file name, test title, tags follow the naming table. Pass.
- Problems: see findings 1.

## D. SOLID and design

- Single responsibility: one spec, one case; `tab()` returns a locator only. Pass.
- Open/closed, Liskov: no special-casing; `PartDetailPage` keeps `BasePage.goto` behaviour. Pass.
- Interface segregation: spec requests only `partDetail` and `data`, both used. Pass.
- Dependency inversion: spec depends on page object and fixture, not DOM or endpoints. Pass.
- DRY: reuses existing `tab()`; no duplication. Pass.

## E. Playwright and TypeScript practice

- All calls awaited; web-first assertion; no conditionals, loops, `try/catch`, `test.only` or `fixme`. Pass.
- Isolation: creates its own category and part, no dependency on demo data. Pass.
- Locator: role-based, exact name, scoped to the part tab list. Pass.
- TypeScript: no `any`, casts or `!`; `const` throughout. Pass.
- Observations: see findings 2 and 3.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Minor | `tests/ui/Detail_View/ui-detail_view-099.spec.ts:15-16` | CLAUDE.md "An app/case mismatch is a finding, not a fix"; UI §3 (spec reads like the case) | The case and R-Detail_View-19 name the tab *BOM*; the spec asserts a tab named *Bill of Materials* and explains the difference only in a code comment. The assertion is not weaker (exact name, same element), and the docs' section heading (`part-views.md` L82 "Bill of Materials") supports the app label, but the wording gap is not recorded anywhere the architect will see it (no entry in `test-cases/findings.md` or the Detail_View open questions). UI-Detail_View-100 will hit the same gap. | Keep the assertion. Report the label difference to the architect as a case-wording note (case and R-Detail_View-19 say *BOM*, 1.5.6 shows *Bill of Materials*) so the case can be marked Changed with the real label, or tag the comment `// CASE DEFECT:`-style for traceability. |
| 2 | Info | `tests/ui/Detail_View/ui-detail_view-099.spec.ts:11` | UI §3 (no extra setup) | `description: partName` is set on the part though the case states no description. Harmless (does not affect the tab under test); likely chosen to keep the record identifiable. | None required; drop it if InvenTree 1.5.6 does not need a description on create. |
| 3 | Info | `tests/ui/Detail_View/ui-detail_view-099.spec.ts:16` | Case technique (decision table) | The spec proves the tab is shown with Assembly on; "visible only if" (the off branch) is UI-Detail_View-100's job, so this is correct scope. Not a weakening. | None. |

## Outside scope

- `pages/part-detail.page.ts:83` `tab(name)` has no doc comment, unlike the neighbouring members (existing code, not added for this spec).
