# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MareArts ANPR is a commercial AI-powered Automatic Number Plate Recognition SDK supporting multiple regions (EU, Korea, China, Universal). The system uses a two-stage pipeline: YOLO-based detection models for license plate localization, followed by region-specific OCR models for character recognition.

## Key Commands

### Docker API Deployment
```bash
# Build multi-platform Docker image
cd API_docker_example && ./build_image.sh

# Run the container
./run_container.sh

# Test API endpoint
./api_call.sh
```

### SDK Installation
```bash
# Standard installation
pip install marearts-anpr

# For GPU acceleration
pip uninstall onnxruntime && pip install onnxruntime-gpu
```

## Architecture

The codebase follows a three-tier structure:

1. **Core SDK**: `marearts-anpr` package providing detection and OCR functionality
2. **Usage Examples**: `example_code/` with basic, advanced, and background subtraction patterns
3. **Production API**: `API_docker_example/` with FastAPI wrapper for deployment

### Two-Stage Processing Pipeline
- **Detection**: YOLO models (v10/v11/v13 variants) locate license plates in images
- **OCR**: Region-specific models extract text from detected plates

### Model Variants
- **Detectors**: nano/small/middle/large sizes for speed vs accuracy tradeoffs
- **OCR Models**: EU, Korea, China, Universal with different generation versions

## Key Integration Patterns

### High-Level API (basic.py)
Single function calls process entire pipeline:
```python
results = marearts_anpr_from_image_file(user_name, serial_key, image_path, region)
```

### Low-Level API (advanced.py)
Separate detector and OCR initialization for performance optimization:
```python
detector = ma_anpr_detector(user_name, serial_key, detector_model)
ocr_engine = ma_anpr_ocr(user_name, serial_key, ocr_model)
```

### Production API (app.py)
FastAPI service with HTTP Basic Auth + API Key authentication, supporting file upload and base64 image processing.

## Authentication

All operations require valid `user_name` and `serial_key` from MareArts licensing. Models are automatically downloaded and cached on first use.

## Output Format

Results include detected text, confidence scores, bounding boxes, and processing times for both detection and OCR stages.