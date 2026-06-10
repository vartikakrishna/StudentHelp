"""End-to-end HTTP tests against REACT_APP_BACKEND_URL covering the 3 flagship
flows (Student ₹199, IT Employee ₹499, Working Professional ₹499) plus the
6 regression categories. Each test: analyze -> create-order (mock) -> verify-payment ->
download PDF, and asserts the V2 premium sections in the unlocked report.
"""
import os
import sys
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://career-blueprint-ai.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

PERS = {"mind": "introvert", "approach": "analytical", "risk": "risk_taker",
        "work_style": "independent", "structure": "structured",
        "leadership_interest": 6, "communication": 7, "stress_tolerance": 7}


def _txt(node):
    if node is None: return ""
    if isinstance(node, str): return node
    if isinstance(node, (int, float, bool)): return str(node)
    if isinstance(node, dict): return " ".join(_txt(v) for v in node.values())
    if isinstance(node, (list, tuple)): return " ".join(_txt(v) for v in node)
    return ""


@pytest.fixture(scope="module")
def s():
    sess = requests.Session()
    sess.headers["Content-Type"] = "application/json"
    return sess


def _funnel(s, user_type, answers, name="TEST_QA"):
    r = s.post(f"{API}/analyze", json={"name": name, "email": "qa@test.com", "phone": "9999999999",
                                       "country": "India", "user_type": user_type,
                                       "answers": answers, "personality": PERS}, timeout=60)
    assert r.status_code == 200, r.text
    sub_id = r.json()["submission_id"]
    plan_price = r.json()["price"]

    r2 = s.post(f"{API}/create-order", json={"submission_id": sub_id}, timeout=30)
    assert r2.status_code == 200, r2.text
    assert r2.json()["mode"] == "mock"

    r3 = s.post(f"{API}/verify-payment", json={"submission_id": sub_id}, timeout=60)
    assert r3.status_code == 200, r3.text
    body = r3.json()
    assert body["success"] is True
    assert "report" in body and "sections" in body["report"]

    pdf = s.get(f"{API}/report/{sub_id}/pdf", timeout=60)
    assert pdf.status_code == 200
    assert "application/pdf" in pdf.headers.get("content-type", "")
    assert len(pdf.content) > 4000, f"PDF too small: {len(pdf.content)} bytes"
    return body["report"], plan_price, sub_id


def _ids(rep):
    return {s["id"] for s in rep["sections"]}


def _sec(rep, sid):
    return next((x for x in rep["sections"] if x["id"] == sid), None)


# ---------------- Health ----------------
def test_health(s):
    r = s.get(f"{API}/", timeout=15)
    assert r.status_code == 200
    j = r.json()
    assert j.get("payment_mode") == "mock"
    assert "MapMyCareer" in j.get("message", "")


# ---------------- Student V2 ₹199 ----------------
def test_student_v2_funnel(s):
    rep, price, _ = _funnel(s, "Student", {
        "marks": "60-75%", "favorite_subjects": ["Computer Science", "Art / Design"],
        "career_interests": ["Software / IT", "Design / Creative"],
        "dream_career": "Game Developer", "parents_preferred": "Doctor",
        "study_discipline": "Medium", "learning_style": "Visual",
        "financial_expectations": "High", "desired_lifestyle": "Balanced",
        "technology_interest": 8, "creativity_level": 8})
    assert price == 199
    ids = _ids(rep)
    for need in ["dream_scores", "dream_verdict", "recommendations", "degrees",
                 "blueprint", "growth", "action_30", "action_90", "letter"]:
        assert need in ids, f"Student missing {need}"
    rec = _sec(rep, "recommendations")
    assert rec["items"][0]["title"] == "Game Developer"
    assert rec["items"][0].get("pros") and rec["items"][0].get("cons")
    assert "data entry" not in _txt(rep["sections"]).lower()
    bp = _sec(rep, "blueprint")
    assert len(bp["items"]) == 4 and all(p.get("groups") for p in bp["items"])


# ---------------- IT Employee V2 ₹499 ----------------
def test_it_employee_v2_funnel(s):
    rep, price, _ = _funnel(s, "IT Employee", {
        "developer_type": "Frontend Developer", "years_experience": "5",
        "cloud_knowledge": "Beginner", "ai_knowledge": "Beginner",
        "system_design": "Intermediate", "tech_stack": ["React"],
        "languages": ["JavaScript"], "future_goal": "AI Engineer",
        "team_size": "1-5", "leadership_experience": "No",
        "desired_salary": "30"})
    assert price == 499
    ids = _ids(rep)
    for need in ["snapshot", "ai_risk", "skill_gap", "system_design",
                 "future_tracks", "salary", "promotion", "learning_plan", "letter"]:
        assert need in ids, f"IT missing {need}"
    sd = _sec(rep, "system_design")
    assert len(sd["items"]) == 4
    sd_text = _txt(sd).lower()
    for kw in ["caching", "cap theorem", "url shortener", "kafka", "observability"]:
        assert kw in sd_text, f"system_design missing keyword {kw}"
    ft = _sec(rep, "future_tracks")
    assert len(ft["items"]) >= 4
    assert all(t.get("pros") and t.get("cons") for t in ft["items"])


# ---------------- Working Professional V2 ₹499 ----------------
def test_pro_v2_funnel(s):
    rep, price, _ = _funnel(s, "Working Professional", {
        "current_role": "Senior Engineer", "industry": "IT / Software",
        "years_experience": "8", "current_salary": "14",
        "desired_position": "Product Manager",
        "promotion_history": "1 promotion",
        "leadership_responsibilities": "Lead a small team"})
    assert price == 499
    ids = _ids(rep)
    for need in ["snapshot", "future_options", "skill_gap", "salary",
                 "growth_90", "growth_year", "letter"]:
        assert need in ids, f"Pro missing {need}"
    fo = _sec(rep, "future_options")
    assert fo["items"][0]["title"] == "Product Manager"
    assert fo["items"][0].get("pros") and fo["items"][0].get("cons")


# ---------------- Regression: remaining 6 categories ----------------
REG_CASES = {
    "Fresher": {"skills": ["Python", "SQL"], "resume_ready": "In progress",
                "linkedin": "Yes", "target_role": "Data Scientist",
                "expected_salary": "6"},
    "Career Switcher": {"current_profession": "Mechanical Engineer",
                        "target_profession": "Data Analyst",
                        "transferable_skills": ["Excel / Sheets"],
                        "learning_time": "10-20 hrs/week",
                        "financial_situation": "3-6 months"},
    "Laid Off Employee": {"previous_role": "Sales Manager",
                          "industry": "Retail / E-commerce",
                          "previous_salary": "18", "years_experience": "7",
                          "skills": ["Communication"], "savings_runway": "3-6 months"},
    "Manager": {"department": "Sales", "team_size": "16-50",
                "conflict_management": "High", "strategic_planning": "Medium"},
    "Freelancer": {"services": ["Design"], "monthly_income": "80000",
                   "clients": "2-4", "pricing": "Mid-market",
                   "portfolio_quality": "Strong"},
    "Business Owner": {"business_type": "Services", "revenue": "500000",
                       "employees": "2-5", "profit_margin": "Low (<10%)",
                       "biggest_challenge": "Getting customers",
                       "growth_goals": "2x revenue"},
}


@pytest.mark.parametrize("ut,answers", list(REG_CASES.items()))
def test_regression_categories(s, ut, answers):
    rep, _, _ = _funnel(s, ut, answers)
    assert any(x["id"] == "letter" for x in rep["sections"])
    assert len(rep["sections"]) >= 6
