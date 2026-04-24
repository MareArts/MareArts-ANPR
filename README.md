# MareArts ANPR

[![PyPI version](https://badge.fury.io/py/marearts-anpr.svg)](https://badge.fury.io/py/marearts-anpr)
[![Python versions](https://img.shields.io/pypi/pyversions/marearts-anpr.svg)](https://pypi.org/project/marearts-anpr/)
[![Downloads](https://pepy.tech/badge/marearts-anpr)](https://pepy.tech/project/marearts-anpr)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](https://www.marearts.com/products/anpr)
[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen.svg)](http://live.marearts.com)

Automatic Number Plate Recognition SDK — detection + OCR for multiple regions, with GPU acceleration and ARM/Windows support.

**One license covers everything:** Python SDK, REST API Server, and Mobile App.

---

## Python SDK

Detect and read license plates in your own Python code.

```bash
pip install marearts-anpr          # CPU (all platforms)
ma-anpr gpu-setup cuda             # switch to NVIDIA CUDA
ma-anpr gpu-setup directml         # switch to Windows GPU
```

```python
from marearts_anpr import (
    ma_anpr_detector_v16, ma_anpr_ocr_v16, marearts_anpr_from_image_file
)

detector = ma_anpr_detector_v16("640p_fp32", user_name, serial_key, signature)
ocr = ma_anpr_ocr_v16("fp32", "univ", user_name, serial_key, signature)

result = marearts_anpr_from_image_file(detector, ocr, "car.jpg")
print(result)
# {'results': [{'ocr': 'ABC1234', 'ocr_conf': 99, 'ltrb': [...], ...}], ...}
```

**[Full SDK Documentation and Examples →](python-sdk/)**

---

## REST API Server

Built-in server with web dashboard and REST API.

```bash
pip install marearts-anpr           # server included in base install
ma-anpr config                     # one-time credential setup
ma-anpr server start               # http://localhost:8000
```

```bash
curl -X POST http://localhost:8000/api/anpr -F "image=@car.jpg"
```

**[Server Documentation →](server/)**

---

## Mobile App

On-device ANPR for iOS and Android — parking, security, fleet management.

[![Download on App Store](https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg)](https://apps.apple.com/us/app/marearts-anpr/id6753904859) [![Get it on Google Play](https://raw.githubusercontent.com/MareArts/MareArts-ANPR/main/promotion_image/google_play_badge.svg)](https://play.google.com/store/apps/details?id=com.marearts.anpr)

- On-device AI (~100-160ms)
- Team collaboration, webhooks, cloud sync
- CSV export, map view, whitelist/blacklist

**[Mobile App Guide →](mobile-app/)**

---

## Supported Regions

**V16** uses **per-country character sets** — pass a 2-letter country code (e.g. `de`, `au`, `ru`) for best accuracy, or a group code (`eu`, `asia`, `eup`, `na`, `univ`, etc.).

Supports **80+ countries** across 12 regional groups: EU (37), Ex-USSR (15), Asia (17), N. America (3), S. America (2), Africa (2), Oceania (2), UK (4), China, Korea, Japan.

Unknown regions fall back to `univ` with a warning.

See **[Full Region & Country Reference](python-sdk/README.md#regions)** for the complete table with all country codes and flags.

---

## More from MareArts

- **[MareArts Road Objects](https://github.com/MareArts/MareArts-Road-Objects)** — Detect persons, vehicles, and 2-wheelers
- **[MareArts Xcolor](https://github.com/MareArts/MareArts-Xcolor)** — Color extraction and similarity
- **[MareArts MAST](https://github.com/MareArts/MareArts-MAST)** — Real-time panoramic stitching

---

## Support

| | |
|---|---|
| Homepage | [marearts.com](https://marearts.com) |
| License | [marearts.com/products/anpr](https://www.marearts.com/products/anpr) |
| Live Demo | [live.marearts.com](http://live.marearts.com) |
| Contact | [hello@marearts.com](mailto:hello@marearts.com) |
| YouTube | [Video Examples](https://www.youtube.com/playlist?list=PLvX6vpRszMkxJBJf4EjQ5VCnmkjfE59-J) |

---

(c) 2026 MareArts. All rights reserved.
