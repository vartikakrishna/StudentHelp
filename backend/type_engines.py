"""Per-category analysis engines. Each user type is its own product:
different scoring model, different report sections, different recommendations,
different action plan. Deterministic numbers here; AI only enhances prose.
"""
from typing import Dict, List, Any
from statistics import mean

from careers import CAREER_BY_KEY, ai_risk_label, rank_careers, match_card, build_avoid_from_scored
from common import (
    clamp, num, as_list, traits_from_personality, trait_labels,
    build_interest_norm, salary_projection, sec,
)

# ============================================================
# PROFILE META — drives the category value screen + report cover
# ============================================================
PROFILE_META: Dict[str, Dict[str, Any]] = {
    "Student": {
        "product": "Career Direction Report", "icon": "GraduationCap",
        "goal": "Career Discovery",
        "tagline": "Find the right career & degree before you waste years on the wrong one.",
        "value": ["Best-fit career paths", "Right degree & stream", "AI-proof career options",
                  "Skills to start now", "10-year growth projection", "Career mistakes to avoid"]},
    "IT Employee": {
        "product": "AI Survival & Growth Report", "icon": "Code",
        "goal": "AI Survival & Salary Growth",
        "tagline": "Find out if AI will replace your role — and exactly how to stay ahead.",
        "value": ["AI replacement risk score", "Future tech demand", "Your tech skill gaps",
                  "Salary growth plan", "Transition opportunities", "Best emerging technologies"]},
    "Working Professional": {
        "product": "Career Growth Report", "icon": "Briefcase",
        "goal": "Promotion & Salary Growth",
        "tagline": "Get a brutally honest read on your promotion, salary and leadership trajectory.",
        "value": ["Promotion readiness score", "Career growth analysis", "Salary forecast",
                  "Leadership potential", "Industry outlook", "90/180/365 growth roadmap"]},
    # ---- Phase 2/3 (interim: generic engines until their dedicated build) ----
    "Fresher": {"product": "First-Job Readiness Report", "icon": "Sprout", "goal": "Landing Your First Job",
                "tagline": "Know exactly how job-ready you are and what to fix first.",
                "value": ["Job readiness score", "Skill gaps", "Resume & interview plan", "90-day action plan"]},
    "Career Switcher": {"product": "Career Transition Blueprint", "icon": "Repeat", "goal": "Switching Careers",
                        "tagline": "See if your switch is realistic — and the fastest path to make it.", "value": ["Switch feasibility", "Transferable skills", "Transition timeline", "Salary impact"]},
    "Laid Off Employee": {"product": "Career Recovery Blueprint", "icon": "LifeBuoy", "goal": "Bouncing Back",
                          "tagline": "Your fastest, clearest path back to income after a layoff.", "value": ["Recovery score", "Reemployment probability", "Emergency income options", "90-day recovery plan"]},
    "Manager": {"product": "Leadership Growth Report", "icon": "Users", "goal": "Leadership Growth",
                "tagline": "Find your path from manager to executive.", "value": ["Executive potential", "Leadership score", "Promotion roadmap", "Personal brand"]},
    "Freelancer": {"product": "Freelance Income Report", "icon": "Laptop", "goal": "Income Growth",
                   "tagline": "Scale your freelance income with a real growth system.", "value": ["Income growth potential", "Client acquisition", "Brand building", "Service expansion"]},
    "Business Owner": {"product": "Business Growth Intelligence Report", "icon": "Building2", "goal": "Business Growth",
                       "tagline": "A brutally honest read on your business health and growth levers.", "value": ["Business health score", "Growth potential", "Marketing opportunities", "Scale plan"]},
}

DEFAULT_META = {"product": "Career Intelligence Report", "icon": "Sparkles", "goal": "Career Growth",
                "tagline": "A brutally honest, personalized career analysis.", "value": []}


def meta_for(user_type: str) -> Dict[str, Any]:
    return PROFILE_META.get(user_type, DEFAULT_META)


# ============================================================
# Helpers
# ============================================================
def _ans(profile: Dict[str, Any]) -> Dict[str, Any]:
    return profile.get("answers") or {}


def _pers(profile: Dict[str, Any]) -> Dict[str, Any]:
    return profile.get("personality") or {}


def _first_name(profile: Dict[str, Any]) -> str:
    return (profile.get("name") or "there").split(" ")[0]


def _cards_by_keys(keys: List[str], suit: int = 80) -> List[Dict[str, Any]]:
    return [match_card(CAREER_BY_KEY[k], suit) for k in keys if k in CAREER_BY_KEY]


