# Reviewer catches: what the creator missed

Every Blocker and Major that `test-case-reviewer` (Opus 5.5) found in cases written by `test-case-creator` (Sonnet 5.5), with a short note on why the creator likely missed it. It shows what the independent review adds, and it drives the changes to the creator's instructions.

Source: the review files in `test-cases/<Area folder>/reviews/`, up to 2026-10-15. "Likely why" is the architect's diagnosis, not the creator's own reasoning (the creator does not explain each case).

## Summary

**74 findings in 14 reviews: 10 Blockers, 64 Majors. 24 resolved (14 fixed, 10 covered by later runs), 50 open.** None would have been caught by the creator's own checks or by the duplicate script.

### By severity

| Severity | Total | Resolved | Open |
|---|---|---|---|
| **Blocker** | 10 | 2 | 8 |
| **Major** | 64 | 22 | 42 |
| Total | 74 | 24 | 50 |

### By category

| Category | Blockers | Majors | Typical miss | Likely why |
|---|---|---|---|---|
| Assumption stated as fact | 9 (2 resolved, 7 open) | 14 (6 resolved, 8 open) | An outcome the docs do not give is written as the expected result ("the line is not saved", "search matches part of a word") | The model fills gaps with plausible InvenTree behaviour; plausible reads as known. |
| Coverage gap or depth | 0 | 24 (10 resolved, 14 open) | A rule with no case, or only one side of it: no boundary on the limit, no negative, no blocked user, no "hidden when" case | The creator plans by rule, not by every clause and class in the rule; long rule lists get thinned out. |
| Open-question bookkeeping | 0 | 10 (1 resolved, 9 open) | A case uses a question but its Review field or the question's Affected cases do not list it, or the reverse | Several files must agree (step, Review field, question row); nothing checks them against each other. |
| Wrong rule citation | 0 | 4 (2 resolved, 2 open) | A case cites a neighbouring rule (R-Part-23 for R-Part-28, the BOM tab rule for Build Orders) | Similar wording between rules; the citation is picked by topic, not by clause. |
| Rule outcome not stated | 0 | 3 (2 resolved, 1 open) | The rule gives the outcome, but the case marks it Proposed or Not known | Over-caution: any open detail made the whole step uncertain. |
| Not observable | 0 | 4 (0 resolved, 4 open) | The Expected result restates the rule ("plugins can lock lists") instead of what the tester sees | Writing from the rule text rather than from the screen. |
| Wrong test setup | 1 (0 resolved, 1 open) | 3 (0 resolved, 3 open) | A user who lacks the permission, a setting left as None, a cleanup a locked part blocks | The user table and settings are read once; their effect on each case is not checked. |
| Tooling limits | 0 | 2 (1 resolved, 1 open) | A duplicate across Areas; two runs giving the same question IDs | `dedupe_cases.py` compares within an Area; two runs in one Area at the same time. |

## Blockers

All 10 Blockers in one place. A Blocker is a case that would mislead the tester: a wrong Expected result, or an assumption presented as a requirement.

| Review | Case | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|
| API Field Validation | API-VAL-061 | Assumed an unlisted content type is rejected; the rule only lists accepted types. | Read "accepted as X, Y, Z" as "only X, Y, Z". | Assumption | Open |
| API Lists and Filters | API-LST-028 | Asserts a partial-word search match, which Q-LST-03 leaves open. | Assumed typical search behaviour. | Assumption | Open |
| API Lists and Filters | API-LST-035 | Assumes partial matching for category search; no source or question. | Same assumption, carried to another endpoint. | Assumption | Open |
| API Lists and Filters | API-LST-040 | Asserts a result that depends on Q-LST-03; not marked. | Did not see its own search term as a fragment. | Assumption | Open |
| Attributes | UI-ATT-070 | Adds a non-Component part to a BOM and expects success (open in Q-ATT-05). | Forgot to set Component, unlike sibling cases. | Assumption | Open |
| Attributes | UI-ATT-005, 021 to 039, 048 | Creates stock as `engineer`, who cannot; negatives would pass for the wrong reason. | User picked by habit, not by the permission the action needs. | Setup | Open |
| Categories | UI-Categories-003 | "Create and edit controls are hidden" taken from the seed's demo-user table. | The seed's "Use for" column read as a requirement. | Assumption | **Resolved**: fixed (checked live with MCP, F-13, Q-Categories-03) |
| Part Detail View: BOM editing and validation | UI-Detail_View-024, 025, 027 | "No Validate BOM button once validated" stated as fact; Q-06 asks it. | Inferred the reverse of a documented condition. | Assumption | Open |
| Part Detail View: BOM contents, calculations, substitutes, Excel import | UI-Detail_View-233 | Summary presents "a component may appear once" as a requirement; Q-04 asks it. | Summary written as fact, steps hedged. | Assumption | **Resolved**: fixed |
| Units of Measure | UI-Unit_measure-026 | Expects an incompatible unit to be rejected; the docs only say compatible units are allowed. | Read "allowed" as "only allowed"; Notes even admit "implied". | Assumption | Open |

