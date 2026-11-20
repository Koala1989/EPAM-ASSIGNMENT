"""TaskCompletion for the automation generators, one run at a time: playwright-test-generator and api-test-generator.

A SubagentStop hook (.claude/settings.json) runs this in the background when either generator finishes; it can also
score saved runs by hand. As in test_agent_task_completion.py, the agent's own report is a claim, so the outcome
evidence is built from facts instead:
  input          the request the skill sent ("Automate test case <ID>.")
  task           the definition of done (from the agent's instructions) as numbered criteria C1..Cn, including when
                 stopping is correct
  tools_called   facts checked in code, each labelled with the criterion it covers: the case's Review status; the live
                 recording (UI); the spec file on disk and its structure against the case; the other files edited;
                 lint, type check and test runs with their results (API)
  actual_output  the agent's final report, or a note that there was none
A denied or failed browser_evaluate call is not counted as sending its requests, and a tool call that Claude Code's
permission system denied (auto mode classifier, deny rule, declined prompt) is listed as a fact. Such runs are logged
with "blocked" and left out of the summary's pass rate and mean, because the environment stopped them, not the agent.

Each score is appended to results/automation_task_completion.jsonl with the agent file's git version, so the pass rate
can be compared across prompt changes, and sent to Grafana as a log event (eval_telemetry.py). The hook scores the spec as the generator left it. Scoring an older run reads
the spec and the case as they are now: the healer may have changed the spec since.

Run from evals/ ($env:PYTHONUTF8 = "1" first; about $0.013 per scored run with Sonnet):
  .venv\\Scripts\\python.exe automation_task_completion.py --transcript <agent-<id>.jsonl>   score one run
  .venv\\Scripts\\python.exe automation_task_completion.py --since 2026-11-05                every unscored run since then
  .venv\\Scripts\\python.exe automation_task_completion.py --summary                         pass rate and mean, free
  add --dry-run to print the test case without calling the judge
"""

import argparse
import collections
import json
import os
import re
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

EVALS = Path(__file__).resolve().parent
os.environ.setdefault("ENV_DIR_PATH", str(EVALS))  # DeepEval reads ANTHROPIC_API_KEY from evals/.env, wherever this runs

from deepeval.metrics import TaskCompletionMetric  # noqa: E402
from deepeval.models import AnthropicModel  # noqa: E402
from deepeval.test_case import LLMTestCase, ToolCall  # noqa: E402

from agent_traces import CASE_ID, TRANSCRIPTS, Run, load_run  # noqa: E402
from case_sources import REPO, find_case  # noqa: E402
from eval_telemetry import try_export  # noqa: E402

LOG = EVALS / "results" / "automation_task_completion.jsonl"
ERRORS = EVALS / "results" / "hook-errors.log"
PASS_THRESHOLD = 0.7  # as for the test-case-creator runs (golden/agent_runs_sample.json)
# Sonnet: TaskCompletion picks its 0-1 score directly, with no rubric, so it needs the stronger judge (see step 5).
JUDGE = "claude-sonnet-4-6"

SUITE = {"playwright-test-generator": "ui", "api-test-generator": "api"}
# Files each generator may write besides its spec (guardrail 5 in both agent files).
ALLOWED = {
    "ui": (r"automation/pages/", r"automation/fixtures/pages\.fixture\.ts$", r"automation/tests/ui/"),
    "api": (r"automation/clients/", r"automation/tests/api/", r"automation/data/api/[^/]+/[^/]+\.json$"),  # rows file
}
# The task criterion each kind of fact covers (the C-numbers in TASKS).
LABEL = {
    "ui": {"case": "C1", "live": "C2", "spec": "C3", "style": "C4", "edits": "C5", "cleanup": "C6"},
    "api": {"case": "C1", "spec": "C2", "style": "C3", "edits": "C3", "checks": "C4", "run": "C5"},
}
FACTS_NOTE = (" The tools called are facts checked in code from the run's transcript and the files on disk, each labelled "
              "with the criterion it covers.")
