"""Premium light-theme PDF (indigo / purple / cyan). Renders the data-driven
typed report sections, so every category produces a distinct document.
"""
import io
from typing import Dict, Any, List

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, NextPageTemplate, PageBreak, Flowable,
)
from reportlab.lib.styles import ParagraphStyle

INDIGO = HexColor("#4F46E5")
PURPLE = HexColor("#7C3AED")
CYAN = HexColor("#06B6D4")
INK = HexColor("#0F172A")
SLATE = HexColor("#475569")
MUTE = HexColor("#94A3B8")
TRACK = HexColor("#E2E8F0")
CARD = HexColor("#F8FAFC")
CARD_BORDER = HexColor("#E2E8F0")
ROSE = HexColor("#E11D48")
EMERALD = HexColor("#10B981")
AMBER = HexColor("#F59E0B")
WHITE = HexColor("#FFFFFF")

TONES = {"indigo": INDIGO, "purple": PURPLE, "cyan": CYAN, "emerald": EMERALD,
         "amber": AMBER, "rose": ROSE, "slate": SLATE, "danger": ROSE,
         "warn": AMBER, "success": EMERALD, "info": INDIGO}

TONE_HEX = {"indigo": "#4F46E5", "purple": "#7C3AED", "cyan": "#06B6D4", "emerald": "#10B981",
            "amber": "#F59E0B", "rose": "#E11D48", "slate": "#475569", "danger": "#E11D48",
            "warn": "#F59E0B", "success": "#10B981", "info": "#4F46E5"}

PAGE_W, PAGE_H = A4


def _tone(name, default=PURPLE):
    return TONES.get(name, default)


def _hex(name, default="#7C3AED"):
    return TONE_HEX.get(name, default)


def _styles():
    return {
        "kicker": ParagraphStyle("kicker", fontName="Helvetica-Bold", fontSize=9, textColor=PURPLE, leading=12, spaceAfter=3),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=18, textColor=INK, leading=22, spaceAfter=6),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10.5, textColor=SLATE, leading=16),
        "bodyi": ParagraphStyle("bodyi", fontName="Helvetica-Oblique", fontSize=11, textColor=INK, leading=18),
        "small": ParagraphStyle("small", fontName="Helvetica", fontSize=9, textColor=SLATE, leading=13),
        "card_title": ParagraphStyle("card_title", fontName="Helvetica-Bold", fontSize=12.5, textColor=INK, leading=15),
        "tag": ParagraphStyle("tag", fontName="Helvetica-Bold", fontSize=8.5, textColor=INDIGO, leading=11),
        "big": ParagraphStyle("big", fontName="Helvetica-Bold", fontSize=24, textColor=PURPLE, leading=26, alignment=TA_CENTER),
        "biglabel": ParagraphStyle("biglabel", fontName="Helvetica", fontSize=8.5, textColor=SLATE, leading=11, alignment=TA_CENTER),
        "cover_title": ParagraphStyle("cover_title", fontName="Helvetica-Bold", fontSize=34, textColor=INK, leading=40, alignment=TA_CENTER),
        "cover_sub": ParagraphStyle("cover_sub", fontName="Helvetica", fontSize=13, textColor=SLATE, leading=20, alignment=TA_CENTER),
    }


class Bar(Flowable):
    def __init__(self, value, width=440, label=None, suffix="%", color=PURPLE):
        super().__init__()
        self.value = max(0, min(100, value))
        self.width = width
        self.label = label
        self.suffix = suffix
        self.color = color
        self.height = 28 if label else 12

    def draw(self):
        c = self.canv
        if self.label:
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 9.5)
            c.drawString(0, 16, self.label)
            c.setFillColor(self.color)
            c.drawRightString(self.width, 16, f"{int(self.value)}{self.suffix}")
        c.setFillColor(TRACK)
        c.roundRect(0, 0, self.width, 7, 3.5, fill=1, stroke=0)
        c.setFillColor(self.color)
        w = max(7, self.width * self.value / 100.0)
        c.roundRect(0, 0, w, 7, 3.5, fill=1, stroke=0)


def _bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(2)
    canvas.line(20 * mm, PAGE_H - 16 * mm, PAGE_W - 20 * mm, PAGE_H - 16 * mm)
    canvas.setFillColor(MUTE)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(20 * mm, 11 * mm, "MAPMYCAREER  ·  Brutally honest career intelligence")
    canvas.drawRightString(PAGE_W - 20 * mm, 11 * mm, f"{doc.page}")
    canvas.restoreState()


