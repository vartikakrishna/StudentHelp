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

## Implemented (2026-06 — dual pricing + honesty)
- **Dual pricing**: Student/Fresher = ₹199 "Student Career Blueprint" (₹999 strike); all professional
  types = ₹499 "Professional Career Intelligence Report" (₹2499 strike). `plan_for()` in server.py;
  PLAN_CONFIG/COMPARISON/UPSELLS in blueprint.js. Plan-specific locked sections, comparison table
  (highlights active plan column), upsell cards, and pro-only report sections (Potential Scores,
  Career Switch, IT Future, Resume/LinkedIn/Interview). Verified E2E (testing iteration_3, 100%).
- **Honesty engine hardened**: ai_engine.py SYSTEM + prompt now enforce ZERO sugar-coating —
  blunt verdicts, named uncomfortable truths, data-backed. (user request 2026-06)
- Fixed: removed "Fresher" from frontend PROFESSIONAL_TYPES so Freshers skip the pro questionnaire
  step (consistent with their student ₹199 plan).

## 🚀 ALL 9 CATEGORIES LIVE (2026-06) — distinct standalone products
Each user type is its own product: unique questionnaire, scoring model, report sections,
recommendations, roadmap, action plan and AI focus. Every report answers the 8 universal
questions (where am I / risks / missed opportunities / focus / stop / 30-day / 90-day / 1-year)
via shared `diagnostic_sections` + `action_roadmap` with category-specific content. Typed
`sections` render identically on web (`ReportRenderer.jsx`) and PDF (`build_pdf`).
Products: Student=Career Direction (₹199), Fresher=First-Job Readiness (₹199), IT Employee=AI
Survival & Growth (₹499), Working Professional=Career Growth (₹499), Career Switcher=Career
Transition Blueprint (₹499), Laid Off=Career Recovery Blueprint (₹499), Manager=Leadership Growth
(₹499), Freelancer=Freelance Income (₹499), Business Owner=Business Growth Intelligence (₹499).
Tested: backend `tests/test_all_types.py` (all 9 distinct + valid PDFs) + frontend iteration_6 (100%).
All categories unlocked; personality = 8 traits (20% weight); category VALUE screen before quiz.

## 🚀 MAJOR UPGRADE — Per-Category Products (data-driven engine)
Each user type is now its own product: different questionnaire, scoring model, report sections,
recommendations and action plan. Architecture is data-driven — engines emit typed `sections`
(intro/callout/scorecards/bars/matches/list/tags/cards/roadmap/salary_chart/letter) rendered
identically on web (`ReportRenderer.jsx`) and PDF (`pdf_generator.build_pdf`).

### Phase 1 — DONE (2026-06), tested iteration_5 (100%)
- **Student → Career Direction Report (₹199):** career match, best degrees, AI-proof options,
  mistakes to avoid, skills, learning roadmap, 10-yr projection, future-self letter.
- **IT Employee → AI Survival & Growth Report (₹499):** AI replacement risk, threat assessment,
  transition opportunities, skill gaps, emerging tech, tech roadmap, salary plan, verdict.
- **Working Professional → Career Growth Report (₹499):** promotion readiness, salary forecast,
  leadership analysis, industry outlook, growth roadmap.
- Personality reduced to 8 traits (5 binary + 3 sliders) used as 20% scoring modifier.
- Category VALUE screen before the questionnaire; typed PREVIEW (some scores visible, some 🔒);
  Hero headline updated; non-Phase-1 types gated as "SOON".
- Backend: `type_engines.py` (engines + dispatch + PROFILE_META), `common.py` (traits, interest
  mapping, section builder), `ai_engine.enhance` (per-category prose, deterministic fallback),
  flexible `/api/analyze` ({user_type, answers, personality}).

### Phase 2 — TODO (P0): Fresher (₹199), Career Switcher (₹499), Laid Off Employee (₹499)
Build dedicated questionnaire + scoring engine + sections per the spec (job readiness / switch
feasibility / recovery roadmaps). Remove their "SOON" gating + interim student/professional routing.

### Phase 3 — TODO (P1): Manager (₹499), Freelancer (₹499), Business Owner (₹499)
Leadership growth / freelance income / business-growth intelligence reports.

