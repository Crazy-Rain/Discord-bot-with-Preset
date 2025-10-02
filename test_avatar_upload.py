#!/usr/bin/env python3
"""Test script for avatar upload feature."""

import sys
import os
import base64
from io import BytesIO
from PIL import Image

def test_base64_data_url_parsing():
    """Test that base64 data URLs can be parsed correctly."""
    print("\n" + "=" * 60)
    print("Testing Base64 Data URL Parsing")
    print("=" * 60)
    
    try:
        # Create a small test image
        img = Image.new('RGB', (100, 100), color='red')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()
        
        # Encode to base64
        base64_data = base64.b64encode(image_bytes).decode('utf-8')
        data_url = f"data:image/png;base64,{base64_data}"
        
        print("\n1. Created test base64 data URL")
        print(f"   ✓ Data URL length: {len(data_url)} characters")
        print(f"   ✓ Starts with: {data_url[:40]}...")
        
        # Test parsing
        if data_url.startswith('data:image'):
            header, encoded = data_url.split(',', 1)
            decoded_bytes = base64.b64decode(encoded)
            print("\n2. Successfully parsed data URL")
            print(f"   ✓ Header: {header}")
            print(f"   ✓ Decoded bytes length: {len(decoded_bytes)}")
            print(f"   ✓ Matches original: {decoded_bytes == image_bytes}")
            
            if decoded_bytes == image_bytes:
                print("\n✅ Base64 data URL parsing works correctly!")
                return True
            else:
                print("\n✗ Decoded bytes don't match original")
                return False
        else:
            print("\n✗ Data URL doesn't start with 'data:image'")
            return False
            
    except Exception as e:
        print(f"\n✗ Error testing base64 parsing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_avatar_upload_endpoint():
    """Test that the upload endpoint exists and is configured."""
    print("\n" + "=" * 60)
    print("Testing Avatar Upload Endpoint Configuration")
    print("=" * 60)
    
    try:
        # Check if character_avatars directory exists
        avatars_dir = 'character_avatars'
        if os.path.exists(avatars_dir):
            print(f"\n✓ Avatar directory exists: {avatars_dir}")
        else:
            print(f"\n✗ Avatar directory missing: {avatars_dir}")
            return False
        
        # Check if web_server.py has the upload endpoint
        with open('web_server.py', 'r') as f:
            content = f.read()
            if '/api/characters/upload_avatar' in content:
                print("✓ Upload endpoint defined in web_server.py")
            else:
                print("✗ Upload endpoint not found in web_server.py")
                return False
            
            if 'secure_filename' in content:
                print("✓ Secure filename handling implemented")
            else:
                print("✗ Secure filename handling missing")
                return False
        
        # Check if discord_bot.py handles data URLs
        with open('discord_bot.py', 'r') as f:
            content = f.read()
            if "startswith('data:image')" in content:
                print("✓ Bot can handle base64 data URLs")
            else:
                print("✗ Bot doesn't handle base64 data URLs")
                return False
        
        print("\n✅ Avatar upload endpoint is properly configured!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error checking configuration: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("Avatar Upload Feature Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test base64 parsing
    results.append(("Base64 Data URL Parsing", test_base64_data_url_parsing()))
    
    # Test upload configuration
    results.append(("Upload Endpoint Configuration", test_avatar_upload_endpoint()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✅ All avatar upload tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    # Install PIL if not available
    try:
        from PIL import Image
    except ImportError:
        print("Installing Pillow for image testing...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'Pillow'])
        from PIL import Image
    
    sys.exit(main())
