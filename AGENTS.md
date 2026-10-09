# Instructions for AI assistants (Codex, Cursor, Claude Code, etc.)

Read `README.md` first, then the relevant file in `docs/`. Some teammates are new to
coding: see "Working with teammates new to coding" below.

## Confidentiality rules (non-negotiable)

- The client and its distributors are **anonymized** in every tracked file:
  "the client", "Distributor A–D", "Master Data".
- If `private/KEY.md` exists locally, you may read it to understand which real
  company a code refers to, but **never write real client, distributor or
  stakeholder names into any tracked file**, commit message, branch name or PR.
  This includes file paths, sheet names and column names typed in notebooks:
  select files with a pattern and sheets/columns by position (see `data/README.md`).
- Never commit anything from `data/` except `README.md` and `.gitkeep` files.
- Never upload data files to websites, APIs or any external service.

## Exploring client data (keep exposure minimal)

- Explore through code that prints **summaries**: shape, column names, types, missing
  counts, value counts of low-cardinality columns, date ranges, `describe()`.
- Do not open raw files directly in the chat and do not print whole tables. If examples
  are needed, show at most 5 rows and only the relevant columns.
- Never print columns with personal data (contact names, e-mails, phone numbers).
- `data/raw/` is the team's shared Google Drive: **read only**. Never create, edit,
  rename, move or delete anything inside it.

## First-time setup (when the user asks to set up the project)

1. `git checkout main` then `git pull`.
2. Check Python ≥ 3.10 (`python3 --version`; on Windows `py --version`). If missing,
   tell the user to install it from python.org and wait.
3. Create the environment: `python3 -m venv .venv`, then
   `.venv/bin/pip install -r requirements.txt` (Windows: `.venv\Scripts\pip`).
4. Run `.venv/bin/nbstripout --install` (Windows: `.venv\Scripts\nbstripout --install`)
   so notebook outputs are removed automatically at each commit.
5. Connect Google Drive (next section).
6. Run `git status` and confirm no data file appears. Tell the user notebooks must use
   the `.venv` kernel.

## Connecting the project to Google Drive (once per computer)

1. Check `private/KEY.md` exists. If not, ask the user to download it from the team's
   Drive folder into `private/`.
2. Check Google Drive for desktop is running and signed in with the user's Columbia
   (LionMail) account. Mac: `~/Library/CloudStorage/GoogleDrive-<email>/`. Windows: a
   drive letter, usually `G:\`. If missing, tell the user to install it from
   https://www.google.com/drive/download/ , sign in, and wait.
3. Find the team folder under `My Drive`. If it is missing, the user must add a shortcut
   on the web: Shared with me → right-click the folder → Organize → Add shortcut → My Drive.
4. For each code in `KEY.md`, locate its Drive folder and create the link
   `data/raw/<code>` (remove the empty folder first if one exists):
   - Mac: `ln -s "<drive folder path>" data/raw/<code>`
   - Windows: `mklink /D data\raw\<code> "<drive folder path>"` (needs Developer Mode)
5. List the files visible through each link (names only) and run `git status`: the links
   must not appear.

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
