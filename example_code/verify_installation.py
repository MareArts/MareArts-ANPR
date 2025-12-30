#!/usr/bin/env python3
"""
Verify Installation - User Troubleshooting Script

Quick script to verify marearts-anpr is installed correctly and all
dependencies are working. Useful for troubleshooting installation issues.
"""

import sys
import subprocess
import os

def check_installation():
    """Verify marearts-anpr installation"""
    
    print("\n" + "="*70)
    print("MAREARTS ANPR - Installation Verification")
    print("="*70)
    
    issues = []
    
    # 1. Check Python version
    print("\n1. Python Version:")
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"   {py_version}")
    if sys.version_info < (3, 9):
        print("   ❌ Python 3.9+ required")
        issues.append("Python version too old")
    elif sys.version_info >= (3, 13):
        print("   ⚠️  Python 3.13+ not officially supported")
    else:
        print("   ✅ Compatible")
    
    # 2. Check NumPy
    print("\n2. NumPy:")
    try:
        import numpy
        numpy_version = numpy.__version__
        print(f"   Version: {numpy_version}")
        
        # Check if NumPy 1.x (required for current builds)
        if numpy_version.startswith('2.'):
            print("   ⚠️  NumPy 2.x detected")
            print("   Current builds require NumPy 1.x")
            print("   Install: pip install 'numpy>=1.26,<2.0'")
            issues.append("NumPy 2.x incompatible with current build")
        else:
            print("   ✅ NumPy 1.x (compatible)")
    except ImportError:
        print("   ❌ NumPy not installed")
        issues.append("NumPy missing")
    
    # 3. Check marearts-anpr
    print("\n3. marearts-anpr Package:")
    try:
        import marearts_anpr
        version = marearts_anpr.__version__
        print(f"   Version: {version}")
        print("   ✅ Package installed")
    except ImportError as e:
        print(f"   ❌ Not installed: {e}")
        issues.append("marearts-anpr not installed")
        print("\n   Install: pip install marearts-anpr")
        return False
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        issues.append(f"Import error: {e}")
        return False
    
    # 4. Check marearts-crystal
    print("\n4. marearts-crystal (License Module):")
    try:
        import marearts_crystal
        print(f"   Version: {marearts_crystal.__version__}")
        print("   ✅ Available")
    except ImportError:
        print("   ❌ Not installed")
        issues.append("marearts-crystal missing")
    
    # 5. Check ONNX Runtime
    print("\n5. ONNX Runtime (V14 Models):")
    try:
        import onnxruntime
        print(f"   Version: {onnxruntime.__version__}")
        providers = onnxruntime.get_available_providers()
        print(f"   Providers: {', '.join(providers[:3])}")
        if 'CUDAExecutionProvider' in providers:
            print("   ✅ GPU acceleration available (CUDA)")
        elif 'DmlExecutionProvider' in providers:
            print("   ✅ GPU acceleration available (DirectML)")
        else:
            print("   ✅ CPU mode (install onnxruntime-gpu for GPU)")
    except ImportError:
        print("   ❌ Not installed")
        issues.append("onnxruntime missing")
    
    # 6. Check OpenCV
    print("\n6. OpenCV:")
    try:
        import cv2
        print(f"   Version: {cv2.__version__}")
        print("   ✅ Available")
    except ImportError:
        print("   ❌ Not installed")
        issues.append("opencv-python missing")
    
    # 7. CLI availability
    print("\n7. CLI Commands:")
    result = subprocess.run('ma-anpr --version', shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"   {result.stdout.strip()}")
        print("   ✅ CLI commands available")
    else:
        print("   ❌ CLI not available")
        issues.append("CLI commands not working")
    
    # 8. Check license configuration
    print("\n8. License Configuration:")
    import os
    has_env_creds = os.getenv('MAREARTS_ANPR_USERNAME') and os.getenv('MAREARTS_ANPR_SERIAL_KEY')
    has_file_creds = os.path.exists(os.path.expanduser('~/.marearts/.marearts_env'))
    
    if has_env_creds or has_file_creds:
        print("   ✅ Credentials configured")
        result = subprocess.run('ma-anpr validate', shell=True, capture_output=True, text=True)
        if "✅ Valid" in result.stdout:
            print("   ✅ License is valid")
        else:
            print("   ⚠️  License validation failed")
    else:
        print("   ⚠️  No credentials configured (optional)")
        print("   💡 Configure with: ma-anpr config")
        print("   💡 Or use free API: ma-anpr test-api image.jpg")
    
    # Summary
    print("\n" + "="*70)
    if not issues:
        print("✅ ALL CHECKS PASSED - Installation is healthy!")
        print("="*70)
        print("\n🎉 You're ready to use MareArts ANPR!")
        print("\n📖 Next steps:")
        print("   • Configure license: ma-anpr config")
        print("   • Test API (free): ma-anpr test-api image.jpg")
        print("   • See examples: ls example_code/")
        print("   • Read docs: docs/")
        return True
    else:
        print("⚠️  SOME ISSUES FOUND")
        print("="*70)
        print("\n❌ Issues to fix:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print("\n💡 Recommended fix:")
        print("   pip install --upgrade marearts-anpr")
        return False

if __name__ == '__main__':
    success = check_installation()
    sys.exit(0 if success else 1)

