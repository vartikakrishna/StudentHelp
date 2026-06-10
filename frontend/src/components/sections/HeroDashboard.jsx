import React from "react";
import { PieChart, Pie, Cell, AreaChart, Area, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

const NAVY = "#0F172A", BLUE = "#2563EB", GREEN = "#10B981", TRACK = "#E2E8F0";

const salaryData = [
  { y: "Yr 1", v: 6 }, { y: "Yr 3", v: 11 }, { y: "Yr 5", v: 18 }, { y: "Yr 7", v: 26 }, { y: "Yr 10", v: 38 },
];
const skillData = [
  { name: "System Design", value: 78 }, { name: "AI / ML", value: 64 }, { name: "Cloud", value: 52 },
];

const Gauge = ({ value, color, label, suffix = "%" }) => {
  const data = [{ v: value }, { v: 100 - value }];
  return (
    <div className="relative flex flex-col items-center">
      <div className="relative w-[112px] h-[72px]">
        <ResponsiveContainer width="100%" height={112}>
          <PieChart>
            <Pie data={data} dataKey="v" startAngle={180} endAngle={0} innerRadius={36} outerRadius={52} cy={64} stroke="none" isAnimationActive={false}>
              <Cell fill={color} /><Cell fill={TRACK} />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute inset-x-0 bottom-1 text-center">
          <span className="font-head font-800 text-xl" style={{ color: NAVY }}>{value}{suffix}</span>
        </div>
      </div>
      <span className="text-[11px] text-[#64748B] -mt-1">{label}</span>
    </div>
  );
};

export const HeroDashboard = () => (
  <div className="rounded-2xl border border-[#E2E8F0] bg-white shadow-[0_20px_60px_-20px_rgba(15,23,42,0.18)] overflow-hidden">
    {/* window chrome */}
    <div className="flex items-center gap-1.5 px-4 py-3 border-b border-[#E2E8F0] bg-[#F8FAFC]">
      <span className="w-2.5 h-2.5 rounded-full bg-[#EF4444]/70" />
      <span className="w-2.5 h-2.5 rounded-full bg-[#F59E0B]/70" />
      <span className="w-2.5 h-2.5 rounded-full bg-[#10B981]/70" />
      <span className="ml-3 text-xs text-[#64748B] font-medium">Career Blueprint · Aryan S.</span>
    </div>

    <div className="p-5 space-y-4">
      {/* gauges */}
      <div className="grid grid-cols-2 gap-3">
        <div className="rounded-xl border border-[#E2E8F0] p-3 bg-white">
          <p className="text-xs text-[#64748B] mb-1">AI Automation Risk</p>
          <div className="flex items-center justify-between">
            <Gauge value={22} color={GREEN} label="Low risk" />
            <span className="text-[11px] font-semibold text-[#10B981] bg-[#10B981]/10 px-2 py-1 rounded-md">Future-proof</span>
          </div>
        </div>
        <div className="rounded-xl border border-[#E2E8F0] p-3 bg-white">
          <p className="text-xs text-[#64748B] mb-1">Career Fit Score</p>
          <div className="flex items-center justify-between">
            <Gauge value={86} color={BLUE} label="Strong match" />
            <span className="text-[11px] font-semibold text-[#2563EB] bg-[#2563EB]/10 px-2 py-1 rounded-md">Top 12%</span>
          </div>
        </div>
      </div>

      {/* salary forecast */}
      <div className="rounded-xl border border-[#E2E8F0] p-3 bg-white">
        <div className="flex items-center justify-between mb-1">
          <p className="text-xs text-[#64748B]">Salary Forecast</p>
          <p className="text-xs font-semibold text-[#0F172A]">₹6 → ₹38 LPA</p>
        </div>
        <div className="h-[88px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={salaryData} margin={{ top: 6, right: 4, left: -22, bottom: 0 }}>
              <defs>
                <linearGradient id="sal" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={BLUE} stopOpacity={0.28} />
                  <stop offset="100%" stopColor={BLUE} stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="y" tick={{ fontSize: 10, fill: "#94A3B8" }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 10, fill: "#94A3B8" }} axisLine={false} tickLine={false} width={34} />
              <Tooltip cursor={{ stroke: TRACK }} contentStyle={{ borderRadius: 10, border: "1px solid #E2E8F0", fontSize: 12 }} />
              <Area type="monotone" dataKey="v" stroke={BLUE} strokeWidth={2.5} fill="url(#sal)" isAnimationActive={true} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* skill gap */}
      <div className="rounded-xl border border-[#E2E8F0] p-3 bg-white">
        <p className="text-xs text-[#64748B] mb-1">Skill Gap Analysis</p>
        <div className="h-[92px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={skillData} layout="vertical" margin={{ top: 2, right: 8, left: 0, bottom: 0 }} barCategoryGap={10}>
              <XAxis type="number" domain={[0, 100]} hide />
              <YAxis type="category" dataKey="name" tick={{ fontSize: 10, fill: "#64748B" }} axisLine={false} tickLine={false} width={78} />
              <Bar dataKey="value" radius={[0, 6, 6, 0]} isAnimationActive={true}>
                {skillData.map((_, i) => <Cell key={i} fill={i === 0 ? BLUE : i === 1 ? "#6366F1" : "#10B981"} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  </div>
);
