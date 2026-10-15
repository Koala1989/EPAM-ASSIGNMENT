# Review: Category hierarchy filtering and parametric tables with unit-aware filtering and sorting (UI), 2026-10-15

**Cases reviewed:** UI-Categories-008 to UI-Categories-023 (16), UI-Part_Params-064 to UI-Part_Params-095 (32) · **Verdict:** Changes required

## Coverage

`coverage_check.py --area Categories --area Part_Params` with the two case files: Rules: 43 · covered: 17 · not cited by any case: 26 · exit 0 (no unknown rule IDs).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Categories-01 | 008, 009, 014, 022 | Covered | None |
| R-Categories-02 | 009, 010, 011, 012, 014, 015, 017, 019, 021, UI-Part_Params-093 | Covered | None (positive, exclusion, empty, deepest level, move and create what-ifs are all here) |
| R-Categories-03 | 008, 011, 013, 021, 023 | Covered | None |
| R-Categories-04 | 016 | Covered | Data has no stock and no image, so "thumbnail" and "stock level" can't be told apart from a placeholder or blank (finding 9) |
| R-Categories-05 | 017, 018, 019, 020, 021 | Covered | 018 (multiple filters) has no concrete second filter and no expected parts (finding 5) |
| R-Categories-06, R-Categories-07 | none | Out of scope | Belong to "Open a part from the category list and the category breadcrumb" (UI-Categories-001 to 007) |
| R-Part_Params-21 | 064, 065, 066, 093, 094, 095 | Covered | Negative 066 has no observable expected result (finding 3) |
| R-Part_Params-22 | 067, 068, 069, 070, 094 | Covered | None |
| R-Part_Params-23 | 071-078, 083, 084, 091, 092, 094 | Covered | None |
| R-Part_Params-24 | 085 | Covered | None (non-matching parts are asserted as excluded) |
| R-Part_Params-25 | 086 (and 090 step 4) | Covered | None |
| R-Part_Params-26 | 087, 088, 089 | Covered | None |
| R-Part_Params-27 | 079, 080, 081, 082, 091, 092 | Covered | None (incompatible-unit and non-numeric negatives present) |
| R-Part_Params-28 | 089, 090 | Covered | None |
| R-Part_Params-29 | 071-078, 082, 087 | Covered | None: each operator has its own case; `>`/`>=`/`<`/`<=` have below, on (10k) and above values; `~` has its negative (078) |
| R-Part_Params-30 | 069, 080 | Covered (support only) | Primary home is parameter entry; it's cited here only for stored mixed-unit values |
| R-Part_Params-33 | 069, 091 | Covered | None |
| R-Part_Params-01 to 20, 31, 32, 34 to 36 | none | Out of scope | Parameters tab, templates, uniqueness, category defaults (functionality "Part parameters tab, parameter templates and category parameters"); unit validation setting and selection lists (functionality "Parameter unit validation setting and selection list administration"); R-Part_Params-31 is about parameter creation, not filtering. R-Part_Params-12 is cited only by 092 (finding 6) |

