"""Curated learning-resource libraries (MapMyCareer V2).

Hand-authored, deterministic resource sets per career-DB *cluster*, with a
*domain* fallback and a generic fallback. Feeds the Student "Learning Blueprint",
degree/certification/university recommendations and the professional learning plans.
The AI layer only personalises narrative on top — these resources always render.

Each entry: skills, tools, courses, books, youtube, projects, certifications, universities.
"""
from typing import Dict, Any, List

# ---------------------------------------------------------------------------
# CLUSTER-LEVEL content (highest-traffic fields authored in depth)
# ---------------------------------------------------------------------------
CLUSTER_CONTENT: Dict[str, Dict[str, List[str]]] = {
    "Software Engineering": {
        "skills": ["Data Structures & Algorithms", "One backend language (Python/Java/Go)", "One frontend stack (React)", "Databases & SQL", "System Design basics", "Git & CI/CD", "Using AI copilots well"],
        "tools": ["VS Code", "Git & GitHub", "Docker", "Postman", "Linux/CLI", "GitHub Copilot"],
        "courses": ["CS50 (Harvard, free)", "The Odin Project (free)", "freeCodeCamp Full-Stack", "Neetcode.io DSA", "Educative: Grokking the Coding Interview"],
        "books": ["Cracking the Coding Interview — McDowell", "Clean Code — Robert C. Martin", "Designing Data-Intensive Applications — Kleppmann", "The Pragmatic Programmer"],
        "youtube": ["NeetCode", "freeCodeCamp", "Fireship", "ThePrimeagen", "Tech With Tim"],
        "projects": ["A full-stack CRUD app (auth + DB)", "A REST API with tests & docs", "Clone a real product (Twitter/Notion-lite)", "Open-source contribution (1 merged PR)"],
        "certifications": ["AWS Certified Developer", "Meta Front-End Developer (Coursera)", "freeCodeCamp certifications"],
        "universities": ["IITs / NITs / IIITs / BITS", "Strong state engineering colleges (placement-focused)", "Tier-1 private (VIT, Manipal, Thapar)"],
    },
    "AI & Data Science": {
        "skills": ["Python for data", "Math: linear algebra, probability, stats", "Machine Learning (sklearn)", "Deep Learning (PyTorch)", "LLMs, RAG & prompt engineering", "SQL & data wrangling", "MLOps basics"],
        "tools": ["Python + Jupyter", "NumPy / Pandas", "scikit-learn", "PyTorch", "Hugging Face", "LangChain", "SQL"],
        "courses": ["Andrew Ng — Machine Learning Specialization (Coursera)", "fast.ai — Practical Deep Learning (free)", "DeepLearning.AI — LLM/GenAI short courses", "Kaggle Learn (free)"],
        "books": ["Hands-On ML with Scikit-Learn & TensorFlow — Géron", "Deep Learning — Goodfellow", "An Introduction to Statistical Learning (free PDF)"],
        "youtube": ["StatQuest with Josh Starmer", "3Blue1Brown", "Andrej Karpathy", "Krish Naik", "Two Minute Papers"],
        "projects": ["EDA + ML model on a Kaggle dataset", "An end-to-end ML pipeline (train→deploy)", "A RAG chatbot over your own docs", "Fine-tune / prompt-engineer an LLM for a task"],
        "certifications": ["TensorFlow Developer Certificate", "AWS ML Specialty", "Kaggle competition medals (signal)"],
        "universities": ["IITs / IISc (AI/DS programs)", "B.Sc/M.Sc Data Science (top universities)", "BITS, IIITs"],
    },
    "Cloud & DevOps": {
        "skills": ["Linux & networking", "One cloud (AWS/GCP/Azure)", "Docker & Kubernetes", "CI/CD pipelines", "Infrastructure as Code (Terraform)", "Observability & monitoring", "Scripting (Bash/Python)"],
        "tools": ["AWS/GCP/Azure", "Docker", "Kubernetes", "Terraform", "GitHub Actions / Jenkins", "Prometheus + Grafana"],
        "courses": ["AWS Cloud Practitioner → Solutions Architect (free tier + docs)", "KodeKloud DevOps paths", "freeCodeCamp DevOps", "Kubernetes the Hard Way (free)"],
        "books": ["The Phoenix Project", "Site Reliability Engineering — Google (free)", "Kubernetes Up & Running"],
        "youtube": ["TechWorld with Nana", "KodeKloud", "freeCodeCamp", "Cloud With Raj"],
        "projects": ["Containerise & deploy an app to Kubernetes", "Build a CI/CD pipeline end-to-end", "Provision infra with Terraform", "Set up monitoring + alerting for a service"],
        "certifications": ["AWS Solutions Architect Associate", "Certified Kubernetes Administrator (CKA)", "HashiCorp Terraform Associate"],
        "universities": ["B.Tech CS/IT + cloud certifications", "Any degree + strong hands-on labs"],
    },
    "Cybersecurity": {
        "skills": ["Networking & TCP/IP", "Linux", "Web & app security (OWASP)", "Threat analysis & SIEM", "Cryptography basics", "Cloud security", "Scripting"],
        "tools": ["Kali Linux", "Wireshark", "Burp Suite", "Metasploit", "Splunk/ELK", "Nmap"],
        "courses": ["TryHackMe (guided, free tiers)", "Hack The Box Academy", "Professor Messer Security+ (free)", "PortSwigger Web Security Academy (free)"],
        "books": ["The Web Application Hacker's Handbook", "Practical Malware Analysis", "Hacking: The Art of Exploitation"],
        "youtube": ["John Hammond", "NetworkChuck", "IppSec", "The Cyber Mentor"],
        "projects": ["Capture-the-Flag (CTF) writeups", "Home lab: pentest a vulnerable VM", "Build a small SIEM dashboard", "Bug bounty report (responsible disclosure)"],
        "certifications": ["CompTIA Security+", "CEH", "OSCP (advanced)"],
        "universities": ["B.Tech CS / B.Sc Cybersecurity", "Any degree + CEH/OSCP track"],
    },
    "Game Development": {
        "skills": ["C# or C++", "A game engine (Unity / Unreal)", "3D math & physics", "Game design fundamentals", "Version control", "Optimisation & profiling", "Shippable polish"],
        "tools": ["Unity", "Unreal Engine", "Blender", "Git + Git LFS", "Visual Studio / Rider"],
        "courses": ["GameDev.tv — Complete C# Unity Developer", "Unreal Online Learning (free)", "CS50's Intro to Game Development (free)", "Brackeys archive (free)"],
        "books": ["The Art of Game Design — Jesse Schell", "Game Programming Patterns — Nystrom (free online)", "Level Up! — Scott Rogers"],
        "youtube": ["Brackeys", "Code Monkey", "Sebastian Lague", "Game Maker's Toolkit", "Unreal Engine"],
        "projects": ["A finished 2D game (ship it on itch.io)", "A 3D prototype with core loop", "A game jam entry (Ludum Dare/GMTK)", "A polished portfolio demo"],
        "certifications": ["Unity Certified Associate", "A public portfolio + shipped games (matters more than certs)"],
        "universities": ["B.Tech CS / B.Des Game Design", "DSK/IIIT/Backstage Pass + strong portfolio"],
    },
    "UX & Product Design": {
        "skills": ["User research & interviews", "Wireframing & prototyping", "Visual & interaction design", "Design systems", "Usability testing", "Figma mastery", "Design storytelling"],
        "tools": ["Figma", "FigJam", "Maze", "Notion", "Framer"],
        "courses": ["Google UX Design Certificate (Coursera)", "Refactoring UI", "Design+Code", "Interaction Design Foundation"],
        "books": ["The Design of Everyday Things — Norman", "Don't Make Me Think — Krug", "About Face — Cooper"],
        "youtube": ["AJ&Smart", "Flux Academy", "The Futur", "Femke (design)"],
        "projects": ["End-to-end case study (research→ship)", "Redesign a real app with rationale", "A reusable design system", "A usability test report"],
        "certifications": ["Google UX Design Certificate", "NN/g UX Certification", "A strong portfolio (decisive)"],
        "universities": ["NID / NIFT / Srishti", "B.Des / HCI programs + portfolio"],
    },
    "Marketing & Social Media": {
        "skills": ["Positioning & messaging", "SEO & content", "Performance ads (Meta/Google)", "Analytics & attribution", "Copywriting", "Email & lifecycle", "AI marketing tools"],
        "tools": ["Google Analytics 4", "Meta/Google Ads", "Ahrefs/SEMrush", "Canva", "HubSpot", "ChatGPT"],
        "courses": ["Google Digital Garage (free)", "HubSpot Academy (free)", "Meta Blueprint", "CXL marketing courses"],
        "books": ["Building a StoryBrand — Miller", "Hooked — Eyal", "$100M Offers — Hormozi", "Influence — Cialdini"],
        "youtube": ["Neil Patel", "GaryVee", "HubSpot", "Ahrefs"],
        "projects": ["Grow a real account/blog to first 1k", "Run a small ad campaign with reporting", "Rank one page on Google", "A full funnel case study"],
        "certifications": ["Google Ads & Analytics certifications", "HubSpot Content/Inbound", "Meta Blueprint"],
        "universities": ["BBA/MBA Marketing", "Any degree + Digital Marketing certs + portfolio"],
    },
    "Product & Strategy": {
        "skills": ["Product discovery & user research", "Prioritisation & roadmapping", "Analytics & metrics", "Stakeholder leadership", "Strategy & business model", "Working with engineering & design", "AI product sense"],
        "tools": ["Jira/Linear", "Amplitude/Mixpanel", "Figma", "Notion", "SQL basics"],
        "courses": ["Reforge (advanced)", "Product School", "SVPG / Marty Cagan resources", "Coursera — Digital Product Management"],
        "books": ["Inspired — Marty Cagan", "Continuous Discovery Habits — Torres", "Hooked — Eyal", "The Lean Startup — Ries"],
        "youtube": ["Lenny's Podcast", "Product School", "Aakash Gupta"],
        "projects": ["A product spec + metrics for a real problem", "An A/B test analysis", "A roadmap with prioritisation rationale", "A teardown of a popular product"],
        "certifications": ["Reforge programs", "Pragmatic Institute", "Demonstrated product work (decisive)"],
        "universities": ["B.Tech + MBA / BBA + experience", "IIMs / ISB for acceleration"],
    },
    "Finance & Banking": {
        "skills": ["Accounting fundamentals", "Financial modelling (Excel)", "Valuation (DCF/comps)", "Markets & instruments", "Risk analysis", "Power BI / SQL", "Communication"],
        "tools": ["Excel (advanced)", "Power BI / Tableau", "Bloomberg/Capital IQ (where available)", "Python for finance"],
        "courses": ["CFI — Financial Modeling & Valuation", "Wall Street Prep", "NPTEL Finance", "Coursera — Investment Management"],
        "books": ["The Intelligent Investor — Graham", "Investment Banking — Rosenbaum & Pearl", "Financial Statement Analysis — Subramanyam"],
        "youtube": ["CA Rachana Ranade", "Financial Education", "Aswath Damodaran (valuation)"],
        "projects": ["Build a 3-statement model + DCF", "Equity research report on a listed company", "A personal investment thesis", "Excel dashboard for a business"],
        "certifications": ["CFA (Level I→III)", "FRM", "CA / CMA", "CFI FMVA"],
        "universities": ["SRCC & top commerce colleges", "CA/CFA institutes", "MBA Finance (tier-1)"],
    },
    "Medicine & Clinical": {
        "skills": ["Biology & human physiology", "Clinical reasoning", "Diagnostics", "Patient communication & empathy", "Evidence-based medicine", "Medical AI literacy"],
        "tools": ["NEET prep ecosystem", "Anatomy atlases", "UpToDate / clinical references"],
        "courses": ["NEET coaching / NCERT mastery", "Osmosis / Lecturio (concepts)", "Coursera — Anatomy/Physiology"],
        "books": ["NCERT Biology (foundation)", "Guyton & Hall Physiology", "Robbins Pathology (later)"],
        "youtube": ["Osmosis", "Ninja Nerd", "Dr. Najeeb Lectures"],
        "projects": ["NEET mock-test discipline", "Clinical volunteering / shadowing", "Research/poster participation"],
        "certifications": ["NEET → MBBS → MD/MS specialisation", "Clinical specialisations"],
        "universities": ["AIIMS & government medical colleges", "Top private medical colleges (NEET)"],
    },
    "Civil & Public Services": {
        "skills": ["General studies (polity/history/geo/economy)", "Current affairs", "Aptitude & reasoning (CSAT)", "Essay & answer writing", "Optional subject mastery", "Interview & personality"],
        "tools": ["NCERTs", "Standard reference books", "PYQ analysis", "Test series"],
        "courses": ["Quality coaching or structured self-study", "Vision IAS / Vajiram material", "PMF IAS (geography)"],
        "books": ["NCERTs (6–12)", "Laxmikanth — Indian Polity", "Spectrum — Modern History", "Economic Survey & budget"],
        "youtube": ["StudyIQ", "Drishti IAS", "Unacademy UPSC"],
        "projects": ["Daily answer-writing practice", "Monthly current-affairs notes", "Full-length mock tests + analysis"],
        "certifications": ["UPSC CSE (Prelims→Mains→Interview)", "State PSC / SSC as parallel tracks"],
        "universities": ["Any graduate degree + disciplined prep", "DU / top universities for foundation"],
    },
    "Content & Writing": {
        "skills": ["Clear writing & editing", "Storytelling & hooks", "SEO writing", "Research", "Audience building", "Distribution", "AI writing tools (as leverage)"],
        "tools": ["Google Docs", "Grammarly", "Ahrefs/SEMrush", "Notion", "Substack/Medium"],
        "courses": ["The Writing Process (Coursera)", "Ship 30 for 30", "HubSpot Content Marketing (free)"],
        "books": ["On Writing Well — Zinsser", "Everybody Writes — Handley", "Bird by Bird — Lamott"],
        "youtube": ["Ali Abdaal (writing/creator)", "The Futur", "HubSpot"],
        "projects": ["Publish 20 pieces consistently", "Grow a newsletter to first 500", "Ghostwrite for one client", "A portfolio site of your best work"],
        "certifications": ["HubSpot Content Marketing", "Portfolio + audience (decisive)"],
        "universities": ["Mass Comm / Journalism (optional)", "Any degree + a strong portfolio"],
    },
}

