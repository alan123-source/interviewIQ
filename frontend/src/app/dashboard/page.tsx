"use client";
import {useState,useEffect} from "react";
import {useRouter} from "next/navigation";

import {getProfile,logoutUser} from "@/services/auth.service";
import {Card,CardContent,CardHeader,CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";

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
    <div>
      <h1 className="text-3xl font-bold">
        Welcome, {user.name}
      </h1>

      <p className="mt-2 text-muted-foreground">
        {user.email}
      </p>
    </div>

    <div className="grid gap-4 md:grid-cols-3 mt-8">
      <Card>
        <CardHeader>
          <CardTitle>Interviews Completed</CardTitle>
        </CardHeader>

        <CardContent>
          <p className="text-3xl font-bold">
            0
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Average Score</CardTitle>
        </CardHeader>

        <CardContent>
          <p className="text-3xl font-bold">
            --
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Practice Sessions</CardTitle>
        </CardHeader>

        <CardContent>
          <p className="text-3xl font-bold">
            0
          </p>
        </CardContent>
      </Card>
    </div>

    <div className="mt-8">
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>

        <CardContent>
          <p className="text-muted-foreground">
            No interview activity yet.
          </p>
        </CardContent>
      </Card>
    </div>

    <Button
      onClick={handleLogout}
      className="border px-4 py-2 rounded mt-6"
    >
      Logout
    </Button>
  </main>
);

    
} 