#!/usr/bin/env python3
"""Test character-linked lorebook functionality."""
import os
import sys
import json
import shutil
from lorebook_manager import LorebookManager

def setup_test_env():
    """Set up test environment."""
    test_dir = "/tmp/test_lorebook"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    return test_dir

def test_create_global_lorebook():
    """Test creating a global lorebook."""
    print("Test 1: Create global lorebook...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    lm.create_lorebook("Global Lore", "World rules", enabled=True, linked_character=None)
    lm.add_or_update_entry(
        "Magic System",
        "Magic is powered by mana crystals",
        keywords=["magic", "mana"],
        activation_type="constant",
        lorebook_name="Global Lore"
    )
    
    lorebooks = lm.list_lorebooks()
    assert len(lorebooks) == 1
    assert lorebooks[0]["name"] == "Global Lore"
    assert lorebooks[0]["linked_character"] is None
    print("✓ Global lorebook created successfully")
    return lm

def test_create_character_linked_lorebook():
    """Test creating a character-linked lorebook."""
    print("\nTest 2: Create character-linked lorebook...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    lm.create_lorebook("Luna's Lore", "Luna-specific lore", enabled=True, linked_character="Luna")
    lm.add_or_update_entry(
        "Luna's Powers",
        "Luna has the power to control moonlight",
        keywords=["luna", "power"],
        activation_type="constant",
        lorebook_name="Luna's Lore"
    )
    
    lorebooks = lm.list_lorebooks()
    assert len(lorebooks) == 1
    assert lorebooks[0]["name"] == "Luna's Lore"
    assert lorebooks[0]["linked_character"] == "Luna"
    print("✓ Character-linked lorebook created successfully")
    return lm

def test_system_prompt_without_character():
    """Test system prompt generation without character."""
    print("\nTest 3: System prompt without character (only global lorebooks)...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    # Create global lorebook
    lm.create_lorebook("Global", "Global lore", enabled=True, linked_character=None)
    lm.add_or_update_entry(
        "World Rule",
        "The world is flat",
        keywords=["world"],
        activation_type="constant",
        lorebook_name="Global"
    )
    
    # Create character-linked lorebook
    lm.create_lorebook("Luna's Lore", "Luna lore", enabled=True, linked_character="Luna")
    lm.add_or_update_entry(
        "Luna's Secret",
        "Luna has a secret power",
        keywords=["luna"],
        activation_type="constant",
        lorebook_name="Luna's Lore"
    )
    
    # Get system prompt without character - should only include global
    prompt = lm.get_system_prompt_section("test message", character_name=None)
    
    assert "World Rule" in prompt
    assert "The world is flat" in prompt
    assert "Luna's Secret" not in prompt
    print("✓ System prompt correctly includes only global lorebooks")

def test_system_prompt_with_character():
    """Test system prompt generation with character."""
    print("\nTest 4: System prompt with character (global + character-specific)...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    # Create global lorebook
    lm.create_lorebook("Global", "Global lore", enabled=True, linked_character=None)
    lm.add_or_update_entry(
        "World Rule",
        "The world is flat",
        keywords=["world"],
        activation_type="constant",
        lorebook_name="Global"
    )
    
    # Create Luna-linked lorebook
    lm.create_lorebook("Luna's Lore", "Luna lore", enabled=True, linked_character="Luna")
    lm.add_or_update_entry(
        "Luna's Secret",
        "Luna has a secret power",
        keywords=["luna"],
        activation_type="constant",
        lorebook_name="Luna's Lore"
    )
    
    # Create Sherlock-linked lorebook
    lm.create_lorebook("Sherlock's Lore", "Sherlock lore", enabled=True, linked_character="Sherlock")
    lm.add_or_update_entry(
        "Sherlock's Method",
        "Sherlock uses deductive reasoning",
        keywords=["sherlock"],
        activation_type="constant",
        lorebook_name="Sherlock's Lore"
    )
    
    # Get system prompt with Luna character - should include global + Luna's
    prompt = lm.get_system_prompt_section("test message", character_name="Luna")
    
    assert "World Rule" in prompt
    assert "The world is flat" in prompt
    assert "Luna's Secret" in prompt
    assert "Luna has a secret power" in prompt
    assert "Sherlock's Method" not in prompt
    print("✓ System prompt correctly includes global + Luna's lorebooks")
    
    # Get system prompt with Sherlock character
    prompt = lm.get_system_prompt_section("test message", character_name="Sherlock")
    
    assert "World Rule" in prompt
    assert "Sherlock's Method" in prompt
    assert "Luna's Secret" not in prompt
    print("✓ System prompt correctly includes global + Sherlock's lorebooks")

def test_update_linked_character():
    """Test updating a lorebook's linked character."""
    print("\nTest 5: Update lorebook's linked character...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    # Create global lorebook
    lm.create_lorebook("My Lore", "Test lore", enabled=True, linked_character=None)
    
    # Link it to Luna
    lm.update_lorebook_metadata("My Lore", linked_character="Luna")
    lorebook = lm.get_lorebook("My Lore")
    assert lorebook["linked_character"] == "Luna"
    print("✓ Lorebook linked to character")
    
    # Unlink it (set back to global)
    lm.update_lorebook_metadata("My Lore", linked_character="")
    lorebook = lm.get_lorebook("My Lore")
    assert lorebook["linked_character"] is None
    print("✓ Lorebook unlinked (back to global)")

def test_import_export_with_linked_character():
    """Test import/export preserves linked character."""
    print("\nTest 6: Import/export with linked character...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    # Create character-linked lorebook
    lm.create_lorebook("Luna's Lore", "Luna's world", enabled=True, linked_character="Luna")
    lm.add_or_update_entry(
        "Luna's Home",
        "Luna lives on the moon",
        keywords=["home", "moon"],
        activation_type="normal",
        lorebook_name="Luna's Lore"
    )
    
    # Export
    exported = lm.export_lorebook_file("Luna's Lore")
    exported_data = json.loads(exported)
    
    assert exported_data["linked_character"] == "Luna"
    print("✓ Export includes linked_character field")
    
    # Import to new instance
    test_dir2 = "/tmp/test_lorebook2"
    if os.path.exists(test_dir2):
        shutil.rmtree(test_dir2)
    os.makedirs(test_dir2)
    
    lm2 = LorebookManager(test_dir2)
    lm2.import_lorebook_file(exported_data)
    
    lorebook = lm2.get_lorebook("Luna's Lore")
    assert lorebook is not None
    assert lorebook["linked_character"] == "Luna"
    print("✓ Import preserves linked_character field")

def test_disabled_character_lorebook():
    """Test that disabled character-linked lorebooks are not included."""
    print("\nTest 7: Disabled character-linked lorebook...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    # Create enabled character-linked lorebook
    lm.create_lorebook("Luna's Lore", "Luna lore", enabled=True, linked_character="Luna")
    lm.add_or_update_entry(
        "Luna's Secret",
        "Luna has a secret power",
        keywords=["luna"],
        activation_type="constant",
        lorebook_name="Luna's Lore"
    )
    
    # Get system prompt with Luna - should include the lorebook
    prompt = lm.get_system_prompt_section("test", character_name="Luna")
    assert "Luna's Secret" in prompt
    print("✓ Enabled lorebook included")
    
    # Disable the lorebook
    lm.disable_lorebook("Luna's Lore")
    
    # Get system prompt again - should NOT include the lorebook
    prompt = lm.get_system_prompt_section("test", character_name="Luna")
    assert "Luna's Secret" not in prompt
    print("✓ Disabled lorebook excluded")

def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Character-Linked Lorebook Feature")
    print("=" * 60)
    
    try:
        test_create_global_lorebook()
        test_create_character_linked_lorebook()
        test_system_prompt_without_character()
        test_system_prompt_with_character()
        test_update_linked_character()
        test_import_export_with_linked_character()
        test_disabled_character_lorebook()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
