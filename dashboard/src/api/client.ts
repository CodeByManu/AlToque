import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export const api = axios.create({
  baseURL,
  timeout: 8000,
});

export const RESTAURANT_ID = import.meta.env.VITE_RESTAURANT_ID as string;
export const WS_URL = (import.meta.env.VITE_WS_URL as string) ?? "ws://localhost:8000";

if (!RESTAURANT_ID) {
  console.warn(
    "VITE_RESTAURANT_ID no esta definido en .env. Hacé curl http://localhost:8000/api/v1/restaurants para obtenerlo."
  );
}
