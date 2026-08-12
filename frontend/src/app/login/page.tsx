"use client";

import { useState } from "react";
import {loginUser} from "@/services/auth.service";
export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

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

        console.log("login successfull");
        setEmail("");
        setPassword("");

    }catch(error){
        console.log(error);
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
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full border p-2 rounded"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border p-2 rounded"
        />

        <button
          type="submit"
          className="border px-4 py-2 rounded"
        >
          Login
        </button>
      </form>
    </main>
  );
}