import React from "react";
import { Reveal } from "../Reveal";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../ui/accordion";
import { FAQS } from "../../data/blueprint";

export const FAQ = () => (
  <section className="py-24 sm:py-32 grad-soft" data-testid="faq-section">
    <div className="max-w-3xl mx-auto px-6 lg:px-8">
      <Reveal>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-4 text-center">FAQ</p>
        <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight text-center text-slate-900 mb-12">
          Questions, <span className="text-gradient">answered.</span>
        </h2>
      </Reveal>
      <Reveal delay={0.1}>
        <Accordion type="single" collapsible className="space-y-3">
          {FAQS.map((f, i) => (
            <AccordionItem
              key={i}
              value={`item-${i}`}
              data-testid={`faq-item-${i}`}
              className="rounded-2xl glass-card px-5 overflow-hidden !border-b"
            >
              <AccordionTrigger className="font-head text-left text-lg text-slate-900 hover:no-underline hover:text-purple-600 py-5">
                {f.q}
              </AccordionTrigger>
              <AccordionContent className="text-slate-600 text-base leading-relaxed pb-5">
                {f.a}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </Reveal>
    </div>
  </section>
);
