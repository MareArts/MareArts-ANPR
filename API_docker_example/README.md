# MareArts ANPR Docker API Example

This example demonstrates how to deploy MareArts ANPR as a REST API service using Docker, with support for both V1 and V2 licenses including V14 models.

## Features

- FastAPI-based REST API
- Support for V1 and V2 licenses
- V14 model support with multi-backend inference
- Auto-update capability (checks for package updates)
- Basic authentication + API key security

## V14 Model Support (V2 License Only)

V14 models require:
- V2 license key (starts with "MAEV2:")
- Digital signature (16 hex characters)
- Backend selection (cpu, cuda, directml, tensorrt)

### Available V14 Models

**Standard Models (ONNX Runtime):**
- `v14_small_320p_fp32`, `v14_small_320p_fp16`
- `v14_small_640p_fp32`, `v14_small_640p_fp16`

**TensorRT Optimized (NVIDIA only):**
- `v14_small_320p_trt_fp16`, `v14_small_320p_trt_fp8`
- `v14_small_640p_trt_fp16`, `v14_small_640p_trt_fp8`

*Note: V14 middle and large models coming soon!*

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

#### V1 License (Legacy Models)
```bash
curl -X POST http://localhost:8000/process_image \
  -H "X-API-Key: your_secret_api_key" \
  -u "user@email.com:your_v1_serial_key" \
  -F "detection_model_version=v13_middle" \
  -F "ocr_model_version=v13_euplus" \
  -F "image=@test.jpg"
```

#### V2 License (V14 Models)
```bash
curl -X POST http://localhost:8000/process_image \
  -H "X-API-Key: your_secret_api_key" \
  -u "user@email.com:MAEV2:your_encrypted_key" \
  -F "detection_model_version=v14_small_640p_fp16" \
  -F "ocr_model_version=v13_euplus" \
  -F "signature=your_16_char_hex" \
  -F "backend=cuda" \
  -F "image=@test.jpg"
```

## API Endpoints

### POST /process_image

**Parameters:**
- `detection_model_version` (required): Detection model name
- `ocr_model_version` (required): OCR model name
- `signature` (optional): Required for V14 models with V2 license
- `backend` (optional): Backend for V14 models (default: "cpu")
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

# V2 License with V14 model
url = "http://localhost:8000/process_image"
headers = {"X-API-Key": "your_secret_api_key"}
auth = HTTPBasicAuth('user@email.com', 'MAEV2:your_key')

data = {
    "detection_model_version": "v14_small_640p_fp16",
    "ocr_model_version": "v13_euplus",
    "signature": "your_16_char_hex",
    "backend": "cuda"
}

with open("test.jpg", "rb") as f:
    files = {"image": ("test.jpg", f, "image/jpeg")}
    response = requests.post(url, headers=headers, auth=auth, data=data, files=files)

print(response.json())
```

## Backend Options for V14

- **cpu**: Cross-platform CPU inference (ONNX Runtime)
- **cuda**: NVIDIA GPU acceleration
- **directml**: Windows GPU acceleration (AMD/Intel/NVIDIA)
- **tensorrt**: NVIDIA TensorRT optimization (fastest)

## Notes

- First request downloads models (may take time)
- Models are cached after first download
- V14 models require more memory than legacy models
- TensorRT models require NVIDIA GPU with TensorRT installed
- Default backend is "cpu" for maximum compatibility