"""Deep 16-20 page Career Blueprint generator (post-payment, premium).

Generates ~17 richly personalized, AI-written sections (Claude Sonnet 4.6) on top
of the deterministic engine report. Runs only for the three flagship paid products
(Student / IT Employee / Working Professional) AFTER payment is verified.

Design notes:
- Generation is split into several SMALL parallel Claude calls (asyncio.gather) to
  keep each response well under the output-token ceiling (avoids truncated JSON)
  and to keep wall-clock latency low.
- Every chunk is best-effort: any chunk that fails/parses-empty is simply skipped,
  so a partial blueprint still renders. If the key is missing, we return [] and the
  base report renders unchanged.
- Output sections reuse the existing typed renderer (intro/callout/cards/bars/list/
  blueprint/...) plus two new types: `table` and `timeline`.
"""
import os
import json
import re
import asyncio
import logging
from typing import Dict, Any, List, Tuple

import career_db
import content_lib
from common import sec

logger = logging.getLogger(__name__)

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")
DEEP_TYPES = {"Student", "IT Employee", "Working Professional"}

SYSTEM = (
    "You are a world-class career strategist, executive coach, industry analyst and learning architect "
    "writing a PREMIUM, deeply personalized MapMyCareer blueprint that should feel worth Rs 5,000+. "
    "Be brutally honest and specific — zero generic advice, zero motivational fluff. Every recommendation must be "
    "concrete and actionable: name exact skills, tools, resources, projects, weekly targets and steps the person can "
    "start tomorrow. Tailor everything to THIS person's exact situation and stated goal. "
    "HONESTY RULE: never replace, downgrade or talk the user out of their stated goal/dream/target. If it is hard, keep "
    "it as the goal and explain bluntly what makes it hard and exactly how to earn it. "
    "Write for an Indian audience (salaries in INR/LPA, Indian context where relevant). "
    "Respond with ONLY valid minified JSON matching the requested shape — no markdown fences, no commentary."
)


def _extract_json(text: str) -> Dict[str, Any]:
    text = re.sub(r"```(json)?", "", (text or "").strip()).strip()
    s, e = text.find("{"), text.rfind("}")
    if s != -1 and e != -1:
        text = text[s:e + 1]
    return json.loads(text)


# --------------------------------------------------------------------------- context
def _resources(profile: Dict[str, Any], report: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, List[str]]]:
    a = profile.get("answers") or {}
    txt = (a.get("dream_career") or a.get("future_goal") or a.get("desired_position")
           or a.get("target_role") or report.get("dream_career") or "")
    career = None
    if txt:
        career, _ = career_db.resolve_career(txt)
    if not career and report.get("matches"):
        career, _ = career_db.resolve_career(report["matches"][0].get("title", ""))
    if not career:
        career = {"domain": "", "cluster": "", "title": "your target career"}
    return career, content_lib.learning_for(career)


def _target_role(profile: Dict[str, Any], report: Dict[str, Any]) -> str:
    a = profile.get("answers") or {}
    return (a.get("dream_career") or a.get("future_goal") or a.get("desired_position")
            or a.get("target_role") or report.get("dream_career")
            or (report["matches"][0]["title"] if report.get("matches") else "your best-fit career"))


def _ctx(profile: Dict[str, Any], report: Dict[str, Any], resources: Dict[str, List[str]]) -> str:
    a = profile.get("answers") or {}
    pers = profile.get("personality") or {}
    sp = report.get("salary_projection") or {}
    matches = report.get("matches", [])
    mline = "; ".join(f"{m.get('title')} ({m.get('score')}% fit, {m.get('ai_risk_label','')}, ~Rs {m.get('salary_mid')} LPA)"
                      for m in matches[:5])
    answers_line = "; ".join(f"{k}={v}" for k, v in a.items() if v and not isinstance(v, (dict,)))
    res = {k: resources.get(k, [])[:8] for k in
           ("skills", "tools", "courses", "books", "youtube", "projects", "certifications", "universities")}
    return (
        f"USER: {profile.get('name')} | type: {report.get('user_type')} | product: {report.get('product_name')} | "
        f"primary goal: {report.get('primary_goal')}.\n"
        f"STATED TARGET/GOAL (keep as the goal, never substitute): {_target_role(profile, report)}.\n"
        f"QUESTIONNAIRE ANSWERS: {answers_line}.\n"
        f"PERSONALITY: {json.dumps(pers)}.\n"
        f"ENGINE MATCHES (top fits): {mline}.\n"
        f"SALARY PROJECTION (Rs LPA): year1={sp.get('year1')}, year3={sp.get('year3')}, year5={sp.get('year5')}, year10={sp.get('year10')}.\n"
        f"CURATED RESOURCES you should weave in (real, vetted — use these names): {json.dumps(res)}.\n"
        f"REPORT FOCUS: {report.get('ai_focus', 'honest, actionable career strategy')}."
    )


