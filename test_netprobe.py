#!/usr/bin/env python3
"""
Simple tests for NetProbe functionality
"""

import sys
import os
import subprocess

def test_help():
    """Test that help command works"""
    result = subprocess.run([sys.executable, 'netprobe.py', '--help'], 
                          capture_output=True, text=True)
    if result.returncode == 0 and 'NetProbe v2.0' in result.stdout:
        print("✅ Help command works")
        return True
    else:
        print("❌ Help command failed")
        return False

def test_localhost_protection():
    """Test that localhost scanning is blocked"""
    result = subprocess.run([sys.executable, 'netprobe.py', '--scan', 'localhost'], 
                          capture_output=True, text=True)
    if result.returncode == 1 and 'not allowed' in result.stdout:
        print("✅ Localhost protection works")
        return True
    else:
        print("❌ Localhost protection failed")
        return False

def test_private_ip_protection():
    """Test that private IP scanning is blocked"""
    result = subprocess.run([sys.executable, 'netprobe.py', '--scan', '192.168.1.1'], 
                          capture_output=True, text=True)
    if result.returncode == 1 and 'private IP' in result.stdout:
        print("✅ Private IP protection works")
        return True
    else:
        print("❌ Private IP protection failed")
        return False

def test_import():
    """Test that the module can be imported without errors"""
    try:
        result = subprocess.run([sys.executable, '-c', 'import netprobe'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Module imports successfully")
            return True
        else:
            print(f"❌ Module import failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Module import failed with exception: {e}")
        return False

def main():
    """Run all tests"""
    print("Running NetProbe tests...\n")
    
    tests = [
        test_help,
        test_localhost_protection,
        test_private_ip_protection,
        test_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Tests passed: {passed}/{total}")
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())