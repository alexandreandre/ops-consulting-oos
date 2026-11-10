# Data dictionary

Preliminary inventory. **Only fill in what has been verified in the files.** Use codes, never real
names. "?" = not yet known.

## Sources

| Code | Owner | Raw folder | Status |
|---|---|---|---|
| Distributor A | Alexandre | `data/raw/distributor_a/` | Explored 2026-10-22, not cleaned |
| Distributor B | Alexandre | `data/raw/distributor_b/` | Explored 2026-10-22. October clean file plus a 2026-11-04 template rebuild, `data/cleaned/distributor_b_v1.xlsx`, not committed |
| Distributor C | Sying | `data/raw/distributor_c/` | Files received, not yet documented |
| Distributor D | Sying | `data/raw/distributor_d/` | Files received, not yet documented |
| Master Data | Lisa | `data/raw/master_data/` | Used for the Distributor B join, 2026-10-23. Not fully documented |
| Planning | Team | `data/raw/planning/` | Snapshot extract checked 2026-11-04. It has no rows for Distributor B. Rechecked 2026-11-10: exactly 500,000 data rows, snapshots taken 2024-08-20 to 2024-12-19 only, forecast months 2024-08 to 2026-10. Possibly cut at a row limit. Not fully documented |

## Files received (client file share, inventory of 2026-10-12)

Metadata only, as listed on the client's file share. Real file names are in `private/KEY.md`.

| Code | Content | Format | Size | File date |
|---|---|---|---|---|
| Distributor A | Fill-rate data | .xlsx | 1.98 MB | 2026-10-02 |
| Distributor B | Fill-rate data | .xlsx | 475 KB | 2026-10-02 |
| Distributor C | Fill-rate data | .xlsx | 3.60 MB | 2026-10-12 |
| Distributor D | Fill-rate data | .xlsx | 2.17 MB | 2026-10-02 |
| Master Data | Product / SKU master data | .xlsm (macro-enabled: never enable macros) | 5.80 MB | 2026-10-09 |
| Planning | Default sourcing matrix | .xlsx | 40.9 MB | 2026-10-09 |
| Planning | Historical forecast snapshots | .xlsx | 40.8 MB | 2026-10-09 |
| Planning | MVP parameters | .xlsx | 7.88 MB | 2026-10-02 |

The four fill-rate files were previously named with a `2026.08` prefix on the client side.

## Files

Real file names stay in `private/KEY.md`. Read these workbooks by column position: the product-id
header is not worded the same way on Distributor A and Distributor B.

### Distributor A fill-rate workbook

| Field | Value |
|---|---|
| Source | Distributor extract. One workbook, one sheet. |
| Distributor | A |
| Business meaning | Monthly cases ordered, confirmed, shipped, unshipped, pick omits, cases OOS, and a case fill rate. |
| Granularity (one row = …) | One SAP product id × one sales org × one month. That key has no duplicate. Product name is not a key: 31 names match more than one id (up to 3). |
| Time coverage | 2024-09 to 2026-08. 24 months, none missing. |
| Key columns | Month (column A), sales org (column C), SAP product id (column G). |
| Units | Physical cases, confirmed by the client on 2026-10-23. 81% of ordered quantities are multiples of 1/6, and fractional quantities are whole bottles under that reading on 97% of testable rows. The 9L factor is a separate column and is not applied on this file yet. Not converted. |
| Known limitations | Cases Shipped is blank on 2,024 rows. Cases Unshipped is blank on 22,359 rows, and on every one of those rows Case Fill Rate is exactly 1. On 21,251 of them shipped equals ordered; on 1,108 (8,624 cases) it does not, and Pick Omits and Cases OOS are blank there too. Pick Omits is blank on 26,990 rows. Cases OOS is blank on 23,555 rows. 9 rows have a 5-digit product id; the rest have 7 digits. |
| Rows | 29,118 |
| Coverage | 6 states, 7 sales orgs (one state has two orgs; each org is in one state), 28 brands, 922 product names, 958 product ids. One vendor value. The second org of the two-org state has rows from 2024-09 to 2025-06 only (0.8% of ordered cases). |
| Owner | Alexandre |
| Date received | 2026-10-02 |
| Explored | 2026-10-22. Not cleaned. Blank Cases Unshipped is still an open client question. |

