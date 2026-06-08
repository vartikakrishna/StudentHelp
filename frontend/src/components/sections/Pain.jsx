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
  <section className="relative py-24 sm:py-32 border-y border-white/5" data-testid="pain-section">
    <div className="max-w-5xl mx-auto px-6 lg:px-8">
      <Reveal>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-amber-500 mb-4">The Uncomfortable Truth</p>
        <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight max-w-3xl">
          Most students study hard — in the <span className="text-gold">wrong direction.</span>
        </h2>
        <p className="mt-5 text-slate-400 text-lg max-w-2xl">
          Working harder on the wrong path doesn&apos;t get you there faster. It just makes the regret bigger.
        </p>
      </Reveal>

      <Stagger className="mt-12 grid sm:grid-cols-2 gap-5">
        {FEARS.map((f) => (
          <Item key={f}>
            <div className="group h-full rounded-xl border border-white/8 bg-[#091226] p-7 hover:border-amber-500/40 hover:-translate-y-1 transition-all duration-300">
              <HelpCircle className="w-7 h-7 text-amber-500 mb-4" strokeWidth={1.6} />
              <p className="font-head text-xl text-white leading-snug">{f}</p>
            </div>
          </Item>
        ))}
      </Stagger>

      <Reveal delay={0.1}>
        <p className="mt-12 text-center font-head text-2xl sm:text-3xl text-white">
          “What if I&apos;m spending years on the wrong path?”
        </p>
        <p className="mt-3 text-center text-slate-400">You don&apos;t have to wonder anymore.</p>
      </Reveal>
    </div>
  </section>
);
