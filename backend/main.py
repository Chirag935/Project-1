"""
Real-time Urban Micro-Climate Map Backend
FastAPI application for webcam data ingestion and computer vision analysis
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import aiohttp
import json
import time
from datetime import datetime
from typing import List, Dict, Any
import logging
import redis
from pathlib import Path
import os
from dotenv import load_dotenv

from webcam_ingestion import WebcamIngestion
from cv_analysis import ComputerVisionAnalyzer
from websocket_manager import ConnectionManager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Urban Micro-Climate Map API", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
webcam_ingestion = WebcamIngestion()
cv_analyzer = ComputerVisionAnalyzer()
websocket_manager = ConnectionManager()

# Redis connection for caching
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    logger.info("Connected to Redis")
except Exception as e:
    logger.warning(f"Redis connection failed: {e}")
    redis_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize background tasks on startup"""
    logger.info("Starting Urban Micro-Climate Map Backend")
    
    # Start webcam data ingestion task
    asyncio.create_task(webcam_data_pipeline())

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Urban Micro-Climate Map Backend")

async def webcam_data_pipeline():
    """Main data pipeline - fetch images, analyze, and broadcast results"""
    while True:
        try:
            # Fetch images from webcams
            webcam_data = await webcam_ingestion.fetch_all_webcams()
            
            # Analyze each image for micro-climate conditions
            analysis_results = []
            for data in webcam_data:
                if data.get('image_data'):
                    analysis = await cv_analyzer.analyze_image(
                        data['image_data'], 
                        data['location']
                    )
                    
                    result = {
                        'webcam_id': data['webcam_id'],
                        'location': data['location'],
                        'timestamp': datetime.now().isoformat(),
                        'analysis': analysis,
                        'image_url': data.get('image_url')
                    }
                    analysis_results.append(result)
                    
                    # Cache in Redis
                    if redis_client:
                        try:
                            redis_client.setex(
                                f"webcam:{data['webcam_id']}", 
                                300,  # 5 minutes TTL
                                json.dumps(result)
                            )
                        except Exception as e:
                            logger.error(f"Redis cache error: {e}")
            
            # Broadcast to connected WebSocket clients
            if analysis_results:
                await websocket_manager.broadcast({
                    'type': 'webcam_update',
                    'data': analysis_results,
                    'timestamp': datetime.now().isoformat()
                })
                
                logger.info(f"Processed {len(analysis_results)} webcam updates")
            
            # Wait before next cycle (configurable interval)
            await asyncio.sleep(int(os.getenv('FETCH_INTERVAL', 60)))  # Default 1 minute
            
        except Exception as e:
            logger.error(f"Error in webcam data pipeline: {e}")
            await asyncio.sleep(10)  # Wait before retrying

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Urban Micro-Climate Map API", "status": "running"}

@app.get("/api/webcams")
async def get_webcams():
    """Get list of configured webcams"""
    return await webcam_ingestion.get_webcam_list()

@app.get("/api/webcams/{webcam_id}/latest")
async def get_latest_analysis(webcam_id: str):
    """Get latest analysis for a specific webcam"""
    if redis_client:
        try:
            cached_data = redis_client.get(f"webcam:{webcam_id}")
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            logger.error(f"Redis retrieval error: {e}")
    
    return {"error": "No recent data available"}

@app.get("/api/all-latest")
async def get_all_latest():
    """Get latest analysis for all webcams"""
    if redis_client:
        try:
            keys = redis_client.keys("webcam:*")
            results = []
            for key in keys:
                data = redis_client.get(key)
                if data:
                    results.append(json.loads(data))
            return results
        except Exception as e:
            logger.error(f"Redis retrieval error: {e}")
    
    return []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle client messages
            data = await websocket.receive_text()
            # Echo back for now (can be extended for client commands)
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)