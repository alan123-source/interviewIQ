"use client";
import {useState,useEffect} from "react";
import {useRouter} from "next/navigation";

import {getProfile,logoutUser} from "@/services/auth.service";

type User={
    id:number;
    name:string;
    email:string;
};

export default function DashboardPage(){

    const router=useRouter();

    const [user,setUser]=useState<User |null>(null);

    const [loading,setLoading]=useState(true);

    useEffect(()=>{
        
        getProfile()
        .then((data)=>{
            setUser(data);
        })
        .catch(()=>{
            localStorage.removeItem("access_token");
            router.push("/login");
        })
        .finally(()=>{
            setLoading(false);
        });
          
    },[router]);

    const handleLogout=()=>{
       logoutUser();
       router.push("/login");
    };

    if (!user){
        return null;
    }
    return (
    <main className="p-10">
      <h1 className="text-3xl font-bold">
        Welcome, {user.name}
      </h1>

      <p className="mt-2">
        {user.email}
      </p>

      <div className="mt-8">
        <p>Your InterviewIQ dashboard will appear here.</p>
      </div>
      <button 
      onClick={handleLogout}
      className="border px-4 py-2 rounded mt-6">
        Logout
      </button>
    </main>
  );

    
} 