import { useState } from "react";
import { resolveAlert } from "../api/endpoints";
import type { Alert } from "../types";
import { AlertCard } from "./AlertCard";

type Props = {
  alerts: Alert[] | null;
  flashIds: Set<string>;
  onResolved: (id: string) => void;
};

export function AlertsSidebar({ alerts, flashIds, onResolved }: Props) {
  const [resolving, setResolving] = useState<Set<string>>(new Set());

  const handleResolve = async (id: string) => {
    setResolving((prev) => new Set(prev).add(id));
    try {
      await resolveAlert(id);
      onResolved(id);
    } catch (e) {
      console.error("[resolveAlert]", e);
    } finally {
      setResolving((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  };

  return (
    <aside className="bg-beige-card rounded-2xl shadow-card p-6 h-fit sticky top-6">
      <div className="flex items-baseline justify-between mb-4">
        <h2 className="text-lg font-semibold text-ink">Alertas activas</h2>
        <span className="text-sm font-semibold text-alert tabular-nums">
          {alerts?.length ?? 0}
        </span>
      </div>
      {alerts === null && (
        <p className="text-sm text-ink-mute py-8 text-center">Cargando…</p>
      )}
      {alerts && alerts.length === 0 && (
        <p className="text-sm text-ink-mute py-8 text-center">
          Sin alertas activas
        </p>
      )}
      <div className="space-y-3">
        {alerts?.map((a) => (
          <AlertCard
            key={a.id}
            alert={a}
            flash={flashIds.has(a.id)}
            resolving={resolving.has(a.id)}
            onResolve={() => handleResolve(a.id)}
          />
        ))}
      </div>
    </aside>
  );
}
