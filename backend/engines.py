"""Deterministic sub-engines: layoff survival, career switch, IT report,
learning plans, and the career-regret (opportunity cost) calculator.
All numbers computed here; AI only explains."""
from typing import Dict, List, Any
from careers import CAREERS, CAREER_BY_KEY, ai_risk_label, INTEREST_LABELS


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


def _num(v, default=0.0):
    try:
        return float(str(v).replace(",", "").strip())
    except (TypeError, ValueError):
        return default


IT_KEYWORDS = ["software", "developer", "engineer", "tester", "qa", "devops",
               "cloud", "tech", "programmer", "computer", "information technology"]


def is_it_profile(profile: Dict[str, Any]) -> bool:
    blob = " ".join(str(profile.get(k, "")) for k in ["user_type", "current_profession", "current_degree", "education", "job_title", "industry"]).lower()
    if "it" in blob.replace(",", " ").split():  # whole-word 'IT' only
        return True
    return any(k in blob for k in IT_KEYWORDS)


def is_professional(profile: Dict[str, Any]) -> bool:
    ut = (profile.get("user_type") or "").lower()
    return any(x in ut for x in ["professional", "employee", "manager", "switcher", "laid", "freelancer", "business", "fresher"])


def build_learning_plans(top_match: Dict[str, Any]) -> List[Dict[str, Any]]:
    skills = top_match.get("learn_next", []) or ["Core fundamentals", "One real project", "Portfolio"]
    s = (skills + skills)[:8]
    return [
        {"phase": "30-Day Plan", "focus": f"Foundations of {top_match['title'].split('/')[0].strip()}",
         "items": [f"Learn {s[0]}", f"Daily practice of {s[1]}", "Ship 1 mini-project", "Set up LinkedIn + GitHub"],
         "expected_salary": f"₹{top_match['salary']['entry']} LPA target", "success_probability": "70%"},
        {"phase": "90-Day Plan", "focus": "Build proof of skill",
         "items": [f"Master {s[2]}", "2 portfolio projects", "Start applying / freelancing", "Mock interviews"],
         "expected_salary": f"₹{round(top_match['salary']['entry']*1.3)} LPA target", "success_probability": "62%"},
        {"phase": "6-Month Plan", "focus": "Get hired / get clients",
         "items": [f"Earn a {s[3]} certification", "Niche specialisation", "Network with 50 people", "Interview readiness"],
         "expected_salary": f"₹{top_match['salary']['mid']} LPA target", "success_probability": "55%"},
        {"phase": "12-Month Plan", "focus": "Compound your advantage",
         "items": ["Advanced projects", "Personal brand", "Promotion / switch", "Income diversification"],
         "expected_salary": f"₹{round((top_match['salary']['mid']+top_match['salary']['senior'])/2)} LPA target", "success_probability": "48%"},
    ]


def build_career_switch(matches: List[Dict[str, Any]], current_salary: float) -> Dict[str, Any]:
    targets = []
    for m in matches:
        if m.get("ai_risk", 0) >= 55:  # never recommend switching INTO a dying field
            continue
        diff = m["difficulty"]
        if diff <= 50:
            difficulty = "Moderate"
        elif diff <= 75:
            difficulty = "Hard"
        else:
            difficulty = "Very Hard"
        impact = m["salary"]["mid"] - current_salary if current_salary else m["salary"]["mid"]
        success = int(_clamp(round(m["score"] * 0.7 + (100 - diff) * 0.3), 30, 90))
        targets.append({
            "title": m["title"], "icon": m["icon"], "difficulty": difficulty,
            "time_required": m["time_to_enter"],
            "salary_impact": f"{'+' if impact >= 0 else ''}₹{round(impact)} LPA" if current_salary else f"₹{m['salary']['mid']} LPA potential",
            "skill_gaps": m.get("learn_next", [])[:3],
            "success_probability": f"{success}%",
        })
    return {"targets": targets[:4]}


