"""Backend API tests for Career Blueprint AI (expanded honesty engine)."""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL").rstrip("/")
API = f"{BASE_URL}/api"


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


def _student_payload():
    return {
        "name": "TEST_Aarav Sharma",
        "email": "test_aarav@example.com",
        "phone": "9999999999",
        "age": "19",
        "gender": "Male",
        "country": "India",
        "state": "MH",
        "user_type": "Student",
        "education": "Class 12",
        "current_degree": "B.Tech CSE",
        "graduation_year": "2027",
        "interests": {
            "technology": 9, "business": 6, "finance": 6, "sales": 3,
            "marketing": 4, "design": 5, "writing": 4, "teaching": 3,
            "research": 7, "psychology": 4, "healthcare": 2, "law": 2,
            "content_creation": 7, "entrepreneurship": 6, "leadership": 8,
            "problem_solving": 9,
        },
        "personality": {
            "mind": "introvert", "approach": "analytical", "risk": "stable",
            "role": "specialist", "work_style": "independent",
            "stress_tolerance": 6, "work_life": 6, "communication": 6, "public_speaking": 5,
        },
        "goals": {
            "priorities": ["High Income", "Creativity"],
            "dream_income_30": "30L+", "dream_income_40": "50L+",
            "challenge": "Don't know what I'm good at",
        },
    }


def _laidoff_payload():
    p = _student_payload()
    p.update({
        "name": "TEST_Priya Laidoff", "email": "test_priya@example.com",
        "user_type": "Laid Off Employee", "age": "31",
        "current_profession": "Software Tester", "current_salary": "8",
        "expected_salary": "18",
        "job_title": "Manual QA", "years_experience": "6",
        "industry": "IT Services", "previous_salary": "8",
        "reason_for_layoff": "Cost cutting / automation",
        "skills": "manual testing, jira, sql, postman",
        "certifications": "ISTQB",
        "desired_industry": "Tech / SaaS", "remote_preference": "Remote",
    })
    return p


# --- Root ---
def test_root(session):
    r = session.get(f"{API}/")
    assert r.status_code == 200
    data = r.json()
    assert data["payment_mode"] in ("mock", "live")


# --- Regret calculator ---
class TestRegret:
    def test_regret_basic(self, session):
        r = session.post(f"{API}/regret", json={"age": "22", "current_salary": "5", "dream_salary": "30"})
        assert r.status_code == 200
        d = r.json()
        for k in ("opportunity_cost", "years", "yearly_gap"):
            assert k in d
        assert d["opportunity_cost"] > 0
        assert 10 <= d["years"] <= 30

    def test_regret_handles_empty(self, session):
        r = session.post(f"{API}/regret", json={"age": "", "current_salary": "", "dream_salary": ""})
        assert r.status_code == 200
        assert r.json()["opportunity_cost"] >= 0


# --- Analyze: Student path ---
class TestAnalyzeStudent:
    def test_analyze_student(self, session):
        r = session.post(f"{API}/analyze", json=_student_payload())
        assert r.status_code == 200, r.text
        data = r.json()
        assert "submission_id" in data and isinstance(data["submission_id"], str)
        assert data["price"] == 199
        prev = data["preview"]
        # Honesty fields
        for k in ("success_score", "ai_resistance_score", "portfolio_ai_risk",
                  "ai_risk_label", "top_matches", "career_reality_check",
                  "strength", "weakness", "hidden_talent", "trait_labels",
                  "ai_threat_examples", "locked"):
            assert k in prev, f"preview missing key: {k}"
        assert len(prev["top_matches"]) == 3
        for m in prev["top_matches"]:
            for k in ("title", "score", "tagline", "ai_risk", "ai_risk_label",
                      "ai_resistance", "market_demand", "salary_mid", "verdict",
                      "explanation"):
                assert k in m, f"match missing key: {k}"
        # Locked counts include careers_to_avoid_count
        assert prev["locked"]["careers_to_avoid_count"] >= 3
        pytest.shared_student_id = data["submission_id"]

    def test_analyze_missing_required(self, session):
        r = session.post(f"{API}/analyze", json={"name": "x"})
        assert r.status_code == 422


