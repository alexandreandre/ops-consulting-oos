# Instructions for AI assistants (Cursor, Claude Code, etc.)

Read `README.md` first, then the relevant file in `docs/`.

## Confidentiality rules (non-negotiable)

- The client and its distributors are **anonymized** in every tracked file:
  "the client", "Distributor A–D", "Master Data".
- If `private/KEY.md` exists locally, you may read it to understand which real
  company a code refers to, but **never write real client, distributor or
  stakeholder names into any tracked file**, commit message, branch name or PR.
- Never commit anything from `data/` except `README.md` and `.gitkeep` files.
- Never send raw data files or their contents to external services.
- Do not print large extracts of raw data; summarize instead.

## Working rules

- Explore before cleaning; document anomalies in the notebook and in
  `docs/open_questions.md`.
- Never overwrite files in `data/raw/`. Write derived files to `data/interim/`,
  `data/cleaned/` or `data/standardized/`.
- Keep original SKUs, vintages, units and granularity; never silently convert.
- Record business decisions in `docs/decisions.md`.
- Clear notebook outputs before committing (outputs can contain client data).
