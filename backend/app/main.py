from __future__ import annotations

import asyncio
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings
from .cache import Cache
from .ingest import IngestionService, load_webcams_from_path
from .schemas import AnalysisResult
from .ws import ConnectionManager

settings = Settings.load()
app = FastAPI(title="Urban Micro-Climate Backend")

if settings.allow_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in settings.allow_origins.split(",")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

cache = Cache(settings.redis_url)
ws_manager = ConnectionManager()

# Will be initialized at startup
ingestion: IngestionService | None = None


@app.on_event("startup")
async def on_startup() -> None:
    global ingestion
    await cache.connect()
    webcams = load_webcams_from_path(settings.webcams_config_path)
    ingestion = IngestionService(webcams=webcams, interval_sec=settings.fetch_interval_sec, cache=cache, ws_manager=ws_manager)
    ingestion.start()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    if ingestion is not None:
        await ingestion.stop()
    await cache.close()


@app.get("/api/webcams")
async def list_webcams():
    webcams = load_webcams_from_path(settings.webcams_config_path)
    return [w.__dict__ for w in webcams]


@app.get("/api/analysis/{webcam_id}")
async def get_analysis(webcam_id: str):
    data = await cache.get_json(f"analysis:{webcam_id}")
    return data or {"webcam_id": webcam_id, "sun_exposure": None}


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive; clients don't need to send messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
    except Exception:
        await ws_manager.disconnect(websocket)