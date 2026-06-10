"""Direct unit tests for MapMyCareer V2 engines + PDF (no HTTP / no payment).

Covers: 300+ career DB, dream-career pinning (Honesty Rule), the V2 premium
sections (recommendations, learning blueprint, system-design roadmap, degree cards),
the Future-Goal/Direction engine, and PDF generation for all 9 categories.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import career_db
from type_engines import analyze_profile
from pdf_generator import build_pdf

PERS = {"mind": "introvert", "approach": "analytical", "risk": "risk_taker", "work_style": "independent",
        "structure": "structured", "leadership_interest": 6, "communication": 7, "stress_tolerance": 7}


def _text(node):
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, (int, float, bool)):
        return str(node)
    if isinstance(node, dict):
        return " ".join(_text(v) for v in node.values())
    if isinstance(node, (list, tuple)):
        return " ".join(_text(v) for v in node)
    return ""


def _sec(rep, sid):
    return next((s for s in rep["sections"] if s["id"] == sid), None)


# ---------------- Career DB ----------------
def test_career_db_has_300_plus():
    assert len(career_db.CAREERS) >= 300
    assert len(career_db.CAREER_BY_KEY) == len(career_db.CAREERS)  # no dup keys


@pytest.mark.parametrize("q,expect", [
    ("Game Developer", "Game Developer"), ("Data Scientist", "Data Scientist"),
    ("Data Analyst", "Data Analyst"), ("Mechanical Engineer", "Mechanical Engineer"),
    ("Civil Engineer", "Civil Engineer"), ("Solutions Architect", "Cloud Architect"),
    ("Dermatologist", "Dermatologist"),
])
def test_resolver(q, expect):
    c, _ = career_db.resolve_career(q)
    assert c and c["title"] == expect


# ---------------- Student V2 ----------------
@pytest.fixture(scope="module")
def student():
    return analyze_profile({"name": "QA", "user_type": "Student", "answers": {
        "marks": "60-75%", "favorite_subjects": ["Computer Science", "Art / Design"],
        "career_interests": ["Software / IT", "Design / Creative"],
        "dream_career": "Game Developer", "parents_preferred": "Doctor"}, "personality": PERS})


def test_student_v2_sections(student):
    ids = {s["id"] for s in student["sections"]}
    for need in {"reality_check", "dream_scores", "dream_verdict", "recommendations", "degrees", "blueprint", "growth", "action_30", "action_90", "letter"}:
        assert need in ids, f"missing {need}"


def test_student_dream_pinned_no_data_entry(student):
    assert student["dream_match_score"] >= 60
    rec = _sec(student, "recommendations")
    assert rec["items"][0]["title"] == "Game Developer"
    assert "data entry" not in _text(student["sections"]).lower()
    dv = _text(_sec(student, "dream_verdict")).lower()
    assert any(k in dv for k in ["unity", "unreal", "gameplay", "game designer"])


def test_student_recommendations_have_pros_cons(student):
    for item in _sec(student, "recommendations")["items"]:
        assert item["pros"] and item["cons"]


def test_student_blueprint_four_years(student):
    bp = _sec(student, "blueprint")
    assert len(bp["items"]) == 4
    assert all(p.get("groups") for p in bp["items"])


def test_student_hard_dream_doctor_pinned():
    r = analyze_profile({"name": "QA", "user_type": "Student", "answers": {
        "marks": "50-60%", "favorite_subjects": ["Biology"], "career_interests": ["Medicine / Healthcare"],
        "dream_career": "Doctor"}, "personality": PERS})
    rec = _sec(r, "recommendations")
    assert "doctor" in rec["items"][0]["title"].lower()


# ---------------- IT V2 ----------------
@pytest.fixture(scope="module")
def it_emp():
    return analyze_profile({"name": "QA", "user_type": "IT Employee", "answers": {
        "developer_type": "Frontend Developer", "years_experience": "5", "cloud_knowledge": "Beginner",
        "ai_knowledge": "Beginner", "system_design": "Intermediate", "tech_stack": ["React"],
        "languages": ["JavaScript"], "future_goal": "AI Engineer"}, "personality": PERS})


def test_it_v2_sections(it_emp):
    ids = {s["id"] for s in it_emp["sections"]}
    for need in {"reality_check", "snapshot", "ai_risk", "skill_gap", "system_design", "future_tracks", "salary", "promotion", "learning_plan", "letter"}:
        assert need in ids, f"missing {need}"


def test_it_system_design_mandatory_l1_l4(it_emp):
    sd = _sec(it_emp, "system_design")
    phases = [p["phase"] for p in sd["items"]]
    assert len(phases) == 4
    txt = _text(sd).lower()
    for kw in ["caching", "cap theorem", "url shortener", "kafka", "observability"]:
        assert kw in txt, f"system design missing {kw}"


def test_it_future_tracks_recommendations(it_emp):
    ft = _sec(it_emp, "future_tracks")
    assert ft and len(ft["items"]) >= 4
    assert all(t["pros"] and t["cons"] for t in ft["items"])


# ---------------- Working Professional V2 ----------------
@pytest.fixture(scope="module")
def professional():
    return analyze_profile({"name": "QA", "user_type": "Working Professional", "answers": {
        "current_role": "Engineer", "industry": "IT / Software", "years_experience": "8",
        "current_salary": "14", "desired_position": "Product Manager",
        "promotion_history": "1 promotion", "leadership_responsibilities": "Lead a small team"}, "personality": PERS})


def test_pro_v2_sections(professional):
    ids = {s["id"] for s in professional["sections"]}
    for need in {"reality_check", "snapshot", "future_options", "skill_gap", "salary", "growth_90", "growth_year", "letter"}:
        assert need in ids, f"missing {need}"


def test_pro_future_options_resolved(professional):
    fo = _sec(professional, "future_options")
    assert fo["items"][0]["title"] == "Product Manager"


# ---------------- All 9 categories + PDF ----------------
ALL_CASES = {
    "Student": {"marks": "60-75%", "favorite_subjects": ["Mathematics", "Computer Science"], "career_interests": ["Software / IT"], "dream_career": "Game Developer", "parents_preferred": "Doctor"},
    "Fresher": {"skills": ["Python", "SQL"], "resume_ready": "In progress", "linkedin": "Yes", "target_role": "Data Scientist", "expected_salary": "6"},
    "IT Employee": {"developer_type": "Frontend Developer", "years_experience": "6", "cloud_knowledge": "Beginner", "ai_knowledge": "Beginner", "system_design": "Intermediate", "tech_stack": ["React"]},
    "Working Professional": {"current_role": "PM", "years_experience": "8", "current_salary": "14", "industry": "IT / Software", "desired_position": "Director", "promotion_history": "1 promotion"},
    "Career Switcher": {"current_profession": "Mechanical Engineer", "target_profession": "Data Analyst", "transferable_skills": ["Excel / Sheets"], "learning_time": "10-20 hrs/week", "financial_situation": "3-6 months"},
    "Laid Off Employee": {"previous_role": "Sales Manager", "industry": "Retail / E-commerce", "previous_salary": "18", "years_experience": "7", "skills": ["Communication"], "savings_runway": "3-6 months"},
    "Manager": {"department": "Sales", "team_size": "16-50", "conflict_management": "High", "strategic_planning": "Medium"},
    "Freelancer": {"services": ["Design"], "monthly_income": "80000", "clients": "2-4", "pricing": "Mid-market", "portfolio_quality": "Strong"},
    "Business Owner": {"business_type": "Services", "revenue": "500000", "employees": "2-5", "profit_margin": "Low (<10%)", "biggest_challenge": "Getting customers", "growth_goals": "2x revenue"},
}


@pytest.mark.parametrize("ut,answers", list(ALL_CASES.items()))
def test_all_categories_report_and_pdf(ut, answers):
    rep = analyze_profile({"name": "QA", "user_type": ut, "answers": answers, "personality": PERS})
    assert rep.get("product_name")
    assert len(rep["sections"]) >= 6
    assert any(s["id"] == "letter" for s in rep["sections"])
    pdf = build_pdf({"report": rep, "user_data": {"name": "QA"}})
    assert isinstance(pdf, (bytes, bytearray)) and len(pdf) > 4000


def test_product_names_distinct():
    names = {ut: analyze_profile({"name": "QA", "user_type": ut, "answers": a, "personality": PERS})["product_name"]
             for ut, a in ALL_CASES.items()}
    # at least the 3 V2 flagship products are distinct
    assert names["Student"] != names["IT Employee"] != names["Working Professional"]
