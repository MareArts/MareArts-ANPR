#!/usr/bin/env python3
"""
Process Images from Memory - For Integration with Existing Software

This example shows how to process images directly from memory without
saving to disk. Perfect for:
- Visual Studio integration
- Real-time camera feeds
- Existing software integration
- Parking/access control systems

Author: MareArts
"""

from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v14
from marearts_anpr import marearts_anpr_from_cv2, marearts_anpr_from_pil
import numpy as np
import cv2
from PIL import Image
import io

# ============================================================================
# CONFIGURATION
# ============================================================================

# Load credentials (configure with: ma-anpr config)
# This automatically loads from ~/.marearts/.marearts_env

import os
from pathlib import Path

def load_credentials():
    """Load credentials from environment or config file"""
    user = os.getenv('MAREARTS_ANPR_USERNAME')
    key = os.getenv('MAREARTS_ANPR_SERIAL_KEY')
    sig = os.getenv('MAREARTS_ANPR_SIGNATURE')
    
    if not all([user, key, sig]):
        config_file = Path.home() / '.marearts' / '.marearts_env'
        if config_file.exists():
            with open(config_file) as f:
                for line in f:
                    if 'MAREARTS_ANPR_USERNAME=' in line:
                        user = line.split('=')[1].strip().strip('"')
                    elif 'MAREARTS_ANPR_SERIAL_KEY=' in line:
                        key = line.split('=')[1].strip().strip('"')
                    elif 'MAREARTS_ANPR_SIGNATURE=' in line:
                        sig = line.split('=')[1].strip().strip('"')
    
    return user, key, sig

USER_NAME, SERIAL_KEY, SIGNATURE = load_credentials()

if not all([USER_NAME, SERIAL_KEY, SIGNATURE]):
    print("❌ No credentials found!")
    print("\n1. Run: ma-anpr config")
    print("2. Enter your username, serial key, and signature")
    print("3. Then run this script again")
    exit(1)

# Model configuration
DETECTOR_MODEL = "medium_640p_fp32"  # Recommended for parking systems
OCR_MODEL = "small_fp32"             # Good balance
REGION = "eup"                       # European plates
BACKEND = "cpu"                      # Use "cuda" if GPU available

# Confidence thresholds
CONF_THRESHOLD = 0.25  # Lower for parking (catch all vehicles)

# ============================================================================
# INITIALIZE MODELS (Do this ONCE at startup, reuse for all images)
# ============================================================================

print("Initializing MareArts ANPR...")
print(f"Model: {DETECTOR_MODEL} / {OCR_MODEL}")
print(f"Region: {REGION}")
print(f"Backend: {BACKEND}")

# Create detector with confidence threshold
detector = ma_anpr_detector_v14(
    DETECTOR_MODEL,
    USER_NAME,
    SERIAL_KEY,
    SIGNATURE,
    backend=BACKEND,
    conf_thres=CONF_THRESHOLD,  # Detection confidence (0.15-0.60)
    iou_thres=0.5               # Overlap threshold
)

# Create OCR
ocr = ma_anpr_ocr_v14(
    OCR_MODEL,
    REGION,
    USER_NAME,
    SERIAL_KEY,
    SIGNATURE,
    backend=BACKEND
)

# 💡 Dynamic region switching (no reload needed!):
# ocr.set_region('eup')   # European plates
# ocr.set_region('kr')    # Korean plates
# ocr.set_region('na')    # North American plates
# ocr.set_region('cn')    # Chinese plates
# ocr.set_region('univ')  # Universal (all regions)
# Saves ~180MB memory per region vs creating multiple OCR instances!

print("✅ Models loaded and ready!\n")

# ============================================================================
# METHOD 1: From NumPy Array (OpenCV - Most Common)
# ============================================================================

def process_from_opencv(image_array):
    """
    Process image from OpenCV numpy array
    
    Args:
        image_array: np.ndarray from cv2.imread() or camera capture
    
    Returns:
        dict with detection results
    """
    print("Method 1: Processing from NumPy array (OpenCV)")
    
    # Use marearts_anpr_from_cv2() - accepts OpenCV numpy array
    result = marearts_anpr_from_cv2(detector, ocr, image_array)
    
    return result

# Example usage with OpenCV:
# image = cv2.imread("plate.jpg")  # Or from camera: image = cap.read()
# result = process_from_opencv(image)

# ============================================================================
# METHOD 2: From PIL Image
# ============================================================================

def process_from_pil(pil_image):
    """
    Process image from PIL Image object
    
    Args:
        pil_image: PIL.Image object
    
    Returns:
        dict with detection results
    """
    print("Method 2: Processing from PIL Image")
    
    # Use marearts_anpr_from_pil() - accepts PIL Image directly
    result = marearts_anpr_from_pil(detector, ocr, pil_image)
    
    return result

