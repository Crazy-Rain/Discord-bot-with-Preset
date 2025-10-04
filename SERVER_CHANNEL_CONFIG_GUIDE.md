# Server Configuration Guide

## Overview

The **Servers/Channels** tab in the web configuration interface allows you to configure settings for each Discord server the bot is active in. This gives you server-wide control over how the bot behaves.

**Important Note:** Channel-specific configurations set via Discord commands (`!preset`, `!character`) will override server-level settings. This allows for flexibility when you need per-channel customization.

## Features

### Per-Server Configuration
For each server, you can configure:

1. **Preset** - Choose which conversation preset to use across all channels
   - Options: Default Preset, or any saved preset (creative, analytical, etc.)
   - If set to "Default Preset", uses the global default preset
   - Can be overridden per-channel using `!preset <name>` command

2. **API Config** - Choose which API configuration to use across all channels
   - Options: Default API Config, or any saved API configuration
   - If set to "Default API Config", uses the global API settings
   - Can be overridden per-channel using Discord commands

3. **Character** - Choose which character card to use across all channels
   - Options: No Character, or any available character card (luna, aria, sherlock, etc.)
   - If set to "No Character", bot responds without a character persona
   - Can be overridden per-channel using `!character <name>` command

## How to Use

### Accessing the Tab
1. Navigate to the web interface at `http://localhost:5000`
2. Click on the **Servers/Channels** tab

### Viewing Servers
- All servers the bot is connected to are displayed
- Each server shows its name and the number of text channels

### Configuring a Server
1. Find the server you want to configure
2. Select values from the three dropdowns:
   - **Preset**: Choose the conversation preset for all channels in this server
   - **API Config**: Choose the API configuration for all channels in this server
   - **Character**: Choose the character card for all channels in this server
3. Click the **💾 Save Configuration** button for that server
4. A success message will appear confirming the save

### Per-Channel Overrides
If you need different settings for specific channels, you can use Discord commands:
- `!preset <preset_name>` - Set a channel-specific preset
- `!character <character_name>` - Set a channel-specific character
- These will override the server-level settings for that channel only

### Refreshing the List
- Click the **🔄 Refresh Servers** button to reload the server list
- This is useful if you've added the bot to new servers

## Configuration Persistence

- All server configurations are saved to `config.json`
- Configurations persist across bot restarts
- Each server's settings are stored independently
- Empty/default values are fully supported
- Channel-specific memory (conversation history) is preserved per channel
- Channel overrides (set via Discord commands) are also saved to `config.json`

## Configuration Priority

The bot uses the following priority order when determining which configuration to use:

1. **Channel-specific config** (set via Discord commands like `!preset`, `!character`)
2. **Server-level config** (set via web interface)
3. **Default/global config** (set in Configuration tab)

This allows you to:
- Set server-wide defaults in the web interface
- Override for specific channels using Discord commands
- Fall back to global defaults when nothing is configured

## Use Cases

### Example 1: Server-Wide Preset
- Configure "creative" preset for the entire "Roleplay Server"
- All channels in that server use the creative preset
- Override #serious-discussion with "analytical" preset using `!preset analytical`

### Example 2: Different Servers, Different Characters
- "Luna Fan Server" - Use "luna" character for all channels
- "Sherlock Mystery Server" - Use "sherlock" character for all channels
- "General Discord" - No character (normal bot responses)

### Example 3: API Configs by Server
- "Production Server" - Use "OpenAI GPT-4" API config
- "Testing Server" - Use "Local Ollama" API config
- Other servers - Use default API config

## Technical Details

### API Endpoints
- `GET /api/servers` - Retrieves all servers with current configs (includes server-level settings)
- `POST /api/server_config/<server_id>` - Saves configuration for a specific server
- `POST /api/channel_config/<channel_id>` - Saves configuration for a specific channel (via Discord commands)

### Configuration Storage
Configurations are stored in `config.json` under the `server_configs` and `channel_configs` keys:

```json
{
  "server_configs": {
    "987654321": {
      "preset": "creative",
      "api_config": "my_api",
      "character": "luna"
    }
  },
  "channel_configs": {
    "123456789": {
      "preset": "analytical",
      "api_config": "",
      "character": ""
    }
  }
}
```

### Memory/Conversation History
- **Conversation history is stored per channel** (not per server)
- Each channel maintains its own conversation context
- Changing server or channel configurations does NOT clear conversation history
- Use `!clear` command to clear a channel's conversation history

## Notes

- The bot must be running and connected to Discord to see servers
- Configuration changes take effect immediately (no bot restart needed)
- If a preset, API config, or character is deleted, the bot will fall back to the next priority level
- Server-level configuration simplifies management for large Discord servers
- Channel-specific overrides via Discord commands remain available for flexibility
