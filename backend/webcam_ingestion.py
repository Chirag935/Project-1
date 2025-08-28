import asyncio
import aiohttp
import logging
from typing import List, Dict, Optional
from datetime import datetime
import redis.asyncio as redis
import json
from PIL import Image, ImageDraw
import io
import base64
import random

from models import WebcamLocation, AnalysisResult, WebcamData
from cv_analysis import ComputerVisionAnalyzer

logger = logging.getLogger(__name__)

class WebcamIngestionService:
    """Service for ingesting images from public webcams"""
    
    def __init__(self):
        self.webcams: Dict[str, WebcamLocation] = {}
        self.cv_analyzer = ComputerVisionAnalyzer()
        self.redis_client: Optional[redis.Redis] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self.ingestion_interval = 60  # seconds
        
        # Sample webcam locations (in a real implementation, this would come from a database)
        self._initialize_sample_webcams()
    
    def _initialize_sample_webcams(self):
        """Initialize with sample webcam locations for demonstration"""
        sample_webcams = [
            {
                "id": "nyc_times_square",
                "name": "Times Square, NYC",
                "latitude": 40.7580,
                "longitude": -73.9855,
                "url": "https://example.com/nyc_times_square.jpg",  # Placeholder URL
                "city": "New York",
                "country": "USA",
                "description": "Times Square webcam showing pedestrian area"
            },
            {
                "id": "london_trafalgar",
                "name": "Trafalgar Square, London",
                "latitude": 51.5080,
                "longitude": -0.1281,
                "url": "https://example.com/london_trafalgar.jpg",  # Placeholder URL
                "city": "London",
                "country": "UK",
                "description": "Trafalgar Square webcam showing central London"
            },
            {
                "id": "paris_eiffel",
                "name": "Eiffel Tower, Paris",
                "latitude": 48.8584,
                "longitude": 2.2945,
                "url": "https://example.com/paris_eiffel.jpg",  # Placeholder URL
                "city": "Paris",
                "country": "France",
                "description": "Eiffel Tower area webcam"
            },
            {
                "id": "tokyo_shibuya",
                "name": "Shibuya Crossing, Tokyo",
                "latitude": 35.6595,
                "longitude": 139.7004,
                "url": "https://example.com/tokyo_shibuya.jpg",  # Placeholder URL
                "city": "Tokyo",
                "country": "Japan",
                "description": "Shibuya crossing webcam"
            }
        ]
        
        for webcam_data in sample_webcams:
            webcam = WebcamLocation(**webcam_data)
            self.webcams[webcam.id] = webcam
    
    async def initialize(self, redis_url: str = "redis://localhost:6379"):
        """Initialize the service with Redis connection"""
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            await self.redis_client.ping()
            logger.info("WebcamIngestionService initialized with Redis")
        except Exception as e:
            logger.error(f"Failed to initialize Redis connection: {e}")
            self.redis_client = None
    
    async def start_continuous_ingestion(self):
        """Start continuous ingestion of webcam images"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        logger.info("Starting continuous webcam ingestion...")
        
        while True:
            try:
                await self.ingest_all_webcams()
                await asyncio.sleep(self.ingestion_interval)
            except Exception as e:
                logger.error(f"Error in continuous ingestion: {e}")
                await asyncio.sleep(10)  # Wait before retrying
    
    async def ingest_all_webcams(self):
        """Ingest images from all webcams concurrently"""
        tasks = []
        for webcam_id in self.webcams.keys():
            task = asyncio.create_task(self.ingest_webcam(webcam_id))
            tasks.append(task)
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            logger.info(f"Ingested {len(results)} webcam images")
    
    async def ingest_webcam(self, webcam_id: str) -> Optional[AnalysisResult]:
        """Ingest and analyze a single webcam image"""
        if webcam_id not in self.webcams:
            logger.warning(f"Webcam {webcam_id} not found")
            return None
        
        webcam = self.webcams[webcam_id]
        
        try:
            # Fetch image from webcam
            image_data = await self._fetch_webcam_image(webcam.url)
            if not image_data:
                logger.warning(f"Failed to fetch image from {webcam_id}")
                return None
            
            # Analyze the image using computer vision
            analysis_result = await self._analyze_image(webcam_id, image_data)
            if not analysis_result:
                logger.warning(f"Failed to analyze image from {webcam_id}")
                return None
            
            # Store result in Redis
            if self.redis_client:
                await self._store_analysis_result(webcam_id, analysis_result)
            
            logger.info(f"Successfully processed webcam {webcam_id}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error processing webcam {webcam_id}: {e}")
            return None
    
    async def _fetch_webcam_image(self, url: str) -> Optional[bytes]:
        """Fetch image data from webcam URL"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            # For demonstration, we'll create a synthetic image
            # In a real implementation, this would fetch from actual webcam URLs
            synthetic_image = self._create_synthetic_image()
            return synthetic_image
        except Exception as e:
            logger.error(f"Error fetching image from {url}: {e}")
            return None
    
    def _create_synthetic_image(self) -> bytes:
        """Create a synthetic image for demonstration purposes"""
        # Create a 640x480 image
        width, height = 640, 480
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Add some random rectangles to simulate sun/shadow patterns
        for _ in range(random.randint(5, 15)):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = x1 + random.randint(20, 100)
            y2 = y1 + random.randint(20, 100)
            
            # Randomly choose between light (sun) and dark (shadow) colors
            if random.random() > 0.5:
                color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
            else:
                color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
            
            draw.rectangle([x1, y1, x2, y2], fill=color)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()
    
    async def _analyze_image(self, webcam_id: str, image_data: bytes) -> Optional[AnalysisResult]:
        """Analyze image using computer vision"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Analyze using CV
            analysis = self.cv_analyzer.analyze_image(image)
            
            # Create analysis result
            result = AnalysisResult(
                webcam_id=webcam_id,
                timestamp=datetime.now(),
                sun_exposure=analysis["sun_exposure"],
                shadow_percentage=analysis["shadow_percentage"],
                wetness_score=analysis["wetness_score"],
                weather_condition=analysis["weather_condition"],
                confidence=analysis["confidence"],
                metadata=analysis.get("metadata", {})
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing image for {webcam_id}: {e}")
            return None
    
    async def _store_analysis_result(self, webcam_id: str, result: AnalysisResult):
        """Store analysis result in Redis"""
        try:
            key = f"analysis:{webcam_id}"
            value = result.json()
            await self.redis_client.set(key, value, ex=3600)  # Expire in 1 hour
            logger.debug(f"Stored analysis result for {webcam_id} in Redis")
        except Exception as e:
            logger.error(f"Error storing analysis result in Redis: {e}")
    
    def get_webcam_list(self) -> List[WebcamLocation]:
        """Get list of all webcams"""
        return list(self.webcams.values())
    
    async def analyze_all_webcams(self) -> List[AnalysisResult]:
        """Analyze all webcams and return results"""
        results = []
        for webcam_id in self.webcams.keys():
            result = await self.ingest_webcam(webcam_id)
            if result:
                results.append(result)
        return results
    
    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
        if self.redis_client:
            await self.redis_client.close()