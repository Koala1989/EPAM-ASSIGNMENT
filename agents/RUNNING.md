# Running the AI workflow

## The workflow at a glance

| Stage | Skill (one trigger) | Agents it runs, in order | Human step afterwards |
|---|---|---|---|
| Manual test cases (UI or API) | `/gen-test-cases` | `test-case-creator` (Sonnet), then `test-case-reviewer` (Opus): rule coverage, case quality, and a duplicate verdict for cases scoring 50 or more | Architect answers open questions and sets each case's Review field to Approved |
| UI automation | `/automate-cases` | `playwright-test-generator` (Sonnet), lint and type check, `playwright-test-healer` (Sonnet), 3-run stability check, `playwright-test-reviewer` (Opus) | Architect reads the review in `automation/reviews/ui/` |
| API automation | `/automate-api-cases` | `api-test-generator` (Sonnet: writes, runs and stabilises), lint and type check, 3-run stability check, `api-test-reviewer` (Opus) | Architect reads the review in `automation/reviews/api/` |

Reviewers always run on a stronger model than the writers, and they only receive IDs or paths, never another agent's reasoning.

Flow diagrams (SVG and PNG; to change one, edit `tools/diagrams/build_diagrams.py`, then run it and `node tools/diagrams/render.js`):

- [Manual test case generation](diagrams/test-case-generation.png)
- [Automation generation, UI and API](diagrams/automation-generation.png)

**Prerequisites:** InvenTree 1.5.6 running locally. Run `npm install` in `automation/` (one project for both suites), plus `npx playwright install chromium` for the UI suite. Python 3 is needed for the tools. The RAG tools need their venv: `tools/rag/requirements.txt`.

---

## 1. Running a skill (recommended)

All three skills (`gen-test-cases`, `automate-cases`, `automate-api-cases`) are set `disable-model-invocation: true`: Claude will not start them on its own from a plain-language request. The slash command is the reliable way to run them.

### a. Slash command in Claude Code (CLI or VS Code extension)

```
/gen-test-cases UI Part category hierarchy and filtering
/gen-test-cases API Part and category CRUD
/automate-cases UI-REV-001 UI-REV-002
/automate-api-cases API-CRUD-001 API-CRUD-008
```

- **`/gen-test-cases`:** the first word is `UI` or `API`, followed by the functionality in plain words.
- **The automation skills:** they take one or more case IDs and handle them one at a time. Each skill skips the other suite's IDs and says which skill to use instead.
- **Picking up changes:** skills are reloaded during the session after a change. If the `.claude/skills/` folder didn't exist when the session started, run `/reload-skills`.
- **In VS Code:** the extension supports only a subset of commands and skills (type `/` to see them). If a skill isn't listed there, use the CLI in the integrated terminal (option b).

### b. Headless CLI (scripts, CI)

```
claude -p "/automate-api-cases API-CRUD-001" --permission-mode acceptEdits --allowedTools "Bash(npx playwright test *),Bash(npm run *),Bash(npx eslint *),Bash(python tools/dedupe_cases.py *)"
```

- **Skills work in headless mode:** put `/skill-name args` in the prompt string.
- **Permissions:** the agents edit files and run commands, so a headless run needs permissions granted in advance with `--permission-mode` and `--allowedTools`. Grant only the commands the agents need. Don't use `bypassPermissions`.
- **Don't use `--bare`:** it skips loading skills, subagents and CLAUDE.md.
- **VS Code users:** the extension doesn't put `claude` on PATH, so install the CLI separately.

### c. Fallback without the skill mechanism

If neither a nor b is available, ask Claude to follow the skill file by hand:

```
Read .claude/skills/automate-api-cases/SKILL.md and follow it for: API-CRUD-001
```

Claude then carries out the same steps by reading the file as instructions. This goes around the skill mechanism, so use it only when a and b aren't possible.

---

## 2. Running one agent on its own

Use this to re-run a single stage: re-review a spec after changes, heal a broken spec, or re-review manual cases.

### Ways to call an agent

| Method | Where | Example |
|---|---|---|
| Plain language naming the agent | CLI and VS Code | `Use the api-test-reviewer agent to review automation/tests/api/CRUD/api-crud-001.spec.ts` |
| @-mention | CLI (not documented for VS Code) | `@agent-playwright-test-healer Run and stabilise automation/tests/ui/Part/ui-part-001.spec.ts` (the typeahead inserts `@"playwright-test-healer (agent)"`) |
| Run the whole session as the agent | CLI | `claude --agent api-test-reviewer`, then give the request |

