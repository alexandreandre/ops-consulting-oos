# Distributor A and B: delivery status

Checked 2026-11-10 against the shared working files and the sources available in the team Drive.
This is a handover for the team, not a client-ready diagnosis.

## Distributor B

- The shared v1 workbook has 7,562 clean rows, matching the source row count.
- Independent sums of ordered, shipped, unshipped and OOS cases each match the source; all four differences are zero.
- A positional row-by-row comparison also found zero differences for ordered, shipped, unshipped, pick-omit and OOS quantities. It does not validate the product mappings or the derived analysis.
- All 7,562 rows have blank current-month, lag-1 and lag-2 forecast fields. Do not interpret a missing extract as a zero forecast.
- The mapping status is matched on 7,366 rows, missing on 189 and ambiguous on 7. Keep the exceptions visible; do not guess a client SKU.
- An independent comparison with the first Master Data sheet reproduces the mapping status on all 7,562 rows and the client SKU on all uniquely matched rows. All 7,366 populated factors that have one unambiguous value per source item also match Master Data. This checks consistency with the supplied reference, not whether the reference is correct or current.
- The source and Planning files visible in the shared Drive were last modified on 2026-10-13. The separately announced 2026 forecast extract was not found among the three Planning files visible there. Confirm its location and whether newer sources should replace these versions.
- The 2026-11-04 analysis in `roadmap.md` reports 53 location × client SKU cells covering 80% of weighted in-scope OOS 9L. This is a descriptive result; forecast bias and causes remain unverified.
- Recalculation from the shared Clean sheet reproduces 415 cells with OOS and 53 cells covering 80.27% of the weighted in-scope OOS 9L. All December and January rows have weight 0.5; all other months have weight 1. This verifies the calculation conditional on the workbook's scope, SKU mappings and conversion factors; it does not independently validate those inputs.
- Scope status covers 6,526 included, 797 excluded and 239 review rows. Their OOS quantities are respectively 15,327.47, 5,896.17 and 177.67 physical cases. These counts describe the workbook's classification, not a decision to discard any row.
- The Action_List and Top_Cells sheets each contain the same 415 unique location × client SKU keys. Every action row has a suggested action and rationale, but all 415 bias fields say `incomplete`; none contains a numeric bias. Current and recommended buffer fields are empty. These action labels require business validation before delivery as recommendations.
- The three supply-constrained item matches and the 14 repeated source keys remain questions for the team or client; see `open_questions.md` questions 13 and 16.

## Distributor A

- Exploration and the shared workbook of blank-cell examples are available. The decision log says not to impute blank unshipped values and not to start cleaning until the client answers.
- An independent check of the source reproduces 1,032 rows with blank unshipped, known shipped and an ordered-minus-shipped gap greater than 0.05 case. Their gap totals 7,644.23 cases and all are reported at 100% fill. Another 76 rows have both shipped and unshipped blank. These observations do not establish the reason for the shortfall.
- Ask whether the shortfalls on the flagged rows represent missed, late or corrected shipments. The 1,032-row count uses a 0.05-case threshold; see `open_questions.md` question 4.

## Before delivery

1. Confirm the current template version and whether the shared B workbook is the latest approved working version.
2. Locate the 2026 forecast extract, establish availability for 2025, and agree how to handle uncovered months. The current file cannot establish forecast bias.
3. Resolve or explicitly report B's mapping and scope exceptions, and obtain the answer on A's blanks.
4. Validate any proposed actions against forecasts, lead times and buffer information before presenting them as causes or recommendations.

The local checks compare the specified quantities in source order. They do not certify the product mappings, formulas, template layout or business interpretation.

## Second pass, 2026-11-10

Done with the AI assistant on Alexandre's computer, after Lena's checks above. New checks are in the notebooks: Distributor A section 19, Distributor B sections 26 to 28. No rule was changed, no cleaning was started and no definition was chosen.

### Template v1.1

