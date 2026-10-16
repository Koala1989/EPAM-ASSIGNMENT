# Review: Part creation form validation: invalid Link URL, leading/trailing whitespace in Name, whitespace-only Revision and Description (UI), 2026-10-15

**Cases reviewed:** UI-Part-065, UI-Part-066, UI-Part-067, UI-Part-068, UI-Part-069, UI-Part-070, UI-Part-071, UI-Part-072, UI-Part-073 · **Verdict:** Approve (Minor findings only; every case stays Draft until its open questions are answered)

## Coverage

`python tools/coverage_check.py --area Part --area REV --file test-cases/Part_Creation_and_Import/part-creation-form-validation.md`: Rules: 56 · covered: 8 · not cited by any case: 48 · exit 0 (no unknown rule IDs).

| Rule | Cases (this batch) | Gap / Out of scope / Covered | Depth issues |
|---|---|---|---|
| R-Part-17 (Link holds a URL; note: invalid URL or no scheme rejected, "Enter a valid URL.") | UI-Part-065, 066, 067, 068, 069 | Covered | Invalid classes (no scheme, not a URL), on-limit 2000, over-limit 2001 and whitespace-only all present. The valid class is covered by UI-Part-004 (part-creation-flow.md). No 1999 case, but the 2000 limit comes from the schema, not the rule, so it is not required. |
| R-Part-13 (Name is a unique text label) | UI-Part-070, 071 | Covered | Padded Name (070) and padded duplicate (071) present. |
| R-Part-14 (Description) | UI-Part-073 | Covered | None |
| R-Part-15, R-REV-03 (Revision optional; any string) | UI-Part-072 | Covered | None |
| R-Part-05 (form errors block submit) | UI-Part-065, 066, 068 | Covered | None |
| R-Part-01 to 04, 06 to 11, 16, 18 to 41 | none in this batch | Out of scope: other Create Part form flow, initial stock, supplier data, Keywords, import and supplier import functionalities | |
| R-REV-01, 02, 04 to 15 | none | Out of scope: Revisions functionality | |

No gaps. Negative cases are present (065, 066, 068).

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Minor | UI-Part-065, 066, 067, 068, 069 | Seed format / No assumptions | The Requirement field describes the Link schema as "nullable, format uri, maxLength 2000" with no line range. The schema is a `oneOf`: a URI of at most 2000 characters **or** a string of `maxLength: 0` (empty string). The empty-string branch is what supports the 069 proposal (whitespace trimmed to empty and accepted). The other cases in the file give line ranges. | openapi-parts.yaml L4176-L4184; R-VAL-05 states "or an empty string" | Edit the schema reference to "`oneOf`: URI maxLength 2000, or empty string; L4176-L4184". |
| 2 | Minor | UI-Part-065, 066 step 2 | Specific Expected results | "The error 'Enter a valid URL.' is stated for an invalid URL (R-Part-17)" describes the rule, not what the tester sees. It should be an observable outcome, e.g. "The text 'Enter a valid URL.' is shown (R-Part-17). Open: Q-Part-21 (where it is shown...)". | R-Part-17 note; Q-Part-21 | Reword step 2 Expected result. |
| 3 | Minor | UI-Part-069 | Specific Expected results | Step 2 proposes that "the part is created with an empty Link", but no step checks the detail page (UI-Part-067 has a step 3 for this). | Q-Part-22 | Add a step: check that the detail page shows no Link (Proposed, Q-Part-22). |
| 4 | Minor | UI-Part-069, 070, 072, 073 | Technique / Type | Type is `Negative`, but the proposed outcome in each case is acceptance (the value is trimmed and the part is created). This is error-guessing input with an unknown outcome. | Q-Part-14, Q-Part-22 | Architect's choice: keep Negative (unusual input) or set the Type once the questions are answered. |
| 5 | Minor | UI-Part-070 | Fidelity | Cites only R-Part-13 ("unique text label"), which says nothing about whitespace. The case relies only on Q-Part-14, which is correctly marked. If the answer is "rejected", R-Part-05 also applies. | part-views.md L32 | No change needed now. Revisit the citation when Q-Part-14 is answered. |
| 6 | Minor | UI-Part-071 | Seed format (cleanup) | The prerequisite part `QA-<suffix> Existing` is created for this case, but the cleanup only covers "a second part". It does not clearly say to delete the prerequisite part. | Seed: "how to remove the records the case created" | Add: "Cleanup as `admin`: set `QA-<suffix> Existing` (and any second part) inactive, then delete." |
| 7 | Minor | UI-Part-070 | Seed format (cleanup) | If the spaces are kept (the open branch), the stored Name is `  QA-<suffix> Padded  `. The cleanup names the trimmed form only. | Q-Part-14 | Make the cleanup "the part whose Name contains `QA-<suffix> Padded`". |
| 8 | Minor | UI-Part-072 | Automation | "Yes: after Q-Part-19 is answered", but the case also depends on Q-Part-14 and Q-REV-01 (as its Review field shows). | Review field of the case | List all three questions. |
| 9 | Minor | Open-question files | Open-question marking (bookkeeping) | The cases are marked correctly, but the questions' "Affected cases" columns do not list them: Q-Part-14 lacks UI-Part-070, 071, 072, 073; Q-Part-16 lacks 071; Q-Part-18 lacks 073; Q-Part-19 lacks 072; Q-REV-01 lacks 072. Q-Part-21 (065, 066) and Q-Part-22 (067 to 069) are complete. | Part_Creation_and_Import/open-questions.md L19, L21, L23, L24; Revisions/open-questions.md L5 | Architect: update the Affected cases columns (agents may not edit question files after writing). |

No Blocker or Major findings. The users (`engineer` for creation, `admin` for setup and cleanup), the Review fields (Draft · Open question) and the "rule outcome first, then Proposed/Open" pattern are correct in all nine cases.

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-Part-065 | 79 | UI-Part-066 | Keep | Different clause of R-Part-17: "without a scheme" (host-like value) vs "invalid URL" (plain text). |
| UI-Part-066 | 79 | UI-Part-065 | Keep | Same pair, seen from the other side. |
| UI-Part-068 | 51 | UI-Part-045 | Keep | Different field, rule, limit and open question (Link/R-Part-17/2000/Q-Part-22 vs Name/R-Part-05/100/Q-Part-15). |

## Questions for the architect

1. **UI-Part-072 vs R-REV-03.** R-REV-03 says the Revision "can be any string". Five spaces is a string, so the rule could be read as stating the outcome (accepted), with only the trimming open. The case instead keeps "or the form rejects the value" as an open branch. Does R-REV-03 settle acceptance? If yes, step 3 should state acceptance as fact (R-REV-03) and leave only trimming open under Q-Part-14.
2. **UI-Part-065 and 066 rely on an API observation.** The "Enter a valid URL." rejection in the R-Part-17 note was observed through the 1.5.6 API, not the UI and not the docs. The cases state UI rejection as fact (R-Part-05, R-Part-17) and leave only the place and timing of the message to Q-Part-21. Do you accept the inventory note as stating the UI outcome, or should the rejection itself be Proposed until Q-Part-21 is answered?