# --------------------------------------------------------------------------- chat
async def _chat(session: str, prompt: str) -> Dict[str, Any]:
    async with _SEM:
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            chat = (LlmChat(api_key=os.environ.get("EMERGENT_LLM_KEY"), session_id=session, system_message=SYSTEM)
                    .with_model("anthropic", "claude-sonnet-4-6"))
            resp = await asyncio.wait_for(chat.send_message(UserMessage(text=prompt)), timeout=110)
            return _extract_json(resp if isinstance(resp, str) else str(resp))
        except Exception as exc:  # noqa: BLE001
            logger.warning("deep_report chunk '%s' failed: %s", session, repr(exc))
            return {}


# --------------------------------------------------------------------------- chunks (small & parallel)
def _c_exec(ctx: str) -> str:
    return (ctx + "\n\nReturn JSON:\n{"
            '"executive_summary":{"current":"1-2 sentences on where they are now","target":"their goal restated","difficulty":"brutally honest difficulty read","timeline":"realistic timeline","recommendation":"the single overall recommendation, 2-3 sentences","opportunities":["3 biggest opportunities"],"risks":["3 biggest risks"]},'
            '"success_blueprint":"the fastest REALISTIC (not easiest) path to success for this person, 4-6 sentences"}')


def _c_dna(ctx: str) -> str:
    return (ctx + "\n\nReturn JSON:\n{"
            '"career_dna":{"bars":[{"label":"Leadership Potential","value":0-100},{"label":"Analytical Thinking","value":0-100},{"label":"Communication","value":0-100},{"label":"Risk Tolerance","value":0-100},{"label":"Learning Ability","value":0-100},{"label":"Entrepreneurial Drive","value":0-100}],"analysis":["4-5 bullets explaining how their specific traits impact future success"]}}')


def _c_market(ctx: str) -> str:
    return (ctx + "\n\nReturn JSON:\n{"
            '"market_position":{"current":"honest paragraph: how valuable are they TODAY in the market","future":[{"period":"1 Year","text":"outlook"},{"period":"3 Year","text":"outlook"},{"period":"5 Year","text":"outlook"},{"period":"10 Year","text":"outlook incl AI impact"}]},'
            '"best_path":{"role":"the best career path name","daily_reality":"what a normal work day actually feels like","mindset":"required mindset","success_traits":["4 traits that succeed here"],"common_mistakes":["4 common mistakes"],"expectations":"what the industry expects"}}')


def _c_skill(ctx: str) -> str:
    return (ctx + "\n\nReturn JSON:\n{"
            '"skill_gap":[{"skill":"name","importance":0-100,"current":"None/Beginner/Intermediate/Advanced","target":"level","hours":estimated_hours_int,"why":"one line why it matters"}]}'
            "\nRules: 6-8 items ordered by importance (most important first).")


def _c_syllabus(ctx: str) -> str:
    return (ctx + "\n\nReturn JSON:\n{"
            '"syllabus":[{"phase":"Stage 1 — <name>","focus":"what this stage achieves + est. time","groups":[{"label":"Learn (in order)","items":["..."]},{"label":"Courses","items":["use the curated course names"]},{"label":"Books","items":["..."]},{"label":"Projects","items":["..."]}]}]}'
            "\nRules: a COMPLETE step-by-step learning syllabus (4-5 progressive stages) to reach the stated goal, weaving in the curated resources.")


def _c_projects(ctx: str) -> str:
    return (ctx + "\n\nReturn JSON:\n{"
            '"projects":[{"name":"specific project name","difficulty":"Beginner/Intermediate/Advanced","tools":["tools used"],"outcome":"what they build/learn","value":"resume & portfolio value"}]}'
            "\nRules: EXACTLY 10 concrete, portfolio-worthy projects tailored to the stated goal, ordered easiest->hardest. Keep each field short.")


