# MareArts ANPR Server — Docker

Run the MareArts ANPR server as a Docker container — with **GPU (CUDA)** or **CPU-only**.

The Docker image includes the complete ANPR server with 20+ REST API endpoints, web dashboard, Vehicle Intelligence, and all V16 models — ready to deploy in seconds.

<div align="center">

| Dashboard | Detection | History |
|:---:|:---:|:---:|
| <img src="../server/server_screenshot/server_overview.png" alt="Dashboard" width="260"/> | <img src="../server/server_screenshot/server_detect.png" alt="Detection" width="260"/> | <img src="../server/server_screenshot/server_history.png" alt="History" width="260"/> |

</div>

---

## Two Images

| | GPU (CUDA) | CPU |
|---|---|---|
| **Dockerfile** | `Dockerfile` | `Dockerfile.cpu` |
| **Base** | `nvidia/cuda:12.5.1-cudnn-runtime-ubuntu22.04` | `ubuntu:22.04` |
| **Python** | 3.13 | 3.13 |
| **Runtime** | `onnxruntime-gpu` (CUDA + TensorRT + CPU fallback) | `onnxruntime` (CPU only) |
| **Image size** | ~5-6 GB | ~1-1.5 GB |
| **Requires** | NVIDIA GPU + Container Toolkit | Any machine with Docker |
| **Best for** | Production, high throughput | Development, testing, no-GPU servers |

---

## Prerequisites

