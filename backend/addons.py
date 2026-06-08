"""Post-purchase add-on deliverables (Resume / LinkedIn / Interview).

Each add-on produces a real, personalized report built deterministically from the
user's existing blueprint — fast, reliable and genuinely useful. The "bundle" grants
all three component deliverables.
"""
from typing import Dict, Any, List

ADDON_CATALOG: Dict[str, Dict[str, Any]] = {
    "resume": {"id": "resume", "title": "Resume Optimization Report", "price": 299},
    "linkedin": {"id": "linkedin", "title": "LinkedIn Optimization Report", "price": 299},
    "interview": {"id": "interview", "title": "Interview Preparation Blueprint", "price": 499},
    "bundle": {"id": "bundle", "title": "Complete Career Transformation Bundle", "price": 999,
               "includes": ["resume", "linkedin", "interview"]},
}

COMPONENT_IDS = ["resume", "linkedin", "interview"]


def normalize_ids(ids: List[str]) -> List[str]:
    """If bundle is selected, it supersedes everything else."""
    ids = [i for i in ids if i in ADDON_CATALOG]
    if "bundle" in ids:
        return ["bundle"]
    seen, out = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i)
            out.append(i)
    return out


def expand_addons(ids: List[str]) -> List[str]:
    """Expand selected ids into the concrete component deliverables to grant."""
    out: List[str] = []
    for i in normalize_ids(ids):
        item = ADDON_CATALOG.get(i, {})
        out.extend(item.get("includes", [i]))
    seen, res = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


def addon_total(ids: List[str]) -> int:
    return sum(ADDON_CATALOG[i]["price"] for i in normalize_ids(ids))


# ----------------------- Content builders -----------------------
def _top_title(r: Dict[str, Any]) -> str:
    return (r.get("matches") or [{}])[0].get("title", "your target role")


def _resume(sub: Dict[str, Any]) -> Dict[str, Any]:
    r = sub["report"]
    top = _top_title(r)
    name = sub.get("name", "You").split(" ")[0]
    learn = r.get("learn_next", []) or []
    skills_raw = (sub.get("professional") or {}).get("skills") or ""
    keywords = list(dict.fromkeys(learn + [s.strip() for s in skills_raw.split(",") if s.strip()]))[:12]
    traits = [t.lower() for t in (r.get("trait_labels") or ["analytical"])[:2]]
    return {
        "title": "Resume Optimization Report",
        "subtitle": f"ATS-ready resume strategy targeting {top}",
        "intro": (f"{name}, recruiters spend roughly 7 seconds on the first scan and ATS software filters out "
                  f"~70% of resumes before a human ever sees them. This report rebuilds your resume around "
                  f"measurable impact and the exact keywords for a {top} role — no fluff, just what gets interviews."),
        "sections": [
            {"heading": "Professional Summary (copy & adapt)", "type": "para",
             "text": (f"{top} candidate with a track record of &lt;impact&gt;. Combines {', '.join(traits)} strengths "
                      f"with hands-on {', '.join(learn[:2]) if learn else 'core technical'} skills. Seeking to drive "
                      f"&lt;specific outcome&gt; at &lt;target company type&gt;.")},
            {"heading": "High-Impact Bullet Formula", "type": "list", "items": [
                "Use: [Action verb] + [what you did] + [measurable result]. e.g. 'Cut processing time 40% by automating X'.",
                "Lead every bullet with a strong verb: Built, Led, Reduced, Launched, Automated, Increased.",
                "Quantify everything — %, \u20b9, time saved, users, scale. Numbers beat adjectives.",
                "Show outcomes, not duties. 'Responsible for X' becomes 'Delivered X resulting in Y'.",
                "Mirror the job description's language for the top 3 responsibilities.",
                "One line per bullet; cut filler ('responsible for', 'helped with')."]},
            {"heading": "ATS Keywords To Include", "type": "list",
             "items": keywords or ["Pull the exact tools and skills named in the job post and weave them in naturally."]},
            {"heading": "Formatting Rules That Pass ATS", "type": "list", "items": [
                "Single column, standard fonts (Calibri/Arial 10\u201312pt). No tables, text boxes or images.",
                "Standard headers: Summary, Experience, Skills, Education, Projects.",
                "Submit as .pdf unless the portal explicitly asks for .docx.",
                "Put your strongest, most relevant experience in the top third of page one.",
                "1 page if under 8 years' experience; 2 pages maximum beyond that."]},
            {"heading": "Mistakes Quietly Killing Your Resume", "type": "list", "items": [
                "A generic objective instead of a targeted summary.",
                "Listing responsibilities with zero metrics.",
                "One resume for every job \u2014 always tailor the top third.",
                "Buzzwords without proof ('hard-working', 'team player').",
                "Typos and inconsistent tense \u2014 an instant credibility killer."]},
        ],
    }


