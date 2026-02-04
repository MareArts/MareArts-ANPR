# MareArts ANPR Docker API Example

This example demonstrates how to deploy MareArts ANPR as a REST API service using Docker.

## Features

- FastAPI-based REST API
- V14 Detector + V15 OCR support (V14 OCR backward compatible)
- Multi-backend inference (cpu, cuda, directml)
- **Smart model caching** - Reuses initialized models when same model requested
- **Dynamic region switching** - Changes region without reloading OCR model
- **Easy OCR version switching** - Select v15 (latest) or v14 via API parameter
- Auto-update capability (checks for package updates)
- Basic authentication + API key security

## Model Requirements

All models require:

- License serial key
- Digital signature (provided with license)
- Backend selection (cpu, cuda, directml) - default: cpu
- Region parameter - default: univ

### Available Models

**V14 Detector Models:**

- `pico_640p_fp32` - Smallest, fast
- `micro_320p_fp32` - Fast, recommended
- `small_640p_fp32` - Balanced performance
- `medium_640p_fp32` - Higher accuracy
- `large_640p_fp32` - Highest accuracy

**V15 OCR Models (Latest - Recommended):**

- `pico_fp32` / `pico_int8` - Smallest
- `micro_fp32` / `micro_int8` - Fast
- `small_fp32` / `small_int8` - Balanced
- `medium_fp32` / `medium_int8` - High accuracy
- `large_fp32` / `large_int8` - Best accuracy

**V14 OCR Models (Backward Compatible):**

- Same model names as V15: `pico_fp32`, `micro_fp32`, etc.
- Use `ocr_version="v14"` parameter to select

**Regions:**

- `kor` or `kr` - Korean plates
- `euplus` or `eup` - European+ plates
- `na` - North American plates
- `china` or `cn` - Chinese plates
- `univ` - Universal (all regions, default)

## Quick Start

### 1. Build Docker Image
```bash
./build_image.sh
```

### 2. Run Container
```bash
./run_container.sh
```

### 3. Test API

```bash
# Using V15 OCR (Latest - Default)
curl -X POST http://localhost:8000/process_image \
  -H "X-API-Key: your_secret_api_key" \
  -u "user@email.com:serial_key" \
  -F "detection_model_version=medium_640p_fp32" \
  -F "ocr_model_version=large_fp32" \
  -F "ocr_version=v15" \
  -F "region=univ" \
  -F "signature=your_signature" \
  -F "backend=cuda" \
  -F "image=@test.jpg"

# Using V14 OCR (Backward Compatible)
curl -X POST http://localhost:8000/process_image \
  -H "X-API-Key: your_secret_api_key" \
  -u "user@email.com:serial_key" \
  -F "detection_model_version=medium_640p_fp32" \
  -F "ocr_model_version=large_fp32" \
  -F "ocr_version=v14" \
  -F "region=univ" \
  -F "signature=your_signature" \
  -F "backend=cpu" \
  -F "image=@test.jpg"
```

## API Endpoints

### POST /process_image

**Parameters:**

- `detection_model_version` (required): V14 Detector model name (e.g., medium_640p_fp32)
- `ocr_model_version` (required): OCR model name (e.g., large_fp32)
- `ocr_version` (optional): OCR version - v15 (latest, default) or v14 (backward compatible)
- `region` (optional): OCR region - kor/kr, euplus/eup, na, china/cn, univ (default: univ)
- `signature` (required): Signature (mandatory)
- `backend` (optional): Backend - cpu, cuda, directml (default: cpu)
- `image` (required): Image file

**Authentication:**

- Header: `X-API-Key: your_secret_api_key`
- Basic Auth: Username and serial key

### GET /health

Returns API status and marearts-anpr version.

## Python Client Example

```python
import requests
from requests.auth import HTTPBasicAuth

# Setup
url = "http://localhost:8000/process_image"
headers = {"X-API-Key": "your_secret_api_key"}
auth = HTTPBasicAuth('user@email.com', 'serial_key')

# Using V15 OCR (Latest - Recommended)
data = {
    "detection_model_version": "small_640p_fp32",
    "ocr_model_version": "small_fp32",
    "ocr_version": "v15",  # v15 (latest) or v14 (backward compatible)
    "region": "kor",       # kor/kr, euplus/eup, na, china/cn, univ (default: univ)
    "signature": "your_signature",
    "backend": "cuda"
}

with open("test.jpg", "rb") as f:
    files = {"image": ("test.jpg", f, "image/jpeg")}
    response = requests.post(url, headers=headers, auth=auth, data=data, files=files)

print(response.json())

# Using V14 OCR (Backward Compatible)
# Just change: "ocr_version": "v14"
```

## Backend Options for V14

- **cpu**: CPU inference (default)
- **cuda**: NVIDIA GPU acceleration
- **directml**: DirectML for Windows GPU

## Notes

- **API automatically reuses models**: If same model requested, no reinitialization (saves time & memory)
- **Dynamic region switching**: Change region parameter without reloading OCR model (>3.6.5)
## Supported Modes

### Detector
  - model: v14_pico_640p_fp32, v14_micro_640p_fp32, v14_small_640p_fp32, v14_medium_640p_fp32, v14_large_640p_fp32
  - backend: "cpu", "cuda", "directml", "auto" (default: cpu)

### OCR
  - model: v14_pico_fp32, v14_micro_fp32, v14_small_fp32, v14_medium_fp32, v14_large_fp32
  - region: "kr", "eup", "na", "cn", "univ" (default: univ)
  - backend: "cpu", "cuda", "directml", "auto" (default: cpu)
- First request downloads models (may take time)
- Models are cached after first download
- V14 models require more memory than legacy models
- TensorRT models require NVIDIA GPU with TensorRT installed
- Default backend is "cpu" for maximum compatibility

## Optimization Examples

**Scenario 1: Same models, different regions**
```python
# Request 1: kr region → Initializes models
# Request 2: eup region → Reuses models, only switches region (fast!)
# Request 3: na region → Reuses models, only switches region (fast!)
```

**Scenario 2: Mixed requests**
```python
# Request 1: v14_medium detector + v14_medium OCR, kr → Initialize both
# Request 2: v14_medium detector + v14_medium OCR, kr → Reuse both (instant)
# Request 3: v14_medium detector + v14_medium OCR, eup → Reuse detector, switch region only
# Request 4: v14_medium detector + v14_large OCR, na → Reuse detector, reload OCR (model changed)
```
