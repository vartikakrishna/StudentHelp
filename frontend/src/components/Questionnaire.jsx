import React, { useState } from "react";
import * as Icons from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Slider } from "./ui/slider";
import { analyze } from "../lib/api";
import { CTAButton } from "./CTAButton";
import {
  USER_TYPES, PROFESSIONAL_TYPES, COUNTRIES, EDUCATION_OPTIONS, EDUCATION_LEVELS,
  INTERESTS, PERSONALITY_BINARY, PERSONALITY_SLIDERS, GOAL_PRIORITIES, DREAM_INCOME,
  CHALLENGES, LAYOFF_REASONS, REMOTE_PREFS, GENDERS,
} from "../data/blueprint";

const defaultInterests = INTERESTS.reduce((a, i) => ({ ...a, [i.key]: 5 }), {});
const defaultPersonality = {
  mind: "", approach: "", risk: "", role: "", work_style: "",
  stress_tolerance: 5, work_life: 5, communication: 5, public_speaking: 5,
};

const inputCls =
  "w-full rounded-xl bg-white border border-slate-200 px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 focus:outline-none transition";

export const Questionnaire = ({ onClose, onComplete }) => {
  const [stepIdx, setStepIdx] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [p, setP] = useState({
    name: "", email: "", phone: "", age: "", gender: "", country: "India", state: "",
    user_type: "", education: "", current_degree: "", current_profession: "", graduation_year: "",
    current_salary: "", expected_salary: "",
    job_title: "", years_experience: "", industry: "", previous_salary: "",
    reason_for_layoff: "", skills: "", certifications: "", desired_industry: "", remote_preference: "",
  });
  const [interests, setInterests] = useState(defaultInterests);
  const [pers, setPers] = useState(defaultPersonality);
  const [goals, setGoals] = useState({ priorities: [], dream_income_30: "", dream_income_40: "", challenge: "" });

  const isPro = PROFESSIONAL_TYPES.includes(p.user_type);
  const isLaidOff = p.user_type === "Laid Off Employee";

  const steps = ["usertype", "about", "background", ...(isPro ? ["professional"] : []), ...(isLaidOff ? ["layoff"] : []), "interests", "personality", "goals"];
  const step = steps[stepIdx];
  const progress = ((stepIdx + 1) / steps.length) * 100;

  const up = (k) => (e) => setP({ ...p, [k]: e.target.value });

  const canNext = () => {
    if (step === "usertype") return !!p.user_type;
    if (step === "about") return p.name.trim() && /\S+@\S+\.\S+/.test(p.email);
    if (step === "personality") return ["mind", "approach", "risk", "role", "work_style"].every((k) => pers[k]);
    if (step === "goals") return goals.priorities.length > 0 && goals.dream_income_30 && goals.challenge;
    return true;
  };

  const next = () => {
    setError("");
    if (!canNext()) { setError("Please complete the highlighted fields to continue."); return; }
    if (stepIdx < steps.length - 1) setStepIdx(stepIdx + 1);
    else submit();
  };

  const submit = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await analyze({ ...p, interests, personality: pers, goals });
      onComplete(data);
    } catch (e) {
      setError("Something went wrong generating your analysis. Please try again.");
      setLoading(false);
    }
  };

  const togglePriority = (x) =>
    setGoals((g) => ({ ...g, priorities: g.priorities.includes(x) ? g.priorities.filter((y) => y !== x) : [...g.priorities, x] }));

  return (
    <div className="fixed inset-0 z-[100] bg-white grad-mesh overflow-y-auto" data-testid="questionnaire">
      <div className="sticky top-0 z-10 glass border-b border-slate-200/70">
        <div className="max-w-2xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <button onClick={onClose} data-testid="quiz-close-btn" className="text-slate-500 hover:text-slate-900 flex items-center gap-1.5 text-sm">
              <Icons.ChevronLeft className="w-4 h-4" /> Exit
            </button>
            <span className="font-mono text-xs text-purple-600 tracking-widest uppercase">Step {stepIdx + 1} / {steps.length}</span>
          </div>
          <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
            <motion.div className="h-full grad-primary-h" animate={{ width: `${progress}%` }} transition={{ duration: 0.4 }} />
          </div>
        </div>
      </div>

      {loading ? (
        <LoadingScreen name={p.name} />
      ) : (
        <div className="max-w-2xl mx-auto px-6 py-10 pb-32">
          <AnimatePresence mode="wait">
            <motion.div key={step} initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }} transition={{ duration: 0.32 }} data-testid={`questionnaire-step-${stepIdx + 1}`}>
              {step === "usertype" && <UserTypeStep p={p} setP={setP} />}
              {step === "about" && <AboutStep p={p} up={up} setP={setP} />}
              {step === "background" && <BackgroundStep p={p} up={up} isPro={isPro} />}
              {step === "professional" && <ProfessionalStep p={p} up={up} />}
              {step === "layoff" && <LayoffStep p={p} up={up} />}
              {step === "interests" && <InterestsStep interests={interests} setInterests={setInterests} />}
              {step === "personality" && <PersonalityStep pers={pers} setPers={setPers} />}
              {step === "goals" && <GoalsStep goals={goals} setGoals={setGoals} togglePriority={togglePriority} />}
            </motion.div>
          </AnimatePresence>

          {error && <p className="mt-6 text-rose-500 text-sm" data-testid="quiz-error">{error}</p>}

          <div className="mt-10 flex items-center justify-between">
            {stepIdx > 0 ? (
              <button onClick={() => setStepIdx(stepIdx - 1)} className="text-slate-500 hover:text-slate-900 flex items-center gap-1.5">
                <Icons.ChevronLeft className="w-5 h-5" /> Back
              </button>
            ) : <span />}
            <CTAButton testid="questionnaire-next-btn" onClick={next}>
              {stepIdx === steps.length - 1 ? "Generate My Blueprint" : "Continue"}
            </CTAButton>
          </div>
        </div>
      )}
    </div>
  );
};

