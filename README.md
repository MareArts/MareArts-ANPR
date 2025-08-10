# MareArts ANPR SDK

[![PyPI version](https://badge.fury.io/py/marearts-anpr.svg)](https://badge.fury.io/py/marearts-anpr)
[![Python versions](https://img.shields.io/pypi/pyversions/marearts-anpr.svg)](https://pypi.org/project/marearts-anpr/)
[![Downloads](https://pepy.tech/badge/marearts-anpr)](https://pepy.tech/project/marearts-anpr)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](https://study.marearts.com/p/anpr-lpr-solution.html)
[![GitHub stars](https://img.shields.io/github/stars/marearts/marearts-anpr.svg)](https://github.com/marearts/marearts-anpr/stargazers)
[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen.svg)](http://live.marearts.com)


**Enterprise-grade** Automatic Number Plate Recognition (ANPR) SDK supporting **European Union**, **Korea**, **China**, and **Universal** license plates with **99%+ accuracy** and **GPU acceleration**.

## ✨ Key Features

- 🚗 **Multi-Region Support**: EU, Korea, China, and Universal license plates
- ⚡ **High Performance**: Optimized C++ core with Python bindings + GPU acceleration
- 🎯 **High Accuracy**: Up to 99.4% accuracy with latest models
- 🛡️ **Enterprise Security**: Military-grade protection with license validation
- 🚀 **GPU Acceleration**: Significantly faster processing with CUDA/DirectML support
- 🔧 **Easy Integration**: Simple Python API with comprehensive examples
- 🐳 **Docker Ready**: Complete Docker deployment examples
- 🌐 **API Server**: REST API examples for production deployment
- 📱 **Multiple Formats**: Support for CV2, PIL, and file inputs
- 🌍 **Multi-Platform**: Linux, Windows, macOS with smart provider detection

## 📁 Repository Structure

This repository contains customer examples, documentation, and usage guides for the MareArts ANPR SDK.

### Directory Structure
```
marearts-anpr/
├── API_docker_example/     # Docker API server example
├── example_code/           # Basic and advanced usage examples  
├── sample_images/          # Test images for different regions
├── md_images/              # Documentation screenshots
├── etc/                    # Additional resources (fonts, utilities)
└── README.md               # This documentation
```


## 📑 Table of Contents
- [🌍 Regional Support](#-regional-support)
- [🔩 Installation](#-installation)
- [🪪 License Key](#-license-key)
- [🤖 Live Test](#-live-test)
- [📺 ANPR Result Videos](#-anpr-result-videos)
- [🚂 Model Version](#-model-version)
- [📝 Using SDK](#-using-sdk)
- [🧪 API for testing](#-api-for-testing)
- [⚓️ Create MareArts ANPR API Docker](#️-create-marearts-anpr-api-docker)
- [⚙️ example_code](#️-example_code)
- [📋 Software Licensing FAQ](#-software-licensing-faq)
- [😎 More Detail](#-more-detail)

## 🌍 Regional Support

MareArts ANPR provides comprehensive license plate recognition across multiple regions with specialized models optimized for each area.

### 🇪🇺 European Union & Plus Countries

**Supported Countries:**

| A-F | G-P | R-Z | Plus |
|-----|-----|-----|------|
| 🇦🇱 Albania | 🇩🇪 Germany | 🇷🇴 Romania | 🇮🇩 Indonesia |
| 🇦🇩 Andorra | 🇬🇷 Greece | 🇸🇲 San Marino | |
| 🇦🇹 Austria | 🇭🇺 Hungary | 🇷🇸 Serbia | |
| 🇧🇪 Belgium | 🇮🇪 Ireland | 🇸🇰 Slovakia | |
| 🇧🇦 Bosnia and Herzegovina | 🇮🇹 Italy | 🇸🇮 Slovenia | |
| 🇧🇬 Bulgaria | 🇱🇮 Liechtenstein | 🇪🇸 Spain | |
| 🇭🇷 Croatia | 🇱🇺 Luxembourg | 🇸🇪 Sweden | |
| 🇨🇾 Cyprus | 🇲🇹 Malta | 🇨🇭 Switzerland | |
| 🇨🇿 Czechia | 🇲🇨 Monaco | 🇬🇧 United Kingdom | |
| 🇩🇰 Denmark | 🇲🇪 Montenegro | | |
| 🇫🇮 Finland | 🇳🇱 Netherlands | | |
| 🇫🇷 France | 🇲🇰 North Macedonia | | |
| | 🇳🇴 Norway | | |
| | 🇵🇱 Poland | | |
| | 🇵🇹 Portugal | | |

**Character Support (50 characters):**
```python
["-", ".", "0-9", "A-Z", "a", "d", "i", "m", "o", "Ö", "Ü", "Ć", "Č", "Đ", "Š", "Ž", "П"]
```

### 🇰🇷 Korea Support
한국 자동차 번호판 인식 솔루션

**Character Support (71 characters):**
```python
['0-9', '가', '강', '거', '견', '경', '고', '곡', '공', '광', '교', '구', '국', '군', '금', '급', '기',
 '나', '남', '너', '노', '녹', '논', '누', '다', '단', '대', '더', '도', '동', '두',
 '라', '러', '렬', '령', '례', '로', '루', '륜', '률', '린', '림', '립',
 '마', '머', '면', '명', '모', '목', '무', '문', '바', '배', '백', '버', '병', '보', '봉', '부', '북', '빙',
 '사', '산', '삼', '상', '서', '성', '세', '소', '수', '순', '신',
 '아', '안', '양', '어', '역', '연', '영', '예', '오', '완', '왕', '외', '용', '우', '운', '울', '원', '월', '위', '유', '육', '은', '이', '익', '인', '일', '임',
 '자', '작', '장', '재', '저', '적', '전', '정', '제', '조', '종', '주', '진',
 '차', '창', '채', '천', '철', '청', '초', '춘', '출', '충', '태', '택', '토', '통', '특',
 '파', '팔', '평', '포', '표', '하', '학', '한', '함', '합', '해', '행', '허', '헌', '협', '형', '호', '홍',
 '화', '황', '흑', '흥']
```

### 🇨🇳 China Support
中国车牌识别解决方案

**Character Support:**
```python
['0-9', 'A-Z', '·', '云', '京', '冀', '吉', '宁', '川', '挂', '新', '晋', '桂',
 '沪', '津', '浙', '渝', '港', '湘', '澳', '琼', '甘', '皖',
 '粤', '苏', '蒙', '藏', '豫', '贵', '赣', '辽', '鄂', '闽', '陕', '青', '鲁', '黑']
```

### 🪐 Universal Model
An integrated model for recognizing license plates from all supported regions with automatic region detection.

<br><br>
## 🔩 Installation

### 💻 CPU Installation (Universal)
```bash
# Lightweight installation for all platforms
pip install marearts-anpr
```

### 🚀 GPU Installation (Recommended for Production)
```bash
# NVIDIA CUDA GPU (Linux/Windows) - Significantly faster
pip install marearts-anpr[gpu]

# Windows GPU (AMD/Intel/NVIDIA) - Faster processing  
pip install marearts-anpr[directml]

# All GPU support (maximum compatibility)
pip install marearts-anpr[all-gpu]

# Development dependencies
pip install marearts-anpr[dev]
```

### 📊 GPU Acceleration
The SDK features smart provider detection that automatically uses the best available hardware. GPU acceleration provides significant performance improvements over CPU processing.

### Installation Recommendations
- **Production High-Throughput**: `pip install marearts-anpr[gpu]` - Best for NVIDIA GPU systems
- **Windows Development**: `pip install marearts-anpr[directml]` - Works with any GPU (AMD/Intel/NVIDIA)
- **CPU/Cloud Deployment**: `pip install marearts-anpr` - Lightweight, no GPU dependencies
- **Maximum Compatibility**: `pip install marearts-anpr[all-gpu]` - Includes all GPU support options

### System Requirements

- **Python**: 3.9, 3.10, 3.11, or 3.12
- **Operating System**: Linux (x86_64, ARM64), macOS, Windows
- **Memory**: Minimum 4GB RAM (8GB recommended for GPU)
- **Storage**: ~500MB for model files
- **GPU** (optional): NVIDIA CUDA or DirectML compatible

<br><br>
## 🪪 License Key

**For private keys,** please visit [MareArts ANPR Solution](https://study.marearts.com/p/anpr-lpr-solution.html).
For inquiries about private keys, contact us at [hello@marearts.com](mailto:hello@marearts.com).

<br><br>
## 🚀 Quick Start

### Environment Setup (Required)
```bash
# Set license credentials (recommended)
export MAREARTS_ANPR_USERNAME="your-email@domain.com"
export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"
```

### Basic Usage
```python
# pip install marearts-anpr[gpu]  # For best performance
from marearts_anpr import marearts_anpr_from_image_file
from marearts_anpr import ma_anpr_detector, ma_anpr_ocr

# Initialize with your credentials
user_name = "your_email"
serial_key = "your_serial_key"

# Optional: Load from environment variables if set
# export MAREARTS_ANPR_USERNAME="your-email@domain.com"
# export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"
# import os
# user_name = os.getenv("MAREARTS_ANPR_USERNAME", user_name)
# serial_key = os.getenv("MAREARTS_ANPR_SERIAL_KEY", serial_key)

detector = ma_anpr_detector("v13_middle", user_name, serial_key)
ocr = ma_anpr_ocr("v13_euplus", user_name, serial_key)

# Process image
result = marearts_anpr_from_image_file(detector, ocr, "image.jpg")
print(result)
# Expected: {'results': [{'ocr': 'ABC123', 'ocr_conf': 99, ...}], 'ltrb_proc_sec': 0.08, 'ocr_proc_sec': 0.05}
```

### CLI Usage
```bash
# Direct image processing
ma-anpr image.jpg

# Test without credentials (1000 requests/day)
ma-anpr test-api image.jpg

# Validate license
ma-anpr validate

# List available models
ma-anpr models

# GPU information
ma-anpr gpu-info
```

<br><br>
## 🤖 Live Test
[MareArts 🎬 Live](http://live.marearts.com)

<br><br>
## 📺 ANPR Result Videos
[Check here](https://www.youtube.com/playlist?list=PLvX6vpRszMkxJBJf4EjQ5VCnmkjfE59-J) to see the license plate recognition results in YouTube videos.

<br><br>
## 🚂 Model Version
### ANPR Detector Model Version

| Model | File Size | Precision | Recall | F1 Score | Avg Detection Time (s) |
|------------|-----------|-----------|---------|----------|------------------------|
| v10_small | 38MB | 0.9852 | 0.9694 | 0.9716 | 0.0468 |
| v10_middle | 79MB | 0.9836 | 0.9680 | 0.9701 | 0.0992 |
| v10_large | 125MB | 0.9858 | 0.9709 | 0.9731 | 0.2307 |
| v11_small | 38MB | 0.9791 | 0.9849 | 0.9779 | 0.0492 |
| v11_middle | 79MB | 0.9799 | 0.9866 | 0.9793 | 0.0938 |
| v11_large | 125MB | 0.9824 | 0.9892 | 0.9823 | 0.1561 |
| v13_nano | 14MB | 0.9657 | 0.9826 | 0.9676 | 0.0356 | 
| v13_small | 49MB | 0.9632 | 0.9920 | 0.9715 | 0.0657 | 
| v13_middle | 103MB | 0.9634 | 0.9940 | 0.9725 | 0.1629 |
| v13_large | 129MB | 0.9642 | 0.9936 | 0.9729 | 0.2053 |

### Recommendations

* 🎯 **Best Precision**: v10_large (0.9858)
* 📈 **Best Recall**: v13_middle (0.9940)
* 🥇 **Best F1 Score**: v11_large (0.9823)
* ⚡ **Fastest Model**: v13_nano (0.0356s)

### Notes
* Speed test is based on i7-9800X 3.8GHz
* Last Update: 2025-03-31 15:26:43
* Please use the latest version of marearts-anpr
* **Use model name in detector code**



### ANPR OCR Model Version
| Model | Region | Size | Accuracy | Character Accuracy | Mean Confidence | Processing Time (s) | Recommendation |
|-------|---------|------|----------|-------------------|-----------------|---------------------|----------------|
| eu | EU | 293MB | 1.0000 | 1.0000 | 96.9071 | 0.0808 | 🎯 |
| euplus | EU Plus | 146MB | 0.9432 | 0.9876 | 94.0371 | 0.0841 | |
| kr | Korea | 146MB | 0.9822 | 0.9967 | 97.4243 | 0.0861 | |
| univ | Universal | 146MB | 0.9348 | 0.9877 | 94.4448 | 0.0862 | |
| v11_eu | EU | 293MB | 0.9900 | 0.9980 | 97.9573 | 0.0830 | 🔍 |
| v11_euplus | EU Plus | 146MB | 0.9822 | 0.9965 | 97.6391 | 0.0823 | 🎯 |
| v11_kr | Korea | 146MB | 0.9938 | 0.9991 | 98.5033 | 0.0852 | 🎯 |
| v11_univ | Universal | 146MB | 0.9600 | 0.9941 | 97.7669 | 0.0845 | ⚡ |
| v13_eu | EU | 295MB | 0.9504 | 0.9860 | 97.4215 | 0.0822 | |
| v13_kr | Korea | 147MB | 0.9721 | 0.9951 | 97.0080 | 0.0855 | |
| v13_cn | China | 147MB | 0.9657 | 0.9932 | 97.7589 | 0.0858 | 🎯 |
| v13_euplus | EU Plus | 147MB | 0.9617 | 0.9901 | 97.6953 | 0.0822 | ⚡ |
| v13_univ | Universal | 147MB | 0.9829 | 0.9963 | 98.6056 | 0.0846 | 🎯 |

### Recommendation Icons
* 🎯 Best Accuracy
* 📝 Best Character Accuracy
* 🔍 Best Confidence
* ⚡ Fastest Model

### Notes
* Speed test is based on i7-9800X 3.8GHz
* Last Update: 2025-04-04 21:38:05
* Please use the latest version of marearts-anpr
* **Use model name in ocr code**

<br><br>
## 🛡️ Enterprise Security

### Security Features
- 🔒 **License Protection**: Military-grade license validation system
- 🚫 **Direct Access Prevention**: Low-level classes protected from bypass attempts
- 🔐 **Environment Variables**: Secure credential management (no config files)
- ⚠️ **Generic Error Messages**: No sensitive information leakage to potential attackers
- 🔄 **Dynamic Validation**: Periodic license state verification

### Credential Management
```bash
# Secure environment variable setup (recommended)
export MAREARTS_ANPR_USERNAME="your-email@domain.com"  
export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"

# Validate credentials
ma-anpr validate
```

### Security Best Practices
- ✅ Use environment variables for credentials
- ✅ Never hardcode license keys in source code
- ✅ Validate license before production deployment
- ✅ Monitor for licensing compliance

<br><br>
## 📝 Using SDK
### 🔬 SDK Usage
Try our interactive demo: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zZlueTZ1Le73yOQ3mdJFONxcebKyCgr-?usp=sharing)


Here's an example of how to use the updated SDK:

```python
# pip install marearts-anpr
import cv2
from PIL import Image
from marearts_anpr import ma_anpr_detector
from marearts_anpr import ma_anpr_ocr
from marearts_anpr import marearts_anpr_from_pil
from marearts_anpr import marearts_anpr_from_image_file
from marearts_anpr import marearts_anpr_from_cv2

if __name__ == '__main__':
    
    #################################
    ## Initiate MareArts ANPR
    print("EU ANPR")
    
    # Initialize with your credentials
    user_name = "your_email"
    serial_key = "your_serial_key"
    
    # Optional: Load from environment variables if set
    # export MAREARTS_ANPR_USERNAME="your-email@domain.com"
    # export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"
    # import os
    # user_name = os.getenv("MAREARTS_ANPR_USERNAME", user_name)
    # serial_key = os.getenv("MAREARTS_ANPR_SERIAL_KEY", serial_key)
    
    detector_model_version = "v13_middle" # Latest v13 series recommended
    ocr_model_version = "v13_euplus" # Latest v13 series recommended

    # MareArts ANPR Detector Inference (with GPU acceleration)
    anpr_d = ma_anpr_detector(detector_model_version, user_name, serial_key, conf_thres=0.3, iou_thres=0.5)
    # MareArts ANPR OCR Inference (with GPU acceleration)
    anpr_r = ma_anpr_ocr(ocr_model_version, user_name, serial_key)
    #################################

    #################################
    # Routine Task 1 - Predict from File
    image_path = './sample_images/eu_test1.jpg'
    output = marearts_anpr_from_image_file(anpr_d, anpr_r, image_path)
    print(output)

    # Routine Task 2 - Predict from cv2
    img = cv2.imread(image_path)
    output = marearts_anpr_from_cv2(anpr_d, anpr_r, img)
    print(output)

    # Routine Task 3 - Predict from Pillow
    pil_img = Image.open(image_path)
    output = marearts_anpr_from_pil(anpr_d, anpr_r, pil_img)
    print(output)
    #################################


    #################################
    ## Initiate MareArts ANPR for Korea
    print("ANPR Korean")
    # user_name, serial_key are already defined (or loaded from environment)
    # anpr_d is also already initiated before
    ocr_model_version = "v13_kr" # Latest v13 series recommended
    # MareArts ANPR OCR Inference (with GPU acceleration)
    anpr_r = ma_anpr_ocr(ocr_model_version, user_name, serial_key)

    #################################
    # Routine Task 1 - Predict from File
    image_path = './sample_images/kr_test2.jpg'
    output = marearts_anpr_from_image_file(anpr_d, anpr_r, image_path)
    print(output)

    # Routine Task 2 - Predict from cv2
    img = cv2.imread(image_path)
    output = marearts_anpr_from_cv2(anpr_d, anpr_r, img)
    print(output)

    # Routine Task 3 - Predict from Pillow
    pil_img = Image.open(image_path)
    output = marearts_anpr_from_pil(anpr_d, anpr_r, pil_img)
    print(output)
    #################################
```
Please refer to the **advanced.py** code in the **./example_code**  folder. This file demonstrates how to implement the ma_anpr_detector and ma_anpr_ocr separately.

<br><br>
### 🔬 Returns
The output from the ANPR will be similar to:

```python
{
    'results': [
        {'ocr': 'SL593LM', 'ocr_conf': 99, 'ltrb': [819, 628, 1085, 694], 'ltrb_conf': 90}
        ], 
    'ltrb_proc_sec': 0.22,
    'ocr_proc_sec': 0.15
}
```
```python
{
    'results': [
        {'ocr': '123가4568', 'ocr_conf': 99, 'ltrb': [181, 48, 789, 186], 'ltrb_conf': 83}, 
        {'ocr': '123가4568', 'ocr_conf': 99, 'ltrb': [154, 413, 774, 557], 'ltrb_conf': 82}, 
        {'ocr': '123가4568', 'ocr_conf': 99, 'ltrb': [154, 601, 763, 746], 'ltrb_conf': 80}, 
        {'ocr': '123가4568', 'ocr_conf': 99, 'ltrb': [156, 217, 773, 369], 'ltrb_conf': 80}
        ],
    'ltrb_proc_sec': 0.23,
    'ocr_proc_sec': 0.6
}
```

- **Results:** Contains OCR text, probabilities, and detection coordinate(left, top, right, bottom).
- **Processing Speeds:** Provided for license plate detection and OCR.

<br><br>
## 🧪 API for Testing

**Daily limit:** 1000 requests

### Quick Test via CLI (Recommended)

```bash
# Test with an image using default models
ma-anpr test-api image.jpg

# Specify custom models
ma-anpr test-api image.jpg --detector v13_small --ocr v13_kr

# Process multiple images
ma-anpr test-api *.jpg

# List available models
ma-anpr test-api --list-models

# Save results to JSON
ma-anpr test-api image.jpg --json results.json
```

### Direct API Call (Advanced)

<details>
<summary>Click to see API details</summary>

**Test Credentials:**
- **User ID:** `marearts@public`
- **API Key:** `J4K9L2Wory34@G7T1Y8rt-PP83uSSvkV3Z6ioSTR!`

```bash
curl -X POST https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr \
     -H "Content-Type: image/jpeg" \
     -H "x-api-key: J4K9L2Wory34@G7T1Y8rt-PP83uSSvkV3Z6ioSTR!" \
     -H "user-id: marearts@public" \
     -H "detector_model_version: v13_middle" \
     -H "ocr_model_version: v13_euplus" \
     --data-binary "@./image.jpg"
```

</details>


<br><br>
## ⚓️ Create MareArts ANPR API Docker
Please refer to **./API_docker_example**  folder. 
```bash
API_docker_example
│
├── api_call.sh           # Shell script to make API calls to the MareArts ANPR application.
├── app.py                # Python script containing the MareArts ANPR application.
├── build_image.sh        # Shell script to build the Docker image from the Dockerfile.
├── Dockerfile            # Dockerfile containing instructions for building the Docker image.
├── request.py            # Python script to send requests to the MareArts ANPR API server.
├── requirements.txt      # Contains a list of Python packages that the app requires.
└── run_container.sh      # Shell script to run the Docker container from the built image.
```

<br><br>
## ⚙️ example_code

**bg_subtraction.py** - Motion detection with OpenCV
- Detects moving objects in video
- Adjustable sensitivity and object size

**basic.py** - Easy license plate recognition
- Uses MareArts ANPR SDK with simple implementation

**advance.py** - Advanced license plate recognition
- Direct control of detection and OCR steps
- Run detection and OCR separately for better control


<br><br>
## ❓ Frequently Asked Questions (FAQ)

### 🛠️ Technical Questions

#### Q: Do I need an internet connection to use the software?
**A:** No, the software works offline after initial setup. Internet is only needed for:
- Initial model download
- Checking/downloading model updates
- Without internet, SDK uses existing downloaded model

#### Q: What's new in the latest version?
**A:** Major enterprise improvements:
- 🛡️ **Enterprise Security**: Military-grade license protection
- 🚀 **GPU Acceleration**: Significantly faster with smart provider detection  
- 🔐 **Environment Variables**: Secure credential management
- 💻 **CLI Interface**: `ma-anpr` command-line tool
- 🌍 **Multi-Platform**: Professional installation variants

#### Q: How do I get GPU acceleration?
**A:** Install the appropriate GPU variant:
- **NVIDIA GPU**: `pip install marearts-anpr[gpu]` (Best performance)
- **Windows GPU**: `pip install marearts-anpr[directml]` (Good performance)
- **All GPUs**: `pip install marearts-anpr[all-gpu]`

#### Q: How do I set up credentials securely?
**A:** Use environment variables:
```bash
export MAREARTS_ANPR_USERNAME="your-email@domain.com"
export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"
ma-anpr validate  # Test credentials
```

### 📋 Licensing & Usage

#### Q: What types of licenses are available?
**A:** Three license types are available:
- **Monthly licenses** - Need renewal every month
- **Yearly licenses** - Need renewal every year  
- **Lifetime licenses** - No expiration, use indefinitely

#### Q: Can I use my license on multiple computers?
**A:** Yes! All licenses have no limits on the number of computers. You can use them on multiple computers simultaneously.

#### Q: How does license renewal work?
**A:** 
- **Monthly/Yearly licenses**: Must be renewed before expiration
- **Lifetime licenses**: No expiration, use indefinitely

### 💳 Billing & Refunds

#### Q: What is your refund policy?
**A:** Refunds are only available when a license key has not been issued. However, subscription cancellation is possible at any time.

#### Q: Can I cancel my subscription anytime?
**A:** Yes, you can cancel your subscription at any time, though refunds are only available if the license key hasn't been issued yet.

### 🔒 Service Continuity

#### Q: What happens if the service discontinues?
**A:** We commit to either:
- Open-sourcing the code, or
- Providing lifetime licenses to active users

### 📞 Support

#### Q: How can I get help?
**A:** Contact our support team at [hello@marearts.com](mailto:hello@marearts.com) for setup, licensing, or technical issues.

<br><br>
## 📞 Support & Resources

| Resource | Link |
|----------|------|
| 📧 **Contact** | [hello@marearts.com](mailto:hello@marearts.com) |
| 🏠 **Homepage** | [https://marearts.com](https://marearts.com) |
| 📚 **Blog** | [http://study.marearts.com](http://study.marearts.com) |
| 💳 **Subscription** | [ANPR Solution](https://study.marearts.com/p/anpr-lpr-solution.html) |
| 🎮 **Live Demo** | [http://live.marearts.com](http://live.marearts.com) |
| 📺 **Video Examples** | [YouTube Playlist](https://www.youtube.com/playlist?list=PLvX6vpRszMkxJBJf4EjQ5VCnmkjfE59-J) |
| 🧪 **Colab Demo** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zZlueTZ1Le73yOQ3mdJFONxcebKyCgr-?usp=sharing) |

## 📜 License

This software is proprietary and protected by copyright. Use requires a valid license key from MareArts.

© 2024 MareArts. All rights reserved.


---

<div align="center">

**Made with ❤️ by [MareArts](https://marearts.com)**

🙇🏻‍♂️ Thank you for using MareArts ANPR!

</div>
