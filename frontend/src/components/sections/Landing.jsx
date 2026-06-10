import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  ArrowRight, Check, ShieldCheck, Bot, TrendingUp, Target, Wrench, Map, LineChart,
  Star, BadgeCheck, Lock, Zap, ChevronDown, GraduationCap, FileText,
} from "lucide-react";
import { PRICE, whatsappLink } from "../../lib/config";
import { track } from "../../lib/analytics";
import { HeroDashboard } from "./HeroDashboard";

const fade = { initial: { opacity: 0, y: 20 }, whileInView: { opacity: 1, y: 0 }, viewport: { once: true, margin: "-60px" }, transition: { duration: 0.5 } };
const container = "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8";
const scrollTo = (id) => document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });

const PrimaryBtn = ({ children, onClick, testid, className = "" }) => (
  <button onClick={onClick} data-testid={testid}
    className={`inline-flex items-center justify-center gap-2 h-12 px-6 rounded-xl bg-[#2563EB] text-white font-semibold hover:bg-blue-700 shadow-sm hover:shadow-md transition-all hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 ${className}`}>
    {children}
  </button>
);
const SecondaryBtn = ({ children, onClick, testid, className = "" }) => (
  <button onClick={onClick} data-testid={testid}
    className={`inline-flex items-center justify-center gap-2 h-12 px-6 rounded-xl bg-white text-[#0F172A] border border-[#E2E8F0] font-semibold hover:bg-[#F8FAFC] transition-all ${className}`}>
    {children}
  </button>
);
const Eyebrow = ({ children }) => <p className="text-sm font-semibold tracking-wide uppercase text-[#2563EB] mb-3">{children}</p>;
const H2 = ({ children }) => <h2 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight text-[#0F172A]">{children}</h2>;

// ---------------- NAV ----------------
const Nav = ({ onStart }) => (
  <header className="fixed top-0 inset-x-0 z-40 bg-white/90 backdrop-blur-md border-b border-[#E2E8F0]">
    <div className={`${container} h-16 flex items-center justify-between`}>
      <span className="font-head font-800 text-lg text-[#0F172A] tracking-tight flex items-center gap-2">
        <span className="w-7 h-7 rounded-lg bg-[#2563EB] flex items-center justify-center"><GraduationCap className="w-4 h-4 text-white" /></span>
        MapMy<span className="text-[#2563EB]">Career</span>
      </span>
      <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-[#334155]">
        <button onClick={() => scrollTo("features")} className="hover:text-[#2563EB] transition">Features</button>
        <button onClick={() => scrollTo("preview")} className="hover:text-[#2563EB] transition">Sample Report</button>
        <button onClick={() => scrollTo("pricing")} className="hover:text-[#2563EB] transition">Pricing</button>
        <button onClick={() => scrollTo("faq")} className="hover:text-[#2563EB] transition">FAQ</button>
      </nav>
      <PrimaryBtn onClick={() => onStart()} testid="nav-cta" className="h-10 px-5 text-sm">Get Started</PrimaryBtn>
    </div>
  </header>
);

// ---------------- HERO ----------------
const Hero = ({ onStart }) => (
  <section className="pt-28 pb-16 md:pt-36 md:pb-24 bg-white">
    <div className={`${container} grid lg:grid-cols-2 gap-12 lg:gap-16 items-center`}>
      <motion.div {...fade}>
        <div className="inline-flex items-center gap-2 rounded-full bg-[#2563EB]/8 border border-[#2563EB]/15 px-3.5 py-1.5 text-xs font-semibold text-[#2563EB] mb-6">
          <Bot className="w-3.5 h-3.5" /> AI-powered career intelligence for students
        </div>
        <h1 className="text-4xl sm:text-5xl lg:text-[3.4rem] leading-[1.08] font-extrabold tracking-tight text-[#0F172A]">
          Most Students Will Spend 4 Years Preparing For Careers That <span className="text-[#2563EB]">AI May Change.</span>
        </h1>
        <p className="text-base sm:text-lg text-[#334155] mt-6 leading-relaxed max-w-xl">
          MapMyCareer analyzes your education, skills, strengths and industry trends to create a personalized, future-ready career roadmap — with salary outlook, skill-gaps and an AI-risk assessment.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 mt-8">
          <PrimaryBtn onClick={() => { track("cta_click", { location: "hero" }); onStart(); }} testid="hero-cta">Generate My Free Career Blueprint <ArrowRight className="w-5 h-5" /></PrimaryBtn>
          <SecondaryBtn onClick={() => scrollTo("preview")} testid="hero-sample">View Sample Report</SecondaryBtn>
        </div>
        <div className="flex flex-wrap items-center gap-x-5 gap-y-2 mt-7 text-sm text-[#64748B]">
          {["Instant report", "Trusted by students across India", "Secure payments"].map((t) => (
            <span key={t} className="inline-flex items-center gap-1.5"><Check className="w-4 h-4 text-[#10B981]" /> {t}</span>
          ))}
        </div>
      </motion.div>
      <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.6 }}>
        <HeroDashboard />
      </motion.div>
    </div>
  </section>
);

