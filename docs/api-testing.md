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

# Specify models
ma-anpr test-api image.jpg --detector v13_small --ocr v13_kr

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
     -H "detector_model_version: v13_middle" \
     -H "ocr_model_version: v13_euplus" \
     --data-binary "@./image.jpg"
```

#### Python Example
```python
import requests
import json

def test_marearts_anpr(image_path):
    url = "https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr"
    
    headers = {
        "Content-Type": "image/jpeg",
        "x-api-key": "J4K9L2Wory34@G7T1Y8rt-PP83uSSvkV3Z6ioSTR!",
        "user-id": "marearts@public",
        "detector_model_version": "v13_middle",
        "ocr_model_version": "v13_euplus"
    }
    
    with open(image_path, 'rb') as f:
        response = requests.post(url, headers=headers, data=f.read())
    
    return response.json()

# Test
result = test_marearts_anpr("test_image.jpg")
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
# European plates
ma-anpr test-api eu_plate.jpg --ocr v13_euplus

# Korean plates
ma-anpr test-api kr_plate.jpg --ocr v13_kr

# Chinese plates
ma-anpr test-api cn_plate.jpg --ocr v13_cn

# Universal (auto-detect)
ma-anpr test-api mixed_plate.jpg --ocr v13_univ
```

## Rate Limiting

### Daily Limits
- **Test API**: 1000 requests per day
- **Reset**: Midnight UTC

### Retry Logic
```python
import time

def test_with_retry(image_path, max_retries=3):
    for attempt in range(max_retries):
        try:
            return test_marearts_anpr(image_path)
        except Exception as e:
            if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                wait_time = 60 * (attempt + 1)
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e
```

## Limitations

**Test API:**
- 1000 requests per day
- 10MB maximum image size
- JPEG/PNG formats only

**Full License:**
- Unlimited requests
- All features available
- On-premise deployment (offline)

## Getting Started

For production use:
- **Purchase**: [ANPR Solution](https://study.marearts.com/p/anpr-lpr-solution.html)
- **Contact**: [hello@marearts.com](mailto:hello@marearts.com)