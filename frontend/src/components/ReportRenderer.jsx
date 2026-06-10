import React from "react";
import * as Icons from "lucide-react";
import { motion } from "framer-motion";

const TONE = {
  indigo: { text: "text-indigo-600", bar: "bg-indigo-500", soft: "border-indigo-200 bg-indigo-50" },
  purple: { text: "text-purple-600", bar: "bg-purple-500", soft: "border-purple-200 bg-purple-50" },
  cyan: { text: "text-cyan-600", bar: "bg-cyan-500", soft: "border-cyan-200 bg-cyan-50" },
  emerald: { text: "text-emerald-600", bar: "bg-emerald-500", soft: "border-emerald-200 bg-emerald-50" },
  amber: { text: "text-amber-600", bar: "bg-amber-500", soft: "border-amber-200 bg-amber-50" },
  rose: { text: "text-rose-600", bar: "bg-rose-500", soft: "border-rose-200 bg-rose-50" },
  slate: { text: "text-slate-600", bar: "bg-slate-400", soft: "border-slate-200 bg-slate-50" },
};
const tone = (t) => TONE[t] || TONE.purple;
const BADGE = {
  indigo: "bg-indigo-50 text-indigo-700 border-indigo-200", purple: "bg-purple-50 text-purple-700 border-purple-200",
  cyan: "bg-cyan-50 text-cyan-700 border-cyan-200", emerald: "bg-emerald-50 text-emerald-700 border-emerald-200",
  amber: "bg-amber-50 text-amber-700 border-amber-200", rose: "bg-rose-50 text-rose-700 border-rose-200",
  slate: "bg-slate-50 text-slate-600 border-slate-200",
};

const Bar = ({ value, color = "bg-purple-500" }) => (
  <div className="w-full h-2.5 rounded-full bg-slate-100 overflow-hidden">
    <motion.div className={`h-full ${color}`} initial={{ width: 0 }} whileInView={{ width: `${Math.min(100, value)}%` }} viewport={{ once: true }} transition={{ duration: 1, ease: "easeOut" }} />
  </div>
);
const Badge = ({ children, t = "indigo" }) => (
  <span className={`inline-block text-[11px] font-mono px-2.5 py-1 rounded-full border ${BADGE[t] || BADGE.indigo}`}>{children}</span>
);

const SectionShell = ({ section, children }) => {
  const Icon = Icons[section.icon] || Icons.Sparkles;
  return (
    <div className="mb-10" data-testid={`report-section-${section.id}`}>
      <div className="flex items-center gap-2.5 mb-4">
        <div className="w-9 h-9 rounded-xl grad-primary flex items-center justify-center shrink-0"><Icon className="w-5 h-5 text-white" strokeWidth={1.8} /></div>
        <h2 className="font-head font-700 text-xl sm:text-2xl text-slate-900">{section.title}</h2>
      </div>
      {children}
    </div>
  );
};

const Intro = ({ s }) => <p className="text-slate-700 leading-relaxed text-base">{s.text}</p>;

const Callout = ({ s }) => (
  <div className={`rounded-3xl border p-6 ${tone(s.tone).soft}`}>
    {s.label && <p className={`font-head font-700 text-lg mb-1 ${tone(s.tone).text}`}>{s.label}</p>}
    <p className="text-slate-700 leading-relaxed">{s.text}</p>
  </div>
);

const ScoreCards = ({ s }) => (
  <div className={`grid gap-4 ${s.items.length >= 3 ? "sm:grid-cols-3" : "sm:grid-cols-2"}`}>
    {s.items.map((it, i) => (
      <div key={i} className="rounded-3xl glass-card p-6 text-center">
        <p className={`font-head font-800 text-4xl ${tone(it.tone).text}`}>{it.value != null ? `${it.value}${it.suffix || ""}` : "—"}</p>
        <p className="font-medium text-slate-900 mt-1">{it.label}</p>
        {it.caption && <p className="text-slate-500 text-xs mt-0.5">{it.caption}</p>}
      </div>
    ))}
  </div>
);

