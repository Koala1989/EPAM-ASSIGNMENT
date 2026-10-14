# Review: UI-Part-005 Supplier Information section shows only while Purchaseable is checked

| Item | Value |
|---|---|
| Spec | `tests/Part/ui-part-005.spec.ts` |
| Case | `test-cases/Part_Creation_and_Import/part-creation-flow.md` (UI-Part-005), Review: Approved (2026-10-11) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-10-12 |
| Verdict | Approve |
| Findings | 0 Blocker, 0 Major, 0 Minor, 2 Info |

## A. Automated checks

- `npm run typecheck`: pass.
- `npm run lint`: pass.
- `npx eslint` on the spec and the framework files it uses (`parts.page.ts`, `part-form.page.ts`, `form.component.ts`, `actions-menu.component.ts`, `data.fixture.ts`): pass.
- `--list`: listed.

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-step: Parts > Add Parts > Create Part | (none) | outside steps, l.13-16 | `partForm.root` visible | OK |
| 1 Check Purchaseable and the form sections | Purchaseable is checked. Supplier Information shown with Supplier, SKU, Manufacturer, MPN | `1. Check the Purchaseable option and the form sections` | `flag('purchaseable')` `toBeChecked()` (l.19), `supplierSection` visible (l.20), four `supplierField(...)` visible (l.21-24) | Covered |
| 2 Uncheck Purchaseable | Supplier Information no longer shown | `2. Uncheck Purchaseable` | `not.toBeChecked()` (l.29), `supplierSection` `toBeHidden()` (l.30) | Covered |
| 3 Check Purchaseable again | Supplier Information shown again | `3. Check Purchaseable again` | `toBeChecked()` (l.35), `supplierSection` visible (l.36) | Covered |
| Postcondition: close with Cancel | (none) | after steps, l.40-41 | `partForm.root` hidden | OK |

- **Order and titles:** match. Pass.
- **Prerequisites:** `engineer`. `data.setSetting('PART_PURCHASEABLE', true)` and `data.setSetting('PART_CREATE_SUPPLIER', true)` match the case's two settings and are restored by the fixture. No data. Pass.
- **Cleanup:** nothing is created. The form is cancelled as the case requires. Pass.
- **Traceability:** header, title, describe, tags `@regression`, `@settings` (case "Regression, Settings-dependent", §9 tag `@settings`). Pass.
- **Review status:** Approved. Pass.

## C. Conventions

Passed: §3, §4 (`setFlag` uses `setChecked`, which waits for the new state), §5, §7, §8, §9.

## D. SOLID and design

Passed: one case (a state transition), page objects only, fixtures limited to `partsPage`, `partForm`, `data`.

## E. Playwright and TypeScript practice

Passed: awaited, web-first, no conditionals, settings isolated through `data.setSetting` with restore (safe with `workers: 1`), clean TypeScript. Passed every run.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Info | pages/part-form.page.ts:52 / pages/components/form.component.ts:38-40 | §9 (locator names say what the user sees) | `supplierSection` is the section's **header button**, not the section body. "Section shown/hidden" is therefore checked through its header, which is enough here because step 1 also checks the four fields. | Optional: rename to `supplierSectionHeader`, or in step 2 also assert one field (e.g. `supplierField('sku')`) is hidden. |
| 2 | Info | tests/Part/ui-part-005.spec.ts:10-11 | §8 | Global settings are changed. This is safe only with `workers: 1` (set in `playwright.config.ts`). | None. |

## Outside scope

None beyond those recorded in the UI-Part-001 review.
