# Installation Guide

## System Requirements

- **Python**: 3.9, 3.10, 3.11, or 3.12
- **Operating System**: Linux (x86_64, ARM64), macOS, Windows
- **Memory**: Minimum 4GB RAM (8GB recommended for GPU)
- **Storage**: ~500MB for model files
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

#### Development Dependencies
For developers and contributors:

```bash
pip install marearts-anpr[dev]
```

## GPU Acceleration

The SDK automatically detects and uses available hardware:

1. **CUDA** (NVIDIA GPUs) - Faster processing
2. **DirectML** (Windows) - Works with various GPU types
3. **CPU** - Default when no GPU is available

### Performance Comparison

| Configuration | Processing Speed | Use Case |
|--------------|------------------|----------|
| NVIDIA GPU (CUDA) | Faster | Production servers |
| DirectML (Windows) | Moderate speedup | Windows development |
| CPU Only | Baseline | General usage |

## License Setup (Optional)

You can set credentials in three ways:

### V1 (Legacy) License Setup
1. **Environment variables** (recommended for security):
```bash
export MAREARTS_ANPR_USERNAME="your-email@domain.com"
export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"
```

2. **CLI configuration**:
```bash
ma-anpr config
```

3. **Direct in code**:
```python
detector = ma_anpr_detector("v13_middle", "your-email", "your-key")
```

### V2 (Current) License Setup
V2 is the current license format. You receive all credentials when you purchase:

1. **Environment variables**:
```bash
export MAREARTS_ANPR_USERNAME="your-email@domain.com"
export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"
export MAREARTS_ANPR_SIGNATURE="your-signature"
```

2. **CLI configuration** (automatically detects V2 and prompts for signature):
```bash
ma-anpr config
```

3. **Direct in code**:
```python
# V14 detector requires signature
detector = ma_anpr_detector_v14(
    "v14_small_640p_fp16", 
    "your-email", 
    "your-serial-key",
    "your-signature",  # provided with V2 license
    backend="cuda"  # or "cpu", "directml", "tensorrt"
)
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
