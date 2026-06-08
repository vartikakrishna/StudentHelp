"""Comprehensive career database (200+ careers across 13 domains), organised in
clusters so we can recommend RELATED careers around a user's dream — never a
generic substitute.

Each generated career is compatible with careers.py scoring (keys: w, t,
market_demand, salary_score, competition, ai_risk, difficulty, time_to_enter,
salary{entry,mid,senior}, growth, industries, learn_next) and adds:
domain, cluster, skills, degrees, related.
"""
import re
from typing import Dict, List, Any, Optional, Tuple

# Default interest weights (keys must be from careers.INTEREST_LABELS) per domain
DOMAIN_INTERESTS = {
    "Technology": {"technology": 0.9, "problem_solving": 0.7},
    "Creative": {"design": 0.9, "content_creation": 0.5},
    "Media": {"content_creation": 0.9, "writing": 0.5, "marketing": 0.4},
    "Business": {"business": 0.9, "leadership": 0.6},
    "Finance": {"finance": 0.9, "business": 0.5, "problem_solving": 0.4},
    "Entrepreneurship": {"entrepreneurship": 1.0, "business": 0.6, "leadership": 0.5},
    "Healthcare": {"healthcare": 1.0, "research": 0.4},
    "Legal": {"law": 1.0, "problem_solving": 0.4},
    "Government": {"law": 0.5, "leadership": 0.5, "problem_solving": 0.4},
    "Defense": {"leadership": 0.6, "problem_solving": 0.4},
    "Education": {"teaching": 1.0, "research": 0.4},
    "Research": {"research": 1.0, "problem_solving": 0.6, "technology": 0.4},
    "Sports": {"leadership": 0.4, "problem_solving": 0.3},
    "Skilled Trades": {"problem_solving": 0.5, "technology": 0.3},
    "Hospitality": {"business": 0.5, "content_creation": 0.4},
}

DOMAIN_TRAITS = {
    "Technology": {"analytical": 0.9, "specialist": 0.5, "independent": 0.4},
    "Creative": {"creative": 1.0, "independent": 0.4},
    "Media": {"creative": 0.8, "extrovert": 0.5, "communication": 0.6},
    "Business": {"leader": 0.7, "extrovert": 0.5, "communication": 0.6},
    "Finance": {"analytical": 0.9, "specialist": 0.4},
    "Entrepreneurship": {"leader": 0.9, "risk": 0.9, "extrovert": 0.5},
    "Healthcare": {"analytical": 0.7, "specialist": 0.6, "communication": 0.5},
    "Legal": {"analytical": 0.8, "communication": 0.7},
    "Government": {"analytical": 0.6, "leader": 0.5, "communication": 0.5},
    "Defense": {"leader": 0.6, "stable": 0.5, "team": 0.5},
    "Education": {"communication": 0.8, "specialist": 0.4},
    "Research": {"analytical": 1.0, "specialist": 0.7, "independent": 0.5},
    "Sports": {"risk": 0.6, "independent": 0.4, "stable": 0.3},
    "Skilled Trades": {"specialist": 0.6, "independent": 0.5},
    "Hospitality": {"extrovert": 0.6, "communication": 0.6, "team": 0.5},
}