const Bars = ({ s }) => (
  <div className="rounded-3xl glass-card p-6 space-y-4">
    {s.items.map((it, i) => (
      <div key={i}>
        <div className="flex justify-between text-sm mb-1.5"><span className="text-slate-600">{it.label}</span><span className={`font-mono ${tone(it.tone).text}`}>{it.value}{it.suffix || "%"}</span></div>
        <Bar value={it.value} color={tone(it.tone).bar} />
        {it.caption && <p className="text-slate-400 text-xs mt-1">{it.caption}</p>}
      </div>
    ))}
  </div>
);

const Matches = ({ s }) => (
  <div className="grid md:grid-cols-2 gap-5">
    {s.items.map((m) => {
      const Icon = Icons[m.icon] || Icons.Sparkles;
      const riskTone = m.ai_risk <= 25 ? "emerald" : m.ai_risk <= 55 ? "amber" : "rose";
      return (
        <div key={m.key} className="rounded-3xl glass-card p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="flex items-center gap-2.5 font-head font-700 text-slate-900"><span className="w-8 h-8 rounded-lg grad-primary flex items-center justify-center"><Icon className="w-4 h-4 text-white" /></span>{m.title}</span>
            <span className="font-mono text-gradient font-700">{m.score}%</span>
          </div>
          <div className="flex flex-wrap gap-2 mb-3"><Badge t="indigo">{m.verdict}</Badge><Badge t={riskTone}>{m.ai_risk_label}</Badge><Badge t="cyan">~₹{m.salary_mid} LPA</Badge></div>
          {[["Market Demand", m.market_demand, "bg-indigo-500"], ["Salary Score", m.salary_score, "bg-cyan-500"], ["Competition", m.competition, "bg-rose-400"]].map(([l, v, c]) => (
            <div key={l} className="mb-2"><div className="flex justify-between text-xs mb-1"><span className="text-slate-500">{l}</span><span className="font-mono text-slate-700">{v}%</span></div><div className="h-2 rounded-full bg-slate-100 overflow-hidden"><div className={`h-full ${c}`} style={{ width: `${v}%` }} /></div></div>
          ))}
          <p className="text-slate-600 text-sm mt-3">{m.tagline}</p>
        </div>
      );
    })}
  </div>
);

const ListBlock = ({ s }) => (
  <div className="rounded-3xl glass-card p-6">
    {s.intro && <p className="text-slate-600 mb-3">{s.intro}</p>}
    <ul className="space-y-2">
      {s.items.map((it, i) => <li key={i} className="flex gap-2.5 text-slate-700"><Icons.Check className="w-5 h-5 text-cyan-500 shrink-0 mt-0.5" strokeWidth={2} />{it}</li>)}
    </ul>
  </div>
);

const Tags = ({ s }) => (
  <div className="rounded-3xl glass-card p-6">
    {s.intro && <p className="text-slate-600 mb-3">{s.intro}</p>}
    <div className="flex flex-wrap gap-2.5">
      {s.items.map((it, i) => <span key={i} className="px-3.5 py-2 rounded-full border border-purple-200 bg-purple-50 text-purple-700 text-sm font-medium">{it}</span>)}
    </div>
  </div>
);

const Cards = ({ s }) => (
  <div className="grid md:grid-cols-2 gap-4">
    {s.items.map((it, i) => (
      <div key={i} className="rounded-2xl glass-card p-5">
        <p className="font-head font-700 text-slate-900 mb-2">{it.title}</p>
        {it.badges && <div className="flex flex-wrap gap-2 mb-2">{it.badges.map((b, j) => <Badge key={j} t={b.tone}>{b.text}</Badge>)}</div>}
        {it.body && <p className="text-slate-600 text-sm">{it.body}</p>}
        {it.points && <ul className="mt-2 space-y-1">{it.points.map((p, j) => <li key={j} className="text-slate-600 text-sm flex gap-2"><Icons.ChevronRight className="w-4 h-4 text-purple-400 shrink-0 mt-0.5" />{p}</li>)}</ul>}
      </div>
    ))}
  </div>
);

