"""Premium light-theme PDF (indigo / purple / cyan) Career Blueprint."""
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
WHITE = HexColor("#FFFFFF")

PAGE_W, PAGE_H = A4


def _styles():
    return {
        "kicker": ParagraphStyle("kicker", fontName="Helvetica-Bold", fontSize=9, textColor=PURPLE, leading=12, spaceAfter=3),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=20, textColor=INK, leading=24, spaceAfter=6),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10.5, textColor=SLATE, leading=16),
        "bodyi": ParagraphStyle("bodyi", fontName="Helvetica-Oblique", fontSize=11, textColor=INK, leading=18),
        "small": ParagraphStyle("small", fontName="Helvetica", fontSize=9, textColor=SLATE, leading=13),
        "card_title": ParagraphStyle("card_title", fontName="Helvetica-Bold", fontSize=12.5, textColor=INK, leading=15),
        "tag": ParagraphStyle("tag", fontName="Helvetica-Bold", fontSize=8.5, textColor=INDIGO, leading=11),
        "cover_title": ParagraphStyle("cover_title", fontName="Helvetica-Bold", fontSize=40, textColor=INK, leading=44, alignment=TA_CENTER),
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
            c.setFillColor(PURPLE)
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
    canvas.drawString(20 * mm, 11 * mm, "CAREER BLUEPRINT AI  ·  Brutally honest career intelligence")
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
    # color band
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


