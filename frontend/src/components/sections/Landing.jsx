import React, { useState } from "react";
import { motion } from "framer-motion";
import * as Icons from "lucide-react";
import {
  ArrowRight, Check, ShieldCheck, Bot, TrendingUp, Target, Wrench, Map, LineChart,
  Star, BadgeCheck, Lock, Zap, AlertTriangle, Sparkles, ChevronDown,
} from "lucide-react";
import { PRICE, whatsappLink } from "../../lib/config";
import { track } from "../../lib/analytics";

const fade = { initial: { opacity: 0, y: 24 }, whileInView: { opacity: 1, y: 0 }, viewport: { once: true, margin: "-60px" } };
const Glow = ({ className }) => <div className={`pointer-events-none absolute rounded-full blur-[120px] opacity-30 ${className}`} />;

const PrimaryBtn = ({ children, onClick, testid, className = "" }) => (
  <button onClick={onClick} data-testid={testid}
    className={`inline-flex items-center justify-center gap-2 h-14 px-8 rounded-full bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-400 text-white font-bold text-base sm:text-lg hover:shadow-[0_0_34px_rgba(168,85,247,0.5)] transition-all hover:-translate-y-0.5 active:translate-y-0 ${className}`}>
    {children}
  </button>
);

const SectionLabel = ({ children }) => (
  <p className="font-mono text-xs tracking-[0.25em] uppercase text-purple-400 mb-3">{children}</p>
);

// ---------------- NAV ----------------
const Nav = ({ onStart }) => (
  <header className="fixed top-0 inset-x-0 z-40 bg-[#05050A]/70 backdrop-blur-xl border-b border-white/5">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <span className="font-head font-800 text-lg text-white tracking-tight">MapMy<span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-300">Career</span></span>
      <nav className="hidden md:flex items-center gap-8 text-sm text-slate-300">
        <a href="#how" className="hover:text-white transition">How it works</a>
        <a href="#features" className="hover:text-white transition">Features</a>
        <a href="#pricing" className="hover:text-white transition">Pricing</a>
        <a href="#faq" className="hover:text-white transition">FAQ</a>
      </nav>
      <button onClick={() => onStart()} data-testid="nav-cta"
        className="h-10 px-5 rounded-full bg-white/10 border border-white/15 text-white text-sm font-semibold hover:bg-white/20 transition">Get Blueprint</button>
    </div>
  </header>
);

