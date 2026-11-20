"""ReviewScore for the automation generators: the reviewer agents' verdict on each generated spec, as a 0-1 score.

A SubagentStop hook (.claude/settings.json) runs this in the background when playwright-test-reviewer or
api-test-reviewer finishes: it scores each review file the run wrote with ReviewScoreMetric (review_metric.py),
appends the result to results/automation_review_score.jsonl and sends it to Grafana as a log event
(eval_telemetry.py). Scoring is parsing only: no LLM call, $0.

Each record names the generator run that wrote the spec (the latest generator run for the case before the review) and
that generator's git version, so the summary groups by generator version, next to TaskCompletion
(automation_task_completion.py). The healer may change a spec between generation and review: the review scores the
spec it saw.

Run from evals/:
  .venv\\Scripts\\python.exe automation_review_score.py --all                 score every review file not yet logged
  .venv\\Scripts\\python.exe automation_review_score.py --file <review.md>    score one review file (again)
  .venv\\Scripts\\python.exe automation_review_score.py --summary             per generator version, free
  .venv\\Scripts\\python.exe automation_review_score.py --scorecard           per case: TaskCompletion and ReviewScore
  add --dry-run to print the score without logging it
"""

import argparse
import collections
import json
import os
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

EVALS = Path(__file__).resolve().parent
os.environ.setdefault("ENV_DIR_PATH", str(EVALS))

from deepeval.test_case import LLMTestCase  # noqa: E402

from agent_traces import TRANSCRIPTS, Run, load_run  # noqa: E402
from automation_task_completion import ERRORS, SUITE, agent_version  # noqa: E402
from automation_task_completion import logged as task_completion_scores  # noqa: E402
from case_sources import REPO  # noqa: E402
from eval_telemetry import try_export  # noqa: E402
from review_metric import ReviewScoreMetric  # noqa: E402

LOG = EVALS / "results" / "automation_review_score.jsonl"
REVIEWS = REPO / "automation" / "reviews"
REVIEWERS = {"playwright-test-reviewer": "ui", "api-test-reviewer": "api"}
GENERATOR = {suite: agent for agent, suite in SUITE.items()}
REVIEW_FILE = re.compile(r"automation/reviews/(ui|api)/[^/]+-review-[^/]+\.md$")


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def runs_of(agent_types) -> list[tuple[Path, str, Run]]:
    runs = []
    for meta in TRANSCRIPTS.glob("*/subagents/*.meta.json"):
        agent_type = json.loads(meta.read_text(encoding="utf-8")).get("agentType")
        if agent_type in agent_types:
            transcript = meta.with_suffix("").with_suffix(".jsonl")
            run = load_run(transcript)
            if run:
                runs.append((transcript, agent_type, run))
    return sorted(runs, key=lambda r: r[2].started)


def review_files(run: Run) -> list[Path]:
    paths = {p for p in run.written if REVIEW_FILE.search(p)}
    return sorted(Path(p) if Path(p).is_absolute() else REPO / p for p in paths)


def generator_of(case: str | None, suite: str, before: str, generators) -> tuple[str | None, str | None]:
    """The latest generator run for this case that started before the review, and that generator's version."""
    agent = GENERATOR[suite]
    match = [run for _, a, run in generators
             if a == agent and case and re.search(rf"\b{re.escape(case)}\b", run.prompt) and run.started < before]
    if not match:
        return None, None
    return match[-1].id, agent_version(agent, match[-1].started, live=False)


def score(path: Path, reviewer: tuple[Path, str, Run] | None, generators, live: bool, dry_run: bool) -> dict:
    suite = REVIEW_FILE.search(rel(path)).group(1)
    text = path.read_text(encoding="utf-8")
    metric = ReviewScoreMetric()
    metric.measure(LLMTestCase(input=f"Review of {path.name}", actual_output=text))
    review = metric.review
    reviewer_agent = reviewer[1] if reviewer else next(a for a, s in REVIEWERS.items() if s == suite)
    if reviewer:
        started = reviewer[2].started
    else:  # no transcript: the review date from the header's Reviewer row, or else the file name
        date = re.search(r"^\| Reviewer \|.*?(\d{4}-\d{2}-\d{2})", text, re.M) or re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
        started = f"{date.group(1)}T23:59:59Z"
    generator_run, generator_version = generator_of(review.case, suite, started, generators)
    record = {
        "scored": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "review": rel(path),
        "suite": suite,
        "case": review.case,
        "spec": review.spec,
        "session": reviewer[0].parent.parent.name if reviewer else None,
        "reviewer_run": reviewer[2].id if reviewer else None,
        "reviewed": started,
        "reviewer": reviewer_agent,
        "reviewer_version": agent_version(reviewer_agent, started, live),
        "generator_run": generator_run,
        "generator_version": generator_version,
        "verdict": review.verdict,
        "findings": review.findings,
        "rows": review.rows,
        "coverage": metric.score_breakdown["coverage"] if metric.score is not None else None,
        "score": metric.score,
        "passed": metric.is_successful(),
        "reason": metric.reason,
        "cost_usd": 0.0,
    }
    if dry_run:
        print(json.dumps(record, indent=1))
    else:
        LOG.parent.mkdir(exist_ok=True)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        try_export("review_score", record, ERRORS)  # to Grafana (Loki), when EVALS_OTLP_ENDPOINT is set
    return record


