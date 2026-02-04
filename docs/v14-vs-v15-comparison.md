# V14 vs V15 OCR Comparison

**Last Updated: February 4, 2026**

This document compares V14 and V15 OCR models to help you choose the right version for your project.

---

## Quick Summary

| Feature | V14 OCR | V15 OCR |
|---------|---------|---------|
| **Status** | Stable, Backward Compatible | ⭐ Latest, Recommended |
| **Accuracy** | Excellent (91-92% average) | Better (94-95% average) |
| **Speed** | Fast (265-302 FPS) | Faster (278-335 FPS) |
| **Multi-line Plates** | Good | Improved |
| **INT8 Support** | ❌ No | ✅ Yes |
| **Recommendation** | Existing projects | 🎯 New projects |

**Bottom Line:** V15 is faster and more accurate. Use V15 for new projects.

---

## Performance Comparison

### Average Performance (All Regions)

| Model | V14 Accuracy | V15 Accuracy | Improvement | V14 FPS | V15 FPS | Speedup |
|-------|-------------|-------------|-------------|---------|---------|---------|
| pico_fp32 | 91.66% | 95.31% | **+3.65%** | 271.7 | 278.2 | 1.02× |
| micro_fp32 | 91.64% | 94.93% | **+3.29%** | 264.8 | 280.8 | 1.06× |
| small_fp32 | 91.36% | 94.17% | **+2.80%** | 301.8 | 334.6 | **1.11×** |
| medium_fp32 | 91.79% | 94.89% | **+3.09%** | 281.3 | 302.4 | 1.07× |
| large_fp32 | 92.30% | 95.26% | **+2.97%** | 264.2 | 291.7 | 1.10× |

**Key Findings:**
- ✅ V15 is 2-11% faster across all models
- ✅ V15 accuracy improved by 2.8-3.7%
- ✅ small_fp32 shows best speedup (11% faster)

### Visual Comparison

![Speed Comparison](comparison_graphs_50pct/speed_comparison.png)

*Speed comparison: V15 models are consistently faster across all sizes*

![Accuracy vs Speed](comparison_graphs_50pct/accuracy_vs_speed_scatter.png)

*Accuracy vs Speed trade-off: V15 achieves better accuracy at higher speeds*

---

## Regional Performance (small_fp32 Model)

| Region | V14 Accuracy | V15 FP32 | V15 INT8 | V14 FPS | V15 FPS | Speedup |
|--------|-------------|----------|----------|---------|---------|---------|
| China (china) | 96.40% | 95.90% | 96.02% | 298.8 | 332.5 | 1.11× |
| Europe+ (euplus) | 94.35% | 94.01% | 94.03% | 301.2 | 337.8 | 1.12× |
| Korea (kor) | 99.22% | 98.99% | 98.96% | 302.1 | 336.7 | 1.11× |
| North America (na) | 70.34% | **85.30%** | 85.30% | 309.2 | 341.6 | 1.10× |
| Universal (univ) | 96.51% | 96.63% | 96.63% | 297.6 | 324.6 | 1.09× |

**Notable Improvements:**
- 🎯 **North America (na)**: Massive improvement from 70% → 85% (+15%)
- ✅ Korean region: Still excellent (99%) with V15
- ✅ All regions faster with V15

### Regional Performance Visualization

![Accuracy by Region](comparison_graphs_50pct/accuracy_comparison_by_region.png)

*V14 vs V15 accuracy across all regions*

![All Regions Comparison](comparison_graphs_50pct/all_regions_detailed_comparison.png)

*Detailed comparison across all regions and models*

---

## V15 INT8 Models (New Feature)

V15 introduces INT8 quantized models:

**Benefits:**
- 📦 **70% smaller file size** (e.g., small: 114MB → ~28MB)
- 📱 **Lower memory usage** (better for mobile/edge)
- 🎯 **Similar accuracy** (<1% difference from FP32)
- ⚡ **50-55 FPS** (suitable for real-time on CPU)

**Performance (GPU CUDA):**

