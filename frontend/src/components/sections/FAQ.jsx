import React from "react";
import { Reveal } from "../Reveal";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../ui/accordion";
import { FAQS } from "../../data/blueprint";

export const FAQ = () => (
  <section className="py-24 sm:py-32" data-testid="faq-section">
    <div className="max-w-3xl mx-auto px-6 lg:px-8">
      <Reveal>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-amber-500 mb-4 text-center">FAQ</p>
        <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight text-center mb-12">
          Questions, answered.
        </h2>
      </Reveal>
      <Reveal delay={0.1}>
        <Accordion type="single" collapsible className="space-y-3">
          {FAQS.map((f, i) => (
            <AccordionItem
              key={i}
              value={`item-${i}`}
              data-testid={`faq-item-${i}`}
              className="rounded-xl border border-white/8 bg-[#091226] px-5 overflow-hidden"
            >
              <AccordionTrigger className="font-head text-left text-lg hover:no-underline hover:text-gold py-5">
                {f.q}
              </AccordionTrigger>
              <AccordionContent className="text-slate-400 text-base leading-relaxed pb-5">
                {f.a}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </Reveal>
    </div>
  </section>
);
