import React, { useState } from "react";
import { motion } from "framer-motion";
import { X, ShieldCheck, Loader2 } from "lucide-react";
import { submitLead } from "../lib/api";
import { track } from "../lib/analytics";

// 3-field lead gate (Name, WhatsApp, Degree) shown right before payment.
// Captures the lead even if the user abandons checkout.
export const LeadGate = ({ defaultName = "", defaultDegree = "", userType = "", onClose, onContinue }) => {
  const [name, setName] = useState(defaultName);
  const [whatsapp, setWhatsapp] = useState("");
  const [degree, setDegree] = useState(defaultDegree);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    if (!name.trim() || whatsapp.replace(/\D/g, "").length < 10) {
      setErr("Please enter your name and a valid WhatsApp number.");
      return;
    }
    setBusy(true);
    try {
      await submitLead({ name: name.trim(), whatsapp: whatsapp.trim(), degree, source: "pre_payment", user_type: userType });
      track("lead_submit", { source: "pre_payment", user_type: userType });
    } catch (_) { /* don't block checkout on lead-store failure */ }
    setBusy(false);
    onContinue({ name: name.trim(), whatsapp: whatsapp.trim(), degree });
  };

  const field = "h-12 w-full bg-black/40 border border-white/10 text-white rounded-xl px-4 focus:outline-none focus:ring-2 focus:ring-purple-500 placeholder:text-slate-500";

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm" data-testid="lead-gate">
      <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md rounded-3xl bg-[#0F0F14] border border-white/10 p-6 sm:p-8 relative">
        <button onClick={onClose} className="absolute top-4 right-4" aria-label="close" data-testid="lead-gate-close"><X className="w-5 h-5 text-slate-400" /></button>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-400 mb-2">Almost there</p>
        <h3 className="font-head font-700 text-2xl text-white mb-1">Where should we send your report?</h3>
        <p className="text-slate-400 text-sm mb-6">We'll send your unlock confirmation & report link on WhatsApp.</p>
        <form onSubmit={submit} className="space-y-3">
          <input data-testid="lead-name" className={field} placeholder="Your name" value={name} onChange={(e) => setName(e.target.value)} />
          <input data-testid="lead-whatsapp" className={field} placeholder="WhatsApp number (e.g. 98765 43210)" inputMode="tel" value={whatsapp} onChange={(e) => setWhatsapp(e.target.value)} />
          <input data-testid="lead-degree" className={field} placeholder="Your degree / major (e.g. B.Tech CSE)" value={degree} onChange={(e) => setDegree(e.target.value)} />
          {err && <p className="text-rose-400 text-xs" data-testid="lead-error">{err}</p>}
          <button type="submit" disabled={busy} data-testid="lead-continue"
            className="w-full h-13 py-3.5 rounded-full bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-400 text-white font-bold flex items-center justify-center gap-2 disabled:opacity-60">
            {busy ? <Loader2 className="w-5 h-5 animate-spin" /> : "Continue to Secure Payment →"}
          </button>
        </form>
        <p className="flex items-center justify-center gap-1.5 text-slate-500 text-xs mt-4"><ShieldCheck className="w-4 h-4 text-emerald-400" /> 100% secure · Powered by Razorpay</p>
      </motion.div>
    </div>
  );
};