### Distributor B fill-rate workbook

| Field | Value |
|---|---|
| Source | Distributor extract. One workbook, one sheet. |
| Distributor | B |
| Business meaning | Same 14 fields as Distributor A, in the same order. |
| Granularity (one row = …) | Intended grain is one SAP product id × one sales org × one month. 14 of those keys appear twice (28 rows, 241 ordered cases), each time with two product names and different quantities. 11 of the 14 fall in the month where one name hands over to the other. 11 ids have more than one product name somewhere in the file. |
| Time coverage | 2024-08 to 2026-08. 25 months, none missing. |
| Key columns | Month (column A), sales org (column C), SAP product id (column G). |
| Units | Physical cases, confirmed by the client on 2026-10-23. 87% of ordered quantities are multiples of 1/6, and fractional quantities are whole bottles under that reading on every testable row. In the clean working file the 9L factor is joined from Master Data where the item match agrees. The physical columns are not overwritten. |
| Known limitations | Quantity columns have no blanks. Case Fill Rate matches Cases Shipped / Cases Ordered within 0.5 point on 7,548 of 7,562 rows, and 1 − Cases Unshipped / Cases Ordered on 7,527. The duplicated keys above are the main defect. |
| Rows | 7,562 |
| Coverage | 1 state, 2 sales orgs, 24 brands, 403 product names, 391 product ids. One vendor value. |
| Owner | Alexandre |
| Date received | 2026-10-02 |
| Explored | 2026-10-22. Clean working file started 2026-10-23. Analysis views added 2026-10-26 (concentration, repeat, month). Raw file unchanged. |

## Column notes

Same positions on both files. Do not print the values of columns B–F (state, sales org, vendor, brand, product name).

| Column | Header | What the exploration found |
|---|---|---|
| A | Yearmonth | Month as YYYYMM. |
| B | State | Geography of the sales org. |
| C | Sales Org Name | Selling organization. Distributor A has 7, Distributor B has 2. |
| D | Vendor Name | A single value in each file. |
| E | Brand Name | 28 brands on A, 24 on B. |
| F | Product Name | Not a stable key. See the file blocks. |
| G | Source id. The header says "SAP product id". | Integer. Leading zeros are already gone. Header text is longer on Distributor A than on B. On Distributor B this is the distributor item code: 371 of 391 ids match column D of the first Master Data sheet, and none match the client SAP SKU in column N. |
| H | Cases Ordered | Always filled, always greater than 0. |
| I | Cases Confirmed | 0 means nothing was confirmed. Never above Cases Ordered. |
| J | Cases Shipped | Blank on some Distributor A rows. On B, within a rounding of Cases Confirmed. |
| K | Cases Unshipped | On A, a blank is scored as a full fill by column N. On B, filled on every row, mostly zeros. Equals OOS + Pick Omits on 28,475 of 29,118 rows of A and 7,495 of 7,562 rows of B; equals ordered − shipped on 7,542 rows of B. |
| L | Pick Omits | Much smaller than the confirmation gap (about 6,200 cases on A, about 80 on B). Not the same quantity as Cases OOS. Equals confirmed − shipped on 7,561 of 7,562 rows of B; on A the identity fails mostly where Pick Omits is blank. |
| M | Cases OOS | On B, the column total matches the confirmation gap. On A, blank on most rows. Equals ordered − confirmed on 28,784 rows of A (blank counted as 0) and 7,474 rows of B. |
| N | Case Fill Rate | Fraction from 0 to 1, never blank. Equals 1 − column K / column H (blank K as 0) on all 29,118 rows of A and on 7,527 of 7,562 rows of B, which is the formula on slide 10 of the client's introduction deck. On B it also tracks column J / column H. The unweighted average of this column is not the share of cases filled. The team standard, agreed 2026-10-23, is the case-weighted version of that formula. |

## Master Data used for Distributor B (2026-10-23)

