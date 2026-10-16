# Review: UI-Part-074 Create a part with Name only

| Item | Value |
|---|---|
| Spec | `tests/ui/Part/ui-part-074.spec.ts` |
| Case | `test-cases/Part_Creation_and_Import/part-creation-required-fields.md` (UI-Part-074), Review: Approved · Open question: Q-Part-23 |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-10-16 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 0 Major, 3 Minor, 3 Info |

## A. Automated checks

- `npm run typecheck`: pass, no errors.
- `npx eslint tests/ui/Part/ui-part-074.spec.ts pages/part-form.page.ts pages/part-detail.page.ts pages/parts.page.ts pages/base.page.ts pages/components/{form,select,actions-menu,table}.component.ts fixtures/*.ts`: pass, no errors or warnings.
- `npx playwright test tests/ui/Part/ui-part-074.spec.ts --list`: 1 test in `chromium` (`UI-Part-074: Create a part with Name only`), plus the `login-smoke` setup.

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-steps | Log in as engineer, open *Parts*, open *Add Parts* > *Create Part* | Before the steps (lines 11-13) | `test.use({ user: 'engineer' })`; `expect(partForm.root).toBeVisible()` | Covered |
| 1. Fill in Name only, leave the rest empty | The field accepts the value | `1. Fill in Name only. ...` | `textField('name')).toHaveValue(partName)` (l.17) | Covered |
| 1 | No form error is shown | same | `invalidFields).toHaveCount(0)`, `formError).toBeHidden()` (l.24-25) | Covered (see #I2) |
| 1 | (action) Category, IPN, Description, Revision, Keywords, Link left empty | same | `toHaveValue('')` on each (l.18-23) | Extra (verifies the action's precondition; acceptable) |
| 2. Press Submit | The form closes | `2. Press Submit.` | `partForm.root).toBeHidden()` (l.30) | Covered |
| 2 | The browser goes to the new part's detail page | same | `partDetail.currentPartId()` (l.31): a `toHaveURL(/\/web\/part\/\d+\//)` inside the page object, return value discarded | Covered, but implicit and not specific to the new part in this step (#3) |
| 3. Check header and details | Name shows `QA-<suffix> MinPart` | `3. Check the detail page header and details.` | `title).toContainText(partName)`, `detail('Name')).toHaveText(partName)` (l.35-36) | Covered |
| 3 | IPN, Revision and Keywords are not required | same | None explicit; proven by the successful submit in step 2 with those fields empty; comment l.37-38 | Covered (implicitly, #I1) |
| 3 | Open: Q-Part-23 (empty-value display) | same | Not asserted, comment cites Q-Part-23 | Correctly left open |

Other B checks:
- Order and titles: one `test.step` per case step, in order, titled `<n>. <case action>`: pass.
- Prerequisites: user `engineer` matches; Settings None, Data None, so no `data.setSetting`/`data.*` records needed: pass.
- Cleanup: `data.trackPart(data.name('MinPart'))` registered before the part is created (l.9): pass.
- Traceability: first-line `// case:` header correct; title `UI-Part-074: Create a part with Name only` matches; tags `@smoke`, `@regression` match Smoke, Regression. `describe` name differs from the case file title (#2).
- Review status: Approved: pass.

## C. Conventions

- No page object or component members are new for this spec: `textField`, `categoryField`, `form.invalidFields`, `form.formError`, `currentPartId` are already used by `ui-part-004`, `ui-part-006` and `ui-xf-001`; git shows no change to `pages/`.
- Single import from `fixtures`, no raw locators, no `process.env`, no setup logic, no hard-coded URLs, IDs or credentials in the spec: pass.
- Assertions are in the spec; names via `data.name`; naming table (file, title, tags): pass.
- Problems: #1, #2.

## D. SOLID and design

- Spec tests one case; depends only on page objects and fixtures (no DOM, CSS or endpoints); requests only the fixtures it uses (`partsPage`, `partForm`, `partDetail`, `data`): pass.
- No duplication with existing page object methods; no special-casing flags added: pass.
- No problems found in scope.

## E. Playwright and TypeScript practice

- Every call awaited; web-first assertions only; no sleeps, conditionals, loops, `try/catch`, `test.only` or `fixme`: pass.
- No `any`, casts or non-null assertions; `const` used: pass.
- Locators reached through role/label-based page object members: pass.
- Problems: #3 (readability of the discarded `currentPartId()` call).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Minor | `tests/ui/Part/ui-part-074.spec.ts:11-13` | UI §3 (spec reads like the case) | The case's Pre-steps (open *Parts*, *Add Parts* > *Create Part*) run as bare statements before step 1. Acceptable since the case lists them as Pre-steps, not steps, but they are invisible in the HTML report/trace. | Optionally wrap them in `test.step('Pre-steps: open Add Parts > Create Part', ...)` so a failure there is labelled. |
| 2 | Minor | `tests/ui/Part/ui-part-074.spec.ts:6` | UI §3 (`test.describe` per functionality, the case file's title) | `describe('Part creation: required fields')` does not match the case file title "Part creation with only the required fields". | Rename to `test.describe('Part creation with only the required fields', ...)`. |
| 3 | Minor | `tests/ui/Part/ui-part-074.spec.ts:31` | UI §3 (each Expected result is an `expect` in its step) | "Goes to the new part's detail page" is only checked by the `toHaveURL` wait inside `PartDetailPage.currentPartId()`, whose return value is discarded; nothing in step 2 shows it is the *new* part's page (that is only proven in step 3 by the Name). | In step 2 add a spec-level assertion tying the page to the new part, e.g. `await expect(partDetail.title).toContainText(partName)` after the URL wait, or keep the ID (`const partId = await partDetail.currentPartId()`) and compare it with `(await data.findParts(partName))[0].pk`. |
| I1 | Info | `tests/ui/Part/ui-part-074.spec.ts:37-38` | Case step 3 | "IPN, Revision and Keywords are not required" has no explicit assertion; it is proven by the part being created with them empty. Reasonable given Q-Part-23 is open; the comment explains it. | None. |
| I2 | Info | `tests/ui/Part/ui-part-074.spec.ts:24-25` | Case step 1 | The no-error checks run before Submit, when InvenTree shows field errors only after a submit attempt, so they are close to trivially true. The form closing in step 2 is the stronger evidence. | None required; optionally note it in a comment. |
| I3 | Info | `tests/ui/Part/ui-part-074.spec.ts:18-23` | B (Extra) | Asserting each untouched field is empty is not an Expected result; it verifies the step's action and does no harm. | None. |

## Outside scope

- `pages/parts.page.ts:35-37` `addParts()` does not wait for the form it opens (UI §4 "methods wait for their own result"); specs compensate with `expect(partForm.root).toBeVisible()`. `PartFormPage.waitUntilOpen()` exists but is not used by `addParts`.
- `pages/components/form.component.ts:27` `invalidFields` uses a CSS attribute locator without the explanatory comment UI §4 asks for.
- `pages/part-detail.page.ts:53-58` `currentPartId()` and `expectOpen()` wrap `expect(...).toHaveURL` in a page object; acceptable as a wait, but `expectOpen` is named like an assertion.