// ---------------- TRUST BAND ----------------
const TRUST = ["AI-Powered Analysis", "Future Career Insights", "Personalized Roadmap", "Secure Payments"];
const PAYMENTS = ["UPI", "PhonePe", "Google Pay", "Paytm", "Visa", "Mastercard"];
const TrustBand = () => (
  <section className="border-y border-[#E2E8F0] bg-white py-8">
    <div className={`${container}`}>
      <div className="flex flex-wrap justify-center gap-x-8 gap-y-3 mb-6">
        {TRUST.map((t) => <span key={t} className="inline-flex items-center gap-2 text-sm font-medium text-[#334155]"><Check className="w-4 h-4 text-[#10B981]" /> {t}</span>)}
      </div>
      <div className="flex flex-wrap items-center justify-center gap-2.5">
        {PAYMENTS.map((p) => <span key={p} className="rounded-lg bg-[#F8FAFC] border border-[#E2E8F0] px-3.5 py-1.5 text-[#475569] text-xs font-semibold">{p}</span>)}
        <span className="inline-flex items-center gap-1.5 rounded-lg bg-[#10B981]/8 border border-[#10B981]/20 px-3.5 py-1.5 text-[#059669] text-xs font-semibold"><ShieldCheck className="w-4 h-4" /> Secured by Razorpay</span>
      </div>
    </div>
  </section>
);

