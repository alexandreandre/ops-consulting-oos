# Roadmap

Status values: **Not started**, **In progress**, **Done** (only with evidence in the repo).
No deadlines are set here; add them when agreed with the client.

| Phase | Status |
|---|---|
| 1. Data inventory and business understanding | In progress |
| 2. Exploratory data analysis | In progress |
| 3. Data quality and cleaning | In progress |
| 4. Standardization and reconciliation | Not started |
| 5. OOS diagnostic analysis | Not started |
| 6. Inventory and DDMRP analysis | Not started |
| 7. Recommendations | Not started |

## Phase 1: Data inventory and business understanding
- **Goal:** know which files exist, what they represent, their grain, time coverage, units and how they relate.
- **Deliverables:** completed `data_dictionary.md`; first list of `open_questions.md`.
- **Depends on:** files received from the client.
- **Done when:** every received file has a data dictionary entry and its business meaning is understood or listed as an open question.

## Phase 2: Exploratory data analysis
- **Goal:** understand structure, distributions, missing values, duplicates and anomalies per distributor.
- **Deliverables:** one EDA notebook per distributor, one for Master Data, and one for Planning. What this phase is: `eda_guide.md`.
- **Also:** training of teammates new to data work.
- **Depends on:** Phase 1.
- **Done when:** each table has been profiled with the shared notebook structure, anomalies are
  documented, and the team has agreed the cleaning decisions (logged in `decisions.md`).
- **Progress (2026-10-23):** Distributor A and Distributor B fill-rate files are explored in
  `notebooks/01_eda_distributor_a.ipynb` and `notebooks/01_eda_distributor_b.ipynb`.
  The client calls of 2026-10-23 answered the unit, the fill-rate definition, the grain
  (SKU × market) and the cross-distributor key. Those decisions are in `decisions.md`.
  Distributor A's blank unshipped cells are still with the client. No cleaning of A.

## Phase 3: Data quality and cleaning
- **Goal:** apply justified, reproducible cleaning rules while keeping raw files untouched.
- **How:** in Excel, following the team's cleaning spec (column list, flags, control totals).
- **Deliverables:** cleaning rules documented per table; cleaned files in `data/cleaned/`.
- **Depends on:** Phase 2; client answers on ambiguous fields.
- **Done when:** every rule is written down with its reason, and raw vs cleaned totals reconcile.
- **Progress (2026-10-23):** Distributor B has a local clean workbook (`data/cleaned/distributor_b_clean.xlsx`,
  also in the team Drive `Working files` folder). Fourteen duplicate keys are summed.
  The 9L factor and the client SAP SKU are joined where Master Data is one-to-one.
  The two sales orgs are not summed on the clean grain. A market view adds them.
  Forecasts, root-cause tags and the pilot are not in that file. Distributor A is not started.
  On 2026-10-26 the same workbook gained the concentration, repeat and month views
  (sheets Analysis, Pareto, Pareto_NG, Seasonality, Month_Id). The quadrant labels
  are readings. They are not root causes.
  On 2026-11-04 a second workbook, `data/cleaned/distributor_b_v1.xlsx`, follows the
  frozen output contract: one raw row per clean row, sales orgs kept apart, cases OOS,
  December and January at half weight, and location × client SAP SKU. Forecast columns
  are blank because the local snapshot extract has no rows for this distributor.

## Phase 4: Standardization and reconciliation
- **Goal:** a common representation across distributors (keys, units, dates, SKUs) without losing detail.
- **Deliverables:** standardized schema; mapping tables (SKUs, units, distributors); validation checks.
- **Depends on:** Phase 3; Master Data mappings.
- **Done when:** standardized data reconciles with each source and mapping gaps are listed.

## Phase 5: OOS diagnostic analysis
- **Progress (2026-11-04):** Distributor B has a second cut in `distributor_b_v1.xlsx`. On the in-scope cells, 53 location × client SKU cells carry 80% of weighted OOS 9L. Repeat cells carry 57% of that weighted loss, and the repeat-and-large quadrant carries 50%. Eight location-months have a spike index of 2 or more. Forecast bias is not calculated. This is still one distributor, so the phase stays not started.
- **Goal:** describe where and when stockouts, pick omits and unfulfilled orders occur, and for which products and distributors.
- **Deliverables:** OOS diagnostic with patterns and candidate root causes.
- **Depends on:** Phase 4; agreed OOS definition.
- **Done when:** the main OOS patterns are quantified and each has evidence-backed candidate causes.

## Phase 6: Inventory and DDMRP analysis
- **Goal:** relate replenishment parameters (ADU, buffers, TOY/TOG, MOQ, lead times, forecasts) to OOS performance.
- **Deliverables:** analysis of parameter adequacy vs observed demand and OOS.
- **Depends on:** Phase 5; access to parameter data and formulas.
- **Done when:** we can say which parameters or processes are linked to OOS, with evidence.

## Phase 7: Recommendations
- **Goal:** translate findings into actionable operational recommendations.
- **Deliverables:** prioritized recommendations with expected impact and trade-offs.
- **Depends on:** Phases 5–6.
- **Done when:** recommendations are reviewed by the team and presented to the client.

## Possible extension (idea, not agreed)

Alexandre's early notes suggest going further: classify each OOS by root cause, build a simple
rule-based "what action for which problem" method, validate it on past OOS (without adding too much
inventory), then test it out of sample. To be discussed with the team and the client.
