from app.services.skill_service import normalize_skills


skills = [
    "Python",
    "python",
    "JS",
    "JavaScript",
    "React",
    "React.js",
    "ReactJS",
    "Postgres",
    "PostgreSQL",
]

result = normalize_skills(skills)

print(result)