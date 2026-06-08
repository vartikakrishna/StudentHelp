"""Premium dark-navy + gold PDF Career Blueprint using ReportLab."""
import io
from typing import Dict, Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, NextPageTemplate, PageBreak, Flowable,
)
from reportlab.lib.styles import ParagraphStyle

NAVY = HexColor("#040914")
NAVY2 = HexColor("#091226")
CARD = HexColor("#0C1730")
GOLD = HexColor("#F59E0B")
GOLD_SOFT = HexColor("#E5C07B")
WHITE = HexColor("#FFFFFF")
SLATE = HexColor("#94A3B8")
TRACK = HexColor("#1E293B")

PAGE_W, PAGE_H = A4


def _styles():
    return {
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=30, textColor=WHITE, leading=34),
        "kicker": ParagraphStyle("kicker", fontName="Helvetica-Bold", fontSize=10, textColor=GOLD, leading=14, spaceAfter=4),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=20, textColor=WHITE, leading=24, spaceAfter=6),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=11, textColor=SLATE, leading=17),
        "bodyw": ParagraphStyle("bodyw", fontName="Helvetica", fontSize=11, textColor=WHITE, leading=17),
        "small": ParagraphStyle("small", fontName="Helvetica", fontSize=9, textColor=SLATE, leading=13),
        "stat": ParagraphStyle("stat", fontName="Helvetica-Bold", fontSize=30, textColor=GOLD, leading=32),
        "statlabel": ParagraphStyle("statlabel", fontName="Helvetica", fontSize=9, textColor=SLATE, leading=12),
        "card_title": ParagraphStyle("card_title", fontName="Helvetica-Bold", fontSize=13, textColor=WHITE, leading=16),
        "letter": ParagraphStyle("letter", fontName="Helvetica-Oblique", fontSize=12, textColor=WHITE, leading=20),
        "cover_title": ParagraphStyle("cover_title", fontName="Helvetica-Bold", fontSize=40, textColor=WHITE, leading=44, alignment=TA_CENTER),
        "cover_sub": ParagraphStyle("cover_sub", fontName="Helvetica", fontSize=13, textColor=SLATE, leading=20, alignment=TA_CENTER),
    }


class Bar(Flowable):
    def __init__(self, value, width=440, label=None, suffix="%"):
        super().__init__()
        self.value = max(0, min(100, value))
        self.width = width
        self.label = label
        self.suffix = suffix
        self.height = 30 if label else 14

    def draw(self):
        c = self.canv
        y = 0
        if self.label:
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(0, 18, self.label)
            c.setFillColor(GOLD)
            c.drawRightString(self.width, 18, f"{int(self.value)}{self.suffix}")
        c.setFillColor(TRACK)
        c.roundRect(0, y, self.width, 8, 4, fill=1, stroke=0)
        c.setFillColor(GOLD)
        w = max(8, self.width * self.value / 100.0)
        c.roundRect(0, y, w, 8, 4, fill=1, stroke=0)