# How Claude Code words a tool call that its permission system stopped: the auto mode classifier, a deny rule, or the
# user declining the prompt. A hook's refusal (the case-fidelity gate) or a tool's own error is not one of these.
DENIED = re.compile(r"Permission (?:for this action|to use \S+) (?:was|has been) denied"
                    r"|The user doesn't want to (?:proceed with this tool use|take this action)")

TASKS = {
    "playwright-test-generator": (
        "Automate one Approved manual UI test case as one Playwright spec, following the playwright-test-generator "
        "instructions. Done means all of: (C1) the case's Review starts with Approved or Changed; (C2) the case's steps "
        "were executed live in the browser, set up with the seed for the case's user, before the spec was written; "
        "(C3) the spec is saved at automation/tests/ui/<Area>/<case id>.spec.ts, its first line names the case, and it "
        "has one test.step per case step, in order, each with at least one expect; (C4) the spec uses page objects "
        "only: no raw locators, no import from @playwright/test, no hard-coded URLs or credentials; (C5) a file other "
        "than the spec is edited only when a step needed page object support that was missing, only under "
        "automation/pages/ (or the page's fixture registration), and only as additions; editing nothing else is "
        "correct when the existing page objects were enough; (C6) every record created for the recording was deleted; "
        "(C7) a final report gives the spec path, page object changes, mismatches and recording cleanup. Stopping "
        "without writing a spec also completes the task when it is the correct outcome: the case is not Approved, or "
        "the app does not match the case (the report then names the step, what the case says and what the app shows). "
        "An unreachable app or any other failure to finish is not a correct stop. Running lint, type check and the "
        "tests is not part of this task: the skill does that after the agent." + FACTS_NOTE
    ),
    "api-test-generator": (
        "Automate one Approved manual API test case as one Playwright API spec and stabilise it, following the "
        "api-test-generator instructions. Done means all of: (C1) the case's Review starts with Approved or Changed; "
        "(C2) the spec is saved at automation/tests/api/<Area>/<case id>.spec.ts, its first line names the case, and "
        "it has one test.step per case step, in order, each with at least one expect (a case with a Data sets table: "
        "one test per row, from a rows file); (C3) the spec calls the API only through the clients: no raw "
        "get/post/fetch, no hosts, URLs or credentials; a file other than the spec is edited only to add a missing "
        "client method under automation/clients/ (additions only) or to write the case's rows file; editing nothing "
        "else is correct when the clients were enough; (C4) type check and lint were run and the last run of each "
        "passed; (C5) the final run with --repeat-each=3 passed, or failed only on known product defects ('Known "
        "product defects only: F-..'), or the test is marked test.fixme with a FINDING or CASE DEFECT comment because "
        "the app differs from the case; (C6) a final report gives the spec path, the final run result, client "
        "changes, findings and left-over records. Stopping without writing a spec also completes the task when the "
        "case is not Approved. Any other failure to finish is not a correct stop." + FACTS_NOTE
    ),
}


def rel(path: str) -> str:
    """A path from a tool call, relative to the repository, with forward slashes."""
    p = Path(path)
    if p.is_absolute():
        try:
            p = p.relative_to(REPO)
        except ValueError:
            return path.replace("\\", "/")
    return p.as_posix()


def written_paths(run: Run) -> list[str]:
    paths = [c["input"].get("file_path", "") for c in run.tool_calls if c["name"] in ("Write", "Edit")]
    paths += [c["input"].get("fileName", "") for c in run.tool_calls if c["name"].endswith("generator_write_test")]
    return list(dict.fromkeys(rel(p) for p in paths if p))


def denied(run: Run) -> list[dict]:
    """The run's tool calls that the permission system stopped. They did not run, and stopping them was not the agent's choice."""
    return [c for c in run.tool_calls if c.get("error") and DENIED.match(c.get("output", "").lstrip())]


