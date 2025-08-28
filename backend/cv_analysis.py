import cv2
import numpy as np
from PIL import Image
import logging
from typing import Dict, Any
from models import WeatherCondition

logger = logging.getLogger(__name__)

class ComputerVisionAnalyzer:
    """Computer vision analyzer for micro-climate conditions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Thresholds for analysis
        self.brightness_threshold = 128  # Threshold for sun vs shadow detection
        self.wetness_threshold = 0.3     # Threshold for wetness detection
        self.confidence_threshold = 0.7  # Minimum confidence for reliable analysis
    
    def analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze an image for micro-climate conditions
        
        Args:
            image: PIL Image object to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Convert PIL image to OpenCV format
            cv_image = self._pil_to_cv(image)
            
            # Perform analysis
            sun_exposure = self._analyze_sun_exposure(cv_image)
            shadow_percentage = 1.0 - sun_exposure
            wetness_score = self._analyze_wetness(cv_image)
            weather_condition = self._determine_weather_condition(sun_exposure, wetness_score)
            confidence = self._calculate_confidence(cv_image)
            
            # Additional metadata
            metadata = {
                "image_size": image.size,
                "brightness_mean": float(np.mean(cv_image)),
                "brightness_std": float(np.std(cv_image)),
                "contrast_score": self._calculate_contrast(cv_image)
            }
            
            return {
                "sun_exposure": sun_exposure,
                "shadow_percentage": shadow_percentage,
                "wetness_score": wetness_score,
                "weather_condition": weather_condition,
                "confidence": confidence,
                "metadata": metadata
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing image: {e}")
            return self._get_default_analysis()
    
    def _pil_to_cv(self, pil_image: Image.Image) -> np.ndarray:
        """Convert PIL Image to OpenCV format"""
        # Convert PIL image to RGB if it's not already
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Convert to numpy array
        cv_image = np.array(pil_image)
        
        # Convert RGB to BGR (OpenCV format)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        
        return cv_image
    
    def _analyze_sun_exposure(self, cv_image: np.ndarray) -> float:
        """
        Analyze sun exposure by detecting bright vs dark areas
        
        Args:
            cv_image: OpenCV image in BGR format
            
        Returns:
            Float between 0.0 and 1.0 representing sun exposure
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply threshold to separate bright (sun) from dark (shadow) areas
            _, binary = cv2.threshold(blurred, self.brightness_threshold, 255, cv2.THRESH_BINARY)
            
            # Calculate percentage of bright pixels (sun exposure)
            total_pixels = binary.shape[0] * binary.shape[1]
            bright_pixels = np.sum(binary == 255)
            sun_exposure = bright_pixels / total_pixels
            
            # Normalize to 0.0-1.0 range
            sun_exposure = np.clip(sun_exposure, 0.0, 1.0)
            
            self.logger.debug(f"Sun exposure analysis: {sun_exposure:.3f}")
            return float(sun_exposure)
            
        except Exception as e:
            self.logger.error(f"Error in sun exposure analysis: {e}")
            return 0.5  # Default to neutral
    
    def _analyze_wetness(self, cv_image: np.ndarray) -> float:
        """
        Analyze wetness by detecting reflections and smooth surfaces
        
        Args:
            cv_image: OpenCV image in BGR format
            
        Returns:
            Float between 0.0 and 1.0 representing wetness likelihood
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Calculate Laplacian variance (measure of image sharpness)
            # Wet surfaces tend to be smoother and less sharp
            laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
            laplacian_var = np.var(laplacian)
            
            # Normalize variance to 0-1 range (lower variance = more likely wet)
            # This is a simplified approach - in practice, you'd need more sophisticated analysis
            max_var = 1000  # Empirical maximum variance for typical images
            normalized_var = np.clip(laplacian_var / max_var, 0.0, 1.0)
            
            # Invert so that lower variance (smoother) = higher wetness
            wetness_score = 1.0 - normalized_var
            
            # Apply threshold to make detection more conservative
            if wetness_score < self.wetness_threshold:
                wetness_score = 0.0
            
            self.logger.debug(f"Wetness analysis: {wetness_score:.3f}")
            return float(wetness_score)
            
        except Exception as e:
            self.logger.error(f"Error in wetness analysis: {e}")
            return 0.0  # Default to dry
    
    def _determine_weather_condition(self, sun_exposure: float, wetness_score: float) -> WeatherCondition:
        """
        Determine overall weather condition based on analysis results
        
        Args:
            sun_exposure: Sun exposure score (0.0-1.0)
            wetness_score: Wetness score (0.0-1.0)
            
        Returns:
            WeatherCondition enum value
        """
        try:
            # Simple rule-based classification
            if wetness_score > 0.5:
                return WeatherCondition.WET
            elif sun_exposure > 0.7:
                return WeatherCondition.SUNNY
            elif sun_exposure < 0.3:
                return WeatherCondition.SHADY
            else:
                return WeatherCondition.DRY
                
        except Exception as e:
            self.logger.error(f"Error determining weather condition: {e}")
            return WeatherCondition.UNKNOWN
    
    def _calculate_confidence(self, cv_image: np.ndarray) -> float:
        """
        Calculate confidence in the analysis based on image quality
        
        Args:
            cv_image: OpenCV image in BGR format
            
        Returns:
            Float between 0.0 and 1.0 representing confidence
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Calculate image quality metrics
            brightness_mean = np.mean(gray)
            brightness_std = np.std(gray)
            
            # High contrast (high std) and good brightness (not too dark/too bright) = high confidence
            contrast_score = np.clip(brightness_std / 128.0, 0.0, 1.0)
            brightness_score = 1.0 - abs(brightness_mean - 128) / 128.0
            
            # Combine scores
            confidence = (contrast_score + brightness_score) / 2.0
            
            # Ensure confidence is within bounds
            confidence = np.clip(confidence, 0.0, 1.0)
            
            self.logger.debug(f"Confidence calculation: {confidence:.3f}")
            return float(confidence)
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence: {e}")
            return 0.5  # Default to medium confidence
    
    def _calculate_contrast(self, cv_image: np.ndarray) -> float:
        """Calculate image contrast score"""
        try:
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            return float(np.std(gray) / 128.0)
        except Exception as e:
            self.logger.error(f"Error calculating contrast: {e}")
            return 0.5
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Return default analysis when errors occur"""
        return {
            "sun_exposure": 0.5,
            "shadow_percentage": 0.5,
            "wetness_score": 0.0,
            "weather_condition": WeatherCondition.UNKNOWN,
            "confidence": 0.0,
            "metadata": {
                "error": "Analysis failed, using default values"
            }
        }
    
    def enhance_analysis(self, base_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance analysis with additional insights
        
        Args:
            base_analysis: Base analysis results
            
        Returns:
            Enhanced analysis with additional insights
        """
        try:
            enhanced = base_analysis.copy()
            
            # Add comfort index (combination of sun and wetness)
            sun_exposure = enhanced.get("sun_exposure", 0.5)
            wetness_score = enhanced.get("wetness_score", 0.0)
            
            # Comfort decreases with extreme sun exposure and wetness
            comfort_score = 1.0 - (abs(sun_exposure - 0.5) + wetness_score) / 2.0
            comfort_score = max(0.0, comfort_score)
            
            enhanced["comfort_index"] = comfort_score
            
            # Add time-based recommendations
            if sun_exposure > 0.8:
                enhanced["recommendation"] = "High sun exposure - consider shade"
            elif wetness_score > 0.6:
                enhanced["recommendation"] = "Wet conditions detected - caution advised"
            elif comfort_score > 0.7:
                enhanced["recommendation"] = "Comfortable conditions"
            else:
                enhanced["recommendation"] = "Moderate conditions"
            
            return enhanced
            
        except Exception as e:
            self.logger.error(f"Error enhancing analysis: {e}")
            return base_analysis