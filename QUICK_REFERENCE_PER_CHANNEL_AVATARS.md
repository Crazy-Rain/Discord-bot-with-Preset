# Per-Channel Character Avatars - Quick Reference

## 🚀 Quick Start

```bash
# 1. Add avatar URL to character card
{
  "name": "Luna",
  "avatar_url": "https://example.com/luna.png"
}

# 2. Grant bot "Manage Webhooks" permission

# 3. Load character in Discord
!character luna

# 4. Chat normally
!chat Hello!
```

## 📋 Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `!character <name>` | Load character for this channel | `!character luna` |
| `!current_character` | Show loaded character | `!current_character` |
| `!unload_character` | Remove character from channel | `!unload_character` |
| `!characters` | List available characters | `!characters` |
| `!chat <message>` | Chat with character | `!chat Hello!` |

## ✅ Benefits

- ✓ **No Rate Limits** - Switch characters unlimited times
- ✓ **Per-Channel** - Different characters in different channels
- ✓ **Instant** - No waiting between switches
- ✓ **Multi-Character** - Multiple characters active simultaneously
- ✓ **Custom Names** - Character name appears instead of bot name
- ✓ **Custom Avatars** - Character avatar appears in messages

## 🎯 Key Differences

### Old Method (Global Avatar)
- Changes bot's profile picture globally
- Limited to 2 changes per hour
- Same avatar in all servers/channels
- 30-minute wait between changes

### New Method (Per-Channel Webhooks)
- Uses webhooks with character avatar
- **No rate limits** - unlimited changes
- Different avatar per channel
- **Instant switching**

## 🔧 Requirements

1. **Bot Permission**: `Manage Webhooks`
2. **Character Card**: Must have `avatar_url` field
3. **Avatar URL**: Must be publicly accessible

## 💡 Usage Examples

### Single Channel
```
!character luna
!chat Tell me a story
Luna: "Once upon a time..."
```

### Multiple Channels (Simultaneously)
```
#fantasy → !character luna
#scifi   → !character robot
#mystery → !character sherlock

All active at the same time!
```

### Quick Switching
```
!character luna
!chat Hello
Luna: "Hi there!"

!character sherlock
!chat Investigate
Sherlock: "Elementary..."

!character luna
!chat Back again
Luna: "Welcome back!"

No waiting required!
```

## 🛠️ Setup Steps

### 1. Prepare Character Card

```json
{
  "name": "Luna",
  "personality": "Friendly, helpful",
  "description": "A caring AI companion",
  "avatar_url": "https://i.imgur.com/example.png"
}
```

### 2. Grant Permission

Server Settings → Roles → Bot Role → ✓ Manage Webhooks

### 3. Load Character

```
!character luna
```

### 4. Start Chatting

```
!chat Hello Luna!
```

## ❓ Troubleshooting

### Avatar Not Showing?

**Check:**
- ✓ Bot has "Manage Webhooks" permission
- ✓ `avatar_url` is set in character card
- ✓ Avatar URL is publicly accessible
- ✓ URL is direct link to image

**Fix:**
```
# Check current character
!current_character

# Reload character
!unload_character
!character luna

# Verify URL works
# Open avatar_url in browser
```

### Permission Error?

```
Server Settings
  → Roles
    → Find bot's role
      → Enable "Manage Webhooks"
        → Try again
```

### Character Not Loading?

```
# List available characters
!characters

# Check if file exists
# Should be in: character_cards/luna.json

# Load with exact name
!character luna
```

## 📖 Documentation Links

- [Complete Guide](PER_CHANNEL_AVATARS_GUIDE.md)
- [Implementation Details](IMPLEMENTATION_PER_CHANNEL_AVATARS.md)
- [Visual Guide](VISUAL_GUIDE_PER_CHANNEL_AVATARS.md)
- [README](README.md)

## 🎨 Character Card Template

```json
{
  "name": "Character Name",
  "personality": "Describe personality traits",
  "description": "Full character description",
  "scenario": "Context for character",
  "system_prompt": "Optional custom system prompt",
  "avatar_url": "https://example.com/avatar.png"
}
```

## 🌐 Avatar URL Sources

### Recommended Services:
- **Imgur**: Upload → Copy image link
- **Discord CDN**: Upload to Discord → Copy link
- **GitHub**: Use raw.githubusercontent.com links

### URL Format:
```
✓ https://i.imgur.com/abc123.png
✓ https://cdn.discordapp.com/attachments/...
✓ https://raw.githubusercontent.com/user/repo/main/avatar.png

✗ https://imgur.com/abc123 (not direct link)
✗ https://example.com/page (webpage, not image)
```

## 🔄 Workflow Diagram

```
Load Character → Chat → Response appears with character avatar
     ↓              ↓              ↓
  (instant)    (normal)        (via webhook)
     ↓              ↓              ↓
Switch anytime without limits!
```

## ⚡ Performance Tips

1. **Webhook Caching**: Bot caches webhooks for fast reuse
2. **Instant Loading**: Character loading is instantaneous
3. **No API Delays**: No waiting for Discord rate limits
4. **Concurrent Characters**: Multiple channels don't interfere

## 🎭 Use Cases

### Roleplay Servers
- Different characters in different RP channels
- Quick character switching for different scenes
- Multiple GMs with different personas

### Storytelling Bots
- Narrator in one channel
- Different characters in story channels
- Quick scene transitions

### Multi-Purpose Bots
- Helpful assistant in support channels
- Fun personality in general channels
- Professional in business channels

### Testing & Development
- Test different character configurations
- Switch between versions quickly
- No rate limit interference

## 🔑 Key Takeaways

1. **Unlimited switches** - No more 2-per-hour limit
2. **Per-channel** - Not just per-server, but per-channel!
3. **Instant** - No waiting between character changes
4. **Multi-character** - Different characters in different channels
5. **Simple** - Just load a character and start chatting

## 📞 Support

For issues or questions:
1. Check [troubleshooting section](#-troubleshooting)
2. Review [complete guide](PER_CHANNEL_AVATARS_GUIDE.md)
3. Verify bot has required permissions
4. Check character card has `avatar_url`

## 🎉 Getting Started

Ready to try it?

```bash
# Step 1: Load a character
!character luna

# Step 2: Start chatting
!chat Hello!

# Step 3: Enjoy! 🎉
```

---

**Version**: 1.0
**Feature**: Per-Channel Character Avatars
**Method**: Discord Webhooks
**Rate Limits**: None ✓
**Status**: ✅ Production Ready