def denial_note(call: dict) -> str:
    """'browser_evaluate (auto mode classifier: Identity Not Given)', or '(declined by the user)'."""
    name, output = call["name"].rsplit("__", 1)[-1], call.get("output", "")
    if output.lstrip().startswith("The user"):
        return f"{name} (declined by the user)"
    by = re.search(r"denied by (?:the )?(?:Claude Code )?([^.]+)", output)
    reason = re.search(r"Reason: \[?([^\].]+)", output)
    return f"{name} ({by.group(1) if by else 'permission system'}" + (f": {reason.group(1).strip()})" if reason else ")")


def permission_evidence(run: Run) -> ToolCall:
    stopped = denied(run)
    if not stopped:
        return ToolCall(name="permissions", output="Permissions: no tool call was denied by Claude Code's permission system")
    return ToolCall(name="permissions", input_parameters={"denied": len(stopped)},
                    output=f"Permissions: {len(stopped)} tool call(s) were denied by Claude Code's permission system and "
                           f"did not run: {'; '.join(denial_note(c) for c in stopped)}. The denial comes from the "
                           "environment, not the agent; what the agent did next is part of the run.")


def case_user(case: dict | None) -> str | None:
    m = re.search(r"User: `(\w+)`", case["fields"].get("Prerequisites", "")) if case else None
    return m.group(1) if m else None


def case_evidence(case_id: str | None, label: dict) -> tuple[dict | None, ToolCall]:
    if not case_id:
        return None, ToolCall(name="read_case", output=f"{label['case']}: the request names no case ID")
    try:
        case = find_case(case_id)
    except KeyError:
        return None, ToolCall(name="read_case", input_parameters={"case": case_id},
                              output=f"{label['case']}: {case_id} does not exist in test-cases/")
    review = case["fields"].get("Review", "").split("·")[0].strip()
    steps = [s["n"] for s in case["steps"]]
    # The Expected results, so the judge can tell a correct negative assertion from a weakened one.
    expected = " ".join(f"Step {s['n']}: {s['expected']}" for s in case["steps"])[:1500]
    return case, ToolCall(name="read_case", input_parameters={"case": case_id},
                          output=f"{label['case']}: the case's Review is '{review}'. The case "
                                 f"({Path(case['file']).as_posix()}) has {len(steps)} steps, numbered {steps}; "
                                 f"its user is {case_user(case) or 'not stated'}. Its Expected results: {expected}")


def recording_evidence(run: Run, case: dict | None, label: dict) -> ToolCall:
    calls = run.tool_calls
    seeds = [c["input"].get("seedFile", "") for c in calls if c["name"].endswith("generator_setup_page")]
    if not seeds:
        return ToolCall(name="record_live", output=f"{label['live']}: no live recording: generator_setup_page was never called")
    user = case_user(case)
    seed_users = {m.group(1) for s in seeds for m in [re.search(r"seeds/(\w+)\.seed", s)] if m}
    browser = [c for c in calls if "__browser_" in c["name"]]
    checks = [c for c in browser if "browser_verify_" in c["name"]]
    failed = [c for c in checks if c.get("error") or "### Error" in c.get("output", "")]
    snapshots = sum(c["name"].endswith("browser_snapshot") for c in browser)
    not_run = sum(bool(c.get("error")) and DENIED.match(c.get("output", "").lstrip()) is not None for c in browser)

    def requests(evaluates: list[dict]) -> collections.Counter:
        return collections.Counter(m for c in evaluates
                                   for m in re.findall(r"method:\s*['\"](POST|PATCH|DELETE)['\"]", c["input"].get("function", "")))
    evaluates = [c for c in calls if c["name"].endswith("browser_evaluate")]
    # A denied or failed call is still in the transcript with its code, but its requests were not sent.
    sent = requests([c for c in evaluates if not c.get("error")])
    unsent = requests([c for c in evaluates if c.get("error")])
    cleanup = (f"{sent['POST']} create requests (POST) and {sent['DELETE']} delete requests (DELETE) sent through "
               f"browser_evaluate" + (", fewer deletes than creates" if sent["DELETE"] < sent["POST"] else "")
               if sent else "no records created through browser_evaluate")
    if unsent:
        cleanup += (f"; in browser_evaluate calls that were denied or failed: {unsent['POST']} POST and "
                    f"{unsent['DELETE']} DELETE (a denied call sent nothing)")
    # Records can also come from submitting a form during the recording, which no request count shows.
    typed = list(dict.fromkeys(
        m for c in browser if not c.get("error") and c["name"].endswith(("browser_type", "browser_fill_form"))
        for m in re.findall(r"QA-REC-[0-9A-Za-z]+(?: [^\"\\]+)?", json.dumps(c["input"]))))
    if typed:
        cleanup += (f"; QA-REC- names typed into forms in the browser (a submitted form creates the record, with no "
                    f"browser_evaluate request): {typed}")
    return ToolCall(
        name="record_live", input_parameters={"seeds": seeds},
        output=f"{label['live']}: live recording set up with {seeds}, which "
               f"{'matches' if user in seed_users else 'does not match'} the case user {user}; {len(browser)} browser "
               f"actions{f' ({not_run} denied, not run)' if not_run else ''}, {len(checks)} checks with browser_verify_* "
               f"({len(failed)} failed) and {snapshots} page snapshots. {label['cleanup']}: {cleanup}")


