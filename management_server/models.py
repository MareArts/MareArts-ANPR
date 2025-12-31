"""
Data Models for MareArts ANPR Server
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class DetectionResult(BaseModel):
    """Single plate detection result"""
    plate_text: str
    confidence: float
    bbox: List[int]  # [x1, y1, x2, y2] - converted from 'ltrb'
    detection_confidence: float


class ANPRResponse(BaseModel):
    """ANPR API response"""
    success: bool
    detection_id: Optional[int] = None
    timestamp: str
    results: List[DetectionResult]
    processing_time: float
    detector_time: float
    ocr_time: float
    image_url: Optional[str] = None
    error: Optional[str] = None


class Base64ImageRequest(BaseModel):
    """Request model for base64 image"""
    image: str  # Base64 encoded image
    save_result: bool = True


class DetectionHistory(BaseModel):
    """Detection history entry"""
    id: int
    timestamp: str
    num_plates: int
    plates: List[str]
    confidences: List[float]
    processing_time: float
    image_path: Optional[str] = None
    thumbnail_path: Optional[str] = None


class ServerStats(BaseModel):
    """Server statistics"""
    total_detections: int
    total_plates_detected: int
    avg_processing_time: float
    avg_confidence: float
    uptime: float
    today_count: int
    success_rate: float

