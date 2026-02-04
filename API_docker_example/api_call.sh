#!/bin/bash

# Example API calls for MareArts ANPR Docker API
# V14 Detector + V15 OCR (latest)

echo "==================================="
echo "MareArts ANPR Docker API Test"
echo "==================================="

# Set common variables
API_KEY="your_secret_api_key"
IMAGE_PATH="../sample_images/eu-a.jpg"

# Example 1: V15 OCR - Korean plates (CPU)
echo "1. Testing V15 OCR - Korean plates (CPU)..."
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "user@email.com:serial_key" \
     -F "detection_model_version=medium_640p_fp32" \
     -F "ocr_model_version=medium_fp32" \
     -F "ocr_version=v15" \
     -F "region=kor" \
     -F "signature=your_signature" \
     -F "backend=cpu" \
     -F "image=@${IMAGE_PATH}"
echo -e "\n"

# Example 2: V15 OCR - European+ plates with CUDA
echo "2. Testing V15 OCR - European+ plates (CUDA)..."
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "user@email.com:serial_key" \
     -F "detection_model_version=medium_640p_fp32" \
     -F "ocr_model_version=medium_fp32" \
     -F "ocr_version=v15" \
     -F "region=euplus" \
     -F "signature=your_signature" \
     -F "backend=cuda" \
     -F "image=@${IMAGE_PATH}"
echo -e "\n"

# Example 3: V15 OCR - Universal (all regions)
echo "3. Testing V15 OCR - Universal (CPU)..."
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "user@email.com:serial_key" \
     -F "detection_model_version=small_640p_fp32" \
     -F "ocr_model_version=small_fp32" \
     -F "ocr_version=v15" \
     -F "region=univ" \
     -F "signature=your_signature" \
     -F "backend=cpu" \
     -F "image=@${IMAGE_PATH}"
echo -e "\n"

# Example 4: V14 OCR - Backward compatible
echo "4. Testing V14 OCR - Backward compatible (CPU)..."
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "user@email.com:serial_key" \
     -F "detection_model_version=small_640p_fp32" \
     -F "ocr_model_version=small_fp32" \
     -F "ocr_version=v14" \
     -F "region=univ" \
     -F "signature=your_signature" \
     -F "backend=cpu" \
     -F "image=@${IMAGE_PATH}"
echo -e "\n"

echo "==================================="
echo "Tests complete!"