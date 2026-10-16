# Requirements inventory: XF (cross-functional scenarios)

End-to-end flows that chain rules from several Areas on the same records. Drafted on 2026-10-15 at the architect's request; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare.

These are not new requirements. Each flow composes reviewed rules from the other Areas' inventories, listed in **Composed of**, and states nothing those rules do not. The doc line for each part is in that rule's own inventory row. A case for a flow cites the flow's `R-XF-NN` and every composed rule it asserts, and reuses the composed Areas' open questions (an Open question there still affects the case here).

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-XF-01 | A part created from the *Parts* view, given a parameter on its *Parameters* tab and a stock item on its *Stock* tab, shows that stock level in its category's part list and that parameter value in the category's parametric view. | Composed of: R-Part-02, R-Part-04, R-Part-06, R-Part_Params-02, R-Part_Params-12, R-Detail_View-11, R-Detail_View-09, R-Detail_View-13, R-Categories-04, R-Categories-06, R-Categories-07, R-Part_Params-21 | H | The brief's example flow. |
| R-XF-02 | A parameter template linked to a category with a default value is applied to a new part created in a sub-category of it; the part, with that parameter, is listed in the parent category's part list and parametric view. | Composed of: R-Part_Params-19, R-Part_Params-20, R-Part-01, R-Part-06, R-Part_Params-02, R-Categories-02, R-Part_Params-21 | H | Use a template without a uniqueness requirement (R-Part_Params-20). |
| R-XF-03 | A part switched to Template gets a variant from its *Variants* tab; stock created on the variant counts in the template part's stock. | Composed of: R-Part_Template-01, R-Part_Template-02, R-Part_Template-03, R-Part_Template-04, R-Part_Template-05, R-Detail_View-08, R-Detail_View-11, R-Detail_View-13, R-Part_Template-07 | H | |
| R-XF-04 | A revision created with *Duplicate Part* from a part that has stock is a separate part linked to the original; the original's stock items are unchanged, and the revision selector moves between the two. | Composed of: R-REV-01, R-REV-02, R-REV-11, R-REV-12, R-REV-13, R-REV-14, R-REV-15, R-Detail_View-09, R-Detail_View-13 | H | Settings-dependent: `PART_ENABLE_REVISION`, `PART_REVISION_ASSEMBLY_ONLY`. |
| R-XF-05 | A Component part with a unit of measure, added to an Assembly's BOM with a raw amount in a compatible unit, gets a converted quantity on the BOM line, lists the assembly on its *Used In* tab, and the change leaves the BOM not validated. | Composed of: R-ATT-08, R-ATT-10, R-Unit_measure-01, R-Unit_measure-03, R-Unit_measure-06, R-Unit_measure-16, R-Detail_View-19, R-Detail_View-62, R-Detail_View-21, R-Detail_View-65, R-Detail_View-67 | H | |
| R-XF-06 | Once a part with a parameter and a BOM line is locked, its parameters and BOM lines cannot be created, edited or deleted and the part cannot be deleted; with `PART_ENABLE_LOCKING` disabled, the same operations are permitted. | Composed of: R-ATT-24, R-ATT-25, R-ATT-26, R-ATT-27, R-Part_Params-12, R-Detail_View-59, R-Detail_View-62 | H | Settings-dependent: `PART_ENABLE_LOCKING`. |
| R-XF-07 | A Virtual part has no stock items and its page hides stock elements, yet it is listed in its category's part list and can be added as a line in an Assembly's BOM. | Composed of: R-ATT-02, R-ATT-03, R-ATT-04, R-ATT-05, R-Categories-04, R-Detail_View-62 | M | |

## Cross-references

| Rule | Primary |
|---|---|
| Every composed rule above | Its own Area's inventory (Part, Detail_View, Categories, ATT, Unit_measure, REV, Part_Params, Part_Template) |
