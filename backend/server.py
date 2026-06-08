from fastapi import FastAPI, APIRouter, HTTPException, Request
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
from ai_engine import enhance_report
from pdf_generator import build_pdf

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

PRICE_INR = 199
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
    design: int = 5
    psychology: int = 5
    teaching: int = 5
    healthcare: int = 5
    finance: int = 5
    content_creation: int = 5
    law: int = 5
    leadership: int = 5


class Personality(BaseModel):
    mind: str = "introvert"
    approach: str = "analytical"
    risk: str = "stable"
    role: str = "specialist"


class Goals(BaseModel):
    priorities: List[str] = Field(default_factory=list)
    dream_income: str = ""
    challenge: str = ""


class AnalyzeRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ""
    age: Optional[str] = ""
    gender: Optional[str] = ""
    education: Optional[str] = ""
    stream: Optional[str] = ""
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


# ----------------------- Helpers -----------------------
def build_preview(report: Dict[str, Any]) -> Dict[str, Any]:
    top3 = []
    for m in report["matches"][:3]:
        top3.append({
            "title": m["title"],
            "icon": m["icon"],
            "score": m["score"],
            "tagline": m["tagline"],
            "ai_resistance": m["ai_resistance"],
            "salary_mid": m["salary"]["mid"],
            "growth": m["growth"],
            "explanation": report.get("match_explanations", {}).get(m["key"], m["tagline"]),
        })
    return {
        "success_score": report["success_score"],
        "ai_resistance_score": report["ai_resistance_score"],
        "top_matches": top3,
        "personality_insight": report.get("personality_insight", ""),
        "hidden_strength": report.get("hidden_strength", {}),
        "trait_labels": report.get("trait_labels", []),
        "locked": {
            "leadership_potential": report["leadership_potential"],
            "business_potential": report["business_potential"],
            "personal_growth": report["personal_growth"],
            "salary_year10": report["salary_projection"]["year10"],
        },
    }


# ----------------------- Routes -----------------------
@api_router.get("/")
async def root():
    return {"message": "Career Blueprint AI", "payment_mode": PAYMENT_MODE}


@api_router.post("/analyze")
async def analyze(req: AnalyzeRequest):
    profile = req.model_dump()
    blueprint = compute_blueprint(profile)
    enhanced = await enhance_report(profile, blueprint)
    blueprint.update(enhanced)

    sub_id = str(uuid.uuid4())
    doc = {
        "id": sub_id,
        "name": req.name,
        "email": req.email,
        "phone": req.phone,
        "age": req.age,
        "gender": req.gender,
        "education": req.education,
        "stream": req.stream,
        "interests": profile["interests"],
        "personality": profile["personality"],
        "goals": profile["goals"],
        "report": blueprint,
        "paid": False,
        "payment_id": None,
        "amount": PRICE_INR,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.submissions.insert_one(doc)
    logger.info("New analysis: %s (%s)", req.name, sub_id)
    return {"submission_id": sub_id, "name": req.name, "preview": build_preview(blueprint), "price": PRICE_INR}


@api_router.post("/create-order")
async def create_order(req: OrderRequest):
    sub = await db.submissions.find_one({"id": req.submission_id}, {"_id": 0})
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    amount_paise = PRICE_INR * 100

    if PAYMENT_MODE == "live":
        import razorpay
        rzp = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        order = rzp.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1,
            "receipt": f"cb_{req.submission_id[:30]}",
        })
        await db.submissions.update_one({"id": req.submission_id}, {"$set": {"order_id": order["id"]}})
        return {"mode": "live", "key_id": RAZORPAY_KEY_ID, "order_id": order["id"],
                "amount": amount_paise, "currency": "INR", "name": sub["name"],
                "email": sub["email"], "phone": sub.get("phone", "")}

    # mock
    order_id = f"order_mock_{uuid.uuid4().hex[:14]}"
    await db.submissions.update_one({"id": req.submission_id}, {"$set": {"order_id": order_id}})
    return {"mode": "mock", "key_id": "rzp_test_mock", "order_id": order_id,
            "amount": amount_paise, "currency": "INR", "name": sub["name"],
            "email": sub["email"], "phone": sub.get("phone", "")}


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

    await db.submissions.update_one(
        {"id": req.submission_id},
        {"$set": {"paid": True, "payment_id": payment_id,
                  "paid_at": datetime.now(timezone.utc).isoformat()}},
    )
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
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


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
