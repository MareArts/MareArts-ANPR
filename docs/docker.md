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
- `detection_model_version`: Detection model (e.g., "v13_middle")
- `ocr_model_version`: OCR model (e.g., "v13_euplus")
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

Based on Python 3.11 slim image with:
- FastAPI web framework
- OpenCV for image processing
- MareArts ANPR SDK

## Requirements

- Docker
- Docker BuildX (for multi-platform builds)
- MareArts ANPR credentials

## Example API Call

```bash
curl -X POST http://localhost:8000/process_image \
  -H "X-API-Key: your_secret_api_key" \
  -u "username:password" \
  -F "detection_model_version=v13_middle" \
  -F "ocr_model_version=v13_euplus" \
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