"""Step 6, layer 1: how did the test-case-creator work? Free checks, no LLM calls.

Sources: Claude Code's saved transcripts of every test-case-creator run (agent_traces.py) and the case files.

  Process (per run that wrote cases, under the instructions in git since 2026-10-13):
    tool order   DeepEval ToolCorrectnessMetric (scored in code): RAG query (UI) -> write cases -> duplicate check -> report
    top-k        every RAG query uses --top-k 3, as the instructions say
    open qs      open questions saved where the rules said at the time
  Output (per case file): seed conformance S1-S8, L1-L4 (seed_conformance.py, a custom DeepEval metric)
  Lookup coverage (per run that used rag_lookup.py): every doc-citing rule its cases cite was looked up
                (DeepEval ToolCorrectnessMetric on the rule IDs, scored in code)
  Labels (report only): Priority vs the cited rules' Risk, Type vs steps, distributions

Run from evals/:  .venv\\Scripts\\python.exe -m pytest test_agent_behaviour.py -v -s
"""

import collections
import re

import pytest
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.models import AnthropicModel
from deepeval.test_case import LLMTestCase, ToolCall, ToolCallParams

from agent_traces import OPEN_QUESTIONS_MOVED, Run, load_runs
from case_sources import load_rule_risks
from seed_conformance import SeedConformanceMetric, case_blocks, split_cases
from rag_lookup import DOC_LINK, load_rules  # tools/rag, on the path through case_sources

RUNS = load_runs()

# ToolCorrectness requires a model object even though, without available_tools, it scores in code and makes no call.
NO_CALL_JUDGE = AnthropicModel(model="claude-haiku-4-5")


# Markers of each workflow step inside one shell command. The agent often chains several steps in one command
# (`python gen.py && python tools/dedupe_cases.py ...`), so every marker is found, in command order.
BASH_STEPS = [
    ("rag_query", re.compile(r"query_index\.py|rag_lookup\.py")),
    ("write_cases", re.compile(r"python\S*\s+(?:-\s+\S*\s*)?\S*gen\w*\.py")),  # runs a case generator script it wrote
    ("write_cases", re.compile(r"python\S*\s+-\s.*?<<.*?###\s+(?:UI|API)-", re.S)),  # inline script that builds cases
    ("write_cases", re.compile(r"cat\s+>>?\s*\S+\.md\s*<<.*?###\s+(?:UI|API)-", re.S)),  # shell write of case text
    ("dedupe_check", re.compile(r"dedupe_cases\.py")),
]


def events(run: Run) -> list[str]:
    """Every workflow step the run took, in order (several may come from one shell command)."""
    found = []
    for call in run.tool_calls:
        name, data = call["name"], call["input"]
        path = data.get("file_path", "").replace("\\", "/")
        if name == "Bash":
            cmd = data.get("command", "")
            hits = sorted((m.start(), step) for step, rx in BASH_STEPS for m in rx.finditer(cmd))
            if re.search(r"gen\w*\.py", cmd):  # generator run through a variable: S=.../gen.py; python "$S"
                hits = sorted(hits + [(m.start(), "write_cases") for m in re.finditer(r'python\S*\s+"\$\w+"', cmd)])
            found += [step for _pos, step in hits]
        elif name in ("Write", "Edit") and "test-cases/" in path and "open-question" not in path and path.endswith(".md"):
            found.append("write_cases")
        elif name == "SubagentHandback":
            found.append("handback")
    return found


def steps_taken(run: Run) -> list[str]:
    """The run's milestones in the order they first happened: first RAG query, first case write, first duplicate
    check after a write, final report. Repeats (a fix-up edit after the duplicate check) do not change the order."""
    seq = events(run)
    first = {}
    for i, step in enumerate(seq):
        first.setdefault(step, i)
    if "dedupe_check" in first and "write_cases" in first:
        after = [i for i, s in enumerate(seq) if s == "dedupe_check" and i > first["write_cases"]]
        if after:
            first["dedupe_check"] = after[0]
        else:
            first.pop("dedupe_check")  # only checked before writing: does not count
    return [step for step, _i in sorted(first.items(), key=lambda kv: kv[1])]


# Runs judged for process: under the instructions in git, finished with a report, and wrote at least one case.
WRITING_RUNS = [r for r in RUNS if r.judged and r.complete and "write_cases" in events(r)]
OTHER_RUNS = [r for r in RUNS if r not in WRITING_RUNS]


def run_id(run: Run) -> str:
    return f"{run.started[5:16]}-{run.kind}-{re.sub(r'[^A-Za-z]+', '_', run.prompt[24:60]).strip('_')}"


