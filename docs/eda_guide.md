# Exploratory data analysis

A short explanation of what we do in Phase 2, before any cleaning.

## What it is

Exploratory data analysis means **looking at a file to understand it**, before changing anything.

You open a distributor file the way you would open an unfamiliar spreadsheet from a colleague: what is this, what does one line mean, what period does it cover, what is counted, and what looks odd? You write that down. You do not fix the file yet.

The aim is a clear picture of the data we received, so the team can decide together what to clean afterwards.

## Why we do it first

The client wants to know why products go out of stock. The files are the only evidence. If we clean or calculate too early, we can erase the clue or invent a pattern that is only a mistake in the export.

A few examples of what exploration is meant to catch:

- A blank cell and a zero are different. Zero stock may be a stockout. A blank may mean "not filled in".
- "Cases" might mean physical cases or 9-liter equivalent cases. The same number is not the same volume.
- Two lines for the same product on the same day might be a duplicate, or two warehouses.
- A fill rate of 100% means nothing until we know what was ordered and what was shipped.

## What to look at

For each sheet, try to answer these in a sentence or two:

1. **One line is…** an order, a product-day, a monthly total, a forecast made on a given date. Say which.
2. **The period is…** from when to when, and whether months are missing.
3. **The quantities are in…** actual cases, 9L cases, bottles, dollars, or order lines.
4. **A stockout would show up as…** zero stock, cases ordered but not shipped, a pick omit, a fill rate under 100%. Name the column.
5. **What looks wrong…** blanks, zeros, duplicates, negatives, values far above the rest, dates outside the period we expect.

That is enough. Charts help only when they make one of these answers obvious, for example orders by month, or how often a quantity is zero.

## How the files differ

Same questions for every file. The thing you are trying to recognize changes:

| File | What you are trying to recognize |
|---|---|
| Distributor A–D | How this distributor records orders, shipments and fill rate. |
| Master Data | What a SKU is: product, size, pack, vintage. Do not turn macros on in the `.xlsm`. |
| Planning | What was forecast, and which replenishment settings exist (ADU, lead time, buffers). A forecast is not a sale. These files are large: one sheet at a time. |

Distributors will not match each other. Different grains and different units are a finding. We align them later, not during exploration.

## What to write, and where

| You found | Write it in |
|---|---|
| What the sheet is, the period, the units, the keys | The notebook, and `data_dictionary.md` |
| Something odd, with a count | The notebook |
| Something only the client or the team can settle | `open_questions.md` |
| A cleaning rule the team has agreed | `decisions.md`, after the meeting, not before |

Use "the client" and "Distributor A–D". Real names stay in `private/KEY.md`. Leave the files in `data/raw/` untouched.

## When to stop

You are done with a file when a teammate who has not opened it can answer: what a line is, which period it covers, which unit it uses, and what you would not trust yet.

Cleaning starts only after the team has read those notes and agreed the rules. Phase 2 does not produce a stockout diagnosis. It produces the right to start one.
