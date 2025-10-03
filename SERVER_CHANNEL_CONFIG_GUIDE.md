# Server/Channel Configuration Guide

## Overview

The **Servers/Channels** tab in the web configuration interface allows you to configure individual settings for each Discord channel the bot is active in. This gives you fine-grained control over how the bot behaves in different channels.

## Features

### Per-Channel Configuration
For each channel, you can configure:

1. **Preset** - Choose which conversation preset to use
   - Options: Default Preset, or any saved preset (creative, analytical, etc.)
   - If set to "Default Preset", uses the global default preset

2. **API Config** - Choose which API configuration to use
   - Options: Default API Config, or any saved API configuration
   - If set to "Default API Config", uses the global API settings

3. **Character** - Choose which character card to use
   - Options: No Character, or any available character card (luna, aria, sherlock, etc.)
   - If set to "No Character", bot responds without a character persona

## How to Use

### Accessing the Tab
1. Navigate to the web interface at `http://localhost:5000`
2. Click on the **Servers/Channels** tab

### Viewing Servers and Channels
- All servers the bot is connected to are displayed
- Each server shows all its text channels in a collapsible section
- Current configuration for each channel is shown in the dropdowns

### Configuring a Channel
1. Find the channel you want to configure
2. Select values from the three dropdowns:
   - **Preset**: Choose the conversation preset
   - **API Config**: Choose the API configuration
   - **Character**: Choose the character card
3. Click the **💾 Save Configuration** button for that channel
4. A success message will appear confirming the save

### Refreshing the List
- Click the **🔄 Refresh Servers** button to reload the server/channel list
- This is useful if you've added the bot to new servers or channels

## Configuration Persistence

- All channel configurations are saved to `config.json`
- Configurations persist across bot restarts
- Each channel's settings are stored independently
- Empty/default values are fully supported

## Use Cases

### Example 1: Different Presets per Channel
- `#general` - Use "analytical" preset for helpful responses
- `#roleplay` - Use "creative" preset for storytelling
- `#bot-commands` - Use default preset

### Example 2: Different Characters per Channel
- `#luna-chat` - Use "luna" character
- `#sherlock-mysteries` - Use "sherlock" character
- `#general` - No character (normal bot responses)

### Example 3: Different API Configs
- `#gpt4-channel` - Use "OpenAI GPT-4" API config
- `#local-llm` - Use "Local Ollama" API config
- Other channels - Use default API config

## Technical Details

### API Endpoints
- `GET /api/servers` - Retrieves all servers and channels with current configs
- `POST /api/channel_config/<channel_id>` - Saves configuration for a specific channel

### Configuration Storage
Configurations are stored in `config.json` under the `channel_configs` key:

```json
{
  "channel_configs": {
    "123456789": {
      "preset": "creative",
      "api_config": "my_api",
      "character": "luna"
    }
  }
}
```

## Notes

- The bot must be running and connected to Discord to see servers/channels
- Only text channels are shown (voice channels are not supported)
- Configuration changes take effect immediately (no bot restart needed)
- If a preset, API config, or character is deleted, the channel will fall back to defaults
