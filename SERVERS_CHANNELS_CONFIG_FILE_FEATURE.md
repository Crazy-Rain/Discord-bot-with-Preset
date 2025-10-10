# Servers/Channels Page - New Config File Management Feature

## The Problem

Previously, when the bot was not connected to Discord, the Servers/Channels page showed:

```
No servers connected. Make sure the bot is running and connected to Discord.
```

**This was a problem because:**
- Users couldn't access server/channel configurations in their config.json
- They couldn't fix problematic configs (e.g., `"api_config": "my_api"` that doesn't exist)
- The only way to fix these was to manually edit config.json
- These configs might override default settings, causing the main config update issue

## The Solution

Now when the bot is not connected, users see:

```
⚠️ Bot Not Connected to Discord

The bot is not currently connected to Discord, so server and channel 
names are not available. However, you can still manage configurations 
saved in your config file.

[📁 View/Edit Config File Settings]
```

### What Happens When You Click the Button

The page shows all server and channel configurations from your config.json file:

#### Server Configurations
```
🖥️ Server Configurations

┌─────────────────────────────────────────────────┐
│ Server ID: 987654321                            │
│                                                  │
│ Preset: [creative ▼]                            │
│ API Config: [my_api ▼]  ← This might not exist! │
│ Character: [luna ▼]                             │
│                                                  │
│ [💾 Save] [🗑️ Delete]                           │
└─────────────────────────────────────────────────┘
```

#### Channel Configurations
```
💬 Channel Configurations

┌─────────────────────────────────────────────────┐
│ Channel ID: 123456                              │
│                                                  │
│ Preset: [creative ▼]                            │
│ API Config: [my_api ▼]  ← This might not exist! │
│ Character: [luna ▼]                             │
│                                                  │
│ [💾 Save] [🗑️ Delete]                           │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Channel ID: 123457                              │
│                                                  │
│ Preset: [analytical ▼]                          │
│ API Config: [Default API Config ▼]              │
│ Character: [sherlock ▼]                         │
│                                                  │
│ [💾 Save] [🗑️ Delete]                           │
└─────────────────────────────────────────────────┘
```

### How to Fix the Issue

If you have configs referencing non-existent API configs like "my_api":

1. **Option 1: Delete the problematic config**
   - Click "🗑️ Delete" button
   - This removes the server/channel-specific config
   - The channel will use default config instead

2. **Option 2: Change to a valid API config**
   - Select "Default API Config" from the dropdown
   - Or select an existing saved API config
   - Click "💾 Save"

3. **Option 3: Create the missing API config**
   - Go to the Configuration tab
   - Create a saved API config named "my_api"
   - Return to Servers/Channels and the config will now work

## Example Scenario

### Problem
```json
// In config.json
{
  "channel_configs": {
    "123456": {
      "api_config": "my_api",  // ← Doesn't exist!
      "preset": "creative",
      "character": "luna"
    }
  },
  "saved_api_configs": {}  // ← Empty!
}
```

When you try to update the default API config in the Configuration tab, the changes don't affect channel 123456 because it's trying to use "my_api" which doesn't exist.

### Solution Using New Feature

1. Click on "Servers/Channels" tab
2. If bot is not connected, you see the warning
3. Click "📁 View/Edit Config File Settings"
4. Find Channel 123456 in the list
5. Change API Config from "my_api" to "Default API Config"
6. Click "💾 Save"
7. Now the channel will use the default API config from the Configuration tab!

## New API Endpoints

### GET /api/all_configs
Returns all server and channel configs from config.json:
```json
{
  "servers": [
    {
      "id": "987654321",
      "name": "Server 987654321",
      "preset": "creative",
      "api_config": "my_api",
      "character": "luna",
      "from_config": true
    }
  ],
  "channels": [
    {
      "id": "123456",
      "name": "Channel 123456",
      "preset": "creative",
      "api_config": "my_api",
      "character": "luna",
      "from_config": true
    }
  ]
}
```

### DELETE /api/server_config/<server_id>
Deletes a server configuration from config.json

### DELETE /api/channel_config/<channel_id>
Deletes a channel configuration from config.json

## Benefits

1. **No Discord Connection Required**: Manage configs even when bot is offline
2. **Fix Config Issues**: Remove or update problematic configurations
3. **Visibility**: See all server/channel configs even without server names
4. **User-Friendly**: No need to manually edit JSON files
5. **Safe**: Proper validation and error handling

## When to Use This Feature

Use this feature when:
- ✅ Bot is not connected to Discord
- ✅ You need to fix channel/server-specific API configs
- ✅ You want to remove old configs for servers/channels you're no longer using
- ✅ You need to see all configured servers/channels by ID
- ✅ Default config updates aren't working (might be overridden by channel config)

## Related to Main Issue

This feature directly addresses the user's comment:
> "the Servers/Channels page isn't loading any Servers or Channels, so this might be part of why this issue is happening, in that if it has been configured through this section/tab, it would be overriding the Default"

Now users can:
1. Access the Servers/Channels page even without bot connection
2. See and fix channel/server-specific configs that override defaults
3. Remove problematic configs that reference non-existent API settings
4. Verify their config structure is correct
