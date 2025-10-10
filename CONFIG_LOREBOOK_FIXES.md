# Bot Configuration and Lorebook Fixes

This document describes the fixes applied to resolve issues with bot configuration updates and lorebook integration.

## Issue 1: Bot Configuration Not Updating (FIXED ✅)

### Problem
When selecting/loading a Proxy or Endpoint URL in the Bot Configuration page and saving, messages in Discord were still being sent to the old URL without updating to the new one.

### Root Cause
The `config_manager.py` module had a critical bug in the `update_config()` method. It was using Python's shallow `dict.update()` which **replaces entire nested dictionaries** instead of merging them.

**Example of the bug:**
```python
# Before update:
config = {
    'openai_config': {
        'api_key': 'sk-secret',
        'base_url': 'https://old-url.com/v1',
        'model': 'gpt-3.5-turbo'
    }
}

# Update sent from web (API key hidden and deleted):
updates = {
    'openai_config': {
        'base_url': 'https://new-url.com/v1',
        'model': 'gpt-4'
    }
}

# After shallow update (BUG!):
config = {
    'openai_config': {
        'base_url': 'https://new-url.com/v1',
        'model': 'gpt-4'
        # ❌ API key is LOST!
    }
}
```

When the API key was displayed as `***HIDDEN***` in the web interface, it was removed from the update data to prevent overwriting. But the shallow `update()` replaced the entire `openai_config` dictionary, causing the API key to be deleted!

### Fix Applied
Implemented a `deep_update()` method that recursively merges nested dictionaries:

```python
def deep_update(self, target: Dict[str, Any], updates: Dict[str, Any]) -> None:
    """Recursively update target dict with updates dict."""
    for key, value in updates.items():
        if key in target and isinstance(target[key], dict) and isinstance(value, dict):
            # Recursively update nested dicts
            self.deep_update(target[key], value)
        else:
            # Replace value
            target[key] = value

def update_config(self, updates: Dict[str, Any]) -> None:
    """Update configuration with new values using deep merge."""
    self.deep_update(self.config, updates)
    self.save_config()
```

### Verification
The fix has been verified to:
- ✅ Preserve API keys when updating other fields
- ✅ Correctly update base URLs and models
- ✅ Apply changes to the running bot immediately
- ✅ Work correctly with channel-specific and server-specific configs

## Issue 2: Lorebook Information Not Being Used (INVESTIGATION COMPLETE ✅)

### Problem
Users reported that despite having lorebooks active and linked to characters, the AI didn't appear to be getting information from them, even for entries set to 'Constant'.

### Investigation Results
After comprehensive testing, **the lorebook functionality is working correctly**. All tests pass:
- ✅ Constant (always active) entries are included
- ✅ Character-linked lorebook filtering works correctly
- ✅ Enabled/disabled lorebook filtering works
- ✅ Lorebooks are properly included in message building
- ✅ Multiple lorebooks can be active simultaneously

### Debug Logging Added
To help users diagnose lorebook issues, comprehensive debug logging has been added:

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

### Common Causes of "Lorebook Not Working"
Since the code is working correctly, if lorebooks seem to not be working, check:

1. **Lorebook is Disabled**: Ensure the lorebook has the "Enabled" checkbox checked
2. **Character Name Mismatch**: The character name must match exactly (case-sensitive)
   - If your character is "Luna", the lorebook must be linked to "Luna" (not "luna" or "LUNA")
3. **Entry Activation Type**: 
   - Set to "Constant" for always-active entries
   - Set to "Normal" and add keywords for context-triggered entries
4. **No Entries Created**: Make sure you've actually added entries to the lorebook
5. **Wrong Lorebook Selected**: Check you're viewing the correct lorebook in the web interface

### How to Verify Lorebooks are Working
When you send a message in Discord, check your bot's console output. You should see `[LOREBOOK]` log messages showing:
- Which character is active
- Which lorebooks are being checked
- Which entries are being included
- How many total entries were added

If you don't see any `[LOREBOOK]` messages, the issue may be with your bot configuration or character setup, not the lorebook system itself.

## Testing
A comprehensive test suite has been added in `test_config_lorebook_fixes.py`:

```bash
python test_config_lorebook_fixes.py
```

All tests pass:
- ✅ Config Update Preserves API Key
- ✅ Bot Receives Updated Config  
- ✅ Lorebook Constant Entries
- ✅ Lorebook Character Filtering
- ✅ Lorebook Enabled/Disabled

## Migration Notes
No migration is needed. The fixes are backward compatible with existing configurations and lorebooks.

## Related Files Modified
- `config_manager.py`: Added `deep_update()` method
- `lorebook_manager.py`: Added debug logging
- `discord_bot.py`: Added debug logging for lorebook integration
- `test_config_lorebook_fixes.py`: Comprehensive test suite
