# Review: UI-Part-004 Create a part with optional IPN, Keywords and Link filled

| Item | Value |
|---|---|
| Spec | `tests/Part/ui-part-004.spec.ts` |
| Case | `test-cases/Part/part-creation-flow.md` (UI-Part-004), Review: Approved (2026-10-11) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-10-12 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 0 Major, 3 Minor, 1 Info |

## A. Automated checks

- `npm run typecheck`: pass.
- `npm run lint`: pass.
- `npx eslint` on the spec and the framework files it uses (`parts.page.ts`, `part-form.page.ts`, `part-detail.page.ts`, `base.page.ts`, components, fixtures, utils): pass.
- `--list`: listed.

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-step: open Parts, Add Parts > Create Part | (none) | outside steps, l.17-20 | `partForm.root` `toBeVisible()` (l.20) | OK (pre-steps are not case steps) |
| 1 Fill in Name, Category and optional fields | Fields accept the values, no form errors are shown | `1. Fill in Name, Category and the optional fields` | `toHaveValue` for name, IPN, keywords, link (l.24-27), `invalidFields` count 0 (l.28), `formError` hidden (l.29) | Covered for the text fields. Category acceptance is not checked anywhere (finding 3). |
| 2 Press Submit | The browser is redirected to the new part's detail page | `2. Press Submit` | `partForm.root` hidden (l.34). Redirect only via the URL wait in `currentPartId()` (l.35) | Covered implicitly (finding 2) |
| 3 Check the part details | IPN, Keywords and Link show the values from step 1 | `3. Check the part details` | `toHaveText` exact for IPN, Keywords, Link (l.39-41) | Covered |

- **Order and titles:** match. Pass.
- **Prerequisites:** `engineer`. No settings. Category through `data.category`. Name through `data.name`. Test data values match the case formats (`QA-<suffix>-IPN1`, `qa<suffix>cap ceramic`, `https://example.com/datasheet`), with `<suffix>` correctly taken as the 8 hex digits. Pass.
- **Cleanup:** `data.trackPart` (l.10) and the category cleanup. Pass.
- **Traceability:** header, title, describe, tag `@regression` matches "Regression". Pass.
- **Review status:** Approved. Pass.

## C. Conventions

Passed: §3 (no raw locators, assertions in spec, pre-steps kept outside the numbered steps), §5, §7, §8, §9. Problems: findings 1 and 2.

## D. SOLID and design

Passed: one case, page objects and fixtures only. Problem: finding 1 (parsing a framework value in the spec).

## E. Playwright and TypeScript practice

Passed: awaited, web-first, exact `toHaveText` on the detail values, no conditionals, isolated, `const` throughout, no `any` or `!`. Passed every run.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Minor | tests/Part/ui-part-004.spec.ts:11-12 | Checklist D (DIP, DRY), Checklist E (readability) | The spec works out the case's `<suffix>` by parsing the generated name: `partName.split(' ')[0].replace('QA-', '')`. This ties the spec to the format of `qaName`. The parse is correct, because `TestData.suffix` already contains `QA-` (see Outside scope), but UI-Part-006 solves the same problem differently, and wrongly. | Add one accessor to `TestData` (e.g. `data.hex` returning the 8 hex digits, or `data.caseValue('IPN1')` returning `QA-<hex>-IPN1`) and use it in 004 and 006. |
| 2 | Minor | tests/Part/ui-part-004.spec.ts:35 | §3 (each Expected result is an `expect` in its step) | As in UI-Part-001: the redirect is checked only by the wait inside `currentPartId()`, and the returned value is thrown away. | Add `await expect(partDetail.title).toContainText(partName)` in step 2. |
| 3 | Minor | tests/Part/ui-part-004.spec.ts:23-29, 38-42 | Checklist B ("Fields accept the values") | Category is filled but checked neither in the form (step 1) nor on the detail page. The case's step 3 lists only IPN, Keywords and Link, so step 1 is the only place where category acceptance is expected. | Assert the selected category in step 1 through a `PartFormPage` accessor, or at least `await expect(partDetail.detail('Category')).toHaveText(String(category.name))` in step 3, marked as supporting evidence for step 1. |
| 4 | Info | tests/Part/ui-part-004.spec.ts:15 | Checklist E | `link` is a fixed string, which is correct because the case gives a fixed value. | None. |

## Outside scope

- `fixtures/data.fixture.ts:19` + `utils/names.ts:3`: `TestData.suffix` is `QA-<8 hex>`, not the 8-hex `<suffix>` the manual cases use. The name invites the mistake made in UI-Part-006 (`QA-${data.suffix}` → `QA-QA-…`). Rename it (e.g. `prefix`), or add a separate hex accessor (architect's decision, since it changes an existing member).
