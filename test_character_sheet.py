#!/usr/bin/env python3
"""Test script to verify character sheet functionality."""

import sys
import os
import json
import tempfile
import shutil

def test_character_sheet():
    """Test character sheet management."""
    print("Testing Character Sheet Functionality...")
    
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp()
    
    try:
        from user_characters_manager import UserCharactersManager
        
        # Initialize manager with test directory
        manager = UserCharactersManager(test_dir)
        
        # Test 1: Add character with sheet
        print("\n1. Testing add character with sheet...")
        manager.add_or_update_character(
            "TestHero",
            "A brave hero with special powers.",
            "Abilities: Flight, Super Strength\nPerks: Enhanced Reflexes",
            True
        )
        
        char = manager.get_character("TestHero")
        assert char['name'] == "TestHero", "Character name mismatch"
        assert char['description'] == "A brave hero with special powers.", "Description mismatch"
        assert char['sheet'] == "Abilities: Flight, Super Strength\nPerks: Enhanced Reflexes", "Sheet mismatch"
        assert char['sheet_enabled'] == True, "Sheet should be enabled"
        print("✓ Character with sheet added successfully")
        
        # Test 2: Update character sheet
        print("\n2. Testing update character sheet...")
        manager.update_character_sheet("TestHero", "Abilities: Flight, Super Strength, Telekinesis")
        char = manager.get_character("TestHero")
        assert "Telekinesis" in char['sheet'], "Sheet update failed"
        print("✓ Character sheet updated successfully")
        
        # Test 3: Disable sheet
        print("\n3. Testing disable sheet...")
        manager.set_sheet_enabled("TestHero", False)
        char = manager.get_character("TestHero")
        assert char['sheet_enabled'] == False, "Sheet should be disabled"
        print("✓ Character sheet disabled successfully")
        
        # Test 4: Enable sheet
        print("\n4. Testing enable sheet...")
        manager.set_sheet_enabled("TestHero", True)
        char = manager.get_character("TestHero")
        assert char['sheet_enabled'] == True, "Sheet should be enabled"
        print("✓ Character sheet enabled successfully")
        
        # Test 5: System prompt with sheet disabled
        print("\n5. Testing system prompt with sheet disabled...")
        manager.set_sheet_enabled("TestHero", False)
        prompt = manager.get_system_prompt_section(["TestHero"])
        assert "[sheet]" not in prompt, "Sheet should not be in prompt when disabled"
        print("✓ Sheet not included when disabled")
        
        # Test 6: System prompt with sheet enabled
        print("\n6. Testing system prompt with sheet enabled...")
        manager.set_sheet_enabled("TestHero", True)
        prompt = manager.get_system_prompt_section(["TestHero"])
        assert "[sheet]" in prompt, "Sheet should be in prompt when enabled"
        assert "This is a sheet of TestHero's Abilities and Perks" in prompt, "Sheet instruction not found"
        assert "Telekinesis" in prompt, "Sheet content not in prompt"
        print("✓ Sheet included when enabled")
        print(f"\nGenerated prompt preview:\n{prompt[:500]}...")
        
        # Test 7: Backward compatibility (character without sheet)
        print("\n7. Testing backward compatibility...")
        manager.add_or_update_character("OldChar", "A character without a sheet")
        char = manager.get_character("OldChar")
        assert char.get('sheet', '') == '', "Old character should have empty sheet"
        assert char.get('sheet_enabled', False) == False, "Old character sheet should be disabled"
        prompt = manager.get_system_prompt_section(["OldChar"])
        assert "[sheet]" not in prompt, "No sheet should be in prompt for old character"
        print("✓ Backward compatibility maintained")
        
        # Test 8: Update character without modifying sheet
        print("\n8. Testing update character preserving sheet...")
        manager.add_or_update_character("TestHero", "Updated description")
        char = manager.get_character("TestHero")
        assert "Telekinesis" in char['sheet'], "Sheet should be preserved"
        assert char['sheet_enabled'] == True, "Sheet enabled status should be preserved"
        print("✓ Sheet preserved when updating character")
        
        print("\n" + "="*60)
        print("✅ All character sheet tests passed!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up test directory
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    success = test_character_sheet()
    sys.exit(0 if success else 1)
