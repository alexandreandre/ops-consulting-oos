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
