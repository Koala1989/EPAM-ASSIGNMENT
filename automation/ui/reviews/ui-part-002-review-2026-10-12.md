# Review: UI-Part-002 Add Parts dropdown offers create and import options

| Item | Value |
|---|---|
| Spec | `tests/Part/ui-part-002.spec.ts` |
| Case | `test-cases/Part/part-creation-flow.md` (UI-Part-002), Review: Approved (2026-10-11) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-10-12 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 0 Major, 1 Minor, 1 Info |

## A. Automated checks

- `npm run typecheck`: pass.
- `npm run lint`: pass.
- `npx eslint` on the spec, `pages/parts.page.ts`, `pages/base.page.ts`, `pages/components/actions-menu.component.ts`, `pages/components/table.component.ts`, `utils/names.ts`, `fixtures/*.ts`: pass.
- `--list`: listed.

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| 1 Open the Parts view | The parts table is shown with the Add Parts dropdown above it | `1. Open the Parts view` | `partsTable.searchInput` `toBeVisible()` (l.11), `addPartsMenu.button` `toBeVisible()` (l.12) | Covered. The table is checked through its search box (Info 2). |
| 2 Open the Add Parts dropdown | The menu lists Create Part and Import from File | `2. Open the Add Parts dropdown` | `item('Create Part')` and `item('Import from File')` `toBeVisible()` (l.17-18) | Covered |

- **Order and titles:** match the case. Pass.
- **Prerequisites:** `engineer`. No settings or data. Pass.
- **Cleanup:** none needed, no data created. Pass.
- **Traceability:** header, title, describe, tags `@smoke`, `@regression`. Pass.
- **Review status:** Approved. Pass.

## C. Conventions

Passed: §3 (header, steps, assertions in spec, no raw `page.*` locators), §5, §7, §8, §9. Problem: finding 1.

## D. SOLID and design

Passed: one case, depends only on `PartsPage` and its components, minimal fixtures (`partsPage` only).

## E. Playwright and TypeScript practice

Passed: everything awaited, web-first assertions, no conditionals, isolated (read-only), clean TypeScript. Passed every run.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Minor | tests/Part/ui-part-002.spec.ts:16 | §4 (page objects hold every UI action), §3 | The spec performs a UI action itself with `partsPage.addPartsMenu.button.click()` instead of calling a page object method. This is not a lint violation (no `getBy*`), but if the menu needs a different way to open (e.g. hover or keyboard), every spec would have to change. | Add `async open()` to `ActionsMenuComponent` (click the button and wait for the menu, e.g. `getByRole('menu')` visible), and/or `PartsPage.openAddParts()`. Call it here. |
| 2 | Info | tests/Part/ui-part-002.spec.ts:11 | Checklist B | "The parts table is shown" is checked through the table's search box, and "above it" (position) is not checked. This is a reasonable stand-in. | Optional: also assert `partsPage.partsTable.rows` is not empty, since the demo dataset has parts. |

## Outside scope

None beyond those recorded in the UI-Part-001 review.
