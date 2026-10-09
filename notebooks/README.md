# notebooks/

One exploratory notebook **per distributor**, with one section per table (see
`docs/methodology.md` for why).

Naming: `NN_<stage>_<scope>.ipynb`, e.g. `01_eda_distributor_a.ipynb`,
`01_eda_master_data.ipynb`, `02_cleaning_distributor_a.ipynb`.

Shared structure for every EDA notebook:

1. Purpose and files covered
2. For each table: load → shape and grain → columns and types → missing values vs zeros
   → duplicates → distributions and outliers → time coverage → units → anomalies found
3. Cross-table relationships (keys, joins, reconciliation)
4. Open questions (also copied to `docs/open_questions.md`)

Before committing: **clear all outputs** (they can contain client data) and use codes, not real names.
