# Decision log

Record decisions that affect the analysis or the way we work. Newest first.

| Date | Decision | Rationale | Responsible |
|---|---|---|---|
| 2026-10-09 | Raw data is read directly from the team's LionMail Google Drive through Google Drive for desktop; each `data/raw/<code>` is a local link to the matching Drive folder. Notebook outputs are stripped automatically with nbstripout. | One master copy, no manual copies to keep in sync, data never touches GitHub; protects teammates new to Git from committing data by mistake. | Alexandre |
| 2026-10-09 | Client, distributors and stakeholders are anonymized in the repository; the name key is kept in git-ignored `private/KEY.md`. | The NDA treats client and customer information as confidential and the client's written consent for GitHub storage has not been obtained. | Alexandre |
| 2026-10-09 | No client data is committed; `data/` is git-ignored except READMEs and placeholders. | Confidentiality (NDA). | Alexandre |
| 2026-10-09 | One exploratory notebook per distributor, with one section per table. | See `methodology.md`. | Alexandre |

Template:

| YYYY-MM-DD | What was decided | Why, and alternatives considered | Who |
