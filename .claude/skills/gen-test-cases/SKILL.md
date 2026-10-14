---
name: gen-test-cases
description: Generate manual test cases for one InvenTree Parts functionality and review them in one run. Calls the test-case-creator agent, then the independent test-case-reviewer agent (rule coverage against the inventory, case quality, and a duplicate verdict for cases scoring 50 or more). Usage /gen-test-cases <UI|API> <functionality>.
argument-hint: <UI|API> <functionality>
disable-model-invocation: true
---

# Generate and review test cases

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

If the report says the request is unclear or asks a question before generating, show that to the user and stop. If it created no cases, say so and stop.

## 3. Run test-case-reviewer

Take the case IDs from the creator's **Created** section (or its **Next step** line). Call the Agent tool, in the foreground, with `subagent_type: test-case-reviewer` and this prompt:

```
Review <UI|API> test cases for <functionality>: <every case ID created>.
```

Pass the IDs and the functionality only. Never pass the creator's report, its reasoning, coverage table or any summary of the cases: the reviewer must stay independent and builds its own coverage from the inventory.

The reviewer gives a duplicate verdict only for cases whose duplicate check scored 50 or more; usually there are none, and it is a coverage and quality review only.

After it returns:
- Check with Glob that a review file for the functionality exists under `test-cases/` in a `reviews/` folder with today's date. If not, say so.
- Check with Grep that every created case with a `**Duplicate check:**` line now has a `**Duplicate judgement:**` line. List any that do not.

Do not loop back to the creator on the reviewer's findings. The user decides.

## 4. Summarise

Give the user one summary, in this order:

1. **Created:** case IDs per Area folder, and how many.
2. **Open questions:** the questions the creator added, with the `open-questions.md` links and the case IDs each one affects (marked `Draft · Open question: ...`). Answering them is the first thing the user must do if there are any.
3. **Review:** the reviewer's verdict and the review file link; coverage gaps (rules in scope with no case, missing boundary, negative, permission or 404 cases); each Blocker and Major.
4. **Duplicates:** the reviewer's verdicts for cases scoring 50 or more, or "none scored 50 or more". Keep needs no action; Merge, Remove and Escalate do.
5. **Next steps for the user:** answer questions, act on the review (for a gap: rerun `/gen-test-cases` for it or ask for the missing cases), run the cases, then set each case's Review field (all cases are `Draft`).

Do not repeat the agents' full reports. If an agent failed or returned something unexpected, say so plainly and stop; do not retry or work around it.