| Model | Exact Match | Char Accuracy | FPS | Time |
|-------|-------------|---------------|-----|------|
| pico_int8 | 91.72% | 96.74% | 55.3 | 18.15ms |
| micro_int8 | 94.80% | 98.08% | 38.3 | 26.13ms |
| small_int8 | 94.18% | 97.85% | 53.5 | 18.70ms |
| medium_int8 | 94.88% | 98.12% | 38.8 | 25.84ms |
| large_int8 | 95.33% | 98.35% | 31.9 | 31.28ms |

**Use Cases:**
- Mobile apps with limited storage
- Edge devices with memory constraints
- Applications prioritizing file size over speed
- CPU-only deployments

### FP32 vs INT8 Comparison

![FP32 vs INT8](comparison_graphs_50pct/fp32_vs_int8_comparison.png)

*V15 FP32 vs INT8 models: Similar accuracy, different performance characteristics*

---

## When to Use Each Version

### Use V15 OCR When:
- ✅ Starting a new project
- ✅ Need best accuracy
- ✅ Need faster inference
- ✅ Working with North American plates (major improvement)
- ✅ Need INT8 models for mobile/edge
- ✅ Want better multi-line plate handling

### Use V14 OCR When:
- ✅ Maintaining existing production systems
- ✅ Need proven stability
- ✅ Already optimized for V14
- ✅ No immediate need for performance improvements

---

## Migration Guide

### From V14 to V15 (Simple!)

**Change 1 line of code:**

```python
# Before (V14)
from marearts_anpr import ma_anpr_ocr_v14
ocr = ma_anpr_ocr_v14("small_fp32", "univ", user_name, serial_key, signature)

# After (V15)
from marearts_anpr import ma_anpr_ocr_v15
ocr = ma_anpr_ocr_v15("small_fp32", "univ", user_name, serial_key, signature)
```

**Or use unified interface:**

```python
from marearts_anpr import ma_anpr_ocr

# Just change version parameter
ocr = ma_anpr_ocr("small_fp32", "univ", user_name, serial_key, signature, version='v15')  # Was: version='v14'
```

**That's it!** Same API, same parameters, just better performance.

---

## Test V14 vs V15 Yourself

Run comparison tests on your own data:

```bash
# Test V14 OCR models
python example_code/quick_test_v14.py

# Test V15 OCR models
python example_code/quick_test_v15.py
```

Both scripts test 5 model sizes (pico → micro → small → medium → large) with your images.

---

## Regional Deep Dive

### Korea (kor) - Highest Accuracy
![Korea Comparison](comparison_graphs_50pct/kor_detailed_comparison.png)

### Europe+ (euplus)
![Europe+ Comparison](comparison_graphs_50pct/euplus_detailed_comparison.png)

### North America (na) - Biggest Improvement
![North America Comparison](comparison_graphs_50pct/na_detailed_comparison.png)

### China (china)
![China Comparison](comparison_graphs_50pct/china_detailed_comparison.png)

### Universal (univ)
![Universal Comparison](comparison_graphs_50pct/univ_detailed_comparison.png)

---

## Benchmarks

- 📊 [V14 OCR Full Report](benchmarks/v14_ocr_evaluation_report_cuda_50pct_20260204_101220.txt) - Feb 4, 2026
- 📊 [V15 OCR Full Report](benchmarks/v15_ocr_evaluation_report_cuda_50pct_20260203_192715.txt) - Feb 3, 2026
- 📈 [Comparison Summary](comparison_graphs_50pct/comparison_summary.txt)

---

## Conclusion

🏆 **V15 OCR is the clear winner:**

1. **2.8-3.7% better accuracy** across all models
2. **6-11% faster** inference speed
3. **Major improvement** in North America region (+15%)
4. **New INT8 models** for mobile/edge deployment
5. **Drop-in replacement** for V14 (no code changes needed)

**Recommendation:** Use V15 OCR for all new projects. Existing V14 deployments can migrate easily for immediate performance gains.

---

**Need help?** Contact [hello@marearts.com](mailto:hello@marearts.com)
