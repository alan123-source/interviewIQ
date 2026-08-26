const API_URL=process.env.NEXT_PUBLIC_API_URL;

export async function loginUser(
    email:string,
    password:string
){

    if (!email||!password){
        
        throw new Error("Please fill all fields");

    }
    const response=await fetch(
        `${API_URL}/auth/login`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json",
            },

            body:JSON.stringify({
                email,password
            })
        }
    );

    const data=await response.json();

    if(!response.ok){
        throw new Error(
            data.detail || data.message ||"Login failed"
        );
    }

    return data;
}

export async function getProfile(){
    const token=localStorage.getItem("access_token");

    if(!token){
        throw new Error("Not authenticated");
    }

    const response=await fetch(
        `${API_URL}/auth/profile`,
        {
            headers:{
                Authorization:`Bearer ${token}`
            },
        }
    );

    const data=await response.json();

    if (response.status==401){
        localStorage.removeItem("access_token");
        throw new Error("Not authenticated");
    }

    if(!response.ok){
        throw new Error(
            data.detail||"unable to fetch profile"
        );
    }

    return data;
}

export function logoutUser(){
    localStorage.removeItem("access_token");
}