def spec_evidence(run: Run, case_id: str | None, case: dict | None, suite: str, label: dict) -> ToolCall:
    wrote = [p for p in written_paths(run) if p.endswith(".spec.ts")]
    found = sorted((REPO / "automation" / "tests" / suite).rglob(f"{case_id.lower()}.spec.ts")) if case_id else []
    if not found:
        return ToolCall(name="write_spec", output=f"{label['spec']}: no spec file for the case exists"
                        + (f"; the run wrote {wrote}" if wrote else ""))
    path = rel(str(found[0]))
    text = found[0].read_text(encoding="utf-8")
    facts = [f"{path} written by this run" if path in wrote else
             f"{path} exists, but this run did not write it" + (f" (the run wrote {wrote})" if wrote else "")]
    first = text.splitlines()[0] if text else ""
    facts.append("its first line names the case" if case_id in first else f"its first line does not name the case: {first[:80]!r}")

    numbers, without_expect = [], []
    for block in re.split(r"(?=\btest\.step\()", text)[1:]:
        m = re.match(r"test\.step\(\s*[`'\"](\d+)\.", block)
        numbers.append(int(m.group(1)) if m else None)
        if not re.search(r"\bexpect(?:\.soft)?\(", block):
            without_expect.append(numbers[-1])
    tests = len(re.findall(r"^\s*test(?:\.fixme)?\(", text, re.M))
    steps = list(dict.fromkeys(n for n in numbers if n is not None))
    case_steps = [s["n"] for s in case["steps"]] if case else []
    match = "yes" if steps == case_steps else "no"
    facts.append(f"{tests} test(s); one test.step per case step, in order: {match} (spec steps {steps}, case steps {case_steps})")
    facts.append(f"steps with no expect: {without_expect}" if without_expect else "every step has at least one expect")
    if "test.fixme" in text:
        notes = re.findall(r"//\s*(FINDING|CASE DEFECT):\s*(.+)", text)
        facts.append("marked test.fixme: " + ("; ".join(f"{k}: {v[:160]}" for k, v in notes) if notes
                                               else "with no FINDING or CASE DEFECT comment"))

    raw = sorted(set(re.findall(r"page\.(?:locator|getBy\w+)\(|from '@playwright/test'|"
                                r"\brequest\.(?:get|post|put|patch|delete|fetch)\(|\bfetch\(", text)))
    hard = sorted(set(re.findall(r"https?://\S+|localhost(?::\d+)?|btoa\(|Basic [A-Za-z0-9+/=]{8,}", text)))
    # The UI recording calls the API with admin credentials, as the generator's workflow says; C4 is about the spec.
    scope = (" in the spec file (C4 covers the spec only; the workflow has the recording's browser_evaluate calls use "
             "admin credentials)") if suite == "ui" else " in the spec file"
    style = [f"raw locators or requests in the spec: {raw}" if raw else "no raw locators, raw requests or @playwright/test import",
             f"possible hard-coded host or credentials: {hard}" if hard else f"no hard-coded host, URL or credentials{scope}"]
    return ToolCall(name="write_spec", input_parameters={"file": path},
                    output=f"{label['spec']}: " + "; ".join(facts) + f". {label['style']}: " + "; ".join(style))


