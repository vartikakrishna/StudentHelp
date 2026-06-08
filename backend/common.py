"""Shared scoring helpers used by all per-type analysis engines.

- Personality (8 high-value traits) -> trait vector + modifiers (20% weighting).
- Interest-norm builder from category answers (subjects / interests).
- Typed report-section builder used by every engine (data-driven reports).
"""
from typing import Dict, List, Any
from careers import ai_risk_label, INTEREST_LABELS  # noqa: F401  (re-exported for engines)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def num(v, default=0.0):
    try:
        return float(str(v).replace(",", "").replace("₹", "").strip())
    except (TypeError, ValueError):
        return default


def as_list(v) -> List[str]:
    if isinstance(v, list):
        return [str(x) for x in v if str(x).strip()]
    if v is None:
        return []
    return [s.strip() for s in str(v).replace(",", "\n").split("\n") if s.strip()]


# ----------------------- Personality (8 traits, 20% weight) -----------------------
def traits_from_personality(pers: Dict[str, Any]) -> Dict[str, float]:
    def sld(k, d=5):
        try:
            return clamp(float(pers.get(k, d)) / 10.0, 0.0, 1.0)
        except (TypeError, ValueError):
            return 0.5
    lead = sld("leadership_interest")
    return {
        "introvert": 1.0 if pers.get("mind") == "introvert" else 0.0,
        "extrovert": 1.0 if pers.get("mind") == "extrovert" else 0.0,
        "creative": 1.0 if pers.get("approach") == "creative" else 0.0,
        "analytical": 1.0 if pers.get("approach") == "analytical" else 0.0,
        "risk": 1.0 if pers.get("risk") == "risk_taker" else 0.0,
        "stable": 1.0 if pers.get("risk") == "stable" else 0.0,
        "team": 1.0 if pers.get("work_style") == "team" else 0.0,
        "independent": 1.0 if pers.get("work_style") == "independent" else 0.0,
        "structured": 1.0 if pers.get("structure") == "structured" else 0.0,
        "flexible": 1.0 if pers.get("structure") == "flexible" else 0.0,
        "leader": 1.0 if lead >= 0.6 else 0.0,
        "specialist": 1.0 if lead < 0.6 else 0.0,
        "leadership": lead,
        "communication": sld("communication"),
        "stress": sld("stress_tolerance"),
    }


def trait_labels(t: Dict[str, float]) -> List[str]:
    return [
        "Extroverted Connector" if t["extrovert"] else "Introspective Deep-Worker",
        "Analytical Strategist" if t["analytical"] else "Creative Originator",
        "Bold Risk-Taker" if t["risk"] else "Steady Stabiliser",
        "Team Player" if t["team"] else "Independent Operator",
        "Structured Planner" if t["structured"] else "Flexible Improviser",
    ]


# ----------------------- Interest mapping (for discovery types) -----------------------
SUBJECT_TO_INTEREST = {
    "Mathematics": ["problem_solving", "finance", "technology"],
    "Physics": ["technology", "research", "problem_solving"],
    "Chemistry": ["research", "healthcare"],
    "Biology": ["healthcare", "research"],
    "Computer Science": ["technology", "problem_solving"],
    "Economics": ["finance", "business"],
    "Business Studies": ["business", "entrepreneurship"],
    "Accountancy": ["finance"],
    "English / Languages": ["writing", "content_creation"],
    "History / Civics": ["law", "teaching"],
    "Geography": ["research"],
    "Psychology": ["psychology"],
    "Art / Design": ["design", "content_creation"],
    "Physical Education / Sports": ["leadership"],
    "Political Science": ["law", "leadership"],
    "Commerce": ["business", "finance"],
}

