# Review: API-VAL-087 Part name is validated on create (absent, null, blank, length boundaries)

| Item | Value |
|---|---|
| Spec | `tests/api/VAL/api-val-087.spec.ts` (rows: `data/api/VAL/api-val-087.json`) |
| Case | `test-cases/API_Field_Validation/part-name-validation-on-create.md` (API-VAL-087), Review: Approved · Open question: Q-VAL-01, Q-VAL-02 |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-10-16 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 2 Major, 3 Minor, 4 Info |

## A. Automated checks

| Check | Result |
|---|---|
| `npm run typecheck` | Pass, no errors. |
| `npx eslint` on the spec, `clients/parts.client.ts`, `clients/base.client.ts`, `clients/index.ts`, `fixtures/index.ts`, `fixtures/api.fixture.ts`, `fixtures/data.fixture.ts`, `fixtures/expect.ts` | Pass (exit 0), 0 errors, 6 warnings, all in the spec: `16:11`, `18:27`, `27:11` `playwright/no-conditional-in-test`; `30:19`, `31:13`, `32:13` `playwright/no-conditional-expect`. See findings 1 and 4. |
| `npx playwright test tests/api/VAL/api-val-087.spec.ts --list` | 7 tests in project `api` (one per row: absent, null, empty, whitespace only, below limit, on limit, over limit) after `api-smoke`. |

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| 1 | `POST /api/part/` as `engineer`, `{"name": <row.name>, "description": "QA-<suffix> <row.tag>"}`, name key left out for *absent* | `<row.expected status>` | `1. POST /api/part/ as engineer` (l.24) | `await expect(res).toHaveStatus(row['expected status'])` (l.26) | Covered |
| 1 | | For a `201`: body valid against `Part` | l.24 | `await expect.soft(res).toMatchSchema('Part')` (l.30), inside `if` | Covered (but see finding 1) |
| 1 | | For a `201`: `name` equals the payload | l.24 | `expect(body.name).toBe(payload.name)` (l.31), inside `if` | Covered (but see finding 1) |
| 1 | | For a `201`: `pk` is an integer | l.24 | `expect(Number.isInteger(body.pk)).toBe(true)` (l.32), inside `if` | Covered (but see finding 1) |
| 1 | | For a rejected request: body is `<row.error>` | l.24 | None; comment l.34 | Covered as stated: every rejected row's error is `Open: Q-VAL-01`, nothing to assert (Info 7) |
| 2 | `GET /api/part/` as `engineer`, `search=QA-<suffix> <row.tag>`, `limit=10` | `200 OK` | `2. GET /api/part/ as engineer` (l.37) | `toHaveStatus(200)` (l.39) | Covered |
| 2 | | `count` is `<row.count>` | l.37 | `expect(body.count).toBe(row.count)` (l.41) | Covered |

**Data sets (rows file vs case table):** 7 objects for 7 table rows, labels identical (`absent`, `null`, `empty`, `whitespace only`, `below limit`, `on limit`, `over limit`), tags `chk01`-`chk07` identical, `expected status` 400/400/400/400/201/201/400 and `count` 0/0/0/0/1/1/0 equal the table (Proposed values taken as stated, Info 6). Name lengths: `QA-<suffix>` (11) + 88/89/90 gives 99/100/101, as the table states. `null`, `""`, `"   "` (3 spaces) unchanged. The `error` column is not carried over (finding 5). The test title per row is `API-VAL-087 [<label>]: <case title>`.

**Other B checks**

- Request fidelity: `api.parts.create(payload)` sends `{ name, description }` unchanged; the absent row sends `{ description }` only; negative values are not altered. Step 2 uses `api.parts.list({ search: tag, limit: 10 })`, matching the case.
- Order and titles: two `test.step`s, in order, titled `<n>. <request>`.
- Prerequisites: `test.use({ user: 'engineer' })` matches; no data or settings needed.
- Cleanup: 201 rows are registered with `data.trackPart(body.pk)` right after the status check and before the schema and value checks; rows that may create a nameless part are not covered (finding 2).
- Schema: `Part` is the `201` response component for `part_create` (`openapi-parts.yaml` L771-776); the check is `expect.soft`.
- Traceability: `// case:` header correct, `describe('Part name validation on create')`, tags `@smoke`, `@regression` match the case's Tags.
- Review status: Approved.
- Fixme: none.

## C. Conventions

Passed: single import from `fixtures`, `test.use` user, no raw requests, paths or hosts, existing client methods only (`ResourceClient.create`, `list`; no client changes), rows file at `data/api/VAL/api-val-087.json`, spec name and location, step titles, status first, soft schema, `limit` sent on the list (API §10). Branching on a row and the rows file's missing column: findings 1, 2, 5.

## D. SOLID and design

