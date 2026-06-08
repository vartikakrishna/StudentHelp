"""AI narrative layer. Explains deterministic results in concise premium copy.

Always returns a complete dict. If the LLM call fails or times out, a
template-based fallback guarantees a fast, valid report (< 10s end to end).
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
    "You are a sharp, premium career strategist writing a paid 'Career Blueprint' for a student. "
    "Tone: confident, warm, specific, motivating. Never generic. Keep every field tight and skimmable. "
    "You MUST respond with ONLY valid JSON, no markdown fences, no commentary."
)


def _extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    text = re.sub(r"^```(json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end + 1]
    return json.loads(text)


def _fallback(profile: Dict[str, Any], blueprint: Dict[str, Any]) -> Dict[str, Any]:
    name = profile.get("name", "there").split(" ")[0]
    top = blueprint["matches"][0]
    second = blueprint["matches"][1]
    traits = blueprint["trait_labels"]
    sp = blueprint["salary_projection"]
    return {
        "personality_insight": (
            f"You are a {traits[1].lower()} with the instincts of a {traits[3].lower()}. "
            f"That rare combination means you don't just follow paths \u2014 you tend to redesign them. "
            f"Your decisions are driven by {('impact and people' if traits[0].startswith('Extro') else 'depth and mastery')}."
        ),
        "hidden_strength": {
            "title": "Pattern Architect",
            "description": (
                f"{name}, you naturally connect ideas others see as unrelated. This makes you unusually strong at "
                f"{top['title'].split('/')[0].strip()} work, where seeing the whole board beats memorising the rules."
            ),
        },
        "career_dna": (
            f"Your Career DNA points sharply toward {top['title']}. With a {top['score']}% alignment, your interests and "
            f"personality reinforce each other instead of pulling apart. You combine the analytical edge needed to solve "
            f"hard problems with enough creative range to avoid being replaced by automation. Your second strongest fit, "
            f"{second['title']}, gives you a powerful backup lane \u2014 meaning you are not betting your future on a single door. "
            f"The data says: stop second-guessing, and start compounding skills in one direction."
        ),
        "match_explanations": {
            m["key"]: f"Your strengths map directly onto what makes a great {m['title'].split('/')[0].strip()} \u2014 a {m['score']}% fit."
            for m in blueprint["matches"]
        },
        "strengths": [
            {"label": s["label"], "description": f"Rated {s['score']}% \u2014 a genuine competitive edge you can build a career around."}
            for s in blueprint["strength_scores"]
        ],
        "growth_obstacles": [
            {"title": "Decision Paralysis", "description": "Too many options can freeze you. Commit to one path for 90 days before judging it."},
            {"title": "Shiny-Object Syndrome", "description": "Your curiosity is a gift and a trap. Depth beats breadth in the first 5 years."},
            {"title": "Avoiding Visibility", "description": "Great work unseen is wasted. Build in public to multiply your luck."},
        ],
        "learning_roadmap": [
            {"phase": "0\u20133 Months", "focus": f"Master the fundamentals of {top['title'].split('/')[0].strip()}", "skills": ["Core tools", "Daily practice", "One real project"]},
            {"phase": "3\u201312 Months", "focus": "Build proof of skill", "skills": ["Portfolio", "Internship / freelance", "Niche specialisation"]},
            {"phase": "1\u20133 Years", "focus": "Compound advantage", "skills": ["Network", "Leadership reps", "Income growth"]},
        ],
        "entrepreneurship": (
            f"Your business potential sits at {blueprint['business_potential']}%. You have the raw material to build something of "
            f"your own \u2014 start as a 'solopreneur' inside the {top['industries'][0]} space before scaling a team."
        ),
        "future_self_letter": (
            f"Dear {name},\n\nFive years from now, you finally stopped guessing. You chose {top['title']} and gave it everything. "
            f"It wasn't always easy, but every late night compounded. Today you earn around \u20b9{sp['year5']} LPA, you are respected "
            f"for what you build, and the fear of 'wasting years' is gone. The version of you reading this letter is exactly where "
            f"that decision began. Don't wait. Choose. Begin.\n\n\u2014 Your Future Self"
        ),
    }


async def enhance_report(profile: Dict[str, Any], blueprint: Dict[str, Any]) -> Dict[str, Any]:
    if not EMERGENT_LLM_KEY:
        return _fallback(profile, blueprint)

    name = profile.get("name", "Student")
    goals = profile.get("goals", {})
    matches_summary = ", ".join(f"{m['title']} ({m['score']}%)" for m in blueprint["matches"][:3])
    strengths_summary = ", ".join(f"{s['label']} ({s['score']}%)" for s in blueprint["strength_scores"])

    prompt = f"""Student profile:
Name: {name}
Age: {profile.get('age')}, Education: {profile.get('education')}, Stream: {profile.get('stream')}
Personality: {blueprint['trait_labels']}
Top career matches (deterministic, DO NOT change numbers): {matches_summary}
Top strengths (deterministic): {strengths_summary}
Goals/priorities: {goals.get('priorities')}; Dream income: {goals.get('dream_income')}; Biggest challenge: {goals.get('challenge')}
Business potential: {blueprint['business_potential']}%, Leadership: {blueprint['leadership_potential']}%
5-year salary estimate: {blueprint['salary_projection']['year5']} LPA

Write ONLY this JSON (each text field concise, no fluff):
{{
  "personality_insight": "2 sentences, sharp and personal",
  "hidden_strength": {{"title": "2-4 words", "description": "2 sentences"}},
  "career_dna": "120-160 words explaining their dominant career identity",
  "match_explanations": {{ {", ".join(f'"{m["key"]}": "one line why it fits"' for m in blueprint["matches"])} }},
  "strengths": [{{"label": "name", "description": "one line"}}],  // 5 items, reuse the strength names above
  "growth_obstacles": [{{"title": "2-3 words", "description": "one line actionable"}}],  // 3 items
  "learning_roadmap": [{{"phase": "0-3 Months", "focus": "...", "skills": ["s1","s2","s3"]}}],  // 3 phases
  "entrepreneurship": "2 sentences",
  "future_self_letter": "120-200 words, second person, signed 'Your Future Self', emotional but grounded"
}}"""

    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"blueprint-{name}",
            system_message=SYSTEM,
        ).with_model("openai", "gpt-5.4-mini")
        resp = await asyncio.wait_for(
            chat.send_message(UserMessage(text=prompt)), timeout=22
        )
        data = _extract_json(resp if isinstance(resp, str) else str(resp))
        fb = _fallback(profile, blueprint)
        # Merge: AI values win, fallback fills any gaps
        for k, v in fb.items():
            if not data.get(k):
                data[k] = v
        return data
    except Exception as e:  # noqa: BLE001
        logger.warning("AI enhancement failed, using fallback: %s", e)
        return _fallback(profile, blueprint)