const Field = ({ label, children }) => (
  <div><label className="block text-sm text-slate-700 mb-2 font-medium">{label}</label>{children}</div>
);
const Sel = ({ testid, value, onChange, options, placeholder = "Select" }) => (
  <select data-testid={testid} className={inputCls} value={value} onChange={onChange}>
    <option value="">{placeholder}</option>
    {options.map((o) => <option key={o} value={o}>{o}</option>)}
  </select>
);
const Chip = ({ active, onClick, children, testid }) => (
  <button type="button" data-testid={testid} onClick={onClick}
    className={`px-4 py-2.5 rounded-full border text-sm font-medium transition-all ${active ? "border-transparent grad-primary-h text-white shadow-md shadow-purple-500/30" : "border-slate-200 bg-white text-slate-600 hover:border-purple-300"}`}>
    {children}
  </button>
);

const UserTypeStep = ({ p, setP }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">Who are you right now?</h2>
    <p className="text-slate-500 mb-8">We tailor the entire analysis to your situation.</p>
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {USER_TYPES.map((u) => {
        const Icon = Icons[u.icon] || Icons.User;
        const active = p.user_type === u.value;
        return (
          <button key={u.value} type="button" data-testid={`q-usertype-${u.value}`} onClick={() => setP({ ...p, user_type: u.value })}
            className={`flex flex-col items-center gap-2 rounded-2xl border p-4 transition-all ${active ? "border-purple-400 bg-purple-50 ring-2 ring-purple-200" : "border-slate-200 bg-white hover:border-purple-300"}`}>
            <span className={`w-11 h-11 rounded-xl flex items-center justify-center ${active ? "grad-primary" : "bg-slate-100"}`}>
              <Icon className={`w-5 h-5 ${active ? "text-white" : "text-slate-500"}`} strokeWidth={1.8} />
            </span>
            <span className="text-sm font-medium text-slate-800 text-center leading-tight">{u.label}</span>
          </button>
        );
      })}
    </div>
  </div>
);

const AboutStep = ({ p, up }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">A bit about you.</h2>
    <p className="text-slate-500 mb-8">So we can personalise and email your blueprint.</p>
    <div className="grid sm:grid-cols-2 gap-5">
      <Field label="Full Name *"><input data-testid="q-name" className={inputCls} value={p.name} onChange={up("name")} placeholder="e.g. Aarav Sharma" /></Field>
      <Field label="Email *"><input data-testid="q-email" className={inputCls} value={p.email} onChange={up("email")} placeholder="you@email.com" /></Field>
      <Field label="Phone"><input data-testid="q-phone" className={inputCls} value={p.phone} onChange={up("phone")} placeholder="Optional" /></Field>
      <Field label="Age"><input data-testid="q-age" className={inputCls} value={p.age} onChange={up("age")} placeholder="e.g. 24" /></Field>
      <Field label="Gender"><Sel testid="q-gender" value={p.gender} onChange={up("gender")} options={GENDERS} /></Field>
      <Field label="Country"><Sel testid="q-country" value={p.country} onChange={up("country")} options={COUNTRIES} /></Field>
      <div className="sm:col-span-2"><Field label="State / Region"><input data-testid="q-state" className={inputCls} value={p.state} onChange={up("state")} placeholder="e.g. Maharashtra" /></Field></div>
    </div>
  </div>
);

