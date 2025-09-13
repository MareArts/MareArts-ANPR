#!/bin/bash

# Example API calls for V1 (Legacy) and V2 (Current) licenses

echo "==================================="
echo "MareArts ANPR Docker API Test"
echo "==================================="

# Set common variables
API_KEY="your_secret_api_key"
IMAGE_PATH="../sample_images/eu-a.jpg"

# Example 1: V1 (Legacy) License
echo "1. Testing V1 (Legacy) License (V13 model)..."
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "user@email.com:your_v1_serial_key" \
     -F "detection_model_version=v13_middle" \
     -F "ocr_model_version=v13_euplus" \
     -F "image=@${IMAGE_PATH}"
echo -e "\n"

# Example 2: V2 (Current) License with V14 models
echo "2. Testing V2 (Current) License (V14 model with CUDA)..."
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "user@email.com:your_v2_serial_key" \
     -F "detection_model_version=v14_middle_640p_fp16" \
     -F "ocr_model_version=v13_euplus" \
     -F "signature=your_signature" \
     -F "backend=cuda" \
     -F "image=@${IMAGE_PATH}"
echo -e "\n"

# Example 3: V2 (Current) License with V14 TensorRT model
echo "3. Testing V2 (Current) License (V14 TensorRT)..."
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "user@email.com:your_v2_serial_key" \
     -F "detection_model_version=v14_small_320p_trt_fp8" \
     -F "ocr_model_version=v13_kr" \
     -F "signature=your_signature" \
     -F "backend=tensorrt" \
     -F "image=@${IMAGE_PATH}"
echo -e "\n"

echo "==================================="
echo "Tests complete!"