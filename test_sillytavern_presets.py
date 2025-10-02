#!/usr/bin/env python3
"""Test script for the new SillyTavern-style preset system."""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from preset_manager import PresetManager
from character_manager import CharacterManager

def test_preset_loading():
    """Test loading presets with new fields."""
    print("=" * 60)
    print("Testing Preset Loading")
    print("=" * 60)
    
    pm = PresetManager()
    
    # Test loading SillyTavern-style preset
    try:
        preset = pm.load_preset("sillytavern_style")
        print("\n✓ Successfully loaded sillytavern_style preset")
        print(f"  - Temperature: {preset.get('temperature')}")
        print(f"  - Prompt Format: {preset.get('prompt_format', 'default')}")
        print(f"  - Character Position: {preset.get('character_position', 'system')}")
        print(f"  - Include Examples: {preset.get('include_examples', True)}")
    except Exception as e:
        print(f"\n✗ Failed to load preset: {e}")
        return False
    
    return True

def test_character_formatting():
    """Test character card formatting with new system."""
    print("\n" + "=" * 60)
    print("Testing Character Card Formatting")
    print("=" * 60)
    
    pm = PresetManager()
    cm = CharacterManager()
    
    try:
        # Load preset and character
        preset = pm.load_preset("sillytavern_style")
        character = cm.load_character("aria")
        
        print("\n✓ Successfully loaded character: Aria")
        
        # Test formatting
        formatted = pm.format_character_for_prompt(character, preset)
        
        print("\nFormatted Character Data:")
        print("-" * 60)
        
        if formatted['system_prompt']:
            print("\n📝 System Prompt:")
            print(f"  {formatted['system_prompt'][:100]}...")
        
        if formatted['character_system']:
            print("\n👤 Character System Info:")
            print(f"  {formatted['character_system'][:100]}...")
        
        if formatted['example_dialogues']:
            print(f"\n💬 Example Dialogues: {len(formatted['example_dialogues'])} messages")
            for i, msg in enumerate(formatted['example_dialogues'][:3], 1):
                role = msg['role']
                content = msg['content'][:50].replace('\n', ' ')
                print(f"  {i}. [{role}] {content}...")
        else:
            print("\n💬 Example Dialogues: None")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Failed to format character: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_message_building():
    """Test building messages with proper role separation."""
    print("\n" + "=" * 60)
    print("Testing Message Building")
    print("=" * 60)
    
    pm = PresetManager()
    cm = CharacterManager()
    
    try:
        # Load preset and character
        preset = pm.load_preset("uncensored_roleplay")
        character = cm.load_character("aria")
        
        # Format character
        formatted = pm.format_character_for_prompt(character, preset)
        
        # Simulate building messages
        messages = []
        
        # 1. System message
        system_prompt = formatted['system_prompt']
        if formatted['character_system']:
            system_prompt += '\n\n' + formatted['character_system']
        messages.append({"role": "system", "content": system_prompt})
        
        # 2. Example dialogues
        messages.extend(formatted['example_dialogues'])
        
        # 3. User message
        messages.append({"role": "user", "content": "Hello! What's your name?"})
        
        print("\n✓ Built message list with proper role separation")
        print(f"\nTotal messages: {len(messages)}")
        print("\nMessage Structure:")
        print("-" * 60)
        
        for i, msg in enumerate(messages, 1):
            role = msg['role']
            content_preview = msg['content'][:60].replace('\n', ' ')
            print(f"{i}. [{role:10}] {content_preview}...")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Failed to build messages: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("SillyTavern-Style Preset System Tests")
    print("=" * 60)
    
    tests = [
        test_preset_loading,
        test_character_formatting,
        test_message_building
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
