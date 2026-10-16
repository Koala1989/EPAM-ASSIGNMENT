# Review: Duplicate and uniqueness conflicts for parts, revisions and categories (API), 2026-10-16

**Cases reviewed:** API-VAL-124, API-VAL-125, API-VAL-126, API-VAL-127, API-VAL-128, API-VAL-129, API-VAL-130, API-VAL-131, API-VAL-132, API-VAL-133, API-VAL-134, API-VAL-135, API-SEC-051 · **Verdict:** Changes required

## Coverage

`coverage_check.py --area VAL --area SEC` (files: [duplicate-and-uniqueness-conflicts.md](../API_Field_Validation/duplicate-and-uniqueness-conflicts.md), [authentication-and-role-permissions.md](../API_Security_and_Permissions/authentication-and-role-permissions.md)): Rules: 27 · covered: 14 · not cited by any case: 13 · exit code 0 (every cited rule ID exists; the cross-Area IDs R-Part-12, R-Part-13, R-REV-07, R-REL-06, R-REL-10, R-CRUD-xx are in their inventories).

The functionality has no rule of its own: uniqueness is stated only by R-Part-13 ("unique" name), R-REV-07 (unique revision code per original) and is explicitly not stated for IPN (R-Part-12, index Not in docs #1, Not in schema #2) and for category names (R-VAL-13 note). The cases are therefore driven by open questions Q-VAL-03, Q-VAL-20, Q-VAL-25 to Q-VAL-31.

| Rule | Cases | Gap / Out of scope / Covered | Depth issues |
|---|---|---|---|
| R-Part-13 (name unique) | 128, 129, 130, 131, 134, SEC-051 (create exact duplicate: API-VAL-091, other file) | Covered | `PATCH` only changes `name` (128); a collision made by changing `IPN` or `revision` on update, and any duplicate via `PUT` (Q-VAL-27 asks both) have no row or case. Minor. |
| R-Part-12 / R-VAL-03 (IPN) | 124, 125, 128 | Covered | Duplicate IPN on update with the setting off has no case. Minor. |
| R-REV-07 (unique revision code) | 126, 127 | Covered (negative rows present) | Rows do not isolate the rule from the combined name/IPN/revision rule: finding 4. |
| R-VAL-07 (revision string) | 126 | Covered | None |
| R-REL-10 (`revision_of`) | 126, 127 | Covered | None |
| R-VAL-12 / R-CRUD-14 (`duplicate`) | 129 | Covered | None |
| R-VAL-13 (category name; uniqueness not stated) | 131, 132, 133, 135 (create under parent: API-VAL-115; rename: API-VAL-123) | Covered | None |
| R-REL-06 (`parent` nullable) | 132, 133 | Covered | None |
| R-CRUD-05, R-CRUD-10, R-CRUD-11 | 130, 134, 135 | Covered (as setup for the conflict) | None |
| R-SEC-04 | SEC-051 | Covered (blocked user `reader`) | None |
| R-VAL-01 | 128, 130 | Covered | Cited for its uniqueness note only. |
| R-VAL-02, -04, -05, -06, -08, -09, -10, -11, -14, -15, -16, -17, -18 | none | Out of scope: field validation (lengths, types, read-only, write-only, content types, initial stock), reviewed under "Part field validation" and "Category field validation". | |
| R-SEC-01 to R-SEC-03, R-SEC-05 to R-SEC-09 | other SEC cases | Out of scope: authentication and permission functionality. | |

404 standing rule: no `{id}` `GET`/`DELETE` operation is the subject of this functionality (the `{id}` calls are `PATCH` under test and `GET`/`DELETE` as setup or verification); their `404` cases sit in CRUD (Q-CRUD-01). No gap. Negative cases: present.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Blocker | API-VAL-129, row `original without IPN` | Rule outcome stated | `count` is `1` as fact. No rule states the copy is refused; the row's own status is only `Proposed, to confirm in Q-VAL-31: 400`. An automated test would assert the assumption. | Q-VAL-31 (Open); R-Part-13 does not settle the combined rule (Doc issue 2, Q-VAL-03) | Edit: `Proposed, to confirm in Q-VAL-31: 1`. |
| 2 | Blocker | API-VAL-132, rows `parent holds same name` and `top level holds same name` | Rule outcome stated | `parent after` is `<pk of B>` as fact, which holds only if the move is refused; refusal is only proposed (Q-VAL-30) and no rule states sibling-name uniqueness (R-VAL-13 note). | R-VAL-13 note "Uniqueness among sibling categories not stated"; Q-VAL-30 (Open) | Edit: `Proposed, to confirm in Q-VAL-30: <pk of B>`. |
| 3 | Major | API-VAL-130, step 4 | Fidelity | `GET` with `active=false` can never count the step 3 part (a new part is active, R-CRUD-11), so `count` is `1` whatever step 3 did; the check on whether a duplicate was created is only in Notes as a conditional extra listing. The case's key outcome is not verified by any step. | R-CRUD-11; step 4 and Notes of the case | Edit: list without the `active` filter (`search=QA-<suffix> Retired`) with `count` `Proposed, to confirm in Q-VAL-28: 1`, or add that step to the table. |
| 4 | Major | API-VAL-126 (row `same code same original`), API-VAL-127 (row `sibling's code`) | Fidelity / No assumptions | The revisions use the original's name and no IPN, so the conflicting row is also an exact name + IPN + revision duplicate (Q-VAL-03). A `400` cannot be attributed to R-REV-07, and the error key may come from the other rule. The Notes justify the shared name with "A revision keeps the name of its original (part-revision.md#L23)"; L23 says only that a revision is a part linked to the original, not that it keeps the name. | [part-revision.md#L23](../../requirements/docs/part-revision.md#L23), [#L37](../../requirements/docs/part-revision.md#L37); Q-VAL-03 | Edit: give each revision a distinct name or IPN so only the revision code collides; remove the unsupported Notes sentence. Or ask the architect (question 1). |
| 5 | Major | API-VAL-128 | Open-question marking | Step 1 relies on two parts sharing IPN `QA-<suffix>-R1` and marks `Open: Q-VAL-25`, but Review is `Draft · Open question: Q-VAL-03, Q-VAL-27` without Q-VAL-25. If duplicate IPNs are refused the case cannot be set up. | Q-VAL-25; step 1 of the case | Edit the Review field to add Q-VAL-25; add API-VAL-128 to Q-VAL-25's Affected cases (architect). |
| 6 | Major | API-VAL-131 | Open-question marking | Notes say the case "depends on both" Q-VAL-03 and Q-VAL-20, and the `category` row is a top-level duplicate (Q-VAL-30 (a)); Review lists only Q-VAL-29. | Q-VAL-29 text ("Depends on the duplicate rules (Q-VAL-03, Q-VAL-20)"); Q-VAL-30 | Edit the Review field: `Draft · Open question: Q-VAL-29, Q-VAL-03, Q-VAL-20, Q-VAL-30`. |
| 7 | Minor | API-VAL-125, Summary | Fidelity (wording) | "the instance setting that forbids duplicate IPNs switched off" is the opposite of the Prerequisites ("the setting that allows duplicate IPNs = off"); a tester following the Summary would allow duplicates. | Prerequisites of the case; findings F-05 (`PART_ALLOW_DUPLICATE_IPN`) | Edit the Summary: "the setting that allows duplicate IPNs switched off". |
| 8 | Minor | API-VAL-131 | Seed format / One behaviour | Step 1 sends two calls in one step (seed: one call per step; inherent to a race, but say so). The status columns are `accepted status` / `other status` rather than `expected status` or `step N status`. The two rows test two different rules (part name, R-Part-13; category name, R-VAL-13) with different open questions. | Seed "Steps" and "Data sets" rules | Consider renaming the columns and noting the two-call step; architect decides whether to split part and category. |
| 9 | Minor | API-VAL-134, API-VAL-135 | User | Every step runs as `admin`; the request under test (the re-create, step 5 / step 4) can be made by `engineer`. Delete as setup by `admin` is fine. | Seed Prerequisites: least-privileged user | Edit: run the re-create step as `engineer`. |
| 10 | Minor | API-VAL-127 | Seed format | Step 1 records only the `pk` of revisions B and C; cleanup deletes "each of the three", including the original whose `pk` is not recorded. | Case step 1 and cleanup | Edit: record the original's `pk`. |
| 11 | Minor | API-SEC-051 | Technique | "Negative (forbidden create as `reader`)" is a case type, not a technique; the case is a decision-table column (add permission missing) plus error guessing. | Seed Technique field | Edit the label. |
| 12 | Minor | API-VAL-134, API-VAL-135, API-SEC-051 | Open-question marking | Each depends on whether a duplicate is refused at all (Q-VAL-03 for parts, Q-VAL-20 for categories): if not, the re-create (134, 135) is trivially accepted and the precedence check (SEC-051) has no duplicate error to lose to. Not listed in Review. | Q-VAL-03, Q-VAL-20 | Consider adding them. |
| 13 | Minor | Open-question files | Bookkeeping | Affected cases columns miss cases that cite the question: Q-VAL-03 (128, 129, 130, 131), Q-VAL-20 (131, 132, 133), Q-VAL-25 (128), Q-REL-08 (126, 127), Q-REV-06 (126), Q-SEC-06 (SEC-051). | [open-question_VAL.md](../Open_Questions/open-question_VAL.md), [open-question_REL.md](../Open_Questions/open-question_REL.md), [open-question_REV.md](../Open_Questions/open-question_REV.md), [open-question_SEC.md](../Open_Questions/open-question_SEC.md) | Architect updates the question files. |
| 14 | Minor | R-Part-13 / R-Part-12 depth | Coverage depth | No row or case for: `PATCH` changing `IPN` or `revision` into a full collision; duplicate via `PUT`; duplicate IPN on update with the setting off. | Q-VAL-27 ("`PATCH` or `PUT` ... changes `name`, `IPN` or `revision`"), Q-VAL-25 | Optional: rerun the creator for these rows. |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| API-VAL-124 | 69 | API-VAL-125 | Keep | Setting at default versus switched off; proposed 201 versus 400. |
| API-VAL-125 | 69 | API-VAL-124 | Keep | Setting switched off versus default; proposed 400 versus 201; adds the empty-IPN step. |
| API-VAL-126 | 50 | API-VAL-127 | Keep | New revision created (`POST`) versus existing revision relabelled (`PATCH`); different rows. |
| API-VAL-127 | 50 | API-VAL-126 | Keep | `PATCH` of an existing revision versus `POST` of a new one; own-code row. |
| API-VAL-133 | 53 | API-VAL-115 (53), API-VAL-113 (50) | Keep | Top level (`parent` absent or `null`) versus a named parent; name uniqueness versus wrong types. |
| API-SEC-051 | 52 | API-SEC-019 | Keep | An existing duplicate part is in place and the case checks which error wins (Q-SEC-06). |

## Questions for the architect

1. API-VAL-126 and API-VAL-127 give revisions the original's name and say a revision "keeps the name of its original". The docs do not say this (part-revision.md#L23). Must a revision share the original's name and IPN in 1.5.6, or should the cases give revisions a distinct name or IPN so they test R-REV-07 alone (finding 4)?
2. API-VAL-124 is typed Negative because the brief lists duplicate IPN as negative, but its proposed outcome is acceptance (`201`). Keep Negative, or retype it Positive under the default setting?
3. Index "Not in schema #2" says the app "enforces name + IPN + revision together", citing findings F-04. F-04 only says this is the likely rule and that rejection is still to be confirmed. Should the index wording be softened to match Q-VAL-03 being open?
