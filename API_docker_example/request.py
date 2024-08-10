import requests
import json
from PIL import Image
import io
from requests.auth import HTTPBasicAuth

url = "http://localhost:8000/process_image"

# API Key in headers
headers = {
    "X-API-Key": "your_secret_api_key"
}

# Form data to be sent along with the file
data = {
    "detection_model_version": "middle",
    "ocr_model_version": "eu"
}

# HTTP Basic Authentication
#user_id and serial_key
auth_values = HTTPBasicAuth('user_id@abc.com', 'serial_key')

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