# Installation Guide

## System Requirements

- **Python**: 3.9, 3.10, 3.11, or 3.12
- **Operating System**: Linux (x86_64, ARM64), macOS, Windows
- **Memory**: Minimum 4GB RAM (8GB recommended for GPU)
- **Storage**: ~500MB for model files (SDK wheels are ~650&nbsp;KB)
- **GPU** (optional): NVIDIA CUDA compatible

## Installation Options

### CPU Installation (Universal)

Lightweight installation for all platforms:

```bash
pip install marearts-anpr
```

### GPU Installation

#### NVIDIA CUDA GPU (Linux/Windows)
For faster processing with CUDA support:

```bash
pip install marearts-anpr[gpu]
```

#### Windows GPU (AMD/Intel/NVIDIA)
DirectML support for Windows systems:

```bash
pip install marearts-anpr[directml]
```

#### All GPU Support
Maximum compatibility across different GPU types:

```bash
pip install marearts-anpr[all-gpu]
```

## GPU Acceleration

The SDK automatically detects and uses available hardware:

1. **CUDA** (NVIDIA GPUs) - Faster processing
2. **DirectML** (Windows) - Works with various GPU types
3. **CPU** - Default when no GPU is available

### Performance Comparison

| Configuration | Processing Speed | Use Case |
|--------------|------------------|----------|
| NVIDIA GPU (CUDA) | Fastest | Production servers, Real-time processing |
| DirectML (Windows) | GPU Accelerated | Windows systems (AMD/Intel/NVIDIA) |
| CPU Only | Baseline | General usage, Edge devices |

## License Setup

You can set credentials in three ways:

### License Configuration

**You receive these credentials when you subscribe:** [Get your license here](https://www.marearts.com/products/anpr)

- Username (your email)
- Serial key
- Signature (for V14 models)

**Setup Methods:**

1. **CLI configuration** (recommended - interactive setup):
```bash
ma-anpr config
```

This command will prompt for your credentials and save them to `~/.marearts/.marearts_env`.

To use in your code, load the environment file:
```bash
source ~/.marearts/.marearts_env
```

Then access in Python:
```python
import os
username = os.getenv("MAREARTS_ANPR_USERNAME")
serial_key = os.getenv("MAREARTS_ANPR_SERIAL_KEY")
signature = os.getenv("MAREARTS_ANPR_SIGNATURE")

detector = ma_anpr_detector_v14("small_640p_fp32", username, serial_key, signature)
```

2. **Environment variables** (manual - temporary, not recommended):
```bash
export MAREARTS_ANPR_USERNAME="your-email@domain.com"
export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"
export MAREARTS_ANPR_SIGNATURE="your-signature"
```
**Note:** This only sets variables for the current session and doesn't save to file. Use `ma-anpr config` for persistent storage.

3. **Direct in code** (hardcoded credentials):
```python
# Supported detector modes:
#   model: {size}_{res}_{prec} (e.g., micro_320p_fp32, medium_640p_fp32)
#   size: pico, micro, small, medium, large | res: 320p, 640p | prec: fp32, fp16
#   backend: "cpu", "cuda", "directml", "auto" (default: cpu)
# V14 detector
detector = ma_anpr_detector_v14(
    "micro_320p_fp32", 
    "your-email", 
    "your-serial-key",
    "your-signature"
)

# Supported OCR modes:
#   model: pico_fp32, micro_fp32, small_fp32, medium_fp32, large_fp32
#   region: "kr", "eup", "na", "cn", "univ" (default: univ)
#   backend: "cpu", "cuda", "directml", "auto" (default: cpu)
# V14 OCR with regional vocabularies
ocr = ma_anpr_ocr_v14(
    model='small_fp32',
    region='kr',  # kr, eup, na, cn, univ (default: univ)
    user_name="your-email",
    serial_key="your-serial-key",
    signature="your-signature"
)
```

**Regions:**
- **kr** - Korean license plates (best for Korean)
- **eup** - European+ plates (EU countries + additional European countries + Indonesia)
- **na** - North American plates (USA, Canada)
- **cn** - Chinese plates
- **univ** - Universal (all regions) - **default, but choose specific region for best accuracy**

### Model Storage Location

Models are automatically downloaded to `~/.marearts/marearts_anpr_data/` on first use.

```
~/.marearts/
├── .marearts_env          # Credentials file
└── marearts_anpr_data/    # ANPR models (auto-downloaded)
    ├── v14_medium_640p_fp32.dat
    ├── v14_medium_fp32.dat
    └── ... (other models)
```

### Verify Installation

After installation, verify everything is working:

```bash
# Check version
ma-anpr --version

# Validate license
ma-anpr validate

# Check GPU availability
ma-anpr gpu-info

# List available models
ma-anpr models
```
