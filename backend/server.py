from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import io
import uuid
import hmac
import hashlib
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

from careers import compute_blueprint
from engines import build_engines, build_regret
from ai_engine import enhance_report
from pdf_generator import build_pdf

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

PRICE_INR = 199
STUDENT_PRICE = 199
PRO_PRICE = 499
STUDENT_TYPES = {"Student", "Fresher"}


def plan_for(user_type: str):
    """Returns (plan_key, amount_inr) based on user type."""
    if (user_type or "").strip() in STUDENT_TYPES:
        return "student", STUDENT_PRICE
    return "professional", PRO_PRICE


RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', '')
PAYMENT_MODE = 'live' if (RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET) else 'mock'

app = FastAPI()
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ----------------------- Models -----------------------
class Interests(BaseModel):
    technology: int = 5
    business: int = 5
    finance: int = 5
    sales: int = 5
    marketing: int = 5
    design: int = 5
    writing: int = 5
    teaching: int = 5
    research: int = 5
    psychology: int = 5
    healthcare: int = 5
    law: int = 5
    content_creation: int = 5
    entrepreneurship: int = 5
    leadership: int = 5
    problem_solving: int = 5


class Personality(BaseModel):
    mind: str = "introvert"
    approach: str = "analytical"
    risk: str = "stable"
    role: str = "specialist"
    work_style: str = "independent"
    stress_tolerance: int = 5
    work_life: int = 5
    communication: int = 5
    public_speaking: int = 5


class Goals(BaseModel):
    priorities: List[str] = Field(default_factory=list)
    dream_income_30: str = ""
    dream_income_40: str = ""
    challenge: str = ""


class AnalyzeRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ""
    age: Optional[str] = ""
    gender: Optional[str] = ""
    country: Optional[str] = ""
    state: Optional[str] = ""
    user_type: Optional[str] = "Student"
    education: Optional[str] = ""
    current_degree: Optional[str] = ""
    current_profession: Optional[str] = ""
    graduation_year: Optional[str] = ""
    current_salary: Optional[str] = ""
    expected_salary: Optional[str] = ""
    # professional / layoff (optional)
    job_title: Optional[str] = ""
    years_experience: Optional[str] = ""
    industry: Optional[str] = ""
    previous_salary: Optional[str] = ""
    reason_for_layoff: Optional[str] = ""
    skills: Optional[str] = ""
    certifications: Optional[str] = ""
    desired_industry: Optional[str] = ""
    remote_preference: Optional[str] = ""
    interests: Interests
    personality: Personality
    goals: Goals


class OrderRequest(BaseModel):
    submission_id: str


class VerifyRequest(BaseModel):
    submission_id: str
    razorpay_order_id: Optional[str] = ""
    razorpay_payment_id: Optional[str] = ""
    razorpay_signature: Optional[str] = ""


class RegretRequest(BaseModel):
    age: str = "22"
    current_salary: str = "0"
    dream_salary: str = "0"


# ----------------------- Helpers -----------------------
def build_preview(report: Dict[str, Any]) -> Dict[str, Any]:
    top3 = []
    for m in report["matches"][:3]:
        top3.append({
            "title": m["title"], "icon": m["icon"], "score": m["score"], "tagline": m["tagline"],
            "ai_risk": m["ai_risk"], "ai_risk_label": m["ai_risk_label"], "ai_resistance": m["ai_resistance"],
            "market_demand": m["market_demand"], "salary_mid": m["salary"]["mid"], "growth": m["growth"],
            "verdict": m["verdict"], "explanation": report.get("match_explanations", {}).get(m["key"], m["tagline"]),
        })
    return {
        "user_type": report.get("user_type"),
        "success_score": report["success_score"],
        "ai_resistance_score": report["ai_resistance_score"],
        "portfolio_ai_risk": report["portfolio_ai_risk"],
        "ai_risk_label": report["ai_risk_label"],
        "top_matches": top3,
        "career_reality_check": report.get("career_reality_check", ""),
        "strength": (report.get("strength_scores") or [{}])[0],
        "weakness": report.get("weakness", {}),
        "hidden_talent": report.get("hidden_talent", {}),
        "trait_labels": report.get("trait_labels", []),
        "ai_threat_examples": report.get("ai_threat_examples", []),
        "locked": {
            "leadership_potential": report["leadership_potential"],
            "business_potential": report["business_potential"],
            "personal_growth": report["personal_growth"],
            "salary_year10": report["salary_projection"]["year10"],
            "careers_to_avoid_count": len(report.get("careers_to_avoid", [])),
        },
    }


# ----------------------- Routes -----------------------
@api_router.get("/")
async def root():
    return {"message": "Career Blueprint AI", "payment_mode": PAYMENT_MODE}


