# Feature Update - Dynamic Config Updates

## New Features

### 1. Per-Channel Character Display via Webhooks

When you load a character card using the `!character <name>` command, the bot will use Discord webhooks to display messages with the character's name and avatar for that specific channel.

**How it works:**
- When you use `!character luna`, the bot will use webhooks to send messages with "Luna" as the display name and the character's avatar (if set)
- This is channel-specific - different channels can have different characters
- The character display persists across bot restarts
- No special permissions are required for this feature

**Example:**
```
User: !character luna
Bot: ✨ Loaded character Luna for this channel!
     The bot will now respond with Luna's avatar and name using webhooks.
[Bot responses in this channel will display as "Luna" with Luna's avatar]
```

### 2. Dynamic Configuration Updates (No Restart Required)

Previously, when you updated the API key or proxy (base URL) in the web configuration interface, you had to restart the bot for the changes to take effect. Now, these changes are applied immediately!

**What's Changed:**
- API Key updates are applied immediately to the running bot
- Proxy/Base URL updates are applied immediately to the running bot
- Model selection updates are applied immediately to the running bot
- No bot restart required after making these changes

**How to use:**
1. Navigate to http://localhost:5000 (or your configured web server port)
2. Go to the Configuration tab
3. Update your API key, Base URL, or Model
4. Click "Save Configuration"
5. You'll see a success message: "Configuration updated and applied to running bot"
6. The bot is now using the new configuration immediately!

**Technical Details:**
- The web server now holds a reference to the bot instance
- When OpenAI configuration changes are detected, the web server calls `bot.update_openai_config()` 
- This recreates the OpenAI client with the new credentials/settings
- The bot can now connect to different proxies or APIs without restarting

## Benefits

1. **Better Immersion**: Character display via webhooks makes roleplay and character interactions more immersive without changing the bot's global identity
2. **Faster Configuration**: No need to restart the bot when switching between different API providers or updating credentials
3. **Easier Testing**: Quickly switch between different API endpoints (e.g., OpenAI, local LM Studio, different proxies) for testing
4. **Improved UX**: Seamless configuration updates without service interruption
5. **No Character Name Limits**: Unlike bot nicknames (limited to 32 characters), webhook usernames support longer character names
