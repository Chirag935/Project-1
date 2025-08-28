import asyncio
import json
import logging
from typing import Dict, List, Optional
import redis.asyncio as redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import cv2
import numpy as np
from PIL import Image
import io
import base64

from webcam_ingestion import WebcamIngestionService
from cv_analysis import ComputerVisionAnalyzer
from models import WebcamData, AnalysisResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Urban Micro-Climate Map API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
redis_client: Optional[redis.Redis] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        if self.active_connections:
            for connection in self.active_connections:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error broadcasting to WebSocket: {e}")
                    # Remove broken connections
                    self.active_connections.remove(connection)

manager = ConnectionManager()

# Initialize services
webcam_service = WebcamIngestionService()
cv_analyzer = ComputerVisionAnalyzer()

@app.on_event("startup")
async def startup_event():
    global redis_client
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        await redis_client.ping()
        logger.info("Connected to Redis")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        redis_client = None

@app.on_event("shutdown")
async def shutdown_event():
    if redis_client:
        await redis_client.close()

@app.get("/")
async def root():
    return {"message": "Urban Micro-Climate Map API"}

@app.get("/webcams")
async def get_webcams():
    """Get list of available webcams"""
    webcams = webcam_service.get_webcam_list()
    return {"webcams": webcams}

@app.get("/analysis/{webcam_id}")
async def get_analysis(webcam_id: str):
    """Get latest analysis for a specific webcam"""
    if not redis_client:
        return {"error": "Redis not available"}
    
    try:
        result = await redis_client.get(f"analysis:{webcam_id}")
        if result:
            return json.loads(result)
        return {"error": "No analysis data found"}
    except Exception as e:
        logger.error(f"Error getting analysis: {e}")
        return {"error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            # Echo back for testing
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/trigger-analysis")
async def trigger_analysis():
    """Manually trigger analysis of all webcams"""
    try:
        results = await webcam_service.analyze_all_webcams()
        
        # Broadcast results to all connected WebSocket clients
        for result in results:
            await manager.broadcast({
                "type": "analysis_update",
                "webcam_id": result.webcam_id,
                "data": result.dict(),
                "timestamp": datetime.now().isoformat()
            })
        
        return {"message": f"Analysis completed for {len(results)} webcams", "results": results}
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)