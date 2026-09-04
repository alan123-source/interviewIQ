import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

from app.schemas.resume import ResumeAIData

from app.services.skill_service import normalize_skills

from pydantic import ValidationError


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def analyze_resume(resume_text: str) -> ResumeAIData:

    prompt = f"""
You are an expert resume information extraction system.

Analyze the following resume and extract the information
into the required structured format.

Rules:

1. Only extract information explicitly present in the resume.
2. Do not invent or assume information.
3. If information is missing, use null or an empty list.
4. Separate technical skills, tools, and concepts.
5. Preserve the meaning of the original resume.
6. technical_skills must contain programming languages,
   frameworks, libraries, databases, and other technical
   technologies explicitly mentioned in the resume.
7. tools must contain development tools, platforms, and
   software tools explicitly mentioned in the resume.
8. concepts must contain technical concepts, methodologies,
   or technical areas such as OOP, DSA, REST APIs,
   authentication, authorization, and microservices.
9. Do not put soft skills such as communication, leadership,
   teamwork, problem solving, adaptability, time management,
   or attention to detail into technical_skills, tools, or concepts.
10. Do not create a separate category for soft skills.
11. A skill should only appear in one of the three categories.

Resume:

{resume_text}
"""

    max_attempts = 3

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ResumeAIData,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True
                    ),
                ),
            )

            result=ResumeAIData.model_validate_json(
                response.text
            )

            result.technical_skills=normalize_skills(
                result.technical_skills
            )

            result.tools=normalize_skills(
                result.tools
            )

            result.concepts=normalize_skills(
                result.concepts
            )

            return result

        except errors.ServerError as exc:

            # Retry temporary Gemini 503 errors
            if attempt == max_attempts - 1:
                raise RuntimeError(
                    "Gemini service is temporarily unavailable"
                ) from exc

            wait_time = 2 ** attempt

            print(
                f"Gemini unavailable. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

        except ValidationError as exc:

            print(f"Resume AI validation failed:{exc}")

            raise RuntimeError(
                "Gemini returned invalid resume data"
            ) from exc
        except Exception as exc:
            raise RuntimeError(
                "Falied to analayze resume"
            ) from exc

    raise RuntimeError("Resume analysis failed")