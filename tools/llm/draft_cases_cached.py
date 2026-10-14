"""Draft manual test cases through the Claude API with explicit prompt caching.

Demonstrates prompt caching: one sequential call per requirement rule,
all sharing a byte-identical cached prefix (instructions, seed template,
requirements inventory). Only the rule and its RAG-retrieved doc
passages vary per call, so they go after the cache breakpoint. The first
call writes the cache; every later call within the TTL reads it.

Drafts are review material only: they are written to agents/runs/, not
to test-cases/, and do not replace the test-case-creator agent, the
duplicate check or the architect's review.

Usage (run with the tools venv, which also has the RAG dependencies):
    tools/rag/.venv/Scripts/python.exe tools/llm/draft_cases_cached.py \
        --area Part --rule R-Part-12 --rule R-Part-14 --rule R-Part-16 [--dry-run]

Needs ANTHROPIC_API_KEY unless --dry-run. Each live call is billed.
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools" / "rag"))
sys.path.insert(0, str(REPO_ROOT / "tools"))
from areas import area_folder  # noqa: E402

SEED = REPO_ROOT / "references" / "seed-manual-test-case.md"
INVENTORY_INDEX = REPO_ROOT / "test-cases" / "requirements-inventory.md"
RUNS_DIR = REPO_ROOT / "agents" / "runs"
DEFAULT_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")

# Prefixes shorter than the model's minimum cacheable length are silently
# not cached. 4096 covers the strictest current models.
MIN_CACHEABLE_TOKENS = 4096

INSTRUCTIONS = """You are a senior QA engineer drafting manual functional test cases for InvenTree 1.5.6's Parts module, for review by a QA architect.

