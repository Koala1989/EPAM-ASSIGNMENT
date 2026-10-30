"""Step 4: RAG retrieval eval.

Runs every golden entry (golden/retrieval_golden.json) through the real search() of tools/rag/query_index.py
and scores what comes back, in two layers:

  Free (no LLM): did a chunk holding the expected doc lines come back in the top K?
                 For unanswerable questions: did nothing come back above the score cutoff?
  Judged (Claude): Contextual Precision, Recall and Relevancy (marked `judged`, costs API credit).

Each answerable entry is queried two ways:
  rule:     the rule text from its requirements inventory, as the test-case-creator agent queries (top-k 3)
  question: the golden question, a tester's paraphrase (harder: different words from the doc)

Run from evals/:
  free only:  .venv\\Scripts\\python.exe -m pytest test_retrieval.py -m "not judged" -v
  one judged: .venv\\Scripts\\deepeval.exe test run test_retrieval.py -k "judged and G-01"
  all:        .venv\\Scripts\\deepeval.exe test run test_retrieval.py
"""

import json
import re
import sys
from pathlib import Path

import pytest
from deepeval import assert_test
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
)
from deepeval.models import AnthropicModel
from deepeval.test_case import LLMTestCase

from case_sources import REPO, load_rule_texts

sys.path.insert(0, str(REPO / "tools" / "rag"))
from query_index import search  # noqa: E402  (the system under test)

# The test-case-creator agent queries with --top-k 3 (.claude/agents/test-case-creator.md, step 4).
TOP_K = 3

GOLDEN = json.loads((Path(__file__).parent / "golden" / "retrieval_golden.json").read_text(encoding="utf-8"))
ANSWERABLE = [e for e in GOLDEN["entries"] if e["expected_sources"]]
UNANSWERABLE = [e for e in GOLDEN["entries"] if not e["expected_sources"]]


RULE_TEXT = load_rule_texts()

# (entry, query kind, query text) for each answerable entry, queried both ways.
QUERIES = [
    pytest.param(e, kind, text, id=f"{e['id']}-{kind}")
    for e in ANSWERABLE
    for kind, text in (("rule", RULE_TEXT[e["rule"]]), ("question", e["question"]))
]

# search() cites chunks as docs/<file>#L<start>-L<end>.
CITATION = re.compile(r"docs/(?P<file>[^#]+)#L(?P<start>\d+)-L(?P<end>\d+)")


def overlaps(hit: dict, source: dict) -> bool:
    """True if the retrieved chunk contains any of the expected doc lines."""
    m = CITATION.match(hit["citation"])
    first, last = source["lines"]
    return m["file"] == source["file"] and int(m["start"]) <= last and first <= int(m["end"])


def first_hit_rank(hits: list[dict], entry: dict) -> int | None:
    """1-based rank of the first chunk holding any expected source, or None."""
    return next(
        (rank for rank, h in enumerate(hits, 1) if any(overlaps(h, s) for s in entry["expected_sources"])),
        None,
    )


def describe(hits: list[dict]) -> str:
    return "\n".join(f"  {i}. {h['citation']} (score {h['score']:.2f})" for i, h in enumerate(hits, 1)) or "  (none)"


# ---------- Free layer: no LLM, no cost ----------

# Reciprocal rank per query kind (1/rank of the first correct chunk, 0 if missed), printed as MRR at the end.
RECIPROCAL_RANKS: dict[str, list[float]] = {"rule": [], "question": []}


@pytest.mark.parametrize(("entry", "kind", "query"), QUERIES)
def test_expected_source_in_top_k(entry, kind, query):
    """Hit rate @ K: at least one expected doc location is inside one of the top K chunks.
    Whether the chunks cover the whole rule is Contextual Recall's job (judged layer)."""
    hits = search(query, top_k=TOP_K)
    rank = first_hit_rank(hits, entry)
    RECIPROCAL_RANKS[kind].append(1 / rank if rank else 0.0)
    assert rank, f"{query}\nexpected one of: {entry['expected_sources']}\ngot:\n{describe(hits)}"


@pytest.mark.xfail(
    strict=True,
    reason="FINDING: a vector score measures topic closeness, not whether a chunk answers the question. "
    "15 unanswerable questions top-score 0.34-0.67; near-topic ones (who can lock a part: 0.67) score above the "
    "weakest correct chunk (0.58 rule wording, 0.46 question), so no floor separates them (2026-10-24). The reader "
    "(agent) must check a chunk states the rule (step 5 traceability). XPASS means retrieval changed: revisit.",
)
@pytest.mark.parametrize("entry", UNANSWERABLE, ids=lambda e: e["id"])
def test_unanswerable_returns_nothing(entry):
    """The docs do not answer this, so ideally no chunk passes search()'s default score cutoff."""
    hits = search(entry["question"], top_k=TOP_K)
    assert not hits, f"{entry['question']}\nexpected no chunks, got:\n{describe(hits)}"


def pytest_terminal_summary_mrr() -> str:
    lines = []
    for kind, ranks in RECIPROCAL_RANKS.items():
        if ranks:
            hits = sum(1 for r in ranks if r > 0)
            lines.append(
                f"{kind} queries (n={len(ranks)}):  Hit@{TOP_K} {hits}/{len(ranks)} = {hits / len(ranks):.0%}"
                f"   MRR@{TOP_K} {sum(ranks) / len(ranks):.2f}"
            )
    return "\n".join(lines)


# ---------- Judged layer: Claude scores the retrieved text ----------

judge = AnthropicModel(model="claude-haiku-4-5")

# Thresholds (step 7, 2026-10-24):
#   Precision (gate, 0.5): are the chunks that answer the question ranked above the ones that don't?
#   Recall    (gate, 0.7): is every fact in expected_output supported by some retrieved chunk? expected_output
#              has one fact per sentence, so a partly retrieved answer scores 0.33, 0.5 or 0.67, not 0 or 1.
#   Relevancy (tracked, threshold 0): how much of the retrieved text is about the question. It measures section
#              size (a chunk is a whole doc section), a chunking trade-off rather than a retrieval fault: G-15
#              failed at 0.25 with Precision and Recall at 1.00. Its score still shows in the report.
METRICS = [
    ContextualPrecisionMetric(model=judge, threshold=0.5, include_reason=True),
    ContextualRecallMetric(model=judge, threshold=0.7, include_reason=True),
    ContextualRelevancyMetric(model=judge, threshold=0.0, include_reason=True),
]


@pytest.mark.judged
@pytest.mark.parametrize("entry", ANSWERABLE, ids=lambda e: e["id"])
def test_retrieval_judged(entry):
    """Judges what the agent really gets: the rule-text query, top K."""
    hits = search(RULE_TEXT[entry["rule"]], top_k=TOP_K)
    case = LLMTestCase(
        input=entry["question"],
        expected_output=entry["expected_output"],
        retrieval_context=[h["text"] for h in hits],  # in rank order: precision depends on it
        metadata={"rule": entry["rule"], "citations": [h["citation"] for h in hits]},
    )
    assert_test(case, METRICS)
