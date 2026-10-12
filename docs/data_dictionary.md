# Data dictionary

Preliminary inventory. **Only fill in what has been verified in the files.** Use codes, never real
names. "?" = not yet known.

## Sources

| Code | Owner | Raw folder | Status |
|---|---|---|---|
| Distributor A | Alexandre | `data/raw/distributor_a/` | Files received, not yet documented |
| Distributor B | Alexandre | `data/raw/distributor_b/` | Files received, not yet documented |
| Distributor C | Sying | `data/raw/distributor_c/` | Files received, not yet documented |
| Distributor D | Sying | `data/raw/distributor_d/` | Files received, not yet documented |
| Master Data | Lisa | `data/raw/master_data/` | Files received, not yet documented |
| Planning | Team | `data/raw/planning/` | Files received, not yet documented |

## Files received (client file share, inventory of 2026-10-12)

Metadata only, as listed on the client's file share. Real file names are in `private/KEY.md`.

| Code | Content | Format | Size | File date |
|---|---|---|---|---|
| Distributor A | Fill-rate data | .xlsx | 1.98 MB | 2026-10-02 |
| Distributor B | Fill-rate data | .xlsx | 475 KB | 2026-10-02 |
| Distributor C | Fill-rate data | .xlsx | 3.60 MB | 2026-10-12 |
| Distributor D | Fill-rate data | .xlsx | 2.17 MB | 2026-10-02 |
| Master Data | Product / SKU master data | .xlsm (macro-enabled: never enable macros) | 5.80 MB | 2026-10-09 |
| Planning | Default sourcing matrix | .xlsx | 40.9 MB | 2026-10-09 |
| Planning | Historical forecast snapshots | .xlsx | 40.8 MB | 2026-10-09 |
| Planning | MVP parameters | .xlsx | 7.88 MB | 2026-10-02 |

The four fill-rate files were previously named with a `2026.08` prefix on the client side.

## Files

Copy one block per file.

### `<file name>`

| Field | Value |
|---|---|
| Source | ? (client / distributor / system export) |
| Distributor | ? |
| Business meaning | ? (e.g. inventory snapshot, orders, shipments, OOS report, buffer parameters) |
| Granularity (one row = …) | ? |
| Time coverage | ? |
| Key columns | ? |
| Units | ? (actual cases, 9L cases, bottles, $) |
| Known limitations | ? |
| Owner | ? |
| Date received | ? |

## Column notes

For important columns, record: name, type, meaning, example (non-sensitive), missing-value
meaning, open questions.
