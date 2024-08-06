#!/bin/bash

# Set variables for API request
API_KEY="your_secret_api_key"
USER_NAME="your_email"
SERIAL_KEY="your_secretkey"
DETECTION_MODEL="middle"
OCR_MODEL="eu"
IMAGE_PATH="../sample_images/eu-a.jpg"  # Ensure this is the correct path to your image
IMAGE_PATH="../sample_images/none.png"  # Ensure this is the correct path to your image

# Send the POST request using curl
curl -X POST "http://localhost:8000/process_image" \
     -H "X-API-Key: ${API_KEY}" \
     -F "user_name=${USER_NAME}" \
     -F "serial_key=${SERIAL_KEY}" \
     -F "detection_model_version=${DETECTION_MODEL}" \
     -F "ocr_model_version=${OCR_MODEL}" \
     -F "image=@${IMAGE_PATH}"
