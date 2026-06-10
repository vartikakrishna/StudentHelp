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
    <div className="fixed bottom-0 left-0 right-0 z-40 sm:hidden p-3 bg-white/95 backdrop-blur-xl border-t border-[#E2E8F0]" data-testid="sticky-mobile-cta">
      <button onClick={() => onStart()} data-testid="sticky-cta-btn"
        className="w-full h-12 rounded-xl bg-[#2563EB] text-white font-semibold flex items-center justify-center gap-2">
        Get My Career Blueprint · ₹{PRICE.student} <ArrowRight className="w-4 h-4" />
      </button>
    </div>
  );
};
