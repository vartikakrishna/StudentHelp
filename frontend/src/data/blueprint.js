// Questionnaire + marketing content config

export const INTERESTS = [
  { key: "technology", label: "Technology & Coding", icon: "Cpu" },
  { key: "business", label: "Business & Strategy", icon: "Briefcase" },
  { key: "design", label: "Design & Creativity", icon: "Palette" },
  { key: "psychology", label: "Psychology & People", icon: "Brain" },
  { key: "teaching", label: "Teaching & Mentoring", icon: "GraduationCap" },
  { key: "healthcare", label: "Healthcare & Medicine", icon: "HeartPulse" },
  { key: "finance", label: "Finance & Investing", icon: "TrendingUp" },
  { key: "content_creation", label: "Content Creation", icon: "Video" },
  { key: "law", label: "Law & Justice", icon: "Scale" },
  { key: "leadership", label: "Leadership & Management", icon: "Crown" },
];

export const PERSONALITY = [
  {
    key: "mind",
    question: "How do you recharge your energy?",
    options: [
      { value: "introvert", label: "Introvert", desc: "Deep focus, quiet, alone" },
      { value: "extrovert", label: "Extrovert", desc: "People, energy, conversation" },
    ],
  },
  {
    key: "approach",
    question: "How do you solve problems?",
    options: [
      { value: "creative", label: "Creative", desc: "Imagination & new ideas" },
      { value: "analytical", label: "Analytical", desc: "Logic, data & structure" },
    ],
  },
  {
    key: "risk",
    question: "How do you make big decisions?",
    options: [
      { value: "risk_taker", label: "Risk Taker", desc: "Bold bets, high reward" },
      { value: "stable", label: "Stability Seeker", desc: "Security & certainty" },
    ],
  },
  {
    key: "role",
    question: "Where do you shine the most?",
    options: [
      { value: "leader", label: "Leader", desc: "Guiding teams & vision" },
      { value: "specialist", label: "Specialist", desc: "Mastering one craft" },
    ],
  },
];

export const GOAL_PRIORITIES = [
  "High Salary",
  "Remote Work",
  "Start a Business",
  "Government Job",
  "Work-Life Balance",
  "Global Career",
];

export const DREAM_INCOME = [
  { value: "10-20 LPA", label: "₹10–20 LPA" },
  { value: "20-50 LPA", label: "₹20–50 LPA" },
  { value: "50-100 LPA", label: "₹50 LPA – 1 Cr" },
  { value: "1 Cr+", label: "₹1 Crore+" },
];

export const CHALLENGES = [
  "I don't know what I'm good at",
  "Too many options confuse me",
  "Pressure from family",
  "Fear of choosing wrong",
  "Worried AI will replace me",
];

export const EDUCATION = ["Class 10", "Class 12", "Diploma", "Undergraduate", "Postgraduate"];
export const STREAMS = ["Science (PCM)", "Science (PCB)", "Commerce", "Arts / Humanities", "Vocational", "Undecided"];
export const GENDERS = ["Male", "Female", "Other", "Prefer not to say"];

export const CHAPTERS = [
  { n: 1, title: "Career DNA Analysis", icon: "Dna", span: "lg:col-span-8" },
  { n: 2, title: "Top 5 Career Matches", icon: "Target", span: "lg:col-span-4" },
  { n: 3, title: "Future Salary Projection", icon: "TrendingUp", span: "lg:col-span-4" },
  { n: 4, title: "AI Risk Analysis", icon: "ShieldAlert", span: "lg:col-span-4" },
  { n: 5, title: "Learning Roadmap", icon: "Map", span: "lg:col-span-4" },
  { n: 6, title: "Best Industries", icon: "Building2", span: "lg:col-span-4" },
  { n: 7, title: "Entrepreneurship Potential", icon: "Rocket", span: "lg:col-span-4" },
  { n: 8, title: "Hidden Strengths", icon: "Gem", span: "lg:col-span-4" },
  { n: 9, title: "Growth Obstacles", icon: "AlertTriangle", span: "lg:col-span-4" },
  { n: 10, title: "Future Self Letter", icon: "Mail", span: "lg:col-span-12" },
];

export const FAQS = [
  { q: "Will AI choose my career for me?", a: "No. The AI provides guidance and data-driven career matching insights. You always stay in control of the final decision." },
  { q: "How long does it take?", a: "Under 2 minutes to answer, and your blueprint is generated in seconds." },
  { q: "Is the report really personalized?", a: "Yes. Every score, salary projection and roadmap is calculated from your exact answers — not a generic template." },
  { q: "Can parents use it for their child?", a: "Absolutely. Many parents use it to guide their teenager toward the right stream and career." },
  { q: "What do I get for ₹199?", a: "A 12–15 page premium PDF Career Blueprint with 10 chapters, salary projections, AI-risk analysis and a personalised roadmap." },
];
