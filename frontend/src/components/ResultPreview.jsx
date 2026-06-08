import React, { useState } from "react";
import * as Icons from "lucide-react";
import { motion } from "framer-motion";
import { Lock, Download, Sparkles, ArrowLeft, ShieldAlert, Gauge } from "lucide-react";
import { PaymentModal } from "./PaymentModal";
import { CTAButton } from "./CTAButton";
import { pdfUrl } from "../lib/api";

const riskStyle = (label = "") => {
  if (label.includes("Very Low") || label === "Low Risk") return "bg-emerald-50 text-emerald-700 border-emerald-200";
  if (label.includes("Medium")) return "bg-amber-50 text-amber-700 border-amber-200";
  return "bg-rose-50 text-rose-700 border-rose-200";
};

const ScoreBar = ({ value, color = "grad-primary-h" }) => (
  <div className="w-full h-2.5 rounded-full bg-slate-100 overflow-hidden">
    <motion.div className={`h-full ${color}`} initial={{ width: 0 }} whileInView={{ width: `${value}%` }} viewport={{ once: true }} transition={{ duration: 1, ease: "easeOut" }} />
  </div>
);

const Badge = ({ children, cls }) => (
  <span className={`inline-block text-[11px] font-mono px-2.5 py-1 rounded-full border ${cls}`}>{children}</span>
);

const PreviewMatch = ({ m, rank }) => {
  const Icon = Icons[m.icon] || Icons.Sparkles;
  return (
    <div className="rounded-3xl glass-card p-6 hover:-translate-y-1 transition">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl grad-primary flex items-center justify-center shadow-md shadow-indigo-500/30"><Icon className="w-6 h-6 text-white" strokeWidth={1.7} /></div>
          <div>
            <p className="font-mono text-[11px] text-slate-400">MATCH #{rank}</p>
            <h3 className="font-head font-700 text-base leading-tight text-slate-900">{m.title}</h3>
          </div>
        </div>
        <span className="font-mono font-700 text-2xl text-gradient">{m.score}%</span>
      </div>
      <ScoreBar value={m.score} />
      <div className="flex flex-wrap gap-2 mt-4">
        <Badge cls="bg-indigo-50 text-indigo-700 border-indigo-200">{m.verdict}</Badge>
        <Badge cls={riskStyle(m.ai_risk_label)}>{m.ai_risk_label}</Badge>
        <Badge cls="bg-cyan-50 text-cyan-700 border-cyan-200">~₹{m.salary_mid} LPA</Badge>
      </div>
      <p className="text-slate-600 text-sm mt-3">{m.explanation || m.tagline}</p>
    </div>
  );
};

