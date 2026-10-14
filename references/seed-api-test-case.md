# Seed: manual API test case

The reference format for every manual API test case. It uses the same header fields as `seed-manual-test-case.md` (Summary to Review, Postconditions, Notes, Duplicate check, Duplicate judgement: same meaning and rules) and differs only where shown here. Agents copy the template, fill every field, and match the worked example for level of detail. A field that does not apply says `None`; it is never deleted.

---

## API Areas

| Area | Covers |
|---|---|
| `CRUD` | Create, read, update (PUT/PATCH) and delete on Parts and Part Categories: the happy path and the response returned. |
| `LST` | List endpoints: filtering, ordering, pagination, search. |
| `VAL` | Field validation: required, max length, nullable, read-only, type and format, invalid payloads. |
| `REL` | Relational integrity: category, default location, supplier and manufacturer links, conflicts when deleting or moving related records. |
| `SEC` | Authentication and per-role permissions: missing or invalid token, users without the required permission. |

Each case belongs to one Area. API cases live in `test-cases/<Area folder>/<functionality>.md`, the Area's folder from "Area folders" in `seed-manual-test-case.md` (e.g. `CRUD` is `test-cases/API_Create_Read_Update_Delete/`); the Area value and the case, rule and question IDs (`API-CRUD-001`, `R-CRUD-01`, `Q-CRUD-01`) stay short. A case that checks a CRUD call as a user who should be blocked is `SEC`; a create that fails on a bad field value is `VAL`.

## Standing rules for API cases

Set by the architect. They apply to every API case and are not open questions.

- **Not found:** a `GET` or `DELETE` of a resource that does not exist returns `404 Not Found`. Every operation with an `{id}` in its path that supports `GET` or `DELETE` has its own Negative case for it (one case per operation, not one per resource), with the Expected result `404 Not Found` and, as observed on 1.5.6, a body of `{"detail": "No <Model> matches the given query."}` (e.g. `No Part matches the given query.`). Never write `Not known` for it.
- **How to get a non-existent ID:** create the resource as `admin` (parts: make it inactive), delete it, and reuse its `pk`. Never a guessed number.
- **Category delete body:** `DELETE /api/part/category/{id}/` needs `{"delete_parts": <bool>, "delete_child_categories": <bool>}` in the body in 1.5.6; without it the call returns `400` before the resource is looked up (not in the schema). Send both flags in every category-delete step.

## Template

### API-<Area>-NNN: <Summary>

| Field | Value |
|---|---|
| **Summary** | One sentence: what is verified, and under which condition. |
| **Requirement** | `R-<Area>-NN` from `test-cases/<Area folder>/requirements-inventory.md`, plus the schema operation: `requirements/openapi-parts.yaml <METHOD> <path>` and, where a field rule applies, the component: `components.schemas.<Name>.<field>`. Add a docs link if the rule cites one. |
| **Area** | `CRUD` · `LST` · `VAL` · `REL` · `SEC` (see API Areas above) |
| **Type** | Positive · Negative · Boundary |
| **Technique** | As in the UI seed. Schema constraints (`required`, `maxLength`, `nullable`, `readOnly`, `enum`, `format`) are stated limits: name them, e.g. `Boundary value analysis (name maxLength + 1)`. |
| **Priority** | As in the UI seed. |
| **Tags** | As in the UI seed. |
| **Prerequisites** | One line, semicolon-separated, in this order: `User: <demo user whose token is sent, least-privileged that can make the call, or "none (no Authorization header)">; Settings: <setting = state, or None>; Data: <records that must exist and how they are created, names with the run suffix QA-<8 hex>, or None>; Pre-steps: <e.g. get the user's token with GET /api/user/me/token/, or None>`. |
| **Automation** | Yes / No / Partial, with a reason if not Yes. |
| **Review** | As in the UI seed. |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | One call per step: `<METHOD> <path>` as `<user>`. Paths only, never a host or port. | Exact JSON body or query parameters. `None` for none. | Status code first, then each check on the response: fields and values, the response body valid against its schema component, headers if relevant, and the business rule (e.g. the record is or is not created). Never "succeeds". Unknown outcome: `Not known: depends on open question Q-<Area>-NN (<what is unknown>).` |

Keep three columns in this order: the duplicate check reads them as action, test data and expected result.

**Postconditions and cleanup**, **Notes**, **Duplicate check**, **Duplicate judgement:** as in the UI seed. Cleanup is done through the API as `admin` (for parts: `PATCH` `active: false`, then `DELETE`).

---

## Worked example

### API-CRUD-001: Create a part with valid data

| Field | Value |
|---|---|
| **Summary** | A user with part create permission can create a part with `POST /api/part/`, and the response returns the new part with the values sent. |
| **Requirement** | `R-CRUD-TBD` (assigned in the API inventory). Schema: `requirements/openapi-parts.yaml POST /api/part/`, response `components.schemas.Part`. |
| **Area** | CRUD |
| **Type** | Positive |
| **Technique** | Equivalence partitioning (valid class: required fields with valid values) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `engineer` (manage parts); Settings: None; Data: category `QA-<suffix> Category` created with `POST /api/part/category/` as `admin`; Pre-steps: get `engineer`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes: core CRUD, Phase 2 scope. |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `POST /api/part/` as `engineer` | `{"name": "QA-<suffix> Resistor 10k", "description": "Seed API part", "category": <category pk>}` | `201 Created`. Body is valid against `Part`; `name`, `description` and `category` equal the payload; `pk` is an integer; `active` is `true`. |
| 2 | `GET /api/part/<pk from step 1>/` as `engineer` | None | `200 OK`. Body is valid against `Part` and equals the step 1 response for `name`, `description` and `category`. |
| 3 | `GET /api/part/` as `engineer` | `category=<category pk>` | `200 OK`. The list contains exactly one part, with the `pk` from step 1. |

**Postconditions and cleanup:** one new part in `QA-<suffix> Category`. Cleanup as `admin`: `PATCH /api/part/<pk>/` with `{"active": false}`, `DELETE /api/part/<pk>/` (`204`), then `DELETE /api/part/category/<category pk>/`.

**Notes:** which fields are required comes from the `Part` schema's `required` list, not from the UI form.
