# Review: UI-Part-003 Add Parts menu is not available without create permission

| Item | Value |
|---|---|
| Spec | `tests/Part/ui-part-003.spec.ts` |
| Case | `test-cases/Part_Creation_and_Import/part-creation-flow.md` (UI-Part-003), Review: Approved (2026-10-11) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-10-12 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 1 Major, 0 Minor, 2 Info |

## A. Automated checks

- `npm run typecheck`: pass.
- `npm run lint`: pass.
- `npx eslint` on the spec and the framework files it uses (`parts.page.ts`, `base.page.ts`, `actions-menu.component.ts`, `table.component.ts`, fixtures): pass.
- `--list`: listed.

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| 1 Open the Parts view | The parts table is shown | `1. Open the Parts view` | `partsTable.searchInput` `toBeVisible()` (l.11) | Covered |
| 2 Look above the parts table for Add Parts | The Add Parts menu is not available | `2. Look above the parts table for the Add Parts dropdown` | `addPartsMenu.button` `toHaveCount(0)` (l.15) | Covered, but the check can pass too early (finding 1) |

- **Order and titles:** match. Pass.
- **Prerequisites:** `test.use({ user: 'reader' })` matches the case. No settings or data. Pass.
- **Cleanup:** none needed. Pass.
- **Traceability:** header, title, describe, tags `@regression`, `@permissions` match "Regression, Permissions". Pass.
- **Review status:** Approved. Pass.

## C. Conventions

Passed: §3, §5, §7, §8, §9. Nothing more to report.

## D. SOLID and design

Passed: one case, page objects only, minimal fixtures.

## E. Playwright and TypeScript practice

Passed: awaited, web-first, no conditionals, isolated, clean TypeScript. Problem: finding 1 (a negative assertion that can pass before the UI is ready).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Major | tests/Part/ui-part-003.spec.ts:15 | Checklist E (web-first assertion that passes without proving anything), §8 | `toHaveCount(0)` passes on its first poll. If the table toolbar that would hold *Add Parts* has not rendered yet, the test passes whether or not the menu would later appear, so a permission regression could go unnoticed. The step-1 check on the search box (l.11, and `PartsPage.open()`) narrows the window, but only if the action buttons render in the same pass as the search box, which nothing in the spec shows. | Before the negative check, assert a positive control in the **same toolbar** that every user sees, e.g. `await expect(partsPage.partsTable.refreshButton).toBeVisible()` (or a page object locator for the toolbar group). Better still, scope `addPartsMenu` to the Parts panel or toolbar so the negative check looks in the right place. Keep `toHaveCount(0)`. |
| 2 | Info | pages/parts.page.ts:20 / pages/components/actions-menu.component.ts:15 | Checklist E (locators) | `addPartsMenu.button` matches the whole page (`page.getByRole('button', { name: 'action-menu-add-parts' })`). A negative check on a wrong locator would always pass. This is covered because UI-Part-002 (l.12) asserts the same locator is visible for `engineer`, so a renamed aria-label would fail 002. | Keep 002 and 003 together in the same runs. No change required. |
| 3 | Info | tests/Part/ui-part-003.spec.ts:4 | Case Notes | The case notes `reader` is "assumed by the seed" to lack create rights. The spec cannot tell "reader lacks permission" apart from "menu missing for everyone"; 002 rules out the second. | None. |

## Outside scope

None beyond those recorded in the UI-Part-001 review.
