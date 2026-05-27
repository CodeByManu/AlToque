import { fetchMetrics } from "../api/endpoints";
import { useFetch } from "./useFetch";

export function useMetrics() {
  return useFetch(fetchMetrics);
}
