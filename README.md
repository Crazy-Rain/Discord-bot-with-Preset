# Discord Bot with Preset System

A feature-rich Discord bot with OpenAI-compatible API integration, preset management system, and character cards support - similar to SillyTavern!

## ✨ Features

- 🤖 **Discord Bot Integration** - Full-featured Discord bot with conversation history
- 🔌 **Custom OpenAI-Compatible API** - Connect to any OpenAI-compatible endpoint (OpenAI, LM Studio, Ollama, Text Generation WebUI, etc.)
- 🎨 **Advanced Preset System** - SillyTavern-style presets with proper role separation for optimal AI performance
  - **NEW**: Separate system, user, and assistant message roles
  - **NEW**: Character card integration with example dialogues
  - **NEW**: Flexible prompt formatting options
  - **NEW**: Support for uncensored character interactions
- 👤 **Character Cards** - Full SillyTavern-compatible character cards with `first_mes` and `mes_example` support
- 🖼️ **Per-Channel Character Avatars** - Load different characters with unique avatars in each channel using webhooks
  - **NEW**: Bypass Discord's 2-per-hour rate limit!
  - **NEW**: Display different character avatars per channel simultaneously!
  - **NEW**: Unlimited character switches without restrictions!
- 👥 **User Character Descriptions** - Save and manage descriptions for user characters in roleplay scenarios
- 📚 **Lorebook System** - Add world-building and lore information that's contextually included (like SillyTavern)
  - **NEW**: Manage multiple lorebooks, enable/disable them individually, and swap between settings!