## Backlog
- **P0**: Add live RAZORPAY_KEY_ID/SECRET → restart backend → flip to live; re-test gateway. (BLOCKED on user keys)
- **P1 (DONE 2026-06)**: Functional post-purchase upsells. `addons.py` (catalog + personalized Resume/
  LinkedIn/Interview deliverables, bundle = all 3). Endpoints: POST /api/create-addon-order (402 until
  main report paid; bundle supersedes), POST /api/verify-addon-payment (grants components, returns
  purchased_addons), GET /api/report/{id}/addon/{addon_id}/pdf (branded add-on PDF, 402 if unpurchased).
  Frontend: interactive multi-select cards + bundle exclusivity + sticky checkout bar + reused PaymentModal
  (addon mode) + purchased-state download links. Verified backend curl + frontend E2E (iteration_4, 100%).
- **P1**: Email the PDF (Resend/SendGrid); admin dashboard for leads/conversions/revenue.
- **P2**: EmailStr validation + rate-limit on /api/analyze & /api/regret; shareable result card; coupon codes;
  per-state salary localisation.

## Next Tasks
1. Add the same Razorpay keys to PRODUCTION env + redeploy to push V2 + new landing live.
2. Paste Meta Pixel / GA4 / GTM IDs when ready (events already wired; just need IDs in env).
3. Optional: email PDF delivery + lead-nurture (leads now captured in db.leads).

## 🎯 LANDING PAGE CRO REDESIGN — Indian Students (2026-06) — DONE
Full conversion-optimized **premium DARK landing** rebuilt per design-agent blueprint, mobile-first
(95% mobile traffic from Reels/Shorts/Meta/WhatsApp). Brand = MapMyCareer; WhatsApp = +918448773316.
- **New landing** (`components/sections/Landing.jsx`): hero with degree lead-magnet input + "Generate My
  Free Career Blueprint" CTA + trust microcopy; AI-disruption pain section; how-it-works (3 steps);
  blurred report-preview tease; 6 feature cards; student testimonials (initials avatars + verified badge +
  stars, "representative" footnote); 5 college-segment cards; ₹499→₹199 pricing with launch urgency;
  payment-security badges (UPI/GPay/PhonePe/Paytm/Visa/Mastercard + Razorpay); FAQ accordion; footer.
- **Functional adds**: floating WhatsApp FAB (`WhatsAppFab.jsx`, z-55, opens wa.me with prefilled msg),
  mobile sticky CTA (`StickyCta.jsx`, appears after scroll), **3-field lead capture** (`LeadGate.jsx`:
  Name/WhatsApp/Degree) shown right BEFORE payment → POST **`/api/lead`** (new endpoint, stores to
  `db.leads`), hero degree prefills the questionnaire.
- **Analytics** (`lib/analytics.js` + `lib/config.js`): dataLayer + GA4(gtag) + Meta Pixel(fbq) wired;
  events fire cta_click / begin_questionnaire / generate_report / lead_submit / whatsapp_click / purchase.
  IDs read from env (REACT_APP_META_PIXEL_ID / GA4_ID / GTM_ID) — blank until provided; events still queue.
- App.js rewritten to home(Landing)→quiz→result flow; the existing premium V2 report + funnel are reused.
- Verified: iteration_10 — backend 6/6 lead tests + 28/28 engines regression + full E2E (hero degree →
  Student quiz → preview → LeadGate → mock-pay → V2 report → PDF) on desktop + 390px mobile, 0 JS errors.

## 🚀 MAPMYCAREER V2 — Decision & Roadmap Platform (2026-06) — DONE
Major upgrade from "report generator" → "career decision & roadmap platform". User decisions:
hybrid curated+AI content, phased Year 1-4 plans, full rename, all 9 categories kept, pricing unchanged
(Student ₹199 / IT ₹499 / Working Professional ₹499).
- **Rename**: Career Blueprint AI → **MapMyCareer** everywhere (navbar, footer, tab title, PaymentModal,
  Razorpay checkout name, PDF cover, AI prompt, API root). Zero old-brand strings remain.
- **Career DB**: expanded `career_db.py` 210 → **317 careers** across 45 clusters (added Mechanical,
  Electrical, Civil, Aerospace/Aviation, Energy, Agriculture, Logistics, Public Health, Medical
  Specialists, Arts, Languages, Maritime, Enterprise-IT, Wellness, Business Ops). Resolver hardened
  (Solutions Architect → Cloud Architect aliases).
