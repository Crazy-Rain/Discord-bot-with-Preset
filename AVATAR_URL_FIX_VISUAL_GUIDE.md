# Avatar URL Fix - Visual Guide

## The Problem

### Before the Fix ❌

```
User uploads image via !image command
           ↓
Image converted to base64 data URL
           ↓
data:image/png;base64,iVBORw0KGg... (very long string)
           ↓
Stored in character card
           ↓
Used with Discord webhook
           ↓
❌ ERROR: "is not supported. Scheme must be one of ('http', 'https')"
           ↓
Bot fails to send response
```

### Error Message
```
"sw4wpeokvbqaaaaasuvork5cyii=" is not supported. 
Scheme must be one of ('http', 'https'). 
Not a well formed URL.
```

## The Solution

### After the Fix ✅

```
User uploads image via !image command
           ↓
Image saved to character_avatars/luna.png
           ↓
HTTP URL generated: http://localhost:5000/character_avatars/luna.png
           ↓
Stored in character card
           ↓
Web server serves image at /character_avatars/luna.png
           ↓
Used with Discord webhook
           ↓
✅ Discord loads avatar from HTTP URL
           ↓
Bot successfully sends response with character avatar
```

## Code Changes

### 1. Web Server - Serve Avatar Images

**File: `web_server.py`**

```python
@self.app.route('/character_avatars/<filename>')
def serve_character_avatar(filename):
    """Serve character avatar images."""
    avatars_dir = os.path.join(os.getcwd(), 'character_avatars')
    return send_from_directory(avatars_dir, filename)
```

### 2. Discord Bot - Generate HTTP URLs

**File: `discord_bot.py`**

```python
def get_web_server_url(self) -> str:
    """Get the web server URL from config."""
    web_config = self.config_manager.get("web_server", {})
    host = web_config.get("host", "0.0.0.0")
    port = web_config.get("port", 5000)
    
    if host == "0.0.0.0":
        host = "localhost"
    
    return f"http://{host}:{port}"
```

### 3. Image Upload - Use HTTP URLs

**File: `discord_bot.py` - `!image` command**

**Before:**
```python
# Convert to base64 data URL
base64_data = base64.b64encode(image_bytes).decode('utf-8')
data_url = f"data:{mime_type};base64,{base64_data}"
character_data['avatar_url'] = data_url
```

**After:**
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

### 4. Webhook - Validate URLs

**File: `discord_bot.py` - `send_as_character` method**

**Before:**
```python
if avatar_url and avatar_url.strip():
    webhook_params['avatar_url'] = avatar_url
```

**After:**
```python
# Only include avatar_url if it's a valid HTTP/HTTPS URL
# Discord webhooks don't support base64 data URLs
if avatar_url and avatar_url.strip() and (avatar_url.startswith('http://') or avatar_url.startswith('https://')):
    webhook_params['avatar_url'] = avatar_url
```

## Directory Structure

```
Discord-bot-with-Preset/
├── character_avatars/           # ← NEW: Avatar images stored here
│   ├── luna.png
│   ├── sherlock.jpg
│   └── aria.gif
├── character_cards/             # Character JSON files
│   ├── luna.json               # avatar_url: "http://localhost:5000/character_avatars/luna.png"
│   ├── sherlock.json
│   └── aria.json
├── discord_bot.py              # ← Modified: Use HTTP URLs
├── web_server.py               # ← Modified: Serve avatar images
├── migrate_avatar_urls.py      # ← NEW: Migration utility
├── test_avatar_url_fix.py      # ← NEW: Test suite
└── AVATAR_URL_FIX.md           # ← NEW: Documentation
```

## Usage Examples

### Upload Avatar

```
!image luna
[Attach luna.png to the message]

✅ Successfully updated avatar for luna!
📁 Image: luna.png (245.3 KB)
💾 Saved to: character_avatars/luna.png
🌐 Avatar URL: http://localhost:5000/character_avatars/luna.png

The new avatar will be used when this character is loaded with !character luna
```

### Load Character

```
!character luna

✅ Character loaded: Luna
The AI will now respond as this character with their avatar.
```

### Chat with Character

```
!chat Hello Luna!

[Bot responds as Luna with avatar displayed via webhook]
Luna: Hello! How can I help you today? 😊
```

## Migration

If you have existing characters with base64 avatars:

```bash
python3 migrate_avatar_urls.py
```

**Output:**
```
======================================================================
CHARACTER AVATAR MIGRATION UTILITY
======================================================================

Using web server URL from config: http://localhost:5000

======================================================================
✓ Migrated luna: 245.3 KB → http://localhost:5000/character_avatars/luna.png
✓ Migrated sherlock: 189.7 KB → http://localhost:5000/character_avatars/sherlock.jpg
⊘ Skipping aria: Already using HTTP URL or no avatar

======================================================================
MIGRATION SUMMARY
======================================================================
✓ Migrated: 2
⊘ Skipped: 1
❌ Errors: 0
Total: 3

✅ Migration complete!
```

## Testing

```bash
python3 test_avatar_url_fix.py
```

**Output:**
```
======================================================================
AVATAR URL FIX VERIFICATION
======================================================================

🔧 Testing web server avatar route...
  ✓ Found avatar route: /character_avatars/<filename>

🔧 Testing web server URL generation...
  ✓ Generated URL: http://localhost:5000

🔧 Testing webhook URL validation...
  ✓ Valid HTTP URL: Included (as expected)
  ✓ Valid HTTPS URL: Included (as expected)
  ✓ Base64 data URL (should be filtered): Filtered (as expected)
  ✓ Empty string: Filtered (as expected)
  ✓ None: Filtered (as expected)

🔧 Testing image command logic...
  ✓ Generated HTTP URL: http://localhost:5000/character_avatars/test_character.png
  ✓ No base64 data in URL

======================================================================
SUMMARY
======================================================================
✅ PASSED - Web Server Route
✅ PASSED - Web Server URL Generation
✅ PASSED - Webhook URL Validation
✅ PASSED - Image Command Logic

======================================================================
✅ All tests passed!
```

## Benefits

✅ **Fixed Error** - No more "scheme must be one of" errors  
✅ **Working Avatars** - Character avatars display correctly in Discord  
✅ **Better Performance** - Images served via HTTP are more efficient than base64  
✅ **Cleaner Code** - Separation of concerns (images in files, URLs in character data)  
✅ **Easy Migration** - One command to convert existing base64 avatars  
✅ **Robust Validation** - Webhook logic filters invalid URLs automatically  

## Notes

- Web server must be running for avatars to work
- Avatar images are cached by Discord for better performance
- Maximum file size: 10MB (Discord limit)
- Supported formats: PNG, JPG, GIF
- Avatar URLs are stored in character JSON files
