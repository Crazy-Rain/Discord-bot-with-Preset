# Image Upload Command Guide

## Overview

The `!image` command allows you to update a character's avatar directly from Discord by attaching an image file to your message. This provides a convenient way to set character avatars without using the web interface.

## Usage

```
!image <character_name>
```

**Attach an image file (PNG, JPG, or GIF) to your message when using this command.**

## Features

- ✅ **Direct Discord Upload** - Upload images directly from Discord chat
- ✅ **Multiple Format Support** - Supports PNG, JPG, JPEG, and GIF formats
- ✅ **Size Validation** - Automatically validates file size (max 10MB)
- ✅ **Format Validation** - Ensures only valid image formats are accepted
- ✅ **Base64 Conversion** - Converts images to base64 data URLs for storage
- ✅ **Auto-Save** - Automatically saves both to character card and backup file
- ✅ **Live Updates** - If character is loaded, avatar updates immediately

## How It Works

1. **Upload**: You send the `!image` command with a character name and attach an image
2. **Validate**: The bot validates the image format and size
3. **Convert**: The image is converted to a base64 data URL
4. **Save**: The avatar is saved to the character's JSON file
5. **Backup**: A copy is also saved to the `character_avatars/` directory
6. **Update**: If the character is loaded in the channel, it updates immediately

## Examples

### Example 1: Basic Usage

```
!image luna
```

*Attach `luna-avatar.png` to this message*

**Result:**
```
✅ Successfully updated avatar for Luna!
📁 Image: luna-avatar.png (245.3 KB)
💾 Saved to: character_avatars/luna.png
🎨 Avatar converted to base64 data URL and stored in character card.

The new avatar will be used when this character is loaded with !character luna
```

### Example 2: Update Existing Character

```
!image sherlock
```

*Attach `detective.jpg` to this message*

**Result:**
- Previous avatar is replaced with the new one
- Character card is updated with the new base64 data URL
- Backup file is created/updated in `character_avatars/sherlock.jpg`

### Example 3: Update Active Character

If you have a character loaded in the current channel:

```
!character aria
!chat Hello!              # Aria responds with old avatar
!image aria               # Upload new avatar
!chat How are you?        # Aria responds with new avatar
```

## Supported Formats

- **PNG** (.png)
- **JPG/JPEG** (.jpg, .jpeg)
- **GIF** (.gif)

## File Size Limits

- **Maximum**: 10MB (Discord's standard limit)
- **Recommended**: Under 1MB for faster processing
- **Optimal**: 256x256 to 512x512 pixels, under 500KB

## Error Messages

### No Image Attached
```
❌ No image attached! Please attach an image file (PNG, JPG, or GIF) to your message.
Usage: `!image <character_name>` with an image attached
```

**Solution**: Make sure to attach an image file to your message.

### Invalid File Type
```
❌ Invalid file type: .pdf
Only PNG, JPG, and GIF files are supported.
```

**Solution**: Use a PNG, JPG, or GIF file instead.

### File Too Large
```
❌ File too large: 15.23MB
Maximum file size is 10MB. Please use a smaller image.
```

**Solution**: Resize or compress your image to under 10MB.

### Character Not Found
```
❌ Character not found: unknown_char
Use `!characters` to see available characters.
```

**Solution**: Check the character name spelling or create the character first.

## Best Practices

### Image Quality

- Use **square images** for best results (Discord crops to square)
- Recommended dimensions: **256x256** or **512x512** pixels
- Use **PNG** for images with transparency
- Use **JPG** for photographs to save space

### File Size Optimization

- Compress images before uploading for faster processing
- Keep images under 1MB when possible
- Use online tools like TinyPNG or Squoosh to compress

### Workflow

1. **Create character** via web interface or have it already created
2. **Upload avatar** using `!image` command
3. **Load character** with `!character` command
4. **Test** with `!chat` to see avatar in action

## Storage Details

### Character Card

The avatar is stored directly in the character card JSON file as a base64 data URL:

```json
{
  "name": "Luna",
  "personality": "Friendly and mysterious",
  "description": "A lunar deity with silver hair",
  "avatar_url": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```

### Backup File

A copy of the original image is also saved to:

```
character_avatars/<character_name>.<extension>
```

Example: `character_avatars/luna.png`

This allows you to:
- Keep a high-quality original
- Re-use the image elsewhere
- Have a backup if needed

## Comparison with Web Interface

| Feature | !image Command | Web Interface |
|---------|----------------|---------------|
| Upload from Discord | ✅ Yes | ❌ No |
| Upload from Computer | ❌ No | ✅ Yes |
| File Size Limit | 10MB | 10MB |
| Format Validation | ✅ Yes | ✅ Yes |
| Preview | ❌ No | ✅ Yes |
| Convenience in Discord | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Editing Character Data | ❌ No | ✅ Yes |

**Recommendation**: Use `!image` for quick avatar updates from Discord, use web interface for full character editing.

## Integration with Other Features

### Per-Channel Avatars

When you use `!image` to update a character's avatar and that character is currently loaded in a channel:

```
!character luna           # Load Luna
!chat Hello!             # Luna responds with old avatar
!image luna              # Update avatar (with attachment)
!chat How are you?       # Luna responds with NEW avatar
```

The avatar updates immediately without needing to reload the character.

### Character Cards

The `!image` command only updates the `avatar_url` field. All other character data (personality, description, etc.) remains unchanged.

To edit other fields, use the web interface at `http://localhost:5000`.

## Tips and Tricks

### Quick Avatar Updates

Keep a collection of character avatars on your device, then use Discord to quickly update them:

```
!image luna      # Attach luna1.png
!image aria      # Attach aria1.png
!image sherlock  # Attach sherlock1.png
```

### Sharing Avatars

Since the avatar is stored as base64 in the character card, you can:
1. Export the character card (web interface)
2. Share the JSON file
3. Other users can import and have the same avatar

### Backup Strategy

The bot saves two copies:
- **In character card**: For portability
- **In character_avatars/**: For backup and reference

This ensures you always have access to the original image file.

## Troubleshooting

### "Permission Denied" Errors

If you get permission errors when saving to `character_avatars/`:

1. Check file permissions on the directory
2. Ensure the bot has write access
3. Try running with appropriate permissions

### Image Not Displaying

If the avatar doesn't show up in webhooks:

1. Verify the character was saved: check the character card JSON
2. Reload the character: `!unload_character` then `!character <name>`
3. Check Discord webhook permissions: Bot needs "Manage Webhooks"

### Large JSON Files

Base64 encoding increases file size by ~33%. For large images:

- 1MB image → ~1.3MB base64
- 5MB image → ~6.5MB base64

Consider compressing images before upload.

## Related Commands

- `!character <name>` - Load a character with its avatar
- `!current_character` - Check which character is loaded
- `!unload_character` - Unload current character
- `!characters` - List all available characters

## Related Documentation

- [PER_CHANNEL_AVATARS_GUIDE.md](PER_CHANNEL_AVATARS_GUIDE.md) - Guide to per-channel avatar system
- [CHARACTER_AVATAR_GUIDE.md](CHARACTER_AVATAR_GUIDE.md) - General avatar feature guide
- [AVATAR_UPLOAD_GUIDE.md](AVATAR_UPLOAD_GUIDE.md) - Web interface upload guide
