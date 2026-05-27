import type { RecentResponse } from "../types";

type Props = { rows: RecentResponse[] | null };

function fmtHora(iso: string) {
  return new Date(iso).toLocaleTimeString("es-CL", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function fmtInteraction(ms: number) {
  if (ms < 1000) return `${ms} ms`;
  return `${(ms / 1000).toFixed(1)} s`;
}

function ratingDot(rating: number | null, action: string) {
  if (action === "skipped" || rating === null) {
    return (
      <span className="inline-flex items-center text-xs text-ink-mute">
        <span className="w-2 h-2 rounded-full bg-ink-mute mr-2" />
        Omitida
      </span>
    );
  }
  const color =
    rating >= 4 ? "#5C7C4E" : rating === 3 ? "#C5B89A" : "#D97757";
  return (
    <span className="inline-flex items-center font-semibold text-ink">
      <span
        className="w-2 h-2 rounded-full mr-2"
        style={{ backgroundColor: color }}
      />
      {rating}/5
    </span>
  );
}

export function RecentResponsesTable({ rows }: Props) {
  return (
    <div className="bg-beige-card rounded-2xl shadow-card p-6">
      <h2 className="text-lg font-semibold text-ink mb-1">
        Últimas respuestas
      </h2>
      <p className="text-sm text-ink-soft mb-4">
        Las 20 más recientes, en tiempo real
      </p>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs uppercase tracking-wider text-ink-mute border-b border-beige-deep">
              <th className="py-3 pr-4 font-medium">Hora</th>
              <th className="py-3 pr-4 font-medium">Mesa</th>
              <th className="py-3 pr-4 font-medium">Garzón</th>
              <th className="py-3 pr-4 font-medium">Pregunta</th>
              <th className="py-3 pr-4 font-medium">Rating</th>
              <th className="py-3 font-medium">Tiempo</th>
            </tr>
          </thead>
          <tbody>
            {rows === null && (
              <tr>
                <td colSpan={6} className="py-8 text-center text-ink-mute">
                  Cargando…
                </td>
              </tr>
            )}
            {rows && rows.length === 0 && (
              <tr>
                <td colSpan={6} className="py-8 text-center text-ink-mute">
                  Todavía no hay respuestas
                </td>
              </tr>
            )}
            {rows?.map((r) => (
              <tr
                key={r.id}
                className="border-b border-beige last:border-b-0 hover:bg-beige/50"
              >
                <td className="py-3 pr-4 text-ink-soft tabular-nums">
                  {fmtHora(r.responded_at)}
                </td>
                <td className="py-3 pr-4 font-semibold">{r.table_number}</td>
                <td className="py-3 pr-4">{r.waiter_name}</td>
                <td className="py-3 pr-4 text-ink-soft max-w-md truncate">
                  {r.question_text ?? "—"}
                </td>
                <td className="py-3 pr-4">{ratingDot(r.rating, r.action)}</td>
                <td className="py-3 text-ink-soft tabular-nums">
                  {fmtInteraction(r.interaction_ms)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
