import type { DashboardMetrics } from "../types";

type Props = { metrics: DashboardMetrics | null; activeAlertsLive: number };

function Card({
  label,
  value,
  hint,
  tone = "default",
}: {
  label: string;
  value: string;
  hint?: string;
  tone?: "default" | "alert";
}) {
  const valueClass =
    tone === "alert" && value !== "0" ? "text-alert" : "text-ink";
  return (
    <div className="bg-beige-card rounded-2xl shadow-card p-6">
      <p className="text-xs uppercase tracking-wider text-ink-mute">{label}</p>
      <p className={`text-4xl font-semibold mt-3 ${valueClass}`}>{value}</p>
      {hint && <p className="text-sm text-ink-soft mt-2">{hint}</p>}
    </div>
  );
}

export function KpiCards({ metrics, activeAlertsLive }: Props) {
  if (!metrics) {
    return (
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div
            key={i}
            className="bg-beige-card rounded-2xl shadow-card p-6 h-32 animate-pulse"
          />
        ))}
      </div>
    );
  }

  const ratePct = (metrics.response_rate * 100).toFixed(1);

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <Card
        label="Tasa de respuesta"
        value={`${ratePct}%`}
        hint={`${metrics.total_responses} respondidas · ${metrics.total_skipped} omitidas`}
      />
      <Card
        label="Rating promedio"
        value={metrics.avg_rating.toFixed(2)}
        hint="sobre 5"
      />
      <Card
        label="Respuestas (histórico)"
        value={metrics.total_responses.toString()}
        hint="Total acumulado"
      />
      <Card
        label="Alertas activas"
        value={activeAlertsLive.toString()}
        hint="Últimas 24h sin resolver"
        tone="alert"
      />
    </div>
  );
}
