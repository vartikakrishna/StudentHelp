import React, { useState } from "react";
import * as Icons from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Slider } from "./ui/slider";
import { analyze } from "../lib/api";
import { CTAButton } from "./CTAButton";
import {
  INTERESTS, PERSONALITY, GOAL_PRIORITIES, DREAM_INCOME,
  CHALLENGES, EDUCATION, STREAMS, GENDERS,
} from "../data/blueprint";

const STEP_TITLES = ["About You", "Your Interests", "Your Personality", "Your Goals"];

const defaultInterests = INTERESTS.reduce((a, i) => ({ ...a, [i.key]: 5 }), {});

export const Questionnaire = ({ onClose, onComplete }) => {
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [profile, setProfile] = useState({
    name: "", email: "", phone: "", age: "", gender: "", education: "", stream: "",
  });
  const [interests, setInterests] = useState(defaultInterests);
  const [personality, setPersonality] = useState({ mind: "", approach: "", risk: "", role: "" });
  const [goals, setGoals] = useState({ priorities: [], dream_income: "", challenge: "" });

  const progress = ((step + 1) / STEP_TITLES.length) * 100;

  const canNext = () => {
    if (step === 0) return profile.name.trim() && /\S+@\S+\.\S+/.test(profile.email);
    if (step === 2) return Object.values(personality).every(Boolean);
    if (step === 3) return goals.priorities.length > 0 && goals.dream_income && goals.challenge;
    return true;
  };

  const next = () => {
    setError("");
    if (!canNext()) {
      setError("Please complete the highlighted fields to continue.");
      return;
    }
    if (step < STEP_TITLES.length - 1) setStep(step + 1);
    else submit();
  };

  const togglePriority = (p) => {
    setGoals((g) => ({
      ...g,
      priorities: g.priorities.includes(p) ? g.priorities.filter((x) => x !== p) : [...g.priorities, p],
    }));
  };

  const submit = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await analyze({ ...profile, interests, personality, goals });
      onComplete(data);
    } catch (e) {
      setError("Something went wrong generating your analysis. Please try again.");
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] bg-white grad-mesh overflow-y-auto" data-testid="questionnaire">
      {/* Progress header */}
      <div className="sticky top-0 z-10 glass border-b border-slate-200/70">
        <div className="max-w-2xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <button onClick={onClose} data-testid="quiz-close-btn" className="text-slate-500 hover:text-slate-900 flex items-center gap-1.5 text-sm">
              <Icons.ChevronLeft className="w-4 h-4" /> Exit
            </button>
            <span className="font-mono text-xs text-purple-600 tracking-widest uppercase">
              Step {step + 1} / {STEP_TITLES.length} · {STEP_TITLES[step]}
            </span>
          </div>
          <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
            <motion.div className="h-full grad-primary-h" animate={{ width: `${progress}%` }} transition={{ duration: 0.4 }} />
          </div>
        </div>
      </div>

      {loading ? (
        <LoadingScreen name={profile.name} />
      ) : (
        <div className="max-w-2xl mx-auto px-6 py-10 pb-32">
          <AnimatePresence mode="wait">
            <motion.div
              key={step}
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -30 }}
              transition={{ duration: 0.35 }}
              data-testid={`questionnaire-step-${step + 1}`}
            >
              {step === 0 && <AboutStep profile={profile} setProfile={setProfile} />}
              {step === 1 && <InterestsStep interests={interests} setInterests={setInterests} />}
              {step === 2 && <PersonalityStep personality={personality} setPersonality={setPersonality} />}
              {step === 3 && (
                <GoalsStep goals={goals} setGoals={setGoals} togglePriority={togglePriority} />
              )}
            </motion.div>
          </AnimatePresence>

          {error && <p className="mt-6 text-rose-500 text-sm" data-testid="quiz-error">{error}</p>}

          <div className="mt-10 flex items-center justify-between">
            {step > 0 ? (
              <button onClick={() => setStep(step - 1)} className="text-slate-500 hover:text-slate-900 flex items-center gap-1.5">
                <Icons.ChevronLeft className="w-5 h-5" /> Back
              </button>
            ) : <span />}
            <CTAButton testid="questionnaire-next-btn" onClick={next}>
              {step === STEP_TITLES.length - 1 ? "Generate My Blueprint" : "Continue"}
            </CTAButton>
          </div>
        </div>
      )}
    </div>
  );
};