@pytest.mark.parametrize("run", WRITING_RUNS, ids=run_id)
def test_run_followed_the_workflow(run):
    expected = (["rag_query"] if run.kind == "UI" else []) + ["write_cases", "dedupe_check", "handback"]
    taken = steps_taken(run)
    metric = ToolCorrectnessMetric(model=NO_CALL_JUDGE, should_consider_ordering=True, include_reason=False, async_mode=False)
    metric.measure(LLMTestCase(
        input=run.prompt,
        actual_output=run.report,
        tools_called=[ToolCall(name=s) for s in taken],
        expected_tools=[ToolCall(name=s) for s in expected],
    ))

    problems = []
    if metric.score < 1.0:
        problems.append(f"tool order {metric.score:.2f}: expected {expected}, took {taken}")
    wrong_k = sorted({q.top_k for q in run.rag_queries if q.top_k != 3}, key=str)
    if wrong_k:
        problems.append(f"--top-k {wrong_k} on {sum(q.top_k != 3 for q in run.rag_queries)} of {len(run.rag_queries)} RAG queries (instructions: 3)")
    if any("2>/dev/null" in c for c in run.bash if "query_index.py" in c or "rag_lookup.py" in c):
        problems.append("RAG output discarded with 2>/dev/null: a no-match warning would be lost")
    question_files = [p for p in run.written if "open-question" in p]
    day = run.started[:10]
    for path in question_files:
        new_place = "/Open_Questions/open-question_" in path
        if (day > OPEN_QUESTIONS_MOVED and not new_place) or (day < OPEN_QUESTIONS_MOVED and new_place):
            problems.append(f"open questions saved to {path.split('test-cases/')[-1]} (wrong location for {day})")
    assert not problems, "\n".join(problems)


def test_other_runs_ended_with_a_report():
    """Runs that wrote no cases: asked for clarification, found the work already done, or were interrupted.
    Report-only; interrupted runs (no handback) are listed, not failed."""
    lines = []
    for run in OTHER_RUNS:
        if not run.judged:
            outcome = "before the instructions were in git (not judged)"
        elif not run.complete:
            outcome = "INTERRUPTED: no report"
        elif re.search(r"already (covered|exist)|would only duplicate|would duplicate", run.report, re.I):
            outcome = "stopped: already covered"
        elif re.search(r"please confirm|questions:|which (one|slice)|confirm which", run.report, re.I):
            outcome = "stopped: asked for clarification"
        else:
            outcome = "stopped: other (read the report)"
        lines.append(f"  {run.started[:16]} {run.kind} | {outcome} | {run.prompt[:60]}")
    print("\nRuns that wrote no cases:\n" + "\n".join(lines))


CASE_FILES = sorted({(folder, case_id.split("-")[0]) for case_id, _b, folder in case_blocks()})


@pytest.mark.parametrize("folder", sorted({f for f, _k in CASE_FILES}))
def test_seed_conformance(folder):
    cases = [c for c in case_blocks() if c[2] == folder]
    metric = SeedConformanceMetric(threshold=1.0)
    metric.measure(LLMTestCase(input=folder, actual_output="", metadata={"cases": cases}))
    failed_cases = sorted({f.split(" ")[0] for f in metric.failures})
    assert metric.is_successful(), (
        f"{len(failed_cases)} of {len(cases)} cases fail a seed check ({metric.score:.1%} of checks pass):\n  "
        + "\n  ".join(metric.failures)
    )


def test_label_consistency_report():
    """Report-only: judgement labels compared with free proxies. A mismatch is a flag for review, not a failure."""
    risks = load_rule_risks()
    expected_priority = {"H": "P1", "M": "P2", "L": "P3"}
    rank = {"H": 3, "M": 2, "L": 1}
    matrix = collections.Counter()
    type_flags, dist = [], collections.defaultdict(collections.Counter)
    for case_id, block, _folder in case_blocks():
        fields = dict(re.findall(r"^\| \*\*(.+?)\*\* \| (.*) \|$", block, re.M))
        priority = fields.get("Priority", "").strip()
        rule_risks = [risks[r] for r in re.findall(r"\bR-[A-Za-z_]+-\d+\b", fields.get("Requirement", "")) if r in risks]
        if rule_risks:
            top = max(rule_risks, key=rank.get)
            matrix[(expected_priority[top], priority)] += 1
        case_type = fields.get("Type", "").strip()
        results = " ".join(re.findall(r"^\| \d+ \|.*\| (.*) \|$", block, re.M)).lower()
        if case_type == "Negative" and not re.search(r"reject|error|not |no |denied|fail|invalid|4\d\d|cannot|hidden", results):
            type_flags.append(case_id)
        dist["Priority"][priority] += 1
        dist["Automation"][re.match(r"\W*(\w*)", fields.get("Automation", "")).group(1)] += 1
        dist["Smoke"]["Smoke" if "Smoke" in fields.get("Tags", "") else "not Smoke"] += 1

    total = sum(matrix.values())
    agree = sum(n for (exp, got), n in matrix.items() if exp == got)
    print(f"\nPriority vs highest Risk of the cited rules (H->P1, M->P2, L->P3): {agree}/{total} = {agree / total:.0%} agree")
    print("  rows: expected from Risk, columns: agent's Priority")
    for exp in ("P1", "P2", "P3"):
        print(f"  {exp}: " + "  ".join(f"{got}={matrix[(exp, got)]:3}" for got in ("P1", "P2", "P3")))
    print(f"Negative cases whose expected results show no rejection or error: {len(type_flags)} {type_flags[:8]}")
    for name, counter in dist.items():
        n = sum(counter.values())
        print(f"{name}: " + ", ".join(f"{k or '(empty)'} {v / n:.0%}" for k, v in counter.most_common()))


