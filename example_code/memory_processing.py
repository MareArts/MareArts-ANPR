#!/usr/bin/env python3
"""
Process Images from Memory - Simple Example

Shows how to process images WITHOUT saving to disk.
Perfect for: Visual Studio, real-time cameras, existing software.

Credential Options:
1. Configure + Auto-load: ma-anpr config (recommended)
2. Hardcode below: Edit USER/KEY/SIG (quick testing)
3. Environment variables: export MAREARTS_ANPR_USERNAME=...
"""

from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v14, marearts_anpr_from_image
import cv2
import numpy as np
import os
from pathlib import Path

# ============================================================================
# CREDENTIALS - Choose one method:
# ============================================================================

# Method 1: Hardcode (quick testing - just edit below!)
USER = "your_email"
KEY = "your_serial_key"
SIG = "your_signature"

# Method 2: Auto-load from ma-anpr config (recommended)
if USER == "your_email":  # If not hardcoded, try auto-load
    def load_credentials():
        user = os.getenv('MAREARTS_ANPR_USERNAME')
        key = os.getenv('MAREARTS_ANPR_SERIAL_KEY')
        sig = os.getenv('MAREARTS_ANPR_SIGNATURE')
        
        if not all([user, key, sig]):
            config_file = Path.home() / '.marearts' / '.marearts_env'
            if config_file.exists():
                with open(config_file) as f:
                    for line in f:
                        if 'MAREARTS_ANPR_USERNAME=' in line:
                            user = line.split('=')[1].strip().strip('"')
                        elif 'MAREARTS_ANPR_SERIAL_KEY=' in line:
                            key = line.split('=')[1].strip().strip('"')
                        elif 'MAREARTS_ANPR_SIGNATURE=' in line:
                            sig = line.split('=')[1].strip().strip('"')
        return user, key, sig
    
    USER, KEY, SIG = load_credentials()

# Verify credentials
if not all([USER, KEY, SIG]) or USER == "your_email":
    print("❌ No credentials!")
    print("\nOption 1: Edit this file - change USER/KEY/SIG above")
    print("Option 2: Run 'ma-anpr config' then run this script")
    exit(1)

# Initialize models (do ONCE at startup)
print("Loading models...")
detector = ma_anpr_detector_v14(
    "medium_640p_fp32", USER, KEY, SIG,
    conf_thres=0.20,  # LOW for parking (0.15-0.30)
    backend="cpu"
)
ocr = ma_anpr_ocr_v14("small_fp32", "eup", USER, KEY, SIG)

# 💡 Switch regions dynamically (no reload!):
# ocr.set_region('kr')   # Korean
# ocr.set_region('na')   # North America
# ocr.set_region('cn')   # China

print("✅ Ready!\n")

# Method 1: From bytes (Visual Studio, HTTP uploads)
def process_bytes(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return marearts_anpr_from_image(detector, ocr, img)

# Method 2: From numpy array (OpenCV, cameras)
def process_array(image_array):
    return marearts_anpr_from_image(detector, ocr, image_array)

# Example usage
if __name__ == '__main__':
    # Test with sample image
    test_img = "../sample_images/eu-a.jpg"
    
    if os.path.exists(test_img):
        # Load and process from bytes
        with open(test_img, "rb") as f:
            image_bytes = f.read()
        
        result = process_bytes(image_bytes)
        
        if result and result.get('results'):
            print(f"✅ Detected {len(result['results'])} plate(s):")
            for p in result['results']:
                print(f"   {p['ocr']} ({p['ocr_conf']}%)")
        else:
            print("❌ No plates detected")
            print("\n💡 Try: Lower confidence to 0.15")
            print("💡 Or: Different region (kr, eup, na, cn)")
    else:
        print("Usage: python memory_processing.py")
        print("\n💡 Edit USER/KEY/SIG variables above")
        print("💡 Or run: ma-anpr config")

print("\n💡 For Visual Studio: See comments in this file")
print("💡 Troubleshooting: ma-anpr validate")

