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

from type_engines import analyze_profile
from ai_engine import enhance
from pdf_generator import build_pdf, build_addon_pdf
from addons import ADDON_CATALOG, expand_addons, addon_total, build_addon_content, normalize_ids

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
# Optional override (e.g. PAYMENT_MODE=mock on staging); otherwise live when keys are present.
PAYMENT_MODE = os.environ.get('PAYMENT_MODE') or ('live' if (RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET) else 'mock')

app = FastAPI()
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ----------------------- Models -----------------------
class AnalyzeRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ""
    country: Optional[str] = "India"
    user_type: str = "Student"
    answers: Dict[str, Any] = Field(default_factory=dict)
    personality: Dict[str, Any] = Field(default_factory=dict)


class OrderRequest(BaseModel):
    submission_id: str


class VerifyRequest(BaseModel):
    submission_id: str
    razorpay_order_id: Optional[str] = ""
    razorpay_payment_id: Optional[str] = ""
    razorpay_signature: Optional[str] = ""


class AddonOrderRequest(BaseModel):
    submission_id: str
    addon_ids: List[str] = Field(default_factory=list)


class AddonVerifyRequest(BaseModel):
    submission_id: str
    addon_ids: List[str] = Field(default_factory=list)
    razorpay_order_id: Optional[str] = ""
    razorpay_payment_id: Optional[str] = ""
    razorpay_signature: Optional[str] = ""


class RegretRequest(BaseModel):
    age: str = "22"
    current_salary: str = "0"
    dream_salary: str = "0"


class LeadRequest(BaseModel):
    name: str = ""
    whatsapp: str = ""
    degree: Optional[str] = ""
    source: Optional[str] = "landing"
    user_type: Optional[str] = ""


# ----------------------- Helpers -----------------------
def regret_calc(age, current_salary, dream_salary):
    cur = num_or(current_salary)
    dream = num_or(dream_salary)
    a = num_or(age) or 22
    years = max(10, min(30, round(50 - a)))
    yearly_gap = max((dream - cur) * 0.6, dream * 0.25, 2)
    return {"opportunity_cost": round(yearly_gap * years), "years": years, "yearly_gap": round(yearly_gap, 1)}


def num_or(v, default=0.0):
    try:
        return float(str(v).replace(",", "").strip())
    except (TypeError, ValueError):
        return default


# ----------------------- Routes -----------------------
@api_router.get("/")
async def root():
    return {"message": "MapMyCareer", "payment_mode": PAYMENT_MODE}


@api_router.post("/regret")
async def regret(req: RegretRequest):
    return regret_calc(req.age, req.current_salary, req.dream_salary)


@api_router.post("/lead")
async def capture_lead(req: LeadRequest):
    lead = req.model_dump()
    lead["lead_id"] = str(uuid.uuid4())
    lead["created_at"] = datetime.now(timezone.utc).isoformat()
    await db.leads.insert_one({**lead})
    return {"ok": True, "lead_id": lead["lead_id"]}


