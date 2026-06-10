import React, { useState } from "react";
import * as Icons from "lucide-react";
import { motion } from "framer-motion";
import { Lock, Download, ArrowLeft } from "lucide-react";
import { PaymentModal } from "./PaymentModal";
import { CTAButton } from "./CTAButton";
import { ReportRenderer } from "./ReportRenderer";
import { pdfUrl, addonPdfUrl } from "../lib/api";
import { toast } from "sonner";
import { PLAN_CONFIG, COMPARISON, UPSELLS, ADDON_LABELS } from "../data/blueprint";
import { LeadGate } from "./LeadGate";
import { track } from "../lib/analytics";

const Tick = ({ on }) => on
  ? <Icons.Check className="w-4 h-4 text-emerald-500 mx-auto" strokeWidth={3} />
  : <Icons.X className="w-4 h-4 text-slate-300 mx-auto" strokeWidth={3} />;

export const ResultPreview = ({ result, onBack }) => {
  const { submission_id, preview } = result;
  const plan = result.plan || (["Student", "Fresher"].includes(result.user_type) ? "student" : "professional");
  const isPro = plan === "professional";
  const [paid, setPaid] = useState(false);
  const [report, setReport] = useState(null);
  const [showPay, setShowPay] = useState(false);
  const [showLead, setShowLead] = useState(false);
  const [lead, setLead] = useState({ name: result.name, phone: result.phone });

  const startUnlock = () => { track("cta_click", { location: "unlock", plan }); setShowLead(true); };
  const onLeadContinue = (info) => {
    setLead({ name: info.name || result.name, phone: info.whatsapp || result.phone });
    setShowLead(false);
    setShowPay(true);
  };
  const onSuccess = (rep) => {
    setReport(rep); setPaid(true); setShowPay(false);
    track("purchase", { plan, value: plan === "professional" ? 499 : 199, currency: "INR" });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="min-h-screen bg-white grad-mesh" data-testid="result-page">
      <div className="max-w-5xl mx-auto px-6 lg:px-8 py-10">
        <button onClick={onBack} className="text-slate-500 hover:text-slate-900 flex items-center gap-2 mb-8 text-sm"><ArrowLeft className="w-4 h-4" /> Back to home</button>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-10">
          <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-3">{preview.product_name}</p>
          <h1 className="font-head font-800 text-3xl sm:text-4xl tracking-tight text-slate-900" data-testid="result-headline">{preview.headline}</h1>
          {preview.verdict && <p className="text-slate-600 mt-3 max-w-2xl mx-auto text-lg" data-testid="result-verdict">{preview.verdict}</p>}
        </motion.div>

        {!paid && <PreviewScores scores={preview.scores} />}

        {paid && report
          ? <FullReport report={report} submissionId={submission_id} isPro={isPro} name={lead.name} email={result.email} phone={lead.phone} />
          : <LockedSection plan={plan} summary={preview.summary} onUnlock={startUnlock} />}
      </div>

      {showLead && <LeadGate defaultName={result.name} defaultDegree={result.answers?.current_degree || result.answers?.stream || ""} userType={result.user_type}
        onClose={() => setShowLead(false)} onContinue={onLeadContinue} />}
      {showPay && <PaymentModal submissionId={submission_id} name={lead.name || "You"} email={result.email} phone={lead.phone} onClose={() => setShowPay(false)} onSuccess={onSuccess} />}
    </div>
  );
};

const PreviewScores = ({ scores = [] }) => (
  <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-12" data-testid="preview-scores">
    {scores.map((s, i) => (
      <div key={i} className={`rounded-3xl p-6 text-center relative overflow-hidden ${s.locked ? "border border-slate-200 bg-slate-50" : "glass-card"}`} data-testid={`preview-score-${i}`}>
        {s.locked ? (
          <>
            <div className="locked-blur"><p className="font-head font-800 text-4xl text-slate-300">88%</p></div>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <Lock className="w-5 h-5 text-purple-500 mb-1" />
              <p className="text-slate-700 text-sm font-medium px-2">{s.label}</p>
            </div>
          </>
        ) : (
          <>
            <p className="font-head font-800 text-4xl text-gradient">{s.value}{s.suffix || ""}</p>
            <p className="font-medium text-slate-900 mt-1 text-sm">{s.label}</p>
          </>
        )}
      </div>
    ))}
  </div>
);

const LockedRow = ({ label }) => (
  <div className="flex items-center justify-between py-3 border-b border-slate-100 last:border-0">
    <span className="text-slate-600 text-sm">{label}</span>
    <div className="locked-blur"><div className="w-32 h-2.5 rounded-full bg-slate-100"><div className="h-full grad-primary-h" style={{ width: "78%" }} /></div></div>
  </div>
);