def _preview(meta, headline, verdict, summary, scores):
    return {"product_name": meta["product"], "headline": headline, "verdict": verdict,
            "summary": summary, "scores": scores}


LEVELS = {"None": 0, "Beginner": 25, "Intermediate": 50, "Advanced": 75, "Expert": 100, "": 30}


# ============================================================
# STUDENT — Career Direction Report
# ============================================================
DEGREE_MAP = {
    "ai_ml_engineer": ["B.Tech CS / AI-ML", "B.Sc Data Science", "M.Tech AI/ML"],
    "data_scientist": ["B.Tech CS", "B.Sc Statistics / Data Science", "M.Sc Data Science"],
    "data_analyst": ["BBA / B.Com + Analytics", "B.Sc Statistics", "Any degree + Analytics cert"],
    "software_engineer": ["B.Tech / BE CS or IT", "BCA → MCA"],
    "cybersecurity": ["B.Tech CS", "B.Sc Cybersecurity", "CEH / OSCP certifications"],
    "cloud_devops": ["B.Tech CS / IT", "Cloud certifications (AWS/GCP)"],
    "product_manager": ["B.Tech + MBA", "BBA / MBA", "Any degree + PM internships"],
    "ux_designer": ["B.Des / B.Sc Design", "HCI / UX bootcamp"],
    "digital_marketer": ["BBA / BMS Marketing", "Any degree + Digital Marketing cert"],
    "content_creator": ["Mass Comm / any degree", "Self-taught + strong portfolio"],
    "entrepreneur": ["BBA / MBA (optional)", "Any degree + a real venture"],
    "investment_banker": ["B.Com + MBA Finance", "Economics + CFA"],
    "financial_analyst": ["B.Com / BBA Finance", "CA / CFA", "MBA Finance"],
    "doctor": ["MBBS + MD/MS", "BDS"],
    "psychologist": ["BA / MA Psychology", "M.Phil Clinical Psychology"],
    "lawyer": ["BA LLB / LLB", "Company Secretary (CS)"],
    "management_consultant": ["B.Tech / BBA + MBA", "Economics + MBA"],
    "sales_leader": ["BBA / any degree", "MBA Sales & Marketing"],
    "teacher_edtech": ["B.Ed + subject degree", "Any degree + content skills"],
}

DOMAIN_OF = {
    "ai_ml_engineer": "tech", "data_scientist": "tech", "data_analyst": "tech",
    "software_engineer": "tech", "cybersecurity": "tech", "cloud_devops": "tech", "ux_designer": "design",
    "product_manager": "business", "management_consultant": "business", "sales_leader": "business",
    "digital_marketer": "business", "entrepreneur": "business",
    "investment_banker": "finance", "financial_analyst": "finance",
    "doctor": "medical", "psychologist": "medical",
    "lawyer": "law", "teacher_edtech": "education", "content_creator": "media",
}

COLLEGES = {
    "tech": ["IITs, NITs, IIITs, BITS Pilani", "Strong state engineering colleges (good placements)", "Tier-1 private (VIT, Manipal, Thapar)"],
    "business": ["SRCC, NMIMS, Christ, top BBA colleges", "IIMs / ISB after graduation", "Tier-1 private B-schools"],
    "finance": ["SRCC & top commerce colleges", "CA / CFA / CMA institutes", "MBA Finance from tier-1"],
    "medical": ["AIIMS & government medical colleges", "Top private medical colleges (NEET)"],
    "design": ["NID, NIFT, Srishti", "Top private design schools + portfolio"],
    "law": ["NLUs (CLAT)", "Symbiosis, Jindal Global Law"],
    "education": ["Central universities + B.Ed", "Build content & teaching skills early"],
    "media": ["Mass-comm colleges (optional)", "Portfolio & audience matter more than the brand"],
    "generic": ["Top government college in your stream", "Reputed private with strong placements", "Prioritise internships + skills over brand name"],
}


