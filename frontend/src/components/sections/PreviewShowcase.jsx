import React from "react";
import { Reveal } from "../Reveal";
import { Lock, Target, Gem, TrendingUp, ShieldCheck, Crown, Briefcase, Sparkles } from "lucide-react";
import { CTAButton } from "../CTAButton";

const MetricRow = ({ label, value, blurred }) => (
  <div className="flex items-center justify-between gap-4 py-3 border-b border-white/5 last:border-0">
    <span className="text-slate-300 text-sm">{label}</span>
    <div className={blurred ? "locked-blur" : ""}>
      <div className="w-40 h-2.5 rounded-full bg-[#1E293B] overflow-hidden">
        <div className="h-full gold-gradient" style={{ width: `${value}%` }} />
      </div>
    </div>
  </div>
);

export const PreviewShowcase = ({ onStart }) => (
  <section className="py-24 sm:py-32 bg-[#070E1E] border-y border-white/5" data-testid="preview-showcase-section">
    <div className="max-w-7xl mx-auto px-6 lg:px-8">
      <Reveal>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-amber-500 mb-4">A Glimpse Inside</p>
        <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight max-w-3xl">
          This is what your Career Blueprint looks like.
        </h2>
      </Reveal>

      <Reveal delay={0.1}>
        <div className="relative mt-12 rounded-3xl border border-white/10 bg-[#091226] overflow-hidden">
          <div className="grid md:grid-cols-2 gap-px bg-white/5">
            <div className="bg-[#091226] p-8">
              <div className="flex items-center gap-2 mb-6">
                <Target className="w-5 h-5 text-gold" />
                <h3 className="font-head font-700 text-xl">Career Match Scores</h3>
              </div>
              {[["AI / ML Engineer", 96], ["Product Manager", 88], ["Data Scientist", 82]].map(([n, v]) => (
                <MetricRow key={n} label={n} value={v} />
              ))}
              <div className="mt-6 flex items-center gap-2 mb-4">
                <Gem className="w-5 h-5 text-gold" />
                <h3 className="font-head font-700 text-xl">Top Strengths</h3>
              </div>
              {[["Analytical Thinking", 94], ["Systems Design", 90]].map(([n, v]) => (
                <MetricRow key={n} label={n} value={v} blurred />
              ))}
            </div>
            <div className="bg-[#091226] p-8">
              {[
                { icon: TrendingUp, label: "Future Salary Potential", v: 92 },
                { icon: ShieldCheck, label: "AI Resistance Score", v: 95 },
                { icon: Crown, label: "Leadership Potential", v: 78 },
                { icon: Briefcase, label: "Business Potential", v: 81 },
                { icon: Sparkles, label: "Personal Growth Insights", v: 88 },
              ].map((m, i) => (
                <MetricRow key={m.label} label={m.label} value={m.v} blurred={i > 0} />
              ))}
            </div>
          </div>

          {/* Lock overlay */}
          <div className="absolute inset-0 z-20 flex flex-col items-center justify-center p-6 bg-[#040914]/55 backdrop-blur-[2px]"
               style={{ background: "linear-gradient(to bottom, rgba(4,9,20,0.1) 0%, rgba(4,9,20,0.85) 60%)" }}>
            <div className="mt-auto text-center">
              <Lock className="w-12 h-12 text-amber-500 mx-auto mb-4 drop-shadow-[0_0_15px_rgba(245,158,11,0.5)]" strokeWidth={1.6} />
              <p className="font-head font-700 text-2xl sm:text-3xl">90% of Your Career Blueprint Is Locked</p>
              <p className="mt-2 text-slate-300">Unlock your full personalised report to see everything.</p>
              <div className="mt-6">
                <CTAButton testid="preview-unlock-btn" onClick={onStart}>Reveal My Career Matches</CTAButton>
              </div>
            </div>
          </div>
        </div>
      </Reveal>
    </div>
  </section>
);
