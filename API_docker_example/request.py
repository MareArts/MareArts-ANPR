import requests
import json
from PIL import Image
import io
from requests.auth import HTTPBasicAuth

# Example Python client for MareArts ANPR Docker API
# V14 Detector + V15 OCR (latest)

url = "http://localhost:8000/process_image"

# API Key in headers
headers = {
    "X-API-Key": "your_secret_api_key"
}

# V15 OCR configuration (Latest - Recommended)
def setup_request():
    print("Testing V14 Detector + V15 OCR...")
    
    data = {
        "detection_model_version": "medium_640p_fp32",  # V14 Detector model
        "ocr_model_version": "large_fp32",              # OCR model (works with v14 or v15)
        "ocr_version": "v15",                           # v15 (latest) or v14 (backward compatible)
        "region": "univ",                               # kor/kr, euplus/eup, na, china/cn, univ (default: univ)
        "signature": "your_signature",                  # Required
        "backend": "cuda"                               # Options: cpu, cuda, directml
    }
    
    auth_values = HTTPBasicAuth('user@email.com', 'serial_key')
    return data, auth_values

# Setup request data and authentication
data, auth_values = setup_request()

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