def keeps_lines(old: str, new: str) -> bool:
    """True if every line of old appears in new, in the same order (new may add lines anywhere)."""
    remaining = iter(new.splitlines())
    return all(any(line == candidate for candidate in remaining) for line in old.splitlines())


def edit_evidence(run: Run, suite: str, label: dict) -> ToolCall:
    paths = [p for p in written_paths(run) if not p.endswith(".spec.ts")]
    # Files made only for the recording, such as an attachment to upload: not framework code.
    temporary = [p for p in paths if p.startswith(".playwright-mcp/") or "/AppData/Local/Temp/" in p]
    paths = [p for p in paths if p not in temporary]
    note = f"; temporary recording files written (not framework code): {temporary}" if temporary else ""
    if not paths:
        return ToolCall(name="edit_framework", output=f"{label['edits']}: no file other than the spec was edited{note}")
    outside = [p for p in paths if not any(re.match(a, p) for a in ALLOWED[suite])]
    # An addition keeps every line it anchors on, in order, with new lines possibly inserted between them;
    # an edit that drops or rewrites an old line changed existing code.
    changed = [rel(c["input"].get("file_path", "")) for c in run.tool_calls if c["name"] == "Edit"
               and not c["input"].get("file_path", "").endswith(".spec.ts")
               and not keeps_lines(c["input"].get("old_string", ""), c["input"].get("new_string", ""))]
    output = f"{label['edits']}: edited {paths}; "
    output += f"outside the folders this agent may edit: {outside}" if outside else "all inside the folders this agent may edit"
    output += f"; edits that changed existing lines: {changed}" if changed else "; every edit kept the existing text (additions only)"
    return ToolCall(name="edit_framework", input_parameters={"files": paths}, output=output + note)


def test_summary(call: dict) -> str:
    output = call.get("output", "")
    counts = re.findall(r"^\s*(\d+) (passed|failed|flaky|skipped|did not run)", output, re.M)
    if not counts:
        return "no summary line; output ends: " + output[-200:].strip()
    errors = list(dict.fromkeys(m.strip()[:200] for m in re.findall(r"^\s*Error: (.+)$", output, re.M)))
    return ", ".join(f"{n} {k}" for n, k in counts) + (f"; first errors: {errors[:2]}" if errors else "")


def checks_evidence(run: Run, label: dict) -> list[ToolCall]:
    bash = [c for c in run.tool_calls if c["name"] == "Bash"]
    calls = []
    for name, pattern in (("type_check", r"npm run typecheck|\btsc\b"), ("lint", r"\beslint\b")):
        runs = [c for c in bash if re.search(pattern, c["input"].get("command", ""))]
        if not runs:
            calls.append(ToolCall(name=name, output=f"{label['checks']}: {name.replace('_', ' ')} not run"))
            continue
        result = "passed" if not runs[-1].get("error") else "failed: " + runs[-1].get("output", "")[-300:].strip()
        calls.append(ToolCall(name=name, input_parameters={"runs": len(runs)},
                              output=f"{label['checks']}: {name.replace('_', ' ')} run {len(runs)} times; last run {result}"))

    tests = [c for c in bash if "playwright test" in c["input"].get("command", "")]
    final = [c for c in tests if re.search(r"--repeat-each[ =]3\b", c["input"]["command"])]
    if not tests:
        output = "the spec was never run"
    elif not final:
        output = f"{len(tests)} runs, none with --repeat-each=3; last run: {test_summary(tests[-1])}"
    else:
        output = f"{len(tests)} runs; final --repeat-each=3 run: {test_summary(final[-1])} (counts include the api-smoke setup tests)"
        if "Known product defects only" in final[-1].get("output", ""):
            output += "; the failures are labelled 'Known product defects only'"
    calls.append(ToolCall(name="run_spec", input_parameters={"runs": len(tests)}, output=f"{label['run']}: {output}"))
    return calls


