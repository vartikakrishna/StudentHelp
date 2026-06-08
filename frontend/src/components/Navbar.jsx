import React, { useState, useEffect } from "react";
import { Sparkles } from "lucide-react";
import { CTAButton } from "./CTAButton";

export const Navbar = ({ onStart }) => {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const h = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", h);
    return () => window.removeEventListener("scroll", h);
  }, []);
  return (
    <header
      data-testid="navbar"
      className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
        scrolled ? "glass border-b border-slate-200/70" : "bg-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl grad-primary flex items-center justify-center shadow-md shadow-indigo-500/30">
            <Sparkles className="w-5 h-5 text-white" strokeWidth={2.2} />
          </div>
          <span className="font-head font-700 text-lg tracking-tight text-slate-900">
            Career Blueprint <span className="text-gradient">AI</span>
          </span>
        </div>
        <CTAButton testid="nav-start-btn" onClick={onStart} size="sm" icon={false}>
          Start Free Analysis
        </CTAButton>
      </div>
    </header>
  );
};
