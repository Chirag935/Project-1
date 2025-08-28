import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Settings:
    """Typed configuration loaded from environment with sensible defaults.

    Avoids pydantic-settings to keep dependencies minimal and stable.
    """

    redis_url: str = "redis://localhost:6379/0"
    fetch_interval_sec: int = 60
    webcams_config_path: str = str(Path(__file__).resolve().parent.parent / "webcams.json")
    allow_origins: Optional[str] = "*"

    @classmethod
    def load(cls) -> "Settings":
        load_dotenv()  # Load .env if present
        redis_url = os.getenv("REDIS_URL", cls.redis_url)
        fetch_interval_sec = int(os.getenv("FETCH_INTERVAL_SEC", str(cls.fetch_interval_sec)))
        webcams_config_path = os.getenv("WEBCAMS_CONFIG_PATH", cls.webcams_config_path)
        allow_origins = os.getenv("ALLOW_ORIGINS", cls.allow_origins)
        return cls(
            redis_url=redis_url,
            fetch_interval_sec=fetch_interval_sec,
            webcams_config_path=webcams_config_path,
            allow_origins=allow_origins,
        )