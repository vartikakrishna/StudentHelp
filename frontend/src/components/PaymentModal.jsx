import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Smartphone, CreditCard, Landmark, Wallet, ShieldCheck, Loader2, CheckCircle2, Lock } from "lucide-react";
import { createOrder, verifyPayment } from "../lib/api";

const METHODS = [
  { key: "upi", label: "UPI", icon: Smartphone, hint: "GPay · PhonePe · Paytm" },
  { key: "card", label: "Cards", icon: CreditCard, hint: "Visa · Mastercard · RuPay" },
  { key: "netbanking", label: "Net Banking", icon: Landmark, hint: "All major banks" },
  { key: "wallet", label: "Wallets", icon: Wallet, hint: "Paytm · Amazon Pay" },
];

export const PaymentModal = ({ submissionId, name, onClose, onSuccess }) => {
  const [order, setOrder] = useState(null);
  const [method, setMethod] = useState("upi");
  const [stage, setStage] = useState("loading"); // loading | pay | processing | done | error
  const [vpa, setVpa] = useState("");

  useEffect(() => {
    createOrder(submissionId)
      .then((o) => { setOrder(o); setStage("pay"); })
      .catch(() => setStage("error"));
  }, [submissionId]);

  const pay = async () => {
    setStage("processing");
    try {
      // Mock gateway: in live mode the Razorpay SDK handles this and returns a signature.
      await new Promise((r) => setTimeout(r, 1600));
      const res = await verifyPayment({
        submission_id: submissionId,
        razorpay_order_id: order.order_id,
        razorpay_payment_id: "",
        razorpay_signature: "",
      });
      setStage("done");
      setTimeout(() => onSuccess(res.report, res.name), 1100);
    } catch (e) {
      setStage("error");
    }
  };

  const amount = order ? order.amount / 100 : 199;

  return (
    <div className="fixed inset-0 z-[200] flex items-end sm:items-center justify-center p-0 sm:p-6" data-testid="razorpay-mock-modal">
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" onClick={onClose} />
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative w-full sm:max-w-md bg-[#0B1426] border border-white/10 rounded-t-3xl sm:rounded-2xl overflow-hidden shadow-2xl"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/8 bg-[#091226]">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-md gold-gradient flex items-center justify-center">
              <Lock className="w-4 h-4 text-[#1a1000]" strokeWidth={2.2} />
            </div>
            <div>
              <p className="font-head font-700 text-sm leading-tight">Career Blueprint AI</p>
              <p className="text-[11px] text-slate-400 font-mono">Secure Checkout</p>
            </div>
          </div>
          <button onClick={onClose} data-testid="payment-close-btn" className="text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Amount */}
        <div className="px-6 py-5 flex items-center justify-between border-b border-white/8">
          <div>
            <p className="text-slate-400 text-sm">Full Career Blueprint (PDF)</p>
            <p className="text-xs text-slate-500 font-mono">{name}</p>
          </div>
          <p className="font-head font-800 text-3xl text-gold">₹{amount}</p>
        </div>

        <div className="px-6 py-5">
          <AnimatePresence mode="wait">
            {stage === "loading" && (
              <motion.div key="l" className="py-10 flex flex-col items-center text-slate-400">
                <Loader2 className="w-7 h-7 animate-spin text-gold mb-3" />
                Setting up secure payment…
              </motion.div>
            )}

            {stage === "pay" && (
              <motion.div key="p" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <div className="grid grid-cols-2 gap-2.5 mb-5">
                  {METHODS.map((m) => (
                    <button
                      key={m.key}
                      data-testid={`pay-method-${m.key}`}
                      onClick={() => setMethod(m.key)}
                      className={`flex items-center gap-2.5 rounded-xl border p-3 text-left transition-all ${
                        method === m.key ? "border-amber-500 bg-amber-500/10" : "border-white/10 hover:border-white/25"
                      }`}
                    >
                      <m.icon className={`w-5 h-5 ${method === m.key ? "text-gold" : "text-slate-400"}`} />
                      <div>
                        <p className="text-sm font-medium text-white">{m.label}</p>
                        <p className="text-[10px] text-slate-500">{m.hint}</p>
                      </div>
                    </button>
                  ))}
                </div>

                {method === "upi" && (
                  <input
                    data-testid="pay-upi-input"
                    value={vpa}
                    onChange={(e) => setVpa(e.target.value)}
                    placeholder="yourname@upi"
                    className="w-full rounded-lg bg-[#091226] border border-white/10 px-4 py-3 text-white placeholder:text-slate-500 focus:border-amber-500/60 focus:outline-none mb-4"
                  />
                )}

                <button
                  data-testid="pay-now-btn"
                  onClick={pay}
                  className="w-full gold-gradient text-[#1a1000] font-head font-700 rounded-lg py-3.5 glow-gold hover:scale-[1.02] transition"
                >
                  Pay ₹{amount} Securely
                </button>
                <p className="mt-3 flex items-center justify-center gap-1.5 text-[11px] text-slate-500 font-mono">
                  <ShieldCheck className="w-3.5 h-3.5" /> 256-bit encrypted · {order?.mode === "live" ? "Razorpay" : "Razorpay (Test)"}
                </p>
              </motion.div>
            )}

            {stage === "processing" && (
              <motion.div key="pr" className="py-10 flex flex-col items-center text-slate-300">
                <Loader2 className="w-8 h-8 animate-spin text-gold mb-4" />
                Confirming your payment…
              </motion.div>
            )}

            {stage === "done" && (
              <motion.div key="d" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="py-10 flex flex-col items-center text-center">
                <CheckCircle2 className="w-14 h-14 text-emerald-400 mb-4" />
                <p className="font-head font-700 text-xl text-white">Payment Successful!</p>
                <p className="text-slate-400 text-sm mt-1">Unlocking your full Career Blueprint…</p>
              </motion.div>
            )}

            {stage === "error" && (
              <motion.div key="e" className="py-10 flex flex-col items-center text-center">
                <p className="text-red-400 mb-4">Payment could not be completed.</p>
                <button onClick={() => setStage("pay")} className="text-gold underline">Try again</button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
  );
};
