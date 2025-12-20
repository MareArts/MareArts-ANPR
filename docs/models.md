# Model Versions & Performance

**Last Updated: December 20, 2025**

**Current Version: V14** - Latest generation with advanced architecture

This document covers the current V14 models. For legacy V13 and earlier models, see [Legacy Models Documentation](legacy-models.md).

## Model Storage

All V14 models are automatically downloaded to `~/.marearts/marearts_anpr_data/` on first use and cached for subsequent requests.

```
~/.marearts/marearts_anpr_data/
├── marearts_anpr_d_v14_micro_320p_fp32.dat  # Detector model
├── marearts_anpr_d_v14_micro_320p_fp16.dat  # Detector model (FP16)
├── marearts_anpr_d_v14_micro_640p_fp32.dat  # Detector model (640p)
├── marearts_anpr_r_v14_large_fp32.dat       # OCR model
├── marearts_anpr_r_v14_large_fp32_config.dat # OCR config
└── ... (other models downloaded as needed)
```

**Environment Variable**: Set `MAREARTS_ANPR_SKIP_UPDATE=1` to skip update checks and use cached models directly (faster initialization in production).

---

## Detector Models

Detection models locate license plates in images.

### V14 Models

The V14 series introduces advanced detection with digital signature authentication and multiple inference backends.

**Available Resolutions:**
- **320p models** (320×320) - Faster speed, excellent detection (96-98%)
- **640p models** (640×640) - Highest detection rates (98-99%), larger input

**Available Precisions:**
- **FP32** - Fastest on GPU (2× faster than FP16), standard size
- **FP16** - 50% smaller file size, same detection rate, slower inference

#### V14 Models - Performance Comparison

![Detector Speed–Accuracy Trade-off](images/detector_performance_comparison.svg)

#### V14 Models - Performance Metrics

| Model Name | Detection Rate | Speed (GPU) | Size | Recommendation |
|------------|----------------|-------------|------|----------------|
| **micro_320p_fp32** | **97.13%** | **128 FPS** (7.8ms) | 83 MB | 🏆 Best overall |
| **micro_320p_fp16** | **97.13%** | **56 FPS** (17.9ms) | 42 MB | 🏆 Best mobile (50% smaller) |
| micro_640p_fp32 | 98.99% | 68 FPS (14.6ms) | 83 MB | Highest detection rate |
| small_320p_fp32 | 98.00% | 142 FPS (7.0ms) | 114 MB | ⚡ Fastest |
| medium_320p_fp32 | 98.06% | 136 FPS (7.4ms) | 153 MB | High detection |
| large_320p_fp32 | 98.40% | 131 FPS (7.6ms) | 164 MB | Strong performance |
| pico_320p_fp32 | 96.02% | 129 FPS (7.8ms) | 75 MB | 📱 Smallest + fast |
| pico_640p_fp32 | 98.54% | 66 FPS (15.2ms) | 75 MB | Balanced |
| small_640p_fp32 | 99.15% | 70 FPS (14.3ms) | 114 MB | High detection |
| medium_640p_fp32 | 99.21% | 66 FPS (15.1ms) | 153 MB | Very high detection |
| large_640p_fp32 | 99.31% | 60 FPS (16.7ms) | 164 MB | Highest detection |

**Key Findings:**
- **320p models**: 2× faster than 640p with excellent detection rates (96-98%)
- **640p models**: Highest detection rates (98-99%) for difficult cases
- **FP16 models**: 50% smaller size, same detection rate, ~50% slower
- **Best overall**: micro_320p_fp32 (97.13% detection, 128 FPS)
- **Best mobile**: micro_320p_fp16 (97.13% detection, 56 FPS, 42 MB)

*Use these model names directly in `ma_anpr_detector_v14()` function*

---

## OCR Models

OCR models read text from detected license plates.

### V14 OCR Models

The V14 OCR series introduces advanced OCR architecture with batch processing support and regional vocabulary filtering.

**✅ Tested on real-world samples with GPU acceleration**

📊 **[View Full OCR Benchmark Results](benchmarks/v14_ocr_benchmark_20251104.txt)** *(Updated: Nov 4, 2025)*

