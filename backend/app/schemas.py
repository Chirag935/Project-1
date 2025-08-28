from typing import Optional
from pydantic import BaseModel, Field


class Webcam(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    image_url: str


class AnalysisResult(BaseModel):
    webcam_id: str
    sun_exposure: float = Field(ge=0.0, le=1.0)
    timestamp: float
    image_url: Optional[str] = None