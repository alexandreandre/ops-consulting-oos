# data/

**Everything in this folder is git-ignored** (except READMEs and `.gitkeep`). Client data never
goes on GitHub.

## Where the data lives

The **master copy** of all raw files is the team's **LionMail Google Drive** folder. Nothing is
copied by hand: on each computer, *Google Drive for desktop* makes the Drive appear as a local
folder, and each `data/raw/<code>` is a **link** to the matching Drive folder (set up once, see
`docs/onboarding.md`). Files added to the Drive appear for everyone automatically.

| Path | Content | Rule |
|---|---|---|
| `raw/distributor_a` … `raw/distributor_d` | Link to that distributor's Drive folder | **Read-only.** Never edit, rename, move or delete: it changes the Drive for the whole team. |
| `raw/master_data` | Link to the Master Data Drive folder | Read-only |
| `interim/` | Local intermediate outputs | Disposable, reproducible |
| `cleaned/` | Local cleaned tables | Produced by documented rules only |
| `standardized/` | Common cross-distributor representation | Only after source differences are understood |

## Loading files without leaking names

Drive file names may contain real company names. Never type them in notebooks: select files with a
pattern on the rest of the name.

```python
from pathlib import Path
RAW_C = Path("data/raw/distributor_c")
inventory_file = next(RAW_C.glob("*Inventory*"))
```

The same applies to sheet and column names that contain a real name: reference them by position.

- Record each file in `docs/data_dictionary.md`, with real names replaced by codes.
- Codes, real names and Drive folders are mapped in `private/KEY.md` (local only).
