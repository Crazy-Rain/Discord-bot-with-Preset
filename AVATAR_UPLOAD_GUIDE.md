# Avatar Upload Feature

## Overview

You can now upload image files directly through the web interface instead of only providing URLs. This makes it easier to use custom avatar images without needing to host them elsewhere.

## How to Use

### Via Web Interface

1. Navigate to http://localhost:5000
2. Go to the "Characters" tab
3. Create or edit a character
4. In the "Avatar" section, you'll see two options:
   - **Use Image URL**: Enter a direct URL to an image
   - **Upload Image File**: Upload an image from your computer
5. Select "Upload Image File"
6. Click "Choose File" and select an image (PNG, JPG, or GIF)
7. Preview the image before saving
8. Click "Save Character"
9. The image is automatically stored and will be used as the bot's avatar

### Supported Formats

- **PNG** (.png)
- **JPG/JPEG** (.jpg, .jpeg)
- **GIF** (.gif)

### File Size Limits

- Maximum file size: 10MB (Discord's limit)
- Recommended: Keep images under 1MB for faster uploads

## How It Works

### Storage

When you upload an image:
1. The file is temporarily saved to the `character_avatars/` directory
2. The image is converted to a base64 data URL
3. The data URL is stored in the character card's `avatar_url` field
4. The bot uses this data URL to update its Discord avatar

### Data URL Format

Uploaded images are stored as base64 data URLs in the character card JSON:

```json
{
  "name": "Luna",
  "personality": "Friendly...",
  "description": "...",
  "avatar_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

This means:
- No external hosting required
- Avatar image is embedded directly in the character card
- Character cards are fully self-contained
- Easy to export/import characters with their avatars

## Benefits of Upload vs URL

| Feature | Upload | URL |
|---------|--------|-----|
| **Ease of Use** | ✅ Very easy | ⚠️ Need hosting |
| **Portability** | ✅ Self-contained | ❌ Depends on external URL |
| **Privacy** | ✅ Stays local | ❌ Public URL needed |
| **Speed** | ⚠️ One-time upload | ✅ Fast loading |
| **File Size** | ⚠️ Increases JSON size | ✅ No JSON impact |

## Best Practices

### When to Use Upload
- Personal/custom character avatars
- You don't want to manage external hosting
- Character cards you want to share with embedded images
- Privacy-sensitive images

### When to Use URL
- Images already hosted online
- Very large files (>1MB)
- When you need to update the image frequently
- Using CDN-hosted images

## Technical Details

### File Upload Process

1. User selects an image file
2. JavaScript previews the image
3. On save, file is uploaded to `/api/characters/upload_avatar`
4. Server validates file type and size
5. Image is saved temporarily with secure filename
6. Image is converted to base64 data URL
7. Data URL is returned to JavaScript
8. Character is saved with data URL in `avatar_url` field

### Security

- **Filename sanitization**: Uses `secure_filename()` to prevent path traversal
- **File type validation**: Only allows PNG, JPG, and GIF
- **Size limits**: Enforced by Flask and Discord API
- **Temporary storage**: Files in `character_avatars/` are just temporary

### Discord Integration

The bot's `update_bot_avatar()` method handles both types:

```python
if avatar_url.startswith('data:image'):
    # Parse base64 data URL
    header, encoded = avatar_url.split(',', 1)
    avatar_bytes = base64.b64decode(encoded)
else:
    # Download from URL
    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as response:
            avatar_bytes = await response.read()

# Update Discord avatar
await self.user.edit(avatar=avatar_bytes)
```

## Troubleshooting

### Upload Button Not Showing

Make sure you're using a modern browser that supports file input elements.

### Preview Not Showing

Check browser console for errors. The preview uses FileReader API.

### Upload Fails

Common causes:
- File is too large (>10MB)
- Invalid file format (not PNG, JPG, or GIF)
- Permissions issue with `character_avatars/` directory

### Character Card Too Large

If the character JSON becomes very large due to embedded images:
- Consider using URL method instead for large images
- Compress images before uploading
- Use PNG with lower color depth

## Migration Notes

### Existing Characters

Characters with URL-based avatars continue to work exactly as before. No migration needed.

### Switching Methods

You can switch between upload and URL methods at any time:
1. Edit the character
2. Select the method you want
3. Provide new avatar (upload or URL)
4. Save

The previous avatar data is simply replaced.

## Examples

### Example 1: Upload PNG Avatar

1. Create/edit character "Luna"
2. Select "Upload Image File"
3. Choose `luna-avatar.png` from your computer
4. See preview
5. Save character
6. Character JSON now contains: `"avatar_url": "data:image/png;base64,..."`

### Example 2: Switch from URL to Upload

1. Character currently has: `"avatar_url": "https://i.imgur.com/abc.png"`
2. Edit character
3. Select "Upload Image File"
4. Upload new image
5. Save
6. Character JSON now has embedded base64 image instead of URL

## Limitations

- **JSON size**: Embedded images increase character card file size
- **No image editing**: Upload and save as-is (edit externally if needed)
- **One image per character**: Can't have multiple avatars
- **Discord rate limits**: Still limited to 2 avatar changes per hour

## Future Enhancements

Possible future improvements:
- Image compression/optimization before embedding
- Multiple avatar options per character
- Avatar gallery/library
- Drag-and-drop upload
- Image cropping/editing interface
