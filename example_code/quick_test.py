#!/usr/bin/env python3
"""
Quick Test - Verify Everything Works

Simple script for users to verify their installation and license.
Tests both the free API and local processing (if license configured).
"""

import sys
import subprocess

def run_test(description, command, required=True):
    """Run a test command and report results"""
    print(f"\n{'='*70}")
    print(f"TEST: {description}")
    print(f"{'='*70}")
    print(f"Command: {command}\n")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ PASS")
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()[:300]}")
        return True
    else:
        if required:
            print("❌ FAIL")
        else:
            print("⚠️  SKIP (optional)")
        if result.stderr.strip():
            print(f"Error: {result.stderr.strip()[:300]}")
        return False

def main():
    print("\n" + "="*70)
    print("MAREARTS ANPR - Quick Test")
    print("="*70)
    print("\nThis script verifies your installation is working correctly.")
    print("\n💡 First time user?")
    print("   If you have a license, run: ma-anpr config")
    print("   This will save your credentials for future use.")
    
    passed = 0
    total = 0
    
    # Test 1: Package installed
    total += 1
    if run_test(
        "Package Installation",
        "python -c \"import marearts_anpr; print(f'Version: {marearts_anpr.__version__}')\"",
        required=True
    ):
        passed += 1
    else:
        print("\n❌ CRITICAL: marearts-anpr not installed")
        print("Fix: pip install marearts-anpr")
        sys.exit(1)
    
    # Test 2: CLI available
    total += 1
    if run_test(
        "CLI Commands",
        "ma-anpr --version",
        required=True
    ):
        passed += 1
    
    # Test 3: Free API test (no license needed)
    print("\n" + "="*70)
    print("Testing Free API (No License Required)")
    print("="*70)
    
    # Check if sample image exists
    sample_exists = False
    import os
    sample_paths = [
        "../sample_images/eu-a.jpg",
        "../sample_images/kr-a.jpg",
        "./sample_image.jpg"
    ]
    
    for path in sample_paths:
        if os.path.exists(path):
            sample_exists = True
            sample_path = path
            break
    
    if sample_exists:
        total += 1
        print(f"\nFound sample image: {sample_path}")
        if run_test(
            "Free API Test (1000/day limit)",
            f'ma-anpr test-api "{sample_path}"',
            required=False
        ):
            passed += 1
            print("\n💡 The free API works! You can test with your own images.")
            print("   Usage: ma-anpr test-api your_image.jpg --region eup")
    else:
        print("\n⚠️  No sample images found - skipping API test")
        print("   You can test with your own image:")
        print("   ma-anpr test-api your_image.jpg")
    
    # Test 4: List available models
    total += 1
    if run_test(
        "List V14 Models (Free API)",
        "ma-anpr test-api --list-models | head -10",
        required=False
    ):
        passed += 1
    
    # Test 5: Check license (optional)
    total += 1
    print("\n" + "="*70)
    print("Checking License Configuration (Optional)")
    print("="*70)
    result = subprocess.run('ma-anpr validate', shell=True, capture_output=True, text=True)
    
    if "✅ Valid" in result.stdout or result.returncode == 0:
        print("✅ License configured and valid!")
        passed += 1
        print(result.stdout)
    else:
        print("⚠️  No license configured (optional)")
        print("\n💡 To configure your license:")
        print("   ma-anpr config")
        print("\n💡 Or continue using the free test API (1000/day)")
    
    # Final summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Tests passed: {passed}/{total}")
    
    if passed >= 3:  # At least installation + CLI + API working
        print("\n🎉 Your installation is working!")
        print("\n📖 Next steps:")
        print("   • Try the free API: ma-anpr test-api your_image.jpg")
        print("   • See all options: ma-anpr test-api --list-models")
        print("   • Check examples: ls example_code/")
        print("   • Configure license: ma-anpr config (if purchased)")
        print("\n🛒 Purchase: https://www.marearts.com/products/anpr")
        return 0
    else:
        print("\n⚠️  Some tests failed - check errors above")
        return 1

if __name__ == '__main__':
    sys.exit(main())

