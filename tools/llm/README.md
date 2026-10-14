# Prompt caching

Prompt caching lets the model reuse the processed form of a prompt prefix it has already seen, instead of reprocessing it. A cached read costs a fraction of normal input tokens and is faster. The prefix must be byte-identical between calls, it expires after its TTL (5 minutes by default, 1 hour optionally), and it must be at least the model's minimum length or it is silently not cached.

This project uses caching in two places.

## 1. Claude Code agents (automatic)

All agents in `.claude/agents/` run inside Claude Code, which caches prompts automatically; no code sets it. What is cached:

| Prefix | Cached across | Why it stays identical |
|---|---|---|
| Tool definitions + the agent's system prompt (its `.md` file) | Runs of the same agent within the TTL | The agent files contain no dates, run IDs or other values that change per run. Keep it that way: any change to an agent file invalidates its cache. |
| Everything earlier in the same run (task prompt, files read, tool results) | Turns within one run | Each turn resends the conversation so far, and Claude Code places cache breakpoints on it. |

What is **not** shared across runs: the files an agent reads (seed, inventory, conventions). They come after the task prompt, which differs per run, so they are re-read and re-processed each run. Moving them into the system prompt would cache them, at the cost of duplicating the seed and inventory inside agent files that would then drift from the originals. We chose not to.

To see it working: run `/usage` (or watch the status line) before and after two quick runs of the same agent; the second run's cache-read tokens rise.

## 2. API pipeline with explicit caching (`draft_cases_cached.py`)

A script that calls the Claude API directly and sets the cache breakpoint itself, to show the mechanism and measure it. It drafts test cases for several requirement rules, one sequential call per rule:

| Part of the request | Content | Cached |
|---|---|---|
| System block 1 | Drafting instructions and guardrails | Yes |
| System block 2 | `references/seed-manual-test-case.md` | Yes |
| System block 3 | `test-cases/requirements-inventory.md` (index, Not in docs, Doc issues) | Yes |
| System block 4 (`cache_control`) | `test-cases/<Area folder>/requirements-inventory.md` | Yes, breakpoint here |
| User message | The rule's row + its top RAG passages from `tools/rag/` | No: differs per call |

Design points:
- **Stable first, variable last.** The cache covers everything up to the block marked `cache_control`, so the per-call content (the rule and its retrieved passages) sits after it. Putting RAG output in the system prompt would change the prefix on every call and nothing would be cached.
- **Sequential calls.** Call 1 writes the cache; calls 2+ read it. Parallel first calls would all miss.
- **Size check.** The prefix is about 6,700 tokens, above the strictest minimum cacheable length (4,096). The script warns if a prefix falls below it.
- **Output is review material only.** Drafts go to `agents/runs/prompt-cache-<timestamp>/drafts.md`, not to `test-cases/`. They skip the duplicate check and the architect's review, so they never become cases directly. `usage.md` in the same folder records, per call, uncached input, cache write, cache read and output tokens.

### Setup and run

Uses the RAG tools' venv (it imports `tools/rag/query_index.py`):

```
tools/rag/.venv/Scripts/python.exe -m pip install -r tools/llm/requirements.txt
```

Inspect the requests without calling the API (no key needed, nothing billed):

```
tools/rag/.venv/Scripts/python.exe tools/llm/draft_cases_cached.py --area Part --rule R-Part-12 --rule R-Part-14 --rule R-Part-16 --dry-run
```

Live run (billed per call; needs `ANTHROPIC_API_KEY`):

```
tools/rag/.venv/Scripts/python.exe tools/llm/draft_cases_cached.py --area Part --rule R-Part-12 --rule R-Part-14 --rule R-Part-16
```

Expected `usage.md` pattern: call 1 shows a cache write of about the prefix size and no cache read; calls 2 and 3 show a cache read of that size and only a few hundred uncached tokens. Options: `--model` (default `claude-sonnet-5-5`, or `CLAUDE_MODEL`), `--ttl 5m|1h`, `--top-k`, `--no-rag`, `--max-tokens`.
