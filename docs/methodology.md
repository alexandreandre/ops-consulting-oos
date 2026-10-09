# Methodology

## Principles

1. **Preserve raw data.** Files in `data/raw/` are never modified. Every derived file can be regenerated from them.
2. **Understand business meaning and grain first.** Before any transformation, know what one row represents and how it was produced.
3. **Explore before cleaning.** Profile the data first; cleaning decisions come from evidence, not habit.
4. **Document anomalies and assumptions** in the notebook and in `open_questions.md`.
5. **Distinguish missing values from genuine zeros.** An empty inventory cell is not the same as zero stock, and zero stock is exactly the event we study.
6. **Preserve original SKUs, vintages, units and granularity.** Add standardized columns next to the originals; never replace them silently.
7. **Apply justified, reproducible cleaning rules.** Each rule has a written reason and is applied by code, not by hand in Excel.
8. **Standardize only after understanding source differences.** Distributors may define the same field differently.
9. **Validate and reconcile.** Row counts and totals (cases, orders) must reconcile between raw, cleaned and standardized data.
10. **Document important business decisions** in `decisions.md`.

## Why one notebook per distributor (not one per table)

- A distributor's tables describe **one operation** (its inventory, orders, shipments). Exploring them
  together reveals keys, joins and inconsistencies that separate notebooks would hide.
- It matches **ownership**: each person is responsible for whole distributors.
- It keeps the number of notebooks small and **comparable**: the same section structure in every
  notebook makes cross-distributor comparison easy.
- If a single table becomes very large or complex, it can be split into its own notebook later.

## Shared notebook structure

See `notebooks/README.md`. Same sections, same order, for every distributor.

## Standard checks per table

Shape and grain · column types · missing values (and what missing means) · zeros vs missing ·
duplicates (exact and on business keys) · date range and gaps · units · outliers and negative values ·
key consistency with other tables and Master Data.
