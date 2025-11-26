# Model Versions & Performance

**Last Updated: November 7, 2025**

**Current Version: V14** - Latest generation with advanced architecture

This document covers the current V14 models. For legacy V13 and earlier models, see [Legacy Models Documentation](legacy-models.md).

## Model Storage

All V14 models are automatically downloaded to `~/.marearts/marearts_anpr_data/` on first use and cached for subsequent requests.

```
~/.marearts/marearts_anpr_data/
├── v14_small_640p_fp32.dat      # Detector model
├── v14_small_fp32.dat           # OCR model
├── v14_medium_640p_fp32.dat
├── v14_medium_fp32.dat
└── ... (other models as needed)
```

**Environment Variable**: Set `MAREARTS_ANPR_SKIP_UPDATE=1` to skip update checks and use cached models directly (faster initialization in production).

---

## Detector Models

Detection models locate license plates in images.

### V14 Models

The V14 series introduces advanced detection with digital signature authentication and multiple inference backends.

#### V14 Models - Performance Metrics

| Model Name | Size | Precision | Recall | F1 Score | FPS (CUDA) | Recommendation |
|------------|------|-----------|--------|----------|------------|----------------|
| pico_640p_fp32 | 100 MB | 0.8819 | 0.9854 | 0.9308 | 69 | 📱 Edge/Mobile |
| micro_640p_fp32 | 111 MB | 0.8840 | 0.9899 | 0.9339 | 70 | ⚡ Fastest |
| small_640p_fp32 | 153 MB | 0.8683 | 0.9915 | 0.9258 | 70 | 🎯 Balanced |
| medium_640p_fp32 | 180 MB | 0.8623 | 0.9921 | 0.9227 | 62 | - |
| large_640p_fp32 | 220 MB | 0.8902 | 0.9904 | 0.9377 | 57 | 🏆 Best accuracy |

**✅ Benchmarked with RTX CUDA GPU**

*Use these model names directly in `ma_anpr_detector_v14()` function*

📊 **[View Full Detector Benchmark Results](benchmarks/v14_detector_benchmark_20251104.txt)** *(Updated: Nov 4, 2025)*

---

## OCR Models

OCR models read text from detected license plates.

### V14 OCR Models

The V14 OCR series introduces advanced OCR architecture with batch processing support and regional vocabulary filtering.

**✅ Tested on real-world samples with RTX CUDA GPU**

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

# V14 detector with CUDA backend (recommended for NVIDIA GPUs)
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
#   model: pico_640p_fp32, micro_640p_fp32, small_640p_fp32, medium_640p_fp32, large_640p_fp32
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

- Benchmarked with RTX CUDA GPU
- CPU speeds typically 3-5x slower than GPU
- FP16 models optimize memory and speed on compatible hardware
- All V14 models require signature for authentication


