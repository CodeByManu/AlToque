import type { Alert } from "../types";

type Props = {
  alert: Alert;
  flash: boolean;
  resolving: boolean;
  onResolve: () => void;
};

function fmtHora(iso: string) {
  return new Date(iso).toLocaleTimeString("es-CL", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function AlertCard({ alert, flash, resolving, onResolve }: Props) {
  return (
    <div
      className={`bg-alert-soft border border-alert/30 rounded-xl p-4 ${
        flash ? "pulse-alert" : ""
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-wider text-alert font-semibold">
            Rating {alert.rating}/5
          </p>
          <p className="text-sm text-ink mt-1">
            Mesa <span className="font-semibold">{alert.table_number}</span> ·{" "}
            {alert.waiter_name}
          </p>
        </div>
        <p className="text-xs text-ink-soft tabular-nums">
          {fmtHora(alert.created_at)}
        </p>
      </div>
      {alert.question_text && (
        <p className="text-sm text-ink-soft italic mt-2">
          "{alert.question_text}"
        </p>
      )}
      <div className="flex items-center justify-between mt-3">
        <p className="text-xs text-ink-mute">
          WhatsApp:{" "}
          <span
            className={
              alert.whatsapp_status === "sent"
                ? "text-brand"
                : alert.whatsapp_status === "failed"
                ? "text-alert"
                : "text-ink-soft"
            }
          >
            {alert.whatsapp_status}
          </span>
        </p>
        <button
          onClick={onResolve}
          disabled={resolving}
          className="text-xs bg-brand text-beige-card px-3 py-1.5 rounded-md hover:bg-brand-dark transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {resolving ? "Resolviendo…" : "Marcar resuelta"}
        </button>
      </div>
    </div>
  );
}
