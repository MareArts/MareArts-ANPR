# MareArts ANPR SDK
*Latest Version : 3.1.5

### 🇪🇺🏳️‍🌈 ANPR EU and Plus
Auto Number Plate Recognition for European Union and Plus countries

🦋 **Available Countries:** (We are adding more countries.)
``` 
EU :
🇦🇱 Albania 🇦🇩 Andorra 🇦🇹 Austria 🇧🇪 Belgium 🇧🇦 Bosnia and Herzegovina 
🇧🇬 Bulgaria 🇭🇷 Croatia 🇨🇾 Cyprus 🇨🇿 Czechia 🇩🇰 Denmark 🇫🇮 Finland 
🇫🇷 France 🇩🇪 Germany 🇬🇷 Greece 🇭🇺 Hungary 🇮🇪 Ireland 🇮🇹 Italy 🇱🇮 Liechtenstein 
🇱🇺 Luxembourg 🇲🇹 Malta 🇲🇨 Monaco 🇲🇪 Montenegro 🇳🇱 Netherlands 🇲🇰 North Macedonia 
🇳🇴 Norway 🇵🇱 Poland 🇵🇹 Portugal 🇷🇴 Romania 🇸🇲 San Marino 🇷🇸 Serbia 
🇸🇰 Slovakia 🇸🇮 Slovenia 🇪🇸 Spain 🇸🇪 Sweden 🇨🇭 Switzerland 🇬🇧 United Kingdom 
Plus:
🇮🇩 Indonesia
```

🦋 **Recognisable Characters:**
```python
char_list = [
    "-", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
    "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "d", "i", 
    "m", "o", "Ö", "Ü", "Ć", "Č", "Đ", "Š", "Ž", "П"
]
```
<br><br>
### 🇰🇷 ANPR Korea
한국 자동차 번호판 인식 솔루션

**인식 가능 문자:**
```python
char_list = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
    '가', '강', '거', '경', '고', '광', '구', '기',
    '나', '남', '너', '노', '누',
    '다', '대', '더', '도', '동', '두',
    '라', '러', '로', '루',
    '마', '머', '모', '무', '문',
    '바', '배', '버', '보', '부', '북',
    '사', '산', '서', '세', '소', '수',
    '아', '어', '오', '우', '울', '원', '육', '인',
    '자', '저', '전', '제', '조', '종', '주',
    '천', '충',
    '하', '허', '호'
]
```

<br><br>
### 🪐 Universal 
An integrated model for recognizing license plates from all the countries we support.

<br><br>
## 🔩 Installation

To install the MareArts ANPR package, use the following pip command:

```bash
pip install marearts-anpr
```
If you want to use CUDA version inference, please install the following additional packages:
```bash
pip install onnxruntime-gpu==1.18.1
```

<br><br>
## 🪪 License Key

**For private keys,** please visit [MareArts ANPR Solution](https://study.marearts.com/p/anpr-lpr-solution.html).
For inquiries about private keys, contact us at [hello@marearts.com](mailto:hello@marearts.com).

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
| Model       | File Size | Accuracy | Recall  | F1     |
|-------------|-----------|----------|---------|--------|
| eu          |  ~100mb   | 0.9346   | 0.9346  | 0.9392 |
| euplus      |  ~100mb   | 0.9554   | 0.9554  | 0.9580 |
| kr          |  ~100mb   | 0.9824   | 0.9824  | 0.9873 |
| univ        |  ~100mb   | 0.9626   | 0.9626  | 0.9630 |
| v11_eu          |  ~100mb   | 0.9919   | 0.9919  | 0.9919 |
| v11_euplus      |  ~100mb   | 0.9853   | 0.9853  | 0.9853 |
| v11_kr          |  ~100mb   | 0.9967   | 0.9967  | 0.9967 |
| v11_univ        |  ~100mb   | 0.9953   | 0.9953  | 0.9953 |
* Use model name in OCR code

<br><br>
## 📝 Using SDK
### 🔬 SDK Usage
Try our interactive demo: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/17jRj1xGOGQdLM5MhAMJEBeM5i8cuD4nP?usp=sharing)


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
    user_name = "your_email"
    serial_key = "your_serial_key"
    detector_model_version = "v11_middle" # Options: refer to detector model table
    ocr_model_version = "v11_euplus" # Options: refer to ocr model table

    # MareArts ANPR Detector Inference
    anpr_d = ma_anpr_detector(detector_model_version, user_name, serial_key, conf_thres=0.3, iou_thres=0.5)
    # MareArts ANPR OCR Inference
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
    # user_name, serial_key are already defined
    # anpr_d is also already initiated before
    ocr_model_version = "v11_kr"
    # MareArts ANPR OCR Inference
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
## 🧪 API for testing

### This is for testing purposes
**API key limits:** 1000 requests per day. <br>
**User ID:** `marearts@public` <br>
**X-API-Key:** `J4K9L2Wory34@G7T1Y8rt-PP83uSSvkV3Z6ioSTR!`

### API Call 

To make an API call for ANPR, use the following command: <br>
**Content-Type** : image/jpeg<br>
**x-api-key**: api_key<br>
**user-id**: user-id<br>
**detector_model_version**: Specifies which version of the detector model to use. Refer to version table<br>
**ocr_model_version**: Specifies which version of the OCR model to use. Refer to version table<br>

```bash
#!bin/bash
curl -X POST https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr \
     -H "Content-Type: image/jpeg" \
     -H "x-api-key: api_key" \
     -H "user-id: user-id" \
     -H "detector_model_version: detector_version" \
     -H "ocr_model_version: ocr_version" \
     --data-binary "@./a.jpg"
```


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
## 😎 More Detail
email : hello@marearts.com <br>
home page : https://marearts.com <br>
blog : http://study.marearts.com <br>
subscription : https://study.marearts.com/p/anpr-lpr-solution.html <br>
live test : http://live.marearts.com

<br><br>
🙇🏻‍♂️ Thank you!