def _slug(t: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", t.lower())).strip("_")


def _salary_score(mid: int) -> int:
    return max(30, min(98, round(34 + mid * 1.35)))


def _time(diff: int) -> str:
    if diff < 40:
        return "3-6 months"
    if diff < 60:
        return "6-12 months"
    if diff < 78:
        return "1-2 years"
    return "2-5 years"


def growth_forecast(market: int) -> str:
    if market >= 88:
        return "Explosive — among the fastest-growing fields"
    if market >= 74:
        return "Strong — healthy, sustained growth"
    if market >= 58:
        return "Steady — stable demand"
    return "Flat / declining — be selective"


# cluster: name, domain, icon, market, ai_risk, competition, difficulty, growth, salary(e,mid,sen),
#          degrees[], skills[], careers[(key,title) | "Title"], optional interests/traits/industries
C = [
    # ---------------- TECHNOLOGY ----------------
    {"cluster": "Software Engineering", "domain": "Technology", "icon": "Code", "market": 90, "ai_risk": 30, "competition": 72, "difficulty": 70, "growth": "High", "salary": (7, 22, 60),
     "degrees": ["B.Tech / BE CS or IT", "BCA → MCA", "Self-taught + portfolio"], "skills": ["DSA", "One backend + one frontend stack", "System Design", "Git", "AI copilots", "Cloud basics"],
     "industries": ["Tech", "SaaS", "Fintech", "Startups"],
     "careers": [("software_engineer", "Software Engineer"), "Backend Developer", "Frontend Developer", "Full Stack Developer", "Mobile App Developer", "API Engineer", ("embedded_engineer", "Embedded Systems Engineer"), "Web Developer"]},
    {"cluster": "AI & Data Science", "domain": "Technology", "icon": "Cpu", "market": 95, "ai_risk": 12, "competition": 70, "difficulty": 84, "growth": "Explosive", "salary": (9, 28, 70),
     "degrees": ["B.Tech CS / AI-ML", "B.Sc / M.Sc Data Science", "M.Tech AI"], "skills": ["Python", "Machine Learning", "LLMs & RAG", "Statistics", "MLOps", "SQL"],
     "industries": ["AI", "Big Tech", "Fintech", "Research"],
     "careers": [("ai_ml_engineer", "AI / Machine Learning Engineer"), ("data_scientist", "Data Scientist"), ("data_analyst", "Data Analyst"), "Data Engineer", "NLP Engineer", "Computer Vision Engineer", "MLOps Engineer", "AI Research Engineer"]},
    {"cluster": "Cloud & DevOps", "domain": "Technology", "icon": "Cloud", "market": 88, "ai_risk": 24, "competition": 56, "difficulty": 68, "growth": "High", "salary": (7, 22, 55),
     "degrees": ["B.Tech CS / IT", "Cloud certifications (AWS/GCP/Azure)"], "skills": ["AWS/GCP/Azure", "Docker & Kubernetes", "CI/CD", "Terraform", "Linux", "Observability"],
     "industries": ["Cloud", "Tech", "SaaS"],
     "careers": [("cloud_devops", "Cloud / DevOps Engineer"), "Site Reliability Engineer", "Platform Engineer", "Cloud Architect", "Network Engineer", "Infrastructure Engineer"]},
    {"cluster": "Cybersecurity", "domain": "Technology", "icon": "ShieldCheck", "market": 92, "ai_risk": 14, "competition": 54, "difficulty": 74, "growth": "Explosive", "salary": (6, 20, 52),
     "degrees": ["B.Tech CS", "B.Sc Cybersecurity", "CEH / OSCP"], "skills": ["Networking", "Linux", "Ethical hacking", "SIEM tools", "Cloud security", "Threat analysis"],
     "industries": ["Security", "BFSI", "Cloud", "Government"],
     "careers": [("cybersecurity", "Cybersecurity Specialist"), "Ethical Hacker", "Security Analyst", "SOC Analyst", "Security Architect", "Penetration Tester"]},
    {"cluster": "Game Development", "domain": "Technology", "icon": "Gamepad2", "market": 80, "ai_risk": 28, "competition": 80, "difficulty": 76, "growth": "High", "salary": (5, 16, 42),
     "degrees": ["B.Tech CS / Game Design", "B.Des Game Design", "Diploma + strong portfolio"], "skills": ["C# / C++", "Unity", "Unreal Engine", "3D Math", "Game Design", "Version Control"],
     "industries": ["Gaming", "AR/VR", "Interactive Media", "Mobile"],
     "interests": {"technology": 0.8, "design": 0.6, "content_creation": 0.4, "problem_solving": 0.7},
     "traits": {"creative": 0.6, "analytical": 0.6, "independent": 0.4},
     "careers": [("game_developer", "Game Developer"), "Gameplay Programmer", "Unity Developer", "Unreal Developer", "Game Designer", "AR/VR Developer", "3D Technical Artist", "Interactive Media Developer", "Level Designer", "Game QA Tester"]},
    {"cluster": "Emerging Tech", "domain": "Technology", "icon": "Rocket", "market": 78, "ai_risk": 20, "competition": 62, "difficulty": 80, "growth": "Explosive", "salary": (8, 24, 60),
     "degrees": ["B.Tech CS", "Specialised bootcamp + projects"], "skills": ["Solidity", "Cryptography", "Distributed systems", "Rust", "IoT", "Robotics"],
     "industries": ["Web3", "Robotics", "IoT", "Deep Tech"],
     "careers": [("blockchain_developer", "Blockchain Developer"), "Smart Contract Engineer", "Robotics Engineer", "IoT Engineer", "AR/VR Engineer", "Quantum Computing Researcher"]},
    {"cluster": "QA & IT Operations", "domain": "Technology", "icon": "Bug", "market": 66, "ai_risk": 58, "competition": 66, "difficulty": 50, "growth": "Moderate", "salary": (4, 11, 26),
     "degrees": ["B.Tech / BCA", "Any degree + certifications"], "skills": ["Test automation", "Selenium", "SQL", "Linux", "Scripting", "Monitoring"],
     "industries": ["IT Services", "SaaS", "Enterprise"],
     "careers": ["QA Engineer", "Automation Tester", "SDET", "IT Support Specialist", "System Administrator", "Database Administrator"]},
    # ---------------- CREATIVE / DESIGN ----------------
    {"cluster": "UX & Product Design", "domain": "Creative", "icon": "Palette", "market": 82, "ai_risk": 28, "competition": 70, "difficulty": 60, "growth": "High", "salary": (5, 16, 42),
     "degrees": ["B.Des / B.Sc Design", "HCI / UX bootcamp", "Any degree + portfolio"], "skills": ["Figma", "User research", "Prototyping", "Interaction design", "Design systems", "Usability testing"],
     "industries": ["Tech", "SaaS", "Consumer Apps", "Agencies"],
     "careers": [("ux_designer", "UX Designer"), "UI Designer", "Product Designer", "Interaction Designer", "Design Researcher", "Design Systems Lead"]},
    {"cluster": "Graphic & Visual Design", "domain": "Creative", "icon": "PenTool", "market": 70, "ai_risk": 45, "competition": 74, "difficulty": 48, "growth": "Moderate", "salary": (3, 9, 24),
     "degrees": ["B.Des / BFA", "Diploma in Graphic Design", "Self-taught + portfolio"], "skills": ["Adobe Suite", "Typography", "Branding", "Layout", "Motion basics", "Color theory"],
     "industries": ["Advertising", "Media", "Startups", "Agencies"],
     "careers": ["Graphic Designer", "Brand Designer", "Illustrator", "Motion Graphics Designer", "Packaging Designer", "Visual Designer"]},
    {"cluster": "Animation & VFX", "domain": "Creative", "icon": "Film", "market": 76, "ai_risk": 38, "competition": 72, "difficulty": 66, "growth": "High", "salary": (4, 13, 38),
     "degrees": ["B.Des Animation", "Diploma in Animation / VFX", "Specialised institute"], "skills": ["3D modelling", "Maya / Blender", "Rigging", "Compositing", "Storyboarding", "Texturing"],
     "industries": ["Film", "Gaming", "OTT", "Advertising"],
     "careers": ["2D Animator", "3D Animator", "VFX Artist", "Character Artist", "Compositor", "Motion Designer", "Storyboard Artist"]},
    {"cluster": "Architecture & Spaces", "domain": "Creative", "icon": "Building", "market": 68, "ai_risk": 30, "competition": 64, "difficulty": 78, "growth": "Steady", "salary": (4, 12, 35),
     "degrees": ["B.Arch", "B.Des Interior", "M.Plan"], "skills": ["AutoCAD", "Revit", "3D rendering", "Design thinking", "Building codes", "Sustainability"],
     "industries": ["Real Estate", "Construction", "Design Firms"],
     "careers": ["Architect", "Interior Designer", "Landscape Architect", "Urban Planner", "Set Designer"]},
    {"cluster": "Fashion & Product Design", "domain": "Creative", "icon": "Shirt", "market": 64, "ai_risk": 32, "competition": 72, "difficulty": 60, "growth": "Steady", "salary": (3, 10, 30),
     "degrees": ["B.Des Fashion (NIFT)", "Diploma in Design", "B.Des Industrial"], "skills": ["Sketching", "Pattern making", "Textiles", "CAD", "Trend research", "Prototyping"],
     "industries": ["Fashion", "Manufacturing", "Retail", "Luxury"],
     "careers": ["Fashion Designer", "Textile Designer", "Industrial Designer", "Jewellery Designer", "Footwear Designer", "Accessory Designer"]},
    # ---------------- MEDIA ----------------
    {"cluster": "Content & Writing", "domain": "Media", "icon": "PenLine", "market": 72, "ai_risk": 52, "competition": 70, "difficulty": 45, "growth": "Moderate", "salary": (3, 10, 28),
     "degrees": ["Any degree + portfolio", "Mass Communication", "Journalism"], "skills": ["Writing", "SEO", "Storytelling", "Editing", "Research", "AI writing tools"],
     "industries": ["Media", "Marketing", "Publishing", "Tech"],
     "careers": [("content_creator", "Content Creator"), "Copywriter", "Technical Writer", "Scriptwriter", "Journalist", "Editor", "Author / Novelist", "UX Writer"]},
    {"cluster": "Film, Video & Audio", "domain": "Media", "icon": "Clapperboard", "market": 74, "ai_risk": 35, "competition": 78, "difficulty": 60, "growth": "High", "salary": (3, 12, 40),
     "degrees": ["Film school / Mass Comm", "Diploma in Film/Audio", "Self-taught + reel"], "skills": ["Editing", "Cinematography", "Sound design", "Storytelling", "Color grading", "Production"],
     "industries": ["Film", "OTT", "YouTube", "Advertising"],
     "careers": ["Filmmaker / Director", "Video Editor", "Cinematographer", "Sound Designer", ("youtuber", "YouTuber / Creator"), "Podcaster", "Music Producer", "Sound Engineer"]},
    {"cluster": "Marketing & Social Media", "domain": "Media", "icon": "Megaphone", "market": 80, "ai_risk": 42, "competition": 72, "difficulty": 52, "growth": "High", "salary": (4, 13, 40),
     "degrees": ["BBA / MBA Marketing", "Any degree + Digital Marketing cert"], "skills": ["SEO", "Performance ads", "Content strategy", "Analytics", "Social media", "Brand building"],
     "industries": ["Marketing", "E-commerce", "Startups", "Agencies"],
     "careers": [("digital_marketer", "Digital Marketer"), "Social Media Manager", "SEO Specialist", "Performance Marketer", "Brand Manager", "PR Specialist", "Influencer / Creator", "Growth Marketer"]},
    # ---------------- BUSINESS ----------------
    {"cluster": "Product & Strategy", "domain": "Business", "icon": "Rocket", "market": 84, "ai_risk": 22, "competition": 78, "difficulty": 75, "growth": "High", "salary": (10, 30, 75),
     "degrees": ["B.Tech + MBA", "BBA / MBA", "Any degree + experience"], "skills": ["Product strategy", "Analytics", "User research", "Stakeholder leadership", "Roadmapping", "AI products"],
     "industries": ["Tech", "SaaS", "Consulting", "Consumer"],
     "careers": [("product_manager", "Product Manager"), "Business Analyst", "Strategy Manager", ("management_consultant", "Management Consultant"), "Operations Manager", "Project Manager", "Program Manager"]},
    {"cluster": "Finance & Banking", "domain": "Finance", "icon": "Landmark", "market": 78, "ai_risk": 38, "competition": 76, "difficulty": 80, "growth": "Steady", "salary": (6, 20, 60),
     "degrees": ["B.Com + MBA Finance", "CA / CFA / CMA", "Economics + Finance"], "skills": ["Financial modelling", "Valuation", "Excel", "Accounting", "Markets", "Risk analysis"],
     "industries": ["BFSI", "Investment", "Consulting", "Corporates"],
     "careers": [("investment_banker", "Investment Banker"), ("financial_analyst", "Financial Analyst"), ("chartered_accountant", "Chartered Accountant"), "Financial Planner", "Equity Research Analyst", "Actuary", "Risk Analyst", "Wealth Manager"]},
    {"cluster": "Sales & Business Development", "domain": "Business", "icon": "Handshake", "market": 76, "ai_risk": 30, "competition": 60, "difficulty": 50, "growth": "High", "salary": (4, 14, 45),
     "degrees": ["BBA / any degree", "MBA Sales & Marketing"], "skills": ["Negotiation", "Communication", "CRM", "Pipeline management", "Relationship building", "Closing"],
     "industries": ["SaaS", "BFSI", "Real Estate", "B2B"],
     "careers": [("sales_leader", "Sales Leader"), "Account Executive", "Business Development Manager", "Key Account Manager", "Inside Sales Rep", "Sales Manager"]},
    {"cluster": "HR & People", "domain": "Business", "icon": "Users", "market": 70, "ai_risk": 40, "competition": 58, "difficulty": 52, "growth": "Steady", "salary": (4, 12, 35),
     "degrees": ["MBA HR", "BBA + HR cert", "Psychology + HR"], "skills": ["Talent acquisition", "People management", "L&D", "HR analytics", "Employee relations", "Communication"],
     "industries": ["Corporates", "Startups", "Consulting"],
     "careers": ["HR Manager", "Talent Acquisition Specialist", "HR Business Partner", "L&D Specialist", "People Operations Manager"]},
    # ---------------- ENTREPRENEURSHIP ----------------
    {"cluster": "Entrepreneurship", "domain": "Entrepreneurship", "icon": "Lightbulb", "market": 72, "ai_risk": 18, "competition": 60, "difficulty": 82, "growth": "High", "salary": (0, 18, 100),
     "degrees": ["No degree required", "BBA / MBA (optional)", "Any degree + a real venture"], "skills": ["Sales", "Product", "Fundraising", "Operations", "Marketing", "Resilience"],
     "industries": ["Startups", "E-commerce", "SaaS", "D2C"],
     "careers": [("entrepreneur", "Startup Founder"), "Solopreneur", "E-commerce Business Owner", "Agency Owner", "Franchise Owner", "Small Business Owner"]},
    # ---------------- HEALTHCARE ----------------
    {"cluster": "Medicine & Clinical", "domain": "Healthcare", "icon": "Stethoscope", "market": 86, "ai_risk": 12, "competition": 88, "difficulty": 92, "growth": "Strong", "salary": (6, 18, 60),
     "degrees": ["MBBS + MD/MS", "BDS", "BAMS / BHMS"], "skills": ["Biology", "Clinical reasoning", "Patient care", "Anatomy", "Diagnostics", "Empathy"],
     "industries": ["Hospitals", "Clinics", "Public Health"],
     "careers": [("doctor", "Doctor / Physician"), "Surgeon", "Dentist", "Radiologist", "Pediatrician", "Cardiologist", "General Practitioner"]},
    {"cluster": "Allied Health & Wellness", "domain": "Healthcare", "icon": "HeartPulse", "market": 78, "ai_risk": 18, "competition": 60, "difficulty": 66, "growth": "Strong", "salary": (3, 10, 28),
     "degrees": ["B.Sc Nursing / Allied Health", "BPT / B.Pharm", "Psychology / Nutrition"], "skills": ["Patient care", "Anatomy", "Communication", "Clinical skills", "Empathy", "Domain knowledge"],
     "industries": ["Hospitals", "Wellness", "Pharma", "Clinics"],
     "careers": [("psychologist", "Psychologist"), "Physiotherapist", "Nurse", "Pharmacist", "Dietitian / Nutritionist", "Optometrist", "Veterinarian", "Clinical Psychologist", "Biomedical Engineer"]},
    # ---------------- LEGAL ----------------
    {"cluster": "Law & Justice", "domain": "Legal", "icon": "Scale", "market": 72, "ai_risk": 30, "competition": 80, "difficulty": 80, "growth": "Steady", "salary": (4, 14, 55),
     "degrees": ["BA LLB / LLB (CLAT)", "Company Secretary (CS)", "LLM"], "skills": ["Legal research", "Drafting", "Argumentation", "Analysis", "Negotiation", "Domain law"],
     "industries": ["Law Firms", "Corporates", "Judiciary", "Compliance"],
     "careers": [("lawyer", "Lawyer / Advocate"), "Corporate Lawyer", "Litigation Lawyer", "Company Secretary", "Legal Advisor", "Paralegal", "Judge (via judiciary exams)"]},
    # ---------------- GOVERNMENT ----------------
    {"cluster": "Civil & Public Services", "domain": "Government", "icon": "Landmark", "market": 70, "ai_risk": 10, "competition": 95, "difficulty": 90, "growth": "Stable", "salary": (8, 16, 30),
     "degrees": ["Any graduate degree (UPSC/SSC)", "Subject degree + exam prep"], "skills": ["General studies", "Aptitude", "Essay & answer writing", "Current affairs", "Discipline", "Interview skills"],
     "industries": ["Government", "Public Sector", "Administration"],
     "careers": [("ias_officer", "IAS Officer"), "IPS Officer", "IFS / Diplomat", "Bank PO", "SSC Officer", "Policy Analyst", "Government Officer"]},
    # ---------------- DEFENSE ----------------
    {"cluster": "Defense & Forces", "domain": "Defense", "icon": "Shield", "market": 68, "ai_risk": 12, "competition": 88, "difficulty": 86, "growth": "Stable", "salary": (8, 15, 28),
     "degrees": ["NDA / CDS", "B.Tech (technical entry)", "Any degree + SSB"], "skills": ["Physical fitness", "Leadership", "Discipline", "Aptitude", "Teamwork", "Decision-making"],
     "industries": ["Armed Forces", "Defense", "Merchant Navy"],
     "careers": ["Army Officer", "Navy Officer", "Air Force Pilot", "Defense Engineer", "Merchant Navy Officer", "Commando / Special Forces"]},
    # ---------------- EDUCATION ----------------
    {"cluster": "Teaching & Academia", "domain": "Education", "icon": "GraduationCap", "market": 70, "ai_risk": 25, "competition": 60, "difficulty": 60, "growth": "Steady", "salary": (3, 9, 25),
     "degrees": ["B.Ed + subject degree", "M.A / M.Sc + NET", "PhD (academia)"], "skills": ["Subject mastery", "Communication", "Lesson design", "Mentoring", "Assessment", "EdTech tools"],
     "industries": ["Schools", "Colleges", "EdTech", "Coaching"],
     "careers": [("teacher_edtech", "School Teacher"), "Professor / Lecturer", "EdTech Content Creator", "Instructional Designer", "Education Counselor", "Academic Researcher", "Corporate Trainer"]},
    # ---------------- RESEARCH ----------------
    {"cluster": "Science & Research", "domain": "Research", "icon": "FlaskConical", "market": 72, "ai_risk": 18, "competition": 66, "difficulty": 85, "growth": "Strong", "salary": (5, 13, 38),
     "degrees": ["B.Sc / M.Sc + PhD", "B.Tech + research", "Integrated MSc"], "skills": ["Research methods", "Data analysis", "Domain expertise", "Scientific writing", "Lab skills", "Statistics"],
     "industries": ["Research", "Academia", "Pharma", "Space / Energy"],
     "careers": ["Research Scientist", "Biotechnologist", "Chemist", "Physicist", "Environmental Scientist", "Space Scientist", "Microbiologist", "Geneticist"]},
    # ---------------- SPORTS ----------------
    {"cluster": "Sports & Fitness", "domain": "Sports", "icon": "Dumbbell", "market": 64, "ai_risk": 10, "competition": 86, "difficulty": 80, "growth": "Steady", "salary": (2, 10, 50),
     "degrees": ["B.P.Ed / Sports Science", "Certification + training", "Talent + coaching"], "skills": ["Discipline", "Physical training", "Sport-specific skill", "Mental toughness", "Nutrition", "Strategy"],
     "industries": ["Sports", "Fitness", "Esports", "Wellness"],
     "careers": [("professional_athlete", "Professional Athlete"), "Cricketer", "Sports Coach", "Fitness Trainer", "Sports Physiotherapist", "Esports Player", "Yoga Instructor", "Sports Analyst"]},
    # ---------------- SKILLED TRADES ----------------
    {"cluster": "Skilled Trades", "domain": "Skilled Trades", "icon": "Wrench", "market": 72, "ai_risk": 16, "competition": 45, "difficulty": 50, "growth": "Steady", "salary": (3, 8, 22),
     "degrees": ["ITI / Diploma", "Apprenticeship", "Vocational certification"], "skills": ["Hands-on skill", "Safety", "Tools mastery", "Problem solving", "Precision", "Customer service"],
     "industries": ["Construction", "Manufacturing", "Services", "Automotive"],
     "careers": ["Electrician", "Plumber", "Automobile Technician", "CNC Machinist", "Welder", "Carpenter", "HVAC Technician", "Beautician / Stylist"]},
    # ---------------- HOSPITALITY / AVIATION ----------------
    {"cluster": "Hospitality, Travel & Aviation", "domain": "Hospitality", "icon": "Plane", "market": 70, "ai_risk": 22, "competition": 60, "difficulty": 58, "growth": "Strong", "salary": (3, 11, 35),
     "degrees": ["Hotel Management (IHM)", "Aviation / DGCA (pilot)", "Tourism / Culinary diploma"], "skills": ["Service excellence", "Communication", "Operations", "Domain skill", "Stamina", "Languages"],
     "industries": ["Hospitality", "Aviation", "Tourism", "Food"],
     "careers": [("commercial_pilot", "Commercial Pilot"), "Cabin Crew", "Hotel Manager", "Chef", "Event Manager", "Travel Consultant", "Cruise Staff"]},
]


def _build():
    careers: List[Dict[str, Any]] = []
    for cl in C:
        dom = cl["domain"]
        base_w = cl.get("interests", DOMAIN_INTERESTS.get(dom, {"problem_solving": 0.5}))
        base_t = cl.get("traits", DOMAIN_TRAITS.get(dom, {"analytical": 0.5}))
        e, mid, sen = cl["salary"]
        cluster_titles = []
        for entry in cl["careers"]:
            if isinstance(entry, tuple):
                key, title = entry[0], entry[1]
                ov = entry[2] if len(entry) > 2 else {}
            else:
                title, ov = entry, {}
                key = _slug(title)
            cluster_titles.append(title)
            market = ov.get("market", cl["market"])
            ai = ov.get("ai_risk", cl["ai_risk"])
            comp = ov.get("competition", cl["competition"])
            diff = ov.get("difficulty", cl["difficulty"])
            sal = ov.get("salary", (e, mid, sen))
            skills = ov.get("skills", cl["skills"])
            careers.append({
                "key": key, "title": title, "icon": cl["icon"], "domain": dom, "cluster": cl["cluster"],
                "tagline": ov.get("tagline", f"{title} — a career in {cl['cluster'].lower()}."),
                "w": base_w, "t": base_t,
                "market_demand": market, "salary_score": _salary_score(sal[1]), "competition": comp,
                "ai_risk": ai, "difficulty": diff, "time_to_enter": _time(diff),
                "salary": {"entry": sal[0], "mid": sal[1], "senior": sal[2]},
                "growth": cl["growth"], "growth_forecast": growth_forecast(market),
                "industries": cl.get("industries", [dom]),
                "skills": skills, "degrees": cl["degrees"], "learn_next": skills[:5],
                "_cluster_titles": cluster_titles,  # filled by reference, finalised below
            })
    # finalise related (cluster siblings)
    by_cluster: Dict[str, List[Dict[str, Any]]] = {}
    for c in careers:
        by_cluster.setdefault(c["cluster"], []).append(c)
    for c in careers:
        sibs = [s for s in by_cluster[c["cluster"]] if s["key"] != c["key"]]
        c["related"] = [s["key"] for s in sibs]
        c.pop("_cluster_titles", None)
    return careers


CAREERS: List[Dict[str, Any]] = _build()
CAREER_BY_KEY = {c["key"]: c for c in CAREERS}
_TITLE_INDEX = {c["title"].lower(): c["key"] for c in CAREERS}

# Common phrasings -> canonical key
ALIASES = {
    "game dev": "game_developer", "game developer": "game_developer", "gaming": "game_developer",
    "game programmer": "gameplay_programmer", "game designer": "game_designer",
    "ar vr": "ar_vr_developer", "vr developer": "ar_vr_developer", "metaverse": "ar_vr_developer",
    "swe": "software_engineer", "software developer": "software_engineer", "programmer": "software_engineer", "coder": "software_engineer", "developer": "software_engineer",
    "ai engineer": "ai_ml_engineer", "ml engineer": "ai_ml_engineer", "machine learning": "ai_ml_engineer", "ai": "ai_ml_engineer", "data science": "data_scientist", "ds": "data_scientist",
    "ui ux": "ux_designer", "ux": "ux_designer", "ui ux designer": "ux_designer", "ux designer": "ux_designer", "ui designer": "ui_designer", "product designer": "product_designer", "designer": "graphic_designer",
    "youtuber": "youtuber", "content creator": "content_creator", "influencer": "influencer_creator", "blogger": "content_creator", "writer": "author_novelist", "author": "author_novelist",
    "film director": "filmmaker_director", "director": "filmmaker_director", "actor": "filmmaker_director", "editor": "video_editor", "video editor": "video_editor",
    "singer": "music_producer", "musician": "music_producer", "music": "music_producer", "dj": "music_producer",
    "marketing": "digital_marketer", "digital marketing": "digital_marketer", "social media": "social_media_manager",
    "product manager": "product_manager", "pm": "product_manager", "consultant": "management_consultant", "business analyst": "business_analyst",
    "ca": "chartered_accountant", "chartered accountant": "chartered_accountant", "investment banker": "investment_banker", "banker": "investment_banker", "finance": "financial_analyst", "stock market": "equity_research_analyst", "trader": "equity_research_analyst",
    "entrepreneur": "entrepreneur", "founder": "entrepreneur", "startup": "entrepreneur", "business": "entrepreneur", "businessman": "entrepreneur",
    "doctor": "doctor", "mbbs": "doctor", "surgeon": "surgeon", "dentist": "dentist", "physiotherapist": "physiotherapist", "nurse": "nurse", "psychologist": "psychologist", "psychiatrist": "psychologist", "vet": "veterinarian", "veterinarian": "veterinarian",
    "lawyer": "lawyer", "advocate": "lawyer", "law": "lawyer", "judge": "judge_via_judiciary_exams_", "cs": "company_secretary",
    "ias": "ias_officer", "ias officer": "ias_officer", "ips": "ips_officer", "upsc": "ias_officer", "civil services": "ias_officer", "collector": "ias_officer", "diplomat": "ifs_diplomat", "bank po": "bank_po",
    "army": "army_officer", "soldier": "army_officer", "navy": "navy_officer", "air force": "air_force_pilot", "pilot": "commercial_pilot", "fighter pilot": "air_force_pilot",
    "teacher": "teacher_edtech", "professor": "professor_lecturer", "lecturer": "professor_lecturer",
    "scientist": "research_scientist", "researcher": "research_scientist", "biotech": "biotechnologist", "astronaut": "space_scientist", "isro": "space_scientist",
    "athlete": "professional_athlete", "cricketer": "cricketer", "footballer": "professional_athlete", "sportsman": "professional_athlete", "coach": "sports_coach", "gym trainer": "fitness_trainer", "fitness": "fitness_trainer", "esports": "esports_player", "gamer": "esports_player", "yoga": "yoga_instructor",
    "chef": "chef", "cook": "chef", "electrician": "electrician", "plumber": "plumber", "mechanic": "automobile_technician", "carpenter": "carpenter", "welder": "welder", "beautician": "beautician_stylist", "makeup artist": "beautician_stylist",
    "pilot commercial": "commercial_pilot", "air hostess": "cabin_crew", "cabin crew": "cabin_crew", "hotel manager": "hotel_manager", "event manager": "event_manager",
    "architect": "architect", "interior designer": "interior_designer", "fashion designer": "fashion_designer", "fashion": "fashion_designer",
    "animator": "3d_animator", "animation": "3d_animator", "vfx": "vfx_artist",
    "cyber security": "cybersecurity", "hacker": "ethical_hacker", "ethical hacker": "ethical_hacker", "cloud": "cloud_devops", "devops": "cloud_devops", "data analyst": "data_analyst",
}


def _tokens(s: str):
    return set(re.findall(r"[a-z0-9]+", s.lower())) - {"a", "an", "the", "of", "and", "in", "to", "i", "want", "be", "become", "my", "dream", "is", "as", "for"}


def resolve_career(text: str) -> Tuple[Optional[Dict[str, Any]], float]:
    """Resolve free-text (dream/target/interest) to a career. Returns (career, confidence 0-1)."""
    if not text:
        return None, 0.0
    t = text.strip().lower()
    # 1) exact alias / exact title (highest confidence, beats greedy substrings)
    if t in ALIASES and ALIASES[t] in CAREER_BY_KEY:
        return CAREER_BY_KEY[ALIASES[t]], 1.0
    if t in _TITLE_INDEX:
        return CAREER_BY_KEY[_TITLE_INDEX[t]], 1.0
    # 2) substring alias — prefer the LONGEST matching phrase (avoids 'scientist' eating 'data scientist')
    alias_hits = [(phrase, key) for phrase, key in ALIASES.items() if phrase in t and key in CAREER_BY_KEY]
    if alias_hits:
        phrase, key = max(alias_hits, key=lambda x: len(x[0]))
        return CAREER_BY_KEY[key], 0.95
    # 3) substring title — prefer the longest matching title
    title_hits = [(tl, key) for tl, key in _TITLE_INDEX.items() if t in tl or tl in t]
    if title_hits:
        tl, key = max(title_hits, key=lambda x: len(x[0]))
        return CAREER_BY_KEY[key], 0.9
    # 4) token overlap
    ut = _tokens(t)
    if not ut:
        return None, 0.0
    best, best_score = None, 0.0
    for c in CAREERS:
        ct = _tokens(c["title"]) | _tokens(c["cluster"])
        if not ct:
            continue
        overlap = len(ut & ct) / len(ut | ct)
        if overlap > best_score:
            best, best_score = c, overlap
    if best and best_score >= 0.3:
        return best, round(0.6 + best_score * 0.3, 2)
    return None, 0.0


def related_careers(career: Dict[str, Any], n: int = 7) -> List[Dict[str, Any]]:
    out = [CAREER_BY_KEY[k] for k in career.get("related", []) if k in CAREER_BY_KEY]
    if len(out) < n:  # pad with same-domain careers
        for c in CAREERS:
            if c["domain"] == career["domain"] and c["key"] != career["key"] and c not in out:
                out.append(c)
            if len(out) >= n:
                break
    return out[:n]


def _interest_fit(career: Dict[str, Any], norm: Dict[str, float]) -> float:
    w = career.get("w", {})
    wsum = sum(w.values()) or 1
    return sum(norm.get(k, 0) * wt for k, wt in w.items()) / wsum


def _personality_fit(career: Dict[str, Any], traits: Dict[str, float]) -> float:
    tw = career.get("t", {})
    tsum = sum(tw.values()) or 1
    return sum(traits.get(k, 0) * wt for k, wt in tw.items()) / tsum if tw else 0.5


def dream_match(career, norm, traits, dream_clarity=1.0):
    """Weighted Dream Career Match: dream 25 · interests 25 · aptitude 20 · personality 15 · market 15."""
    interest = _interest_fit(career, norm)
    aptitude = min(1.0, interest * 0.85 + 0.15)  # academic/skill alignment proxy
    personality = _personality_fit(career, traits)
    market = career["market_demand"] / 100.0
    score = 100 * (0.25 * dream_clarity + 0.25 * interest + 0.20 * aptitude + 0.15 * personality + 0.15 * market)
    return int(max(45, min(99, round(score))))


def success_probability(career, norm, traits):
    """Realism of actually achieving it (competition/difficulty/grit aware)."""
    interest = _interest_fit(career, norm)
    aptitude = min(1.0, interest * 0.85 + 0.15)
    grit = (traits.get("stress", 0.5) * 0.5 + traits.get("risk", 0) * 0.3 + traits.get("leadership", 0.5) * 0.2)
    market = career["market_demand"] / 100.0
    s = 100 * (0.35 * aptitude + 0.20 * market + 0.15 * (1 - career["competition"] / 100.0) +
               0.15 * (1 - career["difficulty"] / 100.0) + 0.15 * grit)
    return int(max(28, min(95, round(s))))


# ============================================================
# FUTURE-GOAL ENGINE — pin the user's stated goal (Honesty Rule),
# recommend RELATED careers, never a generic substitute.
# ============================================================
from careers import ai_risk_label  # noqa: E402  (careers never imports career_db → no cycle)


def _verdict(score: int, c: Dict[str, Any]) -> str:
    if score >= 78 and c["ai_risk"] <= 45:
        return "Strong fit — go for it with conviction"
    if score >= 64:
        return "Workable fit — realistic if you commit"
    if score >= 52:
        return "Stretch — possible, but eyes open"
    return "Hard path — achievable, but brutal. Keep a backup running"


def _card(c: Dict[str, Any], score: int) -> Dict[str, Any]:
    """Build a renderer-compatible match card from a career_db career."""
    return {
        "key": c["key"], "title": c["title"], "icon": c["icon"], "tagline": c["tagline"],
        "score": score, "suitability": score,
        "market_demand": c["market_demand"], "salary_score": c["salary_score"],
        "competition": c["competition"], "ai_risk": c["ai_risk"],
        "ai_risk_label": ai_risk_label(c["ai_risk"]), "ai_resistance": 100 - c["ai_risk"],
        "difficulty": c["difficulty"], "time_to_enter": c["time_to_enter"],
        "salary": c["salary"], "salary_mid": c["salary"]["mid"], "growth": c["growth"],
        "industries": c["industries"], "learn_next": c.get("learn_next", []),
        "domain": c["domain"], "cluster": c["cluster"], "skills": c.get("skills", []),
        "degrees": c.get("degrees", []), "verdict": _verdict(score, c),
    }


def fit_score(c: Dict[str, Any], norm: Dict[str, float], traits: Dict[str, float]) -> int:
    """General best-fit score (no dream component) — used to rank related/overall careers."""
    interest = _interest_fit(c, norm)
    aptitude = min(1.0, interest * 0.85 + 0.15)
    personality = _personality_fit(c, traits)
    market = c["market_demand"] / 100.0
    return int(max(40, min(98, round(100 * (0.34 * interest + 0.26 * aptitude + 0.20 * personality + 0.20 * market)))))


def rank_all(norm: Dict[str, float], traits: Dict[str, float], n: int = 6, exclude=None):
    exclude = exclude or set()
    scored = [(c, fit_score(c, norm, traits)) for c in CAREERS if c["key"] not in exclude]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:n]