export const ResultPreview = ({ result, onBack }) => {
  const { submission_id, preview } = result;
  const [paid, setPaid] = useState(false);
  const [report, setReport] = useState(null);
  const [showPay, setShowPay] = useState(false);

  const onSuccess = (rep) => { setReport(rep); setPaid(true); setShowPay(false); window.scrollTo({ top: 0, behavior: "smooth" }); };

  return (
    <div className="min-h-screen bg-white grad-mesh" data-testid="result-page">
      <div className="max-w-5xl mx-auto px-6 lg:px-8 py-10">
        <button onClick={onBack} className="text-slate-500 hover:text-slate-900 flex items-center gap-2 mb-8 text-sm"><ArrowLeft className="w-4 h-4" /> Back to home</button>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-10">
          <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-3">Your Free Career Truth Preview</p>
          <div className="inline-flex flex-col items-center">
            <div className="relative w-36 h-36 mb-4">
              <svg viewBox="0 0 120 120" className="w-full h-full -rotate-90">
                <defs><linearGradient id="cbGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stopColor="#4F46E5" /><stop offset="50%" stopColor="#7C3AED" /><stop offset="100%" stopColor="#06B6D4" /></linearGradient></defs>
                <circle cx="60" cy="60" r="52" fill="none" stroke="#E2E8F0" strokeWidth="10" />
                <motion.circle cx="60" cy="60" r="52" fill="none" stroke="url(#cbGrad)" strokeWidth="10" strokeLinecap="round"
                  strokeDasharray={2 * Math.PI * 52} initial={{ strokeDashoffset: 2 * Math.PI * 52 }} animate={{ strokeDashoffset: 2 * Math.PI * 52 * (1 - preview.success_score / 100) }} transition={{ duration: 1.4 }} />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="font-head font-800 text-4xl text-gradient" data-testid="success-score">{preview.success_score}%</span>
                <span className="text-[10px] text-slate-400 font-mono uppercase tracking-wider">Success Score</span>
              </div>
            </div>
            <h1 className="font-head font-800 text-3xl sm:text-4xl tracking-tight text-slate-900">{result.name?.split(" ")[0]}, here&apos;s the honest truth.</h1>
            <p className="text-slate-500 mt-2">{preview.user_type} · AI Resistance {preview.ai_resistance_score}% · {preview.trait_labels?.slice(0, 3).join(" · ")}</p>
          </div>
        </motion.div>

        {/* Reality check */}
        <div className="rounded-3xl border border-indigo-200 bg-indigo-50/60 p-6 mb-8">
          <div className="flex items-center gap-2 mb-3"><Gauge className="w-5 h-5 text-indigo-600" /><h3 className="font-head font-700 text-lg text-slate-900">Career Reality Check</h3></div>
          <p className="text-slate-700 leading-relaxed">{preview.career_reality_check}</p>
        </div>

        <div className="grid md:grid-cols-3 gap-5 mb-8">
          {preview.top_matches.map((m, i) => <PreviewMatch key={i} m={m} rank={i + 1} />)}
        </div>

        <div className="grid md:grid-cols-3 gap-5 mb-12">
          <div className="rounded-3xl glass-card p-6">
            <div className="flex items-center gap-2 mb-2"><Icons.Award className="w-5 h-5 text-emerald-500" /><h3 className="font-head font-700 text-slate-900">Top Strength</h3></div>
            <p className="font-medium text-slate-900">{preview.strength?.label}</p>
            <p className="text-slate-500 text-sm">Rated {preview.strength?.score}% — a genuine edge.</p>
          </div>
          <div className="rounded-3xl glass-card p-6">
            <div className="flex items-center gap-2 mb-2"><Icons.AlertTriangle className="w-5 h-5 text-rose-500" /><h3 className="font-head font-700 text-slate-900">Key Weakness</h3></div>
            <p className="font-medium text-slate-900">Low {preview.weakness?.label}</p>
            <p className="text-slate-500 text-sm">Rated {preview.weakness?.score}% — don&apos;t build a career on this.</p>
          </div>
          <div className="rounded-3xl glass-card p-6">
            <div className="flex items-center gap-2 mb-2"><Icons.Gem className="w-5 h-5 text-purple-500" /><h3 className="font-head font-700 text-slate-900">Hidden Talent</h3></div>
            <p className="font-medium text-slate-900">{preview.hidden_talent?.title}</p>
            <p className="text-slate-500 text-sm">{preview.hidden_talent?.description}</p>
          </div>
        </div>

        {paid && report ? <FullReport report={report} submissionId={submission_id} /> : <LockedSection preview={preview} onUnlock={() => setShowPay(true)} />}
      </div>

      {showPay && <PaymentModal submissionId={submission_id} name={result.name || "You"} email={result.email} phone={result.phone} onClose={() => setShowPay(false)} onSuccess={onSuccess} />}
    </div>
  );
};

const LockedRow = ({ label }) => (
  <div className="flex items-center justify-between py-3 border-b border-slate-100 last:border-0">
    <span className="text-slate-600 text-sm">{label}</span>
    <div className="locked-blur"><div className="w-32 h-2.5 rounded-full bg-slate-100"><div className="h-full grad-primary-h" style={{ width: "78%" }} /></div></div>
  </div>
);

