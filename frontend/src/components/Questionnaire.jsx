import React, { useState } from "react";
import * as Icons from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Slider } from "./ui/slider";
import { analyze } from "../lib/api";
import { CTAButton } from "./CTAButton";
import { USER_TYPES, COUNTRIES } from "../data/blueprint";
import { stepsFor, metaFor, PERSONALITY_BINARY, PERSONALITY_SLIDERS, PERSONALITY_KEYS } from "../data/questionnaires";

const inputCls = "w-full rounded-xl bg-white border border-slate-200 px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 focus:outline-none transition";
const defaultPers = { mind: "", approach: "", risk: "", work_style: "", structure: "", leadership_interest: 5, communication: 5, stress_tolerance: 5 };

export const Questionnaire = ({ onClose, onComplete }) => {
  const [stepIdx, setStepIdx] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [p, setP] = useState({ name: "", email: "", phone: "", country: "India", user_type: "" });
  const [answers, setAnswers] = useState({});
  const [pers, setPers] = useState(defaultPers);

  const catSteps = p.user_type ? stepsFor(p.user_type) : [];
  const steps = ["usertype", ...(p.user_type ? ["value", "about", ...catSteps.map((s) => s.id), "personality"] : [])];
  const step = steps[stepIdx];
  const progress = ((stepIdx + 1) / steps.length) * 100;
  const catStep = catSteps.find((s) => s.id === step);
  const meta = p.user_type ? metaFor(p.user_type) : null;

  const setAns = (k, v) => setAnswers((a) => ({ ...a, [k]: v }));

  const canNext = () => {
    if (step === "usertype") return !!p.user_type;
    if (step === "about") return p.name.trim() && /\S+@\S+\.\S+/.test(p.email);
    if (step === "personality") return PERSONALITY_KEYS.every((k) => pers[k]);
    if (catStep) return catStep.fields.every((f) => {
      if (!f.required) return true;
      const v = answers[f.key];
      return f.type === "multiselect" ? Array.isArray(v) && v.length > 0 : !!v;
    });
    return true;
  };

  const next = () => {
    setError("");
    if (!canNext()) { setError("Please complete the highlighted fields to continue."); return; }
    if (stepIdx < steps.length - 1) setStepIdx(stepIdx + 1); else submit();
  };

  const submit = async () => {
    setLoading(true); setError("");
    try {
      const data = await analyze({ name: p.name, email: p.email, phone: p.phone, country: p.country, user_type: p.user_type, answers, personality: pers });
      onComplete(data);
    } catch (e) {
      setError("Something went wrong generating your analysis. Please try again.");
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] bg-white grad-mesh overflow-y-auto" data-testid="questionnaire">
      <div className="sticky top-0 z-10 glass border-b border-slate-200/70">
        <div className="max-w-2xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <button onClick={onClose} data-testid="quiz-close-btn" className="text-slate-500 hover:text-slate-900 flex items-center gap-1.5 text-sm"><Icons.ChevronLeft className="w-4 h-4" /> Exit</button>
            <span className="font-mono text-xs text-purple-600 tracking-widest uppercase">Step {stepIdx + 1} / {steps.length}</span>
          </div>
          <div className="h-2 rounded-full bg-slate-100 overflow-hidden"><motion.div className="h-full grad-primary-h" animate={{ width: `${progress}%` }} transition={{ duration: 0.4 }} /></div>
        </div>
      </div>

      {loading ? <LoadingScreen name={p.name} product={meta?.product} /> : (
        <div className="max-w-2xl mx-auto px-6 py-10 pb-32">
          <AnimatePresence mode="wait">
            <motion.div key={step} initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }} transition={{ duration: 0.3 }} data-testid={`questionnaire-step-${stepIdx + 1}`}>
              {step === "usertype" && <UserTypeStep p={p} setP={setP} />}
              {step === "value" && <ValueStep meta={meta} userType={p.user_type} />}
              {step === "about" && <AboutStep p={p} setP={setP} />}
              {catStep && <CategoryStep step={catStep} answers={answers} setAns={setAns} />}
              {step === "personality" && <PersonalityStep pers={pers} setPers={setPers} />}
            </motion.div>
          </AnimatePresence>

          {error && <p className="mt-6 text-rose-500 text-sm" data-testid="quiz-error">{error}</p>}

          <div className="mt-10 flex items-center justify-between">
            {stepIdx > 0 ? <button onClick={() => setStepIdx(stepIdx - 1)} className="text-slate-500 hover:text-slate-900 flex items-center gap-1.5"><Icons.ChevronLeft className="w-5 h-5" /> Back</button> : <span />}
            <CTAButton testid="questionnaire-next-btn" onClick={next}>{stepIdx === steps.length - 1 ? "Generate My Report" : step === "value" ? "Start My Analysis" : "Continue"}</CTAButton>
          </div>
        </div>
      )}
    </div>
  );
};