def _cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#EEF2FF"))
    canvas.rect(0, PAGE_H / 2 - 75 * mm, PAGE_W, 150 * mm, fill=1, stroke=0)
    canvas.setStrokeColor(PURPLE)
    canvas.setLineWidth(1.5)
    canvas.rect(14 * mm, 14 * mm, PAGE_W - 28 * mm, PAGE_H - 28 * mm, fill=0, stroke=1)
    band = (PAGE_W - 28 * mm) / 3
    canvas.setFillColor(INDIGO)
    canvas.rect(14 * mm, PAGE_H - 17 * mm, band, 3 * mm, fill=1, stroke=0)
    canvas.setFillColor(PURPLE)
    canvas.rect(14 * mm + band, PAGE_H - 17 * mm, band, 3 * mm, fill=1, stroke=0)
    canvas.setFillColor(CYAN)
    canvas.rect(14 * mm + 2 * band, PAGE_H - 17 * mm, band, 3 * mm, fill=1, stroke=0)
    canvas.restoreState()


def _card(inner, width, pad=10, bg=CARD, border=CARD_BORDER):
    t = Table([[inner]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.6, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def _section_block(e, s, st, cw):
    stype = s.get("type")
    title = s.get("title", "")
    if title:
        e.append(Paragraph(title, st["h2"]))
        e.append(Spacer(1, 2 * mm))

    if stype in ("intro",):
        e.append(Paragraph(s.get("text", ""), st["body"]))

    elif stype == "letter":
        letter = (s.get("text", "")).replace("\n", "<br/>")
        e.append(_card([Paragraph(letter, st["bodyi"])], cw, pad=16, bg=HexColor("#EEF2FF"), border=HexColor("#C7D2FE")))

    elif stype == "callout":
        col = _tone(s.get("tone"), INDIGO)
        inner = [Paragraph(f"<font color='{_hex(s.get('tone'))}'><b>{s.get('label','')}</b></font>", st["card_title"]),
                 Spacer(1, 2), Paragraph(s.get("text", ""), st["body"])]
        e.append(_card(inner, cw, bg=HexColor("#F8FAFC"), border=col))

    elif stype == "scorecards":
        items = s.get("items", [])
        cells = []
        for it in items:
            val = it.get("value")
            vtxt = f"{val}{it.get('suffix','')}" if val is not None else "—"
            col = _tone(it.get("tone"), PURPLE)
            big = ParagraphStyle("b", parent=st["big"], textColor=col)
            cells.append([Paragraph(vtxt, big), Paragraph(it.get("label", ""), st["biglabel"]),
                          Paragraph(it.get("caption", ""), st["biglabel"])])
        col_w = cw / max(1, len(cells))
        tbl_cells = [[Table([[c[0]], [c[1]], [c[2]]], colWidths=[col_w - 8]) for c in cells]]
        t = Table(tbl_cells, colWidths=[col_w] * len(cells))
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CARD), ("BOX", (0, 0), (-1, -1), 0.6, CARD_BORDER),
                               ("INNERGRID", (0, 0), (-1, -1), 0.6, WHITE), ("TOPPADDING", (0, 0), (-1, -1), 10),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
        e.append(t)

    elif stype == "bars":
        for it in s.get("items", []):
            e.append(Bar(it.get("value", 0), width=cw, label=it.get("label", ""), suffix=it.get("suffix", "%"), color=_tone(it.get("tone"), PURPLE)))
            e.append(Spacer(1, 4 * mm))

    elif stype == "matches":
        for m in s.get("items", []):
            head = Table([[Paragraph(m["title"], st["card_title"]), Paragraph(f"<b>{m['score']}%</b> fit", st["tag"])]], colWidths=[cw - 80, 60])
            head.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "RIGHT"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
            inner = [head, Spacer(1, 3), Paragraph(f"<i>{m.get('verdict','')}</i> · {m.get('time_to_enter','')} to enter", st["small"]), Spacer(1, 4),
                     Bar(m["market_demand"], width=cw - 24, label="Market Demand", color=INDIGO), Spacer(1, 3),
                     Bar(m["salary_score"], width=cw - 24, label="Salary Score", color=CYAN), Spacer(1, 3),
                     Bar(m["ai_risk"], width=cw - 24, label=f"AI Risk ({m['ai_risk_label']})", color=PURPLE)]
            e.append(_card(inner, cw))
            e.append(Spacer(1, 4 * mm))

    elif stype in ("list", "tags"):
        if s.get("intro"):
            e.append(Paragraph(s["intro"], st["body"]))
            e.append(Spacer(1, 2 * mm))
        for it in s.get("items", []):
            e.append(Paragraph(f"&bull;&nbsp;&nbsp;{it}", st["body"]))
            e.append(Spacer(1, 1.5 * mm))

    elif stype == "cards":
        for it in s.get("items", []):
            parts = [Paragraph(it.get("title", ""), st["card_title"])]
            badges = it.get("badges", [])
            if badges:
                parts.append(Paragraph(" · ".join(f"<font color='{_hex(b.get('tone'))}'>{b.get('text','')}</font>" for b in badges), st["tag"]))
            if it.get("body"):
                parts.append(Spacer(1, 2))
                parts.append(Paragraph(it["body"], st["small"]))
            for pt in it.get("points", []):
                parts.append(Paragraph(f"&bull;&nbsp;{pt}", st["small"]))
            e.append(_card(parts, cw))
            e.append(Spacer(1, 3 * mm))

    elif stype == "roadmap":
        for ph in s.get("items", []):
            parts = [Paragraph(f"<font color='#4F46E5'><b>{ph.get('phase','')}</b></font>" + (f" — {ph['focus']}" if ph.get("focus") else ""), st["card_title"]), Spacer(1, 2)]
            for pt in ph.get("points", []):
                parts.append(Paragraph(f"&bull;&nbsp;{pt}", st["small"]))
            if ph.get("meta"):
                parts.append(Paragraph(ph["meta"], st["tag"]))
            e.append(_card(parts, cw))
            e.append(Spacer(1, 3 * mm))

    elif stype == "salary_chart":
        for pt in s.get("points", []):
            e.append(Bar(min(100, pt["value"]), width=cw, label=f"{pt['label']} — ₹{pt['value']} LPA", suffix="", color=CYAN))
            e.append(Spacer(1, 4 * mm))
        if s.get("note"):
            e.append(Paragraph(s["note"], st["small"]))

    elif stype == "recommendations":
        for m in s.get("items", []):
            head = Table([[Paragraph(m.get("title", ""), st["card_title"]), Paragraph(f"<b>{m.get('score','')}%</b> fit", st["tag"])]], colWidths=[cw - 80, 60])
            head.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "RIGHT"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
            parts = [head, Spacer(1, 2)]
            badge_bits = []
            if m.get("growth"):
                badge_bits.append(f"<font color='#10B981'>{m['growth']} growth</font>")
            if m.get("ai_risk_label"):
                badge_bits.append(f"<font color='{_hex('amber') if m.get('ai_risk',0) <= 55 else _hex('rose')}'>{m['ai_risk_label']}</font>")
            if m.get("salary_mid") is not None:
                badge_bits.append(f"<font color='#06B6D4'>~Rs {m['salary_mid']} LPA</font>")
            if badge_bits:
                parts.append(Paragraph(" · ".join(badge_bits), st["tag"]))
            if m.get("why"):
                parts.append(Spacer(1, 3))
                parts.append(Paragraph(f"<b>Why it fits:</b> {m['why']}", st["small"]))
            if m.get("pros"):
                parts.append(Spacer(1, 2))
                parts.append(Paragraph("<font color='#10B981'><b>Pros</b></font>", st["tag"]))
                for p in m["pros"]:
                    parts.append(Paragraph(f"&bull;&nbsp;{p}", st["small"]))
            if m.get("cons"):
                parts.append(Paragraph("<font color='#E11D48'><b>Cons</b></font>", st["tag"]))
                for p in m["cons"]:
                    parts.append(Paragraph(f"&bull;&nbsp;{p}", st["small"]))
            e.append(_card(parts, cw))
            e.append(Spacer(1, 4 * mm))

    elif stype == "blueprint":
        for ph in s.get("items", []):
            parts = [Paragraph(f"<font color='#7C3AED'><b>{ph.get('phase','')}</b></font>", st["card_title"])]
            if ph.get("focus"):
                parts.append(Paragraph(ph["focus"], st["small"]))
            for g in ph.get("groups", []):
                parts.append(Spacer(1, 2))
                parts.append(Paragraph(f"<font color='#4F46E5'><b>{g.get('label','')}</b></font>", st["tag"]))
                parts.append(Paragraph(", ".join(g.get("items", [])), st["small"]))
            e.append(_card(parts, cw))
            e.append(Spacer(1, 3 * mm))

    elif stype == "table":
        if s.get("intro"):
            e.append(Paragraph(s["intro"], st["body"]))
            e.append(Spacer(1, 2 * mm))
        headers = s.get("headers", [])
        rows = s.get("rows", [])
        hdr_style = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE, leading=11)
        cell_style = ParagraphStyle("td", fontName="Helvetica", fontSize=8.5, textColor=SLATE, leading=11)
        data_rows = [[Paragraph(str(h), hdr_style) for h in headers]]
        for row in rows:
            data_rows.append([Paragraph(str(c), cell_style) for c in row])
        ncol = max(1, len(headers))
        t = Table(data_rows, colWidths=[cw / ncol] * ncol, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), INDIGO),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CARD]),
            ("BOX", (0, 0), (-1, -1), 0.6, CARD_BORDER),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, TRACK),
            ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        e.append(t)

    elif stype == "timeline":
        if s.get("intro"):
            e.append(Paragraph(s["intro"], st["body"]))
            e.append(Spacer(1, 2 * mm))
        for it in s.get("items", []):
            label = it.get("label", "")
            title = it.get("title", "")
            text = it.get("text", "")
            head = f"<font color='#7C3AED'><b>{label}</b></font>"
            if title:
                head += f" &nbsp;<b>{title}</b>"
            e.append(Paragraph(head + (f" — {text}" if text else ""), st["small"]))
            for pt in it.get("points", []):
                e.append(Paragraph(f"&nbsp;&nbsp;&bull;&nbsp;{pt}", st["small"]))
            e.append(Spacer(1, 1.8 * mm))

    e.append(Spacer(1, 6 * mm))


