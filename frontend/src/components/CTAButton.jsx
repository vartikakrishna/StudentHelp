import React from "react";
import { ArrowRight } from "lucide-react";

export const CTAButton = ({ children, onClick, testid, className = "", icon = true, size = "lg" }) => {
  const pad = size === "lg" ? "px-8 py-4 text-base sm:text-lg" : "px-6 py-3 text-sm";
  return (
    <button
      data-testid={testid}
      onClick={onClick}
      className={`group inline-flex items-center justify-center gap-2 gold-gradient text-[#1a1000] font-head font-700 rounded-md ${pad} glow-gold hover:shadow-[0_0_36px_rgba(245,158,11,0.55)] hover:scale-[1.03] active:scale-100 transition-all duration-300 ${className}`}
    >
      {children}
      {icon && <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" strokeWidth={2.2} />}
    </button>
  );
};