def build_case(run: Run, agent_type: str) -> LLMTestCase:
    suite = SUITE[agent_type]
    label = LABEL[suite]
    m = re.search(CASE_ID, run.prompt)
    case_id = m.group(0) if m else None
    case, case_call = case_evidence(case_id, label)
    calls = [case_call]
    if suite == "ui":
        calls.append(recording_evidence(run, case, label))
    calls += [spec_evidence(run, case_id, case, suite, label), edit_evidence(run, suite, label)]
    if suite == "api":
        calls += checks_evidence(run, label)
    calls.append(permission_evidence(run))
    return LLMTestCase(
        input=run.prompt[:3000],
        actual_output=run.report or "(no final message: the run ended without a report)",
        tools_called=calls,
        metadata={"run": run.id, "case": case_id},
    )


def agent_version(agent_type: str, before: str, live: bool) -> str:
    """The agent file's last commit before the run started; '+uncommitted' when a live run used local edits."""
    file = f".claude/agents/{agent_type}.md"
    git = lambda *a: subprocess.run(["git", *a], cwd=REPO, capture_output=True, text=True)
    version = git("log", "-1", f"--before={before}", "--format=%h", "--", file).stdout.strip() or "untracked"
    if live and git("diff", "--quiet", "HEAD", "--", file).returncode:
        version += "+uncommitted"
    return version


def logged() -> list[dict]:
    """The latest score of each run: scoring a run again replaces its earlier score in the summary."""
    if not LOG.exists():
        return []
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    return list({r["run"]: r for r in rows}.values())


def score(transcript: Path, agent_type: str, run: Run, live: bool, dry_run: bool) -> dict | None:
    case = build_case(run, agent_type)
    if dry_run:
        print(json.dumps({"run": run.id, "agent": agent_type, "input": case.input, "actual_output": case.actual_output[:600],
                          "tools_called": [{"name": c.name, "output": c.output} for c in case.tools_called]}, indent=1))
        return None
    metric = TaskCompletionMetric(model=AnthropicModel(model=JUDGE), task=TASKS[agent_type], threshold=PASS_THRESHOLD,
                                  include_reason=True, async_mode=False)
    metric.measure(case, _show_indicator=False)
    record = {
        "scored": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session": transcript.parent.parent.name,
        "run": run.id,
        "started": run.started,
        "agent": agent_type,
        "agent_version": agent_version(agent_type, run.started, live),
        "case": case.metadata["case"],
        "reported": run.report is not None,
        "blocked": [denial_note(c) for c in denied(run)],  # tool calls the permission system stopped; [] = none
        "score": round(metric.score, 3),
        "passed": metric.score >= PASS_THRESHOLD,
        "reason": metric.reason,
        "judge": JUDGE,
        "cost_usd": metric.evaluation_cost,
    }
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    try_export("task_completion", record, ERRORS)  # to Grafana (Loki), when EVALS_OTLP_ENDPOINT is set
    return record


def hook(dry_run: bool) -> None:
    """SubagentStop input on stdin: agent_type, agent_transcript_path, session_id, ..."""
    event = json.load(sys.stdin)
    agent_type = event.get("agent_type")
    if agent_type not in SUITE:
        return
    transcript = Path(os.path.expanduser(event["agent_transcript_path"]))
    run = None
    for _ in range(5):  # the last transcript lines can land just after the hook fires
        run = load_run(transcript) if transcript.is_file() else None
        if run and run.report is not None:
            break
        time.sleep(2)
    if run is None:
        raise RuntimeError(f"no run found in {transcript}")
    if dry_run or run.id not in {r["run"] for r in logged()}:
        score(transcript, agent_type, run, live=True, dry_run=dry_run)


