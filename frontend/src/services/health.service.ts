import { API_URL } from "./api";

export async function getHealth() {
  const response = await fetch(
    `${API_URL}/health`
  );

  return response.json();
}