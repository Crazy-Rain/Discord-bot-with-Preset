# Per-Channel Character Avatars Feature

## Overview

The bot now supports **per-channel character avatars** using Discord webhooks! This revolutionary feature allows you to:
- Load different characters in different channels simultaneously
- Display character-specific avatars and names per channel
- **Bypass Discord's 2-per-hour rate limit** on bot avatar changes
- Switch characters as frequently as you want without restrictions

## How It Works

Unlike traditional bot avatar changes (which are global and rate-limited), this feature uses Discord's webhook system:

1. When you load a character in a channel, the bot creates/reuses a webhook for that channel
2. When the bot responds, it sends messages through the webhook using the character's avatar and name
3. Each channel can have a different character loaded simultaneously
4. There are no rate limits - switch characters as often as you like!

## Commands

### Load a Character (Per Channel)

```
!character <character_name>
```

Loads a character for the current channel. The bot will respond with the character's avatar and name.

**Example:**
```
!character luna
```
Response: `✨ Loaded character Luna for this channel! The bot will now respond with Luna's avatar and name using webhooks.`

### View Current Character

```
!current_character
```

Shows which character is currently loaded for the current channel.

### Unload Character

```
!unload_character
```

Removes the character from the current channel. The bot will respond normally without a character avatar.

### Chat with Character

```
!chat <message>
```

Chat with the AI. If a character is loaded in the channel, responses will appear with the character's avatar and name.

## Example Usage

### Single Channel Setup

```
User: !character luna
Bot: ✨ Loaded character Luna for this channel!

User: !chat Hello Luna!
Luna: Hello! How can I help you today?
[Message appears with Luna's avatar]
```

### Multi-Channel Setup

In **#roleplay-channel-1**:
```
User: !character luna
Bot: ✨ Loaded character Luna for this channel!

User: !chat Tell me a story
Luna: Once upon a time...
[Luna's avatar appears]
```

In **#roleplay-channel-2** (simultaneously):
```
User: !character sherlock
Bot: ✨ Loaded character Sherlock Holmes for this channel!

User: !chat Solve this mystery
Sherlock Holmes: Elementary, my dear Watson...
[Sherlock's avatar appears]
```

Both channels can have different characters active at the same time!

## Key Differences from Global Avatar

| Feature | Global Avatar (Old) | Per-Channel Webhooks (New) |
|---------|---------------------|----------------------------|
| **Scope** | All servers & channels | Per channel |
| **Rate Limit** | 2 changes per hour | No limit |
| **Simultaneous Characters** | Only one | Unlimited (one per channel) |
| **Discord API Used** | `bot.user.edit()` | Webhooks |
| **Permissions Required** | None | Manage Webhooks |
| **Name Display** | Bot's nickname | Character's name |
| **Avatar Display** | Bot's global avatar | Character's avatar URL |

## Setting Up Character Avatars

### Via Web Interface

1. Navigate to http://localhost:5000
2. Go to "Characters" tab
3. Edit or create a character
4. In the "Avatar URL" field, enter a direct URL to an image:
   - Example: `https://i.imgur.com/example.png`
   - Supported formats: PNG, JPG, GIF
   - Must be publicly accessible
5. Click "Save Character"
6. Load the character in Discord: `!character <name>`

### Character Card JSON Format

```json
{
  "name": "Luna",
  "personality": "Friendly, empathetic, supportive",
  "description": "A warm and caring AI companion...",
  "scenario": "You are chatting with users...",
  "system_prompt": "",
  "avatar_url": "https://i.imgur.com/luna-avatar.png"
}
```

## Technical Details

### Webhook Management

- The bot automatically creates a webhook named "Character Bot" in each channel where a character is loaded
- Webhooks are cached and reused to minimize API calls
- If a webhook is deleted, the bot will automatically create a new one
- Webhooks persist across bot restarts

### Permissions Required

The bot needs the **Manage Webhooks** permission to use this feature:
1. Go to Server Settings → Roles
2. Find your bot's role
3. Enable "Manage Webhooks" permission

