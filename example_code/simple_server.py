#!/usr/bin/env python3
"""
Simple ANPR Server - Process Images from Memory

Minimal server using V14 Detector + V15 OCR (latest).
Loads models once and processes images from memory.
Perfect for integration with Visual Studio, C#, or any HTTP client.

Requirements:
    pip install marearts-anpr              # ANPR library
    pip install fastapi uvicorn            # Web server
    pip install python-multipart           # For file uploads

Setup:
    ma-anpr config                         # Configure credentials

Run:
    python simple_server.py

Test:
    curl -X POST http://localhost:8000/detect -F "image=@plate.jpg"
"""

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr, marearts_anpr_from_cv2
import cv2
import numpy as np
import os
import base64

# ============================================================================
# CONFIGURATION
# ============================================================================

USER = os.getenv('MAREARTS_ANPR_USERNAME')
KEY = os.getenv('MAREARTS_ANPR_SERIAL_KEY')
SIG = os.getenv('MAREARTS_ANPR_SIGNATURE')

if not all([USER, KEY, SIG]):
    print("❌ Credentials not found!")
    print("Run: ma-anpr config")
    print("Or: source ~/.marearts/.marearts_env")
    exit(1)

# Settings
DETECTOR_MODEL = "medium_640p_fp32"  # V14 Detector: pico/micro/small/medium/large_640p_fp32
OCR_MODEL = "small_fp32"              # OCR models: pico/micro/small/medium/large_fp32 or _int8
OCR_VERSION = "v15"                   # v15 (latest, recommended) or v14 (backward compatible)
REGION = "euplus"                     # Regions: kor/kr, euplus/eup, na, china/cn, univ
BACKEND = "cpu"                       # cpu, cuda, directml (change to "cuda" if GPU available)
CONFIDENCE = 0.20

# ============================================================================
# LOAD MODELS (Once at startup)
# ============================================================================

print("="*70)
print("Starting ANPR Server...")
print("="*70)

print(f"\nLoading models...")
print(f"  Detector: {DETECTOR_MODEL} (V14)")
print(f"  OCR: {OCR_MODEL} ({OCR_VERSION.upper()})")
print(f"  Region: {REGION}")
print(f"  Backend: {BACKEND}")

# Load detector
detector = ma_anpr_detector_v14(
    DETECTOR_MODEL, USER, KEY, SIG,
    backend=BACKEND,
    conf_thres=CONFIDENCE,
    iou_thres=0.5
)

# Load OCR (unified interface - easily switch v14/v15)
ocr = ma_anpr_ocr(
    model=OCR_MODEL, 
    region=REGION, 
    user_name=USER, 
    serial_key=KEY, 
    signature=SIG, 
    version=OCR_VERSION,  # Change OCR_VERSION above to switch between v15 and v14
    backend=BACKEND
)

# Alternative: Direct import for specific version
# from marearts_anpr import ma_anpr_ocr_v15
# ocr = ma_anpr_ocr_v15(OCR_MODEL, REGION, USER, KEY, SIG, backend=BACKEND)

print("✅ Models loaded and ready!")
print("="*70)

# ============================================================================
# CREATE SERVER
# ============================================================================

app = FastAPI(title="MareArts ANPR Server")

# Request model for base64
class Base64Image(BaseModel):
    image: str  # Base64 encoded image

@app.post("/detect")
async def detect_plate_file(image: UploadFile = File(...)):
    """
    Method 1: Upload image file (multipart/form-data)
    
    Example:
        curl -X POST http://localhost:8000/detect -F "image=@plate.jpg"
    """
    image_bytes = await image.read()
    return process_image_bytes(image_bytes)

@app.post("/detect/binary")
async def detect_plate_binary(request: Request):
    """
    Method 2: Send raw image bytes in request body
    
    Example (Python):
        with open('plate.jpg', 'rb') as f:
            requests.post('http://localhost:8000/detect/binary', data=f.read())
    
    Example (C#):
        var content = new ByteArrayContent(imageBytes);
        content.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
        await client.PostAsync("http://localhost:8000/detect/binary", content);
    """
    image_bytes = await request.body()
    return process_image_bytes(image_bytes)

@app.post("/detect/base64")
async def detect_plate_base64(data: Base64Image):
    """
    Method 3: Send base64 encoded image in JSON
    
    Example (Python):
        import base64
        with open('plate.jpg', 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        requests.post('http://localhost:8000/detect/base64', 
                     json={'image': b64})
    
    Example (C#):
        var base64Image = Convert.ToBase64String(imageBytes);
        var json = JsonSerializer.Serialize(new { image = base64Image });
        await client.PostAsync("http://localhost:8000/detect/base64", 
                              new StringContent(json, Encoding.UTF8, "application/json"));
    """
    try:
        image_bytes = base64.b64decode(data.image)
        return process_image_bytes(image_bytes)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid base64: {str(e)}"}
        )

def process_image_bytes(image_bytes):
    """Process image from bytes"""
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid image format"}
        )
    
    # Process with ANPR (models already loaded!)
    result = marearts_anpr_from_cv2(detector, ocr, img)
    return result

@app.get("/")
def root():
    """Server info"""
    return {
        "service": "MareArts ANPR Server",
        "version": "1.0",
        "model": DETECTOR_MODEL,
        "region": REGION,
        "status": "ready"
    }

@app.get("/health")
def health():
    """Health check"""
    return {"status": "ok", "models": "loaded"}

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("🚀 Server starting on http://localhost:8000")
    print("="*70)
    print("\nEndpoints:")
    print("  POST /detect          - Upload file (multipart/form-data)")
    print("  POST /detect/binary   - Send raw bytes (application/octet-stream)")
    print("  POST /detect/base64   - Send base64 JSON")
    print("  GET  /                - Server info")
    print("  GET  /health          - Health check")
    print("\nExamples:")
    print('  curl -X POST http://localhost:8000/detect -F "image=@plate.jpg"')
    print('  curl -X POST http://localhost:8000/detect/binary --data-binary "@plate.jpg"')
    print("\nTest client:")
    print("  python test_server.py plate.jpg")
    print("\nPress Ctrl+C to stop")
    print("="*70)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

