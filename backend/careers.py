"""Deterministic career scoring engine.

Numbers come from deterministic math (no AI). The AI layer only *explains*
these results, which keeps generation fast and hallucination-free.
"""
from typing import Dict, List, Any

CAREERS: List[Dict[str, Any]] = [
    {
        "key": "ai_ml_engineer",
        "title": "AI / Machine Learning Engineer",
        "icon": "Cpu",
        "tagline": "Build the intelligent systems shaping the future.",
        "weights": {"technology": 1.0, "finance": 0.25, "design": 0.2, "business": 0.2, "leadership": 0.15},
        "traits": {"analytical": 1.0, "specialist": 0.6, "introvert": 0.3, "creative": 0.4},
        "ai_resistance": 96,
        "salary": {"entry": 9, "mid": 28, "senior": 70},
        "growth": "Explosive",
        "industries": ["Artificial Intelligence", "Big Tech", "Fintech", "Autonomous Systems"],
    },
    {
        "key": "data_scientist",
        "title": "Data Scientist",
        "icon": "BarChart3",
        "tagline": "Turn raw data into million-dollar decisions.",
        "weights": {"technology": 0.85, "finance": 0.6, "business": 0.5, "psychology": 0.2, "leadership": 0.2},
        "traits": {"analytical": 1.0, "specialist": 0.5, "creative": 0.3},
        "ai_resistance": 88,
        "salary": {"entry": 8, "mid": 24, "senior": 55},
        "growth": "Explosive",
        "industries": ["Technology", "Finance", "Healthcare", "E-commerce"],
    },
    {
        "key": "product_manager",
        "title": "Product Manager",
        "icon": "Rocket",
        "tagline": "Lead products millions of people love.",
        "weights": {"technology": 0.6, "business": 0.9, "leadership": 0.8, "design": 0.4, "psychology": 0.4},
        "traits": {"leader": 1.0, "extrovert": 0.6, "analytical": 0.6, "risk": 0.4},
        "ai_resistance": 85,
        "salary": {"entry": 10, "mid": 30, "senior": 75},
        "growth": "High",
        "industries": ["Technology", "SaaS", "Fintech", "Consumer Apps"],
    },
    {
        "key": "ux_designer",
        "title": "Product / UX Designer",
        "icon": "Palette",
        "tagline": "Design experiences that feel like magic.",
        "weights": {"design": 1.0, "technology": 0.5, "psychology": 0.5, "content_creation": 0.4, "business": 0.3},
        "traits": {"creative": 1.0, "specialist": 0.4, "introvert": 0.2},
        "ai_resistance": 78,
        "salary": {"entry": 6, "mid": 18, "senior": 45},
        "growth": "High",
        "industries": ["Technology", "Design Studios", "Startups", "Gaming"],
    },
    {
        "key": "doctor",
        "title": "Doctor / Medical Specialist",
        "icon": "HeartPulse",
        "tagline": "Save lives and earn lifelong respect.",
        "weights": {"healthcare": 1.0, "psychology": 0.5, "teaching": 0.2},
        "traits": {"analytical": 0.7, "specialist": 0.8},
        "ai_resistance": 92,
        "salary": {"entry": 7, "mid": 20, "senior": 60},
        "growth": "Stable",
        "industries": ["Hospitals", "Medical Research", "Public Health", "Private Practice"],
    },
    {
        "key": "psychologist",
        "title": "Clinical Psychologist / Therapist",
        "icon": "Brain",
        "tagline": "Heal minds in a world that needs it most.",
        "weights": {"psychology": 1.0, "healthcare": 0.5, "teaching": 0.4, "content_creation": 0.2},
        "traits": {"creative": 0.4, "specialist": 0.6, "introvert": 0.3, "extrovert": 0.3},
        "ai_resistance": 90,
        "salary": {"entry": 5, "mid": 14, "senior": 35},
        "growth": "High",
        "industries": ["Healthcare", "Wellness", "Corporate", "EdTech"],
    },
    {
        "key": "entrepreneur",
        "title": "Entrepreneur / Startup Founder",
        "icon": "Flame",
        "tagline": "Build your own empire and own your time.",
        "weights": {"business": 1.0, "leadership": 0.9, "finance": 0.5, "content_creation": 0.4, "technology": 0.4, "design": 0.3},
        "traits": {"risk": 1.0, "leader": 0.9, "extrovert": 0.6, "creative": 0.6},
        "ai_resistance": 89,
        "salary": {"entry": 4, "mid": 25, "senior": 100},
        "growth": "Explosive",
        "industries": ["Startups", "E-commerce", "SaaS", "D2C Brands"],
    },
    {
        "key": "investment_banker",
        "title": "Investment Banker / Financial Analyst",
        "icon": "TrendingUp",
        "tagline": "Move markets and master money.",
        "weights": {"finance": 1.0, "business": 0.7, "leadership": 0.4, "technology": 0.3},
        "traits": {"analytical": 0.9, "risk": 0.5, "specialist": 0.4},
        "ai_resistance": 72,
        "salary": {"entry": 12, "mid": 35, "senior": 90},
        "growth": "High",
        "industries": ["Investment Banking", "Private Equity", "Hedge Funds", "Consulting"],
    },
    {
        "key": "lawyer",
        "title": "Corporate Lawyer",
        "icon": "Scale",
        "tagline": "Command the courtroom and the boardroom.",
        "weights": {"law": 1.0, "leadership": 0.5, "business": 0.4, "psychology": 0.3},
        "traits": {"analytical": 0.7, "extrovert": 0.5, "leader": 0.5, "specialist": 0.4},
        "ai_resistance": 80,
        "salary": {"entry": 7, "mid": 22, "senior": 65},
        "growth": "Stable",
        "industries": ["Law Firms", "Corporate Legal", "Judiciary", "Compliance"],
    },
    {
        "key": "educator",
        "title": "Educator / EdTech Creator",
        "icon": "GraduationCap",
        "tagline": "Shape the next generation and scale your impact.",
        "weights": {"teaching": 1.0, "psychology": 0.5, "content_creation": 0.5, "technology": 0.3},
        "traits": {"extrovert": 0.5, "creative": 0.5, "specialist": 0.4},
        "ai_resistance": 83,
        "salary": {"entry": 4, "mid": 12, "senior": 40},
        "growth": "High",
        "industries": ["EdTech", "Schools", "Universities", "Online Courses"],
    },
    {
        "key": "content_creator",
        "title": "Content Creator / Digital Marketer",
        "icon": "Video",
        "tagline": "Turn attention into income and influence.",
        "weights": {"content_creation": 1.0, "design": 0.6, "business": 0.5, "psychology": 0.4, "technology": 0.3},
        "traits": {"creative": 1.0, "extrovert": 0.6, "risk": 0.5},
        "ai_resistance": 70,
        "salary": {"entry": 4, "mid": 15, "senior": 50},
        "growth": "Explosive",
        "industries": ["Media", "Marketing", "Creator Economy", "Advertising"],
    },
    {
        "key": "consultant",
        "title": "Management Consultant",
        "icon": "Briefcase",
        "tagline": "Solve the toughest problems for the biggest companies.",
        "weights": {"business": 1.0, "leadership": 0.7, "finance": 0.5, "psychology": 0.3, "technology": 0.3},
        "traits": {"analytical": 0.8, "leader": 0.7, "extrovert": 0.6},
        "ai_resistance": 82,
        "salary": {"entry": 11, "mid": 30, "senior": 80},
        "growth": "High",
        "industries": ["Consulting", "Corporate Strategy", "Private Equity", "Technology"],
    },
]

