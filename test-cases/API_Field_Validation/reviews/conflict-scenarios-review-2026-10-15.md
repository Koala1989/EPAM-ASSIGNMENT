# Review: Conflict scenarios (API), 2026-10-15

**Cases reviewed:** API-VAL-068 to API-VAL-086 (`test-cases/API_Field_Validation/conflict-scenarios.md`), API-REL-057 to API-REL-063 (`test-cases/API_Relationships/conflict-scenarios.md`) · **Verdict:** Approve with changes

Scope: duplicate name/IPN/revision, duplicate category name under one parent, deleting a part in use.

## Coverage

`coverage_check.py --area VAL --area REL` (both case files): Rules 29 · covered 7 · not cited 22 · exit 0 (every cited rule ID exists; cross-Area IDs R-Part-13, R-REV-07, R-CRUD-04, -05, -09, -12, -13 also resolve).

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-VAL-01 / R-Part-13 (name unique) | VAL-068 to 073 | Covered | Exact repeat (068), IPN differs (069), revision differs (070), case variant (071), trailing space (072), PATCH (073). Negative present. See findings 1, 2. |
| R-VAL-03 (IPN, duplicates by setting) | VAL-074 to 077 | Covered | Setting on (074), off (075), PATCH (076), empty IPN (077). No IPN letter-case variant although Q-VAL-10 asks about IPN (finding 11, optional). |
| R-VAL-07 / R-REV-07 / R-REL-10 (revision code unique per original) | VAL-070, 078 to 081 | Covered | Same original (078), other original (079), PATCH (080), case variant (081). |
| R-VAL-13 / R-REL-06 (category name under one parent) | VAL-082 to 086 | Covered | Same parent (082), other parent (083), top level (084), rename (085), move (086). No case-variant category name (optional). |
| R-CRUD-05 (+ answered Q-CRUD-02) (delete a part in use) | REL-057 to 063 | Covered | Stock (057), variant (058), revision (059), BOM (060), supplier part (061), control after variant removed (062), active + stock (063). |
| R-REL-08 | REL-061 | Covered (setup only) | Used to create the supplier-part dependent. |
| R-CRUD-04, R-CRUD-09, R-CRUD-12, R-CRUD-13 | VAL-073, 076, 080, 085, 086, 077, REL-057, 063 | Covered (supporting) | Cited for the update or setup operation. |
| R-VAL-02, -04, -05, -06, -08 to -12, -14 to -18 | none | Out of scope | Field-validation functionality (lengths, types, read-only, write-only, content types); covered by API-VAL-001 to 067. |
| R-REL-01 to -05, -07, -09 | none | Out of scope | Relationships functionality (category/location links, hierarchy, initial supplier). |
| R-REL-11 (locked part cannot be deleted) | none | Out of scope | Locked-part functionality, API-REL-052 to 056; not "in use". |

