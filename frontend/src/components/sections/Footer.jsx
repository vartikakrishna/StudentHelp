import React from "react";
import { Sparkles } from "lucide-react";
import { CTAButton } from "../CTAButton";
import { Reveal } from "../Reveal";

export const Footer = ({ onStart }) => (
  <footer className="relative bg-white" data-testid="footer">
    <div className="max-w-5xl mx-auto px-6 lg:px-8 py-20">
      <Reveal>
        <div className="relative rounded-[2.5rem] grad-primary px-8 py-16 text-center overflow-hidden glow-primary">
          <div className="blob w-64 h-64 bg-white/20 -top-10 -left-10" />
          <div className="blob w-72 h-72 bg-cyan-200/30 bottom-0 right-0" style={{ animationDelay: "3s" }} />
          <h2 className="relative font-head font-800 text-3xl sm:text-5xl tracking-tight text-white">
            Stop guessing. Start knowing.
          </h2>
          <p className="relative mt-5 text-white/85 text-lg max-w-xl mx-auto">
            The career you choose will shape the next 40 years of your life. Spend 2 minutes to get it right.
          </p>
          <div className="relative mt-8 flex justify-center">
            <button
              data-testid="footer-start-btn"
              onClick={onStart}
              className="inline-flex items-center gap-2 bg-white text-purple-700 font-head font-700 rounded-full px-8 py-4 text-lg shadow-xl hover:scale-105 transition-all duration-300"
            >
              Start My Free Career Analysis
            </button>
          </div>
        </div>
      </Reveal>
    </div>
    <div className="border-t border-slate-100">
      <div className="max-w-7xl mx-auto px-6 lg:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl grad-primary flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" strokeWidth={2.2} />
          </div>
          <span className="font-head font-700 text-slate-900">Career Blueprint <span className="text-gradient">AI</span></span>
        </div>
        <p className="text-slate-400 text-sm font-mono">© 2026 Career Blueprint AI · Guidance, not guesswork.</p>
      </div>
    </div>
  </footer>
);
