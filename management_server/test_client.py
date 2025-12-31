#!/usr/bin/env python3
"""
Test client for MareArts ANPR Management Server

Usage:
    python test_client.py image.jpg
"""
import sys
import requests
from pathlib import Path

def test_server(image_path: str, server_url: str = "http://localhost:8000"):
    """Test ANPR server with an image"""
    
    if not Path(image_path).exists():
        print(f"❌ Error: Image file not found: {image_path}")
        return
    
    print(f"\n{'='*70}")
    print(f"Testing MareArts ANPR Server")
    print(f"{'='*70}")
    print(f"Server: {server_url}")
    print(f"Image: {image_path}\n")
    
    try:
        # Test 1: Health check
        print("1️⃣  Health Check...")
        health = requests.get(f"{server_url}/api/health")
        health_data = health.json()
        
        if health_data.get('credentials_configured'):
            print("   ✅ Server is healthy and ready")
        else:
            print("   ⚠️  Warning: Credentials not configured")
            print("   Set environment variables and restart server")
        
        # Test 2: Get statistics
        print("\n2️⃣  Server Statistics...")
        stats = requests.get(f"{server_url}/api/stats")
        stats_data = stats.json()
        print(f"   Total detections: {stats_data.get('total_detections', 0)}")
        print(f"   Today's count: {stats_data.get('today_count', 0)}")
        print(f"   Avg confidence: {stats_data.get('avg_confidence', 0)}%")
        
        # Test 3: Detect plates
        print("\n3️⃣  Detecting License Plates...")
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{server_url}/api/detect", files=files)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success') and result.get('results'):
                print(f"   ✅ Detection successful!")
                print(f"   Processing time: {result['processing_time']*1000:.0f}ms")
                print(f"   Detector time: {result['detector_time']*1000:.0f}ms")
                print(f"   OCR time: {result['ocr_time']*1000:.0f}ms")
                print(f"\n   Found {len(result['results'])} plate(s):")
                
                for i, plate in enumerate(result['results'], 1):
                    print(f"\n   Plate {i}:")
                    print(f"      Text: {plate['plate_text']}")
                    print(f"      Confidence: {plate['confidence']:.1f}%")
                    print(f"      Detection Confidence: {plate['detection_confidence']}%")
                    print(f"      BBox: {plate['bbox']}")
                
                if result.get('image_url'):
                    print(f"\n   📷 Result image: {server_url}{result['image_url']}")
                    print(f"   🔗 Detection ID: #{result['detection_id']}")
            else:
                print(f"   ⚠️  No plates detected")
                if result.get('error'):
                    print(f"   Error: {result['error']}")
        else:
            print(f"   ❌ Error: HTTP {response.status_code}")
            print(f"   {response.text}")
        
        # Test 4: Get history
        print("\n4️⃣  Recent History...")
        history = requests.get(f"{server_url}/api/history?limit=3")
        history_data = history.json()
        
        if history_data.get('results'):
            print(f"   Last {len(history_data['results'])} detection(s):")
            for det in history_data['results']:
                plates = ', '.join(det['plates']) if det['plates'] else 'No plates'
                print(f"   • ID #{det['id']}: {plates} ({det['timestamp']})")
        else:
            print("   No history found")
        
        print(f"\n{'='*70}")
        print(f"✅ Test complete!")
        print(f"{'='*70}")
        print(f"\n📊 Web Dashboard: {server_url}/")
        print(f"📚 API Docs: {server_url}/docs")
        print(f"\n")
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Could not connect to server at {server_url}")
        print(f"Make sure the server is running!")
        print(f"Start it with: python server.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_client.py <image_path>")
        print("Example: python test_client.py plate.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    server_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000"
    
    test_server(image_path, server_url)

