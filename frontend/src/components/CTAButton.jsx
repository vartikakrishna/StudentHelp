import React from "react";
import { ArrowRight } from "lucide-react";

export const CTAButton = ({ children, onClick, testid, className = "", icon = true, size = "lg" }) => {
  const pad = size === "lg" ? "px-8 py-4 text-base sm:text-lg" : "px-5 py-2.5 text-sm";
  return (
    <button
      data-testid={testid}
      onClick={onClick}
      className={`group inline-flex items-center justify-center gap-2 grad-primary-h text-white font-head font-600 rounded-full ${pad} glow-primary hover:shadow-[0_18px_44px_-8px_rgba(124,58,237,0.6)] hover:scale-[1.04] active:scale-100 transition-all duration-300 ${className}`}
    >
      {children}
      {icon && <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" strokeWidth={2.2} />}
    </button>
  );
};
