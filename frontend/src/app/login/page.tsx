"use client";

import { useState } from "react";
import {loginUser} from "@/services/auth.service";
import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message,setMessage]=useState("");

  const handleSubmit=async(
    e:React.FormEvent<HTMLFormElement>
    
  )=>{
    e.preventDefault();

    

    try{

        const data=await loginUser(email,password);
        //console.log(data);

        localStorage.setItem(
          "access_token",
          data.access_token
        );

        setMessage("login successfull");
        setEmail("");
        setPassword("");

    }catch(error){
        if (error instanceof Error){

          setMessage(error.message);
        }else{
          setMessage("Something went wrong");
        }
    }
  }

  return (
    <main className="p-10">
      <h1 className="text-3xl font-bold">
        Login
      </h1>

      <form 
       onSubmit={handleSubmit}
      className="mt-6 space-y-4 max-w-md">
        <Input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          
        />

        <Input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          
        />
        <Button
         type="submit"
        >
          Login
        </Button>
        {
          message &&(
            <p className="mt-4">
              {message}
            </p>
          )
        }
      </form>
    </main>
  );
}