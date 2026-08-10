"use client";
import {useState} from "react";
export default function SignupPage(){

    const [name,setName]=useState("");
    const [email,setEmail]=useState("");
    const [password,setPassword]=useState("");
    const [loading,setLoading]=useState(false);
    const [message,setMessage]=useState("");

    const handleSubmit=async(
        e:React.FormEvent<HTMLFormElement>
    ) => {
        e.preventDefault();
        setLoading(true);
        setMessage("");
    try{
        const response=await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}/auth/register`,
            {
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                },

                body:JSON.stringify({
                    name,
                    email,
                    password
                }),
            }
        );   

        const data=await response.json();
        console.log(data);

        if (!response.ok){

            setMessage(
                "Please fill all fields correctly"
            );

            return;
            
        }

        setMessage("Account Created successfully");
        setName("");
        setEmail("");
        setPassword("");
    }catch(error){
        setMessage(
            "unable to connect to server"
        );
    }finally{
        setLoading(false)
    }
}
    return (
        <main className="p-10">
            <h1 className="text-3xl font-bold">
                Create Account
            </h1>

            <form 
            onSubmit={handleSubmit}
            className="mt-6 space-y-4 max-w-md">
                <input 
                   type="text"
                   placeholder="Name"
                   value={name}
                   onChange={(e) => setName(e.target.value)}
                   className="w-full border p-2 rounded"
                   
                />

                <input 
                   type="email"
                   placeholder="Email"
                   value={email}
                   onChange={(e)=>setEmail(e.target.value)}
                   className="w-full border p-2 rounded"
                />

                <input 
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e)=>setPassword(e.target.value)}
                  className="w-full border p-2 rounded"
                />

                <button
                   type="submit"
                   className="border px-4 py-2 rounded"
                >
                    {

                        loading?"Creating Account....": "Create Account"
                    }
                </button>

                {
                    message&&(
                        <p className="mt-4">
                            {message}
                        </p>
                    )
                }

            </form>

        </main>
    );
}