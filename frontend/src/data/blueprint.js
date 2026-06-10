// Questionnaire + marketing content config

export const USER_TYPES = [
  { value: "Student", label: "Student", icon: "GraduationCap" },
  { value: "Fresher", label: "Fresher", icon: "Sprout" },
  { value: "Working Professional", label: "Working Professional", icon: "Briefcase" },
  { value: "IT Employee", label: "IT Employee", icon: "Code" },
  { value: "Manager", label: "Manager", icon: "Users" },
  { value: "Laid Off Employee", label: "Laid Off Employee", icon: "UserMinus" },
  { value: "Career Switcher", label: "Career Switcher", icon: "Repeat" },
  { value: "Freelancer", label: "Freelancer", icon: "Laptop" },
  { value: "Business Owner", label: "Business Owner", icon: "Building2" },
];

export const PROFESSIONAL_TYPES = [
  "Working Professional", "IT Employee", "Manager", "Laid Off Employee",
  "Career Switcher", "Freelancer", "Business Owner",
];

export const COUNTRIES = ["India", "United States", "United Kingdom", "Canada", "UAE", "Australia", "Singapore", "Germany", "Other"];

export const EDUCATION_OPTIONS = [
  "Computer Science", "Information Technology", "Artificial Intelligence", "Machine Learning",
  "Data Science", "Cybersecurity", "Software Engineering", "Mechanical Engineering",
  "Civil Engineering", "Electronics", "Chemical Engineering", "Biotechnology", "MBBS", "BDS",
  "Nursing", "Pharmacy", "Psychology", "Law", "CA", "CS", "CMA", "Finance", "Economics",
  "Marketing", "HR", "MBA", "Architecture", "Interior Design", "Fashion Design", "Animation",
  "Film Making", "Journalism", "Mass Communication", "Teaching", "Hotel Management", "Aviation",
  "Agriculture", "Defense", "UPSC", "Government Services", "Police", "Sports", "Content Creation",
  "Influencer", "YouTuber", "Business", "Startup Founder", "Other",
];

export const EDUCATION_LEVELS = ["Class 10", "Class 12", "Diploma", "Undergraduate", "Postgraduate", "Doctorate"];

export const INTERESTS = [
  { key: "technology", label: "Technology", icon: "Cpu" },
  { key: "business", label: "Business", icon: "Briefcase" },
  { key: "finance", label: "Finance", icon: "TrendingUp" },
  { key: "sales", label: "Sales", icon: "Handshake" },
  { key: "marketing", label: "Marketing", icon: "Megaphone" },
  { key: "design", label: "Design", icon: "Palette" },
  { key: "writing", label: "Writing", icon: "PenTool" },
  { key: "teaching", label: "Teaching", icon: "GraduationCap" },
  { key: "research", label: "Research", icon: "Microscope" },
  { key: "psychology", label: "Psychology", icon: "Brain" },
  { key: "healthcare", label: "Healthcare", icon: "HeartPulse" },
  { key: "law", label: "Law", icon: "Scale" },
  { key: "content_creation", label: "Content Creation", icon: "Video" },
  { key: "entrepreneurship", label: "Entrepreneurship", icon: "Rocket" },
  { key: "leadership", label: "Leadership", icon: "Crown" },
  { key: "problem_solving", label: "Problem Solving", icon: "Puzzle" },
];

export const PERSONALITY_BINARY = [
  { key: "mind", question: "How do you recharge?", options: [
    { value: "introvert", label: "Introvert", desc: "Quiet, deep focus" },
    { value: "extrovert", label: "Extrovert", desc: "People & energy" }] },
  { key: "approach", question: "How do you solve problems?", options: [
    { value: "creative", label: "Creative", desc: "Ideas & imagination" },
    { value: "analytical", label: "Analytical", desc: "Logic & data" }] },
  { key: "risk", question: "How do you make big decisions?", options: [
    { value: "risk_taker", label: "Risk Taker", desc: "Bold bets" },
    { value: "stable", label: "Stability Seeker", desc: "Security first" }] },
  { key: "role", question: "Where do you shine?", options: [
    { value: "leader", label: "Leader", desc: "Guiding teams" },
    { value: "specialist", label: "Specialist", desc: "Mastering a craft" }] },
  { key: "work_style", question: "How do you work best?", options: [
    { value: "independent", label: "Independent", desc: "Solo & autonomous" },
    { value: "team", label: "Team Player", desc: "Collaborative" }] },
];