- **New curated content modules**: `content_lib.py` (per-cluster/domain learning libraries — skills,
  tools, courses, books, YouTube, projects, certifications, universities) + `system_design.py`
  (fixed L1→L4 System Design syllabus). AI personalises narrative on top (hybrid).
- **New section types** (web + PDF): `recommendations` (Top-N cards with match %, why, pros/cons,
  growth/AI-risk/salary badges) and `blueprint` (phased plan cards with labelled resource groups).
  Added to `ReportRenderer.jsx` (Recommendations/Blueprint components) and `pdf_generator.py`.
- **Student V2**: reality_check, Dream Career Reality Check (scores), Honest Verdict (dream pinned +
  challenges + improvements + backups), Top 5 Recommendations (pros/cons), Degree/Course/Cert/University
  cards, Year 1-4 Learning Blueprint, Financial Projection (+wealth range), Mistakes, 30-Day + 90-Day plans.
- **IT V2**: Career Health Score, AI Replacement Risk (level/why/how), Skill Gap Analysis
  (current/missing/future), MANDATORY System Design Roadmap L1→L4, Future Career Tracks (recommendations),
  Salary Projection, Promotion Readiness, Learning Plan (30/90/6mo/1yr).
- **Working Professional V2**: Promotion/Leadership/Income scorecards, Industry Outlook, Future Career
  Options (recommendations), Skill Gap Analysis, Financial Projection, Leadership Analysis, 90-Day + 1-Year plans.
- **Questionnaire fields added**: Student (Financial Expectations, Desired Lifestyle, Technology Interest,
  Creativity Level + relabelled Study Discipline); IT (Team Size, Leadership Experience, Career Goal/Desired
  Role, Desired Salary); Fresher target_role (prior).
- **New config**: optional `PAYMENT_MODE` env override (staging/testing); default live when keys present.
- Verified: **38/38 backend tests** (`tests/test_engines_v2.py` 28 unit + a generated HTTP E2E 10) +
  full Student UI funnel (iteration_9, 100%, 0 JS errors) — branding, 7 new fields, preview, mock-pay
  unlock, all V2 premium sections + recommendation/blueprint cards rendering, PDFs valid for all 9 types.

## 🧠 DEEP CAREER BLUEPRINT — 16–20 page premium report (2026-06) — DONE
Major upgrade: the paid report is now a deeply AI-generated "Career Transformation Blueprint" for the
3 flagship products (Student ₹199, IT Employee ₹499, Working Professional ₹499). Decisions: generate
AFTER payment (background), AUGMENT existing sections, DROP the Year 1-4 phased blueprint and replace
with a single detailed step-by-step SYLLABUS to reach the goal, target 16–20 pages.
- **`deep_report.py`** (new): `generate_deep_sections(profile, report)` runs ~11 SMALL parallel Claude
  Sonnet 4.6 calls (semaphore=5, 110s timeout each) and assembles ~22 typed sections: Executive Summary,
  Career DNA, Current/Future Market Position, Deep Dive Best Path, Skill Gap (TABLE), Detailed Syllabus
  (blueprint), 10 Projects, Tool Stack, Networking + Cold Message Templates, Personal Brand + Content
  Ideas, Financial Prep, 30-Day (day-by-day) / 90-Day (weekly) / 365-Day (monthly) TIMELINES, Common
  Failure Points, AI Impact, Success Blueprint. Best-effort: failed chunks are skipped; base report still renders.
- **Background generation + polling**: `POST /api/generate-deep/{id}` kicks an asyncio background task
  (returns {status:"generating"}); `GET /api/generate-deep/{id}/status` returns {status:"done", report}
  when ready (deep_generated flag persisted to db). Avoids HTTP timeouts (generation ~110-115s).
- **New render types** (web + PDF): `table` (TableBlock) and `timeline` (Timeline). Added to
  `ReportRenderer.jsx` BLOCKS and `pdf_generator.py` `_section_block`.
- **Frontend**: `ResultPreview.jsx` shows a `BuildingBlueprint` loader (6 animated steps) post-payment,
  polls every 4s up to ~3.5min, then renders the enriched report. Deep sections replace base
  action/learning-plan + Year1-4 blueprint when present.
