# Evaluation of the AI-agent workflow (DeepEval)

How the agent workflow behind this project was evaluated: the RAG index the agents read requirements from, and the `test-case-creator` agent that writes the manual test cases. All evaluation code is in `evals/`; this page summarises method, results, findings and the fixes they led to. Dates are 2026-10-18 to 2026-10-24.

## Summary

- **Retrieval is accurate when queried as instructed.** Rule-wording queries put the right doc section first for 15 of 15 golden rules (Hit@3 100%, MRR 1.00). Retrieval **cannot tell when the docs have no answer**: near-topic questions the docs do not answer score as high as real answers (up to 0.67), so no similarity floor separates them.
- **The agent's cases are traceable to the docs.** A custom GEval metric found 7 of 8 sampled cases fully traceable; the one failure is a citation gap, not an invented requirement. The metric was validated on planted defects before use; DeepEval's built-in Faithfulness was **rejected** because it passed a planted contradiction with two different judge models.
- **The agent follows its workflow but not all of its instructions.** Across 34 recorded runs, the step order was always right (34/34), but only 45% of RAG lookups used the instructed depth, queries were keyword lists instead of the rule's wording, and 7 runs discarded the lookup's no-match warning. 90.5% of 919 cases are fully seed-conformant.
- **Two agent fixes came out of the evaluation:** a fixed RAG lookup command (`tools/rag/rag_lookup.py`) and an instruction to fill coverage gaps instead of reporting a request as already covered. Both are pending a verification run.
- **Cost:** under $1 of judge credit in total. Most checks are deterministic code and free.

## Approach

