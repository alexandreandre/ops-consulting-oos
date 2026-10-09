# Instructions for AI assistants (Codex, Cursor, Claude Code, etc.)

Read `README.md` first, then the relevant file in `docs/`. Some teammates are new to
coding: see "Working with teammates new to coding" below.

## Confidentiality rules (non-negotiable)

- The client and its distributors are **anonymized** in every tracked file:
  "the client", "Distributor A–D", "Master Data".
- If `private/KEY.md` exists locally, you may read it to understand which real
  company a code refers to, but **never write real client, distributor or
  stakeholder names into any tracked file**, commit message, branch name or PR.
- Never commit anything from `data/` except `README.md` and `.gitkeep` files.
- Never upload data files to websites, APIs or any external service.

## Exploring client data (keep exposure minimal)

- Explore through code that prints **summaries**: shape, column names, types, missing
  counts, value counts of low-cardinality columns, date ranges, `describe()`.
- Do not open raw files directly in the chat and do not print whole tables. If examples
  are needed, show at most 5 rows and only the relevant columns.
- Never print columns with personal data (contact names, e-mails, phone numbers).
- Load raw files read-only; never write into `data/raw/`.

## First-time setup (when the user asks to set up the project)

1. `git checkout main` then `git pull`.
2. Check Python ≥ 3.10 (`python3 --version`; on Windows `py --version`). If missing,
   tell the user to install it from python.org and wait.
3. Create the environment: `python3 -m venv .venv`, then install with
   `.venv/bin/pip install -r requirements.txt` (Windows: `.venv\Scripts\pip`).
4. Run `.venv/bin/nbstripout --install` (Windows: `.venv\Scripts\nbstripout --install`)
   so notebook outputs are removed automatically at each commit.
5. Check that `private/KEY.md` exists and list which `data/raw/<code>/` folders
   contain files (file names only). Tell the user what is missing.
6. Run `git status` and confirm no data file appears. Tell the user notebooks must use
   the `.venv` kernel.

## Working with teammates new to coding

- Explain in short, plain English. Do the git and terminal steps for them.
- Follow `docs/team_workflow.md`: never commit to `main`; one branch per piece of work,
  named `<firstname>/<topic>` (e.g. `sying/eda-distributor-c`); pull request to merge.
- Before every commit: run `git status`, show the user the list of files to be committed,
  and confirm none is a data file and no real name appears.
- After pushing, give the user the link to open the pull request.
- Never run `git push --force`, `git reset --hard`, or delete files or branches without
  the user's explicit confirmation.
- When the business meaning of data is unclear, add a question to
  `docs/open_questions.md` instead of guessing.

## Working rules

- Explore before cleaning; document anomalies in the notebook and in
  `docs/open_questions.md`.
- Write derived files to `data/interim/`, `data/cleaned/` or `data/standardized/`.
- Keep original SKUs, vintages, units and granularity; never silently convert.
- Record business decisions in `docs/decisions.md`.
