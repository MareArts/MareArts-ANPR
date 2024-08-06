# MareArts ANPR SDK


### 🇪🇺 ANPR EU (European Union)
Auto Number Plate Recognition for EU countries

🦋 **Available Countries:** (We are adding more countries.)
``` 
🇦🇱 Albania  🇨🇿 Czechia  🇦🇩 Andorra  🇩🇰 Denmark  🇦🇹 Austria  🇫🇮 Finland
🇧🇪 Belgium  🇫🇷 France   🇧🇦 Bosnia and Herzegovina  
🇩🇪 Germany  🇧🇬 Bulgaria 🇬🇷 Greece   🇭🇷 Croatia  🇭🇺 Hungary  🇨🇾 Cyprus   🇮🇪 Ireland
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
## 🔩 Installation

To install the MareArts ANPR package, use the following pip command:

```bash
pip install marearts-anpr
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
## 📝 Using SDK
### 🔬 SDK Usage
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
    detector_model_version = "middle" # Options: not yet
    ocr_model_version = "eu" # Options: "kr"

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
    ocr_model_version = "kr"
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

### API Call for EU

To make an API call for EU ANPR, use the following command:

```bash
#!bin/bash
curl -X POST https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr_eu \
     -H "Content-Type: image/jpeg" \
     -H "x-api-key: api-key" \
     -H "user-id: user-id" \
     --data-binary "@./path/upload.jpg"
```

### API Call for Korea

To make an API call for Korean ANPR, use the following command:

```bash
#!bin/bash
curl -X POST https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr \
     -H "Content-Type: image/jpeg" \
     -H "x-api-key: api-key" \
     -H "user-id: user-id" \
     --data-binary "@./path/upload.jpg"
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
