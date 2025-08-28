from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class WeatherCondition(str, Enum):
    SUNNY = "sunny"
    SHADY = "shady"
    WET = "wet"
    DRY = "dry"
    UNKNOWN = "unknown"

class WebcamLocation(BaseModel):
    """Represents a webcam location with coordinates and metadata"""
    id: str
    name: str
    latitude: float
    longitude: float
    url: str
    city: str
    country: str
    description: Optional[str] = None
    last_updated: Optional[datetime] = None

class AnalysisResult(BaseModel):
    """Result of computer vision analysis on a webcam image"""
    webcam_id: str
    timestamp: datetime
    sun_exposure: float  # 0.0 to 1.0, where 1.0 is full sun
    shadow_percentage: float  # 0.0 to 1.0, percentage of shadow
    wetness_score: float  # 0.0 to 1.0, likelihood of wet conditions
    weather_condition: WeatherCondition
    confidence: float  # 0.0 to 1.0, confidence in the analysis
    metadata: Optional[Dict[str, Any]] = None

class WebcamData(BaseModel):
    """Complete data for a webcam including location and analysis"""
    location: WebcamLocation
    latest_analysis: Optional[AnalysisResult] = None
    image_url: Optional[str] = None
    status: str = "active"  # active, inactive, error

class SystemStatus(BaseModel):
    """Overall system status and health"""
    total_webcams: int
    active_webcams: int
    last_analysis: Optional[datetime] = None
    system_health: str  # healthy, warning, error
    redis_status: str
    analysis_queue_size: int = 0