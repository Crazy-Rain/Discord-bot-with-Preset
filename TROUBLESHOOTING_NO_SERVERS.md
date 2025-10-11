# Troubleshooting Guide: "NO SERVERS" Issue

## Problem
When you open the web interface and click on the **Manual Send** tab or **Servers/Channels** tab, you see "NO SERVERS" even though the bot appears as **Online and Active** in Discord.

## Quick Diagnosis

### Step 1: Run the Diagnostic Tool
```bash
python diagnose_guild_detection.py
```

This will check:
- Configuration
- Bot instance accessibility
- WebServer bot access
- API endpoints
- Discord intents

### Step 2: Check the Health Endpoint
Open your browser and navigate to:
```
http://localhost:5000/api/health
```

This will show you the exact status of the bot and any issues.

## Common Causes and Solutions

### 1. Bot Not Added to Any Servers ⚠️

**Symptoms:**
- Bot shows as "Online" in Discord Developer Portal
- Console shows: "Bot is ready! Logged in as YourBot#1234"
- Console shows: "⚠️ WARNING: Bot is connected but not in any servers!"
- Web interface shows detailed message about bot not being in any servers

**Solution:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your bot application
3. Navigate to **OAuth2** → **URL Generator**
4. Select the following scopes:
   - `bot` (required)
5. Select bot permissions (minimum):
   - Read Messages/View Channels
   - Send Messages
   - Manage Webhooks (for character avatars)
6. Copy the generated URL
7. Open it in your browser and add the bot to a server
8. Restart the bot: `python main.py`

### 2. Timing Issue - Web Interface Opened Too Early ⏰

**Symptoms:**
- You open http://localhost:5000 immediately after starting the bot
- The bot hasn't finished connecting to Discord yet

**Solution:**
1. Wait for the "Bot is ready!" message in console:
   ```
   Bot is ready! Logged in as YourBot#1234
   ✅ Bot is in X server(s):
      - Server Name (ID: 123456789, 5 text channels)
   ```
2. **Then** open or refresh http://localhost:5000
3. Check the Manual Send tab - servers should now appear

### 3. Module Import Issue with `uv run` 🔧

**Symptoms:**
- Using `uv run main.py` to start the bot
- Bot connects but web interface can't see it
- Health endpoint shows: "Cannot import main module"

**Solution:**
Try running the bot with standard Python instead:
```bash
python main.py
# or
python3 main.py
```

If you must use `uv`, ensure it's not isolating the modules.

### 4. Guilds Intent Not Enabled in Discord Portal 🔐

**Note:** The guilds intent is **not** a privileged intent and should work by default. However, verify:

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your bot application
3. Go to **Bot** section
4. Under **Privileged Gateway Intents**, ensure:
   - **Message Content Intent** is **ON** (for reading messages)
   - **Server Members Intent** is optional (not needed for this issue)
5. Save changes
6. Restart the bot

### 5. Bot Instance Not Updating 🔄

**Symptoms:**
- Bot has been running for a while
- Reconnected but web interface doesn't update

**Solution:**
1. Completely stop the bot (Ctrl+C)
2. Wait 2-3 seconds
3. Start it again: `python main.py`
4. Wait for "Bot is ready!" message
5. Refresh the web interface

## Understanding the Error Messages

The web interface now shows detailed error messages:

### "Bot instance not available"
- The bot hasn't started yet or failed to start
- Check console for errors

### "Bot is connected but is not in any servers"
- Bot is authenticated with Discord
- But not added to any Discord servers
- Follow the OAuth2 URL steps above

### "Bot Not Connected to Discord"
- Generic message when bot_instance is None
- Could be before connection or after a crash
- Check console logs

## Verification Steps

### 1. Check Console Output
When the bot starts successfully, you should see:
```
🤖 Starting Discord bot...
🔄 Creating bot instance for initial connection...
Bot is ready! Logged in as YourBot#1234
✅ Bot is in 2 server(s):
   - My Server (ID: 123456789, 5 text channels)
   - Test Server (ID: 987654321, 3 text channels)
```

### 2. Check Health Endpoint
```bash
curl http://localhost:5000/api/health
```

Expected response when working:
```json
{
  "web_server": "running",
  "bot_connected": true,
  "bot_name": "YourBot#1234",
  "guild_count": 2,
  "guilds": [
    {"id": "123456789", "name": "My Server", "channels": 5},
    {"id": "987654321", "name": "Test Server", "channels": 3}
  ],
  "issues": [],
  "main_module": "accessible"
}
```

### 3. Check API Endpoints
```bash
# Check servers
curl http://localhost:5000/api/servers

# Check manual send channels
curl http://localhost:5000/api/manual_send/channels
```

## Advanced Debugging

### Enable Debug Logging
The web server and bot now include debug information in console output.

Look for messages like:
- `⚠️ WARNING: Bot is connected but not in any servers!`
- `✅ Bot is in X server(s):`
- Error messages about missing guilds or connections

### Check Discord.py Version
```bash
pip show discord.py
```

Ensure you have version 2.3.2 or higher.

### Verify Configuration
Check `config.json`:
```json
{
  "discord_token": "YOUR_ACTUAL_TOKEN_HERE",
  ...
}
```

Make sure the token is not `"YOUR_DISCORD_BOT_TOKEN"` (placeholder).

## Still Having Issues?

If none of the above solutions work:

1. **Run the comprehensive diagnostic:**
   ```bash
   python diagnose_guild_detection.py
   ```

2. **Check the diagnostic output** and follow the specific recommendations

3. **Verify bot permissions** in each Discord server:
   - Right-click the bot in the member list
   - Check it has necessary permissions
   - Ensure it can see channels

4. **Test with a fresh Discord server:**
   - Create a new test server
   - Add the bot to it
   - See if it appears in the web interface

5. **Check firewall/network:**
   - Ensure port 5000 is accessible
   - No proxy blocking Discord connections

## Summary Checklist

Before opening an issue, verify:

- [ ] Bot token is configured correctly
- [ ] Bot shows "Bot is ready!" in console
- [ ] Console shows `✅ Bot is in X server(s)` (not 0 servers)
- [ ] Bot is actually added to at least one Discord server
- [ ] You waited for bot to connect before opening web interface
- [ ] You refreshed the web page after bot connected
- [ ] Health endpoint (`/api/health`) shows `bot_connected: true`
- [ ] Running with `python main.py` (not `uv run` or other tools)
- [ ] Discord Developer Portal has Message Content Intent enabled
- [ ] No errors in console about missing modules or import failures

## Files for Debugging

- `diagnose_guild_detection.py` - Comprehensive diagnostic tool
- `diagnose_bot_connection.py` - Connection flow simulator
- `test_real_bot_connection.py` - Real bot connection test
- Health endpoint: `http://localhost:5000/api/health`