## Changes made from these findings

| Date | Change | Prompted by |
|---|---|---|
| 2026-10-14 | Creator: Expected result states the rule's outcome first, then `Open: Q-...`; `Proposed, to confirm in Q-...` for outcomes no rule gives; bare `Not known` only as a last resort. Reviewer: new "Rule outcome stated" check. | 128 bare `Not known` results; Categories #2 |
| 2026-10-14 | Creator: negative depth for every functionality (blocked user, error guessing on inputs, the opposite of every "only / cannot / visible only if"). Reviewer: no Negative case at all is a Major. | Categories review (all 7 cases Positive) |
| 2026-10-15 | Creator: a setting, control or page the docs do not name is never a reason to skip a rule; write the case with `[open: Q-...]`. | Parameters F2 (R-Part_Params-32) |
| 2026-10-15 | Run guidance: never run two generations in the same Area at once. | Return Orders #1 (duplicate question IDs) |
| 2026-10-15 | Creator, guardrail 1: never infer the opposite of a rule. Without `only`, `must`, `cannot`, `never` or `not`, the opposite outcome is `Proposed`; "only if" is one-directional. Five past mistakes as worked examples. Negative depth: opposite cases of positively worded rules are written with a `Proposed` outcome. | Blockers API-VAL-061, UI-Detail_View-024/025/027, UI-Unit_measure-026 (cause A: inferring the opposite) |

**Candidates for the next change:** a script that checks open-question bookkeeping (10 findings); `dedupe_cases.py` comparing across Areas (Parameters F9); the seed's demo-user table reworded so "Use for" is not read as behaviour (Categories #1); the creator checking each case's user against the permission it needs (Attributes F2).

## All findings

Resolution: **Resolved**, either fixed (the case was edited) or covered (a later run added the missing cases); or **Open** (not yet acted on). Checked against the case files on 2026-10-15.

### API Field Validation (2026-10-14)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| 1 | Blocker | API-VAL-061 | Assumed an unlisted content type is rejected; the rule only lists accepted types. | Read "accepted as X, Y, Z" as "only X, Y, Z". | Assumption | Open |
| 2 | Major | R-VAL-10 | No wrong-type case for `revision_of`, `responsible`. | Long field list in one rule; last items dropped. | Coverage | Open |
| 3 | Major | R-VAL-18 | 6 decimal places tested, 5 (on the limit) not. | Boundary done above the limit only. | Coverage | Open |
| 4 | Major | R-VAL-17 | The "update" half of the rule has no case. | Two-clause rule; second clause skipped. | Coverage | Open |
| 5 | Major | API-VAL-043, 062 to 067 | `initial_stock` sent as `engineer` with Settings None; ignores the setting and stock permission. | Setting and permission effect not checked per case. | Setup | Open |
| 6 | Major | API-VAL-055 | Expected `pathstring` value not stated by any source. | Filled with the obvious value. | Assumption | Open |