const Field = ({ label, children }) => (
  <div>
    <label className="block text-sm text-slate-700 mb-2 font-medium">{label}</label>
    {children}
  </div>
);

const inputCls =
  "w-full rounded-xl bg-white border border-slate-200 px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 focus:outline-none transition";

const Chip = ({ active, onClick, children, testid }) => (
  <button
    type="button"
    data-testid={testid}
    onClick={onClick}
    className={`px-4 py-2.5 rounded-full border text-sm font-medium transition-all ${
      active ? "border-transparent grad-primary-h text-white shadow-md shadow-purple-500/30" : "border-slate-200 bg-white text-slate-600 hover:border-purple-300"
    }`}
  >
    {children}
  </button>
);

const AboutStep = ({ profile, setProfile }) => {
  const up = (k) => (e) => setProfile({ ...profile, [k]: e.target.value });
  return (
    <div>
      <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">Let&apos;s start with you.</h2>
      <p className="text-slate-500 mb-8">Your blueprint is personalized — these details shape your results.</p>
      <div className="grid sm:grid-cols-2 gap-5">
        <Field label="Full Name *">
          <input data-testid="q-name" className={inputCls} value={profile.name} onChange={up("name")} placeholder="e.g. Aarav Sharma" />
        </Field>
        <Field label="Email *">
          <input data-testid="q-email" className={inputCls} value={profile.email} onChange={up("email")} placeholder="you@email.com" />
        </Field>
        <Field label="Phone">
          <input data-testid="q-phone" className={inputCls} value={profile.phone} onChange={up("phone")} placeholder="Optional" />
        </Field>
        <Field label="Age">
          <input data-testid="q-age" className={inputCls} value={profile.age} onChange={up("age")} placeholder="e.g. 18" />
        </Field>
        <Field label="Gender">
          <select data-testid="q-gender" className={inputCls} value={profile.gender} onChange={up("gender")}>
            <option value="">Select</option>
            {GENDERS.map((g) => <option key={g} value={g}>{g}</option>)}
          </select>
        </Field>
        <Field label="Education Level">
          <select data-testid="q-education" className={inputCls} value={profile.education} onChange={up("education")}>
            <option value="">Select</option>
            {EDUCATION.map((g) => <option key={g} value={g}>{g}</option>)}
          </select>
        </Field>
        <div className="sm:col-span-2">
          <Field label="Stream / Field">
            <select data-testid="q-stream" className={inputCls} value={profile.stream} onChange={up("stream")}>
              <option value="">Select</option>
              {STREAMS.map((g) => <option key={g} value={g}>{g}</option>)}
            </select>
          </Field>
        </div>
      </div>
    </div>
  );
};

const InterestsStep = ({ interests, setInterests }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">Rate your interests.</h2>
    <p className="text-slate-500 mb-8">Drag each slider from 1 (not interested) to 10 (love it).</p>
    <div className="space-y-6">
      {INTERESTS.map((it) => {
        const Icon = Icons[it.icon] || Icons.Sparkles;
        return (
          <div key={it.key} className="rounded-2xl bg-white border border-slate-100 p-4 soft-shadow">
            <div className="flex items-center justify-between mb-3">
              <span className="flex items-center gap-2.5 text-slate-800 font-medium">
                <span className="w-8 h-8 rounded-lg grad-primary flex items-center justify-center">
                  <Icon className="w-4 h-4 text-white" strokeWidth={1.9} />
                </span>
                {it.label}
              </span>
              <span className="font-mono text-purple-600 text-sm w-7 text-right">{interests[it.key]}</span>
            </div>
            <Slider
              data-testid={`q-interest-${it.key}`}
              min={1} max={10} step={1}
              value={[interests[it.key]]}
              onValueChange={(v) => setInterests({ ...interests, [it.key]: v[0] })}
              className="cb-slider"
            />
          </div>
        );
      })}
    </div>
  </div>
);