- **Docker** 20.10+
- **NVIDIA Container Toolkit** (GPU image only) — [Install Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- **MareArts License** — [Get one here](https://www.marearts.com/products/anpr)

---

## Quick Start — GPU

```bash
docker build -t marearts-anpr-server:latest .
```

```bash
docker run -d \
  --gpus all \
  --name marearts-anpr-server \
  -p 8000:8000 \
  -e MAREARTS_ANPR_USERNAME="your@email.com" \
  -e MAREARTS_ANPR_SERIAL_KEY="your_serial_key" \
  -e MAREARTS_ANPR_SIGNATURE="your_signature" \
  -v ~/.marearts:/root/.marearts \
  marearts-anpr-server:latest
```

## Quick Start — CPU

```bash
docker build -t marearts-anpr-server-cpu:latest -f Dockerfile.cpu .
```

```bash
docker run -d \
  --name marearts-anpr-server-cpu \
  -p 8000:8000 \
  -e MAREARTS_ANPR_USERNAME="your@email.com" \
  -e MAREARTS_ANPR_SERIAL_KEY="your_serial_key" \
  -e MAREARTS_ANPR_SIGNATURE="your_signature" \
  -v ~/.marearts:/root/.marearts \
  marearts-anpr-server-cpu:latest
```

> No `--gpus` flag needed for CPU. Works on any machine — Linux, macOS, Windows, ARM, cloud VMs without GPU.

---

## Use it

```bash
# Health check
curl http://localhost:8000/api/health

# Detect plates
curl -X POST http://localhost:8000/api/anpr -F "image=@car.jpg"

# Vehicle Intelligence (make, model, color, type)
curl -X POST http://localhost:8000/api/anpr/mmc -F "image=@car.jpg"

# Open dashboard in browser
open http://localhost:8000
```

---

## Build from Source

```bash
git clone https://github.com/MareArts/MareArts-ANPR.git
cd MareArts-ANPR/docker

# GPU image
docker build -t marearts-anpr-server:latest .

# CPU image
docker build -t marearts-anpr-server-cpu:latest -f Dockerfile.cpu .
```

---

## Credentials

The server needs your MareArts license credentials. Three options:

### Option 1: Environment Variables (recommended)

```bash
docker run -d \
  -e MAREARTS_ANPR_USERNAME="your@email.com" \
  -e MAREARTS_ANPR_SERIAL_KEY="your_serial_key" \
  -e MAREARTS_ANPR_SIGNATURE="your_signature" \
  ...
```

### Option 2: Credentials File

Create `~/.marearts/.marearts_env`:

```bash
export MAREARTS_ANPR_USERNAME="your@email.com"
export MAREARTS_ANPR_SERIAL_KEY="your_serial_key"
export MAREARTS_ANPR_SIGNATURE="your_signature"
```

Then mount the directory:

```bash
docker run -d \
  -v ~/.marearts:/root/.marearts \
  ...
```

### Option 3: Interactive Setup

```bash
docker run -it --rm \
  -v ~/.marearts:/root/.marearts \
  marearts-anpr-server:latest \
  ma-anpr config
```

This saves credentials to `~/.marearts/` for future use.

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `MAREARTS_ANPR_USERNAME` | License email | (required) |
| `MAREARTS_ANPR_SERIAL_KEY` | License serial key | (required) |
| `MAREARTS_ANPR_SIGNATURE` | License signature | (required) |
| `ANPR_BACKEND` | Inference backend: `auto`, `cuda`, `cpu` | `auto` (GPU) / `cpu` (CPU image) |
| `ANPR_HOST` | Server bind address | `0.0.0.0` |
| `ANPR_PORT` | Server port | `8000` |
| `ANPR_REGION` | Default OCR region | `univ` |
| `ANPR_THREADS` | Worker threads | `4` |

---

## API Endpoints

Once the server is running, you have access to 20+ endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Server health and status |
| `/api/anpr` | POST | Detect and read plates |
| `/api/anpr/mmc` | POST | Vehicle Intelligence (make, model, color, type) |
| `/api/config` | GET | Server configuration |
| `/api/stats` | GET | Request statistics |
| `/api/history` | GET | Detection history |
| `/api/watchlist` | GET/POST | Manage plate watchlist |
| `/api/alerts` | GET | View triggered alerts |
| `/api/regions` | GET | Available OCR regions |
| `/api/models` | GET | Loaded model info |
| `/docs` | GET | Interactive API documentation (Swagger) |

Full API documentation is available at `http://localhost:8000/docs` when the server is running.

---

## Docker Compose

### GPU

```yaml
version: "3.8"
services:
  anpr-server:
    image: marearts-anpr-server:latest
    ports:
      - "8000:8000"
    environment:
      - MAREARTS_ANPR_USERNAME=your@email.com
      - MAREARTS_ANPR_SERIAL_KEY=your_serial_key
      - MAREARTS_ANPR_SIGNATURE=your_signature
      - ANPR_BACKEND=auto
    volumes:
      - ~/.marearts:/root/.marearts
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 60s
      timeout: 30s
      start_period: 300s
      retries: 5
```

### CPU

```yaml
version: "3.8"
services:
  anpr-server:
    image: marearts-anpr-server-cpu:latest
    ports:
      - "8000:8000"
    environment:
      - MAREARTS_ANPR_USERNAME=your@email.com
      - MAREARTS_ANPR_SERIAL_KEY=your_serial_key
      - MAREARTS_ANPR_SIGNATURE=your_signature
      - ANPR_BACKEND=cpu
    volumes:
      - ~/.marearts:/root/.marearts
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 60s
      timeout: 30s
      start_period: 300s
      retries: 5
```

```bash
docker compose up -d
```

---

## Useful Commands

```bash
# View logs
docker logs -f marearts-anpr-server

# Check health
docker exec marearts-anpr-server curl -s http://localhost:8000/api/health

# Verify providers (GPU image)
docker exec marearts-anpr-server python -c "import onnxruntime; print(onnxruntime.get_available_providers())"
# Expected: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']

# Verify providers (CPU image)
docker exec marearts-anpr-server-cpu python -c "import onnxruntime; print(onnxruntime.get_available_providers())"
# Expected: ['CPUExecutionProvider']

# Stop the server
docker stop marearts-anpr-server

# Remove the container
docker rm marearts-anpr-server
```

---

## Support

| | |
|---|---|
| Homepage | [marearts.com](https://marearts.com) |
| License | [marearts.com/products/anpr](https://www.marearts.com/products/anpr) |
| Live Demo | [live.marearts.com](http://live.marearts.com) |
| Contact | [hello@marearts.com](mailto:hello@marearts.com) |
| Server Docs | [Server README](../server/) |
| SDK Docs | [Python SDK README](../python-sdk/) |

---

© 2026 MareArts. All rights reserved.
