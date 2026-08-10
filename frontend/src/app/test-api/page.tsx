"use client";

import {useEffect,useState} from "react";
import {API_URL} from "@/services/api";

export default function TestApiPage(){

    const [status,setStatus]=useState("Loading...");
    useEffect(()=>{
        fetch(`${API_URL}/health`)
          .then((res)=>res.json())
          .then((data)=>{
            setStatus(data.status);
          })
          .catch(()=>{
            setStatus("Backend Offline");
          });
    },[]);
    return (
        <div className="p-10">
            <h1>Backend Status</h1>
            <p>{status}</p>
          
        </div>
    );
}