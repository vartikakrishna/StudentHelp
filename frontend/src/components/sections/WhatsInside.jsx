import React from "react";
import * as Icons from "lucide-react";
import { Reveal, Stagger, Item } from "../Reveal";
import { CHAPTERS } from "../../data/blueprint";

export const WhatsInside = () => (
  <section className="py-24 sm:py-32 bg-[#070E1E] border-y border-white/5" data-testid="whats-inside-section">
    <div className="max-w-7xl mx-auto px-6 lg:px-8">
      <Reveal>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-amber-500 mb-4">Inside The Premium Report</p>
        <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight max-w-3xl">
          A 20+ page blueprint. <span className="text-gold">10 powerful chapters.</span>
        </h2>
        <p className="mt-5 text-slate-400 text-lg max-w-2xl">
          Every chapter is built around <em>you</em> — your answers, your strengths, your future.
        </p>
      </Reveal>

      <Stagger className="mt-14 grid grid-cols-1 lg:grid-cols-12 gap-5 auto-rows-fr">
        {CHAPTERS.map((ch) => {
          const Icon = Icons[ch.icon] || Icons.Sparkles;
          const big = ch.span.includes("col-span-8") || ch.span.includes("col-span-12");
          return (
            <Item key={ch.n} className={ch.span}>
              <div className={`h-full rounded-2xl border border-white/8 bg-white/5 backdrop-blur-xl p-7 hover:border-amber-500/30 hover:-translate-y-1 transition-all duration-300 ${big ? "flex flex-col justify-between" : ""}`}>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-11 h-11 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center shrink-0">
                    <Icon className="w-5 h-5 text-gold" strokeWidth={1.6} />
                  </div>
                  <span className="font-mono text-xs text-slate-500">CHAPTER {ch.n}</span>
                </div>
                <h3 className={`font-head font-700 ${big ? "text-2xl sm:text-3xl" : "text-xl"}`}>{ch.title}</h3>
              </div>
            </Item>
          );
        })}
      </Stagger>
    </div>
  </section>
);
