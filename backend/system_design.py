"""Curated System Design Roadmap (MapMyCareer V2 — IT Employee engine).

A fixed, premium L1→L4 syllabus with learning order, courses, books, projects and
practice resources. Deterministic (same high-quality content for every IT user),
lightly framed by experience. Returned as `blueprint`-type section items.
"""
from typing import Dict, Any, List

COURSES = ["Grokking the System Design Interview (Educative)", "ByteByteGo — System Design (Alex Xu)",
           "MIT 6.824 Distributed Systems (free)", "Gaurav Sen — System Design (YouTube)",
           "freeCodeCamp System Design (YouTube)"]
BOOKS = ["Designing Data-Intensive Applications — Martin Kleppmann", "System Design Interview Vol 1 & 2 — Alex Xu",
         "Understanding Distributed Systems — Roberto Vitillo", "Site Reliability Engineering — Google (free)"]
PRACTICE = ["ByteByteGo newsletter", "High Scalability blog", "Engineering blogs (Netflix, Uber, Stripe)",
            "Mock interviews on Pramp / Excalidraw diagrams"]

LEVELS: List[Dict[str, Any]] = [
    {
        "phase": "Level 1 — Foundations",
        "focus": "The building blocks. Master these before touching design questions.",
        "groups": [
            {"label": "Learn in order", "items": ["Computer Networks (HTTP, TCP/IP, DNS)", "Operating Systems (processes, threads, memory)",
                                                   "Databases (SQL vs NoSQL, indexing, transactions)", "Caching (Redis, cache strategies, invalidation)",
                                                   "Load Balancing (L4/L7, algorithms)", "CAP Theorem & consistency models"]},
            {"label": "Courses", "items": [COURSES[1], COURSES[4]]},
            {"label": "Books", "items": [BOOKS[0]]},
            {"label": "Practice", "items": ["Diagram each concept from memory", "Explain CAP with a real example"]},
        ],
    },
    {
        "phase": "Level 2 — Design Core Systems",
        "focus": "Apply the foundations by designing real, commonly-asked systems end-to-end.",
        "groups": [
            {"label": "Build / design", "items": ["URL Shortener", "Chat System (WhatsApp-lite)", "Notification System",
                                                   "File Storage System (Dropbox-lite)", "Rate Limiter"]},
            {"label": "For each design", "items": ["Requirements → capacity estimate → API → data model → scaling", "Identify bottlenecks & trade-offs"]},
            {"label": "Resources", "items": [COURSES[0], COURSES[3]]},
            {"label": "Books", "items": [BOOKS[1]]},
        ],
    },
    {
        "phase": "Level 3 — Distributed Systems",
        "focus": "Scale beyond one machine. This is where mid→senior engineers separate.",
        "groups": [
            {"label": "Learn in order", "items": ["Distributed Systems fundamentals", "Microservices & service boundaries",
                                                  "Kafka & message queues", "Event-Driven Architecture", "Scalability patterns (sharding, replication)"]},
            {"label": "Courses", "items": [COURSES[2]]},
            {"label": "Books", "items": [BOOKS[2], BOOKS[0]]},
            {"label": "Projects", "items": ["Build an event-driven service with Kafka", "Shard a database & measure it"]},
        ],
    },
    {
        "phase": "Level 4 — Senior / Architect",
        "focus": "Own systems end-to-end. Judgement, reliability and security — what AI can't replace.",
        "groups": [
            {"label": "Master", "items": ["Architecture Design (trade-off driven)", "High Availability & disaster recovery",
                                          "Observability (logs, metrics, traces)", "Security (authN/authZ, threat modelling)"]},
            {"label": "Resources", "items": [BOOKS[3], PRACTICE[2]]},
            {"label": "Practice", "items": PRACTICE[:2] + [PRACTICE[3]]},
            {"label": "Projects", "items": ["Design a system for 10M users with an HA plan", "Add full observability + a security review"]},
        ],
    },
]


def system_design_blueprint(experience: float = 3, sysd_level: int = 30) -> List[Dict[str, Any]]:
    """Return the L1→L4 roadmap, with a focus note tuned to where the user should start."""
    items = [dict(lvl) for lvl in LEVELS]
    if sysd_level >= 60 or experience >= 7:
        items[0]["focus"] = "You likely know most basics — speed-review, then spend your energy on Levels 3–4."
    elif sysd_level <= 30 and experience <= 3:
        items[0]["focus"] = "Start here, seriously. Don't jump to design questions until these are solid."
    return items
