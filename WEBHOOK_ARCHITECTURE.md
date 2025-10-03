# Webhook-Based Character Display Architecture

## Before Fix (Problematic Approach)

```
┌─────────────────────────────────────────────────────────┐
│                    Discord Bot                          │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  on_ready() / !character command                 │  │
│  │                                                  │  │
│  │  1. Load character data                         │  │
│  │  2. Extract character name                      │  │
│  │  3. Try to change bot's global nickname  ❌     │  │
│  │     └─→ Discord 32-char limit                   │  │
│  │     └─→ "Must be 32 or fewer in length" error   │  │
│  │  4. Try to change bot's global avatar    ❌     │  │
│  │     └─→ Requires special permissions            │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  Problems:                                              │
│  • Character names > 32 chars fail                      │
│  • Requires "Change Nickname" permission                │
│  • Changes affect ALL servers                           │
│  • One character for entire bot                         │
└─────────────────────────────────────────────────────────┘
```

## After Fix (Webhook Approach) ✅

```
┌─────────────────────────────────────────────────────────┐
│                    Discord Bot                          │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  on_ready()                                      │  │
│  │                                                  │  │
│  │  1. Load channel configurations                 │  │
│  │  2. Load characters for configured channels     │  │
│  │  3. Store character data per channel            │  │
│  │  ✅ No nickname/avatar changes                   │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  !character luna (in Channel A)                 │  │
│  │                                                  │  │
│  │  1. Load character "Luna" data                  │  │
│  │  2. Store for Channel A only                    │  │
│  │  3. When responding in Channel A:               │  │
│  │     └─→ Use webhook with Luna's name & avatar   │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  send_as_character() - Webhook Method           │  │
│  │                                                  │  │
│  │  webhook_params = {                             │  │
│  │    'username': 'Luna',  # No 32-char limit! ✅  │  │
│  │    'avatar_url': 'https://...'  # If provided   │  │
│  │  }                                               │  │
│  │  await webhook.send(embed=..., **webhook_params)│  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  Benefits:                                              │
│  ✅ No character name length limits                     │
│  ✅ No special permissions required                     │
│  ✅ Different character per channel                     │
│  ✅ Bot identity separate from character                │
└─────────────────────────────────────────────────────────┘
```

## How Webhooks Work

### Channel A: Character "Luna"
```
User: Hello!
Bot Response via Webhook:
┌────────────────────────────────┐
│ 👤 Luna                        │ ← Webhook username
│ 🖼️  [Luna's Avatar]            │ ← Webhook avatar
│                                │
│ Hello! How can I help you?     │
│                                │
│ [🔄 Swipe] [✏️ Edit] [🗑️ Delete] │
└────────────────────────────────┘
```

### Channel B: Character "Sherlock Holmes" (> 32 chars!)
```
User: What do you see?
Bot Response via Webhook:
┌────────────────────────────────┐
│ 👤 Sherlock Holmes             │ ← No length limit!
│ 🖼️  [Sherlock's Avatar]        │
│                                │
│ I observe everything...        │
│                                │
│ [🔄 Swipe] [✏️ Edit] [🗑️ Delete] │
└────────────────────────────────┘
```

## Code Flow

### 1. Character Loading
```python
# User runs: !character luna
@self.command(name="character")
async def character(ctx, character_name: str):
    # Load character data
    character_data = self.character_manager.load_character(character_name)
    
    # Store for THIS channel only
    channel_id = ctx.channel.id
    self.channel_characters[channel_id] = character_data
    
    # ✅ No nickname changes
    # ✅ No avatar changes
    # Just store the data for later use
```

### 2. Sending Responses
```python
# When bot responds in a channel with a character loaded
async def send_as_character(self, channel, content, character_data, view):
    # Get or create webhook for this channel
    webhook = await self.get_or_create_webhook(channel)
    
    # Build webhook parameters
    webhook_params = {
        'username': character_data.get('name'),  # Character name
        'wait': True
    }
    
    # Add avatar if available
    avatar_url = character_data.get('avatar_url')
    if avatar_url and avatar_url.strip():
        webhook_params['avatar_url'] = avatar_url
    
    # Send via webhook with character identity
    embed = discord.Embed(description=content, color=0x2b2d31)
    await webhook.send(embed=embed, view=view, **webhook_params)
```

## Comparison

| Feature | Old (Nickname) | New (Webhook) |
|---------|---------------|---------------|
| Character name length | ❌ Max 32 chars | ✅ No limit |
| Permissions required | ❌ "Change Nickname" | ✅ None |
| Scope | ❌ Global (all servers) | ✅ Per-channel |
| Multiple characters | ❌ One at a time | ✅ Different per channel |
| Reliability | ❌ Errors with long names | ✅ Always works |

## Why This Fix Works

1. **Webhooks bypass Discord nickname limits**: Webhook usernames can be longer than 32 characters
2. **No permissions needed**: Creating/using webhooks doesn't require special bot permissions
3. **Better separation**: Bot's identity is separate from character identity
4. **More flexible**: Different characters can be active in different channels simultaneously
5. **More reliable**: No API errors related to nickname length or permissions

## Migration Notes

- All existing character functionality preserved
- No user-facing changes except error messages are gone
- Character display is actually improved (more reliable)
- No configuration changes needed
