#!/usr/bin/env python3
"""Test suite for fixing Discord chat error and lorebook constant entry issues."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lorebook_manager import LorebookManager


def test_empty_string_character_with_global_lorebook():
    """Test that empty string character name works with global lorebooks."""
    print("\n" + "=" * 70)
    print("TEST: Empty String Character with Global Lorebook")
    print("=" * 70)
    
    lm = LorebookManager()
    lm.create_lorebook('Global', enabled=True, linked_characters=None)
    lm.add_or_update_entry(
        key='Global Entry',
        content='This is a global constant entry',
        activation_type='constant',
        lorebook_name='Global'
    )
    
    # Test with empty string character name
    result = lm.get_system_prompt_section('test message', '')
    
    assert len(result) > 0, "No content returned for empty string character with global lorebook!"
    assert 'Global Entry' in result, "Global entry not included for empty string character!"
    
    print("✅ PASS: Empty string character gets global lorebook entries")
    return True


def test_empty_string_character_with_linked_lorebook():
    """Test that empty string character name works with lorebooks linked to empty string."""
    print("\n" + "=" * 70)
    print("TEST: Empty String Character with Linked Lorebook")
    print("=" * 70)
    
    lm = LorebookManager()
    lm.create_lorebook('EmptyCharLore', enabled=True, linked_characters=[''])
    lm.add_or_update_entry(
        key='Empty Char Entry',
        content='This entry is linked to empty string character',
        activation_type='constant',
        lorebook_name='EmptyCharLore'
    )
    
    # Test with empty string character name (should match)
    result = lm.get_system_prompt_section('test message', '')
    
    assert len(result) > 0, "No content returned for empty string character!"
    assert 'Empty Char Entry' in result, "Empty string linked entry not included!"
    
    # Test with None character name (should NOT match)
    result_none = lm.get_system_prompt_section('test message', None)
    assert 'Empty Char Entry' not in result_none, "Empty string linked entry incorrectly included for None character!"
    
    print("✅ PASS: Empty string character matching works correctly")
    return True


def test_constant_entries_always_included():
    """Test that constant (always active) entries are always included for matching lorebooks."""
    print("\n" + "=" * 70)
    print("TEST: Constant Entries Always Included")
    print("=" * 70)
    
    lm = LorebookManager()
    
    # Global lorebook with constant entry
    lm.create_lorebook('World', enabled=True, linked_characters=None)
    lm.add_or_update_entry(
        key='World Info',
        content='Important world information',
        activation_type='constant',
        lorebook_name='World'
    )
    
    # Character-linked lorebook with constant entry
    lm.create_lorebook('Luna Lore', enabled=True, linked_characters=['Luna'])
    lm.add_or_update_entry(
        key='Luna Info',
        content='Important Luna information',
        activation_type='constant',
        lorebook_name='Luna Lore'
    )
    
    # Test with Luna - should get both global and character-specific constant entries
    result = lm.get_system_prompt_section('any text', 'Luna')
    assert 'World Info' in result, "Global constant entry not included!"
    assert 'Luna Info' in result, "Character constant entry not included!"
    
    # Test with other character - should only get global constant entry
    result = lm.get_system_prompt_section('any text', 'Alice')
    assert 'World Info' in result, "Global constant entry not included for Alice!"
    assert 'Luna Info' not in result, "Luna constant entry incorrectly included for Alice!"
    
    print("✅ PASS: Constant entries are properly filtered and included")
    return True


def test_backward_compatibility_always_active():
    """Test backward compatibility with old always_active field."""
    print("\n" + "=" * 70)
    print("TEST: Backward Compatibility - always_active Field")
    print("=" * 70)
    
    lm = LorebookManager()
    lm.create_lorebook('Legacy', enabled=True)
    
    # Use old always_active parameter (should be converted to activation_type)
    lm.add_or_update_entry(
        key='Legacy Entry',
        content='Old style always active entry',
        always_active=True,
        lorebook_name='Legacy'
    )
    
    # Should be included as a constant entry
    result = lm.get_system_prompt_section('test', None)
    assert 'Legacy Entry' in result, "Legacy always_active entry not included!"
    
    print("✅ PASS: Backward compatibility with always_active works")
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("DISCORD CHAT ERROR & LOREBOOK FIX VERIFICATION")
    print("=" * 70)
    
    # Clean up lorebook directory before tests
    import shutil
    lorebook_dir = os.path.join(os.path.dirname(__file__), 'lorebook')
    if os.path.exists(lorebook_dir):
        shutil.rmtree(lorebook_dir)
    
    tests = [
        ("Empty String Character with Global Lorebook", test_empty_string_character_with_global_lorebook),
        ("Empty String Character with Linked Lorebook", test_empty_string_character_with_linked_lorebook),
        ("Constant Entries Always Included", test_constant_entries_always_included),
        ("Backward Compatibility - always_active", test_backward_compatibility_always_active),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            # Clean up lorebook between tests
            if os.path.exists(lorebook_dir):
                shutil.rmtree(lorebook_dir)
        except Exception as e:
            print(f"❌ FAIL: {test_name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    print(f"\n{'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
