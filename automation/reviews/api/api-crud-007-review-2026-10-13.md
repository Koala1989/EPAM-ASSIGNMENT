# Review: API-CRUD-007 The read-only full_name is returned for a created part

| Item | Value |
|---|---|
| Spec | `tests/CRUD/api-crud-007.spec.ts` |
| Case | `test-cases/API_Create_Read_Update_Delete/part-and-category-crud.md` (API-CRUD-007), Review: Approved · 2026-10-13 |
| Reviewer | api-test-reviewer (Opus 5.5), 2026-10-13 |
| Verdict | Approve with changes |
| Findings | 0 Blocker, 1 Major, 1 Minor, 3 Info |

## A. Automated checks

- `npm run typecheck`: pass (no errors).
- `npx eslint tests/CRUD/api-crud-007.spec.ts clients/parts.client.ts clients/base.client.ts clients/index.ts fixtures/data.fixture.ts fixtures/api.fixture.ts fixtures/expect.ts fixtures/index.ts utils/names.ts`: pass (0 errors, 0 warnings).
- `npx playwright test tests/CRUD/api-crud-007.spec.ts --list`: lists `[api] › CRUD\api-crud-007.spec.ts:7:7 › Part and category CRUD › API-CRUD-007: The read-only full_name is returned for a created part`.

## B. Case coverage

| Case step | Request | Expected result | `test.step` in spec | Assertion(s) | Verdict |
|---|---|---|---|---|---|
| Prereq | Settings: `PART_NAME_FORMAT` at its default | Setting has the default template | none | none | Missing (see finding 1) |
| 1 | `POST /api/part/` as engineer, `{"name": "QA-<suffix> Full Name", "IPN": "QA-<suffix>-IPN"}` | `201 Created` | `1. POST /api/part/ as engineer` (l.16) | `toHaveStatus(201)` (l.18) | Covered |
| 1 | | `full_name` is `QA-<suffix>-IPN \| QA-<suffix> Full Name` | | `expect(body.full_name).toBe(expectedFullName)` (l.21), `expectedFullName = \`${ipn} \| ${name}\`` (l.13) | Covered |
| 2 | `GET /api/part/<pk from step 1>/` as engineer | `200 OK` | `2. GET /api/part/<pk from step 1>/ as engineer` (l.24) | `toHaveStatus(200)` (l.26) | Covered |
| 2 | | `full_name` equals the value from step 1 | | `expect(body.full_name).toBe(expectedFullName)` (l.28) | Covered (compared to the expected constant; equivalent because step 1 asserts the same value with `toBe`) |

Other B checks:
- Request fidelity: `api.parts.create({ name, IPN: ipn })` (l.17) sends exactly the case payload; name `QA-<suffix> Full Name` via `data.name('Full Name')` (l.11), IPN `QA-<suffix>-IPN` (l.12). `api.parts.retrieve(pk)` (l.25). Pass.
- Order and titles: two steps, in order, titled as the case's requests. Pass.
- Prerequisites: `test.use({ user: 'engineer' })` (l.4) matches. Data: None, matches. Settings: not ensured (finding 1).
- Cleanup: the created part is registered with `data.trackPart(body.pk)` in step 1 (l.20). Pass (see Info 4 on placement).
- Schema: the case states no schema check; none asserted. `full_name` is `readOnly` string in `Part` (openapi-parts.yaml L4152-4155). Pass.
- Traceability: `// case:` header (l.1), title matches the case title, describe `Part and category CRUD`, tags `@regression`, `@settings` map the case's Tags "Regression, Settings-dependent". Pass.
- Review status: Approved. Pass.
- Fixme: none used. N/A.
- The case Summary also mentions "a value sent for it is not used as the name"; no step states it and the Notes put it in VAL scope, so its absence is correct (Info 5).

## C. Conventions

- §3 structure, import from `../../fixtures`, one test, steps, status first: pass. §4: no new client code; `PartsClient`/`ResourceClient` used unchanged. §5 fixtures via `fixtures/index.ts`: pass. §7 no hosts/URLs/credentials: pass. §9 naming: pass. §8 isolation: see finding 1; readability of the IPN derivation: finding 2.

## D. SOLID and design

- Spec tests one case; no client changes; depends only on `api` and `data` fixtures, both used. No duplication. Pass.

## E. Playwright and TypeScript practice

- All `expect(res).toHaveStatus` awaited; no conditionals, loops, `try/catch` or `test.only`; `const` used except `pk`, which must be shared across steps; unique QA names. Pass. See findings 2, 3, 4.

## Findings

| # | Severity | File:line | Rule | Problem | Suggested change |
|---|---|---|---|---|---|
| 1 | Major | `tests/CRUD/api-crud-007.spec.ts:10-14` | Case Prerequisites "Settings: `PART_NAME_FORMAT` at its default"; reviewer checklist B (settings through `data.setSetting`); §8 isolation | The spec assumes the instance's `PART_NAME_FORMAT` is at its default instead of establishing it. If any earlier run, manual change or another environment leaves a different format, step 1 fails for a reason unrelated to the behaviour under test. The prerequisite the case names is not automated. | Before step 1, `await data.setSetting('PART_NAME_FORMAT', <default template from the case Notes>)` (restored after the test by the fixture), ideally with the default template held in one named constant. This also makes the `@settings` tag literally true per §8. |
| 2 | Minor | `tests/CRUD/api-crud-007.spec.ts:12` | Readability (E), §8 names | `` `${name.split(' ')[0]}-IPN` `` derives the suffix by parsing the formatted name, coupling the spec to the internal format of `qaName`. | Use the fixture's public suffix: `` const ipn = `${data.suffix}-IPN`; `` which reads like the case's `QA-<suffix>-IPN`. |
| 3 | Info | `tests/CRUD/api-crud-007.spec.ts:19,27` | TypeScript (E) | `res.json()` returns `any`; `body.pk` and `body.full_name` are unchecked. Acceptable and consistent with the other CRUD specs, noted only. | Optional: type the body (e.g. `as ApiRecord`) if the suite adopts that pattern. |
| 4 | Info | `tests/CRUD/api-crud-007.spec.ts:18-20` | §5 "registered at once" | `trackPart` runs after `toHaveStatus(201)`; if the POST created the part but returned a different 2xx code, the assertion throws first and the part leaks. Low risk. | Optionally parse the body and track before asserting the status, or accept as is (same pattern as other specs). |
| 5 | Info | case l.162 | Case consistency | The case Summary claims "a value sent for it is not used as the name", which no step tests (Notes defer it to VAL). Not a spec defect. | Architect may align the Summary with the steps. |

## Outside scope

- None.
