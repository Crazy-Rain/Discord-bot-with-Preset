# Auto Context Limit Feature

## Overview

The Auto Context Limit feature allows you to configure how many messages are automatically loaded from Discord channel history when the bot starts a new conversation. This provides context from previous messages even after bot restarts.

## Configuration Options

### Default Settings
- **Default Limit**: 50 messages
- **Minimum Limit**: 50 messages
- **Maximum Limit**: 5000 messages
- **Step Size**: 50 messages

### Two Ways to Configure

#### 1. Discord Command: `!setcontext`

Use the `!setcontext` command in Discord to set the automatic context limit:

```
!setcontext 100    # Set to 100 messages
!setcontext 500    # Set to 500 messages
!setcontext 1000   # Set to 1000 messages
```

**Features:**
- ✅ Changes are saved permanently to config.json
- ✅ Takes effect immediately for new conversations
- ✅ Validates input (50-5000 range)
- ✅ Provides feedback on success or validation errors

**Examples:**
```
!setcontext 200
✅ Auto context limit set to 200 messages!
This will be used when automatically loading channel history.
The setting has been saved to config and will persist across bot restarts.

!setcontext 25
❌ Limit too low! Minimum is 50 messages.

!setcontext 6000
❌ Limit too high! Maximum is 5000 messages.
```

#### 2. Web Configuration UI

1. Open the web interface at `http://localhost:5000`
2. Navigate to the **Configuration** tab
3. Scroll to the **Auto Context Loading** section
4. Use the slider to adjust the limit (50-5000)
5. Click **Save Configuration**

**Features:**
- ✅ Visual slider for easy adjustment
- ✅ Real-time value display
- ✅ Saves to config.json
- ✅ Updates running bot instance immediately

## How It Works

### Automatic Loading
When you use `!chat` in a Discord channel for the first time (or after `!clear`), the bot automatically:

1. Checks if conversation history is empty
2. Loads the configured number of recent messages from channel history
3. Parses `!chat` commands and bot responses
4. Builds conversation context from these messages
5. Uses this context for AI responses

### Manual Reload
You can also manually reload history with a specific limit using:
```
!reload_history [limit]
```

This temporarily reloads with a custom limit but doesn't change the auto context limit setting.

## Use Cases

### Small Limit (50-100 messages)
- **Best for**: Quick responses, minimal context needed
- **Pros**: Fast loading, lower memory usage
- **Cons**: May miss older relevant context

### Medium Limit (100-500 messages)
- **Best for**: Balanced performance and context
- **Pros**: Good context retention, reasonable speed
- **Cons**: Moderate memory usage

### Large Limit (500-5000 messages)
- **Best for**: Long conversations, extensive context needed
- **Pros**: Maximum context retention
- **Cons**: Slower loading, higher memory usage
- **Note**: With 200,000 token context limit, even 5000 messages should work fine

## Configuration File

The setting is stored in `config.json`:

```json
{
  "auto_context_limit": 50,
  "discord_token": "...",
  "openai_config": {...},
  ...
}
```

## Persistence

- Changes made via `!setcontext` are saved to `config.json`
- Changes made via web UI are saved to `config.json`
- The setting persists across bot restarts
- Both methods update the running bot instance immediately

## Related Commands

- `!chat <message>` - Chat with AI (auto-loads history if empty)
- `!reload_history [limit]` - Manually reload with specific limit
- `!clear` - Clear conversation (next chat will auto-load)
- `!help_bot` - Show all bot commands

## Tips

1. **Start Conservative**: Begin with default 50 and increase if needed
2. **Monitor Performance**: Higher limits take longer to load
3. **Consider Token Limits**: With 200k context, you have plenty of room
4. **Channel-Specific**: Each channel maintains separate context
5. **Combine with !reload_history**: Use auto limit for consistency, manual reload for one-time adjustments
