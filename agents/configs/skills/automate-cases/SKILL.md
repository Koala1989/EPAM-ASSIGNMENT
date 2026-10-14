---
name: automate-cases
description: Automate Approved manual UI test cases end to end in one run. For each case, calls playwright-test-generator to write the spec, runs lint and type check, calls playwright-test-healer to run and stabilise it, checks it passes three times in a row, then calls playwright-test-reviewer for an independent review. Usage /automate-cases <case ID> [<case ID> ...].
argument-hint: <case ID> [<case ID> ...]
disable-model-invocation: true
---

# Automate test cases: generate, heal, review

Request: $ARGUMENTS

You only coordinate. You do not write or edit specs, page objects, fixtures, configuration or test cases, change any Review field, or fix anything an agent left broken. All commands below run from `automation/`.

## 1. Check the request

The request must list one or more UI case IDs (`UI-<Area>-NNN`, e.g. `UI-Part-007`). If there are none, ask the user for them and stop. API case IDs (`API-...`) belong to `/automate-api-cases`: list them as skipped, with that pointer.

Handle the cases **one at a time, in the order given**: complete steps 2-7 for a case before starting the next. Agents may add page object code, and two cases changing the same files at once would conflict.

## 2. Pre-check the case

Without starting an agent, check with Grep in `test-cases/*/*.md` (the Area's folder: "Area folders" in `references/seed-manual-test-case.md`) (not `requirements-inventory.md` or `open-questions.md`):

- **The case exists.** If not: skip it, reason "not found".
- **Review starts with `Approved` or `Changed`**, and the case contains no `Open question`, `[open:` or `Not known`. If not: skip it, reason "not Approved" or "open question".
- **No spec exists yet:** no file under `automation/tests/ui/` whose first line names this case ID. If one exists: skip it, reason "spec exists". Regenerating would overwrite reviewed work; the user can delete the spec first, or ask for the healer or reviewer on their own.

A skipped case gets no agent run. Go to the next case.

## 3. Run playwright-test-generator

Call the Agent tool, in the foreground, with `subagent_type: playwright-test-generator` and this prompt:

```
Automate test case <case ID>.
```

Do not add anything else to the prompt.

- **Not written** (the generator stopped on a guardrail, e.g. the app does not match the case): record the reason and the mismatches it reported, and go to the next case. Do not run the healer or reviewer for it.
- **Written:** note the spec path and every file it lists under page object changes.

## 4. Lint and type check

The generator cannot run these. Run:

```
npm run typecheck
npx eslint <spec path> <every page object or fixture file the generator changed>
```

Keep the full error output, if any, for step 5.

## 5. Run playwright-test-healer

Call the Agent tool, in the foreground, with `subagent_type: playwright-test-healer` and this prompt:

```
Run and stabilise <spec path>.
```

If step 4 failed, add one line and the errors verbatim:

```
Lint and type check errors to fix first:
<errors>
```

Pass only the spec path and the tool output. Never pass the generator's report or reasoning.

After it returns, run step 4's commands again (adding any files the healer changed). If they still fail, record it and skip step 6; still run step 7.

## 6. Stability check: three green runs

Run:

```
npx playwright test <spec path> --project=chromium --repeat-each=3
```

The `login-smoke` project runs first as a dependency. Record the outcome:

- **3 passed:** stable.
- **Any failure:** not stable. Record the failing run's error line. Do not call the healer again; it has already used its bounded attempts.
- **Skipped (`test.fixme`):** the healer found an app finding or case defect. Not stable; record its `FINDING:` or `CASE DEFECT:` comment.

## 7. Run playwright-test-reviewer

Call the Agent tool, in the foreground, with `subagent_type: playwright-test-reviewer` and this prompt:

```
Review <spec path>.
```

Pass the spec path only. Never pass the generator's or healer's reports, the stability result or any summary: the reviewer must stay independent, and it runs its own lint and type check.

After it returns, check with Glob that a review file for this case exists in `automation/reviews/ui/` with today's date. If not, say so.

Do not loop back to the generator or healer on the reviewer's findings. The user decides what to fix.

## 8. Summarise

Give the user one summary, in this order:

1. **Results:** one row per case.

   | Case | Spec | Generator | Lint/type | Healer | 3 runs | Review | Done |
   |---|---|---|---|---|---|---|---|

   **Done** is Yes only when lint and type check pass, all 3 runs pass, and the verdict is Approve or Approve with changes (CONVENTIONS.md UI §12). Skipped cases show the step-2 reason.
2. **Page object changes:** every file the generator or healer created or changed, with the new members. These touch code other specs share, so the user should look at them.
3. **Findings and case defects:** from the generator's mismatches and the healer's fixme comments: case, step, case says, app shows. They go to `test-cases/findings.md` or back to the case author.
4. **Review findings:** each Blocker and Major (case, file:line, problem) and the review file links.
5. **Left-over data:** any `QA-` records the healer reported.
6. **Next steps for the user:** what is needed to get each not-Done case to Done.

Do not repeat the agents' full reports. If an agent failed or returned something unexpected, say so plainly and continue with the next case; do not retry or work around it.
