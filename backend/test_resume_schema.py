from app.schemas.resume import ResumeAIData
from pydantic import ValidationError


valid_data = {
    "personal_info": {
        "name": "Alan Paul John",
        "email": "alan@example.com",
        "phone": "1234567890",
        "linkedin": None,
        "github": None,
        "portfolio": None,
    },
    "technical_skills": ["Python", "React"],
    "tools": ["Git", "Docker"],
    "concepts": ["REST API"],
}


# Test 1 — Valid data
print("TEST 1: Valid data")

try:
    result = ResumeAIData.model_validate(valid_data)
    print("✅ Validation passed")

except ValidationError as e:
    print("❌ Validation failed")
    print(e)


# Test 2 — Wrong type for technical_skills
print("\nTEST 2: Invalid technical_skills")

invalid_data = valid_data.copy()

invalid_data["technical_skills"] = "Python, React"

try:
    result = ResumeAIData.model_validate(invalid_data)
    print("❌ Invalid data was accepted")

except ValidationError:
    print("✅ Invalid data was rejected")


# Test 3 — Wrong type for tools
print("\nTEST 3: Invalid tools")

invalid_data = valid_data.copy()

invalid_data["tools"] = "Docker, Git"

try:
    result = ResumeAIData.model_validate(invalid_data)
    print("❌ Invalid data was accepted")

except ValidationError:
    print("✅ Invalid data was rejected")