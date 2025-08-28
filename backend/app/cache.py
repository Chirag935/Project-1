from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, Optional

try:
    import redis.asyncio as redis  # type: ignore
except Exception:  # pragma: no cover
    redis = None  # Fallback when redis is not installed


class Cache:
    """A minimal async cache interface with Redis or in-memory fallback."""

    def __init__(self, url: str) -> None:
        self._url = url
        self._client: Optional["redis.Redis"] = None
        self._memory: Dict[str, Any] = {}

    async def connect(self) -> None:
        if redis is None:
            return
        try:
            self._client = redis.from_url(self._url, decode_responses=True)
            await self._client.ping()
        except Exception:
            # Keep memory fallback
            self._client = None

    async def close(self) -> None:
        if self._client is not None:
            try:
                await self._client.aclose()
            except Exception:
                pass

    async def set_json(self, key: str, value: Any, ttl_seconds: int = 0) -> None:
        if self._client is not None:
            data = json.dumps(value)
            if ttl_seconds > 0:
                await self._client.setex(key, ttl_seconds, data)
            else:
                await self._client.set(key, data)
            return
        # Fallback: in-memory without TTL eviction
        self._memory[key] = value

    async def get_json(self, key: str) -> Optional[Any]:
        if self._client is not None:
            data = await self._client.get(key)
            if data is None:
                return None
            try:
                return json.loads(data)
            except Exception:
                return None
        return self._memory.get(key)