// ---------------- HOW IT WORKS ----------------
const STEPS = [
  { n: "1", t: "Answer a few questions", d: "Your degree, skills, interests and goals — about 3 minutes." },
  { n: "2", t: "AI analyzes you vs the market", d: "Across 300+ careers, salary data, AI-risk and future demand." },
  { n: "3", t: "Get your career blueprint", d: "Career match, skill-gaps, salary forecast and a year-by-year roadmap." },
];
const How = () => (
  <section className="py-16 md:py-24 bg-[#F8FAFC]">
    <div className={container}>
      <div className="text-center mb-12"><Eyebrow>How it works</Eyebrow><H2>Career clarity in 3 simple steps</H2></div>
      <div className="grid md:grid-cols-3 gap-6">
        {STEPS.map((s, i) => (
          <motion.div key={i} {...fade} transition={{ delay: i * 0.08, duration: 0.5 }} className="rounded-2xl bg-white border border-[#E2E8F0] p-8 shadow-[0_4px_20px_-4px_rgba(15,23,42,0.05)]">
            <div className="w-10 h-10 rounded-xl bg-[#2563EB] text-white flex items-center justify-center font-bold mb-4">{s.n}</div>
            <p className="font-bold text-[#0F172A] text-lg mb-1.5">{s.t}</p>
            <p className="text-[#64748B] text-sm leading-relaxed">{s.d}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

// ---------------- FEATURES ----------------
const FEATURES = [
  { icon: Bot, t: "AI Automation Risk Score", d: "Know how vulnerable your path is to AI disruption before you commit years to it." },
  { icon: TrendingUp, t: "Salary Growth Forecast", d: "Projected earning potential over the next 5–10 years on your chosen path." },
  { icon: Target, t: "Career Match Analysis", d: "Careers aligned with your strengths, interests and the real job market." },
  { icon: Wrench, t: "Skill Gap Assessment", d: "The exact skills employers expect — and which ones you're missing." },
  { icon: Map, t: "Learning Roadmap", d: "What to learn next and in what order, mapped year by year." },
  { icon: LineChart, t: "Industry Outlook", d: "See where your industry is heading before everyone else does." },
];
const Features = () => (
  <section id="features" className="py-16 md:py-24 bg-white">
    <div className={container}>
      <div className="text-center mb-12"><Eyebrow>What you get</Eyebrow><H2>Everything in your career blueprint</H2></div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {FEATURES.map((f, i) => (
          <motion.div key={i} {...fade} transition={{ delay: (i % 3) * 0.07, duration: 0.5 }}
            className="rounded-2xl bg-white border border-[#E2E8F0] p-8 shadow-[0_4px_20px_-4px_rgba(15,23,42,0.05)] hover:shadow-[0_8px_30px_-4px_rgba(15,23,42,0.1)] hover:-translate-y-1 transition-all">
            <div className="w-12 h-12 rounded-xl bg-[#2563EB]/8 flex items-center justify-center mb-4"><f.icon className="w-6 h-6 text-[#2563EB]" /></div>
            <p className="font-bold text-[#0F172A] text-lg mb-1.5">{f.t}</p>
            <p className="text-[#64748B] text-sm leading-relaxed">{f.d}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

// ---------------- REPORT PREVIEW ----------------
const ReportTease = ({ onStart }) => (
  <section id="preview" className="py-16 md:py-24 bg-[#F8FAFC]">
    <div className="max-w-4xl mx-auto px-4 sm:px-6">
      <div className="text-center mb-10"><Eyebrow>Sample report</Eyebrow><H2>A premium, personalized career blueprint</H2></div>
      <motion.div {...fade} className="relative rounded-2xl bg-white border border-[#E2E8F0] overflow-hidden shadow-[0_20px_60px_-24px_rgba(15,23,42,0.18)]">
        <div className="p-6 sm:p-8 grid sm:grid-cols-3 gap-4">
          {[{ l: "AI Automation Risk", v: "Low", c: "text-[#10B981]" }, { l: "Career Fit Score", v: "86%", c: "text-[#2563EB]" }, { l: "Salary Potential", v: "₹18 LPA", c: "text-[#0F172A]" }].map((m, i) => (
            <div key={i} className="rounded-xl bg-[#F8FAFC] border border-[#E2E8F0] p-5 text-center">
              <p className={`font-extrabold text-3xl ${m.c}`}>{m.v}</p><p className="text-[#64748B] text-xs mt-1">{m.l}</p>
            </div>
          ))}
        </div>
        <div className="px-6 sm:px-8 pb-8 space-y-3">
          {["Skill Gap Analysis", "Future Job Outlook", "Recommended Career Paths", "Year 1-4 Learning Blueprint"].map((r) => (
            <div key={r} className="flex items-center justify-between rounded-xl bg-white border border-[#E2E8F0] px-4 py-3">
              <span className="text-[#334155] text-sm font-medium">{r}</span>
              <div className="w-28 h-2 rounded-full bg-[#E2E8F0] overflow-hidden"><div className="h-full bg-[#2563EB]" style={{ width: "72%" }} /></div>
            </div>
          ))}
        </div>
        <div className="absolute inset-x-0 bottom-0 h-2/3 bg-gradient-to-t from-white via-white/92 to-transparent backdrop-blur-[2px] flex flex-col items-center justify-end pb-8">
          <div className="w-12 h-12 rounded-xl bg-[#2563EB] flex items-center justify-center mb-3"><Lock className="w-6 h-6 text-white" /></div>
          <p className="font-bold text-[#0F172A] text-xl mb-4">Unlock Full Personalized Report</p>
          <PrimaryBtn onClick={() => onStart()} testid="tease-cta">Generate My Free Preview <ArrowRight className="w-5 h-5" /></PrimaryBtn>
        </div>
      </motion.div>
    </div>
  </section>
);

// ---------------- SEGMENTS ----------------
const SEGMENTS = [
  { t: "B.Tech", d: "Pinpoint the specialisation (AI, cloud, core) that keeps you employable and pays best." },
  { t: "BCA", d: "Bridge the gap to real dev roles — exact stack, projects and certifications." },
  { t: "B.Com", d: "Finance, analytics, CA/CFA or business — find your highest-ROI direction." },
  { t: "MBA", d: "Specialisation + role fit, salary trajectory and the skills that get you hired." },
  { t: "MCA", d: "Move from coursework to industry-ready engineering with a clear roadmap." },
  { t: "Fresh Graduates", d: "Stop guessing. Get a 90-day plan to land your first real offer." },
];
const Segments = () => (
  <section className="py-16 md:py-24 bg-white">
    <div className={container}>
      <div className="text-center mb-12"><Eyebrow>Built for your path</Eyebrow><H2>Tailored to your degree</H2></div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {SEGMENTS.map((s, i) => (
          <motion.div key={i} {...fade} transition={{ delay: (i % 3) * 0.07, duration: 0.5 }}
            className="rounded-2xl bg-[#F8FAFC] border border-[#E2E8F0] p-6 hover:border-[#2563EB]/30 transition">
            <div className="inline-flex items-center gap-2 rounded-lg bg-white border border-[#E2E8F0] px-3 py-1 text-sm font-bold text-[#2563EB] mb-3"><GraduationCap className="w-4 h-4" /> {s.t}</div>
            <p className="text-[#475569] text-sm leading-relaxed">{s.d}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

// ---------------- SOCIAL PROOF ----------------
const TESTIMONIALS = [
  { n: "Rahul Sharma", s: "Final-Year BCA · Pune", img: "https://images.unsplash.com/photo-1667655861998-46fe4c29a4cf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1MDZ8MHwxfHNlYXJjaHwxfHxpbmRpYW4lMjBzdHVkZW50JTIwcG9ydHJhaXR8ZW58MHx8fHwxNzgxMTA3NTcwfDA&ixlib=rb-4.1.0&q=85", q: "MapMyCareer showed me exactly which skills companies want. I completely changed my learning roadmap." },
  { n: "Sneha Menon", s: "B.Tech ECE · Chennai", img: "https://images.unsplash.com/photo-1604177091072-b7b677a077f6?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1MDZ8MHwxfHNlYXJjaHwzfHxpbmRpYW4lMjBzdHVkZW50JTIwcG9ydHJhaXR8ZW58MHx8fHwxNzgxMTA3NTcwfDA&ixlib=rb-4.1.0&q=85", q: "The report pinpointed where I was falling behind and what to focus on next. Genuinely useful." },
  { n: "Arjun Kumar", s: "B.Com · Bangalore", img: "https://images.pexels.com/photos/15237309/pexels-photo-15237309.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940", q: "I finally have clarity on which career path fits me — and a concrete plan to get there." },
];
const SocialProof = () => (
  <section className="py-16 md:py-24 bg-[#F8FAFC]">
    <div className={container}>
      <div className="text-center mb-12"><Eyebrow>Loved by students</Eyebrow><H2>What students are saying</H2></div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {TESTIMONIALS.map((t, i) => (
          <motion.div key={i} {...fade} transition={{ delay: i * 0.08, duration: 0.5 }} className="rounded-2xl bg-white border border-[#E2E8F0] p-6 shadow-[0_4px_20px_-4px_rgba(15,23,42,0.05)]">
            <div className="flex items-center gap-0.5 mb-3">{[...Array(5)].map((_, j) => <Star key={j} className="w-4 h-4 text-amber-400 fill-amber-400" />)}</div>
            <p className="text-[#334155] text-sm leading-relaxed mb-5">"{t.q}"</p>
            <div className="flex items-center gap-3">
              <img src={t.img} alt={t.n} loading="lazy" className="w-11 h-11 rounded-full object-cover border border-[#E2E8F0]" />
              <div>
                <p className="text-[#0F172A] text-sm font-bold flex items-center gap-1">{t.n} <BadgeCheck className="w-4 h-4 text-[#10B981]" /></p>
                <p className="text-[#64748B] text-xs">{t.s}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

// ---------------- PRICING ----------------
const INCLUDES = ["Personalized Career Roadmap", "Salary Forecast", "AI Risk Analysis", "Future Skills Report", "Skill-gap analysis", "Instant PDF delivery"];
const Pricing = ({ onStart }) => (
  <section id="pricing" className="py-16 md:py-24 bg-white">
    <div className="max-w-lg mx-auto px-4 sm:px-6">
      <div className="text-center mb-10"><Eyebrow>Pricing</Eyebrow><H2>One report. Total clarity.</H2></div>
      <motion.div {...fade} className="rounded-2xl bg-white border-2 border-[#2563EB]/20 p-8 text-center shadow-[0_20px_60px_-24px_rgba(37,99,235,0.25)]">
        <div className="inline-flex items-center gap-1.5 rounded-full bg-[#10B981]/10 border border-[#10B981]/20 px-3 py-1 text-[#059669] text-xs font-semibold mb-5"><Zap className="w-3.5 h-3.5" /> Student Launch Offer · Limited Time</div>
        <div className="flex items-end justify-center gap-2 mb-1">
          <span className="text-[#94A3B8] line-through text-2xl">₹{PRICE.original}</span>
          <span className="font-extrabold text-5xl text-[#0F172A]">₹{PRICE.student}</span>
        </div>
        <p className="text-[#059669] text-sm font-semibold mb-6">You save ₹{PRICE.original - PRICE.student} ({Math.round((1 - PRICE.student / PRICE.original) * 100)}% off)</p>
        <ul className="text-left space-y-2.5 mb-7">
          {INCLUDES.map((f) => <li key={f} className="flex items-center gap-2.5 text-[#334155] text-sm"><Check className="w-4 h-4 text-[#10B981] shrink-0" /> {f}</li>)}
        </ul>
        <PrimaryBtn onClick={() => { track("cta_click", { location: "pricing" }); onStart(); }} testid="pricing-cta" className="w-full">Get My Career Blueprint <ArrowRight className="w-5 h-5" /></PrimaryBtn>
        <p className="text-[#64748B] text-xs mt-4 flex items-center justify-center gap-1.5"><ShieldCheck className="w-4 h-4 text-[#10B981]" /> 100% Secure · Powered by Razorpay · Zero hidden charges</p>
      </motion.div>
    </div>
  </section>
);

// ---------------- FAQ ----------------
const FAQS = [
  { q: "How accurate is the report?", a: "We combine an AI engine with curated, up-to-date industry data and a 300+ career database. It's an honest strategic guide designed to give you real clarity and a concrete plan — not a guarantee." },
  { q: "Is my data private and secure?", a: "Yes. We only use your inputs to generate your report, and payments are processed securely through Razorpay." },
  { q: "Will I receive my report instantly?", a: "Yes — your full report unlocks immediately after payment and is available as a downloadable PDF on the spot." },
  { q: "Can this really help me choose a career?", a: "That's exactly what it's built for: career match, an honest reality-check on your dream career, related backups, skill-gaps, salary outlook and a year-by-year roadmap." },
  { q: "How do payments work?", a: "Secure UPI / cards / wallets via Razorpay. ₹199 launch price, no hidden charges, instant delivery." },
];
const FaqItem = ({ q, a }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="rounded-xl border border-[#E2E8F0] bg-white mb-3 overflow-hidden">
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between px-5 py-4 text-left" data-testid="faq-item">
        <span className="text-[#0F172A] font-semibold text-sm sm:text-base pr-4">{q}</span>
        <ChevronDown className={`w-5 h-5 text-[#2563EB] shrink-0 transition-transform ${open ? "rotate-180" : ""}`} />
      </button>
      {open && <p className="text-[#64748B] text-sm px-5 pb-4 leading-relaxed">{a}</p>}
    </div>
  );
};
const FAQ = () => (
  <section id="faq" className="py-16 md:py-24 bg-[#F8FAFC]">
    <div className="max-w-3xl mx-auto px-4 sm:px-6">
      <div className="text-center mb-10"><Eyebrow>Questions</Eyebrow><H2>Frequently asked</H2></div>
      {FAQS.map((f) => <FaqItem key={f.q} {...f} />)}
    </div>
  </section>
);

// ---------------- CTA + FOOTER ----------------
const FinalCta = ({ onStart }) => (
  <section className="py-16 md:py-20 bg-[#0F172A]">
    <div className={`${container} text-center`}>
      <h2 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight text-white">Build a career AI can't replace.</h2>
      <p className="text-slate-300 mt-3 max-w-xl mx-auto">Get your personalized, future-ready career blueprint in minutes.</p>
      <div className="mt-7 flex justify-center">
        <button onClick={() => onStart()} data-testid="final-cta" className="inline-flex items-center gap-2 h-12 px-7 rounded-xl bg-white text-[#0F172A] font-semibold hover:bg-slate-100 transition-all hover:-translate-y-0.5">
          Generate My Free Career Blueprint <ArrowRight className="w-5 h-5" />
        </button>
      </div>
    </div>
  </section>
);
const Footer = () => (
  <footer className="bg-[#0F172A] border-t border-white/10 py-10">
    <div className={`${container} text-center`}>
      <p className="font-head font-800 text-lg text-white mb-2">MapMy<span className="text-[#60A5FA]">Career</span></p>
      <p className="text-slate-400 text-sm max-w-md mx-auto mb-4">AI-powered career clarity for students. Guidance, not guesswork.</p>
      <button onClick={() => window.open(whatsappLink(), "_blank")} className="text-[#34D399] text-sm hover:underline mb-4">Need help? Chat with us on WhatsApp</button>
      <p className="text-slate-500 text-xs">© 2026 MapMyCareer · Secured by Razorpay</p>
    </div>
  </footer>
);

// ---------------- PAGE ----------------
export const Landing = ({ onStart }) => (
  <div className="bg-white text-[#0F172A] min-h-screen overflow-x-hidden" data-testid="landing">
    <Nav onStart={onStart} />
    <main>
      <Hero onStart={onStart} />
      <TrustBand />
      <How />
      <Features />
      <ReportTease onStart={onStart} />
      <Segments />
      <SocialProof />
      <Pricing onStart={onStart} />
      <FAQ />
      <FinalCta onStart={onStart} />
    </main>
    <Footer />
  </div>
);
