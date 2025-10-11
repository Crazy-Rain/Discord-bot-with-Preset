# Quick Fix Guide: "NO SERVERS" Issue

## TL;DR - Quick Solutions

### 1. Most Common: Bot Not in Any Servers
**You'll see:** "Bot is connected but is not in any servers"

**Fix:**
```bash
# 1. Get your OAuth2 URL from Discord Developer Portal
# 2. Add bot to a server
# 3. Restart: python main.py
```

### 2. Timing Issue: Opened Too Early
**You'll see:** "Bot instance not available"

**Fix:**
```bash
# Wait for this message in console:
# "Bot is ready! Logged in as YourBot#1234"
# "✅ Bot is in X server(s):"
# THEN refresh your browser at http://localhost:5000
```

### 3. Using `uv run` or Similar Tools
**You'll see:** Various import errors or "bot instance not available"

**Fix:**
```bash
# Use standard Python instead:
python main.py
# or
python3 main.py
```

## Step-by-Step Solution

### Step 1: Check Console Output

When you start the bot, you should see:
```
🤖 Starting Discord bot...
🔄 Creating bot instance for initial connection...
Bot is ready! Logged in as YourBot#1234
✅ Bot is in 2 server(s):
   - My Server (ID: 123456789, 5 text channels)
   - Test Server (ID: 987654321, 3 text channels)
```

If you see:
```
⚠️ WARNING: Bot is connected but not in any servers!
```

You need to add the bot to a Discord server (see Step 2).

### Step 2: Add Bot to a Discord Server

1. Go to https://discord.com/developers/applications
2. Select your bot application
3. Click **OAuth2** → **URL Generator**
4. Check these boxes:
   - Under **Scopes**: `bot`
   - Under **Bot Permissions**: 
     - Read Messages/View Channels ✓
     - Send Messages ✓
     - Manage Webhooks ✓
5. Copy the generated URL at the bottom
6. Paste it in your browser
7. Select a server and click "Authorize"
8. Restart the bot: `python main.py`

### Step 3: Verify in Web Interface

1. Make sure console shows "✅ Bot is in X server(s):"
2. Open http://localhost:5000
3. Click **Manual Send** tab
4. You should see servers in the dropdown

If still showing "NO SERVERS":
- Refresh the page
- Check `/api/health` endpoint (see Step 4)

### Step 4: Check Health Status

Open in browser: http://localhost:5000/api/health

**Good Response:**
```json
{
  "bot_connected": true,
  "bot_name": "YourBot#1234",
  "guild_count": 2,
  "issues": []
}
```

**Bad Response:**
```json
{
  "bot_connected": false,
  "issues": [
    "Bot is connected but not in any servers"
  ]
}
```

Follow the recommendations in the `issues` array.

## Diagnostic Tools

### Run Comprehensive Diagnostic
```bash
python diagnose_guild_detection.py
```

This will check everything and tell you exactly what's wrong.

### Check API Endpoints Manually
```bash
# Check if bot sees servers
curl http://localhost:5000/api/servers

# Check if bot sees channels
curl http://localhost:5000/api/manual_send/channels

# Check bot health
curl http://localhost:5000/api/health
```

## Auto-Retry Feature

The web interface now automatically retries loading servers if the bot hasn't connected yet:

- **Manual Send tab**: Retries up to 3 times, every 3 seconds
- **Servers/Channels tab**: Retries up to 3 times, every 3 seconds

You'll see a message: "🔄 Will automatically retry in 3 seconds... (Attempt 1/3)"

## Still Not Working?

1. **Complete restart:**
   ```bash
   # Stop bot (Ctrl+C)
   # Wait 3 seconds
   python main.py
   # Wait for "Bot is ready!" message
   # Open http://localhost:5000
   ```

2. **Check Discord Developer Portal:**
   - Bot section
   - Message Content Intent should be **ON**
   - (Guilds intent is NOT privileged, should work by default)

3. **Verify bot token:**
   - Check `config.json`
   - Make sure token is not `"YOUR_DISCORD_BOT_TOKEN"`
   - Get token from Discord Developer Portal → Bot → Reset Token

4. **Run diagnostic:**
   ```bash
   python diagnose_guild_detection.py
   ```

5. **Read full guide:**
   - See `TROUBLESHOOTING_NO_SERVERS.md` for detailed troubleshooting

## Common Error Messages Explained

| Error Message | Cause | Solution |
|---------------|-------|----------|
| "Bot instance not available" | Bot hasn't started or crashed | Check console for errors, restart bot |
| "Bot is connected but is not in any servers" | Bot not added to any Discord servers | Use OAuth2 URL to add bot to a server |
| "Bot Not Connected to Discord" | Bot instance is None | Wait for bot to connect, check console |
| "Cannot import main module" | Module isolation (uv, venv issues) | Use `python main.py` instead |

## What's New

### Improved Error Messages
- API endpoints now return detailed `bot_status` and `message`
- Frontend shows specific instructions based on the issue
- Console logs guild information on connection

### Health Check Endpoint
- `/api/health` - Check bot status at any time
- Shows connected guilds and diagnostic info

### Auto-Retry
- Automatically retries loading if bot not connected
- Shows retry countdown
- Up to 3 attempts with 3-second delays

### Better Logging
- Console shows guild count on connection
- Lists all servers bot is in
- Warning if bot has no servers
