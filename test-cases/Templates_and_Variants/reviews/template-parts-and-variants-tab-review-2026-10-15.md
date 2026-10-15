# Review: Template parts and the Variants tab (UI), 2026-10-15

**Cases reviewed:** UI-Part_Template-001 to UI-Part_Template-035 (35 cases, `test-cases/Templates_and_Variants/template-parts-and-variants-tab.md`) · **Verdict:** Changes required

## Coverage

`coverage_check.py --area Part_Template`: Rules: 11 · covered: 11 · not cited by any case: 0 (exit 0, no unknown rule IDs).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-Part_Template-01 | 001, 002, 004, 006, 007 | Covered | None. |
| R-Part_Template-02 | 001, 005, 006 | Covered | Permission case present (005, `reader`). |
| R-Part_Template-03 | 017, 018 | Covered | Negative present (017). |
| R-Part_Template-04 | 008-016, 018 | Covered | Negative and permission cases present (012-016). |
| R-Part_Template-05 | 007, 008, 009, 011, 018, 019 | Covered | None. |
| R-Part_Template-06 | 020-023 | Covered | Negative present (020, 021). |
| R-Part_Template-07 | 024-027 | Covered | None. |
| R-Part_Template-08 | 028 | Covered (partly) | **Gap:** the clause "and their stock items" (part-test.md#L19: "Any stock items of the variant parts will have the same test templates associated with them") has no case. 028 checks only the variant's *Test Templates* tab. |
| R-Part_Template-09 | 029-032, 035 | Covered | Negative present (030). |
| R-Part_Template-10 | 033 | Covered | Negative present (033). |
| R-Part_Template-11 | 034, 035 | Covered | None. |

Cross-referenced rules R-REV-08 to R-REV-10 (Revisions) and R-Detail_View-31 (test names across variants) are out of scope for this functionality (owned by the Revisions and Detail_View test-templates functionalities).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | UI-Part_Template-007 step 2 | No assumptions | States as fact that, after the Template option is switched off, "the variant still exists and still references the template part (R-Part_Template-05)". R-05 says nothing about what happens to variants when the template flag is removed, and Q-Part_Template-04 explicitly lists "variants deleted" as a possible outcome. | R-Part_Template-05 (part-template.md#L20); Q-Part_Template-04 | Edit step 2 to `Not known` / `Proposed` under Q-Part_Template-04. |
| 2 | Major | R-Part_Template-08 | Coverage (depth) | No case checks that a variant's stock items carry the master part's test templates. | part-test.md#L19 | Rerun the creator for the stock-item clause (or confirm it is covered in the Detail_View test-templates cases, e.g. those under Q-Detail_View-49). |
| 3 | Major | UI-Part_Template-029, 030, 031, 032, 033, 034, 035 | Seed format (Prerequisites) | Only the template is described as an Assembly; the variants and sub-variant whose *Bill of Materials* tab is opened are not stated to be Assemblies. The BOM tab is visible only for Assembly parts, so the steps may not be executable as written. Whether a variant inherits Assembly is not stated anywhere. | R-Detail_View-19 (part-views.md#L84) | Edit Prerequisites to make every variant and sub-variant an Assembly (created via the API), or raise a question. |
| 4 | Major | UI-Part_Template-020, 021, 022, 023 (also 024-027 data) | User | `engineer` is used to add stock items; the seed's worked example describes `engineer` as "manage parts, view stock". Adding stock may need stock change permission that `engineer` lacks, so the case may fail for the user, not the rule. | references/seed-manual-test-case.md#L55, demo users table | Confirm `engineer`'s stock role; if view-only, use the least-privileged user that can add stock (or create the first stock item via the API as `admin`). |
| 5 | Major | UI-Part_Template-019 | User | Uses `admin` for deleting a template; `engineer` (part management) is the least-privileged user expected to delete parts. | Seed Prerequisites rule (least-privileged) | Edit User to `engineer`, or state why admin is needed. |
| 6 | Major | UI-Part_Template-019 | No assumptions (Summary) | Summary says the template "can be set inactive and deleted only after its variants are handled": an outcome the docs do not state and that Q-Part_Template-04 leaves open. Steps are correctly `Not known`, so the summary contradicts them. | Q-Part_Template-04 | Reword Summary neutrally ("Deleting a template part that has variants"). |
| 7 | Major | UI-Part_Template-027 step 1 | Rule outcome stated | Expected result is only `Not known`, but R-Part_Template-07 states the outcome: the template's stock includes the stock of **all** variants (an inactive variant is still a variant), i.e. 5. The case's own wording ("the docs say all variants") acknowledges this. | R-Part_Template-07 (part-template.md#L26) | Edit to "5 (R-Part_Template-07). Open: Q-Part_Template-06 (whether inactive variants are excluded)". |
| 8 | Major | UI-Part_Template-018 step 3 | Rule outcome stated | Sub-variant creation is written as `Proposed`, but the cited rules state it: any part can be a Template (R-01), once Template is on variants can be created (R-03), and variant-of-variant is named in R-09 ("variant (or sub-variant)"). | R-Part_Template-01, -03, -09 (part-template.md#L32, #L41; manufacturing-bom.md#L80) | Edit step 3 to state creation as fact, keep Open for the UI details. |
| 9 | Major | UI-Part_Template-035 step 2 | Rule outcome stated | `Proposed` that A1 leaves the variant's BOM once *Inherited* is off; the cited rules state it: only Inherited lines are included in variants, a non-inherited line "is only included in the BOM for Template Part A", and edits to the template line are reflected in variants. | R-Part_Template-09, -11 (manufacturing-bom.md#L80, #L91, #L116) | Edit step 2 to state the outcome as fact, keep Open: Q-Part_Template-08 for marking and the field label. |
| 10 | Major | UI-Part_Template-009 step 3 | No assumptions | "Follow the reference: the detail page of the template opens" is stated as fact; the docs say only that the variant references and shows the relationship. A link is only proposed in Q-Part_Template-09. | part-template.md#L20; Q-Part_Template-09 | Mark step 3 `Proposed, to confirm in Q-Part_Template-09`. |
| 11 | Major | UI-Part_Template-017 step 2 | Specific Expected results | Expected result restates the rule ("Variants can be created only once the Template option is on") instead of an observable outcome. | R-Part_Template-03 | Edit to an observable result (e.g. `Proposed, to confirm in Q-Part_Template-03: QA-<suffix> Plain is not offered`). |
| 12 | Major | UI-Part_Template-034, 035 | Open-question marking | Both edit BOM lines as `engineer`, but the BOM edit permission is open in Q-Detail_View-01, which neither case cites. 034 instead attributes "permissions" to Q-Part_Template-08, which does not ask about permissions. 035 also does not cite Q-Detail_View-02 (how a line is edited). | Q-Detail_View-01, Q-Detail_View-02, Q-Part_Template-08 | Add Q-Detail_View-01 (and Q-Detail_View-02 on 035) to Review; fix the Open text in 034 step 1. |
| 13 | Major | UI-Part_Template-025 | Open-question marking | The template holds stock directly (3 units); whether a template can hold stock is open in Q-Part_Template-05, which the case does not cite. | Q-Part_Template-05 | Add Q-Part_Template-05 to Review and Open text. |
| 14 | Minor | UI-Part_Template-007 step 1 | Rule outcome stated / format | `Not known` used although Q-Part_Template-04 proposes an outcome ("switching off is blocked while variants exist"); the seed says use `Proposed` when something can be proposed. Step 3 states tab hidden as fact although step 1 may have been blocked. | Seed Steps rule; Q-Part_Template-04 | Edit to `Proposed, to confirm in Q-Part_Template-04`; make step 3 conditional. |
| 15 | Minor | UI-Part_Template-019 | Seed format | Step 1 combines two actions (set inactive, delete); step 2 Expected is only an `Open:` note with no `Not known:` prefix; Notes ("delete variants before the template to avoid the unknown outcome") contradict step 1, which provokes that outcome. | Seed Steps rule | Edit. |
| 16 | Minor | UI-Part_Template-001, 004, 005, 007, 018, 032 | Seed format (Requirement) | Steps cite R-Detail_View-08 or R-Part_Template-10 that are not listed in the Requirement field (001, 004, 005, 007, 018 use R-Detail_View-08; 032 step 2 uses R-Part_Template-10). | Seed Requirement rule | Add the cited rules to Requirement. |
| 17 | Minor | UI-Part_Template-032 step 2 | Fidelity | Excluding B1 from sibling Variant B is justified by R-Part_Template-10 ("higher up the chain"), but a sibling is not higher up; the correct basis is R-09's scope (only variants of the defining part). | manufacturing-bom.md#L80, #L113 | Change the citation to R-Part_Template-09. |
| 18 | Minor | UI-Part_Template-004 | Technique / Type | Type `Boundary` but nothing is a boundary (default value of a flag); Technique says Equivalence partitioning. | Seed Type field | Type: Positive. |
| 19 | Minor | UI-Part_Template-011 | Technique | "Boundary value analysis (count of variants = 2)": 2 is a "many" class value, not a boundary. | Seed Technique field | Relabel (Equivalence partitioning, several variants) or use count = 1. |
| 20 | Minor | UI-Part_Template-017 | Seed format (Prerequisites) | Pre-step opens `QA-<suffix> Other`, but step 1 opens `QA-<suffix> Plain`. | | Edit Pre-steps. |
| 21 | Minor | UI-Part_Template-016 | Fidelity / format | Tests general page access for `noaccess` rather than R-Part_Template-04 itself; Pre-steps say "log in through the login form, log in as noaccess" (redundant). Overlaps Q-Detail_View-19 (noaccess on a part page). | R-Part_Template-04 | Consider citing Q-Detail_View-19; tidy Pre-steps. |
| 22 | Minor | UI-Part_Template-022 | Fidelity | Summary says "on a template and its variants", but only two variants get stock; the template is not involved. | R-Part_Template-06 | Reword Summary or add a template step. |
| 23 | Minor | UI-Part_Template-023 | Seed format | Cleanup text names variants and a template; the case creates only `Solo 1`, `Solo 2` and a location. Notes reference "guardrail 1" (writer's internal rule). | | Edit Postconditions and Notes. |
| 24 | Minor | UI-Part_Template-024 to 027 | Seed format (Prerequisites) | Stock is created via `POST /api/stock/` without the location the stock item needs (026, 027 do not say how stock is created). | | Add `QA-<suffix> Location` and the creation method. |
| 25 | Minor | UI-Part_Template-012, 013, 014 | Specific Expected results | Last step ("No new variant row is listed") is stated as fact although it depends on the proposed outcome of the step before. | Q-Part_Template-02 | Prefix with the same `Proposed` label. |
| 26 | Minor | UI-Part_Template-028, 034 | Open-question marking | They cite Q-Detail_View-49 and Q-Detail_View-02, but those questions' Affected cases columns do not list them. | test-cases/Part_Detail_View/open-questions.md | Architect: add the cases to those rows when answering. |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Part_Template-012 | 68 | UI-Part_Template-013 | Keep | Empty name vs whitespace-only name: different invalid classes. |
| UI-Part_Template-013 | 68 | UI-Part_Template-012 | Keep | Whitespace-only tests trimming of a non-empty value. |
| UI-Part_Template-020 | 57 | UI-Part_Template-021 | Keep | Sibling variants vs variant and template. |
| UI-Part_Template-021 | 57 | UI-Part_Template-020 | Keep | Variant vs template; also stock held on the template. |
| UI-Part_Template-024 | 53 | UI-Part_Template-026 | Keep | Direct variants only; 026 is sub-variant, 025 adds template stock. |
| UI-Part_Template-025 | 56 | UI-Part_Template-026 | Keep | Template's own stock plus a direct variant; checks the variant's own figure. |
| UI-Part_Template-026 | 56 | UI-Part_Template-025 | Keep | Stock only on a sub-variant. |
| UI-Part_Template-029 | 55 | UI-Part_Template-031 | Keep | Direct variant vs sub-variant clause. |
| UI-Part_Template-031 | 55 | UI-Part_Template-029 | Keep | Sub-variant clause of R-Part_Template-09. |

## Questions for the architect

1. **R-Detail_View-08 is stronger than its source.** The inventory says the *Variants* tab is visible "only if" the part is a Template; part-views.md#L52 says only "If a part is a Template Part then the Variants tab will be visible". Cases 001, 003, 004, 005, 006, 007 and 018 assert the tab is hidden for non-templates on the strength of "only if". Confirm the inventory wording (you own it), or those assertions become Proposed.
2. **Variants tab listing.** 008 step 4, 011 step 1 and 015 step 1 assert that variants are listed on the template's *Variants* tab (citing R-04 or R-05). The docs never say what the tab shows; this is a reasonable reading, but not stated. Accept it as implied, or have it marked Proposed under Q-Part_Template-07.
3. **Does a variant inherit Assembly / Trackable / Testable from its template?** Cases 020-023, 028 and 029-035 set these flags explicitly on some variants but not others (finding 3). The docs do not say.
4. **`engineer`'s stock permission** (finding 4): can `engineer` add stock items in the 1.5.6 demo data?
5. **Q-Part_Template-03, second part** ("may a variant itself become a template") seems answered by R-Part_Template-01 ("Any part can be set as Template") and manufacturing-bom.md#L80 (sub-variants). Consider answering it from those sources.
