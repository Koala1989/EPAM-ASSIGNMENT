"""Run every eval suite and print one summary table.

Free suites (no LLM calls) run by default; judged suites call the Claude judge and cost API credit, so they run
only with --judged. Run from evals/:

    .venv\\Scripts\\python.exe run_evals.py             free only (about 2 minutes)
    .venv\\Scripts\\python.exe run_evals.py --judged    free, then judged (about $0.40 in total, 10 minutes)

Each suite runs as its own pytest process; its full output is saved to reports/<suite>.log.
"""

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
REPORTS = HERE / "reports"

# (name, pytest arguments, judged?, approximate cost)
SUITES = [
    ("Step 4 retrieval, free", ["test_retrieval.py", "-m", "not judged"], False, "free"),
    ("Step 6 agent behaviour", ["test_agent_behaviour.py"], False, "free"),
    ("Step 4 retrieval, judged", ["test_retrieval.py", "-m", "judged"], True, "~$0.20"),
    ("Step 5 traceability controls", ["test_agent_cases.py", "-k", "planted"], True, "~$0.02"),
    ("Step 5 traceability, 8 cases", ["test_agent_cases.py", "-k", "sample"], True, "~$0.05"),
    ("Step 6 task completion", ["test_agent_task_completion.py"], True, "~$0.10"),
]
COUNTS = re.compile(r"(\d+) (passed|failed|skipped|xfailed|xpassed|error|errors|deselected)")


def run(name: str, args: list[str]) -> tuple[dict, float]:
    REPORTS.mkdir(exist_ok=True)
    started = time.time()
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", *args, "-q", "-rfEsxX", "-W", "ignore", "-p", "no:cacheprovider"],
        cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    log = REPORTS / (re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + ".log")
    log.write_text(proc.stdout + proc.stderr, encoding="utf-8")
    last = [line for line in proc.stdout.splitlines() if COUNTS.search(line)]
    counts = {kind: int(n) for n, kind in COUNTS.findall(last[-1])} if last else {"error": 1}
    return counts, time.time() - started


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--judged", action="store_true", help="also run the judged suites (costs API credit)")
    judged = parser.parse_args().judged

    rows, failed = [], False
    for name, args, is_judged, cost in SUITES:
        if is_judged and not judged:
            rows.append((name, cost, "not run (use --judged)", ""))
            continue
        print(f"running: {name} ...", flush=True)
        counts, secs = run(name, args)
        failed |= bool(counts.get("failed") or counts.get("error") or counts.get("errors"))
        summary = ", ".join(f"{n} {k}" for k, n in counts.items() if k != "deselected")
        rows.append((name, cost, summary, f"{secs:.0f}s"))

    width = max(len(r[0]) for r in rows)
    print(f"\n{'Suite':{width}}  {'Cost':7}  {'Result':48}  Time")
    for name, cost, summary, secs in rows:
        print(f"{name:{width}}  {cost:7}  {summary:48}  {secs}")
    print(f"\nFull output per suite: {REPORTS}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
