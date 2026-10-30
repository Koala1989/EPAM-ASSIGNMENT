"""Smoke test: is the Claude judge connected? One metric, one test case, one score."""
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.models import AnthropicModel
from deepeval.test_case import LLMTestCase

# The judge: the LLM that scores outputs. No temperature: the installed Anthropic SDK no longer accepts one.
judge = AnthropicModel(model="claude-haiku-4-5")

# A test case: the question, and the answer being judged.
case = LLMTestCase(
    input="What does the IPN field of a part mean?",
    actual_output="IPN stands for Internal Part Number: a code your company uses to identify the part.",
)

# The metric: does the answer address the question? Score 0-1, pass at 0.7 or more.
metric = AnswerRelevancyMetric(model=judge, threshold=0.7, include_reason=True)
metric.measure(case)

print(f"score={metric.score}  passed={metric.is_successful()}")
print(f"reason: {metric.reason}")
