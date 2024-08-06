import requests
import json
from PIL import Image
import io

url = "http://localhost:8000/process_image"

headers = {
    "X-API-Key": "your_secret_api_key"
}

# Form data to be sent along with the file
data = {
    "user_name": "your_email",
    "serial_key": "your_secretkey",
    "detection_model_version": "middle",
    "ocr_model_version": "eu"
}

# Open the image using PIL
image_path = "../sample_images/eu-a.jpg"
# image_path = "../sample_images/none.png"
pil_image = Image.open(image_path)

# Convert the PIL image to a bytes object
image_bytes_io = io.BytesIO()
pil_image.save(image_bytes_io, format='PNG') #'PNG' 'JPEG'
image_bytes_io.seek(0)  # Move the pointer to the start of the BytesIO object

# Prepare files parameter with the image bytes
files = {
    "image": ("image.jpg", image_bytes_io, "image/jpeg")
}

#from file path
# files = {
#     "image": ("image.jpg", open("../sample_images/eu-a.jpg", "rb"), "image/jpeg")
# }

# Combine the data with the files to send in the same request
response = requests.post(url, headers=headers, data=data, files=files)

if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
