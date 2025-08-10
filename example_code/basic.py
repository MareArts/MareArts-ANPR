# pip install marearts-anpr
import cv2
from PIL import Image
from marearts_anpr_so import ma_anpr_detector
from marearts_anpr_so import ma_anpr_ocr
from marearts_anpr_so import marearts_anpr_from_pil
from marearts_anpr_so import marearts_anpr_from_image_file
from marearts_anpr_so import marearts_anpr_from_cv2

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
    image_path = './sample_images/kr-a.jpg'
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