import { useEffect, useRef } from "react";
import { RESTAURANT_ID, WS_URL } from "../api/client";
import type { WsEvent } from "../types";

type Handlers = {
  onNewResponse?: (e: Extract<WsEvent, { type: "new_response" }>) => void;
  onNewAlert?: (e: Extract<WsEvent, { type: "new_alert" }>) => void;
  onAlertResolved?: (e: Extract<WsEvent, { type: "alert_resolved" }>) => void;
};

// WebSocket simple con reconexion exponencial. Sin libreria.
export function useDashboardWs(handlers: Handlers) {
  const handlersRef = useRef(handlers);
  handlersRef.current = handlers;

  useEffect(() => {
    if (!RESTAURANT_ID) return;

    let ws: WebSocket | null = null;
    let retry = 0;
    let reconnectTimer: number | null = null;
    let closedManually = false;

    const connect = () => {
      const url = `${WS_URL}/ws/dashboard/${RESTAURANT_ID}`;
      ws = new WebSocket(url);

      ws.onopen = () => {
        retry = 0;
        console.info("[ws] conectado");
      };

      ws.onmessage = (msg) => {
        try {
          const event = JSON.parse(msg.data) as WsEvent;
          if (event.type === "new_response") handlersRef.current.onNewResponse?.(event);
          else if (event.type === "new_alert") handlersRef.current.onNewAlert?.(event);
          else if (event.type === "alert_resolved") handlersRef.current.onAlertResolved?.(event);
        } catch (e) {
          console.error("[ws] mensaje no parseable", e);
        }
      };

      ws.onclose = () => {
        if (closedManually) return;
        const delay = Math.min(1000 * 2 ** retry, 15000);
        retry += 1;
        console.warn(`[ws] desconectado, reintento en ${delay}ms`);
        reconnectTimer = window.setTimeout(connect, delay);
      };

      ws.onerror = () => {
        // El close handler maneja el retry; aca solo loggeo
        console.error("[ws] error");
      };
    };

    connect();

    return () => {
      closedManually = true;
      if (reconnectTimer) window.clearTimeout(reconnectTimer);
      ws?.close();
    };
  }, []);
}
