"""
MareArts ANPR — Full Server API Test
Prerequisites:  ma-anpr server start
Just run:       python test_server.py
"""
import base64
import json
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: pip install requests")
    sys.exit(1)

# ── config ──────────────────────────────────────────────────────────
BASE = "http://localhost:8000"
SAMPLE = Path(__file__).resolve().parent / "sample"
EU_IMG = SAMPLE / "eu-a.jpg"
KR_IMG = SAMPLE / "kr-a.jpg"
TIMEOUT = 30

# ── result tracking ─────────────────────────────────────────────────
_results = []

def _run(label, fn):
    t0 = time.perf_counter()
    try:
        detail = fn()
        dt = time.perf_counter() - t0
        _results.append(("PASS", label, f"{dt:.2f}s", detail or ""))
        print(f"  ✅ {label}  ({dt:.2f}s)  {detail or ''}")
    except Exception as e:
        dt = time.perf_counter() - t0
        _results.append(("FAIL", label, f"{dt:.2f}s", str(e)))
        print(f"  ❌ {label}  ({dt:.2f}s)  {e}")


def _get(path, **kw):
    r = requests.get(f"{BASE}{path}", timeout=TIMEOUT, **kw)
    if not r.ok:
        raise Exception(f"HTTP {r.status_code}")
    return r

def _post(path, **kw):
    r = requests.post(f"{BASE}{path}", timeout=TIMEOUT, **kw)
    if not r.ok:
        raise Exception(f"HTTP {r.status_code} {r.text[:200]}")
    return r

def _put(path, **kw):
    r = requests.put(f"{BASE}{path}", timeout=TIMEOUT, **kw)
    if not r.ok:
        raise Exception(f"HTTP {r.status_code}")
    return r

def _delete(path, **kw):
    r = requests.delete(f"{BASE}{path}", timeout=TIMEOUT, **kw)
    if not r.ok:
        raise Exception(f"HTTP {r.status_code}")
    return r


def _plates(d):
    return [det["plate_text"] for det in d.get("detections", [])]


# ====================================================================
#  1. HEALTH & SYSTEM
# ====================================================================
def test_health():
    print("\n" + "=" * 64)
    print("  1. Health & System")
    print("=" * 64)

    _run("GET  /api/health", lambda: f"status={_get('/api/health').json().get('status')}")
    _run("GET  /api/health/check", lambda: _get("/api/health/check") and "OK")
    _run("GET  /api/config", lambda: f"version={_get('/api/config').json().get('version', '?')}")
    _run("GET  /api/stats", lambda: f"total={_get('/api/stats').json().get('total_detections', '?')}")
    _run("GET  /api/stats/chart", lambda: f"buckets={len(_get('/api/stats/chart', params={'period': 24}).json())}")
    _run("GET  /api/threads", lambda: f"threads={_get('/api/threads').json().get('threads', '?')}")
    _run("GET  /api/logs", lambda: f"entries={len(_get('/api/logs', params={'limit': 10}).json())}")
    _run("GET  /api/regions", lambda: f"count={len(_get('/api/regions').json())}")
    _run("GET  /api/region", lambda: f"region={_get('/api/region').json().get('region', '?')}")
    _run("GET  /api/mmc/status", lambda: f"available={_get('/api/mmc/status').json().get('available', '?')}")


# ====================================================================
#  2. DASHBOARD UI
# ====================================================================
def test_dashboard():
    print("\n" + "=" * 64)
    print("  2. Dashboard UI")
    print("=" * 64)

    def _check():
        r = _get("/")
        if "<!doctype html>" not in r.text[:500].lower():
            raise Exception("Not HTML")
        return f"{len(r.text)} bytes"
    _run("GET  /  (dashboard HTML)", _check)


