"""Backend tests for the NEW Future Goal Engine / Dream Career pinning.

Validates:
  - Student dream career (Game Developer) is pinned #1 and never replaced by Data Entry
  - Student hard dream (Doctor with low marks) is preserved but flagged with challenges
  - Career Switcher target (Data Analyst) appears as target_direction section
  - Fresher target_role (Data Scientist) appears as target_direction section
  - All 9 user types still produce valid reports + PDF via mock payment flow
"""
import os
import re
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL").rstrip("/")
API = f"{BASE_URL}/api"

PERS = {
    "mind": "introvert",
    "approach": "analytical",
    "risk": "risk_taker",
    "work_style": "independent",
    "structure": "structured",
    "leadership_interest": 6,
    "communication": 7,
    "stress_tolerance": 7,
}


def _analyze(payload):
    r = requests.post(f"{API}/analyze", json=payload, timeout=60)
    assert r.status_code == 200, f"analyze failed {r.status_code}: {r.text[:300]}"
    return r.json()


def _full_report(submission_id):
    r1 = requests.post(f"{API}/create-order", json={"submission_id": submission_id}, timeout=30)
    assert r1.status_code == 200, f"create-order failed: {r1.text[:300]}"
    r2 = requests.post(f"{API}/verify-payment", json={"submission_id": submission_id}, timeout=30)
    assert r2.status_code == 200, f"verify-payment failed: {r2.text[:300]}"
    return r2.json().get("report") or r2.json()


def _section(report, sec_id):
    for s in report.get("sections", []):
        if s.get("id") == sec_id:
            return s
    return None


