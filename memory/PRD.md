# Career Blueprint AI — PRD

## Original Problem Statement
Build a highly emotional, psychologically persuasive landing page ("Career Blueprint AI") that helps
students discover their ideal career path, earning potential, strengths, and a personalized roadmap.
Funnel: emotional landing → multi-step questionnaire → free preview (blurred premium) → ₹199 Razorpay
payment → unlock full 10-chapter report → premium PDF download. Theme: dark navy + gold, Netflix-quality.

## Architecture
- **Frontend**: React + Tailwind + Framer Motion. View state machine (home | quiz | result) in App.js.
  Sections in `components/sections/*`, funnel in `Questionnaire.jsx`, `ResultPreview.jsx`, `PaymentModal.jsx`.
- **Backend**: FastAPI. `careers.py` (deterministic scoring of 12 careers), `ai_engine.py` (LLM narrative
  via Emergent key gpt-5.4-mini + template fallback), `pdf_generator.py` (ReportLab premium PDF), `server.py` (routes).
- **DB**: MongoDB `submissions` collection (all leads stored, paid flag, payment_id, report data, timestamp).

## User Personas
- Confused student (Class 10–PG) unsure about career/stream.
- Parents guiding a teenager.

## Core Requirements (static)
- Emotional, fear/curiosity/hope-driven copy; cinematic dark+gold design.
- Deterministic scoring first; AI only explains (no hallucinated numbers); generation < 10s.
- Free preview: top-3 matches, success score, 1 personality insight, 1 hidden strength; rest locked.
- Razorpay ₹199 (UPI/Cards/NetBanking/Wallets); success unlocks report instantly.
- Premium 12–15 page PDF (navy/white/gold, progress bars, score cards, 10 chapters).

## Implemented (2026-06)
- Full landing page: Hero, Pain, How It Works, Preview Showcase (lock overlay), Transformation,
  What's Inside (bento, 10 chapters), Pricing ₹199, FAQ, Footer.
- 4-step questionnaire (about, 10 interest sliders, 4 personality, goals) with validation + loading screen.
- `/api/analyze`, `/api/create-order`, `/api/verify-payment`, `/api/report/{id}`, `/api/report/{id}/pdf`.
- Deterministic scoring engine (12 careers, salary/AI-resistance/leadership/business/growth scores).
- AI narrative layer with robust template fallback. Premium ReportLab PDF.
- Mock Razorpay checkout (live-ready: set RAZORPAY_KEY_ID/SECRET to switch). All leads stored.
- Tested E2E: backend 12/12 pytest pass, frontend funnel 100%.

## Backlog
- **P0**: Add real Razorpay keys for live payments (currently MOCK mode).
- **P1**: Email the PDF to the user (Resend/SendGrid); admin dashboard for leads/conversions.
- **P2**: A/B test pricing & headlines; rate limiting on /api/analyze; EmailStr validation;
  shareable result card for social proof; coupon codes.

## Next Tasks
1. Collect Razorpay keys → flip to live mode and re-test payment.
2. Optional: email delivery of the PDF + lead-nurture sequence.
