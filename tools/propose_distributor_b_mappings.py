#!/usr/bin/env python3
"""Propose client SKUs for Distributor B's unmapped item codes, for Lisa to approve.

Bridge: item code -> SCC (the distributor's item list, Master Data sheet 2)
-> client SKU (Master Data sheet 1, SCC column). Tested first on the codes that are
already mapped; the script stops if the bridge disagrees with any of them.

Writes data/interim/distributor_b_mapping_proposals.xlsx (git-ignored). Nothing is
applied to the workbook: template v1.1 requires Lisa's approval for provisional mappings.
Reads by position, never by name.

    .venv/bin/python tools/propose_distributor_b_mappings.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
WORKBOOK = ROOT / "data" / "cleaned" / "distributor_b_v1.xlsx"
OUT = ROOT / "data" / "interim" / "distributor_b_mapping_proposals.xlsx"


def norm(series: pd.Series) -> pd.Series:
    text = series.astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    return text.mask(text.isin(["nan", "None", "NaN", ""]))


def main() -> None:
    md_path = next(p for p in (RAW / "master_data").glob("*.xlsm") if not p.name.startswith("~$"))
    main_sheet = pd.read_excel(md_path, sheet_name=0)
    reference = pd.DataFrame({
        "scc": norm(main_sheet.iloc[:, 6]),
        "sap": norm(main_sheet.iloc[:, 13]),
        "sales_text": main_sheet.iloc[:, 14],
        "factor_9l": pd.to_numeric(main_sheet.iloc[:, 24], errors="coerce"),
    }).dropna(subset=["scc", "sap"])
    by_scc = reference.groupby("scc")["sap"].agg(lambda s: sorted(set(s)))
    details = reference.drop_duplicates("sap").set_index("sap")

    item_raw = pd.read_excel(md_path, sheet_name=1, header=None)
    items = item_raw.iloc[3:, [0, 1, 8, 9, 10]].copy()
    items.columns = ["item", "scc", "item_description", "purchasing", "sales"]
    items["item"] = norm(items["item"])
    items["scc"] = norm(items["scc"])
    items = items.dropna(subset=["item"]).drop_duplicates("item").set_index("item")

    clean = pd.read_excel(WORKBOOK, sheet_name="Clean")
    clean["item"] = norm(clean["Dist_Item"])
    codes = clean.groupby("item").agg(
        status=("Map_Status", "first"),
        current_sku=(clean.columns[21], "first"),  # client SKU, column V
        description=("Product_Desc", "first"),
        rows=("Map_Status", "size"),
        ordered=("Cases_Ordered", "sum"),
        oos=("Cases_OOS", "sum"),
    )
    codes["current_sku"] = norm(codes["current_sku"])
    codes["candidates"] = items["scc"].reindex(codes.index).map(by_scc)

    matched = codes[codes["status"] == "MATCHED"]
    one = matched["candidates"].map(lambda v: isinstance(v, list) and len(v) == 1)
    wrong = matched[one & (matched["candidates"].str[0] != matched["current_sku"])]
    if len(wrong):
        raise SystemExit(f"the SCC bridge disagrees with {len(wrong)} existing mappings; not proposing anything")
    print(f"Bridge test: {int(one.sum())} of {len(matched)} mapped codes reproduced, 0 disagreements")

    rows = []
    for item, row in codes[codes["status"].isin(["NOT_FOUND", "AMBIGUOUS"])].iterrows():
        cands = row["candidates"] if isinstance(row["candidates"], list) else []
        if len(cands) == 1:
            proposal = "PROPOSED"
        elif len(cands) > 1:
            proposal = "SEVERAL CANDIDATES"
        else:
            proposal = "NO CANDIDATE"
        first = cands[0] if cands else None
        rows.append({
            "Dist_Item": item,
            "Current status": row["status"],
            "Product_Desc (extract)": row["description"],
            "Item description (item list)": items["item_description"].get(item),
            "Purchasing status": items["purchasing"].get(item),
            "SCC": items["scc"].get(item),
            "Proposal": proposal,
            "Candidate client SKU(s)": ", ".join(cands) if cands else None,
            "Candidate sales text": details["sales_text"].get(first) if len(cands) == 1 else None,
            "Candidate 9L factor": details["factor_9l"].get(first) if len(cands) == 1 else None,
            "Rows": int(row["rows"]),
            "Cases ordered": round(float(row["ordered"]), 3),
            "Cases OOS": round(float(row["oos"]), 3),
            "Approved (Y/N)": None,
            "Reviewer comment": None,
        })
    out = pd.DataFrame(rows).sort_values(["Proposal", "Cases ordered"], ascending=[False, False])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(OUT, engine="openpyxl") as writer:
        out.to_excel(writer, sheet_name="Proposals", index=False)
        note = pd.DataFrame({"How to use": [
            "Proposals for Distributor B item codes that are missing from Master Data column D, or ambiguous.",
            "Bridge: item code -> SCC on the distributor item list -> client SKU with the same SCC in Master Data.",
            f"Tested on the {len(matched)} codes already mapped: same client SKU every time it gives one.",
            "Nothing is applied. Template v1.1: provisional mappings need Lisa's approval.",
            "Fill 'Approved (Y/N)'. Approved rows can then enter the build as a reviewed lookup.",
        ]})
        note.to_excel(writer, sheet_name="Read_me", index=False)
        ws = writer.sheets["Proposals"]
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="5C1F3A")
        for idx, column in enumerate(out.columns, 1):
            lengths = out[column].map(lambda v: len(str(v)) if pd.notna(v) else 0)
            width = max(len(str(column)), int(lengths.quantile(0.9)) if len(out) else 10)
            ws.column_dimensions[get_column_letter(idx)].width = min(max(width + 2, 10), 60)
        ws.freeze_panes = "B2"
        writer.sheets["Read_me"].column_dimensions["A"].width = 110
    print(f"Wrote {OUT.relative_to(ROOT)}: {out['Proposal'].value_counts().to_dict()}")


if __name__ == "__main__":
    main()
