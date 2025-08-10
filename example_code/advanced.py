# pip install marearts-anpr
import cv2
from PIL import Image
from marearts_anpr_so import ma_anpr_detector
from marearts_anpr_so import ma_anpr_ocr
import time 

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

    # Options: middle, v10_small, v10_middle, more detail refer to version table
    detector_model_version = "middle" 
    # Options: eu, kr, more detail refer to version table
    ocr_model_version = "eu" 

    # MareArts ANPR Detector Inference
    anpr_d = ma_anpr_detector(detector_model_version, user_name, serial_key, conf_thres=0.3, iou_thres=0.5)
    # MareArts ANPR OCR Inference
    anpr_r = ma_anpr_ocr(ocr_model_version, user_name, serial_key)
    #################################


    #################################
    # Routine Task 1 - Predict from File
    image_path = './sample_images/eu-a.jpg'
    # Routine Task 2 - Predict from cv2
    img = cv2.imread(image_path)


    start_time = time.time()
    #marearts anpr detector
    detections = anpr_d.detector(img)
    ltrb_time = time.time() - start_time

    results = []
    ocr_time = 0
    for box_info in detections:
        # Crop image
        l, t, r, b = box_info['box']
        crop_img = img[int(t):int(b), int(l):int(r)]

        if crop_img.size == 0:
            continue

        # Convert to PIL Image
        pil_img = Image.fromarray(crop_img)
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert(mode="RGB")

        start_time = time.time()
        #marearts anpr ocr
        ocr_result = anpr_r.predict(pil_img)
        ocr_time += time.time() - start_time

        # Append results
        results.append({
            "ocr": ocr_result[0],
            "ocr_conf": ocr_result[1],
            "ltrb": [int(l), int(t), int(r), int(b)],
            "ltrb_conf": int(box_info['score'] * 100)
        })

    output = { "results": results, "ltrb_proc_sec": round(ltrb_time, 2), "ocr_proc_sec": round(ocr_time, 2)}
    print(output)
    #################################