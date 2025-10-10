#!/usr/bin/env python3
"""
Demonstration of the Lorebook Constant Entry Fix

This script shows the before/after behavior of the fix.
"""

import sys
import os
import shutil

sys.path.insert(0, '/home/runner/work/Discord-bot-with-Preset/Discord-bot-with-Preset')

from lorebook_manager import LorebookManager

def cleanup():
    lorebook_dir = '/home/runner/work/Discord-bot-with-Preset/Discord-bot-with-Preset/lorebook'
    if os.path.exists(lorebook_dir):
        shutil.rmtree(lorebook_dir)

def demonstrate_fix():
    print("=" * 70)
    print("LOREBOOK CONSTANT ENTRY FIX DEMONSTRATION")
    print("=" * 70)
    
    cleanup()
    
    # Setup
    lm = LorebookManager()
    
    # Create a character-linked lorebook with a CONSTANT entry
    lm.create_lorebook(
        name="Luna's Secrets",
        description="Luna's personal information",
        enabled=True,
        linked_characters=["Luna"]
    )
    
    lm.add_or_update_entry(
        key="Luna's Hidden Power",
        content="Luna possesses the ancient power of moonlight manipulation, which affects the entire world's magic system.",
        activation_type="constant",  # This should ALWAYS be included
        lorebook_name="Luna's Secrets"
    )
    
    print("\n📚 Created Lorebook:")
    print("   Name: Luna's Secrets")
    print("   Linked to: Luna")
    print("   Entry: 'Luna's Hidden Power' (constant)")
    print("   Content: Important world-affecting information")
    
    # Test 1: With Luna (should work)
    print("\n" + "-" * 70)
    print("TEST 1: Using Luna character")
    print("-" * 70)
    
    prompt = lm.get_system_prompt_section(
        relevant_text="test message",
        character_name="Luna"
    )
    
    if "Luna's Hidden Power" in prompt:
        print("✅ Entry IS included (expected)")
    else:
        print("❌ Entry NOT included (bug!)")
    
    # Test 2: With a different character (the bug scenario)
    print("\n" + "-" * 70)
    print("TEST 2: Using Alice character (different from Luna)")
    print("-" * 70)
    print("\n🐛 OLD BEHAVIOR (bug):")
    print("   ❌ Entry would NOT be included")
    print("   ❌ Character link was blocking constant entries")
    print("\n✅ NEW BEHAVIOR (fixed):")
    print("   ✅ Entry IS included")
    print("   ✅ Constant entries ignore character links (matches SillyTavern)")
    
    prompt = lm.get_system_prompt_section(
        relevant_text="test message",
        character_name="Alice"
    )
    
    if "Luna's Hidden Power" in prompt:
        print("\n✅ CONFIRMED: Entry IS included (fix is working!)")
    else:
        print("\n❌ FAILED: Entry NOT included (fix not working)")
    
    # Test 3: With NO character (also a bug scenario)
    print("\n" + "-" * 70)
    print("TEST 3: No character loaded")
    print("-" * 70)
    print("\n🐛 OLD BEHAVIOR (bug):")
    print("   ❌ Entry would NOT be included")
    print("\n✅ NEW BEHAVIOR (fixed):")
    print("   ✅ Entry IS included")
    
    prompt = lm.get_system_prompt_section(
        relevant_text="test message",
        character_name=None
    )
    
    if "Luna's Hidden Power" in prompt:
        print("\n✅ CONFIRMED: Entry IS included (fix is working!)")
    else:
        print("\n❌ FAILED: Entry NOT included (fix not working)")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: Why This Matters")
    print("=" * 70)
    print("""
The fix ensures that CONSTANT entries are truly constant:
- They appear in EVERY conversation
- Character links don't affect them
- This matches SillyTavern behavior
- Perfect for world rules, magic systems, and core lore

Use Cases:
✅ "Magic System" (constant) in "World Lore" → Always available
✅ "Luna's Power" (constant) in "Luna's Lore" → Always available
❌ "Luna's Past" (normal) in "Luna's Lore" → Only when Luna is active + keywords match

The bug was making character-linked constant entries behave like normal entries,
which defeated the purpose of having "constant" activation.
    """)
    
    cleanup()

if __name__ == "__main__":
    demonstrate_fix()