def logged() -> list[dict]:
    """The latest score of each review file."""
    if not LOG.exists():
        return []
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    return list({r["review"]: r for r in rows}.values())


def final_reviews() -> list[dict]:
    """One review per spec as a generator run left it: the latest review of each (case, generator run)."""
    rows = sorted((r for r in logged() if r["score"] is not None), key=lambda r: r["reviewed"])
    return list({(r["case"], r["generator_run"] or r["review"]): r for r in rows}.values())


def summary() -> None:
    rows = final_reviews()
    if not rows:
        print(f"No scores yet in {LOG}")
        return
    groups = collections.defaultdict(list)
    for r in rows:
        agent = GENERATOR[r["suite"]]
        groups[(agent, r["generator_version"] or "unknown")].append(r)
        groups[(agent, "all versions")].append(r)
    print(f"{'generator':28} {'version':14} {'specs':>5} {'passed':>7} {'mean':>5} {'coverage':>8} {'Blk':>4} {'Maj':>4}")
    for (agent, version), rs in sorted(groups.items()):
        n = len(rs)
        print(f"{agent:28} {version:14} {n:>5} {sum(r['passed'] for r in rs) / n:>6.0%} "
              f"{sum(r['score'] for r in rs) / n:>5.2f} {sum(r['coverage'] for r in rs) / n:>8.0%} "
              f"{sum(r['findings']['Blocker'] for r in rs):>4} {sum(r['findings']['Major'] for r in rs):>4}")
    unparsed = [r["review"] for r in logged() if r["score"] is None]
    if unparsed:
        print(f"\nNot in the reviewer format, no score: {', '.join(unparsed)}")


def scorecard() -> None:
    task = {r["run"]: r for r in task_completion_scores()}
    print(f"{'case':22} {'reviewed':10} {'task completion':>15} {'review score':>12}  verdict")
    for r in sorted(final_reviews(), key=lambda r: (r["case"] or "", r["reviewed"])):
        tc = task.get(r["generator_run"])
        tc_score = f"{tc['score']:.2f}" if tc else "-"
        print(f"{r['case'] or '?':22} {r['reviewed'][:10]:10} {tc_score:>15} {r['score']:>12.2f}  {r['verdict']}")


def hook(dry_run: bool) -> None:
    """SubagentStop input on stdin: agent_type, agent_transcript_path, session_id, ..."""
    event = json.load(sys.stdin)
    agent_type = event.get("agent_type")
    if agent_type not in REVIEWERS:
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
    files = review_files(run)
    if not files:
        raise RuntimeError(f"{agent_type} run {run.id} wrote no review file")
    done = {r["review"] for r in logged()}
    generators = runs_of(SUITE)
    for path in files:
        if dry_run or rel(path) not in done:
            score(path, (transcript, agent_type, run), generators, live=True, dry_run=dry_run)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--hook", action="store_true", help="read a SubagentStop event on stdin (used by the hook)")
    parser.add_argument("--file", type=Path, nargs="+", help="score these review files (again)")
    parser.add_argument("--all", action="store_true", help="score every review file not yet in the log")
    parser.add_argument("--summary", action="store_true", help="pass rate, mean score and coverage per generator version")
    parser.add_argument("--scorecard", action="store_true", help="per case: TaskCompletion and ReviewScore side by side")
    parser.add_argument("--dry-run", action="store_true", help="print the score; nothing logged")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if args.hook:
        try:
            hook(args.dry_run)
        except Exception:  # a background hook has nowhere to show errors, so keep them
            ERRORS.parent.mkdir(exist_ok=True)
            with ERRORS.open("a", encoding="utf-8") as f:
                f.write(f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} automation_review_score\n"
                        f"{traceback.format_exc()}\n")
        return

    todo = [p.resolve() for p in args.file or []]
    if args.all:
        done = {r["review"] for r in logged()}
        todo += [p for p in sorted(REVIEWS.glob("*/*-review-*.md")) if args.dry_run or rel(p) not in done]
    if todo:
        writer = {}  # review file -> the reviewer run that wrote it
        for t in runs_of(REVIEWERS):
            for path in review_files(t[2]):
                writer[rel(path)] = t
        generators = runs_of(SUITE)
        for path in todo:
            record = score(path, writer.get(rel(path)), generators, live=False, dry_run=args.dry_run)
            if not args.dry_run:
                shown = "no score" if record["score"] is None else f"{record['score']:.2f} {'pass' if record['passed'] else 'FAIL'}"
                print(f"{record['case']} ({record['review']}): {shown}\n  {record['reason']}")
    if args.summary or (todo and not args.dry_run):
        summary()
    if args.scorecard:
        scorecard()


if __name__ == "__main__":
    main()
