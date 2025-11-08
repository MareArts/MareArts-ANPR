# Try MareArts ANPR

Test our ANPR solution without purchasing a license. We provide free testing options with daily limits.

## Testing Options

### 1. Web Demo
Visit [http://live.marearts.com](http://live.marearts.com) to test ANPR directly in your browser.

### 2. CLI Testing

Test with your images using our free test API (1000 requests/day):

```bash
# Test with single image
ma-anpr test-api image.jpg

# Test with multiple images
ma-anpr test-api *.jpg

# Specify models and region (note: v14_ prefix required for API)
ma-anpr test-api image.jpg --detector v14_micro_640p_fp32 --ocr v14_micro_fp32 --region univ

# Save results
ma-anpr test-api image.jpg --json results.json
```

### 3. Direct API Call

#### Test Credentials
- **User ID**: `marearts@public`
- **API Key**: `J4K9L2Wory34@G7T1Y8rt-PP83uSSvkV3Z6ioSTR!`

#### cURL Example
```bash
curl -X POST https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr \
     -H "Content-Type: image/jpeg" \
     -H "x-api-key: J4K9L2Wory34@G7T1Y8rt-PP83uSSvkV3Z6ioSTR!" \
     -H "user-id: marearts@public" \
     -H "detector_model_version: v14_medium_640p_fp32" \
     -H "ocr_model_version: v14_medium_fp32" \
     -H "region: eup" \
     --data-binary "@./image.jpg"
```

#### Python Example
```python
import requests
import json

def test_marearts_anpr(image_path, region='eup'):
    url = "https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr"
    
    headers = {
        "Content-Type": "image/jpeg",
        "x-api-key": "J4K9L2Wory34@G7T1Y8rt-PP83uSSvkV3Z6ioSTR!",
        "user-id": "marearts@public",
        "detector_model_version": "v14_medium_640p_fp32",
        "ocr_model_version": "v14_medium_fp32",
        "region": region
    }
    
    with open(image_path, 'rb') as f:
        response = requests.post(url, headers=headers, data=f.read())
    
    return response.json()

# Test with different regions
result = test_marearts_anpr("test_image.jpg", region="eup")  # European+ plates
# result = test_marearts_anpr("test_image.jpg", region="kr")   # Korean plates
# result = test_marearts_anpr("test_image.jpg", region="cn")   # Chinese plates
# result = test_marearts_anpr("test_image.jpg", region="na")   # North American plates
# result = test_marearts_anpr("test_image.jpg", region="univ") # Universal (all regions)
print(json.dumps(result, indent=2))
```

## Response Format

```json
{
    "results": [
        {
            "ocr": "ABC123",
            "ocr_conf": 99,
            "ltrb": [819, 628, 1085, 694],
            "ltrb_conf": 90
        }
    ],
    "ltrb_proc_sec": 0.163,
    "ocr_proc_sec": 0.082
}
```

## Testing Different Regions

```bash
# Korean plates
ma-anpr test-api kr_plate.jpg --detector v14_medium_640p_fp32 --ocr v14_medium_fp32 --region kr

# European+ plates
ma-anpr test-api eu_plate.jpg --detector v14_medium_640p_fp32 --ocr v14_medium_fp32 --region eup

# North American plates
ma-anpr test-api na_plate.jpg --detector v14_small_640p_fp32 --ocr v14_small_fp32 --region na

# Chinese plates
ma-anpr test-api cn_plate.jpg --detector v14_medium_640p_fp32 --ocr v14_medium_fp32 --region cn

# Universal (all regions)
ma-anpr test-api mixed_plate.jpg --detector v14_medium_640p_fp32 --ocr v14_medium_fp32 --region univ
```

## Rate Limiting

### Daily Limits
- **Test API**: 1000 requests per day
- **Reset**: Midnight KST (Korea Standard Time / UTC+9)

## Available Models

### Detector Models (API requires v14_ prefix)
- **Sizes**: pico, micro, small, medium, large
- **Resolution**: 640p
- **Precision**: fp32
- **Example**: `v14_medium_640p_fp32`

### OCR Models (API requires v14_ prefix)
- **Sizes**: pico, micro, small, medium, large
- **Precision**: fp32
- **Example**: `v14_medium_fp32`

### Regions
- **kr** - Korean license plates (best for Korean)
- **eup** - European+ license plates (EU countries + additional European countries + Indonesia)
- **na** - North American license plates (USA, Canada)
- **cn** - Chinese license plates
- **univ** - Universal (all regions) - **default, but choose specific region for best accuracy**

## Limitations

**Test API:**
- 1000 requests per day limit
- 10MB maximum image size
- JPEG/PNG formats only

**Licensed Version:**
- Unlimited local requests
- On-premise deployment
- Full access to all models and features

## Getting Started

For production use:
- **Subscribe**: [ANPR Solution](https://www.marearts.com/products/anpr)
- **Contact**: [hello@marearts.com](mailto:hello@marearts.com)