### API Lists and Filters (2026-10-14)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| 1 | Blocker | API-LST-028 | Asserts a partial-word search match, which Q-LST-03 leaves open. | Assumed typical search behaviour. | Assumption | Open |
| 2 | Blocker | API-LST-035 | Assumes partial matching for category search; no source or question. | Same assumption, carried to another endpoint. | Assumption | Open |
| 3 | Blocker | API-LST-040 | Asserts a result that depends on Q-LST-03; not marked. | Did not see its own search term as a fragment. | Assumption | Open |
| 4 | Major | 30+ cases (systemic) | Every case combines filters, which R-LST-13 says to confirm first (Q-LST-07). | Combining filters felt too basic to question. | Assumption | Open |
| 5 | Major | API-LST-060, 061 | Cleanup edits a locked part, which cannot be edited. | Cleanup copied from a template, not checked against the data. | Setup | Open |
| 6 | Major | API-LST-064 | Uses a fragment search; marked only Q-LST-07. | Bookkeeping of a second question. | Bookkeeping | Open |
| 7 | Major | API-LST-007, 011, 045 | States outcomes before the Not known clause that no source gives. | Wrote the likely result, then hedged. | Assumption | Open |
| 8 | Major | R-LST-04 | No search case on MPN, revision, SKU, tag name, tag slug. | Ten search fields; only the first few used. | Coverage | Open |
| 9 | Major | R-LST-15 | No case for the category `starred` filter. | Minor-looking field skipped. | Coverage | Open |
| 10 | Major | R-LST-16 | No category search on `description`. | Same. | Coverage | Open |

### API Relationships (2026-10-14)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| 1 | Major | R-REL-09 | No on-limit case for `sku`; none for `mpn`. | Boundaries done for one field only. | Coverage | Open |
| 2 | Major | API-REL-042 | Expects something no step can observe. | Wrote the conclusion, not a check. | Not observable | Open |
| 3 | Major | API-REL-026 | Summary states what Q-REL-05 asks; baseline values never used. | Summary written before the questions. | Assumption | Open |
| 4 | Major | API-REL-035, 036 | Same setup as 027 to 034, but not marked Q-REL-06. | Inconsistent marking across similar cases. | Bookkeeping | Open |

### Attributes (2026-10-13)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| F1 | Blocker | UI-ATT-070 | Adds a non-Component part to a BOM and expects success (open in Q-ATT-05). | Forgot to set Component, unlike sibling cases. | Assumption | Open |
| F2 | Blocker / Major | UI-ATT-005, 021 to 039, 048 | Creates stock as `engineer`, who cannot; negatives would pass for the wrong reason. | User picked by habit, not by the permission the action needs. | Setup | Open |
| F3 | Major | UI-ATT-007 | Transfer Orders tab may be hidden by a setting, so Virtual is not what is tested. | The rule's second condition ("or the feature is off") ignored. | Wrong citation | Open |
| F4 | Major | UI-ATT-052 to 054 | Same check as 050, which is marked Q-ATT-15; these are not. | Inconsistent marking. | Bookkeeping | Open |

### Categories (2026-10-14)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| 1 | Blocker | UI-Categories-003 | "Create and edit controls are hidden" taken from the seed's demo-user table. | The seed's "Use for" column read as a requirement. | Assumption | **Resolved**: fixed (checked live with MCP, F-13, Q-Categories-03) |
| 2 | Major | UI-Categories-006 | Used "the architect's request" as the source of an outcome. | The request treated as a requirement. | Assumption | **Resolved**: fixed (now Proposed) |
| 3 | Major | UI-Categories-004 | Relies on an active-state filter the docs do not name; not marked. | Hedged in text instead of raising a question. | Assumption | Open |

### Parameters: tab, templates and category parameters (2026-10-15)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| F1 | Major | UI-Part_Params-005 to 008, 012, 013, 018 | Use Q-Part_Params-01 in steps but not in the Review field. | Bookkeeping across step and Review field. | Bookkeeping | Open |
| F2 | Major | R-Part_Params-32 | No case for "unit validation can be disabled". | The setting is not named, so the case seemed unwritable. | Coverage | **Resolved**: covered |
| F3 | Major | R-Part_Params-06 | Only the blank Model Type class tested. | One class per rule. | Coverage | Open |
| F4 | Major | R-Part_Params-09 | Only the negative case; no accepted value. | Negative written, positive assumed obvious. | Coverage | **Resolved**: covered (UI-Part_Params-061) |
| F5 | Major | R-Part_Params-13 | The doc's distinguishing example (same value on another model type) untested. | Tested what both options reject, not where they differ. | Coverage | Open |
| F6 | Major | R-Part_Params-36 | No case for selection lists in the Admin Center. | Admin Center seen as outside "templates". | Coverage | **Resolved**: covered |
| F7 | Major | UI-Part_Params-008 | Only Not known, though two rules give the outcome. | Did not combine rules from two Areas. | Rule outcome not stated | Open |
| F8 | Major | UI-Part_Params-034 | Assumes unit validation is on; setting unnamed, no question. | Noted the assumption instead of raising it. | Assumption | **Resolved**: fixed (setting marked `[open: Q-Part_Params-14]`) |
| F9 | Major | UI-Part_Params-035 | Duplicates UI-ATT-059 in another Area. | `dedupe_cases.py` compares within an Area. | Tooling | Open |

