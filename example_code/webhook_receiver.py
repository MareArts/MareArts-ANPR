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


@app.post("/webhook")
async def receive_webhook(
    file: UploadFile = File(None),
    payload_json: str = Form("{}")
):
    """
    Receive plate detection from MareArts ANPR Mobile App.

    Same multipart format as Discord webhooks:
      - file: plate image (JPEG)
      - payload_json: metadata JSON string

    Payload format:
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
    # Parse metadata
    try:
        metadata = json.loads(payload_json)
    except json.JSONDecodeError:
        metadata = {}

    plate_number = metadata.get("plate", {}).get("number", "unknown")
    det_conf = metadata.get("plate", {}).get("detection_confidence", 0)
    ocr_conf = metadata.get("plate", {}).get("ocr_confidence", 0)
    timestamp = metadata.get("timestamp", datetime.now().isoformat())
    lat = metadata.get("location", {}).get("latitude")
    lon = metadata.get("location", {}).get("longitude")

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
    if file and file.filename:
        save_dir = Path(SAVE_DIR)
        save_dir.mkdir(parents=True, exist_ok=True)

        # Filename: PLATE_TIMESTAMP.jpg
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_plate = plate_number.replace("/", "_").replace("\\", "_")
        filename = f"{safe_plate}_{ts}.jpg"
        saved_path = save_dir / filename

        image_bytes = await file.read()
        with open(saved_path, "wb") as f:
            f.write(image_bytes)
        print(f"  Saved: {saved_path}")

    # Save metadata JSON alongside image
    if saved_path:
        json_path = saved_path.with_suffix(".json")
        with open(json_path, "w") as f:
            json.dump(metadata, f, indent=2)

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

if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 60)
    print("  MareArts ANPR Webhook Receiver")
    print("=" * 60)
    print(f"\n  Endpoint:  POST http://0.0.0.0:9000/webhook")
    print(f"  Save dir:  {SAVE_DIR}/")
    if SLACK_WEBHOOK_URL:
        print(f"  Slack:     enabled")
    if TELEGRAM_BOT_TOKEN:
        print(f"  Telegram:  enabled")
    print(f"\n  Set this URL in MareArts ANPR Mobile App:")
    print(f"    http://YOUR_SERVER_IP:9000/webhook")
    print(f"\n  Test:")
    print(f'    curl -X POST http://localhost:9000/webhook \\')
    print(f'      -F "file=@plate.jpg" \\')
    print(f"      -F 'payload_json={{\"plate\":{{\"number\":\"TEST-123\"}}}}'")
    print("\n" + "=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=9000)
