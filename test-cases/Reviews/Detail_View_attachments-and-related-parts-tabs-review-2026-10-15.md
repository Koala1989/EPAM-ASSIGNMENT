# Review: Attachments and Related Parts tabs (UI), 2026-10-15

**Cases reviewed:** UI-Detail_View-401 to UI-Detail_View-420, UI-Detail_View-501 to UI-Detail_View-516 (36 cases) · **Verdict:** Approve with changes

No case has a Blocker. Four Majors need edits to existing cases, but only to their marking or wording (a `Proposed` label, an `Open:` note, a missing Q-Detail_View-50 marker). None of them changes an outcome a case expects.

## Coverage

`coverage_check.py --area Detail_View --file attachments-tab.md --file related-parts-tab.md`: Rules: 70 · covered: 10 · not cited by any case: 60 · exit code 0 (no unknown rule IDs).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Detail_View-40 | 501-511, 514, 515, 516 | Covered | None. Positive, multiple, self, duplicate, empty, cancel, remove, `reader` and `noaccess` cases all exist. The rule states no permission, so the permission cases rest on Q-Detail_View-54. |
| R-Detail_View-41 | 512, 513, 514 | Covered | None. Both setting states are covered, and so is the toggle. |
| R-Detail_View-42 | 401, 402, 404, 405, 420 | Covered | None. Empty, one, several and isolation cases exist. |
| R-Detail_View-43 | 402, 403, 408, 417, 418, 419, 420 | Covered | None. There are negative cases for no file and for empty or invalid links. |
| R-Detail_View-44 | 406, 407, 408 | Covered | Blocked user: 407 (`noaccess`). See findings 3 and 4 on how the outcomes are worded. |
| R-Detail_View-45 | 409, 410 | Covered | None. |
| R-Detail_View-46 | 409, 411 | Covered | The negative class (non-image) is 411. |
| R-Detail_View-47 | 412 | Covered | None. |
| R-Detail_View-48 | 413 | Covered | None. |
| R-Detail_View-49 | 414, 415, 416 | Covered | None. The rule states no permission (see Questions). |
| R-Detail_View-01 to 39, 50 to 70 | None | Out of scope | These belong to the other Detail_View functionalities: header and tab visibility (01-30), Test Templates tab (31-39) and BOM tab (50-70). |

