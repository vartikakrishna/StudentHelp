"""AI narrative layer (Claude Sonnet 4.6) — rewrites the key prose blocks of each
typed report in a brutally honest, category-specific voice. Deterministic text
already fills every section, so AI failure is a safe no-op.
"""
import os
import json
import re
import asyncio
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")

SYSTEM = (
    "You are a brutally honest senior career strategist writing a paid, category-specific Career Blueprint. "
    "ZERO sugar-coating. No motivational fluff, no astrology, no 'you can be anything'. Name the uncomfortable "
    "truths most advisors avoid and back them with the data given. Direct, specific, practical — honest, never cruel. "
    "Write for the user's exact situation (student vs IT employee vs working professional etc.). "
    "Respond with ONLY valid JSON, no markdown fences, no commentary."
)

# section id -> JSON key the AI fills (only these prose blocks are AI-rewritten)
AI_FIELDS = {"reality_check": "reality_check", "verdict": "verdict",
             "outlook": "outlook", "letter": "letter"}


def _extract_json(text: str) -> Dict[str, Any]:
    text = re.sub(r"```(json)?", "", text.strip()).strip()
    s, e = text.find("{"), text.rfind("}")
    if s != -1 and e != -1:
        text = text[s:e + 1]
    return json.loads(text)


def _summary(profile: Dict[str, Any], report: Dict[str, Any]) -> str:
    scores = report.get("preview", {}).get("scores", [])
    sline = "; ".join(f"{s['label']}={s.get('value')}" for s in scores if not s.get("locked") and s.get("value") is not None)
    matches = report.get("matches", [])
    mline = ", ".join(f"{m['title']} ({m['score']}%)" for m in matches[:3])
    pers = profile.get("personality", {})
    return (f"Product: {report.get('product_name')}. Goal: {report.get('primary_goal')}. "
            f"User type: {report.get('user_type')}. Name: {profile.get('name')}. "
            f"Report focus: {report.get('ai_focus', 'honest career analysis')}. "
            f"Key scores: {sline}. Top paths: {mline}. "
            f"5-yr salary est ₹{report.get('salary_projection', {}).get('year5')} LPA. "
            f"Personality: {pers.get('mind')}, {pers.get('approach')}, {pers.get('risk')}, "
            f"leadership {pers.get('leadership_interest')}/10, communication {pers.get('communication')}/10.")


async def enhance(profile: Dict[str, Any], report: Dict[str, Any]) -> Dict[str, Any]:
    """Rewrite the AI-eligible prose blocks in-place. Safe no-op on any failure."""
    if not EMERGENT_LLM_KEY:
        return report

    wants = [s["id"] for s in report.get("sections", []) if s.get("id") in AI_FIELDS and "text" in s]
    if not wants:
        return report

    fields = []
    if "reality_check" in wants:
        fields.append('"reality_check": "120-160 words, hard truths + the realistic best move for THIS person"')
    if "verdict" in wants:
        fields.append('"verdict": "2-3 sentences, a blunt verdict + the single most important action"')
    if "outlook" in wants:
        fields.append('"outlook": "2 sentences, honest industry/field outlook"')
    if "letter" in wants:
        fields.append('"letter": "120-180 words, second person, signed exactly: — Your Future Self"')

    prompt = (f"{_summary(profile, report)}\n\nWrite ONLY this JSON, brutally honest and specific to this person, "
              f"no sugar-coating:\n{{ {', '.join(fields)} }}")

    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=f"cb-{profile.get('name','u')}-{report.get('user_type')}",
                       system_message=SYSTEM).with_model("anthropic", "claude-sonnet-4-6")
        resp = await asyncio.wait_for(chat.send_message(UserMessage(text=prompt)), timeout=28)
        data = _extract_json(resp if isinstance(resp, str) else str(resp))
        for s in report.get("sections", []):
            key = AI_FIELDS.get(s.get("id"))
            if key and key in data and isinstance(data[key], str) and data[key].strip():
                s["text"] = data[key].strip()
        if data.get("reality_check"):
            report["career_reality_check"] = data["reality_check"].strip()
        if data.get("verdict"):
            report.setdefault("preview", {})["verdict"] = data["verdict"].strip()
    except Exception as e:  # noqa: BLE001
        logger.warning("AI enhance failed (using deterministic text): %s", e)
    return report