const LockedSection = ({ onUnlock }) => (
  <div className="relative rounded-[2rem] glass-card overflow-hidden" data-testid="locked-section">
    <div className="p-8">
      <h3 className="font-head font-700 text-xl mb-4 text-slate-900">The other 90% of your Career Blueprint</h3>
      <div className="grid sm:grid-cols-2 gap-x-10">
        {["Top 5 careers to AVOID (and why)", "AI threat assessment per career", "10-year income projection", "Leadership & business potential",
          "Career-switch opportunities + success odds", "Skill-gap analysis", "30/90/6-month/12-month learning plan", "Resume & LinkedIn strategy",
          "Interview readiness plan", "Layoff recovery roadmap", "Future industry predictions", "Letter from your future self"].map((l) => <LockedRow key={l} label={l} />)}
      </div>
    </div>
    <div className="absolute inset-0 z-20 flex flex-col items-center justify-center text-center p-6" style={{ background: "linear-gradient(to bottom, rgba(255,255,255,0.45), rgba(255,255,255,0.95))", backdropFilter: "blur(4px)" }}>
      <div className="w-16 h-16 rounded-2xl grad-primary flex items-center justify-center mb-4 glow-primary"><Lock className="w-8 h-8 text-white" strokeWidth={1.8} /></div>
      <p className="font-head font-700 text-2xl sm:text-3xl text-slate-900">90% of Your Career Blueprint Is Locked</p>
      <p className="text-slate-500 mt-2 mb-1 max-w-md">Unlock the full 16-chapter report — careers to avoid, AI threat, recovery roadmap & more.</p>
      <p className="text-slate-400 text-sm mb-6"><span className="line-through">₹999</span> &nbsp;Today only <b className="text-purple-600">₹199</b></p>
      <CTAButton testid="unlock-premium-btn" onClick={onUnlock}>Unlock My Career Blueprint · ₹199</CTAButton>
      <p className="mt-3 text-xs text-slate-400 font-mono">One wrong career decision can cost years.</p>
    </div>
  </div>
);

const Section = ({ icon, title, children }) => {
  const Icon = icon;
  return (
    <div className="mb-10">
      <div className="flex items-center gap-2.5 mb-4">
        <div className="w-9 h-9 rounded-xl grad-primary flex items-center justify-center"><Icon className="w-5 h-5 text-white" strokeWidth={1.8} /></div>
        <h2 className="font-head font-700 text-2xl text-slate-900">{title}</h2>
      </div>
      {children}
    </div>
  );
};

