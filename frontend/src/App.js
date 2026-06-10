import React, { useState, useEffect } from "react";
import "@/App.css";
import { Landing } from "@/components/sections/Landing";
import { Questionnaire } from "@/components/Questionnaire";
import { ResultPreview } from "@/components/ResultPreview";
import { WhatsAppFab } from "@/components/WhatsAppFab";
import { StickyCta } from "@/components/StickyCta";
import { initAnalytics, track } from "@/lib/analytics";

function App() {
  const [view, setView] = useState("home"); // home | quiz | result
  const [result, setResult] = useState(null);
  const [degreeHint, setDegreeHint] = useState("");

  useEffect(() => { initAnalytics(); }, []);

  const startQuiz = (degree = "") => {
    if (typeof degree === "string" && degree) setDegreeHint(degree);
    track("begin_questionnaire", { degree: typeof degree === "string" ? degree : "" });
    window.scrollTo({ top: 0 });
    setView("quiz");
  };

  const onComplete = (data) => {
    setResult(data);
    track("generate_report", { user_type: data.user_type });
    setView("result");
    window.scrollTo({ top: 0 });
  };

  if (view === "quiz") {
    return <Questionnaire prefillDegree={degreeHint} onClose={() => setView("home")} onComplete={onComplete} />;
  }

  if (view === "result" && result) {
    return (
      <>
        <ResultPreview result={result} onBack={() => setView("home")} />
        <WhatsAppFab />
      </>
    );
  }

  return (
    <div className="App">
      <Landing onStart={startQuiz} />
      <StickyCta onStart={startQuiz} />
      <WhatsAppFab />
    </div>
  );
}

export default App;
