# pip install marearts-anpr
import cv2
from PIL import Image
from marearts_anpr import ma_anpr_detector_v14
from marearts_anpr import ma_anpr_ocr_v14
from marearts_anpr import marearts_anpr_from_pil
from marearts_anpr import marearts_anpr_from_image_file
from marearts_anpr import marearts_anpr_from_cv2

if __name__ == '__main__':
    
    #################################
    ## Initiate MareArts ANPR V14
    print("MareArts ANPR V14 - Multi-Region Example")
    
    # CREDENTIALS - Choose one:
    # Method 1: Hardcode (edit below)
    user_name = "your_email"
    serial_key = "your_serial_key"
    signature = "your_signature"
    
    # Method 2: Auto-load from ma-anpr config
    if user_name == "your_email":
        import os
        from pathlib import Path
        
        def load_credentials():
            user = os.getenv('MAREARTS_ANPR_USERNAME')
            key = os.getenv('MAREARTS_ANPR_SERIAL_KEY')
            sig = os.getenv('MAREARTS_ANPR_SIGNATURE')
            
            if not all([user, key, sig]):
                config = Path.home() / '.marearts' / '.marearts_env'
                if config.exists():
                    for line in open(config):
                        if 'USERNAME=' in line: user = line.split('=')[1].strip().strip('"')
                        elif 'SERIAL_KEY=' in line: key = line.split('=')[1].strip().strip('"')
                        elif 'SIGNATURE=' in line: sig = line.split('=')[1].strip().strip('"')
            return user, key, sig
        
        user_name, serial_key, signature = load_credentials()
    
    if not all([user_name, serial_key, signature]) or user_name == "your_email":
        print("❌ Edit credentials above OR run: ma-anpr config")
        exit(1)
    
    # V14 Detector models: pico_640p_fp32, micro_640p_fp32, small_640p_fp32, medium_640p_fp32, large_640p_fp32
    detector_model = "medium_640p_fp32"
    # V14 OCR models: pico_fp32, micro_fp32, small_fp32, medium_fp32, large_fp32
    ocr_model = "medium_fp32"
    # Backend: cpu, cuda, directml (default: cpu)
    backend = "cpu"
    
    # Initial region (kr, eup, na, cn, univ)
    region = "kr"  # Change to your region

    # Initialize V14 Detector
    anpr_d = ma_anpr_detector_v14(
        detector_model, 
        user_name, 
        serial_key, 
        signature,
        backend=backend,
        conf_thres=0.25, 
        iou_thres=0.5
    )
    
    # Initialize V14 OCR with regional vocabulary
    # Regions: kr (Korean), eup (Europe+), na (North America), cn (China), univ (Universal)
    anpr_r = ma_anpr_ocr_v14(ocr_model, region, user_name, serial_key, signature)
    
    # 💡 Dynamic region switching (no reload needed!):
    # anpr_r.set_region('eup')   # Switch to European plates
    # anpr_r.set_region('kr')    # Switch to Korean plates
    # anpr_r.set_region('na')    # Switch to North American plates
    # anpr_r.set_region('cn')    # Switch to Chinese plates
    # anpr_r.set_region('univ')  # Switch to Universal
    # Saves ~180MB memory vs creating multiple OCR instances!
    #################################

    #################################
    # Example 1: Process Images
    print("\n=== Processing European Plate ===")
    image_path = './sample_images/eu-a.jpg'
    
    # Method 1: From file
    output = marearts_anpr_from_image_file(anpr_d, anpr_r, image_path)
    print("From file:", output)

    # Method 2: From OpenCV
    img = cv2.imread(image_path)
    output = marearts_anpr_from_cv2(anpr_d, anpr_r, img)
    print("From cv2:", output)

    # Method 3: From Pillow
    pil_img = Image.open(image_path)
    output = marearts_anpr_from_pil(anpr_d, anpr_r, pil_img)
    print("From PIL:", output)
    #################################


    #################################
    # Example 2: Korean Plates (using set_region for efficiency)
    print("\n=== Processing Korean Plate ===")
    
    # NEW (>3.7.0): Use set_region() instead of creating new OCR instance
    # This saves ~180MB memory and is instant!
    anpr_r.set_region('kr')
    
    image_path = './sample_images/kr-a.jpg'
    
    # Method 1: From file
    output = marearts_anpr_from_image_file(anpr_d, anpr_r, image_path)
    print("From file:", output)

    # Method 2: From OpenCV
    img = cv2.imread(image_path)
    output = marearts_anpr_from_cv2(anpr_d, anpr_r, img)
    print("From cv2:", output)

    # Method 3: From Pillow
    pil_img = Image.open(image_path)
    output = marearts_anpr_from_pil(anpr_d, anpr_r, pil_img)
    print("From PIL:", output)
    #################################
    
    
    #################################
    # Example 3: Batch Processing (V14 Feature)
    print("\n=== Example 3: Batch Processing ===")
    
    # Collect multiple plate images for batch processing
    img_kr = cv2.imread('./sample_images/kr-a.jpg')
    img_eu = cv2.imread('./sample_images/eu-a.jpg')
    
    # Switch to universal region for mixed plates
    anpr_r.set_region('univ')
    
    # Convert to PIL
    pil_kr = Image.fromarray(cv2.cvtColor(img_kr, cv2.COLOR_BGR2RGB))
    pil_eu = Image.fromarray(cv2.cvtColor(img_eu, cv2.COLOR_BGR2RGB))
    
    # Detect plates
    detections_kr = anpr_d.detector(img_kr)
    detections_eu = anpr_d.detector(img_eu)
    
    # Collect plate crops
    plate_images = []
    if detections_kr:
        bbox = detections_kr[0]['bbox']
        l, t, r, b = bbox[0], bbox[1], bbox[2], bbox[3]
        crop = img_kr[int(t):int(b), int(l):int(r)]
        plate_images.append(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)))

    if detections_eu:
        bbox = detections_eu[0]['bbox']
        l, t, r, b = bbox[0], bbox[1], bbox[2], bbox[3]
        crop = img_eu[int(t):int(b), int(l):int(r)]
        plate_images.append(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)))
    
    if len(plate_images) > 1:
        # V14 OCR supports batch processing!
        batch_results = anpr_r.predict(plate_images)  # Pass list of images
        print(f"Batch processed {len(plate_images)} plates:")
        for i, (text, conf) in enumerate(batch_results):
            print(f"  Plate {i+1}: {text} ({conf}%)")
    #################################
    
    print("\n✅ Demo complete! Single OCR instance processed both EU and Korean plates.")