import React, { useState } from "react";
import "@/App.css";
import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/sections/Hero";
import { TrustBuilders } from "@/components/sections/TrustBuilders";
import { Pain } from "@/components/sections/Pain";
import { HowItWorks } from "@/components/sections/HowItWorks";
import { UserTypesBand } from "@/components/sections/UserTypesBand";
import { PreviewShowcase } from "@/components/sections/PreviewShowcase";
import { Transformation } from "@/components/sections/Transformation";
import { RegretCalculator } from "@/components/sections/RegretCalculator";
import { WhatsInside } from "@/components/sections/WhatsInside";
import { FutureSelf } from "@/components/sections/FutureSelf";
import { Pricing } from "@/components/sections/Pricing";
import { FAQ } from "@/components/sections/FAQ";
import { Footer } from "@/components/sections/Footer";
import { Questionnaire } from "@/components/Questionnaire";
import { ResultPreview } from "@/components/ResultPreview";

function App() {
  const [view, setView] = useState("home"); // home | quiz | result
  const [result, setResult] = useState(null);

  const startQuiz = () => {
    window.scrollTo({ top: 0 });
    setView("quiz");
  };

  const onComplete = (data) => {
    setResult(data);
    setView("result");
    window.scrollTo({ top: 0 });
  };

  if (view === "quiz") {
    return <Questionnaire onClose={() => setView("home")} onComplete={onComplete} />;
  }

  if (view === "result" && result) {
    return <ResultPreview result={result} onBack={() => setView("home")} />;
  }

  return (
    <div className="App bg-white text-slate-900">
      <Navbar onStart={startQuiz} />
      <main>
        <Hero onStart={startQuiz} />
        <TrustBuilders />
        <Pain onStart={startQuiz} />
        <HowItWorks />
        <UserTypesBand onStart={startQuiz} />
        <PreviewShowcase onStart={startQuiz} />
        <Transformation />
        <RegretCalculator onStart={startQuiz} />
        <WhatsInside />
        <FutureSelf onStart={startQuiz} />
        <Pricing onStart={startQuiz} />
        <FAQ />
        <Footer onStart={startQuiz} />
      </main>
    </div>
  );
}

export default App;
