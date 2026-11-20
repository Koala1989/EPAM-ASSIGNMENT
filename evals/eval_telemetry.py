"""Sends each eval score to OpenTelemetry as one log event, so Grafana can show scores next to Claude Code's telemetry.

automation_task_completion.py and automation_review_score.py call export() right after they log a score (the JSONL
files in results/ stay the source of truth). Each score becomes one OTLP log event with service.name "agent-evals":
the otel-lgtm collector stores it in Loki, where LogQL computes means and pass rates (`| unwrap score`).

Why log events and not Prometheus metrics: every hook is a short-lived process, so its counters would start at zero
and overwrite the previous process's value; an event per score is exact. Case and run IDs are attributes (Loki
structured metadata), not metric labels, so they add no series.

The event's agent_id is the generator run's ID (the "agent-<id>" run in the JSONL logs, and agent_id in Claude Code's
own events), so a run's cost and its scores can be joined. Each event is stamped with its scoring time. Every process
writes its own Loki stream (the SDK gives each a random service.instance.id), so running --backfill twice sends
duplicates: it is a one-time step (done 2026-11-06). Re-scoring a run sends a new event next to the old one.

The collector endpoint comes from EVALS_OTLP_ENDPOINT (OTLP gRPC), set in evals/.env.local (gitignored; DeepEval
loads it), or in the environment. Unset means no export.

Run from evals/ ($env:PYTHONUTF8 = "1" first):
  .venv\\Scripts\\python.exe eval_telemetry.py --backfill            send every logged score (latest per run)
  .venv\\Scripts\\python.exe eval_telemetry.py --backfill --dry-run  print the events instead
"""

import argparse
import json
import os
import sys
from datetime import datetime

ENDPOINT_VAR = "EVALS_OTLP_ENDPOINT"
SERVICE = "agent-evals"
NAMESPACE = "epam-inventree"  # an index label in Loki: the dashboard selects {service_namespace="epam-inventree"}
GENERATOR = {"ui": "playwright-test-generator", "api": "api-test-generator"}


def _ns(iso: str) -> int:
    return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp() * 1e9)


def _run_id(run: str | None) -> str:
    return (run or "").removeprefix("agent-")


def event(metric: str, r: dict) -> dict | None:
    """The log event for one logged score: {"timestamp", "body", "attributes"}; None if it has no score."""
    if r.get("score") is None:
        return None
    if metric == "task_completion":
        agent, version, run = r["agent"], r["agent_version"], r["run"]
        extra = {"judge": r.get("judge", ""), "cost_usd": float(r.get("cost_usd") or 0.0),
                 "reported": bool(r.get("reported")), "started": r.get("started", ""),
                 "suite": "ui" if agent.startswith("playwright") else "api"}
        detail = ""
    else:
        agent, version, run = GENERATOR[r["suite"]], r.get("generator_version") or "unknown", r.get("generator_run")
        f = r["findings"]
        extra = {"suite": r["suite"], "reviewer": r["reviewer"], "reviewer_version": r["reviewer_version"],
                 "reviewer_agent_id": _run_id(r.get("reviewer_run")), "verdict": r["verdict"] or "",
                 "coverage": float(r["coverage"]), "blockers": f["Blocker"], "majors": f["Major"],
                 "minors": f["Minor"], "infos": f["Info"], "review": r["review"], "cost_usd": 0.0}
        detail = f" · {r['verdict']} ({f['Blocker']} Blocker, {f['Major']} Major, {f['Minor']} Minor)"
    label = "TaskCompletion" if metric == "task_completion" else "ReviewScore"
    passed = bool(r["passed"])
    body = (f"{label} {r['score']:.2f} {'pass' if passed else 'FAIL'} · {r['case']} · {agent} {version}"
            f" · agent-{_run_id(run) or '?'}{detail}")
    attributes = {"eval_metric": metric, "score": float(r["score"]), "passed": passed, "case": r["case"] or "",
                  "agent": agent, "agent_version": version, "agent_id": _run_id(run),
                  "session_id": r.get("session") or "", "scored": r["scored"],
                  "reason": (r.get("reason") or "")[:1500], **extra}
    return {"timestamp": _ns(r["scored"]), "body": body, "attributes": attributes}


