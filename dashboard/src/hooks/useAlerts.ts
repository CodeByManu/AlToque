import { fetchAlerts } from "../api/endpoints";
import { useFetch } from "./useFetch";

export function useAlerts() {
  return useFetch(fetchAlerts);
}
