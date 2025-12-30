# pip install marearts-anpr
import cv2
from PIL import Image
from marearts_anpr import ma_anpr_detector_v14
from marearts_anpr import ma_anpr_ocr_v14
import time 

if __name__ == '__main__':
    
    #################################
    ## Initiate MareArts ANPR V14
    print("MareArts ANPR V14 - Advanced Example with Manual Processing")
    
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
    
    # Initialize V14 OCR with Europe+ region
    # Regions: kr (Korean), eup (Europe+), na (North America), cn (China), univ (Universal)
    anpr_r = ma_anpr_ocr_v14(ocr_model, "eup", user_name, serial_key, signature)
    #################################


    #################################
    # Manual Detection and OCR Processing with Timing
    image_path = './sample_images/eu-a.jpg'
    img = cv2.imread(image_path)

    print("\n=== Processing Image with Manual Detection ===")
    
    # Step 1: Detect license plates
    start_time = time.time()
    detections = anpr_d.detector(img)
    ltrb_time = time.time() - start_time
    print(f"Detection time: {ltrb_time:.4f} seconds")
    print(f"Found {len(detections)} plate(s)")

    # Step 2: Process each detection
    results = []
    ocr_time = 0
    
    for i, box_info in enumerate(detections):
        # Crop license plate region
        # Detector returns: {'bbox': [x1, y1, x2, y2], 'score': float, 'class': str}
        bbox = box_info['bbox']
        l, t, r, b = bbox[0], bbox[1], bbox[2], bbox[3]
        crop_img = img[int(t):int(b), int(l):int(r)]

        if crop_img.size == 0:
            print(f"  Plate {i+1}: Skipped (empty crop)")
            continue

        # Convert to PIL Image for OCR
        pil_img = Image.fromarray(crop_img)
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert(mode="RGB")

        # Run OCR with timing
        start_time = time.time()
        ocr_result = anpr_r.predict(pil_img)
        elapsed = time.time() - start_time
        ocr_time += elapsed

        print(f"  Plate {i+1}: {ocr_result[0]} (confidence: {ocr_result[1]}%) - OCR time: {elapsed:.4f}s")

        # Append to results
        results.append({
            "ocr": ocr_result[0],
            "ocr_conf": ocr_result[1],
            "ltrb": [int(l), int(t), int(r), int(b)],
            "ltrb_conf": int(box_info['score'] * 100)
        })

    # Final output
    output = {
        "results": results,
        "ltrb_proc_sec": round(ltrb_time, 2),
        "ocr_proc_sec": round(ocr_time, 2)
    }
    
    print("\n=== Final Results ===")
    print(output)
    print(f"\nTotal processing time: {ltrb_time + ocr_time:.4f} seconds")
    #################################
    
    
    #################################
    # Example 2: Backend Comparison (if multiple backends available)
    print("\n=== Example 2: Backend Comparison ===")
    
    backends_to_test = ["cpu", "cuda"]  # Add "directml" if on Windows
    
    for test_backend in backends_to_test:
        try:
            print(f"\n🔧 Testing backend: {test_backend}")
            
            # Initialize detector with specific backend
            test_detector = ma_anpr_detector_v14(
                detector_model,
                user_name,
                serial_key,
                signature,
                backend=test_backend,
                conf_thres=0.25,
                iou_thres=0.5
            )
            
            # Measure performance
            start = time.time()
            detections = test_detector.detector(img)
            elapsed = time.time() - start
            
            print(f"   Detected {len(detections)} plates in {elapsed:.4f}s")
            
        except Exception as e:
            print(f"   ⚠️  Backend {test_backend} not available: {e}")
    
    print("\n✅ Advanced demo complete!")
    #################################