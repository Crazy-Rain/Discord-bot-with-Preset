# Avatar URL Fix - Quick Start Guide

## Problem Fixed

**Error:** `"sw4wpeokvbqaaaaasuvork5cyii=" is not supported. Scheme must be one of ('http', 'https')`

**Cause:** Discord webhooks don't accept base64 data URLs for avatars

**Solution:** Character avatars now use HTTP URLs served by the web server

## Quick Fix (For New Users)

Just use the bot normally! The fix is already implemented:

1. Start the bot:
   ```bash
   python main.py
   ```

2. Upload a character avatar:
   ```
   !image luna
   [Attach luna.png to your Discord message]
   ```

3. Load the character:
   ```
   !character luna
   ```

4. Chat with the character:
   ```
   !chat Hello!
   ```

The bot will now successfully send responses with the character avatar! ✅

## Migration (For Existing Users with Base64 Avatars)

If you have existing characters with base64 avatars, convert them:

```bash
python3 migrate_avatar_urls.py
```

This will:
- Extract images from base64 data
- Save them to `character_avatars/` directory
- Update character cards with HTTP URLs

## How It Works

### Before (Broken)
```
Character avatar → Base64 data URL → Discord webhook → ❌ Error
```

### After (Fixed)
```
Character avatar → Saved to file → HTTP URL → Discord webhook → ✅ Success
```

## File Locations

```
character_avatars/          # Avatar images stored here
  ├── luna.png
  ├── sherlock.jpg
  └── aria.gif

character_cards/            # Character data (includes HTTP URL)
  ├── luna.json            # avatar_url: "http://localhost:5000/character_avatars/luna.png"
  ├── sherlock.json
  └── aria.json
```

## Configuration

Avatar URLs use your web server configuration from `config.json`:

```json
{
  "web_server": {
    "host": "0.0.0.0",
    "port": 5000
  }
}
```

Default URL: `http://localhost:5000`

## Testing

Verify the fix is working:

```bash
python3 test_avatar_url_fix.py
```

Expected output:
```
✅ All tests passed!
```

## Troubleshooting

### Avatar not displaying?

1. **Check web server is running:**
   - The bot should print: `🌐 Web configuration interface starting at http://localhost:5000`

2. **Verify avatar URL in character card:**
   ```bash
   cat character_cards/luna.json | grep avatar_url
   ```
   Should show: `"avatar_url": "http://localhost:5000/character_avatars/luna.png"`

3. **Check image file exists:**
   ```bash
   ls -la character_avatars/
   ```
   Should show: `luna.png` (or your character's image)

4. **Test the URL directly:**
   - Open in browser: `http://localhost:5000/character_avatars/luna.png`
   - Should display the image

### Still using base64?

Run the migration utility:
```bash
python3 migrate_avatar_urls.py
```

## Documentation

- **FIX_SUMMARY_PR43.md** - Complete technical summary
- **AVATAR_URL_FIX.md** - Detailed documentation
- **AVATAR_URL_FIX_VISUAL_GUIDE.md** - Visual guide with examples

## What Changed

### Code Changes
- `web_server.py` - Added route to serve avatar images
- `discord_bot.py` - Generate HTTP URLs instead of base64

### New Files
- `test_avatar_url_fix.py` - Test suite
- `migrate_avatar_urls.py` - Migration utility
- `character_avatars/` - Directory for avatar images

## Benefits

✅ **Working Avatars** - No more "scheme must be one of" errors  
✅ **Better Performance** - HTTP images load faster than base64  
✅ **Cleaner Code** - Images in files, URLs in character data  
✅ **Easy Migration** - One command to convert existing avatars  

## Support

If you encounter issues:

1. Run the test suite: `python3 test_avatar_url_fix.py`
2. Check the logs when starting the bot
3. Verify web server is accessible
4. Ensure `character_avatars/` directory exists

The fix is minimal, focused, and fully tested. It completely resolves the issue reported in PR #43! 🎉
