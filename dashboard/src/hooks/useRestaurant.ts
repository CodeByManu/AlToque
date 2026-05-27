import { fetchRestaurant } from "../api/endpoints";
import { useFetch } from "./useFetch";

export function useRestaurant() {
  return useFetch(fetchRestaurant);
}
