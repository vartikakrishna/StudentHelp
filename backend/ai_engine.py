"""AI narrative layer (Claude Sonnet 4.6) — explains deterministic results in a
brutally honest, practical tone. Always returns a complete dict via fallback."""
import os
import json
import re
import asyncio
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")

SYSTEM = (
    "You are a brutally honest senior career strategist writing a paid Career Blueprint. "
    "ZERO sugar-coating. No motivational fluff, no astrology, no 'you can be anything', no empty reassurance. "
    "If a path is a bad bet, say it bluntly and say why. Name the uncomfortable truths most advisors avoid: "
    "wasted years, weak skills, oversaturated fields, automation risk, and the real cost of indecision. "
    "Back every hard claim with the data given. Be direct, specific, practical and respectful — honest, never cruel. "
    "Do not soften verdicts with hedging like 'but anything is possible'. Keep every field tight and skimmable. "
    "Respond with ONLY valid JSON, no markdown fences, no commentary."
)


def _extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    text = re.sub(r"^```(json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    s, e = text.find("{"), text.rfind("}")
    if s != -1 and e != -1:
        text = text[s:e + 1]
    return json.loads(text)


def _fallback(profile: Dict[str, Any], bp: Dict[str, Any]) -> Dict[str, Any]:
    name = (profile.get("name") or "there").split(" ")[0]
    top = bp["matches"][0]
    second = bp["matches"][1]
    traits = bp["trait_labels"]
    sp = bp["salary_projection"]
    avoid0 = bp["careers_to_avoid"][0]["title"] if bp.get("careers_to_avoid") else "low-skill routine roles"
    return {
        "career_reality_check": (
            f"Here's the honest version, {name}: your strongest realistic path is {top['title']} "
            f"({top['score']}% fit, {top['ai_risk_label'].lower()}). It is not the easiest option — expect "
            f"{top['time_to_enter']} of real work and {top['competition']}% competition — but the fundamentals "
            f"(demand {top['market_demand']}%, salary {top['salary_score']}%) are on your side. Stop spreading "
            f"yourself thin; commit to one direction and compound."
        ),
        "personality_insight": f"You operate as a {traits[1].lower()} and a {traits[3].lower()}. Lean into that — don't fight it.",
        "strengths": [{"label": s["label"], "description": f"Rated {s['score']}% — a genuine edge worth building on."} for s in bp["strength_scores"]],
        "weaknesses": [
            {"title": f"Low {bp['weakness']['label']}", "description": "This is your weakest area — delegate it or pick paths that don't depend on it."},
            {"title": "Spreading too thin", "description": "Breadth feels safe but kills depth. Pick one lane for 12 months."},
        ],
        "hidden_talent": {"title": "Pattern Architect", "description": f"You connect ideas others miss — a real asset in {top['title'].split('/')[0].strip()} work."},
        "match_explanations": {m["key"]: f"{m['verdict']} — strengths map onto a {m['title'].split('/')[0].strip()} ({m['score']}% fit)." for m in bp["matches"]},
        "careers_to_avoid_note": (
            f"Be honest with yourself about {avoid0}: weak alignment and/or rising automation make it a poor bet for your profile. "
            f"Admiring a field is not the same as being built for it."
        ),
        "ai_threat_summary": (
            f"Your top-3 portfolio carries {bp['ai_risk_label'].lower()} ({bp['portfolio_ai_risk']}% avg AI exposure). "
            f"Survival strategy: move up the value chain — judgement, systems and human trust beat routine execution that AI now does cheaply."
        ),
        "entrepreneurship": f"Business potential {bp['business_potential']}%. Start as a solopreneur inside {top['industries'][0]} before building a team.",
        "resume_linkedin": "Rewrite your resume around measurable impact (numbers, not duties). On LinkedIn, fix the headline and About to target one role, not five.",
        "interview_readiness": f"Prepare 20 role-specific questions for {top['title'].split('/')[0].strip()}, 3 STAR stories, and one portfolio project you can defend deeply.",
        "future_self_letter": (
            f"Dear {name},\n\nFive years from now, you finally stopped guessing. You committed to {top['title']} and gave it everything. "
            f"It was hard — {top['time_to_enter']} of real effort — but every week compounded. Today you earn around ₹{sp['year5']} LPA, "
            f"you're respected for what you build, and the fear of wasting years is gone. The version of you reading this is exactly where "
            f"that decision begins. Don't wait. Choose. Begin.\n\n— Your Future Self"
        ),
        "future_industries": [
            f"{top['industries'][0]} keeps expanding as AI adoption accelerates.",
            f"{second['industries'][0]} offers a strong secondary lane.",
            "Roles blending domain expertise + AI tooling will pay the most.",
        ],
    }


async def enhance_report(profile: Dict[str, Any], bp: Dict[str, Any]) -> Dict[str, Any]:
    if not EMERGENT_LLM_KEY:
        return _fallback(profile, bp)

    name = profile.get("name", "Student")
    matches_summary = "; ".join(f"{m['title']} (fit {m['score']}%, {m['ai_risk_label']}, demand {m['market_demand']}%, comp {m['competition']}%)" for m in bp["matches"][:3])
    avoid_summary = "; ".join(m["title"] for m in bp.get("careers_to_avoid", [])[:3])

    prompt = f"""Profile: {name}, user-type {profile.get('user_type')}, age {profile.get('age')}, education {profile.get('education')}/{profile.get('current_degree')}, profession {profile.get('current_profession')}.
Personality: {bp['trait_labels']}.
TOP MATCHES (deterministic, DO NOT change numbers): {matches_summary}.
CAREERS TO AVOID (deterministic): {avoid_summary}.
Portfolio AI risk: {bp['portfolio_ai_risk']}% ({bp['ai_risk_label']}). Business {bp['business_potential']}%, Leadership {bp['leadership_potential']}%. 5-yr salary est ₹{bp['salary_projection']['year5']} LPA.

Write ONLY this JSON (brutally honest, NO sugar-coating, concise, 1-3 sentences each unless noted. State hard truths plainly and back them with the numbers above):
{{
  "career_reality_check": "120-160 words, hard truths + the realistic best path",
  "personality_insight": "2 sentences",
  "strengths": [{{"label":"name","description":"one line"}}],
  "weaknesses": [{{"title":"2-3 words","description":"one line, honest"}}],
  "hidden_talent": {{"title":"2-4 words","description":"2 sentences"}},
  "match_explanations": {{ {", ".join(f'"{m["key"]}":"one honest line"' for m in bp["matches"])} }},
  "careers_to_avoid_note": "2 sentences, direct",
  "ai_threat_summary": "2-3 sentences incl. a survival strategy",
  "entrepreneurship": "2 sentences",
  "resume_linkedin": "2 sentences, actionable",
  "interview_readiness": "2 sentences, actionable",
  "future_self_letter": "120-200 words, second person, signed 'Your Future Self'",
  "future_industries": ["3 short predictions"]
}}"""

    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=f"blueprint-{name}", system_message=SYSTEM).with_model("anthropic", "claude-sonnet-4-6")
        resp = await asyncio.wait_for(chat.send_message(UserMessage(text=prompt)), timeout=28)
        data = _extract_json(resp if isinstance(resp, str) else str(resp))
        fb = _fallback(profile, bp)
        for k, v in fb.items():
            if not data.get(k):
                data[k] = v
        return data
    except Exception as e:  # noqa: BLE001
        logger.warning("AI enhancement failed, using fallback: %s", e)
        return _fallback(profile, bp)
