#!/bin/bash

# Set variables for API request
API_KEY="your_secret_api_key"
USER_NAME="user_id"
SERIAL_KEY="serial_key"
DETECTION_MODEL="middle"
OCR_MODEL="eu"
IMAGE_PATH="../sample_images/eu-a.jpg"
# IMAGE_PATH="../sample_images/none.png"


# Send the POST request using curl
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -u "${USER_NAME}:${ENCODED_SERIAL_KEY}" \
     -F "detection_model_version=${DETECTION_MODEL}" \
     -F "ocr_model_version=${OCR_MODEL}" \
     -F "image=@${IMAGE_PATH}"

echo # Add a newline for better readability of the output