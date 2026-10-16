# Review: Part attributes (UI), 2026-10-13

**Cases reviewed:** UI-ATT-001 to UI-ATT-070 (all 70, `test-cases/Attributes/part-attributes.md`) · **Verdict:** Changes required

## Coverage

`python tools/coverage_check.py --area ATT --area Detail_View --file test-cases/Attributes/part-attributes.md`: Rules: 99 · covered: 36 · not cited by any case: 63 (exit 0, no unknown rule IDs). All 29 ATT rules are cited. The 63 uncited rules are all Detail_View.

| Rule | Cases | Status | Depth issues |
|---|---|---|---|
| R-ATT-01 | 001-004 | Covered | None |
| R-ATT-02 | 005, 006 | Covered | 005 uses `engineer`, who only views stock, so the negative passes whether or not Virtual blocks it (F2) |
| R-ATT-03 | 007 | Covered | Transfer Orders check passes even if the part is not Virtual unless the transfer order feature is on (F3); other elements open (Q-ATT-08) |
| R-ATT-04 | 008 | Covered | None |
| R-ATT-05 | 009, (011) | Covered | None |
| R-ATT-06 | 010, 011 | Covered | None |
| R-ATT-07 | 012 | Covered | None |
| R-ATT-08 | 013, 014 | Covered | 014 is the same check as 002 (F10) |
| R-ATT-09 | 017 | Covered | Open (Q-ATT-10) |
| R-ATT-10 | 013, 015, 016 | Covered | Negative open (Q-ATT-05) |
| R-ATT-11 | 018, 019, 020 | Covered | None |
| R-ATT-12 | 021, 022, 035 | Covered | Wrong user (F2); nothing says whether a non-Trackable part can take serial numbers (question 4) |
| R-ATT-13 | 039 | Covered | Open (Q-ATT-04); wrong user (F2) |
| R-ATT-14 | 022-029, 034-038 | Covered | Every input-format row has a case; boundaries at length 1 and 0; five invalid classes. Wrong user (F2) |
| R-ATT-15 | 030-033 | Covered | Wrong user (F2) |
| R-ATT-16 | 040 | Covered | None |
| R-ATT-17 | 041 | Covered | Only the "assembly not Trackable" column; the "Trackable assembly + tracked BOM line" column of "regardless" is missing (F13) |
| R-ATT-18 | 042-045, 069 | Covered | The supplier-part half of the negative (Q-ATT-06) has no case (F14) |
| R-ATT-19 | 046, 047 | Covered | None |
| R-ATT-20 | 048 | Covered | Wrong user (F2) |
| R-ATT-21 | 049 | Covered | None |
| R-ATT-22 | 050, 051 | Covered | None |
| R-ATT-23 | 052, 053, 054 | Covered | Not marked with Q-ATT-15 (F4) |
| R-ATT-24 | 055, 062, (065) | Covered | Negative 055 and override 062 are present |
| R-ATT-25 | 056, 057, 058, 063, 065 | Covered | Create, edit and delete each have a negative |
| R-ATT-26 | 059, 060, 061, 064 | Covered | Create, edit and delete each have a negative |
| R-ATT-27 | 062, 063, 064 | Covered | Override covered for delete, BOM create and parameter create only; edit and delete of BOM lines or parameters with locking off are not covered (acceptable reduction, architect's call) |
| R-ATT-28 | 066, (070) | Covered | None |
| R-ATT-29 | 067-070 | Covered | Open (Q-ATT-03); 070 data defect (F1) |
| R-Detail_View-17, -19, -21, -23, -24, -27, -30 | 001-004, 007, 014, 020, 044, 046 | Covered (cross-reference) | None beyond F3 |
| R-Detail_View-26 (Return Orders tab, Salable + feature) | none | Out of scope | Detail_View is the primary Area; the ATT cross-reference lists it, so check it is covered there |
| R-Detail_View-01 to -16, -18, -20, -22, -25, -28, -29, -31 to -70 | none | Out of scope | Detail_View functionality (detail view tabs, stock tab, tests, attachments, BOM) |

No permission rules in ATT, so no blocked-user cases are needed. The lock and unlock permission is part of Q-ATT-01.

## Findings

| # | Severity | Case or rule | Check | Problem | Evidence (rule, doc or schema line) | Suggested action |
|---|---|---|---|---|---|---|
| F1 | Blocker | UI-ATT-070 | No assumptions | Data creates `QA-<suffix> Reactivate` with Active off but does not set *Component* on. Step 2 then expects the BOM line to save "without error". Whether a non-Component part can be added to a BOM is Open (Q-ATT-05), and the schema gives no default for `component`. Every other case that adds a BOM line sets Component on (009, 013, 049, 063, 065, 068). | R-ATT-10; Q-ATT-05; `openapi-parts.yaml#L4128-4130` (no default) | Edit the case: set Component on in Data |
| F2 | Blocker (005, 034-039) / Major (021-033, 048) | UI-ATT-005, 021-039, 048 | User | These cases create stock items as `engineer`, but `engineer` has "Manage parts, view stock". The seed worked example says the same ("manage parts, view stock"), and so does `users.local.json`. The negative cases (005, 034-039) would pass because of the missing stock permission, not because of the rule. The positive cases (021-033, 048) would fail for the same reason. Their Prerequisites also misstate the role as "(manage parts, stock)". | Seed worked example L55, demo users table; `automation/shared/data/users.local.json` L4 | Edit the cases: use a user that can create stock (`allaccess`), or confirm `engineer`'s stock permissions |
| F3 | Major | UI-ATT-007 | Fidelity | R-Detail_View-27 hides the *Transfer Orders* tab if the part is Virtual **or** the transfer order feature is off. With Settings: None, the tab may be hidden for every part, so the case passes without testing Virtual. | [part-views.md#L122](../../requirements/docs/part-views.md#L122); index doc issue 8 (feature setting not named) | Edit the case: set the transfer order feature on (setting name is open), and add a non-Virtual control, or raise an open question |
| F4 | Major | UI-ATT-052, 053, 054 | Open-question marking | They check "not allocated" on a Build Order the same way as UI-ATT-050, which is marked Q-ATT-15 (how a Build Order shows a Consumable part). These three are plain `Draft`, and Q-ATT-15 lists only 050. | Q-ATT-15; [part-consumable.md#L48-L63](../../requirements/docs/part-consumable.md#L48-L63) | Edit the cases: mark Q-ATT-15 and add "Not known" to the allocation Expected results; add the cases to Q-ATT-15's Affected cases |
| F5 | Minor | UI-ATT-025, 032, 033 | Open-question marking | The "next serial" value (8, 14) depends on how `~` is determined. That is marked `[open: Q-ATT-09]` in Prerequisites, but step 3 states `8` / `14, 15, 16` / `14, 15` as fact. | [part-trackable.md#L34](../../requirements/docs/part-trackable.md#L34), [#L41-42](../../requirements/docs/part-trackable.md#L41-L42); Q-ATT-09 | Edit step 3 to depend on the next-serial answer |
| F6 | Minor | UI-ATT-051 | No assumptions | Expected "The Build Order status is Complete": the status label is not in the cited sources (Build Orders docs are outside the snapshot). | [part-consumable.md#L48](../../requirements/docs/part-consumable.md#L48) | Reword to "the build is completed", or mark as open |
| F7 | Minor | UI-ATT-011, 051 | Seed format | Prerequisites Data says "as the Virtual build case above" / "as the previous case": not self-contained. | Seed: Prerequisites must name the records and how they are created | Edit: list the records |
| F8 | Minor | UI-ATT-065, 070 | Requirement | 065 cites R-ATT-24 (locked part cannot be deleted) but tests only BOM editing after unlock. 070 cites R-ATT-28 (active by default) but tests reactivation. | R-ATT-24, R-ATT-28 | Edit: drop the extra rule IDs |
| F9 | Minor | UI-ATT-046 | One behaviour | Step 1 tests R-ATT-19 (add to sales order). Step 2 tests R-Detail_View-17 (*Allocated* tab visible for Salable), which does not depend on step 1 and is already in UI-ATT-003. | R-ATT-19; R-Detail_View-17 | Architect's call: drop step 2 or split |
| F10 | Minor | UI-ATT-014 vs UI-ATT-002 | Duplicate (below 50, no score line) | 014 (Assembly off, Component on; BOM tab not visible) is the same starting state and the same assertion as part of 002. | R-Detail_View-19 | Architect's call: remove 014 or keep it as a single-factor check |
| F11 | Minor | UI-ATT-005 | Fidelity | Step 3 checks stock on the Virtual part's detail page, where R-ATT-03 says stock UI elements are hidden, so the step may not be executable. | [part-virtual.md#L27](../../requirements/docs/part-virtual.md#L27) | Edit: check via the global stock list filtered by the part |
| F12 | Minor | UI-ATT-056, 059 | Specific test data | Step 2 gives a quantity (`3`) or value (`7`) but no sub-component or parameter template, although the data creates them. | Seed: exact values entered | Edit: add `QA-<suffix> Component Lock` / `QA-<suffix> Param` |
| F13 | Minor | R-ATT-17 / UI-ATT-041 | Depth | "Regardless of whether the assembled part itself is trackable": only the non-Trackable assembly column is tested. | [part-trackable.md#L56](../../requirements/docs/part-trackable.md#L56) | Rerun the creator for the Trackable-assembly column if wanted |
| F14 | Minor | R-ATT-18 / Q-ATT-06 | Depth | Q-ATT-06 asks about supplier parts **and** purchase orders for a non-Purchaseable part. Only the purchase-order half has a case (045). | Q-ATT-06 | Rerun the creator for a supplier-part case on a non-Purchaseable part |
| F15 | Minor | UI-ATT-062, 063, 064 | Seed format | Prerequisites say `PART_ENABLE_LOCKING` = off, but step 1 is the action that turns it off. The starting state should be "on". | R-ATT-27 | Edit Prerequisites |
| F16 | Minor | UI-ATT-055 | User | `admin` is used, but the setting is set up in Prerequisites; the action under test (lock, delete) may not need a superuser. Lock permission is part of Q-ATT-01. | Seed: least-privileged user | Revisit after Q-ATT-01 |
| F17 | Minor | UI-ATT-042, 067, 070 | Seed format | Automation `Partial.` with no reason. | Seed: "with a reason if not Yes" | Edit |
| F18 | Minor | UI-ATT-048 | Open-question marking | Automation says "form labels not known" but Review is `Draft` with no question. Either the labels are known (R-Detail_View-11 *New Stock Item*) or a question applies. | R-Detail_View-11 | Edit Automation text |
| F19 | Minor | UI-ATT-001, 027 | Technique | 001: "(Assembly on, Component on off)" is a typo. 027: "Boundary value analysis (length 2)": length 2 is the documented example, not a boundary. | — | Edit labels |
| F20 | Minor | Several (006, 015, 029, 034-038, 045, 047, 068, 069) | Seed format | Summary names the input or situation but not what is verified (for example "`2+0` (length 0)."). Technique values are `;`-separated where the seed says comma-separated (whole file). | Seed Summary and Technique fields | Edit wording |

## Duplicates

| Case | Score | Closest match | Verdict | Reason |
|---|---|---|---|---|
| UI-ATT-001 | 78 | UI-ATT-002 | Keep | Different decision-table column and opposite tab outcome |
| UI-ATT-002 | 78 | UI-ATT-001 | Keep | Different decision-table column and opposite tab outcome |
| UI-ATT-003 | 62 | UI-ATT-004 | Keep | All on vs all off; opposite outcome |
| UI-ATT-004 | 62 | UI-ATT-003 | Keep | All off vs all on; opposite outcome |
| UI-ATT-022 | 72 | UI-ATT-025 | Keep | Single SN vs next SN row; different starting state |
| UI-ATT-023 | 81 | UI-ATT-024 | Keep | List vs range row |
| UI-ATT-024 | 81 | UI-ATT-023 | Keep | Range vs list row |
| UI-ATT-025 | 72 | UI-ATT-022 | Keep | Next SN with existing serial vs literal single |
| UI-ATT-026 | 78 | UI-ATT-027 | Keep | `<start>+` (count from quantity) vs `<start>+<length>` |
| UI-ATT-027 | 78 | UI-ATT-026 | Keep | `<start>+<length>` vs `<start>+` |
| UI-ATT-028 | 69 | UI-ATT-027 | Keep | Length-1 boundary vs documented length 2 |
| UI-ATT-030 | 95 | UI-ATT-031 | Keep | Whitespace vs comma separator: separate clauses of R-ATT-15 |
| UI-ATT-031 | 95 | UI-ATT-030 | Keep | Comma vs whitespace separator |
| UI-ATT-032 | 86 | UI-ATT-033 | Keep | `~+2` explicit length vs `~+` count from quantity |
| UI-ATT-033 | 86 | UI-ATT-032 | Keep | `~+` vs `~+2` |
| UI-ATT-034 | 83 | UI-ATT-038 | Keep | Repeated serial vs count mismatch (different invalid class) |
| UI-ATT-035 | 63 | UI-ATT-034 | Keep | Existing serial in the database (starting state) |
| UI-ATT-036 | 80 | UI-ATT-034 | Keep | Reversed range class |
| UI-ATT-037 | 82 | UI-ATT-034 | Keep | Non-numeric class |
| UI-ATT-038 | 83 | UI-ATT-034 | Keep | Count-mismatch class |
| UI-ATT-045 | 55 | UI-ATT-069 | Keep | R-ATT-18 non-Purchaseable vs R-ATT-29 inactive |
| UI-ATT-047 | 52 | UI-ATT-045 | Keep | Salable/sales order vs Purchaseable/purchase order |
| UI-ATT-052 | 55 | UI-ATT-053 | Keep | Part-level flag vs BOM-line flag; different outcome in build Y |
| UI-ATT-053 | 55 | UI-ATT-052 | Keep | BOM-line flag vs part-level flag |
| UI-ATT-056 | 88 | UI-ATT-057 | Keep | Create vs edit clause of R-ATT-25 |
| UI-ATT-057 | 88 | UI-ATT-056 | Keep | Edit vs create clause |
| UI-ATT-058 | 80 | UI-ATT-057 | Keep | Delete vs edit clause |
| UI-ATT-059 | 87 | UI-ATT-060 | Keep | Create vs edit clause of R-ATT-26 |
| UI-ATT-060 | 87 | UI-ATT-059 | Keep | Edit vs create clause |
| UI-ATT-061 | 78 | UI-ATT-059 | Keep | Delete vs create/edit clause |
| UI-ATT-063 | 50 | UI-ATT-064 | Keep | BOM (R-ATT-25) vs parameter (R-ATT-26) override |
| UI-ATT-064 | 50 | UI-ATT-063 | Keep | Parameter vs BOM override |
| UI-ATT-069 | 55 | UI-ATT-045 | Keep | Inactive (R-ATT-29) vs non-Purchaseable (R-ATT-18) |

## Questions for the architect

1. **Locked means "cannot be modified"?** The docs say parts are locked "to prevent them from being modified" ([part-index.md#L106](../../requirements/docs/part-index.md#L106)), and the schema describes `locked` as "Locked parts cannot be edited" (`openapi-parts.yaml#L4185-4187`). The inventory only has delete, BOM and parameter restrictions (R-ATT-24 to R-ATT-26). Should editing a locked part's own fields be a rule (and a case)?
2. **Locking through the API:** UI-ATT-062 to UI-ATT-065 mark "how the part is locked through the API" as `[open: Q-ATT-01]`. The schema has a `locked` boolean on `Part`. Does that settle the setup part of Q-ATT-01? The UI lock control would stay open.
3. **Engineer's stock permissions (F2):** please confirm whether `engineer` can create stock items in the test instance. The seed and users file say "view stock".
4. **Serial numbers on a non-Trackable part:** R-ATT-12 says Trackable parts *can* have serial numbers. The docs do not say whether a non-Trackable part is blocked. Should this be an open question with a negative case?
5. **Inactive parts and deletion (UI-ATT-055 Notes):** the note "the part must be inactive before it can be deleted" is not in the ATT sources. It is presumably from Q-CRUD-02 (API_CRUD). Is it acceptable as a cross-Area fact in a UI case?
6. **UI-ATT-066 "required field only: Name":** the docs do not say which Create Part fields are required (index Not in docs 9). Is this settled by the Part Area cases or findings?