# ====================================================================
#  3. DETECTION — ANPR
# ====================================================================
def test_detection():
    print("\n" + "=" * 64)
    print("  3. Detection — ANPR")
    print("=" * 64)

    # file upload (EU)
    def _file_eu():
        with open(EU_IMG, "rb") as f:
            d = _post("/api/anpr", files={"image": f}).json()
        return f"plates={_plates(d)}"
    _run("POST /api/anpr  (file, EU)", _file_eu)

    # file upload (KR)
    def _file_kr():
        with open(KR_IMG, "rb") as f:
            d = _post("/api/anpr", files={"image": f}).json()
        return f"plates={_plates(d)}"
    _run("POST /api/anpr  (file, KR)", _file_kr)

    # base64
    def _b64():
        b = base64.b64encode(EU_IMG.read_bytes()).decode()
        d = _post("/api/anpr/base64", json={"image": b}).json()
        return f"plates={_plates(d)}"
    _run("POST /api/anpr/base64", _b64)

    # binary
    def _bin():
        d = _post("/api/anpr/binary", data=EU_IMG.read_bytes(),
                   headers={"Content-Type": "application/octet-stream"}).json()
        return f"plates={_plates(d)}"
    _run("POST /api/anpr/binary", _bin)

    # batch
    def _batch():
        files = [("images", open(EU_IMG, "rb")), ("images", open(KR_IMG, "rb"))]
        r = _post("/api/anpr/batch", files=files)
        d = r.json()
        count = len(d) if isinstance(d, list) else d.get("results", "?")
        return f"results={count}"
    _run("POST /api/anpr/batch  (2 images)", _batch)


# ====================================================================
#  4. DETECTION + MMC
# ====================================================================
def test_detection_mmc():
    print("\n" + "=" * 64)
    print("  4. Detection + MMC")
    print("=" * 64)

    def _mmc_file():
        with open(EU_IMG, "rb") as f:
            d = _post("/api/anpr/mmc", files={"image": f}).json()
        dets = d.get("detections", [])
        if dets:
            det0 = dets[0]
            make = det0.get("mmc_make", "?")
            model = det0.get("mmc_model", "?")
            return f"plates={_plates(d)}  mmc={make} {model}"
        return f"plates={_plates(d)}"
    _run("POST /api/anpr/mmc  (file)", _mmc_file)

    def _mmc_b64():
        b = base64.b64encode(EU_IMG.read_bytes()).decode()
        d = _post("/api/anpr/mmc/base64", json={"image": b}).json()
        return f"plates={_plates(d)}"
    _run("POST /api/anpr/mmc/base64", _mmc_b64)

    def _mmc_bin():
        d = _post("/api/anpr/mmc/binary", data=EU_IMG.read_bytes(),
                   headers={"Content-Type": "application/octet-stream"}).json()
        return f"plates={_plates(d)}"
    _run("POST /api/anpr/mmc/binary", _mmc_bin)

    def _mmc_batch():
        files = [("images", open(EU_IMG, "rb")), ("images", open(KR_IMG, "rb"))]
        r = _post("/api/anpr/mmc/batch", files=files)
        d = r.json()
        count = len(d) if isinstance(d, list) else d.get("results", "?")
        return f"results={count}"
    _run("POST /api/anpr/mmc/batch  (2 images)", _mmc_batch)


# ====================================================================
#  5. HISTORY
# ====================================================================
def test_history():
    print("\n" + "=" * 64)
    print("  5. History")
    print("=" * 64)

    _run("GET  /api/history", lambda: f"count={len(_get('/api/history', params={'limit': 5}).json())}")

    det_id = None

    def _search():
        nonlocal det_id
        d = _get("/api/history/search", params={"limit": 5}).json()
        items = d if isinstance(d, list) else d.get("items", [])
        if items:
            det_id = items[0].get("id")
        return f"results={len(items)}"
    _run("GET  /api/history/search", _search)

    if det_id:
        _run(f"GET  /api/history/{det_id}  (detail)",
             lambda: f"plates={_get(f'/api/history/{det_id}').json().get('plates', '?')}")

    def _export_json():
        r = _get("/api/history/export/json", params={"limit": 3})
        return f"{len(r.content)} bytes"
    _run("GET  /api/history/export/json", _export_json)

    def _export_csv():
        r = _get("/api/history/export/csv", params={"limit": 3})
        return f"{len(r.content)} bytes"
    _run("GET  /api/history/export/csv", _export_csv)


