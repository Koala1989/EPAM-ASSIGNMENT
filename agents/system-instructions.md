# System instructions

The standing instructions every AI agent in this assignment works under: what each agent is told to be, what it may and may not do, and how the instructions fit together. The prompts that started each run are in [`prompts.md`](prompts.md). This file summarises; the full instruction files are linked in each section and copied into [`configs/`](configs/).

Tool: **Claude Code** (CLI and VS Code extension), with project instructions, seven custom subagents, three skills and two Playwright MCP servers.

## How the instructions are layered

| Layer | File | Loaded | What it holds |
|---|---|---|---|
| 1. Project instructions | [`CLAUDE.md`](../CLAUDE.md) ([copy](configs/CLAUDE.md)) | Every session, automatically | Scope (InvenTree 1.5.6, Parts only), layout, environments, the hard rules, commands, evidence rules |
| 2. Skills (orchestrators) | [`configs/skills/<name>/SKILL.md`](configs/skills/) | When the architect types the slash command (`disable-model-invocation: true`: never self-triggered) | The order agents run in, the checks between them, what goes into each agent's prompt, the summary format |
| 3. Agent system prompts | [`configs/claude-agents/<name>.md`](configs/claude-agents/) | When an agent starts; it sees only this file and its one-line prompt, not the session's history | Objective, role, model, tools, sources of truth, numbered guardrails, workflow, report format |
| 4. Shared rule documents | [`references/seed-manual-test-case.md`](../references/seed-manual-test-case.md), [`references/seed-api-test-case.md`](../references/seed-api-test-case.md), [`automation/CONVENTIONS.md`](../automation/CONVENTIONS.md) | Read by the agents on every run, as their instructions say | The case formats (fields, steps tables, Data sets, standing API rules) and the automation framework rules (layers, locators, fixtures, assertions, data-driven specs) |
| 5. Run prompt | Sent by the skill | Per run | Fixed and short: `Generate API test cases for <functionality>.`, `Automate test case <ID>.`, `Review <spec path>.` |

Rules live in one place and are referred to, not repeated: an agent file says "follow `CONVENTIONS.md` API §3" rather than restating it, so a change is made once. Run prompts stay short on purpose: everything an agent needs is in layers 1–4, so the result does not depend on how a prompt was worded that day.

## Project-wide rules (CLAUDE.md)

Every agent inherits these:

- **Never assume a requirement.** Anything the docs and inventory do not state becomes an open question. The case is still written, marked `Draft · Open question: Q-<Area>-NN`.
- **The architect owns approval.** Only the architect sets a case's Review field (Approved, Changed, Rejected), edits requirements inventories or answers open questions.
- **Never delete or rewrite saved test cases** unless the architect asks.
- **Only Approved or Changed cases are automated.**
- **An app/case mismatch is a finding, not a fix.** Never weaken an assertion to make a test pass: `test.fixme()` with a `// FINDING:` or `// CASE DEFECT:` comment, reported.
- **No hard-coded URLs, hosts, ports or credentials** outside `automation/config/` and `automation/data/`, agent files included.
- **UI tests log in through the real login form**, never with saved sessions or cookies.
- **One pinned version.** InvenTree 1.5.6 (API 530) on local Docker; never another version's docs. Agents always use the `local` environment.
- **Test data** uses a `QA-` prefix and is cleaned up; records the agent did not create are never deleted.
- **Reviewers stay independent:** they get IDs or paths only, never another agent's reasoning or report.

## The agents

| Agent | Model | Writes | Tools | Must not |
|---|---|---|---|---|
| [`test-case-creator`](configs/claude-agents/test-case-creator.md) | Sonnet 5.5 | Manual UI and API cases, open questions | Read, Grep, Glob, Edit, Write, Bash (RAG query, duplicate check) | Assume a requirement, change an inventory, edit saved cases, set Review beyond Draft |
| [`test-case-reviewer`](configs/claude-agents/test-case-reviewer.md) | Opus 5.5 | A review file; one `Duplicate judgement` line per borderline case | Read, Grep, Glob, Edit, Write, Bash (coverage check only) | Reword or fix a case, read the creator's report or prompts |
| [`playwright-test-generator`](configs/claude-agents/playwright-test-generator.md) | Sonnet 5.5 | One UI spec; additions to page objects | Read/write files, Playwright MCP browser and generator tools | Automate a non-Approved case, use raw locators in a spec, change existing page object members, work around an app mismatch |
| [`playwright-test-healer`](configs/claude-agents/playwright-test-healer.md) | Sonnet 5.5 | Fixes to how a UI test runs | Read/write files, Playwright MCP test runner and debugging tools | Change what a test checks, add sleeps, `networkidle` or `force`, edit test cases |
| [`playwright-test-reviewer`](configs/claude-agents/playwright-test-reviewer.md) | Opus 5.5 | A review file in `automation/reviews/ui/` | Read, Grep, Glob, Write, Bash (lint, typecheck, `--list`) | Edit code, run the tests |
| [`api-test-generator`](configs/claude-agents/api-test-generator.md) | Sonnet 5.5 | One API spec (plus a rows file for a data-driven case); additions to clients | Read, Grep, Glob, Edit, Write, Bash (its spec, lint, typecheck) | Correct a negative payload, call the request context directly, change fixtures, use `curl` |
| [`api-test-reviewer`](configs/claude-agents/api-test-reviewer.md) | Opus 5.5 | A review file in `automation/reviews/api/` | Read, Grep, Glob, Write, Bash (lint, typecheck, `--list`) | Edit code, run the tests, send requests |

