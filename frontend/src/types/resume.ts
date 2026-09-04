export type PersonalInfo = {
    name: string | null;
    email: string | null;
    phone: string | null;
    linkedin: string | null;
    github: string | null;
    portfolio: string | null;
};

export type Education = {
    degree: string | null;
    institution: string | null;
    start_year: string | null;
    end_year: string | null;
    grade: string | null;
};

export type Experience = {
    company?: string | null;
    role?: string | null;
    start_year?: string | null;
    end_year?: string | null;
    description?: string[];
};

export type Project = {
    name: string;
    technologies: string[];
    description: string[];
};

export type ResumeAIData = {
    personal_info: PersonalInfo;
    summary: string | null;

    technical_skills: string[];
    tools: string[];
    concepts: string[];

    education: Education[];
    experience: Experience[];
    projects: Project[];

    certifications: string[];
    achievements: string[];
};

export type Resume = {
    id: number;
    user_id: number;
    original_filename: string;
    file_path: string;
    extracted_text: string;
    ai_analysis: ResumeAIData | null;
    status: string;
    created_at: string;
    updated_at: string;
};