export const PERSONALITY_SLIDERS = [
  { key: "stress_tolerance", label: "Stress Tolerance" },
  { key: "work_life", label: "Work-Life Balance Importance" },
  { key: "communication", label: "Communication Confidence" },
  { key: "public_speaking", label: "Public Speaking Confidence" },
];

export const GOAL_PRIORITIES = [
  "High Salary", "Remote Work", "Entrepreneurship", "Government Job",
  "Leadership", "Foreign Opportunities", "Financial Freedom", "Work-Life Balance",
];

export const DREAM_INCOME = [
  { value: "10", label: "₹10 LPA" },
  { value: "20", label: "₹20 LPA" },
  { value: "35", label: "₹35 LPA" },
  { value: "50", label: "₹50 LPA" },
  { value: "100", label: "₹1 Cr+" },
];

export const CHALLENGES = [
  "I don't know what I'm good at",
  "Too many options confuse me",
  "Pressure from family",
  "Fear of choosing wrong",
  "Worried AI will replace me",
  "Recently laid off / job insecurity",
];

export const LAYOFF_REASONS = ["Cost cutting", "Restructuring", "Performance", "Company shutdown", "Role automated", "Other"];
export const REMOTE_PREFS = ["Remote", "Hybrid", "On-site", "No preference"];
export const GENDERS = ["Male", "Female", "Other", "Prefer not to say"];

export const PAIN_QUESTIONS = [
  "What if your current career choice is wrong?",
  "What if AI replaces your profession?",
  "What if you discover your true strengths too late?",
  "What if your dream job has little future demand?",
];

export const TRUST_BUILDERS = [
  { icon: "Ban", text: "No Astrology" },
  { icon: "Ban", text: "No Motivation Fluff" },
  { icon: "Ban", text: "No Generic Advice" },
  { icon: "Database", text: "Data-Driven Analysis" },
  { icon: "BrainCircuit", text: "AI + Market Trends + Career Intelligence" },
];

export const CHAPTERS = [
  { n: 1, title: "Career Reality Check", icon: "Gauge", span: "lg:col-span-8" },
  { n: 2, title: "Strengths & Weaknesses", icon: "Scale", span: "lg:col-span-4" },
  { n: 3, title: "Top Career Matches", icon: "Target", span: "lg:col-span-4" },
  { n: 4, title: "Careers To Avoid", icon: "ShieldX", span: "lg:col-span-4" },
  { n: 5, title: "Industry Analysis", icon: "Building2", span: "lg:col-span-4" },
  { n: 6, title: "AI Threat Assessment", icon: "Bot", span: "lg:col-span-6" },
  { n: 7, title: "Income Projection", icon: "TrendingUp", span: "lg:col-span-6" },
  { n: 8, title: "Entrepreneurship Potential", icon: "Rocket", span: "lg:col-span-4" },
  { n: 9, title: "Career Switch Opportunities", icon: "Repeat", span: "lg:col-span-4" },
  { n: 10, title: "Skill Gap Analysis", icon: "Puzzle", span: "lg:col-span-4" },
  { n: 11, title: "Learning Roadmap", icon: "Map", span: "lg:col-span-6" },
  { n: 12, title: "Resume & LinkedIn Strategy", icon: "FileText", span: "lg:col-span-6" },
  { n: 13, title: "Interview Readiness", icon: "MessageSquare", span: "lg:col-span-4" },
  { n: 14, title: "Layoff Recovery Plan", icon: "LifeBuoy", span: "lg:col-span-4" },
  { n: 15, title: "Future Industry Predictions", icon: "Telescope", span: "lg:col-span-4" },
  { n: 16, title: "Future Self Letter", icon: "Mail", span: "lg:col-span-12" },
];

