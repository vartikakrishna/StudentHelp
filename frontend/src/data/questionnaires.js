// Per-category questionnaire schemas + option lists + personality config.
// Each user type renders a completely different questionnaire (80% category, 20% personality).
import { EDUCATION_OPTIONS } from "./blueprint";

// ---- Category value (mirrors backend PROFILE_META) — shown BEFORE the questionnaire ----
export const PROFILE_META = {
  Student: { product: "Career Direction Report", icon: "GraduationCap", goal: "Career Discovery",
    tagline: "Find the right career & degree before you waste years on the wrong one.",
    value: ["Best-fit career paths", "Right degree & stream", "AI-proof career options", "Skills to start now", "10-year growth projection", "Career mistakes to avoid"] },
  "IT Employee": { product: "AI Survival & Growth Report", icon: "Code", goal: "AI Survival & Salary Growth",
    tagline: "Find out if AI will replace your role — and exactly how to stay ahead.",
    value: ["AI replacement risk score", "Future tech demand", "Your tech skill gaps", "Salary growth plan", "Transition opportunities", "Best emerging technologies"] },
  "Working Professional": { product: "Career Growth Report", icon: "Briefcase", goal: "Promotion & Salary Growth",
    tagline: "Get a brutally honest read on your promotion, salary and leadership trajectory.",
    value: ["Promotion readiness score", "Career growth analysis", "Salary forecast", "Leadership potential", "Industry outlook", "90/180/365 growth roadmap"] },
  Fresher: { product: "First-Job Readiness Report", icon: "Sprout", goal: "Landing Your First Job",
    tagline: "Know exactly how job-ready you are and what to fix first.",
    value: ["Job readiness score", "Skill gaps", "Resume & interview plan", "90-day action plan"] },
  "Career Switcher": { product: "Career Transition Blueprint", icon: "Repeat", goal: "Switching Careers",
    tagline: "See if your switch is realistic — and the fastest path to make it.",
    value: ["Switch feasibility", "Transferable skills", "Transition timeline", "Salary impact"] },
  "Laid Off Employee": { product: "Career Recovery Blueprint", icon: "LifeBuoy", goal: "Bouncing Back",
    tagline: "Your fastest, clearest path back to income after a layoff.",
    value: ["Recovery score", "Reemployment probability", "Emergency income options", "90-day recovery plan"] },
  Manager: { product: "Leadership Growth Report", icon: "Users", goal: "Leadership Growth",
    tagline: "Find your path from manager to executive.",
    value: ["Executive potential", "Leadership score", "Promotion roadmap", "Personal brand"] },
  Freelancer: { product: "Freelance Income Report", icon: "Laptop", goal: "Income Growth",
    tagline: "Scale your freelance income with a real growth system.",
    value: ["Income growth potential", "Client acquisition", "Brand building", "Service expansion"] },
  "Business Owner": { product: "Business Growth Intelligence Report", icon: "Building2", goal: "Business Growth",
    tagline: "A brutally honest read on your business health and growth levers.",
    value: ["Business health score", "Growth potential", "Marketing opportunities", "Scale plan"] },
};

// ---- Option lists ----
const SUBJECTS = ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science", "Economics", "Business Studies", "Accountancy", "English / Languages", "History / Civics", "Geography", "Psychology", "Art / Design", "Physical Education / Sports", "Political Science", "Commerce"];
const CAREER_INTERESTS = ["Software / IT", "Engineering", "Medicine / Healthcare", "Business / Management", "Finance / Banking", "Design / Creative", "Law", "Marketing / Media", "Teaching / Research", "Government / Civil Services", "Entrepreneurship / Startup", "Content / Influencer", "Psychology / Counselling", "Sales / Business Dev"];
const EXAMS = ["JEE", "NEET", "CUET", "CLAT", "CA Foundation", "GATE", "CAT (later)", "UPSC (later)", "Board Exams only", "None yet"];
const CLASSES = ["Class 9", "Class 10", "Class 11", "Class 12", "Diploma", "1st Year UG", "2nd Year UG", "3rd Year UG", "Final Year UG", "Postgraduate"];
const MARKS = ["Below 50%", "50-60%", "60-75%", "75-85%", "85-95%", "95%+"];
const STUDY_HABITS = ["Very consistent", "Consistent", "On & off", "Last-minute", "Struggling"];
const LEARNING_STYLE = ["Visual", "Listening", "Reading / Writing", "Hands-on / Practical"];

