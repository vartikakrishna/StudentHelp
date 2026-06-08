import React, { useState } from "react";
import { motion } from "framer-motion";
import { Calculator, TrendingDown, AlertTriangle } from "lucide-react";
import axios from "axios";
import { Reveal } from "../Reveal";
import { CTAButton } from "../CTAButton";
import { API } from "../../lib/api";

export const RegretCalculator = ({ onStart }) => {
  const [age, setAge] = useState(22);
  const [current, setCurrent] = useState(6);
  const [dream, setDream] = useState(30);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const calc = async () => {
    setLoading(true);
    try {
      const { data } = await axios.post(`${API}/regret`, {
        age: String(age), current_salary: String(current), dream_salary: String(dream),
      });
      setResult(data);
    } catch (e) {
      setResult(null);
    }
    setLoading(false);
  };

  const inputCls = "w-full rounded-xl bg-white border border-slate-200 px-4 py-3 text-slate-900 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 focus:outline-none transition";

  return (
    <section className="py-24 sm:py-32 grad-soft" id="regret" data-testid="regret-calculator-section">
      <div className="max-w-5xl mx-auto px-6 lg:px-8">
        <Reveal>
          <div className="text-center mb-10">
            <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-4">Career Regret Calculator</p>
            <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight text-slate-900">
              What&apos;s the <span className="text-gradient">real cost</span> of the wrong path?
            </h2>
            <p className="mt-4 text-slate-600 text-lg">Estimate the lifetime opportunity cost of staying on a path that doesn&apos;t fit.</p>
          </div>
        </Reveal>

        <Reveal delay={0.1}>
          <div className="rounded-[2rem] glass-card p-8 sm:p-10">
            <div className="grid sm:grid-cols-3 gap-5 mb-6">
              <div>
                <label className="block text-sm text-slate-700 mb-2 font-medium">Your Age</label>
                <input data-testid="regret-age" type="number" className={inputCls} value={age} onChange={(e) => setAge(e.target.value)} />
              </div>
              <div>
                <label className="block text-sm text-slate-700 mb-2 font-medium">Current Income (₹ LPA)</label>
                <input data-testid="regret-current" type="number" className={inputCls} value={current} onChange={(e) => setCurrent(e.target.value)} />
              </div>
              <div>
                <label className="block text-sm text-slate-700 mb-2 font-medium">Dream Income (₹ LPA)</label>
                <input data-testid="regret-dream" type="number" className={inputCls} value={dream} onChange={(e) => setDream(e.target.value)} />
              </div>
            </div>
            <button data-testid="regret-calc-btn" onClick={calc}
              className="inline-flex items-center gap-2 grad-primary-h text-white font-head font-700 rounded-full px-6 py-3 glow-primary hover:scale-105 transition">
              <Calculator className="w-5 h-5" /> Calculate My Regret Cost
            </button>

            {result && (
              <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="mt-8 rounded-2xl border border-rose-200 bg-rose-50 p-6" data-testid="regret-result">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-rose-100 flex items-center justify-center shrink-0">
                    <TrendingDown className="w-6 h-6 text-rose-500" />
                  </div>
                  <div>
                    <p className="text-slate-600 text-sm">Estimated opportunity cost over {result.years} working years</p>
                    <p className="font-head font-800 text-4xl sm:text-5xl text-rose-600 mt-1">₹{result.opportunity_cost} <span className="text-2xl">LPA-years</span></p>
                    <p className="text-slate-500 text-sm mt-2 flex items-center gap-1.5">
                      <AlertTriangle className="w-4 h-4 text-rose-400" /> Roughly a ₹{result.yearly_gap} LPA gap every single year you stay misaligned.
                    </p>
                    <div className="mt-5"><CTAButton testid="regret-start-btn" onClick={onStart} size="sm">Find My Right Path Now</CTAButton></div>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </Reveal>
      </div>
    </section>
  );
};
