# Model Versions & Performance

## Detector Models

Detection models locate license plates in images.

### V14 Models (V2 License Required)

The V14 series introduces advanced detection with digital signature authentication and multiple inference backends.

#### V14 Models - Performance Metrics
| Model | Size | Resolution | Precision | Recall | F1 Score | mAP | Speed CUDA | Speed CPU |
|-------|------|------------|-----------|---------|----------|------|------------|-----------|
| **v14_small_320p_fp32** | 135MB | 320p | 0.9593 | 0.9702 | 0.9563 | 0.9367 | 15.9ms | 64.7ms |
| **v14_small_320p_fp16** | 68MB | 320p | 0.9593 | 0.9702 | 0.9563 | 0.9367 | 15.9ms | 64.7ms |
| **v14_small_640p_fp32** | 136MB | 640p | 0.9499 | 0.9840 | 0.9581 | 0.9389 | 22.3ms | 182.2ms |
| **v14_small_640p_fp16** | 68MB | 640p | 0.9499 | 0.9840 | 0.9581 | 0.9389 | 22.3ms | 182.2ms |

#### TensorRT Optimized V14 Models (NVIDIA GPUs Only)
| Model | Size | Format | Resolution | Speed (ms) | Notes |
|-------|------|--------|------------|------------|--------|
| **v14_small_320p_trt_fp16** | 74MB | TRT FP16 | 320p | ~20-30 | Fast inference |
| **v14_small_320p_trt_fp8** | 208MB | TRT FP8 | 320p | ~15-25 | ⚡ Fastest |
| **v14_small_640p_trt_fp16** | 76MB | TRT FP16 | 640p | ~40-60 | 🎯 Recommended |
| **v14_small_640p_trt_fp8** | 210MB | TRT FP8 | 640p | ~35-50 | Best speed |

*Note: V14 middle and large models coming soon!*

### V13 & Legacy Models (V1/V2 License)

| Model | Size | Precision | Recall | F1 Score | Speed CUDA (ms) | Recommendation |
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

### Detector Selection Guide

- **Fast processing**: Use `v13_nano` (36ms)
- **Balanced**: Use `v13_middle` (good balance)
- **Higher accuracy**: Use `v13_large` or `v11_large`
- **Limited resources**: Use `v13_nano` or `v13_small`

## OCR Models

OCR models read text from detected license plates.

### Regional Models

| Model | Region | Size | Accuracy | Char Accuracy | Confidence | Speed (ms) | Status |
|-------|--------|------|----------|---------------|------------|------------|--------|
| **v13_euplus** | EU+ | 147MB | 0.9617 | 0.9901 | 97.70% | 82 | Recommended |
| **v13_kr** | Korea | 147MB | 0.9721 | 0.9951 | 97.01% | 86 | Recommended |
| **v13_cn** | China | 147MB | 0.9657 | 0.9932 | 97.76% | 86 | Recommended |
| **v13_univ** | Universal | 147MB | 0.9829 | 0.9963 | 98.61% | 85 | Good for mixed regions |
| v13_eu | EU | 295MB | 0.9504 | 0.9860 | 97.42% | 82 | |
| v11_euplus | EU+ | 146MB | 0.9822 | 0.9965 | 97.64% | 82 | |
| v11_kr | Korea | 146MB | 0.9938 | 0.9991 | 98.50% | 85 | 📝 Best Korean |
| v11_univ | Universal | 146MB | 0.9600 | 0.9941 | 97.77% | 85 | |

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

### V14 Configuration (V2 License Required)

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr

# V14 detector with CUDA backend (recommended for NVIDIA GPUs)
detector = ma_anpr_detector_v14(
    "v14_small_640p_fp16",   # Model name
    user_name,                # Your username
    serial_key,               # V2 serial key (MAEV2:...)
    signature,                # 16-character hex signature
    backend="cuda"            # Backend: cpu, cuda, directml, tensorrt
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

# OCR (same for V1 and V2 licenses)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)
```

### Standard Configuration (V1/V2 License)

```python
from marearts_anpr import ma_anpr_detector, ma_anpr_ocr

# Balanced configuration
detector = ma_anpr_detector("v13_middle", user_name, serial_key)

# Region-specific OCR
ocr_eu = ma_anpr_ocr("v13_euplus", user_name, serial_key)  # For EU
ocr_kr = ma_anpr_ocr("v13_kr", user_name, serial_key)      # For Korea
ocr_cn = ma_anpr_ocr("v13_cn", user_name, serial_key)      # For China
ocr_univ = ma_anpr_ocr("v13_univ", user_name, serial_key)  # Universal
```

### Fast Processing Configuration

```python
# For V2 license holders - fastest with V14
detector = ma_anpr_detector_v14(
    "v14_small_320p_trt_fp8", user_name, serial_key, signature, backend="tensorrt"
)

# For V1 license holders
detector = ma_anpr_detector("v13_nano", user_name, serial_key)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)
```

### Higher Accuracy Configuration

```python
# For V2 license holders - best accuracy with V14
detector = ma_anpr_detector_v14(
    "v14_small_640p_fp32", user_name, serial_key, signature, backend="cuda"
)

# For V1 license holders
detector = ma_anpr_detector("v11_large", user_name, serial_key)
ocr = ma_anpr_ocr("v13_univ", user_name, serial_key)
```

## Performance Notes

### Test System Specifications
- **CPU**: Intel Core i7-9800X @ 3.80GHz (8 cores, 16 threads)
- **GPU**: NVIDIA GeForce RTX 4090 (24GB VRAM)
- **CUDA**: Driver 535.261.03
- **OS**: Ubuntu Linux
- **RAM**: 64GB DDR4

### Measurement Details
- Speed measurements for V14 models tested on both NVIDIA GPU (CUDA) and Intel CPU
- Speed measurements for V13/legacy models tested on NVIDIA GPU (CUDA)
- CPU speeds typically 3-5x slower than CUDA for same model
- First inference includes model loading time
- Subsequent inferences are faster due to caching
- Batch processing can improve throughput
- TensorRT models require NVIDIA GPU with TensorRT installed

### Performance Expectations
- **RTX 4090**: Baseline performance as shown in tables
- **RTX 3090/3080**: ~20-30% slower than RTX 4090
- **RTX 2080/2070**: ~40-50% slower than RTX 4090
- **GTX 1080/1070**: ~60-70% slower than RTX 4090
- **CPU Only**: 3-5x slower than GPU, varies by CPU model

