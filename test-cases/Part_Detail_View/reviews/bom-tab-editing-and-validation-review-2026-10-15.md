# Review: Bill of materials tab editing and validation (UI), 2026-10-15

**Cases reviewed:** UI-Detail_View-001 to UI-Detail_View-037 (37 cases, `test-cases/Part_Detail_View/bom-tab-editing-and-validation.md`) · **Verdict:** Changes required

## Coverage

`coverage_check.py --area Detail_View --file test-cases/Part_Detail_View/bom-tab-editing-and-validation.md`: Rules 70 · covered 13 · not cited 57 · exit 0. No case cites an unknown rule ID.

R-Detail_View-01 to R-Detail_View-17, R-Detail_View-20 to R-Detail_View-49: out of scope (header, image, Stock, Allocated, other order tabs, Test Templates/Results, Related Parts, Attachments). Not listed one by one below.

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Detail_View-18 (BOM tab lists sub-components and quantities) | none cite it | Covered in practice, not cited | 005, 021 and 023 check lines and quantities in the BOM table but do not cite the rule (Minor). |
| R-Detail_View-19 (BOM tab only for Assembly) | 004 | **Gap** | 004 cites it but tests user permissions, not the Assembly condition. No case checks that a part with Assembly off has no *BOM* tab (the "visible only if" hidden case). |
| R-Detail_View-50 | 005-007, 009-011, 017-020, 022 | Covered | No limits stated. All limit cases are open (Q-04), which is correct. |
| R-Detail_View-51 | 012, 013, 014 | Covered (input only) | 014 assumes an upper boundary at 100 that no source states. That is fine as error guessing, but if Q-04 sets a limit, on-limit and below-limit cases are needed. |
| R-Detail_View-52 | 015 | **Depth gap** | Only a negative input case. The rule's own statement (Setup Quantity is added to the base quantity) is not tested, and no case cites the rule for a valid value. 006 enters 5 but cites only R-50/R-62. |
| R-Detail_View-53 | 016 | **Depth gap** | Same as R-52: the rounding-up behaviour is not tested, and Rounding Multiple `0` is not tried. |
| R-Detail_View-54, -55, -56, -58 | none | Out of scope | Build Order allocation and availability (Build Orders functionality). |
| R-Detail_View-57 | 034-037 | Covered (BOM part) | The stock-allocation clause belongs to Build Orders (out of scope). |
| R-Detail_View-59 | 001, 002, 021, 022, 023 | Covered | |
| R-Detail_View-60 | 003, 004, 033 | Covered | Blocked user `reader` is in 003. |
| R-Detail_View-61 | none | Out of scope | BOM import (data import functionality). |
| R-Detail_View-62 | 005-011, 017, 018 | Covered | Negative 007, cancel 008. |
| R-Detail_View-63 | 030, 034-037 | Covered | |
| R-Detail_View-64 (multi-level BOMs) | none | **Gap** | No case adds a sub-assembly that has its own BOM as a line of another assembly. The rule is about BOM structure, which this functionality edits. If the architect places it elsewhere, it becomes out of scope (see Questions). |
| R-Detail_View-65 | 024-031 | Covered, one column missing | Decision table: Reference, Quantity, Attrition, Setup Quantity, Rounding Multiple, Consumable, Inherited, Optional and Allow Variants are covered, plus create (024) and delete (026). **Component ID** (changing the line's Part) has no case. 027's note calls it "a different action", but the docs list it as a checksum field (manufacturing-bom.md#L170). |
| R-Detail_View-66 | 027, 032, 033 | Covered | |
| R-Detail_View-67 | 024-027, 032, 033 | Covered | |
| R-Detail_View-68, -69 | none | Out of scope | BOM comparison functionality. |
| R-Detail_View-70 | none | Out of scope | Replace Component on the *Used In* tab. |
| Cross-refs R-ATT-25, R-Unit_measure-16 to -18, R-Part_Template-09 to -11 | not cited here | Out of scope (primary Area elsewhere) | R-ATT-25 and R-Unit_measure-16 to -18 are cited by cases in Attributes and Units_of_Measure. |

Negative cases exist (003, 004, 007, 010-012, 015-018, 020, 022, 033, 036, 037).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | UI-Detail_View-024 step 1, UI-Detail_View-025 step 1, UI-Detail_View-027 step 1 | No assumptions | These steps state as fact that a validated BOM shows "no *Validate BOM* button" (027: "The *Validate BOM* button is no longer displayed (R-Detail_View-67)"). The docs say only that the button is displayed when revalidation is needed. Whether it is hidden once validated is exactly what Q-Detail_View-06 asks. 032 step 3 handles this correctly as open. | manufacturing-bom.md#L191; Q-Detail_View-06 ("is the button hidden once validated?") | Edit: state only what R-67 gives (no "Not Validated" status). Mark the button's absence `Proposed, to confirm in Q-Detail_View-06`. |
| 2 | Major | R-Detail_View-19 | Coverage (visible only if) | No case checks that the *BOM* tab is hidden for a part with Assembly off. | part-views.md#L84 | Rerun the creator for the hidden case, or confirm it is covered in another functionality. |
| 3 | Major | R-Detail_View-65 | Coverage (decision table column) | No case changes a line's component (Component ID, a listed checksum field). | manufacturing-bom.md#L170, #L181 | Rerun the creator for a "change the line's Part after validation" case. If the edit form does not allow it, that becomes part of Q-Detail_View-02. |
| 4 | Major | R-Detail_View-64 | Coverage (gap) | No multi-level BOM case (a sub-assembly with its own BOM added as a line). | manufacturing-bom.md#L157 | Rerun the creator, or record the rule as out of scope for this functionality. |
| 5 | Major | R-Detail_View-52, R-Detail_View-53 | Coverage (depth) | The only cases citing these rules are invalid-input cases (015, 016). Neither the rule's behaviour (added to the base quantity, rounded up to the multiple) nor a valid value is tested under the rule. | manufacturing-bom.md#L32-33 | Rerun the creator for valid-value cases. Decide where the computed required quantity can be seen (see Questions). |
| 6 | Major | UI-Detail_View-025, 027, 028, 029, 031, 032 (pre-step) | Open-question marking | Each edits an existing line ("Change Quantity of the line and save", "Edit the line: set ..."), but how a line is edited is open under Q-Detail_View-02. The Review field lacks Q-Detail_View-02 and the steps have no `[open: Q-Detail_View-02, ...]`. 021, 022 and 026 mark it correctly. | Q-Detail_View-02 Affected cases lists only 001, 002, 021, 022, 023, 026 | Add Q-Detail_View-02 to these cases' Review field and the edit steps, and to the question's Affected cases. |
| 7 | Major | UI-Detail_View-006 | Open-question marking | The Test data uses `[open: Q-Detail_View-04, whether 2 or 2%]`, but the Review field lists only Q-01, Q-03 and Q-05, and Q-04's Affected cases omit 006. | Case 006 step 1 Test data; Q-Detail_View-04 row | Add Q-Detail_View-04 to the Review field and the question's Affected cases. |
| 8 | Minor | UI-Detail_View-004 | Fidelity (Requirement) | Cites R-Detail_View-19 (Assembly visibility), but the case tests a user with no permissions on an Assembly. The rule's condition is not exercised. | part-views.md#L84 | Remove R-19 from the Requirement, or replace the case's intent (see finding 2). |
| 9 | Minor | UI-Detail_View-004 | Rule outcome stated | The whole outcome is `Proposed`, although R-60 states as fact that a user without edit permission does not see the *Edit* icon. That part should come first as fact. | manufacturing-bom.md#L127 | Edit step 1: "No *Edit* icon is available (R-60)", then Proposed for the page access. |
| 10 | Minor | UI-Detail_View-008 | Rule outcome stated | Step 2 proposes "no BOM item is created", then step 3 asserts the same outcome as fact (citing R-62). The two steps are inconsistent. | manufacturing-bom.md#L143 | Align: either both cite R-62 as fact, or both are Proposed. |
| 11 | Minor | UI-Detail_View-002 step 1 | No assumptions (borderline) | "The add icon is not shown" is inferred from the docs' click order (Edit, then add). The docs do not say it is hidden in view mode. | manufacturing-bom.md#L124, #L137 | Consider marking as Proposed under Q-Detail_View-02 (which already asks which controls are hidden in view mode). |
| 12 | Minor | UI-Detail_View-006 step 3, UI-Detail_View-013 step 2 | Open-question marking | Which columns the BOM table shows is attributed to Q-Detail_View-03, but Q-03 asks about the *Create BOM Item* form, not the table. 006 also states as fact that the row shows every property. | Q-Detail_View-03 text | Add the table columns to an open question (Q-03 or a new one) and soften 006 step 3. |
| 13 | Minor | UI-Detail_View-033 step 2 | Specific Expected results | A conditional step ("If a *Validate BOM* button is shown, press it"), and the Proposed outcome offers two alternatives ("hidden, or refused with a permission error"). | Q-Detail_View-06 | After Q-06 is answered, make it one action and one outcome. |
| 14 | Minor | UI-Detail_View-027 steps 3-8 | Seed format | Each step has two actions (press *Validate BOM*, then edit a field). The seed asks for one user action per step. | seed-manual-test-case.md Steps | Split, or accept as the decision-table layout. |
| 15 | Minor | UI-Detail_View-020 | Technique / Type | Type is Negative, but the Proposed outcome is that the line is accepted (spaces trimmed). | | Recheck the Type when Q-04 is answered. |
| 16 | Minor | UI-Detail_View-031 | Wording | The Summary says the checksum "must not" change, which presents a Proposed outcome (Q-07) as a requirement. | Q-Detail_View-07 | Reword the Summary neutrally. |
| 17 | Minor | 002-037 (most) | Seed format | Prerequisites Data omits the category, but Cleanup deletes "the category". Several cases also say "components" when only one exists (e.g. 002, 003). | Compare 001 Data | Add the category to Data and fix the plurals. |
| 18 | Minor | UI-Detail_View-025, 027 | Automation field | 025 says `Yes` although its edit control is open (Q-02). | | Set to Partial with the reason. |
| 19 | Minor | R-Detail_View-18 | Coverage (citation) | Exercised by 005, 021 and 023 but not cited by any case. | part-views.md#L84 | Optionally cite it in 005. |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Detail_View-010 | 77 | UI-Detail_View-011 | Keep | A negative numeric quantity (boundary below 0) versus a non-numeric value (wrong type): different invalid classes. |
| UI-Detail_View-011 | 77 | UI-Detail_View-010 | Keep | A wrong-type input class, distinct from the negative number. |
| UI-Detail_View-036 | 53 | UI-Detail_View-037 | Keep | Own component as substitute, on a line with no substitutes, versus a duplicate of an existing substitute: different class and starting state. |
| UI-Detail_View-037 | 53 | UI-Detail_View-036 | Keep | The starting state has substitute Comp B already, and the same part is added again. |

## Questions for the architect

1. **UI-Detail_View-007:** the case states as fact that a line without a Part is not added. R-50 lists Part as a property of every line ("A reference to another Part object which is required to build this assembly"), but the inventory notes "Required fields not stated". Do you accept R-50 as stating that Part is mandatory, or should 007's outcome be `Proposed` under Q-Detail_View-03?
2. **R-Detail_View-65 text vs doc L163:** 024 and 026 rely on "Whenever a BOM line item is created, adjusted or deleted ... must be validated" (manufacturing-bom.md#L163). The inventory's R-65 text covers only changed checksum fields. Should R-65 (or a new rule) include creating and deleting lines?
3. **R-Detail_View-52 / -53:** where should the effect of Setup Quantity and Rounding Multiple be checked (BOM tab, build order required quantity)? If only in Build Orders, are these depth gaps out of scope for this functionality?
4. **R-Detail_View-64:** is the multi-level BOM rule in scope for this functionality, or for a separate BOM structure / Build Orders functionality?
5. **Q-Detail_View-04 follow-up:** if a range is defined for Quantity, Attrition or Rounding Multiple (including whether Rounding Multiple `0` is allowed), on-limit and just-inside cases will be needed beyond 009, 014 and 016.
