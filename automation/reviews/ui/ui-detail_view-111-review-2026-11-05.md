# Review: UI-Detail_View-111 The Suppliers tab is hidden for a part that is not Purchaseable

| Item | Value |
|---|---|
| Spec | `tests/ui/Detail_View/ui-detail_view-111.spec.ts` |
| Case | `test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md` (UI-Detail_View-111), Review: Approved · 2026-11-05 |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-11-05 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 3 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass, no errors |
| `npx eslint` on the spec, `pages/part-detail.page.ts`, `pages/base.page.ts`, `fixtures/data.fixture.ts`, `fixtures/pages.fixture.ts`, `fixtures/index.ts` | Pass, no errors or warnings |
| `npx playwright test <spec> --list` | 1 test listed in project `chromium` |

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-steps: log in, open `QA-<suffix> NoBuy` | (none stated) | Before the steps, line 12 `partDetail.open(part.pk)` | `open` waits for the app shell and the part title (page object) | Covered |
| 1. Check the tabs of the part. | The *Suppliers* tab is not shown (R-Detail_View-23). | `1. Check the tabs of the part.` (line 14) | `await expect(partDetail.tab('Suppliers')).toBeHidden()` (line 17) | Covered |
| (guard) | (not stated) | same step | `await expect(partDetail.tab('Part Details')).toBeVisible()` (line 16) | Extra, justified (Info 1) |

- **Order and titles:** one step, titled `1. <case action>` verbatim. Pass.
- **Prerequisites:** user `allaccess` via `test.use` (line 4) matches; Settings: None, none set; category `data.name('Category')` and part `data.name('NoBuy')` with `purchaseable: false` created through `data` (lines 9-11), matching the case; login through the form by the `user` fixture. Pass. See Info 2 for `description`.
- **Cleanup:** both records created through `data` and removed by it; the step creates nothing through the UI. Pass.
- **Form checks:** not applicable.
- **Absence checks:** the `toBeHidden` on Suppliers is stated by the Expected result, and it runs after the state that would show the tab exists: `open` waits for the part title (part data loaded), and line 16 waits for the part tab list to render. Pass.
- **Traceability:** first-line `// case:` header correct; title `UI-Detail_View-111: The Suppliers tab is hidden for a part that is not Purchaseable` matches; `describe('Part detail header and tab visibility')` matches the case file; tag `@regression` matches Tags: Regression. Pass.
- **Review status:** Approved. Pass.

## C. Conventions

- Layers (UI §1): only fixtures and page objects; no raw locators, API calls, URLs or IDs in the spec. Pass.
- UI §3: one test, one step per case step, assertions in the test, web-first. Pass.
- UI §4: no page object members added for this spec (`pages/part-detail.page.ts` and `pages/base.page.ts` unchanged in git); `tab(name)` delegates to `BasePage.panelTab` (role `tablist` by name, then role `tab`, `exact: true`). Pass.
- UI §5: imports from `fixtures/index.ts`; requests only `partDetail` and `data`. Pass.
- UI §7, §8, §9, §10: no credentials, no sleeps or hidden waits, naming follows the table, panel-tab pattern used. Pass.

No findings in this section.

## D. SOLID and design

- Single responsibility, open/closed, Liskov (`open` uses `BasePage.goto`, keeping the shell wait), interface segregation, dependency inversion: Pass.
- DRY: setup mirrors `ui-detail_view-110.spec.ts`; differs only in name and `purchaseable`. See Info 3.

## E. Playwright and TypeScript practice

- All calls awaited; web-first assertions; no conditionals, loops, `try/catch`, `test.only` or `test.fixme`. Pass.
- Isolation: uses only records it creates. Pass.
- Locators: role with accessible name, exact, scoped to the part tab list. Pass.
- TypeScript: `const` only, no `any`, casts or non-null assertions. Pass.
- Readability: reads like the case; the guard assertion is explained by a comment (line 15). Pass.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | `tests/ui/Detail_View/ui-detail_view-111.spec.ts:16` | Checklist B "Absence checks" / Extra | `expect(partDetail.tab('Part Details')).toBeVisible()` is not stated by the case. It is a deliberate synchronisation guard so that the absence check on line 17 cannot pass before the tab list renders, and it is commented. This strengthens the test rather than adding noise. | None needed. |
| 2 | Info | `tests/ui/Detail_View/ui-detail_view-111.spec.ts:11` | Prerequisites fidelity | `description: partName` is not in the case's Data prerequisite; same pattern as 110 and `ui-rev-001.spec.ts`, likely for create validation. I could not confirm whether 1.5.6 requires it. | None needed; a one-line comment would explain it, or drop it if not required. |
| 3 | Info | `tests/ui/Detail_View/ui-detail_view-111.spec.ts:9-12` | DRY (observation) | Category + part + open setup is repeated in 110 and 111 (and likely 113/114 later). Acceptable at two specs. | If more tab-visibility specs follow, consider a `data` helper for "part in a fresh category"; no change for this spec. |

## Outside scope

- `pages/components/form.component.ts` and `pages/part-form.page.ts` have uncommitted changes; not used by this spec, not reviewed.