# ---------------------------------------------------------------------------
# DOMAIN-LEVEL fallback (covers every career_db domain)
# ---------------------------------------------------------------------------
DOMAIN_CONTENT: Dict[str, Dict[str, List[str]]] = {
    "Technology": CLUSTER_CONTENT["Software Engineering"],
    "Creative": CLUSTER_CONTENT["UX & Product Design"],
    "Media": CLUSTER_CONTENT["Content & Writing"],
    "Business": CLUSTER_CONTENT["Product & Strategy"],
    "Finance": CLUSTER_CONTENT["Finance & Banking"],
    "Healthcare": CLUSTER_CONTENT["Medicine & Clinical"],
    "Government": CLUSTER_CONTENT["Civil & Public Services"],
    "Entrepreneurship": {
        "skills": ["Sales & customer development", "Product & MVP building", "Marketing & distribution", "Unit economics & finance", "Hiring & operations", "Resilience & decision-making"],
        "tools": ["No-code (Bubble/Webflow)", "Stripe/Razorpay", "Notion", "Meta/Google Ads", "Analytics"],
        "courses": ["Y Combinator Startup School (free)", "The Lean Startup", "$100M Offers — Hormozi"],
        "books": ["The Lean Startup — Ries", "Zero to One — Thiel", "The Mom Test — Fitzpatrick"],
        "youtube": ["Y Combinator", "Starter Story", "GaryVee"],
        "projects": ["Validate one idea with 20 customer interviews", "Ship an MVP + first paying customer", "Run a small pre-sell campaign"],
        "certifications": ["Revenue & traction (the only real proof)"],
        "universities": ["No degree required; BBA/MBA optional"],
    },
    "Legal": {
        "skills": ["Legal research", "Drafting & argumentation", "Analysis", "Negotiation", "Domain law", "Legal-tech & AI tools"],
        "tools": ["SCC Online / Manupatra", "Drafting templates", "Legal AI tools"],
        "courses": ["CLAT prep", "NPTEL Law", "Coursera — Introduction to Law"],
        "books": ["Bare Acts", "Legal Method — texts", "Subject-wise standard texts"],
        "youtube": ["Finology Legal", "StudyIQ Judiciary"],
        "projects": ["Moot court participation", "Legal internships", "Drafting portfolio"],
        "certifications": ["BA LLB / LLB (CLAT) → Bar exam", "CS / specialisations"],
        "universities": ["NLUs (CLAT)", "Symbiosis, Jindal Global Law"],
    },
    "Education": {
        "skills": ["Subject mastery", "Communication & explanation", "Lesson & curriculum design", "Assessment", "EdTech tools", "Mentoring"],
        "tools": ["Google Classroom", "Canva", "Notion", "Video tools"],
        "courses": ["B.Ed", "NPTEL / subject MOOCs", "Coursera — Teaching"],
        "books": ["Make It Stick", "Teach Like a Champion"],
        "youtube": ["Subject-expert channels", "EdTech creators"],
        "projects": ["Create a course/playlist", "Tutor and gather outcomes", "Build teaching content"],
        "certifications": ["B.Ed + NET (for academia)", "Subject certifications"],
        "universities": ["Central universities + B.Ed", "M.A/M.Sc + NET"],
    },
    "Research": {
        "skills": ["Research methods", "Data analysis & statistics", "Scientific writing", "Domain expertise", "Lab/technical skills", "Critical reading"],
        "tools": ["Python/R", "LaTeX", "Reference managers", "Lab instruments"],
        "courses": ["NPTEL research methods", "Coursera — research/statistics", "Subject MOOCs"],
        "books": ["Subject standard texts", "How to Write a Lot — Silvia"],
        "youtube": ["Subject lecture series", "Veritasium (science comm)"],
        "projects": ["A research paper / poster", "Lab internships", "Replicate a known study"],
        "certifications": ["M.Sc → PhD", "Research fellowships"],
        "universities": ["IISc / IITs / central universities", "Integrated MSc programs"],
    },
    "Defense": {
        "skills": ["Physical fitness", "Leadership & discipline", "Aptitude & reasoning", "Teamwork", "Decision-making under pressure"],
        "tools": ["NDA/CDS prep material", "Fitness regimen", "SSB resources"],
        "courses": ["NDA/CDS coaching or self-study", "SSB interview prep"],
        "books": ["Pathfinder for NDA/NA", "SSB interview guides"],
        "youtube": ["SSBCrack", "Defence Direct Education"],
        "projects": ["Fitness milestones", "Mock SSB", "Leadership roles in college"],
        "certifications": ["NDA / CDS / SSB clearance", "Technical entries"],
        "universities": ["NDA (after 12th)", "Any degree + CDS/SSB"],
    },
    "Sports": {
        "skills": ["Sport-specific skill", "Physical conditioning", "Mental toughness", "Nutrition", "Strategy", "Discipline"],
        "tools": ["Training plans", "Wearables", "Coaching feedback"],
        "courses": ["NIS coaching diploma", "Sports science programs", "Certifications (fitness)"],
        "books": ["Peak — Ericsson", "The Champion's Mind"],
        "youtube": ["Sport-specific coaching channels", "AthleanX (fitness)"],
        "projects": ["Compete at district/state level", "Build a training log", "Coaching/assistant roles"],
        "certifications": ["B.P.Ed / NIS / fitness certifications"],
        "universities": ["Sports authorities & academies", "B.P.Ed / Sports Science"],
    },
    "Skilled Trades": {
        "skills": ["Hands-on technical skill", "Safety practices", "Tools mastery", "Precision", "Problem solving", "Customer service"],
        "tools": ["Trade-specific tools", "Measurement instruments"],
        "courses": ["ITI / polytechnic diploma", "Apprenticeship", "Vocational certifications"],
        "books": ["Trade manuals", "Safety standards"],
        "youtube": ["Trade-specific how-to channels"],
        "projects": ["Apprenticeship hours", "A portfolio of completed jobs", "Customer testimonials"],
        "certifications": ["ITI / NCVT / trade licenses"],
        "universities": ["ITIs & polytechnics", "Apprenticeships"],
    },
    "Hospitality": {
        "skills": ["Service excellence", "Communication", "Operations", "Domain skill (culinary/aviation)", "Stamina", "Languages"],
        "tools": ["POS / PMS systems", "Reservation systems"],
        "courses": ["IHM / hotel management", "Aviation / DGCA (pilot)", "Culinary diploma"],
        "books": ["Setting the Table — Danny Meyer", "Domain texts"],
        "youtube": ["Hospitality & culinary channels"],
        "projects": ["Internships in hotels/airlines", "Service portfolio"],
        "certifications": ["IHM / DGCA / domain certifications"],
        "universities": ["IHMs", "Aviation academies"],
    },
}

