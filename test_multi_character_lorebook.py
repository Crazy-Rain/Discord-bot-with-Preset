#!/usr/bin/env python3
"""Test multi-character lorebook functionality."""
import os
import sys
import json
import shutil
from lorebook_manager import LorebookManager

def setup_test_env():
    """Set up test environment."""
    test_dir = "/tmp/test_lorebook_multi"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    return test_dir

def test_create_multi_character_lorebook():
    """Test creating a lorebook linked to multiple characters."""
    print("Test 1: Create multi-character lorebook...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    lm.create_lorebook("Shared Lore", "Lore for multiple characters", 
                      enabled=True, linked_characters=["Luna", "Sherlock", "Alice"])
    lm.add_or_update_entry(
        "Team History",
        "Luna, Sherlock, and Alice worked together in the past",
        keywords=["team", "history"],
        activation_type="constant",
        lorebook_name="Shared Lore"
    )
    
    lorebooks = lm.list_lorebooks()
    assert len(lorebooks) == 1
    assert lorebooks[0]["name"] == "Shared Lore"
    assert lorebooks[0]["linked_characters"] == ["Luna", "Sherlock", "Alice"]
    print("✓ Multi-character lorebook created successfully")
    return lm

def test_system_prompt_with_multi_character():
    """Test system prompt includes lorebook for any of the linked characters."""
    print("\nTest 2: System prompt with multiple characters...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    # Create global lorebook
    lm.create_lorebook("Global", "Global lore", enabled=True, linked_characters=None)
    lm.add_or_update_entry(
        "World Rule",
        "The world is flat",
        keywords=["world"],
        activation_type="constant",
        lorebook_name="Global"
    )
    
    # Create multi-character lorebook
    lm.create_lorebook("Team Lore", "Shared lore", enabled=True, 
                      linked_characters=["Luna", "Sherlock"])
    lm.add_or_update_entry(
        "Team Secret",
        "The team has a secret base",
        keywords=["team"],
        activation_type="constant",
        lorebook_name="Team Lore"
    )
    
    # Create Luna-only lorebook
    lm.create_lorebook("Luna's Lore", "Luna lore", enabled=True, 
                      linked_characters=["Luna"])
    lm.add_or_update_entry(
        "Luna's Power",
        "Luna has moonlight powers",
        keywords=["luna"],
        activation_type="constant",
        lorebook_name="Luna's Lore"
    )
    
    # Test with Luna - should include global + team + Luna's
    prompt = lm.get_system_prompt_section("test", character_name="Luna")
    assert "World Rule" in prompt
    assert "Team Secret" in prompt
    assert "Luna's Power" in prompt
    print("✓ Luna's prompt includes global + team + Luna-specific")
    
    # Test with Sherlock - should include global + team (but not Luna's)
    prompt = lm.get_system_prompt_section("test", character_name="Sherlock")
    assert "World Rule" in prompt
    assert "Team Secret" in prompt
    assert "Luna's Power" not in prompt
    print("✓ Sherlock's prompt includes global + team (excludes Luna-specific)")
    
    # Test with Alice - should include only global (not team or Luna's)
    prompt = lm.get_system_prompt_section("test", character_name="Alice")
    assert "World Rule" in prompt
    assert "Team Secret" not in prompt
    assert "Luna's Power" not in prompt
    print("✓ Alice's prompt includes only global")

def test_update_to_multi_character():
    """Test updating a lorebook from single to multiple characters."""
    print("\nTest 3: Update lorebook to multiple characters...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    # Create single-character lorebook
    lm.create_lorebook("My Lore", "Test lore", enabled=True, linked_character="Luna")
    lorebook = lm.get_lorebook("My Lore")
    assert lorebook["linked_characters"] == ["Luna"]
    print("✓ Single-character lorebook created")
    
    # Update to multiple characters
    lm.update_lorebook_metadata("My Lore", linked_characters=["Luna", "Sherlock", "Alice"])
    lorebook = lm.get_lorebook("My Lore")
    assert lorebook["linked_characters"] == ["Luna", "Sherlock", "Alice"]
    print("✓ Updated to multiple characters")
    
    # Update to remove one character
    lm.update_lorebook_metadata("My Lore", linked_characters=["Luna", "Alice"])
    lorebook = lm.get_lorebook("My Lore")
    assert lorebook["linked_characters"] == ["Luna", "Alice"]
    print("✓ Removed one character from list")
    
    # Update to make it global
    lm.update_lorebook_metadata("My Lore", linked_characters=[])
    lorebook = lm.get_lorebook("My Lore")
    assert lorebook["linked_characters"] is None
    print("✓ Updated to global")

def test_import_export_multi_character():
    """Test import/export preserves multiple characters."""
    print("\nTest 4: Import/export with multiple characters...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    # Create multi-character lorebook
    lm.create_lorebook("Team Lore", "Team world", enabled=True, 
                      linked_characters=["Luna", "Sherlock", "Alice"])
    lm.add_or_update_entry(
        "Team Home",
        "The team lives in a castle",
        keywords=["home", "castle"],
        activation_type="normal",
        lorebook_name="Team Lore"
    )
    
    # Export
    exported = lm.export_lorebook_file("Team Lore")
    exported_data = json.loads(exported)
    
    assert exported_data["linked_characters"] == ["Luna", "Sherlock", "Alice"]
    print("✓ Export includes linked_characters list")
    
    # Import to new instance
    test_dir2 = "/tmp/test_lorebook_multi2"
    if os.path.exists(test_dir2):
        shutil.rmtree(test_dir2)
    os.makedirs(test_dir2)
    
    lm2 = LorebookManager(test_dir2)
    lm2.import_lorebook_file(exported_data)
    
    lorebook = lm2.get_lorebook("Team Lore")
    assert lorebook is not None
    assert lorebook["linked_characters"] == ["Luna", "Sherlock", "Alice"]
    print("✓ Import preserves linked_characters list")

def test_backward_compatibility_single_to_multi():
    """Test that old single-character lorebooks are migrated correctly."""
    print("\nTest 5: Backward compatibility - single to multi migration...")
    test_dir = setup_test_env()
    
    # Manually create old-format lorebook
    lorebooks_data = {
        "Old Lore": {
            "name": "Old Lore",
            "description": "Old format",
            "enabled": True,
            "linked_character": "Luna",
            "entries": {
                "Old Entry": {
                    "key": "Old Entry",
                    "content": "Old content",
                    "keywords": ["old"],
                    "activation_type": "normal"
                }
            }
        }
    }
    
    lorebooks_path = os.path.join(test_dir, "lorebooks.json")
    with open(lorebooks_path, "w") as f:
        json.dump(lorebooks_data, f)
    
    # Load with new LorebookManager - should migrate
    lm = LorebookManager(test_dir)
    lorebook = lm.get_lorebook("Old Lore")
    
    assert lorebook is not None
    assert lorebook["linked_characters"] == ["Luna"]
    assert "linked_character" not in lm.lorebooks["Old Lore"]  # Old field should be removed from internal storage
    print("✓ Old single-character format migrated to list")

def test_empty_list_is_global():
    """Test that empty list is treated as global."""
    print("\nTest 6: Empty list is treated as global...")
    test_dir = setup_test_env()
    lm = LorebookManager(test_dir)
    
    # Create with empty list
    lm.create_lorebook("Empty List", "Test", enabled=True, linked_characters=[])
    lm.add_or_update_entry(
        "Global Entry",
        "This is global",
        keywords=["global"],
        activation_type="constant",
        lorebook_name="Empty List"
    )
    
    lorebook = lm.get_lorebook("Empty List")
    assert lorebook["linked_characters"] is None
    print("✓ Empty list converted to None (global)")
    
    # Verify it's included for all characters
    prompt = lm.get_system_prompt_section("test", character_name="Luna")
    assert "Global Entry" in prompt
    
    prompt = lm.get_system_prompt_section("test", character_name="Anyone")
    assert "Global Entry" in prompt
    print("✓ Global lorebook included for all characters")

def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Multi-Character Lorebook Feature")
    print("=" * 60)
    
    try:
        test_create_multi_character_lorebook()
        test_system_prompt_with_multi_character()
        test_update_to_multi_character()
        test_import_export_multi_character()
        test_backward_compatibility_single_to_multi()
        test_empty_list_is_global()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
