"""Smoke test: every user type produces a distinct, valid report end-to-end."""
import os
import requests

API = os.environ.get("REACT_APP_BACKEND_URL", "http://localhost:8001").rstrip("/") + "/api"
PERS = {"mind": "introvert", "approach": "analytical", "risk": "stable", "work_style": "independent",
        "structure": "structured", "leadership_interest": 7, "communication": 6, "stress_tolerance": 7}

CASES = {
    "Student": {"favorite_subjects": ["Mathematics", "Computer Science"], "career_interests": ["Software / IT"], "stream": "Computer Science", "dream_career": "Game Developer", "parents_preferred": "Doctor"},
    "Fresher": {"internships": "1", "projects": "1-2", "skills": ["Python", "SQL"], "resume_ready": "In progress", "linkedin": "Yes", "expected_salary": "6", "job_preference": "Product / Startups"},
    "IT Employee": {"developer_type": "Frontend Developer", "years_experience": "6", "cloud_knowledge": "Beginner", "ai_knowledge": "Beginner", "system_design": "Intermediate", "tech_stack": ["React"]},
    "Working Professional": {"current_role": "PM", "years_experience": "8", "current_salary": "14", "industry": "IT / Software", "team_size": "6-15", "leadership_responsibilities": "Manage a team", "desired_salary": "28", "desired_position": "Director"},
    "Career Switcher": {"current_profession": "Mechanical Engineer", "target_profession": "Data Analyst", "transferable_skills": ["Problem solving / DSA", "Excel / Sheets"], "learning_time": "10-20 hrs/week", "financial_situation": "3-6 months"},
    "Laid Off Employee": {"previous_role": "Sales Manager", "industry": "Retail / E-commerce", "reason_for_layoff": "Restructuring", "previous_salary": "18", "years_experience": "7", "skills": ["Communication", "Marketing"], "savings_runway": "3-6 months", "desired_industry": "IT / Software", "relocation": "Maybe"},
    "Manager": {"department": "Sales", "team_size": "16-50", "budget_responsibility": "Mid (₹50L-5Cr)", "hiring_experience": "Hired independently", "conflict_management": "High", "strategic_planning": "Medium", "revenue_responsibility": "High"},
    "Freelancer": {"services": ["Design", "Development"], "niche": "SaaS landing pages", "monthly_income": "80000", "clients": "2-4", "pricing": "Mid-market", "marketing_channels": ["LinkedIn content"], "portfolio_quality": "Strong"},
    "Business Owner": {"business_type": "Services", "revenue": "500000", "employees": "2-5", "profit_margin": "Low (<10%)", "customer_acquisition": "1 main channel", "biggest_challenge": "Getting customers", "growth_goals": "2x revenue", "marketing_channels": ["Referral programme"]},
}

REQUIRED_SECTION_IDS = {"reality_check", "snapshot", "risks", "opportunities", "focus", "stop", "roadmap", "letter"}


def run():
    seen = {}
    for ut, answers in CASES.items():
        r = requests.post(f"{API}/analyze", json={"name": "QA", "email": "qa@test.com", "user_type": ut, "answers": answers, "personality": PERS}, timeout=60)
        r.raise_for_status()
        d = r.json()
        sid = d["submission_id"]
        assert d["product_name"], ut
        # pay (mock) + fetch full report
        requests.post(f"{API}/create-order", json={"submission_id": sid}, timeout=30)
        rep = requests.post(f"{API}/verify-payment", json={"submission_id": sid}, timeout=30).json()["report"]
        ids = {s["id"] for s in rep["sections"]}
        missing = REQUIRED_SECTION_IDS - ids
        assert not missing, f"{ut} missing sections {missing}"
        # pdf
        pdf = requests.get(f"{API}/report/{sid}/pdf", timeout=60)
        assert pdf.status_code == 200 and len(pdf.content) > 4000, f"{ut} pdf {pdf.status_code}"
        seen[ut] = (d["product_name"], len(rep["sections"]), len(pdf.content))
        print(f"OK  {ut:22} -> {d['product_name']:38} sections={len(rep['sections'])} pdf={len(pdf.content)}B")
    # distinctness: all product names unique
    products = [v[0] for v in seen.values()]
    assert len(set(products)) == len(products), "product names not unique!"
    print("\nAll 9 categories produced distinct, valid reports.")


if __name__ == "__main__":
    run()