Rules:
1. Follow the seed template below exactly: every field, in the same order; `None` where a field does not apply.
2. Draft cases only for the rule given in the user message. Cite its rule ID and source link in Requirement.
3. Use only the rule, the retrieved doc passages and the inventory below as requirements. Do not use your own knowledge of InvenTree.
4. Do not assume anything. If an Expected result, limit, default, label or error text is not stated, write `Not known: <what is unknown>` in that cell (or `[open: <what is unknown>]` in other cells) and list it under "Open questions" after the cases.
5. Review is always `Draft`. IDs are `UI-<Area>-DRAFT-NN`, numbered from 01 for each rule.
6. Apply the test design techniques that fit (equivalence partitioning, boundary values, state transition, decision table, error guessing, negative) and name them in each case's Technique field.
7. Output only Markdown: the cases, then an "Open questions" list (or "Open questions: None")."""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rule_row(inventory: str, rule_id: str) -> str:
    match = re.search(rf"^\| {re.escape(rule_id)} \|.*$", inventory, re.MULTILINE)
    if not match:
        sys.exit(f"Rule {rule_id} not found in the Area inventory.")
    return match.group(0)


def rule_text(row: str) -> str:
    return row.split("|")[2].strip()


def build_system(area_inventory: str, ttl: str) -> list[dict]:
    # Order matters: the cached prefix is everything up to and including the
    # block that carries cache_control, so stable content goes first.
    return [
        {"type": "text", "text": INSTRUCTIONS},
        {"type": "text", "text": "# Seed template\n\n" + read(SEED)},
        {"type": "text", "text": "# Requirements inventory index\n\n" + read(INVENTORY_INDEX)},
        {
            "type": "text",
            "text": "# Area requirements inventory\n\n" + area_inventory,
            "cache_control": {"type": "ephemeral", "ttl": ttl},
        },
    ]


def build_user_message(area: str, row: str, passages: list[dict]) -> str:
    if passages:
        docs = "\n\n".join(f"[{p['citation']}]\n{p['text']}" for p in passages)
    else:
        docs = "None retrieved."
    return (
        f"Draft UI test cases for Area {area}, rule:\n\n{row}\n\n"
        f"Retrieved doc passages (local RAG index, InvenTree 1.5.6 docs):\n\n{docs}"
    )


def estimate_tokens(text: str) -> int:
    return len(text) // 4


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--area", required=True, help="Area value, e.g. Part or ATT (its folder is looked up)")
    parser.add_argument("--rule", action="append", required=True, help="rule ID; repeat for several")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--ttl", choices=["5m", "1h"], default="5m")
    parser.add_argument("--top-k", type=int, default=3, help="RAG passages per rule")
    parser.add_argument("--no-rag", action="store_true", help="send the rule row without doc passages")
    parser.add_argument("--max-tokens", type=int, default=4000)
    parser.add_argument("--dry-run", action="store_true", help="build and show the requests, call nothing")
    args = parser.parse_args()

    inventory_path = area_folder(args.area) / "requirements-inventory.md"
    if not inventory_path.is_file():
        sys.exit(f"No inventory at {inventory_path}")
    area_inventory = read(inventory_path)
    rows = {rule_id: rule_row(area_inventory, rule_id) for rule_id in args.rule}

    system = build_system(area_inventory, args.ttl)
    prefix_tokens = estimate_tokens("".join(block["text"] for block in system))

    search = None
    if not args.no_rag:
        from query_index import search

    requests = []
    for rule_id, row in rows.items():
        passages = search(rule_text(row), top_k=args.top_k) if search else []
        requests.append((rule_id, build_user_message(args.area, row, passages), passages))

    print(f"Cached prefix: {len(system)} system blocks, ~{prefix_tokens} tokens (estimate), "
          f"breakpoint on the last block, TTL {args.ttl}.")
    if prefix_tokens < MIN_CACHEABLE_TOKENS:
        print(f"Warning: prefix may be below the model's minimum cacheable length "
              f"({MIN_CACHEABLE_TOKENS}); caching would silently not apply.")

    if args.dry_run:
        for rule_id, message, passages in requests:
            cites = ", ".join(p["citation"] for p in passages) or "none"
            print(f"- {rule_id}: user message ~{estimate_tokens(message)} tokens (not cached); "
                  f"RAG passages: {cites}")
        print("Dry run: no API calls made.")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Use --dry-run to inspect the requests without it.")

    import anthropic

    client = anthropic.Anthropic()
    run_dir = RUNS_DIR / f"prompt-cache-{datetime.now():%Y%m%d-%H%M%S}"
    run_dir.mkdir(parents=True, exist_ok=True)

    drafts, usage_rows = [], []
    # Sequential on purpose: parallel first calls would all miss the cache.
    for n, (rule_id, message, passages) in enumerate(requests, start=1):
        response = client.messages.create(
            model=args.model,
            max_tokens=args.max_tokens,
            system=system,
            messages=[{"role": "user", "content": message}],
        )
        text = "".join(block.text for block in response.content if block.type == "text")
        drafts.append(f"## {rule_id}\n\n{text.strip()}\n")

        u = response.usage
        written = u.cache_creation_input_tokens or 0
        read_ = u.cache_read_input_tokens or 0
        prompt_total = u.input_tokens + written + read_
        share = 100 * read_ / prompt_total if prompt_total else 0
        usage_rows.append((n, rule_id, u.input_tokens, written, read_, u.output_tokens, share))
        print(f"{n}. {rule_id}: uncached {u.input_tokens}, cache write {written}, "
              f"cache read {read_}, output {u.output_tokens} ({share:.0f}% of prompt from cache)")

    (run_dir / "drafts.md").write_text(
        f"# Draft cases (API, prompt-cached): {args.area}\n\n"
        f"Model {args.model}, {datetime.now():%Y-%m-%d %H:%M}. Review material only; "
        f"not in test-cases/, not duplicate-checked.\n\n" + "\n".join(drafts),
        encoding="utf-8",
    )

    totals = [sum(r[i] for r in usage_rows) for i in (2, 3, 4, 5)]
    prompt_sum = totals[0] + totals[1] + totals[2]
    lines = [
        f"# Prompt cache usage: {args.area}",
        "",
        f"Model {args.model}, TTL {args.ttl}, {len(usage_rows)} sequential calls, "
        f"cached prefix ~{prefix_tokens} tokens (estimate).",
        "",
        "| # | Rule | Uncached input | Cache write | Cache read | Output | Prompt from cache |",
        "|---|---|---|---|---|---|---|",
        *[f"| {n} | {r} | {i} | {w} | {c} | {o} | {s:.0f}% |" for n, r, i, w, c, o, s in usage_rows],
        f"| | **Total** | {totals[0]} | {totals[1]} | {totals[2]} | {totals[3]} | "
        f"{(100 * totals[2] / prompt_sum if prompt_sum else 0):.0f}% |",
        "",
        "Call 1 writes the prefix to the cache; later calls within the TTL read it. "
        "Cache reads are billed at a fraction of the normal input price, cache writes at a premium.",
    ]
    (run_dir / "usage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved {run_dir / 'drafts.md'} and {run_dir / 'usage.md'}")


if __name__ == "__main__":
    main()
