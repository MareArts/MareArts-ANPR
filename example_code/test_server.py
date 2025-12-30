#!/usr/bin/env python3
"""
Test the Simple ANPR Server

Usage:
    # Start server first:
    python simple_server.py
    
    # Then run this test:
    python test_server.py image.jpg
"""

import requests
import sys

def test_server(image_path, server_url="http://localhost:8000"):
    """Test the ANPR server"""
    
    print(f"\nTesting ANPR server: {server_url}")
    print(f"Image: {image_path}\n")
    
    # Test 1: Health check
    print("1. Health check...")
    response = requests.get(f"{server_url}/health")
    print(f"   {response.json()}")
    
    # Test 2: Detect plates
    print("\n2. Detecting plates...")
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(f"{server_url}/detect", files=files)
    
    if response.status_code == 200:
        result = response.json()
        
        if result.get('results'):
            print(f"   ✅ Detected {len(result['results'])} plate(s):")
            for plate in result['results']:
                print(f"      • {plate['ocr']} ({plate['ocr_conf']}%)")
        else:
            print("   ❌ No plates detected")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   {response.text}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_server.py image.jpg")
        sys.exit(1)
    
    test_server(sys.argv[1])

