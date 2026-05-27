import { fetchRecentResponses } from "../api/endpoints";
import { useFetch } from "./useFetch";

export function useRecentResponses(limit = 20) {
  return useFetch(() => fetchRecentResponses(limit));
}
