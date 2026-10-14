# Requirements inventory: Part_Template (templates and variants)

Rules stated in `requirements/docs/` (InvenTree 1.5.6). Built by P03 on 2026-10-10; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare. Risk values are the agent's proposal.

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part_Template-01 | Any part can be set as a Template part. | [part-template.md#L32](../../requirements/docs/part-template.md#L32) | H | |
| R-Part_Template-02 | The Template option is toggled on the part detail page (*Details* tab, part options). | [part-template.md#L34-37](../../requirements/docs/part-template.md#L34-L37) | M | The described UI path may not match 1.5.6 (index, doc issue 9). |
| R-Part_Template-03 | Variants can be created only once the Template option is on. | [part-template.md#L41](../../requirements/docs/part-template.md#L41) | H | |
| R-Part_Template-04 | A variant is created from the *Variants* tab, *New Variant*, which opens the *Duplicate Part* form; Submit creates it. | [part-template.md#L43-44](../../requirements/docs/part-template.md#L43-L44) | H | |
| R-Part_Template-05 | A variant references its template part. | [part-template.md#L20](../../requirements/docs/part-template.md#L20) | M | |
| R-Part_Template-06 | Serial numbers must be unique across a template and all its variants. | [part-template.md#L24](../../requirements/docs/part-template.md#L24) | H | |
| R-Part_Template-07 | A template part's stock includes the stock of all its variants. | [part-template.md#L26](../../requirements/docs/part-template.md#L26) | H | |
| R-Part_Template-08 | Test templates of a master part cascade to its variants and their stock items. | [part-test.md#L19](../../requirements/docs/part-test.md#L19) | M | |
| R-Part_Template-09 | An Inherited BOM line is included automatically in the BOM of every variant and sub-variant. | [manufacturing-bom.md#L35](../../requirements/docs/manufacturing-bom.md#L35), [#L80](../../requirements/docs/manufacturing-bom.md#L80) | H | Worked example at L88-107. |
| R-Part_Template-10 | Inherited BOM lines flow downwards only: a part cannot inherit BOM lines from its variants. | [manufacturing-bom.md#L113](../../requirements/docs/manufacturing-bom.md#L113) | H | |
| R-Part_Template-11 | Editing an inherited BOM line on the template updates it in the variants' BOMs. | [manufacturing-bom.md#L116](../../requirements/docs/manufacturing-bom.md#L116) | M | |

## Cross-references

| Rule | Primary |
|---|---|
| A template part cannot have revisions; variants can | R-REV-08, R-REV-09 |
| A revision of a variant must point to the same template | R-REV-10 |
| *Variants* tab is visible only for a Template part | R-Detail_View-08 |
| Test name uniqueness across a set of variants | R-Detail_View-31 |
