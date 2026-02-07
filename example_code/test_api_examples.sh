#!/bin/bash
################################################################################
# MareArts ANPR - Test API Examples
################################################################################
#
# This script shows all possible ways to use the free test API.
# No license required! 1000 requests per day.
#
# Usage: ./test_api_examples.sh [image_path]
#
################################################################################

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get image path from argument or use default
if [ -n "$1" ]; then
    IMAGE="$1"
else
    # Try to find a sample image
    if [ -f "../sample_images/eu-a.jpg" ]; then
        IMAGE="../sample_images/eu-a.jpg"
    elif [ -f "../sample_images/kr-a.jpg" ]; then
        IMAGE="../sample_images/kr-a.jpg"
    else
        echo "Usage: $0 <image_path>"
        echo "Example: $0 your_plate_image.jpg"
        exit 1
    fi
fi

echo ""
echo "========================================================================"
echo "MAREARTS ANPR - Free Test API Examples"
echo "========================================================================"
echo ""
echo "Testing with image: $IMAGE"
echo "Daily limit: 1000 requests (resets at midnight UTC)"
echo "No license required!"
echo ""

# Function to run example
run_example() {
    local title="$1"
    local cmd="$2"
    
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$title${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo -e "${YELLOW}Command:${NC} $cmd"
    echo ""
    
    eval "$cmd"
    
    echo ""
    read -p "Press Enter to continue to next example..."
}

################################################################################
# BASIC EXAMPLES
################################################################################

echo "========================================================================"
echo "PART 1: BASIC USAGE"
echo "========================================================================"

# Example 1: Default (simplest)
run_example "1. Default Settings (Recommended)" \
    "ma-anpr test-api \"$IMAGE\""

echo "   💡 With license: ma-anpr read \"$IMAGE\" --confidence 0.5"
echo ""

# Example 2: Specify region
run_example "2. European Plates" \
    "ma-anpr test-api \"$IMAGE\" --region eup"

echo "   💡 With license + confidence: ma-anpr read \"$IMAGE\" --region eup --confidence 0.5"
echo ""

run_example "3. Korean Plates" \
    "ma-anpr test-api \"$IMAGE\" --region kr"

echo "   💡 With license + confidence: ma-anpr read \"$IMAGE\" --region kr --confidence 0.5"
echo ""

run_example "4. North American Plates" \
    "ma-anpr test-api \"$IMAGE\" --region na"

echo "   💡 With license + confidence: ma-anpr read \"$IMAGE\" --region na --confidence 0.5"
echo ""

run_example "5. Chinese Plates" \
    "ma-anpr test-api \"$IMAGE\" --region cn"

echo "   💡 With license + confidence: ma-anpr read \"$IMAGE\" --region cn --confidence 0.5"
echo ""

run_example "6. Universal (All Regions)" \
    "ma-anpr test-api \"$IMAGE\" --region univ"

echo "   💡 With license + confidence: ma-anpr read \"$IMAGE\" --region univ --confidence 0.5"
echo ""

################################################################################
# MODEL SIZE EXAMPLES
################################################################################

echo ""
echo "========================================================================"
echo "PART 2: DIFFERENT MODEL SIZES"
echo "========================================================================"

run_example "7. Fastest (Pico - Real-time)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_pico_640p_fp32 --ocr v15_small_fp32 --region univ"

run_example "8. Fast (Micro - Balanced)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_micro_640p_fp32 --ocr v15_small_fp32 --region univ"

run_example "9. Balanced (Small)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_small_640p_fp32 --ocr v15_small_fp32 --region univ"

run_example "10. Best Overall (Medium - Recommended)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_medium_640p_fp32 --ocr v15_small_fp32 --region univ"

run_example "11. Highest Accuracy (Large)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_large_640p_fp32 --ocr v15_large_fp32 --region univ"

################################################################################
# V15 OCR EXAMPLES (Recommended - Better Accuracy)
################################################################################

echo ""
echo "========================================================================"
echo "PART 3: V15 OCR MODELS (Recommended)"
echo "========================================================================"

run_example "12. V15 OCR - Small (Fast & Accurate)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_medium_640p_fp32 --ocr v15_small_fp32 --region univ"

run_example "13. V15 OCR - Medium (Higher Accuracy)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_medium_640p_fp32 --ocr v15_medium_fp32 --region univ"

run_example "14. V15 OCR - Large (Maximum Accuracy)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_large_640p_fp32 --ocr v15_large_fp32 --region univ"

echo ""
echo -e "${YELLOW}Note:${NC} test-api only supports 640p_fp32 detectors and fp32 OCR models"
echo "For 320p, FP16, or INT8 models, use licensed local processing:"
echo "  ma-anpr read image.jpg --detector-model micro_320p_fp32"
echo ""

################################################################################
# USE CASE EXAMPLES
################################################################################

echo ""
echo "========================================================================"
echo "PART 4: COMMON USE CASES (with V15 OCR)"
echo "========================================================================"

run_example "15. Security Camera (Real-time)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_micro_640p_fp32 --ocr v15_small_fp32 --region univ"

echo "   💡 With license + low confidence (catch everything):"
echo "      ma-anpr read \"$IMAGE\" --detector-model micro_640p_fp32 --ocr-model small_fp32 --region univ --confidence 0.25"
echo ""

run_example "16. Parking Management (Balanced)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_medium_640p_fp32 --ocr v15_small_fp32 --region univ"

echo "   💡 With license + medium confidence (balanced):"
echo "      ma-anpr read \"$IMAGE\" --detector-model medium_640p_fp32 --ocr-model small_fp32 --region univ --confidence 0.50"
echo ""

run_example "17. Law Enforcement (Maximum Accuracy)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_large_640p_fp32 --ocr v15_large_fp32 --region univ"

echo "   💡 With license + high confidence (strict):"
echo "      ma-anpr read \"$IMAGE\" --detector-model large_640p_fp32 --ocr-model large_fp32 --region univ --confidence 0.75"
echo ""

run_example "18. Mobile App (Fast & Efficient)" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_small_640p_fp32 --ocr v15_small_fp32 --region univ"

echo "   💡 With license + confidence:"
echo "      ma-anpr read \"$IMAGE\" --detector-model small_640p_fp32 --ocr-model small_fp32 --region univ --confidence 0.50"
echo ""

################################################################################
# ADVANCED OPTIONS
################################################################################

echo ""
echo "========================================================================"
echo "PART 6: ADVANCED OPTIONS"
echo "========================================================================"

# Example with JSON output
run_example "19. Save Results to JSON" \
    "ma-anpr test-api \"$IMAGE\" --detector v14_medium_640p_fp32 --ocr v15_small_fp32 --region univ --json results.json && echo 'Results:' && cat results.json 2>/dev/null"

echo ""
echo -e "${YELLOW}Note:${NC} Confidence threshold is supported via detector initialization:"
echo "  detector = ma_anpr_detector_v14(model, user, key, sig, conf_thres=0.25)"
echo ""

################################################################################
# CONFIDENCE THRESHOLD (LOCAL PROCESSING WITH LICENSE)
################################################################################

echo ""
echo "========================================================================"
echo "PART 7: CONFIDENCE THRESHOLD (Licensed Version Only)"
echo "========================================================================"
echo ""
echo -e "${YELLOW}Note: test-api (free) doesn't support confidence threshold.${NC}"
echo -e "${YELLOW}To control confidence, use local processing with a license.${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CLI Examples with Confidence Threshold (Requires License):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Default threshold (0.50):"
echo -e "   ${GREEN}ma-anpr read image.jpg${NC}"
echo ""
echo "2. Low threshold (0.25) - Security cameras:"
echo -e "   ${GREEN}ma-anpr read image.jpg --confidence 0.25${NC}"
echo "   → Detects more plates, some false positives"
echo ""
echo "3. Medium threshold (0.50) - Balanced:"
echo -e "   ${GREEN}ma-anpr read image.jpg --confidence 0.50${NC}"
echo "   → Default, good balance"
echo ""
echo "4. High threshold (0.75) - Law enforcement:"
echo -e "   ${GREEN}ma-anpr read image.jpg --confidence 0.75${NC}"
echo "   → Only high-confidence detections"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Python API Examples (Detector conf_thres):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v14"
echo ""
echo "# Security camera (detect everything):"
echo "detector = ma_anpr_detector_v14("
echo "    'medium_640p_fp32', user, key, signature,"
echo -e "    ${GREEN}conf_thres=0.15,${NC}  # Low threshold"
echo "    iou_thres=0.5"
echo ")"
echo ""
echo "# General use (balanced):"
echo "detector = ma_anpr_detector_v14("
echo "    'medium_640p_fp32', user, key, signature,"
echo -e "    ${GREEN}conf_thres=0.25,${NC}  # Default"
echo "    iou_thres=0.5"
echo ")"
echo ""
echo "# High precision (law enforcement):"
echo "detector = ma_anpr_detector_v14("
echo "    'medium_640p_fp32', user, key, signature,"
echo -e "    ${GREEN}conf_thres=0.40,${NC}  # Strict"
echo "    iou_thres=0.5"
echo ")"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Use Cases by Confidence Threshold:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  conf_thres=0.15  → Security cameras (catch all vehicles)"
echo "  conf_thres=0.25  → General parking/toll (balanced)"
echo "  conf_thres=0.40  → Law enforcement (high confidence)"
echo "  conf_thres=0.60  → Critical systems (very strict)"
echo ""
echo "💡 To use local processing with confidence control:"
echo "   1. Configure license: ma-anpr config"
echo "   2. Use 'ma-anpr read' instead of 'test-api'"
echo "   3. See example_code/basic.py for Python API"
echo ""
echo "🆓 Free test-api returns all detections (no threshold control)"
echo ""
read -p "Press Enter to see final summary..."

################################################################################
# REFERENCE
################################################################################

echo ""
echo "========================================================================"
echo "QUICK REFERENCE"
echo "========================================================================"
echo ""
echo "List all available models:"
echo "  ma-anpr test-api --list-models"
echo ""
echo "Get help:"
echo "  ma-anpr test-api --help"
echo ""
echo "test-api supported models:"
echo "  Detectors: v14_{pico,micro,small,medium,large}_640p_fp32 (5 models)"
echo "  OCR: v14_{pico,micro,small,medium,large}_fp32 (5 models)"
echo "  OCR: v15_{pico,micro,small,medium,large}_fp32 (5 models, recommended)"
echo ""
echo "All regions (5 total):"
echo "  kr, eup, na, cn, univ"
echo ""
echo "========================================================================"
echo "RECOMMENDED COMBINATIONS"
echo "========================================================================"
echo ""
echo "General use (Default - Uses v15 OCR):"
echo "  ma-anpr test-api image.jpg"
echo ""
echo "Fast processing:"
echo "  ma-anpr test-api image.jpg --detector v14_micro_640p_fp32 --ocr v15_small_fp32"
echo ""
echo "Best quality:"
echo "  ma-anpr test-api image.jpg --detector v14_large_640p_fp32 --ocr v15_large_fp32"
echo ""
echo "Korean plates:"
echo "  ma-anpr test-api image.jpg --region kr"
echo ""
echo "USA/Canada plates:"
echo "  ma-anpr test-api image.jpg --region na"
echo ""
echo "Universal (all regions):"
echo "  ma-anpr test-api image.jpg --region univ"
echo ""
echo "========================================================================"
echo "💡 Tips:"
echo "========================================================================"
echo "• Use v15 OCR for better accuracy (2-3% improvement)"
echo "• Use specific regions for best results"
echo "• test-api only supports 640p_fp32 models"
echo "• For 320p/FP16/INT8 models, use licensed local processing"
echo "• Daily limit: 1000 requests"
echo ""
echo "🛒 Ready to purchase?"
echo "   Visit: https://www.marearts.com/products/anpr"
echo ""
echo "📖 More examples:"
echo "   python example_code/test_api_regions.py"
echo "   python example_code/verify_installation.py"
echo ""

