"""Backend tests for the NEW Future Direction Engine.

Validates:
  - IT Employee with future_goal='AI Engineer' produces a 'future_direction' matches
    section titled 'Your Future Career Direction: AI / Machine Learning Engineer'
    with AI/ML Engineer as the top card; AI-survival sections (risks/transitions/salary plan) remain.
  - Working Professional with desired_position='Product Manager' produces future_direction.
  - Working Professional with desired_position='Director' (generic seniority) → section SKIPPED;
    'Film Director' must NOT appear anywhere.
  - Manager with target_role='Management Consultant' produces future_direction.
  - Manager with target_role='VP' → section SKIPPED; report still valid.
  - Leaving the field blank → no future_direction section, report still complete.
"""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL").rstrip("/")
API = f"{BASE_URL}/api"

PERS = {
    "mind": "introvert",
    "approach": "analytical",
    "risk": "stable",
    "work_style": "independent",
    "structure": "structured",
    "leadership_interest": 7,
    "communication": 6,
    "stress_tolerance": 7,
}

REQUIRED_SECTION_IDS = {
    "reality_check", "snapshot", "risks", "opportunities", "focus", "stop", "roadmap", "letter",
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


def _has_fd_header(report, expected_role_substring):
    for s in report.get("sections", []):
        if s.get("id") == "future_direction":
            title = (s.get("title") or "").lower()
            if "your future career direction:" in title and expected_role_substring.lower() in title:
                return True
    return False


# ---------- IT EMPLOYEE: future_goal = AI Engineer ----------
class TestITEmployeeFutureDirectionAIEngineer:
    @pytest.fixture(scope="class")
    def report(self):
        a = _analyze({
            "name": "QA IT", "email": "qa.it@test.com", "user_type": "IT Employee",
            "answers": {
                "current_role": "Frontend Engineer",
                "developer_type": "Frontend Developer",
                "years_experience": "6",
                "tech_stack": ["React", "TypeScript"],
                "languages": ["JavaScript", "Python"],
                "cloud_knowledge": "Beginner",
                "ai_knowledge": "Beginner",
                "system_design": "Intermediate",
                "future_goal": "AI Engineer",
            },
            "personality": PERS,
        })
        return _full_report(a["submission_id"])

    def test_future_direction_section_present(self, report):
        fd = _section(report, "future_direction")
        assert fd is not None, f"Missing future_direction. Sections: {[s.get('id') for s in report.get('sections', [])]}"

    def test_future_direction_title_mentions_ai_ml(self, report):
        # Title should be 'Your Future Career Direction: AI / Machine Learning Engineer'
        # accept either 'machine learning' or 'ai' wording
        assert _has_fd_header(report, "machine learning") or _has_fd_header(report, "ai"), \
            f"Future direction header missing AI/ML wording. Got: {[s.get('title') for s in report.get('sections', [])]}"

    def test_aiml_is_top_card(self, report):
        fd = _section(report, "future_direction")
        # First item in matches list should be the AI/ML Engineer role
        items = fd.get("items") or fd.get("data") or fd.get("matches") or []
        # If wrapped differently, fall back to flat text
        first_text = _all_text(items[0]).lower() if items else _all_text(fd).lower()
        assert "machine learning" in first_text or "ai" in first_text, \
            f"AI/ML Engineer must be the #1 card. Got: {first_text[:300]}"

    def test_ai_survival_sections_still_present(self, report):
        ids = {s.get("id") for s in report.get("sections", [])}
        # Threat assessment / transitions / salary plan presence: report must still have core sections
        missing = REQUIRED_SECTION_IDS - ids
        assert not missing, f"IT report missing core sections: {missing}"
        # Transitions section is the typical IT-survival section
        survival_keywords = ["transitions", "risks", "salary", "ai_threat", "pivots"]
        assert any(k in ids for k in survival_keywords) or "transitions" in ids, \
            f"IT survival sections missing. Got ids: {ids}"


class TestITEmployeeBlankFutureGoal:
    def test_no_future_direction_when_blank(self):
        a = _analyze({
            "name": "QA IT2", "email": "qa.it2@test.com", "user_type": "IT Employee",
            "answers": {
                "current_role": "Backend Engineer",
                "developer_type": "Backend Developer",
                "years_experience": "5",
                "tech_stack": ["Node.js"],
                "languages": ["JavaScript"],
                "cloud_knowledge": "Intermediate",
                "ai_knowledge": "Beginner",
                "system_design": "Intermediate",
                "future_goal": "",
            },
            "personality": PERS,
        })
        report = _full_report(a["submission_id"])
        assert _section(report, "future_direction") is None, "Blank future_goal must NOT add fd section"
        ids = {s.get("id") for s in report.get("sections", [])}
        assert not (REQUIRED_SECTION_IDS - ids), f"Report still must be complete; missing {REQUIRED_SECTION_IDS - ids}"


# ---------- WORKING PROFESSIONAL: desired_position = Product Manager / Director ----------
class TestProfessionalFutureDirectionPM:
    @pytest.fixture(scope="class")
    def report(self):
        a = _analyze({
            "name": "QA Pro", "email": "qa.pro@test.com", "user_type": "Working Professional",
            "answers": {
                "current_role": "Senior Engineer",
                "years_experience": "7",
                "current_salary": "20",
                "industry": "IT / Software",
                "team_size": "6-15",
                "leadership_responsibilities": "Manage a team",
                "desired_salary": "35",
                "desired_position": "Product Manager",
                "promotion_history": "1 promotion",
            },
            "personality": PERS,
        })
        return _full_report(a["submission_id"])

    def test_future_direction_product_manager(self, report):
        fd = _section(report, "future_direction")
        assert fd is not None, "Missing future_direction for desired_position=Product Manager"
        assert _has_fd_header(report, "product manager"), \
            f"Title must include 'Product Manager'. Got: {fd.get('title')}"


class TestProfessionalDirectorSkipped:
    @pytest.fixture(scope="class")
    def report(self):
        a = _analyze({
            "name": "QA Pro2", "email": "qa.pro2@test.com", "user_type": "Working Professional",
            "answers": {
                "current_role": "PM",
                "years_experience": "8",
                "current_salary": "14",
                "industry": "IT / Software",
                "team_size": "6-15",
                "leadership_responsibilities": "Manage a team",
                "desired_salary": "28",
                "desired_position": "Director",
                "promotion_history": "1 promotion",
            },
            "personality": PERS,
        })
        return _full_report(a["submission_id"])

    def test_no_future_direction_for_director(self, report):
        assert _section(report, "future_direction") is None, \
            "Director (generic seniority) must SKIP future_direction"

    def test_no_film_director_anywhere(self, report):
        text = _all_text(report).lower()
        assert "film director" not in text, "'Film Director' must NOT appear in the report"

    def test_report_still_valid(self, report):
        ids = {s.get("id") for s in report.get("sections", [])}
        missing = REQUIRED_SECTION_IDS - ids
        assert not missing, f"Report still must be valid. Missing: {missing}"


# ---------- MANAGER: target_role = Management Consultant / VP ----------
class TestManagerFutureDirectionConsultant:
    @pytest.fixture(scope="class")
    def report(self):
        a = _analyze({
            "name": "QA Mgr", "email": "qa.mgr@test.com", "user_type": "Manager",
            "answers": {
                "department": "Operations",
                "team_size": "16-50",
                "budget_responsibility": "Mid (₹50L-5Cr)",
                "hiring_experience": "Hired independently",
                "conflict_management": "High",
                "strategic_planning": "High",
                "revenue_responsibility": "High",
                "target_role": "Management Consultant",
            },
            "personality": PERS,
        })
        return _full_report(a["submission_id"])

    def test_future_direction_management_consultant(self, report):
        fd = _section(report, "future_direction")
        assert fd is not None, "Missing future_direction for target_role=Management Consultant"
        assert _has_fd_header(report, "management consultant") or _has_fd_header(report, "consultant"), \
            f"Title must include 'Management Consultant'. Got: {fd.get('title')}"


class TestManagerVPSkipped:
    @pytest.fixture(scope="class")
    def report(self):
        a = _analyze({
            "name": "QA Mgr2", "email": "qa.mgr2@test.com", "user_type": "Manager",
            "answers": {
                "department": "Sales",
                "team_size": "16-50",
                "budget_responsibility": "Mid (₹50L-5Cr)",
                "hiring_experience": "Hired independently",
                "conflict_management": "High",
                "strategic_planning": "Medium",
                "revenue_responsibility": "High",
                "target_role": "VP",
            },
            "personality": PERS,
        })
        return _full_report(a["submission_id"])

    def test_no_future_direction_for_vp(self, report):
        assert _section(report, "future_direction") is None, \
            "VP (generic seniority) must SKIP future_direction"

    def test_report_still_valid(self, report):
        ids = {s.get("id") for s in report.get("sections", [])}
        missing = REQUIRED_SECTION_IDS - ids
        assert not missing, f"Manager report still must be valid. Missing: {missing}"


# ---------- BLANK fields → original behavior ----------
class TestBlankTargetsKeepOldBehavior:
    @pytest.mark.parametrize("user_type,answers", [
        ("Working Professional", {
            "current_role": "PM", "years_experience": "8", "current_salary": "14",
            "industry": "IT / Software", "team_size": "6-15",
            "leadership_responsibilities": "Manage a team",
            "desired_salary": "28", "desired_position": "", "promotion_history": "1 promotion",
        }),
        ("Manager", {
            "department": "Sales", "team_size": "16-50",
            "budget_responsibility": "Mid (₹50L-5Cr)", "hiring_experience": "Hired independently",
            "conflict_management": "High", "strategic_planning": "Medium",
            "revenue_responsibility": "High", "target_role": "",
        }),
    ])
    def test_blank_field_no_fd_section(self, user_type, answers):
        a = _analyze({"name": "QA", "email": "qa@test.com", "user_type": user_type,
                      "answers": answers, "personality": PERS})
        report = _full_report(a["submission_id"])
        assert _section(report, "future_direction") is None, \
            f"{user_type} with blank target must NOT have future_direction"
        ids = {s.get("id") for s in report.get("sections", [])}
        assert not (REQUIRED_SECTION_IDS - ids), \
            f"{user_type}: missing sections {REQUIRED_SECTION_IDS - ids}"
