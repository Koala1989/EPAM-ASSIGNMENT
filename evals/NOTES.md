# LLM evaluation with DeepEval: review notes

Notes from setting up `evals/` (steps 1–4, 2026-10-18 to 2026-10-19). The examples are from this project: the RAG index over the InvenTree docs (`tools/rag/`) and the test-case-creator agent.

---

## 1. The core idea

DeepEval is **pytest for LLM output**. A Playwright test asserts exact values; an LLM eval scores fuzzy output from 0 to 1 and passes it against a threshold.

| DeepEval | Playwright equivalent |
|---|---|
| `LLMTestCase` | One test's data |
| `input` | The steps you performed |
| `actual_output` | What the app showed (the system's real output) |
| `expected_output` | The Expected result in the manual case (your answer key) |
| `retrieval_context` | The doc text the system retrieved |
| Metric, with a threshold | The assertion |
| `assert_test(case, metrics)` | `expect(...)`: fails if any metric scores below its threshold |
| `deepeval test run file.py` | `npx playwright test`: pytest plus a results table and the cost |

**Three building blocks in every eval:** the **judge** (who scores), the **test case** (what's scored), the **metric** (how it's scored, and what counts as a pass).

**Not every metric needs `expected_output`:**
- *Is it correct or complete?* needs an answer key: Contextual Precision, Contextual Recall, Answer Correctness.
- *Is it on-topic or grounded?* doesn't: Answer Relevancy, Faithfulness, Contextual Relevancy.

The step 2 smoke test showed the trap: Answer Relevancy gave 1.0 to an on-topic answer, and would give the same to an on-topic **wrong** answer. Relevance isn't truth.

### Where DeepEval acts in `test_retrieval.py`

Only in the judged layer. The free layer (Hit@3, MRR, unanswerable checks) is plain pytest.

| Line | Code | Whose code | What happens |
|---|---|---|---|
| 26–33 | `from deepeval import ...` | DeepEval | Imports only |
| 133 | `judge = AnthropicModel(model="claude-haiku-4-5")` | DeepEval | Picks the judge, reads the key from `.env`. No API call yet |
| 140–144 | `METRICS = [ContextualPrecisionMetric(model=judge, threshold=0.5, ...), ...]` | DeepEval | Configures the metrics: judge, pass mark, reason on or off |
| 151 | `hits = search(RULE_TEXT[...], top_k=TOP_K)` | **Yours** | The system under test runs. DeepEval isn't involved |
| 152–157 | `case = LLMTestCase(input=..., expected_output=..., retrieval_context=[...])` | DeepEval | Packages the evidence (chunks in rank order). No API call yet |
| **158** | **`assert_test(case, METRICS)`** | DeepEval | **All the judging happens here** |

Inside `assert_test`:
```
for each metric:
    metric.measure(case)
        ├─ builds its prompt from the case fields
        ├─ calls the judge (the API calls that cost credit)
        ├─ turns the yes/no verdicts into a 0–1 score using the formula
        ├─ one more call writes the reason (include_reason=True)
        └─ success = score >= threshold
records scores, reasons and cost for the run report
any metric failed → AssertionError → pytest marks the test FAILED
```

`deepeval test run` is pytest plus a plugin: it prints the results table and cost, and saves `.deepeval/.latest_test_run.json`. Plain `pytest` still judges, but shows no table.

**In short:** line 151 runs your system, line 152 packages the result, line 158 judges it.

---

## 2. The judge (LLM-as-a-judge)

- Most metrics ask an LLM to read the text and decide. It's usually a fixed recipe: split into statements → give a verdict on each one → score = the share that pass → write a reason.
- **Temperature** controls randomness when picking the next word. 0 gives the most repeatable output, which is what you want for judging. **In this setup it can't be set**: the installed Anthropic SDK (1.15.0) rejects it. So expect small score differences between runs, leave margin in thresholds, and rerun a borderline score before trusting it.
- **Judge noise is real:** for G-15 the judge said the context didn't clarify uniqueness while quoting "*(unique) text label*". One score never decides alone.
- **Judge choice:** Claude Haiku 4.5 (cheap, and on DeepEval's built-in price list, so runs report their cost).

### Setup gotchas you hit

| Problem | Cause | Fix |
|---|---|---|
| Script printed nothing | File not saved (0 bytes on disk) | Ctrl+S, or turn on Auto Save |
| `unexpected keyword argument 'temperature'` | Anthropic SDK 1.15 removed it | Don't pass `temperature` |
| `API key is not scoped to a workspace` | The key was created at org level | Create the key inside a workspace in the Console |
| `UnicodeEncodeError ... '⚠'` | The Windows console (cp1252) can't print DeepEval's emoji | `$env:PYTHONUTF8 = "1"` before running |
| Results table squashed | The table fits the terminal width | Widen the terminal, or read `.deepeval/.latest_test_run.json` |

**Billing:** a Claude Pro or Max subscription does **not** pay for API calls. The API needs prepaid credits in console.anthropic.com (you added $5 with a $3 monthly limit). There's no free OpenAI API tier; free alternatives are Groq (hosts OpenAI's open `gpt-oss`), the Gemini free tier, or local models through Ollama, but those are slow on this laptop.

**Real costs:** 1 judged retrieval test cost about $0.011. All 15 cost $0.19 and took 2 min 13 s.

---

## 3. How the RAG retrieval works

```
Build:  doc section ──► one embedding (384 numbers, all-MiniLM-L6-v2) ──► stored with the section's full text
Query:  question    ──► one embedding ──► compared with every chunk ──► top k chunks returned in full
```

- **Similarity score** (in `search()` output) = cosine similarity of the two embeddings, computed locally with no LLM. It measures **how close in topic** two texts are, **not whether one answers the other**.
- **One chunk = one doc section**, from a heading to the next heading. The **whole chunk** always comes back; nothing extracts the matching sentence, because the score is for the chunk as a whole.
- **Who sets k:** `search()` defaults to 5, but the test-case-creator calls it with `--top-k 3` and queries with **the rule's own wording**. An eval must copy the real call.

### Chunking trade-offs

| Technique | Gain | Cost |
|---|---|---|
| Whole sections (current) | Keeps conditions and exceptions ("*However*, compound measurements…") together | More irrelevant text (low Contextual Relevancy) |
| Smaller chunks (paragraphs, with overlap) | Precise matching | Loses surrounding context |
| Small-to-big (also called parent-child) | Match on sentences, return the section | More complex index |
| Reranker | Scores question and chunk *together*, so ranking is more accurate | An extra model, slower |
| Contextual compression | Returns only the relevant sentences | Extra LLM call; may drop a key condition |

---

## 4. Golden datasets

A **golden dataset** is the answer key: questions paired with the correct answer and where it lives. A wrong golden entry makes the eval wrong, however good the metrics are, so **people review it** (the architect approved ours).

Rules for good entries:
1. **Paraphrase, don't copy.** Copying the doc's wording tests keyword matching, not understanding.
2. **Mix difficulty:** plain facts, different wording (G-12: "service" for *virtual part*), rules cited in two places, one easy control.
3. **Include questions the docs can't answer.** A good system admits it has nothing, instead of returning a confident wrong chunk.
4. **Watch for saturation.** When every test scores 1.0, the set is too easy to detect anything short of a big regression; add harder entries.

Ours: `golden/retrieval_golden.json`, with 15 answerable entries (each from an inventory rule, with doc lines checked) and 3 unanswerable ones.

---

## 5. Retrieval metrics

### Free (code plus the answer key; repeatable, run on every change)

| Metric | Question | Formula |
|---|---|---|
| **Hit@k** | Did a correct chunk come back in the top k at all? | hits ÷ queries |
| **MRR@k** (mean reciprocal rank) | How high did the first correct chunk rank? | average of 1/rank (0 if missed) |

Count a hit when **any** expected location comes back. Requiring every cited location was too strict (G-14), because one chunk can state the whole rule; completeness is Recall's job.

### Judged (DeepEval, LLM)

| Metric | Needs | How it scores | Example |
|---|---|---|---|
| **Contextual Precision** | input, expected_output, retrieval_context (in rank order) | Each chunk useful or not; weighted toward useful chunks ranked first (this is **Average Precision**) | ✓✗✗ = 1.0; ✗✓✗ = 0.5; ✓✗✓ = 0.83 |
| **Contextual Recall** | expected_output, retrieval_context | Share of expected_output's statements backed by some chunk | 2 of 2 = 1.0 |
| **Contextual Relevancy** | input, retrieval_context | Share of the retrieved statements that are about the question | 3 of 12 = 0.25 |

### How Contextual Recall is calculated (read from the installed source)

1. **One judge call gives a verdict for each sentence of `expected_output`** (`contextual_recall/templates/generate_verdicts.txt`):
   > *For EACH sentence in the given expected output below, determine whether the sentence can be attributed to the nodes of retrieval contexts… verdict STRICTLY 'yes' or 'no'… the number of verdicts SHOULD BE STRICTLY EQUAL to the number of sentences.*

   It walks through **your answer key**, not the chunks.
2. **The score is computed in code** (`utils/qag.py`, `score_qag_verdicts`):
   ```python
   score = yes_verdicts / all_verdicts       # supported sentences / all sentences
   return 0 if strict_mode and score < threshold else score
   ```
   Empty `expected_output` gives 0. `strict_mode=True` turns every score into pass or fail (0 or the score).
3. **A second call writes the reason**, so that's 2 judge calls per test.

**Real example (G-12):** expected_output has **three facts** in **one sentence** (joined by a semicolon), so the judge gave **one verdict**: `[yes]`, score 1/1 = 1.0. Had only two facts been supported, the score could only be 1.0 or 0.0, never 0.67.

**Lesson: Recall's granularity is the sentences you write.** Write `expected_output` as **one fact per sentence** so it can score partial coverage:
```
"A virtual part represents a non-physical item. It cannot have stock items. Stock-related UI elements are hidden on its page."
→ 3 verdicts → 0, 0.33, 0.67 or 1.0 become possible
```
This partly explains why our Recall scores were all exactly 1.00.

| Metric | Walks through | Asks for each item | Score |
|---|---|---|---|
| **Contextual Recall** | Sentences of **expected_output** | Supported by the chunks? | yes ÷ total |
| Contextual Precision | **Chunks**, in rank order | Useful for expected_output? | Average precision (rank-weighted) |
| Contextual Relevancy | Statements **in the chunks** | Relevant to the input? | relevant ÷ total |

Recall asks whether **everything needed** was retrieved; Precision asks whether **what was retrieved is ranked usefully**.

### Faithfulness (generator metric), and why this project dropped it

**Definition:** Faithfulness measures whether the claims in a system's answer (`actual_output`) are **consistent with the retrieved context** (`retrieval_context`). Score = share of the answer's claims that the context does **not contradict**. It's the standard check for *hallucination against your own documents* in RAG.

**Needs:** `input`, `actual_output`, `retrieval_context`. **Scored by:** LLM judge.

**How it's calculated** (4 judge calls):
1. **Truths:** extract the facts stated in `retrieval_context` (all of them, unless `truths_extraction_limit` caps the number).
2. **Claims:** extract the factual claims made in `actual_output`.
3. **Verdicts:** for each claim, "does it **contradict** any truth?", answered `yes` (agrees), `no` (contradicts) or `borderline` (the context doesn't settle it).
4. **Score:** `(yes + borderline) / all claims`. With `penalize_ambiguous_claims=True`, only `yes` counts. A 4th call writes the reason.

**Parameters:** `threshold` (default 0.5), `model`, `include_reason`, `strict_mode` (score becomes 0 below threshold), `penalize_ambiguous_claims`, `truths_extraction_limit`.

**What it catches:** answers that **contradict** the documents ("returns within 30 days" when the policy says 14).
**What it doesn't:** claims the documents **never mention**. They are `borderline`, which counts as faithful by default. So an invented detail passes unless something in the context contradicts it.

**Faithfulness vs Hallucination:** Faithfulness checks against *retrieved* context (`retrieval_context`); Hallucination checks against *ground truth you supply* (`context`).

**Why this project dropped it (planted controls, 2026-10-20):**
| Control | Expected | Haiku judge | Sonnet judge |
|---|---|---|---|
| Invented error message (not in the docs) | pass (nothing contradicts it) | pass | pass |
| "Revision code may contain only letters and digits" when the rule says "any string" | **fail** | pass (1.00): every claim `borderline` | **pass (1.00)** |

Two judges failing the same way points at the **metric's design, not the judge**. It is built for factual answers ("the return period is 14 days"). Test case Expected results describe *system behaviour* ("the form stays open with an error…"), so the extracted claims are about the UI while the truths are about the field, and the judge sees nothing to contradict. Turning on `penalize_ambiguous_claims` doesn't help, because every UI-mechanics claim ("the form opens") is borderline too, so every case would fail. The custom GEval "Requirement traceability" metric caught both defects, so it replaced Faithfulness.

**Lesson:** a built-in metric can be the wrong tool for your data, whatever the judge. Only planted controls reveal it, because on real cases a metric that can't fail just shows a perfect score.

### MRR versus Contextual Precision

Both reward ranking the right chunk high. With one correct chunk they give the same number; they differ when the answer is spread over several chunks:

| Ranking | MRR | Contextual Precision |
|---|---|---|
| ✓ ✗ ✓ | 1.0 (stops at the first ✓) | 0.83 (penalises the ✗ above the second ✓) |

They also decide "correct" differently: **line numbers** (MRR is too strict if the docs repeat a rule) versus **Claude reading the text** (Contextual Precision is noisier). **Investigate where they disagree:** the answer key may be incomplete, or the chunk wording may be weak.

Pairs: **Hit@k ≈ Contextual Recall** (was the answer retrieved?), **MRR ≈ Contextual Precision** (was it ranked first?).

---

## 6. Results so far

| Measure | Rule-wording queries (as the agent queries) | Paraphrased questions |
|---|---|---|
| Hit@3 | 15/15 = 100% | 14/15 = 93% (G-12 at rank 4) |
| MRR@3 | 1.00 | 0.73 |

| Judged metric (rule queries) | Average | Note |
|---|---|---|
| Contextual Precision | 1.00 | Agrees with MRR |
| Contextual Recall | 1.00 | Agrees with Hit@3 |
| Contextual Relevancy | 0.61 (0.25–1.00) | Measures section size; G-15 failed at 0.25 against a 0.3 threshold |

**Findings:**
1. Retrieval is accurate for how the agent really uses it. Weaker with paraphrases, so keep k ≥ 3.
2. **A vector score can't detect "no answer exists":** unanswerable questions scored 0.42–0.45, the weakest correct chunk 0.46. Retrieval always returns something plausible, so **the reader (the agent) must check that a chunk actually states the rule**. That's why "never assume a requirement" needs its own eval (step 5).
3. Low Contextual Relevancy is a chunking design trade-off, not a retrieval fault. Proposed: gate on Precision and Recall, and track Relevancy as a number.
4. Precision and Recall are saturated at 1.00, so the golden set needs harder entries to catch smaller regressions.

### Pattern: record a known limit with `xfail(strict=True)`

```python
@pytest.mark.xfail(strict=True, reason="FINDING: ... XPASS means retrieval changed: revisit.")
```
It's the pytest version of `test.fixme()` + `// FINDING:`. The run stays green while the limit is recorded, and if behaviour changes, the unexpected pass (**XPASS**) fails the run, so you notice.

---

## 6b. Step 5: is the test-case-creator faithful to the docs?

**Purpose:** step 4 showed the agent *receives* the right doc text; step 5 checks what it *writes*. It turns the hard rule *"never assume a requirement"* into a score.

**Offline eval:** no agent run. The judge scores cases the agent already wrote (`test_agent_cases.py`, sample in `golden/agent_cases_sample.json`):

| DeepEval field | Filled from (`build_case`) |
|---|---|
| `input` | Case title, Summary, Review status, step actions and test data |
| `actual_output` | The **Expected result** column, one line per step (read from `test-cases/` by `find_case`) |
| `retrieval_context` | What the case **cites** in its Requirement field: the **inventory rule texts** (`R-ID: text`, from `load_rule_texts`) plus the **doc section** around each Source line (`doc_sections`, using the RAG indexer's `chunk_file`) |
| `expected_output` | Not needed: the metric is **reference-free** |

The judge sees the requirements only because `SingleTurnParams.RETRIEVAL_CONTEXT` is listed in GEval's `evaluation_params`. It validates against **what the case cites**, not the whole docs, and there's **no RAG search**, so retrieval errors can't mix into this score.

### The categories (the architect's policy, written into the GEval steps)

Each Expected result is split into claims, and each claim gets one category:

| Category | Meaning | Allowed? |
|---|---|---|
| **A** | Stated or directly implied by the retrieval context (inventory rule or doc section) | ✓ "The docs say so" |
| **B** | Generic UI mechanics with no business rule: a form or menu opens, a field accepts input, a page is shown, the browser navigates. Also a value the step itself entered as test data | ✓ "That's just how a screen works" (kept by the architect's decision) |
| **C** | Explicitly flagged as unconfirmed: `[confirm in app: …]`, `Proposed, to confirm in Q-…`, `Open: Q-…`, `[open: …]` | ✓ "We're not sure, and we said so" |
| **D** | A behaviour, value, message, field or rule that is not in the context and **not** flagged | ✗ **An assumed requirement** |

The categories are **not part of GEval**: they're plain text in `evaluation_steps`. A, B and C are the three valid justifications; only **D** affects the score.

### The score formula

1. **The judge picks an integer from 0 to 10, using the rubric**, by counting D claims:

   | D claims | Rubric band |
   |---|---|
   | None | **8–10** (8 or 9 if one claim is borderline between B and D) |
   | Exactly one | **4–7** |
   | Two or more | **0–3** |

2. **DeepEval normalises it:** `score = (judge score − 0) / (10 − 0) = judge score / 10`. (With models that return token probabilities, such as OpenAI's, DeepEval averages the possible scores weighted by probability, as in the G-Eval paper. Claude's API doesn't return them, so the plain integer is used.)
3. **Pass if `score ≥ 0.8`**: only cases with no D claims pass. The threshold sits on a band edge, so small score changes inside a band never flip the verdict.

All of this happens in **one judge call**; only the score and the reason come back. The steps ask the judge to quote each D claim in the reason.

### GEval and DAG, for the record

- **G-Eval** comes from *"G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment"* (Liu et al., 2023). The "G" means **GPT**; there's no official expansion. The method: criteria → evaluation steps → form-filling score (→ probability weighting when available). The judge can be any model; here it's Claude Sonnet.
- **DAG** (*Directed Acyclic Graph*) is the alternative: a decision tree of small judge questions (TaskNode: extract; BinaryJudgementNode: yes/no; NonBinaryJudgementNode: pick a label; VerdictNode: a **score you fix**). More repeatable and easier to debug, but more work to write and more calls. **Not used:** GEval proved stable (below).

### Planted controls: test the metric before trusting it

Copies of real cases with one Expected result replaced in memory:

| Control | Defect | Faithfulness (Haiku → Sonnet) | Traceability (Haiku → Sonnet) |
|---|---|---|---|
| PLANTED-1-invented | Invented error text, flag removed | pass → pass (as expected: nothing contradicts it) | **pass ✗ → fail ✓** |
| PLANTED-2-contradiction | "Letters and digits only" vs the rule "any string" | **pass ✗ → pass ✗** | fail ✓ → fail ✓ |

- **Judge choice mattered:** Haiku read the invented message as "implied" by the uniqueness rule; Sonnet, with the same steps, classed it as D. One variable changed at a time, so the cause is known.
- **Faithfulness was dropped:** 1.00 on a direct contradiction with both judges, so the cause is the metric's design (see section 5).
- **Traceability caught both** kinds of defect, so it's the only metric.

### Results on 8 real cases (Sonnet judge, about $0.05 per run)

| Case | Run 1 | Run 2 | Verdict |
|---|---|---|---|
| UI-REV-002 | 0.6 | 0.5 | **FAIL** both runs |
| UI-Unit_measure-013 | 0.8 | 1.0 | pass |
| UI-REV-006, UI-Part-003, UI-Part-012, UI-REV-016, UI-Part_Template-008, UI-Part-047 | 1.0 | 1.0 | pass |

- **Stable:** 2 runs, 0 verdict flips. Scores moved only within their rubric band.
- **The failure is a citation gap, not an invention:** UI-REV-002 step 4 says the new revision shows its link to the original. The docs do state it (part-revision.md L66, rule R-REV-13), but the case cites only R-REV-07 (L37), and it asserts the link without flagging open question Q-REV-07 (how the link is shown), which UI-REV-009 does flag. An Approved case; the bulk review missed it.
- **Possible judge leniency:** UI-Part-012 passed with "the session is scoped to the single Part data type" classed B, but that's business rule R-Part-24, which the case doesn't cite. Pending the architect's labels.
- **Triage of a D claim:** a real assumption (finding) / stated in an uncited section (citation gap) / really B or C (judge error: tighten the steps, rerun the controls).
- **Judge-to-human agreement:** the architect labels each verdict agree or disagree; agreement (e.g. 7 of 8) is the evidence for trusting the judge.

## 6c. Step 6: how did the test-case-creator work? (layer 1, free)

**Purpose:** step 5 judged *what* the agent wrote; step 6 checks *how* it worked: did it follow its own instructions? This is the **trajectory / process** side of agent evaluation, as opposed to the final output.

### The data: Claude Code session transcripts

Every subagent run is saved as `~/.claude/projects/<project>/<session>/subagents/agent-<id>.jsonl`, with a `.meta.json` naming the agent type. One run holds the task prompt, **every tool call with its input**, and the final report (the `SubagentHandback` message). So **no agent is run again**; `agent_traces.py` parses what was recorded.

- **46 test-case-creator runs** (11–16 October). **42 judged:** the instructions entered git at 7ea9e53 (2026-10-13 00:37 +05:30 = **2026-10-12 19:07 UTC**); earlier runs followed instructions that aren't recorded.
- **Time zones:** git shows local time (+05:30), transcripts use UTC. Convert before comparing.
- **Judge each run by the rules in force when it ran** (e.g. open questions moved to `Open_Questions/` on 16 October; runs that day may use either location).

**Run outcomes** (not every run should write cases):
| Outcome | Runs | Verdict |
|---|---|---|
| Wrote cases | 34 | Judged for process |
| Asked for clarification (e.g. "ATT" alone: whole Area or a slice?) | 1 | ✓ Correct, as its guardrail 8 requires |
| Found the work already covered, wrote nothing | 2 | ✓ Correct: avoided duplicates |
| Interrupted, no report | 5 | Excluded (natural negative controls for TaskCompletion later) |

### Lesson: the evaluator's parser needs checking too

The first layer-1 results were mostly **my parser's mistakes**, not the agent's:
1. The agent **chains steps in one shell command** (`python gen.py && python tools/dedupe_cases.py ...`). Taking one step per command made the duplicate check "disappear". Fix: find **every** step marker in a command, in order.
2. It writes cases **through shell commands** (`cat >> file.md <<'EOF' ... ### UI-...`, inline `python - <<'EOF'`, generator scripts run through a variable `python "$S"`), not only the Write tool. Fix: count a shell write when its text contains a case heading.
3. It **batches RAG queries in shell loops** (`for q in "..." "..."; do query_index.py "$q" --top-k 2; done`). Counting tool calls undercounted queries. Fix: expand the loop's query list.
4. Its report **mentions existing cases** as well as new ones. Fix: take the created case IDs from the **headings it wrote**, falling back to the report only for generator-script runs.
5. Patch scripts with non-raw strings turned `\b` into invisible backspace characters. Fix: raw strings, and a scan for control characters.

Treat a parser's output with the same suspicion as a judge's verdicts: **check a surprising result against the raw transcript before calling it a finding.**

### Checks and results (34 runs that wrote cases, 919 cases)

| Check | How | Result |
|---|---|---|
| **Workflow order:** RAG lookup (UI) → write cases → duplicate check after writing → report | **ToolCorrectnessMetric**, `should_consider_ordering=True`, scored in code (needs a `model` object but makes no call: cost 0) on each run's **milestones** (first occurrence of each step) | **34 of 34** in order |
| **RAG top-k = 3** | Parsed `--top-k` of every query | ✗ **21 of 34 runs**; **57 of 126 queries (45%)** used 3 (67 used 2, 2 used 4) |
| **Output not discarded** | `2>/dev/null` on RAG commands | ✗ **10 of 40** commands (7 runs) |
| **Open questions location** | Path vs the rule on the run's date | ✓ No failures |
| **Seed conformance** | `SeedConformanceMetric`: a **custom DeepEval metric with no LLM** (subclass `BaseMetric`, implement `measure()`) | **832 of 919 (90.5%)** fully conformant |
| **Lookup coverage** | ToolCorrectness on rule IDs (below) | Not measurable before the wrapper; measured from 23 October |

**Seed checks** (from `references/seed-*.md`): S1 ID, Area and folder agree; S2 all 10 fields in order; S3 allowed values (Type, Priority, Tags, Automation with a reason, Review); S4 Prerequisites order; S5 steps table; S6 Postconditions and Notes; S7 no vague results; S8 API data sets have `expected status`; L1 cited rules exist; L2 doc lines and schema operations resolve; L3 cited open questions exist; L4 a Draft case lists the open questions its body cites.

**Seed failures found:** L4 in **54** cases (the body cites an *open* question that Review doesn't list, so the case looks less blocked than it is); S3 in **34** (`Automation: Partial.` with no reason); S8 in **1** (two status columns named differently; arguably fine). A first run showed L3 failing on 771 cases: that was **my bug** (the regex collected `| Q-… |` instead of `Q-…`). Always sanity-check a suspiciously large failure count.

**Judgement labels** (report only; a mismatch is a flag, not a failure):
- **Priority vs Risk:** the inventory's Risk definitions mirror the seed's Priority definitions (H core flow or data integrity = P1, M = P2, L = P3). **Only 56% agree**, and the agent rates **lower**, systematically (193 cases on H rules are P2, 40 are P3).
- **13 Negative cases** show no rejection or error in their Expected results (Type possibly wrong).
- **Distribution:** Priority P2 52%, P1 29%, P3 19%; **Automation: Partial 43%** (high); Smoke 13%.

### The top-k finding: is it an agent error?

| Possible cause | Checked | Verdict |
|---|---|---|
| The instruction said 2 or changed | git: always **3** | ✗ |
| Another file said 2 | CLAUDE.md also **3** | ✗ |
| A tool default | `query_index.py` defaults to **5** | ✗ |
| **The agent chose it** | Every k appears explicitly in the commands it wrote | ✓ |

**Likely why:** big batches (19, 11, 9 queries in one loop) used k = 2; runs with 1–2 queries mostly used 3. Each result is a whole doc section, so the agent appears to **trade depth for less output**. (An inference: transcripts show *what*, not *why*.) The deeper cause is **design**: the instruction was a free-form command, and agents treat example commands as suggestions.

**Impact, measured:** on the golden set, **Hit@2 = Hit@3** (15/15 rule wording, 14/15 questions), so the depth loss costs little. Two problems found next to it matter more:
1. **Keyword queries instead of rule wording** (rule wording MRR 1.00 vs paraphrases 0.73).
2. **`2>/dev/null` discards the no-match warning.** `query_index.py` prints "fall back to requirements/INDEX.md" to **stderr** with exit code 2 when nothing passes the floor; in a loop with `2>/dev/null`, both are lost, which **silently disables the agent's fallback to the docs**.

**Lesson: an eval finding isn't automatically a defect.** "Didn't follow the instruction" is a compliance fact; whether it matters is an impact question. Measuring impact downgraded top-k and found a more serious issue beside it.

### Score floor: should it be raised?

`top_k` is a **maximum**: Chroma always returns k sections, then `search()` drops those below the floor (0.2), so fewer can come back. A partial result is silent; only zero results warn. With a 0.2 floor this almost never happens.

| Floor | Rule wording kept | Questions kept | Unanswerable rejected | Real agent queries with **no** result |
|---|---|---|---|---|
| **0.2** (now) | 15/15 | 15/15 | 0/3 | 0% |
| 0.4 | 15/15 | 15/15 | 0/3 | 6% |
| **0.45** | 15/15 | 15/15 | 2/3 | 7% |
| 0.5 | 15/15 | 14/15 | 3/3 | 17% |
| 0.55 | 15/15 | 10/15 | 3/3 | 25% |

Score ranges: correct section with rule wording **0.58–0.96**; with questions **0.46–0.77**; unanswerable **0.42–0.45**; real agent queries median 0.67.

**Conclusion:** a usable gap exists **only for rule-wording queries**. Order of work: (1) make sure a no-match can't be hidden (done, see below), (2) grow the unanswerable set from 3 to 15–20, (3) then set about **0.45** and update the step 4 `xfail` tests, which will start to XPASS. A floor is **not** the main defence against assumed requirements: the reader still has to check that the text states the rule (step 5).

### The fix: `tools/rag/rag_lookup.py`

The agent's step 2.4 now calls `rag_lookup.py <rule ID> <rule ID> ...` instead of writing its own query:
- the query is the **rule's own wording, read from the inventory**;
- **top-k is fixed at 3** (no option);
- **NO MATCH is printed on stdout** with exit code 2 (unknown rule ID: exit 3), so discarding stderr can't hide it;
- any number of rule IDs in one call, so **no loop is needed**;
- it **marks the chunk holding the cited line**, and warns when that line isn't in the top 3 (this would have flagged UI-REV-002's citation gap).

`query_index.py` stays for **free-text search** on what the inventory doesn't cover. Updated: the agent's instructions (step 2.4, step 2.5, sources table), CLAUDE.md, RUNNING.md, requirements/README.md, the copies in `agents/configs/`, and the "How the instructions changed" table in `agents/system-instructions.md`. **Compliance by design beats compliance by instruction.**

### Lookup coverage: did the run verify every rule its cases rely on?

Three different "coverages":
| # | Question | Who decides | Where checked |
|---|---|---|---|
| 1 Scope | Which feature? | **The caller** (`/gen-test-cases UI Part revisions`) | It's the input |
| 2 Rule-to-case | Does every rule of the feature have a case? | The agent selects the rules | `coverage_check.py`, test-case-reviewer |
| **3 Lookup** | Did it **look up every rule its own cases cite**? | **The agent's instructions** | This check |

**Metric:** *rule lookup coverage* = doc-citing rules cited in the run's cases **and** looked up ÷ doc-citing rules cited (**recall**), threshold **1.0**. Rules looked up but not cited are reported only (exploration). The caller's scope is built in, because the denominator is what the agent itself cited.

**In DeepEval:** **ToolCorrectnessMetric** with `evaluation_params=[ToolCallParams.INPUT_PARAMETERS]`, each lookup as `ToolCall(name="rag_lookup", input_parameters={"rule": "R-REV-07"})`. Verified: all → 1.0; 2 of 3 → 0.667; extra lookups don't lower it; none → 0.0; cost 0. Those 4 cases are kept as **metric controls** (`test_lookup_coverage_metric_controls`), so a scoring change in a DeepEval upgrade is caught.

**Runs before 23 October are skipped:** free-text queries don't record which rule they targeted. **From 23 October** a run citing doc rules **must** call `rag_lookup.py`, or it fails (not skipped, so non-use can't hide). Replay of a real run: all rules looked up → PASS; one left out → *"lookup coverage 95%: cited but never looked up ['R-Part-18']"*; no wrapper → *"cites 21 doc rules but never called rag_lookup.py"*.

**Pending:** one new `/gen-test-cases` run to verify the fix (first run the coverage test measures).

## 6d. Evaluating an agentic workflow: a framework

Classify each agent function by **what kind of "correct" exists for it**; that decides the method. A **rule** defines it → check in code. A **source** defines it → a judge with context. An **expert's judgement** defines it → measure agreement. **Nothing** defines it → coverage and comparison.

| # | Category | "Correct" means | Example here | Method and metrics | Cost |
|---|---|---|---|---|---|
| 1 | **Procedural rules** | A step done, in order, with the right parameters | Duplicate check after saving; RAG top-k 3 | Code over the trace; **ToolCorrectness** (tools, order, arguments); AgentLoopDetection | Free |
| 2 | **Output structure** | Required shape and allowed values | Seed's 10 fields; links resolve | Code; custom `BaseMetric`; JsonCorrectness, PatternMatch | Free |
| 3 | **Information gathering** | Looked up the right sources, the right way | RAG per rule; lookup coverage | Hit@k, MRR, Contextual Precision/Recall; coverage (recall) | Mostly free |
| 4 | **Grounded content** | Each claim comes from the sources | Expected results traceable to cited docs | Custom **GEval** (traceability); Faithfulness or Hallucination for factual answers | Credit |
| 5 | **Judgement decisions** | A label applied per a definition; experts can disagree | Priority, Smoke/Regression, Automation, Type, Technique; Clear/Open/Conflict | Validity (code); **consistency with proxies** (Priority vs Risk); **DAG** on the definition; **accuracy, Cohen's kappa, confusion matrix** vs your labels (ExactMatch per case); stability across runs | Mostly free + labels |
| 6 | **Uncertainty handling** | Knows what it doesn't know; escalates | Raises an open question for a missing message or limit | **Planted ambiguities**; precision/recall of open questions vs expert labels | Low |
| 7 | **Open-ended design** | No single answer; completeness and quality | Which scenarios and edge cases | Rule coverage; recall of an expert's scenario list; duplicate rate; GEval rubric; **ArenaGEval** to compare agent versions | Mixed |
| 8 | **Task outcome and efficiency** | Job done, without waste | All requested cases written and reported | **TaskCompletion**, StepEfficiency, PlanAdherence; tokens, time, cost; success over repeated runs (*pass^k*) | Credit |
| 9 | **Boundaries and safety** | Things it must never do | Never delete others' records; never weaken an assertion | **ToolPermission**; code and diff scans; red-team prompts | Mostly free |

**Principles:**
1. **Use the cheapest method that can be exact.** Never ask an LLM what code can check.
2. **Judgement labels are measured by agreement, not right or wrong.** Disagreement between agent, judge and expert often means the **definition** is ambiguous, so fix the seed too.
3. **Every judge needs controls** before you trust it (planted defects, natural negatives).
4. **Evaluate process and outcome separately.** An agent can finish the job while ignoring its instructions; one end-to-end score hides that.
5. **Probabilistic categories need repeated runs.** Stability (do verdicts flip?) is a measurement in itself.
6. **Uncertainty handling deserves its own category**: it can only be tested by giving the agent something it *shouldn't* know.

**Labels are not facts:** Priority, Type, Automation and similar fields are classification decisions. Faithfulness and Traceability check factual claims against sources; for labels, check **valid → consistent → justified → agrees with an expert**.

**Coverage so far:** categories 1, 2, 3, 4 and part of 5 are covered. **Missing: 6 (uncertainty handling, the most important for "never assume a requirement"), 7, 8 (TaskCompletion planned), 9**, and the **other six agents** aren't evaluated at all.

## 7. Metrics by system type

| System | Typical metrics |
|---|---|
| **RAG** | Retriever: Hit@k, MRR, nDCG, Contextual Precision, Recall, Relevancy. Generator: **Faithfulness**, Answer Relevancy, Answer Correctness. Shorthand: the **"RAG triad"** (context relevance, groundedness, answer relevance) |
| **Agents** | Task completion, **tool correctness**, argument correctness, tool permission, plan quality and adherence, step efficiency, loop detection; repeated-run success (τ-bench *pass^k*); cost, latency, steps |
| **Chatbots** | Turn relevancy, **knowledge retention**, role adherence, conversation completeness, turn faithfulness; containment, CSAT |
| **All** | Safety (toxicity, bias, PII leakage), security (prompt injection, jailbreaks: red teaming, OWASP LLM Top 10), hallucination, consistency, latency, cost |

Text-overlap scores (BLEU, ROUGE, exact match) are weak for open-ended text, which is why LLM judges took over.

### All 60 DeepEval metrics (v4.3.1, checked from the installed package)

The website says "50+"; the installed version exports **60** (leaving out helper classes).

**Scored by:**
- **LLM:** a judge model decides.
- **Code:** deterministic, free, repeatable.
- **Code + LLM reason:** code computes the score; the LLM only writes the explanation.
- **Audio:** signal analysis of a voice recording; takes no judge model.

Single-turn metrics take an `LLMTestCase`; multi-turn metrics take a `ConversationalTestCase` (a list of turns).

**1. RAG, single turn (5)**
| Metric | Scored by | Needs | Checks |
|---|---|---|---|
| ContextualPrecision | LLM | input, expected_output, retrieval_context | Useful chunks ranked first |
| ContextualRecall | LLM | input, expected_output, retrieval_context | Expected facts present in the chunks |
| ContextualRelevancy | LLM | input, retrieval_context | Share of retrieved text on-topic |
| Faithfulness | LLM | input, actual_output, retrieval_context | Answer claims supported by the chunks |
| AnswerRelevancy | LLM | input, actual_output | Answer addresses the question |

**2. Agents, single run (8)**
| Metric | Scored by | Needs | Checks |
|---|---|---|---|
| TaskCompletion | LLM | input, actual_output (+ trace) | Task achieved |
| ToolCorrectness | Code (LLM only if `available_tools` is given) | input, tools_called, expected_tools | Expected tools called (optionally ordered, with arguments) |
| ArgumentCorrectness | LLM | input, tools_called | Tool arguments fit the request |
| ToolPermission | **Code** | tools_called | Only allowed tools used (allow and deny lists) |
| PlanQuality | LLM | input, actual_output (+ trace) | Plan is sound |
| PlanAdherence | LLM | input, actual_output (+ trace) | Followed its own plan |
| StepEfficiency | LLM | input, actual_output (+ trace) | No unnecessary steps |
| AgentLoopDetection | **Code** | input, actual_output (+ trace) | Repeated tool calls, stalled reasoning, cycles |

**3. MCP agents (3):** MCPUse (right MCP tools, resources and prompts; needs `mcp_servers`), MCPTaskCompletion (multi-turn), MultiTurnMCPUse. All LLM.

**4. Chatbots and multi-turn agents (7)**, all LLM:
| Metric | Checks |
|---|---|
| TurnRelevancy | Each reply fits the conversation so far |
| KnowledgeRetention | Remembers facts the user gave earlier |
| RoleAdherence | Stays in its role or persona |
| TopicAdherence | Stays within allowed topics |
| ConversationCompleteness | The user's needs were met by the end |
| GoalAccuracy | Reached the user's goal (agentic chat) |
| ToolUse | Tool selection and arguments across turns |

**5. Multi-turn RAG (4):** TurnFaithfulness, TurnContextualPrecision, TurnContextualRecall, TurnContextualRelevancy. All LLM.

**6. Safety and responsible AI (6)**, all LLM: Bias, Toxicity, PIILeakage, Misuse (misuse of a specialised assistant), NonAdvice (financial, medical or legal advice it shouldn't give), RoleViolation.

**7. Task-specific output quality (4)**
| Metric | Scored by | Needs | Checks |
|---|---|---|---|
| Hallucination | LLM | input, actual_output, **context** | Contradicts *given ground-truth* context |
| Summarization | LLM | input, actual_output | Summary accurate and complete |
| PromptAlignment | LLM | input, actual_output | Followed the system prompt's instructions |
| JsonCorrectness | Code + LLM reason | input, actual_output | Matches a JSON schema |

**8. Deterministic text checks (2):** ExactMatch (equals expected_output), PatternMatch (matches a regex). Both code.

**9. Custom metrics (7)**
| Metric | Scored by | What you write |
|---|---|---|
| **GEval** | LLM | Criteria in plain English, or evaluation steps |
| **DAG** | LLM per node | A decision tree of yes/no or classification judgements, more repeatable than GEval |
| ArenaGEval | LLM | Criteria; compares several outputs and picks the best (A/B tests of prompts or models) |
| ConversationalGEval, ConversationalDAG | LLM | GEval and DAG for whole conversations |
| JevEval, ConversationalJevEval | LLM | A list of check `questions` (new in 4.x; description provisional) |

**10. Images (5):** TextToImage, ImageEditing, ImageCoherence, ImageHelpfulness, ImageReference. Vision-capable LLM.

**11. Voice agents (9):** TranscriptionAccuracy (LLM / speech-to-text), AudioGlitch (LLM); AgentResponsiveness, AudioIntegrity, SpeechIntelligibility, TurnTakingNaturalness, VoiceConsistency, VoiceNaturalness, VoiceReliability (audio analysis).

Total: 5 + 8 + 3 + 7 + 4 + 6 + 4 + 2 + 7 + 5 + 9 = **60**.

**Take-aways:**
- **Few are free:** ExactMatch, PatternMatch, ToolPermission and AgentLoopDetection, plus the score part of ToolCorrectness and JsonCorrectness. Everything else costs judge credit, which is why free Hit@k and MRR checks are worth keeping alongside DeepEval.
- **Faithfulness vs Hallucination** (an interview trap): Faithfulness checks against *what was retrieved*; Hallucination checks against *ground truth you provide*.
- **GEval vs DAG:** GEval is quick to write but noisier. DAG splits the judgement into explicit decisions, so it's more repeatable; use it when a rule has clear branches (*"states a requirement → in the docs? → if not, marked Open question?"*).
- **Relevant to this project:** groups 1, 2, 7 (PromptAlignment) and 9 (GEval, DAG). Images, voice, MCP and multi-turn chat are not.

**DeepEval's guidance:** about **5 metrics at most** per system: **1–2 custom** (your use case's own success criteria) plus **2–3 generic** (for the system type).

### Standards and institutions

There's **no official standard metric set**. Standards bodies publish risk frameworks and quality models (*what* to evaluate), not formulas.

| Body | Publication |
|---|---|
| NIST (US) | AI RMF 1.0; **Generative AI Profile, NIST AI 600-1** (risks such as *confabulation*); runs TREC, which has a RAG track |
| ISO/IEC SC 42 | **ISO/IEC 25059** (quality model for AI systems, extends ISO 25010), 42001 (management), 23894 (risk), TS 4213 |
| EU AI Act | Accuracy, robustness, cybersecurity for high-risk systems (Article 15); standards in progress at CEN-CENELEC JTC 21 |
| UK AI Security Institute | **Inspect**, an open-source eval framework |
| Singapore IMDA / AI Verify | AI Verify toolkit, Project Moonshot (LLM application testing) |
| OWASP | Top 10 for LLM Applications (security) |
| MLCommons, Stanford CRFM | AILuminate (safety), HELM (models) |

Check the current names and versions before citing them; they change often.

---

## 8. Evaluating a whole LLM application (the ShopAssist example)

A support assistant with RAG (policies), tools (order status, returns, escalation) and multi-turn chat. **Evaluate it in layers**, so a failure points to its cause:

| Layer | Metrics |
|---|---|
| 1. Retrieval | Hit@k, MRR, Contextual Precision and Recall |
| 2. Generation | Faithfulness, Answer Relevancy, GEval for business rules ("never promises a refund the policy doesn't allow") |
| 3. Tool use | ToolCorrectness, ArgumentCorrectness, ToolPermission (no action before confirmation) |
| 4. Task outcome | TaskCompletion, StepEfficiency, loop detection |
| 5. Conversation | KnowledgeRetention, RoleAdherence, ConversationCompleteness |
| 6. Safety and security | PIILeakage, NonAdvice, Toxicity, red teaming |
| 7. Classic QA | API and functional tests, JSON validity, p95 latency, cost per conversation |

**Datasets:** golden (reviewed), synthetic (DeepEval `Synthesizer`, then reviewed), adversarial (red team), production samples (anonymised), multi-turn scripts or simulated users.

**When:**
- **Every pull request:** free checks plus a small judged set.
- **Before release:** the full suite, red teaming, repeated runs.
- **In production:** a judge on *sampled* traffic, plus feedback, escalations, cost and latency.

**Tracing:** `@observe` on each component lets you attach metrics per component, not only to the final reply.

**Interview line:**
> "I treat an LLM application as a layered system. Deterministic layers get conventional tests; each probabilistic layer gets its own metric tied to a stated business rule, gated with thresholds in CI, and the same metrics run on sampled production traffic."

---

## 9. Commands (run from `evals/`)

```powershell
$env:PYTHONUTF8 = "1"                                                         # once per terminal
.\.venv\Scripts\python.exe judge_check.py                                     # judge smoke test
.\.venv\Scripts\python.exe -m pytest test_retrieval.py -m "not judged" -v     # free layer, no cost
.\.venv\Scripts\deepeval.exe test run test_retrieval.py -k "judged and G-01"  # one judged test
.\.venv\Scripts\deepeval.exe test run test_retrieval.py -m judged             # all judged tests (~$0.19)
.\.venv\Scripts\deepeval.exe test run test_agent_cases.py -k planted -s     # step 5: metric controls first
.\.venv\Scripts\deepeval.exe test run test_agent_cases.py -k sample          # step 5: 8 real cases (~$0.05)
.\.venv\Scripts\python.exe -m pytest test_agent_behaviour.py -v -s          # step 6 layer 1: process, seed, coverage, labels (free)
..\tools\rag\.venv\Scripts\python.exe ..\tools\rag\rag_lookup.py R-REV-07 R-Part-03   # the agent's rule lookup (from evals/)
```

| File | Purpose |
|---|---|
| `.env` | `ANTHROPIC_API_KEY`, telemetry opt-out (gitignored) |
| `judge_check.py` | One-call judge smoke test |
| `golden/retrieval_golden.json` | Approved answer key |
| `test_retrieval.py` | Retrieval eval (free and judged layers) |
| `conftest.py` | Prints the Hit@3 and MRR summary |
| `test_agent_cases.py` | Step 5: GEval "Requirement traceability" on saved cases, plus planted controls |
| `golden/agent_cases_sample.json` | Step 5 sample (8 cases) and planted defects |
| `case_sources.py` | Reads inventory rules, cases and cited doc sections |
| `agent_traces.py` | Step 6: parses test-case-creator runs from the session transcripts (tool calls, RAG queries, top-k, case IDs, report) |
| `seed_conformance.py` | Step 6: seed checks S1-S8, L1-L4, and `SeedConformanceMetric` (custom metric, no LLM) |
| `test_agent_behaviour.py` | Step 6 layer 1: workflow order, top-k, discarded output, open-question location, seed conformance, lookup coverage, label report |
| `../tools/rag/rag_lookup.py` | The agent's rule lookup: rule wording from the inventory, fixed top-k 3, NO MATCH on stdout |
| `pytest.ini` | Registers the `judged` marker |
| `.deepeval/.latest_test_run.json` | Last run's scores, reasons and cost |

---

## 10. Still to do

- ~~Step 5~~ **Done** (section 6b). Open: the architect's labels on the 8 verdicts; fix or record UI-REV-002.
- **Step 6:** layer 1 **done** (section 6c), plus the `rag_lookup.py` fix and lookup coverage. Open: **one new `/gen-test-cases` run** to verify the fix; **layer 2, TaskCompletion** (fed with layer-1 facts; the 5 interrupted runs as negative controls).
- **Not yet covered:** uncertainty handling (planted ambiguous rules: does it raise an open question?), boundaries, judgement labels against the architect's labels (accuracy, kappa; DAG optional), and the other six agents.
- **Step 7:** tune thresholds from real scores (Relevancy: gate or track?), harder golden entries, rewrite `expected_output` as one fact per sentence so Recall can score partial coverage, 15-20 unanswerable questions, score floor of about 0.45 (then update the `xfail` tests), one command for all evals, a results summary.

---

## 11. Test yourself

1. Why did Answer Relevancy give 1.0 without any `expected_output`, and what wrong answer would it still pass?
2. Why can't a score cutoff in `search()` reject questions the docs don't answer?
3. For the ranking ✗ ✓ ✓, what are MRR and Contextual Precision? *(0.5; (1/2 + 2/3) / 2 ≈ 0.58)*
4. Why did the eval switch to TOP_K = 3 and rule-wording queries?
5. G-15 failed. Was retrieval wrong? Which two scores prove it wasn't?
6. What does `xfail(strict=True)` give you that skipping a test doesn't?
7. Which metrics are free to run on every change, and which belong in less frequent runs?
8. Name the seven layers for evaluating an LLM application, and one metric for each.
9. Which line of `test_retrieval.py` makes the API calls, and which line runs the system under test?
10. An expected_output has 3 facts in one sentence and the chunks support 2 of them. What can Contextual Recall score, and how do you fix that? *(only 1.0 or 0.0; one fact per sentence gives 0.67)*
11. Which DeepEval metrics cost nothing to run?
12. Faithfulness and Hallucination both catch made-up content. What's the difference?
13. What are categories A, B, C and D, and which one lowers the score?
14. The judge returns 7. What score does DeepEval store, and does it pass at 0.8? *(0.7, fail: one D claim)*
15. Why did both judges give Faithfulness 1.00 on a direct contradiction, and what proved it was the metric, not the judge?
16. Where does the judge get the requirements from, and why did UI-REV-002 fail even though the docs state the link?
17. Where does step 6 get its data from, and why is no agent run needed?
18. The first layer-1 results showed the duplicate check missing in several runs. What was really wrong?
19. Was top-k 2 an agent error? Name the causes you ruled out, and the measured impact.
20. Why does `2>/dev/null` in the agent's RAG loops matter more than the top-k?
21. Why can't a higher score floor be set safely today for keyword queries, and what had to be fixed first?
22. What is lookup coverage, what is its denominator, and why doesn't the caller's scope affect it? *(recall; doc rules cited in the run's own cases)*
23. Which three "coverages" exist in this workflow, and who decides each?
24. Why is Priority evaluated by agreement rather than by Faithfulness or Traceability?
25. Name the 9 categories of agent function, and the cheapest exact method for each.
