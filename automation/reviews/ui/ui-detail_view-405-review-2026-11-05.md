# Review: UI-Detail_View-405 Attachments of one part are not listed on another part

| Item | Value |
|---|---|
| Spec | `tests/ui/Detail_View/ui-detail_view-405.spec.ts` |
| Case | `test-cases/Part_Detail_View/attachments-tab.md` (UI-Detail_View-405), Review: Approved (2026-11-05, bulk approval) |
| Reviewer | playwright-test-reviewer (Opus 5.5), 2026-11-05 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 0 Major, 6 Minor, 3 Info |

## A. Automated checks

- `npm run typecheck`: pass, no errors.
- `npx eslint` on the spec, `pages/part-detail.page.ts`, `pages/base.page.ts`, `pages/components/form.component.ts`, `pages/components/table.component.ts`, `fixtures/index.ts`, `fixtures/data.fixture.ts`, `fixtures/pages.fixture.ts`, `utils/names.ts`: pass, no errors or warnings.
- `npx playwright test <spec> --list`: 1 test in 1 file (`[chromium] ... UI-Detail_View-405: ...`).

## B. Case coverage

| Case step | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|
| Pre-steps | Log in as `engineer`, open part A's *Attachments* tab | (before steps, lines 13-15) | `open` and `openTab` wait for the title and the panel | Covered |
| 1. Upload the file to part A with *Add attachment* (file `QA-<suffix>-datasheet.pdf`) | The file is listed on part A | `1. Upload the file to part A with Add attachment.` (17-22) | line 19 `attachmentFileField` `toContainText(fileName)` (field the step fills); line 21 `attachmentLink(fileName)` `toBeVisible()` inside the Attachments panel, exact name | Covered |
| 2. Open part B and its *Attachments* tab | The tab shows part B's attachments only; the file of part A is not listed | `2. Open part B and its Attachments tab.` (24-29) | line 27 `noAttachmentsMessage` `toBeVisible()` (part B has none, so "B only" = empty table; also proves the table loaded); line 28 `attachmentLink(fileName)` `toBeHidden()` after the table loaded | Covered |

- Order and titles: two steps, in case order, titled `<n>. <case action>`. Pass.
- Prerequisites: user `engineer` via `test.use` (line 4) matches the case; settings: none, none set; data: parts A and B via `data.part(data.name('Attach A' / 'Attach B'))` (lines 9-10); file name `QA-<suffix>-datasheet.pdf` (line 11) matches the case's test data; pre-steps done (lines 14-15). Pass.
- Cleanup: parts are removed by `data`; the attachment created in step 1 is not removed explicitly although the case's Postconditions say "delete part A's attachment" (finding 3).
- Form checks: step 1 fills only the file field, and it is asserted (line 19). Pass.
- Absence checks: the one `toBeHidden` (line 28) is stated by the Expected result and runs after the tab opened and its empty state rendered (line 27). Pass.
- Traceability: `// case:` header on line 1, title `UI-Detail_View-405: <case title>`, `describe('Attachments tab')` matches the case file's functionality, tag `@regression` matches Tags "Regression". Pass.
- Review status: Approved. Pass.

## C. Conventions

New page object code used only by this spec (Grep across `tests/ui/`): `PartDetailPage.attachmentsTable`, `noAttachmentsMessage`, `addAttachmentButton`, `attachmentFileField`, `attachmentLink()`, `addAttachment()`. All are additions; no existing member was renamed or changed.

- Layer boundaries (UI §1): spec uses only fixtures and page objects; no raw locators, API calls, URLs or credentials. Pass.
- Import from `fixtures/index.ts`, `test.use({ user })` (UI §5). Pass.
- Assertions only in the spec; page object methods wait (`toBeVisible` on the file field) but assert no business outcome (UI §4). Pass.
- Locator priority (UI §4): `getByRole` with aria-label names (`action-button-add-attachment`, `file-field-attachment`), link by exact name, `getByText` for the empty-state message; all scoped to the Attachments panel or the dialog. Pass.
- Placement: attachments members on `PartDetailPage`, consistent with the existing Parameters and Stock tab members. Pass.
- Waiting (UI §8): no sleeps, `networkidle` or `force`; file chooser promise set up before the click. Pass.
- Naming (UI §9): locator nouns, verb methods in the UI's words. Pass, see finding 5 on `addAttachment`.
- Problems: findings 1, 2, 4, 5, 6.

## D. SOLID and design

- Single responsibility: the spec tests one case; `addAttachment` does one action (open form, choose file). Pass.
- Open/closed: behaviour added through new members, no flags on existing methods. Pass.
- Liskov: `open()` still goes through `BasePage.goto` (waits for the app shell). Pass.
- Interface segregation: spec requests only `partDetail` and `data`. The page object gains an unused member (finding 4).
- Dependency inversion: spec does not know DOM structure or endpoints. Pass.
- Problems: findings 4, 8.

