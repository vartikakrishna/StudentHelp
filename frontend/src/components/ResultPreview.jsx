import React, { useState } from "react";
import * as Icons from "lucide-react";
import { motion } from "framer-motion";
import { Lock, Download, Sparkles, ArrowLeft } from "lucide-react";
import { PaymentModal } from "./PaymentModal";
import { CTAButton } from "./CTAButton";
import { pdfUrl } from "../lib/api";

const ScoreBar = ({ value, gold = true }) => (
  <div className="w-full h-2.5 rounded-full bg-[#1E293B] overflow-hidden">
    <motion.div
      className={gold ? "h-full gold-gradient" : "h-full bg-slate-500"}
      initial={{ width: 0 }}
      whileInView={{ width: `${value}%` }}
      viewport={{ once: true }}
      transition={{ duration: 1, ease: "easeOut" }}
    />
  </div>
);

const MatchCard = ({ m, rank }) => {
  const Icon = Icons[m.icon] || Icons.Sparkles;
  return (
    <div className="rounded-2xl border border-white/10 bg-[#091226] p-6 hover:border-amber-500/30 transition">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center">
            <Icon className="w-6 h-6 text-gold" strokeWidth={1.6} />
          </div>
          <div>
            <p className="font-mono text-[11px] text-slate-500">MATCH #{rank}</p>
            <h3 className="font-head font-700 text-lg leading-tight">{m.title}</h3>
          </div>
        </div>
        <span className="font-mono font-700 text-2xl text-gold">{m.score}%</span>
      </div>
      <ScoreBar value={m.score} />
      <p className="text-slate-400 text-sm mt-4">{m.explanation || m.tagline}</p>
      <div className="flex gap-4 mt-4 text-xs font-mono text-slate-500">
        <span>💰 ~₹{m.salary_mid} LPA</span>
        <span>🛡 {m.ai_resistance}% AI-proof</span>
      </div>
    </div>
  );
};