| Principle | Applied as |
|---|---|
| Evaluate each layer separately | Retrieval (the agent's input), case content (its output), and its process (how it worked) each have their own metrics, so a failure points to its cause |
| Use code where a rule defines the answer | Hit@k, MRR, workflow order, seed format, lookup coverage: deterministic and free. LLM judges only where judgement is needed |
| Validate every metric before trusting it | Planted defects, natural negative controls, metric unit controls, reruns for stability |
| No new agent runs | Saved cases and Claude Code's session transcripts (46 recorded `test-case-creator` runs) are the evidence |
| Judge each run by the rules in force at the time | Runs before the agent's instructions entered git (2026-10-13) are not judged |

Judge model: Claude Sonnet 4.6 for the agent metrics (Haiku 4.5 proved too lenient, see below); Haiku 4.5 for the retrieval metrics.

## What was evaluated

| # | Question | Metric(s) | Type | Data |
|---|---|---|---|---|
| 1 | Does retrieval return the right doc section? | **Hit@3, MRR** | Code | Golden set: 15 answerable rules, each queried as rule wording and as a paraphrased question |
| 2 | Is the retrieved text useful and complete? | **Contextual Precision, Recall, Relevancy** | LLM judge | Same golden set |
| 3 | Can retrieval signal "no answer"? | No-chunk rate, score distribution | Code | 15 unanswerable questions, checked absent from the docs |
| 4 | Are the agent's Expected results traceable to the docs? | **GEval "Requirement traceability"** (custom) | LLM judge | 8 saved cases (4 Approved, 4 Draft with open questions) + 2 planted defects |
| 5 | Did the agent follow its workflow? | **ToolCorrectness** (order), top-k and output checks | Code | 34 runs that wrote cases |
| 6 | Do the cases follow the seed format and link valid requirements? | **Seed conformance** (custom metric, 12 checks) | Code | All 919 cases |
| 7 | Did the agent verify every rule its cases rely on? | **Rule lookup coverage** (recall, via ToolCorrectness on rule IDs) | Code | Runs from 2026-10-23 (after the lookup fix) |
| 8 | Did each run complete its task? | **TaskCompletion** | LLM judge | 13 runs: 5 that wrote cases, 3 that stopped, 5 interrupted |
| 9 | Are judgement labels (Priority, Type, Automation) consistent? | Agreement with proxies, distributions (report only) | Code | All 919 cases |

## Results

### 1-3. Retrieval (step 4)

| Measure | Rule-wording queries | Paraphrased questions |
|---|---|---|
| Hit@3 | 15/15 (100%) | 14/15 (93%) |
| MRR@3 | 1.00 | 0.73 |
| Contextual Precision (judged) | 1.00 | |
| Contextual Recall (judged) | 1.00 | |
| Contextual Relevancy (judged, tracked) | 0.61 (0.25-1.00) | |

- **No-answer detection fails, by design of vector search.** All 15 unanswerable questions return chunks; their top scores range 0.34-0.67. Near-topic questions score highest ("Which users can lock a part?" retrieves the *Locked Parts* section at 0.67), above the weakest correct answer (0.58). A similarity score measures topic, not whether the text answers the question. **Decision: the floor stays at 0.2**; the protection against assumed requirements is the reader's check that a chunk states the rule (item 4). An earlier recommendation to raise the floor to 0.45, based on 3 easy negatives, was reversed when 12 harder ones were added.
- Relevancy is low because a chunk is a whole doc section; it is tracked, not gated (Precision gates at 0.5, Recall at 0.7).
- Judged scores are from the 2026-10-19 run; the golden answers were since rewritten as one fact per sentence (rerun pending).

### 4. Traceability of the agent's cases (step 5)

Each Expected result is classified: **A** stated in the cited docs, **B** generic UI mechanics, **C** flagged as unconfirmed (`[confirm in app]`, `Proposed`, `Open: Q-..`), **D** none of these, an assumed requirement. A rubric maps the number of D claims to a score; pass at 0.8 means no D claim.

| Case | Score (run 1 / run 2) | Verdict |
|---|---|---|
| UI-REV-002 | 0.6 / 0.5 | **Fail:** step 4 relies on rule R-REV-13 without citing it, and asserts a link that open question Q-REV-07 leaves open |
| UI-Unit_measure-013 | 0.8 / 1.0 | Pass |
| 6 other cases | 1.0 / 1.0 | Pass |

7 of 8 pass, with no verdict change between two runs. The failure was missed by the earlier bulk human approval.

### 5-6. Process and format (step 6, 34 runs, 919 cases)

| Check | Result |
|---|---|
| Workflow order: RAG lookup → write cases → duplicate check → report | **34/34** |
| RAG depth `--top-k 3` as instructed | **21/34 runs; 57 of 126 lookups (45%)**. 67 used 2, 2 used 4 |
| No-match warning kept | **10 of 40 lookup commands, in 7 runs, discarded it** with `2>/dev/null` |
| Open questions saved in the right place | No failures |
| Seed conformance | **832/919 cases (90.5%)** fully conformant. Main gaps: 54 Draft cases cite an open question their Review field does not list; 34 have `Automation: Partial` with no reason |
| Runs that wrote nothing | 1 asked for clarification and 2 found the work covered (correct stops); 5 were interrupted |

**Impact of the depth deviation was measured:** on the golden set, Hit@2 equals Hit@3 (the right section ranks first or second), so the cost is small. The discarded warning matters more: it silently disables the agent's fallback to the docs when a lookup finds nothing.

### 8. Task completion (step 6)

| Group | Scores | Expected | Result |
|---|---|---|---|
| Wrote cases (5) | 0.75-0.95 | pass (≥ 0.7) | 5/5 |
| Interrupted (5, negative controls) | 0.00-0.30 | fail (< 0.5) | 5/5 |
| Stopped (3) | 0.70, 0.50, 0.60 | pass | 1/3 |

The evidence given to the judge was built from transcript facts, not from the agent's report; the lowest writing score (0.75) came from the seed-check result in that evidence, which the agent's own report did not mention. Of the two failures, one is a metric-definition problem (the judge applied the writing criteria to a correct stop); **the other is a real finding**: the run reported the request as already covered while its own report listed an uncovered in-scope rule (R-VAL-17 for non-name fields and updates).

### 9. Judgement labels (report only)

- Priority matches the cited rules' Risk (H→P1, M→P2, L→P3, same definitions) in **56%** of cases; the agent consistently rates lower (193 cases on high-risk rules are P2).
- 13 Negative cases show no rejection or error in their Expected results.
- Automation is `Partial` on 43% of cases.

These are flags for review, not failures: labels are judgements, to be measured against the architect's labels (not yet collected).

## Findings and fixes

| Finding | Evidence | Fix | Status |
|---|---|---|---|
| RAG lookups drifted from the instruction: depth 2 instead of 3, keyword queries, no-match warning discarded | Step 6 trace checks | `tools/rag/rag_lookup.py <rule ID> ...`: the query is the rule's wording from the inventory, depth fixed at 3, NO MATCH printed on stdout with exit code 2; agent step 2.4 now uses it | Done; **verification run pending** |
| A run reported "already covered" while listing an in-scope gap; another judged coverage from case headings only | TaskCompletion, run reports | Agent step 4 starts from the saved cases (`coverage_check.py`, read case content), counts a rule covered only for the requested part, and writes any gap in the same run | Done; **verification run pending** |
| UI-REV-002 relies on an uncited rule and an open question | Traceability metric | Architect's decision (fix the case, or record the finding) | Open |
| 54 Draft cases do not list the open questions they cite; 34 lack an Automation reason | Seed conformance | Not changed (saved cases are only edited on the architect's request) | Open |
| Retrieval cannot detect "no answer" | 15 unanswerable questions | No floor change; the reader-side traceability check is the safeguard | Accepted limit, recorded as an `xfail` test |

Both agent fixes are also recorded in `agents/system-instructions.md` ("How the instructions changed").

## How the metrics were validated

| Method | Used on | What it showed |
|---|---|---|
| **Planted defects** (a real case with one Expected result replaced in memory) | Traceability, Faithfulness | Traceability caught an invented error message and a contradiction. With a Haiku judge it missed the invented message; Sonnet caught it with the same instructions. **Faithfulness passed the contradiction with both judges** (it checks for contradiction, and reads an expected error message as a UI claim), so it was dropped |
| **Natural negative controls** | TaskCompletion | All 5 interrupted runs failed, including one with 48 tool calls and no outcome |
| **Metric unit controls** | Lookup coverage | All, 2 of 3, extra lookup, none → 1.0, 0.667, 1.0, 0.0 at zero cost; kept as tests so a DeepEval upgrade that changes scoring is caught |
| **Reruns** | Traceability | 0 verdict changes; scores moved only within their rubric band |
| **Raw-data checks** | Trace parser, seed checks | Early "findings" (missing duplicate checks, 771 failed link checks) were evaluator bugs and were fixed before reporting: the agent chains steps in one shell command and writes cases through shell scripts |
| **Harder test data** | Score floor | Growing unanswerable questions from 3 to 15 reversed the floor recommendation |

## Limits and open items

- **Not yet evaluated:** uncertainty handling (whether the agent raises an open question when a rule lacks a detail, the key behaviour for "never assume a requirement"); agreement of judgement labels with the architect; the other six agents (reviewer, Playwright and API generators, healer, reviewers).
- **Pending:** verification runs for both fixes; the architect's re-approval of the changed golden set; a judged rerun of retrieval with the one-fact-per-sentence answers.
- **Sample sizes are small** for the judged metrics (8 cases, 13 runs); they demonstrate the method and catch real defects, but are not statistically strong.
- **Historical evidence:** some cases written by early runs were later regenerated, so for a few runs only the report, not the case content, could be checked.

## Reproduce

From `evals/` (one-time setup: a Python venv with `deepeval`, `anthropic`, `chromadb` and `sentence-transformers`, and `ANTHROPIC_API_KEY` in `evals/.env`):

```powershell
.\.venv\Scripts\python.exe run_evals.py            # free suites, about 3 minutes
.\.venv\Scripts\python.exe run_evals.py --judged   # also the judged suites, about $0.40
```

| File | Purpose |
|---|---|
| `golden/retrieval_golden.json` | Retrieval answer key: 15 rules, 15 unanswerable questions |
| `golden/agent_cases_sample.json` | Traceability sample and planted defects |
| `golden/agent_runs_sample.json` | TaskCompletion sample and expected verdicts |
| `test_retrieval.py` | Items 1-3 |
| `test_agent_cases.py` | Item 4 |
| `test_agent_behaviour.py` | Items 5-7 and 9 |
| `test_agent_task_completion.py` | Item 8 |
| `agent_traces.py`, `seed_conformance.py`, `case_sources.py` | Transcript parser, seed checks, shared readers |
| `run_evals.py` | Runs every suite and prints a summary |
| `NOTES.md` | Working notes: metric internals, design decisions, lessons |
