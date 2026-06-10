"""Backend tests for the new /api/lead endpoint + payment_mode flag (mock).
Covers POST /api/lead full payload, minimal payload, and root /api/ payment_mode."""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/") or os.environ.get("BACKEND_URL", "").rstrip("/")
if not BASE_URL:
    # fallback for tests run inside container
    BASE_URL = "http://localhost:8001"
API = f"{BASE_URL}/api"


@pytest.fixture(scope="module")
def client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# ---- Root / payment_mode ----
def test_root_returns_payment_mode(client):
    r = client.get(f"{API}/")
    assert r.status_code == 200
    data = r.json()
    assert data.get("message") == "MapMyCareer"
    assert data.get("payment_mode") in ("mock", "live")


# ---- /api/lead ----
class TestLead:
    def test_lead_full_payload(self, client):
        payload = {"name": "TEST_Ravi", "whatsapp": "9876543210",
                   "degree": "B.Tech CSE", "source": "pre_payment", "user_type": "Student"}
        r = client.post(f"{API}/lead", json=payload)
        assert r.status_code == 200, r.text
        data = r.json()
        assert data.get("ok") is True
        assert isinstance(data.get("lead_id"), str) and len(data["lead_id"]) > 0

    def test_lead_minimal_payload(self, client):
        r = client.post(f"{API}/lead", json={"name": "TEST_Min", "whatsapp": "9000000000"})
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["ok"] is True
        assert data.get("lead_id")

    def test_lead_empty_payload_still_succeeds(self, client):
        # All fields default to "" — endpoint accepts and stores it.
        r = client.post(f"{API}/lead", json={})
        assert r.status_code == 200
        assert r.json().get("ok") is True

    def test_lead_distinct_ids(self, client):
        ids = set()
        for _ in range(3):
            r = client.post(f"{API}/lead", json={"name": "TEST_X", "whatsapp": "9000000001"})
            ids.add(r.json()["lead_id"])
        assert len(ids) == 3


# ---- Regression: analyze still works (Student plan = 199) ----
def test_analyze_student_returns_199(client):
    payload = {
        "name": "TEST_Student", "email": "test_student@example.com", "phone": "9000000000",
        "country": "India", "user_type": "Student",
        "answers": {"current_degree": "B.Tech CSE", "dream_career": "Game Developer",
                    "age": "21", "stream": "B.Tech CSE"},
        "personality": {},
    }
    r = client.post(f"{API}/analyze", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["plan"] == "student"
    assert data["price"] == 199
    assert "submission_id" in data and "preview" in data
