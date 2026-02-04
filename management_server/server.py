#!/usr/bin/env python3
"""
MareArts ANPR Management Server
Professional ANPR server with REST API and Web Dashboard
"""
import time
import os
import cv2
import numpy as np
import base64
import shutil
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional
from collections import deque

from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr, marearts_anpr_from_cv2

import config
from database import db
from models import DetectionResult, ANPRResponse, Base64ImageRequest, ServerStats

# ============================================================================
# GLOBAL STATE
# ============================================================================

class ServerState:
    """Global server state"""
    def __init__(self):
        self.detector = None
        self.ocr = None
        self.start_time = time.time()
        self.request_count = 0
        self.credentials_valid = False
        self.log_queue = deque(maxlen=config.MAX_LOG_ENTRIES)  # Configurable retention
        self.log_subscribers = []  # SSE subscribers
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0

state = ServerState()

def add_server_log(message: str, level: str = "info"):
    """Add log entry to server log queue"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    full_timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "full_timestamp": full_timestamp,
        "message": message,
        "level": level
    }
    state.log_queue.append(log_entry)
    
    # Also print to console
    symbols = {
        "info": "ℹ",
        "success": "✓",
        "error": "✗",
        "warning": "⚠"
    }
    print(f"[{timestamp}] {symbols.get(level, 'ℹ')} {message}")
    
    # Notify all SSE subscribers
    for queue in state.log_subscribers:
        try:
            queue.put_nowait(log_entry)
        except:
            pass

# ============================================================================
# INITIALIZE MODELS
# ============================================================================

def init_models():
    """Initialize ANPR models"""
    print("="*70)
    print("MareArts ANPR Management Server")
    print("="*70)
    
    # Check credentials
    if not config.validate_credentials():
        print("\n⚠️  WARNING: Credentials not configured!")
        print("Set environment variables or configure via web interface")
        print("Server will start but ANPR detection will not work")
        print("\nRequired variables:")
        print("  - MAREARTS_ANPR_USERNAME")
        print("  - MAREARTS_ANPR_SERIAL_KEY")
        print("  - MAREARTS_ANPR_SIGNATURE")
        return False
    
    try:
        print(f"\n📦 Loading models...")
        print(f"  Detector: {config.DETECTOR_MODEL} (V14)")
        print(f"  OCR: {config.OCR_MODEL} ({config.OCR_VERSION.upper()})")
        print(f"  Region: {config.REGION}")
        print(f"  Backend: {config.BACKEND}")
        
        # Load detector
        state.detector = ma_anpr_detector_v14(
            config.DETECTOR_MODEL,
            config.MAREARTS_USERNAME,
            config.MAREARTS_SERIAL_KEY,
            config.MAREARTS_SIGNATURE,
            backend=config.BACKEND,
            conf_thres=config.CONFIDENCE_THRESHOLD,
            iou_thres=0.5
        )
        
        # Load OCR (unified interface - supports v14 and v15)
        state.ocr = ma_anpr_ocr(
            model=config.OCR_MODEL,
            region=config.REGION,
            user_name=config.MAREARTS_USERNAME,
            serial_key=config.MAREARTS_SERIAL_KEY,
            signature=config.MAREARTS_SIGNATURE,
            version=config.OCR_VERSION,  # v15 (default) or v14
            backend=config.BACKEND
        )
        
        print("✅ Models loaded successfully!")
        state.credentials_valid = True
        return True
        
    except Exception as e:
        print(f"\n❌ Error loading models: {e}")
        return False

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="MareArts ANPR Management Server",
    description="Professional ANPR server with REST API and Web Dashboard",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(config.STATIC_DIR)), name="static")
app.mount("/results", StaticFiles(directory=str(config.RESULTS_DIR)), name="results")

# Templates
templates = Jinja2Templates(directory=str(config.TEMPLATES_DIR))

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_detection_image(img: np.ndarray, detections: list, detection_id: int) -> tuple:
    """Save detection result image with bounding boxes"""
    if not config.SAVE_IMAGES:
        return None, None
    
    # Draw bounding boxes
    result_img = img.copy()
    for det in detections:
        # Handle both 'ltrb' (from marearts_anpr) and 'bbox' formats
        bbox = det.get('ltrb') or det.get('bbox')
        if not bbox:
            continue
            
        x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        
        # Draw rectangle
        cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Draw text
        text = f"{det['ocr']} ({det['ocr_conf']:.1f}%)"
        cv2.putText(result_img, text, (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Save full image (use timestamp for unique filename since detection_id might be 0)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"detection_{timestamp}.jpg"
    image_path = config.RESULTS_DIR / filename
    cv2.imwrite(str(image_path), result_img)
    
    # Save thumbnail
    height, width = result_img.shape[:2]
    aspect = width / height
    thumb_width = 400
    thumb_height = int(thumb_width / aspect)
    thumb = cv2.resize(result_img, (thumb_width, thumb_height))
    thumb_filename = f"thumb_{timestamp}.jpg"
    thumb_path = config.RESULTS_DIR / thumb_filename
    cv2.imwrite(str(thumb_path), thumb)
    
    return f"/results/{filename}", f"/results/{thumb_filename}"

def process_image_bytes(image_bytes: bytes, client_ip: str = "unknown") -> dict:
    """Process image from bytes"""
    if not state.credentials_valid or not state.detector or not state.ocr:
        add_server_log(f"Request from {client_ip} - Models not loaded", "error")
        raise HTTPException(status_code=503, detail="ANPR models not loaded. Configure credentials first.")
    
    add_server_log(f"Processing image from {client_ip} ({len(image_bytes) / 1024:.1f} KB)", "info")
    
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        add_server_log(f"Invalid image format from {client_ip}", "error")
        raise HTTPException(status_code=400, detail="Invalid image format")
    
    # Process with ANPR
    start_time = time.time()
    result = marearts_anpr_from_cv2(state.detector, state.ocr, img)
    total_time = time.time() - start_time
    
    # Extract results
    detections = result.get('results', [])
    plates = [d['ocr'] for d in detections]
    confidences = [d['ocr_conf'] for d in detections]
    bboxes = [d['ltrb'] for d in detections]
    
    detector_time = result.get('ltrb_proc_sec', 0)
    ocr_time = result.get('ocr_proc_sec', 0)
    
    # Save image with detections first (if enabled)
    image_url, thumb_url = None, None
    if len(detections) > 0:
        image_url, thumb_url = save_detection_image(img, detections, 0)
    
    # Save to database (only once!)
    detection_id = db.add_detection(
        plates=plates,
        confidences=confidences,
        bboxes=bboxes,
        processing_time=total_time,
        detector_time=detector_time,
        ocr_time=ocr_time,
        image_path=image_url,
        thumbnail_path=thumb_url,
        success=len(detections) > 0
    )
    
    state.request_count += 1
    
    # Log results
    if len(detections) > 0:
        plate_list = ', '.join(plates)
        add_server_log(f"✓ {client_ip} - Detected {len(detections)} plate(s): {plate_list} ({total_time*1000:.0f}ms)", "success")
    else:
        add_server_log(f"✗ {client_ip} - No plates detected ({total_time*1000:.0f}ms)", "warning")
    
    return {
        'detection_id': detection_id,
        'results': detections,
        'processing_time': total_time,
        'detector_time': detector_time,
        'ocr_time': ocr_time,
        'image_url': image_url
    }

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Redirect to dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    # Mask credentials for display
    username = config.MAREARTS_USERNAME or ""
    serial_key = config.MAREARTS_SERIAL_KEY or ""
    signature = config.MAREARTS_SIGNATURE or ""
    
    return {
        "status": "ok",
        "credentials_configured": state.credentials_valid,
        "models_loaded": state.detector is not None,
        "uptime": round(time.time() - state.start_time, 2),
        "version": "1.0.0",
        "credentials": {
            "username": username if username else None,
            "serial_key_masked": serial_key[:4] + "***" + serial_key[-4:] if len(serial_key) > 8 else "***" if serial_key else None,
            "signature_masked": signature[:4] + "********" if len(signature) > 4 else "***" if signature else None
        }
    }

@app.post("/api/detect", response_model=ANPRResponse)
async def detect_plate_file(image: UploadFile = File(...), request: Request = None):
    """
    Detect and recognize license plates from uploaded image file
    
    Example:
        curl -X POST http://localhost:8000/api/detect -F "image=@plate.jpg"
    """
    try:
        client_ip = request.client.host if request else "unknown"
        image_bytes = await image.read()
        result = process_image_bytes(image_bytes, client_ip)
        
        # Convert results to DetectionResult format
        detection_results = []
        for r in result['results']:
            detection_results.append(DetectionResult(
                plate_text=r['ocr'],
                confidence=r['ocr_conf'],
                bbox=r['ltrb'],
                detection_confidence=r['ltrb_conf']
            ))
        
        return ANPRResponse(
            success=True,
            detection_id=result['detection_id'],
            timestamp=datetime.now().isoformat(),
            results=detection_results,
            processing_time=result['processing_time'],
            detector_time=result['detector_time'],
            ocr_time=result['ocr_time'],
            image_url=result['image_url']
        )
    except Exception as e:
        return ANPRResponse(
            success=False,
            timestamp=datetime.now().isoformat(),
            results=[],
            processing_time=0,
            detector_time=0,
            ocr_time=0,
            error=str(e)
        )

@app.post("/api/detect/binary", response_model=ANPRResponse)
async def detect_plate_binary(request: Request):
    """
    Detect plates from raw binary image data
    
    Example:
        curl -X POST http://localhost:8000/api/detect/binary \
             --data-binary "@plate.jpg" \
             -H "Content-Type: application/octet-stream"
    """
    try:
        client_ip = request.client.host
        image_bytes = await request.body()
        result = process_image_bytes(image_bytes, client_ip)
        
        # Convert results to DetectionResult format
        detection_results = []
        for r in result['results']:
            detection_results.append(DetectionResult(
                plate_text=r['ocr'],
                confidence=r['ocr_conf'],
                bbox=r['ltrb'],
                detection_confidence=r['ltrb_conf']
            ))
        
        return ANPRResponse(
            success=True,
            detection_id=result['detection_id'],
            timestamp=datetime.now().isoformat(),
            results=detection_results,
            processing_time=result['processing_time'],
            detector_time=result['detector_time'],
            ocr_time=result['ocr_time'],
            image_url=result['image_url']
        )
    except Exception as e:
        return ANPRResponse(
            success=False,
            timestamp=datetime.now().isoformat(),
            results=[],
            processing_time=0,
            detector_time=0,
            ocr_time=0,
            error=str(e)
        )

@app.post("/api/detect/base64", response_model=ANPRResponse)
async def detect_plate_base64(data: Base64ImageRequest, request: Request = None):
    """
    Detect plates from base64 encoded image
    
    Example:
        curl -X POST http://localhost:8000/api/detect/base64 \
             -H "Content-Type: application/json" \
             -d '{"image": "base64_string_here"}'
    """
    try:
        client_ip = request.client.host if request else "unknown"
        image_bytes = base64.b64decode(data.image)
        result = process_image_bytes(image_bytes, client_ip)
        
        # Convert results to DetectionResult format
        detection_results = []
        for r in result['results']:
            detection_results.append(DetectionResult(
                plate_text=r['ocr'],
                confidence=r['ocr_conf'],
                bbox=r['ltrb'],
                detection_confidence=r['ltrb_conf']
            ))
        
        return ANPRResponse(
            success=True,
            detection_id=result['detection_id'],
            timestamp=datetime.now().isoformat(),
            results=detection_results,
            processing_time=result['processing_time'],
            detector_time=result['detector_time'],
            ocr_time=result['ocr_time'],
            image_url=result['image_url']
        )
    except Exception as e:
        return ANPRResponse(
            success=False,
            timestamp=datetime.now().isoformat(),
            results=[],
            processing_time=0,
            detector_time=0,
            ocr_time=0,
            error=str(e)
        )

@app.get("/api/stats", response_model=ServerStats)
def get_statistics():
    """Get server statistics"""
    stats = db.get_statistics()
    stats['uptime'] = round(time.time() - state.start_time, 2)
    return ServerStats(**stats)

@app.get("/api/history")
def get_history(
    limit: int = 100,
    offset: int = 0,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
):
    """Get detection history with optional filters"""
    history = db.get_history(limit=limit, offset=offset, date_from=date_from, date_to=date_to)
    return {"count": len(history), "results": history}

@app.get("/api/history/{detection_id}")
def get_detection(detection_id: int):
    """Get specific detection by ID"""
    detection = db.get_detection_by_id(detection_id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection

@app.get("/api/daily-stats")
def get_daily_statistics(days: int = 7):
    """Get daily statistics for last N days"""
    stats = db.get_daily_stats(days=days)
    return {"days": days, "stats": stats}

@app.get("/api/logs/stream")
async def stream_logs(request: Request):
    """Server-Sent Events endpoint for real-time logs"""
    async def event_generator():
        # Send existing logs first
        for log in list(state.log_queue):
            yield f"data: {log['timestamp']}|{log['level']}|{log['message']}\n\n"
        
        # Create queue for new logs
        queue = asyncio.Queue()
        state.log_subscribers.append(queue)
        
        try:
            while True:
                # Wait for new log entry
                try:
                    log = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield f"data: {log['timestamp']}|{log['level']}|{log['message']}\n\n"
                except asyncio.TimeoutError:
                    # Send keepalive
                    yield f"data: keepalive\n\n"
        except asyncio.CancelledError:
            state.log_subscribers.remove(queue)
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/logs")
def get_logs():
    """Get current log entries"""
    return {
        "logs": list(state.log_queue),
        "total_count": len(state.log_queue),
        "max_retention": config.MAX_LOG_ENTRIES
    }

@app.post("/api/logs/clear")
async def clear_logs():
    """Clear all log entries"""
    count = len(state.log_queue)
    state.log_queue.clear()
    add_server_log(f"Logs cleared ({count} entries removed)", "info")
    return {"success": True, "message": f"Cleared {count} log entries"}

@app.get("/api/debug/database")
def debug_database():
    """Debug endpoint to check database contents"""
    with db.get_connection() as conn:
        # Get total count
        total = conn.execute("SELECT COUNT(*) as count FROM detections").fetchone()['count']
        
        # Get all entries (raw)
        all_entries = conn.execute("""
            SELECT id, timestamp, num_plates, plates, success 
            FROM detections 
            ORDER BY timestamp DESC 
            LIMIT 20
        """).fetchall()
        
        entries = [dict(row) for row in all_entries]
        
        # Get date range
        date_range = conn.execute("""
            SELECT 
                MIN(timestamp) as earliest,
                MAX(timestamp) as latest
            FROM detections
        """).fetchone()
        
        return {
            "total_entries": total,
            "earliest": date_range['earliest'],
            "latest": date_range['latest'],
            "recent_entries": entries,
            "database_path": str(config.DATABASE_PATH)
        }

@app.post("/api/database/clear")
async def clear_database():
    """Clear all detection history (destructive operation!)"""
    try:
        db.clear_all()
        
        # Also delete result images
        if config.RESULTS_DIR.exists():
            for file in config.RESULTS_DIR.glob("*.jpg"):
                file.unlink()
        
        add_server_log("Database cleared - All history deleted", "warning")
        
        return {
            "success": True,
            "message": "All detection history and images deleted"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/configure")
async def configure_credentials(request: Request):
    """Configure credentials manually from web interface"""
    try:
        data = await request.json()
        username = data.get('username')
        serial_key = data.get('serial_key')
        signature = data.get('signature')
        
        if not all([username, serial_key, signature]):
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "All fields are required"}
            )
        
        # Try to load models with new credentials
        try:
            print(f"\n{'='*70}")
            print("Loading models with provided credentials...")
            print(f"{'='*70}")
            
            # Load detector
            test_detector = ma_anpr_detector_v14(
                config.DETECTOR_MODEL,
                username,
                serial_key,
                signature,
                backend=config.BACKEND,
                conf_thres=config.CONFIDENCE_THRESHOLD,
                iou_thres=0.5
            )
            
            # Load OCR (unified interface)
            test_ocr = ma_anpr_ocr(
                model=config.OCR_MODEL,
                region=config.REGION,
                user_name=username,
                serial_key=serial_key,
                signature=signature,
                version=config.OCR_VERSION,
                backend=config.BACKEND
            )
            
            # If successful, update global state
            state.detector = test_detector
            state.ocr = test_ocr
            state.credentials_valid = True
            
            # Update config module
            config.MAREARTS_USERNAME = username
            config.MAREARTS_SERIAL_KEY = serial_key
            config.MAREARTS_SIGNATURE = signature
            
            print("✅ Models loaded successfully with new credentials!")
            add_server_log(f"Credentials configured via web UI - Models loaded", "success")
            
            return {
                "success": True,
                "message": "Credentials validated and models loaded successfully"
            }
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": f"Invalid credentials or model loading failed: {str(e)}"}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/models/status")
def get_models_status():
    """Get available models and their status"""
    models_dir = Path.home() / ".marearts" / "marearts_anpr_data"
    
    detector_models = [
        {"name": "pico_320p_fp32", "description": "Smallest & Fast (96% acc, 129 FPS)"},
        {"name": "pico_640p_fp32", "description": "Balanced (98.5% acc, 66 FPS)"},
        {"name": "micro_320p_fp32", "description": "⭐ Best Overall (97% acc, 128 FPS)"},
        {"name": "micro_320p_fp16", "description": "Best Mobile (97% acc, 56 FPS, 42MB)"},
        {"name": "micro_640p_fp32", "description": "Highest Detection (99% acc, 68 FPS)"},
        {"name": "small_320p_fp32", "description": "⚡ Fastest (98% acc, 142 FPS)"},
        {"name": "small_640p_fp32", "description": "High Detection (99% acc, 70 FPS)"},
        {"name": "medium_320p_fp32", "description": "High Detection (98% acc, 136 FPS)"},
        {"name": "medium_640p_fp32", "description": "Very High (99% acc, 66 FPS)"},
        {"name": "large_320p_fp32", "description": "Strong (98% acc, 131 FPS)"},
        {"name": "large_640p_fp32", "description": "🎯 Highest Accuracy (99.3% acc, 60 FPS)"}
    ]
    
    ocr_models = [
        {"name": "pico_fp32", "description": "📱 Edge/Mobile (92% acc, 270 FPS, 20MB)"},
        {"name": "micro_fp32", "description": "Fast (92% acc, 262 FPS, 71MB)"},
        {"name": "small_fp32", "description": "⚡ Fastest (92% acc, 300 FPS, 112MB)"},
        {"name": "medium_fp32", "description": "Balanced (90% acc, 270 FPS, 164MB)"},
        {"name": "large_fp32", "description": "🎯 Best Accuracy (92% acc, 262 FPS, 179MB)"}
    ]
    
    regions = [
        {"code": "kr", "name": "Korea", "description": "🇰🇷 Korean plates (한국)"},
        {"code": "eup", "name": "Europe+", "description": "🇪🇺 EU, UK, Switzerland, Norway"},
        {"code": "na", "name": "North America", "description": "🇺🇸 USA, Canada, Mexico"},
        {"code": "cn", "name": "China", "description": "🇨🇳 Chinese plates (中国)"},
        {"code": "univ", "name": "Universal", "description": "🌍 All regions (lower accuracy)"}
    ]
    
    detector_status = []
    for model_info in detector_models:
        model = model_info["name"]
        model_file = models_dir / f"marearts_anpr_d_v14_{model}.dat"
        detector_status.append({
            "name": model,
            "description": model_info["description"],
            "downloaded": model_file.exists(),
            "size": model_file.stat().st_size if model_file.exists() else 0,
            "current": model == config.DETECTOR_MODEL
        })
    
    ocr_status = []
    for model_info in ocr_models:
        model = model_info["name"]
        model_file = models_dir / f"marearts_anpr_r_v14_{model}.dat"
        config_file = models_dir / f"marearts_anpr_r_v14_{model}_config.dat"
        ocr_status.append({
            "name": model,
            "description": model_info["description"],
            "downloaded": model_file.exists() and config_file.exists(),
            "size": (model_file.stat().st_size if model_file.exists() else 0),
            "current": model == config.OCR_MODEL
        })
    
    return {
        "detector_models": detector_status,
        "ocr_models": ocr_status,
        "regions": regions,
        "models_directory": str(models_dir),
        "current_detector": config.DETECTOR_MODEL,
        "current_ocr": config.OCR_MODEL,
        "current_region": config.REGION,
        "current_backend": config.BACKEND
    }

@app.post("/api/models/update")
async def update_models(request: Request):
    """Update detector, OCR model, and region"""
    try:
        data = await request.json()
        detector_model = data.get('detector_model')
        ocr_model = data.get('ocr_model')
        region = data.get('region')
        
        if not all([detector_model, ocr_model, region]):
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "All fields are required"}
            )
        
        if not state.credentials_valid:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Credentials not configured. Configure credentials first."}
            )
        
        try:
            print(f"\n{'='*70}")
            print("Reloading models with new configuration...")
            print(f"  Detector: {detector_model}")
            print(f"  OCR: {ocr_model}")
            print(f"  Region: {region}")
            print(f"{'='*70}")
            
            # Load new detector
            new_detector = ma_anpr_detector_v14(
                detector_model,
                config.MAREARTS_USERNAME,
                config.MAREARTS_SERIAL_KEY,
                config.MAREARTS_SIGNATURE,
                backend=config.BACKEND,
                conf_thres=config.CONFIDENCE_THRESHOLD,
                iou_thres=0.5
            )
            
            # Load new OCR (unified interface)
            new_ocr = ma_anpr_ocr(
                model=ocr_model,
                region=region,
                user_name=config.MAREARTS_USERNAME,
                serial_key=config.MAREARTS_SERIAL_KEY,
                signature=config.MAREARTS_SIGNATURE,
                version=config.OCR_VERSION,
                backend=config.BACKEND
            )
            
            # If successful, update global state
            state.detector = new_detector
            state.ocr = new_ocr
            
            # Update config
            config.DETECTOR_MODEL = detector_model
            config.OCR_MODEL = ocr_model
            config.REGION = region
            
            print("✅ Models updated successfully!")
            add_server_log(f"Models updated: {detector_model} + {ocr_model} ({region})", "success")
            
            return {
                "success": True,
                "message": f"Models updated: {detector_model} + {ocr_model} ({region})"
            }
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": f"Failed to load models: {str(e)}"}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("\n" + "="*70)
    print("Starting MareArts ANPR Management Server...")
    print("="*70)
    
    add_server_log("Server starting...", "info")
    
    # Initialize models
    success = init_models()
    
    if success:
        add_server_log(f"Models loaded: {config.DETECTOR_MODEL} + {config.OCR_MODEL} ({config.REGION})", "success")
    else:
        add_server_log("Models not loaded - awaiting configuration", "warning")
    
    add_server_log(f"Server ready on port {config.PORT}", "success")
    
    print("\n" + "="*70)
    print("🚀 Server Ready!")
    print("="*70)
    print(f"\n📍 Web Dashboard: http://{config.HOST}:{config.PORT}/")
    print(f"📍 API Docs: http://{config.HOST}:{config.PORT}/docs")
    print(f"📍 Health Check: http://{config.HOST}:{config.PORT}/api/health")
    print("\nAPI Endpoints:")
    print("  POST /api/detect          - Upload file")
    print("  POST /api/detect/binary   - Raw bytes")
    print("  POST /api/detect/base64   - Base64 image")
    print("  GET  /api/stats           - Statistics")
    print("  GET  /api/history         - Detection history")
    print("\n" + "="*70 + "\n")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        log_level="info"
    )

