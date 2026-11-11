# Team meeting, 2026-11-10 (evening, about 40 minutes)

Notes from the recording, written so teammates who left early or missed it can catch up.
The raw recording and transcript stay outside the repository: they contain real names.
Side conversations that were not part of the meeting are left out.

**How to read this.** The recording's speaker labels are unreliable, so points are attributed
by role (project lead, distributor owner), not by voice. Figures quoted from other owners are
as presented in the meeting; they are not checked in this repository.

## Who works on what (confirmed)

| Distributor | Owner(s) | Status given in the meeting |
|---|---|---|
| A | Yinqi | Cleaned; first analysis presented (below). |
| B | Alexandre and Lena | Cleaned; Pareto done. B covers both locations of the distributor's state. |
| C | Siying | Cleaning finished, no major issue against the standard. Analysis not started. |
| D | Siddarth and Chuxin | First look at the data; questions for the client (below). |

This settles team question 12: A is no longer with Alexandre.

## Dates

- **Thursday 2026-11-12, client call.** Each owner brings a short analysis of their
  distributor, enough to discuss with the client's planning contact. Depth is not expected.
- **2026-12-03, final report.** All analysis done by then.
- Data questions go to the client's planning contact **by email the day after the team
  meeting**, not at the Thursday call, so the contact can get the distributor's answer before
  the following Monday.

## Guidance from the project lead

- The template is a **guide, not a fixed process**. The concepts carry over (which SKUs drive
  the OOS, repeat vs one-off, seasonality, forecast bias). The exact steps may not: some
  forecast lags may not exist for every distributor.
- The January–August 2026 cut in the template exists because Distributor C lacks 24 months of
  history. Distributors with full history (A, B) can analyse the whole period.
- Charts that rank SKUs should show **product names**, or come with a table listing them.
  A bar per SKU with no label is hard to read.
- The 9L weighting puts all products on one unit so they can be compared (template rule).

## Distributor A (presented by its owner)

- Overall OOS about 3% over 24 months. Worst market 4.4%, next 3.3%. The largest market
  (39% of ordered cases) is at 2.6%.
- Worst market-month: 16.2% (July 2026). Biggest spike: 4.4 times normal in the same
  market-month, mostly from one cognac 750 ml SKU.
- Concentration, January–August 2026 (the template's period for the repeat rule): 724
  location × SKU cells had an OOS; 103 of them (14%) make 80% of the loss volume.
  Repeat (OOS in 4 or more of the 8 months) and large: 32 cells, 31% of the loss, to look at
  first. Repeat and small: 37 cells, easy to miss.
- Lag-1 forecast bias (last month's forecast against actual orders; negative means the
  forecast was too low). Problem cells (OOS rate 5% or more): median bias −13.9%, and 63% are
  under-forecast by more than 10%. Healthy cells (about 1%): median −2.1%, 29%. A clear
  signal, maybe not the whole story. A's owner used the forecast data the client sent.
- Feedback: add product names to the SKU chart; possibly use the full period instead of the
  8-month cut.

## Distributor D (first look)

- July 2026 demand is about 9,600 cases, against about three times that in June and August.
  Possibly an incomplete month.
- August fill rate is blank or zero on a whole block of rows.
- In July, one product's forecast is about 2.5 times its demand, against about 1.5 for the rest.
- Negative values in July, mostly returns.
- The client said earlier that D has no historical forecast.

## Points that concern Distributor B

- **Three recently launched SKUs** that share a brand nickname were flagged in the meeting as
  new launches to exclude. They show heavy OOS in every market. On B they are exactly the three
  ids already excluded as `RTS`: 23 rows, 13,390 cases ordered, first month May 2026, none in
  the Pareto. Nothing changes in the B workbook or the client deck. This supports the match in
  client question 13.
- B's forecast data has not come from the client yet (client question 15).
- Owners of B left before the end of the meeting. Nothing after that point concerned B.

## Actions

| Action | Owner | When |
|---|---|---|
| Short analysis of each distributor for the client call | Each owner | 2026-11-12 |
| Email the client's planning contact about A's worst market-month spike, with the one SKU behind it | Yinqi | 2026-11-11 |
| Check the three new-launch SKUs on A and exclude them | Yinqi | Before the call |
| Add product names to the SKU ranking chart | Yinqi | After the meeting |
| Send the client the data questions on D (July volume, August fill rate, July forecast, returns), in writing | Chuxin | 2026-11-11 |
| Analysis of C (seasonality, top SKUs), even brief | Siying | 2026-11-12 |
| Proposed, not assigned in the meeting: email B's open questions to the client's planning contact (allocated items, RTS ids, unmapped codes) under the same rule | Alexandre | 2026-11-11 |
