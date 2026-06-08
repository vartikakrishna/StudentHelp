import React from "react";
import { Reveal } from "../Reveal";
import { X, Check, Frown, Smile, Compass, Sparkles } from "lucide-react";

const BEFORE = ["Confused about the future", "No clear direction", "Overwhelmed by options", "Afraid of wasting years"];
const AFTER = ["A clear, personalized roadmap", "Focused learning that compounds", "Confidence in your decisions", "Excited about your future"];

export const Transformation = () => (
  <section className="py-24 sm:py-32 bg-white" data-testid="transformation-section">
    <div className="max-w-7xl mx-auto px-6 lg:px-8">
      <Reveal>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-4 text-center">The Transformation</p>
        <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight text-center text-slate-900 mb-14">
          From confusion to <span className="text-gradient">clarity.</span>
        </h2>
      </Reveal>

      <div className="grid lg:grid-cols-2 gap-6 items-stretch">
        <Reveal>
          <div className="h-full rounded-3xl border border-rose-100 bg-rose-50/60 p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-11 h-11 rounded-2xl bg-rose-100 flex items-center justify-center">
                <Frown className="w-6 h-6 text-rose-500" strokeWidth={1.8} />
              </div>
              <p className="font-mono text-xs tracking-[0.2em] uppercase text-rose-500">Before</p>
            </div>
            <ul className="space-y-4">
              {BEFORE.map((b) => (
                <li key={b} className="flex items-start gap-3 text-slate-600">
                  <X className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" strokeWidth={2} />
                  {b}
                </li>
              ))}
            </ul>
          </div>
        </Reveal>

        <Reveal delay={0.12}>
          <div className="relative h-full rounded-3xl grad-primary p-8 overflow-hidden text-white glow-primary">
            <Sparkles className="absolute -top-4 -right-4 w-28 h-28 text-white/10" />
            <div className="relative flex items-center gap-3 mb-6">
              <div className="w-11 h-11 rounded-2xl bg-white/20 flex items-center justify-center">
                <Smile className="w-6 h-6 text-white" strokeWidth={1.8} />
              </div>
              <p className="font-mono text-xs tracking-[0.2em] uppercase text-white/90">After</p>
            </div>
            <ul className="relative space-y-4">
              {AFTER.map((a) => (
                <li key={a} className="flex items-start gap-3 text-white">
                  <Check className="w-5 h-5 text-white shrink-0 mt-0.5" strokeWidth={2.4} />
                  {a}
                </li>
              ))}
            </ul>
            <div className="relative mt-8 inline-flex items-center gap-2 rounded-full bg-white/15 px-4 py-2">
              <Compass className="w-4 h-4" />
              <span className="text-sm font-medium">Your personalized direction, unlocked.</span>
            </div>
          </div>
        </Reveal>
      </div>
    </div>
  </section>
);