def build_layoff_engine(profile: Dict[str, Any], blueprint: Dict[str, Any]) -> Dict[str, Any]:
    exp = _num(profile.get("years_experience"), 2)
    skills = profile.get("skills", "")
    skill_count = len([s for s in str(skills).replace(",", " ").split() if len(s) > 1]) if skills else 4
    certs = profile.get("certifications", "")
    cert_count = len([s for s in str(certs).split(",") if s.strip()]) if certs else 0

    top = blueprint["matches"][0]
    role_ai_risk = 100 - blueprint["ai_resistance_score"]

    layoff_risk = int(_clamp(round(role_ai_risk * 0.5 + (40 - min(exp, 10) * 4) * 0.3 + (40 - min(skill_count, 10) * 4) * 0.2), 10, 92))
    employability = int(_clamp(round(top["market_demand"] * 0.45 + min(exp, 12) / 12 * 25 + min(skill_count, 10) * 2 + cert_count * 4 + 10), 25, 96))
    recovery = int(_clamp(round(employability * 0.6 + (100 - layoff_risk) * 0.4), 25, 95))
    salary_recovery = int(_clamp(round(employability * 0.7 + min(exp, 10) * 2.5), 30, 98))

    roadmap = {
        "0-30 Days": ["Rewrite resume for ATS + impact metrics", "Optimise LinkedIn (headline, about, keywords)",
                      "Interview prep: 20 core questions", "List freelancing gigs for emergency income"],
        "30-90 Days": ["Run a skill-gap analysis vs target roles", "Build 2 portfolio projects",
                       "Networking: 5 referrals/week", "Targeted application strategy (quality > quantity)"],
        "3-12 Months": [f"Earn a {top['title'].split('/')[0].strip()} certification", "Personal branding & content",
                        "Career-upgrade / role switch plan", "Diversify income (freelance + job)"],
    }
    return {
        "layoff_risk_score": layoff_risk, "layoff_risk_label": ai_risk_label(layoff_risk),
        "recovery_score": recovery, "employability_score": employability,
        "salary_recovery_potential": salary_recovery, "ai_risk_assessment": ai_risk_label(role_ai_risk),
        "recovery_roadmap": roadmap,
    }


def build_it_report(profile: Dict[str, Any], blueprint: Dict[str, Any]) -> Dict[str, Any]:
    top = blueprint["matches"][0]
    role_ai_risk = 100 - blueprint["ai_resistance_score"]
    promotion = int(_clamp(round(blueprint["leadership_potential"] * 0.6 + top["market_demand"] * 0.3), 30, 95))
    salary_growth = int(_clamp(round(top["salary_score"] * 0.7 + top["market_demand"] * 0.3), 35, 96))
    return {
        "current_role_demand": top["market_demand"],
        "future_demand": int(_clamp(round(top["market_demand"] - (role_ai_risk - 20) * 0.3), 30, 98)),
        "promotion_potential": promotion,
        "ai_risk": role_ai_risk, "ai_risk_label": ai_risk_label(role_ai_risk),
        "salary_growth_potential": salary_growth,
        "emerging_opportunities": top.get("learn_next", [])[:4],
    }


def build_regret(profile: Dict[str, Any], blueprint: Dict[str, Any]) -> Dict[str, Any]:
    age = _num(profile.get("age"), 22)
    expected = _num(profile.get("expected_salary"), 0)
    right_path = blueprint["salary_projection"]["year5"]
    # Assume wrong path tracks ~45% of the right-path trajectory
    yearly_gap = max(right_path - (expected if expected else right_path * 0.55), right_path * 0.35)
    years = int(_clamp(round(50 - age), 10, 30))
    opportunity_cost = round(yearly_gap * years)
    return {
        "opportunity_cost_lpa_gap": round(yearly_gap, 1),
        "years": years,
        "opportunity_cost": opportunity_cost,
        "assumption": f"A ~₹{round(yearly_gap,1)} LPA annual gap over {years} working years on the wrong path.",
    }


def build_engines(profile: Dict[str, Any], blueprint: Dict[str, Any]) -> Dict[str, Any]:
    top = blueprint["matches"][0]
    current_salary = _num(profile.get("current_salary"), 0)
    out = {
        "learning_plans": build_learning_plans(top),
        "career_switch": build_career_switch(blueprint["matches"], current_salary),
        "regret": build_regret(profile, blueprint),
    }
    if is_professional(profile) or current_salary > 0:
        out["layoff"] = build_layoff_engine(profile, blueprint)
    if is_it_profile(profile):
        out["it_report"] = build_it_report(profile, blueprint)
    return out
