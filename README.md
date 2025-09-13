# MareArts ANPR SDK

[![PyPI version](https://badge.fury.io/py/marearts-anpr.svg)](https://badge.fury.io/py/marearts-anpr)
[![Python versions](https://img.shields.io/pypi/pyversions/marearts-anpr.svg)](https://pypi.org/project/marearts-anpr/)
[![Downloads](https://pepy.tech/badge/marearts-anpr)](https://pepy.tech/project/marearts-anpr)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](https://study.marearts.com/p/anpr-lpr-solution.html)
[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen.svg)](http://live.marearts.com)

Automatic Number Plate Recognition (ANPR) SDK for multiple regions with GPU acceleration support.

## Features

- 🚗 **Multi-Region Support**: EU, Korea, China, and Universal license plates
- ⚡ **Performance**: Optimized C++ core with GPU acceleration support
- 🎯 **Accuracy**: Trained detection and OCR models for various regions
- 🆕 **V14 Models**: Latest generation with enhanced security and multi-backend support
- 🔧 **Integration**: Python API and command-line tools
- 🐳 **Deployment**: Docker support and API server examples

## Quick Start

### Installation

```bash
# CPU Installation
pip install marearts-anpr

# GPU Installation (for faster processing)
pip install marearts-anpr[gpu]        # NVIDIA CUDA
pip install marearts-anpr[directml]   # Windows GPU
```

### Basic Usage

#### V1/V2 License (Legacy Models)
```python
from marearts_anpr import marearts_anpr_from_image_file
from marearts_anpr import ma_anpr_detector, ma_anpr_ocr

# Set environment variables (recommended)
# export MAREARTS_ANPR_USERNAME="your-email@domain.com"
# export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"

# Initialize
detector = ma_anpr_detector("v13_middle", user_name, serial_key)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)

# Process image
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
print(result)
# Output: {'results': [{'ocr': 'ABC123', 'ocr_conf': 99, ...}], ...}
```

#### V2 License (V14 Models)
```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr

# V2 credentials with signature
# export MAREARTS_ANPR_SIGNATURE="your-16-char-signature"

# Initialize V14 detector
detector = ma_anpr_detector_v14(
    "v14_small_640p_fp16",  # V14 model
    user_name, 
    serial_key,  # MAEV2: format
    signature,   # Required for V14
    backend="cuda"  # cpu, cuda, directml, tensorrt
)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)

# Process image
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
```

### CLI Usage

```bash
# Process image
ma-anpr image.jpg

# Test without credentials (1000 requests/day)
ma-anpr test-api image.jpg

# Validate license
ma-anpr validate
```

## V14 Models (NEW!)

The latest V14 models introduce enhanced features:

### Features
- 🔐 **Digital Signature Authentication**: Enhanced security with V2 licenses
- 🎯 **Multi-Backend Support**: CPU, CUDA, DirectML, TensorRT
- ⚡ **Optimized Inference**: FP32, FP16, and FP8 precision options
- 🚀 **TensorRT Acceleration**: Up to 4x faster on NVIDIA GPUs

### Requirements
- V2 License key (starts with `MAEV2:`)
- Digital signature (16 hex characters)
- Backend-specific dependencies (CUDA, TensorRT, etc.)

### Available V14 Models
- **Standard**: `v14_small_320p_fp32`, `v14_small_320p_fp16`, `v14_small_640p_fp32`, `v14_small_640p_fp16`
- **TensorRT**: `v14_small_320p_trt_fp8`, `v14_small_320p_trt_fp16`, `v14_small_640p_trt_fp8`, `v14_small_640p_trt_fp16`
- **Coming Soon**: V14 middle and large models

## Documentation

- 📦 [Installation Guide](docs/installation.md) - Detailed installation options and requirements
- 🔧 [Usage Examples](docs/usage.md) - Python SDK and CLI usage
- 🚀 [Model Versions](docs/models.md) - Available models and benchmarks
- 🌍 [Regional Support](docs/regional-support.md) - Supported countries and characters
- 🐳 [Docker Deployment](docs/docker.md) - Container setup and API server
- 🧪 [Try ANPR](docs/api-testing.md) - Test our ANPR without license
- ❓ [FAQ](docs/faq.md) - Frequently asked questions

## Performance

*Benchmarked on: Intel i7-9800X @ 3.8GHz | NVIDIA RTX 4090 | Ubuntu Linux*

### V14 Models (V2 License Required)
| Model | Precision | Recall | F1 Score | Speed CUDA (ms) | Speed CPU (ms) | Notes |
|-------|-----------|---------|----------|-----------------|----------------|--------|
| v14_small_320p_fp16 | 95.93% | 97.02% | 95.63% | 15.9 | 64.7 | Edge devices |
| v14_small_640p_fp16 | 94.99% | 98.40% | 95.81% | 22.3 | 182.2 | 🎯 Recommended |
| v14_small_320p_trt_fp8 | 95.93% | 97.02% | 95.63% | ~8-12 | - | ⚡ Fastest |

### V13 Models (All Licenses)
| Model | Precision | Recall | F1 Score | Speed CUDA (ms) |
|-------|-----------|---------|----------|-----------------|
| v13_nano (Detector) | 95.3% | 96.5% | 0.951 | 7.0 |
| v13_small (Detector) | 95.7% | 97.9% | 0.961 | 7.4 |
| v13_middle (Detector) | 95.7% | 98.0% | 0.962 | 8.3 |
| v13_large (Detector) | 95.9% | 98.1% | 0.964 | 9.5 |
| v13_euplus (OCR) | 96.2% | - | 0.990 | 82 |
| v13_kr (OCR) | 97.2% | - | 0.995 | 85 |
| v13_cn (OCR) | 96.6% | - | 0.993 | 86 |
| v13_univ (OCR) | 98.3% | - | 0.996 | 85 |

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
| 🧪 **Colab Demo** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zZlueTZ1Le73yOQ3mdJFONxcebKyCgr-?usp=sharing) |

## License

© 2024 MareArts. All rights reserved.

This software requires a valid license key. Visit [MareArts ANPR Solution](https://study.marearts.com/p/anpr-lpr-solution.html) for licensing options.