CAREER_INTEREST_TO_INTEREST = {
    "Software / IT": ["technology", "problem_solving"],
    "Engineering": ["technology", "problem_solving"],
    "Medicine / Healthcare": ["healthcare"],
    "Business / Management": ["business", "leadership"],
    "Finance / Banking": ["finance", "business"],
    "Design / Creative": ["design", "content_creation"],
    "Law": ["law"],
    "Marketing / Media": ["marketing", "content_creation"],
    "Teaching / Research": ["teaching", "research"],
    "Government / Civil Services": ["law", "leadership"],
    "Entrepreneurship / Startup": ["entrepreneurship", "business"],
    "Content / Influencer": ["content_creation", "marketing"],
    "Psychology / Counselling": ["psychology"],
    "Sales / Business Dev": ["sales", "business"],
}


def build_interest_norm(favorites: List[str], career_interests: List[str], traits: Dict[str, float]) -> Dict[str, float]:
    """Map category answers -> the 16-dim interest-norm careers.py expects (values 0..1)."""
    scores = {k: 0.0 for k in INTEREST_LABELS}
    for s in favorites:
        for key in SUBJECT_TO_INTEREST.get(s, []):
            scores[key] = scores.get(key, 0.0) + 1.0
    for c in career_interests:
        for key in CAREER_INTEREST_TO_INTEREST.get(c, []):
            scores[key] = scores.get(key, 0.0) + 1.2
    # personality nudges (20% influence)
    scores["leadership"] = scores.get("leadership", 0) + traits["leadership"] * 1.5
    scores["entrepreneurship"] = scores.get("entrepreneurship", 0) + traits["risk"] * 1.0
    scores["problem_solving"] = scores.get("problem_solving", 0) + traits["analytical"] * 1.0
    scores["design"] = scores.get("design", 0) + traits["creative"] * 0.8
    scores["technology"] = scores.get("technology", 0) + traits["analytical"] * 0.6
    mx = max(scores.values()) or 1.0
    return {k: clamp(0.25 + (v / mx) * 0.75, 0.0, 1.0) for k, v in scores.items()}


# ----------------------- Salary helper -----------------------
def salary_projection(salary: Dict[str, int]) -> Dict[str, int]:
    return {"year1": salary["entry"], "year3": round(salary["entry"] * 1.5),
            "year5": salary["mid"], "year10": salary["senior"]}


# ----------------------- Typed report-section builder -----------------------
def sec(sid: str, title: str, icon: str, stype: str, **data) -> Dict[str, Any]:
    """Build one typed report block. Renderer (web + PDF) maps `stype` -> layout."""
    return {"id": sid, "title": title, "icon": icon, "type": stype, **data}


def diagnostic_sections(risks, opportunities, focus, stop):
    """The universal backbone every report shares (content differs per category):
    Q2 risks · Q3 missed opportunities · Q4 what to focus on · Q5 what to stop."""
    return [
        sec("risks", "Your Biggest Risks", "ShieldAlert", "cards", items=risks),
        sec("opportunities", "Opportunities You're Missing", "Lightbulb", "cards", items=opportunities),
        sec("focus", "What To Focus On Next", "Target", "list", intro="Your highest-leverage moves right now:", items=focus),
        sec("stop", "What To Stop Doing", "Ban", "list", intro="These are quietly holding you back — stop now:", items=stop),
    ]


def action_roadmap(d30, d90, y1, extra=None):
    """Q6/Q7/Q8 — 30-day, 90-day and 1-year plan. `extra` adds an optional 4th phase."""
    items = [
        {"phase": "Next 30 Days", "focus": d30.get("focus"), "points": d30["points"]},
        {"phase": "Next 90 Days", "focus": d90.get("focus"), "points": d90["points"]},
        {"phase": "Next 1 Year", "focus": y1.get("focus"), "points": y1["points"]},
    ]
    if extra:
        items.append({"phase": extra["phase"], "focus": extra.get("focus"), "points": extra["points"]})
    return sec("roadmap", "Your 30 / 90 / 365-Day Action Plan", "Map", "roadmap", items=items)


def growth_sp(base):
    base = max(2, round(base))
    return {"year1": base, "year3": round(base * 1.6), "year5": round(base * 2.4), "year10": round(base * 3.8)}