def generator_runs(since: str) -> list[tuple[Path, str, Run]]:
    runs = []
    for meta in TRANSCRIPTS.glob("*/subagents/*.meta.json"):
        agent_type = json.loads(meta.read_text(encoding="utf-8")).get("agentType")
        if agent_type in SUITE:
            transcript = meta.with_suffix("").with_suffix(".jsonl")
            run = load_run(transcript)
            if run and run.started >= since:
                runs.append((transcript, agent_type, run))
    return sorted(runs, key=lambda r: r[2].started)


def was_blocked(r: dict) -> bool:
    """True if the permission system stopped a tool call in the run. A score logged before the 'blocked' field existed
    is checked against its transcript, if that is still there."""
    if "blocked" in r:
        return bool(r["blocked"])
    transcript = TRANSCRIPTS / r["session"] / "subagents" / f"{r['run']}.jsonl"
    run = load_run(transcript) if transcript.is_file() else None
    return bool(run and denied(run))


def summary() -> None:
    rows = logged()
    if not rows:
        print(f"No scores yet in {LOG}")
        return
    groups = collections.defaultdict(list)
    for r in rows:
        r = {**r, "blocked": was_blocked(r)}
        groups[(r["agent"], r["agent_version"])].append(r)
        groups[(r["agent"], "all versions")].append(r)
    print(f"{'agent':28} {'version':22} {'runs':>4} {'blocked':>7} {'passed':>7} {'mean':>5} {'cost $':>7}")
    for (agent, version), rs in sorted(groups.items()):
        clear = [r for r in rs if not r["blocked"]]
        passed = f"{sum(r['passed'] for r in clear) / len(clear):>6.0%}" if clear else f"{'n/a':>6}"
        mean = f"{sum(r['score'] for r in clear) / len(clear):>5.2f}" if clear else f"{'n/a':>5}"
        cost = sum(r["cost_usd"] or 0 for r in rs)
        print(f"{agent:28} {version:22} {len(rs):>4} {len(rs) - len(clear):>7} {passed} {mean} {cost:>7.3f}")
    print("passed and mean leave out blocked runs (a tool call denied by Claude Code's permission system); "
          "their scores stay in the log.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--hook", action="store_true", help="read a SubagentStop event on stdin (used by the hook)")
    parser.add_argument("--transcript", type=Path, help="score one run: a subagents/agent-<id>.jsonl file")
    parser.add_argument("--since", help="score every generator run since this date (YYYY-MM-DD) not yet in the log")
    parser.add_argument("--summary", action="store_true", help="print pass rate and mean score per agent version")
    parser.add_argument("--dry-run", action="store_true", help="print the test case; no judge call, nothing logged")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if args.hook:
        try:
            hook(args.dry_run)
        except Exception:  # a background hook has nowhere to show errors, so keep them
            ERRORS.parent.mkdir(exist_ok=True)
            with ERRORS.open("a", encoding="utf-8") as f:
                f.write(f"{datetime.now(timezone.utc).isoformat(timespec='seconds')}\n{traceback.format_exc()}\n")
        return

    todo = []
    if args.transcript:
        agent_type = json.loads(args.transcript.with_suffix(".meta.json").read_text(encoding="utf-8")).get("agentType")
        if agent_type not in SUITE:
            sys.exit(f"{args.transcript} is a {agent_type} run, not an automation generator run")
        todo.append((args.transcript, agent_type, load_run(args.transcript)))
    if args.since:
        done = {r["run"] for r in logged()}
        todo += [t for t in generator_runs(args.since) if args.dry_run or t[2].id not in done]
    for transcript, agent_type, run in todo:
        record = score(transcript, agent_type, run, live=False, dry_run=args.dry_run)
        if record:
            print(f"{record['case']} ({agent_type}, {record['started'][:16]}): {record['score']:.2f} "
                  f"{'pass' if record['passed'] else 'FAIL'}\n  {record['reason']}")
    if args.summary or (todo and not args.dry_run):
        summary()


if __name__ == "__main__":
    main()