// ---------------- HERO ----------------
const DEGREES = ["B.Tech CSE", "B.Tech ECE", "BCA", "MCA", "B.Com", "BBA", "MBA", "B.Sc", "B.A"];
const Hero = ({ onStart }) => {
  const [degree, setDegree] = useState("");
  const go = () => { track("cta_click", { location: "hero", degree }); onStart(degree); };
  return (
    <section className="relative overflow-hidden pt-32 pb-20 md:pt-40 md:pb-28">
      <Glow className="bg-purple-600 w-[420px] h-[420px] -top-20 -left-20" />
      <Glow className="bg-cyan-500 w-[380px] h-[380px] top-10 right-0" />
      <div className="max-w-4xl mx-auto px-4 sm:px-6 text-center relative">
        <motion.div {...fade} className="inline-flex items-center gap-2 rounded-full bg-white/5 border border-white/10 px-4 py-1.5 text-xs text-slate-300 mb-6">
          <Sparkles className="w-3.5 h-3.5 text-cyan-300" /> AI-powered career intelligence for Indian students
        </motion.div>
        <motion.h1 {...fade} transition={{ delay: 0.05 }} className="font-head font-800 text-4xl sm:text-5xl lg:text-6xl tracking-tight leading-[1.08] text-white">
          Most Students Will Spend 4 Years Preparing For A Career That{" "}
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-300">AI May Change.</span>
        </motion.h1>
        <motion.p {...fade} transition={{ delay: 0.12 }} className="text-slate-300 text-base sm:text-lg mt-6 max-w-2xl mx-auto leading-relaxed">
          MapMyCareer analyzes your degree, skills, interests and future job trends to generate a personalized AI career roadmap, salary outlook, skill-gap analysis and automation-risk report.
        </motion.p>

        <motion.div {...fade} transition={{ delay: 0.2 }} className="mt-9 max-w-xl mx-auto">
          <div className="flex flex-col sm:flex-row gap-3 items-stretch">
            <input list="degree-list" value={degree} onChange={(e) => setDegree(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && go()} data-testid="hero-degree-input"
              placeholder="Enter your degree / major (e.g. B.Tech CSE)"
              className="h-14 flex-1 bg-black/40 border border-white/10 text-white rounded-full px-6 focus:outline-none focus:ring-2 focus:ring-purple-500 placeholder:text-slate-500" />
            <datalist id="degree-list">{DEGREES.map((d) => <option key={d} value={d} />)}</datalist>
            <PrimaryBtn onClick={go} testid="hero-cta" className="shrink-0">Generate My Free Career Blueprint <ArrowRight className="w-5 h-5" /></PrimaryBtn>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2 mt-5 text-xs text-slate-400">
            {["Used by students across India", "Instant report generation", "Mobile-friendly", "No hidden charges"].map((t) => (
              <span key={t} className="inline-flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-emerald-400" /> {t}</span>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
};

// ---------------- PAIN ----------------
const STATS = [
  { icon: AlertTriangle, tone: "text-rose-400", v: "Years behind", l: "College syllabi often lag real industry skills by years." },
  { icon: Bot, tone: "text-amber-400", v: "AI disruption", l: "Routine entry-level tasks are the first to be automated." },
  { icon: Target, tone: "text-orange-400", v: "Late clarity", l: "Most students discover a career mismatch only after graduating." },
];
const Pain = () => (
  <section className="py-20 md:py-28 relative">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 grid lg:grid-cols-2 gap-10 items-center">
      <motion.div {...fade}>
        <SectionLabel>The hard truth</SectionLabel>
        <h2 className="font-head font-700 text-3xl sm:text-4xl tracking-tight text-white leading-tight">The Job Market Is Changing Faster Than College Syllabi.</h2>
        <p className="text-slate-400 mt-5 leading-relaxed">AI is reshaping entire industries while curricula stay frozen. Too many students graduate with outdated skills and realize the mismatch only when it's expensive to fix. The earlier you see it, the easier it is to win.</p>
      </motion.div>
      <div className="grid gap-4">
        {STATS.map((s, i) => (
          <motion.div key={i} {...fade} transition={{ delay: i * 0.08 }}
            className="rounded-2xl bg-[#0A0A0F] border border-white/5 p-5 flex items-start gap-4 hover:border-rose-500/30 transition">
            <div className="w-11 h-11 rounded-xl bg-white/5 flex items-center justify-center shrink-0"><s.icon className={`w-5 h-5 ${s.tone}`} /></div>
            <div><p className="font-head font-700 text-white">{s.v}</p><p className="text-slate-400 text-sm mt-0.5">{s.l}</p></div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

// ---------------- HOW IT WORKS ----------------
const STEPS = [
  { n: "01", t: "Answer a few quick questions", d: "Your degree, skills, interests and goals — takes ~3 minutes." },
  { n: "02", t: "Our AI analyzes you vs the market", d: "Against 300+ careers, salary data, AI-risk and future demand." },
  { n: "03", t: "Get your personalized blueprint", d: "Career match, skill-gaps, salary forecast and a year-by-year roadmap." },
];
const How = () => (
  <section id="how" className="py-20 md:py-28">
    <div className="max-w-7xl mx-auto px-4 sm:px-6">
      <motion.div {...fade} className="text-center mb-12"><SectionLabel>How it works</SectionLabel><h2 className="font-head font-700 text-3xl sm:text-4xl text-white">Clarity in 3 simple steps</h2></motion.div>
      <div className="grid md:grid-cols-3 gap-5">
        {STEPS.map((s, i) => (
          <motion.div key={i} {...fade} transition={{ delay: i * 0.08 }} className="rounded-2xl bg-[#0A0A0F] border border-white/5 p-7 hover:border-purple-500/30 transition">
            <p className="font-mono text-purple-400 text-sm mb-3">{s.n}</p>
            <p className="font-head font-700 text-white text-lg mb-1.5">{s.t}</p>
            <p className="text-slate-400 text-sm leading-relaxed">{s.d}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

// ---------------- REPORT TEASE ----------------
const ReportTease = ({ onStart }) => (
  <section className="py-20 md:py-28">
    <div className="max-w-5xl mx-auto px-4 sm:px-6">
      <motion.div {...fade} className="text-center mb-10"><SectionLabel>Your report preview</SectionLabel><h2 className="font-head font-700 text-3xl sm:text-4xl text-white">A premium, personalized career blueprint</h2></motion.div>
      <motion.div {...fade} className="relative rounded-3xl bg-[#0A0A0F] border border-white/10 overflow-hidden">
        <div className="p-6 sm:p-8 grid sm:grid-cols-3 gap-4">
          {[{ l: "AI Automation Risk", v: "Low", c: "text-emerald-400" }, { l: "Career Fit Score", v: "86%", c: "text-cyan-300" }, { l: "Salary Potential", v: "₹18 LPA", c: "text-purple-300" }].map((m, i) => (
            <div key={i} className="rounded-2xl bg-white/[0.03] border border-white/10 p-5 text-center">
              <p className={`font-head font-800 text-3xl ${m.c}`}>{m.v}</p><p className="text-slate-400 text-xs mt-1">{m.l}</p>
            </div>
          ))}
        </div>
        <div className="px-6 sm:px-8 pb-8 space-y-3">
          {["Skill Gap Analysis", "Future Job Outlook", "Recommended Career Paths", "Year 1-4 Learning Blueprint"].map((r) => (
            <div key={r} className="flex items-center justify-between rounded-xl bg-white/[0.02] border border-white/5 px-4 py-3">
              <span className="text-slate-300 text-sm">{r}</span>
              <div className="w-28 h-2 rounded-full bg-white/10 overflow-hidden"><div className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400" style={{ width: "72%" }} /></div>
            </div>
          ))}
        </div>
        <div className="absolute inset-x-0 bottom-0 h-2/3 bg-gradient-to-t from-[#05050A] via-[#05050A]/85 to-transparent backdrop-blur-[3px] flex flex-col items-center justify-end pb-8">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-400 flex items-center justify-center mb-3"><Lock className="w-7 h-7 text-white" /></div>
          <p className="font-head font-700 text-white text-xl mb-4">Unlock Full Personalized Results</p>
          <PrimaryBtn onClick={() => onStart()} testid="tease-cta">Generate My Free Preview <ArrowRight className="w-5 h-5" /></PrimaryBtn>
        </div>
      </motion.div>
    </div>
  </section>
);

// ---------------- FEATURES ----------------
const FEATURES = [
  { icon: Bot, t: "AI Automation Risk Score", d: "Know how vulnerable your path is to AI disruption — before you commit years to it." },
  { icon: TrendingUp, t: "Salary Growth Forecast", d: "Projected earning potential over the next 5–10 years on your path." },
  { icon: Target, t: "Career Match Analysis", d: "Careers aligned with your strengths, interests and the real market." },
  { icon: Wrench, t: "Skill Gap Report", d: "The exact skills employers expect — and which ones you're missing." },
  { icon: Map, t: "Personalized Learning Roadmap", d: "What to learn next and in what order, year by year." },
  { icon: LineChart, t: "Future Industry Trends", d: "See where your industry is heading before everyone else does." },
];
const Features = () => (
  <section id="features" className="py-20 md:py-28">
    <div className="max-w-7xl mx-auto px-4 sm:px-6">
      <motion.div {...fade} className="text-center mb-12"><SectionLabel>What you get</SectionLabel><h2 className="font-head font-700 text-3xl sm:text-4xl text-white">Everything in your blueprint</h2></motion.div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {FEATURES.map((f, i) => (
          <motion.div key={i} {...fade} transition={{ delay: (i % 3) * 0.07 }}
            className="rounded-2xl bg-[#0A0A0F] border border-white/5 p-6 hover:border-purple-500/30 hover:-translate-y-1 transition-all">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500/20 to-cyan-400/20 border border-white/10 flex items-center justify-center mb-4"><f.icon className="w-6 h-6 text-cyan-300" /></div>
            <p className="font-head font-700 text-white text-lg mb-1.5">{f.t}</p>
            <p className="text-slate-400 text-sm leading-relaxed">{f.d}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

// ---------------- SOCIAL PROOF ----------------
const TESTIMONIALS = [
  { n: "Rahul S.", c: "#6366F1", s: "Final-Year BCA · Pune", q: "MapMyCareer helped me realize which skills companies actually want. I completely changed my learning roadmap." },
  { n: "Sneha M.", c: "#A855F7", s: "B.Tech ECE · Chennai", q: "The report showed exactly where I was falling behind and what to focus on next." },
  { n: "Arjun K.", c: "#06B6D4", s: "B.Com · Bangalore", q: "I finally have clarity on which career path actually fits me — and a real plan." },
];
const SocialProof = () => (
  <section className="py-20 md:py-28">
    <div className="max-w-7xl mx-auto px-4 sm:px-6">
      <motion.div {...fade} className="text-center mb-12"><SectionLabel>Loved by students</SectionLabel><h2 className="font-head font-700 text-3xl sm:text-4xl text-white">What students are saying</h2></motion.div>
      <div className="grid md:grid-cols-3 gap-5">
        {TESTIMONIALS.map((t, i) => (
          <motion.div key={i} {...fade} transition={{ delay: i * 0.08 }} className="rounded-2xl bg-[#0A0A0F] border border-white/5 p-6">
            <div className="flex items-center gap-0.5 mb-3">{[...Array(5)].map((_, j) => <Star key={j} className="w-4 h-4 text-amber-400 fill-amber-400" />)}</div>
            <p className="text-slate-200 text-sm leading-relaxed mb-5">"{t.q}"</p>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold" style={{ background: t.c }}>{t.n[0]}</div>
              <div>
                <p className="text-white text-sm font-600 flex items-center gap-1">{t.n} <BadgeCheck className="w-4 h-4 text-emerald-400" /></p>
                <p className="text-slate-500 text-xs">{t.s}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
      <p className="text-center text-slate-600 text-xs mt-6">*Representative student feedback.</p>
    </div>
  </section>
);

// ---------------- SEGMENTS ----------------
const SEGMENTS = [
  { t: "B.Tech Students", d: "Pinpoint which specialisation (AI, cloud, core) keeps you employable and pays best." },
  { t: "BCA / MCA Students", d: "Bridge the gap to real dev roles — exact stack, projects and certifications." },
  { t: "B.Com Students", d: "Finance, analytics, CA/CFA or business — find your highest-ROI direction." },
  { t: "MBA Aspirants", d: "Specialisation + role fit, salary trajectory and the skills that get you hired." },
  { t: "Fresh Graduates", d: "Stop guessing. Get a 90-day plan to land your first real offer." },
];
const Segments = () => (
  <section className="py-20 md:py-28">
    <div className="max-w-7xl mx-auto px-4 sm:px-6">
      <motion.div {...fade} className="text-center mb-12"><SectionLabel>Built for your path</SectionLabel><h2 className="font-head font-700 text-3xl sm:text-4xl text-white">Tailored to your degree</h2></motion.div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {SEGMENTS.map((s, i) => (
          <motion.div key={i} {...fade} transition={{ delay: (i % 3) * 0.07 }}
            className="rounded-2xl bg-gradient-to-br from-white/[0.04] to-transparent border border-white/10 p-6 hover:border-cyan-400/30 transition">
            <p className="font-head font-700 text-white text-lg mb-1.5">{s.t}</p>
            <p className="text-slate-400 text-sm leading-relaxed">{s.d}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

// ---------------- PRICING ----------------
const INCLUDES = ["One personalized career report", "Career match + roadmap", "Skill-gap analysis", "Salary forecast", "AI risk assessment", "Instant PDF delivery"];
const Pricing = ({ onStart }) => (
  <section id="pricing" className="py-20 md:py-28 relative">
    <Glow className="bg-purple-600 w-[400px] h-[400px] left-1/2 -translate-x-1/2 top-0" />
    <div className="max-w-md mx-auto px-4 sm:px-6 relative">
      <motion.div {...fade} className="rounded-3xl bg-[#0A0A0F] border border-purple-500/30 p-8 text-center shadow-[0_0_40px_rgba(124,58,237,0.18)]">
        <div className="inline-flex items-center gap-1.5 rounded-full bg-amber-400/10 border border-amber-400/30 px-3 py-1 text-amber-300 text-xs mb-5"><Zap className="w-3.5 h-3.5" /> Launch Price · Limited Time</div>
        <p className="font-head font-700 text-white text-xl mb-2">Student Launch Offer</p>
        <div className="flex items-end justify-center gap-2 mb-1">
          <span className="text-slate-500 line-through text-2xl">₹{PRICE.original}</span>
          <span className="font-head font-800 text-5xl bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-300">₹{PRICE.student}</span>
        </div>
        <p className="text-emerald-400 text-sm mb-6">You save ₹{PRICE.original - PRICE.student} ({Math.round((1 - PRICE.student / PRICE.original) * 100)}% off)</p>
        <ul className="text-left space-y-2.5 mb-7">
          {INCLUDES.map((f) => <li key={f} className="flex items-center gap-2.5 text-slate-300 text-sm"><Check className="w-4 h-4 text-emerald-400 shrink-0" /> {f}</li>)}
        </ul>
        <PrimaryBtn onClick={() => { track("cta_click", { location: "pricing" }); onStart(); }} testid="pricing-cta" className="w-full">Get My Career Blueprint Now <ArrowRight className="w-5 h-5" /></PrimaryBtn>
        <p className="text-slate-500 text-xs mt-4 flex items-center justify-center gap-1.5"><ShieldCheck className="w-4 h-4 text-emerald-400" /> 100% Secure · Powered by Razorpay · Zero hidden charges</p>
      </motion.div>
    </div>
  </section>
);

// ---------------- TRUST BADGES ----------------
const PAYMENTS = ["UPI", "Google Pay", "PhonePe", "Paytm", "Visa", "Mastercard"];
const Trust = () => (
  <section className="py-12">
    <div className="max-w-3xl mx-auto px-4 sm:px-6 text-center">
      <p className="text-slate-400 text-sm mb-5 flex items-center justify-center gap-2"><ShieldCheck className="w-4 h-4 text-emerald-400" /> 100% Secure Payments · Instant Report Delivery · Zero Hidden Charges</p>
      <div className="flex flex-wrap items-center justify-center gap-2.5">
        {PAYMENTS.map((p) => <span key={p} className="rounded-lg bg-white/5 border border-white/10 px-3.5 py-1.5 text-slate-300 text-xs font-medium">{p}</span>)}
      </div>
    </div>
  </section>
);

// ---------------- FAQ ----------------
const FAQS = [
  { q: "Is this report personalized?", a: "Yes. Every report is generated from your specific degree, skills, interests and goals — matched against 300+ careers, salary data and AI-risk. No two reports are the same." },
  { q: "How accurate is MapMyCareer?", a: "We combine an AI engine with curated, up-to-date industry data. It's a brutally honest strategic guide — not a guarantee — designed to give you clarity and a concrete plan." },
  { q: "Will I receive my report instantly?", a: "Yes. Your full report unlocks immediately after payment and is available as a downloadable PDF on the spot." },
  { q: "Can this help me choose a career?", a: "That's exactly what it's for — career match, the honest reality of your dream career, related backups, skill-gaps, salary outlook and a year-by-year roadmap." },
  { q: "Is my data secure?", a: "Yes. Payments are processed securely via Razorpay and we only use your inputs to generate your report." },
];
const FaqItem = ({ q, a }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="border-b border-white/10">
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between py-5 text-left" data-testid="faq-item">
        <span className="text-white font-600 text-sm sm:text-base pr-4">{q}</span>
        <ChevronDown className={`w-5 h-5 text-purple-400 shrink-0 transition-transform ${open ? "rotate-180" : ""}`} />
      </button>
      {open && <p className="text-slate-400 text-sm pb-5 leading-relaxed">{a}</p>}
    </div>
  );
};
const FAQ = () => (
  <section id="faq" className="py-20 md:py-28">
    <div className="max-w-2xl mx-auto px-4 sm:px-6">
      <motion.div {...fade} className="text-center mb-10"><SectionLabel>Questions</SectionLabel><h2 className="font-head font-700 text-3xl sm:text-4xl text-white">Frequently asked</h2></motion.div>
      <div>{FAQS.map((f) => <FaqItem key={f.q} {...f} />)}</div>
    </div>
  </section>
);

// ---------------- FOOTER ----------------
const Footer = () => (
  <footer className="border-t border-white/5 py-12">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 text-center">
      <p className="font-head font-800 text-lg text-white mb-2">MapMy<span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-300">Career</span></p>
      <p className="text-slate-500 text-sm max-w-md mx-auto mb-4">AI-powered career clarity for Indian students. Guidance, not guesswork.</p>
      <button onClick={() => window.open(whatsappLink(), "_blank")} className="text-emerald-400 text-sm hover:underline mb-4">Need help? Chat with us on WhatsApp</button>
      <p className="text-slate-600 text-xs">© 2026 MapMyCareer · Secure payments by Razorpay</p>
    </div>
  </footer>
);

// ---------------- PAGE ----------------
export const Landing = ({ onStart }) => (
  <div className="bg-[#05050A] text-white min-h-screen overflow-x-hidden" data-testid="landing-dark">
    <Nav onStart={onStart} />
    <main>
      <Hero onStart={onStart} />
      <Pain />
      <How />
      <ReportTease onStart={onStart} />
      <Features />
      <SocialProof />
      <Segments />
      <Pricing onStart={onStart} />
      <Trust />
      <FAQ />
    </main>
    <Footer />
  </div>
);