No rule in scope is missing a case. Permission depth: `reader` and `noaccess` are covered for both functionalities (UI-Categories-021/022, UI-Part_Params-094/095). Negative cases exist for both.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | UI-Part_Params-081 | No assumptions / Fidelity | Step 2 expects "The filter is added (R-Part_Params-23)" as fact for the invalid value `10 kg`. Step 3 then proposes that the filter is not applied and an error is shown. No rule says an incompatible-unit filter is added. If the app rejects the value in the dialog, step 2 fails falsely, and an automated test would assert the opposite of the proposal. | R-Part_Params-23 ([concepts-parameters.md#L126-130](../../../requirements/docs/concepts-parameters.md#L126-L130)) covers valid filtering only; Q-Part_Params-20 is open | Edit step 2 so it only enters the value, with the outcome "Open: Q-Part_Params-19 (dialog)" as in UI-Part_Params-083 step 2; keep the outcome in step 3. |
| 2 | Blocker | UI-Part_Params-082 | No assumptions / Fidelity | Same as finding 1: step 2 expects "The filter is added (R-Part_Params-23)" for the non-numeric value `abc`, which contradicts step 3. | As finding 1 | As finding 1. |
| 3 | Major | UI-Part_Params-066 | Specific Expected results | Step 2 expected result only repeats the rule ("Only tables that support ... have a button"). It never says what is observed on the opened table (button absent). Also, the table to open is in Pre-steps and step 1 then opens it again. The resistor data in Prerequisites isn't used. | R-Part_Params-21 ([concepts-parameters.md#L114](../../../requirements/docs/concepts-parameters.md#L114)) | State the observable outcome: "Proposed, to confirm in Q-Part_Params-18: no *Parametric View* button is shown above the table". Move the table choice into step 1's test data, and drop the unused data. |
| 4 | Major | UI-Part_Params-067 | Open-question marking | Marked `Q-Part_Params-19` (filter and remove controls, filter dialog, indicator, edit control), but the case uses no filter. Q-Part_Params-19's affected list also names 067. | [open-questions.md Q-Part_Params-19](../../Parameters/open-questions.md) | Remove Q-Part_Params-19 from the Review field. The architect may also remove 067 from Q-Part_Params-19's affected cases. |
| 5 | Major | UI-Categories-018 | Specific Expected results | Both filters are entirely `[open]`, and step 3 expects only "parts that satisfy both filters". No part names are given, and the data has only one distinguishing property (active/inactive), so AND can't be told apart from OR, and the case can't be run or automated. | R-Categories-05 ([part-index.md#L44](../../../requirements/docs/part-index.md#L44)) | Rerun the creator after Q-Categories-04 is answered, or give the data a second property (for example one active part marked Assembly) and name the parts expected under the proposed AND. |
| 6 | Major | UI-Part_Params-092 | Fidelity | Step 3 expects "The parameter is saved (R-Part_Params-12)" for **editing** an existing value. R-Part_Params-12 describes **adding** a parameter (*New Parameters*), and the case's own Notes admit editing is not described. Postconditions say "Nothing changed", but R-4k7's value is changed to 22k. | R-Part_Params-12 ([concepts-parameters.md#L65-69](../../../requirements/docs/concepts-parameters.md#L65-L69)) | Make step 3's outcome "Proposed, to confirm in Q-Part_Params-19: the value is saved" (or set the value via the API as `admin` as a pre-step, since editing isn't under test). Correct the Postconditions. |
| 7 | Major | UI-Part_Params-088 | No assumptions | Step 4 states "No error is shown for the combination" as fact. No source says how contradictory filters are handled. | R-Part_Params-26 ([concepts-parameters.md#L142](../../../requirements/docs/concepts-parameters.md#L142)) | Label it "Proposed, to confirm in Q-Part_Params-19 (or a new question): no error is shown". Add R-Part_Params-24 to the Requirement field, since step 4 cites it. |
| 8 | Major | UI-Part_Params-070 | No assumptions | The Summary says the part without the parameter "is still listed" when sorted, but step 3 says that is not known (Q-Part_Params-21). The Summary states an assumption as the case's purpose. | R-Part_Params-22 ([concepts-parameters.md#L120](../../../requirements/docs/concepts-parameters.md#L120)) is silent on missing values | Reword the Summary neutrally ("where a part without the parameter appears when sorted by it"). |
| 9 | Minor | UI-Categories-016 | Specific Expected results | Thumbnail and stock level are expected, but no part has an image or stock item, so the check can't tell a real value from a blank or placeholder. | R-Categories-04 ([part-index.md#L37-42](../../../requirements/docs/part-index.md#L37-L42)) | Add an image and a stock item to one part, and expect the stock quantity. |
| 10 | Minor | UI-Part_Params-090 | Rule outcome stated | Step 4 marks "the column no longer indicates a filter" as Proposed, but R-Part_Params-25 says each column shows whether a filter is *currently* applied, so the rule states it. R-Part_Params-25 is also missing from the Requirement field. | R-Part_Params-25 ([concepts-parameters.md#L136](../../../requirements/docs/concepts-parameters.md#L136)) | State it as fact (R-Part_Params-25) and add the rule to Requirement. |
| 11 | Minor | UI-Categories-008 to 022 | Seed format | The Postconditions contain the garbled text "Nothing changed. none changed." (014: "... is now in `QA-<suffix> Sibling`. none changed."). 015's cleanup says "clean up the rest as in the data list". | Seed, Postconditions | Edit the wording. |
| 12 | Minor | UI-Categories-021, UI-Part_Params-094 | Technique | Type is Positive, but Technique says "Negative (reader)". | Seed, Technique | Use "Decision table (role x action: reader)". |
| 13 | Minor | UI-Categories-012 | Technique / One behaviour | It's labelled Boundary "deepest level: level 4", but the docs state no depth limit (the case's own Note says so), so there is no boundary. Step 1 repeats UI-Categories-009 step 2 (Part Deep listed under Top). | R-Categories-02 | Relabel as Equivalence partitioning (deep nesting), or consider merging step 2 into 009. |
| 14 | Minor | UI-Categories-023 | Technique | Type Boundary with Technique "Error guessing" only. | Seed | Align Type (Negative/Positive) or add the class. |
| 15 | Minor | UI-Categories-022, UI-Part_Params-095 | Seed format | Pre-steps say "open the *Parts* view" (095: "open the category"), but step 1 is that same action as the user under test. 022's Notes say the pk is read as `admin`, but this isn't in Prerequisites. | Seed, Prerequisites | Pre-steps: "log in as `noaccess`; category pk read as `admin` beforehand". |
| 16 | Minor | UI-Part_Params-083 | One behaviour / Seed format | Step 2 enters two inputs (empty, then a space) under one expected result. | Seed, "One user action per step" | Split into two steps. |
| 17 | Minor | UI-Part_Params-094 | Fidelity | Step 2 states "The filter is added (R-Part_Params-23)" as fact for `reader`, but step 3 says whether filtering works for `reader` is Proposed (Q-Part_Params-23). | Q-Part_Params-23 | Make step 2 consistent with step 3. |
| 18 | Minor | UI-Part_Params-071 to 076, 079, 087 | Seed format | The expected sets depend on unit conversion of stored values (`4.7k`, `1000 kohm`) and of the filter value `10k`. 071 to 076 and 087 don't cite R-Part_Params-27. 082 cites R-Part_Params-29 (operators), which doesn't apply to a non-numeric value. | R-Part_Params-27 | Add R-Part_Params-27 where conversion decides the result. Drop R-Part_Params-29 from 082. |
| 19 | Minor | UI-Part_Params-093 | Technique | Labelled "Exploratory (charter)", but it's a scripted check with fixed expected parts. | Seed | Use "Equivalence partitioning (parts in sub-category)". |
| 20 | Minor | UI-Part_Params-077 | Open-question marking | It's marked Q-Part_Params-22 for case sensitivity of `~`, but the value `-2` has no letters, so case sensitivity can't affect it. | Q-Part_Params-22 | Either use a mixed-case value (for example `beta`) so the question applies, or drop the note. |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Categories-017 | 56 | UI-Categories-019 | Keep | 017 checks the filter narrowing across the subtree; 019 checks removing it (state transition) |
| UI-Categories-019 | 56 | UI-Categories-017 | Keep | Filtered-to-unfiltered transition, different end state |
| UI-Part_Params-067 | 76 | UI-Part_Params-068 | Keep | First sort vs second click (reversed order); 069 differs in rule and data |
| UI-Part_Params-068 | 76 | UI-Part_Params-067 | Keep | Ascending-to-descending transition |
| UI-Part_Params-069 | 54 | UI-Part_Params-067 | Keep | R-Part_Params-33, explicit mixed units |
| UI-Part_Params-071 | 96 | UI-Part_Params-072 | Keep | `>` excludes the 10k boundary; `>=` includes it. "+1 more" match not visible |
| UI-Part_Params-072 | 96 | UI-Part_Params-071 | Keep | Boundary included vs excluded. "+1 more" not visible |
| UI-Part_Params-073 | 98 | UI-Part_Params-074 | Keep | `<` excludes the 10k boundary; `<=` includes it. "+1 more" not visible |
| UI-Part_Params-074 | 98 | UI-Part_Params-073 | Keep | Boundary included vs excluded. "+1 more" not visible |
| UI-Part_Params-075 | 83 | UI-Part_Params-076 | Keep | `=` vs `!=`: complementary expected sets. "+2 more" not visible |
| UI-Part_Params-076 | 83 | UI-Part_Params-075 | Keep | As above |
| UI-Part_Params-077 | 70 | UI-Part_Params-075 | Keep | Text parameter with `~` vs numeric with `=` |
| UI-Part_Params-079 | 51 | UI-Part_Params-080 | Keep | `10k` vs `10000` with `>`; 080 uses an explicit unit with `=` |
| UI-Part_Params-080 | 52 | UI-Part_Params-075 | Keep | Same operator and result, but an explicit compatible unit `10 kohm` vs the shorthand `10k`: different input class under R-Part_Params-27 |
| UI-Part_Params-081 | 73 | UI-Part_Params-082 | Keep | Incompatible unit vs non-numeric value |
| UI-Part_Params-082 | 73 | UI-Part_Params-081 | Keep | As above |
| UI-Part_Params-087 | 57 | UI-Part_Params-073 | Keep | Two filters on one parameter (R-Part_Params-26) vs one operator |
| UI-Part_Params-089 | 53 | UI-Part_Params-090 | Keep | Two filters to one vs one to none |
| UI-Part_Params-090 | 53 | UI-Part_Params-089 | Keep | As above |

The scores of 071 to 076 (83 to 98) come from shared boilerplate (data, step 1, the "filter is added" step). They are not duplicate behaviour. The script's "+N more" matches for 071 to 076 were not listed, so they couldn't be read; the verdicts cover the visible matches only.

## Questions for the architect

1. UI-Categories-017 to 020 make parts inactive and use an "active parts" filter. R-Categories-02 says the list shows *every* part, so step 1 of 017 expects all five, including the inactive ones. If 1.5.6 hides inactive parts by default, is that a finding against R-Categories-02, or should Q-Categories-04 also ask about the default filter state?
2. UI-Part_Params-079 step 3 repeats UI-Part_Params-071 steps 1 to 3 (same `>` `10k` filter, same result). 079 only adds steps 4 and 5. Keep both (different rules: R-Part_Params-29 vs R-Part_Params-27), or cut 079 down to the `10000` comparison?
3. The parametric data stores bare numbers (`500`, `10k`) on an `ohm` template. The docs imply that a bare number is read in the base unit only through the uniqueness example (`1k` duplicates `1000`, [concepts-parameters.md#L92](../../../requirements/docs/concepts-parameters.md#L92)). Is that enough to rely on, or should it be confirmed in a question?