const Field = ({ label, children }) => (<div><label className="block text-sm text-slate-700 mb-2 font-medium">{label}</label>{children}</div>);
const Sel = ({ testid, value, onChange, options, placeholder = "Select" }) => (
  <select data-testid={testid} className={inputCls} value={value || ""} onChange={onChange}><option value="">{placeholder}</option>{options.map((o) => <option key={o} value={o}>{o}</option>)}</select>
);
const Chip = ({ active, onClick, children, testid }) => (
  <button type="button" data-testid={testid} onClick={onClick} className={`px-4 py-2.5 rounded-full border text-sm font-medium transition-all ${active ? "border-transparent grad-primary-h text-white shadow-md shadow-purple-500/30" : "border-slate-200 bg-white text-slate-600 hover:border-purple-300"}`}>{children}</button>
);

const UserTypeStep = ({ p, setP }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">Who are you right now?</h2>
    <p className="text-slate-500 mb-8">Each profile gets a completely different report built for your situation.</p>
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {USER_TYPES.map((u) => {
        const Icon = Icons[u.icon] || Icons.User;
        const active = p.user_type === u.value;
        return (
          <button key={u.value} type="button" data-testid={`q-usertype-${u.value}`} onClick={() => setP({ ...p, user_type: u.value })}
            className={`flex flex-col items-center gap-2 rounded-2xl border p-4 transition-all ${active ? "border-purple-400 bg-purple-50 ring-2 ring-purple-200" : "border-slate-200 bg-white hover:border-purple-300"}`}>
            <span className={`w-11 h-11 rounded-xl flex items-center justify-center ${active ? "grad-primary" : "bg-slate-100"}`}><Icon className={`w-5 h-5 ${active ? "text-white" : "text-slate-500"}`} strokeWidth={1.8} /></span>
            <span className="text-sm font-medium text-slate-800 text-center leading-tight">{u.label}</span>
          </button>
        );
      })}
    </div>
  </div>
);

