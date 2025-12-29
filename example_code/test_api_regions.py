#!/usr/bin/env python3
"""
Test API with Different Regions - User Example

Shows how to use the free test API (1000 requests/day) to try MareArts ANPR
with different regions before purchasing a license.

No credentials required!
"""

import subprocess
import sys
from pathlib import Path

def test_api_example(image_path, region='eup'):
    """
    Test the free API with an image
    
    Args:
        image_path: Path to your image
        region: 'kr', 'eup', 'na', 'cn', or 'univ'
    """
    print(f"\n{'='*70}")
    print(f"Testing {region.upper()} region with: {Path(image_path).name}")
    print(f"{'='*70}")
    
    cmd = f'ma-anpr test-api "{image_path}" --region {region}'
    print(f"Command: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(f"Error: {result.stderr}")
        return False

def main():
    """Run test API examples with different regions"""
    
    print("\n" + "="*70)
    print("MAREARTS ANPR - Free API Testing Examples")
    print("="*70)
    print("\nThis script demonstrates the free test API (1000 requests/day)")
    print("No license required!")
    print("\n💡 Note:")
    print("   • This uses the FREE test API (no configuration needed)")
    print("   • If you have a license, run 'ma-anpr config' to use local processing")
    print("   • Local processing = unlimited requests + offline operation")
    print("\nAvailable regions:")
    print("  • kr   - Korean plates")
    print("  • eup  - European+ plates")
    print("  • na   - North American plates")
    print("  • cn   - Chinese plates")
    print("  • univ - Universal (all regions)")
    
    # Check if ma-anpr is installed
    result = subprocess.run('ma-anpr --version', shell=True, capture_output=True)
    if result.returncode != 0:
        print("\n❌ marearts-anpr not installed!")
        print("Install: pip install marearts-anpr")
        sys.exit(1)
    
    # Get image path from user or use example
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Try to find sample images
        sample_dir = Path(__file__).parent.parent / 'sample_images'
        if sample_dir.exists():
            images = list(sample_dir.glob('*.jpg')) + list(sample_dir.glob('*.png'))
            if images:
                image_path = str(images[0])
                print(f"\nUsing sample image: {image_path}")
            else:
                print("\n❌ No sample images found")
                print("Usage: python test_api_regions.py <image_path>")
                sys.exit(1)
        else:
            print("\n❌ Please provide an image path")
            print("Usage: python test_api_regions.py <image_path>")
            sys.exit(1)
    
    # Test with different regions
    print(f"\n{'='*70}")
    print("Testing Different Regions")
    print(f"{'='*70}")
    
    # Example 1: European plates (default and most common)
    test_api_example(image_path, 'eup')
    
    # Example 2: Korean plates
    # test_api_example(image_path, 'kr')
    
    # Example 3: North American plates
    # test_api_example(image_path, 'na')
    
    # Example 4: Universal (if region unknown)
    # test_api_example(image_path, 'univ')
    
    print(f"\n{'='*70}")
    print("💡 Tips:")
    print(f"{'='*70}")
    print("• Use specific regions (kr, eup, na, cn) for best accuracy")
    print("• Use 'univ' only when region is unknown")
    print("• Daily limit: 1000 requests (resets at midnight UTC)")
    print("• Test different models with --detector and --ocr options")
    print("\n📖 For more options: ma-anpr test-api --help")
    print("📖 See all models: ma-anpr test-api --list-models")
    print("\n🎯 Ready to buy? Visit: https://www.marearts.com/products/anpr")

if __name__ == '__main__':
    main()

