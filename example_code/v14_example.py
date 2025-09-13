# pip install marearts-anpr
"""
V14 Models Example (V2 Current License Required)

This example demonstrates how to use V14 models with MareArts ANPR.
V14 models require:
- V2 (Current) license key
- Digital signature (provided with V2 license)
- Backend selection (cpu, cuda, directml, tensorrt)
"""

import cv2
from PIL import Image
from marearts_anpr import ma_anpr_detector_v14  # V14 detector
from marearts_anpr import ma_anpr_ocr
from marearts_anpr import marearts_anpr_from_pil
from marearts_anpr import marearts_anpr_from_image_file
from marearts_anpr import marearts_anpr_from_cv2
import time

if __name__ == '__main__':
    
    #################################
    ## Initiate MareArts ANPR with V14 Models
    print("MareArts ANPR V14 Example")
    
    # V2 (Current) License credentials - you receive all when you purchase
    user_name = "your_email"
    serial_key = "your_serial_key"  # V2 (Current) license
    signature = "your_signature"  # Provided with V2 license
    
    # Optional: Load from environment variables if set
    # export MAREARTS_ANPR_USERNAME="your-email@domain.com"
    # export MAREARTS_ANPR_SERIAL_KEY="your-serial-key"
    # export MAREARTS_ANPR_SIGNATURE="your-signature"
    # import os
    # user_name = os.getenv("MAREARTS_ANPR_USERNAME", user_name)
    # serial_key = os.getenv("MAREARTS_ANPR_SERIAL_KEY", serial_key)
    # signature = os.getenv("MAREARTS_ANPR_SIGNATURE", signature)
    
    #################################
    # V14 Model Options
    
    # Standard V14 Models (ONNX Runtime):
    # v14_small_320p_fp32, v14_small_320p_fp16
    # v14_small_640p_fp32, v14_small_640p_fp16
    # v14_middle_320p_fp32, v14_middle_320p_fp16
    # v14_middle_640p_fp32, v14_middle_640p_fp16
    # v14_large_320p_fp32, v14_large_320p_fp16
    # v14_large_640p_fp32, v14_large_640p_fp16
    
    # TensorRT Optimized (NVIDIA GPUs only):
    # v14_small_320p_trt_fp16, v14_small_320p_trt_fp8
    # v14_small_640p_trt_fp16, v14_small_640p_trt_fp8
    # v14_middle_320p_trt_fp16, v14_middle_320p_trt_fp8
    # v14_middle_640p_trt_fp16, v14_middle_640p_trt_fp8
    # v14_large_320p_trt_fp16, v14_large_320p_trt_fp8
    # v14_large_640p_trt_fp16, v14_large_640p_trt_fp8
    
    detector_model_version = "v14_middle_640p_fp16"  # V14 model
    ocr_model_version = "v13_euplus"  # OCR same as before
    
    #################################
    # Initialize V14 Detector with Backend Selection
    
    # Backend options:
    # - "cpu": Cross-platform CPU inference (ONNX Runtime)
    # - "cuda": NVIDIA GPU acceleration
    # - "directml": Windows GPU acceleration (AMD/Intel/NVIDIA)
    # - "tensorrt": NVIDIA TensorRT optimization (fastest)
    
    backend = "cuda"  # Change based on your hardware
    
    print(f"Initializing V14 detector: {detector_model_version}")
    print(f"Backend: {backend}")
    
    # V14 detector initialization
    anpr_d = ma_anpr_detector_v14(
        detector_model_version, 
        user_name, 
        serial_key, 
        signature,
        backend=backend
    )
    
    # OCR initialization (same as before)
    anpr_r = ma_anpr_ocr(ocr_model_version, user_name, serial_key)
    
    #################################
    # Example 1: Process with convenience functions
    
    print("\n--- Example 1: Using convenience functions ---")
    image_path = './sample_images/eu-a.jpg'
    
    # From file
    start = time.time()
    output = marearts_anpr_from_image_file(anpr_d, anpr_r, image_path)
    print(f"From file: {output}")
    print(f"Total time: {time.time() - start:.3f}s")
    
    # From OpenCV
    img = cv2.imread(image_path)
    start = time.time()
    output = marearts_anpr_from_cv2(anpr_d, anpr_r, img)
    print(f"From cv2: {output}")
    print(f"Total time: {time.time() - start:.3f}s")
    
    # From PIL
    pil_img = Image.open(image_path)
    start = time.time()
    output = marearts_anpr_from_pil(anpr_d, anpr_r, pil_img)
    print(f"From PIL: {output}")
    print(f"Total time: {time.time() - start:.3f}s")
    
    #################################
    # Example 2: Manual detection and OCR
    
    print("\n--- Example 2: Manual detection and OCR ---")
    
    # Read image
    img = cv2.imread(image_path)
    
    # Step 1: Detect license plates with V14 detector
    # Note: V14 detector method is 'detector' not 'predict'
    start_time = time.time()
    detections = anpr_d.detector(img)  # V14 uses 'detector' method
    detect_time = time.time() - start_time
    print(f"Detection time: {detect_time:.3f}s")
    print(f"Found {len(detections)} license plates")
    
    # Step 2: Process each detection
    results = []
    total_ocr_time = 0
    
    for detection in detections:
        # Extract bounding box
        box = detection['box']
        l, t, r, b = box
        
        # Crop license plate region
        crop_img = img[int(t):int(b), int(l):int(r)]
        
        if crop_img.size == 0:
            continue
        
        # Convert to PIL for OCR
        pil_img = Image.fromarray(cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))
        
        # Run OCR
        start_time = time.time()
        ocr_result = anpr_r.predict(pil_img)
        ocr_time = time.time() - start_time
        total_ocr_time += ocr_time
        
        # Store result
        results.append({
            "ocr": ocr_result[0],
            "ocr_conf": ocr_result[1],
            "ltrb": [int(l), int(t), int(r), int(b)],
            "ltrb_conf": int(detection['score'] * 100)
        })
        
        print(f"Plate: {ocr_result[0]} (conf: {ocr_result[1]}%)")
    
    print(f"Total OCR time: {total_ocr_time:.3f}s")
    
    #################################
    # Example 3: Compare backends (if multiple available)
    
    print("\n--- Example 3: Backend Comparison ---")
    
    backends_to_test = ["cpu", "cuda"]  # Add others if available
    
    for test_backend in backends_to_test:
        try:
            print(f"\nTesting backend: {test_backend}")
            
            # Initialize detector with specific backend
            test_detector = ma_anpr_detector_v14(
                detector_model_version,
                user_name,
                serial_key,
                signature,
                backend=test_backend
            )
            
            # Measure performance
            start = time.time()
            output = marearts_anpr_from_image_file(test_detector, anpr_r, image_path)
            elapsed = time.time() - start
            
            print(f"Result: {output['results']}")
            print(f"Time: {elapsed:.3f}s")
            
        except Exception as e:
            print(f"Backend {test_backend} not available: {e}")
    
    #################################
    # Example 4: TensorRT Optimized Models (NVIDIA only)
    
    print("\n--- Example 4: TensorRT Optimized ---")
    
    try:
        # Use TensorRT optimized model for maximum speed
        trt_model = "v14_small_320p_trt_fp8"  # Fastest model
        
        print(f"Testing TensorRT model: {trt_model}")
        
        trt_detector = ma_anpr_detector_v14(
            trt_model,
            user_name,
            serial_key,
            signature,
            backend="tensorrt"
        )
        
        # Benchmark
        num_iterations = 10
        start = time.time()
        for _ in range(num_iterations):
            output = marearts_anpr_from_image_file(trt_detector, anpr_r, image_path)
        
        avg_time = (time.time() - start) / num_iterations
        print(f"Average inference time: {avg_time:.3f}s")
        print(f"FPS: {1/avg_time:.1f}")
        
    except Exception as e:
        print(f"TensorRT not available: {e}")
    
    print("\n=== V14 Example Complete ===")