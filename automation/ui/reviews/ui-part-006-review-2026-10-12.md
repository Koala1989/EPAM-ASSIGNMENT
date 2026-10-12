# Review: UI-Part-006 Create a part with supplier and manufacturer data from the Supplier Information section

| Item | Value |
|---|---|
| Spec | `tests/Part/ui-part-006.spec.ts` |
| Case | `test-cases/Part/part-creation-flow.md` (UI-Part-006), Review: Approved (2026-10-11) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-10-12 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 2 Major, 4 Minor, 3 Info |

## A. Automated checks

- `npm run typecheck`: pass.
- `npm run lint`: pass.
- `npx eslint` on the spec, `pages/part-detail.page.ts` (including the new members), `pages/part-form.page.ts`, `pages/parts.page.ts`, `pages/base.page.ts`, `pages/components/*.ts`, `fixtures/*.ts`, `utils/*.ts`, `config/env.ts`: pass.
- `--list`: listed.

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-step: as engineer, Parts > Add Parts > Create Part | (none) | outside steps, l.19-22 | `partForm.root` visible | OK |
| 1 Fill Name and Category, leave Purchaseable checked | Supplier Information section is shown | `1. Fill in Name and Category; leave Purchaseable checked` | `flag('purchaseable')` checked (l.26), `supplierSection` visible (l.27) | Covered |
| 2 Enter supplier and manufacturer data | Fields accept the values, no form errors are shown | `2. Enter the supplier and manufacturer data in Supplier Information` | SKU and MPN `toHaveValue` (l.37-38), `invalidFields` count 0 (l.39) | Covered for SKU and MPN. Supplier/Manufacturer selections are not checked in the form, and the form-level error alert is not checked (findings 3, 4). |
| 3 Press Submit | Redirected to the new part's detail page | `3. Press Submit` | `partForm.root` hidden (l.46), `currentPartId()` URL wait (l.47), `title` `toContainText(partName)` (l.48) | Covered |
| 4 As allaccess, open the part and its Suppliers tab | Supplier part (supplier, SKU) listed. Manufacturers section lists the manufacturer part (manufacturer, MPN) | `4. Log out, log in as allaccess, open the new part and its Suppliers tab` | supplier row by SKU `toHaveCount(1)` + `toContainText(supplier)` (l.57-58). Manufacturer row by MPN `toHaveCount(1)` + `toContainText(manufacturer)` (l.61-62), each scoped to its accordion region | Covered. "Listed" is checked by count, not visibility (finding 5). |

- **Order and titles:** match. Pass.
- **Prerequisites:** `engineer` for steps 1-3, `allaccess` for step 4 through `asUser` + `pagesFor` (§5). Both settings are set through `data.setSetting`. Category, supplier company (`is_supplier`) and manufacturer company (`is_manufacturer`, not supplier) come through `data`, with names from `data.name`. **Test data deviates:** SKU and MPN are `QA-QA-<hex>-SKU1` / `QA-QA-<hex>-MPN1`, not the case's `QA-<suffix>-SKU1` (finding 1).
- **Cleanup:** `data.trackPart` (l.15). `TestData.deletePart` removes supplier parts and manufacturer parts (`company/part/`, `company/part/manufacturer/`), sets the part inactive and deletes it. The companies, the category and the settings are then removed or restored in reverse order. This matches the case. Pass.
- **Traceability:** header, title, describe, tags `@regression`, `@cross-functional`, `@settings` match "Regression, Cross-functional, Settings-dependent". Pass.
- **Review status:** Approved. Pass.

## C. Conventions

New page object code (used only by this spec, checked by grep across `tests/`): `PartDetailPage.supplierPartsTable`, `PartDetailPage.manufacturerPartsTable` and the private `accordionSection(name)` helper (`pages/part-detail.page.ts:16-19, 27-28, 42-45`).
- Placement: correct page (the Suppliers tab of the part detail page). It reuses `TableComponent` rather than duplicating table logic. Pass.
- Locator quality: `panel('Suppliers').getByRole('region', { name, exact: true })` is role-first, uses the accessible name, is scoped to the tab panel, and has no CSS, XPath or `nth()`. Pass.
- Naming: nouns in the user's terms. The helper is private, so the public API stays small. JSDoc is present. Pass.
- Waiting and assertions: plain locators, no waits needed and no `expect`. Pass.
- No existing member renamed or changed: the constructor gained two assignments only, and `open`, `openTab`, `detail`, `currentPartId`, `title` are unchanged in behaviour. Pass.

Spec: §3 (no raw locators, assertions in spec), §5 (`pagesFor(await asUser(...))` as documented), §7, §8, §9 pass. Problems: findings 1, 3, 4, 6.

## D. SOLID and design

Passed: SRP (one case; the new locators belong to the page they model), OCP (new members added, nothing special-cased), LSP (`PartDetailPage.open` still goes through `BasePage.goto`), ISP (fixtures requested are all used), DIP (the spec depends on page object members, not on accordion or DOM structure). Info 8 covers a future SRP point. Problem: finding 2 (shared `BasePage.goto` timeout).