def challenges_for(c, dscore, success, norm, traits) -> List[str]:
    """Honesty Rule: brutal-but-specific challenges of chasing THIS career."""
    out = []
    if c["competition"] >= 78:
        out.append(f"Brutal competition ({c['competition']}/100) — only consistent top performers break in.")
    if c["difficulty"] >= 78:
        out.append(f"Steep difficulty ({c['difficulty']}/100) — expect {c['time_to_enter']} of serious effort before real traction.")
    if _interest_fit(c, norm) < 0.5:
        out.append("Your current subjects/interests don't strongly point here yet — you'll build from a weaker base.")
    if c.get("t") and _personality_fit(c, traits) < 0.45:
        out.append("Your personality profile isn't a natural match — doable, but it will cost you more energy.")
    if success < 55:
        out.append(f"Realistic success probability is {success}% — high risk, so run a backup in parallel.")
    if c["ai_risk"] >= 55:
        out.append(f"{ai_risk_label(c['ai_risk'])} of AI disruption — you must own the AI-proof edge of this field.")
    if c["salary"]["entry"] <= 3:
        out.append(f"Low early pay (~₹{c['salary']['entry']} LPA to start) — plan finances for a slow ramp.")
    if not out:
        out.append("You're well-aligned — the real risk now is hesitation. Commit and start building proof.")
    return out[:4]


