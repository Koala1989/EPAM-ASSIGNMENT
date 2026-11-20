# Review: UI-Detail_View-088 The Variants tab is hidden for a part that is not a template

| Item | Value |
|---|---|
| Spec | `tests/ui/Detail_View/ui-detail_view-088.spec.ts` |
| Case | `test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md` (UI-Detail_View-088), Review: Approved · 2026-11-05 |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-11-05 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 1 Major, 1 Minor, 1 Info |

## A. Automated checks

- `npm run typecheck`: pass.
- `npx eslint tests/ui/Detail_View/ui-detail_view-088.spec.ts pages/part-detail.page.ts pages/base.page.ts fixtures/data.fixture.ts fixtures/pages.fixture.ts fixtures/index.ts`: 0 errors, 1 warning:
  - `ui-detail_view-088.spec.ts:15:50` `playwright/no-useless-not`: "Unexpected usage of not.toBeVisible(). Use toBeHidden() instead" (finding 2).
- `npx playwright test tests/ui/Detail_View/ui-detail_view-088.spec.ts --list`: 1 test listed.

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| 1. Check the tabs of the part. | The *Variants* tab is not shown (visible only for Template parts, R-Detail_View-08). | `1. Check the tabs of the part.` (line 14) | `expect(partDetail.tab('Variants')).not.toBeVisible()` (line 15) | Covered, but the absence check is not anchored on the tab list having rendered (finding 1) |

- Order and titles: one step, titled `1. <case action>` verbatim. Pass.
- Prerequisites: user `engineer` (line 4) matches; Settings: None, none set; category and part created through `data` with `data.name` names (lines 9-11), part with `is_template: false` explicitly; pre-step "open the part" done before the step with `partDetail.open(part.pk)` (line 12); login through the form via the `user` fixture. Pass.
- Cleanup: no records created through the UI; `data.category`/`data.part` register their own cleanup. Pass.
- Form checks: not applicable (no form).
- Absence check: the case states it; it runs after the page is opened, but `open()` only waits for the header text (finding 1).
- Traceability: `// case:` header on line 1, title `UI-Detail_View-088: <case title>` matches, `describe` is the case file's title, tag `@regression` matches Tags "Regression". Pass.
- Review status: Approved. Pass.

## C. Conventions

No new page object or component members: `PartDetailPage.open` and `tab` (via `BasePage.panelTab`) already exist and are used by other specs. Import from `fixtures` (UI §5), no raw locators or API calls in the spec (UI §1, UI §3), no hard-coded URLs, IDs or credentials, fixtures requested are only the ones used, naming per UI §9: all pass. Problems: findings 1, 2.

## D. SOLID and design

Single responsibility (one case, one test), open/closed (no special-casing of existing methods), Liskov (`open` goes through `BasePage.goto`), interface segregation (`partDetail`, `data` only), dependency inversion (no DOM or endpoints in the spec), no duplication: all pass.

## E. Playwright and TypeScript practice

All calls awaited, web-first assertion, no conditionals, loops, `try/catch`, `test.only` or `fixme`, isolated data, role-based locator with exact name, no `any`, casts or `!`, `const` throughout: all pass. Problem: finding 1 (false-pass risk).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Major | `tests/ui/Detail_View/ui-detail_view-088.spec.ts:15` (with `pages/part-detail.page.ts:60-63`) | UI §3 "Assert that something is hidden ... only after the action that would show it"; E. false pass | The only check is an absence check. `partDetail.open()` waits for `getByText(/^Part: /)` only, not for the `panel-tabs-part` tab list. If the tab list has not rendered yet (or renders tabs in stages), `not.toBeVisible()` passes immediately, so the test would also pass for a part whose Variants tab is wrongly shown. The sibling spec `ui-detail_view-111.spec.ts:16-17` anchors the same kind of check with a positive tab assertion first. | Before line 15, assert a tab that is always present so the tab list for this part is proven rendered, e.g. `await expect(partDetail.tab('Part Details')).toBeVisible();`, then check Variants. (Optionally also `await expect(partDetail.title).toContainText(partName)` to prove this part's data is loaded.) |
| 2 | Minor | `tests/ui/Detail_View/ui-detail_view-088.spec.ts:15` | UI §12 lint (`playwright/no-useless-not` warning) | `not.toBeVisible()` is flagged by lint; the rest of the suite uses `toBeHidden()`. | Use `await expect(partDetail.tab('Variants')).toBeHidden();`. |
| 3 | Info | `tests/ui/Detail_View/ui-detail_view-088.spec.ts:11` | B. Prerequisites | `description: partName` is not stated by the case; harmless setup detail (presumably to satisfy the API), not asserted. | None needed. |

## Outside scope

- `pages/part-detail.page.ts:60-63`: `open()` waits only for a header text matching `/^Part: /`, not for the panel tab list. Any spec that checks tab absence right after `open()` has the same false-pass risk as finding 1; making `open()` also wait for the `panel-tabs-part` tab list would fix it once for all callers (architect's decision, since it changes an existing method's behaviour).
