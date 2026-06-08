"""Career intelligence engine — deterministic scoring + honesty engine.

Numbers are computed here (no AI). The AI layer only *explains* them.
Covers: career matching, careers-to-avoid, AI-threat assessment, honesty
scorecards (suitability/demand/salary/competition/ai-risk/difficulty/time),
salary projection, potential scores.
"""
from typing import Dict, List, Any

# ---- Interest dimensions (1-10 sliders) ----
INTEREST_LABELS = {
    "technology": "Technology",
    "business": "Business",
    "finance": "Finance",
    "sales": "Sales",
    "marketing": "Marketing",
    "design": "Design",
    "writing": "Writing",
    "teaching": "Teaching",
    "research": "Research",
    "psychology": "Psychology",
    "healthcare": "Healthcare",
    "law": "Law",
    "content_creation": "Content Creation",
    "entrepreneurship": "Entrepreneurship",
    "leadership": "Leadership",
    "problem_solving": "Problem Solving",
}

# w = interest weights, t = trait weights
CAREERS: List[Dict[str, Any]] = [
    {"key": "ai_ml_engineer", "title": "AI / Machine Learning Engineer", "icon": "Cpu", "tagline": "Build the intelligent systems shaping the future.",
     "w": {"technology": 1.0, "research": 0.5, "problem_solving": 0.7, "finance": 0.2},
     "t": {"analytical": 1.0, "specialist": 0.6, "independent": 0.4},
     "market_demand": 96, "salary_score": 92, "competition": 70, "ai_risk": 8, "difficulty": 85, "time_to_enter": "12-24 months",
     "salary": {"entry": 9, "mid": 28, "senior": 70}, "growth": "Explosive",
     "industries": ["Artificial Intelligence", "Big Tech", "Fintech", "Robotics"],
     "learn_next": ["LLMs & RAG", "PyTorch", "MLOps", "System Design", "Agent frameworks"]},

    {"key": "data_scientist", "title": "Data Scientist", "icon": "BarChart3", "tagline": "Turn raw data into million-dollar decisions.",
     "w": {"technology": 0.8, "finance": 0.5, "research": 0.6, "problem_solving": 0.7, "business": 0.4},
     "t": {"analytical": 1.0, "specialist": 0.5},
     "market_demand": 88, "salary_score": 85, "competition": 68, "ai_risk": 18, "difficulty": 78, "time_to_enter": "9-18 months",
     "salary": {"entry": 8, "mid": 24, "senior": 55}, "growth": "Explosive",
     "industries": ["Tech", "Finance", "Healthcare", "E-commerce"],
     "learn_next": ["Python", "SQL", "Machine Learning", "Statistics", "AI analytics"]},

    {"key": "data_analyst", "title": "Data Analyst", "icon": "LineChart", "tagline": "The on-ramp to data — but automation is closing in.",
     "w": {"technology": 0.55, "finance": 0.5, "business": 0.5, "problem_solving": 0.5},
     "t": {"analytical": 0.9, "specialist": 0.4},
     "market_demand": 70, "salary_score": 60, "competition": 75, "ai_risk": 48, "difficulty": 50, "time_to_enter": "3-9 months",
     "salary": {"entry": 5, "mid": 12, "senior": 25}, "growth": "Moderate",
     "industries": ["Tech", "BFSI", "Consulting", "Retail"],
     "learn_next": ["SQL", "Python", "Power BI", "Machine Learning", "AI analytics"]},

    {"key": "software_engineer", "title": "Software Engineer", "icon": "Code", "tagline": "Build products millions rely on every day.",
     "w": {"technology": 0.95, "problem_solving": 0.8, "design": 0.2, "business": 0.2},
     "t": {"analytical": 0.8, "specialist": 0.5, "independent": 0.3},
     "market_demand": 90, "salary_score": 82, "competition": 72, "ai_risk": 28, "difficulty": 70, "time_to_enter": "9-18 months",
     "salary": {"entry": 7, "mid": 22, "senior": 60}, "growth": "High",
     "industries": ["Tech", "SaaS", "Fintech", "Startups"],
     "learn_next": ["AI tools & copilots", "System Design", "Cloud", "DSA", "One backend + one frontend stack"]},

    {"key": "cybersecurity", "title": "Cybersecurity Specialist", "icon": "ShieldCheck", "tagline": "An AI-proof field that only grows more critical.",
     "w": {"technology": 0.85, "problem_solving": 0.7, "research": 0.4},
     "t": {"analytical": 0.9, "specialist": 0.6},
     "market_demand": 92, "salary_score": 80, "competition": 55, "ai_risk": 14, "difficulty": 72, "time_to_enter": "9-18 months",
     "salary": {"entry": 6, "mid": 20, "senior": 50}, "growth": "Explosive",
     "industries": ["Cybersecurity", "BFSI", "Cloud", "Government"],
     "learn_next": ["Networking", "Linux", "SIEM tools", "Cloud security", "Ethical hacking"]},

    {"key": "cloud_devops", "title": "Cloud / DevOps Engineer", "icon": "Cloud", "tagline": "The backbone of every modern tech company.",
     "w": {"technology": 0.9, "problem_solving": 0.6},
     "t": {"analytical": 0.8, "specialist": 0.5},
     "market_demand": 88, "salary_score": 82, "competition": 58, "ai_risk": 22, "difficulty": 68, "time_to_enter": "9-15 months",
     "salary": {"entry": 7, "mid": 22, "senior": 52}, "growth": "High",
     "industries": ["Cloud", "Tech", "SaaS", "Fintech"],
     "learn_next": ["AWS/GCP", "Docker & Kubernetes", "CI/CD", "Terraform", "Observability"]},

    {"key": "product_manager", "title": "Product Manager", "icon": "Rocket", "tagline": "Lead products millions of people love.",
     "w": {"business": 0.9, "leadership": 0.8, "technology": 0.5, "problem_solving": 0.6, "design": 0.3},
     "t": {"leader": 1.0, "extrovert": 0.5, "analytical": 0.6, "communication": 0.6},
     "market_demand": 84, "salary_score": 88, "competition": 78, "ai_risk": 22, "difficulty": 75, "time_to_enter": "12-24 months",
     "salary": {"entry": 10, "mid": 30, "senior": 75}, "growth": "High",
     "industries": ["Tech", "SaaS", "Fintech", "Consumer Apps"],
     "learn_next": ["Product strategy", "Analytics", "User research", "AI products", "Stakeholder leadership"]},

    {"key": "ux_designer", "title": "Product / UX Designer", "icon": "Palette", "tagline": "Design experiences that feel like magic.",
     "w": {"design": 1.0, "psychology": 0.5, "technology": 0.4, "content_creation": 0.3, "problem_solving": 0.4},
     "t": {"creative": 1.0, "specialist": 0.4},
     "market_demand": 74, "salary_score": 68, "competition": 70, "ai_risk": 35, "difficulty": 55, "time_to_enter": "6-12 months",
     "salary": {"entry": 6, "mid": 18, "senior": 45}, "growth": "High",
     "industries": ["Tech", "Design Studios", "Startups", "Gaming"],
     "learn_next": ["Figma", "Design systems", "UX research", "AI design tools", "Portfolio of real products"]},

    {"key": "digital_marketer", "title": "Digital Marketer / Growth", "icon": "Megaphone", "tagline": "Turn attention into revenue.",
     "w": {"marketing": 1.0, "business": 0.5, "content_creation": 0.5, "sales": 0.5, "psychology": 0.3},
     "t": {"creative": 0.6, "extrovert": 0.5, "analytical": 0.5, "communication": 0.5},
     "market_demand": 76, "salary_score": 60, "competition": 72, "ai_risk": 42, "difficulty": 45, "time_to_enter": "3-9 months",
     "salary": {"entry": 4, "mid": 14, "senior": 40}, "growth": "High",
     "industries": ["Marketing", "D2C", "SaaS", "Agencies"],
     "learn_next": ["Performance marketing", "SEO", "Analytics", "AI marketing tools", "Copywriting"]},

    {"key": "content_creator", "title": "Content Creator / Creator-Economy", "icon": "Video", "tagline": "Build an audience, build an asset.",
     "w": {"content_creation": 1.0, "marketing": 0.5, "writing": 0.5, "design": 0.4, "entrepreneurship": 0.4},
     "t": {"creative": 1.0, "extrovert": 0.5, "risk": 0.5, "communication": 0.6},
     "market_demand": 70, "salary_score": 58, "competition": 85, "ai_risk": 40, "difficulty": 55, "time_to_enter": "6-18 months",
     "salary": {"entry": 3, "mid": 15, "senior": 60}, "growth": "Volatile",
     "industries": ["Media", "Creator Economy", "Marketing", "Entertainment"],
     "learn_next": ["Storytelling", "Video editing", "Audience growth", "Monetisation", "AI content tools"]},

    {"key": "entrepreneur", "title": "Startup Founder / Entrepreneur", "icon": "Flame", "tagline": "Build your own empire — high risk, high reward.",
     "w": {"entrepreneurship": 1.0, "business": 0.8, "leadership": 0.8, "sales": 0.5, "finance": 0.4},
     "t": {"risk": 1.0, "leader": 0.9, "extrovert": 0.5, "independent": 0.6},
     "market_demand": 80, "salary_score": 78, "competition": 88, "ai_risk": 12, "difficulty": 90, "time_to_enter": "Immediate (but brutal)",
     "salary": {"entry": 3, "mid": 25, "senior": 100}, "growth": "Explosive",
     "industries": ["Startups", "E-commerce", "SaaS", "D2C"],
     "learn_next": ["Sales", "Fundraising", "Product", "Hiring", "Unit economics"]},

    {"key": "investment_banker", "title": "Investment Banker", "icon": "TrendingUp", "tagline": "Elite pay — brutal hours and competition.",
     "w": {"finance": 1.0, "business": 0.7, "problem_solving": 0.5, "leadership": 0.4},
     "t": {"analytical": 0.9, "leader": 0.4, "risk": 0.4},
     "market_demand": 66, "salary_score": 95, "competition": 90, "ai_risk": 35, "difficulty": 88, "time_to_enter": "18-36 months",
     "salary": {"entry": 12, "mid": 35, "senior": 90}, "growth": "Moderate",
     "industries": ["Investment Banking", "Private Equity", "Hedge Funds"],
     "learn_next": ["Financial modelling", "Valuation", "Excel mastery", "M&A", "Networking"]},

    {"key": "financial_analyst", "title": "Financial Analyst / CA", "icon": "Calculator", "tagline": "Solid path — but routine analysis is automating.",
     "w": {"finance": 1.0, "business": 0.6, "problem_solving": 0.4},
     "t": {"analytical": 0.9, "specialist": 0.5},
     "market_demand": 68, "salary_score": 70, "competition": 72, "ai_risk": 50, "difficulty": 70, "time_to_enter": "12-36 months",
     "salary": {"entry": 6, "mid": 16, "senior": 40}, "growth": "Moderate",
     "industries": ["BFSI", "Consulting", "Corporate Finance", "Audit"],
     "learn_next": ["Advanced Excel", "FP&A", "Power BI", "Python for finance", "Valuation"]},

    {"key": "doctor", "title": "Doctor / Medical Specialist", "icon": "HeartPulse", "tagline": "Deeply AI-proof — but a long, hard road.",
     "w": {"healthcare": 1.0, "psychology": 0.4, "research": 0.3, "problem_solving": 0.4},
     "t": {"analytical": 0.7, "specialist": 0.8},
     "market_demand": 85, "salary_score": 78, "competition": 80, "ai_risk": 8, "difficulty": 95, "time_to_enter": "5-10 years",
     "salary": {"entry": 7, "mid": 20, "senior": 60}, "growth": "Stable",
     "industries": ["Hospitals", "Research", "Public Health", "Private Practice"],
     "learn_next": ["Clinical specialisation", "Medical AI tools", "Research", "Patient communication"]},

    {"key": "psychologist", "title": "Clinical Psychologist / Therapist", "icon": "Brain", "tagline": "Human empathy machines can't replace.",
     "w": {"psychology": 1.0, "healthcare": 0.4, "research": 0.3, "teaching": 0.3},
     "t": {"creative": 0.4, "specialist": 0.5, "communication": 0.5},
     "market_demand": 80, "salary_score": 55, "competition": 55, "ai_risk": 12, "difficulty": 70, "time_to_enter": "3-6 years",
     "salary": {"entry": 5, "mid": 14, "senior": 35}, "growth": "High",
     "industries": ["Healthcare", "Wellness", "Corporate", "EdTech"],
     "learn_next": ["Clinical training", "CBT", "Assessment tools", "Tele-therapy", "Niche specialisation"]},

    {"key": "lawyer", "title": "Corporate Lawyer", "icon": "Scale", "tagline": "Prestige and pay — but research is automating fast.",
     "w": {"law": 1.0, "leadership": 0.4, "business": 0.4, "writing": 0.4},
     "t": {"analytical": 0.7, "extrovert": 0.4, "communication": 0.6},
     "market_demand": 66, "salary_score": 75, "competition": 82, "ai_risk": 32, "difficulty": 85, "time_to_enter": "3-6 years",
     "salary": {"entry": 7, "mid": 22, "senior": 65}, "growth": "Stable",
     "industries": ["Law Firms", "Corporate Legal", "Compliance", "Judiciary"],
     "learn_next": ["Contract law", "Legal-tech & AI tools", "Negotiation", "Drafting", "Specialisation"]},

    {"key": "management_consultant", "title": "Management Consultant", "icon": "Briefcase", "tagline": "Solve the hardest problems for the biggest companies.",
     "w": {"business": 1.0, "leadership": 0.6, "problem_solving": 0.7, "finance": 0.4},
     "t": {"analytical": 0.8, "leader": 0.6, "extrovert": 0.5, "communication": 0.6},
     "market_demand": 74, "salary_score": 86, "competition": 85, "ai_risk": 25, "difficulty": 82, "time_to_enter": "12-24 months",
     "salary": {"entry": 11, "mid": 30, "senior": 80}, "growth": "High",
     "industries": ["Consulting", "Corporate Strategy", "PE", "Tech"],
     "learn_next": ["Structured problem solving", "Business frameworks", "Storytelling", "Excel/PPT", "Domain depth"]},

    {"key": "sales_leader", "title": "Sales / Business Development Leader", "icon": "Handshake", "tagline": "Recession-proof if you can close.",
     "w": {"sales": 1.0, "business": 0.6, "leadership": 0.6, "psychology": 0.4},
     "t": {"extrovert": 0.8, "leader": 0.6, "communication": 0.8, "risk": 0.4},
     "market_demand": 82, "salary_score": 72, "competition": 60, "ai_risk": 28, "difficulty": 45, "time_to_enter": "3-9 months",
     "salary": {"entry": 5, "mid": 18, "senior": 55}, "growth": "High",
     "industries": ["SaaS", "BFSI", "Real Estate", "B2B"],
     "learn_next": ["Consultative selling", "CRM tools", "Negotiation", "Pipeline management", "Domain expertise"]},

    {"key": "teacher_edtech", "title": "Educator / EdTech Creator", "icon": "GraduationCap", "tagline": "Scale your impact beyond a classroom.",
     "w": {"teaching": 1.0, "psychology": 0.4, "content_creation": 0.5, "writing": 0.3},
     "t": {"extrovert": 0.4, "communication": 0.6, "creative": 0.4},
     "market_demand": 70, "salary_score": 52, "competition": 60, "ai_risk": 30, "difficulty": 45, "time_to_enter": "3-12 months",
     "salary": {"entry": 4, "mid": 12, "senior": 40}, "growth": "Moderate",
     "industries": ["EdTech", "Schools", "Online Courses", "Universities"],
     "learn_next": ["Curriculum design", "Content creation", "AI teaching tools", "Community building"]},

    # ---- High-risk / 'avoid' candidates ----
    {"key": "manual_tester", "title": "Manual QA Tester", "icon": "Bug", "tagline": "Being automated away — pivot to automation now.",
     "w": {"technology": 0.5, "problem_solving": 0.4},
     "t": {"specialist": 0.4, "analytical": 0.4},
     "market_demand": 40, "salary_score": 40, "competition": 70, "ai_risk": 82, "difficulty": 30, "time_to_enter": "1-3 months",
     "salary": {"entry": 3, "mid": 7, "senior": 14}, "growth": "Declining",
     "industries": ["IT Services"],
     "learn_next": ["Automation testing", "Selenium", "Python", "AI-based QA", "API testing"]},

    {"key": "data_entry", "title": "Data Entry Operator", "icon": "Keyboard", "tagline": "Critical AI risk — exit this path.",
     "w": {"technology": 0.2},
     "t": {},
     "market_demand": 20, "salary_score": 20, "competition": 80, "ai_risk": 96, "difficulty": 10, "time_to_enter": "Days",
     "salary": {"entry": 2, "mid": 3, "senior": 5}, "growth": "Dying",
     "industries": ["BPO", "Back office"],
     "learn_next": ["Excel automation", "Data analysis", "RPA", "Any in-demand skill"]},

    {"key": "customer_support", "title": "Customer Support Executive", "icon": "Headphones", "tagline": "AI chatbots are shrinking these roles.",
     "w": {"psychology": 0.3, "sales": 0.3},
     "t": {"communication": 0.5, "team": 0.4},
     "market_demand": 50, "salary_score": 35, "competition": 65, "ai_risk": 58, "difficulty": 20, "time_to_enter": "Weeks",
     "salary": {"entry": 3, "mid": 6, "senior": 12}, "growth": "Declining",
     "industries": ["BPO", "SaaS", "E-commerce"],
     "learn_next": ["Customer success", "CRM tools", "Upselling", "Tech support", "Product expertise"]},

    {"key": "graphic_designer_basic", "title": "Basic Graphic Designer", "icon": "Image", "tagline": "Generic design is the most AI-exposed creative job.",
     "w": {"design": 0.6, "content_creation": 0.4},
     "t": {"creative": 0.6},
     "market_demand": 48, "salary_score": 40, "competition": 80, "ai_risk": 75, "difficulty": 30, "time_to_enter": "2-6 months",
     "salary": {"entry": 3, "mid": 7, "senior": 16}, "growth": "Declining",
     "industries": ["Agencies", "Freelance"],
     "learn_next": ["UX/Product design", "Motion design", "AI design tools", "Branding strategy"]},
]

