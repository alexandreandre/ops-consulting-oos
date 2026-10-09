# Onboarding

Step-by-step setup for a new teammate, **including if you have never coded**. You don't need
to write code: Codex (the AI in Cursor) does the technical steps. You tell it what you want in
plain English and check what it does.

Already done if you are reading this: Cursor and Codex installed, repository cloned, GitHub access.

## 1. Open the project

Cursor → **File → Open Folder** → select the `ops-consulting-oos` folder.

## 2. Privacy settings (once)

- In ChatGPT (the account Codex uses): **Settings → Data controls → turn off "Improve the model for everyone"**.
- In Cursor: **Settings → search "Privacy Mode" → turn it on**.

## 3. Get the data (never through GitHub)

The raw files and `KEY.md` are in the **team's shared data folder** (ask Alexandre for the link).

1. Copy `KEY.md` into the `private/` folder of the project.
2. Copy your raw files into the matching folder, without renaming or opening them in Excel first
   (saving from Excel can change dates and formats):

   | Data | Folder |
   |---|---|
   | Distributor A | `data/raw/distributor_a/` |
   | Distributor B | `data/raw/distributor_b/` |
   | Distributor C | `data/raw/distributor_c/` |
   | Distributor D | `data/raw/distributor_d/` |
   | Master Data | `data/raw/master_data/` |

   `KEY.md` tells you which real distributor each code is.
3. Check: in Cursor's file panel, the data files appear **greyed out**. That means Git ignores
   them and they will never be uploaded. They must **not** appear in the Source Control panel.

## 4. First message to Codex (setup, once)

Copy-paste this into Codex:

> Read AGENTS.md and docs/onboarding.md. I'm new to coding. Get the latest version of the
> project, set up the Python environment, and check that everything works. Explain each step
> briefly in plain English.

Codex will ask permission to run commands. If you don't understand one, ask it
*"What does this do?"* before approving.

## 5. Everyday prompts

**Start a piece of work**
> I want to start exploring Distributor C. Create a new branch for this, then create the
> exploration notebook following notebooks/README.md. Go one table at a time and explain
> what you find in plain English.

**Note something unclear**
> Add this question to docs/open_questions.md: …

**Save and share your work**
> Save my work: check that no data files or real names are included, commit with a clear
> message, push, and give me the link to open a pull request.

Then open the link, click **Create pull request**, and tell the team it's ready for review.

**Get the team's latest changes**
> Switch to main and get the latest version from GitHub.

## 6. Rules to remember

- Data never goes on GitHub. If a `.csv` or `.xlsx` file shows up in Source Control or in
  Codex's list of files to commit, **stop** and ask the team.
- Never type real client or distributor names in notebooks, docs or commit messages. Use the codes.
- If you see "conflict", "rejected" or red errors you don't understand, don't force anything.
  Message Alexandre.
- See `docs/team_workflow.md` for what branches, commits and pull requests are.
