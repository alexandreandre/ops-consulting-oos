# Out-of-Stock Reduction in a Demand-Driven Environment

Private workspace of **116th Consulting** (Columbia University student consulting team)
for an operations consulting engagement with a wines & spirits client.

> **Confidentiality.** The client and its distributors are anonymized in this repository
> ("the client", "Distributor A–D"). The name key lives in `private/KEY.md`, which is
> git-ignored and shared only through the team's private channel. No client data is
> ever committed. See [Confidentiality](#confidentiality).

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

**Phase 1–2: data inventory, business understanding and exploration.** Initial distributor
datasets and supporting documentation have been received; more may follow. No analysis
results exist yet.

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
raw data ──► explore (one notebook per distributor) ──► documented cleaning
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
| `docs/team_workflow.md` | Git/GitHub workflow, incl. a beginner guide |
| `docs/open_questions.md` | Questions for the client or the team |
| `docs/decisions.md` | Decision log |
| `docs/onboarding.md` | Setup guide for new teammates (no coding needed) |
| `data/` | Local data only (git-ignored). See `data/README.md` |
| `notebooks/` | Exploratory notebooks (one per distributor) |
| `src/` | Reusable code, once patterns repeat |
| `reports/` | Generated outputs (git-ignored) |
| `tests/` | Validation checks on transformations |
| `AGENTS.md` | Rules for AI coding assistants |
| `private/` | Local-only files such as the name key (git-ignored) |
| `requirements.txt` | Python packages for notebooks |

## Getting started

Follow **[docs/onboarding.md](docs/onboarding.md)**: step-by-step setup with Cursor + Codex,
written for teammates who have never coded. In short: clone the repo, copy `KEY.md` and your raw
files from the team's shared data folder into `private/` and `data/raw/<code>/`, then ask Codex to
set up the environment (Python, `requirements.txt`, automatic notebook-output stripping).

## Confidentiality

All team members signed an NDA with the client. In practice:

- **Never commit** data files, client slides, emails, NDA documents, passwords or keys. `.gitignore`
  blocks common formats, but check `git status` before every commit.
- **Never write real client, distributor or stakeholder names** in tracked files, commit messages,
  branch names or pull requests. Use the codes.
- Do not upload client data to external tools (including AI assistants) beyond what the team has
  agreed is allowed.
- Clear notebook outputs before committing.
- At the end of the engagement, the NDA requires deleting all project files: this includes the
  GitHub repository and every local clone.
