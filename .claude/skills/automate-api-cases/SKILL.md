---
name: automate-api-cases
description: Automate Approved manual API test cases end to end in one run. For each case, calls api-test-generator to write, run and stabilise the Playwright API spec, re-runs lint and type check, checks the spec passes three times in a row, then calls api-test-reviewer for an independent review. Usage /automate-api-cases <case ID> [<case ID> ...].
argument-hint: <case ID> [<case ID> ...]
disable-model-invocation: true
---

# Automate API test cases: generate, verify, review

Request: $ARGUMENTS

You only coordinate. You do not write or edit specs, clients, fixtures, configuration or test cases, change any Review field, or fix anything an agent left broken. All commands below run from `automation/api/`.

## 1. Check the request

The request must list one or more API case IDs (`API-<Area>-NNN`, e.g. `API-CRUD-001`). If there are none, ask the user for them and stop. UI case IDs (`UI-...`) belong to `/automate-cases`: list them as skipped, with that pointer.

Handle the cases **one at a time, in the order given**: complete steps 2-6 for a case before starting the next. The generator may add client methods, and two cases changing the same files at once would conflict.

## 2. Pre-check the case

Without starting an agent, check with Grep in `test-cases/API_<Area>/*.md` (e.g. `API-CRUD-001` is in `test-cases/API_CRUD/`; not `requirements-inventory.md` or `open-questions.md`):

- **The case exists.** If not: skip it, reason "not found".
- **Review starts with `Approved` or `Changed`**, and the case contains no `Open question`, `[open:` or `Not known`. If not: skip it, reason "not Approved" or "open question".
- **No spec exists yet:** no file under `automation/api/tests/` whose first line names this case ID. If one exists: skip it, reason "spec exists". Regenerating would overwrite reviewed work; the user can delete the spec first, or ask for the reviewer on its own.

A skipped case gets no agent run. Go to the next case.

## 3. Run api-test-generator

Call the Agent tool, in the foreground, with `subagent_type: api-test-generator` and this prompt:

```
Automate test case <case ID>.
```

Do not add anything else to the prompt.

- **Not written** (the generator stopped on a guardrail): record the reason and go to the next case. Do not run the reviewer for it.
- **Written:** note the spec path, its reported run result, every client file it lists as changed, and any findings or case defects it reported.

The generator writes the spec, runs it and fixes how it runs; there is no separate healer for API specs.

## 4. Lint and type check

The generator ran these itself; run them again as an independent check of its claim:

```
npm run typecheck
npx eslint <spec path> <every client or fixture file the generator changed>
```

If they fail, record the errors, skip step 5 and still run step 6. Do not call the generator again.

## 5. Stability check: three green runs

Run:

```
npx playwright test <spec path> --project=api --repeat-each=3
```

The `api-smoke` project runs first as a dependency. This checks the generator's own result independently. Record the outcome:

- **3 passed:** stable.
- **3 failed, known product defects only:** every failure in all three runs is a soft `toMatchSchema` error whose message says `Known product defects only: F-..`. Stable; record the finding IDs. The rest of the test's checks ran and passed.
- **Any other failure** (a status or value check, a `[NEW]` schema error, or runs that differ): not stable. Record the failing run's error line (the `toHaveStatus` message includes the response body). Do not call the generator again; it has used its bounded attempts.
- **Skipped (`test.fixme`):** the generator found an app finding or case defect. Not stable; record its `FINDING:` or `CASE DEFECT:` comment.

Do not query InvenTree yourself to look for leftover `QA-` data (that needs credentials); rely on the generator's report, and never delete records.

## 6. Run api-test-reviewer

Call the Agent tool, in the foreground, with `subagent_type: api-test-reviewer` and this prompt:

```
Review <spec path>.
```

Pass the spec path only. Never pass the generator's report, the stability result or any summary: the reviewer must stay independent, and it runs its own lint and type check.

After it returns, check with Glob that a review file for this case exists in `automation/api/reviews/` with today's date. If not, say so.

Do not loop back to the generator on the reviewer's findings. The user decides what to fix.

## 7. Summarise

Give the user one summary, in this order:

1. **Results:** one row per case.

   | Case | Spec | Generator | Lint/type | 3 runs | Review | Done |
   |---|---|---|---|---|---|---|

   **Done** is Yes only when lint and type check pass, all 3 runs pass or fail on known product defects only (show it as `Yes (F-11)`), and the verdict is Approve or Approve with changes (`automation/api/CONVENTIONS.md` §12). Skipped cases show the step-2 reason.
2. **Client changes:** every client file the generator created or changed, with the new methods. These are shared by other specs, so the user should look at them.
3. **Findings and case defects:** from the generator's report and the fixme comments: case, step, case says, app returns. They go to `test-cases/findings.md` or back to the case author.
4. **Review findings:** each Blocker and Major (case, file:line, problem) and the review file links.
5. **Left-over data:** any `QA-` records the generator reported.
6. **Next steps for the user:** what is needed to get each not-Done case to Done.

Do not repeat the agents' full reports. If an agent failed or returned something unexpected, say so plainly and continue with the next case; do not retry or work around it.
