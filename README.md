# Out-of-Stock Reduction in a Demand-Driven Environment

Private workspace of **116th Consulting** (Columbia University student consulting team)
for an operations consulting engagement with a wines & spirits client.

> **Confidentiality.** The client and its distributors are anonymized in this repository
> ("the client", "Distributor A–D"). The name key lives in `private/KEY.md`, which is
> git-ignored and kept in the team's Drive folder. No client data is ever committed.
> Rules and automatic checks: **[DATA_POLICY.md](DATA_POLICY.md)**.

## The business problem

The client sells through several distributors. Products sometimes go **out of stock (OOS)**
even though the client plans replenishment with a demand-driven method (DDMRP). We want to
understand **why stockouts happen** and **what operational levers would reduce them** without
simply adding inventory.

## Objectives

1. Understand the datasets the client and its distributors have shared.
2. Build reliable, documented, comparable data across distributors.
3. Diagnose OOS drivers (demand, replenishment parameters, lead times, distributor operations, data issues).
4. Recommend actionable improvements to inventory and replenishment practices.

## Current phase

**Phase 1–2: data inventory, business understanding and exploration.** The client's files
(four distributor fill-rate files, master data, planning files) have been received and inventoried.
Next: train teammates and explore the data; cleaning decisions are taken together at the end of
exploration, then cleaning is done in Excel. No analysis results exist yet.

Cleaning is a means, not the goal: the end product is a diagnosis of OOS drivers and
recommendations. See [docs/roadmap.md](docs/roadmap.md).

## Team

| Member | Initial responsibility |
|---|---|
| Alexandre | Distributor A and Distributor B datasets |
| Sying | Distributor C and Distributor D datasets |
| Lisa | Master Data, ambiguous mappings, standardization support, reconciliation |

This allocation may evolve. Everyone follows the same methodology so results stay comparable.

## Workflow

```
raw data ──► explore (one notebook per distributor) ──► team decisions ──► cleaning in Excel
        ──► standardization across distributors ──► OOS diagnosis ──► DDMRP analysis ──► recommendations
```

## Repository map

| Path | Content |
|---|---|
| `docs/project_overview.md` | Mission, scope, stakeholders, expected outputs |
| `docs/business_context.md` | OOS and DDMRP explained; general vs client-specific facts |
| `docs/roadmap.md` | Phases, deliverables, completion criteria, status |
| `docs/data_dictionary.md` | Inventory of datasets (filled as we learn) |
| `docs/glossary.md` | Supply-chain and DDMRP terms in plain language |
| `docs/methodology.md` | How we explore, clean and standardize data |
| `docs/eda_guide.md` | What exploratory analysis is, in short |
| `docs/team_workflow.md` | Git/GitHub workflow, incl. a beginner guide |
| `docs/open_questions.md` | Questions for the client or the team |
| `docs/decisions.md` | Decision log |
| `docs/onboarding.md` | Setup guide for new teammates (no coding needed) |
| `data/` | Links to the team's Google Drive data (git-ignored). See `data/README.md` |
| `notebooks/` | Exploratory notebooks (one per distributor) |
| `src/` | Reusable code, once patterns repeat |
| `reports/` | Generated outputs (git-ignored) |
| `tests/` | Validation checks on transformations |
| `DATA_POLICY.md` | Confidentiality rules, automatic checks, end-of-project checklist, signatures |
| `AGENTS.md` | Rules for AI coding assistants |
| `tools/guard.py`, `.githooks/` | Confidentiality guard used by Git hooks and the GitHub check |
| `private/` | Local-only files such as the name key (git-ignored) |
| `requirements.txt` | Python packages for notebooks |

## Getting started

Follow **[docs/onboarding.md](docs/onboarding.md)**: step-by-step setup with Cursor + Codex,
written for teammates who have never coded. In short: install Google Drive for desktop (LionMail account), add the team folder to My Drive, then ask
Codex to set up the project (Python environment, confidentiality guard, link to the Drive data,
automatic notebook-output stripping). Your first pull request is signing `DATA_POLICY.md`.

## Confidentiality

All team members signed an NDA with the client. **[DATA_POLICY.md](DATA_POLICY.md)** turns it into
eight rules, lists what is enforced automatically (Git hooks, GitHub check, protected `main`, AI
read restrictions) and holds each member's signed acknowledgement. Read it before your first commit.