INTEREST_LABELS = {
    "technology": "Technology & Coding",
    "business": "Business & Strategy",
    "design": "Design & Creativity",
    "psychology": "Psychology & People",
    "teaching": "Teaching & Mentoring",
    "healthcare": "Healthcare & Medicine",
    "finance": "Finance & Investing",
    "content_creation": "Content Creation",
    "law": "Law & Justice",
    "leadership": "Leadership & Management",
}


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


def _traits_vector(pers: Dict[str, str]) -> Dict[str, float]:
    return {
        "introvert": 1.0 if pers.get("mind") == "introvert" else 0.0,
        "extrovert": 1.0 if pers.get("mind") == "extrovert" else 0.0,
        "creative": 1.0 if pers.get("approach") == "creative" else 0.0,
        "analytical": 1.0 if pers.get("approach") == "analytical" else 0.0,
        "risk": 1.0 if pers.get("risk") == "risk_taker" else 0.0,
        "stable": 1.0 if pers.get("risk") == "stable" else 0.0,
        "leader": 1.0 if pers.get("role") == "leader" else 0.0,
        "specialist": 1.0 if pers.get("role") == "specialist" else 0.0,
    }


def _trait_labels(traits: Dict[str, float]) -> List[str]:
    labels = []
    labels.append("Extroverted Connector" if traits["extrovert"] else "Introspective Deep-Worker")
    labels.append("Analytical Strategist" if traits["analytical"] else "Creative Originator")
    labels.append("Bold Risk-Taker" if traits["risk"] else "Steady Stabiliser")
    labels.append("Natural Leader" if traits["leader"] else "Focused Specialist")
    return labels