def analyze_student(profile: Dict[str, Any]) -> Dict[str, Any]:
    a, pers = _ans(profile), _pers(profile)
    name = _first_name(profile)
    traits = traits_from_personality(pers)
    favorites = as_list(a.get("favorite_subjects"))
    interests = as_list(a.get("career_interests"))
    norm = build_interest_norm(favorites, interests, traits)
    scored = rank_careers(norm, traits)
    matches = [match_card(c, s) for c, s in scored[:5]]
    avoid = build_avoid_from_scored(scored, 4)
    top = matches[0]
    top3 = matches[:3]

    career_match = top["score"]
    ai_resistance = round(mean(m["ai_resistance"] for m in top3))
    personality_fit = int(clamp(round(60 + traits["leadership"] * 12 + (traits["analytical"] or traits["creative"]) * 10 + (career_match - 70) * 0.3), 45, 97))
    sp = salary_projection(top["salary"])
    ai_proof = sorted(matches, key=lambda m: m["ai_risk"])[:3]

    degrees = []
    for m in top3:
        for d in DEGREE_MAP.get(m["key"], []):
            if d not in degrees:
                degrees.append(d)
    domain = DOMAIN_OF.get(top["key"], "generic")
    colleges = COLLEGES.get(domain, COLLEGES["generic"])
    skills = top.get("learn_next", [])

    dream = (a.get("dream_career") or "").strip()
    parents = (a.get("parents_preferred") or "").strip()
    mistakes = [{"title": x["title"], "badges": [{"text": x["ai_risk_label"], "tone": "rose"}],
                 "body": "Why avoid: " + "; ".join(x["why"])} for x in avoid[:3]]
    if parents:
        mistakes.append({"title": f"Blindly following '{parents}'", "badges": [{"text": "Parental pressure", "tone": "amber"}],
                         "body": "Your parents mean well, but a career that doesn't match your strengths and the market is a slow, expensive mistake. Use this data to have an honest conversation with them."})
    if dream and dream.lower() not in top["title"].lower():
        mistakes.append({"title": f"Chasing '{dream}' on hope alone", "badges": [{"text": "Reality check", "tone": "amber"}],
                         "body": f"If '{dream}' is your dream, that's fine — but validate it against demand, competition and your actual strengths before committing years to it."})

    reality = (f"{name}, here's the honest version. Based on your subjects, interests and how you're wired, "
               f"your strongest realistic direction is {top['title']} ({career_match}% fit, {top['ai_risk_label'].lower()}). "
               f"Stop trying to keep every option open — that's exactly how students waste 3-4 years. Pick a direction now, "
               f"and use the next 12 months to build proof, not just marks.")
    letter = (f"Dear {name},\n\nYears from now, you'll be glad you stopped guessing. You leaned into {top['title']}, chose the "
              f"right degree instead of the 'safe' one everyone pushed, and started building skills while your friends were "
              f"still confused. It wasn't always comfortable — but by your mid-20s you were earning around ₹{sp['year5']} LPA and "
              f"doing work that actually fits you. This is where that decision begins. Choose. Commit. Start.\n\n— Your Future Self")

    meta = PROFILE_META["Student"]
    sections = [
        sec("reality_check", "Your Career Reality Check", "Gauge", "intro", text=reality),
        sec("snapshot", "Your Snapshot", "Activity", "scorecards", items=[
            {"label": "Career Match", "value": career_match, "suffix": "%", "tone": "indigo", "caption": top["title"]},
            {"label": "AI Resistance", "value": ai_resistance, "suffix": "%", "tone": "emerald", "caption": "How future-proof"},
            {"label": "Personality Fit", "value": personality_fit, "suffix": "%", "tone": "purple", "caption": "You + the path"},
        ]),
        sec("matches", "Your Best-Fit Career Paths", "Target", "matches", items=matches),
        sec("degrees", "Best Degree & Stream Options", "BookOpen", "tags",
            intro="Degrees that lead directly into your best-fit careers:", items=degrees or ["Pick a degree aligned to your top career above, not just the 'popular' one."]),
        sec("demand", "Future Industry Demand", "TrendingUp", "bars",
            items=[{"label": m["title"], "value": m["market_demand"], "suffix": "%", "tone": "indigo"} for m in top3]),
        sec("ai_proof", "AI-Proof Career Options", "ShieldCheck", "cards",
            items=[{"title": m["title"], "badges": [{"text": m["ai_risk_label"], "tone": "emerald"}, {"text": f"~₹{m['salary_mid']} LPA", "tone": "cyan"}],
                    "body": m["tagline"]} for m in ai_proof]),
        sec("mistakes", "Career Mistakes To Avoid", "ShieldX", "cards", items=mistakes),
        sec("skills", "Skills To Start Learning Now", "Wrench", "list",
            intro="Don't wait for college. Start these now:", items=skills),
        sec("roadmap", "Your Learning Roadmap", "Map", "roadmap", items=[
            {"phase": "Next 6 Months", "focus": "Explore & prove interest", "points": [f"Try a free intro course in {skills[0] if skills else top['title']}", "Build one tiny project / portfolio piece", "Talk to 2 people already in this field"]},
            {"phase": "This Year", "focus": "Build foundations", "points": [f"Go deeper on {', '.join(skills[1:3]) if len(skills) > 2 else 'core skills'}", "Target the right degree & entrance exams", "Maintain marks but prioritise skills"]},
            {"phase": "Before College", "focus": "Lock your direction", "points": ["Shortlist colleges aligned to your path", "Prepare entrance strategy", "Build a simple portfolio / GitHub / profile"]},
            {"phase": "First Year of College", "focus": "Get ahead of peers", "points": ["Start internships early", "Join communities & competitions", "Keep compounding your top skill"]},
        ]),
        sec("growth", "10-Year Growth Projection", "LineChart", "salary_chart",
            points=[{"label": "Start", "value": sp["year1"]}, {"label": "Year 3", "value": sp["year3"]},
                    {"label": "Year 5", "value": sp["year5"]}, {"label": "Year 10", "value": sp["year10"]}],
            note=f"Projected earning trajectory on the {top['title']} path (₹ LPA)."),
        sec("colleges", "College & Prep Recommendations", "Building", "list", intro="Where & how to aim:", items=colleges),
        sec("letter", "A Letter From Your Future Self", "Mail", "letter", text=letter),
    ]
    preview = _preview(meta, f"{name}, your clearest career direction is ready.",
                       f"Your strongest path: {top['title']} ({career_match}% fit).",
                       "Career discovery report — best-fit paths, the right degree, AI-proof options and a 10-year plan.",
                       [{"label": "Career Match", "value": career_match, "suffix": "%", "locked": False},
                        {"label": "Personality Fit", "value": personality_fit, "suffix": "%", "locked": False},
                        {"label": "AI Resistance Score", "locked": True},
                        {"label": "Best Career Path", "locked": True},
                        {"label": "Future Income Potential", "locked": True},
                        {"label": "10-Year Salary Forecast", "locked": True}])

    return _wrap(profile, meta, reality, sections, preview, matches, skills, sp,
                 extra={"ai_resistance_score": ai_resistance, "career_match": career_match,
                        "leadership_potential": int(clamp(round(traits["leadership"] * 100), 20, 95))})


