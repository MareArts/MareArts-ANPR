# MareArts ANPR Example Code

This directory contains example code demonstrating how to use the MareArts ANPR SDK.

## Examples

### 1. basic.py
Basic usage example showing:
- How to initialize detector and OCR
- Processing images from file, OpenCV, and PIL
- Multi-region support (EU and Korean plates)
- V1/V2 license compatible

### 2. advanced.py
Advanced usage example showing:
- Manual detection and OCR processing
- Working with individual detections
- Performance timing measurements
- Custom result formatting

### 3. v14_example.py (V2 Current License Required)
V14 models example showing:
- V14 detector initialization with signature
- Backend selection (CPU, CUDA, DirectML, TensorRT)
- Performance comparison between backends
- TensorRT optimized models usage

### 4. bg_subtraction.py
Background subtraction example for:
- Video processing
- Motion detection
- Processing only moving vehicles

## Quick Start

### V1 (Legacy) License

```python
from marearts_anpr import ma_anpr_detector, ma_anpr_ocr
from marearts_anpr import marearts_anpr_from_image_file

# Initialize
user_name = "your_email"
serial_key = "your_serial_key"

# Create detector and OCR
detector = ma_anpr_detector("v13_middle", user_name, serial_key, conf_thres=0.7, iou_thres=0.5)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)

# Process image
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
print(result)
```

### V2 (Current) License - V14 Models

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr
from marearts_anpr import marearts_anpr_from_image_file

# Initialize with V2 (Current) credentials - you receive all when you purchase
user_name = "your_email"
serial_key = "your_serial_key"
signature = "your_signature"

# Create V14 detector with backend selection
detector = ma_anpr_detector_v14(
    "v14_small_640p_fp16",
    user_name,
    serial_key,
    signature,
    backend="cuda",  # Options: cpu, cuda, directml, tensorrt
    conf_thres=0.25,  # Optional: Detection confidence threshold
    iou_thres=0.5     # Optional: IoU threshold for NMS
)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)

# Process image
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
print(result)
```

## Model Options

### Detector Models

**V14 Models (V2 Current License Only):**
- Standard: `v14_small_320p_fp32`, `v14_small_320p_fp16`, `v14_small_640p_fp32`, `v14_small_640p_fp16`
- TensorRT: `v14_small_320p_trt_fp8`, `v14_small_320p_trt_fp16`, `v14_small_640p_trt_fp8`, `v14_small_640p_trt_fp16`

**V13 Models (V1 Legacy / V2 Current License):**
- `v13_nano`, `v13_small`, `v13_middle`, `v13_large`

**Legacy Models:**
- `v10_small`, `v10_middle`, `v10_large`
- `v11_small`, `v11_middle`, `v11_large`

### OCR Models
- **V13**: `v13_eu`, `v13_euplus`, `v13_kr`, `v13_cn`, `v13_univ`
- **V11**: `v11_eu`, `v11_euplus`, `v11_kr`, `v11_cn`, `v11_univ`
- **Base**: `eu`, `euplus`, `kr`, `cn`, `univ`

## Backend Options (V14 Models with V2 Current License)

- **cpu**: Cross-platform CPU inference
- **cuda**: NVIDIA GPU acceleration
- **directml**: Windows GPU acceleration
- **tensorrt**: NVIDIA TensorRT optimization

## Environment Variables

Set credentials via environment variables:

```bash
export MAREARTS_ANPR_USERNAME="your-email@domain.com"
export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"
export MAREARTS_ANPR_SIGNATURE="your-signature"  # V2 (Current) license only
```

## Requirements

```bash
pip install marearts-anpr
pip install opencv-python  # For OpenCV examples
pip install pillow  # For PIL examples
```

## Notes

- V14 models require V2 (Current) license
- First run downloads models (may take time)
- Models are cached after first download
- TensorRT models require NVIDIA GPU with TensorRT