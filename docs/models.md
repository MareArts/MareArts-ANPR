# Model Versions & Performance

## Detector Models

Detection models locate license plates in images.

### V14 Models (V2 Current License Only)

The V14 series introduces advanced detection with digital signature authentication and multiple inference backends.

#### V14 Models - Performance Metrics
| Model Name | Size | Resolution | Precision | Recall | F1 Score | mAP | Speed CUDA | Speed CPU |
|-------|------|------------|-----------|---------|----------|------|------------|-----------|
| **v14_small_320p_fp32** | 135MB | 320p | 0.9593 | 0.9702 | 0.9562 | 0.9366 | 9.9ms (101 FPS) | 37ms (27 FPS) |
| **v14_small_320p_fp16** | 68MB | 320p | 0.9593 | 0.9702 | 0.9562 | 0.9366 | 15.9ms (63 FPS) | 64.7ms (15 FPS) |
| **v14_small_640p_fp32** | 136MB | 640p | 0.9497 | 0.9840 | 0.9580 | 0.9387 | 12.7ms (79 FPS) | 102.8ms (10 FPS) |
| **v14_small_640p_fp16** | 68MB | 640p | 0.9499 | 0.9840 | 0.9581 | 0.9389 | 22.3ms (45 FPS) | 182.2ms (5 FPS) |

#### TensorRT Optimized V14 Models (NVIDIA GPUs Only)
| Model Name | Size | Format | Resolution | Speed (ms) | F1 Score | mAP | Notes |
|-------|------|--------|------------|------------|----------|-----|---------|
| **v14_small_320p_trt_fp16** | 74MB | TRT FP16 | 320p | 7.9ms (127 FPS) | 0.9618 | 0.9437 | Fast inference |
| **v14_small_320p_trt_fp32** | 135MB | TRT FP32 | 320p | 8.8ms (114 FPS) | 0.9618 | 0.9437 | Standard precision |
| **v14_small_320p_trt_fp8** | 208MB | TRT FP8 | 320p | 8.7ms (115 FPS) | 0.9618 | 0.9437 | ⚡ Fastest |
| **v14_small_320p_trt_bf16** | 74MB | TRT BF16 | 320p | 8.6ms (116 FPS) | 0.9618 | 0.9437 | Brain float precision |
| **v14_small_640p_trt_fp16** | 76MB | TRT FP16 | 640p | 12.1ms (83 FPS) | 0.9607 | 0.9419 | 🎯 Recommended |
| **v14_small_640p_trt_fp32** | 163MB | TRT FP32 | 640p | 12.7ms (79 FPS) | 0.9607 | 0.9418 | Standard precision |
| **v14_small_640p_trt_fp8** | 163MB | TRT FP8 | 640p | 13.9ms (72 FPS) | 0.9607 | 0.9418 | RTX 40 only |
| **v14_small_640p_trt_bf16** | 154MB | TRT BF16 | 640p | 12.5ms (80 FPS) | 0.9615 | 0.9433 | Best accuracy |

*Note: V14 middle and large models coming soon!*

*Use these model names directly in `ma_anpr_detector_v14()` function*

### V13 & Legacy Models (V1 / V2 License)

| Model Name | Size | Precision | Recall | F1 Score | Speed CUDA (ms) | Recommendation |
|-------|------|-----------|---------|----------|-----------------|----------------|
| **v13_nano** | 14MB | 0.9531 | 0.9653 | 0.9513 | 7.0 | ⚡ Fastest |
| **v13_small** | 49MB | 0.9565 | 0.9788 | 0.9608 | 7.4 | |
| **v13_middle** | 103MB | 0.9572 | 0.9801 | 0.9619 | 8.3 | 🎯 Best Balance |
| **v13_large** | 129MB | 0.9592 | 0.9808 | 0.9636 | 9.5 | 📈 Best v13 |
| v11_small | 38MB | 0.9667 | 0.9620 | 0.9587 | 9.5 | |
| v11_middle | 79MB | 0.9724 | 0.9701 | 0.9660 | 12.3 | |
| v11_large | 125MB | 0.9740 | 0.9719 | 0.9680 | 14.8 | 🥇 Best v11 |
| v10_small | 38MB | 0.9754 | 0.9518 | 0.9566 | 9.4 | |
| v10_middle | 79MB | 0.9719 | 0.9492 | 0.9537 | 12.2 | |
| v10_large | 125MB | 0.9733 | 0.9512 | 0.9559 | 14.8 | Best Precision |

*Use these model names in `ma_anpr_detector()` function*

### Detector Selection Guide

**Recommended (V2 License with V14 models):**
- **Fast processing**: Use `v14_small_320p_trt_fp16` (7.9ms, 127 FPS)
- **Balanced**: Use `v14_small_640p_trt_fp16` (12.1ms, 83 FPS)
- **Best accuracy**: Use `v14_small_640p_trt_bf16` (12.5ms, 80 FPS)
- **CPU only**: Use `v14_small_320p_fp32` (37ms, 27 FPS)

