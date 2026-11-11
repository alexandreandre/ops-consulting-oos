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

### Template v1.1 and the client's answers (updated the same evening)

- **Found.** Template v1.1 is a Google Doc in the team's project folder, frozen on 2026-11-02 and owned by Lisa. It is the cleaning standard. It does not name distributors by code; the mapping to A and B comes from `private/KEY.md`. The rules are recorded in `decisions.md` (2026-11-10).
- **Distributor A.** No divergence left. The template and the client (2026-10-30, 2026-11-10) agree: short-shipped rows with fill rate 1 count as fulfilled; the 76 rows with shipped, unshipped and OOS blank are excluded; the 1,948 rows with shipped blank and unshipped filled count as fully OOS. The client also asked on 2026-11-10 to exclude the second org of the two-org state. With all of this, January–August 2026 stays at 95.7% (full period 95.92% to 95.89%; notebook A, section 20). A's cleaning is no longer blocked.
- **Distributor B duplicates.** No divergence. For this distributor the template keeps both rows when one code carries two products, as the 2026-11-04 workbook does. The "merge" rule applies to other distributors. Only open point: whether the kept rows should also be copied to `Removed_Dups` (team question 11).
- **Not yet in the template:** the client's answers of 2026-11-10 (second org of A's two-org state, "VV" vintages). Lisa to add them.

### Cases OOS or Cases Unshipped

- **Distributor B.** The two columns are equal on 7,495 of 7,562 rows. On the 67 rows with a pick omit, Cases OOS = Unshipped + Pick Omits (75.7 cases in all). On the weighted 9L ranking, the OOS Pareto has 53 cells and the Unshipped one 52, all 52 shared; every cell keeps its repeat pattern. The template's choice of Cases OOS changes nothing material.
- **Distributor A.** The columns differ by about 9,650 cases (Unshipped 73,303; OOS 63,654), mostly pick omits: here Unshipped = OOS + Pick Omits. That is the opposite convention to B. Ranked by source id, the 101 ids in the OOS Pareto all sit inside the 108 of the Unshipped Pareto. Neither column covers the blank-unshipped rows: Cases OOS is blank on all of them.
- Template v1.1 sets the procedure: compare Σ OOS with Σ Unshipped; a small gap means pick one, a large gap means ask the client whether pick omits count. B's gap is 0.35%, so Cases OOS stays. A's gap is about 13%, so the question goes to the client (client question 1).

### Forecasts for Distributor B

- The three Planning files are the only ones in the team folder. Judged by their names and the snapshot file's content, none is a 2026 extract; the sourcing matrix and parameters files were not opened.
- The snapshot file holds exactly 500,000 data rows. Every snapshot in it was taken between 2024-08-20 and 2024-12-19, and December has only 3,597 rows. The round count and the thin last month suggest an export cut at a row limit; this is an inference to confirm with whoever made the extract.
- It has no row in Distributor B's state, under any spelling. 238 of B's 370 client SKUs appear in it for other states.
- So no lag-1 forecast exists locally for any 2025 or 2026 month, for any distributor. The blank forecast columns mean missing data, not a zero forecast. Client question 15.
- Update the same evening: the client saved the 2026 extract for A and B on 2026-10-29 in the client's shared folder. Copy it into the team Planning folder, then rebuild. B's 2025 snapshots are still with the client's IT, so B's 2025 months stay "Lag1 incomplete". A's snapshots exist from September 2024.

### Exceptions kept visible on B

Mapping: 7,366 matched, 189 not found, 7 ambiguous. Scope: 6,526 included (15,327.5 OOS cases); excluded 372 limited edition (1,420.8), 23 supply-constrained `RTS` (2,488.7), 402 VAP (1,986.7); review 196 mapping (164.7) and 43 size (13.0). None is dropped and no client SKU is guessed.

### What can be delivered now

