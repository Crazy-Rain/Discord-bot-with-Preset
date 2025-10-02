# Feature Update - Bot Name Change & Dynamic Config Updates

## New Features

### 1. Bot Name Changes to Match Character

When you load a character card using the `!character <name>` command, the bot will now automatically change its display name (nickname) to match the character's display name.

**How it works:**
- When you use `!character luna`, the bot's nickname in Discord will change to "Luna" (or whatever name is specified in the character card's `name` field)
- The bot will update its nickname in all servers it's a member of
- If the bot doesn't have permission to change its nickname in a server, it will silently continue (no error shown to users)
- When the bot starts, if a character is already loaded, it will set its nickname to that character automatically

**Example:**
```
User: !character luna
Bot: Loaded character: luna
[Bot's nickname changes to "Luna"]
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

1. **Better Immersion**: The bot's display name matching the character makes roleplay and character interactions more immersive
2. **Faster Configuration**: No need to restart the bot when switching between different API providers or updating credentials
3. **Easier Testing**: Quickly switch between different API endpoints (e.g., OpenAI, local LM Studio, different proxies) for testing
4. **Improved UX**: Seamless configuration updates without service interruption

## Permissions Note

For the bot name change feature to work, the bot needs the "Change Nickname" permission in your Discord server. If it doesn't have this permission, the feature will fail silently (no error shown to users, but the name won't change).

To grant this permission:
1. Go to Server Settings → Roles
2. Find your bot's role
3. Enable "Change Nickname" permission
