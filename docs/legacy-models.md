# Legacy Model Versions (V13 and Earlier)

**⚠️ DEPRECATED - PyPI Support Only **

This document contains information about legacy V13 and earlier models. These models are **no longer recommended** for new projects and are **only available through the PyPI package** for backward compatibility.

**For new projects, please use [V14 Models](models.md) instead.**

---

## Overview

Legacy models (V13, V11, V10) were the previous generation of MareArts ANPR models. While they remain functional through the PyPI package, they:

- ❌ Are not available in API/Live Test
- ❌ No longer receive updates or improvements
- ❌ Do not support the latest features
- ❌ Have lower accuracy compared to V14 models
- ✅ Remain available in PyPI for existing integrations

## Detector Models (Legacy)
* all tested by legacy dataset

### V13 Models (PyPI Only)

| Model Name | Size | Precision | Recall | F1 Score | Speed CUDA (ms) | Recommendation |
|-------|------|-----------|---------|----------|-----------------|----------------|
| **v13_nano** | 14MB | 0.9531 | 0.9653 | 0.9513 | 7.0 | ⚡ Fastest |
| **v13_small** | 49MB | 0.9565 | 0.9788 | 0.9608 | 7.4 | |
| **v13_middle** | 103MB | 0.9572 | 0.9801 | 0.9619 | 8.3 | 🎯 Best Balance |
| **v13_large** | 129MB | 0.9592 | 0.9808 | 0.9636 | 9.5 | 📈 Best v13 |

### V11 Models (PyPI Only)

| Model Name | Size | Precision | Recall | F1 Score | Speed CUDA (ms) |
|-------|------|-----------|---------|----------|-----------------|
| v11_small | 38MB | 0.9667 | 0.9620 | 0.9587 | 9.5 |
| v11_middle | 79MB | 0.9724 | 0.9701 | 0.9660 | 12.3 |
| v11_large | 125MB | 0.9740 | 0.9719 | 0.9680 | 14.8 |

### V10 Models (PyPI Only)

| Model Name | Size | Precision | Recall | F1 Score | Speed CUDA (ms) |
|-------|------|-----------|---------|----------|-----------------|
| v10_small | 38MB | 0.9754 | 0.9518 | 0.9566 | 9.4 |
| v10_middle | 79MB | 0.9719 | 0.9492 | 0.9537 | 12.2 |
| v10_large | 125MB | 0.9733 | 0.9512 | 0.9559 | 14.8 |

*Use these model names in `ma_anpr_detector()` function*

## OCR Models (Legacy)
* all tested by legacy dataset
### V13 OCR Models (PyPI Only)

| Model Name | Region | Size | Accuracy | Char Accuracy | Confidence | Speed (ms) | Status |
|-------|--------|------|----------|---------------|------------|------------|--------|
| **v13_euplus** | EU+ | 147MB | 0.9617 | 0.9901 | 97.70% | 82 | Recommended |
| **v13_kr** | Korea | 147MB | 0.9721 | 0.9951 | 97.01% | 86 | Recommended |
| **v13_cn** | China | 147MB | 0.9657 | 0.9932 | 97.76% | 86 | Recommended |
| **v13_univ** | Universal | 147MB | 0.9829 | 0.9963 | 98.61% | 85 | Good for mixed regions |
| v13_eu | EU | 295MB | 0.9504 | 0.9860 | 97.42% | 82 | |

### V11 OCR Models (PyPI Only)

| Model Name | Region | Size | Accuracy | Char Accuracy | Confidence | Speed (ms) |
|-------|--------|------|----------|---------------|------------|------------|
| v11_euplus | EU+ | 146MB | 0.9822 | 0.9965 | 97.64% | 82 |
| v11_kr | Korea | 146MB | 0.9938 | 0.9991 | 98.50% | 85 |
| v11_univ | Universal | 146MB | 0.9600 | 0.9941 | 97.77% | 85 |

*Use these model names in `ma_anpr_ocr()` function*

## Usage Examples (Legacy)

### V13 Configuration

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

### Fast Processing Configuration (Legacy)

```python
detector = ma_anpr_detector("v13_nano", user_name, serial_key, conf_thres=0.7, iou_thres=0.5)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)
```

### Higher Accuracy Configuration (Legacy)

```python
detector = ma_anpr_detector("v11_large", user_name, serial_key, conf_thres=0.7, iou_thres=0.5)
ocr = ma_anpr_ocr("v13_univ", user_name, serial_key)
```

## Migration Guide

### Why Migrate to V14?

1. **Better Accuracy**: V14 models have improved detection and OCR performance
2. **Modern Architecture**: Batch processing support for higher throughput
3. **Regional Vocabularies**: Optimized character filtering per region
4. **Active Support**: Only V14 receives updates and improvements
5. **API Support**: V14 is the only version supported in API/Docker deployments

### How to Migrate

**From V13 Detector:**
```python
# OLD (V13)
detector = ma_anpr_detector("v13_middle", user_name, serial_key)

# NEW (V14)
detector = ma_anpr_detector_v14(
    "small_640p_fp32", 
    user_name, 
    serial_key, 
    signature,
    backend="cuda"
)
```

**From V13 OCR:**
```python
# OLD (V13)
ocr = ma_anpr_ocr("v13_kr", user_name, serial_key)

# NEW (V14)
ocr = ma_anpr_ocr_v14(
    model='small_fp32',
    region='kr',  # kr, eup, na, cn, univ
    user_name=user_name,
    serial_key=serial_key,
    signature=signature
)
```

## Support Policy

- **V14 Models**: ✅ Full support, active development, API + PyPI
- **V13 Models**: ⚠️ Maintenance only, PyPI only (no API)
- **V11/V10 Models**: ⚠️ Deprecated, PyPI only (no updates)

## Notes

- V13 and earlier models work only with PyPI package installation
- No API or Docker support for legacy models
- All licenses can use legacy V13/V11/V10 models through PyPI
- V14 models recommended for new projects (better accuracy, active support)

---

**For current documentation, see [V14 Models](models.md)**