def _c_tools(ctx: str) -> str:
    return (ctx + "\n\nReturn JSON:\n{"
            '"tool_stack":[{"tool":"exact tool","why":"why it matters for this goal"}],'  # 6-8
            '"networking":{"who":["4-5 specific types of people to connect with"],"where":["where to find them"],"weekly_target":"a concrete weekly networking target","linkedin":["4-5 LinkedIn optimization actions"],"templates":[{"title":"Cold connection request","text":"a ready-to-send message"},{"title":"Follow-up message","text":"a ready-to-send message"}]},'
            '"financial_prep":{"applicable":true_or_false,"points":["savings/emergency-fund/runway/income-bridge guidance if relevant; [] if not applicable"]}}')


def _c_brand(ctx: str) -> str:
    return (ctx + "\n\nReturn JSON:\n{"
            '"personal_brand":{"strategy":["4-5 authority-building actions"],"content_ideas":["~20 specific content ideas they can post"]}}'
            "\nRules: content_ideas must be specific to their field, short.")


def _c_plan30(ctx: str) -> str:
    return (ctx + "\n\nReturn JSON:\n{"
            '"plan_30":[{"label":"Day 1","text":"one concrete action (<=14 words)"}]}'
            "\nRules: a true day-by-day plan, ~20-30 entries spanning Day 1 to Day 30. Every entry is a concrete action, no fluff.")


def _c_plan_long(ctx: str) -> str:
    return (ctx + "\n\nReturn JSON:\n{"
            '"plan_90":[{"label":"Week 1","text":"the focus + key actions for this week"}],'
            '"plan_365":[{"label":"Month 1","text":"milestone + focus for this month"}]}'
            "\nRules: plan_90 = 12 weekly entries (Week 1..Week 12). plan_365 = 12 monthly entries (Month 1..Month 12). Keep each text concise.")


def _c_fail(ctx: str) -> str:
    return (ctx + "\n\nReturn JSON:\n{"
            '"failure_points":[{"title":"reason people fail","why":"why it happens","fix":"how to avoid it"}],'  # 5
            '"ai_impact":{"automated":["what AI will automate in this career"],"safe":["what stays valuable"],"future_proof":["how THIS person stays future-proof"]}}')


CHUNKS = [
    ("exec", _c_exec), ("dna", _c_dna), ("market", _c_market), ("skill", _c_skill),
    ("syllabus", _c_syllabus), ("projects", _c_projects), ("tools", _c_tools),
    ("brand", _c_brand), ("plan30", _c_plan30), ("planlong", _c_plan_long), ("fail", _c_fail),
]
_SEM = asyncio.Semaphore(5)  # tested-safe concurrency for the LLM key


# --------------------------------------------------------------------------- assembly
def _badge(text, tone):
    return {"text": text, "tone": tone}


def _diff_tone(d: str) -> str:
    d = (d or "").lower()
    return "emerald" if "begin" in d else "amber" if "inter" in d else "rose"


