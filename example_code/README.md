# MareArts ANPR Example Code

This directory contains example code demonstrating how to use the MareArts ANPR SDK (V14 detector + V14/V15 OCR).

**Quick comparison:**
- **V14 OCR:** Standard accuracy
- **V15 OCR:** ⭐ Improved accuracy, better multi-line support (recommended)

Test both: `quick_test_v14.py` and `quick_test_v15.py`

<br>


## Quick Start

### V14 Detector + V14 OCR

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
# Regions: univ (universal), kr, eup, na, cn
ocr = ma_anpr_ocr_v14("medium_fp32", "univ", user_name, serial_key, signature)

# Process image
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
print(result)
```

### V14 Detector + V15 OCR (Latest - Recommended)

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v15
from marearts_anpr import marearts_anpr_from_image_file

# V15 OCR: Improved accuracy, better multi-line support
# Use 'univ' for universal region (recommended)
ocr = ma_anpr_ocr_v15("medium_fp32", "univ", user_name, serial_key, signature)

# Use V14 detector with V15 OCR
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
```

> **Test both versions:** Use `quick_test_v14.py` and `quick_test_v15.py` to compare models

<br>



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
<br>


### 1. quick_test_v14.py / quick_test_v15.py ⚡ (Model Testing)

**Test V14 and V15 local models:**
- Tests 5 model pairs (pico, micro, small, medium, large) = **5 tests total**
- Uses universal region (works for all plate types)
- Shows actual OCR results with confidence scores
- Requires: License configured with `ma-anpr config`

```bash
# Test V14 detector + V14 OCR (5 tests)
python example_code/quick_test_v14.py

# Test V14 detector + V15 OCR (5 tests, latest)
python example_code/quick_test_v15.py
```

**When to use:** Quick test and compare V14 vs V15 OCR models!
<br>


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

**Basic usage with V14 models:**
- Simple initialization with V14 detector + V14 OCR
- Processing images from file, OpenCV, and PIL
- **Multi-region support using set_region()** (>3.6.5)
- **Batch processing** - Process multiple plates efficiently
- Memory-efficient region switching (saves ~180MB per region)

> **Tip:** Change `ma_anpr_ocr_v14` to `ma_anpr_ocr_v15` to use V15 OCR (improved accuracy)

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

---


## Integration & Troubleshooting



### 6. simple_server.py 🌐 (HTTP Server - Easiest Integration!)

**Minimal HTTP server - load models once, accept images from memory:**
- 3 input methods: file upload, raw bytes, base64
- No disk I/O - process from memory
- Perfect for Visual Studio / C# integration
- Server loads models ONCE (~22s), then fast processing (~0.03s per image)

**Step 1: Install requirements**
```bash
pip install fastapi uvicorn python-multipart
```

**Step 2: Start server** (one terminal, leave running)
```bash
python example_code/simple_server.py
# Models load once, then server waits for requests
```

**Step 3: Send images** (another terminal or from your app)

From command line:
```bash
curl -X POST http://localhost:8000/detect -F "image=@plate.jpg"
curl -X POST http://localhost:8000/detect/binary --data-binary "@plate.jpg"
```

From Python:
```bash
python example_code/test_server.py your_image.jpg
```

From Visual Studio C#:
```csharp
var client = new HttpClient();
var content = new ByteArrayContent(imageBytes);
await client.PostAsync("http://localhost:8000/detect/binary", content);
```



**Use case:** Easiest way to integrate with ANY software (C#, Visual Studio, web app)

**Note:** Server must be running before sending images!



### 7. memory_processing.py 💾 (Direct Integration)

**Process images from memory without server:**
- Process bytes, numpy arrays
- 40 lines - copy into your code
- Confidence threshold control

```bash
python example_code/memory_processing.py
```

**Use case:** Embed directly in your Python application

**Troubleshooting:**
- If "test-api works but local doesn't": Lower confidence to 0.15-0.20
- Check region: eup, kr, na, cn
- Run: `ma-anpr validate`



## Available Models & Configuration

For complete model specifications, performance benchmarks, and configuration options, see:

- **[V14 Models Documentation](../docs/models.md)** - All available models, performance, sizes, and recommendations
- **[Regional Support](../docs/regional-support.md)** - Regional vocabularies (kr, eup, na, cn, univ)
- **[Usage Guide](../docs/usage.md)** - Backend options (cpu, cuda, directml), dynamic region switching


## New Features

### V15 OCR (Latest)

New V15 OCR models with improved accuracy and multi-line support:

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v15

# Use V15 OCR for better accuracy
detector = ma_anpr_detector_v14("medium_640p_fp32", user_name, serial_key, signature)
ocr = ma_anpr_ocr_v15("medium_fp32", "univ", user_name, serial_key, signature)
```

Test and compare: `python quick_test_v14.py` vs `python quick_test_v15.py`

### Dynamic Region Switching (>3.7.0)

Use `set_region()` to switch regions without creating new OCR instances:

```python
# Works with both V14 and V15 OCR
ocr = ma_anpr_ocr_v15("medium_fp32", "univ", user_name, serial_key, signature)

# Switch regions on demand
ocr.set_region('univ')  # Universal (all regions)
ocr.set_region('eup')   # Europe+
ocr.set_region('na')    # North America
ocr.set_region('cn')    # China
ocr.set_region('kr')    # Korea

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
   python example_code/quick_test_v15.py  # Test V15 OCR (recommended)
   # or
   python example_code/quick_test_v14.py  # Test V14 OCR
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

- V14/V15 models require signature for authentication
- First run downloads models (may take time)
- Models are cached after first download
- GPU acceleration significantly improves performance
- Use specific regions for best accuracy (kr, eup, na, cn)
- For multi-region applications, use set_region() instead of creating multiple instances
- **V15 OCR recommended** for better accuracy and multi-line support