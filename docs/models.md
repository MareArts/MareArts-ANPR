# Model Versions & Performance

**Last Updated: February 4, 2026**

**Current Version: V14 Detector + V15 OCR** - Latest generation with advanced architecture

This document covers V14 detector models and V14/V15 OCR models. For legacy V13 and earlier models, see [Legacy Models Documentation](legacy-models.md).

📊 **[V14 vs V15 OCR Comparison →](v14-vs-v15-comparison.md)** - Side-by-side comparison with benchmarks and migration guide

## Model Storage

All models are automatically downloaded to `~/.marearts/marearts_anpr_data/` on first use and cached for subsequent requests.

```
~/.marearts/marearts_anpr_data/
├── marearts_anpr_d_v14_micro_320p_fp32.dat  # V14 Detector model
├── marearts_anpr_d_v14_micro_320p_fp16.dat  # V14 Detector model (FP16)
├── marearts_anpr_d_v14_micro_640p_fp32.dat  # V14 Detector model (640p)
├── marearts_anpr_r_v14_large_fp32.dat       # V14 OCR model
├── marearts_anpr_r_v14_large_fp32_config.dat # V14 OCR config
├── marearts_anpr_r_v15_large_fp32.dat       # V15 OCR model
├── marearts_anpr_r_v15_large_fp32_config.dat # V15 OCR config
└── ... (other models downloaded as needed)
```

**Environment Variable**: Set `MAREARTS_ANPR_SKIP_UPDATE=1` to skip update checks and use cached models directly (faster initialization in production).

---

## Detector Models

Detection models locate license plates in images.

### V14 Detector Models

The V14 detector series introduces advanced detection with digital signature authentication and multiple inference backends.

**Available Resolutions:**
- **320p models** (320×320) - Faster speed, excellent detection (96-98%)
- **640p models** (640×640) - Highest detection rates (98-99%), larger input

**Available Precisions:**
- **FP32** - Fastest on GPU (2× faster than FP16), standard size
- **FP16** - 50% smaller file size, same detection rate, slower inference

#### V14 Detector Models - Performance Comparison

![Detector Speed–Accuracy Trade-off](images/detector_performance_comparison.svg)

#### V14 Detector Models - Performance Metrics

| Model Name | Detection Rate | Speed (GPU) | Size | Recommendation |
|------------|----------------|-------------|------|----------------|
| pico_320p_fp32 | 96.02% | 129 FPS (7.8ms) | 75 MB | 📱 Smallest + fast |
| pico_640p_fp32 | 98.54% | 66 FPS (15.2ms) | 75 MB | Balanced |
| **micro_320p_fp32** | **97.13%** | **128 FPS** (7.8ms) | 83 MB | 🏆 Best overall |
| **micro_320p_fp16** | **97.13%** | **56 FPS** (17.9ms) | 42 MB | 🏆 Best mobile (50% smaller) |
| micro_640p_fp32 | 98.99% | 68 FPS (14.6ms) | 83 MB | Highest detection rate |
| small_320p_fp32 | 98.00% | 142 FPS (7.0ms) | 114 MB | ⚡ Fastest |
| small_640p_fp32 | 99.15% | 70 FPS (14.3ms) | 114 MB | High detection |
| medium_320p_fp32 | 98.06% | 136 FPS (7.4ms) | 153 MB | High detection |
| medium_640p_fp32 | 99.21% | 66 FPS (15.1ms) | 153 MB | Very high detection |
| large_320p_fp32 | 98.40% | 131 FPS (7.6ms) | 164 MB | Strong performance |
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

### V15 OCR Models ⭐ (Recommended - Latest)

The V15 OCR series delivers improved accuracy and better multi-line plate handling with batch processing support and regional vocabulary filtering.

**Why choose V15?** 2.8-3.7% better accuracy, 6-11% faster inference. [See detailed comparison →](v14-vs-v15-comparison.md)

📊 [View V15 OCR Benchmarks](benchmarks/v15_ocr_evaluation_report_cuda_50pct_20260203_192715.txt) *(Feb 3, 2026)*

#### V15 OCR Models - Performance by Region (FP32)

**Universal (univ) - All Character Sets**

| Model | Exact Match | Char Accuracy | FPS (GPU) | Time | Recommendation |
|-------|-------------|---------------|-----------|------|----------------|
| pico_fp32 | 97.15% | 98.80% | 274.8 | 3.64ms | 📱 Smallest |
| micro_fp32 | 97.01% | 98.75% | 274.7 | 3.64ms | Fast |
| small_fp32 | 96.63% | 98.61% | 324.6 | 3.08ms | ⚡ Fastest |
| medium_fp32 | 97.00% | 98.73% | 293.6 | 3.41ms | Balanced |
| large_fp32 | 97.07% | 98.80% | 288.2 | 3.47ms | 🏆 Best accuracy |