# Example usage with PIL:
# from PIL import Image
# pil_image = Image.open("plate.jpg")  # Or from memory stream
# result = process_from_pil(pil_image)

# ============================================================================
# METHOD 3: From Bytes/Stream (For HTTP uploads, database BLOBs)
# ============================================================================

def process_from_bytes(image_bytes):
    """
    Process image from raw bytes
    
    Args:
        image_bytes: bytes object (JPEG, PNG, etc.)
    
    Returns:
        dict with detection results
    """
    print("Method 3: Processing from bytes stream")
    
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Process
    result = marearts_anpr_from_cv2(detector, ocr, image)
    
    return result

# Example usage with bytes:
# with open("plate.jpg", "rb") as f:
#     image_bytes = f.read()
# result = process_from_bytes(image_bytes)

# ============================================================================
# METHOD 4: From Base64 String (For web APIs)
# ============================================================================

def process_from_base64(base64_string):
    """
    Process image from base64 encoded string
    
    Args:
        base64_string: Base64 encoded image data
    
    Returns:
        dict with detection results
    """
    print("Method 4: Processing from base64 string")
    
    import base64
    
    # Decode base64 to bytes
    image_bytes = base64.b64decode(base64_string)
    
    # Convert to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Process
    result = marearts_anpr_from_cv2(detector, ocr, image)
    
    return result

# ============================================================================
# METHOD 5: From Camera/Video Stream (Real-time)
# ============================================================================

def process_video_stream(camera_id=0, num_frames=10):
    """
    Process frames from camera/video stream
    
    Args:
        camera_id: Camera index or video file path
        num_frames: Number of frames to process
    
    Returns:
        list of results
    """
    print(f"Method 5: Processing from video stream (camera {camera_id})")
    
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print("❌ Failed to open camera")
        return []
    
    results = []
    frame_count = 0
    
    while frame_count < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame directly from memory
        result = marearts_anpr_from_cv2(detector, ocr, frame)
        
        if result and result.get('results'):
            print(f"Frame {frame_count}: Found {len(result['results'])} plates")
            for plate in result['results']:
                print(f"  → {plate['ocr']} ({plate['ocr_conf']}%)")
            results.append(result)
        
        frame_count += 1
    
    cap.release()
    return results

# ============================================================================
# DEMO - Test All Methods
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("MAREARTS ANPR - Process Images from Memory")
    print("="*70)
    print("\nThis example shows 5 ways to process images WITHOUT saving to disk")
    print("Perfect for Visual Studio integration and real-time systems!\n")
    
    # Check if we have sample images
    import os
    sample_images = [
        "../sample_images/eu-a.jpg",
        "../sample_images/kr-a.jpg",
        "test_image.jpg"
    ]
    
    test_image = None
    for path in sample_images:
        if os.path.exists(path):
            test_image = path
            break
    
    if not test_image:
        print("⚠️  No sample images found")
        print("Place a test image and update the path in this script")
        print("\nExample code structure is shown above - adapt for your use case!")
        exit(0)
    
    print(f"Using test image: {test_image}\n")
    print("="*70)
    
    # Method 1: OpenCV (numpy array)
    print("\nMETHOD 1: OpenCV (numpy array)")
    print("-"*70)
    image_cv = cv2.imread(test_image)
    result1 = process_from_opencv(image_cv)
    print(f"Result: {result1.get('results', [])[:1]}")  # Show first result
    
    # Method 2: PIL Image
    print("\n" + "="*70)
    print("\nMETHOD 2: PIL Image")
    print("-"*70)
    pil_image = Image.open(test_image)
    result2 = process_from_pil(pil_image)
    print(f"Result: {result2.get('results', [])[:1]}")
    
    # Method 3: Bytes
    print("\n" + "="*70)
    print("\nMETHOD 3: Raw bytes (memory stream)")
    print("-"*70)
    with open(test_image, "rb") as f:
        image_bytes = f.read()
    result3 = process_from_bytes(image_bytes)
    print(f"Result: {result3.get('results', [])[:1]}")
    
    # Method 4: Base64 (for web APIs)
    print("\n" + "="*70)
    print("\nMETHOD 4: Base64 string (web APIs)")
    print("-"*70)
    import base64
    with open(test_image, "rb") as f:
        base64_string = base64.b64encode(f.read()).decode('utf-8')
    result4 = process_from_base64(base64_string)
    print(f"Result: {result4.get('results', [])[:1]}")
    
    print("\n" + "="*70)
    print("\n✅ All methods work! Images processed from memory.")
    print("\n💡 For Visual Studio / C# integration:")
    print("   1. Use Python.NET or IronPython")
    print("   2. Or create REST API with this Python code")
    print("   3. Or use Windows DLL wrapper")
    print("\n📧 Contact hello@marearts.com for C#/Visual Studio integration help")
    print("="*70)

