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

### CLI Usage

```bash
# Process image
ma-anpr image.jpg

# Test without credentials (1000 requests/day)
ma-anpr test-api image.jpg

# Validate license
ma-anpr validate
```

## Documentation

- 📦 [Installation Guide](docs/installation.md) - Detailed installation options and requirements
- 🔧 [Usage Examples](docs/usage.md) - Python SDK and CLI usage
- 🚀 [Model Versions](docs/models.md) - Available models and benchmarks
- 🌍 [Regional Support](docs/regional-support.md) - Supported countries and characters
- 🐳 [Docker Deployment](docs/docker.md) - Container setup and API server
- 🧪 [API Testing](docs/api-testing.md) - Test API documentation
- ❓ [FAQ](docs/faq.md) - Frequently asked questions

## Performance

| Model | Accuracy | F1 Score | Speed (ms) |
|-------|----------|----------|------------|
| v13_middle (Detector) | 96.3% | 0.973 | 163 |
| v13_euplus (OCR) | 96.2% | 0.990 | 82 |
| v13_kr (OCR) | 97.2% | 0.995 | 85 |
| v13_cn (OCR) | 96.6% | 0.993 | 86 |
| v13_univ (OCR) | 98.3% | 0.996 | 85 |

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