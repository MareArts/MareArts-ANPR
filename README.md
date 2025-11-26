# MareArts ANPR SDK

[![PyPI version](https://badge.fury.io/py/marearts-anpr.svg)](https://badge.fury.io/py/marearts-anpr)
[![Python versions](https://img.shields.io/pypi/pyversions/marearts-anpr.svg)](https://pypi.org/project/marearts-anpr/)
[![Downloads](https://pepy.tech/badge/marearts-anpr)](https://pepy.tech/project/marearts-anpr)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](https://study.marearts.com/p/anpr-lpr-solution.html)
[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen.svg)](http://live.marearts.com)

Automatic Number Plate Recognition (ANPR) SDK for multiple regions with GPU acceleration support.

## Features

- 🌍 **Multi-Region Support**: Korean, Europe+, North America, China, and Universal license plates
- 🔄 **Dynamic Region Switching**: Change regions instantly with `set_region()` without model reload
- ⚡ **GPU Acceleration**: CUDA, DirectML support for real-time processing
- 🎯 **High Accuracy**: Advanced models with regional vocabulary optimization
- 📦 **Batch Processing**: Process multiple plates simultaneously
- 🐳 **Production Ready**: Docker API with smart model caching and multi-architecture support

## Quick Start

### Installation

```bash
# CPU Installation
pip install marearts-anpr

# GPU Installation (CUDA, DirectML)
pip install marearts-anpr[gpu]        # NVIDIA CUDA
pip install marearts-anpr[directml]   # Windows GPU (AMD/Intel/NVIDIA)
```

📦 [See complete installation guide](docs/installation.md)

### Basic Usage

💡 **Model names**: See [models and benchmarks](docs/models.md) (e.g., `small_640p_fp32`, `small_fp32`)

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v14, marearts_anpr_from_image_file

# Initialize detector
detector = ma_anpr_detector_v14(
    "small_640p_fp32",  # pico_640p_fp32, micro_640p_fp32, small_640p_fp32, medium_640p_fp32, large_640p_fp32
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

#### Dynamic Region Switching

Switch regions without reinitialization:

```python
ocr.set_region('eup')  # Europe+
ocr.set_region('kr')   # Korean
ocr.set_region('na')   # North America
```

🔄 [Learn more about dynamic region switching](docs/usage.md#dynamic-region-switching-370)

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

🔧 [See complete usage examples and CLI reference](docs/usage.md)

## Model Performance

### Detector Performance

| Model Name | F1 Score | Speed CUDA | Speed CPU | Notes |
|-------|----------|------------|-----------|-------|
| pico_640p_fp32 | 93.08% | 68.7 FPS (14.5ms) | - | Fastest, smallest model |
| micro_640p_fp32 | 93.39% | 69.5 FPS (14.4ms) | - | Fast with good accuracy |
| small_640p_fp32 | 92.58% | 69.5 FPS (14.4ms) | - | Balanced performance |
| medium_640p_fp32 | 92.27% | 62.1 FPS (16.1ms) | - | Higher accuracy |
| large_640p_fp32 | 93.77% | 57.4 FPS (17.4ms) | - | 🎯 Highest F1 score |

### OCR Performance

*Average across all regions*

| Model Name | Exact Match | Char Accuracy | FPS | Notes |
|-------|-------------|---------------|-----|-------|
| pico_fp32 | 91.78% | 96.65% | 270 | Fastest, smallest |
| micro_fp32 | 91.86% | 96.50% | 262 | Fast with good accuracy |
| small_fp32 | 91.54% | 96.64% | **300** | ⚡ Fastest inference |
| medium_fp32 | 90.36% | 96.45% | 270 | Balanced performance |
| **large_fp32** | **91.70%** | **96.27%** | 262 | 🎯 Best accuracy |

**Supported Regions**: Korean (`kr`), Europe+ (`eup`), North America (`na`), China (`cn`), Universal (`univ`)

📊 [See detailed benchmarks by region](docs/models.md)

## Regional Support

MareArts ANPR supports license plates from multiple regions with specialized vocabulary optimization:

- 🇰🇷 **Korean (`kr`)** - Korean license plates with Hangul characters (best accuracy: 99.27%)
- 🇪🇺 **Europe+ (`eup`)** - EU countries + Albania, Andorra, Bosnia & Herzegovina, Indonesia, and more
- 🇺🇸 **North America (`na`)** - USA and Canada license plates
- 🇨🇳 **China (`cn`)** - Chinese license plates with province codes
- 🌍 **Universal (`univ`)** - All regions (default, but choose specific region for best accuracy)

💡 **Dynamic Region Switching**: Use `ocr.set_region('kr')` to switch regions instantly without reloading the model, saving ~180 MB per additional region.

🌍 [See complete regional support and character sets](docs/regional-support.md)

## Documentation

- 📦 [Installation Guide](docs/installation.md) - Detailed installation options and requirements
- 🔧 [Usage Examples](docs/usage.md) - Python SDK, CLI usage, dynamic region switching, and environment variables
- 💻 [Example Code](example_code/) - Basic, advanced, and batch processing examples
- 🚀 [Model Versions](docs/models.md) - Available models, benchmarks, and performance metrics
- 🌍 [Regional Support](docs/regional-support.md) - Supported countries and character sets
- 🐳 [Docker Deployment](docs/docker.md) - Container setup, API server, and multi-architecture builds
- 🧪 [Try ANPR](docs/api-testing.md) - Test our ANPR without license (1000 requests/day)
- ❓ [FAQ](docs/faq.md) - Licensing, regions, features, and troubleshooting

## MareArts Ecosystem

Explore our AI toolkit:

- **marearts-anpr** - Automatic Number Plate Recognition ([GitHub](https://github.com/MareArts/MareArts-ANPR))
- **marearts-road-objects** - Road object detection for persons, vehicles, and 2-wheelers ([GitHub](https://github.com/MareArts/MareArts-Road-Objects))
- **marearts-xcolor** - Color extraction and similarity analysis ([GitHub](https://github.com/MareArts/MareArts-Xcolor))
- **marearts-mast** - Real-time panoramic stitching ([GitHub](https://github.com/MareArts/MareArts-MAST))
- **marearts-crystal** - Encryption and decryption toolkit ([PyPI](https://pypi.org/project/marearts-crystal/))

## Support & Resources

| Resource | Link |
|----------|------|
| 📧 **Contact** | [hello@marearts.com](mailto:hello@marearts.com) |
| 🏠 **Homepage** | [https://marearts.com](https://marearts.com) |
| 💳 **License Purchase** | [ANPR Solution](https://study.marearts.com/p/anpr-lpr-solution.html) |
| 🎮 **Live Demo** | [http://live.marearts.com](http://live.marearts.com) |
| 📺 **Video Examples** | [YouTube Playlist](https://www.youtube.com/playlist?list=PLvX6vpRszMkxJBJf4EjQ5VCnmkjfE59-J) |

## License

© 2024 MareArts. All rights reserved.

This software requires a valid license key. Visit [MareArts ANPR Solution](https://study.marearts.com/p/anpr-lpr-solution.html) for licensing options.
