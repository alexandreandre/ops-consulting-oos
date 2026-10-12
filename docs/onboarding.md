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

## 3. Connect to the team's Google Drive (once)

The raw data stays in the team's **LionMail Google Drive**. The project reads it from there: nothing
is downloaded or copied by hand, and new files appear automatically.

1. Install **Google Drive for desktop** (https://www.google.com/drive/download/) and sign in with
   your **Columbia (LionMail)** account. Keep **"Stream files"**. When it offers to sync your
   Documents, Desktop or Downloads folders, **untick everything and skip**.
2. In Google Drive on the web, go to **Shared with me**, right-click the team data folder →
   **Organize → Add shortcut → My Drive**. (Drive for desktop only shows what is in My Drive.)

## 4. First message to Codex (setup, once)

Copy-paste this into Codex:

> Read AGENTS.md and docs/onboarding.md. I'm new to coding. Set up the project on my computer:
> get the latest version, set up the Python environment, turn on the confidentiality guard, and
> connect the project to Google Drive. Explain each step briefly in plain English.

Codex will ask permission to run commands. If you don't understand one, ask it
*"What does this do?"* before approving.

At the end, in Cursor's file panel, `data/raw/distributor_c` (etc.) show the Drive files, greyed out:
Git ignores them and they will never be uploaded. They must **not** appear in the Source Control panel.

**Never edit, rename or delete files inside `data/raw/`**: they are the team's shared Drive files.

## 5. Your first pull request: sign the data policy

Read `DATA_POLICY.md` (one page), then ask Codex:

> Show me that the confidentiality guard works: create a test file containing the name of one of
> the distributors from private/KEY.md, try to commit it, show me the result, then delete the test file.

> Create a branch, add my name, my GitHub username and today's date to the acknowledgement table
> in DATA_POLICY.md, commit, push, and give me the link to open the pull request.

Open the link, click **Create pull request**, and tell Alexandre. This is exactly how every piece
of work will be shared.

## 6. Everyday prompts

**Start a piece of work**
> I want to start exploring Distributor C. Create a new branch for this, then create the
> exploration notebook following notebooks/README.md. Go one table at a time and explain
> what you find in plain English.

**Note something unclear**
> Add this question to docs/open_questions.md: …

**Save and share your work**
> Save my work: check that no data files or real names are included, commit with a clear
> message, push, and give me the link to open a pull request.

**Get the team's latest changes**
> Switch to main and get the latest version from GitHub.

## 7. Rules to remember

- Data never goes on GitHub, and you write codes, not real names. The guard blocks mistakes:
  if it says **"Blocked by the confidentiality guard"**, nothing was sent. Ask Codex to explain and fix.
- Never bypass the guard (`--no-verify`). See `DATA_POLICY.md`.
- If you see "conflict", "rejected" or red errors you don't understand, don't force anything.
  Message Alexandre.
- See `docs/team_workflow.md` for what branches, commits and pull requests are.