CAREER_BY_KEY = {c["key"]: c for c in CAREERS}


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


def ai_risk_label(risk: int) -> str:
    if risk <= 20:
        return "Very Low Risk"
    if risk <= 40:
        return "Low Risk"
    if risk <= 60:
        return "Medium Risk"
    if risk <= 80:
        return "High Risk"
    return "Critical Risk"


def _traits_vector(pers: Dict[str, Any]) -> Dict[str, float]:
    def sld(k):
        try:
            return float(pers.get(k, 5)) / 10.0
        except (TypeError, ValueError):
            return 0.5
    return {
        "introvert": 1.0 if pers.get("mind") == "introvert" else 0.0,
        "extrovert": 1.0 if pers.get("mind") == "extrovert" else 0.0,
        "creative": 1.0 if pers.get("approach") == "creative" else 0.0,
        "analytical": 1.0 if pers.get("approach") == "analytical" else 0.0,
        "risk": 1.0 if pers.get("risk") == "risk_taker" else 0.0,
        "stable": 1.0 if pers.get("risk") == "stable" else 0.0,
        "leader": 1.0 if pers.get("role") == "leader" else 0.0,
        "specialist": 1.0 if pers.get("role") == "specialist" else 0.0,
        "team": 1.0 if pers.get("work_style") == "team" else 0.0,
        "independent": 1.0 if pers.get("work_style") == "independent" else 0.0,
        "communication": sld("communication"),
    }


