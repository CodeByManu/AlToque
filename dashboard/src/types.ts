// Mirror de app/schemas.py — mantener sincronizado al cambiar la API.

export type Restaurant = {
  id: string;
  name: string;
};

export type CategoryStats = {
  count: number;
  avg: number;
};

export type DashboardMetrics = {
  total_responses: number;
  total_skipped: number;
  response_rate: number;
  avg_rating: number;
  avg_interaction_ms: number;
  rating_distribution: Record<string, number>;
  by_category: Record<string, CategoryStats>;
  active_alerts: number;
};

export type RecentResponse = {
  id: string;
  rating: number | null;
  action: "answered" | "skipped";
  question_text: string | null;
  category: string | null;
  table_number: number;
  waiter_name: string;
  responded_at: string;
  interaction_ms: number;
};

export type Alert = {
  id: string;
  response_id: string;
  whatsapp_status: "pending" | "sent" | "failed";
  whatsapp_message_sid: string | null;
  sent_at: string | null;
  resolved_at: string | null;
  created_at: string;
  rating: number | null;
  table_number: number | null;
  waiter_name: string | null;
  question_text: string | null;
};

export type WsEvent =
  | {
      type: "new_response";
      data: {
        id: string;
        rating: number | null;
        action: string;
        interaction_ms: number;
        responded_at: string;
      };
    }
  | {
      type: "new_alert";
      data: { id: string; response_id: string; rating: number };
    }
  | { type: "alert_resolved"; data: { id: string } };