def avoid_block(norm, traits, exclude_keys, limit: int = 4):
    exclude_keys = exclude_keys or set()
    scored = []
    for c in CAREERS:
        if c["key"] in exclude_keys:
            continue
        suit = fit_score(c, norm, traits)
        avoid_score = (100 - suit) * 0.4 + c["ai_risk"] * 0.35 + c["competition"] * 0.1 + (100 - c["market_demand"]) * 0.15
        scored.append((c, suit, avoid_score))
    scored.sort(key=lambda x: x[2], reverse=True)
    out = []
    for c, suit, _ in scored[:limit]:
        reasons = []
        if c["ai_risk"] >= 55:
            reasons.append(f"{ai_risk_label(c['ai_risk'])} — automation is shrinking this field")
        if suit < 55:
            reasons.append("weak alignment with your strengths")
        if c["competition"] >= 80:
            reasons.append("brutal competition for limited seats")
        if c["market_demand"] <= 55:
            reasons.append("soft / declining demand")
        if not reasons:
            reasons.append("better-aligned options exist for your profile")
        out.append({"title": c["title"], "icon": c["icon"], "ai_risk": c["ai_risk"],
                    "ai_risk_label": ai_risk_label(c["ai_risk"]), "market_demand": c["market_demand"],
                    "competition": c["competition"], "suitability": suit, "why": reasons[:2]})
    return out