def build_pdf(submission: Dict[str, Any]) -> bytes:
    st = _styles()
    r = submission["report"]
    name = submission.get("name", "You")
    product = r.get("product_name", "MapMyCareer")
    headline = r.get("headline", "Your Career Truth Report")
    buf = io.BytesIO()

    doc = BaseDocTemplate(buf, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=22 * mm, bottomMargin=18 * mm)
    cw = doc.width
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    cover = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="cover")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover], onPage=_cover_bg),
        PageTemplate(id="main", frames=[frame], onPage=_bg),
    ])

    e: List[Any] = []
    e.append(Spacer(1, 60 * mm))
    e.append(Paragraph("MAPMYCAREER", st["kicker"]))
    e.append(Spacer(1, 4 * mm))
    e.append(Paragraph(product, st["cover_title"]))
    e.append(Spacer(1, 8 * mm))
    e.append(Paragraph(headline, st["cover_sub"]))
    e.append(Spacer(1, 8 * mm))
    e.append(Paragraph(f"Prepared for <b>{name}</b>  ·  {r.get('user_type','')}", st["cover_sub"]))
    e.append(NextPageTemplate("main"))
    e.append(PageBreak())

    for i, s in enumerate(r.get("sections", [])):
        _section_block(e, s, st, cw)
        # light pacing: page break after heavy sections
        if s.get("type") in ("matches", "roadmap", "recommendations", "blueprint") and i < len(r["sections"]) - 1:
            e.append(PageBreak())

    doc.build(e)
    return buf.getvalue()