const ComparisonTable = ({ plan }) => (
  <div className="rounded-2xl border border-slate-200 overflow-hidden bg-white" data-testid="comparison-table">
    <div className="grid grid-cols-[1fr_auto_auto] text-xs font-mono">
      <div className="px-4 py-3 bg-slate-50 font-bold text-slate-600">Feature</div>
      <div className={`px-4 py-3 text-center font-bold ${plan === "student" ? "bg-purple-50 text-purple-700" : "bg-slate-50 text-slate-500"}`}>Student ₹199</div>
      <div className={`px-4 py-3 text-center font-bold ${plan === "professional" ? "bg-purple-50 text-purple-700" : "bg-slate-50 text-slate-500"}`}>Pro ₹499</div>
      {COMPARISON.map((row, i) => (
        <React.Fragment key={row.feature}>
          <div className={`px-4 py-2.5 text-slate-700 ${i % 2 ? "bg-slate-50/50" : ""}`}>{row.feature}</div>
          <div className={`px-4 py-2.5 ${i % 2 ? "bg-slate-50/50" : ""}`}><Tick on={row.student} /></div>
          <div className={`px-4 py-2.5 ${i % 2 ? "bg-slate-50/50" : ""}`}><Tick on={row.pro} /></div>
        </React.Fragment>
      ))}
    </div>
  </div>
);

const LockedSection = ({ plan, summary, onUnlock }) => {
  const cfg = PLAN_CONFIG[plan] || PLAN_CONFIG.student;
  return (
    <div data-testid="locked-section">
      {summary && <p className="text-center text-slate-500 mb-6 max-w-2xl mx-auto">{summary}</p>}
      <div className="relative rounded-[2rem] glass-card overflow-hidden mb-8">
        <div className="p-8">
          <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-2">{cfg.name}</p>
          <h3 className="font-head font-700 text-xl mb-5 text-slate-900">Everything inside your full report</h3>
          <div className="grid sm:grid-cols-2 gap-x-10">{cfg.features.map((l) => <LockedRow key={l} label={l} />)}</div>
        </div>
        <div className="absolute inset-0 z-20 flex flex-col items-center justify-center text-center p-6" style={{ background: "linear-gradient(to bottom, rgba(255,255,255,0.45), rgba(255,255,255,0.95))", backdropFilter: "blur(4px)" }}>
          <div className="w-16 h-16 rounded-2xl grad-primary flex items-center justify-center mb-4 glow-primary"><Lock className="w-8 h-8 text-white" strokeWidth={1.8} /></div>
          <p className="font-head font-700 text-2xl sm:text-3xl text-slate-900 max-w-lg">{cfg.headline}</p>
          <p className="text-slate-500 mt-2 mb-3 max-w-md">{cfg.subheadline}</p>
          <p className="text-slate-400 text-sm mb-5"><span className="line-through">₹{cfg.original}</span> &nbsp;Today only <b className="text-purple-600 text-base">₹{cfg.price}</b></p>
          <CTAButton testid="unlock-premium-btn" onClick={onUnlock}>{cfg.ctaText} · ₹{cfg.price}</CTAButton>
          <p className="mt-3 text-xs text-slate-400 font-mono">{cfg.footnote}</p>
        </div>
      </div>

      <div className="rounded-[2rem] glass-card p-6 sm:p-8">
        <h3 className="font-head font-700 text-lg text-slate-900 mb-1 text-center">Compare your options</h3>
        <p className="text-slate-500 text-sm text-center mb-6">Your plan: <b className="text-purple-600">{cfg.name} · ₹{cfg.price}</b></p>
        <ComparisonTable plan={plan} />
        <div className="text-center mt-6"><CTAButton testid="unlock-premium-btn-2" onClick={onUnlock}>{cfg.ctaText} · ₹{cfg.price}</CTAButton></div>
      </div>
    </div>
  );
};