const FullReport = ({ report, submissionId }) => {
  const sp = report.salary_projection;
  const maxSalary = Math.max(...Object.values(sp));
  return (
    <div data-testid="full-report">
      <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6 mb-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Icons.CheckCircle2 className="w-8 h-8 text-emerald-500" />
          <div><p className="font-head font-700 text-lg text-slate-900">Your full Career Blueprint is unlocked!</p><p className="text-slate-500 text-sm">Download your premium 16-chapter PDF below.</p></div>
        </div>
        <a href={pdfUrl(submissionId)} target="_blank" rel="noreferrer" data-testid="download-pdf-btn"
           className="inline-flex items-center gap-2 grad-primary-h text-white font-head font-700 rounded-full px-6 py-3 glow-primary hover:scale-105 transition"><Download className="w-5 h-5" /> Download PDF</a>
      </div>

      {/* All matches with honesty scorecards */}
      <Section icon={Icons.Target} title="Top 5 Career Matches">
        <div className="grid md:grid-cols-2 gap-5">
          {report.matches.map((m) => {
            const Icon = Icons[m.icon] || Icons.Sparkles;
            return (
              <div key={m.key} className="rounded-3xl glass-card p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="flex items-center gap-2.5 font-head font-700 text-slate-900"><span className="w-8 h-8 rounded-lg grad-primary flex items-center justify-center"><Icon className="w-4 h-4 text-white" /></span>{m.title}</span>
                  <span className="font-mono text-gradient font-700">{m.score}%</span>
                </div>
                <div className="flex flex-wrap gap-2 mb-3"><Badge cls="bg-indigo-50 text-indigo-700 border-indigo-200">{m.verdict}</Badge><Badge cls={riskStyle(m.ai_risk_label)}>{m.ai_risk_label}</Badge><Badge cls="bg-slate-50 text-slate-600 border-slate-200">Enter: {m.time_to_enter}</Badge></div>
                {[["Market Demand", m.market_demand, "bg-indigo-500"], ["Salary Score", m.salary_score, "bg-cyan-500"], ["Competition", m.competition, "bg-rose-400"]].map(([l, v, c]) => (
                  <div key={l} className="mb-2"><div className="flex justify-between text-xs mb-1"><span className="text-slate-500">{l}</span><span className="font-mono text-slate-700">{v}%</span></div><div className="h-2 rounded-full bg-slate-100 overflow-hidden"><div className={`h-full ${c}`} style={{ width: `${v}%` }} /></div></div>
                ))}
                <p className="text-slate-600 text-sm mt-3">{report.match_explanations?.[m.key] || m.tagline}</p>
              </div>
            );
          })}
        </div>
      </Section>

      {/* Careers to avoid */}
      <Section icon={ShieldAlert} title="Careers To Avoid">
        <div className="grid md:grid-cols-2 gap-4">
          {report.careers_to_avoid?.map((a, i) => (
            <div key={i} className="rounded-2xl border border-rose-200 bg-rose-50 p-5">
              <div className="flex items-center justify-between mb-1"><p className="font-head font-700 text-slate-900">{a.title}</p><Badge cls={riskStyle(a.ai_risk_label)}>{a.ai_risk_label}</Badge></div>
              <p className="text-slate-600 text-sm">Why: {a.why?.join("; ")}</p>
            </div>
          ))}
        </div>
        {report.careers_to_avoid_note && <p className="text-slate-600 mt-4">{report.careers_to_avoid_note}</p>}
      </Section>

      {/* AI threat */}
      <Section icon={Icons.Bot} title="AI Threat Assessment">
        <div className="rounded-3xl glass-card p-6">
          <p className="text-slate-700 mb-4">Portfolio AI exposure: <b>{report.portfolio_ai_risk}% ({report.ai_risk_label})</b>. {report.ai_threat_summary}</p>
          {report.matches.map((m) => (
            <div key={m.key} className="mb-3"><div className="flex justify-between text-sm mb-1"><span className="text-slate-600">{m.title}</span><span className="font-mono text-purple-600">{m.ai_risk_label}</span></div><ScoreBar value={m.ai_risk} color="bg-purple-500" /></div>
          ))}
        </div>
      </Section>

      {/* Income + potential */}
      <Section icon={Icons.TrendingUp} title="Income Projection & Potential">
        <div className="grid lg:grid-cols-2 gap-5">
          <div className="rounded-3xl glass-card p-6">
            <h3 className="font-head font-700 text-lg mb-5 text-slate-900">Salary Projection (₹ LPA)</h3>
            <div className="flex items-end gap-4 h-44">
              {[["Yr 1", sp.year1], ["Yr 3", sp.year3], ["Yr 5", sp.year5], ["Yr 10", sp.year10]].map(([l, v]) => (
                <div key={l} className="flex-1 flex flex-col items-center justify-end h-full">
                  <span className="font-mono text-purple-600 text-sm mb-2">₹{v}</span>
                  <motion.div className="w-full grad-primary rounded-t-xl" initial={{ height: 0 }} whileInView={{ height: `${(v / maxSalary) * 100}%` }} viewport={{ once: true }} transition={{ duration: 1 }} />
                  <span className="text-xs text-slate-400 mt-2">{l}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-3xl glass-card p-6">
            <h3 className="font-head font-700 text-lg mb-5 text-slate-900">Your Potential Scores</h3>
            {[["AI Resistance", report.ai_resistance_score], ["Leadership Potential", report.leadership_potential], ["Business Potential", report.business_potential], ["Personal Growth", report.personal_growth]].map(([l, v]) => (
              <div key={l} className="mb-4"><div className="flex justify-between text-sm mb-1.5"><span className="text-slate-600">{l}</span><span className="font-mono text-purple-600">{v}%</span></div><ScoreBar value={v} /></div>
            ))}
            <p className="text-slate-600 text-sm mt-2">{report.entrepreneurship}</p>
          </div>
        </div>
      </Section>

      {/* Career switch */}
      {report.career_switch?.targets?.length > 0 && (
        <Section icon={Icons.Repeat} title="Career Switch Opportunities">
          <div className="grid md:grid-cols-2 gap-4">
            {report.career_switch.targets.map((t, i) => (
              <div key={i} className="rounded-2xl glass-card p-5">
                <p className="font-head font-700 text-slate-900 mb-2">{t.title}</p>
                <div className="flex flex-wrap gap-2 mb-2"><Badge cls="bg-slate-50 text-slate-600 border-slate-200">{t.difficulty}</Badge><Badge cls="bg-cyan-50 text-cyan-700 border-cyan-200">{t.salary_impact}</Badge><Badge cls="bg-emerald-50 text-emerald-700 border-emerald-200">{t.success_probability} success</Badge></div>
                <p className="text-slate-500 text-sm">Skill gaps: {t.skill_gaps?.join(", ")} · {t.time_required}</p>
              </div>
            ))}
          </div>
        </Section>
      )}

      {/* Layoff */}
      {report.layoff && (
        <Section icon={Icons.LifeBuoy} title="Layoff Recovery Plan">
          <div className="grid sm:grid-cols-4 gap-4 mb-5">
            {[["Layoff Risk", report.layoff.layoff_risk_score, "text-rose-600"], ["Recovery", report.layoff.recovery_score, "text-emerald-600"], ["Employability", report.layoff.employability_score, "text-indigo-600"], ["Salary Recovery", report.layoff.salary_recovery_potential, "text-cyan-600"]].map(([l, v, c]) => (
              <div key={l} className="rounded-2xl glass-card p-4 text-center"><p className={`font-head font-800 text-3xl ${c}`}>{v}%</p><p className="text-slate-500 text-xs mt-1">{l}</p></div>
            ))}
          </div>
          <div className="grid md:grid-cols-3 gap-4">
            {Object.entries(report.layoff.recovery_roadmap).map(([phase, items]) => (
              <div key={phase} className="rounded-2xl glass-card p-5"><p className="font-mono text-purple-600 text-sm mb-2">{phase}</p><ul className="space-y-1.5">{items.map((it) => <li key={it} className="text-slate-600 text-sm flex gap-2"><Icons.Check className="w-4 h-4 text-cyan-500 shrink-0 mt-0.5" />{it}</li>)}</ul></div>
            ))}
          </div>
        </Section>
      )}

      {/* IT report */}
      {report.it_report && (
        <Section icon={Icons.Code} title="IT Employee Future Report">
          <div className="grid sm:grid-cols-3 gap-4">
            {[["Current Role Demand", report.it_report.current_role_demand], ["Future Demand", report.it_report.future_demand], ["Promotion Potential", report.it_report.promotion_potential], ["AI Risk", report.it_report.ai_risk], ["Salary Growth", report.it_report.salary_growth_potential]].map(([l, v]) => (
              <div key={l} className="rounded-2xl glass-card p-5"><div className="flex justify-between text-sm mb-1.5"><span className="text-slate-600">{l}</span><span className="font-mono text-purple-600">{v}%</span></div><ScoreBar value={v} /></div>
            ))}
          </div>
        </Section>
      )}

      {/* Learning roadmap */}
      <Section icon={Icons.Map} title="Skill Gap & Learning Roadmap">
        <div className="rounded-2xl glass-card p-5 mb-4"><p className="text-slate-700"><b>Learn next:</b> {report.learn_next?.join(" · ")}</p></div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          {report.learning_plans?.map((ph, i) => (
            <div key={i} className="rounded-2xl glass-card p-5">
              <p className="font-mono text-purple-600 text-sm mb-1">{ph.phase}</p>
              <p className="font-head font-700 text-slate-900 mb-3 text-sm">{ph.focus}</p>
              <ul className="space-y-1.5 mb-3">{ph.items?.map((it) => <li key={it} className="text-slate-600 text-xs flex gap-2"><Icons.Check className="w-3.5 h-3.5 text-cyan-500 shrink-0 mt-0.5" />{it}</li>)}</ul>
              <Badge cls="bg-emerald-50 text-emerald-700 border-emerald-200">{ph.success_probability} success</Badge>
            </div>
          ))}
        </div>
      </Section>

      {/* Resume + interview */}
      <Section icon={Icons.FileText} title="Resume, LinkedIn & Interview Strategy">
        <div className="grid md:grid-cols-2 gap-4">
          <div className="rounded-2xl glass-card p-5"><p className="font-head font-700 text-slate-900 mb-1">Resume & LinkedIn</p><p className="text-slate-600 text-sm">{report.resume_linkedin}</p></div>
          <div className="rounded-2xl glass-card p-5"><p className="font-head font-700 text-slate-900 mb-1">Interview Readiness</p><p className="text-slate-600 text-sm">{report.interview_readiness}</p></div>
        </div>
      </Section>

      {/* Future industries */}
      {report.future_industries?.length > 0 && (
        <Section icon={Icons.Telescope} title="Future Industry Predictions">
          <div className="grid md:grid-cols-3 gap-4">
            {report.future_industries.map((fi, i) => <div key={i} className="rounded-2xl glass-card p-5 text-slate-700 text-sm">{fi}</div>)}
          </div>
        </Section>
      )}

      {/* Future self letter */}
      <div className="rounded-[2rem] grad-primary p-8 mb-6 text-white glow-primary overflow-hidden relative">
        <Icons.Mail className="absolute -top-3 -right-3 w-28 h-28 text-white/10" />
        <div className="relative flex items-center gap-2 mb-4"><Icons.Mail className="w-5 h-5" /><h3 className="font-head font-700 text-lg">A Letter From Your Future Self</h3></div>
        <p className="relative text-white/95 leading-relaxed whitespace-pre-line italic">{report.future_self_letter}</p>
      </div>
    </div>
  );
};