#### V14 OCR Models - Performance by Region

**Universal (univ) - Default, All Character Sets**

| Model | Exact Match | Char Accuracy | FPS | Size | Recommendation |
|-------|-------------|---------------|-----|------|----------------|
| pico_fp32 | 97.48% | 98.87% | 264 | 20 MB | 📱 Edge/Mobile |
| micro_fp32 | 97.54% | 98.86% | 260 | 71 MB | - |
| small_fp32 | 97.51% | 98.85% | 291 | 112 MB | 🎯 Balanced |
| medium_fp32 | 97.57% | 98.89% | 245 | 164 MB | - |
| large_fp32 | 97.75% | 98.91% | 253 | 179 MB | 🏆 Best accuracy |

**Korean (kr) - Best Overall Accuracy**

| Model | Exact Match | Char Accuracy | FPS | Size | Recommendation |
|-------|-------------|---------------|-----|------|----------------|
| pico_fp32 | 98.99% | 99.77% | 272 | 20 MB | 📱 Edge/Mobile |
| micro_fp32 | 99.21% | 99.80% | 250 | 71 MB | - |
| small_fp32 | 99.19% | 99.80% | 295 | 112 MB | 🎯 Balanced |
| medium_fp32 | 99.21% | 99.80% | 267 | 164 MB | - |
| large_fp32 | 99.27% | 99.82% | 265 | 179 MB | 🏆 Best accuracy |

**Europe+ (eup) - EU + Additional Countries**

| Model | Exact Match | Char Accuracy | FPS | Size | Recommendation |
|-------|-------------|---------------|-----|------|----------------|
| pico_fp32 | 94.98% | 97.39% | 280 | 20 MB | 📱 Edge/Mobile |
| micro_fp32 | 95.07% | 97.46% | 266 | 71 MB | - |
| small_fp32 | 94.98% | 97.43% | 304 | 112 MB | 🎯 Balanced |
| medium_fp32 | 95.03% | 97.46% | 278 | 164 MB | - |
| large_fp32 | 95.32% | 97.54% | 260 | 179 MB | 🏆 Best accuracy |

**North America (na)**

| Model | Exact Match | Char Accuracy | FPS | Size | Recommendation |
|-------|-------------|---------------|-----|------|----------------|
| pico_fp32 | 71.21% | 88.43% | 268 | 20 MB | 📱 Edge/Mobile |
| micro_fp32 | 71.21% | 87.67% | 269 | 71 MB | - |
| small_fp32 | 69.70% | 88.27% | 311 | 112 MB | 🎯 Balanced |
| medium_fp32 | 63.64% | 87.24% | 284 | 164 MB | - |
| large_fp32 | 69.70% | 86.25% | 271 | 179 MB | 🏆 Best accuracy |

**China (cn)**

| Model | Exact Match | Char Accuracy | FPS | Size | Recommendation |
|-------|-------------|---------------|-----|------|----------------|
| pico_fp32 | 96.24% | 98.82% | 268 | 20 MB | 📱 Edge/Mobile |
| micro_fp32 | 96.30% | 98.74% | 265 | 71 MB | - |
| small_fp32 | 96.36% | 98.88% | 301 | 112 MB | 🎯 Balanced |
| medium_fp32 | 96.36% | 98.89% | 276 | 164 MB | - |
| large_fp32 | 96.49% | 98.87% | 262 | 179 MB | 🏆 Best accuracy |

#### Model Averages (All Regions)
| Model | Exact Match | Char Accuracy | Avg FPS | Size |
|-------|-------------|---------------|---------|------|
| large_fp32 | 91.70% | 96.27% | 262 | 179 MB |
| small_fp32 | 91.54% | 96.64% | **300** | 112 MB |
| pico_fp32 | 91.78% | 96.65% | 270 | 20 MB |
| micro_fp32 | 91.86% | 96.50% | 262 | 71 MB |
| medium_fp32 | 90.36% | 96.45% | 270 | 164 MB |

#### V14 Regional Vocabularies