def _linkedin(sub: Dict[str, Any]) -> Dict[str, Any]:
    r = sub["report"]
    top = _top_title(r)
    name = sub.get("name", "You").split(" ")[0]
    learn = r.get("learn_next", []) or []
    return {
        "title": "LinkedIn Optimization Report",
        "subtitle": f"Turn your profile into an inbound-opportunity magnet for {top}",
        "intro": (f"{name}, 87% of recruiters vet candidates on LinkedIn. A keyword-optimized profile gets you "
                  f"found for {top} roles even while you sleep. Here is the exact rewrite and visibility plan."),
        "sections": [
            {"heading": "Headline Formula", "type": "para",
             "text": (f"&lt;Role&gt; | helping &lt;who&gt; achieve &lt;result&gt; with &lt;skills&gt;. Example: "
                      f"'{top} | Building reliable systems with {', '.join(learn[:2]) if learn else 'modern tooling'}'. "
                      f"Use all 220 characters \u2014 never just your job title.")},
            {"heading": "About Section (rewrite template)", "type": "para",
             "text": (f"Line 1 hook: the problem you solve. Lines 2\u20133: proof (numbers, wins). Line 4: your stack "
                      f"({', '.join(learn[:4]) if learn else 'your core skills'}). Final line: a clear CTA "
                      f"('Open to {top} roles \u2014 DM me').")},
            {"heading": "Skills To List (most in-demand first)", "type": "list",
             "items": learn[:10] or ["Add the 10 most in-demand skills for your target role, strongest first."]},
            {"heading": "Profile Completeness Checklist", "type": "list", "items": [
                "Professional headshot \u2014 profiles with photos get 21x more views.",
                "Custom banner that states your value proposition.",
                "Custom URL (linkedin.com/in/yourname).",
                "Featured section with your best project, article or portfolio.",
                "Turn on 'Open to Work' (recruiters-only mode if currently employed)."]},
            {"heading": "4-Week Visibility Plan", "type": "list", "items": [
                "Week 1: Rewrite headline + About + skills. Request 3 recommendations.",
                "Week 2: Post 2 short insights. Comment thoughtfully on 5 industry posts a day.",
                "Week 3: Publish a 'what I learned' post with a result. Connect with 20 target-company people.",
                "Week 4: Share a project/case study. Message 5 recruiters with a tailored note."]},
        ],
    }


def _interview(sub: Dict[str, Any]) -> Dict[str, Any]:
    r = sub["report"]
    top = _top_title(r)
    name = sub.get("name", "You").split(" ")[0]
    learn = r.get("learn_next", []) or []
    return {
        "title": "Interview Preparation Blueprint",
        "subtitle": f"Walk into your {top} interview ready for anything",
        "intro": (f"{name}, most candidates lose offers not on skill but on unstructured answers. This blueprint "
                  f"gives you the likely questions, a proven story framework and the prep checklist for {top}."),
        "sections": [
            {"heading": "12 Questions You Will Likely Face", "type": "list", "items": [
                "Tell me about yourself (90 seconds, role-focused).",
                "Why this role and why now?",
                "Walk me through a project you're proud of.",
                "Describe a time you failed and what you learned.",
                "How do you handle conflict on a team?",
                "Tell me about a tight deadline you delivered under.",
                "A hard decision you made with incomplete information.",
                "Where do you want to be in 3 years?",
                "Your biggest weakness \u2014 and how you're fixing it.",
                f"A role-specific question on {', '.join(learn[:2]) if learn else 'your core skills'}.",
                "A time you influenced someone without authority.",
                "Why should we hire you over other candidates?"]},
            {"heading": "The STAR Framework (use for every behavioral answer)", "type": "para",
             "text": ("Situation: set the scene in 1\u20132 lines. Task: your specific responsibility. Action: what YOU "
                      "did (most detail here). Result: the measurable outcome. Prepare 3 STAR stories you can flex.")},
            {"heading": "3 Stories To Prepare Now", "type": "list", "items": [
                "A win where you drove a measurable result.",
                "A conflict or failure and what you changed afterward.",
                "A time you learned something hard, fast."]},
            {"heading": "Technical Prep Checklist", "type": "list",
             "items": learn[:8] or ["Revise the core concepts and tools for your target role."]},
            {"heading": "Smart Questions To Ask Them", "type": "list", "items": [
                "What does success look like in the first 90 days?",
                "What's the biggest challenge the team faces right now?",
                "How is performance measured for this role?",
                "What's the growth path from here?"]},
            {"heading": "Red Flags That Cost Offers", "type": "list", "items": [
                "Rambling answers with no structure (use STAR).",
                "Badmouthing a previous employer.",
                "Having no questions for the interviewer.",
                "Vague answers with zero metrics or specifics.",
                "Not researching the company or role beforehand."]},
        ],
    }


_BUILDERS = {"resume": _resume, "linkedin": _linkedin, "interview": _interview}


def build_addon_content(component_id: str, sub: Dict[str, Any]) -> Dict[str, Any]:
    fn = _BUILDERS.get(component_id)
    return fn(sub) if fn else {}
