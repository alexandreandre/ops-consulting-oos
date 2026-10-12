# Data policy

Applies to everyone working on this project. It turns the NDA each of us signed with the client
into concrete rules. Most of them are enforced automatically, so following them costs nothing day to day.

## Rules

1. **Client data stays in two places only:** the team's LionMail Google Drive folder and team
   members' computers. Never on GitHub, personal cloud storage (iCloud, Dropbox, personal Google
   Drive), USB drives, e-mail or messaging apps.
2. **Use codes, never real names** (client, distributors, brands, client contacts) in the repository:
   files, notebooks, commit messages, branch names, pull requests. The key is in `private/KEY.md`.
3. **Share data only with team members who signed the NDA**, and only through the team's Drive folder.
4. **Raw files are read-only.** Never edit or save over a file in the Drive data folders. Excel
   working files go to the `Working files` folder of the team Drive.
5. **AI assistants** (Codex, Claude, Cursor) may run code that prints summaries of the data. Never
   paste raw files or full tables into a chat. Keep model training off (ChatGPT: Settings → Data
   controls → "Improve the model for everyone" off; Cursor: Privacy Mode on).
6. **Never bypass the automatic checks** (no `--no-verify`, no editing the guard files to silence a block).
7. **Report any accidental disclosure immediately** to Alexandre, who informs the client as the NDA
   requires (§6).
8. **At the end of the engagement, delete everything** (NDA §5): see the checklist below.

## What is enforced automatically

| Protection | What it does |
|---|---|
| Git hooks (`.githooks/`, installed at setup) | Before each commit and push: block data files, files over 1 MB, notebook outputs and real names (checked against `tools/blocked_terms.sha256`, which holds hashes only); block direct pushes to `main`. |
| GitHub check (`confidentiality-guard`) | Runs the same checks on every pull request and on `main`. |
| Protected `main` | Changes only through a pull request with the check passing. Nobody can push directly. |
| AI read restrictions | Claude Code cannot read `data/` (`.claude/settings.json`); Cursor's AI ignores `data/` and `private/` (`.cursorignore`); Codex follows `AGENTS.md`. |
| Drive sharing | Restricted to named team members. Raw data folders are read-only for teammates. |

These checks prevent accidents. They cannot stop someone who deliberately copies a file: that is
what the NDA, and this signed policy, are for.

## End of engagement checklist (NDA §5)

- [ ] Alexandre deletes the GitHub repository: `gh repo delete alexandreandre/ops-consulting-oos`
- [ ] Alexandre deletes the team data folder in Google Drive (name in `private/KEY.md`), then empties the Drive trash.
- [ ] Each member deletes their local clone (with its data links), downloaded files, Excel working files, and empties the computer's trash.
- [ ] Each member deletes AI chat histories that mention project data (ChatGPT/Codex, Claude, Cursor).
- [ ] Each member revokes tool access no longer needed (e.g. rclone at https://myaccount.google.com/permissions; sign out of Google Drive for desktop if unused).
- [ ] Each member confirms to Alexandre that deletion is complete.

## Acknowledgement

By adding my name below through a pull request, I confirm that I have read this policy and the
NDA, and that I will follow them. Git records who added each line and when.

| Name | GitHub | Date |
|---|---|---|
| Alexandre André | alexandreandre | 2026-10-12 |