If the bot doesn't have this permission:
- Character loading will still work
- But responses will fall back to normal messages without character avatars

### Fallback Behavior

The bot gracefully handles errors:
- If webhook creation fails → Falls back to normal messages
- If webhook sending fails → Falls back to normal messages
- If no avatar URL is set → Uses character name only (no avatar)

## Advantages Over Global Avatar

1. **No Rate Limits**: Switch characters as often as you want
2. **Multi-Character Support**: Different characters in different channels
3. **Better for Communities**: Each roleplay channel can have its own character
4. **Instant Switching**: No waiting between character changes
5. **Name Display**: Character name appears instead of bot name

## Best Practices

1. **Set Avatar URLs**: Make sure your characters have avatar_url set for best experience
2. **Use Reliable Hosting**: Use Imgur, Discord CDN, or other reliable image hosts
3. **Grant Webhook Permission**: Ensure bot has "Manage Webhooks" permission
4. **Per-Channel Characters**: Load different characters for different purposes
5. **Clear When Done**: Use `!unload_character` when you want to return to normal bot behavior

## Troubleshooting

### Character Not Showing Avatar

1. **Check Avatar URL**: Ensure `avatar_url` is set in character card
2. **Check URL Accessibility**: Try opening the URL in a browser
3. **Check Permissions**: Bot needs "Manage Webhooks" permission
4. **Check Bot Logs**: Look for webhook-related errors in console

### Webhook Permissions Error

If you see "No permission to create webhook":
1. Go to Server Settings → Roles
2. Find your bot's role
3. Enable "Manage Webhooks" permission
4. Try loading the character again

### Messages Appearing Without Avatar

This means the webhook fallback is working:
- Character is loaded but webhook couldn't be used
- Check bot has "Manage Webhooks" permission
- Check the avatar URL is valid and accessible

## Limitations

- Requires "Manage Webhooks" permission
- Avatar URL must be publicly accessible
- Webhook messages cannot be edited by the bot later
- Reactions on webhook messages work normally

## Comparison: When to Use Which Method

### Use Per-Channel Webhooks When:
- You want different characters in different channels
- You need to switch characters frequently
- You're running a roleplay server with multiple characters
- You want unlimited character switches without rate limits

### Use Global Avatar When:
- You only use one character across all servers
- You don't mind the 2-per-hour rate limit
- You prefer the bot's nickname to show in server member lists
- You don't need per-channel character separation

## Examples

### Roleplay Server Setup

```
#general
User: !character narrator
Bot: ✨ Loaded character Narrator

#fantasy-rp
User: !character wizard
Bot: ✨ Loaded character Wizard Eldrin

#scifi-rp  
User: !character robot
Bot: ✨ Loaded character AI-2077

Each channel now has its own character active!
```

### Character Testing

```
User: !character luna
User: !chat Hello!
Luna: Hi there!

User: !character sherlock
User: !chat Hello!
Sherlock Holmes: Good day!

User: !character luna
User: !chat Hi again!
Luna: Welcome back!

No rate limits - switch as much as you want!
```

## Migration from Global Avatar

If you were using the global avatar feature before:

1. **Old Behavior**: `!character luna` changed the bot's global avatar
2. **New Behavior**: `!character luna` loads character for current channel only

The global avatar methods are still available in the code but are no longer called by the `!character` command. The new webhook-based approach is the recommended method going forward.

## Future Enhancements

Potential future improvements:
- Per-server default characters
- Character presets per channel
- Auto-load character based on channel name
- Webhook message editing support

## Summary

The per-channel character avatar feature revolutionizes how you can use characters in Discord:
- ✅ Unlimited character switches (no rate limits)
- ✅ Different characters per channel
- ✅ Character avatars and names displayed via webhooks
- ✅ Perfect for roleplay servers and multi-character scenarios
- ✅ Graceful fallbacks if webhooks unavailable

Start using it today with `!character <name>` in any channel!
