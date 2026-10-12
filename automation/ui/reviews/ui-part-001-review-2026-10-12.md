# Review: UI-Part-001 Create a part with only the required fields

| Item | Value |
|---|---|
| Spec | `tests/Part/ui-part-001.spec.ts` |
| Case | `test-cases/Part/part-creation-flow.md` (UI-Part-001), Review: Approved (2026-10-11) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-10-12 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 0 Major, 3 Minor, 2 Info |

## A. Automated checks

- `npm run typecheck`: pass, no errors.
- `npm run lint`: pass, no errors or warnings.
- `npx eslint` on the spec, `pages/base.page.ts`, `pages/parts.page.ts`, `pages/part-form.page.ts`, `pages/part-detail.page.ts`, `pages/components/*.ts`, `fixtures/*.ts`, `utils/*.ts`, `config/env.ts`: pass.
- `npx playwright test tests/Part --list`: the test is listed as `Part creation flow › UI-Part-001: Create a part with only the required fields`.

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| 1 Open Add Parts, select Create Part | The part creation form opens | `1. Open the Add Parts dropdown above the parts table and select Create Part` | `expect(partForm.root).toBeVisible()` (l.15) | Covered |
| 2 Fill required field and category, leave IPN empty | Fields accept the values, no form errors are shown | `2. Fill in the required field and the category only; leave IPN empty` | name `toHaveValue(partName)` (l.20), IPN `toHaveValue('')` (l.21), `invalidFields` `toHaveCount(0)` (l.22), `formError` `toBeHidden()` (l.23) | Covered. The category value is not checked in the form (finding 3), but step 4 confirms it was saved. |
| 3 Press Submit | The form closes and the browser is redirected to the new part's detail page | `3. Press Submit` | `partForm.root` `toBeHidden()` (l.28). The redirect is checked only by the URL wait inside `partDetail.currentPartId()` (l.29) | Covered. The redirect is checked implicitly (finding 2). |
| 4 Check the part details | Name and category show the values from step 2. IPN is empty. | `4. Check the part details` | Name `toHaveText` (l.33), Category `toContainText` (l.34), IPN row `toHaveCount(0)` (l.36) | Covered. Category is asserted less strictly than it could be (finding 1). IPN is checked by the row being absent (Info 5). |

- **Order and titles:** four steps in case order, titled `<n>. <case action>`. Pass.
- **Prerequisites:** `test.use({ user: 'engineer' })` matches. No settings. Category created through `data.category(data.name('Category'))`. Part name comes from `data.name('Resistor 10k')`. The pre-step (open Parts view) is part of step 1 via `partsPage.open()`. Pass.
- **Cleanup:** `data.trackPart` registers the UI-created part (l.10). Category cleanup comes from `data.category`. Cleanup order is part first, then category, which matches the case. Pass.
- **Traceability:** `// case:` header on line 1, title `UI-Part-001: ...`, describe `Part creation flow`, tags `@smoke`, `@regression` match "Smoke, Regression". Pass.
- **Review status:** Approved. Pass.

## C. Conventions

Passed: §3 single test per case, imports from `fixtures`, no raw locators, no setup logic in the spec. §5 fixtures from `fixtures/index.ts` and only the fixtures the test uses. §7 no hard-coded URLs, IDs or credentials. §8 no sleeps, `networkidle` or `force`. §9 file, title and data names. Problems: findings 2 and 3.

## D. SOLID and design

Passed: the spec tests one case and depends only on page objects and fixtures (DIP). No duplication with page object methods. `PartDetailPage` keeps the `BasePage.goto` contract. See Outside scope for `PartFormPage` not extending `BasePage`.

## E. Playwright and TypeScript practice

Passed: every call is awaited, assertions are web-first, there is no conditional logic, `try/catch`, `test.only` or `fixme`, the test is isolated (its own category, unique names), there is no `any` or `!` in the spec, and `const` is used throughout. Run history: one failure in about 8 runs with the error output lost (Info 4).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Minor | tests/Part/ui-part-001.spec.ts:34 | Checklist B (specificity) | `toContainText(String(category.name))` would also pass for a value such as `Parent/QA-… Category` or one with extra text. The case says Category "shows the value from step 2". The category is top-level with a unique name, so the real risk of a false pass is low. | Use `toHaveText(String(category.name))` if the cell holds exactly the category path (top-level, so path = name). Otherwise add a comment explaining why `toContainText` is needed. |
| 2 | Minor | tests/Part/ui-part-001.spec.ts:29 | §3 (each Expected result is an `expect` in its step) | The redirect to the detail page is checked only by the `toHaveURL` wait inside `PartDetailPage.currentPartId()`, and the returned ID is thrown away. The line looks like an action, not a check, and the spec never shows that the page is the **new** part's page. | Add a spec-level assertion, as UI-Part-006 l.48 does: `await expect(partDetail.title).toContainText(partName)`, keeping `currentPartId()` as the wait. |
| 3 | Minor | tests/Part/ui-part-001.spec.ts:19-23 | Checklist B (Expected result "Fields accept the values") | Name and IPN are checked in the form, but the selected Category is not. If the tree select silently failed, the step would pass and the failure would only show up in step 4. | Add a `PartFormPage` accessor for the category field's displayed value and assert it in step 2. If the tree widget offers no readable value, leave it and note that step 4 covers it. |
| 4 | Info | tests/Part/ui-part-001.spec.ts (whole) | Stability | One failure in about 8 runs, cause unknown. Static reading finds no clear flake source: every wait is web-first and the IPN negative check (l.36) runs after the Name row has rendered (l.33). Possible causes: the modal form re-rendering after server data loads and clearing the typed Name (the same pattern §10 records for the login form), or the category tree option list not having filtered yet when `.first()` is clicked. UI-Part-004 uses the same flow and has not failed, so this is unconfirmed. | Under §11/§12 the spec needs three green runs in a row. Keep the `test-results/` trace from the next failure (`trace: 'retain-on-failure'` is already set) or run `--repeat-each=10` to capture it before changing anything. |
| 5 | Info | tests/Part/ui-part-001.spec.ts:35-36 | Checklist B | "IPN is empty" is asserted as "IPN row absent", which the comment says is how 1.5.6 behaves. This is a negative check, but the same `detail('IPN')` locator is proven positive in UI-Part-004 l.39, so it cannot pass just because the locator is wrong. | None. |

## Outside scope

- `pages/part-form.page.ts:44`: `PartFormPage` does not extend `BasePage`, although §4 says "Every page object extends it". The class wraps `FormComponent` and works as a component, so either make it extend `BasePage` or rename and move it to `components/` (architect's decision).
- `pages/parts.page.ts:35-37`: `addParts()` does not wait for its result (§4 "Methods wait for their own result"). Every spec adds its own `expect(partForm.root).toBeVisible()`. Consider `await this.form().root.waitFor()` or returning the opened `PartFormPage`.
- `pages/components/form.component.ts:25`: `invalidFields` uses the CSS selector `[aria-invalid="true"]` with no comment saying why (§4 requires one for CSS).