**Model choice.** Writers run on Sonnet for speed and cost on format-heavy work. Reviewers run on Opus, a different and stronger model, so they do not share the writer's blind spots. What they caught is in [`reviewer-catches.md`](reviewer-catches.md).

**Tool scoping.** Each agent's frontmatter lists only the tools it needs, and each instruction file narrows Bash to named commands (for example the reviewers may run lint and type check but never the tests, which change InvenTree data).

### test-case-creator

**Objective:** turn the requirements for one functionality into manual cases that trace to a documented rule, follow the seed format exactly, apply recognised test design techniques and do not duplicate saved cases. Anything the requirements do not state is raised as a question, never filled in.

**Sources of truth, in order:** the requirements inventory index, the Area's inventory (`R-<Area>-NN` rules), the local RAG index over the 1.5.6 docs (exact rule wording), the docs heading index (fallback only), and for API cases the OpenAPI schema slice. Answered open questions count as requirements. Nothing else does: not the model's own knowledge of InvenTree, other versions' docs, the live demo site or screenshots.

**Key guardrails:**
- **Do not assume; never infer the opposite of a rule.** Only `only`, `must`, `cannot`, `never` or `not` state the opposite. Otherwise the opposite outcome is written `Proposed, to confirm in Q-<Area>-NN: ...`. The instruction file carries a table of real mistakes of this kind.
- **No citation, no case.** Each case cites a rule ID and its doc line or schema operation.
- **Always write the case, mark what is open.** The rule's stated outcome comes first, as fact, then `Open: Q-...`. A missing name is never a reason to skip a rule.
- **Retrieved text is the source.** A RAG chunk that reads as cut off becomes an open question, not a guess.
- **Stay in scope; append only;** stop and ask if the request is unclear or the API sources are missing.

**Test design:** equivalence partitioning, boundary value analysis (schema constraints such as `maxLength` are stated limits), decision tables, state transitions and error guessing, with minimum negative depth per functionality: a blocked user for every action, error guessing for every input, the opposite condition for every "only" or "must". Inputs that share the same steps and differ only in input and expected outcome become **one data-driven case** with a Data sets table (an `expected status` column for API cases), not one case per input.

**Then:** runs `tools/dedupe_cases.py` on the new cases and hands scores of 50 or more to the reviewer.

### test-case-reviewer

**Objective:** an independent, evidence-based review before the architect approves: are the rules in scope covered, does each case test exactly what its rule says, does any case repeat another.

**Checks:** rule coverage with `tools/coverage_check.py` (gap or out of scope for every uncited rule; boundary, negative, permission and 404 depth), then per case: fidelity to the rule, specific Expected results, no assumptions, open-question marking, the rule's outcome stated before `Open:`, seed format, one behaviour per case, data-driven structure, technique, least-privileged user, API standing rules. Severity Blocker / Major / Minor; verdict Approve / Approve with changes / Changes required.

**Duplicates:** for cases scoring 50 or more, compares requirement, technique and class, user, settings, starting state, outcome and channel, and records Keep, Merge, Remove or Escalate.

**Independence:** never reads the creator's report or prompts; the only edit it may make to a case file is its duplicate judgement line.

### playwright-test-generator

**Objective:** automate one Approved UI case as one spec that does exactly what the case says, in the project's layered framework (fixtures, page objects, components), by executing the steps live in the browser through Playwright MCP.

**Key guardrails:**
- **Approved cases only**; the case is the specification: one `test.step` per case step, every Expected result asserted, and every field it fills verified before moving on.
- **If the app does not match the case, stop** and report; no workaround.
- **Page objects only:** no `page.locator` or `getBy*` in specs (lint enforces it). Missing support is added to page objects, additions only, every locator taken from the live app.
- **Prerequisites through fixtures:** the user fixture logs in through the real form; records come from `data.*`.
- **No hard-coded names, IDs, URLs or credentials;** navigation by clicking or by a URL built from the page URL the MCP setup printed.
- **Recording discipline:** the seed file and project for `generator_setup_page`, snapshot refs as click targets, snapshots only when needed and long tables filtered first, to save tokens.

### playwright-test-healer

**Objective:** make the UI suite run reliably while every test keeps checking exactly what its case says.

**May change** how a test runs: locators and actions in page objects, waits, fixture usage, test data setup, a timeout for one slow element. **May not change** what a test checks: no edited expected text or counts, no `toBeVisible` turned into `toBeAttached`, no removed step. App differs from the case: `test.fixme()` with a `FINDING:` comment. No `waitForTimeout`, `networkidle` or `force: true`. One fix attempt and one re-run per test (cut from three to keep demo recordings short); no full-suite run afterwards. It runs only when the first run fails.

