#!/usr/bin/env python3
"""
Quick Test V15 - Test Multiple V15 OCR Models

Tests V14 detector + V15 OCR (latest) with different model sizes.
V15 OCR features: Improved accuracy, better multi-line support
Tests: pico, micro, small, medium, large
Requires: License configured with `ma-anpr config`
"""

import sys
import os
from pathlib import Path
import time

def load_credentials():
    """Load credentials from ~/.marearts/.marearts_env file"""
    config = Path.home() / '.marearts' / '.marearts_env'
    
    user = None
    key = None
    sig = None
    
    # First try environment variables
    user = os.getenv('MAREARTS_ANPR_USERNAME')
    key = os.getenv('MAREARTS_ANPR_SERIAL_KEY')
    sig = os.getenv('MAREARTS_ANPR_SIGNATURE')
    
    # Then load from config file
    if not all([user, key, sig]) and config.exists():
        print(f"Loading credentials from: {config}")
        for line in open(config):
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            if 'MAREARTS_ANPR_USERNAME=' in line or 'USERNAME=' in line:
                user = line.split('=', 1)[1].strip().strip('"').strip("'")
            elif 'MAREARTS_ANPR_SERIAL_KEY=' in line or 'SERIAL_KEY=' in line:
                key = line.split('=', 1)[1].strip().strip('"').strip("'")
            elif 'MAREARTS_ANPR_SIGNATURE=' in line or 'SIGNATURE=' in line:
                sig = line.split('=', 1)[1].strip().strip('"').strip("'")
        
        print(f"✓ Username: {user}")
        print(f"✓ Serial Key: {key[:10]}...{key[-10:] if key and len(key) > 20 else ''}")
        print(f"✓ Signature: {sig[:4]}...{sig[-4:] if sig and len(sig) > 8 else ''}")
    
    return user, key, sig

def test_model_combination(detector_model, ocr_model, sample_path, user_name, serial_key, signature, region="univ"):
    """Test a specific detector + V15 OCR combination"""
    from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v15
    from marearts_anpr import marearts_anpr_from_image_file
    
    print(f"\n{'='*70}")
    print(f"Testing: Detector={detector_model}, OCR V15={ocr_model}, Region={region}")
    print(f"{'='*70}")
    
    try:
        # Load detector
        start_time = time.time()
        detector = ma_anpr_detector_v14(
            detector_model,
            user_name,
            serial_key,
            signature,
            backend="cpu"
        )
        detector_time = time.time() - start_time
        print(f"✅ Detector loaded ({detector_time:.2f}s)")
        
        # Load V15 OCR
        start_time = time.time()
        ocr = ma_anpr_ocr_v15(
            ocr_model,
            region,
            user_name,
            serial_key,
            signature
        )
        ocr_time = time.time() - start_time
        print(f"✅ V15 OCR loaded ({ocr_time:.2f}s)")
        
        # Test inference
        start_time = time.time()
        result = marearts_anpr_from_image_file(detector, ocr, sample_path)
        inference_time = time.time() - start_time
        
        # Handle result format
        if isinstance(result, dict):
            # Result is a dictionary with 'results' key
            plates = result.get('results', [])
            if plates and len(plates) > 0:
                print(f"✅ Inference successful ({inference_time:.2f}s)")
                for i, plate in enumerate(plates):
                    # Debug: print available keys
                    if isinstance(plate, dict):
                        # Try multiple possible keys
                        plate_str = (plate.get('plate_string') or 
                                   plate.get('text') or 
                                   plate.get('plate') or 
                                   plate.get('ocr_text') or
                                   str(plate))
                        conf = (plate.get('confidence') or 
                               plate.get('conf') or 
                               plate.get('score') or 0.0)
                        
                        # If still N/A, show what keys are available
                        if plate_str == str(plate):
                            print(f"   Plate {i+1}: [Debug - Available keys: {list(plate.keys())}]")
                            print(f"   Data: {plate}")
                        else:
                            print(f"   Plate {i+1}: {plate_str} (conf: {conf:.2f})")
                    else:
                        print(f"   Plate {i+1}: {plate}")
                return True
            else:
                print(f"⚠️  No plates detected ({inference_time:.2f}s)")
                return False
        elif isinstance(result, list) and len(result) > 0:
            # Result is a list of plates
            print(f"✅ Inference successful ({inference_time:.2f}s)")
            for i, plate in enumerate(result):
                if isinstance(plate, dict):
                    plate_str = plate.get('plate_string', plate.get('text', 'N/A'))
                    conf = plate.get('confidence', plate.get('conf', 0.0))
                else:
                    plate_str = str(plate)
                    conf = 1.0
                print(f"   Plate {i+1}: {plate_str} (conf: {conf:.2f})")
            return True
        else:
            print(f"⚠️  No plates detected ({inference_time:.2f}s)")
            return False
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("MAREARTS ANPR - Quick Test V15 (Multiple OCR Models)")
    print("="*70)
    print("\nTests V14 detector + V15 OCR (latest) with different model sizes")
    print("V15 OCR: Improved accuracy, better multi-line support")
    print("Models: pico, micro, small, medium, large")
    print("Region: univ (Universal - works for all regions)")
    
    # Load credentials
    user_name, serial_key, signature = load_credentials()
    
    if not all([user_name, serial_key, signature]):
        print("\n❌ ERROR: No credentials found")
        print("\n💡 Configure your license: ma-anpr config")
        return 1
    
    print(f"\n✅ Credentials loaded for: {user_name}")
    
    # Find sample image (use just one)
    all_sample_paths = [
        "../sample_images/eu-a.jpg",
        "../sample_images/eu-b.jpg",
        "../sample_images/kr-a.jpg",
        "../sample_images/kr-b.jpg",
        "../sample_images/us-a.jpg",
        "./sample_image.jpg"
    ]
    
    sample_path = None
    for path in all_sample_paths:
        if os.path.exists(path):
            sample_path = path
            break
    
    if not sample_path:
        print("\n⚠️  No sample images found")
        print("   Please provide test images in ../sample_images/")
        return 1
    
    print(f"✅ Test image: {sample_path}")
    
    # Model pairs to test (matching sizes)
    model_pairs = [
        ("pico_640p_fp32", "pico_fp32"),
        ("micro_640p_fp32", "micro_fp32"),
        ("small_640p_fp32", "small_fp32"),
        ("medium_640p_fp32", "medium_fp32"),
        ("large_640p_fp32", "large_fp32")
    ]
    
    print("\n" + "="*70)
    print("V15 OCR MODEL TESTS (with V14 Detector)")
    print(f"Testing {len(model_pairs)} model pairs")
    print("="*70)
    
    passed = 0
    total = 0
    
    # Test each model pair
    for det_model, ocr_model in model_pairs:
        total += 1
        if test_model_combination(det_model, ocr_model, sample_path, 
                                 user_name, serial_key, signature):
            passed += 1
        
        # Small delay between tests
        time.sleep(0.3)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY - V15 OCR Testing")
    print("="*70)
    print(f"Tests passed: {passed}/{total}")
    print(f"Tested {len(model_pairs)} model pairs = {total} tests")
    
    if passed > 0:
        print("\n🎉 V15 OCR models are working!")
    
    return 0 if passed > 0 else 1

if __name__ == '__main__':
    sys.exit(main())