def _bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # top hairline
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(2)
    canvas.line(20 * mm, PAGE_H - 18 * mm, PAGE_W - 20 * mm, PAGE_H - 18 * mm)
    # footer
    canvas.setFillColor(SLATE)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(20 * mm, 12 * mm, "CAREER BLUEPRINT AI")
    canvas.drawRightString(PAGE_W - 20 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()


def _cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(NAVY2)
    canvas.rect(0, PAGE_H / 2 - 70 * mm, PAGE_W, 140 * mm, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1)
    canvas.rect(14 * mm, 14 * mm, PAGE_W - 28 * mm, PAGE_H - 28 * mm, fill=0, stroke=1)
    canvas.restoreState()


def _card(flow_rows, width, pad=10):
    t = Table([[flow_rows]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#1E2A45")),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def build_pdf(submission: Dict[str, Any]) -> bytes:
    st = _styles()
    report = submission["report"]
    name = submission.get("name", "Student")
    buf = io.BytesIO()

    doc = BaseDocTemplate(buf, pagesize=A4,
                          leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=24 * mm, bottomMargin=20 * mm)
    content_w = doc.width
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    cover_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="cover")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=_cover_bg),
        PageTemplate(id="main", frames=[frame], onPage=_bg),
    ])

    e = []

    # ---------- COVER ----------
    e.append(Spacer(1, 70 * mm))
    e.append(Paragraph("CAREER BLUEPRINT AI", st["kicker"]))
    e.append(Spacer(1, 4 * mm))
    e.append(Paragraph("Your Personalised<br/>Career Blueprint", st["cover_title"]))
    e.append(Spacer(1, 8 * mm))
    e.append(Paragraph(f"Prepared exclusively for<br/><b><font color='#F59E0B'>{name}</font></b>", st["cover_sub"]))
    e.append(Spacer(1, 14 * mm))
    e.append(Paragraph(f"Overall Success Score &nbsp;\u2022&nbsp; {report['success_score']}%", st["cover_sub"]))
    e.append(NextPageTemplate("main"))
    e.append(PageBreak())

    def chapter(num, title):
        e.append(Paragraph(f"CHAPTER {num}", st["kicker"]))
        e.append(Paragraph(title, st["h2"]))
        e.append(Spacer(1, 4 * mm))

    # ---------- CH1 Career DNA ----------
    chapter(1, "Your Career DNA")
    e.append(Paragraph(report.get("career_dna", ""), st["body"]))
    e.append(Spacer(1, 6 * mm))
    trait_cells = [Paragraph(f"<b><font color='#FFFFFF'>{t}</font></b>", st["small"]) for t in report.get("trait_labels", [])]
    tt = Table([trait_cells], colWidths=[content_w / 4.0] * 4)
    tt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY2),
        ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#1E2A45")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, HexColor("#1E2A45")),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    e.append(tt)
    e.append(Spacer(1, 6 * mm))
    e.append(Paragraph("Personality Insight", st["card_title"]))
    e.append(Spacer(1, 2 * mm))
    e.append(Paragraph(report.get("personality_insight", ""), st["body"]))
    e.append(PageBreak())

    # ---------- CH2 Top 5 Matches ----------
    chapter(2, "Top 5 Career Matches")
    expls = report.get("match_explanations", {})
    for m in report["matches"]:
        inner = [
            Paragraph(m["title"], st["card_title"]),
            Spacer(1, 3),
            Bar(m["score"], width=content_w - 24),
            Spacer(1, 5),
            Paragraph(expls.get(m["key"], m.get("tagline", "")), st["small"]),
        ]
        e.append(_card(inner, content_w))
        e.append(Spacer(1, 4 * mm))
    e.append(PageBreak())

    # ---------- CH3 Salary Projection ----------
    chapter(3, "Future Salary Projection")
    sp = report["salary_projection"]
    e.append(Paragraph("Estimated annual income for your #1 path (INR, lakhs per annum):", st["body"]))
    e.append(Spacer(1, 5 * mm))
    for label, key in [("Year 1 (Entry)", "year1"), ("Year 3", "year3"), ("Year 5", "year5"), ("Year 10 (Senior)", "year10")]:
        e.append(Bar(min(100, sp[key]), width=content_w, label=f"{label}  \u2014  \u20b9{sp[key]} LPA", suffix=""))
        e.append(Spacer(1, 6 * mm))
    e.append(PageBreak())

    # ---------- CH4 AI Risk ----------
    chapter(4, "AI Risk Analysis")
    e.append(Paragraph(f"Your career portfolio carries an AI-Resistance Score of <b><font color='#F59E0B'>{report['ai_resistance_score']}%</font></b>. The higher this number, the safer your path is from automation.", st["body"]))
    e.append(Spacer(1, 5 * mm))
    for m in report["matches"]:
        e.append(Bar(m["ai_resistance"], width=content_w, label=m["title"]))
        e.append(Spacer(1, 5 * mm))
    e.append(PageBreak())

    # ---------- CH5 Learning Roadmap ----------
    chapter(5, "Your Learning Roadmap")
    for ph in report.get("learning_roadmap", []):
        inner = [
            Paragraph(f"<font color='#F59E0B'>{ph.get('phase','')}</font>", st["card_title"]),
            Spacer(1, 2),
            Paragraph(ph.get("focus", ""), st["bodyw"]),
            Spacer(1, 2),
            Paragraph("&bull; " + "&nbsp;&nbsp;&bull; ".join(ph.get("skills", [])), st["small"]),
        ]
        e.append(_card(inner, content_w))
        e.append(Spacer(1, 4 * mm))
    e.append(PageBreak())

    # ---------- CH6 Best Industries ----------
    chapter(6, "Best Industries For You")
    rows, row = [], []
    for i, ind in enumerate(report.get("industries", [])):
        row.append(Paragraph(f"<b><font color='#FFFFFF'>{ind}</font></b>", st["small"]))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        row.append(Paragraph("", st["small"]))
        rows.append(row)
    if rows:
        it = Table(rows, colWidths=[content_w / 2.0] * 2)
        it.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CARD),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, NAVY),
            ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#1E2A45")),
            ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ]))
        e.append(it)
    e.append(PageBreak())

    # ---------- CH7 Entrepreneurship ----------
    chapter(7, "Entrepreneurship Potential")
    e.append(Bar(report["business_potential"], width=content_w, label="Business Potential"))
    e.append(Spacer(1, 4 * mm))
    e.append(Bar(report["leadership_potential"], width=content_w, label="Leadership Potential"))
    e.append(Spacer(1, 6 * mm))
    e.append(Paragraph(report.get("entrepreneurship", ""), st["body"]))
    e.append(PageBreak())

    # ---------- CH8 Hidden Strengths ----------
    chapter(8, "Hidden Strengths")
    hs = report.get("hidden_strength", {})
    inner = [
        Paragraph(hs.get("title", "Hidden Strength"), st["card_title"]),
        Spacer(1, 3),
        Paragraph(hs.get("description", ""), st["small"]),
    ]
    e.append(_card(inner, content_w))
    e.append(Spacer(1, 5 * mm))
    for s in report.get("strengths", []):
        e.append(Paragraph(f"<b><font color='#FFFFFF'>{s.get('label','')}</font></b> \u2014 {s.get('description','')}", st["body"]))
        e.append(Spacer(1, 3 * mm))
    e.append(PageBreak())

    # ---------- CH9 Growth Obstacles ----------
    chapter(9, "Growth Obstacles")
    for o in report.get("growth_obstacles", []):
        inner = [
            Paragraph(o.get("title", ""), st["card_title"]),
            Spacer(1, 2),
            Paragraph(o.get("description", ""), st["small"]),
        ]
        e.append(_card(inner, content_w))
        e.append(Spacer(1, 4 * mm))
    e.append(PageBreak())

    # ---------- CH10 Future Self Letter ----------
    chapter(10, "A Letter From Your Future Self")
    letter = report.get("future_self_letter", "").replace("\n", "<br/>")
    e.append(_card([Paragraph(letter, st["letter"])], content_w, pad=16))

    doc.build(e)
    return buf.getvalue()