def _trait_labels(traits, pers) -> List[str]:
    return [
        "Extroverted Connector" if traits["extrovert"] else "Introspective Deep-Worker",
        "Analytical Strategist" if traits["analytical"] else "Creative Originator",
        "Bold Risk-Taker" if traits["risk"] else "Steady Stabiliser",
        "Natural Leader" if traits["leader"] else "Focused Specialist",
        "Team Player" if traits["team"] else "Independent Operator",
    ]


def _suitability(career, norm, traits) -> float:
    wsum = sum(career["w"].values()) or 1
    interest_score = sum(norm.get(k, 0) * w for k, w in career["w"].items()) / wsum
    tw = career.get("t", {})
    tsum = sum(tw.values()) or 1
    pers_score = sum(traits.get(k, 0) * w for k, w in tw.items()) / tsum if tw else 0.5
    return 0.7 * interest_score + 0.3 * pers_score


def _verdict(score, career):
    if score >= 80 and career["ai_risk"] <= 45:
        return "Strong fit"
    if score >= 65:
        return "Workable fit"
    if score >= 50:
        return "Stretch — proceed with caution"
    return "Poor fit"


def compute_blueprint(profile: Dict[str, Any]) -> Dict[str, Any]:
    interests = profile.get("interests", {})
    pers = profile.get("personality", {})
    norm = {k: _clamp(interests.get(k, 5), 0, 10) / 10.0 for k in INTEREST_LABELS}
    traits = _traits_vector(pers)

    raw = [(c, _suitability(c, norm, traits)) for c in CAREERS]
    raw.sort(key=lambda x: x[1], reverse=True)
    top_raw = raw[0][1] or 1.0

    scored = []
    for c, r in raw:
        suit = int(_clamp(round(52 + (r / top_raw) * 46), 38, 98))
        scored.append((c, suit))

    def card(c, suit):
        return {
            "key": c["key"], "title": c["title"], "icon": c["icon"], "tagline": c["tagline"],
            "score": suit, "suitability": suit,
            "market_demand": c["market_demand"], "salary_score": c["salary_score"],
            "competition": c["competition"], "ai_risk": c["ai_risk"],
            "ai_risk_label": ai_risk_label(c["ai_risk"]), "ai_resistance": 100 - c["ai_risk"],
            "difficulty": c["difficulty"], "time_to_enter": c["time_to_enter"],
            "salary": c["salary"], "salary_mid": c["salary"]["mid"], "growth": c["growth"],
            "industries": c["industries"], "learn_next": c.get("learn_next", []),
            "verdict": _verdict(suit, c),
        }

    matches = [card(c, s) for c, s in scored[:5]]

    avoid_ranked = []
    for c, suit in scored:
        avoid_score = (100 - suit) * 0.45 + c["ai_risk"] * 0.30 + c["competition"] * 0.10 + (100 - c["market_demand"]) * 0.15
        avoid_ranked.append((c, suit, avoid_score))
    avoid_ranked.sort(key=lambda x: x[2], reverse=True)
    careers_to_avoid = []
    for c, suit, _ in avoid_ranked[:5]:
        reasons = []
        if c["ai_risk"] >= 60:
            reasons.append(f"{ai_risk_label(c['ai_risk'])} — automation is shrinking this field")
        if suit < 55:
            reasons.append("weak alignment with your strengths")
        if c["competition"] >= 78:
            reasons.append("brutal competition for limited seats")
        if c["market_demand"] <= 50:
            reasons.append("declining market demand")
        if not reasons:
            reasons.append("better-aligned options exist for your profile")
        careers_to_avoid.append({
            "title": c["title"], "icon": c["icon"], "ai_risk": c["ai_risk"],
            "ai_risk_label": ai_risk_label(c["ai_risk"]), "market_demand": c["market_demand"],
            "competition": c["competition"], "suitability": suit, "why": reasons[:2],
        })

    top3 = matches[:3]
    success_score = int(_clamp(round(0.6 * top3[0]["score"] + 0.25 * top3[1]["score"] + 0.15 * top3[2]["score"]), 50, 97))
    ai_resistance_score = round(sum(m["ai_resistance"] for m in top3) / 3)
    portfolio_ai_risk = round(sum(m["ai_risk"] for m in top3) / 3)

    leadership_potential = int(_clamp(round(norm["leadership"] * 55 + traits["leader"] * 28 + traits["extrovert"] * 12 + traits["communication"] * 10), 30, 98))
    business_potential = int(_clamp(round(norm["entrepreneurship"] * 45 + norm["business"] * 20 + traits["risk"] * 20 + traits["leader"] * 12), 30, 98))
    personal_growth = int(_clamp(round(58 + traits["creative"] * 8 + (norm["psychology"] + norm["research"]) * 12 + (success_score - 70) * 0.3), 45, 96))

    ranked_interests = sorted(INTEREST_LABELS.keys(), key=lambda k: norm[k], reverse=True)
    strength_scores = [{"label": INTEREST_LABELS[k], "score": int(_clamp(round(50 + norm[k] * 48), 40, 99))} for k in ranked_interests[:5]]
    weakness = {"label": INTEREST_LABELS[ranked_interests[-1]], "score": int(_clamp(round(20 + norm[ranked_interests[-1]] * 40), 12, 55))}

    top = matches[0]
    salary_projection = {"year1": top["salary"]["entry"], "year3": round(top["salary"]["entry"] * 1.5),
                         "year5": top["salary"]["mid"], "year10": top["salary"]["senior"]}

    industries = []
    for m in top3:
        for ind in m["industries"]:
            if ind not in industries:
                industries.append(ind)

    ai_threat_examples = [
        {"area": "Data Entry / Back office", "label": "Critical Risk"},
        {"area": "Manual QA Testing", "label": "High Risk"},
        {"area": "Basic Graphic Design", "label": "High Risk"},
        {"area": "Customer Support (L1)", "label": "Medium Risk"},
        {"area": "Cybersecurity", "label": "Low Risk"},
        {"area": "AI / ML Engineering", "label": "Very Low Risk"},
    ]

    return {
        "user_type": profile.get("user_type", "Student"),
        "matches": matches,
        "careers_to_avoid": careers_to_avoid,
        "success_score": success_score,
        "ai_resistance_score": ai_resistance_score,
        "portfolio_ai_risk": portfolio_ai_risk,
        "ai_risk_label": ai_risk_label(portfolio_ai_risk),
        "ai_threat_examples": ai_threat_examples,
        "leadership_potential": leadership_potential,
        "business_potential": business_potential,
        "personal_growth": personal_growth,
        "strength_scores": strength_scores,
        "weakness": weakness,
        "trait_labels": _trait_labels(traits, pers),
        "salary_projection": salary_projection,
        "industries": industries[:6],
        "learn_next": top.get("learn_next", []),
    }