| Region | Code | Description | Characters |
|--------|------|-------------|------------|
| Universal | `univ` | All regions (default) | All character sets |
| Korea | `kr` | Korean plates | Hangul + Latin + Digits |
| Europe+ | `eup` | EU + additional countries | Latin + Cyrillic + Special |
| North America | `na` | USA/Canada | Latin + Digits |
| China | `cn` | Chinese plates | Chinese + Latin + Digits |

*Future: FP16 and INT8 variants coming soon*

*Use these region codes in `ma_anpr_ocr_v14()` function*

**Notes:**
- All V14 models support native batch processing
- Region parameter is optional (default: `univ`)
- **Recommendation**: Choose specific region for best accuracy, only use `univ` when region is unknown

---

## Usage Examples

### V14 Configuration

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v14

# V14 detector with CUDA backend (GPU acceleration)
detector = ma_anpr_detector_v14(
    "small_640p_fp32",   # Model name
    user_name,                # Your username
    serial_key,               # Serial key
    signature,                # Signature provided with license
    backend="cuda",           # Backend: cpu, cuda, directml
    conf_thres=0.25,          # Optional: Detection confidence threshold
    iou_thres=0.5             # Optional: IoU threshold for NMS
)

# V14 OCR with regional vocabulary
ocr = ma_anpr_ocr_v14(
    model='small_fp32',       # Model: pico/micro/small/medium/large_fp32
    region='kr',              # Region: kr/eup/na/cn/univ (default: univ)
    user_name=user_name,
    serial_key=serial_key,
    signature=signature
)

# Single image inference
text, confidence = ocr.predict(plate_image)
print(f"{text} ({confidence}%)")

# Batch processing (4 images)
results = ocr.predict([img1, img2, img3, img4])
for text, conf in results:
    print(f"{text}: {conf}%")

# For different regions, initialize ONE model for your target region:
# ocr = ma_anpr_ocr_v14('small_fp32', 'eup', user_name, serial_key, signature)   # Europe+
# ocr = ma_anpr_ocr_v14('small_fp32', 'kr', user_name, serial_key, signature)    # Korea
# ocr = ma_anpr_ocr_v14('small_fp32', 'na', user_name, serial_key, signature)    # North America
# ocr = ma_anpr_ocr_v14('small_fp32', 'cn', user_name, serial_key, signature)    # China

# NEW (>3.6.5): Dynamic region switching (saves memory)
# Supported detector modes:
#   model: {size}_{res}_{prec} (e.g., micro_320p_fp32, medium_640p_fp32)
#   size: pico, micro, small, medium, large | res: 320p, 640p | prec: fp32, fp16
#   backend: "cpu", "cuda", "directml", "auto" (default: cpu)
# Supported OCR modes:
#   model: pico_fp32, micro_fp32, small_fp32, medium_fp32, large_fp32
#   region: "kr", "eup", "na", "cn", "univ" (default: univ)
#   backend: "cpu", "cuda", "directml", "auto" (default: cpu)
ocr.set_region('eup')  # Switch to Europe+
ocr.set_region('kr')   # Switch to Korea
ocr.set_region('na')   # Switch to North America
# Use ONE instance instead of creating multiple - saves ~360 MB for 3 regions!
```

### Fast Processing Configuration

```python
# Fastest V14 detector
detector = ma_anpr_detector_v14(
    "pico_640p_fp32", user_name, serial_key, signature, backend="cuda"
)

# Fast OCR
ocr = ma_anpr_ocr_v14('pico_fp32', 'eup', user_name, serial_key, signature)
```

### Higher Accuracy Configuration

```python
# Best accuracy V14 detector
detector = ma_anpr_detector_v14(
    "large_640p_fp32", user_name, serial_key, signature, backend="cuda"
)

# Best accuracy OCR
ocr = ma_anpr_ocr_v14('large_fp32', 'kr', user_name, serial_key, signature)
```

---

**Looking for V13 or earlier models?** See [Legacy Models Documentation](legacy-models.md) (PyPI only, no API support).

---

## Performance Notes

- Benchmarked with GPU acceleration
- CPU speeds typically 3-5x slower than GPU
- FP16 models optimize memory and speed on compatible hardware
- All V14 models require signature for authentication