GENERIC = {
    "skills": ["Core fundamentals of the field", "Communication", "One practical, in-demand tool", "Problem solving", "A portfolio that proves capability", "AI tools as leverage"],
    "tools": ["Industry-standard tools for the role", "Google Workspace / Notion", "AI assistants"],
    "courses": ["A reputable foundational course (Coursera/NPTEL)", "Hands-on certification in your field", "YouTube + structured practice"],
    "books": ["The standard introductory text for the field", "Deep Work — Cal Newport", "So Good They Can't Ignore You — Newport"],
    "youtube": ["Top creators in your specific field", "Ali Abdaal (productivity/learning)"],
    "projects": ["One real, shippable project that proves a skill", "A public portfolio / profile", "An internship or apprenticeship"],
    "certifications": ["The recognised entry credential for your field", "A portfolio of real work (decisive)"],
    "universities": ["Top government college in your stream", "Reputed private with strong placements"],
}


def learning_for(career: Dict[str, Any]) -> Dict[str, List[str]]:
    """Return curated learning resources for a career (cluster → domain → generic)."""
    base = dict(GENERIC)
    dom = DOMAIN_CONTENT.get(career.get("domain", ""))
    if dom:
        base = {**base, **dom}
    cl = CLUSTER_CONTENT.get(career.get("cluster", ""))
    if cl:
        base = {**base, **cl}
    # prefer the career's own cluster skills if present
    if career.get("skills"):
        base = {**base, "skills": career["skills"]}
    # always attach the career's own degrees as universities/degrees hint
    return base
