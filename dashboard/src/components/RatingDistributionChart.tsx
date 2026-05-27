import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { DashboardMetrics } from "../types";

type Props = { metrics: DashboardMetrics | null };

const BAR_COLORS: Record<string, string> = {
  "1": "#D97757",
  "2": "#E29A7F",
  "3": "#C5B89A",
  "4": "#A8C09A",
  "5": "#5C7C4E",
};

export function RatingDistributionChart({ metrics }: Props) {
  const data = ["1", "2", "3", "4", "5"].map((r) => ({
    rating: r,
    count: metrics?.rating_distribution[r] ?? 0,
    fill: BAR_COLORS[r],
  }));

  return (
    <div className="bg-beige-card rounded-2xl shadow-card p-6">
      <h2 className="text-lg font-semibold text-ink mb-1">
        Distribución de ratings
      </h2>
      <p className="text-sm text-ink-soft mb-4">
        Cantidad de respuestas por puntaje
      </p>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 16, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#EAE2CC" />
            <XAxis
              dataKey="rating"
              tick={{ fill: "#4A5747", fontSize: 14 }}
              axisLine={{ stroke: "#EAE2CC" }}
              tickLine={false}
            />
            <YAxis
              allowDecimals={false}
              tick={{ fill: "#4A5747", fontSize: 12 }}
              axisLine={{ stroke: "#EAE2CC" }}
              tickLine={false}
            />
            <Tooltip
              cursor={{ fill: "rgba(168,192,154,0.15)" }}
              contentStyle={{
                background: "#FAF6EC",
                border: "1px solid #EAE2CC",
                borderRadius: 8,
                fontSize: 13,
              }}
            />
            <Bar dataKey="count" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