The workbook has eight sheets. Only the join below was checked. Macros were not enabled.

| Where | What was checked |
|---|---|
| First sheet, column D | Distributor B item code. 1,574 filled cells, 1,494 distinct. 53 codes appear twice and point at two different client SAP SKUs. |
| First sheet, column N | Client SAP SKU. 7,196 rows, 7,196 distinct. Distributor B's column G matches none of them. |
| First sheet, column Y | 9L factor. One value per client SAP SKU. |
| First sheet, column M | Display type. Four values. |
| First sheet, column L | Bottle size. |
| First sheet, columns BD and DH | A deletion mark and an active flag. Copied when the matched item rows agree. Not interpreted. |
| Fourth sheet | Location list: name, market, state. Both of Distributor B's sales-org names match one row each, and both rows have the same market code. |

Of Distributor B's 391 source ids, 371 match column D, 20 do not (189 rows, about 2,032 cases ordered), and 1 matched id points at two client SAP SKUs (7 rows, 9 cases). The 9L factor agrees on that ambiguous id, so the factor is kept and the client SAP SKU is left blank.

Distributor A was not joined in this pass. Distributor C's worked file is a format reference only. It is not a raw source and it is not in `data/raw`.

## Analysis views on the Distributor B clean file (2026-10-26)

Local workbook only (`data/cleaned/distributor_b_clean.xlsx`), also in the team Drive `Working files` folder. Not committed.

| Sheet | One row is | What it answers |
|---|---|---|
| Analysis | The front page: totals, the two Pareto cuts, the repeat matrix, the busiest months | Where to read the result, and which totals must reconcile to zero |
| Pareto | One source id with a 9L factor, RTS excluded, both sales orgs added | Which ids carry the unshipped 9L, and whether they miss in 4 or more months |
| Pareto_NG | The same, kept to naked goods and gift box | The same ranking on the display types named for this cut |
| Seasonality | One month | The fill rate and the unshipped 9L, with RTS and without |
| Month_Id | One source id in one month, both sales orgs added | The working table the formulas read. Not a separate finding |

The row order on Pareto is the unshipped 9L at build. Amounts are formulas against Clean. Ids with no 9L factor stay off the ranking and remain on Exceptions. The quadrant labels are readings, not root causes.

## Template rebuild for Distributor B (2026-11-04)

Local workbook `data/cleaned/distributor_b_v1.xlsx`, also copied to the team Drive `Working files` folder. Not committed. Built by `tools/build_distributor_b_v1.py` from the raw extract. The October workbook above is unchanged.

Clean has one row per raw row and the template columns A–AL. The 14 duplicate item-month keys stay on Clean. `Removed_Dups` is empty, and the ordered, unshipped and cases-OOS totals match the raw extract (373,828.151 ordered, 21,325.637 unshipped, 21,401.305 cases OOS).

| Sheet | What it answers |
|---|---|
| Action_List | The reading for each in-scope location × client SKU with OOS 9L, in the template column order |
| Location_Severity | OOS rate and OOS 9L for each sales org at or above 10,000 ordered 9L, plus a month heatmap |
| Top_Cells | Pareto of weighted OOS 9L. December and January count half |
| Bias_Test | Present and empty. The local snapshot extract has no rows for this distributor |
| Spikes | Location-months whose weighted OOS 9L is at least twice that location's monthly average |
| QA | Raw-versus-clean differences, map status, scope, pattern and quadrant counts |
| Clean | Row-level data. Forecast columns are blank |
| Removed_Dups | Empty on purpose |

In-scope means naked goods or gift box, a one-to-one client SAP SKU, a 9L factor, and not a supply-constrained id, limited edition or VAP. On that cut, ordered 9L is 243,789.668 and OOS 9L is 10,699.074, an OOS rate of 4.4%. 602 location × client SKU cells. 415 have any OOS 9L. 53 of them carry 80.3% of weighted OOS 9L. Repeat cells carry 56.7% of that weighted loss. The repeat-and-large quadrant is 28 cells and 50.0%. Both sales orgs pass the 10,000 ordered-9L cut. Eight location-months spike, and five are marked as the shortlist.