**Korean (kor) - Best Overall Accuracy**

| Model | Exact Match | Char Accuracy | FPS (GPU) | Time | Recommendation |
|-------|-------------|---------------|-----------|------|----------------|
| pico_fp32 | 98.91% | 99.74% | 279.0 | 3.58ms | 📱 Smallest |
| micro_fp32 | 98.94% | 99.75% | 285.8 | 3.50ms | Fast |
| small_fp32 | 98.99% | 99.76% | 336.7 | 2.97ms | ⚡ Fastest |
| medium_fp32 | 98.95% | 99.75% | 303.3 | 3.30ms | Balanced |
| large_fp32 | 98.68% | 99.70% | 287.5 | 3.48ms | 🏆 Best accuracy |

**Europe+ (euplus) - EU + Additional Countries**

| Model | Exact Match | Char Accuracy | FPS (GPU) | Time | Recommendation |
|-------|-------------|---------------|-----------|------|----------------|
| pico_fp32 | 95.44% | 97.65% | 281.8 | 3.55ms | 📱 Smallest |
| micro_fp32 | 94.90% | 97.54% | 278.3 | 3.59ms | Fast |
| small_fp32 | 94.01% | 97.22% | 337.8 | 2.96ms | ⚡ Fastest |
| medium_fp32 | 94.90% | 97.49% | 306.9 | 3.26ms | Balanced |
| large_fp32 | 95.77% | 97.79% | 293.4 | 3.41ms | 🏆 Best accuracy |

**North America (na)**

| Model | Exact Match | Char Accuracy | FPS (GPU) | Time | Recommendation |
|-------|-------------|---------------|-----------|------|----------------|
| pico_fp32 | 88.54% | 96.11% | 271.1 | 3.69ms | 📱 Smallest |
| micro_fp32 | 87.58% | 95.72% | 285.4 | 3.50ms | Fast |
| small_fp32 | 85.30% | 94.90% | 341.6 | 2.93ms | ⚡ Fastest |
| medium_fp32 | 87.31% | 95.85% | 306.9 | 3.26ms | Balanced |
| large_fp32 | 88.36% | 96.42% | 296.9 | 3.37ms | 🏆 Best accuracy |

**China (china)**

| Model | Exact Match | Char Accuracy | FPS (GPU) | Time | Recommendation |
|-------|-------------|---------------|-----------|------|----------------|
| pico_fp32 | 96.52% | 98.93% | 284.3 | 3.52ms | 📱 Smallest |
| micro_fp32 | 96.23% | 98.86% | 280.0 | 3.57ms | Fast |
| small_fp32 | 95.90% | 98.78% | 332.5 | 3.01ms | ⚡ Fastest |
| medium_fp32 | 96.27% | 98.83% | 301.2 | 3.32ms | Balanced |
| large_fp32 | 96.44% | 98.92% | 292.4 | 3.42ms | 🏆 Best accuracy |

#### V15 Model Averages (All Regions)

**FP32 Models:**

| Model | Exact Match | Char Accuracy | Avg FPS | Avg Time | Size |
|-------|-------------|---------------|---------|----------|------|
| pico_fp32 | 95.31% | 98.24% | 278.2 | 3.59ms | 20 MB |
| micro_fp32 | 94.93% | 98.12% | 280.8 | 3.56ms | 71 MB |
| small_fp32 | 94.16% | 97.85% | **334.6** | 2.99ms | 112 MB |
| medium_fp32 | 94.88% | 98.13% | 302.3 | 3.31ms | 164 MB |
| large_fp32 | 95.26% | 98.32% | 291.6 | 3.43ms | 179 MB |

**INT8 Models:**

| Model | Exact Match | Char Accuracy | Avg FPS | Avg Time | Size |
|-------|-------------|---------------|---------|----------|------|
| pico_int8 | 91.72% | 96.74% | 55.3 | 18.15ms | ~15 MB |
| micro_int8 | 94.80% | 98.08% | 38.3 | 26.13ms | ~18 MB |
| small_int8 | 94.18% | 97.85% | 53.5 | 18.70ms | ~28 MB |
| medium_int8 | 94.88% | 98.12% | 38.8 | 25.84ms | ~41 MB |
| large_int8 | 95.33% | 98.35% | 31.9 | 31.28ms | ~45 MB |

**Note:** INT8 models are 75% smaller with similar accuracy. FP32 models are faster on GPU.

#### V15 Regional Vocabularies