def compute_blueprint(profile: Dict[str, Any]) -> Dict[str, Any]:
    interests = profile.get("interests", {})
    pers = profile.get("personality", {})
    norm = {k: _clamp(interests.get(k, 5), 0, 10) / 10.0 for k in INTEREST_LABELS}
    traits = _traits_vector(pers)

    scored = []
    for c in CAREERS:
        wsum = sum(c["weights"].values()) or 1
        interest_score = sum(norm.get(k, 0) * w for k, w in c["weights"].items()) / wsum
        tw = c.get("traits", {})
        tsum = sum(tw.values()) or 1
        pers_score = sum(traits.get(k, 0) * w for k, w in tw.items()) / tsum
        raw = 0.72 * interest_score + 0.28 * pers_score
        scored.append((c, raw))

    scored.sort(key=lambda x: x[1], reverse=True)
    top_raw = scored[0][1] or 1.0

    matches = []
    for c, raw in scored:
        score = round(56 + (raw / top_raw) * 41)
        score = int(_clamp(score, 41, 98))
        matches.append({
            "key": c["key"],
            "title": c["title"],
            "icon": c["icon"],
            "tagline": c["tagline"],
            "score": score,
            "ai_resistance": c["ai_resistance"],
            "salary": c["salary"],
            "growth": c["growth"],
            "industries": c["industries"],
        })

    top5 = matches[:5]
    top3 = matches[:3]

    success_score = round(0.6 * top3[0]["score"] + 0.25 * top3[1]["score"] + 0.15 * top3[2]["score"])
    success_score = int(_clamp(success_score, 55, 97))

    ai_resistance_score = round(sum(m["ai_resistance"] for m in top3) / 3)
    leadership_potential = int(_clamp(round(norm["leadership"] * 58 + traits["leader"] * 27 + traits["extrovert"] * 15), 35, 98))
    business_potential = int(_clamp(round(norm["business"] * 48 + norm["finance"] * 17 + traits["risk"] * 20 + traits["leader"] * 15), 35, 98))
    personal_growth = int(_clamp(round(58 + traits["creative"] * 8 + (norm["psychology"] + norm["teaching"]) * 12 + (success_score - 70) * 0.3), 50, 96))

    # Top strengths derived from highest-rated interests + dominant traits
    ranked_interests = sorted(INTEREST_LABELS.keys(), key=lambda k: norm[k], reverse=True)
    strength_scores = [
        {"label": INTEREST_LABELS[k], "score": int(_clamp(round(50 + norm[k] * 48), 40, 99))}
        for k in ranked_interests[:5]
    ]

    top = top5[0]
    salary_projection = {
        "year1": top["salary"]["entry"],
        "year3": round(top["salary"]["entry"] * 1.5),
        "year5": top["salary"]["mid"],
        "year10": top["salary"]["senior"],
    }

    industries = []
    for m in top3:
        for ind in m["industries"]:
            if ind not in industries:
                industries.append(ind)

    return {
        "matches": top5,
        "success_score": success_score,
        "ai_resistance_score": ai_resistance_score,
        "leadership_potential": leadership_potential,
        "business_potential": business_potential,
        "personal_growth": personal_growth,
        "strength_scores": strength_scores,
        "trait_labels": _trait_labels(traits),
        "salary_projection": salary_projection,
        "industries": industries[:6],
    }
