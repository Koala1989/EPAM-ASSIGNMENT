"""Step 6, layer 2: did each test-case-creator run complete its task? DeepEval TaskCompletionMetric (judged).

TaskCompletion asks a judge to extract the task and the outcome, then score 0-1 how well the outcome achieves the
task. The agent's own report is a claim, so the outcome evidence is built from transcript facts instead:
  input          the request the skill sent
  task           the definition of done (from the agent's instructions), including when stopping is correct
  tools_called   facts from layer 1: RAG lookups, case files saved and their seed check, open questions recorded,
                 duplicate check and whether it ran after writing
  actual_output  the agent's final report, or a note that there was none

Sample: golden/agent_runs_sample.json. Interrupted runs are natural negative controls and must fail.

Run from evals/ ($env:PYTHONUTF8 = "1" first):
  .venv\\Scripts\\python.exe -m pytest test_agent_task_completion.py -v -s     (about $0.10 with Sonnet)
"""

import collections
import json
import re
from pathlib import Path

import pytest
from deepeval.metrics import TaskCompletionMetric
from deepeval.models import AnthropicModel
from deepeval.test_case import LLMTestCase, ToolCall

from agent_traces import Run, load_runs
from seed_conformance import case_blocks, check_case
from test_agent_behaviour import events, steps_taken

SAMPLE = json.loads((Path(__file__).parent / "golden" / "agent_runs_sample.json").read_text(encoding="utf-8"))
RUNS = {r.started[:16]: r for r in load_runs()}

# Sonnet: TaskCompletion picks its 0-1 score directly, with no rubric, so it needs the stronger judge (see step 5).
judge = AnthropicModel(model="claude-sonnet-4-6")

TASK = (
    "Generate manual {kind} test cases for the functionality named in the request, following the test-case-creator "
    "instructions. Done means: (1) cases for the functionality's rules are saved to the Area's test-cases folder in "
    "the seed format; (2) each rule that cites the docs was confirmed through the RAG index; (3) open questions for "
    "unclear rules are recorded in the Area's open-questions file; (4) the duplicate check was run on the saved "
    "cases; (5) a final report lists what was created, with counts and case IDs. Stopping without writing cases "
    "also completes the task when it is the correct outcome: the request does not name a functionality clearly "
    "(ask which one), or saved cases already cover it (point to them)."
)


def evidence(run: Run) -> list[ToolCall]:
    """What the run did, as facts from its transcript and the case files (not from its own report)."""
    calls = []
    queries = run.rag_queries
    if queries:
        k_used = dict(collections.Counter(q.top_k for q in queries))
        discarded = sum("2>/dev/null" in c for c in run.bash if "query_index.py" in c or "rag_lookup.py" in c)
        note = f"; output discarded with 2>/dev/null in {discarded} commands" if discarded else ""
        calls.append(ToolCall(name="rag_lookup", input_parameters={"queries": len(queries), "top_k_used": k_used},
                              output=f"{len(queries)} RAG lookups made{note}"))
    else:
        calls.append(ToolCall(name="rag_lookup", output="no RAG lookups made"))

    wrote = "write_cases" in events(run)
    if wrote:
        by_folder = collections.defaultdict(list)
        for case_id, block, folder in case_blocks(run.case_ids):
            by_folder[folder].append((case_id, [c for c in check_case(case_id, block, folder) if not c.ok]))
        for folder, cases in by_folder.items():
            conformant = sum(not fails for _id, fails in cases)
            issues = collections.Counter(f.id for _id, fails in cases for f in fails)
            calls.append(ToolCall(
                name="write_cases",
                input_parameters={"folder": folder, "cases": len(cases)},
                output=f"{len(cases)} cases saved in test-cases/{folder} ({cases[0][0]} .. {cases[-1][0]}); "
                       f"seed format check: {conformant}/{len(cases)} fully conformant"
                       + (f"; issues: {dict(issues)}" if issues else ""),
            ))
        found = {case_id for cases in by_folder.values() for case_id, _fails in cases}
        gone = sorted(set(run.case_ids) - found)
        if gone:
            calls.append(ToolCall(name="write_cases", output=f"{len(gone)} more case IDs ({gone[0]} .. {gone[-1]}) are "
                                  "listed in the run's report but no longer exist in the case files (later deleted or "
                                  "regenerated), so their content cannot be checked"))
        if not by_folder:
            calls.append(ToolCall(name="write_cases", output="case-writing commands ran, but no saved case can be "
                                                            "identified (generator script, and no final report listing IDs)"))
    else:
        calls.append(ToolCall(name="write_cases", output="no case files written"))

    question_files = sorted({p.split("test-cases/")[-1] for p in run.written if "open-question" in p})
    question_files += [m.group(1).split("test-cases/")[-1] for c in run.bash for m in re.finditer(r">>?\s*\"?(\S*open-questions?\S*\.md)", c)]
    if question_files:
        calls.append(ToolCall(name="record_open_questions", input_parameters={"files": sorted(set(question_files))},
                              output="open questions appended"))

    if run.dedupe_runs:
        after = "dedupe_check" in steps_taken(run)
        calls.append(ToolCall(name="duplicate_check", input_parameters={"runs": run.dedupe_runs},
                              output="run after the cases were saved" if after else "run, but not after saving cases"))
    else:
        calls.append(ToolCall(name="duplicate_check", output="not run"))
    return calls


def build_case(run: Run) -> LLMTestCase:
    return LLMTestCase(
        input=run.prompt[:3000],
        actual_output=run.report or "(no final message: the run ended without a report)",
        tools_called=evidence(run),
        metadata={"run": run.started[:16]},
    )


@pytest.mark.judged
@pytest.mark.parametrize("entry", SAMPLE["runs"], ids=lambda e: f"{e['started']}-{e['group'].replace(' ', '_')}")
def test_task_completion(entry):
    run = RUNS[entry["started"]]
    metric = TaskCompletionMetric(model=judge, task=TASK.format(kind=run.kind), threshold=SAMPLE["pass_threshold"],
                                  include_reason=True, async_mode=False)
    metric.measure(build_case(run))
    summary = f"{entry['started']} {entry['group']}: score {metric.score:.2f} (expect {entry['expect']})\n  {metric.reason}"
    print("\n" + summary)
    if entry["expect"] == "pass":
        assert metric.score >= SAMPLE["pass_threshold"], summary
    else:
        assert metric.score < SAMPLE["fail_below"], summary
