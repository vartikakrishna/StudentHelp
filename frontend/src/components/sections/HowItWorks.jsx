import React from "react";
import { Reveal, Stagger, Item } from "../Reveal";
import { ClipboardList, BrainCircuit, FileBadge2 } from "lucide-react";

const STEPS = [
  { icon: ClipboardList, n: "01", title: "Answer simple questions", desc: "Tell us about your interests, personality and goals. Takes under 2 minutes — no essays." },
  { icon: BrainCircuit, n: "02", title: "AI analyzes you", desc: "Our engine scores your personality, interests and goals against 12 high-growth career paths." },
  { icon: FileBadge2, n: "03", title: "Receive your Blueprint", desc: "Get your personalised career matches, salary potential, AI-risk score and roadmap instantly." },
];

export const HowItWorks = () => (
  <section className="py-24 sm:py-32" data-testid="how-it-works-section">
    <div className="max-w-7xl mx-auto px-6 lg:px-8">
      <Reveal>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-amber-500 mb-4">How It Works</p>
        <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight">
          Clarity in three steps.
        </h2>
      </Reveal>

      <Stagger className="mt-14 grid md:grid-cols-3 gap-6">
        {STEPS.map((s) => (
          <Item key={s.n}>
            <div className="relative h-full rounded-2xl border border-white/8 bg-[#091226] p-8 overflow-hidden hover:border-amber-500/30 transition-all duration-300">
              <span className="absolute -top-4 right-4 font-head font-800 text-7xl text-white/5">{s.n}</span>
              <div className="w-14 h-14 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center mb-6">
                <s.icon className="w-7 h-7 text-gold" strokeWidth={1.6} />
              </div>
              <h3 className="font-head font-700 text-2xl mb-3">{s.title}</h3>
              <p className="text-slate-400 leading-relaxed">{s.desc}</p>
            </div>
          </Item>
        ))}
      </Stagger>
    </div>
  </section>
);
