# Review: Open a part from the category list and the category breadcrumb (UI), 2026-10-14

**Cases reviewed:** UI-Categories-001, UI-Categories-002, UI-Categories-003, UI-Categories-004, UI-Categories-005, UI-Categories-006, UI-Categories-007 · **Verdict:** Changes required

## Coverage

`python tools/coverage_check.py --area Categories --file test-cases/Categories/open-part-from-category-list-and-breadcrumb.md`: Rules: 7 · covered: 4 · not cited by any case: 3 (R-Categories-01, R-Categories-03, R-Categories-04). Exit code 0: no case cites an unknown rule ID.

| Rule | Cases | Gap / Out of scope / Covered | Depth issues |
|---|---|---|---|
| R-Categories-01 (hierarchical categories, organise and filter) | none | Out of scope: general description of the category hierarchy; belongs to category hierarchy management (Not in docs item 5), not to opening a part. | None |
| R-Categories-02 (list shows parts of the category and all sub-categories) | 002, 007 | Covered (supporting rule here) | None for this functionality. Only one level of nesting is exercised; "all its sub-categories" at deeper levels belongs to a category-list functionality. |
| R-Categories-03 (category shows its sub-categories) | none | Out of scope: sub-category list functionality. Note UI-Categories-002 step 1 asserts it without citing it (finding 4). | None |
| R-Categories-04 (list columns: name, description, thumbnail, category, stock) | none | Out of scope: category part list content functionality. | None |
| R-Categories-05 (user-configurable filters) | 004 | Covered (supporting rule here) | Filters are not named in the docs; see finding 3. |
| R-Categories-06 (clicking the part name opens Part Detail) | 001, 002, 003, 004, 006, 007 | Covered | None: the rule states no limit, "must", "only" or permission condition, so no boundary, negative or blocked-user case is required. |
| R-Categories-07 (part's categories in the top navigation bar) | 005, 006, 007 | Covered, depends on Q-Categories-01 and Q-Categories-02 | None required by the rule. |

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | UI-Categories-003 | No assumptions / Fidelity | Step 2 Expected result "The create and edit controls are hidden for this user." is not stated by R-Categories-06 or any doc line; it comes from the seed's demo-user table, which is not a requirement. The case's own Notes admit "the docs state no permission condition for opening a part". It is also vague (which controls). | R-Categories-06, [part-index.md#L46](../../requirements/docs/part-index.md#L46); seed "Demo users" table | Remove the assertion, or raise an open question on what a view-only user sees on the Part Detail view and mark the case `Draft · Open question: Q-Categories-NN` with the unknown part marked. |
| 2 | Major | UI-Categories-006 | Open-question marking | Step 1 Expected result adds "Expected by the architect's request: the category page opens." after the `Not known` marker. The request is not a requirement source; an unknown outcome must be left as `Not known: depends on open question ...` only. | R-Categories-07, [part-views.md#L17-L21](../../requirements/docs/part-views.md#L17-L21); Q-Categories-02 is Open | Delete the "Expected by the architect's request" sentence, or answer Q-Categories-02 and update the step. |
| 3 | Major | UI-Categories-004 | No assumptions / Open-question marking | Step 1 relies on a filter on the active state ("active parts only") and expects the list to show only Part A. The docs do not name any filter (index Not in docs item 6), and do not say whether an inactive part is listed by default. The case hedges in text but is not linked to an open question and is marked plain `Draft`. | R-Categories-05, [part-index.md#L44](../../requirements/docs/part-index.md#L44); index Not in docs item 6 | Raise an open question on which filters the category part list offers (and whether inactive parts are listed by default), add it to the Review field, and mark the filter in Test data as `[open: Q-Categories-NN, ...]`. Alternatively drop R-Categories-05 from this case. |
| 4 | Minor | UI-Categories-002 | Fidelity / Requirement | Step 1 asserts "The sub-category list shows `QA-<suffix> Child`", which is R-Categories-03, not cited in the Requirement field. | R-Categories-03, [part-index.md#L33](../../requirements/docs/part-index.md#L33) | Cite R-Categories-03 or drop that sentence. |
| 5 | Minor | UI-Categories-001, 002, 004, 005, 006, 007 | User | `engineer` is used for actions that need only view access; `reader` is the least-privileged demo user that can open a part (as UI-Categories-003 shows). The seed names `engineer` as the Parts UI default, so this conflicts with the "least-privileged" rule. | Seed Prerequisites field ("least-privileged that can do the action") | Architect to decide which convention applies; switch to `reader` if least-privilege wins. |
| 6 | Minor | UI-Categories-002 | Technique | "State transition (parent list, then detail view)" labels page navigation, not a state change of the part; the case is an equivalence class case. | Seed Technique field | Drop the State transition label. |
| 7 | Minor | UI-Categories-006 | Open-question marking (cell) | Step 1 Test data names the breadcrumb entry `QA-<suffix> Parent`, but Q-Categories-01 asks what label each entry carries; UI-Categories-007 correctly marks the equivalent cell `[open: Q-Categories-01, ...]`. | Q-Categories-01 | Mark the cell `[open: Q-Categories-01, label of the entry]`. |
| 8 | Minor | UI-Categories-005, UI-Categories-006 | Priority / Tags | `Smoke` (and P1 on 006) on cases whose expected outcome depends on Open questions and on an L-risk rule (R-Categories-07). A smoke case should not have unknown expected results. | Inventory R-Categories-07 risk L; seed Tags and Priority | Consider `Regression` only and P2/P3 until the questions are answered. |
| 9 | Minor | UI-Categories-004 | Postconditions | Cleanup says "set the parts inactive", but Part C is created inactive. | Prerequisites of the case | Wording only. |

## Duplicates

No case scored 50 or more (no case carries a `**Duplicate check:**` line). For information: UI-Categories-006 and UI-Categories-007 differ in starting state (part directly in the category vs in a sub-category, direct vs ancestor breadcrumb entry); UI-Categories-001 and UI-Categories-003 differ in user (`engineer` vs `reader`).

## Questions for the architect

1. UI-Categories-001 step 2 expects the URL `/web/part/<pk>/`. The docs do not state the URL; the pattern comes from the seed's worked example. Is the seed an accepted source for the URL pattern, or should it be an open question?
2. Should there be a case for `noaccess` (no permissions) trying to open a category or part? No inventoried rule states a permission condition for viewing parts, so this review does not count it as a gap.
3. Does a part in a grandchild category (two levels down) belong in this functionality (R-Categories-02, "all its sub-categories"), or in a separate category-list functionality?
