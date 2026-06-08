import React from "react";
import { Reveal } from "../Reveal";
import { Mail, Lock } from "lucide-react";
import { CTAButton } from "../CTAButton";

export const FutureSelf = ({ onStart }) => (
  <section className="py-24 sm:py-32 bg-white" data-testid="future-self-section">
    <div className="max-w-4xl mx-auto px-6 lg:px-8">
      <Reveal>
        <p className="font-mono text-xs tracking-[0.2em] uppercase text-purple-500 mb-4 text-center">Meet Your Future Self</p>
        <h2 className="font-head font-700 text-3xl sm:text-4xl lg:text-5xl tracking-tight text-center text-slate-900 mb-10">
          A letter from the <span className="text-gradient">you of 5 years from now.</span>
        </h2>
      </Reveal>

      <Reveal delay={0.1}>
        <div className="relative rounded-[2rem] grad-primary p-[1.5px] glow-primary">
          <div className="relative rounded-[1.9rem] bg-white p-8 sm:p-10 overflow-hidden">
            <div className="flex items-center gap-3 mb-5">
              <div className="w-11 h-11 rounded-2xl grad-primary flex items-center justify-center"><Mail className="w-5 h-5 text-white" /></div>
              <p className="font-head font-700 text-lg text-slate-900">Dear You,</p>
            </div>
            <p className="text-slate-700 leading-relaxed">
              Five years from now, you finally stopped guessing. You committed to the right path and gave it everything.
              It wasn&apos;t easy, but every week compounded. Today you earn more than you imagined, you&apos;re respected for what you build, and the fear of wasting years is gone…
            </p>
            <div className="relative mt-4">
              <p className="text-slate-700 leading-relaxed locked-blur">
                The turning point was the day you read your Career Blueprint and finally understood exactly where your strengths, the market and AI trends aligned. You stopped chasing
                what looked impressive and started building what actually fit. By year three you had…
              </p>
              <div className="absolute inset-0 flex flex-col items-center justify-center text-center"
                   style={{ background: "linear-gradient(to bottom, rgba(255,255,255,0.4), rgba(255,255,255,0.96))" }}>
                <div className="w-12 h-12 rounded-2xl grad-primary flex items-center justify-center mb-3 glow-primary"><Lock className="w-6 h-6 text-white" /></div>
                <p className="font-head font-700 text-slate-900">Your full letter is in your Blueprint</p>
                <div className="mt-4"><CTAButton testid="futureself-start-btn" onClick={onStart} size="sm">Read My Future Self Letter</CTAButton></div>
              </div>
            </div>
          </div>
        </div>
      </Reveal>
    </div>
  </section>
);
