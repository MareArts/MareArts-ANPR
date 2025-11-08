#!/bin/bash

# Example API calls for V14 models

echo "==================================="
echo "MareArts ANPR Docker API Test"
echo "==================================="

# Set common variables
API_KEY="your_secret_api_key"
IMAGE_PATH="../sample_images/eu-a.jpg"

# Example 1: Korean plates (CPU)
echo "1. Testing V14 model - Korean plates (CPU)..."
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "user@email.com:serial_key" \
     -F "detection_model_version=v14_medium_640p_fp32" \
     -F "ocr_model_version=v14_medium_fp32" \
     -F "region=kr" \
     -F "signature=your_signature" \
     -F "backend=cpu" \
     -F "image=@${IMAGE_PATH}"
echo -e "\n"

# Example 2: European+ plates with CUDA
echo "2. Testing V14 model - European+ plates (CUDA)..."
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "user@email.com:serial_key" \
     -F "detection_model_version=v14_medium_640p_fp32" \
     -F "ocr_model_version=v14_medium_fp32" \
     -F "region=eup" \
     -F "signature=your_signature" \
     -F "backend=cuda" \
     -F "image=@${IMAGE_PATH}"
echo -e "\n"

# Example 3: Universal (all regions)
echo "3. Testing V14 model - Universal (CPU)..."
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "user@email.com:serial_key" \
     -F "detection_model_version=v14_small_640p_fp32" \
     -F "ocr_model_version=v14_small_fp32" \
     -F "region=univ" \
     -F "signature=your_signature" \
     -F "backend=cpu" \
     -F "image=@${IMAGE_PATH}"
echo -e "\n"

# Example 4: No region specified (defaults to univ)
echo "4. Testing V14 model - Default region (univ)..."
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "user@email.com:serial_key" \
     -F "detection_model_version=v14_small_640p_fp32" \
     -F "ocr_model_version=v14_small_fp32" \
     -F "signature=your_signature" \
     -F "backend=cpu" \
     -F "image=@${IMAGE_PATH}"
echo -e "\n"

echo "==================================="
echo "Tests complete!"