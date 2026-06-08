# Career Blueprint AI — PRD

## Original Problem Statement
A brutally-honest AI career intelligence platform for students, freshers, working professionals,
IT employees, laid-off employees, career switchers, freelancers, managers and business owners.
Provides honest career direction, salary projections, AI-disruption analysis, layoff survival,
career-switch guidance, skill roadmaps and growth plans. Tone: "a brutally honest career strategist",
not a motivational personality test. Funnel: emotional landing → adaptive questionnaire → free preview
(blurred premium) → ₹199 Razorpay → unlock 16-chapter report → premium PDF.

## Architecture
- **Frontend**: React + Tailwind + Framer Motion. View state machine (home | quiz | result).
  Adaptive multi-step questionnaire (steps change by user_type). Light "Future Gradient"
  indigo/purple/cyan glassmorphism theme.
- **Backend**: FastAPI.
  - `careers.py` — 23-career DB + honesty scoring (suitability/demand/salary/competition/AI-risk/
    difficulty/time-to-enter), careers-to-avoid, AI-threat, potential scores.
  - `engines.py` — layoff survival, career-switch, IT future report, 30/90/6mo/12mo learning plans, regret.
  - `ai_engine.py` — Claude Sonnet 4.6 (explain-only) + full deterministic template fallback.
  - `pdf_generator.py` — 16-chapter indigo/purple/cyan PDF (ReportLab).
- **DB**: MongoDB `submissions` (all leads, paid flag, payment_id, report, timestamp).
- **Payment**: Razorpay — live (checkout.js + HMAC verify) when keys set, else mock.

## User Personas
Student, Fresher, Working Professional, IT Employee, Manager, Laid-Off Employee, Career Switcher,
Freelancer, Business Owner.

## Core Requirements (static)
- Brutally honest: careers-to-avoid, weaknesses, AI-risk labels (Very Low→Critical). No fluff/astrology.
- Deterministic scoring first; AI only explains. Report generation < 10s.
- Free preview: top-3 matches (+verdict +AI-risk), success score, 1 strength, 1 weakness, 1 hidden talent, reality check.
- ₹199 (₹999 strike) Razorpay (UPI/Cards/NetBanking/Wallets); instant unlock.
- 12–15 page premium PDF (16 chapters), brand colors, mobile-first.

## Implemented (2026-06)
- Honest landing: hero ("Most People Waste Years…"), trust-builders, pain (4 Qs), how-it-works,
  user-types band, preview showcase, transformation, **regret calculator (live /api/regret)**,
  what's-inside (16 chapters), future-self teaser, pricing, FAQ, footer.
- Adaptive questionnaire (user-type → conditional Professional + Layoff steps; 16 interests, 5 binary +
  4 slider personality, goals incl. dream income @30/@40).
- Honesty engine, AI-threat, careers-to-avoid, layoff survival, IT future report, career-switch,
  learning plans, regret. Claude narrative + fallback. 16-chapter brand PDF.
- Live-ready Razorpay (mock active until keys added). All leads stored.
- Tested: backend 15/15 pytest pass; frontend Student + Laid-Off funnels 100%; IT-detection verified.

## Backlog
- **P0**: Add live RAZORPAY_KEY_ID/SECRET → restart backend → flip to live; re-test gateway.
- **P1**: Email the PDF (Resend/SendGrid); admin dashboard for leads/conversions/revenue.
- **P2**: EmailStr validation + rate-limit on /api/analyze & /api/regret; shareable result card; coupon codes;
  per-state salary localisation.

## Next Tasks
1. Receive Razorpay keys → enable live payments.
2. Optional: email delivery + lead-nurture sequence.