const Roadmap = ({ s }) => (
  <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
    {s.items.map((ph, i) => (
      <div key={i} className="rounded-2xl glass-card p-5">
        <p className="font-mono text-purple-600 text-sm mb-1">{ph.phase}</p>
        {ph.focus && <p className="font-head font-700 text-slate-900 mb-3 text-sm">{ph.focus}</p>}
        <ul className="space-y-1.5">{ph.points.map((p, j) => <li key={j} className="text-slate-600 text-xs flex gap-2"><Icons.Check className="w-3.5 h-3.5 text-cyan-500 shrink-0 mt-0.5" />{p}</li>)}</ul>
        {ph.meta && <p className="mt-2 text-xs font-mono text-emerald-600">{ph.meta}</p>}
      </div>
    ))}
  </div>
);

const SalaryChart = ({ s }) => {
  const max = Math.max(...s.points.map((p) => p.value), 1);
  return (
    <div className="rounded-3xl glass-card p-6">
      <div className="flex items-end gap-4 h-48">
        {s.points.map((p, i) => (
          <div key={i} className="flex-1 flex flex-col items-center justify-end h-full">
            <span className="font-mono text-purple-600 text-sm mb-2">₹{p.value}</span>
            <motion.div className="w-full grad-primary rounded-t-xl" initial={{ height: 0 }} whileInView={{ height: `${(p.value / max) * 100}%` }} viewport={{ once: true }} transition={{ duration: 1 }} />
            <span className="text-xs text-slate-400 mt-2">{p.label}</span>
          </div>
        ))}
      </div>
      {s.note && <p className="text-slate-500 text-sm mt-4">{s.note}</p>}
    </div>
  );
};

const Letter = ({ s }) => (
  <div className="rounded-[2rem] grad-primary p-8 text-white glow-primary overflow-hidden relative">
    <Icons.Mail className="absolute -top-3 -right-3 w-28 h-28 text-white/10" />
    <p className="relative text-white/95 leading-relaxed whitespace-pre-line italic">{s.text}</p>
  </div>
);