- **BUG FIXED (root cause)**: `EMERGENT_LLM_KEY` was read at module-import time, BEFORE `load_dotenv()`
  in server.py → it was always None, so ai_engine.enhance was a silent no-op AND deep_report produced
  nothing. Fixed both modules to read the key at call-time (AI narrative now actually runs).
- Verified: backend assembly unit-test (22 sections), real LLM E2E (31 sections for Professional, valid
  31-page PDF), and full frontend Student E2E (iteration_12, 100%, 0 console errors): loader → ~110s
  generation → 29 sections incl table-skill_gap + 3 timelines → PDF 200. PAYMENT_MODE restored to live.

## 💳 LIVE RAZORPAY ENABLED (2026-06) — DONE
PAYMENT_MODE flipped mock→live in preview .env; live keys (rzp_live_SxDQOWrUTiEaTB) validated against
Razorpay (real order created). Code (create-order → checkout.js → HMAC verify, main + add-ons) was already
implemented. NOTE: production deployment needs RAZORPAY_KEY_ID/SECRET + PAYMENT_MODE=live set in prod env + redeploy.


Extended the goal engine into the remaining "direction" categories. New shared
`type_engines._future_direction(goal_text, traits, prefix)` resolves a free-text target role via
`career_db.goal_block()` and, when it maps to a real career, inserts a `future_direction` matches
section (resolved role pinned #1 + related careers). Generic seniority titles (Director/VP/CEO/CTO/
Manager/Lead/Principal…) are intentionally SKIPPED via a GENERIC_LEVELS guard so we never misfire
(e.g. corporate "Director" no longer resolves to "Film Director"). Wired into:
- `analyze_it` → `answers['future_goal']` (new IT questionnaire field "Your Future Direction").
- `analyze_professional` → `answers['desired_position']` (existing field).
- `analyze_manager` → `answers['target_role']` (new Manager field "Your Target Leadership Role").
Added career_db aliases (solutions/software/technical/cloud architect → cloud_architect). Blank field =
old behavior preserved. Verified: 31/31 backend pytest (test_future_direction.py + test_dream_engine.py)
+ 3 UI funnels (iteration_8, 100%).

## 🎯 FUTURE-GOAL / DREAM CAREER ENGINE (2026-06) — P0 bias fix DONE
Fixed the critical recommendation bias where the engine overrode users' dream careers with
unrelated generic jobs (e.g. "Game Developer" → "Data Entry"). The previous agent had built
`career_db.py` (200+ careers across 15 clusters + free-text resolver + dream_match weights) but
it was never wired in. Now integrated:
- **`career_db.py`**: `goal_block()` resolves the user's stated dream/target via `resolve_career()`
  (ordering fixed so exact titles beat greedy alias substrings — Data Scientist no longer → Research
  Scientist), PINS it as the #1 match (Honesty Rule — never substituted), adds 2-3 RELATED backup
  careers from the same cluster + an honest `challenges_for()` read. Weights: Dream 25 · Interest 25 ·
  Aptitude 20 · Personality 15 · Market 15. Plus `fit_score`, `rank_all`, `avoid_block`, `_card`.
- **`type_engines.py`**: `analyze_student` rewritten → "Dream Career Match" + "Success Probability"
  scorecards, new `dream_verdict` cards section (goal card with challenges + backup-plan card),
  matches = dream + related + best-fit. `analyze_switcher` → `target_direction` matches section on the
  resolved target profession. `analyze_fresher` → optional `target_role` field → `target_direction`.
- **`ai_engine.py`**: SYSTEM prompt now carries the HONESTY RULE (LLM may explain challenges but must
  never replace/downgrade the dream or suggest an unrelated "safe" job).
- **Frontend**: Fresher questionnaire gained a "Your Dream / Target Role" text field.
- Per user direction, the engine is a **"Future Goal Engine"**: Student/Fresher/Switcher → Dream Career;
  IT/Professional/Manager → Future Direction; Freelancer → Business Goal; Business Owner → Growth Goal;
  Laid-Off → Recovery Goal (each engine already optimizes for its own objective).
- Verified: backend 17/17 pytest (`tests/test_dream_engine.py`) + `tests/test_all_types.py` (9 distinct
  valid PDFs) + frontend Student "Game Developer" funnel E2E (iteration_7, 100%). Game Developer pinned
  #1 @86% with Gameplay Programmer/Unity/Unreal backups; zero Data Entry leakage.