| Region | Code | Short Code | Description | Characters |
|--------|------|------------|-------------|------------|
| Universal | `univ` | - | All regions | All character sets |
| Korea | `kor` | `kr` | Korean plates | Hangul + Latin + Digits |
| Europe+ | `euplus` | `eup` | EU + additional countries | Latin + Cyrillic + Special |
| North America | `na` | - | USA/Canada | Latin + Digits |
| China | `china` | `cn` | Chinese plates | Chinese + Latin + Digits |

*Use these region codes in `ma_anpr_ocr_v15()` function. Both full names and short codes are accepted (e.g., `kor` or `kr`)*

**Notes:**
- All V15 models support native batch processing
- FP32 and INT8 variants available
- Region parameter is optional (default: `univ`)
- **Recommendation**: Choose specific region for best accuracy, only use `univ` when region is unknown

---

### V14 OCR Models (Backward Compatible)

V14 OCR models remain fully supported for existing projects.

📊 [View V14 OCR Benchmarks](benchmarks/v14_ocr_evaluation_report_cuda_50pct_20260204_101220.txt) *(Feb 4, 2026)*

**Recommendation:** New projects should use V15 OCR for improved accuracy. [Compare V14 vs V15 →](v14-vs-v15-comparison.md)

---

## Usage Examples

### V15 OCR Configuration (Recommended)

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v15

# V14 detector with CUDA backend (GPU acceleration)
detector = ma_anpr_detector_v14(
    "small_640p_fp32",        # Model name
    user_name,                # Your username
    serial_key,               # Serial key
    signature,                # Signature provided with license
    backend="cuda",           # Backend: cpu, cuda, directml
    conf_thres=0.25,          # Optional: Detection confidence threshold
    iou_thres=0.5             # Optional: IoU threshold for NMS
)

# V15 OCR with regional vocabulary (Latest - Improved accuracy)
ocr = ma_anpr_ocr_v15(
    model='small_fp32',       # Model: pico/micro/small/medium/large_fp32 or _int8
    region='univ',            # Region: kor/euplus/na/china/univ (default: univ)
    user_name=user_name,
    serial_key=serial_key,
    signature=signature
)

# Or use V14 OCR (backward compatible)
# from marearts_anpr import ma_anpr_ocr_v14
# ocr = ma_anpr_ocr_v14('small_fp32', 'univ', user_name, serial_key, signature)

# Or use unified interface with version parameter
# from marearts_anpr import ma_anpr_ocr
# ocr = ma_anpr_ocr('small_fp32', 'univ', user_name, serial_key, signature, version='v15')  # v15 or v14


# Single image inference
text, confidence = ocr.predict(plate_image)
print(f"{text} ({confidence}%)")

# Batch processing (4 images)
results = ocr.predict([img1, img2, img3, img4])
for text, conf in results:
    print(f"{text}: {conf}%")

# Dynamic region switching (saves memory - works with V14 and V15)
ocr.set_region('euplus')  # Switch to Europe+
ocr.set_region('kor')     # Switch to Korea
ocr.set_region('na')      # Switch to North America
ocr.set_region('china')   # Switch to China
ocr.set_region('univ')    # Switch to Universal
# Use ONE instance instead of creating multiple - saves ~360 MB for 3 regions!
```

### Fast Processing Configuration

```python
# Fastest V14 detector
detector = ma_anpr_detector_v14(
    "small_320p_fp32", user_name, serial_key, signature, backend="cuda"
)

# Fastest V15 OCR
ocr = ma_anpr_ocr_v15('small_fp32', 'univ', user_name, serial_key, signature)
```

### Higher Accuracy Configuration

```python
# Best accuracy V14 detector
detector = ma_anpr_detector_v14(
    "large_640p_fp32", user_name, serial_key, signature, backend="cuda"
)

# Best accuracy V15 OCR
ocr = ma_anpr_ocr_v15('large_fp32', 'kor', user_name, serial_key, signature)
```

---

**Model Version Summary:**
- **V15 OCR**: Latest, recommended (improved accuracy, multi-line support)
- **V14 OCR**: Stable, backward compatible
- **V14 Detector**: Current detector version (works with both V14 and V15 OCR)
- **V13 and earlier**: See [Legacy Models Documentation](legacy-models.md)

---

## Performance Notes

- All benchmarks performed with GPU (CUDA) acceleration
- CPU speeds typically 3-5× slower than GPU
- FP32 models are faster on GPU than INT8
- INT8 models are 75% smaller files with similar accuracy
- FP16 detector models: 50% smaller size, same detection rate, ~50% slower
- All V14 and V15 models require V2 license with signature for authentication
- **V15 OCR recommended** for new projects (improved accuracy)


