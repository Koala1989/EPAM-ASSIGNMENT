# Review: Test templates tab (UI), 2026-10-15

**Cases reviewed:** UI-Detail_View-301 to UI-Detail_View-341 (41 cases, `test-cases/Part_Detail_View/test-templates-tab.md`) · **Verdict:** Changes required

## Coverage

`python tools/coverage_check.py --area Detail_View --area Part_Template --file test-cases/Part_Detail_View/test-templates-tab.md`: Rules: 81 · covered: 11 · not cited by any case: 70 · exit 0 (no unknown rule IDs).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Detail_View-29 | 301, 302, 328, 334, 335, 336, 337, 338, 339 | Covered | None. No permission rule exists; 337 to 339 rest on Q-Detail_View-45. |
| R-Detail_View-31 | 310, 311, 312, 313, 314, 316, 340, 341 | Covered | Negative (310) and cross-variant (313) present. 341 cites it wrongly (finding 1). |
| R-Detail_View-32 | 302, 304-309, 311, 314, 315, 329 | Covered | None. |
| R-Detail_View-33 | 304, 305, 306, 307 | Covered | All four doc examples present. |
| R-Detail_View-34 | 303, 317 | Covered | None. |
| R-Detail_View-35 | 303, 318 | Covered | None (effect on a stock item open in Q-Detail_View-47). |
| R-Detail_View-36 | 303, 319, 320 | Covered | Negative (319) and positive (320) present. |
| R-Detail_View-37 | 303, 321, 322 | Covered | Negative (321) and positive (322) present. |
| R-Detail_View-38 | 303, 323, 324 | Covered | None. |
| R-Detail_View-39 | 325, 326, 327, 329 | Covered | 326 tests the rule; 329 cites it wrongly (finding 4). |
| R-Part_Template-08 | 313, 330, 331, 332, 333 | Covered | Both clauses (variants, their stock items) present. |
| R-Detail_View-30 | None | Out of scope | Test Results tab: functionality "Return Orders, Transfer Orders and Test Results tab visibility". |
| R-Detail_View-01 to 28, 40 to 70 | None | Out of scope | Header, other tabs, related parts, attachments, BOM functionalities of Detail_View. |
| R-Part_Template-01 to 07, 09 to 11 | None | Out of scope | Template/variant creation, serials, stock, inherited BOM (Templates_and_Variants functionalities). |

