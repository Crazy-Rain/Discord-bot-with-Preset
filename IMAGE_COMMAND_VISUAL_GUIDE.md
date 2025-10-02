# !image Command - Quick Visual Guide

## Usage Flow

```
┌─────────────────────────────────────────────────────────┐
│  Discord User                                            │
└─────────────────────────────────────────────────────────┘
                    │
                    │ 1. Send message with attachment
                    │    !image luna
                    │    📎 luna-avatar.png
                    ▼
┌─────────────────────────────────────────────────────────┐
│  Bot Validates                                           │
│  ✓ File format (PNG/JPG/GIF)                            │
│  ✓ File size (≤10MB)                                    │
│  ✓ Character exists                                     │
└─────────────────────────────────────────────────────────┘
                    │
                    │ 2. Download & Convert
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  Image Processing                                        │
│  • Download from Discord                                 │
│  • Convert to base64 data URL                           │
│  • Create data:image/png;base64,iVBORw0K...             │
└─────────────────────────────────────────────────────────┘
                    │
                    │ 3. Save to multiple locations
                    │
      ┌─────────────┴─────────────┐
      ▼                           ▼
┌──────────────┐          ┌──────────────┐
│ Character    │          │ Backup File  │
│ Card JSON    │          │ Directory    │
│ avatar_url:  │          │ character_   │
│ data:image/  │          │ avatars/     │
│ png;base64,  │          │ luna.png     │
│ iVBORw0K...  │          │              │
└──────────────┘          └──────────────┘
      │                           │
      └─────────────┬─────────────┘
                    │ 4. Confirmation
                    ▼
┌─────────────────────────────────────────────────────────┐
│  Bot Responds                                            │
│  ✅ Successfully updated avatar for Luna!               │
│  📁 Image: luna-avatar.png (245.3 KB)                   │
│  💾 Saved to: character_avatars/luna.png                │
│  🎨 Avatar converted to base64 data URL                 │
└─────────────────────────────────────────────────────────┘
```

## Example Conversation

```
User: !characters
Bot: Available characters: luna, aria, sherlock

User: !image luna
      [Attached: my-luna-pic.png]

Bot: ✅ Successfully updated avatar for Luna!
     📁 Image: my-luna-pic.png (125.6 KB)
     💾 Saved to: character_avatars/luna.png
     🎨 Avatar converted to base64 data URL and stored in character card.
     
     The new avatar will be used when this character is loaded with !character luna

User: !character luna
Bot: ✨ Loaded character Luna for this channel!
     The bot will now respond with Luna's avatar and name using webhooks.

User: !chat Hello!
Bot: (Response appears with Luna's NEW avatar and name)
```

## Error Examples

### No Attachment
```
User: !image luna
Bot: ❌ No image attached! Please attach an image file (PNG, JPG, or GIF) to your message.
     Usage: `!image <character_name>` with an image attached
```

### Wrong File Type
```
User: !image luna
      [Attached: document.pdf]

Bot: ❌ Invalid file type: .pdf
     Only PNG, JPG, and GIF files are supported.
```

### File Too Large
```
User: !image sherlock
      [Attached: huge-image.png (15MB)]

Bot: ❌ File too large: 15.23MB
     Maximum file size is 10MB. Please use a smaller image.
```

### Character Not Found
```
User: !image unknown_character
      [Attached: avatar.png]

Bot: ❌ Character not found: unknown_character
     Use `!characters` to see available characters.
```

## Integration with Per-Channel Avatars

```
Channel #roleplay-1              Channel #roleplay-2
─────────────────────            ─────────────────────
!character luna                  !character aria
Luna loaded ✓                    Aria loaded ✓

!chat Hello!                     !chat Hi there!
[Luna avatar] Hello!             [Aria avatar] Hi there!

!image luna (new pic)            !image aria (new pic)
Avatar updated ✓                 Avatar updated ✓

!chat How are you?               !chat What's up?
[NEW Luna avatar] Fine!          [NEW Aria avatar] Good!
```

## Before and After

### Before !image command
```
1. Open web browser
2. Navigate to http://localhost:5000
3. Go to Characters tab
4. Find character
5. Click Edit
6. Choose avatar method
7. Upload file or paste URL
8. Save character
9. Return to Discord
10. Reload character
```

### After !image command
```
1. Type: !image luna
2. Attach image
3. Send
   ✅ Done!
```

## File Storage

```
project-root/
├── character_cards/
│   └── luna.json          ← Contains base64 embedded avatar
│       {
│         "name": "Luna",
│         "avatar_url": "data:image/png;base64,iVBORw0K..."
│       }
│
└── character_avatars/     ← Backup directory
    └── luna.png          ← Original image file
```

## Command Comparison

| Feature              | !image | Web Interface |
|---------------------|--------|---------------|
| Upload from Discord | ✅ Yes | ❌ No         |
| Upload from PC      | ❌ No  | ✅ Yes        |
| Speed               | ⚡ Fast| 🐌 Slow       |
| Convenience         | ⭐⭐⭐⭐⭐ | ⭐⭐           |
| Edit Other Fields   | ❌ No  | ✅ Yes        |
| Preview Before Save | ❌ No  | ✅ Yes        |

## Tips

### Quick Upload Workflow
```
1. Have images ready on your device
2. Drag image into Discord (don't send yet)
3. Type: !image <character_name>
4. Send message with attachment
5. Avatar is updated immediately!
```

### Batch Updates
```
!image luna    [attach luna.png]
!image aria    [attach aria.png]
!image sherlock [attach sherlock.png]
```

### Quality Recommendations
```
✅ Good: 256x256 PNG, 100KB
✅ Good: 512x512 JPG, 300KB
⚠️  OK: 1024x1024 PNG, 1MB
❌ Bad: 2048x2048 PNG, 8MB (unnecessary size)
```

### File Size Guide
```
📦 Tiny:   < 100KB  - Perfect for simple icons
📦 Small:  100-500KB - Good for most avatars
📦 Medium: 500KB-2MB - High quality, larger images
📦 Large:  2-10MB   - Very high quality (may be overkill)
⛔ Too Big: > 10MB  - Won't be accepted
```

## Success Indicators

After running `!image`, you should see:
- ✅ Green checkmark
- 📁 Original filename and size
- 💾 Backup file location
- 🎨 Confirmation of base64 conversion
- 📝 Instructions for loading the character

If you see ❌ (red X), read the error message carefully - it will tell you exactly what went wrong and how to fix it.

## Related Commands

- `!characters` - List all available characters
- `!character <name>` - Load a character (to see new avatar)
- `!current_character` - Check which character is loaded
- `!unload_character` - Unload current character

## Documentation

For more details, see:
- [IMAGE_COMMAND_GUIDE.md](IMAGE_COMMAND_GUIDE.md) - Complete user guide
- [IMAGE_UPLOAD_IMPLEMENTATION.md](IMAGE_UPLOAD_IMPLEMENTATION.md) - Technical details
- [PER_CHANNEL_AVATARS_GUIDE.md](PER_CHANNEL_AVATARS_GUIDE.md) - Avatar system guide