# ---------- Lookup coverage: did the run verify every rule its cases rely on? ----------

# tools/rag/rag_lookup.py replaced free-text lookups on this day. Earlier runs queried free text, so which rule a
# query targeted is not recorded and coverage cannot be measured exactly; from this day a run must use the wrapper.
WRAPPER_SINCE = "2026-10-23"
RULES = load_rules()


def cited_doc_rules(run: Run) -> set[str]:
    """Doc-citing rules cited in the Requirement field of the cases the run reports it created.
    Schema-only rules are left out: RAG does not apply to them."""
    cited = set()
    for _case_id, block, _folder in case_blocks(run.case_ids):
        requirement = dict(re.findall(r"^\| \*\*(.+?)\*\* \| (.*) \|$", block, re.M)).get("Requirement", "")
        cited |= {r for r in re.findall(r"\bR-[A-Za-z_]+-\d+\b", requirement) if r in RULES and DOC_LINK.search(RULES[r][1])}
    return cited


def looked_up_rules(run: Run) -> list[str]:
    return [q.text for q in run.rag_queries if q.text.startswith("R-")]


def lookup_coverage(looked_up: list[str], cited: set[str]) -> float:
    """Share of cited rules that were looked up (recall). Extra lookups do not lower it."""
    metric = ToolCorrectnessMetric(model=NO_CALL_JUDGE, evaluation_params=[ToolCallParams.INPUT_PARAMETERS],
                                   include_reason=False, async_mode=False)
    call = lambda rule: ToolCall(name="rag_lookup", input_parameters={"rule": rule})  # noqa: E731
    metric.measure(LLMTestCase(input="lookup coverage", actual_output="",
                               tools_called=[call(r) for r in looked_up], expected_tools=[call(r) for r in sorted(cited)]))
    return metric.score


@pytest.mark.parametrize("run", WRITING_RUNS, ids=run_id)
def test_rule_lookup_coverage(run):
    cited = cited_doc_rules(run)
    if not cited:
        pytest.skip("its cases cite no doc rules (schema rules only)")
    looked_up = looked_up_rules(run)
    if not looked_up:
        if run.started < WRAPPER_SINCE:
            pytest.skip("before rag_lookup.py: free-text queries do not record which rule they targeted")
        pytest.fail(f"cites {len(cited)} doc rules but never called rag_lookup.py (instructions: step 2.4)")
    score = lookup_coverage(looked_up, cited)
    missing = sorted(cited - set(looked_up))
    extra = sorted(set(looked_up) - cited)
    if extra:
        print(f"\n{run_id(run)}: looked up but not cited (exploration, not a failure): {extra}")
    assert score == 1.0, f"lookup coverage {score:.0%}: cited but never looked up {missing}"


@pytest.mark.parametrize(
    ("looked_up", "cited", "expected"),
    [
        (["R-A-01", "R-A-02", "R-A-03"], {"R-A-01", "R-A-02", "R-A-03"}, 1.0),
        (["R-A-01", "R-A-02"], {"R-A-01", "R-A-02", "R-A-03"}, 2 / 3),
        (["R-A-01", "R-A-02", "R-A-03", "R-A-09"], {"R-A-01", "R-A-02", "R-A-03"}, 1.0),
        ([], {"R-A-01"}, 0.0),
    ],
    ids=["all", "two-of-three", "extra-lookup-ignored", "none"],
)
def test_lookup_coverage_metric_controls(looked_up, cited, expected):
    """Controls for the metric itself: ToolCorrectness on rule IDs must score as recall, ignoring extra lookups."""
    assert lookup_coverage(looked_up, cited) == pytest.approx(expected, abs=0.001)
