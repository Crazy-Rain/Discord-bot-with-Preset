# Quick Troubleshooting Guide

## Bot Configuration Not Updating? 

### The Issue Has Been Fixed! ✅
If you were experiencing issues where changing the proxy/endpoint URL didn't take effect, this has been resolved. The bot now correctly updates when you:

1. Load a saved API configuration
2. Edit the Base URL or Model fields  
3. Click "Save Configuration"

### How to Verify It's Working
1. Open the Bot Configuration page
2. Change the Base URL to a different proxy
3. Click "Save Configuration"
4. Send a message in Discord
5. Check your bot's console - you should see it using the new URL

---

## Lorebooks Not Working?

### Common Issues (All User Error, Not Bugs)

The lorebook system is working correctly. If your lorebooks aren't appearing in AI responses, check these:

#### 1. ✓ Lorebook is Enabled
- In the Lorebook tab, make sure the checkbox next to your lorebook is **checked**
- Disabled lorebooks won't be used even if they have entries

#### 2. ✓ Character Names Match Exactly
- Character names are **case-sensitive**
- If your character is "Luna", the lorebook must be linked to "Luna" (not "luna" or "LUNA")
- Check the character name in the Characters tab matches the lorebook link

#### 3. ✓ Entry Activation Type is Set Correctly
- **Constant** = Always included in every message from ALL enabled lorebooks (even character-linked ones)
- **Normal** = Only included when keywords appear in the message AND (for character-linked lorebooks) the character is active
- **Vectorized** = Currently works the same as Normal (semantic search not yet implemented)

**Important**: Character links only affect Normal/Vectorized entries. Constant entries are ALWAYS included, matching SillyTavern behavior.

#### 4. ✓ Entries Actually Exist
- Make sure you've created entries in your lorebook
- Click on the lorebook name and check the entries list
- Each entry needs:
  - Key (name/title)
  - Content (the actual information)
  - Activation type

#### 5. ✓ Character is Loaded for the Channel
- Use `!character <name>` to load a character for the channel
- Character-linked lorebooks only activate when that character is loaded

### How to Debug Lorebooks

When you send a message in Discord, check your bot's **console output** for `[LOREBOOK]` messages:

```
[LOREBOOK] Getting lorebook entries for character: Luna
[LOREBOOK] Total lorebooks: 2
[LOREBOOK] Including lorebook 'Global Lore' (linked_chars: None)
[LOREBOOK]   Added constant entry: Magic System
[LOREBOOK]   Total entries from 'Global Lore': 1
[LOREBOOK] Including lorebook 'Luna Lore' (linked_chars: ['Luna'])
[LOREBOOK]   Added constant entry: Luna's Past
[LOREBOOK]   Total entries from 'Luna Lore': 1
[LOREBOOK] Total entries to include: 2
[LOREBOOK] Added lorebook section (290 chars)
```

#### What to Look For:
- **"Skipping disabled lorebook"** = You need to enable it
- **"Skipping lorebook... (linked_chars: ['X'], current: Y)"** = Character name mismatch
- **"Total entries from '...' : 0"** = No constant entries and no keyword matches
- **"No entries found, returning empty string"** = No lorebooks matched your criteria

### Quick Setup Example

1. **Create a global lorebook** for world rules:
   ```
   Name: World Lore
   Description: Core world information
   Enabled: ✓
   Linked Characters: (leave empty for global)
   ```

2. **Add a constant entry**:
   ```
   Key: Magic System
   Content: Magic is powered by mana crystals...
   Keywords: magic, mana, spell (optional for constant)
   Activation Type: Constant
   ```

3. **Send a test message** and check the console for `[LOREBOOK]` logs

---

## Still Having Issues?

If you've checked all the above and lorebooks still aren't working:

1. **Check the console logs** - They will show exactly what's happening
2. **Verify character name** - Use the exact name from the Characters tab
3. **Test with a global lorebook** - Try without character linking first
4. **Check activation type** - Set to "Constant" for testing
5. **Restart the bot** - Sometimes a clean start helps

The debug logs will show you exactly what the bot is doing, making it easy to spot the issue!
