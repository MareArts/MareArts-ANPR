# Model Versions & Performance

## Detector Models

Detection models locate license plates in images.

### Performance Metrics

| Model | Size | Precision | Recall | F1 Score | Speed (ms) | Recommendation |
|-------|------|-----------|---------|----------|------------|----------------|
| **v13_nano** | 14MB | 0.9657 | 0.9826 | 0.9676 | 36 | ⚡ Fastest |
| **v13_small** | 49MB | 0.9632 | 0.9920 | 0.9715 | 66 | |
| **v13_middle** | 103MB | 0.9634 | 0.9940 | 0.9725 | 163 | 🎯 Best Balance |
| **v13_large** | 129MB | 0.9642 | 0.9936 | 0.9729 | 205 | 📈 Best Recall |
| v11_small | 38MB | 0.9791 | 0.9849 | 0.9779 | 49 | |
| v11_middle | 79MB | 0.9799 | 0.9866 | 0.9793 | 94 | |
| v11_large | 125MB | 0.9824 | 0.9892 | 0.9823 | 156 | 🥇 Best F1 |
| v10_small | 38MB | 0.9852 | 0.9694 | 0.9716 | 47 | |
| v10_middle | 79MB | 0.9836 | 0.9680 | 0.9701 | 99 | |
| v10_large | 125MB | 0.9858 | 0.9709 | 0.9731 | 231 | 🎯 Best Precision |

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

### Standard Configuration

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
# For faster processing
detector = ma_anpr_detector("v13_nano", user_name, serial_key)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)
```

### Higher Accuracy Configuration

```python
# For higher accuracy
detector = ma_anpr_detector("v11_large", user_name, serial_key)
ocr = ma_anpr_ocr("v13_univ", user_name, serial_key)
```

## Performance Notes

- Speed measurements based on i7-9800X 3.8GHz CPU
- GPU acceleration can provide faster processing
- First inference includes model loading time
- Subsequent inferences are faster due to caching
- Batch processing can improve throughput