const BackgroundStep = ({ p, up, isPro }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">Your background.</h2>
    <p className="text-slate-500 mb-8">Education and field shape your honest match scores.</p>
    <div className="grid sm:grid-cols-2 gap-5">
      <Field label="Education Level"><Sel testid="q-edulevel" value={p.education} onChange={up("education")} options={EDUCATION_LEVELS} /></Field>
      <Field label="Degree / Field"><Sel testid="q-degree" value={p.current_degree} onChange={up("current_degree")} options={EDUCATION_OPTIONS} /></Field>
      <Field label="Graduation Year"><input data-testid="q-gradyear" className={inputCls} value={p.graduation_year} onChange={up("graduation_year")} placeholder="e.g. 2024" /></Field>
      {isPro && <Field label="Current Profession"><input data-testid="q-profession" className={inputCls} value={p.current_profession} onChange={up("current_profession")} placeholder="e.g. QA Engineer" /></Field>}
    </div>
  </div>
);

const ProfessionalStep = ({ p, up }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">Your work life.</h2>
    <p className="text-slate-500 mb-8">For salary, layoff-risk and career-switch analysis.</p>
    <div className="grid sm:grid-cols-2 gap-5">
      <Field label="Current Job Title"><input data-testid="q-jobtitle" className={inputCls} value={p.job_title} onChange={up("job_title")} placeholder="e.g. Software Engineer" /></Field>
      <Field label="Years of Experience"><input data-testid="q-exp" className={inputCls} value={p.years_experience} onChange={up("years_experience")} placeholder="e.g. 5" /></Field>
      <Field label="Industry"><input data-testid="q-industry" className={inputCls} value={p.industry} onChange={up("industry")} placeholder="e.g. IT Services" /></Field>
      <Field label="Current Salary (₹ LPA)"><input data-testid="q-cursalary" className={inputCls} value={p.current_salary} onChange={up("current_salary")} placeholder="e.g. 8" /></Field>
      <Field label="Expected Salary (₹ LPA)"><input data-testid="q-expsalary" className={inputCls} value={p.expected_salary} onChange={up("expected_salary")} placeholder="e.g. 18" /></Field>
    </div>
  </div>
);

const LayoffStep = ({ p, up }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">Layoff recovery details.</h2>
    <p className="text-slate-500 mb-8">We&apos;ll build your survival &amp; recovery roadmap.</p>
    <div className="grid sm:grid-cols-2 gap-5">
      <Field label="Previous Salary (₹ LPA)"><input data-testid="q-prevsalary" className={inputCls} value={p.previous_salary} onChange={up("previous_salary")} placeholder="e.g. 9" /></Field>
      <Field label="Reason For Layoff"><Sel testid="q-layoffreason" value={p.reason_for_layoff} onChange={up("reason_for_layoff")} options={LAYOFF_REASONS} /></Field>
      <div className="sm:col-span-2"><Field label="Your Skills (comma separated)"><input data-testid="q-skills" className={inputCls} value={p.skills} onChange={up("skills")} placeholder="e.g. Python, SQL, Testing" /></Field></div>
      <Field label="Certifications"><input data-testid="q-certs" className={inputCls} value={p.certifications} onChange={up("certifications")} placeholder="e.g. AWS, ISTQB" /></Field>
      <Field label="Desired Industry"><input data-testid="q-desired" className={inputCls} value={p.desired_industry} onChange={up("desired_industry")} placeholder="e.g. Product Tech" /></Field>
      <div className="sm:col-span-2"><Field label="Remote Preference"><Sel testid="q-remote" value={p.remote_preference} onChange={up("remote_preference")} options={REMOTE_PREFS} /></Field></div>
    </div>
  </div>
);

const InterestsStep = ({ interests, setInterests }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">Rate your interests.</h2>
    <p className="text-slate-500 mb-8">1 = not interested, 10 = love it.</p>
    <div className="space-y-5">
      {INTERESTS.map((it) => {
        const Icon = Icons[it.icon] || Icons.Sparkles;
        return (
          <div key={it.key} className="rounded-2xl bg-white border border-slate-100 p-4 soft-shadow">
            <div className="flex items-center justify-between mb-3">
              <span className="flex items-center gap-2.5 text-slate-800 font-medium">
                <span className="w-8 h-8 rounded-lg grad-primary flex items-center justify-center"><Icon className="w-4 h-4 text-white" strokeWidth={1.9} /></span>{it.label}
              </span>
              <span className="font-mono text-purple-600 text-sm w-7 text-right">{interests[it.key]}</span>
            </div>
            <Slider data-testid={`q-interest-${it.key}`} min={1} max={10} step={1} value={[interests[it.key]]} onValueChange={(v) => setInterests({ ...interests, [it.key]: v[0] })} className="cb-slider" />
          </div>
        );
      })}
    </div>
  </div>
);

