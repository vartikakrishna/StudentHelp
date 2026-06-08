import React from "react";
import { motion } from "framer-motion";
import { CheckCircle2, Sparkles, ShieldCheck, TrendingUp } from "lucide-react";
import { CTAButton } from "../CTAButton";

const BENEFITS = [
  "Careers where you'll succeed",
  "Skills to build next",
  "Your real income potential",
  "AI-proof career options",
  "Your hidden strengths",
  "A personalized roadmap",
];

const MINI = [
  { label: "AI / ML Engineer", v: 96 },
  { label: "Product Manager", v: 88 },
  { label: "Data Scientist", v: 82 },
];

const HeroCard = () => (
  <motion.div
    initial={{ opacity: 0, y: 30, rotate: -2 }}
    animate={{ opacity: 1, y: 0, rotate: 0 }}
    transition={{ duration: 0.8, delay: 0.3 }}
    className="relative animate-floaty"
  >
    <div className="glass-card rounded-[2rem] p-7 ring-gradient max-w-sm mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <p className="font-mono text-[10px] tracking-[0.2em] uppercase text-indigo-500">Career Match</p>
          <p className="font-head font-700 text-slate-900">Your Blueprint</p>
        </div>
        <div className="relative w-20 h-20">
          <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
            <defs>
              <linearGradient id="heroGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#4F46E5" />
                <stop offset="50%" stopColor="#7C3AED" />
                <stop offset="100%" stopColor="#06B6D4" />
              </linearGradient>
            </defs>
            <circle cx="50" cy="50" r="42" fill="none" stroke="#E2E8F0" strokeWidth="9" />
            <motion.circle
              cx="50" cy="50" r="42" fill="none" stroke="url(#heroGrad)" strokeWidth="9" strokeLinecap="round"
              strokeDasharray={2 * Math.PI * 42}
              initial={{ strokeDashoffset: 2 * Math.PI * 42 }}
              animate={{ strokeDashoffset: 2 * Math.PI * 42 * (1 - 0.94) }}
              transition={{ duration: 1.6, delay: 0.6 }}
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="font-head font-800 text-lg text-gradient">94%</span>
          </div>
        </div>
      </div>
      {MINI.map((m, i) => (
        <div key={m.label} className="mb-3.5">
          <div className="flex justify-between text-xs mb-1.5">
            <span className="text-slate-600 font-medium">{m.label}</span>
            <span className="font-mono text-indigo-500">{m.v}%</span>
          </div>
          <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
            <motion.div className="h-full grad-primary-h rounded-full"
              initial={{ width: 0 }} animate={{ width: `${m.v}%` }} transition={{ duration: 1, delay: 0.7 + i * 0.15 }} />
          </div>
        </div>
      ))}
      <div className="mt-5 grid grid-cols-2 gap-3">
        <div className="rounded-2xl bg-indigo-50 p-3">
          <ShieldCheck className="w-4 h-4 text-indigo-500 mb-1" />
          <p className="font-head font-700 text-slate-900 text-sm">95% AI-proof</p>
        </div>
        <div className="rounded-2xl bg-cyan-50 p-3">
          <TrendingUp className="w-4 h-4 text-cyan-500 mb-1" />
          <p className="font-head font-700 text-slate-900 text-sm">₹28 LPA</p>
        </div>
      </div>
    </div>
  </motion.div>
);

export const Hero = ({ onStart }) => (
  <section className="relative min-h-screen flex items-center overflow-hidden grad-mesh" data-testid="hero-section">
    <div className="blob w-[420px] h-[420px] bg-indigo-300/50 -top-24 -left-20" />
    <div className="blob w-[380px] h-[380px] bg-purple-300/50 top-10 right-10" style={{ animationDelay: "3s" }} />
    <div className="blob w-[360px] h-[360px] bg-cyan-300/50 bottom-0 left-1/3" style={{ animationDelay: "6s" }} />

    <div className="relative max-w-7xl mx-auto px-6 lg:px-8 pt-28 pb-16 w-full grid lg:grid-cols-2 gap-12 items-center">
      <div>
        <motion.div
          initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}
          className="inline-flex items-center gap-2 rounded-full glass px-4 py-1.5 mb-7 soft-shadow"
        >
          <Sparkles className="w-4 h-4 text-purple-500" />
          <span className="font-mono text-xs tracking-[0.15em] uppercase text-slate-700">AI Career Intelligence</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.1 }}
          className="font-head font-800 tracking-tight leading-[1.05] text-4xl sm:text-5xl lg:text-6xl text-slate-900"
        >
          Don&apos;t Spend 4 Years Preparing For The <span className="text-gradient">Wrong Career.</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.25 }}
          className="mt-6 text-base sm:text-lg text-slate-600 max-w-xl leading-relaxed"
        >
          AI analyzes your strengths, career fit, salary potential, future demand and AI
          disruption risk to build your personalized career roadmap — a brutally honest truth report, not a motivation test.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.35 }}
          className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2.5 max-w-lg"
        >
          {BENEFITS.map((b) => (
            <div key={b} className="flex items-center gap-2.5 text-slate-700 text-sm sm:text-base">
              <CheckCircle2 className="w-5 h-5 text-purple-500 shrink-0" strokeWidth={1.8} />
              {b}
            </div>
          ))}
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.5 }}
          className="mt-10 flex flex-col sm:flex-row items-start sm:items-center gap-4"
        >
          <CTAButton testid="start-analysis-btn" onClick={onStart}>Start Free Analysis</CTAButton>
          <span className="text-slate-500 text-sm font-mono">No signup · Under 2 min · Free preview</span>
        </motion.div>
      </div>

      <HeroCard />
    </div>
  </section>
);
