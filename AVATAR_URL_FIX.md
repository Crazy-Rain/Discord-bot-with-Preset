# Avatar URL Fix - Discord Webhook Compatibility

## Problem

The bot was experiencing an error when trying to send messages with character avatars:

```
"sw4wpeokvbqaaaaasuvork5cyii=" is not supported. Scheme must be one of ('http', 'https'). Not a well formed URL.
```

This error occurred because:
1. Character avatars were being stored as base64 data URLs (e.g., `data:image/png;base64,iVBORw0KG...`)
2. Discord webhooks only accept HTTP/HTTPS URLs for avatars
3. When the bot tried to use base64 data URLs with webhooks, Discord rejected them

## Solution

The fix involves three key changes:

### 1. Web Server Route for Avatar Images

Added a new route in `web_server.py` to serve character avatar images via HTTP:

```python
@self.app.route('/character_avatars/<filename>')
def serve_character_avatar(filename):
    """Serve character avatar images."""
    avatars_dir = os.path.join(os.getcwd(), 'character_avatars')
    return send_from_directory(avatars_dir, filename)
```

### 2. Modified Image Upload Command

Updated the `!image` command in `discord_bot.py` to:
- Save avatar images to the `character_avatars/` directory
- Generate HTTP URLs instead of base64 data URLs
- Store HTTP URLs in character cards

Before:
```python
# Convert to base64 data URL
base64_data = base64.b64encode(image_bytes).decode('utf-8')
data_url = f"data:{mime_type};base64,{base64_data}"
character_data['avatar_url'] = data_url
```

After:
```python
# Save image file
filepath = os.path.join(avatars_dir, f"{character_name}.{file_ext}")
with open(filepath, 'wb') as f:
    f.write(image_bytes)

# Create HTTP URL
web_server_url = self.get_web_server_url()
avatar_url = f"{web_server_url}/character_avatars/{character_name}.{file_ext}"
character_data['avatar_url'] = avatar_url
```

### 3. Webhook URL Validation

Updated webhook logic to filter out invalid URLs and only use HTTP/HTTPS:

```python
# Only include avatar_url if it's a valid HTTP/HTTPS URL
# Discord webhooks don't support base64 data URLs
if avatar_url and avatar_url.strip() and (avatar_url.startswith('http://') or avatar_url.startswith('https://')):
    webhook_params['avatar_url'] = avatar_url
```

## How It Works

1. **Upload**: When you use `!image <character_name>` with an attached image:
   - Image is saved to `character_avatars/<character_name>.<ext>`
   - HTTP URL is generated (e.g., `http://localhost:5000/character_avatars/luna.png`)
   - Character card is updated with the HTTP URL

2. **Serve**: The web server serves avatar images at `/character_avatars/<filename>`

3. **Use**: When sending messages with webhooks:
   - Only HTTP/HTTPS URLs are passed to Discord
   - Base64 data URLs are filtered out
   - Discord successfully loads the avatar from the HTTP URL

## Migration

If you have existing characters with base64 avatar URLs, use the migration utility:

```bash
python3 migrate_avatar_urls.py
```

This will:
- Extract image data from base64 URLs
- Save images to `character_avatars/` directory
- Update character cards with HTTP URLs

## Files Modified

- `web_server.py` - Added route to serve avatar images
- `discord_bot.py` - Modified `!image` command and webhook logic
- `test_avatar_url_fix.py` - Test suite to verify the fix
- `migrate_avatar_urls.py` - Migration utility for existing characters
- `AVATAR_URL_FIX.md` - This documentation

## Testing

Run the test suite to verify the fix:

```bash
python3 test_avatar_url_fix.py
```

Expected output:
```
✅ All tests passed!

Fix implemented:
  ✓ Web server serves character avatars via HTTP
  ✓ !image command generates HTTP URLs instead of base64
  ✓ Webhook logic filters out base64 data URLs
  ✓ Only HTTP/HTTPS URLs are used for Discord webhooks

This fixes the error:
  "sw4wpeokvbqaaaaasuvork5cyii=" is not supported.
  Scheme must be one of ('http', 'https').
```

## Impact

### For Users
- ✅ Character avatars now work correctly with Discord webhooks
- ✅ No more "scheme must be one of" errors
- ✅ Bot can successfully send responses with character avatars
- ✅ Existing base64 avatars can be migrated with one command

### For Developers
- ✅ Cleaner architecture using HTTP URLs
- ✅ Avatar images are stored in a dedicated directory
- ✅ Web server properly serves static avatar files
- ✅ Webhook logic validates URLs before sending

## Notes

- Make sure the web server is running and accessible
- The web server URL is configured in `config.json` under `web_server.host` and `web_server.port`
- Avatar images are served from the `character_avatars/` directory
- Only PNG, JPG, and GIF formats are supported
- Maximum file size is 10MB per Discord's limits
