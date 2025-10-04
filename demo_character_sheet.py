#!/usr/bin/env python3
"""
Demo script to show character sheet feature in action.
This creates a sample character with abilities and shows how it appears in the system prompt.
"""

import json
import tempfile
import shutil
from user_characters_manager import UserCharactersManager

def main():
    print("="*70)
    print("CHARACTER SHEET FEATURE DEMONSTRATION")
    print("="*70)
    
    # Create temporary directory for demo
    demo_dir = tempfile.mkdtemp()
    
    try:
        manager = UserCharactersManager(demo_dir)
        
        # Example 1: Create a superhero character with abilities
        print("\n1. Creating a superhero character 'Phoenix'...")
        manager.add_or_update_character(
            name="Phoenix",
            description="A fiery hero with red and gold armor, known for her bravery and fierce determination. She has flowing red hair and golden eyes that glow when using her powers.",
            sheet="""Combat Abilities:
- Fire Manipulation: Can create and control flames up to 2000°F
- Flight: Can fly at speeds up to 300 mph
- Regeneration: Heals from injuries at 10x normal rate

Special Powers:
- Phoenix Force: When critically injured, can resurrect with full health (once per day)
- Heat Resistance: Immune to fire and extreme heat
- Energy Blasts: Can shoot concentrated fire beams from hands

Weaknesses:
- Water-based attacks deal 2x damage
- Powers weaken in cold environments
- Resurrection ability has 24-hour cooldown""",
            sheet_enabled=True
        )
        
        # Example 2: Create a wizard character
        print("2. Creating a wizard character 'Merlin'...")
        manager.add_or_update_character(
            name="Merlin",
            description="An ancient wizard with a long white beard and purple robes adorned with silver stars. His eyes sparkle with centuries of knowledge.",
            sheet="""Magical Abilities:
- Teleportation: Can teleport up to 100 miles
- Elemental Magic: Control over fire, water, earth, and air
- Illusions: Can create realistic illusions to deceive enemies
- Time Magic: Can slow time in a 10-foot radius for up to 30 seconds

Artifacts:
- Staff of Power: Amplifies all magic by 50%
- Amulet of Protection: Provides magical shield

Limitations:
- Must speak incantations for complex spells
- Cannot use magic while holding iron objects
- Time magic requires 1 hour cooldown between uses""",
            sheet_enabled=True
        )
        
        # Example 3: Regular character without special abilities
        print("3. Creating a regular character 'Bob' (no sheet)...")
        manager.add_or_update_character(
            name="Bob",
            description="A skilled merchant with a friendly smile. He's great at negotiating deals and has contacts all over the kingdom."
        )
        
        print("\n" + "="*70)
        print("SYSTEM PROMPT GENERATION")
        print("="*70)
        
        # Show how Phoenix appears in the system prompt
        print("\n📋 Phoenix's System Prompt (with sheet enabled):")
        print("-"*70)
        phoenix_prompt = manager.get_system_prompt_section(["Phoenix"])
        print(phoenix_prompt)
        
        # Show how Bob appears (no sheet)
        print("\n📋 Bob's System Prompt (no sheet):")
        print("-"*70)
        bob_prompt = manager.get_system_prompt_section(["Bob"])
        print(bob_prompt)
        
        # Show multiple characters
        print("\n📋 Combined System Prompt (Phoenix + Merlin + Bob):")
        print("-"*70)
        combined_prompt = manager.get_system_prompt_section(["Phoenix", "Merlin", "Bob"])
        print(combined_prompt)
        
        # Demonstrate disabling a sheet
        print("\n" + "="*70)
        print("TESTING SHEET ENABLE/DISABLE")
        print("="*70)
        
        print("\n4. Disabling Phoenix's character sheet...")
        manager.set_sheet_enabled("Phoenix", False)
        
        print("\n📋 Phoenix's System Prompt (with sheet disabled):")
        print("-"*70)
        phoenix_disabled = manager.get_system_prompt_section(["Phoenix"])
        print(phoenix_disabled)
        print("\n✓ Notice: The [sheet] block is not present when disabled!")
        
        # Re-enable it
        print("\n5. Re-enabling Phoenix's character sheet...")
        manager.set_sheet_enabled("Phoenix", True)
        phoenix_enabled = manager.get_system_prompt_section(["Phoenix"])
        print("\n📋 Phoenix's System Prompt (with sheet re-enabled):")
        print("-"*70)
        print(phoenix_enabled)
        print("\n✓ The [sheet] block is back!")
        
        print("\n" + "="*70)
        print("DEMONSTRATION COMPLETE")
        print("="*70)
        print("\n✨ Key Points:")
        print("  • Character sheets add special abilities and perks to characters")
        print("  • Sheets are wrapped in [sheet][/sheet] tags in the system prompt")
        print("  • The AI is instructed to consider these abilities")
        print("  • Sheets can be enabled/disabled without losing the data")
        print("  • Characters work fine without sheets (like Bob)")
        print("\n📚 See CHARACTER_SHEET_GUIDE.md for detailed usage instructions")
        
    finally:
        # Cleanup
        shutil.rmtree(demo_dir)

if __name__ == "__main__":
    main()
