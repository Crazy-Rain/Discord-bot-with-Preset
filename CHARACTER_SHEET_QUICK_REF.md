# Character Sheet Quick Reference

## Discord Commands

### Set Character Sheet
```
!set_sheet <Character Name> <Sheet Content>
```
Example:
```
!set_sheet Alice Abilities: Flight, Super Strength. Perks: Enhanced Reflexes
```

### Enable Sheet
```
!enable_sheet <Character Name>
```

### Disable Sheet
```
!disable_sheet <Character Name>
```

### View Character (with sheet)
```
!user_char <Character Name>
```

## Web Interface

1. Go to **User Characters** tab
2. Enter character name and description
3. Check **"Enable Character Sheet"** checkbox
4. Enter abilities/perks in **Character Sheet** field
5. Click **Save**

## How It Works

When enabled, the sheet appears in the system prompt like this:

```
[CharacterName Description]
Name: CharacterName
Description: [description]
[sheet]
This is a sheet of CharacterName's Abilities and Perks. 
Always take them into account when considering what CharacterName is able to do.
[abilities and perks]
[/sheet]
Note: This is a User Character...
[/CharacterName Description]
```

## Example

```
!update Alice: A brave warrior with silver armor and red hair.
!set_sheet Alice Abilities: Flight (300 mph), Super Strength (50 tons), Energy Shield. Weaknesses: Magic, Darkness
!enable_sheet Alice
!chat Alice: "I'll fly up to scout ahead!" *takes flight*
```

The AI will now know Alice can fly and respond appropriately.

## Tips

- **Draft First**: Create sheet while disabled, enable when ready
- **Be Specific**: Include limits and weaknesses
- **Toggle Freely**: Disable temporarily without losing data
- **Keep Concise**: Focus on key abilities for better AI context

## Sheet Format Examples

**Simple List:**
```
Abilities: Flight, Super Strength, Telekinesis
Perks: Night Vision, Healing Factor
```

**Categorized:**
```
Physical: Super Strength, Enhanced Speed
Mental: Telepathy, Mind Control
Special: Regeneration
```

**Detailed:**
```
Flight: Up to 500 mph, max altitude 10,000 ft
Strength: Can lift 50 tons
Weakness: Vulnerable to magic attacks
```

## See Also

- `CHARACTER_SHEET_GUIDE.md` - Full user guide
- `CHARACTER_SHEET_IMPLEMENTATION.md` - Technical details
- `USER_CHARACTERS_GUIDE.md` - Basic user character features