### Parameters: unit validation and selection lists (2026-10-15)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| 1 | Major | UI-Part_Params-060 | No template or part in Prerequisites; cites a rule not in Requirement. | Setup written from the step, not checked. | Bookkeeping | Open |
| 2 | Major | UI-Part_Params-063 | Expected result restates the rule, nothing observable. | Wrote the rule, not the screen. | Not observable | Open |

### Part import (2026-10-13)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| 1 | Major | UI-Part-026 | Cites the mapping rule, but tests upload handling. | Picked the nearest rule; no rule covers file types. | Wrong citation | Open |
| 2 | Major | UI-Part-026 | Summary states an outcome the steps leave unknown. | Summary written first. | Assumption | Open |
| 4 | Major | R-Part-29 | No negative: a Pending row is not imported. | "Must" rule without its negative. | Coverage | Open |
| 5 | Major | R-Part-19 | No staff user without `change` permission. | Permission rule without its blocked user. | Coverage | Open |

### Part Detail View: BOM editing and validation (2026-10-15)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| 1 | Blocker | UI-Detail_View-024, 025, 027 | "No Validate BOM button once validated" stated as fact; Q-06 asks it. | Inferred the reverse of a documented condition. | Assumption | Open |
| 2 | Major | R-Detail_View-19 | No case: BOM tab hidden when Assembly is off. | "Visible only if" without its hidden case. | Coverage | **Resolved**: covered (UI-Detail_View-100) |
| 3 | Major | R-Detail_View-65 | No case changes a line's component (a listed checksum field). | Long field list; one item dropped. | Coverage | **Resolved**: covered (UI-Detail_View-077) |
| 4 | Major | R-Detail_View-64 | No multi-level BOM case. | Scoped out as "structure". | Coverage | **Resolved**: covered (UI-Detail_View-051 to 055) |
| 5 | Major | R-Detail_View-52, 53 | Only invalid inputs; the calculation itself untested. | Negatives first; the positive calculation left. | Coverage | **Resolved**: covered (UI-Detail_View-206 to 212) |
| 6 | Major | UI-Detail_View-025, 027 to 029, 031, 032 | Edit a line but not marked Q-02 (how a line is edited). | Bookkeeping. | Bookkeeping | Open |
| 7 | Major | UI-Detail_View-006 | Uses Q-04 in test data; not in Review field. | Bookkeeping. | Bookkeeping | Open |

### Part Detail View: BOM lines, multi-level, import, comparison, replace (2026-10-15)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| F1 | Major | R-Detail_View-57, 58 | No line with two or more substitutes. | "Several" tested with one. | Coverage | **Resolved**: covered (UI-Detail_View-216 and later) |
| F2 | Major | R-Detail_View-61 | Only CSV imported; the rule names Excel too. | One file class per rule. | Coverage | **Resolved**: covered (Excel import run) |
| F3 | Major | UI-Detail_View-061 | "Not Validated" marked Proposed; the rules state it. | Over-caution after an import question. | Rule outcome not stated | **Resolved**: fixed |
| F4 | Major | UI-Detail_View-077 | Same as F3 for a component change. | Same. | Rule outcome not stated | **Resolved**: fixed |
| F5 | Major | UI-Detail_View-079 | Credited a rule with "replaced on confirmation"; contradicts step 1. | Made the rule say what the case needed. | Assumption | **Resolved**: fixed |
| F6 | Major | UI-Detail_View-050 | "The substitute is removed" stated as fact; no rule covers removing. | The obvious inverse of "add". | Assumption | **Resolved**: fixed |
| F7 | Major | 038 to 079 | View-only cases marked with an edit question; dependent cases missing from question rows. | Question copied to every case in the file. | Bookkeeping | Open |

