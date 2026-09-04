from pydantic import BaseModel
from typing import List, Optional


class PersonalInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None


class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    start_year: Optional[str] = None
    end_year: Optional[str] = None
    grade: Optional[str] = None


class Experience(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: List[str] = []


class Project(BaseModel):
    name: Optional[str] = None
    technologies: List[str] = []
    description: List[str] = []


class ResumeAIData(BaseModel):
    personal_info: PersonalInfo
    summary: Optional[str] = None

    technical_skills: List[str] = []
    tools: List[str] = []
    concepts: List[str] = []

    education: List[Education] = []
    experience: List[Experience] = []
    projects: List[Project] = []

    certifications: List[str] = []
    achievements: List[str] = []