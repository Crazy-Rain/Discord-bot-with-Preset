#!/usr/bin/env python3
"""Test script for character avatar feature."""

import sys
import json
from character_manager import CharacterManager

def test_character_avatar_field():
    """Test that character cards support avatar_url field."""
    print("\n" + "=" * 60)
    print("Testing Character Avatar Field")
    print("=" * 60)
    
    try:
        char_manager = CharacterManager()
        
        # Test 1: Load a character and check avatar_url field exists
        print("\n1. Loading character 'luna' and checking avatar_url field...")
        character_data = char_manager.load_character('luna')
        
        if 'avatar_url' in character_data:
            print(f"   ✓ Character has avatar_url field: '{character_data['avatar_url']}'")
        else:
            print("   ✗ Character missing avatar_url field")
            return False
        
        # Test 2: Save a character with avatar_url
        print("\n2. Testing saving character with avatar_url...")
        test_char = {
            'name': 'Test Character',
            'personality': 'Test personality',
            'description': 'Test description',
            'scenario': 'Test scenario',
            'system_prompt': '',
            'avatar_url': 'https://example.com/avatar.png'
        }
        
        char_manager.save_character('test_avatar', test_char)
        print("   ✓ Saved character with avatar_url")
        
        # Test 3: Load the saved character and verify avatar_url
        print("\n3. Loading saved character and verifying avatar_url...")
        loaded_char = char_manager.load_character('test_avatar')
        
        if loaded_char.get('avatar_url') == 'https://example.com/avatar.png':
            print(f"   ✓ Avatar URL correctly saved: {loaded_char['avatar_url']}")
        else:
            print(f"   ✗ Avatar URL not saved correctly: {loaded_char.get('avatar_url')}")
            return False
        
        # Cleanup
        print("\n4. Cleaning up test character...")
        char_manager.delete_character('test_avatar')
        print("   ✓ Test character deleted")
        
        print("\n✅ Character avatar field feature verified!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error testing character avatar field: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("Character Avatar Feature Test")
    print("=" * 60)
    
    result = test_character_avatar_field()
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{status} - Character Avatar Field")
    
    print("=" * 60)
    if result:
        print("✅ Test passed!")
        return 0
    else:
        print("❌ Test failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