404 standing rule: the `{id}` operations touched (`/api/part/{id}/`, `/api/part/category/{id}/`, `/api/company/part/{id}/`) already have their 404 cases (API-CRUD-009, -018, -023, -024, API-REL-035, -036). No 404 gap. Negative cases present. No permission rule in scope.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| 1 | Major | API-VAL-068, 070, 071, 072, 073 | Open-question marking / Prerequisites | Both parts share IPN `QA-<suffix>-IPN-1` but Settings is `None` and Q-VAL-09 is not marked. If duplicate IPNs are not allowed, 073's setup (P2 with IPN-1) fails, and 068's rejection could come from the IPN rule, so the case would pass for the wrong reason; 070/071/072 would be rejected for the IPN, which hides the name/revision behaviour they test. | R-VAL-03; Q-VAL-09 (default and setting open); findings F-05 (setting on in the test instance) | Edit Settings to `duplicate IPN allowed [open: Q-VAL-09, ...]` (as in API-VAL-074) and add Q-VAL-09 to Review. |
| 2 | Major | API-VAL-068 (steps 2, 3), API-VAL-073 (steps 1, 2) | Rule outcome stated | The rejection is written `Proposed, to confirm in Q-VAL-08` although the cited R-Part-13 states the Name is unique, and with name, IPN and revision all equal it is a duplicate under every reading of Doc issue 2 (068's own Note says so). | R-Part-13, [part-views.md#L32](../../../requirements/docs/part-views.md#L32); index Doc issue 2 | Edit to fact first: `The part is not created (R-Part-13). Open: Q-VAL-08 (status code, error body, field).`; 073: `The update is not accepted (R-Part-13) ...`; step 3/2 count/name unchanged as fact. |
| 3 | Minor | API-VAL-080 step 2 | Rule outcome stated | `revision is still C` is Proposed, but step 1 states as fact (R-REV-07) that the update is not accepted; API-VAL-078 step 2 states the same consequence as fact. | R-REV-07, [part-revision.md#L37](../../../requirements/docs/part-revision.md#L37) | Edit to `200 OK. revision is still C (R-REV-07).` |
| 4 | Minor | API-VAL-071, 072, 081 | Technique / Type | Type is Negative, but the expected (proposed) outcome is `201 Created` (value accepted). 069/070/079/083 with the same pattern are Positive. | Q-VAL-10 proposed answer | Set Type to Positive (or re-label once Q-VAL-10 is answered). |
| 5 | Minor | API-VAL-073, 080, 085, 086 | Seed format | Requirement cites the schema operation `POST /api/part/` or `POST /api/part/category/` although the call under test is `PATCH /api/part/{id}/` (`PatchedPart`) or `PATCH /api/part/category/{id}/` (`PatchedCategory`); the PATCH is only named as an extra rule. | Seed API Requirement field; [openapi-parts.yaml#L2767](../../../requirements/openapi-parts.yaml#L2767), [#L1370](../../../requirements/openapi-parts.yaml#L1370) | Edit the Schema part of Requirement to the PATCH operation and component. |
| 6 | Minor | API-REL-060 | Seed format (source link) | `manufacturing-bom.md#L219` "(Used In)" points to the *Replacing Components* heading; *Used In* is described at part-views.md#L90-92. | [part-views.md#L90](../../../requirements/docs/part-views.md#L90), [manufacturing-bom.md#L219](../../../requirements/docs/manufacturing-bom.md#L219) | Edit the link. |
| 7 | Minor | API-VAL-072; open-question files | Open-question marking | 072 step 1 says "if rejected: status code and error body" without a question ID (Q-VAL-08's subject); 072 is not marked Q-VAL-08. The question files' Affected cases omit cases that are marked with them: Q-VAL-06 (VAL-070), Q-REL-08 (VAL-070, 078, 079, 080, 081, REL-059), Q-REL-06 (REL-061), Q-VAL-08 (072). | Q-VAL-06, Q-VAL-08, Q-REL-06, Q-REL-08 rows | Mark 072 with Q-VAL-08; architect updates the Affected cases columns. |
| 8 | Minor | API-REL-058, 059, 061 | Specific Expected results | Step 1 expects "the template/original/part is not deleted", but no step reads that part back (only its dependent); API-REL-057 does (step 3). | R-CRUD-05; Q-REL-10 | Add `GET /api/part/<target pk>/` expecting `200 OK` (Proposed, Q-REL-10). |
| 9 | Minor | API-REL-057 to 063 | User | All calls as `admin`; the seed lists `allaccess` for full create/edit/delete (engineer's delete permission is open, Q-SEC-04). Consistent with API-CRUD-013/014, which also use `admin`. | Seed demo users; seed API Prerequisites (least-privileged) | Switch to `allaccess`, or keep `admin` and note why. |
| 10 | Minor | API-REL-063 step 1 | Rule outcome stated | "the part is not deleted" sits inside the Proposed sentence although the answered Q-CRUD-02 settles that an active part is not deleted (`400`, part unchanged); only which message wins is open. | Q-CRUD-02 answer | Edit: `The part is not deleted (Q-CRUD-02). Proposed, to confirm in Q-REL-10: 400 with ... Open: Q-REL-10 (...)`. |
| 11 | Minor | R-VAL-03, R-VAL-13 | Depth (optional) | Q-VAL-10 asks whether IPN comparison is case-sensitive/trimmed, but no case sends a case-variant IPN with duplicates not allowed; no case-variant category name. | Q-VAL-10 | Optional: rerun the creator for these two cases. |

No Blocker.

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| API-VAL-068 | 52 | API-VAL-071 | Keep | Exact repeat vs letter-case and trailing-space variants: different class and outcome. |
| API-VAL-069 | 58 | API-VAL-070 | Keep | IPN differs vs revision differs: different decision-table column. |
| API-VAL-070 | 58 | API-VAL-069 | Keep | Revision differs (settings-dependent) vs IPN differs. |
| API-VAL-071 | 75 | API-VAL-072 | Keep | Letter case vs whitespace trimming; 081 is a different field and rule. |
| API-VAL-072 | 75 | API-VAL-071 | Keep | Whitespace trimming vs letter case. |
| API-VAL-073 | 50 | API-VAL-076 | Keep | Name (R-Part-13) vs IPN under the setting (R-VAL-03). |
| API-VAL-076 | 50 | API-VAL-073 | Keep | IPN under the setting vs name. |
| API-VAL-078 | 52 | API-VAL-080 | Keep | Create vs PATCH; 081 is a case variant. |
| API-VAL-080 | 52 | API-VAL-078 | Keep | PATCH transition vs create. |
| API-VAL-081 | 51 | API-VAL-078 | Keep | Case variant (proposed accepted) vs exact duplicate (rejected). |
| API-VAL-082 | 79 | API-VAL-084 | Keep | Set parent vs top level (`parent` null). |
| API-VAL-084 | 79 | API-VAL-082 | Keep | Top level vs set parent. |
| API-VAL-085 | 59 | API-VAL-086 | Keep | Rename (`name`) vs move (`parent`). |
| API-VAL-086 | 59 | API-VAL-085 | Keep | Move (`parent`) vs rename (`name`). |
| API-REL-057 | 54 | API-REL-058 | Keep | Stock vs variant/revision dependents; inactive vs active (063). |
| API-REL-058 | 68 | API-REL-059 | Keep | Variant (`variant_of`) vs revision (`revision_of`). |
| API-REL-059 | 68 | API-REL-058 | Keep | Revision vs variant. |
| API-REL-063 | 51 | API-REL-057 | Keep | Active vs inactive part with stock. |

## Questions for the architect

1. Q-CRUD-02 (and Q-CRUD-01, -03) have an Answer filled but Status still `Open`; the REL cases and the index (line 85) treat them as answered. Confirm and set the Status.
2. API-VAL-069 proposes that a second part with the same name and a different IPN is accepted, against the literal R-Part-13 ("unique"). F-04 only shows same name + same IPN + different revision in the demo data. Settling Doc issue 2 / Q-VAL-08 decides whether 069 stays Positive.
3. API-REL-057 step 1 and API-REL-063 step 2 state `total_in_stock` `10` as fact from `initial_stock` (R-CRUD-13). Doc issue 8 lists a *Create Initial Stock* setting with no name or default; is the API `initial_stock` gated by it? If so, both cases need a Settings entry.
4. API-VAL-078 to 081 and API-REL-059 create several parts with an empty IPN; if Q-VAL-09 is answered "empty IPNs count as duplicates when duplicates are not allowed", their setup depends on the duplicate-IPN setting too.
