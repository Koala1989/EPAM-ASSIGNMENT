# Requirements inventory: REV (revisions)

Rules stated in `requirements/docs/` (InvenTree 1.5.6). Built by P03 on 2026-10-10; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare. Risk values are the agent's proposal.

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-REV-01 | A revision is itself a part, with its own part number, stock, parameters and BOM, linked to the original part. | [part-revision.md#L23](../../requirements/docs/part-revision.md#L23) | H | |
| R-REV-02 | Creating a revision does not affect data that refers to the original part (stock items, build orders, purchase orders). | [part-revision.md#L19](../../requirements/docs/part-revision.md#L19) | H | |
| R-REV-03 | The Revision field is user-defined and can be any string. | [part-revision.md#L29](../../requirements/docs/part-revision.md#L29) | M | Max length not stated. |
| R-REV-04 | The Revision Of field references the part this part is a revision of. | [part-revision.md#L30](../../requirements/docs/part-revision.md#L30) | M | |
| R-REV-05 | The Revision field is optional on a part. | [part-views.md#L36](../../requirements/docs/part-views.md#L36) | M | |
| R-REV-06 | A part cannot be a revision of itself (circular reference). | [part-revision.md#L36](../../requirements/docs/part-revision.md#L36) | H | Error text not stated. |
| R-REV-07 | Two revisions of the same part cannot have the same revision code. | [part-revision.md#L37](../../requirements/docs/part-revision.md#L37) | H | Case sensitivity of the comparison not stated. |
| R-REV-08 | A template part cannot have revisions. | [part-revision.md#L38](../../requirements/docs/part-revision.md#L38) | H | In 1.5.6 the UI enforces this by not offering template parts in the *Revision Of* field; the API rejects it: "Cannot make a revision of a template part" (checked 2026-10-11). |
| R-REV-09 | A variant part can have revisions. | [part-revision.md#L38](../../requirements/docs/part-revision.md#L38) | H | |
| R-REV-10 | A revision of a variant part must point to the same template as the original part. | [part-revision.md#L39](../../requirements/docs/part-revision.md#L39) | H | |
| R-REV-11 | Revisions are controlled by the global settings `PART_ENABLE_REVISION` and `PART_REVISION_ASSEMBLY_ONLY`. | [part-revision.md#L43-48](../../requirements/docs/part-revision.md#L43-L48) | H | Descriptions and defaults are an unrendered macro in the snapshot (index, doc issue 8). |
| R-REV-12 | A revision is created from the part actions menu, *Duplicate Part*: set *Revision Of* to the original and *Revision* to a unique code, then Submit. | [part-revision.md#L53-64](../../requirements/docs/part-revision.md#L53-L64) | H | |
| R-REV-13 | After a successful submit, the user is redirected to the new revision, which shows its link to the original part. | [part-revision.md#L66](../../requirements/docs/part-revision.md#L66) | M | |
| R-REV-14 | When several revisions exist, the *Select Part Revision* drop-down at the top of the part page navigates between them. | [part-revision.md#L72](../../requirements/docs/part-revision.md#L72) | M | |
| R-REV-15 | The revision selector is visible only when multiple revisions exist. | [part-revision.md#L77](../../requirements/docs/part-revision.md#L77) | M | |

## Cross-references

| Rule | Primary |
|---|---|
| Parameters with a unique template are skipped when duplicating a part | R-Part_Params-18 |
