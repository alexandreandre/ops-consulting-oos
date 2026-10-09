# Roadmap

Status values: **Not started**, **In progress**, **Done** (only with evidence in the repo).
No deadlines are set here; add them when agreed with the client.

| Phase | Status |
|---|---|
| 1. Data inventory and business understanding | In progress |
| 2. Exploratory data analysis | Not started |
| 3. Data quality and cleaning | Not started |
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
- **Deliverables:** one EDA notebook per distributor and one for Master Data.
- **Depends on:** Phase 1.
- **Done when:** each table has been profiled with the shared notebook structure and anomalies are documented.

## Phase 3: Data quality and cleaning
- **Goal:** apply justified, reproducible cleaning rules while keeping raw files untouched.
- **Deliverables:** cleaning rules documented per table; cleaned files in `data/cleaned/`.
- **Depends on:** Phase 2; client answers on ambiguous fields.
- **Done when:** every rule is written down with its reason, and raw vs cleaned totals reconcile.

## Phase 4: Standardization and reconciliation
- **Goal:** a common representation across distributors (keys, units, dates, SKUs) without losing detail.
- **Deliverables:** standardized schema; mapping tables (SKUs, units, distributors); validation checks.
- **Depends on:** Phase 3; Master Data mappings.
- **Done when:** standardized data reconciles with each source and mapping gaps are listed.

## Phase 5: OOS diagnostic analysis
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
