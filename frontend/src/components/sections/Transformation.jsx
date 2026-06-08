import React from "react";
import { Reveal } from "../Reveal";
import { X, Check } from "lucide-react";

const BEFORE = ["Confused about the future", "No clear direction", "Overwhelmed by options", "Afraid of wasting years"];
const AFTER = ["A clear, personalised roadmap", "Focused learning that compounds", "Confidence in your decisions", "Excited about your future"];

export const Transformation = () => (
  <section className="py-24 sm:py-32" data-testid="transformation-section">
    <div className="max-w-7xl mx-auto px-6 lg:px-8">
      <div className="grid lg:grid-cols-2 gap-10 items-center">
        <Reveal>
          <div className="relative rounded-3xl overflow-hidden border border-white/10 h-[420px]">
            <img
              src="https://images.unsplash.com/photo-1760004941335-6feccb7f800a?crop=entropy&cs=srgb&fm=jpg&q=85&w=1200"
              alt="Confident student"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-[#040914] via-transparent to-transparent" />
            <div className="absolute bottom-6 left-6">
              <p className="font-mono text-xs tracking-[0.2em] uppercase text-amber-400">The Transformation</p>
              <p className="font-head font-700 text-2xl">From confusion to clarity.</p>
            </div>
          </div>
        </Reveal>

        <Reveal delay={0.1}>
          <div className="grid sm:grid-cols-2 gap-5">
            <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-7">
              <p className="font-mono text-xs tracking-[0.2em] uppercase text-red-400 mb-5">Before</p>
              <ul className="space-y-4">
                {BEFORE.map((b) => (
                  <li key={b} className="flex items-start gap-3 text-slate-300">
                    <X className="w-5 h-5 text-red-400 shrink-0 mt-0.5" strokeWidth={2} />
                    {b}
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-2xl border border-amber-500/30 bg-amber-500/5 p-7">
              <p className="font-mono text-xs tracking-[0.2em] uppercase text-amber-400 mb-5">After</p>
              <ul className="space-y-4">
                {AFTER.map((a) => (
                  <li key={a} className="flex items-start gap-3 text-white">
                    <Check className="w-5 h-5 text-gold shrink-0 mt-0.5" strokeWidth={2} />
                    {a}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </Reveal>
      </div>
    </div>
  </section>
);
