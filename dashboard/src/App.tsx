import { useCallback, useEffect, useRef, useState } from "react";
import { AlertsSidebar } from "./components/AlertsSidebar";
import { Header } from "./components/Header";
import { KpiCards } from "./components/KpiCards";
import { NewAlertToast } from "./components/NewAlertToast";
import { RatingDistributionChart } from "./components/RatingDistributionChart";
import { RecentResponsesTable } from "./components/RecentResponsesTable";
import { useAlerts } from "./hooks/useAlerts";
import { useDashboardWs } from "./hooks/useDashboardWs";
import { useMetrics } from "./hooks/useMetrics";
import { useRecentResponses } from "./hooks/useRecentResponses";
import { useRestaurant } from "./hooks/useRestaurant";

type ToastState = { id: number; rating: number } | null;

export default function App() {
  const restaurant = useRestaurant();
  const metrics = useMetrics();
  const recent = useRecentResponses(20);
  const alerts = useAlerts();

  const [toast, setToast] = useState<ToastState>(null);
  const [flashIds, setFlashIds] = useState<Set<string>>(new Set());
  const toastTimerRef = useRef<number | null>(null);

  const triggerToast = useCallback((rating: number) => {
    setToast({ id: Date.now(), rating });
    if (toastTimerRef.current) window.clearTimeout(toastTimerRef.current);
    toastTimerRef.current = window.setTimeout(() => setToast(null), 5000);
  }, []);

  const flashAlert = useCallback((alertId: string) => {
    setFlashIds((prev) => new Set(prev).add(alertId));
    window.setTimeout(() => {
      setFlashIds((prev) => {
        const next = new Set(prev);
        next.delete(alertId);
        return next;
      });
    }, 3000);
  }, []);

  useDashboardWs({
    onNewResponse: () => {
      metrics.refetch();
      recent.refetch();
    },
    onNewAlert: (event) => {
      triggerToast(event.data.rating);
      alerts.refetch();
      metrics.refetch();
      flashAlert(event.data.id);
    },
    onAlertResolved: () => {
      alerts.refetch();
      metrics.refetch();
    },
  });

  useEffect(() => {
    return () => {
      if (toastTimerRef.current) window.clearTimeout(toastTimerRef.current);
    };
  }, []);

  const activeAlertsLive = alerts.data?.length ?? metrics.data?.active_alerts ?? 0;

  return (
    <div className="min-h-screen flex flex-col">
      <Header restaurantName={restaurant.data?.name ?? null} />

      <main className="flex-1 max-w-[1600px] w-full mx-auto px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-6">
          <div className="space-y-6">
            <KpiCards metrics={metrics.data} activeAlertsLive={activeAlertsLive} />
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <RatingDistributionChart metrics={metrics.data} />
              <div className="bg-beige-card rounded-2xl shadow-card p-6">
                <h2 className="text-lg font-semibold text-ink mb-1">
                  Por categoría
                </h2>
                <p className="text-sm text-ink-soft mb-4">
                  Promedio por tipo de pregunta
                </p>
                {metrics.data ? (
                  Object.keys(metrics.data.by_category).length === 0 ? (
                    <p className="text-sm text-ink-mute py-6 text-center">
                      Sin datos aún
                    </p>
                  ) : (
                    <ul className="space-y-3">
                      {Object.entries(metrics.data.by_category).map(
                        ([cat, stats]) => (
                          <li
                            key={cat}
                            className="flex items-baseline justify-between"
                          >
                            <span className="capitalize text-ink">{cat}</span>
                            <span className="text-sm text-ink-soft">
                              <span className="font-semibold text-ink mr-2">
                                {stats.avg.toFixed(2)}
                              </span>
                              ({stats.count})
                            </span>
                          </li>
                        )
                      )}
                    </ul>
                  )
                ) : (
                  <div className="h-32 animate-pulse bg-beige rounded" />
                )}
              </div>
            </div>
            <RecentResponsesTable rows={recent.data} />
          </div>

          <AlertsSidebar
            alerts={alerts.data}
            flashIds={flashIds}
            onResolved={() => {
              alerts.refetch();
              metrics.refetch();
            }}
          />
        </div>
      </main>

      {toast && (
        <NewAlertToast
          key={toast.id}
          rating={toast.rating}
          onDismiss={() => setToast(null)}
        />
      )}
    </div>
  );
}
