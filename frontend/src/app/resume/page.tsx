"use client";

import {useState} from "react";
import {useRouter} from "next/navigation";
import {Button} from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle

} from "@/components/ui/card";
import {Input} from "@/components/ui/input";
import {uploadResume} from "@/services/resume.service";


export default function ResumePage() {

    const router=useRouter();
    const [file,setFile]=useState<File |null>(null);
    const [error,setError]=useState("");
    const [uploading,setUploading]=useState(false)

    
    const handleFileChange=(
        event:React.ChangeEvent<HTMLInputElement>
    )=>{
        const selectedFile=event.target.files?.[0];
        if(!selectedFile) {
            return;
        }

        setError("");

        if(selectedFile.type!=="application/pdf"){
            setError("Only PDF files are allowed.");
            setFile(null);
            return;
        }
        //file size=5MB
        const maxSize=5*1024*1024;
        if(selectedFile.size>maxSize){
            setError("File size must be less than 5 MB");
            setFile(null);
            return;
        }
        setFile(selectedFile);

    };

    const handleUpload=async ()=>{
        if(!file){
            setError("Please select a PDF first");
            return;
        }

       setError("");
       setUploading(true);
       try{
        const data=await uploadResume(file);
        console.log("upload successful",data);
        router.push("/dashboard");
       }catch(error){
        if (error instanceof Error){
            setError(error.message)
       }else{
        setError("Something went wrong while uploading")
       }
       }finally{
        setUploading(false);
       }
    };

    return(
        <main className="flex min-h-screen items-center justify-center p-6">
            <Card className="w-full max-w-lg">
                <CardHeader>
                    <CardTitle>
                        Upload Your Resume
                    </CardTitle>
                    <CardDescription>
                        Upload your resume in PDF format to get started with IntervviewIQ 
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    <div className="space-y-2">
                        <Input 
                           type="file"
                           accept=".pdf"
                           onChange={handleFileChange}
                        />
                        <p className="text-sm text-muted-foreground">
                            PDF only Maximum size:5MB
                        </p>
                    </div>
                    {
                        file && (
                            <div className="rounded-md border p-3">
                                <p className="text-sm font-medium">
                                    Selected File
                                </p>
                                <p className="text-sm text-muted-foreground">
                                    {file.name}
                                </p>
                            </div>
                        )
                    }

                    {
                        error&&(
                            <p className="text-sm text-destructive">
                                {error}
                            </p>
                        )
                    }
                    <Button 
                       className="w-full"
                       onClick={handleUpload}
                       disabled={!file||uploading}
                    >
                        {uploading ?"Uploading...":"Upload Resume"}
                    </Button>
                </CardContent>

            </Card>
        </main>
    )
}