## E. Playwright and TypeScript practice

- Every call awaited; the `filechooser` promise is created before the click and awaited after it. Pass.
- Web-first assertions only; no polling, conditionals, loops, `try/catch`, `test.only` or `test.fixme`. Pass.
- Isolation: both parts and the file name are unique per test; no demo data used. Pass.
- TypeScript: no `any`, no `!`, `const` throughout. `Number(partA.pk)` matches the pattern of other specs. Pass.
- Problems: findings 1, 2.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Minor | `tests/ui/Detail_View/ui-detail_view-405.spec.ts:11` | UI §3 (tests read like the case), UI §6 | The file name is built in the spec with string manipulation: `` `${data.name('datasheet')}.pdf`.replace(/ /g, '-') ``. This is a hidden formatting rule (the `QA-<suffix> <label>` form becomes `QA-<suffix>-<label>`) that every attachment spec will repeat. | Add a `data.fileName('datasheet', 'pdf')` (or a `utils/names.ts` helper) that returns `QA-<suffix>-datasheet.pdf`, and use it here. Fixture changes are the architect's decision. |
| 2 | Minor | `tests/ui/Detail_View/ui-detail_view-405.spec.ts:18` | Readability (magic strings) | `'%PDF-1.4 QA'` is a magic file content with no explanation; the case states only the file name. | Name it (`const pdfContent = '%PDF-1.4 QA'; // minimal PDF header, content not under test`) or let `addAttachment` default the content. |
| 3 | Minor | `tests/ui/Detail_View/ui-detail_view-405.spec.ts:20-21` | Review checklist B (cleanup), case Postconditions | The attachment created through the UI is not registered or removed; the case's cleanup says "delete part A's attachment". Cleanup relies on InvenTree deleting a part's attachments with the part, which this review could not verify (no tracker for attachments exists in `data`). If it does not cascade, every run leaves an orphan attachment and an uploaded file. | Confirm the cascade in 1.5.6; if it does not cascade, add `data.trackAttachment(...)` (architect) and register the attachment after step 1. |
| 4 | Minor | `pages/part-detail.page.ts:33,43` | UI §4, interface segregation | `attachmentsTable` is added but used by no spec (Grep across `tests/ui/`); an unused member added for this spec. | Remove it until a spec needs it, or keep it only if UI-Detail_View-401/404 will use it soon. |
| 5 | Minor | `pages/part-detail.page.ts:119` | UI §4 (methods are user intentions), UI §9 | `addAttachment(fileName, content)` opens the form and chooses a file but does not submit, while its name reads like the whole action "add an attachment". The spec then calls `partDetail.form().submit()` separately (line 20), which is fine for the case (it asserts the chosen file before submitting), but the name invites misuse. | Rename for new code to `chooseAttachment(...)` / `openAddAttachment(...)` + `chooseFile(...)`, or keep the name and rely on the doc comment; the generator may not rename after merge (UI §11), so decide before committing. |
| 6 | Minor | `pages/part-detail.page.ts:124` | Open/closed, UI §4 | `mimeType: 'application/pdf'` is hard-coded while `fileName` is a parameter, so a future `.png` upload (thumbnail cases, Q-Detail_View-52) would be sent as PDF. | Derive the MIME type from the extension or take it as an optional parameter with `application/pdf` as default. |
| 7 | Info | `tests/ui/Detail_View/ui-detail_view-405.spec.ts:27` | Case fidelity | `'No attachments found'` (`part-detail.page.ts:44`) is the observed empty-state text; the empty-state wording is an open question in sibling cases (Q-Detail_View-50). It is a reasonable, specific way to assert "part B's attachments only" (B has none) and it synchronises the absence check on line 28. No change needed; if the architect answers Q-Detail_View-50 differently, update the page object. |
| 8 | Info | `pages/part-detail.page.ts` | Single responsibility | `PartDetailPage` now holds members for the Suppliers, Parameters, Stock and Attachments tabs. Each tab is a widget of its own; an `AttachmentsPanelComponent` (and similar per tab) would keep the class from growing with every Detail_View case. Existing pattern, not introduced by this spec. | Consider extracting tab components when the attachment cases 401-406 are automated. |
| 9 | Info | `tests/ui/Detail_View/ui-detail_view-405.spec.ts:9-10` | Case fidelity | The parts get a `description` the case does not state. Harmless (needed or not by `data.part`), but not asked for. | None required. |

## Outside scope

- `pages/part-form.page.ts` (`duplicateSection`, `closeDropdown`) and `pages/components/form.component.ts` (`dismissDropdown`) have uncommitted additions not used by this spec; not reviewed here.
- `fixtures/data.fixture.ts` has no way to register attachments (`deletePart` removes stock, supplier and manufacturer parts only); the attachment cases (UI-Detail_View-402 to 406) will all depend on part deletion cascading to attachments.