# --- Order ---
class TestOrder:
    def test_create_order_mock(self, session):
        sub_id = pytest.shared_student_id
        r = session.post(f"{API}/create-order", json={"submission_id": sub_id})
        assert r.status_code == 200
        d = r.json()
        assert d["mode"] in ("mock", "live")
        assert d["amount"] == 19900
        assert d["currency"] == "INR"
        assert d["order_id"].startswith("order_")

    def test_create_order_not_found(self, session):
        r = session.post(f"{API}/create-order", json={"submission_id": "nonexistent"})
        assert r.status_code == 404


# --- Report + Payment unlock (Student) ---
class TestReportAndPayment:
    def test_unpaid_preview(self, session):
        sub_id = pytest.shared_student_id
        r = session.get(f"{API}/report/{sub_id}")
        assert r.status_code == 200
        d = r.json()
        assert d["paid"] is False
        assert "preview" in d

    def test_pdf_402_before_pay(self, session):
        sub_id = pytest.shared_student_id
        r = session.get(f"{API}/report/{sub_id}/pdf")
        assert r.status_code == 402

    def test_verify_payment_unlocks_full(self, session):
        sub_id = pytest.shared_student_id
        r = session.post(f"{API}/verify-payment", json={"submission_id": sub_id})
        assert r.status_code == 200
        d = r.json()
        assert d["success"] is True
        assert d["payment_id"].startswith("pay_mock_")
        rep = d["report"]
        # Required keys per problem statement
        required = ["matches", "careers_to_avoid", "ai_threat_examples",
                    "learning_plans", "career_switch", "regret"]
        for k in required:
            assert k in rep, f"full report missing: {k}"
        assert len(rep["matches"]) >= 5
        # Each match has the honesty bars
        for m in rep["matches"]:
            for k in ("market_demand", "salary_score", "competition", "ai_risk",
                      "ai_risk_label", "difficulty", "time_to_enter"):
                assert k in m
        # careers_to_avoid sanity
        assert len(rep["careers_to_avoid"]) >= 3
        for c in rep["careers_to_avoid"]:
            assert "why" in c and isinstance(c["why"], list) and len(c["why"]) >= 1
        # career switch & learning plans
        assert len(rep["learning_plans"]) == 4
        assert "targets" in rep["career_switch"]
        # regret block
        assert rep["regret"]["opportunity_cost"] > 0
        # Student should NOT have layoff/it_report
        assert "layoff" not in rep, "Student profile must not include layoff section"

    def test_paid_pdf(self, session):
        sub_id = pytest.shared_student_id
        r = session.get(f"{API}/report/{sub_id}/pdf")
        assert r.status_code == 200
        assert r.headers.get("content-type", "").startswith("application/pdf")
        assert r.content[:4] == b"%PDF"
        assert len(r.content) > 5000


# --- Laid-Off path: must contain layoff + it_report ---
class TestLaidOff:
    def test_analyze_laidoff(self, session):
        r = session.post(f"{API}/analyze", json=_laidoff_payload())
        assert r.status_code == 200, r.text
        data = r.json()
        pytest.shared_laidoff_id = data["submission_id"]
        prev = data["preview"]
        assert prev["user_type"] == "Laid Off Employee"

    def test_laidoff_full_report_has_layoff_and_it(self, session):
        sub_id = pytest.shared_laidoff_id
        r = session.post(f"{API}/verify-payment", json={"submission_id": sub_id})
        assert r.status_code == 200
        rep = r.json()["report"]
        assert "layoff" in rep, "Laid-Off report missing 'layoff' section"
        for k in ("layoff_risk_score", "recovery_score", "employability_score",
                  "salary_recovery_potential", "recovery_roadmap"):
            assert k in rep["layoff"]
        # IT report should also be present because industry contains 'IT'/Tech
        assert "it_report" in rep, "IT-flavoured layoff report should include it_report"


# --- Errors ---
def test_verify_not_found(session):
    r = session.post(f"{API}/verify-payment", json={"submission_id": "missing"})
    assert r.status_code == 404


def test_report_not_found(session):
    r = session.get(f"{API}/report/missing-id")
    assert r.status_code == 404
