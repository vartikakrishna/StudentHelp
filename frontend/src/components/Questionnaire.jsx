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
    <div className="fixed inset-0 z-[100] bg-[#040914] overflow-y-auto" data-testid="questionnaire">
      {/* Progress header */}
      <div className="sticky top-0 z-10 bg-[#040914]/90 backdrop-blur-xl border-b border-white/8">
        <div className="max-w-2xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <button onClick={onClose} data-testid="quiz-close-btn" className="text-slate-400 hover:text-white flex items-center gap-1.5 text-sm">
              <Icons.ChevronLeft className="w-4 h-4" /> Exit
            </button>
            <span className="font-mono text-xs text-amber-500 tracking-widest uppercase">
              Step {step + 1} / {STEP_TITLES.length} · {STEP_TITLES[step]}
            </span>
          </div>
          <div className="h-1.5 rounded-full bg-[#1E293B] overflow-hidden">
            <motion.div className="h-full gold-gradient" animate={{ width: `${progress}%` }} transition={{ duration: 0.4 }} />
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

          {error && <p className="mt-6 text-red-400 text-sm" data-testid="quiz-error">{error}</p>}

          <div className="mt-10 flex items-center justify-between">
            {step > 0 ? (
              <button onClick={() => setStep(step - 1)} className="text-slate-400 hover:text-white flex items-center gap-1.5">
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
    <label className="block text-sm text-slate-300 mb-2 font-medium">{label}</label>
    {children}
  </div>
);

const inputCls =
  "w-full rounded-lg bg-[#091226] border border-white/10 px-4 py-3 text-white placeholder:text-slate-500 focus:border-amber-500/60 focus:ring-2 focus:ring-amber-500/30 focus:outline-none transition";

const Chip = ({ active, onClick, children, testid }) => (
  <button
    type="button"
    data-testid={testid}
    onClick={onClick}
    className={`px-4 py-2.5 rounded-lg border text-sm font-medium transition-all ${
      active ? "border-amber-500 bg-amber-500/15 text-white" : "border-white/10 bg-[#091226] text-slate-300 hover:border-white/25"
    }`}
  >
    {children}
  </button>
);

const AboutStep = ({ profile, setProfile }) => {
  const up = (k) => (e) => setProfile({ ...profile, [k]: e.target.value });
  return (
    <div>
      <h2 className="font-head font-700 text-3xl mb-2">Let&apos;s start with you.</h2>
      <p className="text-slate-400 mb-8">Your blueprint is personalised — these details shape your results.</p>
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
    <h2 className="font-head font-700 text-3xl mb-2">Rate your interests.</h2>
    <p className="text-slate-400 mb-8">Drag each slider from 1 (not interested) to 10 (love it).</p>
    <div className="space-y-6">
      {INTERESTS.map((it) => {
        const Icon = Icons[it.icon] || Icons.Sparkles;
        return (
          <div key={it.key}>
            <div className="flex items-center justify-between mb-2">
              <span className="flex items-center gap-2.5 text-white font-medium">
                <Icon className="w-4 h-4 text-gold" strokeWidth={1.8} /> {it.label}
              </span>
              <span className="font-mono text-gold text-sm w-7 text-right">{interests[it.key]}</span>
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
    <h2 className="font-head font-700 text-3xl mb-2">How are you wired?</h2>
    <p className="text-slate-400 mb-8">Pick whatever feels most like you.</p>
    <div className="space-y-8">
      {PERSONALITY.map((p) => (
        <div key={p.key}>
          <p className="font-head text-lg mb-3">{p.question}</p>
          <div className="grid sm:grid-cols-2 gap-3">
            {p.options.map((o) => {
              const active = personality[p.key] === o.value;
              return (
                <button
                  key={o.value}
                  type="button"
                  data-testid={`q-personality-${p.key}-${o.value}`}
                  onClick={() => setPersonality({ ...personality, [p.key]: o.value })}
                  className={`text-left rounded-xl border p-4 transition-all ${
                    active ? "border-amber-500 bg-amber-500/15" : "border-white/10 bg-[#091226] hover:border-white/25"
                  }`}
                >
                  <p className="font-head font-700 text-white">{o.label}</p>
                  <p className="text-sm text-slate-400 mt-0.5">{o.desc}</p>
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
    <h2 className="font-head font-700 text-3xl mb-2">What do you want?</h2>
    <p className="text-slate-400 mb-8">Be honest — there are no wrong answers.</p>

    <p className="font-head text-lg mb-3">What matters most? <span className="text-slate-500 text-sm font-body">(pick any)</span></p>
    <div className="flex flex-wrap gap-2.5 mb-8">
      {GOAL_PRIORITIES.map((p) => (
        <Chip key={p} active={goals.priorities.includes(p)} onClick={() => togglePriority(p)} testid={`q-goal-${p}`}>
          {p}
        </Chip>
      ))}
    </div>

    <p className="font-head text-lg mb-3">Your dream income?</p>
    <div className="flex flex-wrap gap-2.5 mb-8">
      {DREAM_INCOME.map((d) => (
        <Chip key={d.value} active={goals.dream_income === d.value} onClick={() => setGoals({ ...goals, dream_income: d.value })} testid={`q-income-${d.value}`}>
          {d.label}
        </Chip>
      ))}
    </div>

    <p className="font-head text-lg mb-3">Your biggest challenge right now?</p>
    <div className="space-y-2.5">
      {CHALLENGES.map((c) => {
        const active = goals.challenge === c;
        return (
          <button
            key={c}
            type="button"
            data-testid={`q-challenge-${c}`}
            onClick={() => setGoals({ ...goals, challenge: c })}
            className={`w-full text-left rounded-xl border px-4 py-3.5 transition-all ${
              active ? "border-amber-500 bg-amber-500/15 text-white" : "border-white/10 bg-[#091226] text-slate-300 hover:border-white/25"
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
    "Writing your personalised blueprint…",
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
        className="w-20 h-20 rounded-full border-2 border-amber-500/20 border-t-amber-500 mb-8"
      />
      <h3 className="font-head font-700 text-2xl sm:text-3xl mb-3">
        Building {name ? name.split(" ")[0] + "'s" : "your"} Career Blueprint…
      </h3>
      <AnimatePresence mode="wait">
        <motion.p key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} className="text-amber-400 font-mono text-sm">
          {lines[i]}
        </motion.p>
      </AnimatePresence>
    </div>
  );
};
