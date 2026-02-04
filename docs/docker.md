# Docker Deployment

**Last Updated:** February 4, 2026

Deploy MareArts ANPR as a REST API service using Docker with V14 Detector + V15 OCR (V14 OCR also supported).

## Quick Start

### Build and Run

```bash
cd API_docker_example/

# Build Docker image
./build_image.sh

# Run container
./run_container.sh
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Process Image
**POST** `/process_image`

Authentication: Basic Auth (username/password) + API Key

Form data:
- `detection_model_version`: V14 Detector model name
  - Example: "micro_320p_fp32" or "medium_640p_fp32"
  - Sizes: pico, micro, small, medium, large
  - Resolutions: 320p (fast), 640p (accurate)
  - Precision: fp32 (fast), fp16 (compact)
- `ocr_model_version`: OCR model name
  - Example: "medium_fp32"
  - Sizes: pico, micro, small, medium, large
  - Precision: fp32 (or int8 for smaller files)
- `ocr_version`: (Optional) OCR version - "v15" (latest, default) or "v14" (backward compatible)
- `region`: OCR region
  - Options: "kor"/"kr", "euplus"/"eup", "na", "china"/"cn", "univ"
- `signature`: Required signature
- `backend`: (Optional) Backend: "cpu", "cuda", "directml" (default: "cpu")
- `image`: Image file (JPEG/PNG)

Headers:
- `X-API-Key`: your_secret_api_key
- `Authorization`: Basic Auth with credentials

### Health Check
**GET** `/health`

Returns API status and version information.

## Files Overview

```
API_docker_example/
├── dockerfile          # Docker image configuration
├── app.py             # FastAPI application
├── requirements.txt   # Python dependencies
├── build_image.sh     # Build Docker image
├── run_container.sh   # Run Docker container
├── api_call.sh        # Example API call
└── request.py         # Python client example
```

## Dockerfile

Based on Python 3.12 slim image with:
- FastAPI web framework
- OpenCV for image processing
- MareArts ANPR SDK

Supports multiple architectures:
- **linux/amd64** (x86_64) - Intel/AMD processors
- **linux/arm64** (aarch64) - ARM processors (Apple Silicon, Raspberry Pi, etc.)

## Requirements

- Docker
- Docker BuildX (for multi-platform builds)
- MareArts ANPR credentials

## Example API Calls

### V14 Models

```bash
# Korean plates
curl -X POST http://localhost:8000/process_image \
  -H "X-API-Key: your_secret_api_key" \
  -u "username:serial_key" \
  -F "detection_model_version=v14_medium_640p_fp32" \
  -F "ocr_model_version=v14_medium_fp32" \
  -F "region=kr" \
  -F "signature=your_signature" \
  -F "backend=cuda" \
  -F "image=@test_image.jpg"

# European+ plates
curl -X POST http://localhost:8000/process_image \
  -H "X-API-Key: your_secret_api_key" \
  -u "username:serial_key" \
  -F "detection_model_version=v14_medium_640p_fp32" \
  -F "ocr_model_version=v14_medium_fp32" \
  -F "region=eup" \
  -F "signature=your_signature" \
  -F "backend=cuda" \
  -F "image=@test_image.jpg"

# Universal (all regions) - default if region not specified
curl -X POST http://localhost:8000/process_image \
  -H "X-API-Key: your_secret_api_key" \
  -u "username:serial_key" \
  -F "detection_model_version=v14_medium_640p_fp32" \
  -F "ocr_model_version=v14_medium_fp32" \
  -F "signature=your_signature" \
  -F "backend=cpu" \
  -F "image=@test_image.jpg"
```

## Response Format

```json
{
  "results": [
    {
      "ocr": "ABC123",
      "ocr_conf": 99,
      "ltrb": [100, 200, 300, 250],
      "ltrb_conf": 95
    }
  ],
  "ltrb_proc_sec": 0.15,
  "ocr_proc_sec": 0.08
}
```

## Notes

- Container runs on port 8000 by default
- Supports both AMD64 (x86_64) and ARM64 (aarch64) architectures
- **Smart model caching** - API reuses initialized models when same model requested (>3.6.5)
- **Dynamic region switching** - Region changes without reloading OCR model (>3.6.5)
- Models are downloaded on first use and cached
- Credentials passed via Basic Auth for security
- Requires license with signature
- Region parameter optional (default: univ)

### Performance Optimization

The API automatically optimizes model usage:
- **Same model requests** → Reuses existing instance (no reload)
- **Region changes only** → Uses `set_region()` for instant switching
- **Model changes** → Only reloads the changed model (detector or OCR)


## Supported Modes

### V14 Detector
  - Model: {size}_{res}_{prec} (e.g., micro_320p_fp32, medium_640p_fp32)
    - size: pico, micro, small, medium, large
    - res: 320p (fast), 640p (accurate)
    - prec: fp32 (fast), fp16 (compact)
  - backend: "cpu", "cuda", "directml" (default: cpu)

### OCR (V15 Latest / V14 Backward Compatible)
  - Model: pico_fp32, micro_fp32, small_fp32, medium_fp32, large_fp32
           pico_int8, micro_int8, small_int8, medium_int8, large_int8 (V15 only)
  - Version: "v15" (latest, default) or "v14" (backward compatible)
  - Region: "kor"/"kr", "euplus"/"eup", "na", "china"/"cn", "univ" (default: univ)
  - backend: "cpu", "cuda", "directml" (default: cpu)

**Example:** Consecutive requests with `medium_fp32` OCR and v15 but different regions (kor → euplus → na) will reuse the same OCR instance and only switch regions internally.

## Regions

- **kor** (or kr) - Korean license plates
- **euplus** (or eup) - European+ license plates (EU + additional countries)
- **na** - North American license plates (USA, Canada)
- **china** (or cn) - Chinese license plates
- **univ** - Universal (all regions) - default, but choose specific region for best accuracy
