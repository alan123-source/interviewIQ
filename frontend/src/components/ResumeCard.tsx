"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import type { Resume } from "@/types/resume";
import {useRouter} from "next/navigation";
import {deleteResume} from "@/services/resume.service";

type ResumeCardProps = {
    resume: Resume;
    onDelete:(resumeId:number)=>void;
};

export default function ResumeCard({ resume ,onDelete}: ResumeCardProps) {
    
    const router=useRouter();


    const handleDelete=async()=>{

    
            const confirmed=window.confirm(
                "Are you sure you want to delete this resume?"
            );
            if(!confirmed){
                return;
            }

            try{
                await deleteResume(resume.id);
                onDelete(resume.id)

            }catch(error){
                if(error instanceof Error){
                    window.alert(error.message);

                }else{
                    window.alert("Falied to delete resume")
                }
            }
    }
    
    return (
        <Card>
            <CardHeader>
                <CardTitle>
                    {resume.original_filename}
                </CardTitle>
            </CardHeader>

            <CardContent>
                <p className="text-sm text-muted-foreground">
                    Status: {resume.status}
                </p>

                <p className="text-sm text-muted-foreground mt-2">
                    Uploaded:{" "}
                    {new Date(resume.created_at).toLocaleDateString()}
                </p>

                <div className="flex gap-3 mt-4">
                    <Button 
                       onClick={()=>router.push(`/resumes/${resume.id}`)}
                    >
                        View Resume
                    </Button>

                    <Button variant="outline"
                      onClick={handleDelete}
                    >
                        Delete
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}