# ============================================================
# IT EMPLOYEE — AI Survival & Growth Report
# ============================================================
DEV_RISK = {
    "ML / AI Engineer": 15, "Data Engineer": 30, "DevOps / Platform Engineer": 28, "Security Engineer": 22,
    "Backend Developer": 38, "Full Stack Developer": 35, "Mobile Developer": 42, "Embedded Engineer": 26,
    "Frontend Developer": 46, "QA / Test Engineer": 70, "Support Engineer": 76, "Other": 45, "": 45,
}
IN_DEMAND_TECH = ["Cloud (AWS/GCP/Azure)", "Kubernetes & Docker", "System Design", "LLMs & RAG",
                  "AI/ML fundamentals", "CI/CD & IaC", "Microservices", "Data pipelines", "Security", "TypeScript", "Go / Rust", "Observability"]
EMERGING_TECH = ["AI Agents & LLM orchestration", "Vector databases & RAG", "Platform Engineering",
                 "Kubernetes at scale", "Rust for systems", "Edge & WebAssembly", "MLOps", "AI security"]
TRANSITION_KEYS = ["ai_ml_engineer", "cloud_devops", "cybersecurity", "data_scientist", "software_engineer"]


def analyze_it(profile: Dict[str, Any]) -> Dict[str, Any]:
    a, pers = _ans(profile), _pers(profile)
    name = _first_name(profile)
    traits = traits_from_personality(pers)
    exp = num(a.get("years_experience"), 3)
    dev_type = a.get("developer_type") or "Other"
    cloud = LEVELS.get(a.get("cloud_knowledge", ""), 30)
    ai_k = LEVELS.get(a.get("ai_knowledge", ""), 30)
    sysd = LEVELS.get(a.get("system_design", ""), 30)
    oss = a.get("open_source", "No")
    user_tech = set(s.lower() for s in as_list(a.get("tech_stack")) + as_list(a.get("languages")))

    base = DEV_RISK.get(dev_type, 45)
    risk = base - ai_k * 0.22 - (cloud + sysd) / 2 * 0.12 - min(exp, 12) * 0.8 - (6 if oss == "Yes" else 0)
    ai_risk = int(clamp(round(risk), 8, 92))
    ai_resistance = 100 - ai_risk
    future_demand = int(clamp(round(60 + (cloud + sysd + ai_k) / 3 * 0.3 - (ai_risk - 30) * 0.25), 28, 96))
    salary_growth = int(clamp(round(40 + min(exp, 12) * 2.5 + (cloud + sysd) / 2 * 0.2 + ai_k * 0.1), 35, 96))
    promotion = int(clamp(round(sysd * 0.4 + traits["leadership"] * 30 + min(exp, 12) * 2), 25, 95))

    gaps = [t for t in IN_DEMAND_TECH if not any(w in t.lower() for w in user_tech)][:6]
    if ai_k < 50 and "AI/ML fundamentals" not in gaps:
        gaps.insert(0, "AI/ML fundamentals")
    transitions = []
    for k in TRANSITION_KEYS:
        c = CAREER_BY_KEY[k]
        feas = int(clamp(round((cloud + sysd + ai_k) / 3 * 0.5 + min(exp, 10) * 3 + (100 - c["difficulty"]) * 0.2 + 15), 30, 92))
        transitions.append({"title": c["title"], "badges": [{"text": f"{feas}% feasible", "tone": "emerald"},
                            {"text": ai_risk_label(c["ai_risk"]), "tone": "indigo"}, {"text": f"~₹{c['salary']['mid']} LPA", "tone": "cyan"}],
                            "body": c["tagline"], "_feas": feas})
    transitions.sort(key=lambda x: x["_feas"], reverse=True)
    for t in transitions:
        t.pop("_feas", None)

    base_sal = max(5, round(5 + exp * 1.6 + (cloud + sysd) / 100 * 6))
    sp = {"year1": base_sal, "year3": round(base_sal * 1.4), "year5": round(base_sal * 2.0), "year10": round(base_sal * 3.2)}
    best_role = CAREER_BY_KEY[TRANSITION_KEYS[0]]
    matches = _cards_by_keys(TRANSITION_KEYS[:3])
    learn = (gaps + EMERGING_TECH)[:6]

    risk_tone = "rose" if ai_risk >= 60 else "amber" if ai_risk >= 40 else "emerald"
    reality = (f"{name}, no sugar-coating: as a {dev_type.lower()} with {int(exp)} years in, your role carries "
               f"{ai_risk_label(ai_risk).lower()} of AI disruption ({ai_risk}%). The developers who get replaced are the ones "
               f"doing what an AI copilot already does. The ones who thrive move up — system design, judgement, AI tooling and "
               f"ownership. Your AI knowledge is your single biggest lever right now.")
    verdict = ("You're in a defensible position — protect it by going deeper, not wider." if ai_risk < 45
               else "You're exposed. Treat the next 6 months as a sprint to move up the value chain before the market does it for you.")
    letter = (f"Dear {name},\n\nThe wave you were afraid of? You learned to surf it. Instead of competing with AI on speed, you "
              f"used it — and stacked the skills it can't replace: design, systems, taste and trust. Today you're a {best_role['title']}-grade "
              f"engineer earning around ₹{sp['year5']} LPA, and 'will AI take my job' is a question other people ask. This is where that pivot starts.\n\n— Your Future Self")

    meta = PROFILE_META["IT Employee"]
    sections = [
        sec("reality_check", "Your AI Reality Check", "Bot", "intro", text=reality),
        sec("snapshot", "Your AI-Survival Snapshot", "Activity", "scorecards", items=[
            {"label": "AI Replacement Risk", "value": ai_risk, "suffix": "%", "tone": risk_tone, "caption": ai_risk_label(ai_risk)},
            {"label": "Future Demand", "value": future_demand, "suffix": "%", "tone": "indigo", "caption": "For your trajectory"},
            {"label": "AI Resistance", "value": ai_resistance, "suffix": "%", "tone": "emerald", "caption": "How defensible"},
        ]),
        sec("threat", "AI Threat Assessment", "ShieldAlert", "bars", items=[
            {"label": "Routine coding (AI copilots)", "value": int(clamp(ai_risk + 15, 10, 99)), "suffix": "%", "tone": "rose"},
            {"label": "Your current role", "value": ai_risk, "suffix": "%", "tone": risk_tone},
            {"label": "System design & architecture", "value": int(clamp(100 - sysd, 10, 80)), "suffix": "%", "tone": "amber"},
            {"label": "AI / ML specialisation", "value": int(clamp(40 - ai_k * 0.3, 8, 45)), "suffix": "%", "tone": "emerald"},
        ]),
        sec("transitions", "Transition Opportunities", "Repeat", "cards", items=transitions[:4]),
        sec("gaps", "Your Tech Skill Gaps", "Puzzle", "tags", intro="In-demand skills you're missing (close these first):", items=gaps or ["Your stack is solid — go deeper on system design + AI."]),
        sec("emerging", "Best Emerging Technologies", "Rocket", "tags", intro="Where the next decade of high pay is heading:", items=EMERGING_TECH),
        sec("roadmap", "Future Tech Roadmap", "Map", "roadmap", items=[
            {"phase": "0-30 Days", "focus": "Stop the bleeding", "points": ["Daily reps with AI tooling on real work", f"Start {gaps[0] if gaps else 'system design'}", "Audit your role vs what AI already does"]},
            {"phase": "30-90 Days", "focus": "Move up the value chain", "points": [f"Ship a project using {learn[0]}", "Lead one design discussion", "Open-source or write about your work"]},
            {"phase": "3-6 Months", "focus": "Specialise", "points": [f"Go deep on {', '.join(learn[1:3])}", "Earn one credible certification", "Target a higher-leverage role internally"]},
            {"phase": "6-12 Months", "focus": "Become AI-proof", "points": ["Own a system end-to-end", "Mentor / build reputation", "Negotiate up or switch with leverage"]},
        ]),
        sec("salary", "Salary Growth Plan", "TrendingUp", "salary_chart",
            points=[{"label": "Now", "value": sp["year1"]}, {"label": "Year 3", "value": sp["year3"]},
                    {"label": "Year 5", "value": sp["year5"]}, {"label": "Year 10", "value": sp["year10"]}],
            note="Projected trajectory if you execute the roadmap (₹ LPA)."),
        sec("verdict", "Your AI-Survival Verdict", "Flag", "callout", tone=risk_tone, label=ai_risk_label(ai_risk), text=verdict),
        sec("letter", "A Letter From Your Future Self", "Mail", "letter", text=letter),
    ]
    preview = _preview(meta, f"{name}, your AI-survival report is ready.",
                       f"AI replacement risk: {ai_risk}% ({ai_risk_label(ai_risk)}).",
                       "AI-survival report — replacement risk, future demand, skill gaps, transitions and a salary growth plan.",
                       [{"label": "AI Replacement Risk", "value": ai_risk, "suffix": "%", "locked": False},
                        {"label": "Future Demand", "value": future_demand, "suffix": "%", "locked": False},
                        {"label": "AI Resistance Score", "locked": True},
                        {"label": "Salary Growth Plan", "locked": True},
                        {"label": "Top Transition Role", "locked": True},
                        {"label": "5-Year Salary Forecast", "locked": True}])

    return _wrap(profile, meta, reality, sections, preview, matches, learn, sp,
                 extra={"ai_resistance_score": ai_resistance, "ai_replacement_risk": ai_risk,
                        "future_demand": future_demand, "salary_growth": salary_growth,
                        "promotion_potential": promotion, "leadership_potential": int(clamp(round(traits["leadership"] * 100), 20, 95))})


