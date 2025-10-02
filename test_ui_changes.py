#!/usr/bin/env python3
"""Simple test to verify the UI changes work correctly."""
import os
import sys

def test_html_has_multi_character_ui():
    """Test that HTML file contains the new multi-character UI elements."""
    print("Test: HTML contains multi-character UI...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Check for new elements
    assert 'new-lorebook-character-selector' in html_content, "Missing new character selector in create dialog"
    assert 'new-lorebook-linked-characters' in html_content, "Missing new linked characters display in create dialog"
    assert 'edit-lorebook-character-selector' in html_content, "Missing edit character selector"
    assert 'edit-lorebook-linked-characters' in html_content, "Missing edit linked characters display"
    assert 'addCharacterToNewLorebook' in html_content, "Missing add character function for new lorebook"
    assert 'addCharacterToEditLorebook' in html_content, "Missing add character function for edit lorebook"
    assert 'removeCharacterFromNewLorebook' in html_content, "Missing remove character function for new lorebook"
    assert 'removeCharacterFromEditLorebook' in html_content, "Missing remove character function for edit lorebook"
    assert 'linked_characters' in html_content, "Missing linked_characters field in JavaScript"
    
    # Check for backward compatibility
    assert 'linked_character' in html_content, "Should still support linked_character for backward compatibility"
    
    print("✓ HTML contains all required multi-character UI elements")

def test_html_display_logic():
    """Test that display logic handles multiple characters."""
    print("\nTest: HTML display logic supports multiple characters...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Check display logic
    assert 'lb.linked_characters' in html_content, "Missing linked_characters check in list display"
    assert 'lorebook.linked_characters' in html_content, "Missing linked_characters check in detail display"
    assert '.join' in html_content, "Missing join logic for displaying multiple characters"
    
    print("✓ HTML display logic supports multiple characters")

def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Multi-Character UI Changes")
    print("=" * 60)
    
    try:
        test_html_has_multi_character_ui()
        test_html_display_logic()
        
        print("\n" + "=" * 60)
        print("✓ All UI tests passed!")
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
