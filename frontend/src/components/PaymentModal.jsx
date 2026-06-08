import React, { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Smartphone, CreditCard, Landmark, Wallet, ShieldCheck, Loader2, CheckCircle2, Sparkles } from "lucide-react";
import { createOrder, verifyPayment, createAddonOrder, verifyAddonPayment } from "../lib/api";

const METHODS = [
  { key: "upi", label: "UPI", icon: Smartphone, hint: "GPay · PhonePe · Paytm" },
  { key: "card", label: "Cards", icon: CreditCard, hint: "Visa · Mastercard · RuPay" },
  { key: "netbanking", label: "Net Banking", icon: Landmark, hint: "All major banks" },
  { key: "wallet", label: "Wallets", icon: Wallet, hint: "Paytm · Amazon Pay" },
];

const loadRazorpay = () =>
  new Promise((resolve) => {
    if (window.Razorpay) return resolve(true);
    const s = document.createElement("script");
    s.src = "https://checkout.razorpay.com/v1/checkout.js";
    s.onload = () => resolve(true);
    s.onerror = () => resolve(false);
    document.body.appendChild(s);
  });

export const PaymentModal = ({ submissionId, name, email, phone, addonIds = null, addonLabel = "", addonAmount = 0, onClose, onSuccess }) => {
  const [order, setOrder] = useState(null);
  const [method, setMethod] = useState("upi");
  const [stage, setStage] = useState("loading"); // loading | pay | processing | done | error
  const [vpa, setVpa] = useState("");
  const isAddon = Array.isArray(addonIds) && addonIds.length > 0;

  const finish = useCallback(async (verifyPayload) => {
    setStage("processing");
    try {
      if (isAddon) {
        const res = await verifyAddonPayment({ ...verifyPayload, addon_ids: addonIds });
        setStage("done");
        setTimeout(() => onSuccess(res.purchased_addons), 1100);
      } else {
        const res = await verifyPayment(verifyPayload);
        setStage("done");
        setTimeout(() => onSuccess(res.report, res.name), 1100);
      }
    } catch (e) {
      setStage("error");
    }
  }, [onSuccess, isAddon, addonIds]);

  const openLive = useCallback(async (ord) => {
    const ok = await loadRazorpay();
    if (!ok) { setStage("error"); return; }
    const rzp = new window.Razorpay({
      key: ord.key_id, amount: ord.amount, currency: ord.currency, order_id: ord.order_id,
      name: "Career Blueprint AI", description: isAddon ? (ord.label || "Career Add-ons") : "Full Career Blueprint (PDF)",
      prefill: { name: name || "", email: email || "", contact: phone || "" },
      theme: { color: "#7C3AED" },
      handler: (resp) => finish({
        submission_id: submissionId,
        razorpay_order_id: resp.razorpay_order_id,
        razorpay_payment_id: resp.razorpay_payment_id,
        razorpay_signature: resp.razorpay_signature,
      }),
      modal: { ondismiss: () => setStage("pay") },
    });
    rzp.open();
  }, [finish, name, email, phone, submissionId, isAddon]);

  useEffect(() => {
    const orderPromise = isAddon ? createAddonOrder(submissionId, addonIds) : createOrder(submissionId);
    orderPromise
      .then((o) => {
        setOrder(o);
        if (o.mode === "live") { setStage("processing"); openLive(o); }
        else setStage("pay");
      })
      .catch(() => setStage("error"));
  }, [submissionId, openLive, isAddon, addonIds]);

  const payMock = async () => {
    setStage("processing");
    await new Promise((r) => setTimeout(r, 1500));
    finish({ submission_id: submissionId, razorpay_order_id: order.order_id, razorpay_payment_id: "", razorpay_signature: "" });
  };

  const amount = order ? order.amount / 100 : (isAddon ? addonAmount : 199);
  const isLive = order?.mode === "live";
  const productLabel = isAddon ? (addonLabel || "Career Add-ons") : (order?.plan === "professional" ? "Professional Career Intelligence Report" : "Student Career Blueprint");

  return (
    <div className="fixed inset-0 z-[200] flex items-end sm:items-center justify-center p-0 sm:p-6" data-testid="razorpay-mock-modal">
      <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" onClick={onClose} />
      <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} className="relative w-full sm:max-w-md bg-white border border-slate-200 rounded-t-[2rem] sm:rounded-[2rem] overflow-hidden shadow-2xl">
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl grad-primary flex items-center justify-center"><Sparkles className="w-5 h-5 text-white" strokeWidth={2.2} /></div>
            <div><p className="font-head font-700 text-sm leading-tight text-slate-900">Career Blueprint AI</p><p className="text-[11px] text-slate-400 font-mono">Secure Checkout</p></div>
          </div>
          <button onClick={onClose} data-testid="payment-close-btn" className="text-slate-400 hover:text-slate-700"><X className="w-5 h-5" /></button>
        </div>

        <div className="px-6 py-5 flex items-center justify-between border-b border-slate-100 bg-indigo-50/40">
          <div><p className="text-slate-600 text-sm">{productLabel}</p><p className="text-xs text-slate-400 font-mono">{name}</p></div>
          <p className="font-head font-800 text-3xl text-gradient">₹{amount}</p>
        </div>

        <div className="px-6 py-5">
          <AnimatePresence mode="wait">
            {stage === "loading" && (
              <motion.div key="l" className="py-10 flex flex-col items-center text-slate-500"><Loader2 className="w-7 h-7 animate-spin text-purple-500 mb-3" />Setting up secure payment…</motion.div>
            )}

            {stage === "pay" && (
              <motion.div key="p" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                {isLive ? (
                  <button data-testid="pay-now-btn" onClick={() => { setStage("processing"); openLive(order); }} className="w-full grad-primary-h text-white font-head font-700 rounded-full py-3.5 glow-primary hover:scale-[1.02] transition">Pay ₹{amount} with Razorpay</button>
                ) : (
                  <>
                    <div className="grid grid-cols-2 gap-2.5 mb-5">
                      {METHODS.map((m) => (
                        <button key={m.key} data-testid={`pay-method-${m.key}`} onClick={() => setMethod(m.key)}
                          className={`flex items-center gap-2.5 rounded-2xl border p-3 text-left transition-all ${method === m.key ? "border-purple-400 bg-purple-50 ring-2 ring-purple-200" : "border-slate-200 hover:border-purple-300"}`}>
                          <m.icon className={`w-5 h-5 ${method === m.key ? "text-purple-600" : "text-slate-400"}`} />
                          <div><p className="text-sm font-medium text-slate-900">{m.label}</p><p className="text-[10px] text-slate-400">{m.hint}</p></div>
                        </button>
                      ))}
                    </div>
                    {method === "upi" && <input data-testid="pay-upi-input" value={vpa} onChange={(e) => setVpa(e.target.value)} placeholder="yourname@upi" className="w-full rounded-xl bg-white border border-slate-200 px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 focus:outline-none mb-4" />}
                    <button data-testid="pay-now-btn" onClick={payMock} className="w-full grad-primary-h text-white font-head font-700 rounded-full py-3.5 glow-primary hover:scale-[1.02] transition">Pay ₹{amount} Securely</button>
                  </>
                )}
                <p className="mt-3 flex items-center justify-center gap-1.5 text-[11px] text-slate-400 font-mono"><ShieldCheck className="w-3.5 h-3.5" /> 256-bit encrypted · {isLive ? "Razorpay" : "Razorpay (Test)"}</p>
              </motion.div>
            )}

            {stage === "processing" && (
              <motion.div key="pr" className="py-10 flex flex-col items-center text-slate-600"><Loader2 className="w-8 h-8 animate-spin text-purple-500 mb-4" />{isLive ? "Opening secure Razorpay…" : "Confirming your payment…"}</motion.div>
            )}

            {stage === "done" && (
              <motion.div key="d" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="py-10 flex flex-col items-center text-center"><CheckCircle2 className="w-14 h-14 text-emerald-500 mb-4" /><p className="font-head font-700 text-xl text-slate-900">Payment Successful!</p><p className="text-slate-500 text-sm mt-1">{isAddon ? "Unlocking your add-ons…" : "Unlocking your full Career Blueprint…"}</p></motion.div>
            )}

            {stage === "error" && (
              <motion.div key="e" className="py-10 flex flex-col items-center text-center"><p className="text-rose-500 mb-4">Payment could not be completed.</p><button onClick={() => setStage("pay")} className="text-purple-600 underline">Try again</button></motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
  );
};
