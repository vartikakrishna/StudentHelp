import React from "react";
import { Reveal } from "../Reveal";
import { Check, Clock } from "lucide-react";
import { CTAButton } from "../CTAButton";

const INCLUDES = [
  "12–15 page premium PDF report",
  "Top 5 personalized career matches",
  "Future salary projection (10 years)",
  "AI risk & resistance analysis",
  "Step-by-step learning roadmap",
  "Hidden strengths + growth obstacles",
  "A letter from your future self",
  "Instant download — yours forever",
];

export const Pricing = ({ onStart }) => (
  <section className="py-24 sm:py-32 bg-white" id="pricing" data-testid="pricing-section">
    <div className="max-w-5xl mx-auto px-6 lg:px-8">
      <Reveal>
        <div className="text-center mb-12">
          <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-4">Pricing</p>
          <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight text-slate-900">
            One wrong career decision can cost you <span className="text-gradient">years.</span>
          </h2>
          <p className="mt-4 text-slate-600 text-lg">Your personalized Career Blueprint costs less than a movie night.</p>
        </div>
      </Reveal>

      <Reveal delay={0.1}>
        <div className="relative rounded-[2rem] p-[1.5px] grad-primary glow-primary">
          <div className="rounded-[1.9rem] bg-white p-8 sm:p-12 overflow-hidden">
            <div className="grid md:grid-cols-2 gap-10 items-center">
              <div>
                <div className="flex items-end gap-3">
                  <span className="font-head font-800 text-6xl sm:text-7xl text-gradient">₹199</span>
                  <span className="text-slate-400 mb-3 line-through font-mono">₹999</span>
                </div>
                <p className="mt-2 inline-flex items-center gap-2 text-sm text-purple-600 font-mono bg-purple-50 rounded-full px-3 py-1">
                  <Clock className="w-4 h-4" /> Limited launch price
                </p>
                <p className="mt-6 text-slate-600">
                  A complete, personalized career blueprint generated in seconds and delivered as a premium PDF you can download instantly.
                </p>
                <div className="mt-8">
                  <CTAButton testid="pricing-unlock-btn" onClick={onStart}>Unlock My Full Career Blueprint</CTAButton>
                </div>
                <p className="mt-4 text-xs text-slate-400 font-mono">Secure payment · UPI · Cards · Net Banking · Wallets</p>
              </div>
              <ul className="space-y-3.5">
                {INCLUDES.map((i) => (
                  <li key={i} className="flex items-start gap-3 text-slate-700">
                    <span className="w-5 h-5 rounded-full grad-primary flex items-center justify-center shrink-0 mt-0.5">
                      <Check className="w-3.5 h-3.5 text-white" strokeWidth={3} />
                    </span>
                    {i}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </Reveal>
    </div>
  </section>
);
