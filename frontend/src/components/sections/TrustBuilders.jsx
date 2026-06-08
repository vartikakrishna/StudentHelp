import React from "react";
import * as Icons from "lucide-react";
import { TRUST_BUILDERS } from "../../data/blueprint";

export const TrustBuilders = () => (
  <section className="py-10 border-y border-slate-100 bg-white" data-testid="trust-builders">
    <div className="max-w-7xl mx-auto px-6 lg:px-8">
      <div className="flex flex-wrap items-center justify-center gap-x-8 gap-y-4">
        {TRUST_BUILDERS.map((t) => {
          const Icon = Icons[t.icon] || Icons.Check;
          const isBan = t.icon === "Ban";
          return (
            <div key={t.text} className="flex items-center gap-2.5">
              <Icon className={`w-5 h-5 ${isBan ? "text-rose-400" : "text-purple-500"}`} strokeWidth={1.8} />
              <span className={`text-sm font-medium ${isBan ? "text-slate-500" : "text-slate-800"}`}>{t.text}</span>
            </div>
          );
        })}
      </div>
    </div>
  </section>
);