No gaps: every rule of this functionality is cited, Negative cases exist, and no in-scope rule states a numeric limit.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | UI-Detail_View-341 | Fidelity (wrong rule) | The only rule cited, R-Detail_View-31 (name unique for a part), has nothing to do with editing a template another user has deleted. Coverage for R-Detail_View-31 is overstated by this case. | R-Detail_View-31; part-test.md#L27 | Edit the Requirement: no rule covers the stale edit; cite the closest rule (R-Detail_View-29) or mark it as error guessing tied to Q-Detail_View-48 only. |
| 2 | Major | UI-Detail_View-305, 306, 307, 309, 311, 312, 313, 315, 316, 324, 327, 329, 341 | Open-question marking | Steps reference `Open: Q-Detail_View-45` (step 1 and/or step 2 text), but the Review field omits Q-Detail_View-45. Q-Detail_View-45's Affected cases list also omits these cases. | Each case's step 1/2 vs its Review line; open-question_Detail_View.md Q-Detail_View-45 | Add Q-Detail_View-45 to these Review fields (architect edit, or rerun creator), and add the cases to Q-Detail_View-45's Affected cases. |
| 3 | Major | UI-Detail_View-309 | Rule outcome stated | Step 3 is only `Not known` plus a `Proposed` key outcome, although cited R-Detail_View-32 states the key "consists only of lowercase alphanumeric characters". The rule outcome should come first as fact (if saved, the key has only lowercase alphanumeric characters), then the open part (whether the name is accepted, whether `Ü` counts as alphanumeric). | R-Detail_View-32; part-test.md#L31 | Edit step 3. |
| 4 | Major | UI-Detail_View-329 | Fidelity | Cites R-Detail_View-39 (deleting a template deletes its results), but the case renames, never deletes. Also the `Proposed` outcome (result stays linked) runs against the literal reading of the cited R-Detail_View-32 (results are matched by the key, and the key is regenerated on save); see Question 3. | R-Detail_View-32, R-Detail_View-39; part-test.md#L31, #L64 | Drop R-Detail_View-39 from the Requirement; settle Question 3 before approval. |
| 5 | Major | UI-Detail_View-313 | Specific Expected results | Type is Negative, but step 3's Expected result restates the rule ("The name must be unique across a set of variants") with no observable outcome (created or not created, table content). | R-Detail_View-31; index doc issue 4 | Edit step 3: state the outcome the rule's literal reading gives (template not created), then `Open: Q-Detail_View-46`; or `Proposed, to confirm in Q-Detail_View-46: ...`. |
| 6 | Major | UI-Detail_View-302 | Specific Expected results | "Its key is generated from the name" is vague; R-Detail_View-32 gives enough to state the expected key (`qa<suffix>voltagecheck`, lowercase alphanumeric only). | R-Detail_View-32; part-test.md#L31 | Edit step 3 to state the expected key (with the hyphen-dropping part marked if the architect considers it open, Q-Detail_View-46). |
| 7 | Major | UI-Detail_View-337 | Rule outcome stated / No assumptions | Step 1 states as fact "The tab opens" for `reader`, which no source states; the same cell then marks it open. It must carry the `Proposed, to confirm in Q-Detail_View-45` label. | R-Detail_View-29; Q-Detail_View-45 | Edit step 1. |
| 8 | Minor | UI-Detail_View-303 | One behaviour | One case cites five rules (R-Detail_View-34 to 38) and only checks persistence of the fields, not the behaviour each rule states; overlaps 317 and 318. | R-Detail_View-34 to 38 | Keep as an "all fields saved" case but cite R-Detail_View-29 (definition) or narrow the rule list. |
| 9 | Minor | UI-Detail_View-317 | Specific Expected results | Step 4 "not used by the testing framework, so it does not change test behaviour" is not observable in the UI. | R-Detail_View-34; part-test.md#L48 | Keep only the stored-value check, or drop the unobservable sentence. |
| 10 | Minor | UI-Detail_View-309 | Technique | Type `Boundary` with Technique `Error guessing`; no boundary is exercised. | Seed Type/Technique fields | Type Negative or Positive per the eventual answer. |
| 11 | Minor | UI-Detail_View-333 | Technique | `Exploratory` for a fixed positive check of the second clause of R-Part_Template-08. | part-test.md#L19 | Equivalence partitioning (valid class: stock item of a variant). |
| 12 | Minor | UI-Detail_View-311, 314, 315, 332, 337 | No assumptions (title/summary) | Title or Summary states the `Proposed` outcome as fact ("is rejected", "does not appear", "hidden"), while the steps label it Proposed. | Q-Detail_View-45, 46, 49 | Neutral wording in title/summary until the questions are answered. |
| 13 | Minor | UI-Detail_View-307 | Seed format | `Open: Q-Detail_View-46` appears twice in step 3. | Step 3 | Merge into one Open note. |
| 14 | Minor | UI-Detail_View-304 to 308 | Test data | Template names `Firmware Version`, ` My NEW T E sT `, `Test 123`, `100 Percent Test`, `Hardware Revision` lack the `QA-` prefix. Templates sit on a `QA-` part, so cleanup is safe, but the project rule asks for `QA-` names. | CLAUDE.md, test records | Architect: accept as needed for the doc examples, or note the exception in each case. |
| 15 | Minor | UI-Detail_View-301, 334, 335, 339 | Postconditions | Cleanup says "delete the template if it exists" though the case creates none. | Postconditions | Trim cleanup text. |
| 16 | Minor | UI-Detail_View-319, 320, 321, 322 | Seed format | Pre-steps say "open the part detail page", but the steps work on the stock item; 320 to 322 have no navigation step to the stock item's results. | Prerequisites, step 1 | Align pre-steps with the stock item path (still open in Q-Detail_View-47). |
| 17 | Minor | UI-Detail_View-339 | Seed format | Pre-steps already "open the part detail page", step 1 opens it again by URL. | Prerequisites | Pre-steps: log in only. |
| 18 | Minor | UI-Detail_View-336 | Open-question marking | Steps 1 and 2 toggle Testable without referencing how (Q-Detail_View-23, used by 335 for the same action). | Q-Detail_View-23 | Add `Open: Q-Detail_View-23 (edit form control label)`. |
| 19 | Minor | UI-Detail_View-335, 339 | Open-question marking | They cite Q-Detail_View-23 and Q-Detail_View-19, whose Affected cases lists do not include them. | open-question_Detail_View.md Q-Detail_View-19, Q-Detail_View-23 | Architect: add the cases to those rows. |
| 20 | Minor | UI-Detail_View-330 | Seed format | Prerequisites do not state whether the master's template is created before or after the variant (this decides whether it repeats 331). | Prerequisites | State the order (template first, then variant). |
| 21 | Minor | UI-Detail_View-325 | Fidelity | Cites R-Detail_View-39 (results deleted with the template) while testing a template with no results; the rule's clause is not exercised (326 does). | R-Detail_View-39 | Cite R-Detail_View-29 as well, or note the case is the no-results baseline. |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Detail_View-302 | 53 | UI-Detail_View-304 | Keep | R-Detail_View-29 name-only creation smoke vs the R-Detail_View-33 key mappings. |
| UI-Detail_View-304 | 81 | UI-Detail_View-306 | Keep | Baseline example (inner space, capitals); each match exercises another key-generation class. |
| UI-Detail_View-305 | 76 | UI-Detail_View-304 | Keep | Only trimming case (leading, trailing, repeated spaces). |
| UI-Detail_View-306 | 81 | UI-Detail_View-304 | Keep | Only case with digits kept inside the key. |
| UI-Detail_View-307 | 76 | UI-Detail_View-306 | Keep | Only leading-digit / underscore case (doc issue 3). |
| UI-Detail_View-310 | 63 | UI-Detail_View-311 | Keep | Exact same name vs same-key different spelling; others differ in state or class. |
| UI-Detail_View-311 | 63 | UI-Detail_View-310 | Keep | Same-key, different-name invalid class. |
| UI-Detail_View-313 | 56 | UI-Detail_View-310 | Keep | Cross-variant clause; name defined on the template part. |
| UI-Detail_View-314 | 61 | UI-Detail_View-311 | Keep | Empty-name class. |
| UI-Detail_View-315 | 55 | UI-Detail_View-311 | Keep | Whitespace-only class. |
| UI-Detail_View-323 | 63 | UI-Detail_View-324 | Keep | Enabled to disabled vs the reverse transition. |
| UI-Detail_View-324 | 63 | UI-Detail_View-323 | Keep | Disabled to enabled vs the reverse transition. |
| UI-Detail_View-330 | 51 | UI-Detail_View-331 | Escalate | Prerequisites do not fix whether the template exists before the variant; if not, it repeats 331 (finding 20). |
| UI-Detail_View-331 | 51 | UI-Detail_View-330 | Keep | Explicit state: variant exists before the template is added. |
| UI-Detail_View-340 | 61 | UI-Detail_View-310 | Keep | No existing template; double submit of one name. |