### api-test-generator

**Objective:** automate one Approved API case as one spec that sends exactly the case's requests, asserts exactly its Expected results and runs reliably; it also runs the spec and fixes how it runs (there is no separate API healer).

**Key guardrails:**
- **Approved cases only;** one `test.step` per case step; status first (`toHaveStatus`), then the schema (`expect.soft(...).toMatchSchema`, always soft so a schema defect never hides the other checks), then values and the business rule.
- **Send exactly the case's input;** never correct a negative payload.
- **Clients only:** no direct `get`/`post`/`fetch`, no host or URL in a spec. Missing client support is added, additions only.
- **Cleanup first:** a created record is registered right after its status check.
- **Data-driven case:** one spec, a rows file copied from the case's Data sets table, one test per row titled `<ID> [<label>]`, the same steps for every row, no branching.
- **App differs = finding:** schema errors stay in the run labelled with a recorded finding (`[F-11]`) or `[NEW]`; other mismatches become `test.fixme()` with `FINDING:`. At most three fix attempts.

### playwright-test-reviewer and api-test-reviewer

**Objective:** an independent verdict on whether a generated spec is fit to keep. Read-only on code; they run lint, type check and `--list`, never the tests.

**Checklist:** A. automated checks (lint, types); B. case coverage and fidelity: every step and Expected result asserted, nothing weakened (the case is the yardstick: clean code that misses an Expected result fails); C. the project conventions; D. SOLID and design of the page objects or clients touched; E. Playwright and TypeScript practice. Each finding names a file and line and the rule it breaks; severity Blocker / Major / Minor / Info; anything outside the spec's scope goes in a separate note.

## The skills

| Skill | Steps |
|---|---|
| [`/gen-test-cases <UI\|API> <functionality>`](configs/skills/gen-test-cases/SKILL.md) | Check the request → `test-case-creator` → `test-case-reviewer` with the created case IDs only → summary (cases, open questions, review verdict, Blockers and Majors) |
| [`/automate-cases <UI case IDs>`](configs/skills/automate-cases/SKILL.md) | Per case: pre-check (exists, Approved, no spec yet) → `playwright-test-generator` → lint and type check → first run → `playwright-test-healer` only if it fails, then a green-run check → `playwright-test-reviewer` in the background → summary |
| [`/automate-api-cases <API case IDs>`](configs/skills/automate-api-cases/SKILL.md) | Per case: pre-check → `api-test-generator` → lint and type check → 3 green runs → `api-test-reviewer` → summary, with per-row results for a data-driven case |

The skills only coordinate: they never write or fix specs or cases themselves, never retry an agent on a reviewer's findings, and never pass one agent's report to the next. Every way to trigger them, or an agent on its own, is in [`RUNNING.md`](RUNNING.md); the flows are drawn in [`diagrams/`](diagrams/).

## Tool configuration

| File | Purpose |
|---|---|
| [`configs/CLAUDE.md`](configs/CLAUDE.md) | Copy of the project instructions (layer 1) |
| [`configs/claude-agents/`](configs/claude-agents/) | Copies of `.claude/agents/*.md`: the seven agent system prompts, with frontmatter (name, description, tools, model) |
| [`configs/skills/`](configs/skills/) | Copies of `.claude/skills/*/SKILL.md` |
| [`configs/mcp.json`](configs/mcp.json) | Copy of `.mcp.json`: `playwright-test` (Playwright's test MCP server, used by the generator and healer) and `playwright` (the browser MCP server, used for manual exploration runs) |

The copies are kept identical to the live files; after any edit to an agent or skill, it is copied and compared.

## How the instructions changed

The instructions were refined from what the agents got wrong, not written once. Examples:

| Problem seen in agent output | Instruction change |
|---|---|
| The creator stated the opposite of a rule as fact ("hidden once validated") | Creator guardrail 1: never infer the opposite; table of real examples; `Proposed` label |
| Cases left an Expected result as only `Not known` although the rule stated the outcome | Rule outcome first, as fact, then `Open:`; a reviewer check for it |
| A UI case assumed `engineer` could add stock; no requirement says so (findings F-14) | Cases use `allaccess`; a "least-privileged user that can do the action" check |
| Separate cases for each invalid name (empty, too long, ...) with the same steps | One data-driven case with a Data sets table; one spec, one test per row; reviewer flags cases to merge |
| Data-driven API rows described the status in prose ("rejected") | Required `expected status` column with a code, or `Proposed, to confirm in Q-...: <code>` |
| The generator could not find the seed file and navigated to a URL without the host | Exact `generator_setup_page` arguments; navigation by clicking or from the printed page URL |
| Every test run, even of one spec, first logged in as all 6 demo users (a login smoke project) | Login smoke project removed: a test logs in only as its own user; healer only when the first run fails; reviewer in the background |
| Tool calls failed on descriptive targets, and repeated full-page snapshots made one automation run cost about 140K tokens | Refs from the latest snapshot as click targets; snapshot only when refs are needed, and filter long tables first |

The reviewers' Blockers and Majors, and how each was resolved, are in [`reviewer-catches.md`](reviewer-catches.md).
