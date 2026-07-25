#!/usr/bin/env python3
"""
MareArts ANPR Webhook Receiver

Receives plate detection results from MareArts ANPR Mobile App.
Same multipart format as Discord webhooks - works as a drop-in replacement.

The mobile app sends: image file + payload_json (metadata)
This server receives both, saves them, and optionally forwards to Slack/Telegram.

Requirements:
    pip install fastapi uvicorn python-multipart

Run:
    python webhook_receiver.py

    Then set this URL in MareArts ANPR Mobile App:
        http://YOUR_SERVER_IP:9000/webhook

Test:
    curl -X POST http://localhost:9000/webhook \
      -F "file=@plate.jpg" \
      -F 'payload_json={"source":"marearts_anpr","event":"plate_detected","plate":{"number":"ABC-123","detection_confidence":0.95,"ocr_confidence":0.99}}'
"""

import json
import os
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.responses import JSONResponse
from starlette.datastructures import UploadFile as StarletteUploadFile

# ============================================================================
# CONFIGURATION
# ============================================================================

# Where to save received images
SAVE_DIR = "received_plates"

# Optional: Forward to Slack (set your Slack webhook URL or leave empty)
SLACK_WEBHOOK_URL = ""  # e.g. "https://hooks.slack.com/services/T.../B.../xxx"

# Optional: Forward to Telegram (set bot token + chat ID or leave empty)
TELEGRAM_BOT_TOKEN = ""  # e.g. "123456:ABC-DEF..."
TELEGRAM_CHAT_ID = ""    # e.g. "-1001234567890"

# ============================================================================
# SERVER
# ============================================================================

app = FastAPI(title="MareArts ANPR Webhook Receiver")

