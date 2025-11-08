# MareArts ANPR Docker API Example

This example demonstrates how to deploy MareArts ANPR as a REST API service using Docker with V14 models.

## Features

- FastAPI-based REST API
- V14 model support with multi-backend inference (cpu, cuda, directml)
- **Smart model caching** - Reuses initialized models when same model requested (>3.7.0)
- **Dynamic region switching** - Changes region without reloading OCR model (>3.7.0)
- Auto-update capability (checks for package updates)
- Basic authentication + API key security

## V14 Model Requirements

V14 models require:

- License serial key
- Digital signature (provided with license)
- Backend selection (cpu, cuda, directml) - default: cpu
- Region parameter (kr, eup, na, cn, univ) - default: univ

### Available V14 Models

**Detector Models (example, actual models may vary):**

- `v14_pico_640p_fp32` - Fastest, smallest
- `v14_micro_640p_fp32` - Fast with good accuracy
- `v14_small_640p_fp32` - Balanced performance
- `v14_medium_640p_fp32` - Higher accuracy
- `v14_large_640p_fp32` - Highest accuracy

**OCR Models (example, actual models may vary):**

- `v14_pico_fp32` - Fast
- `v14_micro_fp32` - Balanced
- `v14_small_fp32` - Fastest
- `v14_medium_fp32` - High accuracy
- `v14_large_fp32` - Highest exact match

**Regions:**

- `kr` - Korean plates (best for Korean)
- `eup` - European+ plates (EU countries + additional European countries + Indonesia)
- `na` - North American plates (USA, Canada)
- `cn` - Chinese plates
- `univ` - Universal (all regions) - **default, but choose specific region for best accuracy**

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
curl -X POST http://localhost:8000/process_image \
  -H "X-API-Key: your_secret_api_key" \
  -u "user@email.com:serial_key" \
  -F "detection_model_version=v14_medium_640p_fp32" \
  -F "ocr_model_version=v14_large_fp32" \
  -F "region=univ" \
  -F "signature=your_signature" \
  -F "backend=cuda" \
  -F "image=@test.jpg"
```

## API Endpoints

### POST /process_image

**Parameters:**

- `detection_model_version` (required): Detection model name (e.g., v14_medium_640p_fp32)
- `ocr_model_version` (required): OCR model name (e.g., v14_medium_fp32)
- `region` (optional): OCR region - kr, eup, na, cn, univ (default: univ)
- `signature` (required): Signature for V14 models (mandatory)
- `backend` (optional): Backend for V14 models - cpu, cuda, directml (default: cpu)
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

# V14 models
url = "http://localhost:8000/process_image"
headers = {"X-API-Key": "your_secret_api_key"}
auth = HTTPBasicAuth('user@email.com', 'serial_key')

data = {
    "detection_model_version": "v14_small_640p_fp32",
    "ocr_model_version": "v14_small_fp32",
    "region": "kr",  # Optional: kr, eup, na, cn, univ (default: univ). Choose specific region for best accuracy!
    "signature": "your_signature",
    "backend": "cuda"
}

with open("test.jpg", "rb") as f:
    files = {"image": ("test.jpg", f, "image/jpeg")}
    response = requests.post(url, headers=headers, auth=auth, data=data, files=files)

print(response.json())
```

## Backend Options for V14

- **cpu**: CPU inference (default)
- **cuda**: NVIDIA GPU acceleration
- **directml**: DirectML for Windows GPU

## Notes

- **API automatically reuses models**: If same model requested, no reinitialization (saves time & memory)
- **Dynamic region switching**: Change region parameter without reloading OCR model (>3.7.0)
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
