# Team workflow

## Rules

- `main` is the stable reference. No direct commits to `main`.
- One **branch** per meaningful contribution, named `<name>/<topic>`, e.g. `sying/eda-distributor-c`.
- Open a **pull request (PR)** to merge into `main`; at least one teammate reviews it.
- Clear, short **commit messages** in the imperative: `Add EDA sections for Distributor C orders`.
- **No client data, ever**: check `git status` before each commit. Clear notebook outputs.
- **No real client, distributor or stakeholder names** in files, commits, branches or PRs.
- Record assumptions in `open_questions.md` and decisions in `decisions.md`.

## Daily loop

```bash
git checkout main
git pull                                  # get the latest main
git checkout -b sying/eda-distributor-c   # new branch for your work
# ... work ...
git status                                # check: no data files listed
git add notebooks/01_eda_distributor_c.ipynb docs/data_dictionary.md
git commit -m "Add first EDA of Distributor C inventory table"
git push -u origin sying/eda-distributor-c
# then open a pull request on GitHub
```

## Git in 2 minutes (beginner guide)

- **Repository (repo):** the project folder plus its full history.
- **Commit:** a saved snapshot of your changes, with a message explaining what changed. You can always go back to it.
- **Branch:** a parallel copy of the project where you can work without affecting others. `main` is the shared official version.
- **Push:** send your commits from your computer to GitHub.
- **Pull:** download the latest changes from GitHub to your computer.
- **Pull request (PR):** on GitHub, a request to merge your branch into `main`. Teammates read the changes, comment, then approve.
- **Merge:** bringing the branch's changes into `main` once the PR is approved.

If something goes wrong (conflict, wrong commit), stop and ask the team before forcing anything.
