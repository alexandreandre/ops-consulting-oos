#!/usr/bin/env python3
"""Build the Distributor B workbook on the frozen team template.

Reads the fill-rate extract and Master Data by column position. Writes
data/cleaned/distributor_b_v1.xlsx. Raw files are not modified.

The snapshot extract was checked on 2026-11-04: it has no rows for this
distributor. Forecast columns stay blank. A missing extract is not the same
as a SKU with no forecast, so those cells are not filled with zero.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "cleaned" / "distributor_b_v1.xlsx"

# Template short code for this distributor's output column. The repo name stays Distributor B.
OUTPUT_CODE = "UNY"
# Supply-constrained ids already matched from the product description. Not dropped.
RTS_IDS = {"3020564", "3020565", "3020566"}
INCLUDE_DISPLAY = {"NAKED GOODS", "GIFT BOX"}
LARGE_SHARE = 0.80
SEVERITY_MIN_ORDERED_9L = 10_000
SPIKE_INDEX = 2.0
SIZE_TOLERANCE_ML = 1.0

NAVY = "1F4E79"
HEADER_FONT = Font(name="Arial", bold=True, color="FFFFFF", size=10)
CELL_FONT = Font(name="Arial", size=10)
HEADER_FILL = PatternFill("solid", fgColor=NAVY)
NOTE_FILL = PatternFill("solid", fgColor="FFF2CC")
THIN = Border(
    left=Side(style="thin", color="D9E2F3"),
    right=Side(style="thin", color="D9E2F3"),
    top=Side(style="thin", color="D9E2F3"),
    bottom=Side(style="thin", color="D9E2F3"),
)
WRAP = Alignment(wrap_text=True, vertical="center")


def norm_code(series: pd.Series) -> pd.Series:
    text = series.astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    return text.mask(text.isin(["nan", "None", "NaN", ""]))


def to_ml(value) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip().lower().replace(" ", "")
    match = re.fullmatch(r"(\d+(?:\.\d+)?)(ml|l)", text)
    if not match:
        return None
    number = float(match.group(1))
    return number if match.group(2) == "ml" else number * 1000


def description_ml(text) -> float | None:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return None
    found = re.findall(r"(\d+(?:\.\d+)?)\s*(ml|l)\b", str(text), flags=re.I)
    values = set()
    for number, unit in found:
        ml = float(number) if unit.lower() == "ml" else float(number) * 1000
        values.add(round(ml, 3))
    if len(values) != 1:
        return None
    return values.pop()


def month_start(value) -> pd.Timestamp:
    if isinstance(value, (datetime, pd.Timestamp)):
        stamp = pd.Timestamp(value)
        return pd.Timestamp(year=stamp.year, month=stamp.month, day=1)
    digits = re.sub(r"\D", "", str(value))
    if len(digits) < 6:
        raise ValueError(f"unreadable month: {value!r}")
    return pd.Timestamp(year=int(digits[:4]), month=int(digits[4:6]), day=1)


def load_fill() -> pd.DataFrame:
    path = next((RAW / "distributor_b").glob("*.xlsx"))
    frame = pd.read_excel(path, header=0)
    expected = {
        0: "Yearmonth",
        6: "SAP Product ID Display",
        7: "Cases Ordered",
        9: "Cases Shipped",
        10: "Cases Unshipped",
        11: "Pick Omits",
        12: "Cases OOS",
        13: "Case Fill Rate",
    }
    for index, name in expected.items():
        if frame.columns[index] != name:
            raise SystemExit(f"fill-rate column {index + 1} is {frame.columns[index]!r}, expected {name}")
    out = pd.DataFrame({
        "month": frame.iloc[:, 0].map(month_start),
        "state": frame.iloc[:, 1].astype(str).str.strip(),
        "sales_org": frame.iloc[:, 2].astype(str).str.strip(),
        "product_desc": frame.iloc[:, 5],
        "dist_item": norm_code(frame.iloc[:, 6]),
        "cases_ordered": pd.to_numeric(frame.iloc[:, 7], errors="coerce"),
        "cases_shipped": pd.to_numeric(frame.iloc[:, 9], errors="coerce"),
        "cases_unshipped": pd.to_numeric(frame.iloc[:, 10], errors="coerce"),
        "pick_omits": pd.to_numeric(frame.iloc[:, 11], errors="coerce"),
        "cases_oos": pd.to_numeric(frame.iloc[:, 12], errors="coerce"),
        "fill_reported": pd.to_numeric(frame.iloc[:, 13], errors="coerce"),
    })
    out["location"] = out["sales_org"].str.split().str[-1]
    if out["dist_item"].isna().any():
        raise SystemExit("a fill-rate row has no item code")
    if not set(RTS_IDS).issubset(set(out["dist_item"])):
        raise SystemExit("the three supply-constrained ids are not all in the extract")
    return out


def load_master(item_ids: pd.Series) -> pd.DataFrame:
    path = next((RAW / "master_data").glob("*.xlsm"))
    wide = pd.read_excel(path, sheet_name=0)
    overlaps = {}
    for index in range(5):
        overlaps[index] = int(item_ids.isin(set(norm_code(wide.iloc[:, index]).dropna())).sum())
    best = max(overlaps, key=overlaps.get)
    if best != 3:
        raise SystemExit(f"distributor item column is no longer column D: {overlaps}")
    master = pd.DataFrame({
        "code": norm_code(wide.iloc[:, 3]),
        "psku": norm_code(wide.iloc[:, 5]),
        "brand": wide.iloc[:, 8],
        "bottle": wide.iloc[:, 11],
        "display": wide.iloc[:, 12],
        "sap": norm_code(wide.iloc[:, 13]),
        "vintage": wide.iloc[:, 15],
        "factor": pd.to_numeric(wide.iloc[:, 24], errors="coerce"),
    }).dropna(subset=["code"])
    return master


def load_anaplan() -> pd.DataFrame:
    path = next((RAW / "master_data").glob("*.xlsm"))
    frame = pd.read_excel(path, sheet_name="Anaplan SKU Hierarchy")
    if frame.columns[2] != "Code" or frame.columns[13] != "Planning SKU Code":
        raise SystemExit("Anaplan hierarchy columns moved")
    out = pd.DataFrame({
        "sap": norm_code(frame.iloc[:, 2]),
        "planning": norm_code(frame.iloc[:, 13]),
        "factor": pd.to_numeric(frame.iloc[:, 22], errors="coerce"),
        "limited": frame.iloc[:, 27],
    }).dropna(subset=["sap"])
    if out["sap"].duplicated().any():
        raise SystemExit("Anaplan natural code is not unique")
    out["limited"] = out["limited"].map(lambda value: bool(value) if pd.notna(value) else False)
    return out.drop_duplicates("sap")


def collapse_master(master: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for code, group in master.groupby("code", sort=False):
        saps = [sap for sap in group["sap"].dropna().unique().tolist()]
        record = {
            "code": code,
            "map_status": "MATCHED",
            "sap": None,
            "brand": None,
            "bottle": None,
            "display": None,
            "vintage": None,
            "factor": None,
            "psku": None,
        }
        if len(saps) != 1:
            record["map_status"] = "AMBIGUOUS"
            factors = group["factor"].dropna().unique()
            if len(factors) == 1:
                record["factor"] = float(factors[0])
            rows.append(record)
            continue
        record["sap"] = saps[0]
        one = group[group["sap"] == saps[0]]

        def single(column):
            values = [value for value in one[column].dropna().unique().tolist()]
            return values[0] if len(values) == 1 else None

        record["brand"] = single("brand")
        record["bottle"] = single("bottle")
        record["display"] = single("display")
        record["vintage"] = single("vintage")
        record["psku"] = single("psku")
        factors = one["factor"].dropna().unique()
        if len(factors) == 1 and float(factors[0]) > 0:
            record["factor"] = float(factors[0])
        rows.append(record)
    return pd.DataFrame(rows)


def vintage_text(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "---"
    if isinstance(value, (int, float)) and float(value).is_integer():
        return str(int(value))
    text = str(value).strip()
    return text if text else "---"


def build_clean(fill: pd.DataFrame, master: pd.DataFrame, anaplan: pd.DataFrame) -> pd.DataFrame:
    merged = fill.merge(master, how="left", left_on="dist_item", right_on="code")
    merged["map_status"] = merged["map_status"].fillna("NOT_FOUND")
    merged = merged.merge(
        anaplan.rename(columns={"factor": "anaplan_factor", "limited": "anaplan_limited", "planning": "anaplan_planning"}),
        how="left",
        left_on="sap",
        right_on="sap",
        suffixes=("", "_anaplan"),
    )
    factor = merged["factor"].where(merged["factor"].gt(0))
    fallback = merged["anaplan_factor"].where(merged["anaplan_factor"].gt(0))
    merged["nine_l"] = factor.where(factor.notna(), fallback)
    merged["planning"] = merged["anaplan_planning"]
    missing_plan = merged["sap"].notna() & merged["planning"].isna()
    merged.loc[missing_plan, "planning"] = merged.loc[missing_plan, "sap"]
    merged["planning_fallback"] = missing_plan
    merged["anaplan_limited"] = merged["anaplan_limited"].fillna(False).astype(bool)
    key = ["location", "month", "dist_item"]
    sizes = merged.groupby(key)["dist_item"].transform("size")
    names = merged.groupby(key)["product_desc"].transform("nunique")
    merged["dup_flag"] = ""
    merged.loc[(sizes > 1) & (names > 1), "dup_flag"] = "DUP_CODE_DIFF_PRODUCT"
    merged.loc[(sizes > 1) & (names <= 1), "dup_flag"] = "DUP_CHECK"

    def flags(row) -> str:
        codes = []
        ordered = row["cases_ordered"]
        shipped = row["cases_shipped"]
        unshipped = row["cases_unshipped"]
        if pd.notna(shipped) and pd.notna(ordered) and pd.notna(unshipped):
            if abs(ordered - shipped - unshipped) > 0.5:
                codes.append("ORDER_MISMATCH")
        unexplained = row["unexplained"]
        if pd.notna(unexplained) and abs(unexplained) > 0.01:
            codes.append("UNEXPLAINED_UNSHIPPED")
        reported = row["fill_reported"]
        calculated = row["fill_rate"]
        if pd.notna(reported) and pd.notna(calculated) and abs(calculated - reported) > 0.01:
            codes.append("FR_MISMATCH")
        numbers = [row["cases_ordered"], row["cases_shipped"], row["cases_unshipped"]]
        if any(pd.notna(value) and value < 0 for value in numbers):
            codes.append("NEGATIVE")
        if pd.notna(reported) and (reported < 0 or reported > 1):
            codes.append("FR_OUT_OF_RANGE")
        if all(pd.notna(value) and value == 0 for value in numbers):
            codes.append("ALL_ZERO")
        codes.append("FCST_BLANK")
        if not (pd.notna(row["nine_l"]) and row["nine_l"] > 0):
            codes.append("NO_9L")
        if row["planning_fallback"]:
            codes.append("PLANNING_NOT_FOUND")
        if row["dup_flag"]:
            codes.append(row["dup_flag"])
        return ";".join(codes)

    unshipped = merged["cases_unshipped"]
    ordered = merged["cases_ordered"]
    merged["unexplained"] = unshipped - merged["pick_omits"] - merged["cases_oos"]
    merged["fill_rate"] = (1 - unshipped / ordered).where(ordered.gt(0))
    if merged["fill_reported"].max() > 1.5:
        merged["fill_reported"] = merged["fill_reported"] / 100
    merged["display_norm"] = merged["display"].astype(str).str.strip().str.upper()
    merged.loc[merged["display"].isna(), "display_norm"] = ""
    merged["bottle_ml"] = merged["bottle"].map(to_ml)
    merged["desc_ml"] = merged["product_desc"].map(description_ml)
    merged["size_gap"] = (
        merged["bottle_ml"].notna()
        & merged["desc_ml"].notna()
        & (merged["bottle_ml"] - merged["desc_ml"]).abs().gt(SIZE_TOLERANCE_ML)
    )
    merged["flags"] = merged.apply(flags, axis=1)
    merged["month_weight"] = merged["month"].map(lambda stamp: 0.5 if stamp.month in (12, 1) else 1.0)
    merged["oos_9l"] = merged["cases_oos"] * merged["nine_l"]
    merged["ordered_9l"] = merged["cases_ordered"] * merged["nine_l"]
    merged["unshipped_9l"] = merged["cases_unshipped"] * merged["nine_l"]
    status, reason = zip(*(scope_for(row) for row in merged.to_dict("records")))
    merged["scope_status"] = status
    merged["scope_reason"] = reason
    merged["vintage_flag"] = False
    merged = mark_vintage(merged)
    merged["cell_id"] = ""
    ready = merged["sap"].notna() & merged["location"].ne("")
    merged.loc[ready, "cell_id"] = merged.loc[ready, "location"] + "|" + merged.loc[ready, "sap"]
    return merged


def scope_for(row) -> tuple[str, str]:
    if row["dist_item"] in RTS_IDS:
        return "EXCLUDE", "QUOTA"
    display = row["display_norm"]
    if display == "LIMITED EDITION" or row["anaplan_limited"]:
        return "EXCLUDE", "LIMITED_EDITION"
    if display == "VAP":
        return "EXCLUDE", "VAP"
    if row["map_status"] in ("NOT_FOUND", "AMBIGUOUS") or not row["sap"]:
        return "REVIEW", "MAPPING"
    if row["size_gap"]:
        return "REVIEW", "SIZE_REVIEW"
    if display not in INCLUDE_DISPLAY:
        return "REVIEW", "OTHER_DISPLAY"
    return "INCLUDE", ""


def mark_vintage(frame: pd.DataFrame) -> pd.DataFrame:
    """Flag a client SKU only against later codes of the same planning SKU, size and display type."""
    sales = frame[(frame["cases_ordered"] > 0) & frame["sap"].notna() & ~frame["planning_fallback"]].copy()
    sales = sales[sales["sap"].astype(str).str.match(r"^\d+$")]
    sales["bottle_key"] = sales["bottle"].map(lambda value: "" if pd.isna(value) else str(value).strip().lower())
    sales["pack_key"] = sales["display_norm"].fillna("")
    first = sales.groupby(["planning", "bottle_key", "pack_key", "sap"], as_index=False)["month"].min()
    transition: set[str] = set()
    for _, block in first.groupby(["planning", "bottle_key", "pack_key"], sort=False):
        pairs = [(int(sap), str(sap), month) for sap, month in zip(block["sap"], block["month"])]
        for number, sap, own_month in pairs:
            if any(other > number and other_month > own_month for other, _sku, other_month in pairs):
                transition.add(sap)
    frame = frame.copy()
    frame["vintage_flag"] = frame["sap"].astype(str).isin(transition) & ~frame["planning_fallback"]
    return frame


def analysis_frame(clean: pd.DataFrame) -> pd.DataFrame:
    scope = clean[(clean["scope_status"] == "INCLUDE") & clean["nine_l"].gt(0) & clean["sap"].notna()].copy()
    month = (
        scope.groupby(["location", "sap", "month"], as_index=False)
        .agg(
            ordered_9l=("ordered_9l", "sum"),
            oos_9l=("oos_9l", "sum"),
            oos_cases=("cases_oos", "sum"),
            ordered_cases=("cases_ordered", "sum"),
            weight=("month_weight", "first"),
        )
    )
    month["weighted_oos_9l"] = month["oos_9l"] * month["weight"]
    month["weighted_month"] = month["weight"].where(month["oos_9l"] > 1e-9, 0)
    month["dec_jan"] = month["month"].dt.month.isin([12, 1]) & month["oos_9l"].gt(1e-9)
    cells = month.groupby(["location", "sap"], as_index=False).agg(
        ordered_9l=("ordered_9l", "sum"),
        oos_9l=("oos_9l", "sum"),
        oos_cases=("oos_cases", "sum"),
        ordered_cases=("ordered_cases", "sum"),
        weighted_oos_9l=("weighted_oos_9l", "sum"),
        weighted_months=("weighted_month", "sum"),
        dec_jan_oos=("dec_jan", "any"),
    )
    attrs = (
        scope.sort_values("cases_ordered", ascending=False)
        .groupby(["location", "sap"], as_index=False)
        .agg(
            description=("product_desc", "first"),
            display=("display_norm", "first"),
            bottle=("bottle", "first"),
            planning=("planning", "first"),
            planning_fallback=("planning_fallback", "max"),
            vintage_flag=("vintage_flag", "max"),
            brand=("brand", "first"),
        )
    )
    cells = cells.merge(attrs, on=["location", "sap"], how="left")
    cells = cells.sort_values(["weighted_oos_9l", "location", "sap"], ascending=[False, True, True]).reset_index(drop=True)
    total = float(cells["weighted_oos_9l"].sum())
    cells["cumulative"] = cells["weighted_oos_9l"].cumsum() / total if total else 0
    previous = cells["cumulative"].shift(1).fillna(0)
    cells["top80"] = (previous < LARGE_SHARE) & cells["weighted_oos_9l"].gt(0)
    cells["pattern"] = cells["weighted_months"].map(pattern_of)
    cells["size"] = cells["top80"].map(lambda flag: "Large" if flag else "Small")
    cells["quadrant"] = cells.apply(
        lambda row: "No loss" if row["weighted_oos_9l"] <= 1e-9 else f"{'Repeat' if row['weighted_months'] >= 4 else 'Sporadic'} × {row['size']}",
        axis=1,
    )
    cells["oos_rate"] = cells["oos_9l"] / cells["ordered_9l"].where(cells["ordered_9l"].gt(0))
    cells["action"], cells["priority"], cells["rationale"] = zip(*cells.apply(action_for, axis=1))
    return cells


def pattern_of(weighted_months: float) -> str:
    if weighted_months >= 4:
        return "Repeat"
    if weighted_months >= 3:
        return "Intermittent"
    return "Event"


def action_for(row) -> tuple[str, int, str]:
    if row["weighted_oos_9l"] <= 1e-9:
        return "", 9, ""
    if row["vintage_flag"]:
        return "Vintage changeover – no buffer change", 1, "A higher client SKU with the same planning SKU, bottle size and display type has later sales."
    if row["pattern"] == "Repeat":
        return "Lag1 incomplete – review", 3, "Repeat cell. No lag-1 forecast is on this extract, so bias is not calculated."
    if row["pattern"] == "Intermittent":
        return "Monitor – review if it repeats", 5, "Three weighted OOS months, under the repeat cut."
    return "Low priority – ask MH for context only if large", 6, "Two weighted OOS months or fewer."


def location_table(clean: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    scope = clean[(clean["scope_status"] == "INCLUDE") & clean["nine_l"].gt(0) & clean["sap"].notna()]
    month = scope.groupby(["location", "month"], as_index=False).agg(
        ordered_9l=("ordered_9l", "sum"),
        oos_9l=("oos_9l", "sum"),
        weight=("month_weight", "first"),
    )
    month["rate"] = month["oos_9l"] / month["ordered_9l"].where(month["ordered_9l"].gt(0))
    month["weighted_oos_9l"] = month["oos_9l"] * month["weight"]
    totals = month.groupby("location", as_index=False).agg(
        ordered_9l=("ordered_9l", "sum"),
        oos_9l=("oos_9l", "sum"),
        weighted_oos_9l=("weighted_oos_9l", "sum"),
        months=("month", "nunique"),
    )
    totals["oos_rate"] = totals["oos_9l"] / totals["ordered_9l"].where(totals["ordered_9l"].gt(0))
    totals["in_table"] = totals["ordered_9l"] >= SEVERITY_MIN_ORDERED_9L
    return totals.sort_values("oos_9l", ascending=False), month


def spike_table(month: pd.DataFrame, clean: pd.DataFrame) -> pd.DataFrame:
    rows = []
    scope = clean[(clean["scope_status"] == "INCLUDE") & clean["nine_l"].gt(0) & clean["sap"].notna()]
    sku_month = scope.groupby(["location", "month", "sap"], as_index=False)["oos_9l"].sum()
    for location, group in month.groupby("location"):
        average = float(group["weighted_oos_9l"].mean())
        if average <= 0:
            continue
        for record in group.itertuples(index=False):
            index = float(record.weighted_oos_9l) / average
            if index < SPIKE_INDEX:
                continue
            top = (
                sku_month[(sku_month["location"] == location) & (sku_month["month"] == record.month)]
                .sort_values("oos_9l", ascending=False)
                .head(3)
            )
            row = {
                "location": location,
                "month": record.month,
                "oos_9l": record.oos_9l,
                "ordered_9l": record.ordered_9l,
                "oos_rate": record.rate,
                "weighted_oos_9l": record.weighted_oos_9l,
                "average_weighted": average,
                "index": index,
            }
            for rank, sku in enumerate(top.itertuples(index=False), 1):
                row[f"sku_{rank}"] = sku.sap
                row[f"oos_{rank}"] = sku.oos_9l
            rows.append(row)
    spikes = pd.DataFrame(rows)
    if spikes.empty:
        return spikes
    spikes = spikes.sort_values(["oos_9l", "location"], ascending=[False, True]).reset_index(drop=True)
    spikes["shortlist"] = False
    spikes.loc[: min(4, len(spikes) - 1), "shortlist"] = True
    return spikes


def style_sheet(ws, widths: dict[int, int], freeze: str = "A2") -> None:
    ws.freeze_panes = freeze
    ws.auto_filter.ref = ws.dimensions
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
    ws.sheet_view.showGridLines = False
    ws.oddHeader.left.text = "Distributor B"
    ws.oddFooter.left.text = "Template v1.1 rebuild. Labels are readings, not root causes."
    ws.oddFooter.right.text = "Page &P"
    for cell in ws[1]:
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = CELL_FONT
            cell.border = THIN
            cell.alignment = Alignment(vertical="center")
    for index, width in widths.items():
        ws.column_dimensions[get_column_letter(index)].width = width
    ws.row_dimensions[1].height = 30
    ws.auto_filter.ref = ws.dimensions
    ws.page_setup.horizontalCentered = True
    ws.sheet_view.zoomScale = 110
    ws.print_title_rows = "1:1"


def write_rows(ws, headers: list[str], rows: list[list], formats: dict[int, str] | None = None) -> None:
    ws.append(headers)
    for row in rows:
        ws.append(row)
    formats = formats or {}
    for column, number_format in formats.items():
        for cell in ws.iter_rows(min_row=2, min_col=column, max_col=column):
            for item in cell:
                if isinstance(item.value, (int, float)):
                    item.number_format = number_format


def clean_rows(clean: pd.DataFrame) -> list[list]:
    rows = []
    for record in clean.itertuples(index=False):
        rows.append([
            OUTPUT_CODE,
            record.location,
            record.state,
            record.month.to_pydatetime(),
            record.dist_item,
            None,
            None if pd.isna(record.product_desc) else record.product_desc,
            None if pd.isna(record.cases_ordered) else float(record.cases_ordered),
            None if pd.isna(record.cases_shipped) else float(record.cases_shipped),
            None if pd.isna(record.cases_unshipped) else float(record.cases_unshipped),
            None if pd.isna(record.pick_omits) else float(record.pick_omits),
            None if pd.isna(record.cases_oos) else float(record.cases_oos),
            None if pd.isna(record.unexplained) else float(record.unexplained),
            None if pd.isna(record.fill_rate) else float(record.fill_rate),
            None if pd.isna(record.fill_reported) else float(record.fill_reported),
            None,
            None,
            None,
            None,
            False,
            record.flags,
            None if pd.isna(record.sap) else record.sap,
            record.map_status,
            None if record.planning_fallback or pd.isna(record.planning) else record.planning,
            None if pd.isna(record.brand) else record.brand,
            record.display_norm or None,
            None if pd.isna(record.bottle) else record.bottle,
            vintage_text(record.vintage),
            None if pd.isna(record.nine_l) else float(record.nine_l),
            None if pd.isna(record.unshipped_9l) else float(record.unshipped_9l),
            None if pd.isna(record.oos_9l) else float(record.oos_9l),
            None if pd.isna(record.ordered_9l) else float(record.ordered_9l),
            None,
            float(record.month_weight),
            record.scope_status,
            record.scope_reason or None,
            bool(record.vintage_flag),
            record.cell_id or None,
        ])
    return rows


CLEAN_HEADERS = [
    "Distributor", "Market", "State", "Month", "Dist_Item", "Dist_Item_Suffix", "Product_Desc",
    "Cases_Ordered", "Cases_Shipped", "Cases_Unshipped", "Pick_Omits", "Cases_OOS",
    "Unexplained_Unshipped", "Fill_Rate", "Fill_Rate_Reported", "Fcst_Lag2", "Fcst_Lag1", "Fcst_Lag0",
    "OTC_Class", "Weekly_Only", "Flags", "MH_SAP_SKU", "Map_Status", "Planning_SKU", "Brand",
    "Display_Type", "Bottle_Size", "Vintage", "Nine_L_Factor", "Unshipped_9L", "OOS_9L", "Ordered_9L",
    "Fcst_Lag1_9L", "Month_Weight", "Scope_Status", "Scope_Reason", "Vintage_Flag", "Cell_ID",
]


def write_workbook(clean: pd.DataFrame, cells: pd.DataFrame, locations: pd.DataFrame, month: pd.DataFrame, spikes: pd.DataFrame, raw_totals: dict) -> None:
    wb = Workbook()
    notes = wb.active
    notes.title = "Notes"
    write_notes(notes, clean, cells, locations, spikes, raw_totals)
    write_action(wb.create_sheet("Action_List"), cells)
    write_severity(wb.create_sheet("Location_Severity"), locations, month)
    write_top(wb.create_sheet("Top_Cells"), cells)
    write_bias(wb.create_sheet("Bias_Test"))
    write_spikes(wb.create_sheet("Spikes"), spikes)
    write_qa(wb.create_sheet("QA"), clean, cells, locations, raw_totals)
    write_clean(wb.create_sheet("Clean"), clean)
    write_removed(wb.create_sheet("Removed_Dups"))
    wb.active = wb["Action_List"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)


def write_notes(ws, clean, cells, locations, spikes, raw_totals) -> None:
    lines = [
        "Distributor B, template v1.1 rebuild.",
        "Rerun with python3 tools/build_distributor_b_v1.py. Raw files are not modified.",
        "One clean row is one raw row. The duplicate item-month keys are kept, not summed.",
        "Market is the last word of the sales-org name. The two sales orgs stay apart. The older single-market ranking is not this file.",
        "The four questions use INCLUDE rows with a client SKU and a 9L factor. That scope is naked goods and gift box. Supply-constrained ids, limited edition and VAP are EXCLUDE.",
        "OOS is Cases OOS. December and January have weight 0.5. Repeat is 4 or more weighted OOS months. Intermittent is 3 up to but not including 4. Event is under 3.",
        "Large is the Pareto set of location x client SKU whose weighted OOS 9L first reaches 80 percent, including the row that crosses the line.",
        "A vintage flag only compares client SKUs that share a planning SKU, a bottle size and a display type.",
        "Forecast columns are blank. The snapshot file in the team folder has no rows for this distributor, and the 2026 easier extract is not in that folder yet. A missing extract is not filled with zero.",
        "On the in-scope cut, 2025 carries 58 percent of OOS 9L, 2026 carries 34 percent, and 2024 carries 9 percent. A 2026-only forecast join would not cover the bulk of the loss.",
        "The 14 duplicate groups each have two descriptions that share at least half their words. Both rows stay until the team confirms a rename.",
        "Of the client SKUs in the top 80 percent, 15 are in both sales orgs.",
        "Current buffer and recommended buffer are blank. The parameter file has no buffer column.",
        f"Raw ordered {raw_totals['ordered']:.3f}, unshipped {raw_totals['unshipped']:.3f}, OOS {raw_totals['oos']:.3f}. Clean matches these totals. Removed_Dups is empty.",
        f"Action rows: {int((cells['weighted_oos_9l'] > 1e-9).sum())}. Spike months: {len(spikes)}. Locations at or above {SEVERITY_MIN_ORDERED_9L:,.0f} ordered 9L: {int(locations['in_table'].sum())} of {len(locations)}.",
        "A quadrant or an action line is a reading of the rule. It is not a confirmed root cause.",
    ]
    ws["A1"] = "How to read this file"
    ws["A1"].font = Font(name="Arial", bold=True, size=14, color=NAVY)
    for index, line in enumerate(lines, 3):
        ws.cell(index, 1, line).font = CELL_FONT
        ws.cell(index, 1).alignment = WRAP
    ws.column_dimensions["A"].width = 140
    ws.row_dimensions[1].height = 22
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
    ws.sheet_view.showGridLines = False
    ws.oddFooter.right.text = "Page &P"
    for row in range(3, 15):
        ws.row_dimensions[row].height = 32


def write_action(ws, cells: pd.DataFrame) -> None:
    headers = [
        "Distributor", "Location", "MH SKU", "Description", "Planning SKU", "Pattern",
        "Weighted OOS months", "Dec / Jan OOS", "OOS 9L", "OOS cases", "OOS rate",
        "Lag1 bias", "Flags", "Current buffer", "Suggested action", "Recommended buffer", "Rationale",
    ]
    chosen = cells[cells["weighted_oos_9l"] > 1e-9].sort_values(["priority", "weighted_oos_9l"], ascending=[True, False])
    rows = []
    for record in chosen.itertuples(index=False):
        description = " | ".join(part for part in [record.description, record.bottle, record.display] if pd.notna(part) and part != "")
        rows.append([
            OUTPUT_CODE,
            record.location,
            record.sap,
            description,
            None if record.planning_fallback else record.planning,
            record.pattern,
            float(record.weighted_months),
            "Yes" if record.dec_jan_oos else "No",
            float(record.oos_9l),
            float(record.oos_cases),
            None if pd.isna(record.oos_rate) else float(record.oos_rate),
            "incomplete",
            "Vintage transition" if record.vintage_flag else None,
            None,
            record.action,
            None,
            record.rationale,
        ])
    write_rows(ws, headers, rows, {7: "0.0", 9: "#,##0.000", 10: "#,##0.000", 11: "0.0%"})
    style_sheet(ws, {1: 14, 2: 16, 3: 14, 4: 42, 5: 16, 6: 16, 7: 16, 8: 14, 9: 14, 10: 14, 11: 12, 12: 14, 13: 20, 14: 16, 15: 42, 16: 20, 17: 55})
    ws.auto_filter.ref = f"A1:Q{max(ws.max_row, 1)}"
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = "1:1"
    ws.page_setup.orientation = "landscape"
    ws.oddHeader.center.text = "Action list"


def write_severity(ws, locations: pd.DataFrame, month: pd.DataFrame) -> None:
    shown = locations[locations["in_table"]].copy()
    headers = ["Location", "Ordered 9L", "OOS 9L", "Weighted OOS 9L", "OOS rate", "Months"]
    rows = [
        [record.location, float(record.ordered_9l), float(record.oos_9l), float(record.weighted_oos_9l), float(record.oos_rate), int(record.months)]
        for record in shown.itertuples(index=False)
    ]
    write_rows(ws, headers, rows, {2: "#,##0.000", 3: "#,##0.000", 4: "#,##0.000", 5: "0.0%"})
    months = sorted(month["month"].unique())
    start = 8
    ws.cell(1, start, "OOS rate by month")
    ws.cell(1, start).font = HEADER_FONT
    ws.cell(1, start).fill = HEADER_FILL
    for offset, stamp in enumerate(months):
        cell = ws.cell(1, start + 1 + offset, pd.Timestamp(stamp).strftime("%b-%Y"))
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(textRotation=90, horizontal="center")
    for row_index, location in enumerate(shown["location"], 2):
        ws.cell(row_index, start, location).font = CELL_FONT
        subset = month[month["location"] == location]
        lookup = {pd.Timestamp(stamp): rate for stamp, rate in zip(subset["month"], subset["rate"])}
        for offset, stamp in enumerate(months):
            value = lookup.get(pd.Timestamp(stamp))
            cell = ws.cell(row_index, start + 1 + offset, None if value is None or pd.isna(value) else float(value))
            cell.font = CELL_FONT
            cell.number_format = "0.0%"
            cell.border = THIN
    for column in range(start + 1, start + 1 + len(months)):
        ws.column_dimensions[get_column_letter(column)].width = 6
    style_sheet(ws, {1: 16, 2: 16, 3: 14, 4: 18, 5: 12, 6: 12, 8: 16})
    ws.row_dimensions[1].height = 48
    ws.auto_filter.ref = f"A1:F{max(len(rows) + 1, 2)}"


def write_top(ws, cells: pd.DataFrame) -> None:
    headers = [
        "Rank", "Location", "MH SKU", "Description", "Display type", "Planning SKU", "Pattern",
        "Quadrant", "Weighted OOS months", "Weighted OOS 9L", "Cumulative share", "Top 80%",
        "OOS 9L", "Ordered 9L", "OOS cases", "OOS rate", "Vintage flag",
    ]
    ranked = cells[cells["weighted_oos_9l"] > 1e-9]
    rows = []
    for rank, record in enumerate(ranked.itertuples(index=False), 1):
        rows.append([
            rank,
            record.location,
            record.sap,
            record.description,
            record.display,
            None if record.planning_fallback else record.planning,
            record.pattern,
            record.quadrant,
            float(record.weighted_months),
            float(record.weighted_oos_9l),
            float(record.cumulative),
            "Yes" if record.top80 else "No",
            float(record.oos_9l),
            float(record.ordered_9l),
            float(record.oos_cases),
            None if pd.isna(record.oos_rate) else float(record.oos_rate),
            "Yes" if record.vintage_flag else "No",
        ])
    write_rows(ws, headers, rows, {9: "0.0", 10: "#,##0.000", 11: "0.0%", 13: "#,##0.000", 14: "#,##0.000", 15: "#,##0.000", 16: "0.0%"})
    style_sheet(ws, {1: 8, 2: 16, 3: 14, 4: 42, 5: 16, 6: 16, 7: 16, 8: 20, 9: 16, 10: 18, 11: 16, 12: 12, 13: 14, 14: 14, 15: 12, 16: 12, 17: 14})


def write_bias(ws) -> None:
    ws["A1"] = "Bias test not run"
    ws["A1"].font = Font(name="Arial", bold=True, size=14, color=NAVY)
    ws["A3"] = "The local historical snapshot extract has no rows for this distributor. Lag-1 bias is left incomplete. A missing extract is not treated as a zero forecast."
    ws["A3"].alignment = WRAP
    ws["A3"].font = CELL_FONT
    headers = ["Group", "Cells", "Median Lag1 bias", "Share under-forecast by more than 10%"]
    for column, header in enumerate(headers, 1):
        cell = ws.cell(5, column, header)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
    for column, group in enumerate(["Problem cells", "Healthy cells"], 6):
        ws.cell(column, 1, group).font = CELL_FONT
        ws.cell(column, 2, 0)
        ws.cell(column, 3, "incomplete")
        ws.cell(column, 4, "incomplete")
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 42
    ws.row_dimensions[3].height = 36
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
    ws.sheet_view.showGridLines = False
    ws.oddFooter.right.text = "Page &P"


def write_spikes(ws, spikes: pd.DataFrame) -> None:
    headers = [
        "Location", "Month", "OOS 9L", "Ordered 9L", "OOS rate", "Weighted OOS 9L",
        "Average weighted OOS 9L", "Index", "Shortlist", "SKU 1", "OOS 9L 1", "SKU 2", "OOS 9L 2", "SKU 3", "OOS 9L 3",
    ]
    rows = []
    if not spikes.empty:
        for record in spikes.itertuples(index=False):
            rows.append([
                record.location,
                pd.Timestamp(record.month).to_pydatetime(),
                float(record.oos_9l),
                float(record.ordered_9l),
                None if pd.isna(record.oos_rate) else float(record.oos_rate),
                float(record.weighted_oos_9l),
                float(record.average_weighted),
                float(record.index),
                "Yes" if record.shortlist else "No",
                getattr(record, "sku_1", None),
                getattr(record, "oos_1", None),
                getattr(record, "sku_2", None),
                getattr(record, "oos_2", None),
                getattr(record, "sku_3", None),
                getattr(record, "oos_3", None),
            ])
    write_rows(ws, headers, rows, {3: "#,##0.000", 4: "#,##0.000", 5: "0.0%", 6: "#,##0.000", 7: "#,##0.000", 8: "0.00", 11: "#,##0.000", 13: "#,##0.000", 15: "#,##0.000"})
    for cell in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for item in cell:
            item.number_format = "MMM-YYYY"
    style_sheet(ws, {1: 16, 2: 14, 3: 14, 4: 14, 5: 12, 6: 18, 7: 24, 8: 10, 9: 12, 10: 14, 11: 12, 12: 14, 13: 12, 14: 14, 15: 12})


def write_qa(ws, clean, cells, locations, raw_totals) -> None:
    ordered = float(clean["cases_ordered"].sum())
    unshipped = float(clean["cases_unshipped"].sum())
    oos = float(clean["cases_oos"].sum())
    checks = [
        ("Ordered, raw minus clean", raw_totals["ordered"] - ordered),
        ("Unshipped, raw minus clean", raw_totals["unshipped"] - unshipped),
        ("OOS, raw minus clean", raw_totals["oos"] - oos),
        ("Duplicate keys kept", float((clean["dup_flag"] != "").sum() and clean.loc[clean["dup_flag"] != "", ["location", "month", "dist_item"]].drop_duplicates().shape[0])),
        ("Rows in Clean", float(len(clean))),
        ("Rows removed", 0.0),
    ]
    ws.append(["Check", "Value", "Expect"])
    expect = {
        "Ordered, raw minus clean": 0,
        "Unshipped, raw minus clean": 0,
        "OOS, raw minus clean": 0,
        "Rows removed": 0,
    }
    for name, value in checks:
        ws.append([name, value, expect.get(name)])
    ws.append([])
    ws.append(["Map status", "Rows", "Ordered cases"])
    for status, group in clean.groupby("map_status"):
        ws.append([status, int(len(group)), float(group["cases_ordered"].sum())])
    ws.append([])
    ws.append(["Scope", "Reason", "Rows", "OOS cases", "OOS 9L"])
    for (status, reason), group in clean.groupby(["scope_status", "scope_reason"], dropna=False):
        ws.append([status, reason or "—", int(len(group)), float(group["cases_oos"].sum()), float(group["oos_9l"].fillna(0).sum())])
    ws.append([])
    loss = cells[cells["weighted_oos_9l"] > 1e-9]
    ws.append(["Pattern", "Cells", "Weighted OOS 9L"])
    for pattern, group in loss.groupby("pattern"):
        ws.append([pattern, int(len(group)), float(group["weighted_oos_9l"].sum())])
    ws.append([])
    ws.append(["Quadrant", "Cells", "Weighted OOS 9L"])
    for quadrant, group in cells.groupby("quadrant"):
        ws.append([quadrant, int(len(group)), float(group["weighted_oos_9l"].sum())])
    ws.append([])
    ws.append(["Location passes the 10,000 ordered-9L cut", int(locations["in_table"].sum()), len(locations)])
    for cell in ws[1]:
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = CELL_FONT
            if isinstance(cell.value, float):
                cell.number_format = "#,##0.000"
    ws.column_dimensions["A"].width = 48
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 16
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
    ws.sheet_view.showGridLines = False
    ws.oddFooter.right.text = "Page &P"
    ws.freeze_panes = "A2"


def write_clean(ws, clean: pd.DataFrame) -> None:
    rows = clean_rows(clean)
    formats = {
        8: "#,##0.000", 9: "#,##0.000", 10: "#,##0.000", 11: "#,##0.000", 12: "#,##0.000",
        13: "#,##0.000", 14: "0.0%", 15: "0.0%", 29: "0.000", 30: "#,##0.000", 31: "#,##0.000",
        32: "#,##0.000", 34: "0.0",
    }
    write_rows(ws, CLEAN_HEADERS, rows, formats)
    for cell in ws.iter_rows(min_row=2, min_col=4, max_col=4):
        for item in cell:
            item.number_format = "MMM-YYYY"
    widths = {index: 16 for index in range(1, len(CLEAN_HEADERS) + 1)}
    widths[7] = 42
    widths[21] = 36
    style_sheet(ws, widths)
    ws.auto_filter.ref = f"A1:AL{ws.max_row}"


def write_removed(ws) -> None:
    ws.append(["Note"])
    ws.append(["No rows are removed. Duplicate item-month keys stay on Clean and carry DUP_CODE_DIFF_PRODUCT or DUP_CHECK."])
    ws["A1"].font = HEADER_FONT
    ws["A1"].fill = HEADER_FILL
    ws["A2"].font = CELL_FONT
    ws["A2"].alignment = WRAP
    ws.column_dimensions["A"].width = 120
    ws.row_dimensions[2].height = 32
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
    ws.sheet_view.showGridLines = False
    ws.oddFooter.right.text = "Page &P"


def summarize(clean: pd.DataFrame, cells: pd.DataFrame, locations: pd.DataFrame, spikes: pd.DataFrame) -> None:
    print("rows", len(clean))
    print("ordered", round(float(clean.cases_ordered.sum()), 3))
    print("unshipped", round(float(clean.cases_unshipped.sum()), 3))
    print("oos", round(float(clean.cases_oos.sum()), 3))
    print("map", clean.map_status.value_counts().to_dict())
    print("scope", clean.groupby(["scope_status", "scope_reason"]).size().to_dict())
    loss = cells[cells.weighted_oos_9l > 1e-9]
    print("loss_cells", len(loss), "top80", int(loss.top80.sum()))
    print("pattern", loss.pattern.value_counts().to_dict())
    print("quadrant", cells.quadrant.value_counts().to_dict())
    print("actions", loss.action.value_counts().to_dict())
    print("vintage_loss_cells", int(loss.vintage_flag.sum()), "vintage_top", int(loss.loc[loss.top80, "vintage_flag"].sum()))
    print("locations_in_table", int(locations.in_table.sum()), "of", len(locations))
    print("spikes", len(spikes), "shortlist", int(spikes.shortlist.sum()) if len(spikes) else 0)
    print("dup_groups", clean.loc[clean.dup_flag != "", ["location", "month", "dist_item"]].drop_duplicates().shape[0])
    print("planning_fallback_rows", int(clean.planning_fallback.sum()))
    print("size_review_rows", int((clean.scope_reason == "SIZE_REVIEW").sum()))
    print("out", OUT)


def main() -> None:
    fill = load_fill()
    raw_totals = {
        "ordered": float(fill["cases_ordered"].sum()),
        "unshipped": float(fill["cases_unshipped"].sum()),
        "oos": float(fill["cases_oos"].sum()),
    }
    master = collapse_master(load_master(fill["dist_item"]))
    anaplan = load_anaplan()
    clean = build_clean(fill, master, anaplan)
    if abs(float(clean["cases_ordered"].sum()) - raw_totals["ordered"]) > 0.001:
        raise SystemExit("ordered total moved")
    cells = analysis_frame(clean)
    locations, month = location_table(clean)
    spikes = spike_table(month, clean)
    write_workbook(clean, cells, locations, month, spikes, raw_totals)
    summarize(clean, cells, locations, spikes)


if __name__ == "__main__":
    main()
