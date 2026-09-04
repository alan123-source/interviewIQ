const API_URL=process.env.NEXT_PUBLIC_API_URL;

export async function uploadResume(file:File){
    const token=localStorage.getItem("access_token");

    if(!token){
        throw new Error("Not authenicated");

    }

    const formData=new FormData();

    formData.append("file",file);

    const response=await fetch(
        `${API_URL}/resumes/upload`,
        {
            method:"POST",
            headers:{
                Authorization:`Bearer ${token}`,
            },
            body:formData,
        }
    );

    const data=await response.json();

    if(response.status===401){
        throw new Error("Not authenticated");
    }

    if(!response.ok){
        throw new Error(data.detail||data.message||"Resume upload failed");
    }

    return data;

}

export async function getResumes(){
    const token=localStorage.getItem("access_token");

    if(!token){
        throw new Error("Not authenticated");
    }

    const response=await fetch(
        `${API_URL}/resumes`,
        {
            method:"GET",
            headers:{
                Authorization:`Bearer ${token}`,
            },
        }
    );

    const data=await response.json();

    if(response.status===401){
        throw new Error("Not authenticated")
    }

    if(!response.ok){
        throw new Error(
            data.detail||data.message||"Failed to fetch resumes"
        );
    }

    return data
}

export async function getResume(resumeId:number){

    const token=localStorage.getItem("access_token");

    if(!token){
        throw new Error("Not authenticated");
    }

    const response=await fetch(
        `${API_URL}/resumes/${resumeId}`,
        {
            method:"GET",
            headers:{
                Authorization:`Bearer ${token}`,
            },
        }
    );

    const data=await response.json();

    if(response.status===401){
        throw new Error("Not authenticated");
    }

    if(!response.ok){
        throw new Error(
            data.detail ||"Falied to fech resume"
        );
    }
    return data
}


export async function deleteResume(resumeId: number) {
    const token = localStorage.getItem("access_token");

    if (!token) {
        throw new Error("Not authenticated");
    }

    const response = await fetch(
        `${API_URL}/resumes/${resumeId}`,
        {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    const data = await response.json();

    if (response.status === 401) {
        throw new Error("Not authenticated");
    }

    if (!response.ok) {
        throw new Error(
            data.detail || "Failed to delete resume"
        );
    }

    return data;
}