# ============================================================
# WORKING PROFESSIONAL — Career Growth Report
# ============================================================
INDUSTRY_OUTLOOK = {
    "IT / Software": (86, 30), "Finance / BFSI": (76, 38), "Healthcare": (80, 18), "Manufacturing": (60, 40),
    "Retail / E-commerce": (70, 45), "Education": (64, 28), "Consulting": (76, 25), "Marketing / Media": (66, 48),
    "Government / Public": (55, 20), "Telecom": (58, 42), "Real Estate": (62, 30), "Other": (66, 35), "": (66, 35),
}
PROMO_HISTORY = {"Never promoted": 10, "1 promotion": 40, "2-3 promotions": 70, "Frequently promoted": 92, "": 35}
LEAD_RESP = {"None": 10, "Lead a small team": 45, "Manage a team": 70, "Manage managers / dept": 92, "": 25}
TEAM_SIZE = {"Just me / IC": 10, "2-5": 35, "6-15": 60, "16-50": 80, "50+": 95, "": 35}


def analyze_professional(profile: Dict[str, Any]) -> Dict[str, Any]:
    a, pers = _ans(profile), _pers(profile)
    name = _first_name(profile)
    traits = traits_from_personality(pers)
    exp = num(a.get("years_experience"), 4)
    cur_sal = num(a.get("current_salary"), 0)
    des_sal = num(a.get("desired_salary"), 0)
    industry = a.get("industry") or "Other"
    ind_demand, ind_risk = INDUSTRY_OUTLOOK.get(industry, (66, 35))
    promo_h = PROMO_HISTORY.get(a.get("promotion_history", ""), 35)
    lead_resp = LEAD_RESP.get(a.get("leadership_responsibilities", ""), 25)
    team = TEAM_SIZE.get(a.get("team_size", ""), 35)
    satisfaction = num(a.get("job_satisfaction"), 6)
    role = a.get("current_role") or "your role"
    desired = a.get("desired_position") or "the next level up"

    leadership_potential = int(clamp(round(traits["leadership"] * 40 + lead_resp * 0.3 + team * 0.15 + traits["communication"] * 15), 25, 97))
    promotion_potential = int(clamp(round(leadership_potential * 0.3 + promo_h * 0.25 + min(exp, 15) / 15 * 20 + sysd_proxy(traits) + ind_demand * 0.1), 25, 96))
    career_growth = int(clamp(round(0.4 * promotion_potential + 0.3 * ind_demand + 0.3 * (100 - ind_risk)), 30, 95))
    salary_now = cur_sal if cur_sal else max(6, round(5 + exp * 1.4))
    target = des_sal if des_sal else round(salary_now * 1.8)
    sp = {"year1": round(salary_now), "year3": round(salary_now + (target - salary_now) * 0.45),
          "year5": round(max(target, salary_now * 1.6)), "year10": round(max(target, salary_now) * 1.7)}
    feasible = int(clamp(round(100 - max(0, (target - salary_now) / max(salary_now, 1) - 0.8) * 60), 30, 95)) if salary_now else 70

    matches = _cards_by_keys(["product_manager", "management_consultant", "sales_leader"])
    if matches:
        matches[0]["title"] = desired if a.get("desired_position") else matches[0]["title"]
    learn = ["Stakeholder leadership", "Strategic communication", "Data-driven decisions", "Executive presence", "Domain depth"]

    reality = (f"{name}, the honest read on your growth: in {industry} as {role} with {int(exp)} years, your promotion potential "
               f"is {promotion_potential}% and your industry outlook is {'strong' if ind_demand >= 75 else 'moderate' if ind_demand >= 60 else 'soft'}. "
               f"What's holding most people at your stage back isn't skill — it's visibility, ownership and positioning. "
               f"{'Your satisfaction is low — that is data, not a mood. ' if satisfaction <= 4 else ''}You don't need to work harder; you need to be seen leading.")
    outlook = (f"{industry} demand is {ind_demand}% with {ai_risk_label(ind_risk).lower()} automation exposure. "
               f"{'Position yourself in the AI-resistant, high-judgement parts of your field.' if ind_risk >= 40 else 'The fundamentals favour you — compound your advantage.'}")
    letter = (f"Dear {name},\n\nYou stopped waiting to be noticed and started leading out loud. You took ownership others avoided, "
              f"made your impact measurable, and positioned yourself for {desired}. Today you earn around ₹{sp['year5']} LPA and people "
              f"bring you the hard problems. The version of you reading this is exactly where that shift begins. Lead now.\n\n— Your Future Self")

    meta = PROFILE_META["Working Professional"]
    sections = [
        sec("reality_check", "Your Growth Reality Check", "Gauge", "intro", text=reality),
        sec("snapshot", "Your Growth Snapshot", "Activity", "scorecards", items=[
            {"label": "Promotion Potential", "value": promotion_potential, "suffix": "%", "tone": "indigo", "caption": f"Toward {desired}"},
            {"label": "Career Growth", "value": career_growth, "suffix": "%", "tone": "purple", "caption": "Overall trajectory"},
            {"label": "Leadership Potential", "value": leadership_potential, "suffix": "%", "tone": "cyan", "caption": "Your ceiling"},
        ]),
        sec("readiness", "Promotion Readiness Breakdown", "BarChart3", "bars", items=[
            {"label": "Leadership signal", "value": leadership_potential, "suffix": "%", "tone": "indigo"},
            {"label": "Track record (promotions)", "value": promo_h, "suffix": "%", "tone": "purple"},
            {"label": "Tenure & experience", "value": int(clamp(round(min(exp, 15) / 15 * 100), 10, 100)), "suffix": "%", "tone": "cyan"},
            {"label": "Communication & visibility", "value": int(round(traits["communication"] * 100)), "suffix": "%", "tone": "amber"},
        ]),
        sec("salary", "Salary Forecast", "TrendingUp", "salary_chart",
            points=[{"label": "Now", "value": sp["year1"]}, {"label": "Year 3", "value": sp["year3"]},
                    {"label": "Year 5", "value": sp["year5"]}, {"label": "Year 10", "value": sp["year10"]}],
            note=f"Realistic trajectory ({'feasibility ' + str(feasible) + '% for your target' if cur_sal else 'estimate'}). ₹ LPA."),
        sec("leadership", "Leadership Analysis", "Crown", "cards", items=[
            {"title": "Your leadership style", "badges": [{"text": "Team Player" if traits["team"] else "Independent Operator", "tone": "indigo"}, {"text": trait_labels(traits)[0], "tone": "purple"}],
             "body": f"You lead best as a {'collaborative' if traits['team'] else 'directive, autonomous'} operator with {'high' if traits['communication'] >= 0.6 else 'developing'} communication confidence.",
             "points": ["Double down on visible ownership", "Build executive communication", "Sponsor / mentor to multiply impact"]},
            {"title": "Biggest growth gap", "badges": [{"text": "Fix this first", "tone": "rose"}],
             "body": "Most professionals plateau on visibility and strategic positioning, not capability. Make your wins legible to decision-makers."},
        ]),
        sec("outlook", "Industry Outlook", "Building2", "callout", tone="indigo" if ind_demand >= 70 else "amber", label=f"{industry} — {ind_demand}% demand", text=outlook),
        sec("roadmap", "Your Growth Roadmap", "Map", "roadmap", items=[
            {"phase": "Next 90 Days", "focus": "Become visible", "points": ["Own one high-impact, measurable project", "Build a relationship with your skip-level", "Quantify and broadcast your wins"]},
            {"phase": "6 Months", "focus": "Lead beyond your role", "points": [f"Develop {learn[0]} & {learn[1]}", "Take on cross-functional leadership", "Close one strategic skill gap"]},
            {"phase": "12 Months", "focus": "Earn the next level", "points": [f"Position explicitly for {desired}", "Build a sponsor, not just mentors", "Negotiate with documented impact"]},
        ]),
        sec("letter", "A Letter From Your Future Self", "Mail", "letter", text=letter),
    ]
    preview = _preview(meta, f"{name}, your career growth report is ready.",
                       f"Promotion potential: {promotion_potential}% · Leadership: {leadership_potential}%.",
                       "Career growth report — promotion readiness, salary forecast, leadership analysis and a growth roadmap.",
                       [{"label": "Career Growth", "value": career_growth, "suffix": "%", "locked": False},
                        {"label": "Leadership Potential", "value": leadership_potential, "suffix": "%", "locked": False},
                        {"label": "Promotion Readiness", "locked": True},
                        {"label": "Salary Growth Plan", "locked": True},
                        {"label": "Next Best Role", "locked": True},
                        {"label": "5-Year Salary Forecast", "locked": True}])

    return _wrap(profile, meta, reality, sections, preview, matches, learn, sp,
                 extra={"ai_resistance_score": 100 - ind_risk, "promotion_potential": promotion_potential,
                        "career_growth": career_growth, "leadership_potential": leadership_potential})


