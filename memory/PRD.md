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
1. ✅ Razorpay LIVE keys added (2026-06) → `payment_mode: live`, real order creation verified
   (order_Sz9MmMOnodWX93, ₹199). Add the same keys to the PRODUCTION deployment env to go live there too.
2. Optional: email delivery + lead-nurture sequence.

## 🧭 FUTURE-DIRECTION ENGINE for IT / Professional / Manager (2026-06) — DONE
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