### What each agent expects

| Agent | Model | Does | Input | Example request |
|---|---|---|---|---|
| `test-case-creator` | Sonnet | Writes manual cases from the requirements inventory, raises open questions, runs the duplicate check | `UI` or `API` plus a functionality | `Generate API test cases for Part and category CRUD.` |
| `test-case-reviewer` | Opus | Independent review of new cases: rule coverage against the inventory (`tools/coverage_check.py`), fidelity, specific Expected results, open-question marking, seed format, API standing rules; Keep, Merge, Remove or Escalate for cases scoring 50 or more. Saves `test-cases/Reviews/<Area>_<functionality>-review-<date>.md` | `UI` or `API`, the functionality, and the case IDs | `Review API test cases for Part and category CRUD: API-CRUD-001, API-CRUD-002.` |
| `playwright-test-generator` | Sonnet | Records one Approved UI case live and writes its spec, adding page-object code if needed | One UI case ID | `Automate test case UI-REV-001.` |
| `playwright-test-healer` | Sonnet | Runs UI specs and fixes how they run, never what they check | Spec paths, or none for the whole UI suite | `Run and stabilise automation/tests/ui/Part/ui-part-001.spec.ts` |
| `playwright-test-reviewer` | Opus | Independent review of UI specs, saved to `automation/reviews/ui/` | Spec paths or case IDs, or none to review every spec not yet reviewed | `Review automation/tests/ui/Part/ui-part-006.spec.ts` |
| `api-test-generator` | Sonnet | Writes one Approved API case's spec, runs it, and must reach 3 green runs | One API case ID | `Automate test case API-CRUD-001.` |
| `api-test-reviewer` | Opus | Independent review of API specs, saved to `automation/reviews/api/` | Spec paths or case IDs, or none to review every spec not yet reviewed | `Review automation/tests/api/CRUD/api-crud-001.spec.ts` |

### Rules when calling agents directly (the skills enforce these automatically)

- **Keep the reviewers independent:** give them IDs or paths only, never another agent's report.
- **Only Approved or Changed cases are automated.** The generators refuse anything else.
- **Check the generator's work yourself:** after a generator runs, run lint, the type check and the 3-run stability check yourself (section 3).

---

## 3. Without any agent (tools and test suites)

| Task | Command |
|---|---|
| Duplicate check | `python tools/dedupe_cases.py --case <ID> [--case <ID> ...]`, or `--dry-run` for a report only |
| Rule coverage | `python tools/coverage_check.py --area <Area> [--area ...] [--file <case file> ...]` |
| Rebuild the schema slice (InvenTree running) | `tools/rag/.venv/Scripts/python.exe tools/slice_schema.py` |
| Build or query the RAG index | `tools/rag/.venv/Scripts/python.exe tools/rag/build_index.py`, then `tools/rag/.venv/Scripts/python.exe tools/rag/query_index.py "<question>" --top-k 3` |
| Both suites (from `automation/`) | `npm test` (UI and API), `npm run test:smoke`, `npm run lint`, `npm run typecheck`, `npm run report` |
| UI suite (from `automation/`) | `npm run test:ui`, `npx playwright test <spec> --project=chromium` |
| Run against demo.inventree.org (architect only; it runs 1.6.0 dev, not 1.5.6) | from `automation/`: `$env:TEST_ENV='demo-web'; npm run test:smoke`, then `Remove-Item Env:TEST_ENV` to return to `local` |
| UI stability check | `npx playwright test <spec> --project=chromium --repeat-each=3` |
| API suite (from `automation/`) | `npm run test:api`, `npx playwright test <spec> --project=api` |
| API stability check | `npx playwright test <spec> --project=api --repeat-each=3` |
| Prompt-caching demo | `tools/rag/.venv/Scripts/python.exe tools/llm/draft_cases_cached.py --area Part --rule R-Part-12 --dry-run` (drop `--dry-run` for a live, billed run; needs `ANTHROPIC_API_KEY`) |
| Manual run of a case through the browser (Playwright MCP server `playwright`) | Ask Claude: `Using the Playwright MCP, execute UI-Part-001 step by step and report pass or fail per step.` |