const ValueStep = ({ meta, userType }) => {
  const Icon = Icons[meta.icon] || Icons.Sparkles;
  return (
    <div data-testid="category-value-screen">
      <div className="inline-flex items-center gap-2 rounded-full glass px-4 py-1.5 mb-5 soft-shadow"><Icon className="w-4 h-4 text-purple-500" /><span className="font-mono text-xs tracking-widest uppercase text-slate-700">{userType}</span></div>
      <h2 className="font-head font-800 text-3xl sm:text-4xl mb-2 text-slate-900">Your {meta.product}</h2>
      <p className="text-slate-500 mb-8 text-lg">{meta.tagline}</p>
      <p className="font-head font-600 text-slate-900 mb-4">Here is exactly what you will get:</p>
      <div className="grid sm:grid-cols-2 gap-3">
        {meta.value.map((v) => (
          <div key={v} className="flex items-center gap-2.5 rounded-2xl border border-slate-100 bg-white p-3.5 soft-shadow" data-testid={`value-prop-${v}`}>
            <span className="w-7 h-7 rounded-lg grad-primary flex items-center justify-center shrink-0"><Icons.Check className="w-4 h-4 text-white" strokeWidth={2.5} /></span>
            <span className="text-slate-800 text-sm font-medium">{v}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

const AboutStep = ({ p, setP }) => {
  const up = (k) => (e) => setP({ ...p, [k]: e.target.value });
  return (
    <div>
      <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">A bit about you.</h2>
      <p className="text-slate-500 mb-8">So we can personalise and email your report.</p>
      <div className="grid sm:grid-cols-2 gap-5">
        <Field label="Full Name *"><input data-testid="q-name" className={inputCls} value={p.name} onChange={up("name")} placeholder="e.g. Aarav Sharma" /></Field>
        <Field label="Email *"><input data-testid="q-email" className={inputCls} value={p.email} onChange={up("email")} placeholder="you@email.com" /></Field>
        <Field label="Phone"><input data-testid="q-phone" className={inputCls} value={p.phone} onChange={up("phone")} placeholder="Optional" /></Field>
        <Field label="Country"><Sel testid="q-country" value={p.country} onChange={up("country")} options={COUNTRIES} /></Field>
      </div>
    </div>
  );
};

const CategoryStep = ({ step, answers, setAns }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">{step.title}</h2>
    {step.subtitle && <p className="text-slate-500 mb-8">{step.subtitle}</p>}
    <div className="grid sm:grid-cols-2 gap-5">
      {step.fields.map((f) => (
        <div key={f.key} className={f.type === "multiselect" || f.type === "slider" || !f.half ? "sm:col-span-2" : ""}>
          <FieldInput f={f} value={answers[f.key]} setAns={setAns} />
        </div>
      ))}
    </div>
  </div>
);

const FieldInput = ({ f, value, setAns }) => {
  const label = f.label + (f.required ? " *" : "");
  if (f.type === "select") return <Field label={label}><Sel testid={`q-${f.key}`} value={value} onChange={(e) => setAns(f.key, e.target.value)} options={f.options} /></Field>;
  if (f.type === "number") return <Field label={label}><input data-testid={`q-${f.key}`} type="number" className={inputCls} value={value || ""} onChange={(e) => setAns(f.key, e.target.value)} placeholder={f.placeholder} /></Field>;
  if (f.type === "text") return <Field label={label}><input data-testid={`q-${f.key}`} className={inputCls} value={value || ""} onChange={(e) => setAns(f.key, e.target.value)} placeholder={f.placeholder} /></Field>;
  if (f.type === "slider") {
    const v = value || 5;
    return (
      <div className="rounded-2xl bg-white border border-slate-100 p-4 soft-shadow">
        <div className="flex items-center justify-between mb-3"><span className="text-slate-800 font-medium">{label}</span><span className="font-mono text-purple-600 text-sm">{v}</span></div>
        <Slider data-testid={`q-${f.key}`} min={1} max={10} step={1} value={[v]} onValueChange={(arr) => setAns(f.key, arr[0])} className="cb-slider" />
      </div>
    );
  }
  // multiselect
  const arr = Array.isArray(value) ? value : [];
  const toggle = (o) => setAns(f.key, arr.includes(o) ? arr.filter((x) => x !== o) : [...arr, o]);
  return (
    <div>
      <label className="block text-sm text-slate-700 mb-2 font-medium">{label}</label>
      <div className="flex flex-wrap gap-2.5">
        {f.options.map((o) => <Chip key={o} active={arr.includes(o)} onClick={() => toggle(o)} testid={`q-${f.key}-${o}`}>{o}</Chip>)}
      </div>
    </div>
  );
};

const PersonalityStep = ({ pers, setPers }) => (
  <div>
    <h2 className="font-head font-700 text-3xl mb-2 text-slate-900">How are you wired?</h2>
    <p className="text-slate-500 mb-8">Eight quick reads — we use these to tailor your recommendations.</p>
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
                  <p className="font-head font-700 text-slate-900">{o.label}</p><p className="text-sm text-slate-500 mt-0.5">{o.desc}</p>
                </button>
              );
            })}
          </div>
        </div>
      ))}
      <div className="space-y-5 pt-2">
        {PERSONALITY_SLIDERS.map((s) => (
          <div key={s.key} className="rounded-2xl bg-white border border-slate-100 p-4 soft-shadow">
            <div className="flex items-center justify-between mb-3"><span className="text-slate-800 font-medium">{s.label}</span><span className="font-mono text-purple-600 text-sm">{pers[s.key]}</span></div>
            <Slider data-testid={`q-pslider-${s.key}`} min={1} max={10} step={1} value={[pers[s.key]]} onValueChange={(v) => setPers({ ...pers, [s.key]: v[0] })} className="cb-slider" />
          </div>
        ))}
      </div>
    </div>
  </div>
);

const LoadingScreen = ({ name, product }) => {
  const lines = ["Analysing your answers…", "Running your category-specific scoring model…", "Building your honest recommendations…", `Finalising your ${product || "report"}…`];
  const [i, setI] = useState(0);
  React.useEffect(() => { const t = setInterval(() => setI((x) => Math.min(x + 1, lines.length - 1)), 1500); return () => clearInterval(t); }, []);
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] px-6 text-center" data-testid="quiz-loading">
      <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 2.4, ease: "linear" }} className="w-20 h-20 rounded-full border-4 border-purple-100 border-t-purple-500 mb-8" />
      <h3 className="font-head font-700 text-2xl sm:text-3xl mb-3 text-slate-900">Building {name ? name.split(" ")[0] + "'s" : "your"} report…</h3>
      <AnimatePresence mode="wait"><motion.p key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} className="text-purple-600 font-mono text-sm">{lines[i]}</motion.p></AnimatePresence>
    </div>
  );
};
