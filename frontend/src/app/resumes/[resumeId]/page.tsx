"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import { getResume } from "@/services/resume.service";
import type { Resume } from "@/types/resume";

import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function ResumeDetailsPage() {
    const params = useParams();
    const router = useRouter();

    const [resume, setResume] = useState<Resume | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const resumeId = Number(params.resumeId);

        if (!resumeId) {
            setError("Invalid resume ID");
            setLoading(false);
            return;
        }

        getResume(resumeId)
            .then((data) => {
                setResume(data);
            })
            .catch((error) => {
                if (error instanceof Error) {
                    setError(error.message);
                } else {
                    setError("Failed to load resume");
                }
            })
            .finally(() => {
                setLoading(false);
            });
    }, [params.resumeId]);

    if (loading) {
        return (
            <main className="p-10">
                <p>Loading resume...</p>
            </main>
        );
    }

    if (error) {
        return (
            <main className="p-10">
                <p className="text-destructive">
                    {error}
                </p>
            </main>
        );
    }

    if (!resume) {
        return null;
    }

    const analysis = resume.ai_analysis;

    if (!analysis) {
        return (
            <main className="p-10">
                <Button
                    variant="outline"
                    onClick={() => router.back()}
                >
                    ← Back
                </Button>

                <Card className="mt-6">
                    <CardHeader>
                        <CardTitle>
                            Resume Analysis
                        </CardTitle>
                    </CardHeader>

                    <CardContent>
                        <p className="text-muted-foreground">
                            AI analysis is not available for this resume.
                        </p>
                    </CardContent>
                </Card>
            </main>
        );
    }

    return (
        <main className="p-6 md:p-10 space-y-6">

            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold">
                        {analysis.personal_info.name ?? "Resume"}
                    </h1>

                    <p className="text-muted-foreground mt-1">
                        {resume.original_filename}
                    </p>
                </div>

                <Button
                    variant="outline"
                    onClick={() => router.back()}
                >
                    ← Back
                </Button>
            </div>

            {/* Personal Information */}
            <Card>
                <CardHeader>
                    <CardTitle>
                        Personal Information
                    </CardTitle>
                </CardHeader>

                <CardContent className="space-y-2">
                    <p>
                        <strong>Email:</strong>{" "}
                        {analysis.personal_info.email ?? "Not provided"}
                    </p>

                    <p>
                        <strong>Phone:</strong>{" "}
                        {analysis.personal_info.phone ?? "Not provided"}
                    </p>

                    <p>
                        <strong>LinkedIn:</strong>{" "}
                        {analysis.personal_info.linkedin ?? "Not provided"}
                    </p>

                    <p>
                        <strong>GitHub:</strong>{" "}
                        {analysis.personal_info.github ?? "Not provided"}
                    </p>

                    <p>
                        <strong>Portfolio:</strong>{" "}
                        {analysis.personal_info.portfolio ?? "Not provided"}
                    </p>
                </CardContent>
            </Card>

            {/* Summary */}
            <Card>
                <CardHeader>
                    <CardTitle>
                        Professional Summary
                    </CardTitle>
                </CardHeader>

                <CardContent>
                    <p className="text-muted-foreground">
                        {analysis.summary ?? "No summary provided."}
                    </p>
                </CardContent>
            </Card>

            {/* Technical Skills */}
            <Card>
                <CardHeader>
                    <CardTitle>
                        Technical Skills
                    </CardTitle>
                </CardHeader>

                <CardContent>
                    {analysis.technical_skills.length > 0 ? (
                        <div className="flex flex-wrap gap-2">
                            {analysis.technical_skills.map((skill) => (
                                <span
                                    key={skill}
                                    className="rounded-md border px-3 py-1 text-sm"
                                >
                                    {skill}
                                </span>
                            ))}
                        </div>
                    ) : (
                        <p className="text-muted-foreground">
                            No technical skills listed.
                        </p>
                    )}
                </CardContent>
            </Card>

            {/* Tools */}
            <Card>
                <CardHeader>
                    <CardTitle>
                        Tools
                    </CardTitle>
                </CardHeader>

                <CardContent>
                    {analysis.tools.length > 0 ? (
                        <div className="flex flex-wrap gap-2">
                            {analysis.tools.map((tool) => (
                                <span
                                    key={tool}
                                    className="rounded-md border px-3 py-1 text-sm"
                                >
                                    {tool}
                                </span>
                            ))}
                        </div>
                    ) : (
                        <p className="text-muted-foreground">
                            No tools listed.
                        </p>
                    )}
                </CardContent>
            </Card>

            {/* Concepts */}
            <Card>
                <CardHeader>
                    <CardTitle>
                        Concepts
                    </CardTitle>
                </CardHeader>

                <CardContent>
                    {analysis.concepts.length > 0 ? (
                        <div className="flex flex-wrap gap-2">
                            {analysis.concepts.map((concept) => (
                                <span
                                    key={concept}
                                    className="rounded-md border px-3 py-1 text-sm"
                                >
                                    {concept}
                                </span>
                            ))}
                        </div>
                    ) : (
                        <p className="text-muted-foreground">
                            No concepts listed.
                        </p>
                    )}
                </CardContent>
            </Card>

            {/* Education */}
            <Card>
                <CardHeader>
                    <CardTitle>
                        Education
                    </CardTitle>
                </CardHeader>

                <CardContent>
                    {analysis.education.length > 0 ? (
                        <div className="space-y-5">
                            {analysis.education.map((education, index) => (
                                <div key={index}>
                                    <h3 className="font-semibold">
                                        {education.degree ?? "Degree not provided"}
                                    </h3>

                                    <p className="text-muted-foreground">
                                        {education.institution ?? "Institution not provided"}
                                    </p>

                                    <p className="text-sm mt-1">
                                        {education.start_year ?? "?"} -{" "}
                                        {education.end_year ?? "?"}
                                    </p>

                                    <p className="text-sm">
                                        Grade: {education.grade ?? "Not provided"}
                                    </p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-muted-foreground">
                            No education information listed.
                        </p>
                    )}
                </CardContent>
            </Card>

            {/* Experience */}
            <Card>
                <CardHeader>
                    <CardTitle>
                        Experience
                    </CardTitle>
                </CardHeader>

                <CardContent>
                    {analysis.experience.length > 0 ? (
                        <div className="space-y-5">
                            {analysis.experience.map((experience, index) => (
                                <div key={index}>
                                    <h3 className="font-semibold">
                                        {experience.role ?? "Role not provided"}
                                    </h3>

                                    <p className="text-muted-foreground">
                                        {experience.company ?? "Company not provided"}
                                    </p>

                                    {experience.description &&
                                        experience.description.length > 0 && (
                                            <ul className="list-disc pl-5 mt-2 space-y-1">
                                                {experience.description.map(
                                                    (description, descriptionIndex) => (
                                                        <li key={descriptionIndex}>
                                                            {description}
                                                        </li>
                                                    )
                                                )}
                                            </ul>
                                        )}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-muted-foreground">
                            No experience listed.
                        </p>
                    )}
                </CardContent>
            </Card>

            {/* Projects */}
            <Card>
                <CardHeader>
                    <CardTitle>
                        Projects
                    </CardTitle>
                </CardHeader>

                <CardContent>
                    {analysis.projects.length > 0 ? (
                        <div className="space-y-6">
                            {analysis.projects.map((project, index) => (
                                <div key={index}>
                                    <h3 className="font-semibold text-lg">
                                        {project.name}
                                    </h3>

                                    {project.technologies.length > 0 && (
                                        <div className="flex flex-wrap gap-2 mt-2">
                                            {project.technologies.map(
                                                (technology) => (
                                                    <span
                                                        key={technology}
                                                        className="rounded-md border px-2 py-1 text-xs"
                                                    >
                                                        {technology}
                                                    </span>
                                                )
                                            )}
                                        </div>
                                    )}

                                    {project.description.length > 0 && (
                                        <ul className="list-disc pl-5 mt-3 space-y-1">
                                            {project.description.map(
                                                (description, descriptionIndex) => (
                                                    <li key={descriptionIndex}>
                                                        {description}
                                                    </li>
                                                )
                                            )}
                                        </ul>
                                    )}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-muted-foreground">
                            No projects listed.
                        </p>
                    )}
                </CardContent>
            </Card>

            {/* Certifications */}
            <Card>
                <CardHeader>
                    <CardTitle>
                        Certifications
                    </CardTitle>
                </CardHeader>

                <CardContent>
                    {analysis.certifications.length > 0 ? (
                        <ul className="list-disc pl-5 space-y-1">
                            {analysis.certifications.map(
                                (certification) => (
                                    <li key={certification}>
                                        {certification}
                                    </li>
                                )
                            )}
                        </ul>
                    ) : (
                        <p className="text-muted-foreground">
                            No certifications listed.
                        </p>
                    )}
                </CardContent>
            </Card>

            {/* Achievements */}
            <Card>
                <CardHeader>
                    <CardTitle>
                        Achievements
                    </CardTitle>
                </CardHeader>

                <CardContent>
                    {analysis.achievements.length > 0 ? (
                        <ul className="list-disc pl-5 space-y-1">
                            {analysis.achievements.map(
                                (achievement) => (
                                    <li key={achievement}>
                                        {achievement}
                                    </li>
                                )
                            )}
                        </ul>
                    ) : (
                        <p className="text-muted-foreground">
                            No achievements listed.
                        </p>
                    )}
                </CardContent>
            </Card>

        </main>
    );
}