const PersonalityStep = ({ personality, setPersonality }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">How are you wired?</h2>
    <p className="text-slate-500 mb-8">Pick whatever feels most like you.</p>
    <div className="space-y-8">
      {PERSONALITY.map((p) => (
        <div key={p.key}>
          <p className="font-head font-600 text-lg mb-3 text-slate-900">{p.question}</p>
          <div className="grid sm:grid-cols-2 gap-3">
            {p.options.map((o) => {
              const active = personality[p.key] === o.value;
              return (
                <button
                  key={o.value}
                  type="button"
                  data-testid={`q-personality-${p.key}-${o.value}`}
                  onClick={() => setPersonality({ ...personality, [p.key]: o.value })}
                  className={`text-left rounded-2xl border p-4 transition-all ${
                    active ? "border-purple-400 bg-purple-50 ring-2 ring-purple-200" : "border-slate-200 bg-white hover:border-purple-300"
                  }`}
                >
                  <p className="font-head font-700 text-slate-900">{o.label}</p>
                  <p className="text-sm text-slate-500 mt-0.5">{o.desc}</p>
                </button>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  </div>
);

const GoalsStep = ({ goals, setGoals, togglePriority }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">What do you want?</h2>
    <p className="text-slate-500 mb-8">Be honest — there are no wrong answers.</p>

    <p className="font-head font-600 text-lg mb-3 text-slate-900">What matters most? <span className="text-slate-400 text-sm font-body">(pick any)</span></p>
    <div className="flex flex-wrap gap-2.5 mb-8">
      {GOAL_PRIORITIES.map((p) => (
        <Chip key={p} active={goals.priorities.includes(p)} onClick={() => togglePriority(p)} testid={`q-goal-${p}`}>
          {p}
        </Chip>
      ))}
    </div>

    <p className="font-head font-600 text-lg mb-3 text-slate-900">Your dream income?</p>
    <div className="flex flex-wrap gap-2.5 mb-8">
      {DREAM_INCOME.map((d) => (
        <Chip key={d.value} active={goals.dream_income === d.value} onClick={() => setGoals({ ...goals, dream_income: d.value })} testid={`q-income-${d.value}`}>
          {d.label}
        </Chip>
      ))}
    </div>

    <p className="font-head font-600 text-lg mb-3 text-slate-900">Your biggest challenge right now?</p>
    <div className="space-y-2.5">
      {CHALLENGES.map((c) => {
        const active = goals.challenge === c;
        return (
          <button
            key={c}
            type="button"
            data-testid={`q-challenge-${c}`}
            onClick={() => setGoals({ ...goals, challenge: c })}
            className={`w-full text-left rounded-2xl border px-4 py-3.5 transition-all ${
              active ? "border-purple-400 bg-purple-50 text-slate-900 ring-2 ring-purple-200" : "border-slate-200 bg-white text-slate-600 hover:border-purple-300"
            }`}
          >
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
    "Scoring 12 high-growth career paths…",
    "Calculating salary & AI-risk projections…",
    "Writing your personalized blueprint…",
  ];
  const [i, setI] = useState(0);
  React.useEffect(() => {
    const t = setInterval(() => setI((p) => Math.min(p + 1, lines.length - 1)), 1400);
    return () => clearInterval(t);
  }, []);
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] px-6 text-center" data-testid="quiz-loading">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: 2.4, ease: "linear" }}
        className="w-20 h-20 rounded-full border-4 border-purple-100 border-t-purple-500 mb-8"
      />
      <h3 className="font-head font-700 text-2xl sm:text-3xl mb-3 text-slate-900">
        Building {name ? name.split(" ")[0] + "'s" : "your"} Career Blueprint…
      </h3>
      <AnimatePresence mode="wait">
        <motion.p key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} className="text-purple-600 font-mono text-sm">
          {lines[i]}
        </motion.p>
      </AnimatePresence>
    </div>
  );
};
