# MareArts ANPR — Python SDK

## Installation

```bash
# CPU (all platforms: Linux, macOS, Windows, ARM)
pip install marearts-anpr

# GPU — use the built-in setup command (recommended):
ma-anpr gpu-setup cuda              # NVIDIA CUDA
ma-anpr gpu-setup directml          # Windows AMD/Intel/NVIDIA
ma-anpr gpu-setup cpu               # switch back to CPU-only
```

> **Why `gpu-setup` instead of `pip install [gpu]`?**
> `onnxruntime` (CPU) and `onnxruntime-gpu` are separate packages that conflict.
> pip extras install the GPU package but don't remove the CPU one, which shadows the GPU provider.
> `ma-anpr gpu-setup` handles the uninstall/install correctly in one step.

**Requirements:** Python 3.10 — 3.14

---

## License Setup

Get your credentials at [marearts.com/products/anpr](https://www.marearts.com/products/anpr).

```bash
ma-anpr config
```

This saves credentials to `~/.marearts/.marearts_env`. Alternatively, set environment variables:

```bash
export MAREARTS_ANPR_USERNAME="your-email"
export MAREARTS_ANPR_SERIAL_KEY="your-key"
export MAREARTS_ANPR_SIGNATURE="your-signature"
```

---

## Initialize Models

```python
from marearts_anpr import (
    ma_anpr_detector_v16, ma_anpr_ocr_v16, ma_anpr_mmc,
    marearts_anpr_from_image_file,
    marearts_anpr_from_pil,
    marearts_anpr_from_cv2,
)

detector = ma_anpr_detector_v16("640p_fp32", user_name, serial_key, signature)
ocr = ma_anpr_ocr_v16("fp32", "univ", user_name, serial_key, signature)

# MMC is optional — requires internet
# Adds 7 cloud AI features: make, model, color, type, front/rear, plate nation, plate OCR
mmc = ma_anpr_mmc(user_name, serial_key, signature)
```

> **Performance tip:** Load models once, then call detection in a loop. Model loading takes seconds but each detection call takes milliseconds. Never put `ma_anpr_detector_v16()` or `ma_anpr_ocr_v16()` inside a loop.

All three input functions (`marearts_anpr_from_image_file`, `marearts_anpr_from_pil`, `marearts_anpr_from_cv2`) accept the same argument combinations. Examples below use `marearts_anpr_from_image_file` but the same patterns work with all three.

---

## MMC and Internet

MMC is a cloud feature that requires internet. The SDK handles it simply:

- **With internet:** Pass `mmc` to get vehicle info. Works normally.
- **Without internet:** Don't pass `mmc`. ANPR runs fully offline with zero overhead.
- **Internet drops during use:** MMC call times out (10s) and returns `mmc_error`. Local ANPR results (plates, OCR, bboxes) are still returned. Only MMC fields are missing.
- **Daily quota exhausted:** MMC returns `mmc_error`. Local ANPR results are still returned.

In all error cases you always get the full local ANPR result — plates, OCR text, bounding boxes, confidence scores. Only the 7 MMC fields will be missing, and `mmc_error` tells you why.

```python
# With MMC (requires internet)
result = marearts_anpr_from_image_file(detector, ocr, "car.jpg", mmc)

# Without MMC (fully offline, no internet needed)
result = marearts_anpr_from_image_file(detector, ocr, "car.jpg")

# Always check mmc_error — you still get ANPR results even when MMC fails
if result.get("mmc_error"):
    print(f"MMC skipped: {result['mmc_error']}")
    # result["results"] still has plates, OCR, bboxes — just no mmc_* fields
for r in result["results"]:
    print(f"  {r['ocr']} ({r['ocr_conf']}%)")
```

No automatic recovery or retry. You control whether to use MMC or not.

---

## Usage: All Combinations

### 1. Detection Only (detector, image)

Locate plates without reading text.

```python
result = marearts_anpr_from_image_file(detector, "car.jpg")
```

Output:
```python
{
    "results": [
        {
            "ocr": "",
            "ocr_conf": 0.0,
            "ltrb": [120, 230, 380, 290],
            "ltrb_conf": 95
        }
    ],
    "ltrb_proc_sec": 0.03,
    "ocr_proc_sec": 0.0
}
```

### 2. OCR Only (ocr, image)

Read text from a pre-cropped plate image (no detection). `ltrb` is set to the full image bounds, `ltrb_conf` is always `100`.

```python
result = marearts_anpr_from_image_file(ocr, "plate_crop.jpg")
```

Output:
```python
{
    "results": [
        {
            "ocr": "ABC1234",
            "ocr_conf": 99,
            "ltrb": [0, 0, 300, 80],
            "ltrb_conf": 100
        }
    ],
    "ltrb_proc_sec": 0.0,
    "ocr_proc_sec": 0.01
}
```

### 3. Detection + OCR (detector, ocr, image)

Full ANPR pipeline: detect plates then read text.

```python
result = marearts_anpr_from_image_file(detector, ocr, "car.jpg")
```

Output:
```python
{
    "results": [
        {
            "ocr": "ABC1234",
            "ocr_conf": 99,
            "ltrb": [120, 230, 380, 290],
            "ltrb_conf": 95
        }
    ],
    "ltrb_proc_sec": 0.03,
    "ocr_proc_sec": 0.01
}
```

### 4. Detection + MMC (detector, image, mmc)

Detect plates and get vehicle info, without reading plate text.

```python
result = marearts_anpr_from_image_file(detector, "car.jpg", mmc)
```

Output:
```python
{
    "results": [
        {
            "ocr": "ABC1234",
            "ocr_conf": 88.0,
            "ltrb": [120, 230, 380, 290],
            "ltrb_conf": 95,
            "mmc_make": "Toyota",
            "mmc_make_conf": 0.92,
            "mmc_model": "Camry",
            "mmc_model_conf": 0.87,
            "mmc_color": "White",
            "mmc_color_conf": 0.95,
            "mmc_type": "Sedan",
            "mmc_type_conf": 0.91,
            "mmc_vehicle_side": "front",
            "mmc_vehicle_side_conf": 0.97,
            "mmc_plate_nation": "US",
            "mmc_plate_nation_conf": 0.85,
            "mmc_plate": "ABC1234",
            "mmc_plate_conf": 0.88
        }
    ],
    "ltrb_proc_sec": 0.03,
    "ocr_proc_sec": 0.0,
    "mmc_model_sec": 0.15,
    "mmc_request_sec": 0.42,
    "mmc_daily_limit": 1000,
    "mmc_calls_today": 5,
    "mmc_request_id": "req_abc123"
}
```

> When local `ocr` is empty (`""`), MMC backfills `ocr` and `ocr_conf` from its server-side plate reading (`mmc_plate` / `mmc_plate_conf`).

### 5. OCR + MMC (ocr, image, mmc)

Read plate text and get vehicle info from a pre-cropped image.

```python
result = marearts_anpr_from_image_file(ocr, "plate_crop.jpg", mmc)
```

Output:
```python
{
    "results": [
        {
            "ocr": "ABC1234",
            "ocr_conf": 99,
            "ltrb": [0, 0, 300, 80],
            "ltrb_conf": 100,
            "mmc_make": "Toyota",
            "mmc_make_conf": 0.92,
            # ... same 7 mmc fields as above ...
        }
    ],
    "ltrb_proc_sec": 0.0,
    "ocr_proc_sec": 0.01,
    "mmc_model_sec": 0.15,
    "mmc_request_sec": 0.42,
    "mmc_daily_limit": 1000,
    "mmc_calls_today": 6,
    "mmc_request_id": "req_abc124"
}
```

### 6. Detection + OCR + MMC (detector, ocr, image, mmc)

Full pipeline: detect plates, read text, and get vehicle info.

```python
result = marearts_anpr_from_image_file(detector, ocr, "car.jpg", mmc)
```

Output:
```python
{
    "results": [
        {
            "ocr": "ABC1234",
            "ocr_conf": 99,
            "ltrb": [120, 230, 380, 290],
            "ltrb_conf": 95,
            "mmc_make": "Toyota",
            "mmc_make_conf": 0.92,
            "mmc_model": "Camry",
            "mmc_model_conf": 0.87,
            "mmc_color": "White",
            "mmc_color_conf": 0.95,
            "mmc_type": "Sedan",
            "mmc_type_conf": 0.91,
            "mmc_vehicle_side": "front",
            "mmc_vehicle_side_conf": 0.97,
            "mmc_plate_nation": "US",
            "mmc_plate_nation_conf": 0.85,
            "mmc_plate": "ABC1234",
            "mmc_plate_conf": 0.88
        }
    ],
    "ltrb_proc_sec": 0.03,
    "ocr_proc_sec": 0.01,
    "mmc_model_sec": 0.15,
    "mmc_request_sec": 0.42,
    "mmc_daily_limit": 1000,
    "mmc_calls_today": 7,
    "mmc_request_id": "req_abc125"
}
```

---

## Input Formats

All six combinations above work with all three input functions:

```python
from PIL import Image

# From file path
result = marearts_anpr_from_image_file(detector, ocr, "car.jpg")

# From Pillow image
result = marearts_anpr_from_pil(detector, ocr, Image.open("car.jpg"))

# From numpy array (BGR format, same as OpenCV)
import numpy as np
result = marearts_anpr_from_cv2(detector, ocr, img_bgr)
```

> **Note:** `marearts_anpr_from_cv2` accepts a numpy array in BGR channel order. OpenCV is NOT required — any BGR numpy array works.

---

## Output Fields Reference

### Base fields (always present)

| Field | Type | Description |
|-------|------|-------------|
| `results` | list | List of detected plates |
| `ltrb_proc_sec` | float | Detection time in seconds (0.0 if no detector) |
| `ocr_proc_sec` | float | OCR time in seconds (0.0 if no OCR) |

### Per-plate fields (each item in `results`)

| Field | Type | Description |
|-------|------|-------------|
| `ocr` | str | Plate text (`""` if detection-only) |
| `ocr_conf` | int | OCR confidence 0-100 (`0` if detection-only) |
| `ltrb` | list[int] | Bounding box `[left, top, right, bottom]` in pixels |
| `ltrb_conf` | int | Detection confidence 0-100 (`100` if OCR-only) |

### MMC fields (when mmc is passed)

Per-plate — 7 features, each with `_conf` score:

| # | Field | Description |
|---|-------|-------------|
| 1 | `mmc_make` / `mmc_make_conf` | Vehicle make (e.g. Toyota) |
| 2 | `mmc_model` / `mmc_model_conf` | Vehicle model (e.g. Camry) |
| 3 | `mmc_color` / `mmc_color_conf` | Vehicle color (e.g. White) |
| 4 | `mmc_type` / `mmc_type_conf` | Vehicle type (sedan, SUV, truck, etc.) |
| 5 | `mmc_vehicle_side` / `mmc_vehicle_side_conf` | Front or rear view |
| 6 | `mmc_plate_nation` / `mmc_plate_nation_conf` | Plate country/nation |
| 7 | `mmc_plate` / `mmc_plate_conf` | Plate OCR (cloud AI — see note below) |

> **`mmc_plate` vs `plate_text`:** `plate_text` is the local on-device ANPR result, while `mmc_plate` is a separate plate reading from cloud AI. The cloud OCR can be more accurate in some cases. You can compare both values and pick the one with higher confidence, or use `mmc_plate` as a cross-check to validate local results.

Response-level:

| Field | Description |
|-------|-------------|
| `mmc_model_sec` | MMC model inference time |
| `mmc_request_sec` | Total MMC API round-trip time |
| `mmc_daily_limit` | Your daily quota |
| `mmc_calls_today` | Calls used today |
| `mmc_request_id` | Request tracking ID |
| `mmc_error` | Error message (only on failure: timeout, quota, no internet) |

---

## Dynamic Region Switching

Switch regions without reloading the model (instant, in-memory):

```python
ocr.set_region('kr')     # Korean plates
ocr.set_region('eup')    # Europe+
ocr.set_region('na')     # North America
ocr.set_region('cn')     # China
ocr.set_region('jp')     # Japan (V16 only)
ocr.set_region('univ')   # Universal (all regions)

# Check current state
print(ocr.current_region)      # e.g. 'kr'
print(ocr.available_regions)   # e.g. ['africa', 'asia', 'china', ..., 'univ']
```

---

## V16 Models

### Detector

| Model | Description |
|-------|-------------|
| `640p_fp32` | High accuracy (recommended) |
| `640p_int8` | High accuracy, smaller file |
| `320p_fp32` | Fast |
| `320p_int8` | Fast, smaller file |

```python
detector = ma_anpr_detector_v16(
    "640p_fp32",           # model name
    user_name, serial_key, signature,
    backend="auto",        # auto, cpu, cuda, dml (auto → cuda > dml > cpu)
    conf_thres=0.25,       # detection confidence threshold
    iou_thres=0.5          # NMS IoU threshold
)
```

### OCR

| Model | Description |
|-------|-------------|
| `fp32` | Standard (recommended) |
| `int8` | Smaller file |

```python
ocr = ma_anpr_ocr_v16(
    "fp32",                # model name
    "univ",                # region: univ, eup, na, kr, cn, jp
    user_name, serial_key, signature,
    backend="auto"         # auto, cpu, cuda, dml
)
```

### Regions

**V16** uses **per-country character sets** — pass a 2-letter country code for best accuracy.

| Group | Input | Countries |
|-------|-------|-----------|
| **EU** | `eu` | 🇦🇩`ad` 🇦🇱`al` 🇦🇹`at` 🇦🇽`ax` 🇧🇦`ba` 🇧🇪`be` 🇧🇬`bg` 🇨🇭`ch` 🇨🇾`cy` 🇨🇿`cz` 🇩🇪`de` 🇩🇰`dk` 🇪🇸`es` 🇫🇮`fi` 🇫🇷`fr` 🇬🇷`gr` 🇭🇷`hr` 🇭🇺`hu` 🇮🇪`ie` 🇮🇸`is` 🇮🇹`it` 🇱🇮`li` 🇱🇺`lu` 🇲🇨`mc` 🇲🇪`me` 🇲🇰`mk` 🇲🇹`mt` 🇳🇱`nl` 🇳🇴`no` 🇵🇱`pl` 🇵🇹`pt` 🇷🇴`ro` 🇷🇸`rs` 🇸🇪`se` 🇸🇮`si` 🇸🇰`sk` 🇸🇲`sm` (37) |
| **Ex-USSR** | `exussr` | 🇦🇲`am` 🇦🇿`az` 🇧🇾`by` 🇪🇪`ee` 🇬🇪`ge` 🇰🇬`kg` 🇰🇿`kz` 🇱🇹`lt` 🇱🇻`lv` 🇲🇩`md` 🇷🇺`ru` `su` 🇹🇯`tj` 🇺🇦`ua` 🇺🇿`uz` (15) |
| **EU+** | `eup` | EU + Ex-USSR + UK (broad) |
| **Asia** | `asia` | 🇦🇪`ae` 🇧🇭`bh` 🇮🇩`id` 🇮🇱`il` 🇮🇶`iq` 🇮🇷`ir` 🇰🇭`kh` 🇱🇦`la` 🇲🇳`mn` 🇲🇾`my` 🇵🇸`ps` 🇶🇦`qa` 🇸🇦`sa` 🇸🇬`sg` 🇹🇭`th` 🇹🇷`tr` 🇻🇳`vn` (17) |
| **Africa** | `africa` | 🇪🇬`eg` 🇲🇦`ma` (2) |
| **Oceania** | `oceania` | 🇦🇺`au` 🇳🇿`nz` (2) |
| **UK** | `gb`/`uk` | 🇬🇧`uk` 🇬🇬`gg` 🇬🇮`gi` 🇯🇪`je` (4) |
| **N. America** | `na` | 🇺🇸`us` 🇨🇦`ca` 🇲🇽`mx` (3) |
| **S. America** | `southamerica` | 🇦🇷`ar` 🇧🇷`br` (2) |
| **China** | `cn` | 🇨🇳`cn` 🇭🇰`hk` (2) |
| **Korea** | `kr` | 🇰🇷 South Korea |
| **Japan** | `jp` | 🇯🇵 Japan |
| **Universal** | `univ` | All characters (default) |

**Accepted input formats** (case-insensitive, spaces/underscores/hyphens ignored):

- **2-letter ISO code**: `de`, `au`, `ru`, `us`, `kr`, `jp`, `cn`, ...
- **3-letter code**: `kor`, `jpn`, `chn`, `rus`, `usa`, ...
- **Full name**: `germany`, `australia`, `russia`, `brazil`, `turkey`, ...
- **Native name**: `deutschland`, `turkiye`, ...
- **Group code**: `eu`, `eup` / `eu+` / `euplus`, `asia`, `africa`, `oceania`, `na`, `exussr`, `southamerica`, `univ`, ...
- **Aliases**: `korean`, `japanese`, `chinese`, `europe`, `latin america`, `britain`, ...

Unknown regions **fall back to `univ`** with a warning.

> **Note**: `ch` = Switzerland (ISO 3166), use `cn` for China.

---

## CLI

```bash
# Read plates from image (uses V16 by default)
ma-anpr car.jpg
ma-anpr car.jpg --region kr
ma-anpr car.jpg --detector-model 320p_int8 --ocr-model int8
ma-anpr car.jpg --backend cuda

# Batch processing
ma-anpr *.jpg --json results.json

# Specify detector/OCR version
ma-anpr car.jpg --detector-version v14 --detector-model micro_640p_fp32
ma-anpr car.jpg --ocr-version v15 --ocr-model small_fp32

# Save annotated image
ma-anpr car.jpg --output detected.jpg

# Other commands
ma-anpr config          # Configure credentials
ma-anpr validate        # Validate license
ma-anpr model-info      # List all models, regions, backends
ma-anpr gpu-info        # Check GPU/backend support
ma-anpr --version       # Show version
```

### Server commands

```bash
ma-anpr server start                     # foreground
ma-anpr server start --daemon            # background
ma-anpr server start --port 9000         # custom port
ma-anpr server start --workers 8         # set thread pool size
ma-anpr server start --config config.yaml
ma-anpr server stop                      # stop current config server
ma-anpr server stop --port 8001          # stop by port
ma-anpr server stop --pid 12345          # stop by PID
ma-anpr server stop --all                # stop all ANPR instances
ma-anpr server stop --force              # force kill (SIGKILL)
ma-anpr server list                      # list all running instances
ma-anpr server restart
ma-anpr server status
ma-anpr server upgrade
ma-anpr server logs
ma-anpr server logs --follow

# Detection via CLI (server must be running)
ma-anpr server detect car.jpg            # local ANPR only
ma-anpr server detect car.jpg --mmc      # ANPR + MMC enrichment
ma-anpr server detect car.jpg --region kr
ma-anpr server mmc                       # MMC status and quota
ma-anpr server health                    # server health
```

---

## Backend Options

| Backend | Platform | Install |
|---------|----------|---------|
| `auto` | Auto-detect best (default) | `pip install marearts-anpr` |
| `cpu` | All platforms | `pip install marearts-anpr` |
| `cuda` | Linux/Windows with NVIDIA GPU | `ma-anpr gpu-setup cuda` |
| `dml` | Windows (AMD/Intel/NVIDIA) | `ma-anpr gpu-setup directml` |

---

## Legacy Models

### V14 Detector

Sizes: `pico`, `micro`, `small`, `medium`, `large` | Resolutions: `320p`, `640p` | Precision: `fp32`, `fp16`

```python
from marearts_anpr import ma_anpr_detector_v14

detector = ma_anpr_detector_v14(
    "micro_320p_fp32",     # {size}_{resolution}_{precision}
    user_name, serial_key, signature,
    backend="auto",        # auto, cpu, cuda, dml
    conf_thres=0.25,
    iou_thres=0.5
)
```

### V15 OCR

Sizes: `pico`, `micro`, `small`, `medium`, `large` | Precision: `fp32`, `int8`

Regions: `univ`, `eup`, `na`, `kr`, `cn`

```python
from marearts_anpr import ma_anpr_ocr_v15

ocr = ma_anpr_ocr_v15(
    "small_fp32",          # {size}_{precision}
    "univ",                # region
    user_name, serial_key, signature,
    backend="auto"
)
```

### V14 OCR

Sizes: `pico`, `micro`, `small`, `medium`, `large` | Precision: `fp32` only

Regions: `univ`, `eup`, `na`, `kr`, `cn`

```python
from marearts_anpr import ma_anpr_ocr_v14

ocr = ma_anpr_ocr_v14(
    "small_fp32",          # {size}_fp32
    "univ",                # region
    user_name, serial_key, signature,
    backend="auto"
)
```

### Generic Wrapper (version selection)

```python
from marearts_anpr import ma_anpr_ocr

ocr = ma_anpr_ocr("fp32", "univ", user_name, serial_key, signature, version="v16")
ocr = ma_anpr_ocr("small_fp32", "univ", user_name, serial_key, signature, version="v15")
ocr = ma_anpr_ocr("small_fp32", "univ", user_name, serial_key, signature, version="v14")
```

---

## Examples

See [examples/](examples/) for complete working code:
- [basic.py](examples/basic.py) — All 6 combinations (det/ocr/mmc) with output
- [advanced.py](examples/advanced.py) — Manual pipeline, input formats, region switching, backends

---

## Support

- Homepage: [marearts.com](https://marearts.com)
- License: [marearts.com/products/anpr](https://www.marearts.com/products/anpr)
- Contact: [hello@marearts.com](mailto:hello@marearts.com)
