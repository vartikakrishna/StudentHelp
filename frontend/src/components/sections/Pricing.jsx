import React from "react";
import * as Icons from "lucide-react";
import { Reveal } from "../Reveal";
import { Check, X } from "lucide-react";
import { CTAButton } from "../CTAButton";
import { PLAN_CONFIG, COMPARISON } from "../../data/blueprint";

const PlanCard = ({ cfg, featured, onStart }) => (
  <div className={`relative rounded-[2rem] p-[1.5px] ${featured ? "grad-primary glow-primary" : "bg-slate-200"}`}>
    {featured && <span className="absolute -top-3 left-1/2 -translate-x-1/2 z-10 text-[11px] font-mono bg-white text-purple-700 border border-purple-200 rounded-full px-3 py-1 shadow">MOST POPULAR</span>}
    <div className="rounded-[1.9rem] bg-white p-7 sm:p-8 h-full flex flex-col">
      <p className="font-mono text-xs tracking-[0.18em] uppercase text-purple-500 mb-2">{cfg.name}</p>
      <h3 className="font-head font-700 text-xl text-slate-900 leading-snug mb-3">{cfg.headline}</h3>
      <div className="flex items-end gap-2 mb-1">
        <span className="font-head font-800 text-5xl text-gradient">₹{cfg.price}</span>
        <span className="text-slate-400 mb-2 line-through font-mono text-sm">₹{cfg.original}</span>
      </div>
      <p className="text-xs text-slate-400 font-mono mb-4">{cfg.footnote}</p>
      <div className="flex flex-wrap gap-1.5 mb-5">
        {cfg.perfectFor.map((x) => <span key={x} className="text-[11px] rounded-full bg-slate-100 text-slate-600 px-2.5 py-1">{x}</span>)}
      </div>
      <ul className="space-y-2.5 mb-7 flex-1">
        {cfg.features.slice(0, featured ? 14 : 9).map((f) => (
          <li key={f} className="flex items-start gap-2.5 text-slate-700 text-sm">
            <span className="w-4.5 h-4.5 rounded-full grad-primary flex items-center justify-center shrink-0 mt-0.5"><Check className="w-3 h-3 text-white" strokeWidth={3} /></span>{f}
          </li>
        ))}
      </ul>
      <CTAButton testid={`pricing-cta-${cfg.key}`} onClick={onStart} className="w-full">{cfg.ctaText}</CTAButton>
    </div>
  </div>
);

const Tick = ({ on }) => on ? <Check className="w-4 h-4 text-emerald-500 mx-auto" strokeWidth={3} /> : <X className="w-4 h-4 text-slate-300 mx-auto" strokeWidth={3} />;

export const Pricing = ({ onStart }) => (
  <section className="py-24 sm:py-32 bg-white" id="pricing" data-testid="pricing-section">
    <div className="max-w-6xl mx-auto px-6 lg:px-8">
      <Reveal>
        <div className="text-center mb-12">
          <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-4">Pricing</p>
          <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight text-slate-900">
            Pick the plan that <span className="text-gradient">fits your stage.</span>
          </h2>
          <p className="mt-4 text-slate-600 text-lg">One career mistake can cost years of lost income. Your blueprint costs less than a movie night.</p>
        </div>
      </Reveal>

      <Reveal delay={0.1}>
        <div className="grid md:grid-cols-2 gap-6 items-stretch">
          <PlanCard cfg={PLAN_CONFIG.student} onStart={onStart} />
          <PlanCard cfg={PLAN_CONFIG.professional} featured onStart={onStart} />
        </div>
      </Reveal>

      <Reveal delay={0.15}>
        <div className="mt-12 rounded-[2rem] glass-card p-6 sm:p-8 overflow-x-auto">
          <h3 className="font-head font-700 text-lg text-slate-900 mb-6 text-center">Student ₹199 vs Professional ₹499</h3>
          <div className="grid grid-cols-[1fr_auto_auto] text-sm min-w-[420px]" data-testid="pricing-comparison">
            <div className="px-4 py-3 bg-slate-50 font-bold text-slate-600 font-mono text-xs">Feature</div>
            <div className="px-4 py-3 bg-slate-50 text-center font-bold text-slate-600 font-mono text-xs">Student ₹199</div>
            <div className="px-4 py-3 bg-purple-50 text-center font-bold text-purple-700 font-mono text-xs">Pro ₹499</div>
            {COMPARISON.map((row, i) => (
              <React.Fragment key={row.feature}>
                <div className={`px-4 py-2.5 text-slate-700 ${i % 2 ? "bg-slate-50/50" : ""}`}>{row.feature}</div>
                <div className={`px-4 py-2.5 ${i % 2 ? "bg-slate-50/50" : ""}`}><Tick on={row.student} /></div>
                <div className={`px-4 py-2.5 ${i % 2 ? "bg-purple-50/40" : "bg-purple-50/20"}`}><Tick on={row.pro} /></div>
              </React.Fragment>
            ))}
          </div>
        </div>
      </Reveal>
    </div>
  </section>
);
