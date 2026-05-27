import { api, RESTAURANT_ID } from "./client";
import type {
  Alert,
  DashboardMetrics,
  RecentResponse,
  Restaurant,
} from "../types";

export async function fetchRestaurant(): Promise<Restaurant> {
  const { data } = await api.get<Restaurant>(
    `/api/v1/restaurants/${RESTAURANT_ID}`
  );
  return data;
}

export async function fetchMetrics(): Promise<DashboardMetrics> {
  const { data } = await api.get<DashboardMetrics>(
    "/api/v1/dashboard/metrics",
    { params: { restaurant_id: RESTAURANT_ID } }
  );
  return data;
}

export async function fetchRecentResponses(
  limit = 20
): Promise<RecentResponse[]> {
  const { data } = await api.get<RecentResponse[]>(
    "/api/v1/dashboard/responses/recent",
    { params: { restaurant_id: RESTAURANT_ID, limit } }
  );
  return data;
}

export async function fetchAlerts(): Promise<Alert[]> {
  const { data } = await api.get<Alert[]>("/api/v1/dashboard/alerts", {
    params: { restaurant_id: RESTAURANT_ID },
  });
  return data;
}

export async function resolveAlert(alertId: string): Promise<Alert> {
  const { data } = await api.patch<Alert>(
    `/api/v1/alerts/${alertId}/resolve`
  );
  return data;
}
