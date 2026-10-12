# Requirements inventory: Part_Params (parameters)

Rules stated in `requirements/docs/` (InvenTree 1.5.6). Built by P03 on 2026-10-10; **pending architect review**. Risk: H core flow or data integrity, M important behaviour, L informational or rare. Risk values are the agent's proposal.

## Parameters on a part

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part_Params-01 | Parameters are metadata only and are not used in core business logic. | [concepts-parameters.md#L18](../../requirements/docs/concepts-parameters.md#L18) | L | |
| R-Part_Params-02 | The part detail page has a *Parameters* tab listing all the part's parameters. | [concepts-parameters.md#L24](../../requirements/docs/concepts-parameters.md#L24), [part-views.md#L148](../../requirements/docs/part-views.md#L148) | M | |
| R-Part_Params-12 | A parameter is added from the *Parameters* tab, *New Parameters*: choose a Template, enter Data, Submit. | [concepts-parameters.md#L65-69](../../requirements/docs/concepts-parameters.md#L65-L69) | H | |

## Parameter templates

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part_Params-03 | A parameter template name must be unique. | [concepts-parameters.md#L34](../../requirements/docs/concepts-parameters.md#L34) | H | Case sensitivity not stated. |
| R-Part_Params-04 | A template's description is optional. | [concepts-parameters.md#L35](../../requirements/docs/concepts-parameters.md#L35) | L | |
| R-Part_Params-05 | A template's units are optional, but must be a valid physical unit if given. | [concepts-parameters.md#L36](../../requirements/docs/concepts-parameters.md#L36) | H | |
| R-Part_Params-06 | A template with a blank Model Type can be used for any model. | [concepts-parameters.md#L37](../../requirements/docs/concepts-parameters.md#L37) | M | |
| R-Part_Params-07 | Choices is a comma-separated list of the valid values for parameters of that template. | [concepts-parameters.md#L38](../../requirements/docs/concepts-parameters.md#L38) | H | Behaviour for a value not in the list is not stated. |
| R-Part_Params-08 | With Checkbox set, parameter values can only be true or false. | [concepts-parameters.md#L39](../../requirements/docs/concepts-parameters.md#L39) | H | |
| R-Part_Params-09 | With a Selection List set, values can only come from that list. | [concepts-parameters.md#L40](../../requirements/docs/concepts-parameters.md#L40) | H | |
| R-Part_Params-10 | Templates are created in the Admin Center: *Parameters* tab, *New Parameter*, form with Name (required) and Units (optional), Submit. | [concepts-parameters.md#L47-55](../../requirements/docs/concepts-parameters.md#L47-L55) | M | L47 says Admin Center, L51 says the "Settings" page (index, doc issue 5). |
| R-Part_Params-11 | An existing template is edited with its *Edit* button. | [concepts-parameters.md#L57](../../requirements/docs/concepts-parameters.md#L57) | M | |
| R-Part_Params-34 | Template choices are limited to 5000 characters; selection lists overcome this. | [concepts-parameters.md#L197](../../requirements/docs/concepts-parameters.md#L197) | M | Boundary: 5000 and 5001 characters. |
| R-Part_Params-35 | Plugins can lock selection lists. | [concepts-parameters.md#L199](../../requirements/docs/concepts-parameters.md#L199) | L | |
| R-Part_Params-36 | Selection lists are managed in the Admin Center *Parameter* section or via the API. | [concepts-parameters.md#L202](../../requirements/docs/concepts-parameters.md#L202) | L | |

## Uniqueness

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part_Params-13 | A template's Unique option is one of: no uniqueness (default), unique for model type, globally unique. | [concepts-parameters.md#L77-81](../../requirements/docs/concepts-parameters.md#L77-L81) | H | |
| R-Part_Params-14 | Uniqueness checks are case-insensitive (`ABC123` duplicates `abc123`). | [concepts-parameters.md#L84](../../requirements/docs/concepts-parameters.md#L84) | H | |
| R-Part_Params-15 | A value that breaks its template's uniqueness rule is rejected with an error. | [concepts-parameters.md#L86](../../requirements/docs/concepts-parameters.md#L86) | H | Error text not stated. |
| R-Part_Params-16 | For a template with units, uniqueness compares the normalised numeric value (`1k` duplicates `1000` ohm). | [concepts-parameters.md#L90-92](../../requirements/docs/concepts-parameters.md#L90-L92) | H | |
| R-Part_Params-17 | For a template without units, uniqueness compares the raw text, case-insensitively. | [concepts-parameters.md#L94](../../requirements/docs/concepts-parameters.md#L94) | M | |
| R-Part_Params-18 | When parameters are copied (e.g. duplicating a part), parameters of unique templates are skipped. | [concepts-parameters.md#L98-100](../../requirements/docs/concepts-parameters.md#L98-L100) | M | |

## Category parameters

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part_Params-19 | A template can be linked to a category with a default value, applied to new parts created in that category or its sub-categories. | [concepts-parameters.md#L104](../../requirements/docs/concepts-parameters.md#L104) | H | |
| R-Part_Params-20 | The category default is not applied for a template with a uniqueness requirement. | [concepts-parameters.md#L108](../../requirements/docs/concepts-parameters.md#L108) | M | |

## Parametric tables

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part_Params-21 | Tables that support parametric filtering and sorting have a *Parametric View* button. | [concepts-parameters.md#L112-114](../../requirements/docs/concepts-parameters.md#L112-L114) | M | |
| R-Part_Params-22 | Clicking a parameter column header sorts parts by that parameter. | [concepts-parameters.md#L120](../../requirements/docs/concepts-parameters.md#L120) | M | |
| R-Part_Params-23 | Parts can be filtered by a parameter value; the filter options depend on the parameter type (choices, numeric with operator). | [concepts-parameters.md#L126-130](../../requirements/docs/concepts-parameters.md#L126-L130) | M | |
| R-Part_Params-24 | With filters on several parameters, only parts matching all filters are shown. | [concepts-parameters.md#L134](../../requirements/docs/concepts-parameters.md#L134) | H | |
| R-Part_Params-25 | Each parameter column shows whether a filter is applied. | [concepts-parameters.md#L136](../../requirements/docs/concepts-parameters.md#L136) | L | |
| R-Part_Params-26 | Several filters can be applied to the same parameter (e.g. greater than 10k and less than 100k). | [concepts-parameters.md#L142](../../requirements/docs/concepts-parameters.md#L142) | M | |
| R-Part_Params-27 | Filters on a parameter with units accept any compatible unit (`10k` = `10000`). | [concepts-parameters.md#L148-150](../../requirements/docs/concepts-parameters.md#L148-L150) | M | |
| R-Part_Params-28 | A filter is removed with its remove button. | [concepts-parameters.md#L156](../../requirements/docs/concepts-parameters.md#L156) | L | |
| R-Part_Params-29 | Filter operators: `=`, `>`, `>=`, `<`, `<=`, `!=`, `~` (contains, text). | [concepts-parameters.md#L164-170](../../requirements/docs/concepts-parameters.md#L164-L170) | M | |

## Parameter units

| Rule ID | Rule | Source | Risk | Notes |
|---|---|---|---|---|
| R-Part_Params-30 | Parameter values must use units compatible with the template's base unit, and are converted. | [concepts-parameters.md#L174-176](../../requirements/docs/concepts-parameters.md#L174-L176) | H | |
| R-Part_Params-31 | A value with units incompatible with the template is rejected. | [concepts-parameters.md#L183](../../requirements/docs/concepts-parameters.md#L183) | H | Error text not stated. |
| R-Part_Params-32 | Unit validation can be disabled so that any value is accepted. | [concepts-parameters.md#L187](../../requirements/docs/concepts-parameters.md#L187) | M | Setting name and default not stated. |
| R-Part_Params-33 | Sorting by a parameter accounts for unit conversion. | [concepts-parameters.md#L191](../../requirements/docs/concepts-parameters.md#L191) | M | |

## Cross-references

| Rule | Primary |
|---|---|
| Parameters of a locked part cannot be created, edited or deleted | R-ATT-26 |
| Unit syntax (notation, case sensitivity) | R-Unit_measure-07 to R-Unit_measure-11 |
