---
name: gen-test-cases
description: Generate manual test cases for one InvenTree Parts functionality and check them for duplicates in one run. Calls the test-case-creator agent, then the duplicate-judge agent on the borderline cases. Usage /gen-test-cases <UI|API> <functionality>.
argument-hint: <UI|API> <functionality>
disable-model-invocation: true
---

# Generate test cases and judge duplicates

Request: $ARGUMENTS

You only coordinate. You do not write or edit test cases, answer open questions, or change any Review field.

## 1. Check the request

The first word of the request must be `UI` or `API`, and a functionality must follow (for example `UI Part creation flow`). If either is missing, ask the user for it and stop. Do not start an agent.

## 2. Run test-case-creator

Call the Agent tool, in the foreground, with `subagent_type: test-case-creator` and this prompt, filled in:

```
Generate <UI|API> test cases for <functionality>.
```

Do not add anything else to the prompt.

If the report says the request is unclear or asks a question before generating, show that to the user and stop.

## 3. Pick the cases for the judge

In the creator's report, find the **Next step** line.

- `Run duplicate-judge for: <IDs>`: those IDs go to the judge.
- `None`: skip step 4.

Cases the creator listed as Duplicate (above 80) are not judged; they go to the architect.

## 4. Run duplicate-judge

Call the Agent tool, in the foreground, with `subagent_type: duplicate-judge` and this prompt:

```
Judge these cases: <IDs>.
```

Pass the IDs only. Never pass the creator's report, its reasoning, coverage table or any summary of the cases: the judge must stay independent.

After it returns, check with Grep that each judged case now has a `**Duplicate judgement:**` line. List any that do not.

## 5. Summarise

Give the user one summary, in this order:

1. **Created:** case IDs per Area folder, and how many.
2. **Open questions:** the questions the creator added, with the `open-questions.md` links and the case IDs each one affects (marked `Draft · Open question: ...`). Answering them is the first thing the user must do if there are any.
3. **Duplicates:** cases above 80 (for the user to decide), and the judge's verdicts. Keep needs no action; Merge, Remove and Escalate do.
4. **Next steps for the user:** answer questions, run the cases, then set each case's Review field (all cases are `Draft`).

Do not repeat the agents' full reports. If an agent failed or returned something unexpected, say so plainly and stop; do not retry or work around it.
