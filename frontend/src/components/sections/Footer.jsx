import React from "react";
import { Compass } from "lucide-react";
import { CTAButton } from "../CTAButton";
import { Reveal } from "../Reveal";

export const Footer = ({ onStart }) => (
  <footer className="relative border-t border-white/8 bg-[#070E1E]" data-testid="footer">
    <div className="max-w-5xl mx-auto px-6 lg:px-8 py-20 text-center">
      <Reveal>
        <h2 className="font-head font-800 text-3xl sm:text-5xl tracking-tight">
          Stop guessing. <span className="text-gold text-glow">Start knowing.</span>
        </h2>
        <p className="mt-5 text-slate-400 text-lg max-w-xl mx-auto">
          The career you choose will shape the next 40 years of your life. Spend 2 minutes to get it right.
        </p>
        <div className="mt-8 flex justify-center">
          <CTAButton testid="footer-start-btn" onClick={onStart}>Start My Free Career Analysis</CTAButton>
        </div>
      </Reveal>
    </div>
    <div className="border-t border-white/5">
      <div className="max-w-7xl mx-auto px-6 lg:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-md gold-gradient flex items-center justify-center">
            <Compass className="w-4 h-4 text-[#1a1000]" strokeWidth={2.2} />
          </div>
          <span className="font-head font-700">Career Blueprint <span className="text-gold">AI</span></span>
        </div>
        <p className="text-slate-500 text-sm font-mono">© 2026 Career Blueprint AI · Guidance, not guesswork.</p>
      </div>
    </div>
  </footer>
);
