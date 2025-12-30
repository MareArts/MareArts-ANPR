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
ocr = ma_anpr_ocr_v14("medium_fp32", "kr", user_name, serial_key, signature)

# Process image
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
print(result)
```

> **Note**: For legacy V13 models, see [Legacy Models Documentation](../docs/legacy-models.md)

## Testing & Verification (Start Here!)

### 0. verify_installation.py 🔍 (First Time Setup)

**Check if everything is installed correctly:**
- Verifies Python version compatibility
- Checks NumPy version (must be 1.x, not 2.x)
- Tests all dependencies
- Validates CLI commands
- Checks license configuration status

```bash
python example_code/verify_installation.py
```

**When to use:** Run this first to diagnose any installation issues!

### 1. quick_test.py ⚡ (Quick Validation)

**Complete installation and API test:**
- Tests package installation
- Tests CLI commands
- Tests free API (no license needed)
- Validates license (if configured)
- Guides next steps

```bash
python example_code/quick_test.py
```

**When to use:** Quick check that everything works!

### 2. test_api_regions.py 🌍 (Try Before You Buy)

**Test the free API with different regions:**
- No license required! (1000 requests/day)
- Test Korean, European, US, Chinese plates
- Examples for all regions
- Shows how regions affect accuracy

```bash
python example_code/test_api_regions.py your_image.jpg
```

**When to use:** Try MareArts ANPR before purchasing!

### 2b. test_api_examples.sh 📋 (Interactive Examples)

**Comprehensive test-api tutorial with 20+ examples:**
- All detector models (pico → large)
- All regions (kr, eup, na, cn, univ)
- Different resolutions (320p vs 640p)
- Precision options (FP16 vs FP32)
- Use case examples (security, parking, law enforcement)
- Interactive - press Enter between examples

```bash
./example_code/test_api_examples.sh your_image.jpg
```

**When to use:** Learn all available options interactively!

---

## Usage Examples

### 3. basic.py ⭐ (Recommended Starting Point)

**V14 basic usage:**
- Simple initialization with V14 models
- Processing images from file, OpenCV, and PIL
- **Multi-region support using set_region()** (>3.6.5)
- **Batch processing** - Process multiple plates efficiently
- Memory-efficient region switching (saves ~180MB per region)

**Requires:** License configured with `ma-anpr config`

```bash
python example_code/basic.py
```

### 4. advanced.py (Manual Processing & Performance)

**V14 advanced usage:**
- Manual detection and OCR processing with V14 models
- Working with individual detections
- Performance timing measurements
- **Backend comparison** - Test cpu vs cuda performance
- Custom result formatting

**Requires:** License configured

### 5. bg_subtraction.py (Utility)

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
ocr = ma_anpr_ocr_v14("medium_fp32", "eup", user_name, serial_key, signature)

# Switch regions on demand
ocr.set_region('eup')  # Europe+
ocr.set_region('na')   # North America
ocr.set_region('cn')   # China

# Saves ~180 MB per region vs creating multiple instances!
```

## Setup & Configuration

### First Time Users

1. **Install the package:**
   ```bash
   pip install marearts-anpr
   ```

2. **Verify installation:**
   ```bash
   python example_code/verify_installation.py
   ```

3. **If you have a license, configure credentials:**
   ```bash
   ma-anpr config
   ```
   
   You'll be prompted to enter:
   - Username/email
   - Serial key
   - Signature (for V2 licenses)

4. **Test it works:**
   ```bash
   python example_code/quick_test.py
   ```

### No License?

Use the **free test API** (1000 requests/day):

**Quick test:**
```bash
ma-anpr test-api your_image.jpg --region eup
```

**Interactive examples (20+ test cases):**
```bash
./example_code/test_api_examples.sh your_image.jpg
```

**Python script:**
```bash
python example_code/test_api_regions.py your_image.jpg
```

See **[Installation Guide](../docs/installation.md)** for more details.

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