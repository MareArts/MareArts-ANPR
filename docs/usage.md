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
# For V1 (Legacy) or V2 (Current) license:
detector = ma_anpr_detector("v13_middle", user_name, serial_key)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)

# For V2 (Current) license with V14 models:
# from marearts_anpr import ma_anpr_detector_v14
# detector = ma_anpr_detector_v14("v14_small_640p_fp16", user_name, serial_key, signature, backend="cuda")
# ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)

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

# Initialize detector with all parameters
detector = ma_anpr_detector(
    model_name="v13_middle",    # Required: Model name (v13_nano, v13_small, v13_middle, v13_large)
    user_name=user_name,        # Required: Your email
    serial_key=serial_key,       # Required: Your serial key
    conf_thres=0.25,           # Default: 0.25 (Detection confidence threshold)
    iou_thres=0.5              # Default: 0.5 (IoU threshold for NMS)
)

# Or with defaults (minimal parameters)
detector = ma_anpr_detector("v13_middle", user_name, serial_key)
# Uses conf_thres=0.25, iou_thres=0.5

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

### V14 Models Usage (V2 Current License Only)

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr
from marearts_anpr import marearts_anpr_from_image_file

# V2 (Current) license credentials - you receive all when you purchase
user_name = "your_email"
serial_key = "your_serial_key"
signature = "your_signature"  # Provided with V2 license

# Initialize V14 detector with all parameters
detector_v14 = ma_anpr_detector_v14(
    model_name="v14_small_640p_fp16",  # Required: V14 model name
    user_name=user_name,                # Required: Your email
    serial_key=serial_key,               # Required: Your V2 serial key
    signature=signature,                 # Required for V14: Your signature
    backend="auto",                     # Default: "auto" (Options: auto, cpu, cuda, directml, tensorrt)
    conf_thres=0.25,                    # Default: 0.25 (Detection confidence threshold)
    iou_thres=0.5                       # Default: 0.5 (IoU threshold for NMS)
)

# Or with defaults (minimal parameters)
detector_v14 = ma_anpr_detector_v14(
    "v14_small_640p_fp16",
    user_name,
    serial_key,
    signature
)  # Uses backend="auto", conf_thres=0.25, iou_thres=0.5

# OCR remains the same
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)

# Process image - detector method name is 'detector' not 'predict'
image = cv2.imread("test.jpg")
plates = detector_v14.detector(image)  # Note: method is 'detector'

# Or use the convenience function
result = marearts_anpr_from_image_file(detector_v14, ocr, "test.jpg")
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

# Specify models (V1/V2 with legacy models)
ma-anpr image.jpg --detector-model v13_small --ocr-model v13_kr

# V14 models (V2 Current license only)
ma-anpr image.jpg --detector-model v14_middle_640p_fp16 --backend cuda

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
3. **Choose appropriate models** based on your license and needs:
   - **V2 (Current) License holders**: Use V14 models for best performance
     - `v14_small_320p_trt_fp8` with TensorRT for maximum speed
     - `v14_middle_640p_fp16` with CUDA for balanced performance
     - `v14_large_640p_fp32` for maximum accuracy
   - **V1 License holders**: Use V13 models
     - `v13_nano` for speed
     - `v13_middle` for balance
     - `v13_large` for accuracy
4. **Reuse detector/OCR instances** instead of recreating them
5. **Adjust confidence thresholds** to reduce false positives
6. **For V14 models**, select appropriate backend:
   - `tensorrt`: Fastest on NVIDIA GPUs
   - `cuda`: Good performance on NVIDIA GPUs
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