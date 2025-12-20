# MareArts ANPR SDK

[![PyPI version](https://badge.fury.io/py/marearts-anpr.svg)](https://badge.fury.io/py/marearts-anpr)
[![Python versions](https://img.shields.io/pypi/pyversions/marearts-anpr.svg)](https://pypi.org/project/marearts-anpr/)
[![Downloads](https://pepy.tech/badge/marearts-anpr)](https://pepy.tech/project/marearts-anpr)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](https://www.marearts.com/products/anpr)
[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen.svg)](http://live.marearts.com)

[![Python SDK](https://img.shields.io/github/v/release/MareArts/MareArts-ANPR?filter=marearts-anpr-python-sdk-*&label=Python%20SDK&color=blue)](https://pypi.org/project/marearts-anpr/)
[![iOS App](https://img.shields.io/github/v/release/MareArts/MareArts-ANPR?filter=marearts-anpr-mobile-app-ios-*&label=iOS%20App&color=green)](https://apps.apple.com/app/marearts-anpr/id6753904859)

<div align="center">

| ANPR Detection | Road Objects Detection | Mobile App |
|:---:|:---:|:---:|
| <img src="https://raw.githubusercontent.com/MareArts/MareArts-ANPR/main/promotion_image/anpr_result.png" alt="ANPR Results" width="280"/> | <img src="https://raw.githubusercontent.com/MareArts/MareArts-ANPR/main/promotion_image/robj_result.png" alt="Road Objects Results" width="280"/> | <img src="https://raw.githubusercontent.com/MareArts/MareArts-ANPR/main/mobile_app/scan_page.png" alt="Mobile App" width="280"/> |

</div>

Automatic Number Plate Recognition (ANPR) SDK for multiple regions with GPU acceleration support.

**💎 One License, All Access:** SDK + Mobile App + Road Objects Detection - Use everywhere with a single license.

---

## 🎉 New: MareArts ANPR Mobile App Released!

**📱 Now available on iOS! Android coming soon.**

Experience the power of MareArts ANPR directly on your mobile device! Fast, accurate, on-device license plate recognition for parking management, security, and vehicle tracking.

[![Download on App Store](https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg)](https://apps.apple.com/us/app/marearts-anpr/id6753904859)

✨ **Key Features:**
- 🚀 Fast on-device AI processing
- 🔒 100% offline - privacy first
- 📊 Statistics and analytics
- 🗺️ Map view with GPS tracking
- ✅ Whitelist/Blacklist management
- 🌍 Multi-region support

📖 **[Read the complete Mobile App Guide →](https://github.com/MareArts/MareArts-ANPR/blob/main/mobile_app/APP_GUIDE.md)**

> **🎁 Special Offer:** Use the mobile app as your ANPR license - no additional purchase required!  
> Get your license at [marearts.com/products/anpr](https://www.marearts.com/products/anpr)

---

<br>

## Features

- 🌍 **Multi-Region Support**: Korean, Europe+, North America, China, and Universal license plates
- 🔄 **Dynamic Region Switching**: Change regions instantly with `set_region()` without model reload
- ⚡ **GPU Acceleration**: CUDA, DirectML support for real-time processing
- 🎯 **High Accuracy**: Advanced models with regional vocabulary optimization
- 📦 **Batch Processing**: Process multiple plates simultaneously
- 🐳 **Production Ready**: Docker API with smart model caching and multi-architecture support

<br>

## Quick Start

### Installation

```bash
# CPU Installation
pip install marearts-anpr

# GPU Installation (CUDA, DirectML)
pip install marearts-anpr[gpu]        # NVIDIA CUDA
pip install marearts-anpr[directml]   # Windows GPU (AMD/Intel/NVIDIA)
```

📦 [See complete installation guide](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/installation.md)

### Basic Usage


```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v14, marearts_anpr_from_image_file

# Initialize detector
detector = ma_anpr_detector_v14(
    "micro_320p_fp32",
    # 320p models (Fast): pico_320p_fp32/fp16, micro_320p_fp32/fp16, small_320p_fp32/fp16, medium_320p_fp32/fp16, large_320p_fp32/fp16
    # 640p models (High detection): pico_640p_fp32/fp16, micro_640p_fp32/fp16, small_640p_fp32/fp16, medium_640p_fp32/fp16, large_640p_fp32/fp16
    user_name,
    serial_key,
    signature,
    backend="cuda",  # cpu, cuda, directml (auto-selected if "auto")
    conf_thres=0.25,  # Detection confidence threshold (default: 0.25)
    iou_thres=0.5     # IoU threshold for NMS (default: 0.5)
)

# Initialize OCR with regional vocabulary
ocr = ma_anpr_ocr_v14(
    "small_fp32",       # Model: pico_fp32, micro_fp32, small_fp32, medium_fp32, large_fp32
    "univ",             # Region: kr, eup, na, cn, univ (choose specific region for best accuracy)
    user_name,
    serial_key,
    signature,
    backend="cuda",  # cpu, cuda, directml (auto-selected if "auto") 
)

# Process image
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
print(result)
# Output: {'results': [{'ocr': 'ABC123', 'ocr_conf': 99, ...}], ...}
```
💡 🔄 [Learn more about usage](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/usage.md#dynamic-region-switching)

#### Dynamic Region Switching

Switch regions without reinitialization:

```python
ocr.set_region('eup')  # Europe+
ocr.set_region('kr')   # Korean
ocr.set_region('na')   # North America
ocr.set_region('cn')   # China
ocr.set_region('univ') # Universal (all regions)
```

🔄 [Learn more about dynamic region switching](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/usage.md#dynamic-region-switching)

#### Multiple Input Formats & CLI

**From different image sources:**
```python
import cv2
from PIL import Image
from marearts_anpr import marearts_anpr_from_cv2, marearts_anpr_from_pil

result = marearts_anpr_from_cv2(detector, ocr, cv2.imread("image.jpg"))
result = marearts_anpr_from_pil(detector, ocr, Image.open("image.jpg"))
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
```

**CLI commands:**
```bash
ma-anpr image.jpg                    # Process image
ma-anpr test-api image.jpg           # Test API (1000/day limit)
ma-anpr validate                     # Validate license
```

🔧 [See complete usage examples and CLI reference](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/usage.md)

<br>

## Model Performance

### Detector Performance

| Model Name | Detection Rate | Speed (GPU) | Notes |
|------------|----------------|-------------|-------|
| **micro_320p_fp32** | **97.13%** | **128 FPS** (7.8ms) | 🏆 Best overall |
| **micro_320p_fp16** | **97.13%** | **56 FPS** (17.9ms) | 🏆 Best mobile (50% smaller) |
| micro_640p_fp32 | 98.99% | 68 FPS (14.6ms) | Highest detection |
| small_320p_fp32 | 98.00% | 142 FPS (7.0ms) | ⚡ Fastest |
| medium_320p_fp32 | 98.06% | 136 FPS (7.4ms) | High detection |
| pico_320p_fp32 | 96.02% | 129 FPS (7.8ms) | Smallest + fast |
| pico_640p_fp32 | 98.54% | 66 FPS (15.2ms) | Balanced |

**Note:** 320p models are 2× faster than 640p. FP16 models are 50% smaller with same detection rate.

<br>

### OCR Performance

*Average across all regions*

| Model Name | Exact Match | Character Accuracy | Speed (GPU) | Notes |
|------------|-------------|-------------------|-------------|-------|
| **large_fp32** | **91.70%** | **96.27%** | 262 FPS (3.8ms) | 🎯 Best accuracy |
| micro_fp32 | 91.86% | 96.50% | 262 FPS (3.8ms) | Fast with good accuracy |
| pico_fp32 | 91.78% | 96.65% | 270 FPS (3.7ms) | Fastest, smallest |
| small_fp32 | 91.54% | 96.64% | 300 FPS (3.3ms) | ⚡ Fastest inference |
| medium_fp32 | 90.36% | 96.45% | 270 FPS (3.7ms) | Balanced performance |

**Supported Regions**: Korean (`kr`), Europe+ (`eup`), North America (`na`), China (`cn`), Universal (`univ`)

📊 [See all models and benchmarks](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/models.md)

<br>

## Regional Support

MareArts ANPR supports license plates from multiple regions with specialized vocabulary optimization:

- 🇰🇷 **Korean (`kr`)** - Korean license plates with Hangul characters (best accuracy: 99.27%)
- 🇪🇺 **Europe+ (`eup`)** - EU countries + Albania, Andorra, Bosnia & Herzegovina, Indonesia, and more
- 🇺🇸🇨🇦🇲🇽 **North America (`na`)** - USA, Canada, and Mexico license plates
- 🇨🇳 **China (`cn`)** - Chinese license plates with province codes
- 🌍 **Universal (`univ`)** - All regions (default, but choose specific region for best accuracy)

💡 **Dynamic Region Switching**: Use `ocr.set_region('kr')` to switch regions instantly without reloading the model, saving ~180 MB per additional region.

🌍 [See complete regional support and character sets](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/regional-support.md)

<br>

## Documentation

- 📦 [Installation Guide](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/installation.md) - Detailed installation options and requirements
- 🔧 [Usage Examples](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/usage.md) - Python SDK, CLI usage, dynamic region switching, and environment variables
- 💻 [Example Code](https://github.com/MareArts/MareArts-ANPR/tree/main/example_code) - Basic, advanced, and batch processing examples
- 🚀 [Model Versions](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/models.md) - Available models, benchmarks, and performance metrics
- 🌍 [Regional Support](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/regional-support.md) - Supported countries and character sets
- 🐳 [Docker Deployment](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/docker.md) - Container setup, API server, and multi-architecture builds
- 🧪 [Try ANPR](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/api-testing.md) - Test our ANPR without license (1000 requests/day)
- ❓ [FAQ](https://github.com/MareArts/MareArts-ANPR/blob/main/docs/faq.md) - Licensing, regions, features, and troubleshooting

<br>

## MareArts Ecosystem

Explore our AI toolkit:

- **marearts-anpr** - Automatic Number Plate Recognition ([GitHub](https://github.com/MareArts/MareArts-ANPR))
- **🎉 marearts-anpr Mobile App** - ANPR on iOS & Android ([App Store](https://apps.apple.com/us/app/marearts-anpr/id6753904859) | [Guide](https://github.com/MareArts/MareArts-ANPR/blob/main/mobile_app/APP_GUIDE.md))
- **marearts-road-objects** - Road object detection for persons, vehicles, and 2-wheelers ([GitHub](https://github.com/MareArts/MareArts-Road-Objects))
- **marearts-xcolor** - Color extraction and similarity analysis ([GitHub](https://github.com/MareArts/MareArts-Xcolor))
- **marearts-mast** - Real-time panoramic stitching ([GitHub](https://github.com/MareArts/MareArts-MAST))
- **marearts-crystal** - Encryption and decryption toolkit ([PyPI](https://pypi.org/project/marearts-crystal/))

<br>

## Support & Resources

| Resource | Link |
|----------|------|
| 📧 **Contact** | [hello@marearts.com](mailto:hello@marearts.com) |
| 🏠 **Homepage** | [https://marearts.com](https://marearts.com) |
| 💳 **License Purchase** | [ANPR Solution](https://www.marearts.com/products/anpr) |
| 🎮 **Live Demo** | [http://live.marearts.com](http://live.marearts.com) |
| 📺 **Video Examples** | [YouTube Playlist](https://www.youtube.com/playlist?list=PLvX6vpRszMkxJBJf4EjQ5VCnmkjfE59-J) |

<br>

## License

© 2024 MareArts. All rights reserved.

This software requires a valid license key. Visit [MareArts ANPR Solution](https://www.marearts.com/products/anpr) for licensing options.