const DEVELOPER_TYPES = ["Frontend Developer", "Backend Developer", "Full Stack Developer", "Mobile Developer", "DevOps / Platform Engineer", "Data Engineer", "ML / AI Engineer", "Security Engineer", "Embedded Engineer", "QA / Test Engineer", "Support Engineer", "Other"];
const LEVELS = ["None", "Beginner", "Intermediate", "Advanced", "Expert"];
const LANGUAGES = ["Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "Go", "Rust", "PHP", "Ruby", "Kotlin", "Swift", "SQL"];
const TECH_STACK = ["React", "Angular", "Vue", "Node.js", "Django", "Spring", ".NET", "AWS", "GCP", "Azure", "Docker", "Kubernetes", "React Native", "Flutter", "TensorFlow", "PyTorch", "Kafka", "PostgreSQL", "MongoDB"];
const OPEN_SOURCE = ["Yes", "Some", "No"];

const INDUSTRIES = ["IT / Software", "Finance / BFSI", "Healthcare", "Manufacturing", "Retail / E-commerce", "Education", "Consulting", "Marketing / Media", "Government / Public", "Telecom", "Real Estate", "Other"];
const PROMO_HISTORY = ["Never promoted", "1 promotion", "2-3 promotions", "Frequently promoted"];
const TEAM_SIZE = ["Just me / IC", "2-5", "6-15", "16-50", "50+"];
const LEAD_RESP = ["None", "Lead a small team", "Manage a team", "Manage managers / dept"];

// Fresher
const GEN_SKILLS = ["Communication", "Problem solving / DSA", "Excel / Sheets", "SQL", "Python", "Git", "Data analysis", "Design", "Writing", "Marketing", "Public speaking", "Domain fundamentals"];
const COUNT_0_3 = ["None", "1", "2", "3+"];
const COUNT_PROJ = ["None", "1-2", "3-5", "5+"];
const RESUME_OPTS = ["Yes, polished", "In progress", "Not yet"];
const YESNO = ["Yes", "No"];
const JOBPREF = ["Product / Startups", "Service / IT", "Core / Domain", "Government / PSU", "Research / Higher studies", "Open to anything"];
// Switcher
const LEARN_TIME = ["<5 hrs/week", "5-10 hrs/week", "10-20 hrs/week", "20+ hrs/week"];
const RUNWAY = ["No savings", "1-3 months", "3-6 months", "6-12 months", "12+ months"];
const SWITCH_REASON = ["Better pay", "More passion / meaning", "Industry decline", "Burnout", "Growth ceiling", "Other"];
// Laid off
const SAVINGS = ["No savings", "<1 month", "1-3 months", "3-6 months", "6-12 months", "12+ months"];
const RELOCATE = ["Yes", "Maybe", "No"];
const LAYOFF_REASON = ["Company downsizing", "Restructuring", "Performance", "Startup shutdown", "Role eliminated", "Other"];
// Manager
const BUDGET = ["None", "Small (<₹50L)", "Mid (₹50L-5Cr)", "Large (₹5Cr+)"];
const HIRING = ["None", "Helped hire", "Hired independently", "Built teams"];
const SCALE3 = ["Low", "Medium", "High"];
// Freelancer
const FREELANCE_SERVICES = ["Design", "Development", "Writing / Content", "Marketing", "Video / Editing", "Consulting", "Photography", "Other"];
const CLIENTS_OPTS = ["0-1", "2-4", "5-10", "10+"];
const PRICING = ["Budget / low", "Mid-market", "Premium"];
const PORTFOLIO = ["Weak / none", "Okay", "Strong", "Outstanding"];
const FREELANCE_CHANNELS = ["Referrals system", "LinkedIn content", "Cold outreach", "Niche communities", "SEO / inbound", "Marketplaces (Upwork etc.)", "Email list"];
// Business
const BIZ_TYPE = ["Services", "Retail / E-commerce", "SaaS / Tech", "Manufacturing", "Food & Beverage", "Agency", "Consulting", "Other"];
const EMP_OPTS = ["Just me", "2-5", "6-20", "21-50", "50+"];
const MARGIN = ["Loss-making", "Break-even", "Low (<10%)", "Healthy (10-25%)", "Strong (25%+)"];
const ACQ = ["Word of mouth only", "1 main channel", "Few channels", "Diversified & systematic"];
const BIZ_CHALLENGE = ["Getting customers", "Cash flow / margins", "Hiring & team", "Scaling operations", "Marketing", "Retention", "Founder is the bottleneck"];
const BIZ_CHANNELS = ["Referral programme", "Paid ads", "SEO / content", "Email & retention", "Partnerships", "Social / community", "Sales team / outbound"];

// ---- Personality (8 high-value traits, used as 20% scoring modifier) ----
export const PERSONALITY_BINARY = [
  { key: "mind", question: "How do you recharge?", options: [{ value: "introvert", label: "Introvert", desc: "Quiet, deep focus" }, { value: "extrovert", label: "Extrovert", desc: "People & energy" }] },
  { key: "approach", question: "How do you solve problems?", options: [{ value: "analytical", label: "Analytical", desc: "Logic & data" }, { value: "creative", label: "Creative", desc: "Ideas & imagination" }] },
  { key: "risk", question: "How do you make big decisions?", options: [{ value: "risk_taker", label: "Risk Taker", desc: "Bold bets" }, { value: "stable", label: "Stability Seeker", desc: "Security first" }] },
  { key: "work_style", question: "You do your best work…", options: [{ value: "team", label: "In a Team", desc: "Collaborative" }, { value: "independent", label: "Independently", desc: "Solo & autonomous" }] },
  { key: "structure", question: "Your ideal workflow?", options: [{ value: "structured", label: "Structured", desc: "Plans & process" }, { value: "flexible", label: "Flexible", desc: "Adapt & improvise" }] },
];
export const PERSONALITY_SLIDERS = [
  { key: "leadership_interest", label: "Leadership Interest" },
  { key: "communication", label: "Communication Confidence" },
  { key: "stress_tolerance", label: "Stress Tolerance" },
];
export const PERSONALITY_KEYS = ["mind", "approach", "risk", "work_style", "structure"];

// ---- Per-type questionnaires ----
const STUDENT_STEPS = [
  { id: "academics", title: "Your academics", subtitle: "What you study shapes your honest match scores.", fields: [
    { key: "current_class", label: "Current Class / Level", type: "select", options: CLASSES, required: true, half: true },
    { key: "stream", label: "Degree / Stream", type: "select", options: EDUCATION_OPTIONS, half: true },
    { key: "marks", label: "Marks / Percentage", type: "select", options: MARKS, half: true },
    { key: "favorite_subjects", label: "Favorite Subjects", type: "multiselect", options: SUBJECTS, required: true },
    { key: "least_favorite_subjects", label: "Least Favorite Subjects", type: "multiselect", options: SUBJECTS },
    { key: "exams", label: "Competitive Exams Preparing For", type: "multiselect", options: EXAMS } ] },
  { id: "aspirations", title: "Your aspirations", subtitle: "Be honest — this is how we cut through the noise.", fields: [
    { key: "career_interests", label: "Career Interests", type: "multiselect", options: CAREER_INTERESTS, required: true },
    { key: "dream_career", label: "Your Dream Career", type: "text", placeholder: "e.g. Game Developer", half: true },
    { key: "parents_preferred", label: "Parents' Preferred Career", type: "text", placeholder: "e.g. Doctor", half: true },
    { key: "study_habits", label: "Study Habits", type: "select", options: STUDY_HABITS, half: true },
    { key: "learning_style", label: "Learning Style", type: "select", options: LEARNING_STYLE, half: true } ] },
];

const IT_STEPS = [
  { id: "profile", title: "Your tech profile", subtitle: "The basics of your engineering role.", fields: [
    { key: "current_role", label: "Current Role", type: "text", placeholder: "e.g. Frontend Engineer", half: true },
    { key: "developer_type", label: "Developer Type", type: "select", options: DEVELOPER_TYPES, required: true, half: true },
    { key: "years_experience", label: "Years of Experience", type: "number", placeholder: "e.g. 6", half: true },
    { key: "certifications", label: "Certifications", type: "text", placeholder: "e.g. AWS SAA", half: true },
    { key: "languages", label: "Programming Languages", type: "multiselect", options: LANGUAGES },
    { key: "tech_stack", label: "Tech Stack / Frameworks", type: "multiselect", options: TECH_STACK } ] },
  { id: "depth", title: "Your skill depth", subtitle: "Be brutally honest — this drives your AI-risk score.", fields: [
    { key: "cloud_knowledge", label: "Cloud Knowledge", type: "select", options: LEVELS, required: true, half: true },
    { key: "ai_knowledge", label: "AI / ML Knowledge", type: "select", options: LEVELS, required: true, half: true },
    { key: "system_design", label: "System Design Knowledge", type: "select", options: LEVELS, required: true, half: true },
    { key: "open_source", label: "Open Source Contributions", type: "select", options: OPEN_SOURCE, half: true } ] },
];

const PRO_STEPS = [
  { id: "role", title: "Your current role", subtitle: "Where you are today.", fields: [
    { key: "current_role", label: "Current Role / Title", type: "text", placeholder: "e.g. Marketing Manager", half: true },
    { key: "industry", label: "Industry", type: "select", options: INDUSTRIES, required: true, half: true },
    { key: "years_experience", label: "Years of Experience", type: "number", placeholder: "e.g. 8", half: true },
    { key: "current_salary", label: "Current Salary (₹ LPA)", type: "number", placeholder: "e.g. 14", half: true },
    { key: "team_size", label: "Team Size", type: "select", options: TEAM_SIZE, half: true },
    { key: "leadership_responsibilities", label: "Leadership Responsibilities", type: "select", options: LEAD_RESP, half: true } ] },
  { id: "growth", title: "Your growth goals", subtitle: "Where you want to be.", fields: [
    { key: "promotion_history", label: "Promotion History", type: "select", options: PROMO_HISTORY, half: true },
    { key: "desired_salary", label: "Desired Salary (₹ LPA)", type: "number", placeholder: "e.g. 28", half: true },
    { key: "desired_position", label: "Desired Position", type: "text", placeholder: "e.g. Head of Marketing", half: true },
    { key: "job_satisfaction", label: "Current Job Satisfaction", type: "slider" } ] },
];

export const QUESTIONNAIRES = {
  Student: STUDENT_STEPS,
  Fresher: [
    { id: "education", title: "Your education", subtitle: "Where you're starting from.", fields: [
      { key: "degree", label: "Degree", type: "select", options: EDUCATION_OPTIONS, half: true },
      { key: "graduation_year", label: "Graduation Year", type: "number", placeholder: "e.g. 2025", half: true },
      { key: "internships", label: "Internships Done", type: "select", options: COUNT_0_3, required: true, half: true },
      { key: "projects", label: "Projects Built", type: "select", options: COUNT_PROJ, required: true, half: true },
      { key: "certifications", label: "Certifications", type: "text", placeholder: "e.g. Google Data Analytics", half: true },
      { key: "skills", label: "Your Skills", type: "multiselect", options: GEN_SKILLS, required: true } ] },
    { id: "jobreadiness", title: "Your job search", subtitle: "Be honest — this drives your employability score.", fields: [
      { key: "resume_ready", label: "Resume Prepared?", type: "select", options: RESUME_OPTS, required: true, half: true },
      { key: "linkedin", label: "LinkedIn Profile?", type: "select", options: YESNO, half: true },
      { key: "expected_salary", label: "Expected Salary (₹ LPA)", type: "number", placeholder: "e.g. 6", half: true },
      { key: "job_preference", label: "Job Preference", type: "select", options: JOBPREF, half: true } ] },
  ],
  "IT Employee": IT_STEPS,
  "Working Professional": PRO_STEPS,
  "Career Switcher": [
    { id: "switch", title: "Your transition", subtitle: "From where, to where, and why.", fields: [
      { key: "current_profession", label: "Current Profession", type: "text", placeholder: "e.g. Mechanical Engineer", required: true, half: true },
      { key: "target_profession", label: "Target Profession", type: "text", placeholder: "e.g. Data Analyst", required: true, half: true },
      { key: "reason_for_switch", label: "Reason For Switch", type: "select", options: SWITCH_REASON, half: true },
      { key: "salary_expectation", label: "Salary Expectation (₹ LPA)", type: "number", placeholder: "e.g. 12", half: true },
      { key: "transferable_skills", label: "Transferable Skills", type: "multiselect", options: GEN_SKILLS } ] },
    { id: "capacity", title: "Your capacity to switch", subtitle: "How much you can invest in the move.", fields: [
      { key: "learning_time", label: "Available Learning Time", type: "select", options: LEARN_TIME, required: true, half: true },
      { key: "financial_situation", label: "Financial Runway", type: "select", options: RUNWAY, required: true, half: true } ] },
  ],
  "Laid Off Employee": [
    { id: "background", title: "Your background", subtitle: "Where you were before the layoff.", fields: [
      { key: "previous_role", label: "Previous Role", type: "text", placeholder: "e.g. Sales Manager", half: true },
      { key: "industry", label: "Industry", type: "select", options: INDUSTRIES, half: true },
      { key: "reason_for_layoff", label: "Reason For Layoff", type: "select", options: LAYOFF_REASON, half: true },
      { key: "previous_salary", label: "Previous Salary (₹ LPA)", type: "number", placeholder: "e.g. 18", half: true },
      { key: "years_experience", label: "Years of Experience", type: "number", placeholder: "e.g. 7", half: true },
      { key: "skills", label: "Your Skills", type: "multiselect", options: GEN_SKILLS, required: true } ] },
    { id: "recovery", title: "Your recovery situation", subtitle: "This shapes your fastest path back.", fields: [
      { key: "savings_runway", label: "Savings Runway", type: "select", options: SAVINGS, required: true, half: true },
      { key: "desired_industry", label: "Desired Industry", type: "select", options: INDUSTRIES, half: true },
      { key: "relocation", label: "Willing To Relocate?", type: "select", options: RELOCATE, half: true } ] },
  ],
  Manager: [
    { id: "scope", title: "Your management scope", subtitle: "The size of what you run today.", fields: [
      { key: "department", label: "Department", type: "text", placeholder: "e.g. Sales / Engineering", half: true },
      { key: "team_size", label: "Team Size", type: "select", options: TEAM_SIZE, required: true, half: true },
      { key: "budget_responsibility", label: "Budget Responsibility", type: "select", options: BUDGET, half: true },
      { key: "hiring_experience", label: "Hiring Experience", type: "select", options: HIRING, half: true } ] },
    { id: "leadership", title: "Your leadership depth", subtitle: "Rate your real exposure.", fields: [
      { key: "conflict_management", label: "Conflict Management", type: "select", options: SCALE3, required: true, half: true },
      { key: "strategic_planning", label: "Strategic Planning", type: "select", options: SCALE3, required: true, half: true },
      { key: "revenue_responsibility", label: "Revenue / P&L Responsibility", type: "select", options: SCALE3, half: true } ] },
  ],
  Freelancer: [
    { id: "business", title: "Your freelance business", subtitle: "What you sell and to whom.", fields: [
      { key: "services", label: "Services Offered", type: "multiselect", options: FREELANCE_SERVICES, required: true },
      { key: "niche", label: "Your Niche", type: "text", placeholder: "e.g. SaaS landing pages", half: true },
      { key: "monthly_income", label: "Monthly Income (₹)", type: "number", placeholder: "e.g. 80000", half: true },
      { key: "clients", label: "Active Clients", type: "select", options: CLIENTS_OPTS, half: true },
      { key: "pricing", label: "Pricing Position", type: "select", options: PRICING, required: true, half: true } ] },
    { id: "growth", title: "Your growth engine", subtitle: "How clients find you today.", fields: [
      { key: "marketing_channels", label: "Marketing Channels You Use", type: "multiselect", options: FREELANCE_CHANNELS },
      { key: "portfolio_quality", label: "Portfolio Quality", type: "select", options: PORTFOLIO, required: true, half: true } ] },
  ],
  "Business Owner": [
    { id: "business", title: "Your business", subtitle: "The shape of what you run.", fields: [
      { key: "business_type", label: "Business Type", type: "select", options: BIZ_TYPE, required: true, half: true },
      { key: "revenue", label: "Monthly Revenue (₹)", type: "number", placeholder: "e.g. 500000", half: true },
      { key: "employees", label: "Employees", type: "select", options: EMP_OPTS, half: true },
      { key: "profit_margin", label: "Profit Margin", type: "select", options: MARGIN, required: true, half: true } ] },
    { id: "growth", title: "Your growth picture", subtitle: "Where the friction and upside are.", fields: [
      { key: "customer_acquisition", label: "Customer Acquisition", type: "select", options: ACQ, required: true, half: true },
      { key: "biggest_challenge", label: "Biggest Challenge", type: "select", options: BIZ_CHALLENGE, required: true, half: true },
      { key: "growth_goals", label: "Growth Goal", type: "text", placeholder: "e.g. 2x revenue in 12 months", half: true },
      { key: "marketing_channels", label: "Marketing Channels You Use", type: "multiselect", options: BIZ_CHANNELS } ] },
  ],
};

const STUDENT_LIKE = ["Student", "Fresher"];

export const ACTIVE_TYPES = ["Student", "Fresher", "IT Employee", "Working Professional", "Manager", "Laid Off Employee", "Career Switcher", "Freelancer", "Business Owner"];

export function stepsFor(userType) {
  if (QUESTIONNAIRES[userType]) return QUESTIONNAIRES[userType];
  return STUDENT_LIKE.includes(userType) ? STUDENT_STEPS : PRO_STEPS;
}

export function metaFor(userType) {
  return PROFILE_META[userType] || { product: "Career Intelligence Report", icon: "Sparkles", goal: "Career Growth", tagline: "A brutally honest, personalized career analysis.", value: [] };
}
