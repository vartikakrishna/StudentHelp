"""Backend API tests for Career Blueprint AI."""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://career-blueprint-ai.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="module")
def sample_payload():
    return {
        "name": "TEST_Aarav Sharma",
        "email": "test_aarav@example.com",
        "phone": "9999999999",
        "age": "19",
        "gender": "Male",
        "education": "Class 12",
        "stream": "Science (PCM)",
        "interests": {
            "technology": 9, "business": 6, "design": 5, "psychology": 4,
            "teaching": 3, "healthcare": 2, "finance": 6, "content_creation": 7,
            "law": 2, "leadership": 8,
        },
        "personality": {
            "mind": "introvert", "approach": "analytical",
            "risk": "stable", "role": "specialist",
        },
        "goals": {
            "priorities": ["High Income", "Creativity"],
            "dream_income": "30L+",
            "challenge": "Don't know what I'm good at",
        },
    }


# --- Health / Root ---
def test_root(session):
    r = session.get(f"{API}/")
    assert r.status_code == 200
    data = r.json()
    assert "payment_mode" in data
    assert data["payment_mode"] in ("mock", "live")


# --- /api/analyze ---
class TestAnalyze:
    def test_analyze_success(self, session, sample_payload):
        r = session.post(f"{API}/analyze", json=sample_payload)
        assert r.status_code == 200, r.text
        data = r.json()
        assert "submission_id" in data
        assert isinstance(data["submission_id"], str)
        assert data["name"] == sample_payload["name"]
        assert data["price"] == 199
        prev = data["preview"]
        assert "success_score" in prev and 0 <= prev["success_score"] <= 100
        assert "top_matches" in prev and len(prev["top_matches"]) == 3
        for m in prev["top_matches"]:
            for k in ("title", "score", "tagline", "ai_resistance", "salary_mid", "explanation"):
                assert k in m
        assert prev.get("personality_insight")
        assert prev.get("hidden_strength", {}).get("title")
        assert "locked" in prev
        pytest.shared_submission_id = data["submission_id"]

    def test_analyze_missing_required_field(self, session):
        r = session.post(f"{API}/analyze", json={"name": "x"})
        assert r.status_code == 422


# --- /api/create-order ---
class TestOrder:
    def test_create_order_success(self, session):
        sub_id = getattr(pytest, "shared_submission_id", None)
        assert sub_id, "Need submission from analyze"
        r = session.post(f"{API}/create-order", json={"submission_id": sub_id})
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["mode"] in ("mock", "live")
        assert data["amount"] == 19900
        assert data["currency"] == "INR"
        assert data["order_id"].startswith("order_")

    def test_create_order_not_found(self, session):
        r = session.post(f"{API}/create-order", json={"submission_id": "nonexistent-id"})
        assert r.status_code == 404


# --- /api/report (preview/full) ---
class TestReportAndPayment:
    def test_get_report_unpaid_returns_preview(self, session):
        sub_id = pytest.shared_submission_id
        r = session.get(f"{API}/report/{sub_id}")
        assert r.status_code == 200
        data = r.json()
        assert data["paid"] is False
        assert "preview" in data
        assert "report" not in data

    def test_pdf_unpaid_returns_402(self, session):
        sub_id = pytest.shared_submission_id
        r = session.get(f"{API}/report/{sub_id}/pdf")
        assert r.status_code == 402

    def test_verify_payment_mock_unlocks_report(self, session):
        sub_id = pytest.shared_submission_id
        r = session.post(f"{API}/verify-payment", json={
            "submission_id": sub_id,
            "razorpay_order_id": "", "razorpay_payment_id": "",
            "razorpay_signature": "",
        })
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["success"] is True
        assert data["payment_id"].startswith("pay_mock_")
        report = data["report"]
        # full report contains all expected sections
        for k in ("matches", "salary_projection", "learning_roadmap", "strengths",
                  "growth_obstacles", "future_self_letter", "ai_resistance_score",
                  "leadership_potential", "business_potential", "personal_growth"):
            assert k in report, f"Missing key: {k}"
        assert len(report["matches"]) >= 5
        sp = report["salary_projection"]
        for yr in ("year1", "year3", "year5", "year10"):
            assert yr in sp

    def test_get_report_paid_returns_full(self, session):
        sub_id = pytest.shared_submission_id
        r = session.get(f"{API}/report/{sub_id}")
        assert r.status_code == 200
        data = r.json()
        assert data["paid"] is True
        assert "report" in data
        assert "matches" in data["report"]

    def test_pdf_paid_returns_pdf(self, session):
        sub_id = pytest.shared_submission_id
        r = session.get(f"{API}/report/{sub_id}/pdf")
        assert r.status_code == 200
        assert r.headers.get("content-type", "").startswith("application/pdf")
        assert len(r.content) > 2000
        assert r.content[:4] == b"%PDF"


# --- error path ---
def test_verify_payment_not_found(session):
    r = session.post(f"{API}/verify-payment", json={"submission_id": "missing"})
    assert r.status_code == 404


def test_report_not_found(session):
    r = session.get(f"{API}/report/missing-id")
    assert r.status_code == 404
