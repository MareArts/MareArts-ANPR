# Usage Examples

## Python SDK Usage

### Basic Usage

```python
from marearts_anpr import marearts_anpr_from_image_file
from marearts_anpr import ma_anpr_detector, ma_anpr_ocr

# Initialize with credentials
user_name = "your_email"
serial_key = "your_serial_key"

# Or load from environment variables
import os
user_name = os.getenv("MAREARTS_ANPR_USERNAME", "")
serial_key = os.getenv("MAREARTS_ANPR_SERIAL_KEY", "")

# Create detector and OCR instances
detector = ma_anpr_detector("v13_middle", user_name, serial_key)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)

# Process image file
result = marearts_anpr_from_image_file(detector, ocr, "path/to/image.jpg")
print(result)
```

### Multiple Input Formats

```python
import cv2
from PIL import Image
from marearts_anpr import marearts_anpr_from_cv2, marearts_anpr_from_pil

# From OpenCV image
img_cv2 = cv2.imread("image.jpg")
result = marearts_anpr_from_cv2(detector, ocr, img_cv2)

# From PIL image
img_pil = Image.open("image.jpg")
result = marearts_anpr_from_pil(detector, ocr, img_pil)

# From file path
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
```

### Advanced Usage - Separate Detection and OCR

```python
from marearts_anpr import ma_anpr_detector, ma_anpr_ocr
import cv2

# Initialize
detector = ma_anpr_detector("v13_middle", user_name, serial_key, 
                           conf_thres=0.3, iou_thres=0.5)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)

# Load image
image = cv2.imread("test.jpg")

# Step 1: Detect license plates
plates = detector.predict(image)
print(f"Found {len(plates)} license plates")

# Step 2: Process each detected plate
for plate in plates:
    x1, y1, x2, y2, conf = plate
    
    # Crop license plate region
    plate_img = image[int(y1):int(y2), int(x1):int(x2)]
    
    # Run OCR on cropped plate
    text, confidence = ocr.predict(plate_img)
    
    print(f"Plate: {text} (confidence: {confidence}%)")
    print(f"Location: [{x1}, {y1}, {x2}, {y2}]")
    print(f"Detection confidence: {conf}%")
```

### Batch Processing

```python
import glob
from marearts_anpr import marearts_anpr_from_image_file

# Process multiple images
image_files = glob.glob("images/*.jpg")

results = []
for image_path in image_files:
    result = marearts_anpr_from_image_file(detector, ocr, image_path)
    results.append({
        'file': image_path,
        'plates': result['results'],
        'processing_time': result['ltrb_proc_sec'] + result['ocr_proc_sec']
    })

# Print summary
for r in results:
    print(f"{r['file']}: {len(r['plates'])} plates found in {r['processing_time']:.3f}s")
```

### Multi-Region Support

```python
# Initialize OCR models for different regions
ocr_models = {
    'eu': ma_anpr_ocr("v13_euplus", user_name, serial_key),
    'kr': ma_anpr_ocr("v13_kr", user_name, serial_key),
    'cn': ma_anpr_ocr("v13_cn", user_name, serial_key),
    'universal': ma_anpr_ocr("v13_univ", user_name, serial_key)
}

# Use appropriate model based on region
def process_image(image_path, region='universal'):
    ocr = ocr_models.get(region, ocr_models['universal'])
    return marearts_anpr_from_image_file(detector, ocr, image_path)

# Examples
eu_result = process_image("eu_plate.jpg", region='eu')
kr_result = process_image("kr_plate.jpg", region='kr')
cn_result = process_image("cn_plate.jpg", region='cn')
```

## CLI Usage

### Basic Commands

```bash
# Process single image
ma-anpr image.jpg

# Process multiple images
ma-anpr *.jpg

# Specify models
ma-anpr image.jpg --detector v13_small --ocr v13_kr

# Save results to JSON
ma-anpr image.jpg --json results.json

# Verbose output
ma-anpr image.jpg --verbose
```

### Testing and Validation

```bash
# Test without credentials (1000 requests/day limit)
ma-anpr test-api image.jpg

# Validate license
ma-anpr validate

# Check GPU information
ma-anpr gpu-info

# List available models
ma-anpr models

# Show version
ma-anpr --version
```

### Advanced CLI Options

```bash
# Custom confidence thresholds
ma-anpr image.jpg --conf-thres 0.5 --iou-thres 0.4

# Process video file (saves frames with detections)
ma-anpr video.mp4 --output-dir ./output

# Benchmark performance
ma-anpr benchmark image.jpg --iterations 100
```

## Output Format

### Standard Output

```python
{
    'results': [
        {
            'ocr': 'ABC123',         # Recognized text
            'ocr_conf': 99,          # OCR confidence (0-100)
            'ltrb': [x1, y1, x2, y2], # Bounding box coordinates
            'ltrb_conf': 95          # Detection confidence (0-100)
        }
    ],
    'ltrb_proc_sec': 0.163,         # Detection time in seconds
    'ocr_proc_sec': 0.082           # OCR time in seconds
}
```

### Multiple Detections

```python
{
    'results': [
        {'ocr': '123가4568', 'ocr_conf': 99, 'ltrb': [181, 48, 789, 186], 'ltrb_conf': 83},
        {'ocr': '456나7890', 'ocr_conf': 97, 'ltrb': [154, 413, 774, 557], 'ltrb_conf': 82}
    ],
    'ltrb_proc_sec': 0.23,
    'ocr_proc_sec': 0.16
}
```

## Error Handling

```python
from marearts_anpr import marearts_anpr_from_image_file

try:
    result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
    
    if result['results']:
        for plate in result['results']:
            print(f"Found: {plate['ocr']}")
    else:
        print("No license plates detected")
        
except FileNotFoundError:
    print("Image file not found")
except Exception as e:
    print(f"Error processing image: {e}")
```

## Performance Tips

1. **Use GPU acceleration** when available
2. **Batch process** multiple images together
3. **Choose appropriate models** based on your needs:
   - `v13_nano` for speed
   - `v13_middle` for balance
   - `v13_large` for accuracy
4. **Reuse detector/OCR instances** instead of recreating them
5. **Adjust confidence thresholds** to reduce false positives