import React from "react";
import { Reveal, Stagger, Item } from "../Reveal";
import { ClipboardList, BrainCircuit, FileBadge2 } from "lucide-react";

const STEPS = [
  { icon: ClipboardList, n: "01", title: "Answer simple questions", desc: "Tell us about your interests, personality and goals. Takes under 2 minutes — no essays." },
  { icon: BrainCircuit, n: "02", title: "AI analyzes you", desc: "Our engine scores your personality, interests and goals against 12 high-growth career paths." },
  { icon: FileBadge2, n: "03", title: "Receive your Blueprint", desc: "Get your personalized matches, salary potential, AI-risk score and roadmap instantly." },
];

export const HowItWorks = () => (
  <section className="py-24 sm:py-32 bg-white" data-testid="how-it-works-section">
    <div className="max-w-7xl mx-auto px-6 lg:px-8">
      <Reveal>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-4">How It Works</p>
        <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight text-slate-900">
          Clarity in <span className="text-gradient">three steps.</span>
        </h2>
      </Reveal>

      <Stagger className="mt-14 grid md:grid-cols-3 gap-6">
        {STEPS.map((s) => (
          <Item key={s.n}>
            <div className="relative h-full rounded-3xl glass-card p-8 overflow-hidden hover:-translate-y-1.5 transition-all duration-300">
              <span className="absolute -top-3 right-5 font-head font-800 text-7xl text-transparent bg-clip-text grad-primary opacity-10">{s.n}</span>
              <div className="w-14 h-14 rounded-2xl grad-primary flex items-center justify-center mb-6 shadow-lg shadow-indigo-500/30">
                <s.icon className="w-7 h-7 text-white" strokeWidth={1.7} />
              </div>
              <h3 className="font-head font-700 text-2xl mb-3 text-slate-900">{s.title}</h3>
              <p className="text-slate-600 leading-relaxed">{s.desc}</p>
            </div>
          </Item>
        ))}
      </Stagger>
    </div>
  </section>
);
