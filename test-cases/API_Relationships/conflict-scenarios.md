# Conflict scenarios: REL test cases

### API-REL-057: Delete an inactive part that holds stock

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/{id}/` on an inactive part that has stock (created with `initial_stock`): whether the delete is refused is checked. |
| **Requirement** | R-CRUD-05 ([openapi-parts.yaml#L2803](../../requirements/openapi-parts.yaml#L2803)); inactive-first rule `open-questions.md Q-CRUD-02` (answered). Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/`. Index Not in schema #1. `initial_stock`: R-CRUD-13, `components.schemas.InitialStock`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | What-if business scenario (part with stock removed), Decision table (inactive x in use by stock) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: part `QA-<suffix> Stocked Part` created with `POST /api/part/` and `initial_stock` `{"quantity": "10"}`, then set inactive, as `admin`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the status code and error body are not known yet. |
| **Review** | Draft · Open question: Q-REL-10 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `GET /api/part/<pk>/` as `admin` | None | `200 OK`. `total_in_stock` is `10` (initial stock added, R-CRUD-13); `active` is `false`. |
| 2 | `DELETE /api/part/<pk>/` as `admin` | None | Proposed, to confirm in Q-REL-10: refused with `400` and an error body that names the stock as the reason; the part is not deleted. Open: Q-REL-10 (whether the delete is refused, status code and error body). |
| 3 | `GET /api/part/<pk>/` as `admin` | None | Proposed, to confirm in Q-REL-10: `200 OK`, the part still exists with `total_in_stock` `10`. |

**Postconditions and cleanup:** The part and its stock remain if the delete is refused. Removing the stock needs an endpoint outside the schema slice [open: Q-REL-10, how to remove stock for cleanup]; then `DELETE /api/part/<pk>/` (`204`).

**Notes:** Part with a stock history is the most common real case for a refused delete. The part is inactive first so the active-part refusal (Q-CRUD-02) is not what blocks the call.

**Duplicate check:** 54 · Review · matches: [API-REL-058](conflict-scenarios.md) (54), [API-REL-059](conflict-scenarios.md) (51), [API-REL-063](conflict-scenarios.md) (51)

**Duplicate judgement:** Keep · The dependent is stock, unlike a variant (058) or a revision (059), and the part is inactive, unlike the active part of 063: different starting state each time · test-case-reviewer, 2026-10-15

