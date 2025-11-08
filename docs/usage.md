# Usage Examples

## Python SDK Usage

### Basic Usage

```python
from marearts_anpr import marearts_anpr_from_image_file
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v14

# Initialize with credentials (V2 license required for V14)
user_name = "your_email"
serial_key = "your_serial_key"
signature = "your_signature"  # Required - provided with your V2 license

# Or load from environment variables
import os
user_name = os.getenv("MAREARTS_ANPR_USERNAME", "")
serial_key = os.getenv("MAREARTS_ANPR_SERIAL_KEY", "")
signature = os.getenv("MAREARTS_ANPR_SIGNATURE", "")

# Create V14 detector and OCR instances (V2 license required)
detector = ma_anpr_detector_v14("medium_640p_fp32", user_name, serial_key, signature, backend="cuda")
ocr = ma_anpr_ocr_v14("large_fp32", "univ", user_name, serial_key, signature)  # univ = universal (all regions)

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
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v14
import cv2

# Initialize V14 detector with all parameters
detector = ma_anpr_detector_v14(
    model_name="medium_640p_fp32",  # Required: V14 detector model
    user_name=user_name,            # Required: Your email
    serial_key=serial_key,          # Required: Your V2 serial key
    signature=signature,            # Required: Your signature
    backend="cuda",                 # Optional: "auto", "cpu", "cuda", "directml"
    conf_thres=0.25,                # Optional: Detection confidence threshold
    iou_thres=0.5                   # Optional: IoU threshold for NMS
)

# Or with minimal parameters
detector = ma_anpr_detector_v14("medium_640p_fp32", user_name, serial_key, signature)

# Initialize V14 OCR
ocr = ma_anpr_ocr_v14("large_fp32", "univ", user_name, serial_key, signature)

# Load image
image = cv2.imread("test.jpg")

# Step 1: Detect license plates
plates = detector.detector(image)  # Note: V14 uses 'detector' method
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

### V14 Models Configuration

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v14
from marearts_anpr import marearts_anpr_from_image_file

# V2 license credentials - you receive all when you purchase
user_name = "your_email"
serial_key = "your_serial_key"
signature = "your_signature"  # Required - provided with V2 license

# Initialize V14 detector with all parameters
detector_v14 = ma_anpr_detector_v14(
    model_name="small_640p_fp32",   # Required: V14 model name
    user_name=user_name,            # Required: Your email
    serial_key=serial_key,          # Required: Your V2 serial key
    signature=signature,            # Required: Your signature (mandatory for V14)
    backend="auto",                 # Optional: "auto" (Options: auto, cpu, cuda, directml)
    conf_thres=0.25,                # Optional: Detection confidence threshold
    iou_thres=0.5                   # Optional: IoU threshold for NMS
)

# Or with minimal parameters
detector_v14 = ma_anpr_detector_v14(
    "small_640p_fp32",
    user_name,
    serial_key,
    signature  # Required
)

# Initialize V14 OCR
ocr = ma_anpr_ocr_v14("large_fp32", "univ", user_name, serial_key, signature)  # signature required

# Process image - detector method name is 'detector' not 'predict'
image = cv2.imread("test.jpg")
plates = detector_v14.detector(image)  # Note: method is 'detector'

# Or use the convenience function
result = marearts_anpr_from_image_file(detector_v14, ocr, "test.jpg")
```

### Multi-Region Support

```python
# Option 1: Initialize with specific region
ocr = ma_anpr_ocr_v14("large_fp32", "kr", user_name, serial_key, signature)    # Korean
# ocr = ma_anpr_ocr_v14("large_fp32", "eup", user_name, serial_key, signature)   # Europe+
# ocr = ma_anpr_ocr_v14("large_fp32", "na", user_name, serial_key, signature)    # North America
# ocr = ma_anpr_ocr_v14("large_fp32", "cn", user_name, serial_key, signature)    # China

# Option 2: Universal region (handles all regions)
ocr = ma_anpr_ocr_v14("large_fp32", "univ", user_name, serial_key, signature)

# Process images
result = marearts_anpr_from_image_file(detector, ocr, "plate.jpg")
```

### Dynamic Region Switching (>3.7.0)

For applications processing plates from multiple regions, use `set_region()` to dynamically switch regions without creating multiple OCR instances. This **saves significant memory** (~180 MB per additional region).

