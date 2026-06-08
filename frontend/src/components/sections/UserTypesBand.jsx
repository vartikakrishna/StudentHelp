import React from "react";
import * as Icons from "lucide-react";
import { Reveal, Stagger, Item } from "../Reveal";
import { USER_TYPES } from "../../data/blueprint";

export const UserTypesBand = ({ onStart }) => (
  <section className="py-20 bg-white" data-testid="user-types-section">
    <div className="max-w-7xl mx-auto px-6 lg:px-8 text-center">
      <Reveal>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-4">Built For Every Stage</p>
        <h2 className="font-head font-700 text-3xl sm:text-4xl tracking-tight text-slate-900 mb-3">
          Whoever you are, the truth <span className="text-gradient">applies to you.</span>
        </h2>
        <p className="text-slate-500 max-w-2xl mx-auto mb-10">From confused students to laid-off professionals — honest, personalised intelligence for your exact situation.</p>
      </Reveal>
      <Stagger className="flex flex-wrap justify-center gap-3">
        {USER_TYPES.map((u) => {
          const Icon = Icons[u.icon] || Icons.User;
          return (
            <Item key={u.value}>
              <button onClick={onStart} data-testid={`usertype-chip-${u.value}`}
                className="group flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2.5 hover:border-purple-300 hover:-translate-y-0.5 transition-all soft-shadow">
                <Icon className="w-4 h-4 text-purple-500" strokeWidth={1.8} />
                <span className="text-sm font-medium text-slate-700 group-hover:text-slate-900">{u.label}</span>
              </button>
            </Item>
          );
        })}
      </Stagger>
    </div>
  </section>
);
