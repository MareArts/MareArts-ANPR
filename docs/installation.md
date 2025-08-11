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

## Environment Setup

### License Credentials

Set your license credentials as environment variables:

```bash
# Linux/macOS
export MAREARTS_ANPR_USERNAME="your-email@domain.com"
export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"

# Windows (Command Prompt)
set MAREARTS_ANPR_USERNAME=your-email@domain.com
set MAREARTS_ANPR_SERIAL_KEY=your-serial-key

# Windows (PowerShell)
$env:MAREARTS_ANPR_USERNAME="your-email@domain.com"
$env:MAREARTS_ANPR_SERIAL_KEY="your-serial-key"
```

### Verify Installation

After installation, verify everything is working:

```bash
# Check installation
python -c "import marearts_anpr; print(marearts_anpr.__version__)"

# Validate license
ma-anpr validate

# Check GPU availability
ma-anpr gpu-info

# List available models
ma-anpr models
```
