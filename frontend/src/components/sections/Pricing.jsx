import React from "react";
import { Reveal } from "../Reveal";
import { Check, Clock } from "lucide-react";
import { CTAButton } from "../CTAButton";

const INCLUDES = [
  "12–15 page premium PDF report",
  "Top 5 personalised career matches",
  "Future salary projection (10 years)",
  "AI risk & resistance analysis",
  "Step-by-step learning roadmap",
  "Hidden strengths + growth obstacles",
  "A letter from your future self",
  "Instant download — yours forever",
];

export const Pricing = ({ onStart }) => (
  <section className="py-24 sm:py-32" id="pricing" data-testid="pricing-section">
    <div className="max-w-5xl mx-auto px-6 lg:px-8">
      <Reveal>
        <div className="text-center mb-12">
          <p className="font-mono text-xs tracking-[0.2em] uppercase text-amber-500 mb-4">Pricing</p>
          <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight">
            One wrong career decision can cost you <span className="text-gold">years.</span>
          </h2>
          <p className="mt-4 text-slate-400 text-lg">Your personalised Career Blueprint costs less than a movie night.</p>
        </div>
      </Reveal>

      <Reveal delay={0.1}>
        <div className="relative rounded-3xl border border-amber-500/30 bg-gradient-to-b from-[#0C1730] to-[#091226] p-8 sm:p-12 overflow-hidden">
          <div className="absolute -top-24 -right-24 w-72 h-72 rounded-full bg-amber-500/10 blur-3xl" />
          <div className="relative grid md:grid-cols-2 gap-10 items-center">
            <div>
              <div className="flex items-end gap-2">
                <span className="font-head font-800 text-6xl sm:text-7xl text-gold text-glow">₹199</span>
                <span className="text-slate-400 mb-3 line-through font-mono">₹1,499</span>
              </div>
              <p className="mt-2 inline-flex items-center gap-2 text-sm text-amber-300 font-mono">
                <Clock className="w-4 h-4" /> Limited launch price
              </p>
              <p className="mt-6 text-slate-300">
                A complete, personalised career blueprint generated in seconds and delivered as a premium PDF you can download instantly.
              </p>
              <div className="mt-8">
                <CTAButton testid="pricing-unlock-btn" onClick={onStart}>Unlock My Full Career Blueprint</CTAButton>
              </div>
              <p className="mt-4 text-xs text-slate-500 font-mono">Secure payment · UPI · Cards · Net Banking · Wallets</p>
            </div>
            <ul className="space-y-3.5">
              {INCLUDES.map((i) => (
                <li key={i} className="flex items-start gap-3 text-slate-200">
                  <span className="w-5 h-5 rounded-full bg-amber-500/15 flex items-center justify-center shrink-0 mt-0.5">
                    <Check className="w-3.5 h-3.5 text-gold" strokeWidth={2.5} />
                  </span>
                  {i}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Reveal>
    </div>
  </section>
);