def build_pdf(submission: Dict[str, Any]) -> bytes:
    st = _styles()
    r = submission["report"]
    name = submission.get("name", "Student")
    cw = None
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

    # COVER
    e.append(Spacer(1, 68 * mm))
    e.append(Paragraph("CAREER BLUEPRINT AI", st["kicker"]))
    e.append(Spacer(1, 4 * mm))
    e.append(Paragraph("Your Career<br/>Truth Report", st["cover_title"]))
    e.append(Spacer(1, 8 * mm))
    e.append(Paragraph(f"Prepared for <b>{name}</b>  ·  {r.get('user_type','')}", st["cover_sub"]))
    e.append(Spacer(1, 10 * mm))
    e.append(Paragraph(f"Success Score {r['success_score']}%   ·   AI Resistance {r['ai_resistance_score']}%", st["cover_sub"]))
    e.append(NextPageTemplate("main"))
    e.append(PageBreak())

    def chapter(num, title):
        e.append(Paragraph(f"CHAPTER {num}", st["kicker"]))
        e.append(Paragraph(title, st["h2"]))
        e.append(Spacer(1, 3 * mm))

    # CH1
    chapter(1, "Career Reality Check")
    e.append(Paragraph(r.get("career_reality_check", ""), st["body"]))
    e.append(Spacer(1, 5 * mm))
    traits = [Paragraph(f"<b>{t}</b>", st["small"]) for t in r.get("trait_labels", [])]
    if traits:
        tt = Table([traits[:3], traits[3:] + [Paragraph("", st["small"])] * (3 - len(traits[3:]))], colWidths=[cw / 3.0] * 3)
        tt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CARD), ("BOX", (0, 0), (-1, -1), 0.6, CARD_BORDER),
                                ("INNERGRID", (0, 0), (-1, -1), 0.6, WHITE), ("TOPPADDING", (0, 0), (-1, -1), 7),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 7), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
        e.append(tt)
    e.append(PageBreak())

    # CH2
    chapter(2, "Strengths & Weaknesses")
    e.append(Paragraph("Your Strengths", st["card_title"]))
    e.append(Spacer(1, 2 * mm))
    for s in r.get("strengths", []):
        e.append(Paragraph(f"<b>{s.get('label','')}</b> — {s.get('description','')}", st["body"]))
        e.append(Spacer(1, 2 * mm))
    e.append(Spacer(1, 3 * mm))
    e.append(Paragraph("Your Weaknesses (the honest part)", st["card_title"]))
    e.append(Spacer(1, 2 * mm))
    for w in r.get("weaknesses", []):
        e.append(Paragraph(f"<font color='#E11D48'><b>{w.get('title','')}</b></font> — {w.get('description','')}", st["body"]))
        e.append(Spacer(1, 2 * mm))
    e.append(PageBreak())

    # CH3
    chapter(3, "Top 5 Career Matches")
    expl = r.get("match_explanations", {})
    for m in r["matches"]:
        rows = [
            [Paragraph(m["title"], st["card_title"]), Paragraph(f"<b>{m['score']}%</b> fit", st["tag"])],
        ]
        head = Table(rows, colWidths=[cw - 80, 60])
        head.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                  ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                                  ("ALIGN", (1, 0), (1, 0), "RIGHT")]))
        inner = [head, Spacer(1, 3),
                 Paragraph(f"<i>{m['verdict']}</i> · {m['time_to_enter']} to enter", st["small"]),
                 Spacer(1, 4),
                 Bar(m["market_demand"], width=cw - 24, label="Market Demand", color=INDIGO), Spacer(1, 3),
                 Bar(m["salary_score"], width=cw - 24, label="Salary Score", color=CYAN), Spacer(1, 3),
                 Bar(m["competition"], width=cw - 24, label="Competition", color=ROSE), Spacer(1, 3),
                 Bar(m["ai_risk"], width=cw - 24, label=f"AI Risk ({m['ai_risk_label']})", color=PURPLE), Spacer(1, 4),
                 Paragraph(expl.get(m["key"], m.get("tagline", "")), st["small"])]
        e.append(_card(inner, cw))
        e.append(Spacer(1, 4 * mm))
    e.append(PageBreak())

    # CH4
    chapter(4, "Careers To Avoid")
    e.append(Paragraph("Based on your profile, these paths are a poor bet — admiring a field isn't the same as being built for it.", st["body"]))
    e.append(Spacer(1, 4 * mm))
    for a in r.get("careers_to_avoid", []):
        inner = [Paragraph(f"<font color='#E11D48'><b>{a['title']}</b></font>  ·  {a['ai_risk_label']}", st["card_title"]),
                 Spacer(1, 2), Paragraph("Why: " + "; ".join(a.get("why", [])), st["small"])]
        e.append(_card(inner, cw, bg=HexColor("#FFF1F2"), border=HexColor("#FECDD3")))
        e.append(Spacer(1, 3 * mm))
    e.append(Paragraph(r.get("careers_to_avoid_note", ""), st["body"]))
    e.append(PageBreak())

    # CH5 + CH6
    chapter(5, "Industry Analysis")
    inds = r.get("industries", [])
    if inds:
        rows, row = [], []
        for ind in inds:
            row.append(Paragraph(f"<b>{ind}</b>", st["small"]))
            if len(row) == 2:
                rows.append(row)
                row = []
        if row:
            row.append(Paragraph("", st["small"]))
            rows.append(row)
        it = Table(rows, colWidths=[cw / 2.0] * 2)
        it.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CARD), ("BOX", (0, 0), (-1, -1), 0.6, CARD_BORDER),
                                ("INNERGRID", (0, 0), (-1, -1), 0.6, WHITE), ("TOPPADDING", (0, 0), (-1, -1), 10),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 10), ("LEFTPADDING", (0, 0), (-1, -1), 10)]))
        e.append(it)
    e.append(Spacer(1, 6 * mm))
    chapter(6, "AI Threat Assessment")
    e.append(Paragraph(f"Portfolio AI exposure: <b>{r['portfolio_ai_risk']}% ({r['ai_risk_label']})</b>.", st["body"]))
    e.append(Spacer(1, 3 * mm))
    for m in r["matches"]:
        e.append(Bar(m["ai_risk"], width=cw, label=f"{m['title']} — {m['ai_risk_label']}", color=PURPLE))
        e.append(Spacer(1, 3.5 * mm))
    e.append(Spacer(1, 2 * mm))
    e.append(Paragraph(r.get("ai_threat_summary", ""), st["body"]))
    e.append(PageBreak())

    # CH7
    chapter(7, "Income Projection")
    sp = r["salary_projection"]
    for label, key in [("Year 1 (Entry)", "year1"), ("Year 3", "year3"), ("Year 5", "year5"), ("Year 10 (Senior)", "year10")]:
        e.append(Bar(min(100, sp[key]), width=cw, label=f"{label} — ₹{sp[key]} LPA", suffix="", color=CYAN))
        e.append(Spacer(1, 5 * mm))
    e.append(Spacer(1, 2 * mm))
    for lab, v in [("Leadership Potential", r["leadership_potential"]), ("Business Potential", r["business_potential"]), ("Personal Growth", r["personal_growth"])]:
        e.append(Bar(v, width=cw, label=lab, color=INDIGO))
        e.append(Spacer(1, 4 * mm))
    e.append(PageBreak())

    # CH8 + CH9
    chapter(8, "Entrepreneurship Potential")
    e.append(Bar(r["business_potential"], width=cw, label="Business Potential", color=PURPLE))
    e.append(Spacer(1, 4 * mm))
    e.append(Paragraph(r.get("entrepreneurship", ""), st["body"]))
    e.append(Spacer(1, 6 * mm))
    chapter(9, "Career Switch Opportunities")
    for tgt in r.get("career_switch", {}).get("targets", [])[:4]:
        inner = [Paragraph(f"<b>{tgt['title']}</b>", st["card_title"]), Spacer(1, 2),
                 Paragraph(f"Difficulty: {tgt['difficulty']} · Time: {tgt['time_required']} · Impact: {tgt['salary_impact']} · Success: {tgt['success_probability']}", st["small"]),
                 Spacer(1, 2), Paragraph("Skill gaps: " + ", ".join(tgt.get("skill_gaps", [])), st["small"])]
        e.append(_card(inner, cw))
        e.append(Spacer(1, 3 * mm))
    e.append(PageBreak())

    # CH10 + CH11
    chapter(10, "Skill Gap Analysis")
    e.append(Paragraph("What to learn next for your #1 path:", st["body"]))
    e.append(Spacer(1, 2 * mm))
    e.append(Paragraph("• " + "<br/>• ".join(r.get("learn_next", [])), st["body"]))
    e.append(Spacer(1, 6 * mm))
    chapter(11, "Learning Roadmap")
    for ph in r.get("learning_plans", []):
        inner = [Paragraph(f"<font color='#4F46E5'><b>{ph['phase']}</b></font> — {ph['focus']}", st["card_title"]),
                 Spacer(1, 2), Paragraph("• " + "  • ".join(ph.get("items", [])), st["small"]),
                 Spacer(1, 2), Paragraph(f"Target: {ph.get('expected_salary','')} · Success: {ph.get('success_probability','')}", st["tag"])]
        e.append(_card(inner, cw))
        e.append(Spacer(1, 3 * mm))
    e.append(PageBreak())

    # CH12 + CH13
    chapter(12, "Resume & LinkedIn Strategy")
    e.append(Paragraph(r.get("resume_linkedin", ""), st["body"]))
    e.append(Spacer(1, 6 * mm))
    chapter(13, "Interview Readiness")
    e.append(Paragraph(r.get("interview_readiness", ""), st["body"]))

    # CH14 (layoff) — conditional
    layoff = r.get("layoff")
    if layoff:
        e.append(PageBreak())
        chapter(14, "Layoff Recovery Plan")
        for lab, v in [("Layoff Risk", layoff["layoff_risk_score"]), ("Recovery Score", layoff["recovery_score"]),
                     ("Employability", layoff["employability_score"]), ("Salary Recovery", layoff["salary_recovery_potential"])]:
            color = ROSE if lab == "Layoff Risk" else INDIGO
            e.append(Bar(v, width=cw, label=lab, color=color))
            e.append(Spacer(1, 4 * mm))
        for phase, items in layoff.get("recovery_roadmap", {}).items():
            inner = [Paragraph(f"<b>{phase}</b>", st["card_title"]), Spacer(1, 2),
                     Paragraph("• " + "<br/>• ".join(items), st["small"])]
            e.append(_card(inner, cw))
            e.append(Spacer(1, 3 * mm))

    e.append(PageBreak())
    # CH15
    chapter(15, "Future Industry Predictions")
    for fi in r.get("future_industries", []):
        e.append(Paragraph(f"• {fi}", st["body"]))
        e.append(Spacer(1, 2 * mm))
    e.append(Spacer(1, 6 * mm))
    # CH16
    chapter(16, "A Letter From Your Future Self")
    letter = r.get("future_self_letter", "").replace("\n", "<br/>")
    e.append(_card([Paragraph(letter, st["bodyi"])], cw, pad=16, bg=HexColor("#EEF2FF"), border=HexColor("#C7D2FE")))

    doc.build(e)
    return buf.getvalue()
