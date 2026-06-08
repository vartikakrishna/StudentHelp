"""Per-category analysis engines. Each user type is its own product:
different scoring model, different report sections, different recommendations,
different action plan. Deterministic numbers here; AI only enhances prose.
"""
from typing import Dict, List, Any
from statistics import mean

from careers import CAREER_BY_KEY, ai_risk_label, rank_careers, match_card, build_avoid_from_scored
import career_db
from common import (
    clamp, num, as_list, traits_from_personality, trait_labels,
    build_interest_norm, salary_projection, sec, diagnostic_sections, action_roadmap, growth_sp,
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

# career_db domain -> COLLEGES bucket
DB_DOMAIN_COLLEGE = {
    "Technology": "tech", "Creative": "design", "Media": "media", "Business": "business",
    "Finance": "finance", "Entrepreneurship": "business", "Healthcare": "medical",
    "Legal": "law", "Government": "generic", "Defense": "generic", "Education": "education",
    "Research": "generic", "Sports": "generic", "Skilled Trades": "generic", "Hospitality": "generic",
}


def analyze_student(profile: Dict[str, Any]) -> Dict[str, Any]:
    a, pers = _ans(profile), _pers(profile)
    name = _first_name(profile)
    traits = traits_from_personality(pers)
    favorites = as_list(a.get("favorite_subjects"))
    interests = as_list(a.get("career_interests"))
    norm = build_interest_norm(favorites, interests, traits)

    dream_text = (a.get("dream_career") or "").strip()
    parents = (a.get("parents_preferred") or "").strip()
    gb = career_db.goal_block(dream_text, norm, traits, n_related=3)
    dream = gb["dream"]

    # Matches: dream/best-fit first, then related, then top overall fits (deduped)
    matches = list(gb["matches"])
    seen = {m["key"] for m in matches}
    for c, s in career_db.rank_all(norm, traits, 10):
        if len(matches) >= 5:
            break
        if c["key"] not in seen:
            matches.append(career_db._card(c, s))
            seen.add(c["key"])
    top = matches[0]
    top3 = matches[:3]

    career_match = gb["dream_score"]
    success = gb["success_probability"]
    ai_resistance = round(mean(m["ai_resistance"] for m in top3))
    personality_fit = int(clamp(round(60 + traits["leadership"] * 12 + (traits["analytical"] or traits["creative"]) * 10 + (career_match - 70) * 0.3), 45, 97))
    sp = salary_projection(top["salary"])
    ai_proof = sorted(matches, key=lambda m: m["ai_risk"])[:3]
    avoid = career_db.avoid_block(norm, traits, gb.get("exclude"), 4)

    degrees = []
    for m in [dream] + gb["related"]:
        for d in (m.get("degrees") or []):
            if d not in degrees:
                degrees.append(d)
    degrees = degrees[:6]
    colleges = COLLEGES.get(DB_DOMAIN_COLLEGE.get(dream["domain"], "generic"), COLLEGES["generic"])
    skills = dream.get("skills") or dream.get("learn_next") or top.get("learn_next", [])

    # Honesty Rule — keep the dream, show challenges + backups (never substitute)
    dream_label = gb["career_title"] if gb["resolved"] else top["title"]
    success_tone = "emerald" if (success or 0) >= 60 else "amber" if (success or 0) >= 40 else "rose"
    risk_tone = "emerald" if dream["ai_risk"] <= 30 else "amber" if dream["ai_risk"] < 60 else "rose"
    dream_cards = [{
        "title": f"Your goal: {dream_label}",
        "badges": [{"text": f"{career_match}% Dream Match", "tone": "indigo"},
                   {"text": f"{success}% Success Odds", "tone": success_tone} if success else {"text": "Best-fit path", "tone": "indigo"},
                   {"text": dream["ai_risk_label"], "tone": risk_tone},
                   {"text": dream["verdict"], "tone": "purple"}],
        "body": (f"You told us this is your dream — so we kept it front and centre. We won't swap it for a 'safer' job. "
                 f"But honesty matters: here's exactly what makes it hard and what you must do to earn it." if gb["resolved"]
                 else "Based on your subjects, interests and wiring, this is your strongest realistic direction."),
        "points": gb["challenges"] or ["You're well-aligned — commit and start building proof."],
    }]
    if gb["related"]:
        dream_cards.append({
            "title": "Your backup plan — related careers in the same world",
            "body": "If the dream proves too brutal, these keep you in the same field without starting from zero:",
            "points": [f"{r['title']} — {r['score']}% fit · {r['ai_risk_label'].lower()} · ~₹{r['salary_mid']} LPA" for r in gb["related"]],
        })

    mistakes = [{"title": x["title"], "badges": [{"text": x["ai_risk_label"], "tone": "rose"}],
                 "body": "Why avoid: " + "; ".join(x["why"])} for x in avoid[:3]]
    if parents and (not gb["resolved"] or parents.lower() not in dream_label.lower()):
        mistakes.append({"title": f"Blindly following '{parents}'", "badges": [{"text": "Parental pressure", "tone": "amber"}],
                         "body": "Your parents mean well, but a career that doesn't match your strengths and the market is a slow, expensive mistake. Use this data to have an honest conversation with them."})

    reality = (f"{name}, you said your dream is {dream_label}. Honest read: it's a {career_match}% match with a {success}% realistic "
               f"success probability — {dream['verdict'].lower()}. I'm not going to talk you out of it, and I'm not going to pretend it's easy. "
               f"The next 12 months decide it: build proof, not just marks, and keep a related backup alive so one setback doesn't end the dream."
               if gb["resolved"] else
               f"{name}, here's the honest version. Based on your subjects, interests and how you're wired, your strongest realistic direction "
               f"is {top['title']} ({career_match}% fit, {top['ai_risk_label'].lower()}). Stop trying to keep every option open — that's exactly "
               f"how students waste 3-4 years. Pick a direction now, and use the next 12 months to build proof, not just marks.")
    letter = (f"Dear {name},\n\nYears from now, you'll be glad you stopped guessing. You committed to {dream_label}, did the brutal work others "
              f"avoided, and started building skills while your friends were still confused. It wasn't always comfortable — but by your mid-20s "
              f"you were earning around ₹{sp['year5']} LPA and doing work that actually fits you. This is where that decision begins. Choose. Commit. Start.\n\n— Your Future Self")

    meta = PROFILE_META["Student"]
    sections = [
        sec("reality_check", "Your Career Reality Check", "Gauge", "intro", text=reality),
        sec("snapshot", "Your Snapshot", "Activity", "scorecards", items=[
            {"label": "Dream Career Match", "value": career_match, "suffix": "%", "tone": "indigo", "caption": dream_label},
            {"label": "Success Probability", "value": success or career_match, "suffix": "%", "tone": success_tone, "caption": "Realistic odds"},
            {"label": "AI Resistance", "value": ai_resistance, "suffix": "%", "tone": "emerald", "caption": "How future-proof"},
        ]),
        sec("dream_verdict", "Your Dream Career — Honest Verdict", "Target", "cards", items=dream_cards),
        sec("matches", "Your Dream + Best-Fit Paths", "Compass", "matches", items=matches),
        sec("degrees", "Best Degree & Stream Options", "BookOpen", "tags",
            intro="Degrees that lead directly into your dream & best-fit careers:", items=degrees or ["Pick a degree aligned to your top career above, not just the 'popular' one."]),
        sec("demand", "Future Industry Demand", "TrendingUp", "bars",
            items=[{"label": m["title"], "value": m["market_demand"], "suffix": "%", "tone": "indigo"} for m in top3]),
        sec("ai_proof", "AI-Proof Career Options", "ShieldCheck", "cards",
            items=[{"title": m["title"], "badges": [{"text": m["ai_risk_label"], "tone": "emerald"}, {"text": f"~₹{m['salary_mid']} LPA", "tone": "cyan"}],
                    "body": m["tagline"]} for m in ai_proof]),
        sec("mistakes", "Career Mistakes To Avoid", "ShieldX", "cards", items=mistakes),
        sec("skills", "Skills To Start Learning Now", "Wrench", "list",
            intro="Don't wait for college. Start these now:", items=skills),
        sec("learning_roadmap", "Your Learning Roadmap", "Map", "roadmap", items=[
            {"phase": "Next 6 Months", "focus": "Explore & prove interest", "points": [f"Try a free intro course in {skills[0] if skills else dream_label}", "Build one tiny project / portfolio piece", "Talk to 2 people already in this field"]},
            {"phase": "This Year", "focus": "Build foundations", "points": [f"Go deeper on {', '.join(skills[1:3]) if len(skills) > 2 else 'core skills'}", "Target the right degree & entrance exams", "Maintain marks but prioritise skills"]},
            {"phase": "Before College", "focus": "Lock your direction", "points": ["Shortlist colleges aligned to your path", "Prepare entrance strategy", "Build a simple portfolio / GitHub / profile"]},
            {"phase": "First Year of College", "focus": "Get ahead of peers", "points": ["Start internships early", "Join communities & competitions", "Keep compounding your top skill"]},
        ]),
        sec("growth", "10-Year Growth Projection", "LineChart", "salary_chart",
            points=[{"label": "Start", "value": sp["year1"]}, {"label": "Year 3", "value": sp["year3"]},
                    {"label": "Year 5", "value": sp["year5"]}, {"label": "Year 10", "value": sp["year10"]}],
            note=f"Projected earning trajectory on the {dream_label} path (₹ LPA)."),
        sec("colleges", "College & Prep Recommendations", "Building", "list", intro="Where & how to aim:", items=colleges),
        *diagnostic_sections(
            risks=[
                {"title": f"Drifting toward {avoid[0]['title']}", "badges": [{"text": avoid[0]["ai_risk_label"], "tone": "rose"}], "body": "A weak-fit, high-competition path quietly wastes your most valuable years."},
                {"title": "Following pressure, not fit", "badges": [{"text": "Common trap", "tone": "amber"}], "body": "Choosing a career to please others or chase prestige is the #1 regret students have years later."},
                {"title": "Chasing the dream with zero backup", "badges": [{"text": "Costly", "tone": "amber"}], "body": "Going all-in with no related fallback means one setback can end the dream. Keep a backup alive."}],
            opportunities=[
                {"title": f"Lean into {ai_proof[0]['title']}", "body": f"An AI-resistant, well-matched path ({ai_proof[0]['ai_risk_label']}) — start early and you'll be years ahead of peers."},
                {"title": "Build skills before college", "body": "Most students wait. The ones who start projects and skills now enter college already ahead."},
                {"title": "Early internships & communities", "body": "Real exposure beats theory — it compounds into clarity and opportunities."}],
            focus=[f"Commit to {dream_label} and build proof", f"Start learning {skills[0] if skills else 'your top skill'}", "Plan the right degree & entrance strategy", "Keep one related backup career alive"],
            stop=["Keeping every option open out of fear", "Choosing a path only for prestige or pressure", "Chasing marks while ignoring real skills", "Comparing your start to everyone else's"]),
        action_roadmap(
            {"focus": "Explore with intent", "points": [f"Try a free intro to {skills[0] if skills else dream_label}", "Talk to 2 people in that career", "Confirm your direction"]},
            {"focus": "Build foundations", "points": ["Start core skills + entrance prep", "Ship one small project", "Maintain marks without obsessing"]},
            {"focus": "Commit & get ahead", "points": ["Lock your degree & college shortlist", "Build a simple portfolio/profile", "Start early internships / competitions"]}),
        sec("letter", "A Letter From Your Future Self", "Mail", "letter", text=letter),
    ]
    preview = _preview(meta, f"{name}, your clearest career direction is ready.",
                       f"Your dream — {dream_label} — is a {career_match}% match ({dream['verdict'].lower()}).",
                       "Career discovery report — your dream career verdict, related backups, the right degree, AI-proof options and a 10-year plan.",
                       [{"label": "Dream Career Match", "value": career_match, "suffix": "%", "locked": False},
                        {"label": "Personality Fit", "value": personality_fit, "suffix": "%", "locked": False},
                        {"label": "Success Probability", "locked": True},
                        {"label": "Related Backup Careers", "locked": True},
                        {"label": "Future Income Potential", "locked": True},
                        {"label": "10-Year Salary Forecast", "locked": True}])

    return _wrap(profile, meta, reality, sections, preview, matches, skills, sp,
                 extra={"ai_resistance_score": ai_resistance, "career_match": career_match,
                        "dream_career": dream_label, "dream_match_score": career_match, "success_probability": success,
                        "ai_focus": "career discovery for a student: HONOR the stated dream career as #1, never substitute it; be brutally honest about its challenges, give a realistic success probability and related backup careers",
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
        sec("tech_roadmap", "Future Tech Roadmap", "Map", "roadmap", items=[
            {"phase": "0-30 Days", "focus": "Stop the bleeding", "points": ["Daily reps with AI tooling on real work", f"Start {gaps[0] if gaps else 'system design'}", "Audit your role vs what AI already does"]},
            {"phase": "30-90 Days", "focus": "Move up the value chain", "points": [f"Ship a project using {learn[0]}", "Lead one design discussion", "Open-source or write about your work"]},
            {"phase": "3-6 Months", "focus": "Specialise", "points": [f"Go deep on {', '.join(learn[1:3])}", "Earn one credible certification", "Target a higher-leverage role internally"]},
            {"phase": "6-12 Months", "focus": "Become AI-proof", "points": ["Own a system end-to-end", "Mentor / build reputation", "Negotiate up or switch with leverage"]},
        ]),
        sec("salary", "Salary Growth Plan", "TrendingUp", "salary_chart",
            points=[{"label": "Now", "value": sp["year1"]}, {"label": "Year 3", "value": sp["year3"]},
                    {"label": "Year 5", "value": sp["year5"]}, {"label": "Year 10", "value": sp["year10"]}],
            note="Projected trajectory if you execute the roadmap (₹ LPA)."),
        *diagnostic_sections(
            risks=[
                {"title": "Replaced by AI copilots", "badges": [{"text": ai_risk_label(ai_risk), "tone": risk_tone}], "body": "If most of your day is what an AI assistant already does well, your role is exposed."},
                {"title": "Falling behind on AI tooling", "badges": [{"text": "Skill decay", "tone": "amber"}], "body": "Engineers who don't use AI daily are being out-shipped by those who do."},
                {"title": "Narrow, replaceable skillset", "badges": [{"text": "Gap", "tone": "amber"}], "body": "Single-layer skills (only frontend, only manual QA) are the easiest to automate or offshore."}],
            opportunities=[
                {"title": f"Move toward {transitions[0]['title'] if transitions else 'higher-leverage roles'}", "body": "Higher-judgement roles AI can't do are where pay and security are heading."},
                {"title": "Specialise in AI / systems", "body": "AI engineering and system design are the most defensible, best-paid directions."},
                {"title": "Own systems end-to-end", "body": "Ownership and architecture beat raw coding speed in the AI era."}],
            focus=[f"Close your top gap: {gaps[0] if gaps else 'system design'}", "Use AI tooling on real work daily", "Go deep on system design", "Plan a move up the value chain"],
            stop=["Doing only what AI copilots already do", "Avoiding AI tools out of pride", "Staying in a comfortable, replaceable role", "Collecting tutorials without shipping"]),
        action_roadmap(
            {"focus": "Stop the bleeding", "points": ["Use AI tooling on real work daily", f"Start {gaps[0] if gaps else 'system design'}", "Audit your role vs AI"]},
            {"focus": "Move up the chain", "points": [f"Ship a project using {learn[0] if learn else 'a modern skill'}", "Lead one design discussion", "Build reputation (OSS / writing)"]},
            {"focus": "Become AI-proof", "points": ["Own a system end-to-end", "Earn a credible certification", "Negotiate up or switch with leverage"]}),
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
                        "ai_focus": "AI disruption for an IT employee: be blunt about replacement risk and the fastest move up the value chain",
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
        sec("growth_roadmap", "Your Growth Roadmap", "Map", "roadmap", items=[
            {"phase": "Next 90 Days", "focus": "Become visible", "points": ["Own one high-impact, measurable project", "Build a relationship with your skip-level", "Quantify and broadcast your wins"]},
            {"phase": "6 Months", "focus": "Lead beyond your role", "points": [f"Develop {learn[0]} & {learn[1]}", "Take on cross-functional leadership", "Close one strategic skill gap"]},
            {"phase": "12 Months", "focus": "Earn the next level", "points": [f"Position explicitly for {desired}", "Build a sponsor, not just mentors", "Negotiate with documented impact"]},
        ]),
        *diagnostic_sections(
            risks=[
                {"title": "Invisible to decision-makers", "badges": [{"text": "Promotion-blocker", "tone": "rose"}], "body": "Hard work that skip-levels never see doesn't get promoted. Visibility is the real gate."},
                {"title": "Plateauing on skill alone", "badges": [{"text": "Ceiling", "tone": "amber"}], "body": "Past a point, capability stops differentiating you — positioning and leadership do."},
                {"title": f"{industry} automation exposure", "badges": [{"text": ai_risk_label(ind_risk), "tone": "amber" if ind_risk < 45 else "rose"}], "body": "Stay in the high-judgement, AI-resistant parts of your field."}],
            opportunities=[
                {"title": "Own a high-impact project", "body": "One visible, measurable win moves you more than a year of quiet reliability."},
                {"title": "Find a sponsor", "body": "Mentors advise; sponsors promote. Most professionals only build mentors."},
                {"title": f"Position for {desired}", "body": "Explicitly signalling your target role shapes how leaders see you."}],
            focus=["Own one visible, measurable initiative", f"Develop {learn[0]} & {learn[1]}", "Build a sponsor relationship", f"Position explicitly for {desired}"],
            stop=["Working harder while staying invisible", "Waiting to be noticed", "Measuring yourself only on output", "Ignoring the strategic / political side of growth"]),
        action_roadmap(
            {"focus": "Become visible", "points": ["Own one high-impact project", "Build a skip-level relationship", "Quantify & broadcast your wins"]},
            {"focus": "Lead beyond your role", "points": [f"Develop {learn[0]} & {learn[1]}", "Take cross-functional leadership", "Close one strategic gap"]},
            {"focus": "Earn the next level", "points": [f"Position for {desired}", "Build a sponsor", "Negotiate with documented impact"]}),
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
                        "ai_focus": "promotion & income growth for a working professional: be honest about visibility, positioning and the real path to the next level",
                        "career_growth": career_growth, "leadership_potential": leadership_potential})


def sysd_proxy(traits: Dict[str, float]) -> float:
    """Small competence proxy from analytical/structured traits for promotion math."""
    return (traits["analytical"] * 0.5 + traits["structured"] * 0.5) * 15


# ============================================================
# FRESHER — First-Job Readiness Report
# ============================================================
INTERNSHIP_SCORE = {"None": 12, "1": 48, "2": 72, "3+": 92, "": 20}
PROJECT_SCORE = {"None": 12, "1-2": 50, "3-5": 78, "5+": 94, "": 25}
RESUME_SCORE = {"Yes, polished": 100, "In progress": 55, "Not yet": 12, "": 30}
JOBPREF = ["Product / Startups", "Service / IT", "Core / Domain", "Government / PSU", "Research / Higher studies", "Open to anything"]
FRESHER_DEMAND = ["Communication & clarity", "Problem solving / DSA", "Excel / Sheets", "SQL", "One core tool for your field", "Git & version control", "A portfolio project", "Internship experience", "Aptitude / reasoning", "Domain fundamentals"]


def analyze_fresher(profile):
    a, pers = _ans(profile), _pers(profile)
    name = _first_name(profile)
    traits = traits_from_personality(pers)
    intern = INTERNSHIP_SCORE.get(a.get("internships", ""), 20)
    proj = PROJECT_SCORE.get(a.get("projects", ""), 25)
    skills = as_list(a.get("skills"))
    skillcount = clamp(len(skills) * 12, 0, 100)
    resume = RESUME_SCORE.get(a.get("resume_ready", ""), 30)
    linkedin = 85 if a.get("linkedin") == "Yes" else 20
    certs = 65 if (a.get("certifications") or "").strip() else 20
    employability = int(clamp(round(intern * 0.24 + proj * 0.24 + skillcount * 0.24 + resume * 0.1 + linkedin * 0.08 + certs * 0.1), 18, 96))
    job_readiness = int(clamp(round(employability * 0.7 + resume * 0.2 + linkedin * 0.1), 18, 96))
    interview = int(clamp(round(skillcount * 0.4 + proj * 0.3 + traits["communication"] * 30), 18, 95))
    gaps = [s for s in FRESHER_DEMAND if all(s.lower() not in x.lower() and x.lower() not in s.lower() for x in skills)][:6]
    base = max(3, round(3 + skillcount / 100 * 4 + proj / 100 * 2 + (1 if a.get("job_preference") == "Product / Startups" else 0)))
    sp = growth_sp(base)
    exp = num(a.get("expected_salary"), 0)

    # Future-Goal engine: resolve the fresher's dream/target role + related entry roles
    target_text = (a.get("target_role") or "").strip()
    matches = []
    target_section = None
    if target_text:
        norm = build_interest_norm([], [], traits)
        tgt = career_db.goal_block(target_text, norm, traits, n_related=3)
        matches = tgt["matches"]
        if tgt["resolved"]:
            tc = tgt["dream"]
            need = [s for s in (tc.get("skills") or []) if all(s.lower() not in x.lower() and x.lower() not in s.lower() for x in skills)]
            gaps = (need + gaps)[:6]
        target_section = sec("target_direction", f"Your Target Role: {tgt.get('career_title', target_text)}", "Compass", "matches", items=matches)

    reality = (f"{name}, blunt truth: companies don't hire potential, they hire proof. Your employability sits at {employability}% — "
               f"{'you have real signal, now convert it into offers' if employability >= 60 else 'right now your profile looks like every other fresher, and that is the problem'}. "
               f"{'Your resume isn’t ready, which means recruiters are filtering you out before a human reads it. ' if resume < 60 else ''}"
               f"The next 90 days decide whether you start strong or settle.")
    meta = PROFILE_META["Fresher"]
    sections = [
        sec("reality_check", "Where You Are Today", "Gauge", "intro", text=reality),
        sec("snapshot", "Your Readiness Snapshot", "Activity", "scorecards", items=[
            {"label": "Job Readiness", "value": job_readiness, "suffix": "%", "tone": "indigo", "caption": "Overall"},
            {"label": "Employability", "value": employability, "suffix": "%", "tone": "purple", "caption": "vs the market"},
            {"label": "Interview Readiness", "value": interview, "suffix": "%", "tone": "cyan", "caption": "Can you convert?"}]),
        sec("breakdown", "Readiness Breakdown", "BarChart3", "bars", items=[
            {"label": "Internship experience", "value": intern, "suffix": "%", "tone": "indigo"},
            {"label": "Projects / portfolio", "value": proj, "suffix": "%", "tone": "purple"},
            {"label": "Skills depth", "value": int(skillcount), "suffix": "%", "tone": "cyan"},
            {"label": "Resume & LinkedIn", "value": int((resume + linkedin) / 2), "suffix": "%", "tone": "amber"}]),
        sec("gaps", "Your Skill Gaps", "Puzzle", "tags", intro="Close these to clear the first filter:", items=gaps or ["Your basics are solid — now build proof through projects."]),
        *( [target_section] if target_section else [] ),
        *diagnostic_sections(
            risks=[
                {"title": "Resume gets auto-rejected", "badges": [{"text": "High impact", "tone": "rose"}], "body": "No ATS-ready resume means you never reach a human. This is the #1 silent killer for freshers."},
                {"title": "Zero differentiation", "badges": [{"text": "Common", "tone": "amber"}], "body": "Same degree, same generic skills as thousands of others. Without a project or internship you blend in."},
                {"title": "Over-applying, under-preparing", "badges": [{"text": "Behaviour", "tone": "amber"}], "body": "Mass-applying without interview prep burns opportunities you can't get back."}],
            opportunities=[
                {"title": "One strong portfolio project", "body": "A single real, shippable project beats 10 lines of 'familiar with' on your resume."},
                {"title": "Referrals over portals", "body": "70%+ of fresher hires come through referrals — your LinkedIn + alumni network is underused."},
                {"title": "Interview reps now", "body": "Mock interviews + DSA/aptitude practice compound fast over 90 days."}],
            focus=["Make your resume ATS-ready and tailored to 1 role type", "Ship one portfolio project that proves a skill", "Do 3 mock interviews + daily aptitude/DSA reps", f"Close your top gap: {gaps[0] if gaps else 'core domain fundamentals'}"],
            stop=["Mass-applying with a generic resume", "Waiting to feel 'fully ready' before applying", "Collecting random certificates with no projects", "Ignoring LinkedIn and referrals"]),
        sec("salary", "Your Salary Projection", "TrendingUp", "salary_chart",
            points=[{"label": "First job", "value": sp["year1"]}, {"label": "Year 3", "value": sp["year3"]}, {"label": "Year 5", "value": sp["year5"]}, {"label": "Year 10", "value": sp["year10"]}],
            note=f"Realistic trajectory if you execute the plan{' (you quoted ₹' + str(int(exp)) + ' LPA expected)' if exp else ''}. ₹ LPA."),
        action_roadmap(
            {"focus": "Get hireable", "points": ["Rebuild resume (ATS + tailored)", "Optimise LinkedIn headline & About", "List 30 target companies + referral contacts"]},
            {"focus": "Convert", "points": ["Ship 1 portfolio project", "Apply via referrals to 30 roles", "Complete 5 mock interviews + aptitude prep"]},
            {"focus": "Grow in role", "points": ["Land & onboard strong in first job", "Build one in-demand skill deeply", "Document wins for your first appraisal"]}),
        sec("letter", "A Letter From Your Future Self", "Mail", "letter", text=(
            f"Dear {name},\n\nYou stopped waiting to feel ready and started proving you were. You fixed the resume, shipped the project, "
            f"used referrals instead of spraying applications — and the offers came. That first job set the trajectory for everything after. "
            f"This is exactly where it begins. Start today.\n\n— Your Future Self")),
    ]
    preview = _preview(meta, f"{name}, your first-job readiness report is ready.",
                       f"Job readiness: {job_readiness}% · Employability: {employability}%.",
                       "First-job readiness report — employability, skill gaps, interview plan and a 90-day action plan.",
                       [{"label": "Job Readiness", "value": job_readiness, "suffix": "%", "locked": False},
                        {"label": "Employability", "value": employability, "suffix": "%", "locked": False},
                        {"label": "Interview Readiness", "locked": True}, {"label": "Skill Gaps", "locked": True},
                        {"label": "Salary Projection", "locked": True}, {"label": "First-Job Strategy", "locked": True}])
    return _wrap(profile, meta, reality, sections, preview, matches, gaps, sp,
                 extra={"ai_focus": "first-job employability: be blunt about why a fresher gets filtered out and the fastest path to a real offer. If a target role is given, honor it and recommend related entry roles",
                        "career_match": employability, "ai_resistance_score": 75})


# ============================================================
# CAREER SWITCHER — Career Transition Blueprint
# ============================================================
LEARN_TIME = {"<5 hrs/week": 25, "5-10 hrs/week": 55, "10-20 hrs/week": 80, "20+ hrs/week": 95, "": 45}
RUNWAY = {"No savings": 15, "1-3 months": 40, "3-6 months": 65, "6-12 months": 85, "12+ months": 95, "": 45}


def analyze_switcher(profile):
    a, pers = _ans(profile), _pers(profile)
    name = _first_name(profile)
    traits = traits_from_personality(pers)
    current = a.get("current_profession") or "your current field"
    target = a.get("target_profession") or "your target field"
    transfer = as_list(a.get("transferable_skills"))
    learn_time = LEARN_TIME.get(a.get("learning_time", ""), 45)
    runway = RUNWAY.get(a.get("financial_situation", ""), 45)
    transfer_score = int(clamp(len(transfer) * 14 + 20, 20, 92))
    feasibility = int(clamp(round(transfer_score * 0.35 + learn_time * 0.3 + runway * 0.2 + traits["risk"] * 15), 20, 94))
    difficulty = int(clamp(100 - feasibility + 10, 15, 90))
    success = int(clamp(round(feasibility * 0.6 + learn_time * 0.25 + traits["stress"] * 15), 20, 93))
    months = max(3, round(18 - learn_time / 100 * 12 + difficulty / 100 * 8))
    base = 6 + transfer_score / 100 * 6
    sp = growth_sp(base)
    gaps = ["Core skills for " + target, "A portfolio in the new field", "Network in the target industry", "Proof of capability (project/freelance)", "Domain vocabulary & tools"]

    # Future-Goal engine: resolve the target profession + related bridge careers (Honesty Rule)
    norm = build_interest_norm([], [], traits)
    tgt = career_db.goal_block(target, norm, traits, n_related=4)
    matches = tgt["matches"]
    if tgt["resolved"]:
        tc = tgt["dream"]
        gaps = (tc.get("skills") or [])[:4] + ["A portfolio/freelance proof in " + tc["title"], "Network in the target industry"]
        target = tc["title"]

    reality = (f"{name}, honest assessment: switching from {current} to {target} is {'very doable' if feasibility >= 70 else 'realistic but hard' if feasibility >= 50 else 'an uphill climb'} "
               f"({feasibility}% feasibility). The market doesn't reward intention — it rewards proof in the new field. "
               f"{'Your runway is thin, so speed and a bridge income matter. ' if runway < 50 else ''}You'll switch on the strength of transferable skills + visible projects, not a fresh start from zero.")
    meta = PROFILE_META["Career Switcher"]
    sections = [
        sec("reality_check", "Where You Are Today", "Gauge", "intro", text=reality),
        sec("snapshot", "Your Switch Snapshot", "Activity", "scorecards", items=[
            {"label": "Switch Feasibility", "value": feasibility, "suffix": "%", "tone": "indigo", "caption": f"{current} → {target}"},
            {"label": "Success Probability", "value": success, "suffix": "%", "tone": "emerald", "caption": "If you commit"},
            {"label": "Difficulty", "value": difficulty, "suffix": "%", "tone": "amber" if difficulty < 70 else "rose", "caption": "Honest rating"}]),
        sec("breakdown", "Feasibility Breakdown", "BarChart3", "bars", items=[
            {"label": "Transferable skills", "value": transfer_score, "suffix": "%", "tone": "indigo"},
            {"label": "Learning capacity", "value": learn_time, "suffix": "%", "tone": "purple"},
            {"label": "Financial runway", "value": runway, "suffix": "%", "tone": "cyan"},
            {"label": "Risk appetite", "value": int(traits["risk"] * 100), "suffix": "%", "tone": "amber"}]),
        sec("transfer", "Your Transferable Advantages", "Recycle", "tags", intro="Lean on these to switch faster:", items=transfer or ["Identify and document the skills that carry over — communication, analysis, domain knowledge."]),
        sec("target_direction", f"Your Target Direction: {target}", "Compass", "matches", items=matches),
        sec("gaps", "Skill Gaps To Close", "Puzzle", "tags", intro=f"What {target} demands that you must build:", items=gaps),
        *diagnostic_sections(
            risks=[
                {"title": "Switching with zero proof", "badges": [{"text": "Critical", "tone": "rose"}], "body": f"Wanting {target} isn't enough — without a project/freelance proof you compete as a beginner."},
                {"title": "Running out of runway", "badges": [{"text": "Financial", "tone": "amber"}], "body": "Quitting before you have traction or a bridge income is the most common switch failure."},
                {"title": "Half-committing", "badges": [{"text": "Behaviour", "tone": "amber"}], "body": "Casual upskilling without a deadline drags the switch out for years."}],
            opportunities=[
                {"title": "Bridge roles", "body": f"Hybrid roles that blend {current} + {target} let you switch with less risk and salary drop."},
                {"title": "Freelance to prove it", "body": "One paid freelance gig in the new field is louder than any certificate."},
                {"title": "Your existing network", "body": "People who already trust you are your fastest door into the new industry."}],
            focus=[f"Build 1 real {target} project this quarter", "Find a bridge role that values your current experience", f"Close your top gap: {gaps[0]}", "Network with 10 people already in the target field"],
            stop=["Collecting courses without shipping anything", "Quitting before you have traction or savings", "Comparing your start to others' middle", "Hiding your current experience instead of leveraging it"]),
        sec("salary", "Salary Impact Of The Switch", "TrendingUp", "salary_chart",
            points=[{"label": "Switch yr", "value": sp["year1"]}, {"label": "Year 3", "value": sp["year3"]}, {"label": "Year 5", "value": sp["year5"]}, {"label": "Year 10", "value": sp["year10"]}],
            note=f"Expect a possible short-term dip, then a steeper climb. Estimated transition: ~{months} months. ₹ LPA."),
        action_roadmap(
            {"focus": "Validate & plan", "points": [f"Map {current}→{target} skill overlap", "Pick 1 focused learning path", "Build a bridge-income plan"]},
            {"focus": "Build proof", "points": [f"Ship 1 {target} project / freelance gig", "Network with 10 insiders", "Apply to bridge roles"]},
            {"focus": "Complete the switch", "points": ["Land a role in the new field", "Negotiate using transferable value", "Compound your new-field reputation"]}),
        sec("letter", "A Letter From Your Future Self", "Mail", "letter", text=(
            f"Dear {name},\n\nThe switch felt impossible until you stopped waiting for permission and started building proof. You used "
            f"what you already had, shipped real work in {target}, and crossed over without starting from zero. Today this is just your career — "
            f"not a leap of faith. It begins with the first project. Build it.\n\n— Your Future Self")),
    ]
    preview = _preview(meta, f"{name}, your career transition blueprint is ready.",
                       f"Switch feasibility: {feasibility}% · Success probability: {success}%.",
                       "Career transition blueprint — feasibility, transferable skills, timeline, salary impact and a migration plan.",
                       [{"label": "Switch Feasibility", "value": feasibility, "suffix": "%", "locked": False},
                        {"label": "Difficulty", "value": difficulty, "suffix": "%", "locked": False},
                        {"label": "Success Probability", "locked": True}, {"label": "Transition Timeline", "locked": True},
                        {"label": "Skill Gaps", "locked": True}, {"label": "Salary Impact", "locked": True}])
    return _wrap(profile, meta, reality, sections, preview, matches, gaps, sp,
                 extra={"ai_focus": f"career switch from {current} to {target}: be honest about feasibility, the proof needed, and the fastest low-risk path. Keep the user's target field — recommend RELATED bridge roles, never an unrelated substitute",
                        "career_match": feasibility, "ai_resistance_score": 72})


# ============================================================
# LAID OFF EMPLOYEE — Career Recovery Blueprint
# ============================================================
SAVINGS = {"No savings": 10, "<1 month": 30, "1-3 months": 50, "3-6 months": 72, "6-12 months": 88, "12+ months": 96, "": 45}
RELOCATE = {"Yes": 90, "Maybe": 55, "No": 25, "": 50}


def analyze_laidoff(profile):
    a, pers = _ans(profile), _pers(profile)
    name = _first_name(profile)
    traits = traits_from_personality(pers)
    exp = num(a.get("years_experience"), 4)
    prev_sal = num(a.get("previous_salary"), 0)
    skills = as_list(a.get("skills"))
    skillcount = clamp(len(skills) * 12, 0, 100)
    savings = SAVINGS.get(a.get("savings_runway", ""), 45)
    reloc = RELOCATE.get(a.get("relocation", ""), 50)
    industry = a.get("desired_industry") or a.get("industry") or "your field"
    ind_demand = INDUSTRY_OUTLOOK.get(a.get("desired_industry") or a.get("industry") or "Other", (66, 35))[0]
    recovery = int(clamp(round(skillcount * 0.3 + min(exp, 15) / 15 * 25 + ind_demand * 0.2 + reloc * 0.1 + traits["stress"] * 15), 20, 94))
    reemploy = int(clamp(round(recovery * 0.6 + ind_demand * 0.25 + reloc * 0.15), 20, 95))
    salary_recovery = int(clamp(round(60 + min(exp, 15) * 1.5 + skillcount * 0.15 - (20 if ind_demand < 60 else 0)), 35, 95))
    base = prev_sal if prev_sal else max(6, round(5 + exp * 1.4))
    sp = {"year1": round(base * 0.9), "year3": round(base * 1.2), "year5": round(base * 1.6), "year10": round(base * 2.4)}
    gaps = ["Refreshed, ATS-ready resume", "Active referral pipeline", "One current in-demand skill", "Interview reps", "A short bridge-income source"]

    reality = (f"{name}, first: a layoff is a market event, not a verdict on your worth. Now the honest part — your recovery score is "
               f"{recovery}% and you have roughly {a.get('savings_runway','limited')} of runway. Speed matters more than perfection. "
               f"The fastest path back to income is leveraging your network and existing skills now, while upskilling in parallel — not after.")
    meta = PROFILE_META["Laid Off Employee"]
    sections = [
        sec("reality_check", "Where You Are Today", "Gauge", "intro", text=reality),
        sec("snapshot", "Your Recovery Snapshot", "Activity", "scorecards", items=[
            {"label": "Recovery Score", "value": recovery, "suffix": "%", "tone": "indigo", "caption": "Bounce-back strength"},
            {"label": "Reemployment Probability", "value": reemploy, "suffix": "%", "tone": "emerald", "caption": "Next 90 days"},
            {"label": "Salary Recovery", "value": salary_recovery, "suffix": "%", "tone": "cyan", "caption": "vs previous pay"}]),
        sec("breakdown", "Recovery Breakdown", "BarChart3", "bars", items=[
            {"label": "Skills & experience", "value": int((skillcount + min(exp, 15) / 15 * 100) / 2), "suffix": "%", "tone": "indigo"},
            {"label": f"{industry} demand", "value": ind_demand, "suffix": "%", "tone": "purple"},
            {"label": "Financial runway", "value": savings, "suffix": "%", "tone": "cyan" if savings >= 50 else "rose"},
            {"label": "Flexibility (relocation)", "value": reloc, "suffix": "%", "tone": "amber"}]),
        sec("income", "Emergency Income Options", "Wallet", "cards", items=[
            {"title": "Freelance / consulting", "badges": [{"text": "Fastest", "tone": "emerald"}], "body": "Sell your existing expertise by the hour while you search — covers runway and keeps your skills sharp."},
            {"title": "Contract / temp roles", "badges": [{"text": "Bridge", "tone": "indigo"}], "body": "Contract work converts to full-time often and fills resume gaps."},
            {"title": "Part-time in adjacent field", "badges": [{"text": "Stability", "tone": "cyan"}], "body": "Buys time and options without derailing your main search."}],),
        *diagnostic_sections(
            risks=[
                {"title": "Letting the gap grow", "badges": [{"text": "Time-sensitive", "tone": "rose"}], "body": "The longer the resume gap, the harder the conversation. Add a freelance/contract line fast."},
                {"title": "Searching in silence", "badges": [{"text": "Behaviour", "tone": "amber"}], "body": "Quietly applying online while avoiding your network is the slowest route back."},
                {"title": "Runway running out", "badges": [{"text": "Financial", "tone": "rose" if savings < 50 else "amber"}], "body": "Without a bridge income, desperation forces a worse deal later."}],
            opportunities=[
                {"title": "Your network is warm", "body": "Most people want to help after a layoff — a direct, specific ask converts fast."},
                {"title": "Pivot to higher-demand field", "body": f"{industry} has demand at {ind_demand}% — re-position toward its growing roles."},
                {"title": "Negotiate from contract", "body": "Contract-to-hire lets you prove value and negotiate up."}],
            focus=["Tell your network you're looking — specific, this week", "Refresh resume + add a freelance/consulting line", "Line up one bridge-income source", "Target reemployment in the highest-demand part of your field"],
            stop=["Applying silently and waiting", "Holding out only for your exact old title/pay", "Spending the search 'perfecting' instead of contacting people", "Treating the layoff as a personal failure"]),
        sec("salary", "Your Income Recovery Path", "TrendingUp", "salary_chart",
            points=[{"label": "Re-entry", "value": sp["year1"]}, {"label": "Year 3", "value": sp["year3"]}, {"label": "Year 5", "value": sp["year5"]}, {"label": "Year 10", "value": sp["year10"]}],
            note="Often a small dip at re-entry, then full recovery and beyond. ₹ LPA."),
        action_roadmap(
            {"focus": "Stabilise & activate", "points": ["Tell 20 contacts you're looking (specific ask)", "Refresh resume + LinkedIn 'Open to Work'", "Start one bridge-income stream"]},
            {"focus": "Convert", "points": ["Apply via referrals to 30 roles", "Take 5 interviews + negotiate", "Upskill one in-demand skill in parallel"]},
            {"focus": "Recover & grow", "points": ["Land role at/above previous level", "Rebuild emergency runway", "Future-proof with a current skill"]}),
        sec("letter", "A Letter From Your Future Self", "Mail", "letter", text=(
            f"Dear {name},\n\nThe layoff felt like the floor falling out. But you moved fast, leaned on people who wanted to help, and bridged "
            f"the gap with your own skills. Within months you were back — and looking back, it became a turning point, not an ending. "
            f"You're closer to that comeback than it feels right now. Start with one message today.\n\n— Your Future Self")),
    ]
    preview = _preview(meta, f"{name}, your career recovery blueprint is ready.",
                       f"Recovery score: {recovery}% · Reemployment probability: {reemploy}%.",
                       "Career recovery blueprint — recovery score, emergency income options, pivot opportunities and a 90-day comeback plan.",
                       [{"label": "Recovery Score", "value": recovery, "suffix": "%", "locked": False},
                        {"label": "Reemployment Probability", "value": reemploy, "suffix": "%", "locked": False},
                        {"label": "Salary Recovery Potential", "locked": True}, {"label": "Fastest Return To Income", "locked": True},
                        {"label": "Career Pivot Opportunities", "locked": True}, {"label": "90-Day Recovery Roadmap", "locked": True}])
    return _wrap(profile, meta, reality, sections, preview, [], gaps, sp,
                 extra={"ai_focus": "post-layoff recovery: be reassuring but brutally practical about the fastest path back to income",
                        "career_match": recovery, "ai_resistance_score": 70})


# ============================================================
# MANAGER — Leadership Growth Report
# ============================================================
BUDGET = {"None": 10, "Small (<₹50L)": 45, "Mid (₹50L-5Cr)": 72, "Large (₹5Cr+)": 92, "": 30}
HIRING = {"None": 15, "Helped hire": 45, "Hired independently": 72, "Built teams": 92, "": 30}
SCALE3 = {"Low": 25, "Medium": 55, "High": 85, "": 45}


def analyze_manager(profile):
    a, pers = _ans(profile), _pers(profile)
    name = _first_name(profile)
    traits = traits_from_personality(pers)
    team = TEAM_SIZE.get(a.get("team_size", ""), 45)
    budget = BUDGET.get(a.get("budget_responsibility", ""), 30)
    hiring = HIRING.get(a.get("hiring_experience", ""), 30)
    conflict = SCALE3.get(a.get("conflict_management", ""), 45)
    strategy = SCALE3.get(a.get("strategic_planning", ""), 45)
    revenue = SCALE3.get(a.get("revenue_responsibility", ""), 45)
    leadership = int(clamp(round(traits["leadership"] * 30 + team * 0.2 + conflict * 0.2 + traits["communication"] * 20 + hiring * 0.1), 30, 97))
    executive = int(clamp(round(strategy * 0.35 + revenue * 0.25 + budget * 0.2 + leadership * 0.2), 25, 96))
    promotion = int(clamp(round(executive * 0.4 + leadership * 0.3 + hiring * 0.15 + traits["communication"] * 15), 25, 95))
    style = "Visionary Strategist" if strategy >= 70 else "People-First Coach" if traits["team"] else "Decisive Operator"
    sp = growth_sp(max(18, round(14 + team / 100 * 14)))
    gaps = ["Executive communication & storytelling", "P&L / business ownership", "Strategic planning at scale", "Board / stakeholder influence", "Building a personal leadership brand"]

    reality = (f"{name}, the honest read: you're a {'strong' if leadership >= 70 else 'developing'} manager (leadership {leadership}%), but executive "
               f"readiness is {executive}%. The jump from manager to leader isn't about managing more people — it's about owning outcomes, "
               f"strategy and revenue. {'You manage well; now you must be seen shaping direction, not just executing it.' if strategy < 70 else 'You think strategically — make that visible to the people who promote.'}")
    meta = PROFILE_META["Manager"]
    sections = [
        sec("reality_check", "Where You Are Today", "Gauge", "intro", text=reality),
        sec("snapshot", "Your Leadership Snapshot", "Activity", "scorecards", items=[
            {"label": "Executive Potential", "value": executive, "suffix": "%", "tone": "indigo", "caption": "Manager → leader"},
            {"label": "Leadership Score", "value": leadership, "suffix": "%", "tone": "purple", "caption": "Today"},
            {"label": "Promotion Potential", "value": promotion, "suffix": "%", "tone": "cyan", "caption": "Next level"}]),
        sec("breakdown", "Executive Readiness Breakdown", "BarChart3", "bars", items=[
            {"label": "Strategic planning", "value": strategy, "suffix": "%", "tone": "indigo"},
            {"label": "Business / revenue ownership", "value": revenue, "suffix": "%", "tone": "purple"},
            {"label": "People leadership & hiring", "value": int((team + hiring) / 2), "suffix": "%", "tone": "cyan"},
            {"label": "Influence & communication", "value": int(traits["communication"] * 100), "suffix": "%", "tone": "amber"}]),
        sec("style", "Your Management Style", "Crown", "cards", items=[
            {"title": style, "badges": [{"text": "Your signature", "tone": "indigo"}, {"text": trait_labels(traits)[0], "tone": "purple"}],
             "body": f"You lead best as a {'collaborative coach' if traits['team'] else 'decisive operator'}. Your edge is {'people & culture' if traits['team'] else 'execution & clarity'}; your risk is over-indexing there.",
             "points": ["Pair your style with visible strategy", "Delegate execution to free up for direction", "Make your team's wins legible upward"]}]),
        sec("brand", "Influence & Personal Brand", "Megaphone", "cards", items=[
            {"title": "Build executive presence", "badges": [{"text": "Promotion lever", "tone": "emerald"}], "body": "Promotions to leadership are decided on perceived judgement and influence, not effort. Be visible where strategy is discussed."},
            {"title": "Sponsor, don't just manage", "body": "Develop a sponsor above you and become one below you — multiplied influence is what executives have."}]),
        *diagnostic_sections(
            risks=[
                {"title": "Stuck as 'the great manager'", "badges": [{"text": "Career-capping", "tone": "rose"}], "body": "Being too good at execution can trap you — leaders are promoted for outcomes and strategy, not reliability."},
                {"title": "Invisible to decision-makers", "badges": [{"text": "Visibility", "tone": "amber"}], "body": "If skip-levels don't see your strategic thinking, you won't be in the room for the next role."},
                {"title": "No business ownership", "badges": [{"text": "Gap", "tone": "amber"}], "body": "Without P&L or revenue exposure, the executive jump stalls."}],
            opportunities=[
                {"title": "Own a strategic initiative", "body": "Volunteering for a cross-functional, revenue-linked project is the fastest path to executive visibility."},
                {"title": "Build a leadership brand", "body": "Speaking, writing, mentoring — your reputation is a promotion accelerant most managers ignore."},
                {"title": "Develop successors", "body": "Leaders who build leaders get promoted; irreplaceable managers get stuck."}],
            focus=["Take ownership of one revenue/strategy initiative", f"Close your top exec gap: {gaps[0]}", "Increase visibility with skip-level leaders", "Develop a successor for your current role"],
            stop=["Doing IC work that should be delegated", "Measuring yourself only on team output", "Avoiding the political / strategic side of leadership", "Being the bottleneck instead of the multiplier"]),
        sec("salary", "Leadership Earning Trajectory", "TrendingUp", "salary_chart",
            points=[{"label": "Now", "value": sp["year1"]}, {"label": "Year 3", "value": sp["year3"]}, {"label": "Year 5", "value": sp["year5"]}, {"label": "Year 10", "value": sp["year10"]}],
            note="Executive trajectory if you make the manager→leader shift. ₹ LPA."),
        action_roadmap(
            {"focus": "Shift the lens", "points": ["Claim 1 strategic, revenue-linked initiative", "Schedule skip-level visibility", "Audit what to delegate"]},
            {"focus": "Lead beyond your team", "points": ["Deliver the strategic initiative", "Close one executive skill gap", "Start a leadership-brand habit (write/speak/mentor)"]},
            {"focus": "Earn the executive seat", "points": ["Own a P&L or business outcome", "Build a sponsor + a successor", "Position explicitly for the leadership role"]}),
        sec("letter", "A Letter From Your Future Self", "Mail", "letter", text=(
            f"Dear {name},\n\nYou stopped trying to be the most reliable manager and started being the most strategic leader. You delegated, "
            f"owned outcomes, made your thinking visible — and the title followed the influence. Today you shape direction, not just deliver it. "
            f"That shift starts with one initiative you choose to own. Choose it.\n\n— Your Future Self")),
    ]
    preview = _preview(meta, f"{name}, your leadership growth report is ready.",
                       f"Executive potential: {executive}% · Leadership score: {leadership}%.",
                       "Leadership growth report — executive potential, management style, influence building and a promotion roadmap.",
                       [{"label": "Executive Potential", "value": executive, "suffix": "%", "locked": False},
                        {"label": "Leadership Score", "value": leadership, "suffix": "%", "locked": False},
                        {"label": "Promotion Potential", "locked": True}, {"label": "Management Style", "locked": True},
                        {"label": "Executive Readiness", "locked": True}, {"label": "Personal Brand Plan", "locked": True}])
    return _wrap(profile, meta, reality, sections, preview, [], gaps, sp,
                 extra={"ai_focus": "manager-to-executive growth: be blunt about why great managers get stuck and what executive readiness really requires",
                        "career_match": executive, "leadership_potential": leadership, "ai_resistance_score": 78})


# ============================================================
# FREELANCER — Freelance Income Report
# ============================================================
PRICING = {"Budget / low": 25, "Mid-market": 55, "Premium": 85, "": 40}
PORTFOLIO = {"Weak / none": 20, "Okay": 50, "Strong": 80, "Outstanding": 95, "": 45}
CLIENTS_MAP = {"0-1": 20, "2-4": 50, "5-10": 75, "10+": 92, "": 35}


def analyze_freelancer(profile):
    a, pers = _ans(profile), _pers(profile)
    name = _first_name(profile)
    traits = traits_from_personality(pers)
    services = as_list(a.get("services"))
    monthly = num(a.get("monthly_income"), 0)
    clients = CLIENTS_MAP.get(a.get("clients", ""), 35)
    pricing = PRICING.get(a.get("pricing", ""), 40)
    channels = as_list(a.get("marketing_channels"))
    portfolio = PORTFOLIO.get(a.get("portfolio_quality", ""), 45)
    brand = int(clamp(round(portfolio * 0.45 + len(channels) * 8 + traits["communication"] * 20), 20, 95))
    acquisition = int(clamp(round(len(channels) * 12 + clients * 0.4 + brand * 0.2), 20, 94))
    income_growth = int(clamp(round(pricing * 0.35 + acquisition * 0.3 + brand * 0.2 + traits["risk"] * 15), 25, 95))
    expansion = int(clamp(round((len(services) * 10) + pricing * 0.3 + traits["leadership"] * 20 + 20), 25, 94))
    base_year = max(4, round((monthly * 12 / 100000) if monthly else 6))
    sp = {"year1": base_year, "year3": round(base_year * 1.8), "year5": round(base_year * 2.8), "year10": round(base_year * 4.5)}
    missing_channels = [c for c in ["Referrals system", "LinkedIn content", "Cold outreach", "Niche communities", "SEO / inbound", "Marketplaces (Upwork etc.)", "Email list"] if c not in channels][:5]
    gaps = ["Premium positioning & niche", "A repeatable client pipeline", "Productized services / retainers", "Strong proof (case studies)", "Systems to scale beyond hours"]

    reality = (f"{name}, straight talk: your income growth potential is {income_growth}%, but most freelancers stay stuck trading hours for "
               f"low rates because they under-position and under-market. {'Your pricing is leaving money on the table. ' if pricing < 55 else ''}"
               f"The leap from freelancer to freelance-business is a niche, a pipeline and retainers — not just more hustle.")
    meta = PROFILE_META["Freelancer"]
    sections = [
        sec("reality_check", "Where You Are Today", "Gauge", "intro", text=reality),
        sec("snapshot", "Your Freelance Snapshot", "Activity", "scorecards", items=[
            {"label": "Income Growth Potential", "value": income_growth, "suffix": "%", "tone": "indigo", "caption": "Upside"},
            {"label": "Personal Brand Score", "value": brand, "suffix": "%", "tone": "purple", "caption": "Visibility"},
            {"label": "Client Acquisition", "value": acquisition, "suffix": "%", "tone": "cyan", "caption": "Pipeline health"}]),
        sec("breakdown", "Business Health Breakdown", "BarChart3", "bars", items=[
            {"label": "Pricing power", "value": pricing, "suffix": "%", "tone": "indigo"},
            {"label": "Portfolio & proof", "value": portfolio, "suffix": "%", "tone": "purple"},
            {"label": "Marketing reach", "value": int(clamp(len(channels) * 16, 10, 100)), "suffix": "%", "tone": "cyan"},
            {"label": "Expansion potential", "value": expansion, "suffix": "%", "tone": "amber"}]),
        sec("channels", "Marketing Channels To Add", "Megaphone", "tags", intro="Add 1-2 of these to build a predictable pipeline:", items=missing_channels or ["Double down on your best-performing channel and systematise referrals."]),
        sec("expand", "Service Expansion Plays", "Layers", "cards", items=[
            {"title": "Productize & retain", "badges": [{"text": "Stable income", "tone": "emerald"}], "body": "Convert one-off projects into monthly retainers and fixed-scope packages to escape the feast-famine cycle."},
            {"title": "Move up-market", "badges": [{"text": "Higher rates", "tone": "indigo"}], "body": "Niche down, raise prices, and target clients who value outcomes over hourly cost."}]),
        *diagnostic_sections(
            risks=[
                {"title": "Trading time for money", "badges": [{"text": "Ceiling", "tone": "rose"}], "body": "Hourly, generalist work caps your income at your available hours. That's a job, not a business."},
                {"title": "Feast-or-famine pipeline", "badges": [{"text": "Instability", "tone": "amber"}], "body": "No system for leads means income swings wildly and you accept bad clients out of fear."},
                {"title": "Under-pricing", "badges": [{"text": "Money left on table", "tone": "amber"}], "body": "Low rates signal low value and attract the worst clients."}],
            opportunities=[
                {"title": "Niche + premium positioning", "body": "Specialists charge 2-5x generalists. A sharp niche is your fastest rate increase."},
                {"title": "Retainers & productized services", "body": "Predictable monthly revenue changes everything — stability funds growth."},
                {"title": "Content as a sales engine", "body": "One consistent channel (LinkedIn/SEO) compounds into inbound leads that pre-sell you."}],
            focus=["Define a sharp niche and raise your rates", "Build one repeatable lead channel", "Convert clients to retainers/packages", "Publish 2-3 case studies as proof"],
            stop=["Competing on price as a generalist", "Saying yes to every low-value client", "Relying on word-of-mouth alone", "Selling hours instead of outcomes"]),
        sec("salary", "Your Income Growth Path", "TrendingUp", "salary_chart",
            points=[{"label": "Now", "value": sp["year1"]}, {"label": "Year 3", "value": sp["year3"]}, {"label": "Year 5", "value": sp["year5"]}, {"label": "Year 10", "value": sp["year10"]}],
            note="Annualised income if you niche, raise rates and systematise leads. ₹ LPA equivalent."),
        action_roadmap(
            {"focus": "Position & price", "points": ["Pick a profitable niche", "Raise rates / repackage offers", "Publish 2 case studies"]},
            {"focus": "Build the pipeline", "points": ["Launch 1 lead channel (content/outreach)", "Convert 2 clients to retainers", "Set up a referral system"]},
            {"focus": "Scale beyond hours", "points": ["Productize a core service", "Hit a stable monthly revenue floor", "Consider subcontracting/team to scale"]}),
        sec("letter", "A Letter From Your Future Self", "Mail", "letter", text=(
            f"Dear {name},\n\nYou stopped competing on price and started owning a niche. You raised your rates, built a pipeline that brought clients "
            f"to you, and turned projects into predictable retainers. The freelancer became a freelance business — and your income finally matched "
            f"your skill. It starts with choosing your niche. Choose it.\n\n— Your Future Self")),
    ]
    preview = _preview(meta, f"{name}, your freelance income report is ready.",
                       f"Income growth potential: {income_growth}% · Brand score: {brand}%.",
                       "Freelance income report — income growth potential, client acquisition, brand building and a business roadmap.",
                       [{"label": "Income Growth Potential", "value": income_growth, "suffix": "%", "locked": False},
                        {"label": "Personal Brand Score", "value": brand, "suffix": "%", "locked": False},
                        {"label": "Client Acquisition Strategy", "locked": True}, {"label": "Service Expansion", "locked": True},
                        {"label": "Pricing Strategy", "locked": True}, {"label": "Income Growth Path", "locked": True}])
    return _wrap(profile, meta, reality, sections, preview, [], gaps, sp,
                 extra={"ai_focus": "freelancer income growth: be blunt about why they're stuck trading hours for low rates and the path to a freelance business",
                        "career_match": income_growth, "ai_resistance_score": 74})


# ============================================================
# BUSINESS OWNER — Business Growth Intelligence Report
# ============================================================
MARGIN = {"Loss-making": 10, "Break-even": 30, "Low (<10%)": 45, "Healthy (10-25%)": 75, "Strong (25%+)": 92, "": 40}
EMP_MAP = {"Just me": 20, "2-5": 45, "6-20": 70, "21-50": 85, "50+": 95, "": 35}
ACQ = {"Word of mouth only": 25, "1 main channel": 50, "Few channels": 72, "Diversified & systematic": 92, "": 40}


def analyze_business(profile):
    a, pers = _ans(profile), _pers(profile)
    name = _first_name(profile)
    traits = traits_from_personality(pers)
    btype = a.get("business_type") or "your business"
    revenue = num(a.get("revenue"), 0)
    employees = EMP_MAP.get(a.get("employees", ""), 35)
    margin = MARGIN.get(a.get("profit_margin", ""), 40)
    channels = as_list(a.get("marketing_channels"))
    acq = ACQ.get(a.get("customer_acquisition", ""), 40)
    challenge = a.get("biggest_challenge") or "scaling sustainably"
    marketing = int(clamp(round(len(channels) * 11 + acq * 0.4), 15, 95))
    health = int(clamp(round(margin * 0.4 + acq * 0.25 + marketing * 0.2 + employees * 0.15), 20, 95))
    growth = int(clamp(round(marketing * 0.3 + acq * 0.3 + traits["risk"] * 20 + (100 - margin) * 0.1 + 15), 25, 95))
    revenue_opt = int(clamp(round(margin * 0.5 + acq * 0.3 + traits["analytical"] * 20), 25, 94))
    base = max(8, round(revenue / 100000) if revenue else 12)
    sp = {"year1": base, "year3": round(base * 1.9), "year5": round(base * 3.2), "year10": round(base * 6)}
    missing_channels = [c for c in ["Referral programme", "Paid ads", "SEO / content", "Email & retention", "Partnerships", "Social / community", "Sales team / outbound"] if c not in channels][:5]
    gaps = ["A diversified acquisition system", "Pricing & margin optimisation", "Retention / repeat revenue", "Delegation & systems", "Data-driven decisions"]

    reality = (f"{name}, the honest diagnosis: your business health is {health}% with {challenge.lower()} as your stated bottleneck. "
               f"{'Thin margins mean you’re working hard for little — fix pricing and retention before chasing more leads. ' if margin < 50 else ''}"
               f"Most owners plateau because they stay the bottleneck: everything depends on them. Real growth comes from systems, acquisition diversity and margins — not just more hours.")
    meta = PROFILE_META["Business Owner"]
    sections = [
        sec("reality_check", "Where You Are Today", "Gauge", "intro", text=reality),
        sec("snapshot", "Your Business Snapshot", "Activity", "scorecards", items=[
            {"label": "Business Health", "value": health, "suffix": "%", "tone": "indigo", "caption": "Overall"},
            {"label": "Growth Potential", "value": growth, "suffix": "%", "tone": "purple", "caption": "Upside"},
            {"label": "Revenue Optimisation", "value": revenue_opt, "suffix": "%", "tone": "cyan", "caption": "Margin & pricing"}]),
        sec("breakdown", "Health Breakdown", "BarChart3", "bars", items=[
            {"label": "Profit margin", "value": margin, "suffix": "%", "tone": "indigo" if margin >= 50 else "rose"},
            {"label": "Customer acquisition", "value": acq, "suffix": "%", "tone": "purple"},
            {"label": "Marketing reach", "value": marketing, "suffix": "%", "tone": "cyan"},
            {"label": "Team & systems", "value": employees, "suffix": "%", "tone": "amber"}]),
        sec("revenue", "Revenue Opportunities", "Coins", "cards", items=[
            {"title": "Raise prices / improve margin", "badges": [{"text": "Fastest profit", "tone": "emerald"}], "body": "A small price increase or cost fix often beats months of new-customer chasing — it drops straight to profit."},
            {"title": "Retention & repeat revenue", "badges": [{"text": "Compounding", "tone": "indigo"}], "body": "Selling more to existing customers is 5-7x cheaper than acquiring new ones. Most owners ignore it."},
            {"title": "Upsells & bundles", "body": "Increase average order value with packages, add-ons and tiers."}]),
        sec("marketing", "Marketing Channels To Add", "Megaphone", "tags", intro="Diversify acquisition so you don't depend on one source:", items=missing_channels or ["Systematise and double down on your best channel, then add one more."]),
        sec("challenge", "Your #1 Bottleneck", "AlertTriangle", "callout", tone="amber", label=challenge, text="This is the constraint capping your growth right now. The 30/90/365 plan below is sequenced to break it first — everything else compounds once it's solved."),
        *diagnostic_sections(
            risks=[
                {"title": "You are the bottleneck", "badges": [{"text": "Scale-blocker", "tone": "rose"}], "body": "If revenue stops when you stop, you own a job, not a scalable business. Systems and delegation are non-negotiable."},
                {"title": "Single acquisition channel", "badges": [{"text": "Fragile", "tone": "amber"}], "body": "Depending on one source (or word-of-mouth) means one change can sink revenue overnight."},
                {"title": "Thin / unknown margins", "badges": [{"text": "Profit risk", "tone": "rose" if margin < 50 else "amber"}], "body": "Growing revenue with bad margins just grows your problems. Fix unit economics first."}],
            opportunities=[
                {"title": "Margin & pricing fixes", "body": "Often the fastest profit lever — most owners under-price and over-discount."},
                {"title": "Retention engine", "body": "Repeat & referral revenue is cheaper and more predictable than constant new acquisition."},
                {"title": "Systemise to scale", "body": "Documented processes + the right hire free you to work ON the business, not IN it."}],
            focus=["Fix pricing/margins and unit economics", "Add one reliable acquisition channel", "Build a retention/repeat-revenue play", f"Solve your #1 bottleneck: {challenge.lower()}"],
            stop=["Being involved in every decision", "Relying on a single lead source", "Discounting to win low-quality customers", "Chasing revenue while ignoring profit"]),
        sec("salary", "Revenue Growth Trajectory", "TrendingUp", "salary_chart",
            points=[{"label": "Now", "value": sp["year1"]}, {"label": "Year 3", "value": sp["year3"]}, {"label": "Year 5", "value": sp["year5"]}, {"label": "Year 10", "value": sp["year10"]}],
            note="Revenue trajectory (₹ Lakh) if you fix margins, diversify acquisition and systemise."),
        action_roadmap(
            {"focus": "Fix the foundation", "points": ["Audit pricing & margins; fix unit economics", "Document your top 3 processes", "Identify the #1 bottleneck to break"]},
            {"focus": "Diversify & retain", "points": ["Launch 1 new acquisition channel", "Set up a retention/referral play", "Make one freeing hire or delegation"]},
            {"focus": "Scale the system", "points": ["Hit a higher, stable revenue floor", "Build a repeatable growth engine", "Work ON the business, not IN it"]}),
        sec("letter", "A Letter From Your Future Self", "Mail", "letter", text=(
            f"Dear {name},\n\nYou stopped being the bottleneck. You fixed your margins, built systems, diversified how customers found you, and "
            f"hired so the business could run without you in every decision. {btype} grew because you finally worked on it, not just in it. "
            f"That shift starts with the next 30 days. Begin.\n\n— Your Future Self")),
    ]
    preview = _preview(meta, f"{name}, your business growth intelligence report is ready.",
                       f"Business health: {health}% · Growth potential: {growth}%.",
                       "Business growth intelligence — health score, revenue opportunities, marketing roadmap and a scale plan.",
                       [{"label": "Business Health", "value": health, "suffix": "%", "locked": False},
                        {"label": "Growth Potential", "value": growth, "suffix": "%", "locked": False},
                        {"label": "Revenue Optimisation", "locked": True}, {"label": "Marketing Opportunities", "locked": True},
                        {"label": "Expansion Strategy", "locked": True}, {"label": "Scale Plan", "locked": True}])
    return _wrap(profile, meta, reality, sections, preview, [], gaps, sp,
                 extra={"ai_focus": "business growth: be a brutally honest advisor about margins, the owner-as-bottleneck trap, and the real growth levers",
                        "career_match": health, "ai_resistance_score": 80})


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
    "Fresher": analyze_fresher,
    "IT Employee": analyze_it,
    "Working Professional": analyze_professional,
    "Career Switcher": analyze_switcher,
    "Laid Off Employee": analyze_laidoff,
    "Manager": analyze_manager,
    "Freelancer": analyze_freelancer,
    "Business Owner": analyze_business,
}


def analyze_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    ut = profile.get("user_type") or "Student"
    engine = ENGINES.get(ut, analyze_professional)
    return engine(profile)