# ====================================================================
#  6. WATCHLIST & ALERTS
# ====================================================================
def test_watchlist():
    print("\n" + "=" * 64)
    print("  6. Watchlist & Alerts")
    print("=" * 64)

    _run("GET  /api/watchlist", lambda: f"count={len(_get('/api/watchlist').json())}")

    wl_id = None

    def _add():
        nonlocal wl_id
        d = _post("/api/watchlist", json={"plate": "_SDK_TEST_", "label": "test"}).json()
        wl_id = d.get("id")
        return f"id={wl_id}"
    _run("POST /api/watchlist  (add)", _add)

    if wl_id:
        _run(f"DELETE /api/watchlist/{wl_id}  (remove)",
             lambda: _delete(f"/api/watchlist/{wl_id}") and "OK")

    _run("GET  /api/alerts", lambda: f"count={len(_get('/api/alerts', params={'limit': 5}).json())}")
    _run("GET  /api/alerts/count", lambda: f"unread={_get('/api/alerts/count').json().get('unread', '?')}")
    _run("POST /api/alerts/read  (mark read)", lambda: _post("/api/alerts/read") and "OK")


# ====================================================================
#  7. REGION & MODEL CONFIG
# ====================================================================
def test_config():
    print("\n" + "=" * 64)
    print("  7. Region & Model Config")
    print("=" * 64)

    def _set_get_region():
        orig = _get("/api/region").json().get("region", "univ")
        _put("/api/region", json={"region": "eu"})
        cur = _get("/api/region").json().get("region")
        _put("/api/region", json={"region": orig})
        return f"set eu → got {cur} → restored {orig}"
    _run("PUT  /api/region  (round-trip)", _set_get_region)


# ====================================================================
#  8. THREADS
# ====================================================================
def test_threads():
    print("\n" + "=" * 64)
    print("  8. Thread Control")
    print("=" * 64)

    def _set_get():
        orig = _get("/api/threads").json().get("threads", 4)
        _put("/api/threads", params={"count": 2})
        cur = _get("/api/threads").json().get("threads")
        _put("/api/threads", params={"count": orig})
        return f"set 2 → got {cur} → restored {orig}"
    _run("PUT  /api/threads  (round-trip)", _set_get)


# ====================================================================
#  REPORT
# ====================================================================
def report():
    print("\n" + "=" * 64)
    print("  REPORT")
    print("=" * 64)

    total = len(_results)
    passed = sum(1 for r in _results if r[0] == "PASS")
    failed = total - passed

    print(f"\n  Total : {total}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")

    if failed:
        print("\n  Failed tests:")
        for status, label, dt, detail in _results:
            if status == "FAIL":
                print(f"    ❌ {label}  →  {detail}")
        print(f"\n  ⚠️  {failed} test(s) FAILED")
        return 1
    else:
        print(f"\n  🎉 ALL {total} SERVER TESTS PASSED")
        return 0


# ====================================================================
def main():
    print("MareArts ANPR — Full Server API Test")
    print(f"Server: {BASE}")
    print(f"EU img: {EU_IMG}")
    print(f"KR img: {KR_IMG}")

    # connectivity check
    try:
        requests.get(f"{BASE}/api/health", timeout=5)
    except Exception:
        print(f"\n  ERROR: Cannot reach server at {BASE}")
        print("  Start it first:  ma-anpr server start")
        sys.exit(1)

    test_health()
    test_dashboard()
    test_detection()
    test_detection_mmc()
    test_history()
    test_watchlist()
    test_config()
    test_threads()

    rc = report()
    sys.exit(rc)


if __name__ == "__main__":
    main()