export const FAQS = [
  { q: "Is this just another personality test?", a: "No. This is a brutally honest, data-driven career intelligence report — real scores for demand, salary, competition and AI risk, not vague motivation." },
  { q: "Will it tell me hard truths?", a: "Yes. We show careers to avoid, your weaknesses, and AI-disruption risk. We don't tell everyone they can become anything." },
  { q: "How long does it take?", a: "Under 2 minutes to answer, and your blueprint generates in seconds." },
  { q: "Does it work for working professionals and laid-off employees?", a: "Yes — there's a dedicated layoff survival engine, IT future report and career-switch engine for professionals." },
  { q: "What do I get for ₹199?", a: "A 12–15 page premium PDF with 16 chapters: reality check, top matches, careers to avoid, AI threat, salary projection, recovery roadmap and more." },
];

const STUDENT_FEATURES = [
  "Career Match Analysis",
  "Top 5 Career Recommendations",
  "Careers To Avoid",
  "Salary Potential Forecast",
  "AI Risk Analysis",
  "Skill Development Roadmap",
  "Learning Path",
  "Future Self Letter",
  "Industry Demand Forecast",
];

export const PLAN_CONFIG = {
  student: {
    key: "student",
    name: "Student Career Report",
    price: 199,
    original: 999,
    headline: "Don't Waste 4 Years Preparing For The Wrong Career.",
    subheadline: "Discover the path where your skills, interests and future opportunities align.",
    perfectFor: ["School Students", "College Students", "Fresh Graduates"],
    features: STUDENT_FEATURES,
    ctaText: "Unlock My Career Report",
    footnote: "Less than the cost of one movie night.",
  },
  professional: {
    key: "professional",
    name: "Professional Career Intelligence Report",
    price: 499,
    original: 2499,
    headline: "Is Your Career Future-Proof In The Age Of AI?",
    subheadline: "Get a brutally honest analysis of your career growth, salary potential, AI risk and next best move.",
    perfectFor: ["Working Professionals", "IT Employees", "Managers", "Career Switchers", "Freelancers", "Business Owners", "Laid-Off Employees"],
    features: [
      ...STUDENT_FEATURES,
      "Career Growth Analysis",
      "Promotion Readiness Score",
      "Salary Growth Forecast",
      "Industry Risk Assessment",
      "AI Disruption Analysis",
      "Layoff Risk Assessment",
      "Career Switching Opportunities",
      "Leadership Potential Analysis",
      "Personal Branding Strategy",
      "LinkedIn Optimization Guidance",
      "Income Diversification Plan",
      "Future Industry Forecast",
      "Career Recovery Roadmap",
      "30/90/180/365 Day Action Plan",
    ],
    ctaText: "Unlock My Professional Career Intelligence Report",
    footnote: "One career mistake can cost years of lost income.",
  },
};

export const COMPARISON = [
  { feature: "Career Match Analysis", student: true, pro: true },
  { feature: "Salary Forecast", student: true, pro: true },
  { feature: "AI Risk Analysis", student: true, pro: true },
  { feature: "Learning Roadmap", student: true, pro: true },
  { feature: "Career Switching Plan", student: false, pro: true },
  { feature: "Promotion Analysis", student: false, pro: true },
  { feature: "Layoff Risk Assessment", student: false, pro: true },
  { feature: "Leadership Potential", student: false, pro: true },
  { feature: "Income Growth Strategy", student: false, pro: true },
  { feature: "LinkedIn Strategy", student: false, pro: true },
  { feature: "Personal Branding Plan", student: false, pro: true },
  { feature: "Career Recovery Roadmap", student: false, pro: true },
];

export const UPSELLS = [
  { id: "resume", title: "Resume Optimization Report", price: 299, icon: "FileText" },
  { id: "linkedin", title: "LinkedIn Optimization Report", price: 299, icon: "Linkedin" },
  { id: "interview", title: "Interview Preparation Blueprint", price: 499, icon: "MessageSquare" },
  { id: "bundle", title: "Complete Career Transformation Bundle", price: 999, icon: "Sparkles", best: true },
];

export const ADDON_LABELS = {
  resume: "Resume Report",
  linkedin: "LinkedIn Report",
  interview: "Interview Blueprint",
};
