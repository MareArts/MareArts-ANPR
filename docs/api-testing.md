# API Testing Guide

## Test API Overview

MareArts provides a free test API with a daily limit of 1000 requests for evaluation purposes. No license key required for testing.

## Quick Start with CLI

### Basic Testing

```bash
# Test with single image
ma-anpr test-api image.jpg

# Test with multiple images
ma-anpr test-api *.jpg

# Specify custom models
ma-anpr test-api image.jpg --detector v13_small --ocr v13_kr

# Save results to JSON
ma-anpr test-api image.jpg --json results.json

# List available models
ma-anpr test-api --list-models
```

### CLI Options

```bash
ma-anpr test-api --help

Options:
  --detector MODEL     Detection model (default: v13_middle)
  --ocr MODEL         OCR model (default: v13_euplus)
  --json FILE         Save results to JSON file
  --verbose           Show detailed output
  --list-models       List available models
```

## Direct API Testing

### REST API Endpoint

```
https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr
```

### Test Credentials

- **User ID**: `marearts@public`
- **API Key**: `J4K9L2Wory34@G7T1Y8rt-PP83uSSvkV3Z6ioSTR!`

### cURL Example

```bash
curl -X POST https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr \
     -H "Content-Type: image/jpeg" \
     -H "x-api-key: J4K9L2Wory34@G7T1Y8rt-PP83uSSvkV3Z6ioSTR!" \
     -H "user-id: marearts@public" \
     -H "detector_model_version: v13_middle" \
     -H "ocr_model_version: v13_euplus" \
     --data-binary "@./test_image.jpg"
```

### Python Example

```python
import requests
import base64
import json

def test_anpr_api(image_path, detector="v13_middle", ocr="v13_euplus"):
    """Test ANPR API with free credentials"""
    
    url = "https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr"
    
    headers = {
        "Content-Type": "image/jpeg",
        "x-api-key": "J4K9L2Wory34@G7T1Y8rt-PP83uSSvkV3Z6ioSTR!",
        "user-id": "marearts@public",
        "detector_model_version": detector,
        "ocr_model_version": ocr
    }
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    response = requests.post(url, headers=headers, data=image_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# Example usage
if __name__ == "__main__":
    result = test_anpr_api("test_image.jpg")
    print(json.dumps(result, indent=2))
```

### JavaScript/Node.js Example

```javascript
const fs = require('fs');
const axios = require('axios');

async function testANPR(imagePath) {
    const url = 'https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr';
    
    const imageBuffer = fs.readFileSync(imagePath);
    
    const config = {
        headers: {
            'Content-Type': 'image/jpeg',
            'x-api-key': 'J4K9L2Wory34@G7T1Y8rt-PP83uSSvkV3Z6ioSTR!',
            'user-id': 'marearts@public',
            'detector_model_version': 'v13_middle',
            'ocr_model_version': 'v13_euplus'
        }
    };
    
    try {
        const response = await axios.post(url, imageBuffer, config);
        return response.data;
    } catch (error) {
        console.error('API Error:', error.response?.data || error.message);
        throw error;
    }
}

// Usage
testANPR('test_image.jpg')
    .then(result => console.log(JSON.stringify(result, null, 2)))
    .catch(error => console.error(error));
```

## API Response Format

### Successful Response

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
    "ocr_proc_sec": 0.082,
    "status": "success"
}
```

### Error Response

```json
{
    "error": "Invalid image format",
    "status": "error",
    "code": 400
}
```

## Testing Different Regions

### European Plates

```bash
# Using CLI
ma-anpr test-api eu_plate.jpg --ocr v13_euplus

# Using cURL
curl -X POST https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr \
     -H "ocr_model_version: v13_euplus" \
     # ... other headers
```

### Korean Plates

```bash
# Using CLI
ma-anpr test-api kr_plate.jpg --ocr v13_kr

# Using cURL
curl -X POST https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr \
     -H "ocr_model_version: v13_kr" \
     # ... other headers
```

### Chinese Plates

```bash
# Using CLI
ma-anpr test-api cn_plate.jpg --ocr v13_cn

# Using cURL
curl -X POST https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr \
     -H "ocr_model_version: v13_cn" \
     # ... other headers
```

### Universal (Mixed Regions)

```bash
# Using CLI
ma-anpr test-api mixed_plate.jpg --ocr v13_univ

# Using cURL
curl -X POST https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr \
     -H "ocr_model_version: v13_univ" \
     # ... other headers
```

## Batch Testing Script

```python
import os
import glob
import json
from datetime import datetime

def batch_test_images(image_pattern="*.jpg", output_file="test_results.json"):
    """Test multiple images and save results"""
    
    results = []
    images = glob.glob(image_pattern)
    
    print(f"Testing {len(images)} images...")
    
    for image_path in images:
        try:
            result = test_anpr_api(image_path)
            results.append({
                "file": image_path,
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "data": result
            })
            print(f"✓ {image_path}: {len(result['results'])} plates found")
        except Exception as e:
            results.append({
                "file": image_path,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            })
            print(f"✗ {image_path}: {e}")
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    successful = sum(1 for r in results if r['success'])
    print(f"\nSummary: {successful}/{len(images)} successful")
    print(f"Results saved to {output_file}")
    
    return results

# Run batch test
if __name__ == "__main__":
    batch_test_images("test_images/*.jpg")
```

## Performance Testing

```python
import time
import statistics

def performance_test(image_path, iterations=10):
    """Test API performance with multiple iterations"""
    
    times = []
    
    for i in range(iterations):
        start = time.time()
        result = test_anpr_api(image_path)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"Iteration {i+1}: {elapsed:.3f}s")
    
    print(f"\nPerformance Statistics:")
    print(f"Average: {statistics.mean(times):.3f}s")
    print(f"Median: {statistics.median(times):.3f}s")
    print(f"Min: {min(times):.3f}s")
    print(f"Max: {max(times):.3f}s")
    print(f"Std Dev: {statistics.stdev(times):.3f}s")

# Run performance test
performance_test("test_image.jpg", iterations=10)
```

## Rate Limiting

### Daily Limits
- **Test API**: 1000 requests per day
- **Reset Time**: Midnight UTC
- **Rate**: ~40 requests per hour average

### Handling Rate Limits

```python
import time

def test_with_retry(image_path, max_retries=3):
    """Test API with retry logic for rate limits"""
    
    for attempt in range(max_retries):
        try:
            return test_anpr_api(image_path)
        except Exception as e:
            if "rate limit" in str(e).lower():
                wait_time = 60 * (attempt + 1)  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e
    
    raise Exception("Max retries exceeded")
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

## Getting Help

For test API issues:
- Check status: [http://live.marearts.com](http://live.marearts.com)
- Contact: [hello@marearts.com](mailto:hello@marearts.com)

For production license:
- Visit: [ANPR Solution](https://study.marearts.com/p/anpr-lpr-solution.html)