- 🔄 **Context Persistence** - Automatically loads channel history to maintain conversation context across bot restarts
- 🌐 **Web Configuration Interface** - Beautiful web UI to manage all settings, presets, characters, and lorebook
- 💾 **Import/Export** - Full import/export functionality for presets, character cards, user characters, and lorebook
- 🔄 **Swipe Functionality** - Generate and navigate through alternative AI responses (like SillyTavern)
- 📊 **Extended Token Limits** - Support for up to 200,000 context tokens with separate response length control
- 📝 **Smart Message Handling** - Uses Discord embeds for 2x capacity (4096 vs 2000 chars) with intelligent splitting that preserves markdown formatting

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Discord Bot Token ([Create one here](https://discord.com/developers/applications))
- OpenAI API key or access to an OpenAI-compatible API endpoint

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Crazy-Rain/Discord-bot-with-Preset.git
cd Discord-bot-with-Preset
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the bot:
   - Copy `config.example.json` to `config.json`
   - Update with your settings, or use the web interface after starting

4. Run the bot:
```bash
python main.py
```

5. Access the web configuration interface at `http://localhost:5000`

## ⚙️ Configuration

### config.json Structure

```json
{
  "discord_token": "YOUR_DISCORD_BOT_TOKEN",
  "openai_config": {
    "api_key": "YOUR_API_KEY",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-3.5-turbo"
  },
  "web_server": {
    "host": "0.0.0.0",
    "port": 5000
  },
  "default_preset": {
    "temperature": 0.7,
    "max_tokens": 2000,
    "max_response_length": 2000,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "system_prompt": "You are a helpful AI assistant."
  }
}
```

### Supported OpenAI-Compatible APIs

This bot works with any OpenAI-compatible API endpoint:

- **OpenAI** - `https://api.openai.com/v1`
- **LM Studio** - `http://localhost:1234/v1`
- **Ollama** - `http://localhost:11434/v1` (with compatibility layer)
- **Text Generation WebUI** - `http://localhost:5000/v1`
- **KoboldAI** - with OpenAI-compatible extension
- **Any other OpenAI-compatible endpoint**

## 🎮 Discord Commands

### Core Commands
- `!chat <message>` - Chat with the AI using current preset and character
- `!clear` - Clear conversation history and character names for the current channel
- `!reload_history [limit]` - Reload conversation context from channel history (default: 50, max: 100)

### Character Commands (Per-Channel Avatars)
- `!character <name>` - Load a character card for this channel (uses webhooks for avatar)
- `!current_character` - Show which character is loaded for this channel
- `!unload_character` - Unload the current character from this channel
- `!characters` - List all available character cards
- `!image <character_name>` - Update character avatar from an attached image (PNG/JPG/GIF, max 10MB)

### Preset Commands
- `!preset <name>` - Load a specific preset
- `!presets` - List all available presets

### Alternative Response Commands
- `!swipe` - Generate an alternative response to the last message
- `!swipe_left` - Navigate to the previous alternative response
- `!swipe_right` - Navigate to the next alternative response

### User Character Commands
- `!update <Name>: <Description>` - Update user character description
- `!user_chars` - List saved user characters
- `!user_char <name>` - View a specific user character
- `!delete_user_char <name>` - Delete a user character

### Help
- `!help_bot` - Show help information

### 🖼️ Per-Channel Character Avatars

The bot now supports loading different characters with unique avatars in each channel using Discord webhooks!

**Key Benefits:**
- ✅ **No Rate Limits** - Bypass Discord's 2-per-hour avatar change limit
- ✅ **Multi-Character Support** - Different characters in different channels simultaneously
- ✅ **Instant Switching** - Change characters as often as you want
- ✅ **Character Names & Avatars** - Messages appear with the character's name and avatar

**How to use:**
```
!character luna          # Load Luna character in this channel
!chat Hello!            # Bot responds as Luna with her avatar
!current_character      # Check which character is loaded
!unload_character       # Return to normal bot behavior
```

See [PER_CHANNEL_AVATARS_GUIDE.md](PER_CHANNEL_AVATARS_GUIDE.md) for complete documentation.

**Requirements:** Bot needs "Manage Webhooks" permission to use this feature.

### 👥 Character Name Tracking

Users can identify themselves as characters by using the format `CharacterName: message`. This helps the AI understand who is speaking in roleplay scenarios.

**Formatting Guidelines:**

1. **Spoken Dialogue** - Use `"quotes"` for words spoken by characters:
   ```
   !chat Alice: "Hello, how are you today?"
   ```

2. **Actions** - Use `*asterisks*` for actions performed by characters:
   ```
   !chat Bob: *waves* "Hi everyone!"
   ```

3. **Descriptive Text** - Text without quotes or asterisks is descriptive or contextual:
   ```
   !chat Charlie: Looks around thoughtfully "I'm doing great, thanks!"
   ```

**Combined Example:**
```
!chat Sarah: *enters the room* "Good morning!" She smiles warmly at everyone
```

The bot will:
- Track all character names used in the conversation
- Include character context in the AI's system prompt
- Ensure the AI doesn't pretend to be these characters
- Maintain character names until `!clear` is used
- Understand the difference between dialogue, actions, and descriptions

### 📝 User Character Descriptions

Save and manage descriptions for your user characters to give the AI more context during roleplay scenarios.

**Discord Commands:**
```
!update Alice: A brave warrior with long red hair and green eyes, wearing silver armor. Known for her courage and compassion.
!user_chars                    # List all saved user characters
!user_char Alice               # View Alice's description
!delete_user_char Alice        # Delete Alice's character
```

**Web Interface:**
- Navigate to the "User Characters" tab at `http://localhost:5000`
- Add/edit character names and descriptions
- Import/export character descriptions as JSON
- Saved between sessions automatically

**How It Works:**
When you use a character name in chat (e.g., `!chat Alice: "Hello!"`), the bot will:
1. Check if Alice has a saved description
2. Include Alice's description in the AI's system prompt
3. Provide context to the AI about Alice's appearance and traits
4. Tell the AI NOT to act or write for Alice (only reference)

This allows for richer, more contextualized roleplay conversations!

## 🎨 Preset System

Presets allow you to customize the AI's behavior with different parameters. The system now supports **SillyTavern-style presets** with advanced message formatting!

### Standard Preset Parameters

- **Temperature** - Controls randomness (0.0 = deterministic, 2.0 = very random)
- **Max Tokens (Context)** - Maximum context window size (up to 200,000 tokens)
- **Max Response Length** - Maximum length of AI response (separate from context limit)
- **Top P** - Nucleus sampling parameter
- **Frequency Penalty** - Reduces repetition of frequent tokens
- **Presence Penalty** - Reduces repetition of any tokens
- **System Prompt** - Instructions for the AI's behavior

### 🆕 SillyTavern-Style Advanced Features

The preset system now supports proper message role separation and character card integration, similar to SillyTavern!

**New Preset Fields:**
- **`prompt_format`** - Style of prompt formatting (`"default"` or `"sillytavern"`)
- **`character_position`** - Where to inject character info (`"system"`, `"examples"`, or `"both"`)
- **`include_examples`** - Whether to include example dialogues from character cards
- **`example_separator`** - Separator used in character card examples (default: `"<START>"`)

**Benefits:**
- ✅ **Proper Role Separation** - System, user, and assistant messages sent separately
- ✅ **Example-Based Learning** - AI learns from character example dialogues
- ✅ **Better Character Consistency** - More control over character behavior
- ✅ **Uncensored Characters** - Optimal formatting for unfiltered roleplay

**Example SillyTavern-Style Preset:**
```json
{
  "temperature": 0.85,
  "max_tokens": 4000,
  "max_response_length": 2000,
  "top_p": 0.95,
  "frequency_penalty": 0.1,
  "presence_penalty": 0.1,
  "system_prompt": "Write {{char}}'s next reply in a fictional chat. Stay in character and be creative.",
  "prompt_format": "sillytavern",
  "character_position": "both",
  "include_examples": true,
  "example_separator": "<START>"
}
```

See **[SILLYTAVERN_PRESETS_GUIDE.md](SILLYTAVERN_PRESETS_GUIDE.md)** for complete documentation on the new preset system!

### Creating Presets

You can create presets in two ways:

1. **Web Interface**: Navigate to the Presets tab at `http://localhost:5000`
2. **Manual JSON**: Create a file in the `presets/` directory

Example preset (`presets/creative.json`):
```json
{
  "temperature": 0.9,
  "max_tokens": 2000,
  "max_response_length": 2000,
  "top_p": 1.0,
  "frequency_penalty": 0.7,
  "presence_penalty": 0.6,
  "system_prompt": "You are a creative and imaginative AI assistant."
}
```

### Swipe Functionality

Similar to SillyTavern, you can generate and navigate through alternative AI responses:

1. Use `!chat` to get an initial response
2. Use `!swipe` to generate alternative responses to the last message
3. Use `!swipe_left` and `!swipe_right` to navigate between alternatives
4. Each alternative is stored and you can switch between them at any time

This allows you to explore different creative directions without losing previous responses!

### Import/Export Presets

- Export presets as JSON files to share or backup
- Import presets from JSON files or paste JSON directly in the web interface

## 👤 Character Cards

Character cards define AI personalities with full **SillyTavern compatibility**!

### Standard Character Fields

- **Name** - Character's display name
- **Personality** - Character traits
- **Description** - Background and characteristics
- **Scenario** - Context for interactions
- **System Prompt** - Optional custom system prompt (overrides auto-generated one)
- **Avatar URL** - URL to character's avatar image (for webhook displays)

### 🆕 SillyTavern-Compatible Fields

- **`first_mes`** - Character's opening message (becomes first assistant message in examples)
- **`mes_example`** - Example dialogue exchanges separated by `<START>` tags
- **Placeholder support** - Use `{{char}}` for character name and `{{user}}` for user

**Example Character with Dialogues:**
```json
{
  "name": "Aria",
  "personality": "Confident, flirtatious, adventurous",
  "description": "A charming rogue with a silver tongue and mysterious past.",
  "scenario": "You've just met Aria at a tavern.",
  "first_mes": "*glances over with a playful smirk* Well, well. You look interesting. Care for a drink?",
  "mes_example": "<START>\n{{user}}: What brings you here?\n{{char}}: *leans back* Oh, the usual. Good drinks, better company, maybe some treasure. *grins*\n<START>\n{{user}}: You seem dangerous.\n{{char}}: *laughs* Flattery will get you everywhere, darling.",
  "system_prompt": "",
  "avatar_url": ""
}
```

When using a SillyTavern-style preset (with `include_examples: true`), these example dialogues are sent as separate user/assistant messages, helping the AI learn the character's voice and behavior patterns.

### Creating Character Cards

1. **Web Interface**: Navigate to the Characters tab at `http://localhost:5000`
2. **Manual JSON**: Create a file in the `character_cards/` directory

### Character Card Formats

The bot supports multiple approaches:

1. **Auto-generated** - Combines name, description, personality, and scenario
2. **Custom system_prompt** - Use a custom system prompt field (takes precedence)
3. **SillyTavern-style** - Use `first_mes` and `mes_example` with appropriate presets for example-based character behavior

## 🌐 Web Configuration Interface

Access the web interface at `http://localhost:5000` to:

- Configure Discord bot token and OpenAI API settings
- Manage presets (create, edit, delete, import/export)
- Manage character cards (create, edit, delete, import/export)
- Manage user character descriptions (create, edit, delete, import/export)
- Adjust all AI parameters with interactive sliders
- Real-time configuration updates

## 📁 Project Structure

```
Discord-bot-with-Preset/
├── main.py                      # Main entry point
├── config_manager.py            # Configuration management
├── discord_bot.py               # Discord bot implementation
├── openai_client.py             # OpenAI API client wrapper
├── preset_manager.py            # Preset management
├── character_manager.py         # Character card management
├── user_characters_manager.py   # User character descriptions management
├── lorebook_manager.py          # Lorebook management
├── web_server.py                # Flask web server
├── templates/
│   └── index.html              # Web UI
├── presets/                    # Preset storage
│   ├── creative.json
│   └── analytical.json
├── character_cards/            # Character card storage
│   ├── sherlock.json
│   └── luna.json
├── user_characters/            # User character descriptions storage
│   └── user_characters.json
├── lorebook/                   # Lorebook storage
│   └── lorebook.json
├── config.json                 # Configuration (created from example)
├── config.example.json         # Example configuration
├── requirements.txt            # Python dependencies
├── LOREBOOK_GUIDE.md           # Lorebook feature guide
├── USER_CHARACTERS_GUIDE.md    # User characters guide
└── README.md                  # This file
```

## 📚 Documentation

- **[SillyTavern Presets Guide](SILLYTAVERN_PRESETS_GUIDE.md)** - **NEW!** Complete guide to the advanced preset system
- **[Context Management Guide](CONTEXT_MANAGEMENT.md)** - How the bot handles conversation history and channel context
- **[Lorebook Guide](LOREBOOK_GUIDE.md)** - Complete guide to using the lorebook feature
- **[User Characters Guide](USER_CHARACTERS_GUIDE.md)** - Guide for user character descriptions
- **[Per-Channel Avatars Guide](PER_CHANNEL_AVATARS_GUIDE.md)** - Guide for webhook-based character avatars
- **[Image Command Guide](IMAGE_COMMAND_GUIDE.md)** - **NEW!** Upload character avatars directly from Discord
- **[Examples](EXAMPLES.md)** - Usage examples and common scenarios
- **[Setup Guide](SETUP.md)** - Detailed setup instructions

## 🔧 Troubleshooting

### API Key Configuration
- The bot will now start even without a valid API key configured
- You can configure the API key via the web interface at `http://localhost:5000`
- The API key is validated only when making actual API calls, not during initialization

### Bot won't start
- Ensure `config.json` has valid Discord token
- Check that all dependencies are installed: `pip install -r requirements.txt`

### API errors
- Verify your API key and base URL are correct
- Check if the API endpoint is accessible
- Ensure the model name is valid for your endpoint

### Web interface not accessible / 404 errors
- The web server takes a few seconds to start - wait for the "✅ Web interface should now be accessible" message
- Check if port 5000 is available or change the port in `config.json`
- Try accessing via `http://127.0.0.1:5000` instead of `localhost`
- Verify firewall isn't blocking the port
- If you see Flask startup messages, the server is running - just wait 2-3 seconds after startup

### Web interface not accessible
- Check if port 5000 is available
- Try accessing via `http://127.0.0.1:5000` instead of `localhost`
- Check firewall settings

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Inspired by [SillyTavern](https://github.com/SillyTavern/SillyTavern)
- Built with [discord.py](https://github.com/Rapptz/discord.py)
- Uses [OpenAI Python SDK](https://github.com/openai/openai-python)

## 💡 Tips

- Use lower temperature (0.1-0.5) for factual/analytical responses
- Use higher temperature (0.7-1.2) for creative/varied responses
- Character cards override preset system prompts
- Conversation history is per-channel and limited to last 20 messages
- Use `!clear` to reset context when switching topics
- Long messages (>4096 chars) are automatically split intelligently to preserve markdown formatting
