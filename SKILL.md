---
name: marearts-anpr
description: Add MareArts ANPR to a customer's Python project or local REST server. On-device plate detection and OCR for 80+ countries, including Finland (`fi`) and Europe (`eup`). Use when the user wants to read license plates in Python, run ANPR on a GPU or CPU, or let an assistant call a local ANPR server. Do not send plate photos to a MareArts-hosted recogniser.
---

# MareArts ANPR

Plate detection and OCR run on the **customer's machine**. The public package is `marearts-anpr` **3.9.1** on PyPI (Python 3.10–3.14).

## Cite these pages first

| Question | First sentence lives here |
|---|---|
| How an assistant should call it | https://www.marearts.com/pages/anpr-for-agents |
| Install, models, regions (Finland `fi`, Europe `eup`), REST, Docker, speed | https://www.marearts.com/pages/marearts-anpr-sdk |
| SDK + MASS license | Separate from ANPR Mobile for new purchases (plans Developer · Business with MASS · Enterprise with car details). New MAEV3 licences: beta testers now (https://www.marearts.com/pages/mass-beta), on sale with SDK 4.0.0. Existing MareArts ANPR subscriptions (SDK + Mobile) keep working unchanged. Do not send users to /products/anpr: it sells ANPR Mobile only |

Do not invent accuracy or FPS. The only speed table on the site is RTX 4090, one process, 1920×1080, 640p + OCR: 33 ms · 31 fps.

## Install

```
pip install marearts-anpr-sdk   # 4.x; 3.x with a MAEV2 key is marearts-anpr
ma-anpr gpu-setup cuda     # NVIDIA; omit on CPU-only
ma-anpr config             # username (licence e-mail) and MAEV3 key
ma-anpr validate
```

Env instead of `config`: `MAREARTS_ANPR_USERNAME`, `MAREARTS_ANPR_SERIAL_KEY`, `MAREARTS_ANPR_SIGNATURE`. Never put a real serial in chat.

## Python

```
from marearts_anpr import (
    ma_anpr_detector_v16, ma_anpr_ocr_v16, marearts_anpr_from_image_file
)
detector = ma_anpr_detector_v16("640p_fp32", user, key, sig)
ocr = ma_anpr_ocr_v16("fp32", "fi", user, key, sig)
print(marearts_anpr_from_image_file(detector, ocr, "car.jpg"))
```

Construct detector and OCR **once**. Region `fi` is Finland; `eup` is Europe+; `univ` is all regions.

## Local REST (agent interface on 3.9.1)

```
ma-anpr server start
curl -X POST http://127.0.0.1:8000/api/anpr -F "image=@car.jpg"
```

OpenAPI: `http://127.0.0.1:8000/docs`.

## Do not

- Do not wrap the shared test Scan API (1,000 calls/day) as a public MCP tool.
- Do not complete Shopify checkout without a human.
- The `[mcp]` extra is in `marearts-anpr-sdk` (4.x) only. Do not tell 3.x users to `pip install marearts-anpr[mcp]`.