### API-REL-058: Delete an inactive template part that has a variant

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/{id}/` on an inactive template part that still has a variant: whether the delete is refused is checked. |
| **Requirement** | R-CRUD-05 ([openapi-parts.yaml#L2803](../../requirements/openapi-parts.yaml#L2803)); inactive-first rule `open-questions.md Q-CRUD-02` (answered). Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/`. Index Not in schema #1. Variants: R-REL-10 (`variant_of`, [openapi-parts.yaml#L4242](../../requirements/openapi-parts.yaml#L4242)). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | What-if business scenario (template removed while variants exist), State transition (template with variants to deleted) |
| **Priority** | P1 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: template part `QA-<suffix> Template` (`is_template` `true`) and variant `QA-<suffix> Variant` (`variant_of` = template pk), template set inactive, created as `admin`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the status code and error body are not known yet. |
| **Review** | Draft · Open question: Q-REL-10 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<template pk>/` as `admin` | None | Proposed, to confirm in Q-REL-10: refused with `400` and an error body that names the variant; the template is not deleted. Open: Q-REL-10 (whether the delete is refused, status code and error body). |
| 2 | `GET /api/part/<variant pk>/` as `admin` | None | Proposed, to confirm in Q-REL-10: `200 OK`, the variant exists and `variant_of` equals the template pk. Open: Q-REL-10 (the variant's `variant_of` if the delete was accepted). |

**Postconditions and cleanup:** Both parts remain if refused. As `admin`: set the variant inactive, `DELETE` it (`204`), then `DELETE` the template (`204`).

**Notes:** None

**Duplicate check:** 68 · Review · matches: [API-REL-059](conflict-scenarios.md) (68), [API-REL-057](conflict-scenarios.md) (54), [API-REL-063](conflict-scenarios.md) (50)

**Duplicate judgement:** Keep · The dependent is a variant (`variant_of`), unlike a revision (`revision_of`, 059) or stock (057, 063): a different starting state and a different link checked afterwards · test-case-reviewer, 2026-10-15

### API-REL-059: Delete an inactive original part that has a revision

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/{id}/` on an inactive original part that still has a revision: whether the delete is refused is checked. |
| **Requirement** | R-CRUD-05 ([openapi-parts.yaml#L2803](../../requirements/openapi-parts.yaml#L2803)); inactive-first rule `open-questions.md Q-CRUD-02` (answered). Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/`. Index Not in schema #1. Revisions: R-REL-10 (`revision_of`, [openapi-parts.yaml#L4212](../../requirements/openapi-parts.yaml#L4212)), R-REV-07. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | What-if business scenario (original removed while a revision exists), State transition (part with revision to deleted) |
| **Priority** | P2 |
| **Tags** | Regression, Settings-dependent |
| **Prerequisites** | User: `admin`; Settings: revision settings (`PART_ENABLE_REVISION`, `PART_REVISION_ASSEMBLY_ONLY`) = [open: Q-REL-08, names and defaults not rendered in the docs, Doc issue 8]; Data: original part `QA-<suffix> Original` (flags needed for revisions [open: Q-REL-08]) and revision `QA-<suffix> Original B` (`revision_of` = original pk, `revision` `B`), original set inactive, created as `admin`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the status code and error body are not known yet. |
| **Review** | Draft · Open question: Q-REL-10, Q-REL-08 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<original pk>/` as `admin` | None | Proposed, to confirm in Q-REL-10: refused with `400`; the original is not deleted. Open: Q-REL-10 (whether the delete is refused, status code and error body). |
| 2 | `GET /api/part/<revision pk>/` as `admin` | None | Proposed, to confirm in Q-REL-10: `200 OK`, the revision exists and `revision_of` equals the original pk. Open: Q-REL-10 (the revision's `revision_of` if the delete was accepted). |

**Postconditions and cleanup:** Both parts remain if refused. As `admin`: set the revision inactive, `DELETE` it (`204`), then `DELETE` the original (`204`).

**Notes:** A revision is itself a part (part-revision.md#L23), so it is a separate record that references the original.

**Duplicate check:** 68 · Review · matches: [API-REL-058](conflict-scenarios.md) (68), [API-REL-057](conflict-scenarios.md) (51)

**Duplicate judgement:** Keep · The dependent is a revision (`revision_of`, settings-dependent), unlike a variant (058) or stock (057): a different starting state and link checked · test-case-reviewer, 2026-10-15

### API-REL-060: Delete an inactive component used in an assembly's BOM

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/{id}/` on an inactive component part that is a line of an assembly's bill of materials: whether the delete is refused is checked. |
| **Requirement** | R-CRUD-05 ([openapi-parts.yaml#L2803](../../requirements/openapi-parts.yaml#L2803)); inactive-first rule `open-questions.md Q-CRUD-02` (answered). Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/`. Index Not in schema #1. BOM use: [manufacturing-bom.md#L219](../../requirements/docs/manufacturing-bom.md#L219) (Used In). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | What-if business scenario (component removed while used in a BOM), Decision table (inactive x used in BOM) |
| **Priority** | P1 |
| **Tags** | Smoke, Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: assembly `QA-<suffix> Assembly` (`assembly` `true`), component `QA-<suffix> Component` (`component` `true`, set inactive) and a BOM line linking them [open: Q-REL-11, endpoint and body to create a BOM item, outside the schema slice], created as `admin`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the BOM endpoint is outside the schema slice and the outcome is not known. |
| **Review** | Draft · Open question: Q-REL-11 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<component pk>/` as `admin` | None | Proposed, to confirm in Q-REL-11: refused with `400` and an error body that names the BOM; the component is not deleted. Open: Q-REL-11 (whether the delete is refused, status code and error body). |
| 2 | `GET /api/part/<component pk>/` as `admin` | None | Proposed, to confirm in Q-REL-11: `200 OK`, the component still exists. |
| 3 | Read the assembly's BOM [open: Q-REL-11, BOM list endpoint] | [open: Q-REL-11, request] | Proposed, to confirm in Q-REL-11: the BOM line for the component is unchanged. |

**Postconditions and cleanup:** Remove the BOM line [open: Q-REL-11], then as `admin` `DELETE` the component and the assembly after setting them inactive (`204`).

**Notes:** The BOM endpoints are outside `requirements/openapi-parts.yaml` (index, Out of scope).

### API-REL-061: Delete an inactive part that has a supplier part

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/{id}/` on an inactive part that is linked to a supplier by a supplier part: whether the delete is refused is checked. |
| **Requirement** | R-CRUD-05 ([openapi-parts.yaml#L2803](../../requirements/openapi-parts.yaml#L2803)); inactive-first rule `open-questions.md Q-CRUD-02` (answered). Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/`. Index Not in schema #1. Supplier part: R-REL-08 (`POST /api/company/part/`, [L185](../../requirements/openapi-parts.yaml#L185)). |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | What-if business scenario (part removed while supplied), Decision table (inactive x has supplier part) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: purchaseable part `QA-<suffix> Supplied Part` set inactive; a supplier company [open: Q-REL-06, how to create it] and a supplier part with `part` = part pk, `supplier` = company pk and `SKU` `QA-<suffix>-SKU`, created with `POST /api/company/part/` as `admin`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: the supplier company endpoint is outside the schema slice and the outcome is not known. |
| **Review** | Draft · Open question: Q-REL-10, Q-REL-06 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<part pk>/` as `admin` | None | Proposed, to confirm in Q-REL-10: refused with `400`; the part is not deleted. Open: Q-REL-10 (whether the delete is refused, status code and error body). |
| 2 | `GET /api/company/part/<supplier part pk>/` as `admin` | None | Proposed, to confirm in Q-REL-10: `200 OK`, the supplier part exists and `part` equals the part pk. Open: Q-REL-10 (the supplier part if the delete was accepted). |

**Postconditions and cleanup:** As `admin`: `DELETE /api/company/part/<supplier part pk>/`, then `DELETE` the part (`204`), then remove the supplier company [open: Q-REL-06].

**Notes:** None

### API-REL-062: Delete a template part after its last variant is deleted

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/{id}/` on an inactive template part succeeds with `204` once its only variant has been deleted. |
| **Requirement** | R-CRUD-05 ([openapi-parts.yaml#L2803](../../requirements/openapi-parts.yaml#L2803)); inactive-first rule `open-questions.md Q-CRUD-02` (answered). Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/`. Index Not in schema #1. Variants: R-REL-10. |
| **Area** | REL |
| **Type** | Positive |
| **Technique** | State transition (template with a variant, variant deleted, template deleted) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: template part `QA-<suffix> Template` (`is_template` `true`) and variant `QA-<suffix> Variant` (`variant_of` = template pk), created as `admin`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Yes: no unknown outcome; the steps use the answered Q-CRUD-02 rule. |
| **Review** | Draft |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `PATCH /api/part/<variant pk>/` as `admin` | `{"active": false}` | `200 OK`. `active` is `false`. |
| 2 | `DELETE /api/part/<variant pk>/` as `admin` | None | `204 No Content`. The body is empty (Q-CRUD-02). |
| 3 | `PATCH /api/part/<template pk>/` as `admin` | `{"active": false}` | `200 OK`. `active` is `false`. |
| 4 | `DELETE /api/part/<template pk>/` as `admin` | None | `204 No Content`. The body is empty (R-CRUD-05, Q-CRUD-02). |
| 5 | `GET /api/part/<template pk>/` as `admin` | None | `404 Not Found`. Body is `{"detail": "No Part matches the given query."}` (Q-CRUD-01). |

**Postconditions and cleanup:** No records remain.

**Notes:** Control case for API-REL-058: with no variant left the delete is accepted.

### API-REL-063: Delete an active part that holds stock

| Field | Value |
|---|---|
| **Summary** | `DELETE /api/part/{id}/` on an active part that has stock: whether the active-part refusal applies, and the part and stock remain. |
| **Requirement** | R-CRUD-05 ([openapi-parts.yaml#L2803](../../requirements/openapi-parts.yaml#L2803)); inactive-first rule `open-questions.md Q-CRUD-02` (answered). Schema: `requirements/openapi-parts.yaml DELETE /api/part/{id}/`. Index Not in schema #1. Active part: R-CRUD-05, `open-questions.md Q-CRUD-02`. |
| **Area** | REL |
| **Type** | Negative |
| **Technique** | Decision table (active x in use by stock), What-if business scenario (delete tried without deactivating) |
| **Priority** | P2 |
| **Tags** | Regression |
| **Prerequisites** | User: `admin`; Settings: None; Data: active part `QA-<suffix> Stocked Part` created with `POST /api/part/` and `initial_stock` `{"quantity": "10"}` as `admin`; Pre-steps: get `admin`'s token with `GET /api/user/me/token/` (basic auth) and send it as `Authorization: Token <token>`. |
| **Automation** | Partial: which refusal applies when both conditions hold is not known. |
| **Review** | Draft · Open question: Q-REL-10 |

**Steps**

| # | Request | Payload / parameters | Expected result |
|---|---|---|---|
| 1 | `DELETE /api/part/<pk>/` as `admin` | None | Proposed, to confirm in Q-REL-10: `400` with `{"non_field_errors": ["Cannot delete this part as it is still active"]}` (the answer to Q-CRUD-02 for an active part); the part is not deleted. Open: Q-REL-10 (which refusal is returned when the part is also in use). |
| 2 | `GET /api/part/<pk>/` as `admin` | None | `200 OK`. The part still exists, `active` is `true` and `total_in_stock` is `10`. |

**Postconditions and cleanup:** One part with stock. Same cleanup as API-REL-057 (stock removal [open: Q-REL-10]).

**Notes:** Related: API-CRUD-014 (active part with no dependents).

**Duplicate check:** 51 · Review · matches: [API-REL-057](conflict-scenarios.md) (51), [API-REL-058](conflict-scenarios.md) (50)

**Duplicate judgement:** Keep · The part is active (decision-table column active x in use), unlike the inactive stocked part of 057 and the inactive template of 058 · test-case-reviewer, 2026-10-15
