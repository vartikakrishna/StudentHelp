import React from "react";
import { motion } from "framer-motion";
import { CheckCircle2, Sparkles } from "lucide-react";
import { CTAButton } from "../CTAButton";

const BENEFITS = [
  "Careers where you're most likely to succeed",
  "Skills you should build next",
  "Your real income potential",
  "AI-proof career options",
  "Your hidden strengths",
  "Your personalized roadmap",
];

export const Hero = ({ onStart }) => {
  return (
    <section className="relative min-h-screen flex items-center overflow-hidden" data-testid="hero-section">
      {/* background image + overlays */}
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: "url(https://images.unsplash.com/photo-1556139930-c23fa4a4f934?crop=entropy&cs=srgb&fm=jpg&q=85&w=1920)" }}
      />
      <div className="absolute inset-0 bg-[#040914]/80" />
      <div className="absolute inset-0 bg-gradient-to-b from-[#040914]/70 via-[#040914]/85 to-[#040914]" />
      <div className="aurora-blob w-[480px] h-[480px] bg-[#F59E0B]/20 -top-20 -left-20" />
      <div className="aurora-blob w-[420px] h-[420px] bg-[#1d4ed8]/20 bottom-0 right-0" style={{ animationDelay: "4s" }} />

      <div className="relative max-w-7xl mx-auto px-6 lg:px-8 pt-28 pb-20 w-full">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          className="inline-flex items-center gap-2 rounded-full border border-amber-500/30 bg-amber-500/10 px-4 py-1.5 mb-7"
        >
          <Sparkles className="w-4 h-4 text-gold" />
          <span className="font-mono text-xs tracking-[0.18em] uppercase text-amber-200">AI Career Intelligence</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="font-head font-800 tracking-tighter leading-[1.05] text-4xl sm:text-5xl lg:text-7xl max-w-4xl"
        >
          Your Future Is <span className="text-gold text-glow">Too Important</span> To Leave To Guesswork.
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.25 }}
          className="mt-6 text-base sm:text-lg text-slate-300 max-w-2xl leading-relaxed"
        >
          In just 5 minutes, discover the career path that matches your personality,
          strengths, interests and future market demand — before you waste years on the wrong one.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.35 }}
          className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2.5 max-w-2xl"
        >
          {BENEFITS.map((b) => (
            <div key={b} className="flex items-center gap-2.5 text-slate-200 text-sm sm:text-base">
              <CheckCircle2 className="w-5 h-5 text-gold shrink-0" strokeWidth={1.8} />
              {b}
            </div>
          ))}
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.5 }}
          className="mt-10 flex flex-col sm:flex-row items-start sm:items-center gap-4"
        >
          <CTAButton testid="start-analysis-btn" onClick={onStart}>Start Free Analysis</CTAButton>
          <span className="text-slate-400 text-sm font-mono">No signup · Under 2 minutes · Free preview</span>
        </motion.div>
      </div>
    </section>
  );
};