@api_router.post("/regret")
async def regret(req: RegretRequest):
    cur = float(req.current_salary or 0) if str(req.current_salary).replace('.', '').isdigit() else 0
    dream = float(req.dream_salary or 0) if str(req.dream_salary).replace('.', '').isdigit() else 0
    age = float(req.age or 22) if str(req.age).replace('.', '').isdigit() else 22
    years = max(10, min(30, round(50 - age)))
    yearly_gap = max((dream - cur) * 0.6, dream * 0.25, 2)
    return {"opportunity_cost": round(yearly_gap * years), "years": years,
            "yearly_gap": round(yearly_gap, 1)}


@api_router.post("/analyze")
async def analyze(req: AnalyzeRequest):
    profile = req.model_dump()
    blueprint = compute_blueprint(profile)
    enhanced = await enhance_report(profile, blueprint)
    blueprint.update(enhanced)
    blueprint.update(build_engines(profile, blueprint))

    plan, amount = plan_for(req.user_type)
    sub_id = str(uuid.uuid4())
    doc = {
        "id": sub_id, "name": req.name, "email": req.email, "phone": req.phone,
        "age": req.age, "gender": req.gender, "country": req.country, "state": req.state,
        "user_type": req.user_type, "education": req.education, "current_degree": req.current_degree,
        "current_profession": req.current_profession, "current_salary": req.current_salary,
        "expected_salary": req.expected_salary,
        "interests": profile["interests"], "personality": profile["personality"], "goals": profile["goals"],
        "professional": {k: profile.get(k) for k in ["job_title", "years_experience", "industry", "previous_salary",
                                                      "reason_for_layoff", "skills", "certifications", "desired_industry", "remote_preference"]},
        "report": blueprint, "paid": False, "payment_id": None, "plan": plan, "amount": amount,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.submissions.insert_one(doc)
    logger.info("New analysis: %s (%s) type=%s plan=%s ₹%s", req.name, sub_id, req.user_type, plan, amount)
    return {"submission_id": sub_id, "name": req.name, "email": req.email, "phone": req.phone,
            "plan": plan, "price": amount, "preview": build_preview(blueprint)}


@api_router.post("/create-order")
async def create_order(req: OrderRequest):
    sub = await db.submissions.find_one({"id": req.submission_id}, {"_id": 0})
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    amount_paise = int(sub.get("amount", STUDENT_PRICE)) * 100
    plan = sub.get("plan", "student")

    if PAYMENT_MODE == "live":
        import razorpay
        rzp = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        order = rzp.order.create({"amount": amount_paise, "currency": "INR", "payment_capture": 1,
                                  "receipt": f"cb_{req.submission_id[:30]}"})
        await db.submissions.update_one({"id": req.submission_id}, {"$set": {"order_id": order["id"]}})
        return {"mode": "live", "key_id": RAZORPAY_KEY_ID, "order_id": order["id"], "amount": amount_paise, "plan": plan,
                "currency": "INR", "name": sub["name"], "email": sub["email"], "phone": sub.get("phone", "")}

    order_id = f"order_mock_{uuid.uuid4().hex[:14]}"
    await db.submissions.update_one({"id": req.submission_id}, {"$set": {"order_id": order_id}})
    return {"mode": "mock", "key_id": "rzp_test_mock", "order_id": order_id, "amount": amount_paise, "plan": plan,
            "currency": "INR", "name": sub["name"], "email": sub["email"], "phone": sub.get("phone", "")}


@api_router.post("/verify-payment")
async def verify_payment(req: VerifyRequest):
    sub = await db.submissions.find_one({"id": req.submission_id}, {"_id": 0})
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    if PAYMENT_MODE == "live":
        body = f"{req.razorpay_order_id}|{req.razorpay_payment_id}"
        expected = hmac.new(RAZORPAY_KEY_SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, req.razorpay_signature or ""):
            raise HTTPException(status_code=400, detail="Payment signature verification failed")
        payment_id = req.razorpay_payment_id
    else:
        payment_id = req.razorpay_payment_id or f"pay_mock_{uuid.uuid4().hex[:14]}"

    await db.submissions.update_one({"id": req.submission_id},
                                    {"$set": {"paid": True, "payment_id": payment_id,
                                              "paid_at": datetime.now(timezone.utc).isoformat()}})
    updated = await db.submissions.find_one({"id": req.submission_id}, {"_id": 0})
    return {"success": True, "payment_id": payment_id, "report": updated["report"], "name": updated["name"]}


@api_router.get("/report/{submission_id}")
async def get_report(submission_id: str):
    sub = await db.submissions.find_one({"id": submission_id}, {"_id": 0})
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    if not sub.get("paid"):
        return {"paid": False, "preview": build_preview(sub["report"]), "name": sub["name"]}
    return {"paid": True, "report": sub["report"], "name": sub["name"]}


@api_router.get("/report/{submission_id}/pdf")
async def report_pdf(submission_id: str):
    sub = await db.submissions.find_one({"id": submission_id}, {"_id": 0})
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    if not sub.get("paid"):
        raise HTTPException(status_code=402, detail="Payment required to download the full report")
    pdf_bytes = build_pdf(sub)
    filename = f"Career_Blueprint_{sub['name'].split(' ')[0]}.pdf"
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf",
                             headers={"Content-Disposition": f'attachment; filename="{filename}"'})


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
