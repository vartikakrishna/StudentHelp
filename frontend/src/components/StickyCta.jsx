import React, { useEffect, useState } from "react";
import { ArrowRight } from "lucide-react";
import { PRICE } from "../lib/config";

// Mobile-only sticky checkout bar that appears after scrolling past the hero.
export const StickyCta = ({ onStart }) => {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const onScroll = () => setShow(window.scrollY > 700);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  if (!show) return null;
  return (
    <div className="fixed bottom-0 left-0 right-0 z-40 sm:hidden p-3 bg-[#05050A]/90 backdrop-blur-xl border-t border-white/10" data-testid="sticky-mobile-cta">
      <button onClick={() => onStart()} data-testid="sticky-cta-btn"
        className="w-full h-12 rounded-full bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-400 text-white font-bold flex items-center justify-center gap-2">
        Get My Career Blueprint · ₹{PRICE.student} <ArrowRight className="w-4 h-4" />
      </button>
    </div>
  );
};