@api_router.post("/analyze")
async def analyze(req: AnalyzeRequest):
    profile = req.model_dump()
    report = analyze_profile(profile)
    report = await enhance(profile, report)

    plan, amount = plan_for(req.user_type)
    sub_id = str(uuid.uuid4())
    doc = {
        "id": sub_id, "name": req.name, "email": req.email, "phone": req.phone,
        "country": req.country, "user_type": req.user_type,
        "answers": req.answers, "personality": req.personality,
        "report": report, "paid": False, "payment_id": None, "plan": plan, "amount": amount,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.submissions.insert_one(doc)
    logger.info("New analysis: %s (%s) type=%s plan=%s ₹%s", req.name, sub_id, req.user_type, plan, amount)
    return {"submission_id": sub_id, "name": req.name, "email": req.email, "phone": req.phone,
            "plan": plan, "price": amount, "user_type": req.user_type,
            "product_name": report.get("product_name"), "primary_goal": report.get("primary_goal"),
            "preview": report["preview"]}


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
        return {"paid": False, "preview": sub["report"]["preview"], "name": sub["name"]}
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


# ----------------------- Add-ons (post-purchase upsells) -----------------------
@api_router.post("/create-addon-order")
async def create_addon_order(req: AddonOrderRequest):
    sub = await db.submissions.find_one({"id": req.submission_id}, {"_id": 0})
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    if not sub.get("paid"):
        raise HTTPException(status_code=402, detail="Unlock your main report before adding extras")
    ids = normalize_ids(req.addon_ids)
    total = addon_total(ids)
    if total <= 0:
        raise HTTPException(status_code=400, detail="No valid add-ons selected")
    amount_paise = total * 100
    label = ", ".join(ADDON_CATALOG[i]["title"] for i in ids)

    if PAYMENT_MODE == "live":
        import razorpay
        rzp = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        order = rzp.order.create({"amount": amount_paise, "currency": "INR", "payment_capture": 1,
                                  "receipt": f"cba_{req.submission_id[:26]}"})
        return {"mode": "live", "key_id": RAZORPAY_KEY_ID, "order_id": order["id"], "amount": amount_paise,
                "currency": "INR", "label": label, "name": sub["name"], "email": sub["email"], "phone": sub.get("phone", "")}

    order_id = f"order_addon_mock_{uuid.uuid4().hex[:12]}"
    return {"mode": "mock", "key_id": "rzp_test_mock", "order_id": order_id, "amount": amount_paise,
            "currency": "INR", "label": label, "name": sub["name"], "email": sub["email"], "phone": sub.get("phone", "")}


@api_router.post("/verify-addon-payment")
async def verify_addon_payment(req: AddonVerifyRequest):
    sub = await db.submissions.find_one({"id": req.submission_id}, {"_id": 0})
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    if not sub.get("paid"):
        raise HTTPException(status_code=402, detail="Unlock your main report before adding extras")

    if PAYMENT_MODE == "live":
        body = f"{req.razorpay_order_id}|{req.razorpay_payment_id}"
        expected = hmac.new(RAZORPAY_KEY_SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, req.razorpay_signature or ""):
            raise HTTPException(status_code=400, detail="Payment signature verification failed")
        payment_id = req.razorpay_payment_id
    else:
        payment_id = req.razorpay_payment_id or f"pay_addon_mock_{uuid.uuid4().hex[:12]}"

    components = expand_addons(req.addon_ids)
    if not components:
        raise HTTPException(status_code=400, detail="No valid add-ons selected")

    addons = sub.get("addons") or {}
    for c in components:
        if c not in addons:
            addons[c] = build_addon_content(c, sub)
    purchased = sorted(set((sub.get("purchased_addons") or []) + components))
    await db.submissions.update_one(
        {"id": req.submission_id},
        {"$set": {"addons": addons, "purchased_addons": purchased},
         "$push": {"addon_payments": {"payment_id": payment_id, "components": components,
                                      "at": datetime.now(timezone.utc).isoformat()}}})
    logger.info("Add-ons purchased: %s -> %s", req.submission_id, components)
    return {"success": True, "payment_id": payment_id, "purchased_addons": purchased}


@api_router.get("/report/{submission_id}/addon/{addon_id}/pdf")
async def addon_pdf(submission_id: str, addon_id: str):
    sub = await db.submissions.find_one({"id": submission_id}, {"_id": 0})
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    if addon_id not in (sub.get("purchased_addons") or []):
        raise HTTPException(status_code=402, detail="This add-on has not been purchased")
    if not (sub.get("addons") or {}).get(addon_id):
        sub.setdefault("addons", {})[addon_id] = build_addon_content(addon_id, sub)
    pdf_bytes = build_addon_pdf(sub, addon_id)
    title = ADDON_CATALOG.get(addon_id, {}).get("title", "Addon").replace(" ", "_")
    filename = f"{title}_{sub['name'].split(' ')[0]}.pdf"
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