| Item | Status |
|---|---|
| B Clean sheet, totals and lineage | Ready as a working file. Totals reconcile. Duplicate handling matches template v1.1. |
| B concentration (Pareto, repeat, spikes) | Ready as a description, with its limits: in-scope cut, mappings as supplied, Cases OOS. |
| B action list | Not ready. All 415 bias fields are `incomplete` and buffers are empty. Labels are readings, not causes. |
| B forecast bias | Blocked. The 2026 extract is on the client's shared folder, not yet in the team Drive; 2025 snapshots are still with the client's IT (client question 15). |
| A exploration notebook | Ready. |
| A clean workbook and analysis | Not started. Unblocked on 2026-11-10: the client answered and the rules are logged. Owner to confirm (team question 12). |

### Refresh checklist

When a new fill-rate extract, Master Data or forecast extract arrives:

1. Put it in the team folder; do not overwrite the current file. Note its date in `data_dictionary.md`.
2. Rerun `tools/build_distributor_b_v1.py`. It stops if a source column moved.
3. Rerun the B notebook. Section 28 asserts the published totals; a failed assert means the totals moved and must be explained before delivery.
4. For a forecast extract: check snapshot dates, forecast months and B's state first (section 27). Only then decide, as a team, how a SKU absent from a complete extract is read.

## Client deck for Distributor B (2026-11-10)

For the client call of 2026-11-12. `tools/build_distributor_b_deck.py` reads `data/cleaned/distributor_b_v1.xlsx` and writes `reports/distributor_b_client_deck.pptx` (11 slides, speaker notes in English with a plain French line). The deck is not committed; a copy is in the team Drive `Working files` folder. Display names come from a git-ignored file, `private/deck_labels.json`. Rebuild it after each new extract.

What it says: in-scope OOS rate 4.3% (9L); 53 of 415 loss cells carry 80% of weighted OOS; repeat cells 57%; eight spike location-months; forecast bias not run yet, with what is needed; four data questions for the client. Correction made while building it: the in-scope OOS rate is 4.3% over all in-scope volume, not 4.4% (that figure divided by the volume of the loss cells only).

## Distributor B, later the same evening

- **Code review.** An independent read of `tools/build_distributor_b_v1.py` against template v1.1 raised 13 points. The bugs are fixed and logged in `decisions.md`; the rebuilt workbook has the same totals, the same 53 Pareto cells and the same patterns. The open method points are listed there for the team.
- **New context (notebook B, part 7).** About 70% of the weighted loss is on items the distributor lists as "Allocated - Supplier" and 20% on "Discontinued" items (client question 17). The 53 Pareto cells all come from one source, shared by both locations. 42 of them have buffer settings, all at the default variability factor, none overridden; repeat and one-off cells have the same settings. The two locations have their own location codes and parameters.
- **Unmapped codes.** The SCC bridge proposes a client SKU for 11 of the 20 codes, after reproducing all 370 existing mappings. Proposals for Lisa: `tools/propose_distributor_b_mappings.py` writes `data/interim/distributor_b_mapping_proposals.xlsx` (copy in `Working files`). Not applied.
- **Client deck.** Now 12 slides: a supply-context slide and updated questions (unmapped codes with proposals, supplier allocation). Rebuilt workbook and proposals are in `Working files`; the deck stays on Alexandre's computer.

## Team meeting, 2026-11-10

Notes kept locally by Alexandre, shared within the team directly. For B:

- Alexandre and Lena own B; Yinqi owns A. A's cleaning in this branch stops at the notebook checks; A's owner takes it from there.
- The three recently launched SKUs the A owner wants excluded are B's three `RTS` ids, already excluded. The workbook and the client deck do not change.
- Each owner brings a short analysis to the 2026-11-12 call: for B, the 12-slide deck.
- Data questions go to the client by email the day after the meeting. B's open questions (17, 13, 12) can go out on 2026-11-11.

- After the meeting (same evening): notebook B part 8 and a new deck slide (now 13 slides). Each spike is narrow: three products make 65% to 87% of it. One client SKU, a 750 ml gift box, is in 7 of the 8 spikes, ranks 1 and 2 in the Pareto, and carries about 22% of the weighted loss for about 4% of the volume; its item status is "Allocated - Supplier". No spike comes back in the same calendar month a year later: no seasonality to report. The deck stays on Alexandre's computer (`reports/`, not shared on the Drive).