const Recommendations = ({ s }) => (
  <div className="space-y-4">
    {s.items.map((m, i) => {
      const Icon = Icons[m.icon] || Icons.Sparkles;
      const riskTone = m.ai_risk <= 25 ? "emerald" : m.ai_risk <= 55 ? "amber" : "rose";
      return (
        <div key={m.key || i} className="rounded-3xl glass-card p-6" data-testid={`recommendation-${i}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="flex items-center gap-2.5 font-head font-700 text-slate-900 text-lg">
              <span className="w-8 h-8 rounded-lg grad-primary flex items-center justify-center shrink-0"><Icon className="w-4 h-4 text-white" /></span>{m.title}
            </span>
            <span className="font-mono text-gradient font-800 text-xl shrink-0">{m.score}%</span>
          </div>
          <div className="flex flex-wrap gap-2 mb-3">
            {m.growth && <Badge t="emerald">{m.growth} growth</Badge>}
            <Badge t={riskTone}>{m.ai_risk_label}</Badge>
            {m.salary_mid != null && <Badge t="cyan">~₹{m.salary_mid} LPA</Badge>}
          </div>
          {m.why && <p className="text-slate-700 text-sm mb-3"><span className="font-600 text-slate-900">Why it fits: </span>{m.why}</p>}
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <p className="text-xs font-700 text-emerald-600 mb-1.5 uppercase tracking-wide">Pros</p>
              <ul className="space-y-1">{(m.pros || []).map((p, j) => <li key={j} className="text-slate-600 text-sm flex gap-2"><Icons.Check className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />{p}</li>)}</ul>
            </div>
            <div>
              <p className="text-xs font-700 text-rose-600 mb-1.5 uppercase tracking-wide">Cons</p>
              <ul className="space-y-1">{(m.cons || []).map((p, j) => <li key={j} className="text-slate-600 text-sm flex gap-2"><Icons.X className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />{p}</li>)}</ul>
            </div>
          </div>
        </div>
      );
    })}
  </div>
);

const GROUP_ICON = { Skills: "Wrench", Tools: "Settings", Courses: "GraduationCap", Projects: "FolderGit2", Books: "BookOpen", YouTube: "Youtube" };
const Blueprint = ({ s }) => (
  <div className="space-y-5">
    {s.items.map((ph, i) => (
      <div key={i} className="rounded-3xl glass-card p-6" data-testid={`blueprint-phase-${i}`}>
        <div className="flex items-center gap-2 mb-1">
          <span className="font-mono text-purple-600 text-sm">{ph.phase}</span>
        </div>
        {ph.focus && <p className="font-head font-700 text-slate-900 mb-4">{ph.focus}</p>}
        <div className="grid sm:grid-cols-2 gap-x-6 gap-y-4">
          {(ph.groups || []).map((g, j) => {
            const GIcon = Icons[GROUP_ICON[g.label]] || Icons.ChevronRight;
            return (
              <div key={j}>
                <p className="text-xs font-700 text-indigo-600 mb-1.5 uppercase tracking-wide flex items-center gap-1.5"><GIcon className="w-3.5 h-3.5" />{g.label}</p>
                <ul className="space-y-1">{g.items.map((it, k) => <li key={k} className="text-slate-600 text-sm flex gap-2"><Icons.Dot className="w-4 h-4 text-purple-400 shrink-0 mt-0.5" />{it}</li>)}</ul>
              </div>
            );
          })}
        </div>
      </div>
    ))}
  </div>
);

const TableBlock = ({ s }) => (
  <div className="rounded-3xl glass-card p-6 overflow-x-auto" data-testid={`table-${s.id}`}>
    {s.intro && <p className="text-slate-600 mb-4">{s.intro}</p>}
    <table className="w-full text-sm border-collapse">
      <thead>
        <tr>{(s.headers || []).map((h, i) => <th key={i} className="text-left font-700 text-slate-900 pb-2 pr-4 border-b-2 border-slate-200">{h}</th>)}</tr>
      </thead>
      <tbody>
        {(s.rows || []).map((row, i) => (
          <tr key={i} className="border-b border-slate-100 last:border-0">
            {row.map((c, j) => <td key={j} className={`py-2.5 pr-4 align-top ${j === 0 ? "font-600 text-slate-900" : "text-slate-600"}`}>{c}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

const Timeline = ({ s }) => (
  <div className="rounded-3xl glass-card p-6" data-testid={`timeline-${s.id}`}>
    {s.intro && <p className="text-slate-600 mb-4">{s.intro}</p>}
    <div className="space-y-3">
      {s.items.map((it, i) => (
        <div key={i} className="flex gap-3 sm:gap-4">
          <span className="font-mono text-xs text-purple-600 font-700 whitespace-nowrap min-w-[64px] sm:min-w-[80px] pt-0.5">{it.label}</span>
          <div className="border-l-2 border-purple-100 pl-3 sm:pl-4 pb-1 flex-1">
            {it.title && <p className="font-600 text-slate-900 text-sm">{it.title}</p>}
            {it.text && <p className="text-slate-600 text-sm">{it.text}</p>}
            {it.points && <ul className="mt-1 space-y-1">{it.points.map((p, j) => <li key={j} className="text-slate-600 text-sm flex gap-2"><Icons.Check className="w-3.5 h-3.5 text-cyan-500 shrink-0 mt-0.5" />{p}</li>)}</ul>}
          </div>
        </div>
      ))}
    </div>
  </div>
);

const BLOCKS = { intro: Intro, callout: Callout, scorecards: ScoreCards, bars: Bars, matches: Matches, list: ListBlock, tags: Tags, cards: Cards, roadmap: Roadmap, salary_chart: SalaryChart, letter: Letter, recommendations: Recommendations, blueprint: Blueprint, table: TableBlock, timeline: Timeline };

export const ReportRenderer = ({ sections = [] }) => (
  <div data-testid="report-renderer">
    {sections.map((s) => {
      const Block = BLOCKS[s.type];
      if (!Block) return null;
      return <SectionShell key={s.id} section={s}><Block s={s} /></SectionShell>;
    })}
  </div>
);
