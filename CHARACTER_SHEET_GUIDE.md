# Character Sheet Feature Guide

## Overview

The Character Sheet feature allows you to add special abilities, perks, and powers to your user characters. When enabled, the character sheet is sent to the AI along with the character description, instructing the AI to always consider these abilities when determining what the character can do.

## Key Concepts

- **Character Sheet**: A text field containing the character's special abilities, perks, or powers
- **Sheet Enabled**: A toggle that controls whether the sheet is sent to the AI
- **Sheet Block**: The sheet is wrapped in `[sheet][/sheet]` tags in the system prompt
- **AI Instructions**: The AI is explicitly told to consider these abilities when the character acts

## Using the Web Interface

### Adding a Character Sheet

1. Navigate to the **User Characters** tab
2. Enter or select a character name
3. Fill in the character description (required)
4. Check the **"Enable Character Sheet"** checkbox
5. Enter the character's abilities and perks in the **Character Sheet** field
6. Click **"Save User Character"**

### Example Character Sheet

```
Abilities: Flight, Super Strength, Energy Manipulation
Perks: Enhanced Reflexes, Night Vision, Healing Factor
Weaknesses: Vulnerable to magic, loses power in darkness
```

### Character Sheet Format

The sheet can be formatted however you like. Common formats include:

**List Format:**
```
Abilities: Flight, Super Strength
Perks: Enhanced Reflexes
```

**Categorized Format:**
```
Physical Abilities:
- Super Strength
- Enhanced Speed
- Flight

Mental Powers:
- Telepathy
- Mind Reading

Special Perks:
- Healing Factor
- Night Vision
```

**Detailed Format:**
```
Flight: Can fly at speeds up to 500 mph
Super Strength: Can lift up to 50 tons
Energy Manipulation: Can create and control energy blasts
```

## Using Discord Commands

### Set a Character Sheet

```
!set_sheet <Character Name> <Sheet Content>
```

Example:
```
!set_sheet Alice Abilities: Flight, Super Strength. Perks: Enhanced Reflexes, Night Vision
```

### Enable Character Sheet

```
!enable_sheet <Character Name>
```

Example:
```
!enable_sheet Alice
```

### Disable Character Sheet

```
!disable_sheet <Character Name>
```

Example:
```
!disable_sheet Alice
```

### View Character with Sheet

```
!user_char <Character Name>
```

This shows the character's description and sheet (with enabled/disabled status).

Example:
```
!user_char Alice
```

## How It Works

When a character sheet is enabled, it's included in the system prompt like this:

```
[Alice Description]
Name: Alice
Description: A brave warrior with long red hair and green eyes...
[sheet]
This is a sheet of Alice's Abilities and Perks. Always take them into account when considering what Alice is able to do.
Abilities: Flight, Super Strength
Perks: Enhanced Reflexes, Night Vision
[/sheet]
Note: This is a User Character, for referencing when Alice is doing something, In scene, or needing to be referenced in some manner. Do not Act, or Write for this Character, they are only for the Human to Act/Write/Play as.
[/Alice Description]
```

The AI will:
1. See the character's abilities and perks
2. Be instructed to consider them when Alice acts
3. Not act as Alice (still controlled by the human)

## Example Usage

### Setup

```
!update Alice: A brave warrior with long red hair and green eyes, wearing silver armor.
!set_sheet Alice Abilities: Flight, Super Strength, Energy Shield. Perks: Enhanced Reflexes, Battle Tactics Expertise
!enable_sheet Alice
```

### In Roleplay

```
!chat Alice: "I need to reach the tower quickly!" *prepares to take flight*
```

The AI will understand that Alice can fly and will respond accordingly:

```
The tower looms high above, at least 200 feet tall. With Alice's flight ability, 
she could easily reach the top in seconds. The wind picks up as she prepares to 
launch herself skyward...
```

## Visibility Control

The sheet is **only sent to the AI when enabled**. This allows you to:

1. **Draft a sheet** without it affecting the AI (disabled)
2. **Enable it** when you want the AI to know about those abilities
3. **Disable it** if circumstances change (character loses powers, different scenario, etc.)

## Backward Compatibility

- Characters created before this feature automatically have no sheet (disabled)
- Updating a character's description preserves the existing sheet
- The old `!update` command works the same way (doesn't modify sheets)
- Sheet data is optional - characters work fine without it

## Best Practices

### Good Character Sheets

✅ **Be Specific**:
```
Flight: Can fly at speeds up to 500 mph, max altitude 10,000 feet
```

✅ **Include Limitations**:
```
Super Strength: Can lift 50 tons, but only for short bursts
```

✅ **Organize by Category**:
```
Combat Abilities: Super Strength, Energy Blasts
Utility Powers: Flight, Force Fields
```

### When to Use Sheets

- **Superpowered characters** with abilities beyond human limits
- **Fantasy characters** with magic or special skills
- **Sci-fi characters** with cybernetic enhancements or alien abilities
- **Any character** with unusual capabilities the AI should know about

### When NOT to Use Sheets

- Regular human characters without special abilities
- When abilities are already well-described in the character description
- For simple personality traits (those go in the description)

## Tips

1. **Start Disabled**: Create the character first, then add and enable the sheet
2. **Update as Needed**: Use `!set_sheet` to modify abilities as the story progresses
3. **Toggle On/Off**: Disable the sheet temporarily if the character loses powers
4. **Combine with Description**: The sheet complements, doesn't replace, the description
5. **Test the Output**: Use `!user_char` to see how it looks before using in roleplay

## Troubleshooting

### Sheet Not Appearing in AI Responses

1. Make sure the sheet is **enabled** (`!enable_sheet <name>`)
2. Verify the character name matches exactly
3. Check that you're using the character name in your `!chat` messages
4. Use `!user_char <name>` to confirm the sheet is saved and enabled

### Sheet Not Preserved When Updating

- Use the web interface to update both description and sheet together
- Or use `!set_sheet` separately to update just the sheet
- The `!update` command only changes the description, preserving the sheet

### Sheet Too Long

- Keep it concise - focus on key abilities
- Use bullet points or short descriptions
- Remember the AI has token limits for context

## Integration with Other Features

### With Lorebook

- **Lorebook**: World information, lore, locations, NPCs
- **Character Sheet**: Individual character abilities and perks
- They work together to give the AI complete context

### With Character Cards

- **AI Character Card**: The AI's personality and behavior
- **User Character Description**: Who the human is playing
- **User Character Sheet**: What special abilities the human's character has

All three can be active simultaneously for rich roleplay.

## File Storage

Character sheets are stored in:
```
user_characters/user_characters.json
```

Example structure:
```json
{
  "Alice": {
    "name": "Alice",
    "description": "A brave warrior...",
    "sheet": "Abilities: Flight, Super Strength",
    "sheet_enabled": true
  }
}
```

## Questions?

For more information:
- See `USER_CHARACTERS_GUIDE.md` for basic user character features
- Use `!help_bot` in Discord for command help
- Check the main `README.md` for general bot usage