export const ResultPreview = ({ result, onBack }) => {
  const { submission_id, preview } = result;
  const [paid, setPaid] = useState(false);
  const [report, setReport] = useState(null);
  const [showPay, setShowPay] = useState(false);

  const onSuccess = (rep) => {
    setReport(rep);
    setPaid(true);
    setShowPay(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="min-h-screen bg-[#040914]" data-testid="result-page">
      <div className="max-w-5xl mx-auto px-6 lg:px-8 py-10">
        <button onClick={onBack} className="text-slate-400 hover:text-white flex items-center gap-2 mb-8 text-sm">
          <ArrowLeft className="w-4 h-4" /> Back to home
        </button>

        {/* Success score hero */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-12">
          <p className="font-mono text-xs tracking-[0.2em] uppercase text-amber-500 mb-3">Your Free Career Preview</p>
          <div className="inline-flex flex-col items-center">
            <div className="relative w-40 h-40 mb-4">
              <svg viewBox="0 0 120 120" className="w-full h-full -rotate-90">
                <circle cx="60" cy="60" r="52" fill="none" stroke="#1E293B" strokeWidth="10" />
                <motion.circle
                  cx="60" cy="60" r="52" fill="none" stroke="#F59E0B" strokeWidth="10" strokeLinecap="round"
                  strokeDasharray={2 * Math.PI * 52}
                  initial={{ strokeDashoffset: 2 * Math.PI * 52 }}
                  animate={{ strokeDashoffset: 2 * Math.PI * 52 * (1 - preview.success_score / 100) }}
                  transition={{ duration: 1.4, ease: "easeOut" }}
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="font-head font-800 text-4xl text-gold text-glow" data-testid="success-score">{preview.success_score}%</span>
                <span className="text-[11px] text-slate-400 font-mono uppercase tracking-wider">Success Score</span>
              </div>
            </div>
            <h1 className="font-head font-800 text-3xl sm:text-4xl tracking-tight">Your Top Career Matches Are In.</h1>
            <p className="text-slate-400 mt-2">{preview.trait_labels?.join(" · ")}</p>
          </div>
        </motion.div>

        {/* Top 3 matches (free) */}
        <div className="grid md:grid-cols-3 gap-5 mb-10">
          {preview.top_matches.map((m, i) => <MatchCard key={i} m={m} rank={i + 1} />)}
        </div>

        {/* Free insights */}
        <div className="grid md:grid-cols-2 gap-5 mb-12">
          <div className="rounded-2xl border border-white/10 bg-[#091226] p-6">
            <div className="flex items-center gap-2 mb-3">
              <Sparkles className="w-5 h-5 text-gold" />
              <h3 className="font-head font-700 text-lg">Personality Insight</h3>
            </div>
            <p className="text-slate-300 leading-relaxed">{preview.personality_insight}</p>
          </div>
          <div className="rounded-2xl border border-white/10 bg-[#091226] p-6">
            <div className="flex items-center gap-2 mb-3">
              <Icons.Gem className="w-5 h-5 text-gold" />
              <h3 className="font-head font-700 text-lg">Hidden Strength: {preview.hidden_strength?.title}</h3>
            </div>
            <p className="text-slate-300 leading-relaxed">{preview.hidden_strength?.description}</p>
          </div>
        </div>

        {paid && report ? (
          <FullReport report={report} submissionId={submission_id} />
        ) : (
          <LockedSection preview={preview} onUnlock={() => setShowPay(true)} />
        )}
      </div>

      {showPay && (
        <PaymentModal
          submissionId={submission_id}
          name={result.name || "You"}
          onClose={() => setShowPay(false)}
          onSuccess={onSuccess}
        />
      )}
    </div>
  );
};

const LockedRow = ({ label }) => (
  <div className="flex items-center justify-between py-3 border-b border-white/5 last:border-0">
    <span className="text-slate-300 text-sm">{label}</span>
    <div className="locked-blur"><div className="w-32 h-2.5 rounded-full bg-[#1E293B]"><div className="h-full gold-gradient" style={{ width: "78%" }} /></div></div>
  </div>
);

const LockedSection = ({ onUnlock }) => (
  <div className="relative rounded-3xl border border-white/10 overflow-hidden" data-testid="locked-section">
    <div className="p-8 bg-[#091226]">
      <h3 className="font-head font-700 text-xl mb-4">The other 90% of your Blueprint</h3>
      <div className="grid sm:grid-cols-2 gap-x-10">
        {["Career #4 & #5 deep-dive", "10-year salary projection", "AI risk per career", "Leadership potential",
          "Business / startup potential", "Personalised learning roadmap", "Best industries for you", "Growth obstacles to avoid",
          "Hidden strengths breakdown", "Letter from your future self"].map((l) => <LockedRow key={l} label={l} />)}
      </div>
    </div>
    <div className="absolute inset-0 z-20 flex flex-col items-center justify-center text-center p-6"
         style={{ background: "linear-gradient(to bottom, rgba(4,9,20,0.4), rgba(4,9,20,0.92))", backdropFilter: "blur(3px)" }}>
      <Lock className="w-12 h-12 text-amber-500 mb-4 drop-shadow-[0_0_15px_rgba(245,158,11,0.5)]" strokeWidth={1.6} />
      <p className="font-head font-700 text-2xl sm:text-3xl">90% of Your Career Blueprint Is Locked</p>
      <p className="text-slate-300 mt-2 mb-6 max-w-md">Unlock your complete 12–15 page premium report — instant PDF download.</p>
      <CTAButton testid="unlock-premium-btn" onClick={onUnlock}>Unlock Full Blueprint · ₹199</CTAButton>
      <p className="mt-3 text-xs text-slate-500 font-mono">One wrong career decision can cost years.</p>
    </div>
  </div>
);

const FullReport = ({ report, submissionId }) => {
  const sp = report.salary_projection;
  const maxSalary = Math.max(...Object.values(sp));
  return (
    <div data-testid="full-report">
      <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/5 p-6 mb-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Icons.CheckCircle2 className="w-8 h-8 text-emerald-400" />
          <div>
            <p className="font-head font-700 text-lg">Your full Career Blueprint is unlocked!</p>
            <p className="text-slate-400 text-sm">Download your premium 12–15 page PDF report below.</p>
          </div>
        </div>
        <a href={pdfUrl(submissionId)} target="_blank" rel="noreferrer" data-testid="download-pdf-btn"
           className="inline-flex items-center gap-2 gold-gradient text-[#1a1000] font-head font-700 rounded-lg px-6 py-3 glow-gold hover:scale-105 transition">
          <Download className="w-5 h-5" /> Download PDF
        </a>
      </div>

      {/* All 5 matches */}
      <h2 className="font-head font-700 text-2xl mb-4">All Top 5 Career Matches</h2>
      <div className="grid md:grid-cols-2 gap-5 mb-10">
        {report.matches.map((m, i) => {
          const Icon = Icons[m.icon] || Icons.Sparkles;
          return (
            <div key={m.key} className="rounded-2xl border border-white/10 bg-[#091226] p-6">
              <div className="flex items-center justify-between mb-3">
                <span className="flex items-center gap-2.5 font-head font-700"><Icon className="w-5 h-5 text-gold" /> {m.title}</span>
                <span className="font-mono text-gold">{m.score}%</span>
              </div>
              <ScoreBar value={m.score} />
              <p className="text-slate-400 text-sm mt-3">{report.match_explanations?.[m.key] || m.tagline}</p>
            </div>
          );
        })}
      </div>

      {/* Salary projection */}
      <div className="grid lg:grid-cols-2 gap-5 mb-10">
        <div className="rounded-2xl border border-white/10 bg-[#091226] p-6">
          <h3 className="font-head font-700 text-lg mb-5">Future Salary Projection (₹ LPA)</h3>
          <div className="flex items-end gap-4 h-44">
            {[["Yr 1", sp.year1], ["Yr 3", sp.year3], ["Yr 5", sp.year5], ["Yr 10", sp.year10]].map(([l, v]) => (
              <div key={l} className="flex-1 flex flex-col items-center justify-end h-full">
                <span className="font-mono text-gold text-sm mb-2">₹{v}</span>
                <motion.div className="w-full gold-gradient rounded-t-md" initial={{ height: 0 }} whileInView={{ height: `${(v / maxSalary) * 100}%` }} viewport={{ once: true }} transition={{ duration: 1 }} />
                <span className="text-xs text-slate-400 mt-2">{l}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-2xl border border-white/10 bg-[#091226] p-6">
          <h3 className="font-head font-700 text-lg mb-5">Your Potential Scores</h3>
          {[["AI Resistance", report.ai_resistance_score], ["Leadership Potential", report.leadership_potential], ["Business Potential", report.business_potential], ["Personal Growth", report.personal_growth]].map(([l, v]) => (
            <div key={l} className="mb-4">
              <div className="flex justify-between text-sm mb-1.5"><span className="text-slate-300">{l}</span><span className="font-mono text-gold">{v}%</span></div>
              <ScoreBar value={v} />
            </div>
          ))}
        </div>
      </div>

      {/* Roadmap */}
      <h2 className="font-head font-700 text-2xl mb-4">Your Learning Roadmap</h2>
      <div className="grid md:grid-cols-3 gap-5 mb-10">
        {(report.learning_roadmap || []).map((ph, i) => (
          <div key={i} className="rounded-2xl border border-white/10 bg-[#091226] p-6">
            <p className="font-mono text-gold text-sm mb-2">{ph.phase}</p>
            <p className="font-head font-700 mb-3">{ph.focus}</p>
            <ul className="space-y-1.5">
              {(ph.skills || []).map((s) => <li key={s} className="text-slate-400 text-sm flex gap-2"><Icons.Check className="w-4 h-4 text-gold shrink-0 mt-0.5" />{s}</li>)}
            </ul>
          </div>
        ))}
      </div>

      {/* Strengths + obstacles */}
      <div className="grid md:grid-cols-2 gap-5 mb-10">
        <div className="rounded-2xl border border-white/10 bg-[#091226] p-6">
          <h3 className="font-head font-700 text-lg mb-4">Your Strengths</h3>
          {(report.strengths || []).map((s, i) => (
            <div key={i} className="mb-3"><p className="font-medium text-white">{s.label}</p><p className="text-slate-400 text-sm">{s.description}</p></div>
          ))}
        </div>
        <div className="rounded-2xl border border-white/10 bg-[#091226] p-6">
          <h3 className="font-head font-700 text-lg mb-4">Growth Obstacles</h3>
          {(report.growth_obstacles || []).map((o, i) => (
            <div key={i} className="mb-3"><p className="font-medium text-white flex items-center gap-2"><Icons.AlertTriangle className="w-4 h-4 text-amber-500" />{o.title}</p><p className="text-slate-400 text-sm">{o.description}</p></div>
          ))}
        </div>
      </div>

      {/* Future self letter */}
      <div className="rounded-2xl border border-amber-500/30 bg-gradient-to-b from-[#0C1730] to-[#091226] p-8 mb-6">
        <div className="flex items-center gap-2 mb-4"><Icons.Mail className="w-5 h-5 text-gold" /><h3 className="font-head font-700 text-lg">A Letter From Your Future Self</h3></div>
        <p className="text-slate-200 leading-relaxed whitespace-pre-line italic">{report.future_self_letter}</p>
      </div>
    </div>
  );
};
