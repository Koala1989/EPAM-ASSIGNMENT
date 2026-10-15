# Review: Part detail view header details and tab visibility, including the Allocated and Build Orders tabs (UI), 2026-10-15

**Cases reviewed:** UI-Detail_View-080 to UI-Detail_View-114 (35 cases, `test-cases/Part_Detail_View/part-detail-header-and-tab-visibility.md`) · **Verdict:** Approve with changes

## Coverage

`coverage_check.py --area Detail_View --file part-detail-header-and-tab-visibility.md`: Rules: 70 · covered: 11 · not cited by any case: 59 · exit 0 (every rule ID cited is in the inventory).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Detail_View-01 | 080, 081 | Covered | None (show and hide). |
| R-Detail_View-02 | 082, 083 | Covered | None. |
| R-Detail_View-03 | 084, 085 | Covered | None. The rule does not state the noaccess outcome; 084 labels it Proposed. |
| R-Detail_View-04 to 07 | none | Out of scope | Part image, thumbnail, image actions and notes: not header details or tab visibility. See question 2. |
| R-Detail_View-08 | 085, 086, 087, 088, 089, 090 | Covered | None (shown, hidden, both transitions). |
| R-Detail_View-09 to 15 | none | Out of scope | Stock tab content and stock flags. |
| R-Detail_View-16 | 095, 096, 097, 098 | Covered | Minor: no case for a part allocated to a build order and a sales order together ("and/or" in the rule); no case for a completed or shipped sales order (only a cancelled build, 098). |
| R-Detail_View-17 | 085, 086, 091, 092, 093, 094, 095, 096, 097, 107 | Covered | None (all four decision-table columns plus reader). |
| R-Detail_View-18 | none | Out of scope | BOM tab content (the BOM functionalities). |
| R-Detail_View-19 | 085, 086, 099, 100, 104 | Covered | 104 cites it wrongly (finding 1). The real coverage is 085, 086, 099, 100, which is enough. |
| R-Detail_View-20 | 101, 102, 103, 104, 105, 106, 108 | Covered | None. The visibility condition is open (Q-Detail_View-16). |
| R-Detail_View-21 | 085, 086, 109 | Covered | The hidden case is UI-Detail_View-070 (BOM functionality file), as 109 notes. |
| R-Detail_View-22 | none | Out of scope | Pricing tab content; no visibility condition. |
| R-Detail_View-23 | 085, 086, 110, 111, 112 | Covered | None (shown, hidden, blocked user). |
| R-Detail_View-24 | 085, 086, 113, 114 | Covered | Minor: no case for `engineer` on a Purchaseable part, the counterpart of 112 that Q-Detail_View-21 asks about. |
| R-Detail_View-25 | none | Out of scope | Sales Orders tab content; no visibility condition stated. |
| R-Detail_View-26 | none | **Gap** | "Visible only if Salable and the return order feature is enabled": a tab-visibility rule with no shown or hidden case. See question 1. |
| R-Detail_View-27 | none | **Gap** | "Hidden if Virtual or the transfer order feature is disabled": a tab-visibility rule with no case. See question 1. |
| R-Detail_View-28, 29 | none | Out of scope | Stock History content; Test Templates (test template functionality). |
| R-Detail_View-30 | none | **Gap** (visibility clause) | "Visible only if Testable": the visibility clause has no case. The table-content clause is out of scope. See question 1. |
| R-Detail_View-31 to 70 | none | Out of scope | Test templates, related parts, attachments, BOM (other functionalities of the Area). |

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Major | UI-Detail_View-104 | Fidelity | The Requirement cites R-Detail_View-19 (the *BOM* tab is visible only for an Assembly), but the case checks the *Build Orders* tab. R-19 says nothing about Build Orders, and the citation makes coverage_check count 104 as an R-19 case. The Expected result is correctly labelled Proposed, so the outcome does not mislead. | part-views.md#L84 (BOM), #L88 (Build Orders, no condition) | Edit the case: remove `R-Detail_View-19` from the Requirement. |
| 2 | Major | UI-Detail_View-091, UI-Detail_View-092, UI-Detail_View-113 (vs 085, 094, 110) | Open-question marking | These cases run as `allaccess`, who has every build, sales and purchase order permission. Q-Detail_View-19 and Q-Detail_View-21 ask whether the tabs also need those permissions, but the answer cannot change what these cases expect, so the questions do not affect them. Marking is also inconsistent: 094 (Allocated, allaccess) and 110 (Suppliers, allaccess) are plain `Draft`, while 091, 092 and 113 are held at `Draft · Open question`. | Q-Detail_View-19 and Q-Detail_View-21 rows; seed Review field ("when an open question affects the case") | Edit the cases: drop Q-Detail_View-19 from 091 and 092, and Q-Detail_View-21 from 113 (Review field, `Open:` notes, and the question rows' Affected cases). Or record why they should stay. |
| 3 | Major | R-Detail_View-26, R-Detail_View-27, R-Detail_View-30 | Coverage | Gap: these tab-visibility rules (Return Orders, Transfer Orders, Test Results) have no case, although this functionality is "tab visibility". | part-views.md#L118, #L122, #L134 | Rerun the creator for these rules, or confirm they belong to another functionality (question 1). |
| 4 | Minor | UI-Detail_View-107 | Rule outcome stated | The Expected result is only `Proposed`, but 091 states the same R-Detail_View-17 outcome (Component part: tab shown) as fact. Only the user differs, which is what Q-Detail_View-19 leaves open. This is inconsistent with 091. | R-Detail_View-17; part-views.md#L80 | Edit the case: either "The *Allocated* tab is shown (R-Detail_View-17). Open: Q-Detail_View-19 (...)" or keep Proposed deliberately and note why. |
| 5 | Minor | UI-Detail_View-107, UI-Detail_View-108 | Technique | Type is Positive, but the Technique includes "Negative (viewer without edit rights)". No negative input or blocked action is exercised. | seed Technique field | Edit: drop "Negative" from the Technique. |
| 6 | Minor | UI-Detail_View-081, UI-Detail_View-083 | Technique / Type | Type is Negative, but 081 is the reverse transition of a toggle and 083 checks a correct display. Neither tests a rejected or blocked action. | seed Type field | Edit: set Type to Positive. |
| 7 | Minor | UI-Detail_View-103 | Technique / wording | The Technique lists "State transition (Pending to Complete)", but no transition happens in the steps (both states are set in Data). The title and Summary claim the pending build shows no completion date, while the Expected result leaves that open (Q-Detail_View-17), and says "Both builds are listed with ... completion date". | R-Detail_View-20; Q-Detail_View-17 | Edit: drop the State transition label, and align the title and Summary with the Expected result. |
| 8 | Minor | UI-Detail_View-095, UI-Detail_View-096 | Technique | "Exploratory, What-if business scenario" for a scripted check of one valid class (allocation to a pending build or sales order). | seed Technique field | Edit: Equivalence partitioning (valid class: pending build order / pending sales order allocation). |
| 9 | Minor | UI-Detail_View-094 | No assumptions | "and appears only once in the tab list" is not stated by any source. It is a harmless error-guessing check, but it is not labelled as such. | R-Detail_View-17 | Edit: add Error guessing to the Technique, or drop the clause. |
| 10 | Minor | UI-Detail_View-085 | One behaviour | One decision-table column checks six visibility rules plus R-03. This is acceptable as the "all true" column, but it overlaps 087, 091 to 094, 099, 109, 110 and 113. If step 2 fails, it does not show which tab is wrong. | R-Detail_View-03, 08, 17, 19, 21, 23, 24 | No change needed. Optionally expect each panel by name in step 2. |
| 11 | Minor | UI-Detail_View-098 | Automation | "Partial: build order cancellation is a pre-step in another page": the pre-step can be done through the API, so this is not a reason for Partial. | Prerequisites of 098 | Edit: Automation Yes (cancel through the API), or give the real reason. |
| 12 | Minor | R-Detail_View-16, R-Detail_View-24 | Depth | Optional extra cases: a part allocated to both a build order and a sales order (rule says "and/or"); `engineer` on a Purchaseable part for the *Purchase Orders* tab (Q-Detail_View-21). | part-views.md#L80, #L108-110 | Rerun the creator for these two cases if wanted. |

No Blockers. Checked and correct: seed field order and Steps columns on all 35 cases; every Requirement has a rule ID and a source link; Review fields are all `Draft` or `Draft · Open question: ...`; Proposed outcomes carry their label; 084 and 112 use the blocked user; 088, 093, 100, 111 and 114 give the hidden case for each "visible only if" rule (070 for Used In).

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Detail_View-091 | 81 | 092 | Keep | Different R-17 column (Component only vs Salable only); 094 both on; 107 a different user. |
| UI-Detail_View-092 | 81 | 091 | Keep | Salable-only column; 094 both on; 107 reader. |
| UI-Detail_View-094 | 63 | 091 | Keep | Both-on column; 107 a different user. |
| UI-Detail_View-095 | 75 | 096 | Keep | Build-order clause of R-16 vs sales-order clause. |
| UI-Detail_View-096 | 75 | 095 | Keep | Sales-order clause vs build-order clause. |
| UI-Detail_View-104 | 50 | 108 | Keep | allaccess vs reader. |
| UI-Detail_View-105 | 79 | 106 | Keep | Component off vs on; this column decides "Assembly only" vs "Component too" (Q-16). |
| UI-Detail_View-106 | 79 | 105 | Keep | Component on vs off (Q-16). |
| UI-Detail_View-107 | 54 | 091 | Keep | reader vs allaccess. |
| UI-Detail_View-108 | 50 | 104 | Keep | reader vs allaccess. |
| UI-Detail_View-111 | 52 | 112 | Keep | Purchaseable off with allaccess vs Purchaseable on with engineer. |
| UI-Detail_View-112 | 52 | 111 | Keep | Permission condition vs attribute condition. |

## Questions for the architect

1. Are the visibility rules of the *Return Orders* (R-Detail_View-26), *Transfer Orders* (R-Detail_View-27) and *Test Results* (R-Detail_View-30) tabs part of this "tab visibility" functionality? This review treats them as gaps. If they belong to a separate order-tabs or test-templates functionality, finding 3 is out of scope. Both feature settings are unnamed in the docs (inventory notes), so cases for them would need open questions.
2. Is the part image (R-Detail_View-04 to 06), shown in the header panel, meant to be part of "header details"? This review treats it as out of scope (image functionality).
3. R-Detail_View-17 says the *Allocated* tab is "only visible if" Component or Salable. That is a necessary condition, so it is not strictly a sufficient one. Cases 091, 092 and 094 read it as "visible if", and 107 treats it as Proposed. Which reading should the cases use (it decides finding 4)?
