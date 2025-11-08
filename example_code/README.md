# MareArts ANPR Example Code

This directory contains example code demonstrating how to use the MareArts ANPR V14 SDK.

## Quick Start

### V14 Models (Recommended)

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v14
from marearts_anpr import marearts_anpr_from_image_file

# Initialize with V2 credentials
user_name = "your_email"
serial_key = "your_serial_key"
signature = "your_signature"  # Provided with license

# Create V14 detector
detector = ma_anpr_detector_v14(
    "medium_640p_fp32",
    user_name,
    serial_key,
    signature,
    backend="cuda"  # cpu, cuda, directml
)

# Create V14 OCR with regional vocabulary
# Regions: kr, eup, na, cn, univ
ocr = ma_anpr_ocr_v14("medium_fp32", "eup", user_name, serial_key, signature)

# Process image
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
print(result)
```

> **Note**: For legacy V13 models, see [Legacy Models Documentation](../docs/legacy-models.md)

## Examples

### 1. basic.py ⭐ (Recommended Starting Point)

**V14 basic usage:**
- Simple initialization with V14 models
- Processing images from file, OpenCV, and PIL
- **Multi-region support using set_region()** (>3.7.0)
- **Batch processing** - Process multiple plates efficiently
- Memory-efficient region switching (saves ~180MB per region)

### 2. advanced.py (Manual Processing & Performance)

**V14 advanced usage:**
- Manual detection and OCR processing with V14 models
- Working with individual detections
- Performance timing measurements
- **Backend comparison** - Test cpu vs cuda performance
- Custom result formatting

### 3. bg_subtraction.py (Utility)

**Background subtraction for video processing:**
- Video processing
- Motion detection
- Processing only moving vehicles
- Can be combined with V14 ANPR

## Available Models & Configuration

For complete model specifications, performance benchmarks, and configuration options, see:

- **[V14 Models Documentation](../docs/models.md)** - All available models, performance, sizes, and recommendations
- **[Regional Support](../docs/regional-support.md)** - Regional vocabularies (kr, eup, na, cn, univ)
- **[Usage Guide](../docs/usage.md)** - Backend options (cpu, cuda, directml), dynamic region switching

## New Features (>3.7.0)

### Dynamic Region Switching

Use `set_region()` to switch regions without creating new OCR instances:

```python
# Initialize once
ocr = ma_anpr_ocr_v14("medium_fp32", "kr", user_name, serial_key, signature)

# Switch regions on demand
ocr.set_region('eup')  # Europe+
ocr.set_region('na')   # North America
ocr.set_region('cn')   # China

# Saves ~180 MB per region vs creating multiple instances!
```

## Setup

See **[Installation Guide](../docs/installation.md)** for credential configuration with `ma-anpr config`.

## Requirements

```bash
pip install marearts-anpr
pip install opencv-python  # For OpenCV examples
pip install pillow  # For PIL examples
```

## Model Storage

Models are automatically downloaded to `~/.marearts/marearts_anpr_data/` on first use and cached for subsequent runs.

## Notes

- V14 models require signature for authentication
- First run downloads models (may take time)
- Models are cached after first download
- GPU acceleration significantly improves performance
- Use specific regions for best accuracy (kr, eup, na, cn)
- For multi-region applications, use set_region() instead of creating multiple instances