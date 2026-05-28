import logging
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app import config
from app.routers import admin, alerts, dashboard, responses, restaurants, sessions, tables, waiters
from app.ws import manager

# Logging estructurado segun CLAUDE.md regla 4
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("app.main")

app = FastAPI(title="AlToque API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router)
app.include_router(responses.router)
app.include_router(dashboard.router)
app.include_router(restaurants.router)
app.include_router(alerts.router)
app.include_router(tables.router)
app.include_router(waiters.router)
app.include_router(admin.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.websocket("/ws/dashboard/{restaurant_id}")
async def ws_dashboard(websocket: WebSocket, restaurant_id: uuid.UUID) -> None:
    rid = str(restaurant_id)
    await manager.connect(rid, websocket)
    try:
        while True:
            # No esperamos mensajes del cliente, solo mantenemos la conexion.
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(rid, websocket)


@app.on_event("startup")
def on_startup() -> None:
    logger.info(
        "AlToque API arrancando · log_level=%s · origins=%s",
        config.LOG_LEVEL,
        config.ALLOWED_ORIGINS,
    )