```python
# Initialize ONE OCR instance
ocr = ma_anpr_ocr_v14("large_fp32", "kr", user_name, serial_key, signature)

# Process Korean plates
korean_result = marearts_anpr_from_image_file(detector, ocr, "korean_plate.jpg")

# Switch to Europe+ region
ocr.set_region('eup')
european_result = marearts_anpr_from_image_file(detector, ocr, "eu_plate.jpg")

# Switch to North America
ocr.set_region('na')
us_result = marearts_anpr_from_image_file(detector, ocr, "us_plate.jpg")

# Switch to China
ocr.set_region('cn')
china_result = marearts_anpr_from_image_file(detector, ocr, "china_plate.jpg")

# Switch to Universal (all regions)
ocr.set_region('univ')
```

**Benefits:**
- 💾 **Memory efficient**: Use 1 instance (~180 MB) instead of multiple instances
- ⚡ **No reinitialization**: Instant region switching
- 🎯 **Same accuracy**: Region-specific vocabulary filtering maintained

**When to use `set_region()` vs multiple instances:**
- ✅ Use `set_region()`: Processing different regions sequentially, memory-constrained environments
- ❌ Avoid `set_region()`: Multi-threaded concurrent processing (use separate instances per thread)

## CLI Usage

### Basic Commands

```bash
# Process single image
ma-anpr image.jpg

# Process multiple images
ma-anpr *.jpg

# Specify V14 models
ma-anpr image.jpg --detector-model medium_640p_fp32 --ocr-model large_fp32 --backend cuda

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

### Detector API Output

When using `detector.detector()` directly (advanced usage), it returns a list of detections:

```python
detections = detector.detector(image)
# Returns: List of detection dictionaries

# Each detection contains:
[
    {
        'bbox': [x1, y1, x2, y2],  # Bounding box coordinates (left, top, right, bottom)
        'score': 0.98,              # Detection confidence (0.0-1.0)
        'class': 'license_plate'    # Object class
    },
    # ... more detections
]
```

**Example usage:**
```python
import cv2
from PIL import Image

img = cv2.imread("image.jpg")
detections = detector.detector(img)

for det in detections:
    bbox = det['bbox']
    x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
    score = det['score']

    # Crop the plate region
    crop = img[int(y1):int(y2), int(x1):int(x2)]

    # Convert to PIL for OCR
    plate_img = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    text, conf = ocr.predict(plate_img)

    print(f"Plate: {text} (detection: {score*100:.1f}%, OCR: {conf}%)")
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
3. **Choose appropriate V14 models** based on your needs:
   - `pico_640p_fp32` - Fastest, smallest model
   - `micro_640p_fp32` - Fast with good accuracy
   - `small_640p_fp32` - Balanced performance
   - `medium_640p_fp32` - Higher accuracy
   - `large_640p_fp32` - Highest F1 score
4. **Reuse detector/OCR instances** instead of recreating them
5. **Adjust confidence thresholds** to reduce false positives
6. **Select appropriate backend**:
   - `cuda`: NVIDIA GPU acceleration (fastest)
   - `directml`: For Windows with various GPU types
   - `cpu`: Cross-platform compatibility

## Environment Variables

### Performance Optimization

```bash
# Skip model update checks for faster initialization (default: 0)
export MAREARTS_ANPR_SKIP_UPDATE=1

# Enable verbose logging for debugging (default: 0)
export MAREARTS_VERBOSE=1
```

**MAREARTS_ANPR_SKIP_UPDATE**: When set to `1`, skips server checks for model updates and uses cached files directly. This significantly reduces initialization time. Useful for production environments where models are stable. Default is `0` (checks for updates).

**MAREARTS_VERBOSE**: When set to `1`, enables detailed logging showing download progress, server checks, and timing information. Useful for debugging and monitoring. Default is `0` (minimal output).

Example usage:
```python
import os

# Configure before importing marearts_anpr
os.environ['MAREARTS_ANPR_SKIP_UPDATE'] = '1'  # Skip update checks
os.environ['MAREARTS_VERBOSE'] = '1'           # Enable verbose output

from marearts_anpr import ma_anpr_detector, ma_anpr_ocr
# Models will load faster without server checks
```