**Legacy models (no longer updated):**
- Fast: `v13_nano` (36ms)
- Balanced: `v13_middle`
- Higher accuracy: `v13_large`

## OCR Models

OCR models read text from detected license plates.

### Regional Models

| Model Name | Region | Size | Accuracy | Char Accuracy | Confidence | Speed (ms) | Status |
|-------|--------|------|----------|---------------|------------|------------|--------|
| **v13_euplus** | EU+ | 147MB | 0.9617 | 0.9901 | 97.70% | 82 | Recommended |
| **v13_kr** | Korea | 147MB | 0.9721 | 0.9951 | 97.01% | 86 | Recommended |
| **v13_cn** | China | 147MB | 0.9657 | 0.9932 | 97.76% | 86 | Recommended |
| **v13_univ** | Universal | 147MB | 0.9829 | 0.9963 | 98.61% | 85 | Good for mixed regions |
| v13_eu | EU | 295MB | 0.9504 | 0.9860 | 97.42% | 82 | |
| v11_euplus | EU+ | 146MB | 0.9822 | 0.9965 | 97.64% | 82 | |
| v11_kr | Korea | 146MB | 0.9938 | 0.9991 | 98.50% | 85 | 📝 Best Korean |
| v11_univ | Universal | 146MB | 0.9600 | 0.9941 | 97.77% | 85 | |

*Use these model names in `ma_anpr_ocr()` function*

### OCR Selection Guide

#### By Region
- **European plates**: `v13_euplus` (includes EU + Indonesia)
- **Korean plates**: `v13_kr` or `v11_kr` (highest accuracy)
- **Chinese plates**: `v13_cn`
- **Mixed/Unknown**: `v13_univ` (best overall)

#### By Use Case
- **Single region**: Use region-specific v13 model
- **Multi-region**: Use `v13_univ`
- **Korean plates**: Consider `v11_kr` for higher accuracy
- **Speed**: All v13 models have similar speeds (~82-86ms)

## Usage Examples

### V14 Configuration (V2 Current License Only)

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr

# V14 detector with CUDA backend (recommended for NVIDIA GPUs)
detector = ma_anpr_detector_v14(
    "v14_small_640p_fp16",   # Model name
    user_name,                # Your username
    serial_key,               # V2 (Current) serial key
    signature,                # Provided with V2 license
    backend="cuda",           # Backend: cpu, cuda, directml, tensorrt
    conf_thres=0.25,          # Optional: Detection confidence threshold
    iou_thres=0.5             # Optional: IoU threshold for NMS
)

# TensorRT optimized for maximum speed (NVIDIA only)
detector_trt = ma_anpr_detector_v14(
    "v14_small_640p_trt_fp8",
    user_name,
    serial_key,
    signature,
    backend="tensorrt"
)

# CPU backend for cross-platform compatibility
detector_cpu = ma_anpr_detector_v14(
    "v14_small_320p_fp32",
    user_name,
    serial_key,
    signature,
    backend="cpu"
)

# OCR (same for V1 Legacy and V2 Current licenses)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)
```

### Standard Configuration (V1 Legacy / V2 Current License)

```python
from marearts_anpr import ma_anpr_detector, ma_anpr_ocr

# Balanced configuration
detector = ma_anpr_detector("v13_middle", user_name, serial_key, conf_thres=0.7, iou_thres=0.5)

# Region-specific OCR
ocr_eu = ma_anpr_ocr("v13_euplus", user_name, serial_key)  # For EU
ocr_kr = ma_anpr_ocr("v13_kr", user_name, serial_key)      # For Korea
ocr_cn = ma_anpr_ocr("v13_cn", user_name, serial_key)      # For China
ocr_univ = ma_anpr_ocr("v13_univ", user_name, serial_key)  # Universal
```

### Fast Processing Configuration

```python
# For V2 (Current) license holders - fastest with V14
detector = ma_anpr_detector_v14(
    "v14_small_320p_trt_fp8", user_name, serial_key, signature, backend="tensorrt"
)

# For V1 (Legacy) license holders
detector = ma_anpr_detector("v13_nano", user_name, serial_key, conf_thres=0.7, iou_thres=0.5)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)
```

### Higher Accuracy Configuration

```python
# For V2 (Current) license holders - best accuracy with V14
detector = ma_anpr_detector_v14(
    "v14_small_640p_fp32", user_name, serial_key, signature, backend="cuda"
)

# For V1 (Legacy) license holders
detector = ma_anpr_detector("v11_large", user_name, serial_key, conf_thres=0.7, iou_thres=0.5)
ocr = ma_anpr_ocr("v13_univ", user_name, serial_key)
```

## Performance Notes

### Performance Notes
- Benchmarked on RTX 4090 + Intel i7-9800X
- CPU speeds typically 3-5x slower than GPU
- TensorRT models require NVIDIA GPU

