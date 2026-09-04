from typing import List


SKILL_ALIASES = {
    # Programming languages
    "js": "JavaScript",
    "javascript": "JavaScript",
    "py": "Python",
    "python": "Python",
    "ts": "TypeScript",
    "typescript": "TypeScript",

    # Frontend
    "reactjs": "React",
    "react.js": "React",
    "react": "React",

    "nextjs": "Next.js",
    "next.js": "Next.js",

    # Backend
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "node": "Node.js",

    "expressjs": "Express.js",
    "express.js": "Express.js",

    # Databases
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "postgresql db": "PostgreSQL",

    "mongo": "MongoDB",
    "mongodb": "MongoDB",

    # Tools
    "git": "Git",
    "github": "GitHub",
    "git/github": "Git/GitHub",

    # Concepts
    "rest": "REST API",
    "rest api": "REST API",
    "rest apis": "REST API",
}

def normalize_skill(skill: str) -> str:
    cleaned = skill.strip()

    if not cleaned:
        return ""

    key = cleaned.lower()

    return SKILL_ALIASES.get(key, cleaned)

def normalize_skills(skills: List[str]) -> List[str]:
    normalized = []

    seen = set()

    for skill in skills:

        normalized_skill = normalize_skill(skill)

        if not normalized_skill:
            continue

        key = normalized_skill.lower()

        if key in seen:
            continue
        seen.add(key)
        normalized.append(normalized_skill)

    return normalized
