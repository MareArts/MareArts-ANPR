# MareArts ANPR — Test Suite

## Quick Start

```bash
# SDK test (no server needed)
python test_sdk.py

# Server test (start server first)
ma-anpr server start
python test_server.py
```

Credentials are loaded from `~/.marearts/.marearts_env`.
Zero arguments needed — just run and get a full report.

---

## test_sdk.py — Python SDK (V16)

| Section | What it tests |
|---------|---------------|
| **Package & License** | `import`, `validate_user_key`, `validate_user_key_with_signature`, `validate_user_key_with_dates` |
| **Detector V16** | `ma_anpr_detector_v16` — 640p_fp32, 640p_int8, 320p_fp32, 320p_int8 |
| **OCR V16** | `ma_anpr_ocr_v16` — fp32 & int8 × eu, kr, univ |
| **Inference** | `from_image_file`, `from_cv2`, `from_pil` × EU & KR images |
| **MMC** | `ma_anpr_mmc` init + `enrich()` |
| **Region Aliases** | `normalize_region_alias` |

---

## test_server.py — Server REST API

| Section | What it tests |
|---------|---------------|
| **Health & System** | `/api/health`, `/api/health/check`, `/api/config`, `/api/stats`, `/api/stats/chart`, `/api/threads`, `/api/logs`, `/api/regions`, `/api/region`, `/api/mmc/status` |
| **Dashboard** | `GET /` serves HTML |
| **Detection** | `/api/anpr` (file EU, file KR), `/api/anpr/base64`, `/api/anpr/binary`, `/api/anpr/batch` |
| **Detection + MMC** | `/api/anpr/mmc` (file), `/api/anpr/mmc/base64`, `/api/anpr/mmc/binary`, `/api/anpr/mmc/batch` |
| **History** | `/api/history`, `/api/history/search`, `/api/history/{id}`, `/api/history/export/json`, `/api/history/export/csv` |
| **Watchlist & Alerts** | `/api/watchlist` (list, add, delete), `/api/alerts`, `/api/alerts/count`, `/api/alerts/read` |
| **Config** | `PUT /api/region` round-trip |
| **Threads** | `PUT /api/threads` round-trip |

---

## Folder Structure

```
marearts-anpr-test/
├── README.md
├── test_sdk.py
├── test_server.py
└── sample/
    ├── eu-a.jpg, eu-b.jpg
    ├── kr-a.jpg, kr-b.jpg
    └── 1–18.jpg
```