def _assemble(data: Dict[str, Any], report: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], set]:
    out: List[Dict[str, Any]] = []
    replaced: set = set()  # base section ids this deep content supersedes

    es = data.get("executive_summary") or {}
    if es.get("recommendation"):
        body = " ".join(filter(None, [
            f"<b>Where you are:</b> {es.get('current','')}" if es.get("current") else "",
        ])) if False else es["recommendation"]
        meta_pts = [p for p in [
            f"Where you are now: {es['current']}" if es.get("current") else None,
            f"Your target: {es['target']}" if es.get("target") else None,
            f"Transition difficulty: {es['difficulty']}" if es.get("difficulty") else None,
            f"Realistic timeline: {es['timeline']}" if es.get("timeline") else None,
        ] if p]
        out.append(sec("exec_summary", "Executive Summary", "FileText", "callout",
                       tone="indigo", label="The honest bottom line", text=body))
        cards = []
        if meta_pts:
            cards.append({"title": "Your Situation At A Glance", "badges": [_badge("Snapshot", "indigo")], "points": meta_pts})
        if es.get("opportunities"):
            cards.append({"title": "Your Biggest Opportunities", "badges": [_badge("Upside", "emerald")], "points": es["opportunities"]})
        if es.get("risks"):
            cards.append({"title": "Your Biggest Risks", "badges": [_badge("Watch out", "rose")], "points": es["risks"]})
        if cards:
            out.append(sec("exec_detail", "Opportunities & Risks", "Scale", "cards", items=cards))

    dna = data.get("career_dna") or {}
    if dna.get("bars"):
        bars = [{"label": b.get("label", ""), "value": int(b.get("value", 50)), "suffix": "%",
                 "tone": "emerald" if b.get("value", 50) >= 70 else "indigo" if b.get("value", 50) >= 45 else "amber"}
                for b in dna["bars"] if b.get("label")]
        out.append(sec("career_dna", "Your Career DNA", "Fingerprint", "bars", items=bars))
        if dna.get("analysis"):
            out.append(sec("career_dna_notes", "What Your DNA Means", "Brain", "list",
                           intro="How your specific wiring shapes your career:", items=dna["analysis"]))

    mp = data.get("market_position") or {}
    if mp.get("current"):
        out.append(sec("market_now", "Your Current Market Position", "Gauge", "intro", text=mp["current"]))
    if mp.get("future"):
        out.append(sec("market_future", "Your Future Market Position", "TrendingUp", "cards",
                       items=[{"title": f.get("period", ""), "badges": [_badge("Outlook", "indigo")], "body": f.get("text", "")}
                              for f in mp["future"] if f.get("text")]))

    bp = data.get("best_path") or {}
    if bp.get("daily_reality"):
        cards = [{"title": "A Day In This Career", "badges": [_badge(bp.get("role", "Best path"), "indigo")], "body": bp["daily_reality"]}]
        if bp.get("mindset"):
            cards.append({"title": "The Mindset It Demands", "badges": [_badge("Mindset", "purple")], "body": bp["mindset"]})
        if bp.get("success_traits"):
            cards.append({"title": "Traits That Win Here", "badges": [_badge("Success traits", "emerald")], "points": bp["success_traits"]})
        if bp.get("common_mistakes"):
            cards.append({"title": "Common Mistakes To Avoid", "badges": [_badge("Avoid", "rose")], "points": bp["common_mistakes"]})
        if bp.get("expectations"):
            cards.append({"title": "What The Industry Expects", "badges": [_badge("Expectations", "amber")], "body": bp["expectations"]})
        out.append(sec("best_path", "Deep Dive: Your Best Career Path", "Telescope", "cards", items=cards))

    sg = data.get("skill_gap") or []
    if sg:
        headers = ["Skill", "Importance", "Now", "Target", "Hours", "Why it matters"]
        rows = [[s.get("skill", ""), f"{int(s.get('importance', 0))}/100", s.get("current", "—"),
                 s.get("target", "—"), f"~{int(s.get('hours', 0))}h", s.get("why", "")]
                for s in sg]
        out.append(sec("skill_gap", "Skill Gap Analysis", "Puzzle", "table",
                       intro="The exact skills between you and your goal — ordered by importance:",
                       headers=headers, rows=rows))
        replaced.add("skill_gap")

    syl = data.get("syllabus") or []
    if syl:
        items = []
        for ph in syl:
            groups = [{"label": g.get("label", ""), "items": [i for i in (g.get("items") or []) if i]}
                      for g in (ph.get("groups") or []) if g.get("items")]
            items.append({"phase": ph.get("phase", ""), "focus": ph.get("focus", ""), "groups": groups})
        out.append(sec("syllabus", "Detailed Syllabus To Reach Your Goal", "Map", "blueprint", items=items))
        replaced.add("blueprint")

    pr = data.get("projects") or []
    if pr:
        cards = []
        for p in pr:
            pts = []
            if p.get("tools"):
                pts.append("Tools: " + ", ".join(p["tools"]))
            if p.get("value"):
                pts.append("Value: " + p["value"])
            cards.append({"title": p.get("name", ""), "badges": [_badge(p.get("difficulty", "Project"), _diff_tone(p.get("difficulty")))],
                          "body": p.get("outcome", ""), "points": pts})
        out.append(sec("projects", "Your Project Roadmap (10 Projects)", "FolderGit2", "cards", items=cards))

    ts = data.get("tool_stack") or []
    if ts:
        out.append(sec("tool_stack", "Your Tool Stack", "Wrench", "list",
                       intro="The exact tools to master — and why each one matters:",
                       items=[f"{t.get('tool','')} — {t.get('why','')}" for t in ts if t.get("tool")]))

    nw = data.get("networking") or {}
    if nw:
        cards = []
        if nw.get("who"):
            cards.append({"title": "Who To Connect With", "badges": [_badge("Targets", "indigo")], "points": nw["who"]})
        if nw.get("where"):
            cards.append({"title": "Where To Find Them", "badges": [_badge("Channels", "cyan")], "points": nw["where"]})
        if nw.get("linkedin"):
            cards.append({"title": "LinkedIn Strategy", "badges": [_badge("LinkedIn", "indigo")], "points": nw["linkedin"]})
        if nw.get("weekly_target"):
            cards.append({"title": "Your Weekly Target", "badges": [_badge("Cadence", "emerald")], "body": nw["weekly_target"]})
        if cards:
            out.append(sec("networking", "Networking Strategy", "Network", "cards", items=cards))
        if nw.get("templates"):
            out.append(sec("net_templates", "Cold Message Templates (ready to send)", "MessageSquare", "cards",
                           items=[{"title": t.get("title", "Message"), "badges": [_badge("Copy & send", "purple")], "body": t.get("text", "")}
                                  for t in nw["templates"] if t.get("text")]))

    pb = data.get("personal_brand") or {}
    if pb.get("strategy"):
        out.append(sec("personal_brand", "Personal Brand Strategy", "BadgeCheck", "list",
                       intro="Build authority so opportunities come to you:", items=pb["strategy"]))
    if pb.get("content_ideas"):
        out.append(sec("content_ideas", "Content Ideas To Build Authority", "Lightbulb", "tags",
                       intro="Ready-to-use content ideas — post consistently:", items=pb["content_ideas"]))

    fp = data.get("financial_prep") or {}
    if fp.get("applicable") and fp.get("points"):
        out.append(sec("financial_prep", "Financial Preparation Plan", "PiggyBank", "list",
                       intro="Protect your runway as you make this move:", items=fp["points"]))

    p30 = data.get("plan_30") or []
    if p30:
        out.append(sec("plan_30", "Your 30-Day Execution Plan", "Rocket", "timeline",
                       intro="Exactly what to do, day by day:",
                       items=[{"label": d.get("label", ""), "text": d.get("text", "")} for d in p30 if d.get("text")]))
        replaced.update({"action_30", "action_90", "learning_plan", "growth_90", "growth_year"})

    p90 = data.get("plan_90") or []
    if p90:
        out.append(sec("plan_90", "Your 90-Day Execution Plan", "CalendarCheck", "timeline",
                       intro="Week-by-week strategy for your first 90 days:",
                       items=[{"label": w.get("label", ""), "text": w.get("text", "")} for w in p90 if w.get("text")]))
        replaced.update({"action_90", "growth_90", "learning_plan", "growth_year"})

    p365 = data.get("plan_365") or []
    if p365:
        out.append(sec("plan_365", "Your 365-Day Master Roadmap", "CalendarDays", "timeline",
                       intro="Month-by-month milestones for your first year:",
                       items=[{"label": m.get("label", ""), "text": m.get("text", "")} for m in p365 if m.get("text")]))

    fps = data.get("failure_points") or []
    if fps:
        out.append(sec("failure_points", "Common Failure Points (and how to avoid them)", "AlertTriangle", "cards",
                       items=[{"title": f.get("title", ""), "badges": [_badge("Why it happens", "rose")],
                               "body": f.get("why", ""), "points": [f"Fix: {f.get('fix','')}"] if f.get("fix") else []}
                              for f in fps]))

    ai = data.get("ai_impact") or {}
    if ai.get("automated") or ai.get("safe") or ai.get("future_proof"):
        cards = []
        if ai.get("automated"):
            cards.append({"title": "What AI Will Automate", "badges": [_badge("At risk", "rose")], "points": ai["automated"]})
        if ai.get("safe"):
            cards.append({"title": "What Stays Valuable", "badges": [_badge("Safe", "emerald")], "points": ai["safe"]})
        if ai.get("future_proof"):
            cards.append({"title": "How You Stay Future-Proof", "badges": [_badge("Your moat", "indigo")], "points": ai["future_proof"]})
        out.append(sec("ai_impact", "AI Impact Report", "Bot", "cards", items=cards))

    if es.get("recommendation") and data.get("success_blueprint"):
        out.append(sec("success_blueprint", "Your Success Blueprint", "Trophy", "callout",
                       tone="emerald", label="The fastest realistic path", text=data["success_blueprint"]))

    return out, replaced


async def generate_deep_sections(profile: Dict[str, Any], report: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], set]:
    """Return (deep_sections, base_section_ids_to_remove). Empty list on total failure."""
    if not os.environ.get("EMERGENT_LLM_KEY"):
        return [], set()
    _, resources = _resources(profile, report)
    ctx = _ctx(profile, report, resources)
    sid = f"deep-{profile.get('name','u')}-{report.get('user_type')}"

    chunks = await asyncio.gather(
        *[_chat(f"{sid}-{tag}", build(ctx)) for tag, build in CHUNKS],
        return_exceptions=True,
    )
    data: Dict[str, Any] = {}
    for c in chunks:
        if isinstance(c, dict):
            data.update(c)
    return _assemble(data, report)
