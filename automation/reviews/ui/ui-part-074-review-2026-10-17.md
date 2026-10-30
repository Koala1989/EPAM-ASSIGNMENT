# Review: UI-Part-074 Create a part with Name only

| Item | Value |
|---|---|
| Spec | `tests/ui/Part/ui-part-074.spec.ts` |
| Case | `test-cases/Part_Creation_and_Import/part-creation-required-fields.md` (UI-Part-074), Review: Approved · Open question: Q-Part-23 |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-10-17 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 1 Major, 2 Minor, 3 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass, no errors |
| `npx eslint` on the spec, `pages/part-form.page.ts`, `pages/part-detail.page.ts`, `pages/parts.page.ts`, `pages/base.page.ts`, `pages/components/{form,actions-menu,select,table}.component.ts`, `fixtures/{index,pages,data,auth,user}.fixture.ts` | Pass, 0 errors, 0 warnings |
| `npx playwright test tests/ui/Part/ui-part-074.spec.ts --list` | 1 test listed: `Part creation with only the required fields › UI-Part-074: Create a part with Name only` |

The spec was reviewed in its current working-tree state (uncommitted changes against `0fd4cea`: describe title, step titles, the step 1 `formError` check and the Q-Part-23 comment).

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-steps | Log in as `engineer`, open *Parts*, open *Add Parts* > *Create Part* | none (lines 11-13, before the steps) | `test.use({ user: 'engineer' })`; `partsPage.open()`, `addParts('Create Part')`, `partForm.waitUntilOpen()` | Covered (setup, see #5 Info) |
| 1. Fill in Name only | The field accepts the value | `1. Fill in Name only. ...` (line 15) | `textField('name')` `toHaveValue(partName)` (line 17) | Covered |
| 1. Fill in Name only | No form error is shown | same | `form.formError` `toHaveCount(0)` (line 18), before *Submit* | Covered in step 2 by the form closing; the step 1 check proves nothing (#1 Major) |
| 2. Press *Submit* | The form closes | `2. Press Submit.` (line 21) | `partForm.root` `toBeHidden()` (line 24) | Covered |
| 2. Press *Submit* | The browser goes to the new part's detail page | same | `partDetail.currentPartId()` (line 23): an `expect(page).toHaveURL(/\/web\/part\/\d+\//)` inside the page object, return value unused | Covered, weakly in this step: any part detail URL passes; "new part" is only proven in step 3 (#2 Minor) |
| 3. Check header and details | Name shows `QA-<suffix> MinPart` | `3. Check the detail page header and details.` (line 27) | `detail('Name')` `toHaveText(partName)` (line 29) | Covered (exact) |
| 3. Check header and details | (header, from the action) | same | `title` `toContainText(partName)` (line 28) | Covered; the case states no exact header text, so `toContainText` is appropriate |
| 3. Check header and details | IPN, Revision and Keywords are not required | same | Proven by the successful create in step 2 with those fields empty | Covered (implicitly) |
| 3. Check header and details | Open: Q-Part-23 (display of empty fields) | same | None, with comment at line 30 | Correctly not asserted (open question) |

Other B checks:
- **Order and titles:** three `test.step`s, in order, titled `<n>. <case action>` matching the case's Action text. Pass.
- **Prerequisites:** user `engineer` matches; Settings None; Data None; pre-steps performed. Pass.
- **Cleanup:** `data.trackPart(data.name('MinPart'))` (line 9) registers the part by name before it is created. Pass.
- **Form checks:** step 1 fills only Name and asserts only Name; untouched fields are not asserted. Pass.
- **Absence checks:** `partForm.root` `toBeHidden()` is stated by the case ("The form closes") and runs after *Submit*. Pass. `formError` `toHaveCount(0)` at line 18 is stated but runs before *Submit*: #1.
- **Traceability:** `// case:` header on line 1 correct; title `UI-Part-074: Create a part with Name only`; describe `Part creation with only the required fields` matches the case file title; tags `@smoke`, `@regression` match Tags. Pass.
- **Review status:** Approved. Pass.

## C. Conventions

Passed: single fixtures import (UI §5); `test.use` user (Shared §4); no raw locators, API calls, URLs, IDs or credentials in the spec (UI §3); test data name through `data.name` (UI §9); assertions only in the spec (UI §3); no `waitForTimeout`/`networkidle`/`force` (UI §8); file and naming conventions (UI §9). No page object or component member is used only by this spec (`waitUntilOpen`, `formError`, `currentPartId`, `textField`, `detail`, `title` are all shared with `ui-part-004`, `ui-part-006` or `ui-xf-001`), so no new framework code to review. Problems: #3.

## D. SOLID and design

Passed: spec tests one case (SRP); requests only the fixtures it uses (`partsPage`, `partForm`, `partDetail`, `data`) (ISP); depends on page objects and fixtures, not DOM or endpoints (DIP); no duplication of page object logic. Problems: #3 (a page object action that does not wait for its own result, pushing the wait into the spec).

## E. Playwright and TypeScript practice

Passed: every call awaited; web-first assertions only; no conditionals, loops, `try/catch`, `test.only` or `test.fixme`; test creates its own data and depends on no demo records; no `any`, casts or non-null assertions; `const` used; reads like the case. Problems: #2 (unused return value used as an implicit assertion).

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Major | `tests/ui/Part/ui-part-074.spec.ts:18` | UI §3 "Assert what the case asks" (absence checks only after the action that would show the element) | `await expect(partForm.form.formError).toHaveCount(0);` runs before *Submit*. InvenTree shows the *Form Error* alert only after a submit, so this passes even if the form would reject Name-only input. It is a check that cannot fail, and the convention calls out this exact pattern. | Remove line 18 and record in step 1 that "no form error" is proven by step 2 (the form closes and the detail page opens), as the earlier version's comment did. If an explicit check is wanted, it belongs after `partForm.submit()`, though `partForm.root` `toBeHidden()` already implies it. Also see Outside scope: the case's wording puts this Expected result in step 1. |
| 2 | Minor | `tests/ui/Part/ui-part-074.spec.ts:23` | UI §3 (each Expected result is at least one `expect` in its step); readability | Step 2's "the browser goes to the new part's detail page" is checked only by `await partDetail.currentPartId();`. The call discards its return value and works as an implicit assertion inside the page object (`toHaveURL(/\/web\/part\/\d+\//)`). Any part detail page passes it, so "new part" is proven only by the title and Name checks in step 3. | Make the step 2 check explicit and specific. For example, move `await expect(partDetail.title).toContainText(partName);` into step 2 after the navigation wait (step 3 keeps the Name detail check). Or compare `currentPartId()` with the pk from `data.findParts(partName)`. |
| 3 | Minor | `pages/parts.page.ts:35-37` (used at spec lines 12-13) | UI §4 "Methods wait for their own result" | `addParts(option)` clicks the menu item but does not wait for the form to open, so the spec has to call `partForm.waitUntilOpen()` itself. A sibling method does wait: `PartDetailPage.addParameter` (part-detail.page.ts:89-92) waits for the form's Submit button. | Not for the generator to change (it changes existing behaviour; architect's decision, UI §11): have `addParts('Create Part')` wait for the form's Submit button, then drop line 13 from specs. |
| 4 | Info | `tests/ui/Part/ui-part-074.spec.ts:28` | Case fidelity | `title` `toContainText(partName)` is appropriate. With no IPN or revision the header is presumably exactly `Part: <name>`, but the case does not state the header text (Q-Part-23 covers empty-field display), so a stricter check would be Extra. | None. |
| 5 | Info | `tests/ui/Part/ui-part-074.spec.ts:11-13` | UI §3 readability | The pre-steps (open Parts, Add Parts > Create Part) run outside any `test.step`, so they appear as loose actions in the report. This is consistent with the case listing them under Prerequisites, not Steps. | Optional: wrap them in `test.step('Pre-steps: open Parts, Add Parts > Create Part', ...)` for a clearer trace. |
| 6 | Info | `tests/ui/Part/ui-part-074.spec.ts:30` | Hard rules (never assume a requirement) | The Q-Part-23 comment correctly leaves the display of empty Category/IPN/Revision/Keywords/Link/Description unasserted until the open question is answered. | Revisit when Q-Part-23 is answered. |

## Outside scope

- **Case wording (for the architect):** UI-Part-074 step 1's Expected result "No form error is shown" can only be observed after *Submit*. Moving it to step 2 ("The form closes without a form error...") would let the spec assert it where it can fail. This is not a reason to block the spec.
- `pages/part-form.page.ts:44`: `PartFormPage` does not extend `BasePage`, although UI §4 says every page object does. A form is arguably a component (`FormComponent` wrapper), so the architect should decide whether to rename it or record an exception in the conventions.
- `pages/part-detail.page.ts:39`: `title = page.getByText(/^Part: /)` is page-wide text matching. It could match any other text node that starts with "Part: ". A header-scoped or role-based locator would be more robust.
