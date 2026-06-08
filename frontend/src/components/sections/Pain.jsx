import React from "react";
import { Reveal, Stagger, Item } from "../Reveal";
import { HelpCircle } from "lucide-react";

const FEARS = [
  "What if your current career choice is completely wrong?",
  "What if your real strengths are being ignored right now?",
  "What if 5 years from now you realize you chose the wrong path?",
  "What if AI replaces the exact career you're preparing for?",
];

export const Pain = ({ onStart }) => (
  <section className="relative py-24 sm:py-32 grad-soft" data-testid="pain-section">
    <div className="max-w-5xl mx-auto px-6 lg:px-8">
      <Reveal>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-4">The Uncomfortable Truth</p>
        <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight max-w-3xl text-slate-900">
          Most students study hard — in the <span className="text-gradient">wrong direction.</span>
        </h2>
        <p className="mt-5 text-slate-600 text-lg max-w-2xl">
          Working harder on the wrong path doesn&apos;t get you there faster. It just makes the regret bigger.
        </p>
      </Reveal>

      <Stagger className="mt-12 grid sm:grid-cols-2 gap-5">
        {FEARS.map((f) => (
          <Item key={f}>
            <div className="group h-full rounded-3xl glass-card p-7 hover:-translate-y-1.5 hover:shadow-[0_20px_50px_-12px_rgba(124,58,237,0.28)] transition-all duration-300">
              <div className="w-12 h-12 rounded-2xl grad-primary flex items-center justify-center mb-5 shadow-md shadow-purple-500/30">
                <HelpCircle className="w-6 h-6 text-white" strokeWidth={1.8} />
              </div>
              <p className="font-head text-xl text-slate-800 leading-snug">{f}</p>
            </div>
          </Item>
        ))}
      </Stagger>

      <Reveal delay={0.1}>
        <p className="mt-14 text-center font-head font-700 text-2xl sm:text-3xl text-slate-900">
          “What if I&apos;m spending years on the wrong path?”
        </p>
        <p className="mt-3 text-center text-slate-500">You don&apos;t have to wonder anymore.</p>
      </Reveal>
    </div>
  </section>
);
