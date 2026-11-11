#!/usr/bin/env python3
"""Build the client deck for Distributor B from the template workbook.

Reads data/cleaned/distributor_b_v1.xlsx (built by tools/build_distributor_b_v1.py)
and writes reports/distributor_b_client_deck.pptx. Both files are git-ignored.

Real names never appear in this script. The distributor, client and team labels
shown on the slides come from private/deck_labels.json (git-ignored):

    {"distributor": "...", "client": "...", "team": "...", "meeting": "..."}

Without that file the deck says "Distributor B" and "the client".
Location names and product descriptions are read from the workbook.

Rebuild after each new extract:
    .venv/bin/python tools/build_distributor_b_v1.py
    .venv/bin/python tools/build_distributor_b_deck.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION, XL_TICK_MARK
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "data" / "cleaned" / "distributor_b_v1.xlsx"
LABELS = ROOT / "private" / "deck_labels.json"
OUT = ROOT / "reports" / "distributor_b_client_deck.pptx"

# Palette: deep wine as the dominant colour, a muted rose as support, slate for text.
WINE = RGBColor(0x5C, 0x1F, 0x3A)
ROSE = RGBColor(0xB0, 0x6F, 0x7E)
BLUSH = RGBColor(0xF6, 0xEC, 0xEF)
SLATE = RGBColor(0x2E, 0x34, 0x3B)
MUTED = RGBColor(0x6B, 0x72, 0x7A)
GRID = RGBColor(0xE3, 0xE5, 0xE8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEAL = RGBColor(0x2F, 0x6F, 0x73)
HEAD = "Cambria"
BODY = "Calibri"

W, H = Inches(13.333), Inches(7.5)
MARGIN = Inches(0.6)


# ---------------------------------------------------------------- figures
def load_figures() -> dict:
    clean = pd.read_excel(WORKBOOK, sheet_name="Clean")
    top = pd.read_excel(WORKBOOK, sheet_name="Top_Cells")
    spikes = pd.read_excel(WORKBOOK, sheet_name="Spikes")
    qa = pd.read_excel(WORKBOOK, sheet_name="QA", header=None)
    # QA rows 1-3: ordered, unshipped and OOS, raw minus clean (row 0 is the header).
    assert float(pd.to_numeric(qa.iloc[1:4, 1]).abs().sum()) == 0, "raw minus clean totals are not zero"

    clean["Month"] = pd.to_datetime(clean["Month"])
    scope = clean[(clean["Scope_Status"] == "INCLUDE") & clean["Cell_ID"].notna()].copy()
    f: dict = {}
    f["rows"] = len(clean)
    f["first"], f["last"] = clean["Month"].min(), clean["Month"].max()
    f["months"] = clean["Month"].nunique()
    f["items"] = clean["Dist_Item"].nunique()
    f["locations"] = sorted(clean["Market"].dropna().unique().tolist())
    f["ordered_cases"] = clean["Cases_Ordered"].sum()
    f["fill_all"] = 1 - clean["Cases_Unshipped"].sum() / f["ordered_cases"]

    # Scope funnel in physical OOS cases.
    reason = clean["Scope_Reason"].fillna("")
    groups = {
        "In scope": clean["Scope_Status"].eq("INCLUDE"),
        "Supply-constrained (RTS)": reason.eq("QUOTA"),
        "VAP": reason.eq("VAP"),
        "Limited edition": reason.eq("LIMITED_EDITION"),
        "To review (mapping, size)": clean["Scope_Status"].eq("REVIEW"),
    }
    f["funnel"] = {name: float(clean.loc[mask, "Cases_OOS"].sum()) for name, mask in groups.items()}
    f["oos_cases_all"] = float(clean["Cases_OOS"].sum())

    # In-scope OOS rate in 9L, over all in-scope ordered volume.
    f["ordered_9l"] = scope["Ordered_9L"].sum()
    f["oos_9l"] = scope["OOS_9L"].sum()
    f["oos_rate"] = f["oos_9l"] / f["ordered_9l"]

    by_loc = scope.groupby("Market").agg(ordered=("Ordered_9L", "sum"), oos=("OOS_9L", "sum"))
    by_loc["rate"] = by_loc["oos"] / by_loc["ordered"]
    f["by_location"] = by_loc
    monthly = scope.groupby(["Month", "Market"]).agg(ordered=("Ordered_9L", "sum"), oos=("OOS_9L", "sum"))
    monthly["rate"] = monthly["oos"] / monthly["ordered"]
    f["monthly_rate"] = monthly["rate"].unstack("Market").sort_index()

    # Concentration and patterns, from the template's Top_Cells sheet.
    f["cells_total"] = scope["Cell_ID"].nunique()
    f["cells_loss"] = len(top)
    f["cells_top80"] = int((top["Top 80%"] == "Yes").sum())
    weighted = top["Weighted OOS 9L"]
    f["top80_share"] = float(weighted[top["Top 80%"] == "Yes"].sum() / weighted.sum())
    f["cumulative"] = top["Cumulative share"].tolist()
    f["pattern_share"] = (top.groupby("Pattern")["Weighted OOS 9L"].sum() / weighted.sum()).to_dict()
    f["pattern_cells"] = top["Pattern"].value_counts().to_dict()
    quad = top.groupby("Quadrant")["Weighted OOS 9L"].sum() / weighted.sum()
    f["repeat_large_share"] = float(quad.get("Repeat × Large", 0))
    f["repeat_large_cells"] = int((top["Quadrant"] == "Repeat × Large").sum())
    f["top10"] = pd.DataFrame({
        "rank": top["Rank"],
        "location": top["Location"],
        "sku": top.iloc[:, 2].astype(str).str.replace(r"\.0$", "", regex=True),
        "description": top["Description"],
        "pattern": top["Pattern"],
        "months": top["Weighted OOS months"],
        "oos_9l": top["Weighted OOS 9L"],
        "rate": top["OOS rate"],
    }).head(10)

    # Spikes: location-months at twice the location's average weighted OOS or more.
    spikes["Month"] = pd.to_datetime(spikes["Month"])
    f["spikes"] = spikes
    f["spike_months"] = sorted(spikes["Month"].dt.strftime("%b %Y").unique().tolist(),
                               key=lambda m: pd.to_datetime(m))

    # Data questions.
    status = clean.groupby("Map_Status").agg(rows=("Map_Status", "size"),
                                             ordered=("Cases_Ordered", "sum"),
                                             codes=("Dist_Item", "nunique"))
    f["map"] = status
    f["rts_rows"] = int(reason.eq("QUOTA").sum())
    f["rts_codes"] = clean.loc[reason.eq("QUOTA"), "Dist_Item"].nunique()
    f["dup_rows"] = int(clean["Flags"].fillna("").str.contains("DUP_CODE_DIFF_PRODUCT").sum())
    f["fcst_blank"] = bool(clean["Fcst_Lag1"].isna().all())
    return f


def labels() -> dict:
    base = {"distributor": "Distributor B", "client": "the client", "team": "The team", "meeting": "Client call"}
    if LABELS.exists():
        base.update(json.loads(LABELS.read_text()))
    return base


# ---------------------------------------------------------------- helpers
def num(value: float, digits: int = 0) -> str:
    return f"{value:,.{digits}f}"


def pct(value: float, digits: int = 1) -> str:
    return f"{value * 100:.{digits}f}%"


def text(slide, x, y, w, h, runs, size=16, color=SLATE, font=BODY, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, name=None, spacing=6):
    """Add a text box. `runs` is a string or a list of paragraphs; a paragraph is a string or a list of
    (text, {options}) tuples."""
    box = slide.shapes.add_textbox(x, y, w, h)
    if name:
        box.name = name
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    paragraphs = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(spacing)
        pieces = para if isinstance(para, list) else [(para, {})]
        for piece, opts in pieces:
            r = p.add_run()
            r.text = piece
            r.font.name = opts.get("font", font)
            r.font.size = Pt(opts.get("size", size))
            r.font.bold = opts.get("bold", bold)
            r.font.italic = opts.get("italic", False)
            r.font.color.rgb = opts.get("color", color)
    return box


def card(slide, x, y, w, h, fill=BLUSH, name=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.adjustments[0] = 0.06
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    shape.shadow.inherit = False
    if name:
        shape.name = name
    return shape


def stat(slide, x, y, w, h, value, label, value_color=WINE):
    card(slide, x, y, w, h)
    text(slide, x + Inches(0.3), y + Inches(0.25), w - Inches(0.6), Inches(0.9), value,
         size=40, font=HEAD, bold=True, color=value_color)
    text(slide, x + Inches(0.3), y + Inches(1.2), w - Inches(0.6), h - Inches(1.35), label, size=14, color=SLATE)


def base_slide(prs, title, subtitle=None, footer=""):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WHITE
    text(slide, MARGIN, Inches(0.45), W - 2 * MARGIN, Inches(0.8), title, size=30, font=HEAD, bold=True,
         color=WINE, name="Title")
    if subtitle:
        text(slide, MARGIN, Inches(1.2), W - 2 * MARGIN, Inches(0.5), subtitle, size=16, color=MUTED,
             name="Subtitle")
    text(slide, MARGIN, H - Inches(0.45), Inches(9), Inches(0.3), footer, size=10, color=MUTED, name="Footer")
    number = len(prs.slides)
    text(slide, W - MARGIN - Inches(1), H - Inches(0.45), Inches(1), Inches(0.3), str(number), size=10,
         color=MUTED, align=PP_ALIGN.RIGHT, name="Slide number")
    return slide


def notes(slide, say: str, plain: str):
    slide.notes_slide.notes_text_frame.text = f"SAY:\n{say}\n\nEN CLAIR :\n{plain}"


def style_chart(chart, percent_axis=False, legend=True):
    chart.font.name = BODY
    chart.font.size = Pt(12)
    chart.font.color.rgb = SLATE
    chart.has_legend = legend
    if legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(12)
    va = chart.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = GRID
    va.format.line.fill.background()
    va.tick_labels.font.size = Pt(12)
    va.tick_labels.font.color.rgb = MUTED
    if percent_axis:
        va.tick_labels.number_format = "0%"
        va.tick_labels.number_format_is_linked = False
    ca = chart.category_axis
    ca.format.line.color.rgb = GRID
    ca.tick_labels.font.size = Pt(12)
    ca.tick_labels.font.color.rgb = MUTED
    ca.has_major_gridlines = False


# ---------------------------------------------------------------- slides
def build(f: dict, lab: dict) -> Presentation:
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    period = f"{f['first']:%b %Y} – {f['last']:%b %Y}"
    footer = f"{lab['distributor']} · fill-rate data {period} · draft for discussion · confidential"
    loc_a, loc_b = f["locations"][0], f["locations"][1]
    share = f["pattern_share"]

    # 1. Title
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = WINE
    text(s, Inches(0.9), Inches(1.0), Inches(4), Inches(0.4), lab["team"].upper(), size=14, color=BLUSH, bold=True)
    text(s, Inches(0.9), Inches(2.2), Inches(11.5), Inches(1.8),
         f"{lab['distributor']}: where out-of-stocks concentrate", size=44, font=HEAD, bold=True, color=WHITE)
    text(s, Inches(0.9), Inches(4.3), Inches(11), Inches(1.0),
         [f"First read of the fill-rate data, {period}",
          f"{lab['meeting']} · draft for discussion"], size=20, color=BLUSH)
    notes(s,
          "Today we show the first read of the Upstate data: where the stockouts are, which products, "
          "whether they repeat, and when. The forecast part is not done yet; we'll say what we need for it.",
          "On présente la première lecture des données Upstate : où sont les ruptures, quels produits, "
          "est-ce que ça se répète, et quand. La partie prévisions n'est pas faite : on dit ce qu'il nous manque.")

    # 2. Key messages
    s = base_slide(prs, "Four things to take away", footer=footer)
    cw, ch, gap = Inches(2.85), Inches(2.6), Inches(0.3)
    top_y = Inches(1.55)
    stats = [
        (pct(f["oos_rate"]), f"of in-scope volume (9L) was out of stock, {period}"),
        (f"{f['cells_top80']} cells", f"of {f['cells_loss']} with a stockout make {pct(f['top80_share'], 0)} of the loss "
                                       "(cell = product × location)"),
        (pct(share.get("Repeat", 0), 0), "of the loss sits in cells that miss 4 months or more"),
        (f"{len(f['spikes'])} spikes", "location-months at twice the usual level or more"),
    ]
    for i, (value, label) in enumerate(stats):
        stat(s, MARGIN + i * (cw + gap), top_y, cw, ch, value, label)
    text(s, MARGIN, Inches(4.6), W - 2 * MARGIN, Inches(1.8),
         [[("Not yet answered: ", {"bold": True, "color": WINE}),
           ("do forecasts explain the stockouts? The forecast extract is needed first (slide 9).", {})],
          [("Every figure ties back to the raw file: ", {"bold": True, "color": WINE}),
           ("ordered, unshipped and out-of-stock totals match to the case.", {})]], size=16)
    notes(s,
          f"Four messages. About {pct(f['oos_rate'], 0)} of the volume we look at went out of stock. "
          f"It is concentrated: {f['cells_top80']} product-location pairs make {pct(f['top80_share'], 0)} of it. "
          f"Most of it, {pct(share.get('Repeat', 0), 0)}, repeats month after month. And a few months spike. "
          "What we can't say yet is whether forecasts explain it.",
          "4 messages : ~4 % de rupture ; très concentré (une cinquantaine de couples produit-entrepôt = 80 %) ; "
          "surtout des ruptures qui se répètent ; quelques mois de pic. On ne sait pas encore si la prévision explique.")

    # 3. Data and scope
    s = base_slide(prs, "What we looked at",
                   f"{num(f['rows'])} rows · {f['months']} months · {f['items']} distributor items · "
                   f"2 shipping locations ({loc_a}, {loc_b})", footer=footer)
    data = CategoryChartData()
    funnel = f["funnel"]
    data.categories = list(funnel.keys())[::-1]
    data.add_series("Out-of-stock cases", [round(v) for v in list(funnel.values())[::-1]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, MARGIN, Inches(1.9), Inches(7.4), Inches(4.6), data)
    chart = gf.chart
    style_chart(chart, legend=False)
    chart.has_title = True
    chart.chart_title.text_frame.text = "Out-of-stock cases by scope group (physical cases)"
    chart.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(14)
    chart.chart_title.text_frame.paragraphs[0].runs[0].font.bold = True
    plot = chart.plots[0]
    plot.gap_width = 60
    plot.has_data_labels = True
    plot.data_labels.number_format = "#,##0"
    plot.data_labels.number_format_is_linked = False
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    plot.data_labels.font.size = Pt(12)
    ser = plot.series[0]
    for idx in range(len(funnel)):
        point = ser.points[idx]
        point.format.fill.solid()
        point.format.fill.fore_color.rgb = WINE if idx == len(funnel) - 1 else ROSE
    chart.value_axis.visible = False
    chart.value_axis.has_major_gridlines = False
    x2 = MARGIN + Inches(7.8)
    card(s, x2, Inches(1.9), W - MARGIN - x2, Inches(4.6))
    text(s, x2 + Inches(0.3), Inches(2.15), W - MARGIN - x2 - Inches(0.6), Inches(4.2),
         [[("How we read it", {"bold": True, "color": WINE, "size": 18})],
          "One cell = one product (client SKU) at one shipping location.",
          "Out-of-stock = Cases OOS, converted to 9-liter cases so pack sizes compare.",
          "December and January count half, as agreed.",
          "In scope: naked goods and gift boxes. RTS, VAP and limited editions are set aside, not deleted.",
          "Rows we could not map stay visible for review."], size=14, spacing=8)
    notes(s,
          "This is the data and the rules. Out-of-stock cases, converted to 9-liter so we can compare pack sizes. "
          "We keep the main cut on naked goods and gift boxes; RTS, VAP and limited editions are set aside, "
          "as you asked, but nothing is deleted.",
          "Les données et les règles. On compte les caisses en rupture, converties en 9 litres pour comparer. "
          "Le périmètre principal : produits simples et coffrets. Le reste est mis de côté, pas supprimé.")

    # 4. Where: by location and month
    s = base_slide(prs, "Similar rate at both locations; a few months stand out",
                   f"Out-of-stock rate by month (OOS 9L / ordered 9L, in scope). Overall: "
                   f"{loc_a} {pct(f['by_location'].loc[loc_a, 'rate'])}, {loc_b} {pct(f['by_location'].loc[loc_b, 'rate'])}",
                   footer=footer)
    rates = f["monthly_rate"]
    data = CategoryChartData()
    data.categories = [m.strftime("%b %y") for m in rates.index]
    for loc in rates.columns:
        data.add_series(loc, [round(float(v), 4) for v in rates[loc].fillna(0)])
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, MARGIN, Inches(1.8), W - 2 * MARGIN, Inches(4.9), data)
    chart = gf.chart
    style_chart(chart, percent_axis=True)
    for ser, colour in zip(chart.plots[0].series, [WINE, TEAL]):
        ser.smooth = False
        ser.format.line.color.rgb = colour
        ser.format.line.width = Pt(2.25)
        ser.marker.format.fill.solid()
        ser.marker.format.fill.fore_color.rgb = colour
        ser.marker.format.line.color.rgb = colour
        ser.marker.size = 5
    chart.category_axis.tick_labels.font.size = Pt(11)
    peak = rates.max(axis=1).sort_values(ascending=False).head(3)
    notes(s,
          f"Both locations are close: {loc_a} {pct(f['by_location'].loc[loc_a, 'rate'])}, "
          f"{loc_b} {pct(f['by_location'].loc[loc_b, 'rate'])}. The highest months are "
          + ", ".join(f"{m:%B %Y}" for m in peak.index) + ". They often peak at the same time. "
          "Question for you: do the two locations ship from separate warehouses?",
          "Les deux entrepôts ont un taux proche. Certains mois sont bien plus hauts, souvent en même temps "
          "aux deux endroits. Question au client : est-ce deux entrepôts séparés ?")

    # 5. Concentration
    s = base_slide(prs, f"{f['cells_top80']} product-location cells make {pct(f['top80_share'], 0)} of the loss",
                   f"Cumulative share of weighted out-of-stock 9L, cells ranked from largest to smallest "
                   f"({f['cells_loss']} cells with a stockout, out of {f['cells_total']})", footer=footer)
    data = CategoryChartData()
    data.categories = [str(i) for i in range(1, len(f["cumulative"]) + 1)]
    data.add_series("Cumulative share", [round(float(v), 4) for v in f["cumulative"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE, MARGIN, Inches(1.8), Inches(8.2), Inches(4.55), data)
    chart = gf.chart
    style_chart(chart, percent_axis=True, legend=False)
    chart.value_axis.maximum_scale = 1.0
    chart.value_axis.minimum_scale = 0
    chart.has_title = False
    chart.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.NONE
    chart.category_axis.has_major_gridlines = False
    chart.category_axis.major_tick_mark = XL_TICK_MARK.NONE
    ser = chart.plots[0].series[0]
    ser.smooth = False
    ser.format.line.color.rgb = WINE
    ser.format.line.width = Pt(2.5)
    # tick spacing: python-pptx has no direct API; set via XML.
    text(s, MARGIN + Inches(0.6), Inches(6.45), Inches(7.4), Inches(0.3),
         f"Cells ranked from largest to smallest loss (1 to {f['cells_loss']}) →", size=12, color=MUTED)
    x2 = MARGIN + Inches(8.6)
    stat(s, x2, Inches(1.8), W - MARGIN - x2, Inches(2.3), f"{f['cells_top80']} of {f['cells_loss']}",
         f"cells carry {pct(f['top80_share'], 0)} of the weighted loss")
    stat(s, x2, Inches(4.4), W - MARGIN - x2, Inches(2.3), f"{f['repeat_large_cells']} cells",
         f"are both large and repeating: {pct(f['repeat_large_share'], 0)} of the loss")
    notes(s,
          f"The loss is concentrated. Out of {f['cells_loss']} product-location pairs that had a stockout, "
          f"{f['cells_top80']} make 80%. And {f['repeat_large_cells']} of them are large and repeat, which is half of the loss. "
          "That is where a buffer review would start.",
          "Peu de couples produit-entrepôt font l'essentiel des ruptures. Une trentaine sont à la fois gros et "
          "répétés : la moitié de la perte. C'est par là qu'il faudrait commencer à revoir les stocks tampons.")

    # 6. Top cells table
    s = base_slide(prs, "The ten largest cells",
                   "Ranked by weighted out-of-stock 9L. Pattern: repeat = 4+ weighted months with a stockout",
                   footer=footer)
    t = f["top10"]
    cols = ["#", "Location", "Client SKU", "Product", "Pattern", "OOS months", "OOS 9L", "OOS rate"]
    widths = [0.45, 1.35, 1.25, 4.9, 1.35, 1.2, 1.0, 1.0]
    tbl = s.shapes.add_table(len(t) + 1, len(cols), MARGIN, Inches(1.8), Inches(sum(widths)), Inches(4.6)).table
    for j, wdt in enumerate(widths):
        tbl.columns[j].width = Inches(wdt)
    rows = [[str(int(r.rank)), r.location, r.sku, str(r.description), r.pattern, f"{r.months:.1f}",
             num(r.oos_9l), pct(r.rate)] for r in t.itertuples(index=False)]
    for i, row in enumerate([cols] + rows):
        for j, value in enumerate(row):
            cell = tbl.cell(i, j)
            cell.text = value
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            para = cell.text_frame.paragraphs[0]
            para.alignment = PP_ALIGN.RIGHT if j in (0, 5, 6, 7) else PP_ALIGN.LEFT
            run = para.runs[0]
            run.font.name = BODY
            run.font.size = Pt(12 if i == 0 else 11)
            run.font.bold = i == 0
            run.font.color.rgb = WHITE if i == 0 else SLATE
            cell.fill.solid()
            cell.fill.fore_color.rgb = WINE if i == 0 else (BLUSH if i % 2 == 0 else WHITE)
    notes(s,
          "These are the ten biggest. For each: where, which product, how many months it missed, and how much. "
          "Most are repeat cells. We'd like your read: is any of these a known supply issue, a vintage change, "
          "or a product being phased out?",
          "Les 10 plus gros couples produit-entrepôt. Demander au client s'il connaît la raison pour certains "
          "(problème d'approvisionnement, changement de millésime, produit en fin de vie).")

    # 7. Patterns
    s = base_slide(prs, f"{pct(share.get('Repeat', 0), 0)} of the loss is in cells that miss again and again",
                   "Share of weighted out-of-stock 9L by how often the cell missed", footer=footer)
    order = [("Repeat", "Repeat (4+ months)"), ("Intermittent", "Intermittent (3 months)"), ("Event", "One-off (2 or fewer)")]
    data = CategoryChartData()
    data.categories = [label for _, label in order]
    data.add_series("Share of loss", [round(float(share.get(k, 0)), 4) for k, _ in order])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, MARGIN, Inches(1.8), Inches(7.4), Inches(4.9), data)
    chart = gf.chart
    style_chart(chart, percent_axis=True, legend=False)
    plot = chart.plots[0]
    plot.gap_width = 70
    plot.has_data_labels = True
    plot.data_labels.number_format = "0%"
    plot.data_labels.number_format_is_linked = False
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    plot.data_labels.font.size = Pt(14)
    plot.data_labels.font.bold = True
    for idx, colour in enumerate([WINE, ROSE, ROSE]):
        pt = plot.series[0].points[idx]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = colour
    chart.value_axis.maximum_scale = 0.7
    x2 = MARGIN + Inches(7.8)
    card(s, x2, Inches(1.8), W - MARGIN - x2, Inches(4.9))
    cells = f["pattern_cells"]
    text(s, x2 + Inches(0.3), Inches(2.05), W - MARGIN - x2 - Inches(0.6), Inches(4.5),
         [[("What it suggests", {"bold": True, "color": WINE, "size": 18})],
          f"{cells.get('Repeat', 0)} repeat cells, {cells.get('Intermittent', 0)} intermittent, "
          f"{cells.get('Event', 0)} one-off.",
          "A stockout that comes back month after month points to a setting that does not fit demand: "
          "buffer size, forecast or lead time.",
          "A one-off points to a supply or allocation event.",
          [("These are readings, not causes. ", {"bold": True}),
           ("Confirming them needs the forecast and buffer data.", {})]], size=14, spacing=8)
    notes(s,
          "Most of the loss is in cells that miss again and again. That usually points to a setting that doesn't "
          "fit demand, not to bad luck. But we can only confirm the cause once we have the forecasts and buffers.",
          "La majorité des ruptures se répètent. Ça fait penser à un réglage inadapté (stock tampon, prévision, "
          "délai), mais on ne pourra le confirmer qu'avec les prévisions et les buffers.")

    # 8. Spikes
    sp = f["spikes"]
    s = base_slide(prs, "A few months spike, often at both locations at once",
                   "Location-months whose weighted out-of-stock 9L is at least twice the location's monthly average",
                   footer=footer)
    data = CategoryChartData()
    sp_sorted = sp.sort_values(["Month", "Location"])
    data.categories = [f"{m:%b %Y} · {loc}" for m, loc in zip(sp_sorted["Month"], sp_sorted["Location"])]
    data.add_series("Times the monthly average", [round(float(v), 2) for v in sp_sorted["Index"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, MARGIN, Inches(1.8), Inches(7.4), Inches(4.9), data)
    chart = gf.chart
    style_chart(chart, legend=False)
    chart.category_axis.reverse_order = True
    plot = chart.plots[0]
    plot.gap_width = 50
    plot.has_data_labels = True
    plot.data_labels.number_format = '0.0"×"'
    plot.data_labels.number_format_is_linked = False
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    plot.data_labels.font.size = Pt(12)
    plot.series[0].format.fill.solid()
    plot.series[0].format.fill.fore_color.rgb = WINE
    chart.value_axis.visible = False
    chart.value_axis.has_major_gridlines = False
    x2 = MARGIN + Inches(7.8)
    card(s, x2, Inches(1.8), W - MARGIN - x2, Inches(4.9))
    text(s, x2 + Inches(0.3), Inches(2.05), W - MARGIN - x2 - Inches(0.6), Inches(4.5),
         [[("Questions for you", {"bold": True, "color": WINE, "size": 18})],
          "Spike months: " + ", ".join(f["spike_months"]) + ".",
          "Was there a known event (supply delay, allocation, promotion, price change)?",
          "When both locations spike together, the cause is likely upstream of the distributor."],
         size=14, spacing=8)
    notes(s,
          "Some months are much worse than usual, for example " + ", ".join(f["spike_months"][:3]) + ". "
          "Several hit both locations at the same time, which suggests a cause upstream. "
          "Do you know what happened in those months?",
          "Quelques mois sont bien pires que d'habitude, souvent aux deux entrepôts en même temps : la cause "
          "est sans doute en amont. Demander au client s'il sait ce qui s'est passé ces mois-là.")

    # 9. Forecast
    s = base_slide(prs, "Do forecasts explain the stockouts? Not answered yet",
                   "What we need to run the forecast-bias test", footer=footer)
    steps = [
        ("Have", "Fill-rate data to August 2026, cleaned and checked. Client SKU and 9L factor on every in-scope row."),
        ("Need", "The 2026 forecast extract saved on 29 October, in our shared folder. It gives lag 0, 1 and 2 for 2026."),
        ("Need", "2025 forecast snapshots for this distributor, still with IT. Without them, 2025 months stay blank."),
        ("Then", "Lag-1 bias per cell: did forecasts sit below what was ordered in the months that ran out?"),
    ]
    sw, sgap = Inches(2.85), Inches(0.3)
    for i, (tag, body) in enumerate(steps):
        x = MARGIN + i * (sw + sgap)
        fill = BLUSH if tag != "Need" else RGBColor(0xFB, 0xE3, 0xE6)
        card(s, x, Inches(1.9), sw, Inches(3.6), fill=fill)
        text(s, x + Inches(0.3), Inches(2.15), sw - Inches(0.6), Inches(0.6), tag, size=22, font=HEAD, bold=True,
             color=WINE)
        text(s, x + Inches(0.3), Inches(2.9), sw - Inches(0.6), Inches(2.5), body, size=14)
    text(s, MARGIN, Inches(5.8), W - 2 * MARGIN, Inches(0.9),
         "Rule we follow: a SKU with no forecast in an available snapshot counts as zero; a missing month or a "
         "missing file stays blank, never zero.", size=14, color=MUTED)
    notes(s,
          "We can't answer the forecast question yet. We need the 2026 extract you saved on October 29 in our "
          "folder, and the 2025 snapshots once IT has them. A missing file stays blank; we never treat it as zero.",
          "On ne peut pas encore répondre sur les prévisions. Il nous faut le fichier 2026 (sur leur SharePoint) "
          "et les prévisions 2025 (encore chez leur informatique). Un fichier manquant n'est jamais compté comme zéro.")

    # 10. Data questions
    m = f["map"]
    nf = m.loc["NOT_FOUND"] if "NOT_FOUND" in m.index else None
    amb = m.loc["AMBIGUOUS"] if "AMBIGUOUS" in m.index else None
    s = base_slide(prs, "Four questions on the data", footer=footer)
    qs = [
        ("Unmapped items",
         f"{int(nf.codes) if nf is not None else 0} distributor items ({int(nf.rows) if nf is not None else 0} rows, "
         f"{num(nf.ordered) if nf is not None else 0} cases ordered) are not in Master Data. "
         f"{int(amb.codes) if amb is not None else 0} item points to two client SKUs. Which SKU should each map to?"),
        ("RTS items",
         f"{f['rts_codes']} items ({f['rts_rows']} rows) are set aside as RTS, matched from the description. "
         "Are they the three RTS SKUs you named?"),
        ("Two locations", "Do the two shipping locations run separate warehouses and buffers?"),
        ("Flags", "Do the Master Data deletion or active flags mean \"do not replenish\"?"),
    ]
    qw, qh, qgap = Inches(5.9), Inches(2.25), Inches(0.33)
    for i, (head, body) in enumerate(qs):
        x = MARGIN + (i % 2) * (qw + qgap)
        y = Inches(1.6) + (i // 2) * (qh + qgap)
        card(s, x, y, qw, qh)
        text(s, x + Inches(0.3), y + Inches(0.22), qw - Inches(0.6), Inches(0.5), head, size=20, font=HEAD,
             bold=True, color=WINE)
        text(s, x + Inches(0.3), y + Inches(0.85), qw - Inches(0.6), qh - Inches(1.0), body, size=14)
    notes(s,
          "Four questions where we need you. Some items are not in Master Data, and we don't want to guess. "
          "We need to confirm the three RTS items. And whether the two locations are separate warehouses.",
          "Quatre questions pour le client : les codes produits introuvables (on ne devine pas), les 3 produits RTS, "
          "les deux entrepôts séparés ou non, et le sens des indicateurs de Master Data.")

    # 11. Next steps
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = WINE
    text(s, Inches(0.9), Inches(0.9), Inches(11), Inches(1), "Next steps", size=40, font=HEAD, bold=True, color=WHITE)
    steps = [
        ("1", "Copy the 2026 forecast extract into the shared folder", lab["client"] + " / our team"),
        ("2", "Run the forecast-bias test on 2026 months", "Our team"),
        ("3", "Answer the four data questions", lab["client"]),
        ("4", "Turn the repeat cells into a short list of buffer changes to review", "Together"),
    ]
    for i, (n, what, who) in enumerate(steps):
        y = Inches(2.2) + i * Inches(1.1)
        circle = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.9), y, Inches(0.7), Inches(0.7))
        circle.fill.solid()
        circle.fill.fore_color.rgb = BLUSH
        circle.line.fill.background()
        text(s, Inches(0.9), y + Inches(0.12), Inches(0.7), Inches(0.5), n, size=20, bold=True, color=WINE,
             align=PP_ALIGN.CENTER)
        text(s, Inches(1.9), y + Inches(0.02), Inches(7.6), Inches(0.7), what, size=20, color=WHITE)
        text(s, Inches(9.4), y + Inches(0.08), Inches(3.1), Inches(0.6), who, size=16, color=BLUSH,
             align=PP_ALIGN.RIGHT)
    notes(s,
          "Next steps: get the forecast file into our folder, run the bias test, get your answers on the data "
          "questions, then turn the repeat cells into a short list of buffer changes.",
          "Prochaines étapes : récupérer le fichier de prévisions, faire le test, obtenir les réponses du client, "
          "puis proposer une courte liste de changements de stock tampon.")
    return prs


def main() -> None:
    figures = load_figures()
    out = OUT
    # Layout check without product names: DECK_MASK=/path/to/copy.pptx writes a copy with
    # every product description replaced by a placeholder of the same length.
    if os.environ.get("DECK_MASK"):
        out = Path(os.environ["DECK_MASK"])
        figures["top10"]["description"] = figures["top10"]["description"].astype(str).map(
            lambda d: ("Product name " * 10)[: len(d)])
    deck = build(figures, labels())
    out.parent.mkdir(exist_ok=True)
    deck.save(out)
    print(f"Wrote {out.name}: {len(deck.slides)} slides")
    print(f"In-scope OOS rate {pct(figures['oos_rate'], 2)}; top-80 cells {figures['cells_top80']} "
          f"of {figures['cells_loss']}; spikes {len(figures['spikes'])}")


if __name__ == "__main__":
    main()
