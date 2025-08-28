import cv2
import numpy as np
from pathlib import Path
from typing import Dict

def analyze_sun_shadow(image_path: str) -> Dict[str, float]:
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Cannot read image {image_path}")
    # threshold to binary: pixels above 127 assumed sun (white), below shadow (black)
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    total_pixels = thresh.size
    sun_pixels = np.count_nonzero(thresh == 255)
    shadow_pixels = total_pixels - sun_pixels
    sun_exposure = sun_pixels / total_pixels if total_pixels else 0.0
    return {
        "sun_exposure": round(sun_exposure, 4),
        "shadow_ratio": round(shadow_pixels / total_pixels if total_pixels else 0.0, 4),
    }

if __name__ == "__main__":
    test_image = "/workspace/data/raw/sample.jpg"  # replace
    print(analyze_sun_shadow(test_image))