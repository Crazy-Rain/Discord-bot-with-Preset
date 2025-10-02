# Character Avatar Feature

## Overview

The bot now supports setting a custom avatar/profile picture for each character. When you load a character with an avatar URL, the bot's Discord profile picture will automatically update to match the character's image.

## How to Use

### Via Web Interface

1. Navigate to http://localhost:5000
2. Go to the "Characters" tab
3. Create or edit a character
4. In the "Avatar URL" field, enter a direct URL to an image:
   - Example: `https://i.imgur.com/example.png`
   - Supported formats: PNG, JPG, GIF
   - Recommended size: 256x256 or larger (Discord will resize)
5. Click "Save Character"
6. Load the character using `!character <name>` in Discord

### Via Discord Commands

When you load a character that has an avatar URL configured:

```
User: !character luna
Bot: Loaded character: luna
Bot: ✨ Updated bot avatar to match Luna
```

The bot's profile picture will change to the image at the specified URL.

## Character Card JSON Format

Character cards now support an optional `avatar_url` field:

```json
{
  "name": "Luna",
  "personality": "Friendly, empathetic, supportive, creative",
  "description": "A warm and caring AI companion...",
  "scenario": "You are chatting with users...",
  "system_prompt": "",
  "avatar_url": "https://example.com/luna-avatar.png"
}
```

## Features

- **Automatic Updates**: Avatar changes automatically when loading a character
- **Startup Support**: If a character is already loaded, the avatar is set on bot startup
- **Error Handling**: If the avatar URL is invalid or unreachable, the bot continues to work normally
- **Optional**: The `avatar_url` field is optional - leave it empty if you don't want to change the avatar

## Technical Details

### How It Works

1. When a character is loaded, the bot checks for an `avatar_url` field
2. If present, the bot downloads the image from the URL
3. The image is converted to bytes and used to update the bot's Discord avatar
4. The avatar change is global - it applies across all servers

### Rate Limits

Discord has rate limits on avatar changes:
- You can change the avatar at most 2 times per hour
- Exceeding this limit will result in errors (gracefully handled)
- Plan your character switches accordingly

### Image Requirements

- **Format**: PNG, JPG, or GIF
- **Size**: Maximum 10MB file size
- **Recommended dimensions**: 256x256 or larger (Discord will resize)
- **URL**: Must be a direct link to an image file
- **Accessibility**: The URL must be publicly accessible (not behind authentication)

## Examples

### Example 1: Using Imgur

1. Upload an image to Imgur
2. Right-click the image and select "Copy image address"
3. Use that URL in the character's `avatar_url` field
4. Example: `https://i.imgur.com/abc123.png`

### Example 2: Using Discord CDN

1. Upload an image to Discord (in any channel or DM)
2. Right-click the image and select "Copy link"
3. Use that URL in the character's `avatar_url` field
4. Example: `https://cdn.discordapp.com/attachments/...`

### Example 3: Using Direct Links

Any direct link to an image file works:
- GitHub: `https://raw.githubusercontent.com/user/repo/main/avatar.png`
- Direct URLs: `https://example.com/images/character.jpg`
- CDNs: Any CDN that serves images directly

## Troubleshooting

### Avatar Not Changing

1. **Check the URL**: Make sure it's a direct link to an image (ends in .png, .jpg, .gif)
2. **Check accessibility**: Open the URL in a browser to verify it loads
3. **Check rate limits**: Wait at least 30 minutes between avatar changes
4. **Check bot logs**: Look for error messages in the console output

### Avatar Quality Issues

- Use higher resolution images (at least 256x256)
- Ensure the image is square (Discord crops non-square images)
- Use PNG for best quality with transparency

### Privacy Considerations

- The avatar URL is stored in the character card JSON file
- Anyone with access to the character cards folder can see the URL
- Don't use private/sensitive images accessible only to you

## Permissions

No special Discord permissions are required to change the bot's avatar. This is a bot-wide change that the bot owner can always perform.

## Differences from Nickname

| Feature | Nickname | Avatar |
|---------|----------|--------|
| **Scope** | Per-server | Global (all servers) |
| **Permission Required** | "Change Nickname" | None (bot owner action) |
| **Rate Limit** | None | 2 per hour |
| **Field Type** | Text | Image URL |

## Best Practices

1. **Use reliable hosting**: Use established image hosting services (Imgur, Discord CDN, etc.)
2. **Keep images appropriate**: The avatar will be visible to all users in all servers
3. **Test first**: Verify the URL works before saving the character
4. **Plan switches**: Be mindful of the 2-per-hour rate limit
5. **Use consistent styling**: Keep character avatars visually consistent for better UX

## Limitations

- Discord's 2-per-hour rate limit on avatar changes
- Image must be publicly accessible via URL
- Maximum 10MB file size per Discord's limits
- Avatar is global (cannot be different per server)
