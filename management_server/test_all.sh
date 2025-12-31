#!/bin/bash
#
# Comprehensive Test Script for MareArts ANPR Management Server
# Tests all API endpoints with sample images
#

SERVER_URL="http://localhost:8000"
# Use relative path to sample_images in parent directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SAMPLE_DIR="$SCRIPT_DIR/../sample_images"

echo "========================================================================"
echo "MareArts ANPR Server - Comprehensive Test Suite"
echo "========================================================================"
echo ""

# Check if server is running
echo "🔍 Checking server status..."
if ! curl -s "$SERVER_URL/api/health" > /dev/null 2>&1; then
    echo "❌ Error: Server is not running!"
    echo "   Start it with: python server.py"
    exit 1
fi
echo "✅ Server is running"
echo ""

# Health check
echo "========================================================================"
echo "TEST 1: Health Check"
echo "========================================================================"
curl -s "$SERVER_URL/api/health" | python3 -m json.tool
echo ""
echo ""

# Statistics (before)
echo "========================================================================"
echo "TEST 2: Server Statistics (Before)"
echo "========================================================================"
curl -s "$SERVER_URL/api/stats" | python3 -m json.tool
echo ""
echo ""

# Test images
IMAGES=(
    "eu-a.jpg"
    "eu-b.jpg"
    "kr-a.jpg"
)

for img in "${IMAGES[@]}"; do
    IMG_PATH="$SAMPLE_DIR/$img"
    
    if [ ! -f "$IMG_PATH" ]; then
        echo "⚠️  Skipping $img (not found)"
        continue
    fi
    
    echo "========================================================================"
    echo "TEST 3: File Upload - $img"
    echo "========================================================================"
    curl -s -X POST "$SERVER_URL/api/detect" -F "image=@$IMG_PATH" | python3 -m json.tool
    echo ""
    echo ""
    
    echo "========================================================================"
    echo "TEST 4: Binary Upload - $img"
    echo "========================================================================"
    curl -s -X POST "$SERVER_URL/api/detect/binary" \
        --data-binary "@$IMG_PATH" \
        -H "Content-Type: application/octet-stream" | python3 -m json.tool
    echo ""
    echo ""
    
    echo "========================================================================"
    echo "TEST 5: Base64 Upload - $img"
    echo "========================================================================"
    # Use Python for base64 (curl command line has size limits)
    python3 -c "
import base64, requests, json
with open('$IMG_PATH', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
    response = requests.post('$SERVER_URL/api/detect/base64', json={'image': b64})
    print(json.dumps(response.json(), indent=2))
"
    echo ""
    echo ""
done

# Python client test
echo "========================================================================"
echo "TEST 6: Python Test Client"
echo "========================================================================"
if [ -f "$SAMPLE_DIR/eu-a.jpg" ]; then
    python test_client.py "$SAMPLE_DIR/eu-a.jpg"
fi
echo ""

# Statistics (after)
echo "========================================================================"
echo "TEST 7: Server Statistics (After)"
echo "========================================================================"
curl -s "$SERVER_URL/api/stats" | python3 -m json.tool
echo ""
echo ""

# History
echo "========================================================================"
echo "TEST 8: Detection History (Last 5)"
echo "========================================================================"
curl -s "$SERVER_URL/api/history?limit=5" | python3 -m json.tool
echo ""
echo ""

# Daily stats
echo "========================================================================"
echo "TEST 9: Daily Statistics"
echo "========================================================================"
curl -s "$SERVER_URL/api/daily-stats?days=7" | python3 -m json.tool
echo ""
echo ""

# Model status
echo "========================================================================"
echo "TEST 10: Model Status"
echo "========================================================================"
curl -s "$SERVER_URL/api/models/status" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Current Config:\")
print(f\"  Detector: {data['current_detector']}\")
print(f\"  OCR: {data['current_ocr']}\")
print(f\"  Region: {data['current_region']}\")
print(f\"\nDetector Models:\")
for m in data['detector_models'][:5]:
    status = '✓' if m['downloaded'] else '✗'
    current = ' [CURRENT]' if m['current'] else ''
    print(f\"  {status} {m['name']}{current}\")
print(f\"\nOCR Models:\")
for m in data['ocr_models']:
    status = '✓' if m['downloaded'] else '✗'
    current = ' [CURRENT]' if m['current'] else ''
    print(f\"  {status} {m['name']}{current}\")
"
echo ""
echo ""

echo "========================================================================"
echo "✅ All Tests Complete!"
echo "========================================================================"
echo ""
echo "📊 Web Dashboard: $SERVER_URL/"
echo "📚 API Docs: $SERVER_URL/docs"
echo ""
echo "💡 Tips:"
echo "  • Korean plate accuracy low? Change region to 'kr' in Settings tab"
echo "  • For best accuracy, always use the correct region"
echo ""
echo "Next steps:"
echo "  1. Open web dashboard in browser"
echo "  2. Check History tab for all detections"
echo "  3. View Statistics tab for charts"
echo "  4. Configure models/region in Settings tab"
echo ""