def build_addon_pdf(submission: Dict[str, Any], component_id: str) -> bytes:
    """Render a single add-on deliverable (resume / linkedin / interview) as a branded PDF."""
    st = _styles()
    content = (submission.get("addons") or {}).get(component_id) or {}
    name = submission.get("name", "You")
    buf = io.BytesIO()

    doc = BaseDocTemplate(buf, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=22 * mm, bottomMargin=18 * mm)
    cw = doc.width
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    cover = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="cover")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover], onPage=_cover_bg),
        PageTemplate(id="main", frames=[frame], onPage=_bg),
    ])

    e: List[Any] = []
    e.append(Spacer(1, 66 * mm))
    e.append(Paragraph("MAPMYCAREER", st["kicker"]))
    e.append(Spacer(1, 4 * mm))
    e.append(Paragraph(content.get("title", "Add-on Report"), st["cover_title"]))
    e.append(Spacer(1, 8 * mm))
    e.append(Paragraph(content.get("subtitle", ""), st["cover_sub"]))
    e.append(Spacer(1, 8 * mm))
    e.append(Paragraph(f"Prepared for <b>{name}</b>", st["cover_sub"]))
    e.append(NextPageTemplate("main"))
    e.append(PageBreak())

    if content.get("intro"):
        e.append(_card([Paragraph(content["intro"], st["bodyi"])], cw, pad=14,
                       bg=HexColor("#EEF2FF"), border=HexColor("#C7D2FE")))
        e.append(Spacer(1, 6 * mm))

    for sct in content.get("sections", []):
        e.append(Paragraph(sct.get("heading", ""), st["h2"]))
        e.append(Spacer(1, 2 * mm))
        if sct.get("type") == "list":
            for it in sct.get("items", []):
                e.append(Paragraph(f"&bull;&nbsp;&nbsp;{it}", st["body"]))
                e.append(Spacer(1, 1.5 * mm))
        else:
            e.append(Paragraph(sct.get("text", ""), st["body"]))
        e.append(Spacer(1, 6 * mm))

    doc.build(e)
    return buf.getvalue()
