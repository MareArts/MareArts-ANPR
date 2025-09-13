import requests
import json
from PIL import Image
import io
from requests.auth import HTTPBasicAuth

# Example Python client for MareArts ANPR Docker API
# Supports both V1 and V2 licenses

url = "http://localhost:8000/process_image"

# API Key in headers
headers = {
    "X-API-Key": "your_secret_api_key"
}

# Example 1: V1 License configuration
def test_v1_license():
    print("Testing V1 License with V13 models...")
    
    data = {
        "detection_model_version": "v13_middle",
        "ocr_model_version": "v13_euplus"
    }
    
    auth_values = HTTPBasicAuth('user@email.com', 'your_v1_serial_key')
    return data, auth_values

# Example 2: V2 License configuration with V14 models
def test_v2_license():
    print("Testing V2 License with V14 models...")
    
    data = {
        "detection_model_version": "v14_middle_640p_fp16",
        "ocr_model_version": "v13_euplus",
        "signature": "your_16_char_hex",  # Required for V14
        "backend": "cuda"  # Options: cpu, cuda, directml, tensorrt
    }
    
    auth_values = HTTPBasicAuth('user@email.com', 'MAEV2:your_encrypted_key')
    return data, auth_values

# Choose which license to test
# data, auth_values = test_v1_license()
data, auth_values = test_v2_license()

# Open the image using PIL
image_path = "../sample_images/eu-a.jpg"
# image_path = "../sample_images/none.png"
pil_image = Image.open(image_path)

# Convert the PIL image to a bytes object
image_bytes_io = io.BytesIO()
pil_image.save(image_bytes_io, format='PNG')  # 'PNG' or 'JPEG'
image_bytes_io.seek(0)  # Move the pointer to the start of the BytesIO object

# Prepare files parameter with the image bytes
files = {
    "image": ("image.jpg", image_bytes_io, "image/jpeg")
}

# Alternative: Use file path directly
# files = {
#     "image": ("image.jpg", open("../sample_images/eu-a.jpg", "rb"), "image/jpeg")
# }

# Send the POST request
response = requests.post(url, headers=headers, data=data, files=files, auth=auth_values)

if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)