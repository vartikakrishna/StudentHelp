import React, { useState } from "react";
import { MessageCircle, X } from "lucide-react";
import { whatsappLink } from "../lib/config";
import { track } from "../lib/analytics";

export const WhatsAppFab = () => {
  const [open, setOpen] = useState(false);
  const onChat = () => { track("whatsapp_click", { location: "fab" }); window.open(whatsappLink(), "_blank"); };

  return (
    <div className="fixed bottom-24 right-5 z-[55] flex flex-col items-end gap-3" data-testid="whatsapp-fab">
      {open && (
        <div className="w-64 rounded-2xl bg-[#0F0F14] border border-white/10 shadow-2xl p-4 animate-in" data-testid="whatsapp-card">
          <div className="flex items-start justify-between">
            <p className="font-head font-700 text-white text-sm">Need help? 💬</p>
            <button onClick={() => setOpen(false)} aria-label="close"><X className="w-4 h-4 text-slate-400" /></button>
          </div>
          <p className="text-slate-400 text-xs mt-1 mb-3">Questions about your report, payment or access? Chat with us on WhatsApp.</p>
          <button onClick={onChat} data-testid="whatsapp-chat-btn"
            className="w-full rounded-full bg-[#25D366] text-white font-semibold text-sm py-2.5 hover:brightness-110 transition">
            Chat With Us
          </button>
        </div>
      )}
      <button onClick={() => (open ? onChat() : setOpen(true))} aria-label="WhatsApp support"
        className="w-14 h-14 rounded-full bg-[#25D366] text-white flex items-center justify-center shadow-[0_0_24px_rgba(37,211,102,0.5)] hover:scale-105 transition relative">
        <MessageCircle className="w-7 h-7" />
        <span className="absolute -top-0.5 -right-0.5 w-3.5 h-3.5 bg-white rounded-full border-2 border-[#25D366]" />
      </button>
    </div>
  );
};
