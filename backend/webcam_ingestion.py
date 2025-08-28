"""
Webcam Data Ingestion Module
Handles fetching images from public webcams using asyncio and aiohttp
"""

import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
import base64
from PIL import Image
import io

logger = logging.getLogger(__name__)

class WebcamIngestion:
    """Handles webcam data ingestion from public sources"""
    
    def __init__(self):
        self.webcams = self._load_webcam_config()
        self.session: Optional[aiohttp.ClientSession] = None
    
    def _load_webcam_config(self) -> List[Dict[str, Any]]:
        """Load webcam configuration - in production this would be from a database"""
        return [
            {
                'webcam_id': 'nyc_times_square',
                'name': 'New York - Times Square',
                'url': 'https://images-webcams.windy.com/90/1593596090/current/icon/1593596090.jpg',
                'location': {
                    'lat': 40.7580,
                    'lng': -73.9855,
                    'city': 'New York',
                    'country': 'USA'
                },
                'update_interval': 60
            },
            {
                'webcam_id': 'london_tower_bridge',
                'name': 'London - Tower Bridge',
                'url': 'https://images-webcams.windy.com/12/1269348812/current/icon/1269348812.jpg',
                'location': {
                    'lat': 51.5055,
                    'lng': -0.0754,
                    'city': 'London',
                    'country': 'UK'
                },
                'update_interval': 60
            },
            {
                'webcam_id': 'tokyo_shibuya',
                'name': 'Tokyo - Shibuya Crossing',
                'url': 'https://images-webcams.windy.com/47/1584692947/current/icon/1584692947.jpg',
                'location': {
                    'lat': 35.6598,
                    'lng': 139.7006,
                    'city': 'Tokyo',
                    'country': 'Japan'
                },
                'update_interval': 60
            },
            {
                'webcam_id': 'paris_eiffel',
                'name': 'Paris - Eiffel Tower',
                'url': 'https://images-webcams.windy.com/85/1441619285/current/icon/1441619285.jpg',
                'location': {
                    'lat': 48.8584,
                    'lng': 2.2945,
                    'city': 'Paris',
                    'country': 'France'
                },
                'update_interval': 60
            },
            {
                'webcam_id': 'sydney_harbor',
                'name': 'Sydney - Harbor Bridge',
                'url': 'https://images-webcams.windy.com/20/1441895820/current/icon/1441895820.jpg',
                'location': {
                    'lat': -33.8523,
                    'lng': 151.2108,
                    'city': 'Sydney',
                    'country': 'Australia'
                },
                'update_interval': 60
            }
        ]
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers={
                    'User-Agent': 'Urban-Microclimate-Monitor/1.0'
                }
            )
        return self.session
    
    async def fetch_webcam_image(self, webcam: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch image from a single webcam"""
        session = await self._get_session()
        
        try:
            async with session.get(webcam['url']) as response:
                if response.status == 200:
                    image_data = await response.read()
                    
                    # Validate it's actually an image
                    try:
                        img = Image.open(io.BytesIO(image_data))
                        img.verify()
                        
                        # Convert to base64 for JSON serialization
                        image_b64 = base64.b64encode(image_data).decode('utf-8')
                        
                        return {
                            'webcam_id': webcam['webcam_id'],
                            'name': webcam['name'],
                            'location': webcam['location'],
                            'image_data': image_data,  # Raw bytes for CV processing
                            'image_b64': image_b64,   # Base64 for API responses
                            'image_url': webcam['url'],
                            'timestamp': datetime.now().isoformat(),
                            'status': 'success',
                            'image_size': len(image_data)
                        }
                    except Exception as e:
                        logger.error(f"Invalid image from {webcam['webcam_id']}: {e}")
                        return self._create_error_result(webcam, f"Invalid image: {e}")
                else:
                    logger.warning(f"HTTP {response.status} for {webcam['webcam_id']}")
                    return self._create_error_result(webcam, f"HTTP {response.status}")
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching {webcam['webcam_id']}")
            return self._create_error_result(webcam, "Timeout")
        except Exception as e:
            logger.error(f"Error fetching {webcam['webcam_id']}: {e}")
            return self._create_error_result(webcam, str(e))
    
    def _create_error_result(self, webcam: Dict[str, Any], error: str) -> Dict[str, Any]:
        """Create error result for failed webcam fetch"""
        return {
            'webcam_id': webcam['webcam_id'],
            'name': webcam['name'],
            'location': webcam['location'],
            'image_data': None,
            'image_b64': None,
            'image_url': webcam['url'],
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': error
        }
    
    async def fetch_all_webcams(self) -> List[Dict[str, Any]]:
        """Fetch images from all configured webcams concurrently"""
        logger.info(f"Fetching images from {len(self.webcams)} webcams")
        
        # Use asyncio.gather for concurrent fetching
        tasks = [self.fetch_webcam_image(webcam) for webcam in self.webcams]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log them
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Exception for webcam {self.webcams[i]['webcam_id']}: {result}")
                valid_results.append(self._create_error_result(self.webcams[i], str(result)))
            else:
                valid_results.append(result)
        
        successful = len([r for r in valid_results if r['status'] == 'success'])
        logger.info(f"Successfully fetched {successful}/{len(self.webcams)} webcam images")
        
        return valid_results
    
    async def get_webcam_list(self) -> List[Dict[str, Any]]:
        """Get list of configured webcams (metadata only)"""
        return [{
            'webcam_id': webcam['webcam_id'],
            'name': webcam['name'],
            'location': webcam['location'],
            'update_interval': webcam['update_interval']
        } for webcam in self.webcams]
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    def __del__(self):
        """Cleanup session on deletion"""
        if hasattr(self, 'session') and self.session and not self.session.closed:
            asyncio.create_task(self.session.close())