def goal_block(goal_text: str, norm: Dict[str, float], traits: Dict[str, float], n_related: int = 3) -> Dict[str, Any]:
    """Future-Goal engine. Resolves the user's stated goal/dream, KEEPS it as #1
    (Honesty Rule — never substituted), adds related cluster careers as backups,
    and an honest challenges read. Falls back to best-fit ranking if unresolved."""
    career, conf = resolve_career(goal_text or "")
    if not career:
        ranked = rank_all(norm, traits, 5)
        cards = [_card(c, s) for c, s in ranked]
        return {"resolved": False, "goal_text": (goal_text or "").strip(),
                "dream": cards[0] if cards else None, "dream_score": cards[0]["score"] if cards else 0,
                "success_probability": None, "matches": cards, "related": cards[1:4],
                "challenges": [], "exclude": {c["key"] for c, _ in ranked}}
    dscore = dream_match(career, norm, traits, dream_clarity=max(conf, 0.85))
    success = success_probability(career, norm, traits)
    dream = _card(career, dscore)
    dream["is_dream"] = True
    dream["success_probability"] = success
    rel = related_careers(career, 7)
    rel_scored = sorted([(c, fit_score(c, norm, traits)) for c in rel], key=lambda x: x[1], reverse=True)
    related = [_card(c, s) for c, s in rel_scored[:n_related]]
    exclude = {career["key"]} | {r["key"] for r in related}
    return {"resolved": True, "goal_text": (goal_text or "").strip(), "career_title": career["title"],
            "dream": dream, "dream_score": dscore, "success_probability": success,
            "matches": [dream] + related, "related": related,
            "challenges": challenges_for(career, dscore, success, norm, traits), "exclude": exclude}