Passed: the spec depends only on the `api` and `data` fixtures; `PartsClient` is unchanged and keeps the `ResourceClient` contract; no duplicated client logic; one spec for one case. See finding 1 (the case's conditional Expected result forces a branch) and finding 2 (fixture cannot register a nameless part).

## E. Playwright and TypeScript practice

Passed: every request and matcher awaited, no `try/catch`, no `test.only`, no `any`, casts or non-null assertions, `const` throughout, unique `QA-` names per test, no dependence on demo data. Conditionals: findings 1 and 4; readability: findings 3 and 4.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Major | `tests/api/VAL/api-val-087.spec.ts:27-33` | API §3 data-driven: "Never branch on a row inside a test"; API §3 "No conditional logic"; lint `no-conditional-in-test`, `no-conditional-expect` (warnings) | `if (row['expected status'] === 201) { ... trackPart, toMatchSchema, name, pk ... }`: the 201 rows and the rejected rows run different assertions. The cause is the case: step 1's Expected result is itself conditional ("For a `201`, ... For a rejected request, ..."), so the rows do not share one set of checks. | Report a `CASE DEFECT` to the architect: split the table into an accepted-rows case (`below limit`, `on limit`: schema, name, pk) and a rejected-rows case (`absent`, `null`, `empty`, `whitespace only`, `over limit`: error body, count 0), each with unconditional steps; then remove the `if`. Do not change the assertions themselves. |
| 2 | Major | `tests/api/VAL/api-val-087.spec.ts:20-22, 29` | API §3 "Cleanup without branching" (register before the request by unique name; if the fixture cannot, stop and report); case Postconditions ("any row the API accepts against the proposal") | For `absent`, `null`, `empty` and `whitespace only` the registered name is `${suffix}` alone (`QA-XXXXXXXX`), a name these rows can never create. The pk is tracked only inside the `if` for rows *expected* to return 201, after a hard `toHaveStatus`. If InvenTree accepts any of these four rows (which the case explicitly anticipates), `toHaveStatus` fails, the part (name `""`, `"   "` or default) is never registered and is left behind without a `QA-` name. The comment on l.21 ("for them the pk is tracked after a 201") does not match the code. | The fixture cannot register a part by description tag: report it to the architect (fixtures are the architect's change), e.g. a `data` method that registers parts found by a search term, called with `tag` before the request for every row. Until then, correct the l.21 comment so it does not claim cleanup that does not happen. |
| 3 | Minor | `tests/api/VAL/api-val-087.spec.ts:13` | Readability (E) | `data.name('').trim()` rebuilds the suffix by relying on `qaName`'s `<suffix> <label>` format. `TestData.suffix` is public (`fixtures/data.fixture.ts:19`). | `const suffix = data.suffix;` |
| 4 | Minor | `tests/api/VAL/api-val-087.spec.ts:15-18, 22` | Readability (E); API §3 no conditional logic | The padded name is built twice (l.16 and l.22, `'x'.repeat(row['name padding'])` repeated) and the input building uses two conditionals (`typeof row.name === 'string'`, sentinel `'(key left out)'`), each a lint warning. | Build the padded QA name once (`const qaName = suffix + 'x'.repeat(row['name padding'])`) and reuse it for the payload and for `trackPart`; keep a single, commented rule for the absent row. |
| 5 | Minor | `data/api/VAL/api-val-087.json:2-8` | API §3 Rows: "the row's inputs and expected values under the case's column names ... no value changed" | The case's `error` column (`Open: Q-VAL-01 (error body and text)` / `None`) is missing from every row, so the rows file does not mirror the table and the open check is visible only in a spec comment. | Add `"error"` to every row with the case's value (`"Open: Q-VAL-01 (error body and text)"` or `null` for `None`). |
| 6 | Info | `data/api/VAL/api-val-087.json:2-4, 5-6, 8` | Case Data sets | `expected status` 400 for absent, null, empty, whitespace, over limit and `count` 0 for empty and whitespace are `Proposed, to confirm in Q-VAL-01/Q-VAL-02` in the case. Asserting them as stated is correct; a failure there is an answer to the open question, not a test bug. | None. |
| 7 | Info | `tests/api/VAL/api-val-087.spec.ts:34` | Case step 1 | The rejected body is not asserted; the case gives it only as `Open: Q-VAL-01`. Not Weakened. | Add the assertion once Q-VAL-01 is answered and the case updated. |
| 8 | Info | `tests/api/VAL/api-val-087.spec.ts:22, 29` | Cleanup | 201 rows are registered twice (by name and by pk). Harmless: cleanups run in reverse, the pk cleanup deletes the part and the name lookup then finds nothing (`data.fixture.ts:86-92, 143`). | Optional: none needed. |
| 9 | Info | `tests/api/VAL/api-val-087.spec.ts:38` | Case Notes | Step 2 relies on `search` matching `description` as well as `name`; the case's Notes state this assumption. Not verified (tests not run by the reviewer). | None. |

## Outside scope

None.
