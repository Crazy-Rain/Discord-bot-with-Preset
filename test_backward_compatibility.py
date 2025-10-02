#!/usr/bin/env python3
"""Test backward compatibility with old presets."""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from preset_manager import PresetManager
from character_manager import CharacterManager

def test_old_preset_compatibility():
    """Test that old presets without new fields still work."""
    print("=" * 60)
    print("Testing Backward Compatibility")
    print("=" * 60)
    
    pm = PresetManager()
    cm = CharacterManager()
    
    try:
        # Load old-style preset (creative.json)
        preset = pm.load_preset("creative")
        print("\n✓ Successfully loaded old-style preset: creative")
        
        # Load old-style character (luna.json)
        character = cm.load_character("luna")
        print("✓ Successfully loaded old-style character: luna")
        
        # Test formatting with old preset/character (should use defaults)
        formatted = pm.format_character_for_prompt(character, preset)
        
        print("\nFormatted with Old-Style Preset:")
        print("-" * 60)
        print(f"System Prompt: {'Present' if formatted['system_prompt'] else 'None'}")
        print(f"Character System: {'Present' if formatted['character_system'] else 'None'}")
        print(f"Example Dialogues: {len(formatted['example_dialogues'])}")
        
        # Verify defaults are used
        assert formatted['system_prompt'] != '', "Should have system prompt"
        assert formatted['character_system'] != '', "Should have character system info"
        assert len(formatted['example_dialogues']) == 0, "Old characters should have no examples"
        
        print("\n✓ Old presets work correctly with default behavior")
        return True
        
    except Exception as e:
        print(f"\n✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mixed_scenario():
    """Test new preset with old character."""
    print("\n" + "=" * 60)
    print("Testing Mixed Scenario (New Preset + Old Character)")
    print("=" * 60)
    
    pm = PresetManager()
    cm = CharacterManager()
    
    try:
        # Load new preset with old character
        preset = pm.load_preset("sillytavern_style")
        character = cm.load_character("sherlock")
        
        print("\n✓ Loaded new preset with old character")
        
        formatted = pm.format_character_for_prompt(character, preset)
        
        print("\nResult:")
        print("-" * 60)
        print(f"System Prompt: {'Present' if formatted['system_prompt'] else 'None'}")
        print(f"Character System: {'Present' if formatted['character_system'] else 'None'}")
        print(f"Example Dialogues: {len(formatted['example_dialogues'])}")
        
        # Old characters don't have examples, should work fine
        assert len(formatted['example_dialogues']) == 0, "Old character should have no examples"
        
        print("\n✓ New preset works with old character (graceful degradation)")
        return True
        
    except Exception as e:
        print(f"\n✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all backward compatibility tests."""
    print("\n" + "=" * 60)
    print("Backward Compatibility Tests")
    print("=" * 60)
    
    tests = [
        test_old_preset_compatibility,
        test_mixed_scenario
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
        print("\n✓ All backward compatibility tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
