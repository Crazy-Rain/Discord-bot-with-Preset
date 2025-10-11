# Manual Send and Context Optimization Implementation

## Overview
This update implements two major feature sets:
1. **Manual Send Mode** - Allows manual message sending via web UI without AI API calls
2. **Context Optimization** - Simplified context structure and intelligent token limiting

## Features Implemented

### 1. Manual Send Mode

#### Web UI Components
- **New "Manual Send" tab** in the web interface
  - Channel selection dropdown (fetches all channels bot has access to)
  - Character selection dropdown (loads from available characters)
  - Message textarea for composing messages
  - Send button to dispatch messages
  
- **Manual Send Mode toggle** in Configuration tab
  - When enabled, blocks all API calls from !chat command
  - Forces use of Manual Send tab for all bot responses
  - Useful for manual roleplay without AI involvement

#### Backend Implementation
- New API endpoint: `GET /api/manual_send/channels` - Lists all accessible Discord channels
- New API endpoint: `POST /api/manual_send` - Sends message as selected character to chosen channel
- Discord bot checks `manual_send_enabled` config before making API calls
- Messages sent via webhook as the selected character (with avatar/name)

### 2. Context Restructuring

#### Simplified Preset Logic
- **Removed channel/server preset overrides** - Now uses global default preset only
- All channels use the same preset from Configuration → Default Preset
- Simplifies configuration and ensures consistent behavior

#### Simplified Lorebook Logic  
- **Removed character linking** - Lorebooks no longer tied to specific characters
- All **active** lorebooks are checked for triggered entries
- Entries with "constant" activation are always included
- Entries with keyword triggers are included when keywords match
- More predictable and easier to manage

#### Context Components (in order)
1. **Preset** - Global default preset from Configuration tab
2. **Character** - Per-channel character set via !character command (preserved)
3. **User Character** - Name, description, and character sheet (if enabled)
4. **Lorebook** - Active lorebooks with triggered/constant entries
5. **Channel Messages** - Previous !chat messages and bot responses

### 3. Token Limit Optimization

#### Intelligent Token Trimming
- Estimates token count using ~4 characters per token ratio
- Compares total context against `max_tokens` from preset
- Automatically trims oldest messages to fit within limit
- **Preservation priorities:**
  1. System messages (always kept)
  2. Current user message (always kept)
  3. Recent conversation history (kept as space allows)
  4. Oldest messages trimmed first

#### Debug Logging
- Logs estimated token counts before/after trimming
- Shows number of messages trimmed
- Helps diagnose context limit issues

## Configuration

### New Config Fields

```json
{
  "manual_send_enabled": false  // Enable Manual Send Mode (blocks API calls)
}
```

### Updated Context Flow

When `!chat` is used:
1. Check if `manual_send_enabled` - if true, reject with message
2. Load global default preset (no channel/server overrides)
3. Get per-channel character (if set via !character)
4. Build context with user characters + active lorebooks
5. Add conversation history from channel
6. Trim to fit within `max_tokens` limit
7. Send to API

## API Endpoints

### Manual Send Endpoints
- `GET /api/manual_send/channels` - Get all channels bot can access
- `POST /api/manual_send` - Send manual message
  ```json
  {
    "channel_id": "123456789",
    "character_name": "luna",
    "message": "Hello from the web interface!"
  }
  ```

## Testing

Automated tests added in `test_manual_send_context.py`:
- ✅ Token estimation accuracy
- ✅ Message trimming preserves system messages
- ✅ Message trimming preserves current message
- ✅ Message trimming respects token limits
- ✅ Preset logic returns global default only

## Screenshots

### Manual Send Tab
![Manual Send Tab](https://github.com/user-attachments/assets/0eae23a6-dd20-45b5-b60f-53243fad6814)

### Manual Send Mode Toggle
![Manual Send Mode](https://github.com/user-attachments/assets/6e823efb-2ebc-4053-a579-a02ce7c2090e)

### Configuration Tab
![Configuration](https://github.com/user-attachments/assets/518ea279-5ca4-46ed-a29e-3ea2b959181d)

## Breaking Changes

⚠️ **Preset Configuration**: Channel and server-specific preset configurations are no longer used. All channels now use the global default preset.

⚠️ **Lorebook Character Linking**: Lorebooks are no longer linked to specific characters. All active lorebooks apply globally.

## Migration Guide

1. **Presets**: Review your default preset in Configuration tab - this will apply to all channels
2. **Lorebooks**: Review active lorebooks - they will apply regardless of character
3. **Manual Send**: Enable Manual Send Mode in Configuration to block AI calls and use manual sending

## Backward Compatibility

- Per-channel character selection via !character still works
- User characters with sheets still work as before
- !clear and !reload_history commands unchanged
- Conversation history loading unchanged