def round_floats(obj, precision=4):
    """Recursively round float values for cleaner saved JSON."""
    if isinstance(obj, float):
        return round(obj, precision)
    if isinstance(obj, dict):
        return {k: round_floats(v, precision) for k, v in obj.items()}
    if isinstance(obj, list):
        return [round_floats(v, precision) for v in obj]
    return obj


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Receive plate detection from MareArts ANPR Mobile App.

    Supports multiple formats:
      - multipart/form-data with file + payload_json (Discord-compatible)
      - application/json body (direct JSON post)
      - Any other multipart fields the app sends

    Payload format (new):
    {
        "source": "marearts_anpr",
        "event": "plate_detected",
        "timestamp": "2026-02-10T22:52:35",
        "plate": {
            "number": "VGZ-277",
            "detection_confidence": 0.92,
            "ocr_confidence": 1.00
        },
        "bbox": {
            "left": 220.56,
            "top": 421.41,
            "right": 476.06,
            "bottom": 512.11
        },
        "location": {
            "latitude": 60.1538,
            "longitude": 24.7464,
            "address": null
        },
        "scan_mode": "scan"
    }
    """
    content_type = request.headers.get("content-type", "")
    metadata = {}
    file_data = None
    file_name = "plate.jpg"

    if "multipart/form-data" in content_type:
        # Parse multipart form
        form = await request.form()

        # Debug: show all received field names
        print(f"\n  [DEBUG] Multipart fields: {list(form.keys())}")

        # Get image file (try common field names, including files[0])
        for field_name in form.keys():
            upload = form[field_name]
            if hasattr(upload, "read"):
                file_data = await upload.read()
                file_name = getattr(upload, "filename", "plate.jpg") or "plate.jpg"
                print(f"  [DEBUG] Image field: '{field_name}', size: {len(file_data)} bytes, name: {file_name}")
                break

        # Get metadata JSON (try multiple field names, in priority order)
        for field_name in ["metadata_json", "payload_json", "metadata", "data", "json", "content"]:
            if field_name in form:
                val = form[field_name]
                if hasattr(val, "read"):
                    continue  # skip file fields
                raw = val if isinstance(val, str) else str(val)
                print(f"  [DEBUG] JSON field: '{field_name}', value: {raw[:300]}")
                try:
                    parsed = json.loads(raw)
                    # Handle Discord wrapper: {"content": "{\"plateNumber\":...}"}
                    if isinstance(parsed, dict) and "content" in parsed and len(parsed) <= 2:
                        inner = parsed["content"]
                        if isinstance(inner, str):
                            try:
                                metadata = json.loads(inner)
                                print(f"  [DEBUG] Unwrapped Discord content -> keys: {list(metadata.keys())}")
                            except json.JSONDecodeError:
                                metadata = parsed
                        else:
                            metadata = parsed
                    else:
                        metadata = parsed
                except json.JSONDecodeError:
                    pass
                if metadata:
                    break

        # If no JSON field found, collect all non-file fields as metadata
        if not metadata:
            for key in form.keys():
                val = form[key]
                if not hasattr(val, "read"):
                    raw = val if isinstance(val, str) else str(val)
                    try:
                        metadata[key] = json.loads(raw)
                    except (json.JSONDecodeError, TypeError):
                        metadata[key] = raw
            print(f"  [DEBUG] Collected fields as metadata: {json.dumps(metadata, default=str)[:300]}")

    elif "application/json" in content_type:
        # Direct JSON body
        body = await request.body()
        print(f"\n  [DEBUG] JSON body: {body.decode()[:300]}")
        try:
            metadata = json.loads(body)
        except json.JSONDecodeError:
            metadata = {}
    else:
        # Try to read as raw body
        body = await request.body()
        print(f"\n  [DEBUG] Raw body ({content_type}): {body[:300]}")
        try:
            metadata = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            metadata = {}

    # Extract fields - support BOTH old (flat) and new (nested) format
    # New format: plate.number, plate.detection_confidence
    # Old format: plateNumber, detectionConfidence
    plate_number = (
        metadata.get("plate", {}).get("number")
        or metadata.get("plateNumber")
        or metadata.get("plate_number")
        or "unknown"
    )
    det_conf = (
        metadata.get("plate", {}).get("detection_confidence")
        or metadata.get("detectionConfidence")
        or metadata.get("detection_confidence")
        or 0
    )
    ocr_conf = (
        metadata.get("plate", {}).get("ocr_confidence")
        or metadata.get("ocrConfidence")
        or metadata.get("ocr_confidence")
        or 0
    )
    timestamp = metadata.get("timestamp", datetime.now().isoformat())

    # GPS - support both formats
    loc = metadata.get("location") or metadata.get("gps") or {}
    lat = loc.get("latitude")
    lon = loc.get("longitude")

    # Print to console
    print(f"\n{'='*50}")
    print(f"  Plate Detected: {plate_number}")
    print(f"  Detection: {det_conf:.2f}  OCR: {ocr_conf:.2f}")
    print(f"  Time: {timestamp}")
    if lat and lon:
        print(f"  GPS: {lat:.4f}, {lon:.4f}")
    print(f"{'='*50}")

    # Save image if provided
    saved_path = None
    if file_data and len(file_data) > 0:
        save_dir = Path(SAVE_DIR)
        save_dir.mkdir(parents=True, exist_ok=True)

        # Filename: PLATE_TIMESTAMP.jpg
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_plate = plate_number.replace("/", "_").replace("\\", "_").replace(" ", "_")
        ext = Path(file_name).suffix or ".jpg"
        filename = f"{safe_plate}_{ts}{ext}"
        saved_path = save_dir / filename

        with open(saved_path, "wb") as f:
            f.write(file_data)
        print(f"  Saved: {saved_path} ({len(file_data)} bytes)")

    # Save metadata JSON alongside image
    if saved_path:
        json_path = saved_path.with_suffix(".json")
        metadata_clean = round_floats(metadata, precision=4)
        with open(json_path, "w") as f:
            json.dump(metadata_clean, f, indent=2)

    # Optional: Forward to Slack
    if SLACK_WEBHOOK_URL:
        forward_to_slack(metadata, saved_path)

    # Optional: Forward to Telegram
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        forward_to_telegram(metadata, saved_path)

    return {
        "status": "ok",
        "plate": plate_number,
        "saved": str(saved_path) if saved_path else None
    }


@app.get("/")
def root():
    """Server info"""
    return {
        "service": "MareArts ANPR Webhook Receiver",
        "version": "1.0",
        "endpoint": "POST /webhook",
        "status": "ready"
    }


@app.get("/health")
def health():
    """Health check"""
    return {"status": "ok"}


# ============================================================================
# OPTIONAL: Forward to other services
# ============================================================================

def forward_to_slack(metadata, image_path=None):
    """Forward detection to Slack channel"""
    try:
        import requests

        plate = metadata.get("plate", {})
        loc = metadata.get("location", {})
        text = (
            f"*Plate Detected: {plate.get('number', '?')}*\n"
            f"Detection: {plate.get('detection_confidence', 0):.2f} | "
            f"OCR: {plate.get('ocr_confidence', 0):.2f}\n"
            f"Time: {metadata.get('timestamp', '?')}"
        )
        if loc.get("latitude"):
            text += f"\nGPS: {loc['latitude']:.4f}, {loc['longitude']:.4f}"

        requests.post(SLACK_WEBHOOK_URL, json={"text": text}, timeout=5)
        print("  -> Forwarded to Slack")
    except Exception as e:
        print(f"  -> Slack error: {e}")


def forward_to_telegram(metadata, image_path=None):
    """Forward detection to Telegram chat"""
    try:
        import requests

        plate = metadata.get("plate", {})
        loc = metadata.get("location", {})
        text = (
            f"Plate: {plate.get('number', '?')}\n"
            f"Det: {plate.get('detection_confidence', 0):.2f} | "
            f"OCR: {plate.get('ocr_confidence', 0):.2f}\n"
            f"Time: {metadata.get('timestamp', '?')}"
        )
        if loc.get("latitude"):
            text += f"\nGPS: {loc['latitude']:.4f}, {loc['longitude']:.4f}"

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as img:
                requests.post(
                    f"{url}/sendPhoto",
                    data={"chat_id": TELEGRAM_CHAT_ID, "caption": text},
                    files={"photo": img},
                    timeout=10
                )
        else:
            requests.post(
                f"{url}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
                timeout=5
            )
        print("  -> Forwarded to Telegram")
    except Exception as e:
        print(f"  -> Telegram error: {e}")


# ============================================================================
# RUN
# ============================================================================

def get_local_ip():
    """Get the machine's local network IP address"""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


if __name__ == "__main__":
    import uvicorn

    local_ip = get_local_ip()
    port = 9000

    print("\n" + "=" * 60)
    print("  MareArts ANPR Webhook Receiver")
    print("=" * 60)
    print(f"\n  Local IP:  {local_ip}")
    print(f"  Port:      {port}")
    print(f"  Endpoint:  POST http://{local_ip}:{port}/webhook")
    print(f"  Save dir:  {SAVE_DIR}/")
    if SLACK_WEBHOOK_URL:
        print(f"  Slack:     enabled")
    if TELEGRAM_BOT_TOKEN:
        print(f"  Telegram:  enabled")
    print(f"\n  Set this URL in MareArts ANPR Mobile App:")
    print(f"    http://{local_ip}:{port}/webhook")
    print(f"\n  Test:")
    print(f'    curl -X POST http://{local_ip}:{port}/webhook \\')
    print(f'      -F "file=@plate.jpg" \\')
    print(f"      -F 'payload_json={{\"plate\":{{\"number\":\"TEST-123\"}}}}'")
    print("\n" + "=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=port)
