"use client";

import { useEffect, useState } from "react";

type User = {
  id: number;
  name: string;
  email: string;
};

export default function ProfileTestPage() {
  const [user, setUser] = useState<User | null>(null);
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setMessage("No authentication token found.");
      return;
    }

    fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/auth/profile`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail || "Unable to fetch profile."
          );
        }

        return data;
      })
      .then((data) => {
        setUser(data);
        setMessage("");
      })
      .catch((error) => {
        setMessage(error.message);
      });
  }, []);

  return (
    <main className="p-10">
      <h1 className="text-3xl font-bold">
        Profile Test
      </h1>

      {message && (
        <p className="mt-4">
          {message}
        </p>
      )}

      {user && (
        <div className="mt-6">
          <p>ID: {user.id}</p>
          <p>Name: {user.name}</p>
          <p>Email: {user.email}</p>
        </div>
      )}
    </main>
  );
}