const PersonalityStep = ({ pers, setPers }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">How are you wired?</h2>
    <p className="text-slate-500 mb-8">Pick what feels most like you.</p>
    <div className="space-y-7">
      {PERSONALITY_BINARY.map((q) => (
        <div key={q.key}>
          <p className="font-head font-600 text-lg mb-3 text-slate-900">{q.question}</p>
          <div className="grid sm:grid-cols-2 gap-3">
            {q.options.map((o) => {
              const active = pers[q.key] === o.value;
              return (
                <button key={o.value} type="button" data-testid={`q-personality-${q.key}-${o.value}`} onClick={() => setPers({ ...pers, [q.key]: o.value })}
                  className={`text-left rounded-2xl border p-4 transition-all ${active ? "border-purple-400 bg-purple-50 ring-2 ring-purple-200" : "border-slate-200 bg-white hover:border-purple-300"}`}>
                  <p className="font-head font-700 text-slate-900">{o.label}</p>
                  <p className="text-sm text-slate-500 mt-0.5">{o.desc}</p>
                </button>
              );
            })}
          </div>
        </div>
      ))}
      <div className="space-y-5 pt-2">
        {PERSONALITY_SLIDERS.map((s) => (
          <div key={s.key} className="rounded-2xl bg-white border border-slate-100 p-4 soft-shadow">
            <div className="flex items-center justify-between mb-3">
              <span className="text-slate-800 font-medium">{s.label}</span>
              <span className="font-mono text-purple-600 text-sm">{pers[s.key]}</span>
            </div>
            <Slider data-testid={`q-pslider-${s.key}`} min={1} max={10} step={1} value={[pers[s.key]]} onValueChange={(v) => setPers({ ...pers, [s.key]: v[0] })} className="cb-slider" />
          </div>
        ))}
      </div>
    </div>
  </div>
);

const GoalsStep = ({ goals, setGoals, togglePriority }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">What do you want?</h2>
    <p className="text-slate-500 mb-8">Be honest — there are no wrong answers.</p>

    <p className="font-head font-600 text-lg mb-3 text-slate-900">What matters most? <span className="text-slate-400 text-sm font-body">(pick any)</span></p>
    <div className="flex flex-wrap gap-2.5 mb-8">
      {GOAL_PRIORITIES.map((x) => <Chip key={x} active={goals.priorities.includes(x)} onClick={() => togglePriority(x)} testid={`q-goal-${x}`}>{x}</Chip>)}
    </div>

    <p className="font-head font-600 text-lg mb-3 text-slate-900">Dream income at age 30?</p>
    <div className="flex flex-wrap gap-2.5 mb-8">
      {DREAM_INCOME.map((d) => <Chip key={d.value} active={goals.dream_income_30 === d.value} onClick={() => setGoals({ ...goals, dream_income_30: d.value })} testid={`q-income30-${d.value}`}>{d.label}</Chip>)}
    </div>

    <p className="font-head font-600 text-lg mb-3 text-slate-900">Dream income at age 40?</p>
    <div className="flex flex-wrap gap-2.5 mb-8">
      {DREAM_INCOME.map((d) => <Chip key={d.value} active={goals.dream_income_40 === d.value} onClick={() => setGoals({ ...goals, dream_income_40: d.value })} testid={`q-income40-${d.value}`}>{d.label}</Chip>)}
    </div>

    <p className="font-head font-600 text-lg mb-3 text-slate-900">Your biggest challenge right now?</p>
    <div className="space-y-2.5">
      {CHALLENGES.map((c) => {
        const active = goals.challenge === c;
        return (
          <button key={c} type="button" data-testid={`q-challenge-${c}`} onClick={() => setGoals({ ...goals, challenge: c })}
            className={`w-full text-left rounded-2xl border px-4 py-3.5 transition-all ${active ? "border-purple-400 bg-purple-50 text-slate-900 ring-2 ring-purple-200" : "border-slate-200 bg-white text-slate-600 hover:border-purple-300"}`}>
            {c}
          </button>
        );
      })}
    </div>
  </div>
);

const LoadingScreen = ({ name }) => {
  const lines = [
    "Mapping your personality profile…",
    "Scoring careers on demand, salary, competition & AI risk…",
    "Running the honesty + AI-threat engine…",
    "Building your recovery & learning roadmap…",
  ];
  const [i, setI] = useState(0);
  React.useEffect(() => {
    const t = setInterval(() => setI((x) => Math.min(x + 1, lines.length - 1)), 1500);
    return () => clearInterval(t);
  }, []);
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] px-6 text-center" data-testid="quiz-loading">
      <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 2.4, ease: "linear" }} className="w-20 h-20 rounded-full border-4 border-purple-100 border-t-purple-500 mb-8" />
      <h3 className="font-head font-700 text-2xl sm:text-3xl mb-3 text-slate-900">Building {name ? name.split(" ")[0] + "'s" : "your"} Career Blueprint…</h3>
      <AnimatePresence mode="wait">
        <motion.p key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} className="text-purple-600 font-mono text-sm">{lines[i]}</motion.p>
      </AnimatePresence>
    </div>
  );
};