## E. Playwright and TypeScript practice

Passed: everything awaited, web-first assertions, no conditionals, the second user's context is closed by the `asUser` fixture, no `any` or `!` in the spec. Run history: one failure in 8 at `allaccess.partDetail.open()` (finding 2). Problem: finding 6 (`let` across steps).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Major | tests/Part/ui-part-006.spec.ts:16-17 | Checklist B (test data from the case), §9 | `data.suffix` already contains the prefix (`qaSuffix()` returns `QA-<8 hex>`, `utils/names.ts:3`), so `` `QA-${data.suffix}-SKU1` `` produces `QA-QA-1A2B3C4D-SKU1`. The case gives `QA-<suffix>-SKU1` / `QA-<suffix>-MPN1`. The assertions still agree with the data the spec used, so coverage holds, but the values differ from the case and from UI-Part-004's (correct) format. | Use `` `${data.suffix}-SKU1` `` / `` `${data.suffix}-MPN1` ``, or better, the shared hex or case-value accessor proposed in the UI-Part-004 review (finding 1), so both specs build case values the same way. |
| 2 | Major | pages/base.page.ts:23 (called from tests/Part/ui-part-006.spec.ts:53) | §8 (stability), Checklist D (LSP contract of `goto`) | `goto` waits for the app shell with the default `expect` timeout (`env.expectTimeout`, 10 s). The first navigation in a fresh `asUser('allaccess')` context loads the full SPA bundle, server info and the user profile cold. Run history shows exactly this timing out once in 8. Any spec that opens a second user's page will see the same thing. | In `BasePage.goto`, give the app-shell check its own longer timeout from `config/env.ts` (e.g. `env.navigationTimeout`, default 30 s): `await expect(this.navigationMenu).toBeVisible({ timeout: env.navigationTimeout })`. This changes *how* `goto` waits, not what it does, so it is within what the healer may do (§11). Do not add retries or sleeps in the spec. |
| 3 | Minor | tests/Part/ui-part-006.spec.ts:37-39 | Checklist B ("no form errors are shown"), consistency with 001/004 | Step 2 checks `invalidFields` but not `partForm.form.formError`, which UI-Part-001 l.23 and UI-Part-004 l.29 both assert for the same Expected-result wording. | Add `await expect(partForm.form.formError).toBeHidden();`. |
| 4 | Minor | tests/Part/ui-part-006.spec.ts:31-38 | Checklist B ("Fields accept the values") | The Supplier and Manufacturer related-field selections are not checked in step 2. Only SKU and MPN are. If either selection failed, step 2 would pass and the failure would show up only in step 4 as a missing row. | Add a `PartFormPage` accessor for a related field's selected value (e.g. `supplierSelection(name)`) and assert the chosen company names in step 2. |
| 5 | Minor | tests/Part/ui-part-006.spec.ts:57, 61 | Checklist B (specificity: "is listed") | `toHaveCount(1)` and `toContainText` both pass on hidden elements. If an accordion section were collapsed, the part would not be "listed" to the user, yet the test would still pass. | Add `await expect(supplierPart).toBeVisible()` and `await expect(manufacturerPart).toBeVisible()` (keep `toHaveCount(1)` for uniqueness). |
| 6 | Minor | tests/Part/ui-part-006.spec.ts:42, 47 | Checklist E (`const` by default, readability) | `let partId = 0` is mutated inside step 3 and read in step 4. A failed step 3 would leave `0`, although Playwright stops the test anyway. | `const partId = await test.step('3. Press Submit', async () => { ...; return partDetail.currentPartId(); });` |
| 7 | Info | tests/Part/ui-part-006.spec.ts:52 | Checklist B | "Log out, log in as allaccess" is done with a second logged-in browser context (`asUser`), not a real logout and login. This is equivalent for what the case checks (what allaccess sees) and matches §5. | None. |
| 8 | Info | pages/part-detail.page.ts:16-19, 42-45 | Checklist D (SRP, future) | The new members are correct and small. If more Suppliers-tab members are added (row actions, add supplier part), `PartDetailPage` will start to model several tabs. | When that happens, move the Suppliers tab into a `components/part-suppliers-panel.component.ts` holding both tables. No change now. |
| 9 | Info | tests/Part/ui-part-006.spec.ts:14 | Checklist B | The manufacturer company is created with `is_supplier: false`, which keeps it out of the Supplier dropdown. This is a good choice that keeps the two related-field searches unambiguous. | None. |

## Outside scope

- `fixtures/data.fixture.ts:19`: the misleading `TestData.suffix` name (it holds `QA-<hex>`), which caused finding 1. See the UI-Part-004 review.
- `pages/part-detail.page.ts:39`: a non-null assertion (`!`) in `currentPartId()`. It is safe after the preceding `toHaveURL`, but a `?.[1]` with an explicit `throw` would be clearer.
- Recorded in the UI-Part-001 review: `PartFormPage` does not extend `BasePage`, `PartsPage.addParts()` does not wait for the form, and the CSS `invalidFields` locator has no comment.
