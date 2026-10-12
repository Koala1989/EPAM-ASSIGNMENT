# Requirements inventory: Unit_measure (units of measure)

Rules stated in `requirements/docs/` (InvenTree 1.5.6). Built by P03 on 2026-10-10; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare. Risk values are the agent's proposal.

## Part units

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Unit_measure-01 | Each part can define a unit of measure used to track its quantities. | [part-index.md#L120](../../requirements/docs/part-index.md#L120) | H | |
| R-Unit_measure-02 | By default a part's unit of measure is blank, meaning dimensionless "pieces". | [part-index.md#L120](../../requirements/docs/part-index.md#L120) | M | Conflicts with part-views.md#L44, "The default is 'pcs'" (index, doc issue 1). |
| R-Unit_measure-03 | Parts can be tracked in physical units such as metres or litres. | [part-index.md#L127](../../requirements/docs/part-index.md#L127) | M | |
| R-Unit_measure-04 | A supplier part's unit defaults to its base part's unit and can be changed to any compatible unit. | [part-index.md#L133](../../requirements/docs/part-index.md#L133) | H | Example: base `metres` allows `feet`, `cm`, `inches`. |
| R-Unit_measure-05 | An incompatible supplier part unit shows an error. | [part-index.md#L138](../../requirements/docs/part-index.md#L138) | H | Error text not stated. |

## Unit input and conversion

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Unit_measure-06 | Values convert between compatible units (mass, length). | [concepts-units.md#L24](../../requirements/docs/concepts-units.md#L24) | M | |
| R-Unit_measure-07 | Engineering notation is valid: `10k3` = 10,300, `10M3` = 10,000,000, `3n02` = 0.00000000302. | [concepts-units.md#L28-32](../../requirements/docs/concepts-units.md#L28-L32) | M | |
| R-Unit_measure-08 | Scientific notation is valid: `1E-3` = 0.001, `1E3` = 1000, `-123.45E-3` = -0.12345. | [concepts-units.md#L36-40](../../requirements/docs/concepts-units.md#L36-L40) | M | |
| R-Unit_measure-09 | Scientific notation is case-sensitive: `1E3` is valid, `1e3` is not. | [concepts-units.md#L43](../../requirements/docs/concepts-units.md#L43) | M | Negative case. |
| R-Unit_measure-10 | Feet and inches shorthand is valid (`3'`, `6"`); compound values like `3'6"` are not supported. | [concepts-units.md#L49-52](../../requirements/docs/concepts-units.md#L49-L52) | M | |
| R-Unit_measure-11 | Units are case-sensitive: `kg` is valid, `KG` is not. | [concepts-units.md#L56](../../requirements/docs/concepts-units.md#L56) | H | |

## Custom units

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Unit_measure-12 | Built-in custom units: `piece`, `each` (one item), `dozen` (12), `hundred` (100), `thousand` (1000), all dimensionless. | [concepts-units.md#L87-93](../../requirements/docs/concepts-units.md#L87-L93) | M | |
| R-Unit_measure-13 | Custom units are viewed, edited and created in the *Physical Units* tab of the settings panel. | [concepts-units.md#L97](../../requirements/docs/concepts-units.md#L97) | M | Required permission not stated. |
| R-Unit_measure-14 | A custom unit can define a new quantity, link existing units, or alias an existing unit. | [concepts-units.md#L78](../../requirements/docs/concepts-units.md#L78) | L | |
| R-Unit_measure-15 | A custom dimensionless unit must have the literal `1` as its definition. | [concepts-units.md#L104](../../requirements/docs/concepts-units.md#L104) | M | |

## BOM quantities

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Unit_measure-16 | A BOM line's raw amount can be given in any unit compatible with the part's unit; quantity is calculated from it automatically. | [manufacturing-bom.md#L29-30](../../requirements/docs/manufacturing-bom.md#L29-L30), [#L41-43](../../requirements/docs/manufacturing-bom.md#L41-L43) | H | Example: part in `kg`, raw amount in `g`, `mg`, `lb`. |
| R-Unit_measure-17 | If the part has no unit of measure, the raw amount cannot include units. | [manufacturing-bom.md#L45](../../requirements/docs/manufacturing-bom.md#L45) | H | |
| R-Unit_measure-18 | The raw amount accepts fractions: `500 g`, `0.5 kg` and `1/2 kg` all give 0.5 kg. | [manufacturing-bom.md#L49](../../requirements/docs/manufacturing-bom.md#L49) | M | |

## Cross-references

| Rule | Primary |
|---|---|
| Parameter values must use units compatible with the template | R-Part_Params-05, R-Part_Params-30 to R-Part_Params-33 |
| Unit-aware parametric filtering | R-Part_Params-27 |
