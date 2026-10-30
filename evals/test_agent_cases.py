"""Step 5: does the test-case-creator stay faithful to the docs?

Scores saved manual cases (golden/agent_cases_sample.json) offline: no agent run, only the judge.
Each case becomes one DeepEval test case:
  input              the case's title, summary, review status and step actions
  actual_output      its Expected results, one line per step (what the agent claims should happen)
  retrieval_context  the inventory rules it cites, and the doc sections around its Source lines

One metric:
  Requirement traceability  (GEval, custom) no Expected result is an unflagged assumption (category D),
                            which includes contradicting the cited docs

Faithfulness (built in) was dropped on 2026-10-20: on the planted contradiction it scored 1.00 with both a Haiku
and a Sonnet judge, because it checks claims for contradiction and the judge did not read an expected error
message as a claim about the field rule. Evidence and definition: NOTES.md, section 5.

Planted controls are copies of a real case with one Expected result replaced (the files are never changed).
They check that the metric fails when it should, before its verdicts on real cases are trusted.

Run from evals/ ($env:PYTHONUTF8 = "1" first):
  controls first: .venv\\Scripts\\deepeval.exe test run test_agent_cases.py -k planted
  real cases:     .venv\\Scripts\\deepeval.exe test run test_agent_cases.py -k sample
"""

import json
from pathlib import Path

import pytest
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.metrics.g_eval import Rubric
from deepeval.models import AnthropicModel
from deepeval.test_case import LLMTestCase, SingleTurnParams

from case_sources import RULE_ID, doc_sections, find_case, load_rule_texts

SAMPLE = json.loads((Path(__file__).parent / "golden" / "agent_cases_sample.json").read_text(encoding="utf-8"))
RULE_TEXT = load_rule_texts()

# Sonnet, not Haiku: with Haiku, traceability passed the planted invented error message (it read the message as
# implied by the uniqueness rule); Sonnet classified it as D with the same instructions (2026-10-20).
# About 3x Haiku's cost per call.
judge = AnthropicModel(model="claude-sonnet-4-6")


def traceability() -> GEval:
    # The architect's policy as categories. Only D (an unflagged assumption) lowers the score.
    return GEval(
        name="Requirement traceability",
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.RETRIEVAL_CONTEXT,
        ],
        evaluation_steps=[
            "The actual output lists a manual test case's expected results, one per step. The input gives the case "
            "for context only; judge only the expected results.",
            "Split each expected result into its separate claims.",
            "Classify each claim: "
            "A = stated or directly implied by the retrieval context (inventory rules and doc sections); "
            "B = generic UI mechanics that state no business rule (a form or menu opens, a field accepts input, "
            "a page or record is shown, the browser navigates); "
            "C = explicitly flagged as unconfirmed with '[confirm in app: ...]', 'Proposed, to confirm in Q-...', "
            "'Open: Q-...' or '[open: ...]'; "
            "D = a behaviour, value, message, field or rule that is not in the retrieval context and is not flagged.",
            "A claim that only names a value the step itself entered as test data is B, not D.",
            "Every D claim is an assumed requirement. In the reason, quote each D claim and say what is missing.",
        ],
        rubric=[
            Rubric(score_range=(0, 3), expected_outcome="Two or more D claims."),
            Rubric(score_range=(4, 7), expected_outcome="Exactly one D claim."),
            Rubric(score_range=(8, 10), expected_outcome="No D claims; 8 or 9 if one claim is borderline between B and D."),
        ],
        threshold=0.8,
        model=judge,
    )


def build_case(case: dict, replace_step: int | None = None, replacement: str | None = None) -> LLMTestCase:
    fields = case["fields"]
    steps = case["steps"]
    expected = [replacement if s["n"] == replace_step else s["expected"] for s in steps]
    rules = sorted(set(RULE_ID.findall(fields["Requirement"])))
    return LLMTestCase(
        input="\n".join(
            [f"{case['id']}: {case['title']}", f"Summary: {fields['Summary']}", f"Review: {fields['Review']}"]
            + [f"Step {s['n']}: {s['action']} Test data: {s['data']}" for s in steps]
        ),
        actual_output="\n".join(f"Step {s['n']}: {e}" for s, e in zip(steps, expected)),
        retrieval_context=[f"{r}: {RULE_TEXT[r]}" for r in rules if r in RULE_TEXT]
        + doc_sections(fields["Requirement"]),
        metadata={"case": case["id"], "file": case["file"]},
    )


@pytest.mark.judged
@pytest.mark.parametrize("entry", SAMPLE["cases"], ids=lambda e: f"sample-{e['id']}")
def test_case_traceable_to_docs(entry):
    assert_test(build_case(find_case(entry["id"])), [traceability()])


@pytest.mark.judged
@pytest.mark.parametrize("plant", SAMPLE["planted"], ids=lambda p: p["id"])
def test_planted_defect_is_caught(plant):
    """Passes when the metric gives the verdict the control expects (a planted defect must fail it)."""
    case = build_case(find_case(plant["base"]), plant["step"], plant["expected"])
    report = []
    for name, metric in (("Requirement traceability", traceability()),):
        metric.measure(case)
        got = "pass" if metric.is_successful() else "fail"
        report.append((name, plant["should"][name], got, metric.score, metric.reason))
    wrong = [r for r in report if r[1] != r[2]]
    summary = "\n".join(f"  {n}: expected {s}, got {g} (score {sc:.2f})\n    {why}" for n, s, g, sc, why in report)
    assert not wrong, f"{plant['id']} ({plant['defect']})\n{summary}"
    print(f"\n{plant['id']}\n{summary}")
