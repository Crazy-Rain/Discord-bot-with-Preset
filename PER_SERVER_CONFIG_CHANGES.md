# Per-Server Configuration - Change Summary

## What Changed?

The configuration UI has been simplified from **per-channel** to **per-server** configuration while maintaining backward compatibility with channel-specific settings via Discord commands.

## Before (Per-Channel Configuration)

### Web UI:
- ❌ Each channel had its own dropdowns (Preset, API Config, Character)
- ❌ Servers showed collapsible list of all channels
- ❌ Required configuring each channel individually
- ❌ Could be overwhelming for servers with many channels

### Example:
```
Server: My Discord Server (50 channels)
  └─ #general
       ├─ Preset: [dropdown]
       ├─ API Config: [dropdown]
       ├─ Character: [dropdown]
       └─ [Save] button
  └─ #roleplay
       ├─ Preset: [dropdown]
       ├─ API Config: [dropdown]
       ├─ Character: [dropdown]
       └─ [Save] button
  └─ ... (48 more channels)
```

## After (Per-Server Configuration)

### Web UI:
- ✅ Each server has one set of dropdowns (Preset, API Config, Character)
- ✅ Configuration applies to all channels in that server
- ✅ Much simpler - one configuration per server
- ✅ Channel overrides available via Discord commands

### Example:
```
Server: My Discord Server (50 channels)
  ├─ Preset: [dropdown]
  ├─ API Config: [dropdown]
  ├─ Character: [dropdown]
  └─ [Save Configuration] button
  
(Applies to all 50 channels unless overridden)
```

## Configuration Priority

The bot now uses a three-tier priority system:

### 1. Channel Config (Highest Priority)
- Set via Discord commands: `!preset <name>`, `!character <name>`
- Overrides server and default configs
- Stored in `channel_configs`

### 2. Server Config (Medium Priority)
- Set via Web UI (Servers/Channels tab)
- Applies to all channels in the server
- Stored in `server_configs`

### 3. Default Config (Lowest Priority)
- Set via Web UI (Configuration tab)
- Global fallback when nothing else is set
- Stored in `default_preset` and `openai_config`

## What Stays the Same?

### ✅ Conversation History
- **Still stored per channel**
- Each channel maintains its own conversation context
- Not affected by configuration changes

### ✅ Channel Overrides
- Discord commands (`!preset`, `!character`) still work
- Can override server config for specific channels
- Useful for special-purpose channels

### ✅ Backward Compatibility
- Existing `channel_configs` still respected
- No data loss from previous configurations
- Smooth transition

## Use Cases

### Simple Setup (Most Common)
1. Go to Servers/Channels tab
2. Select preset, API config, and character for each server
3. Click Save
4. All channels in that server now use those settings

### Advanced Setup (When Needed)
1. Set server-wide config in Web UI
2. Use Discord commands to override specific channels:
   - `!preset analytical` in #serious-discussion
   - `!character sherlock` in #mystery-channel
3. Override channels use their config, others use server config

## Configuration Storage

### config.json Structure:
```json
{
  "server_configs": {
    "987654321": {
      "preset": "creative",
      "api_config": "openai_gpt4",
      "character": "luna"
    }
  },
  "channel_configs": {
    "123456789": {
      "preset": "analytical",
      "api_config": "",
      "character": "sherlock"
    }
  }
}
```

## Benefits

1. **Simpler Management**: One config per server instead of per channel
2. **Easier Setup**: Configure once for the entire server
3. **Flexibility**: Still allows channel overrides when needed
4. **Better Performance**: Less data to load and manage
5. **Clearer UI**: No more scrolling through hundreds of channels

## Migration Notes

- No migration needed - existing configs continue to work
- Channel configs from before are preserved
- Can gradually move to server-level config at your own pace