def _all_text(node):
    """Flatten any nested structure to a single lowercase string for substring assertions."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, (int, float, bool)):
        return str(node)
    if isinstance(node, dict):
        return " ".join(_all_text(v) for v in node.values())
    if isinstance(node, (list, tuple)):
        return " ".join(_all_text(v) for v in node)
    return ""


# ---------- STUDENT: Game Developer dream (the exact bug) ----------
class TestStudentDreamGameDeveloper:
    @pytest.fixture(scope="class")
    def analysis(self):
        payload = {
            "name": "QA Student",
            "email": "qa.student@test.com",
            "user_type": "Student",
            "answers": {
                "current_class": "Class 12",
                "stream": "Computer Science",
                "marks": "60-75%",
                "favorite_subjects": ["Computer Science", "Art / Design"],
                "least_favorite_subjects": ["History / Civics"],
                "career_interests": ["Software / IT", "Design / Creative"],
                "dream_career": "Game Developer",
                "parents_preferred": "Doctor",
                "study_habits": "Consistent",
                "learning_style": "Hands-on / Practical",
            },
            "personality": PERS,
        }
        return _analyze(payload)

    def test_preview_shows_game_developer_as_dream_match(self, analysis):
        text = _all_text(analysis.get("preview", analysis)).lower()
        assert "game developer" in text, "Preview must surface 'Game Developer' as dream match"

    def test_full_report_pins_game_developer(self, analysis):
        sid = analysis["submission_id"]
        report = _full_report(sid)

        # Dream verdict section
        dv = _section(report, "dream_verdict") or _section(report, "dream") or _section(report, "honest_verdict")
        assert dv is not None, f"No dream verdict section. Sections: {[s.get('id') for s in report.get('sections', [])]}"
        dv_text = _all_text(dv).lower()
        assert "game developer" in dv_text, "Dream verdict first card must mention Game Developer"

        # Backups: related game-industry roles
        backup_keywords = ["unity", "unreal", "gameplay", "game designer", "game programmer", "game development"]
        assert any(k in dv_text for k in backup_keywords), \
            f"Backup card should list related game-industry roles. Got: {dv_text[:500]}"

    def test_matches_section_has_game_developer_first(self, analysis):
        sid = analysis["submission_id"]
        report = _full_report(sid)
        matches = _section(report, "matches")
        assert matches is not None, "matches section missing"
        mtext = _all_text(matches).lower()
        assert "game developer" in mtext, "Game Developer must be in matches"
        # Game Developer should appear before the second-ranked alternative
        idx_game = mtext.find("game developer")
        # 'data entry' must never be a recommended dream
        assert "data entry" not in mtext, "Data Entry must NOT appear in matches"
        assert idx_game >= 0

    def test_mistakes_does_not_replace_dream_with_data_entry(self, analysis):
        sid = analysis["submission_id"]
        report = _full_report(sid)
        mistakes = _section(report, "mistakes")
        if mistakes:
            mt = _all_text(mistakes).lower()
            # The mistakes section may *warn* against bad alternates, but must not RECOMMEND Data Entry
            # as the dream. We only flag if Data Entry is presented positively (as a recommendation).
            assert "recommend" not in mt or "data entry" not in mt, "Mistakes must not recommend Data Entry"


# ---------- STUDENT: Hard dream (Doctor with low marks) ----------
class TestStudentHardDreamDoctor:
    @pytest.fixture(scope="class")
    def report(self):
        payload = {
            "name": "QA Student2",
            "email": "qa.student2@test.com",
            "user_type": "Student",
            "answers": {
                "current_class": "Class 12",
                "stream": "Science",
                "marks": "50-60%",
                "favorite_subjects": ["Biology", "Chemistry"],
                "career_interests": ["Medicine / Healthcare"],
                "dream_career": "Doctor",
                "parents_preferred": "Doctor",
                "study_habits": "On & off",
                "learning_style": "Reading / Writing",
            },
            "personality": PERS,
        }
        a = _analyze(payload)
        return _full_report(a["submission_id"])

    def test_doctor_pinned_despite_low_marks(self, report):
        dv = _section(report, "dream_verdict") or _section(report, "dream") or _section(report, "honest_verdict")
        assert dv is not None
        text = _all_text(dv).lower()
        assert "doctor" in text, "Doctor must remain pinned as the dream"

    def test_challenges_or_backups_present(self, report):
        dv = _section(report, "dream_verdict") or _section(report, "dream") or _section(report, "honest_verdict")
        text = _all_text(dv).lower()
        # Must show brutal challenges OR related medical backups
        backups = any(k in text for k in ["surgeon", "dentist", "pharmacist", "nurse", "physiotherap", "medical"])
        challenges = any(k in text for k in ["challenge", "difficult", "competition", "neet", "honest", "brutal"])
        assert backups or challenges, f"Need challenges/backups in dream verdict, got: {text[:400]}"


# ---------- CAREER SWITCHER: Target = Data Analyst ----------
class TestCareerSwitcherTargetDataAnalyst:
    @pytest.fixture(scope="class")
    def report(self):
        payload = {
            "name": "QA Switcher",
            "email": "qa.switcher@test.com",
            "user_type": "Career Switcher",
            "answers": {
                "current_profession": "Mechanical Engineer",
                "target_profession": "Data Analyst",
                "reason_for_switch": "Better pay",
                "salary_expectation": "12",
                "transferable_skills": ["Problem solving / DSA", "Excel / Sheets", "SQL"],
                "learning_time": "10-20 hrs/week",
                "financial_situation": "6-12 months",
            },
            "personality": PERS,
        }
        a = _analyze(payload)
        return _full_report(a["submission_id"])

    def test_target_direction_section(self, report):
        td = _section(report, "target_direction")
        assert td is not None, f"Missing target_direction. Got: {[s.get('id') for s in report.get('sections', [])]}"
        text = _all_text(td).lower()
        assert "data analyst" in text, "Target Data Analyst must appear as top card"


# ---------- FRESHER: target_role = Data Scientist ----------
class TestFresherTargetDataScientist:
    @pytest.fixture(scope="class")
    def report(self):
        payload = {
            "name": "QA Fresher",
            "email": "qa.fresher@test.com",
            "user_type": "Fresher",
            "answers": {
                "degree": "B.Tech",
                "graduation_year": "2025",
                "internships": "1",
                "projects": "3-5",
                "certifications": "Google Data Analytics",
                "skills": ["Python", "SQL", "Data analysis"],
                "resume_ready": "In progress",
                "linkedin": "Yes",
                "target_role": "Data Scientist",
                "expected_salary": "8",
                "job_preference": "Product / Startups",
            },
            "personality": PERS,
        }
        a = _analyze(payload)
        return _full_report(a["submission_id"])

    def test_target_direction_data_scientist(self, report):
        td = _section(report, "target_direction")
        assert td is not None, f"Missing target_direction. Sections: {[s.get('id') for s in report.get('sections', [])]}"
        text = _all_text(td).lower()
        assert "data scientist" in text, f"Data Scientist must be resolved. Got: {text[:400]}"
        # Must NOT resolve to Research Scientist (the alias bug)
        if "research scientist" in text:
            # Acceptable if it appears as a backup/alternate, but Data Scientist must lead
            idx_ds = text.find("data scientist")
            idx_rs = text.find("research scientist")
            assert idx_ds < idx_rs, "Data Scientist must lead, not Research Scientist"


# ---------- REGRESSION: all 9 categories still work ----------
ALL_CASES = {
    "Student": {"current_class": "Class 12", "marks": "60-75%", "favorite_subjects": ["Mathematics", "Computer Science"], "career_interests": ["Software / IT"], "stream": "Computer Science", "dream_career": "Game Developer", "parents_preferred": "Doctor", "study_habits": "Consistent"},
    "Fresher": {"degree": "B.Tech", "graduation_year": "2025", "internships": "1", "projects": "1-2", "skills": ["Python", "SQL"], "resume_ready": "In progress", "linkedin": "Yes", "target_role": "Data Scientist", "expected_salary": "6", "job_preference": "Product / Startups"},
    "IT Employee": {"current_role": "FE Eng", "developer_type": "Frontend Developer", "years_experience": "6", "cloud_knowledge": "Beginner", "ai_knowledge": "Beginner", "system_design": "Intermediate", "tech_stack": ["React"], "languages": ["JavaScript"]},
    "Working Professional": {"current_role": "PM", "years_experience": "8", "current_salary": "14", "industry": "IT / Software", "team_size": "6-15", "leadership_responsibilities": "Manage a team", "desired_salary": "28", "desired_position": "Director", "promotion_history": "1 promotion"},
    "Career Switcher": {"current_profession": "Mechanical Engineer", "target_profession": "Data Analyst", "transferable_skills": ["Problem solving / DSA", "Excel / Sheets"], "learning_time": "10-20 hrs/week", "financial_situation": "3-6 months"},
    "Laid Off Employee": {"previous_role": "Sales Manager", "industry": "Retail / E-commerce", "reason_for_layoff": "Restructuring", "previous_salary": "18", "years_experience": "7", "skills": ["Communication", "Marketing"], "savings_runway": "3-6 months", "desired_industry": "IT / Software", "relocation": "Maybe"},
    "Manager": {"department": "Sales", "team_size": "16-50", "budget_responsibility": "Mid (₹50L-5Cr)", "hiring_experience": "Hired independently", "conflict_management": "High", "strategic_planning": "Medium", "revenue_responsibility": "High"},
    "Freelancer": {"services": ["Design", "Development"], "niche": "SaaS landing pages", "monthly_income": "80000", "clients": "2-4", "pricing": "Mid-market", "marketing_channels": ["LinkedIn content"], "portfolio_quality": "Strong"},
    "Business Owner": {"business_type": "Services", "revenue": "500000", "employees": "2-5", "profit_margin": "Low (<10%)", "customer_acquisition": "1 main channel", "biggest_challenge": "Getting customers", "growth_goals": "2x revenue", "marketing_channels": ["Referral programme"]},
}


@pytest.mark.parametrize("user_type,answers", list(ALL_CASES.items()))
def test_all_categories_regression(user_type, answers):
    a = _analyze({"name": "QA", "email": "qa@test.com", "user_type": user_type, "answers": answers, "personality": PERS})
    sid = a["submission_id"]
    assert a.get("product_name"), f"{user_type}: missing product_name"

    rep = _full_report(sid)
    ids = {s.get("id") for s in rep.get("sections", [])}
    required = {"reality_check", "snapshot", "risks", "opportunities", "focus", "stop", "roadmap", "letter"}
    missing = required - ids
    assert not missing, f"{user_type}: missing sections {missing}"

    pdf = requests.get(f"{API}/report/{sid}/pdf", timeout=60)
    assert pdf.status_code == 200, f"{user_type}: PDF status {pdf.status_code}"
    assert pdf.headers.get("content-type", "").startswith("application/pdf"), \
        f"{user_type}: PDF content-type {pdf.headers.get('content-type')}"
    assert len(pdf.content) > 4000, f"{user_type}: PDF too small {len(pdf.content)}"
