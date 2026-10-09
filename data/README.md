# data/

**Everything in this folder is git-ignored** (except READMEs and `.gitkeep`). Data stays on
each team member's machine or in the team's approved storage, never on GitHub.

| Folder | Purpose | Rule |
|---|---|---|
| `raw/distributor_a/` … `raw/distributor_d/` | Files exactly as received, per distributor | Read-only. Never edit, rename or overwrite. |
| `raw/master_data/` | Client product / SKU master data | Read-only |
| `interim/` | Intermediate outputs during exploration | Disposable, reproducible |
| `cleaned/` | One cleaned version per source table | Produced by documented rules only |
| `standardized/` | Common cross-distributor representation | Only after source differences are understood |

- Keep original file names in `raw/` so every file can be traced back to what the client sent.
- Record each new file in `docs/data_dictionary.md` (no client names, use codes).
- The mapping between codes and real distributors is in `private/KEY.md` (local only).
