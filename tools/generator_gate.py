"""Case-fidelity gate: refuses a playwright-test-generator spec write that does not match its Approved case.

A PreToolUse hook (.claude/settings.json, matcher generator_write_test|Write|Edit) runs this before the tool call.
For playwright-test-generator only, and only for a spec in automation/tests/ui/<Area>/, it builds the file as the
call would leave it and runs tools/case_fidelity.py on it:
  - no problems: exit 0, and the write goes ahead;
  - problems: exit 2, so the write is refused and stderr goes back to the generator as the reason. The generator
    keeps its whole context (the same run carries on), so it fixes the lines named and writes the spec again;
  - MAX_BLOCKS refusals for the same spec in one run: still refused, but now the message tells the generator to stop
    retrying and report the mismatch to its caller as a CASE DEFECT or FINDING for the architect. The gate fails
    closed: the generator never writes a spec that does not match its case.
A crash in the gate itself lets the write through (exit 0) and is logged: a gate bug must not stop the work.
Every decision is appended to evals/results/generator_gate.jsonl (GATE_LOG overrides the path, for tests).

Why PreToolUse and not SubagentStop: in VS Code the generator hands its report back with SubagentHandback, which
delivers it before the agent stops, so a SubagentStop block comes after the report reached the caller. Refusing the
write itself also limits the gate to the spec this run is writing: a spec or page object from an earlier run never
blocks it.
"""

import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from case_fidelity import REPO, SPEC_PATH, check  # noqa: E402

AGENT = "playwright-test-generator"
WRITE_TEST = "mcp__playwright-test__generator_write_test"
MAX_BLOCKS = 3
LOG = Path(os.environ.get("GATE_LOG") or REPO / "evals" / "results" / "generator_gate.jsonl")


def proposed(tool: str, args: dict) -> tuple[str, str] | None:
    """(spec path relative to the repo, file text after the call), or None if the call does not write a UI spec."""
    if tool == WRITE_TEST:
        path, text = args.get("fileName", ""), args.get("code")
    elif tool == "Write":
        path, text = args.get("file_path", ""), args.get("content")
    elif tool == "Edit":
        path = args.get("file_path", "")
        file = Path(path) if Path(path).is_absolute() else REPO / path
        old = args.get("old_string", "")
        current = file.read_text(encoding="utf-8") if file.is_file() else None
        if current is None or not old or old not in current:
            return None  # the Edit fails on its own
        text = current.replace(old, args.get("new_string", ""), -1 if args.get("replace_all") else 1)
    else:
        return None
    path = path.replace("\\", "/")
    m = SPEC_PATH.search(path)
    if not m or text is None:
        return None
    return m.group(0), text


def earlier_blocks(agent_id: str, spec: str) -> int:
    if not LOG.is_file():
        return 0
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    return sum(r.get("agent_id") == agent_id and r.get("spec") == spec and r.get("decision") in ("block", "escalate")
               for r in rows)


def log(record: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def message(result, spec: str, tool: str, attempt: int) -> str:
    problems = "\n".join(f"- {p}" for p in result.problems)
    limit = f"the limit of {MAX_BLOCKS} is reached" if attempt >= MAX_BLOCKS else f"after {MAX_BLOCKS} you must stop"
    case = f"its case {result.case_id} ({result.case_file})" if result.case_id else "its case"
    head = (f"CASE-FIDELITY GATE: refused. {spec} was NOT written (refusal {attempt}; {limit}).\n"
            f"It does not match {case}, which is the specification (guardrail 2):\n{problems}\n")
    if result.not_approved:
        return (f"CASE-FIDELITY GATE: refused. {spec} was NOT written.\n{problems}\n"
                "Guardrail 1: write nothing for this case. Stop and report to your caller that it is not Approved.")
    if attempt >= MAX_BLOCKS:
        return head + ("Stop retrying this spec. Report to your caller that the spec could not be made to match the "
                       "case, list the problems above, and say whether you think the case or the app is wrong "
                       "(CASE DEFECT or FINDING). The architect decides; do not work around it.")
    again = "write the whole spec again to the same path with generator_write_test" if tool == WRITE_TEST \
        else "make the same call again"
    return head + (f"Fix only these lines and {again}. Nothing was saved, so there is no other copy to keep in step: "
                   "do not create another spec, page object or method for this. If the case itself is wrong, do not "
                   "work around it: stop and report it as a CASE DEFECT.")


def main() -> int:
    event = json.load(sys.stdin)
    if event.get("agent_type") != AGENT:
        return 0
    write = proposed(event.get("tool_name", ""), event.get("tool_input") or {})
    if write is None:
        return 0
    spec, text = write
    result = check(text, spec)
    record = {"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "agent_id": event.get("agent_id"),
              "session_id": event.get("session_id"), "tool": event.get("tool_name"), "spec": spec,
              "case": result.case_id, "problems": [str(p) for p in result.problems],
              "warnings": [str(w) for w in result.warnings]}
    if result.ok:
        log({**record, "decision": "pass"})
        return 0
    attempt = earlier_blocks(event.get("agent_id"), spec) + 1
    log({**record, "decision": "escalate" if attempt >= MAX_BLOCKS else "block", "attempt": attempt})
    sys.stderr.write(message(result, spec, event.get("tool_name", ""), attempt))
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # noqa: BLE001 - a gate bug lets the write through, and is kept for the architect
        try:
            log({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "decision": "error",
                 "error": traceback.format_exc()})
        finally:
            sys.exit(0)
