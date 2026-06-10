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

  const field = "h-12 w-full bg-white border border-[#E2E8F0] text-[#0F172A] rounded-xl px-4 focus:outline-none focus:ring-2 focus:ring-blue-400 placeholder:text-[#94A3B8]";

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-[#0F172A]/50 backdrop-blur-sm" data-testid="lead-gate">
      <motion.div initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md rounded-2xl bg-white border border-[#E2E8F0] p-6 sm:p-8 relative shadow-2xl">
        <button onClick={onClose} className="absolute top-4 right-4" aria-label="close" data-testid="lead-gate-close"><X className="w-5 h-5 text-[#94A3B8]" /></button>
        <p className="text-xs font-semibold tracking-wide uppercase text-[#2563EB] mb-2">Almost there</p>
        <h3 className="font-head font-800 text-2xl text-[#0F172A] mb-1">Where should we send your report?</h3>
        <p className="text-[#64748B] text-sm mb-6">We'll send your unlock confirmation & report link on WhatsApp.</p>
        <form onSubmit={submit} className="space-y-3">
          <input data-testid="lead-name" className={field} placeholder="Your name" value={name} onChange={(e) => setName(e.target.value)} />
          <input data-testid="lead-whatsapp" className={field} placeholder="WhatsApp number (e.g. 98765 43210)" inputMode="tel" value={whatsapp} onChange={(e) => setWhatsapp(e.target.value)} />
          <input data-testid="lead-degree" className={field} placeholder="Your degree / major (e.g. B.Tech CSE)" value={degree} onChange={(e) => setDegree(e.target.value)} />
          {err && <p className="text-rose-500 text-xs" data-testid="lead-error">{err}</p>}
          <button type="submit" disabled={busy} data-testid="lead-continue"
            className="w-full h-12 rounded-xl bg-[#2563EB] text-white font-semibold flex items-center justify-center gap-2 hover:bg-blue-700 transition disabled:opacity-60">
            {busy ? <Loader2 className="w-5 h-5 animate-spin" /> : "Continue to Secure Payment →"}
          </button>
        </form>
        <p className="flex items-center justify-center gap-1.5 text-[#64748B] text-xs mt-4"><ShieldCheck className="w-4 h-4 text-[#10B981]" /> 100% secure · Powered by Razorpay</p>
      </motion.div>
    </div>
  );
};