Optional, for the architect: 304 to 307 share every step and differ only in name and expected key; they could be one data-driven case with four rows if fewer cases are preferred.

## Questions for the architect

1. **Name length and empty name (316, 314, Q-Detail_View-46).** The Parts schema slice gives `PartTestTemplate.test_name` `maxLength: 100` and lists `test_name` as required; `description` has `maxLength: 100` ([openapi-parts.yaml#L4917-L4926](../../requirements/openapi-parts.yaml#L4917), required list L4947-L4952). Do you accept the schema as the source for these UI limits when answering Q-Detail_View-46? If so, 316 can state 99/100/101 and a description-length boundary case may be wanted.
2. **`choices` field.** The schema has a `choices` field on test templates ("Valid choices for this test (comma-separated)", L4943-L4946) that the docs do not mention. Should it be added to the index "Not in docs" table, and is it in scope for this tab?
3. **Rename after results (329).** R-Detail_View-32 says results are matched by the key and the key is regenerated on every save. Read literally, renaming would unlink existing results; the case proposes they stay linked. Which outcome should the case expect (Q-Detail_View-48)?
4. **User for stock test results (319 to 322, 326, 329).** Recording a test result is a stock action. The docs do not say whether `engineer` (seed: manage parts, view stock) may add stock test results, nor who the least-privileged user is. Add this to Q-Detail_View-47?
5. **Unicode in keys (309).** Does "lowercase alphanumeric" include non-ASCII letters such as `ü`, or are they dropped? The docs do not say.