- The template file was not found on this computer, in the team data folder, or through the Drive connector. The only trace in the repository is the footer the B build script writes ("Template v1.1 rebuild"). The divergences below are as Lena reported them; check them against the template text. Team question 10.
- **Distributor A.** Lena reports that the template gives instructions for partly shipped rows and for the 76 rows where shipped and unshipped are both blank. The decision of 2026-10-23 says not to impute and to wait for the client. Both cannot apply. Until the team chooses, the decision log stands. What is at stake: 1,032 rows (7,644 cases) and 76 rows (980 cases). Reading them as misses moves January–August 2026 from 95.7% to 95.3%.
- **Distributor B duplicates.** Three statements disagree on the 14 repeated item-month keys (28 rows): the decision of 2026-10-23 sums them; the decision of 2026-11-04 keeps both rows, flagged, and cites the frozen template; Lena reads template v1.1 as asking to merge them. Two facts help decide. First, the workbook already has an empty `Removed_Dups` sheet, and the template's flag list separates `DUP_CHECK` (same product) from `DUP_CODE_DIFF_PRODUCT` (different product names); all 28 rows carry the second flag. Check whether the merge instruction covers that case. Second, merging changes only the Clean row count (7,562 to 7,548): both rows share the location, month and client SKU, so the cell totals, the Pareto, the repeat patterns and the action list do not change.

### Cases OOS or Cases Unshipped

- **Distributor B.** The two columns are equal on 7,495 of 7,562 rows. On the 67 rows with a pick omit, Cases OOS = Unshipped + Pick Omits (75.7 cases in all). On the weighted 9L ranking, the OOS Pareto has 53 cells and the Unshipped one 52, all 52 shared; every cell keeps its repeat pattern. The template's choice of Cases OOS changes nothing material.
- **Distributor A.** The columns differ by about 9,650 cases (Unshipped 73,303; OOS 63,654), mostly pick omits: here Unshipped = OOS + Pick Omits. That is the opposite convention to B. Ranked by source id, the 101 ids in the OOS Pareto all sit inside the 108 of the Unshipped Pareto. Neither column covers the blank-unshipped rows: Cases OOS is blank on all of them.
- Which column the client means by out-of-stock, and whether a pick omit counts, is client question 1. The data cannot settle it.

### Forecasts for Distributor B

- The three Planning files are the only ones in the team folder. None of them is a 2026 extract.
- The snapshot file holds exactly 500,000 data rows. Every snapshot in it was taken between 2024-08-20 and 2024-12-19, and December has only 3,597 rows. The round count and the thin last month suggest an export cut at a row limit; this is an inference to confirm with whoever made the extract.
- It has no row in Distributor B's state, under any spelling. 238 of B's 370 client SKUs appear in it for other states.
- So no lag-1 forecast exists locally for any 2025 or 2026 month, for any distributor. The blank forecast columns mean missing data, not a zero forecast. Client question 15.

### Exceptions kept visible on B

Mapping: 7,366 matched, 189 not found, 7 ambiguous. Scope: 6,526 included (15,327.5 OOS cases); excluded 372 limited edition (1,420.8), 23 supply-constrained `QUOTA` (2,488.7), 402 VAP (1,986.7); review 196 mapping (164.7) and 43 size (13.0). None is dropped and no client SKU is guessed.

### What can be delivered now

| Item | Status |
|---|---|
| B Clean sheet, totals and lineage | Ready as a working file. Totals reconcile. Pending: the duplicate rule (team question 10). |
| B concentration (Pareto, repeat, spikes) | Ready as a description, with its limits: in-scope cut, mappings as supplied, Cases OOS. |
| B action list | Not ready. All 415 bias fields are `incomplete` and buffers are empty. Labels are readings, not causes. |
| B forecast bias | Blocked. No usable extract (client question 15). |
| A exploration notebook | Ready. |
| A clean workbook and analysis | Not started, by decision. Blocked on the blank-unshipped answer and on the template divergence. |

### Refresh checklist

When a new fill-rate extract, Master Data or forecast extract arrives:

1. Put it in the team folder; do not overwrite the current file. Note its date in `data_dictionary.md`.
2. Rerun `tools/build_distributor_b_v1.py`. It stops if a source column moved.
3. Rerun the B notebook. Section 28 asserts the published totals; a failed assert means the totals moved and must be explained before delivery.
4. For a forecast extract: check snapshot dates, forecast months and B's state first (section 27). Only then decide, as a team, how a SKU absent from a complete extract is read.