def export(items: list[tuple[str, dict]]) -> int:
    """Send these (metric, logged score) pairs; returns how many were sent (0 when no endpoint is configured).
    Raises RuntimeError if the collector did not accept them.

    Events go out oldest first: Loki refuses an entry that is more than about an hour older than the newest entry
    already in its stream, so history must arrive in time order, and both metrics share one stream."""
    endpoint = os.environ.get(ENDPOINT_VAR, "").strip()
    events = sorted((e for e in (event(m, r) for m, r in items) if e), key=lambda e: e["timestamp"])
    if not endpoint or not events:
        return 0
    from opentelemetry._logs import SeverityNumber
    from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
    from opentelemetry.sdk._logs import LoggerProvider, LogRecordProcessor
    from opentelemetry.sdk._logs.export import LogRecordExportResult
    from opentelemetry.sdk.resources import Resource

    class Collect(LogRecordProcessor):  # export once at the end, so the result can be checked
        def __init__(self):
            self.records = []

        def on_emit(self, log_record):
            self.records.append(log_record)

        def shutdown(self):
            pass

        def force_flush(self, timeout_millis: int = 30000) -> bool:
            return True

    collect = Collect()
    provider = LoggerProvider(resource=Resource.create({"service.name": SERVICE, "service.namespace": NAMESPACE,
                                                        "project": NAMESPACE, "env": "local"}))
    provider.add_log_record_processor(collect)
    logger = provider.get_logger(SERVICE)
    for e in events:
        logger.emit(timestamp=e["timestamp"], observed_timestamp=e["timestamp"], body=e["body"],
                    attributes=e["attributes"], event_name="eval_score", severity_number=SeverityNumber.INFO,
                    severity_text="INFO")
    exporter = OTLPLogExporter(endpoint=endpoint, insecure=endpoint.startswith("http://"), timeout=10)
    try:
        result = exporter.export(collect.records)
    finally:
        exporter.shutdown()
    if result != LogRecordExportResult.SUCCESS:
        raise RuntimeError(f"OTLP export of {len(events)} event(s) to {endpoint} failed: {result}")
    return len(events)


def try_export(metric: str, record: dict, errors_file) -> None:
    """For the scoring scripts: export one score, never failing the scoring (the JSONL row is already written)."""
    try:
        export([(metric, record)])
    except Exception as e:  # noqa: BLE001
        errors_file.parent.mkdir(exist_ok=True)
        with errors_file.open("a", encoding="utf-8") as f:
            f.write(f"{datetime.now().astimezone().isoformat(timespec='seconds')} eval_telemetry: {e}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--backfill", action="store_true", help="send every logged score (latest per run)")
    parser.add_argument("--dry-run", action="store_true", help="print the events; nothing sent")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if not args.backfill:
        parser.print_help()
        return
    # These imports also load evals/.env.local through DeepEval.
    import automation_review_score
    import automation_task_completion

    items = [("task_completion", r) for r in automation_task_completion.logged()]
    items += [("review_score", r) for r in automation_review_score.logged()]
    if args.dry_run:
        for e in sorted(filter(None, (event(m, r) for m, r in items)), key=lambda e: e["timestamp"]):
            print(json.dumps({"body": e["body"], **{k: e["attributes"][k] for k in ("agent_id", "session_id", "scored")}}))
        return
    if not os.environ.get(ENDPOINT_VAR):
        sys.exit(f"{ENDPOINT_VAR} is not set (evals/.env.local or the environment)")
    print(f"sent {export(items)} event(s), oldest first")


if __name__ == "__main__":
    main()
