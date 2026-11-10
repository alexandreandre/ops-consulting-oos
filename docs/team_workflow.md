# Team workflow

## Rules

- **`main` is the stable version.** It is protected: it changes only through a pull request whose
  `confidentiality-guard` check is green. No human review is required to merge; nobody waits for one.
- **Speed between teammates goes through shared branches, not `main`.** One branch per topic,
  named `<firstname>/<topic>`, e.g. `sying/eda-distributor-c`. Everyone working on that topic
  pulls it at the start and pushes it when a step reads well. Teammates may push to each other's
  branches (Lena can push to Alexandre's).
- **One commit per readable step**: a notebook section, a decision, a script, a doc. Not every
  keystroke, not the whole distributor at the end. Short imperative messages:
  `Add EDA sections for Distributor C orders`.
- **Merge into `main`** only when the step is coherent and the guard is green.
- **No client data, ever**: check `git status` before each commit. The guard blocks data files,
  notebook outputs and real names automatically; never bypass it with `--no-verify`.
- **No real client, distributor or stakeholder names** in files, commits, branches or PRs.
- Record assumptions in `open_questions.md` and decisions in `decisions.md`.
- **Conflict on pull:** stop and ask. Never `git push --force` or `git reset --hard`.

The AI assistant does these git steps itself, without being asked.

## Daily loop

```bash
git fetch
git checkout sying/eda-distributor-c      # the branch of the topic
git pull                                  # what teammates pushed on it
# ... work until one step reads on its own ...
git status                                # check: no data files listed
git add notebooks/01_eda_distributor_c.ipynb docs/data_dictionary.md
git commit -m "Add first EDA of Distributor C inventory table"
git push                                  # updates the open pull request
```

## New topic

```bash
git fetch
git checkout main
git pull                                  # latest stable version
git checkout -b sying/eda-distributor-c   # new branch for the topic
# ... first readable step, commit as above ...
git push -u origin sying/eda-distributor-c
# open the pull request once; later pushes update it
```

## Git in 2 minutes (beginner guide)

- **Repository (repo):** the project folder plus its full history.
- **Commit:** a saved snapshot of your changes, with a message explaining what changed. You can always go back to it.
- **Branch:** a parallel copy of the project where you can work without affecting others. `main` is the shared official version.
- **Push:** send your commits from your computer to GitHub.
- **Pull:** download the latest changes from GitHub to your computer.
- **Pull request (PR):** on GitHub, a request to merge your branch into `main`. It shows the changes; teammates can comment. The guard runs on it.
- **Merge:** bringing the branch's changes into `main` once the step is coherent and the guard is green.

If something goes wrong (conflict, wrong commit), stop and ask the team before forcing anything.
