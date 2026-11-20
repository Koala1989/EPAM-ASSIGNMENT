# Review: UI-Detail_View-110 The Suppliers tab is visible for a Purchaseable part

| Item | Value |
|---|---|
| Spec | `tests/ui/Detail_View/ui-detail_view-110.spec.ts` |
| Case | `test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md` (UI-Detail_View-110), Review: Approved · 2026-11-05 |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-11-05 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 2 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass, no errors |
| `npx eslint` on the spec, `pages/part-detail.page.ts`, `pages/base.page.ts`, `fixtures/data.fixture.ts`, `fixtures/pages.fixture.ts`, `fixtures/index.ts` | Pass, no errors or warnings |
| `npx playwright test <spec> --list` | 1 test listed in project `chromium` |

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-steps: log in, open `QA-<suffix> Buy` | (none stated) | Before the steps, line 12 `partDetail.open(part.pk)` | `open` waits for the part header (page object) | Covered |
| 1. Check the tabs of the part. | The *Suppliers* tab is shown (R-Detail_View-23). | `1. Check the tabs of the part.` (line 14) | `await expect(partDetail.tab('Suppliers')).toBeVisible()` (line 15) | Covered |

- **Order and titles:** one step, titled `1. <case action>` verbatim. Pass.
- **Prerequisites:** user `allaccess` via `test.use` (line 4) matches the case; Settings: None, none set; data: category `data.name('Category')` and part `data.name('Buy')` with `purchaseable: true` created through `data` as admin (lines 9-11), matching the case; login through the form by the `user` fixture. Pass. See Info 1 for the extra `description` field.
- **Cleanup:** both records are created through `data` and removed by it (part made inactive and deleted, then the category); the steps create nothing through the UI. Pass.
- **Form checks:** not applicable (no form).
- **Absence checks:** none. Pass.
- **Traceability:** first-line `// case:` header correct; test title `UI-Detail_View-110: The Suppliers tab is visible for a Purchaseable part` matches; `describe('Part detail header and tab visibility')` matches the case file title; tag `@regression` matches Tags: Regression. Pass.
- **Review status:** Approved. Pass.

## C. Conventions

- Layers (UI §1): spec uses only fixtures and page objects; no raw locators, no API calls, no URLs or IDs (part ID comes from `data`). Pass.
- UI §3: one test, one step per case step, assertion in the test, web-first. Pass.
- UI §4: no page object members were added for this spec (`pages/part-detail.page.ts` is unchanged in git); `tab(name)` is an existing member delegating to `BasePage.panelTab`, `getByRole('tablist', { name: 'panel-tabs-part' }).getByRole('tab', { name, exact: true })`, which follows the locator priority and UI §10 pattern. Pass.
- UI §5: imports from `fixtures/index.ts`; requests only `partDetail` and `data`. Pass.
- UI §7, UI §8, UI §9: no credentials, no sleeps, naming of file, folder and test follows the table. Pass.

No findings in this section.

## D. SOLID and design

- Single responsibility: the spec tests one case; `PartDetailPage` models the part detail page. Pass.
- Open/closed, Liskov: no flags or special cases added; `PartDetailPage.open` uses `BasePage.goto`, which keeps the app-shell wait. Pass.
- Interface segregation: only the two fixtures used are requested. Pass.
- Dependency inversion: no DOM, CSS or endpoint knowledge in the spec. Pass.
- DRY: data setup mirrors the pattern in `tests/ui/REV/ui-rev-001.spec.ts`; no duplicated page object logic. Pass.

## E. Playwright and TypeScript practice

- All calls awaited; web-first assertion; no conditionals, loops, `try/catch`, `test.only` or `test.fixme`. Pass.
- Isolation: uses only records it creates. Pass.
- Locator: role with accessible name, `exact: true`, scoped to the part tab list. Pass.
- TypeScript: `const` only, no `any`, casts or non-null assertions. Pass.
- Readability: reads like the case. See Info 2.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/ui/Detail_View/ui-detail_view-110.spec.ts:11` | UI §3 "Assert what the case asks" / Prerequisites fidelity | The part is created with `description: partName`, a field the case's Data prerequisite does not state. It does not affect the assertion and matches the pattern in `ui-rev-001.spec.ts`, so it is probably there to satisfy InvenTree's create validation; I could not confirm whether 1.5.6 requires it. | None needed. If description is not required by the API, it can be dropped; otherwise a one-line comment would explain it. |
| 2 | Info | `tests/ui/Detail_View/ui-detail_view-110.spec.ts:15` | Design note | The positive check alone cannot tell "tab shown because Purchaseable" from "tab always shown"; the decision table is only proven together with UI-Detail_View-111 (Purchaseable off: tab hidden). | None for this spec; make sure UI-Detail_View-111 is automated alongside it. |

## Outside scope

- `pages/components/form.component.ts` and `pages/part-form.page.ts` have uncommitted additions; this spec does not use them, so they were not reviewed here.
