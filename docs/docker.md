# Docker Deployment

Deploy MareArts ANPR as a REST API service using Docker.

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
- `detection_model_version`: Detection model (e.g., "v13_middle", "v14_small_640p_fp16" for V2 Current license)
- `ocr_model_version`: OCR model (e.g., "v13_euplus")
- `signature`: (Optional) Signature for V14 models (provided with V2 Current license)
- `backend`: (Optional) Backend for V14 models: "cpu", "cuda", "directml", "tensorrt" (default: "cuda")
- `image`: Image file (JPEG/PNG)

Headers:
- `X-API-Key`: your_secret_api_key
- `Authorization`: Basic Auth with credentials (V1 Legacy or V2 Current serial key)

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

Based on Python 3.11 slim image with:
- FastAPI web framework
- OpenCV for image processing
- MareArts ANPR SDK

## Requirements

- Docker
- Docker BuildX (for multi-platform builds)
- MareArts ANPR credentials

## Example API Calls

### V1 (Legacy) License
```bash
curl -X POST http://localhost:8000/process_image \
  -H "X-API-Key: your_secret_api_key" \
  -u "username:v1_serial_key" \
  -F "detection_model_version=v13_middle" \
  -F "ocr_model_version=v13_euplus" \
  -F "image=@test_image.jpg"
```

### V2 (Current) License with V14 Models
```bash
curl -X POST http://localhost:8000/process_image \
  -H "X-API-Key: your_secret_api_key" \
  -u "username:v2_serial_key" \
  -F "detection_model_version=v14_small_640p_fp16" \
  -F "ocr_model_version=v13_euplus" \
  -F "signature=your_signature" \
  -F "backend=cuda" \
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
- Supports AMD64 architecture (ARM64 commented out)
- Models are downloaded on first use
- Credentials passed via Basic Auth for security
- V14 models require V2 (Current) license with signature
- Auto-update feature checks for marearts-anpr updates on health checks
- Default backend for V14 is "cuda" in Docker deployment