def sysd_proxy(traits: Dict[str, float]) -> float:
    """Small competence proxy from analytical/structured traits for promotion math."""
    return (traits["analytical"] * 0.5 + traits["structured"] * 0.5) * 15


# ============================================================
# Wrapper + dispatch
# ============================================================
def _wrap(profile, meta, reality, sections, preview, matches, learn, sp, extra=None):
    out = {
        "user_type": profile.get("user_type"),
        "product_name": meta["product"], "product_icon": meta["icon"],
        "primary_goal": meta["goal"], "headline": preview["headline"],
        "sections": sections, "preview": preview,
        # flat fields reused by add-ons + PDF cover
        "matches": matches or [], "learn_next": learn or [], "salary_projection": sp,
        "career_reality_check": reality,
    }
    if extra:
        out.update(extra)
    out.setdefault("ai_resistance_score", 70)
    return out


ENGINES = {
    "Student": analyze_student,
    "IT Employee": analyze_it,
    "Working Professional": analyze_professional,
}


def analyze_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    ut = profile.get("user_type") or "Student"
    engine = ENGINES.get(ut)
    if engine:
        return engine(profile)
    # Phase 2/3 interim routing (until dedicated engines are built)
    if ut in ("Student", "Fresher"):
        return analyze_student(profile)
    if ut == "IT Employee":
        return analyze_it(profile)
    return analyze_professional(profile)
