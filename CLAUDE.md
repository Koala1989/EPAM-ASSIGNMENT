# EPAM Quality Architect assignment: InvenTree Parts

AI-assisted QA of InvenTree's **Parts module only**: manual UI and API test cases generated from requirements, then Playwright UI automation and pytest API automation. Agents do the heavy lifting; the architect (the user) directs, reviews and approves.

## Application under test

- **InvenTree 1.5.6 (API 530)**, local Docker. Never upgrade it, and never compare against another version's docs.
- The address and user passwords come only from `automation/ui/config/env.ts` (overridable via `automation/ui/.env`, template `.env.example`). Demo users and roles: `automation/ui/data/users.json`.
- Never run tests or create data on demo.inventree.org.
- Test records use a `QA-` name prefix and are cleaned up. Never delete records you did not create.

## Layout

| Path | Contents |
|---|---|
| `requirements/docs/` | Docs snapshot pinned to 1.5.6 (read-only). `INDEX.md`: heading index. |
| `requirements/.rag-index/` | Local vector index over the docs (gitignored, rebuildable). |
| `test-cases/requirements-inventory.md`, `test-cases/<Area>/requirements-inventory.md` | Reviewed, rule-ID'd requirements (`R-<Area>-NN`). Built by a full read of the docs, not by RAG. |
| `test-cases/<Area>/*.md` | Manual cases (`UI-<Area>-NNN`, `API-<Area>-NNN`), one folder per Area. |
| `test-cases/<Area>/open-questions.md`, `test-cases/findings.md` | Questions for the architect; app/doc mismatches found. |
| `references/seed-manual-test-case.md` | The manual case format. |
| `automation/ui/` | Playwright + TypeScript framework. Rules: `automation/ui/CONVENTIONS.md`. |
| `tools/` | `dedupe_cases.py` (duplicate check), `rag/` (index build and query), `llm/` (prompt-caching demo). |
| `.claude/agents/`, `.claude/skills/` | Agents and skills. Submission copies: `agents/configs/`. |

## Agents and skills

| Step | Use |
|---|---|
| Manual cases | `/gen-test-cases <UI\|API> <functionality>`: test-case-creator, then duplicate-judge |
| UI automation | `/automate-cases <case ID> ...`: playwright-test-generator, healer, 3-run check, playwright-test-reviewer |

Keep reviewers and judges independent: pass them IDs or paths only, never another agent's reasoning or report. After editing any file in `.claude/agents/` or `.claude/skills/`, copy it to `agents/configs/` (same relative path) and check the copies match.

## Hard rules

- **Never assume a requirement.** Anything the docs and inventory do not state becomes an open question. Cases are still written, marked `Draft · Open question: Q-<Area>-NN`.
- **The architect owns approval.** Only the user sets a case's Review field to Approved, Changed or Rejected, edits requirements inventories, or answers open questions.
- **Never delete or rewrite saved test cases** unless the user asks.
- **Only Approved or Changed cases are automated.**
- **An app/case mismatch is a finding, not a fix.** Never weaken an assertion to make a test pass: mark it `test.fixme()` with a `// FINDING:` or `// CASE DEFECT:` comment and report it.
- **No hard-coded URLs, hosts, ports or credentials** anywhere outside `automation/ui/config/env.ts`, including agent files.
- **UI tests log in through the real login form**, never with saved sessions or cookies.

## Commands

| Task | Command (from repo root unless noted) |
|---|---|
| Duplicate check | `python tools/dedupe_cases.py --case <ID> ...` |
| Build RAG index | `tools/rag/.venv/Scripts/python.exe tools/rag/build_index.py` (after any change to `requirements/docs/`) |
| Query RAG index | `tools/rag/.venv/Scripts/python.exe tools/rag/query_index.py "<question>" --top-k 3` |
| UI lint / types / tests | from `automation/ui/`: `npm run lint`, `npm run typecheck`, `npx playwright test <spec>` |
| Stability check | from `automation/ui/`: `npx playwright test <spec> --project=chromium --repeat-each=3` |

## Evidence

The brief grades the agent workflow itself, so keep the trail:
- Agent prompts go in `agents/prompts.md`.
- Never present hand-written tests as agent-generated.
