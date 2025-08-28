from __future__ import annotations

import io
import time
from typing import Tuple

import cv2
import numpy as np


def compute_sun_exposure_from_bytes(image_bytes: bytes) -> Tuple[float, int, int]:
    """Compute simple sun exposure metric using grayscale thresholding.

    Returns:
        sun_exposure: float between 0 and 1 (higher = more bright pixels)
        width: image width
        height: image height
    """
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if img is None:
        # Could not decode; default neutral value
        return 0.5, 0, 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Otsu thresholding to separate bright vs dark
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    white_pixels = float(np.count_nonzero(thresh))
    total_pixels = float(thresh.size)
    sun_exposure = white_pixels / total_pixels if total_pixels else 0.5

    h, w = gray.shape
    return float(sun_exposure), int(w), int(h)