"""MareArts ANPR — Server REST API Examples

Prerequisites:
    pip install requests
    ma-anpr server start

Covers: single detect, batch, MMC, base64, binary, URL,
        history, search, export, watchlist, alerts, region, threads.
"""
import base64
import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("pip install requests")
    sys.exit(1)

SERVER = "http://127.0.0.1:8000"
SAMPLE = Path(__file__).resolve().parent.parent.parent / "sample_images"
EU_IMG = SAMPLE / "eu-a.jpg"
KR_IMG = SAMPLE / "kr-a.jpg"


def section(title):
    print(f"\n{'=' * 60}\n  {title}\n{'=' * 60}")


# ── 1. Health check ──────────────────────────────────────────
section("1. Health Check")

r = requests.get(f"{SERVER}/api/health")
info = r.json()
print(f"  Status:  {info['status']}")
print(f"  Version: {info.get('version', '?')}")
print(f"  Models:  {info.get('models_loaded')}")


# ── 2. Single image detection (local ANPR) ───────────────────
section("2. Single Image — Local ANPR")

with open(EU_IMG, "rb") as f:
    r = requests.post(f"{SERVER}/api/anpr", files={"image": f})
data = r.json()
for plate in data["results"]:
    print(f"  {plate['plate_text']} ({plate['confidence']}%)  bbox={plate['bbox']}")
print(f"  Time: {data['processing_sec']}s")


# ── 3. Single image + MMC enrichment ─────────────────────────
section("3. Single Image — ANPR + MMC")

with open(EU_IMG, "rb") as f:
    r = requests.post(f"{SERVER}/api/anpr/mmc", files={"image": f})
data = r.json()
for plate in data["results"]:
    print(f"  {plate['plate_text']} ({plate['confidence']}%)")
    if plate.get("mmc_make"):
        print(f"    Vehicle: {plate['mmc_color']} {plate['mmc_make']} {plate['mmc_model']}")
        print(f"    Type: {plate['mmc_type']}  Side: {plate['mmc_vehicle_side']}")
        print(f"    Nation: {plate.get('mmc_plate_nation', '?')}  Cloud OCR: {plate.get('mmc_plate', '?')}")
if data.get("mmc_error"):
    print(f"  MMC error: {data['mmc_error']}")
else:
    print(f"  MMC quota: {data.get('mmc_calls_today', '?')}/{data.get('mmc_daily_limit', '?')}")


# ── 4. Detection with specific region ────────────────────────
section("4. Detection with Region")

with open(KR_IMG, "rb") as f:
    r = requests.post(f"{SERVER}/api/anpr",
                      files={"image": f}, data={"region": "kr"})
data = r.json()
for plate in data["results"]:
    print(f"  [kr] {plate['plate_text']} ({plate['confidence']}%)")


# ── 5. Base64 input ──────────────────────────────────────────
section("5. Base64 Input")

b64 = base64.b64encode(EU_IMG.read_bytes()).decode()
r = requests.post(f"{SERVER}/api/anpr/base64",
                  json={"image": b64, "region": "eup"})
data = r.json()
for plate in data["results"]:
    print(f"  {plate['plate_text']} ({plate['confidence']}%)")


# ── 6. Raw binary input ─────────────────────────────────────
section("6. Binary Input")

r = requests.post(f"{SERVER}/api/anpr/binary",
                  data=EU_IMG.read_bytes(),
                  headers={"Content-Type": "application/octet-stream"})
data = r.json()
for plate in data["results"]:
    print(f"  {plate['plate_text']} ({plate['confidence']}%)")


# ── 7. Batch (multiple images) ───────────────────────────────
section("7. Batch Detection")

files = [("images", open(EU_IMG, "rb")), ("images", open(KR_IMG, "rb"))]
r = requests.post(f"{SERVER}/api/anpr/batch", files=files)
data = r.json()
print(f"  Images: {data.get('total_images', '?')}")
print(f"  Plates: {data.get('total_plates', '?')}")
for item in data.get("results", []):
    plates = [p["plate_text"] for p in item.get("results", [])]
    print(f"    {item.get('filename', '?')}: {plates}")


# ── 8. History & search ──────────────────────────────────────
section("8. History & Search")

r = requests.get(f"{SERVER}/api/history", params={"limit": 3})
items = r.json()
print(f"  Recent detections: {len(items)}")

r = requests.get(f"{SERVER}/api/history/search",
                 params={"q": "BG", "min_confidence": 80, "limit": 5})
results = r.json()
items = results if isinstance(results, list) else results.get("items", [])
print(f"  Search 'BG' (>80%): {len(items)} result(s)")


# ── 9. Export ────────────────────────────────────────────────
section("9. Export")

r = requests.get(f"{SERVER}/api/history/export/csv", params={"limit": 5})
print(f"  CSV: {len(r.content)} bytes")

r = requests.get(f"{SERVER}/api/history/export/json", params={"limit": 5})
print(f"  JSON: {len(r.content)} bytes")


# ── 10. Watchlist & alerts ───────────────────────────────────
section("10. Watchlist & Alerts")

r = requests.post(f"{SERVER}/api/watchlist",
                  json={"plate": "EXAMPLE123", "label": "demo"})
entry = r.json()
wl_id = entry.get("id")
print(f"  Added: id={wl_id}")

r = requests.get(f"{SERVER}/api/watchlist")
print(f"  Watchlist: {len(r.json())} entries")

r = requests.get(f"{SERVER}/api/alerts/count")
print(f"  Unread alerts: {r.json().get('count', 0)}")

if wl_id:
    requests.delete(f"{SERVER}/api/watchlist/{wl_id}")
    print(f"  Removed: id={wl_id}")


# ── 11. Region & thread control ─────────────────────────────
section("11. Runtime Config")

r = requests.get(f"{SERVER}/api/region")
print(f"  Region: {r.json().get('active_region', '?')}")

r = requests.get(f"{SERVER}/api/threads")
print(f"  Threads: {r.json().get('threads', '?')}")

r = requests.get(f"{SERVER}/api/mmc/status")
mmc = r.json()
print(f"  MMC: {'available' if mmc.get('available') else 'unavailable'}")


print(f"\n{'=' * 60}")
print("  Done. See http://127.0.0.1:8000/docs for full Swagger UI.")
print(f"{'=' * 60}")