No gaps. Each functionality has Negative cases (attachments: 407, 408, 411-413, 415-420; related parts: 505-508, 510-512). No rule in scope states a numeric limit, so no boundary cases are needed.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Major | UI-Detail_View-401 | No assumptions | Step 1 states as fact that `engineer` sees the *Add attachment* and *Add external link* buttons. R-Detail_View-43 only says the buttons exist on the tab, not who gets them. Q-Detail_View-50 explicitly asks which permission is needed to add, and whether `engineer` has it. R-Detail_View-43 is also asserted but missing from the Requirement field. | R-Detail_View-43, [concepts-attachments.md#L55](../../requirements/docs/concepts-attachments.md#L55); Q-Detail_View-50 | Edit the case: add `Open: Q-Detail_View-50 (permission needed to add; whether engineer has it)` to step 1, and add R-Detail_View-43 to the Requirement field. |
| 2 | Major | UI-Detail_View-405, 409, 410, 411, 412, 413 | Open-question marking | Each case adds an attachment as `engineer`, so each depends on Q-Detail_View-50 (permission to add, and whether `engineer` has it). 405 is plain `Draft`. 409-413 are marked only with Q-Detail_View-52. Q-Detail_View-50's Affected cases list none of them. | Q-Detail_View-50 | Add Q-Detail_View-50 to their Review field and to Q-Detail_View-50's Affected cases. Alternatively, have the attachment created as `admin` in Data, where the add step is not under test. |
| 3 | Major | UI-Detail_View-406 | Specific Expected results | Step 1 only repeats the rule ("can be downloaded or viewed by a user with the appropriate permissions"). It does not say whether `reader`, the user in the case, can download the file, so the step has no pass/fail outcome. The summary and the technique ("valid class: user with permission") assume that `reader` has the permission. | R-Detail_View-44 ("Which permission is not stated"), [concepts-attachments.md#L34](../../requirements/docs/concepts-attachments.md#L34); Q-Detail_View-51 | Edit step 1 to read `Proposed, to confirm in Q-Detail_View-51: reader can download or view the file.`, followed by the existing Open note. |
| 4 | Major | UI-Detail_View-407 | Rule outcome stated (Proposed written as fact) | Step 1 states "the file is not available to `noaccess`" as a consequence of R-Detail_View-44. The rule does not define the "appropriate permissions", so it does not say that `noaccess` lacks them. This is the Proposed outcome of Q-Detail_View-51, written as fact. Compare UI-Detail_View-511, which labels the same kind of outcome as Proposed. | R-Detail_View-44; Q-Detail_View-51 (Proposed: `noaccess` sees no attachments) | Edit step 1 to read `Proposed, to confirm in Q-Detail_View-51: the file is not available to noaccess.`, followed by the existing Open note. |
| 5 | Minor | UI-Detail_View-408 | Fidelity | The case cites R-Detail_View-44 (download or view of uploaded files), but it tests the add controls. That rule does not cover adding, and citing it inflates R-Detail_View-44's coverage. | R-Detail_View-44, [concepts-attachments.md#L34](../../requirements/docs/concepts-attachments.md#L34) | Remove R-Detail_View-44 from the Requirement field. |
| 6 | Minor | UI-Detail_View-410 | Seed format | Every step asserts `is_image` is true, but the Requirement field cites only R-Detail_View-45. R-Detail_View-46 appears only inside step 1. | R-Detail_View-46, [concepts-attachments.md#L42](../../requirements/docs/concepts-attachments.md#L42) | Add R-Detail_View-46 to the Requirement field. |
| 7 | Minor | UI-Detail_View-409 | Fidelity (less than the rule) | Step 2 checks only the aspect ratio. The rule also says the thumbnail has a reduced image size. | [concepts-attachments.md#L40](../../requirements/docs/concepts-attachments.md#L40) | Add "with a reduced size (smaller than 800x400)" to the step 2 Expected result. |
| 8 | Minor | UI-Detail_View-411 | Specific Expected results | The step 2 action checks the thumbnail and the flag, but the Expected result covers only the flag. The docs say a thumbnail is generated only if the file is a valid image, so "no thumbnail" can be stated. | [concepts-attachments.md#L38](../../requirements/docs/concepts-attachments.md#L38) | Add "No thumbnail is generated" to the step 2 Expected result. |
| 9 | Minor | UI-Detail_View-412 | Seed format (consistency) | The Summary says the corrupt file "is accepted as an attachment". Step 1 leaves acceptance open (Q-Detail_View-52). The two should agree. L43 refers to the attachment record's `is_image`, which supports acceptance. | [concepts-attachments.md#L42-L43](../../requirements/docs/concepts-attachments.md#L42-L43) | Align the Summary and step 1. Either state acceptance in both (citing L42-43), or mark it open in both. |
| 10 | Minor | UI-Detail_View-506 | One behaviour | One case holds two classes: a duplicate in the same direction (A→B again), and a duplicate in the reverse direction (B→A). The step 2 class also depends on the unresolved premise of UI-Detail_View-503 (the relation shows on both parts). | R-Detail_View-40; Q-Detail_View-54 | Consider splitting step 2 into its own case once Q-Detail_View-54 is answered. |
| 11 | Minor | UI-Detail_View-513 | Specific Expected results | The step 1 Expected result says "Related parts can be added", but no step adds one. It also cites R-Detail_View-40, which is not in the Requirement field. | R-Detail_View-40, R-Detail_View-41 | Reword to what is observed (the *Related Parts* table and its add control are shown), and add R-Detail_View-40 to the Requirement field. |

## Duplicates

No case scored 50 or more. None of the 36 cases has a `**Duplicate check:**` line.

## Questions for the architect

1. **Rename permission (UI-Detail_View-414 to 416).** No rule or question covers which permission is needed to *Edit* (rename) an attachment, or whether `engineer` has it. Q-Detail_View-53 asks about the Edit form fields and the name rules, but not about permission. Should Q-Detail_View-53 be extended, or a new question raised? If a permission applies, should there be a `reader` case for the Edit action?
2. **UI-Detail_View-512 / R-Detail_View-41.** The case reads "the feature is disabled" as "related parts are not offered" and states it as fact. This review accepts that reading as the plain meaning of "disabled". Confirm that you agree. The form it takes (hidden tab or a message) is already open in Q-Detail_View-55.