const FullReport = ({ report, submissionId, name, email, phone }) => {
  const [selected, setSelected] = useState(new Set());
  const [purchased, setPurchased] = useState(new Set());
  const [showAddonPay, setShowAddonPay] = useState(false);

  const compsOf = (u) => (u.id === "bundle" ? ["resume", "linkedin", "interview"] : [u.id]);
  const isBought = (u) => compsOf(u).every((c) => purchased.has(c));
  const toggle = (u) => setSelected((prev) => {
    const n = new Set(prev);
    if (u.id === "bundle") { if (n.has("bundle")) n.delete("bundle"); else { n.clear(); n.add("bundle"); } }
    else { n.delete("bundle"); if (n.has(u.id)) n.delete(u.id); else n.add(u.id); }
    return n;
  });
  const selectedTotal = UPSELLS.filter((u) => selected.has(u.id)).reduce((s, u) => s + u.price, 0);
  const onAddonSuccess = (list) => {
    setPurchased(new Set([...purchased, ...(list || [])]));
    setSelected(new Set()); setShowAddonPay(false);
    toast.success("Add-ons unlocked — download them below.");
  };

  return (
    <div data-testid="full-report">
      <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6 mb-10 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Icons.CheckCircle2 className="w-8 h-8 text-emerald-500" />
          <div><p className="font-head font-700 text-lg text-slate-900">Your full report is unlocked!</p><p className="text-slate-500 text-sm">Download your premium PDF below.</p></div>
        </div>
        <a href={pdfUrl(submissionId)} target="_blank" rel="noreferrer" data-testid="download-pdf-btn"
           className="inline-flex items-center gap-2 grad-primary-h text-white font-head font-700 rounded-full px-6 py-3 glow-primary hover:scale-105 transition"><Download className="w-5 h-5" /> Download PDF</a>
      </div>

      <ReportRenderer sections={report.sections} />

      {/* Upsells — selectable post-purchase add-ons */}
      <div className="mb-10">
        <div className="flex items-center gap-2.5 mb-4"><div className="w-9 h-9 rounded-xl grad-primary flex items-center justify-center"><Icons.Plus className="w-5 h-5 text-white" strokeWidth={1.8} /></div><h2 className="font-head font-700 text-xl sm:text-2xl text-slate-900">Supercharge Your Career</h2></div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4" data-testid="upsells">
          {UPSELLS.map((u) => {
            const Icon = Icons[u.icon] || Icons.Sparkles;
            const bought = isBought(u);
            const sel = selected.has(u.id);
            return (
              <div key={u.id} data-testid={`upsell-${u.id}`}
                className={`relative rounded-2xl p-5 transition ${bought ? "border-2 border-emerald-300 bg-emerald-50" : u.best ? "grad-primary text-white glow-primary" : sel ? "ring-2 ring-purple-400 bg-purple-50 border border-purple-200" : "glass-card"}`}>
                {u.best && !bought && <span className="absolute top-3 right-3 text-[10px] font-mono bg-white/20 rounded-full px-2 py-0.5">BEST VALUE</span>}
                {bought && <span className="absolute top-3 right-3 text-[10px] font-mono bg-emerald-500 text-white rounded-full px-2 py-0.5">PURCHASED</span>}
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3 ${bought ? "bg-emerald-500" : u.best ? "bg-white/20" : "grad-primary"}`}><Icon className="w-5 h-5 text-white" strokeWidth={1.8} /></div>
                <p className={`font-head font-700 text-sm mb-1 ${u.best && !bought ? "text-white" : "text-slate-900"}`}>{u.title}</p>
                {bought ? (
                  <div className="mt-2 space-y-1.5">
                    {compsOf(u).map((c) => (
                      <a key={c} href={addonPdfUrl(submissionId, c)} target="_blank" rel="noreferrer" data-testid={`addon-download-${c}`} className="flex items-center gap-1.5 text-sm font-medium text-emerald-700 hover:underline"><Download className="w-4 h-4" /> {ADDON_LABELS[c]}</a>
                    ))}
                  </div>
                ) : (
                  <>
                    <p className={`font-head font-800 text-2xl ${u.best ? "text-white" : "text-gradient"}`}>₹{u.price}</p>
                    <button onClick={() => toggle(u)} data-testid={`upsell-select-${u.id}`}
                      className={`mt-3 w-full rounded-full py-2 text-sm font-medium transition ${sel ? "bg-purple-600 text-white" : u.best ? "bg-white text-purple-700 hover:scale-105" : "border border-purple-200 text-purple-700 hover:bg-purple-50"}`}>{sel ? "Selected ✓" : "Add to order"}</button>
                  </>
                )}
              </div>
            );
          })}
        </div>
        {selected.size > 0 && (
          <div className="sticky bottom-4 mt-5 z-30">
            <div className="flex items-center justify-between gap-4 rounded-2xl glass-card border border-purple-200 px-5 py-3 shadow-xl" data-testid="addon-checkout-bar">
              <p className="text-sm text-slate-600">{selected.size} add-on{selected.size > 1 ? "s" : ""} selected · <b className="text-purple-600">₹{selectedTotal}</b></p>
              <CTAButton testid="buy-addons-btn" onClick={() => setShowAddonPay(true)}>Buy Add-ons · ₹{selectedTotal}</CTAButton>
            </div>
          </div>
        )}
      </div>

      {showAddonPay && (
        <PaymentModal submissionId={submissionId} name={name} email={email} phone={phone}
          addonIds={Array.from(selected)} addonLabel={`${selected.size} Career Add-on${selected.size > 1 ? "s" : ""}`} addonAmount={selectedTotal}
          onClose={() => setShowAddonPay(false)} onSuccess={onAddonSuccess} />
      )}
    </div>
  );
};