### Part Detail View: BOM contents, calculations, substitutes, Excel import (2026-10-15)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| F-01 | Blocker | UI-Detail_View-233 | Summary presents "a component may appear once" as a requirement; Q-04 asks it. | Summary written as fact, steps hedged. | Assumption | **Resolved**: fixed |
| F-02 | Major | UI-Detail_View-209 to 211 | Required quantities stated as fact; the formula is open (Q-41). | Rounding is stated, so the whole value felt known. | Assumption | **Resolved**: fixed |
| F-03 | Major | UI-Detail_View-216 | "Allocation is saved" stated; splitting it is open (Q-44). | Asked the question, then assumed its answer. | Assumption | **Resolved**: fixed |
| F-04 | Major | UI-Detail_View-223 | Cited R-Part-23 (related fields) for header mapping (R-Part-28). | Similar wording ("map manually"). | Wrong citation | **Resolved**: fixed |

### Part Detail View: header details and tab visibility (2026-10-15)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| 1 | Major | UI-Detail_View-104 | Cited the BOM tab rule for the Build Orders tab. | Neighbouring rule, same "Assembly" condition. | Wrong citation | **Resolved**: fixed |
| 2 | Major | UI-Detail_View-091, 092, 113 | Marked with permission questions that cannot change an `allaccess` result. | Question applied to every case on the tab. | Bookkeeping | **Resolved**: fixed |
| 3 | Major | R-Detail_View-26, 27, 30 | No case for Return Orders, Transfer Orders, Test Results visibility. | Request named only Allocated and Build Orders. | Coverage | **Resolved**: covered (UI-Detail_View-115 to 127) |

### Part Detail View: Return Orders, Transfer Orders and Test Results tabs (2026-10-15)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| 1 | Major | UI-Detail_View-115 to 127 | Q-Detail_View-22 and 23 defined twice in `open-questions.md`. | Two generation runs in the same Area at the same time. | Tooling | **Resolved**: fixed (renumbered 40 to 44) |
| 2 | Major | R-Detail_View-30 | Test Results table only checked empty. | Visibility tested, content clause left. | Coverage | Open |

### Units of Measure (2026-10-14)

| # | Sev. | Case or rule | What was missed | Likely why | Category | Resolution |
|---|---|---|---|---|---|---|
| 1 | Blocker | UI-Unit_measure-026 | Expects an incompatible unit to be rejected; the docs only say compatible units are allowed. | Read "allowed" as "only allowed"; Notes even admit "implied". | Assumption | Open |
| 2 | Major | UI-Unit_measure-007, 013, 015, 017 | "Is not saved" asserted; the docs say only "an error is shown". | Error assumed to block saving. | Assumption | Open |
| 3 | Major | R-Unit_measure-14 | Only the alias class of three tested. | One class per rule. | Coverage | Open |
| 4 | Major | R-Unit_measure-13 | No case edits a custom unit; 019's Summary claims it. | Summary broader than the steps. | Coverage | Open |
| 5 | Major | UI-Unit_measure-022 | Expects the list to show dimensionality; not documented. | Assumed a UI detail. | Assumption | Open |
| 6 | Major | UI-Unit_measure-018 | Meanings (12, 100, 1000) restated, never observed. | Wrote the rule, not a check. | Not observable | Open |
| 7 | Major | UI-Unit_measure-003 | "Quantities are dimensionless pieces" is not observable. | Same. | Not observable | Open |
| 8 | Major | UI-Unit_measure-008 | Uses Q-02 in test data; not in Review field; Q-04 unused. | Bookkeeping. | Bookkeeping | Open |
| 9 | Major | UI-Unit_measure-011 to 013, 016, 017 | Part's unit not set, so results may depend on R-Unit_measure-17. | Starting state left implicit. | Setup | Open |

## Keeping this list up to date

After each `/gen-test-cases` run, add the review's Blockers and Majors here with a "likely why", and update Resolution when a case is fixed or a later run covers the gap. Recurring causes go into "Candidates for the next change".
