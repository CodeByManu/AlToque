"""
WebSocket manager para el dashboard en tiempo real.

Por simplicidad: un dict {restaurant_id: set[WebSocket]} en memoria del
proceso. Si escalamos a multiples workers de uvicorn, esto deja de ser
suficiente y habria que pasar a Redis pub/sub. Para el piloto: alcanza.
"""
import asyncio
import logging
from collections import defaultdict
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, restaurant_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections[restaurant_id].add(websocket)
        logger.info(
            "WS conectado restaurant=%s · total=%d",
            restaurant_id,
            len(self._connections[restaurant_id]),
        )

    async def disconnect(self, restaurant_id: str, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections[restaurant_id].discard(websocket)
        logger.info(
            "WS desconectado restaurant=%s · total=%d",
            restaurant_id,
            len(self._connections.get(restaurant_id, set())),
        )

    async def broadcast(self, restaurant_id: str, event: dict[str, Any]) -> None:
        async with self._lock:
            targets = list(self._connections.get(restaurant_id, set()))
        dead: list[WebSocket] = []
        for ws in targets:
            try:
                await ws.send_json(event)
            except Exception as e:
                logger.warning("WS send fallo, marcando para purga: %s", e)
                dead.append(ws)
        if dead:
            async with self._lock:
                for ws in dead:
                    self._connections[restaurant_id].discard(ws)


manager = ConnectionManager()


def broadcast_event(restaurant_id: str, event: dict[str, Any]) -> None:
    """
    Wrapper sincrono para llamar desde BackgroundTasks.
    Programa el broadcast async en el event loop activo.
    """
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(manager.broadcast(restaurant_id, event))
    except RuntimeError:
        # Sin loop activo (raro en FastAPI, pero por las dudas).
        asyncio.run(manager.broadcast(restaurant_id, event))
