"""
Computer Vision Analysis Module
Uses OpenCV for sun/shadow detection and micro-climate analysis
"""

import cv2
import numpy as np
import logging
from typing import Dict, Any, Tuple, Optional
from PIL import Image
import io
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class ComputerVisionAnalyzer:
    """Handles computer vision analysis for micro-climate detection"""
    
    def __init__(self):
        self.min_contour_area = 100  # Minimum area for shadow/sun regions
    
    async def analyze_image(self, image_data: bytes, location: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze webcam image for micro-climate conditions
        
        Args:
            image_data: Raw image bytes
            location: Location metadata
            
        Returns:
            Analysis results with sun/shadow percentages and conditions
        """
        try:
            # Convert bytes to OpenCV image
            image_array = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            
            if image is None:
                return self._create_error_result("Failed to decode image")
            
            # Perform sun/shadow analysis
            sun_shadow_analysis = await self._analyze_sun_shadow(image)
            
            # Additional analysis
            brightness_analysis = await self._analyze_brightness(image)
            weather_indicators = await self._detect_weather_indicators(image)
            
            # Combine all analyses
            analysis = {
                'timestamp': datetime.now().isoformat(),
                'location': location,
                'sun_shadow': sun_shadow_analysis,
                'brightness': brightness_analysis,
                'weather': weather_indicators,
                'micro_climate_score': self._calculate_micro_climate_score(
                    sun_shadow_analysis, brightness_analysis, weather_indicators
                )
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"CV analysis error: {e}")
            return self._create_error_result(str(e))
    
    async def _analyze_sun_shadow(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze sun/shadow patterns in the image"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Calculate adaptive threshold for better shadow detection
            adaptive_thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Simple threshold for bright areas (sun exposure)
            _, bright_thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
            
            # Simple threshold for dark areas (shadows)
            _, dark_thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY_INV)
            
            # Calculate percentages
            total_pixels = gray.shape[0] * gray.shape[1]
            bright_pixels = np.sum(bright_thresh == 255)
            dark_pixels = np.sum(dark_thresh == 255)
            
            sun_exposure = (bright_pixels / total_pixels) * 100
            shadow_coverage = (dark_pixels / total_pixels) * 100
            
            # Analyze distribution patterns
            sun_regions = self._find_contours_and_areas(bright_thresh)
            shadow_regions = self._find_contours_and_areas(dark_thresh)
            
            return {
                'sun_exposure_percent': round(sun_exposure, 2),
                'shadow_coverage_percent': round(shadow_coverage, 2),
                'sun_regions_count': len(sun_regions),
                'shadow_regions_count': len(shadow_regions),
                'largest_sun_area': max(sun_regions) if sun_regions else 0,
                'largest_shadow_area': max(shadow_regions) if shadow_regions else 0,
                'sun_shadow_ratio': round(sun_exposure / max(shadow_coverage, 1), 2)
            }
            
        except Exception as e:
            logger.error(f"Sun/shadow analysis error: {e}")
            return {'error': str(e)}
    
    async def _analyze_brightness(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze overall brightness and contrast"""
        try:
            # Convert to grayscale for brightness analysis
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calculate brightness metrics
            mean_brightness = np.mean(gray)
            std_brightness = np.std(gray)
            
            # Calculate histogram for distribution analysis
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            
            # Brightness classification
            if mean_brightness > 180:
                brightness_level = "very_bright"
            elif mean_brightness > 140:
                brightness_level = "bright"
            elif mean_brightness > 100:
                brightness_level = "moderate"
            elif mean_brightness > 60:
                brightness_level = "dim"
            else:
                brightness_level = "dark"
            
            # Contrast analysis
            contrast = std_brightness
            if contrast > 60:
                contrast_level = "high"
            elif contrast > 40:
                contrast_level = "moderate"
            else:
                contrast_level = "low"
            
            return {
                'mean_brightness': round(float(mean_brightness), 2),
                'brightness_std': round(float(std_brightness), 2),
                'brightness_level': brightness_level,
                'contrast_level': contrast_level,
                'dynamic_range': int(np.max(gray) - np.min(gray))
            }
            
        except Exception as e:
            logger.error(f"Brightness analysis error: {e}")
            return {'error': str(e)}
    
    async def _detect_weather_indicators(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect weather indicators like clouds, rain, fog"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect potential cloud coverage using texture analysis
            # Apply Sobel operator for edge detection
            sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
            
            # High-frequency texture analysis for clouds
            texture_variance = np.var(sobel_magnitude)
            
            # Analyze color channels for weather indicators
            b, g, r = cv2.split(image)
            
            # Blue channel dominance might indicate clear sky
            blue_dominance = np.mean(b) / (np.mean(g) + np.mean(r) + 1)
            
            # Gray uniformity might indicate overcast
            color_uniformity = 1 - (np.std([np.mean(b), np.mean(g), np.mean(r)]) / 255)
            
            # Weather classification (simplified)
            if blue_dominance > 0.6 and texture_variance < 1000:
                weather_condition = "clear"
                cloud_coverage = "low"
            elif color_uniformity > 0.8:
                weather_condition = "overcast"
                cloud_coverage = "high"
            elif texture_variance > 1500:
                weather_condition = "partly_cloudy"
                cloud_coverage = "moderate"
            else:
                weather_condition = "variable"
                cloud_coverage = "moderate"
            
            return {
                'weather_condition': weather_condition,
                'cloud_coverage': cloud_coverage,
                'blue_dominance': round(float(blue_dominance), 2),
                'color_uniformity': round(float(color_uniformity), 2),
                'texture_variance': round(float(texture_variance), 2)
            }
            
        except Exception as e:
            logger.error(f"Weather detection error: {e}")
            return {'error': str(e)}
    
    def _find_contours_and_areas(self, binary_image: np.ndarray) -> list:
        """Find contours and return their areas"""
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        areas = [cv2.contourArea(contour) for contour in contours if cv2.contourArea(contour) > self.min_contour_area]
        return sorted(areas, reverse=True)
    
    def _calculate_micro_climate_score(self, sun_shadow: Dict, brightness: Dict, weather: Dict) -> Dict[str, Any]:
        """Calculate overall micro-climate comfort score"""
        try:
            # Base score calculation
            score = 50  # Start with neutral
            
            # Sun exposure impact
            sun_exposure = sun_shadow.get('sun_exposure_percent', 0)
            if 30 <= sun_exposure <= 70:  # Optimal sun exposure
                score += 20
            elif sun_exposure > 80:  # Too much sun
                score -= 15
            elif sun_exposure < 15:  # Too little sun
                score -= 10
            
            # Shadow coverage impact
            shadow_coverage = sun_shadow.get('shadow_coverage_percent', 0)
            if 20 <= shadow_coverage <= 50:  # Good shadow availability
                score += 15
            
            # Brightness impact
            brightness_level = brightness.get('brightness_level', 'moderate')
            if brightness_level in ['bright', 'moderate']:
                score += 10
            elif brightness_level in ['very_bright', 'dark']:
                score -= 10
            
            # Weather impact
            weather_condition = weather.get('weather_condition', 'variable')
            if weather_condition == 'clear':
                score += 15
            elif weather_condition == 'overcast':
                score -= 5
            elif weather_condition == 'partly_cloudy':
                score += 5
            
            # Normalize score to 0-100 range
            score = max(0, min(100, score))
            
            # Determine comfort level
            if score >= 80:
                comfort_level = "excellent"
            elif score >= 65:
                comfort_level = "good"
            elif score >= 45:
                comfort_level = "moderate"
            elif score >= 25:
                comfort_level = "poor"
            else:
                comfort_level = "very_poor"
            
            return {
                'score': round(score, 1),
                'comfort_level': comfort_level,
                'factors': {
                    'sun_exposure': sun_exposure,
                    'shadow_availability': shadow_coverage,
                    'brightness': brightness_level,
                    'weather': weather_condition
                }
            }
            
        except Exception as e:
            logger.error(f"Micro-climate score calculation error: {e}")
            return {'score': 50, 'comfort_level': 'unknown', 'error': str(e)}
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """Create error result for failed analysis"""
        return {
            'timestamp': datetime.now().isoformat(),
            'error': error_message,
            'status': 'failed'
        }