from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass
from typing import Dict, List

import aiohttp

from .analysis import compute_sun_exposure_from_bytes
from .cache import Cache
from .schemas import AnalysisResult
from .ws import ConnectionManager


@dataclass
class WebcamSource:
    id: str
    name: str
    latitude: float
    longitude: float
    image_url: str


class IngestionService:
    def __init__(self, *, webcams: List[WebcamSource], interval_sec: int, cache: Cache, ws_manager: ConnectionManager) -> None:
        self._webcams = webcams
        self._interval_sec = max(10, interval_sec)  # avoid hammering demo endpoints
        self._cache = cache
        self._ws = ws_manager
        self._task: asyncio.Task | None = None
        self._stop_event = asyncio.Event()

    def start(self) -> None:
        if self._task is None or self._task.done():
            self._stop_event.clear()
            self._task = asyncio.create_task(self._run_loop(), name="ingestion-loop")

    async def stop(self) -> None:
        self._stop_event.set()
        if self._task is not None:
            await asyncio.wait([self._task], timeout=5)

    async def _run_loop(self) -> None:
        async with aiohttp.ClientSession() as session:
            while not self._stop_event.is_set():
                await self._process_all(session)
                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=self._interval_sec)
                except asyncio.TimeoutError:
                    pass

    async def _process_all(self, session: aiohttp.ClientSession) -> None:
        tasks = [self._process_one(session, cam) for cam in self._webcams]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _process_one(self, session: aiohttp.ClientSession, cam: WebcamSource) -> None:
        try:
            async with session.get(cam.image_url, timeout=20) as resp:
                if resp.status != 200:
                    return
                image_bytes = await resp.read()
        except Exception:
            return

        sun_exposure, _, _ = compute_sun_exposure_from_bytes(image_bytes)
        result = AnalysisResult(
            webcam_id=cam.id,
            sun_exposure=float(round(sun_exposure, 4)),
            timestamp=time.time(),
            image_url=cam.image_url,
        )
        key = f"analysis:{cam.id}"
        await self._cache.set_json(key, result.model_dump())
        await self._ws.broadcast_json({"type": "analysis", "payload": result.model_dump()})


def load_webcams_from_path(path: str) -> List[WebcamSource]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    webcams: List[WebcamSource] = []
    for item in data:
        webcams.append(
            WebcamSource(
                id=item["id"],
                name=item.get("name", item["id"]),
                latitude=float(item["latitude"]),
                longitude=float(item["longitude"]),
                image_url=item["image_url"],
            )
        )
    return webcams