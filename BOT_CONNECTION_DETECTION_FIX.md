# Bot Connection Detection Fix

## Problem Statement

The bot was connected and active (showing in Discord as online), but the HTML web interface was not recognizing this fact:

1. **Servers/Channels Tab**: Showing "Bot Not Connected to Discord" even though the bot was connected
2. **Manual Send Tab**: No servers showing in dropdown, with message asking to ensure bot is connected

## Root Cause

The issue was in how the WebServer received the bot instance reference in `main.py`:

```python
# Line 104 in main.py - Creates placeholder bot
bot_instance = DiscordBot(config_manager)

# Line 19 in run_web_server() - Passes placeholder to WebServer
web_server = WebServer(config_manager, bot_instance)  # ← OLD placeholder!

# Line 50 in run_discord_bot() - Creates NEW bot that actually connects
bot_instance = DiscordBot(config_manager)  # ← ACTUAL connected bot
```

The WebServer stored the placeholder bot as `self._bot_instance_ref`, and the property logic prioritized this reference:

```python
# web_server.py property
@property
def bot_instance(self):
    # This check returned the OLD placeholder!
    if self._bot_instance_ref is not None:
        return self._bot_instance_ref  # ← Always returns OLD bot
    
    # Never reached this line:
    import main
    return main.bot_instance
```

### Why This Happened

1. **Line 104**: Placeholder `bot_instance` created before web server starts
2. **Line 19**: Web server initialized with this placeholder bot
3. **Line 50**: NEW `bot_instance` created that actually connects to Discord
4. **WebServer property**: Always returned the OLD placeholder because `_bot_instance_ref` was not None
5. **Result**: Web server never saw the connected bot's guilds

## Solution

**Remove the bot_instance parameter when initializing WebServer** in `run_web_server()`:

```python
def run_web_server(config_manager: ConfigManager):
    """Run the web server in a separate thread."""
    web_config = config_manager.get("web_server", {})
    # Don't pass bot_instance - let WebServer get current instance dynamically from main.bot_instance
    web_server = WebServer(config_manager)  # ← No bot_instance parameter
    web_server.run(
        host=web_config.get("host", "0.0.0.0"),
        port=web_config.get("port", 5000),
        debug=False
    )
```

Now the WebServer's `bot_instance` property will:
1. Check `_bot_instance_ref` → None (nothing was passed)
2. Import `main` module and return `main.bot_instance` → Returns current connected bot!

## How It Works Now

### Startup Flow
1. Line 104: Creates placeholder bot (for initial setup)
2. Line 107-112: Web server starts WITHOUT bot reference
3. Line 50: Creates NEW bot instance
4. Line 52: Bot connects to Discord
5. `on_ready` event fires, bot receives guilds
6. Web server's property dynamically gets `main.bot_instance` → sees connected bot!

### When Tab is Loaded
1. User clicks "Servers/Channels" or "Manual Send" tab
2. JavaScript calls `/api/servers` endpoint
3. WebServer's `bot_instance` property is accessed
4. Property returns current `main.bot_instance` (the connected one!)
5. Endpoint returns `bot_instance.guilds` → actual server list
6. UI displays servers correctly

### During Reconnection
1. Connection lost, bot closes
2. Line 50: Creates fresh bot instance
3. `main.bot_instance` updated to new instance
4. Bot reconnects
5. Web server automatically sees new bot instance
6. UI shows updated server list

## Files Changed

- **main.py**: Removed `bot_instance` parameter from `WebServer()` initialization (1 line changed)
- **test_bot_connection_detection.py**: Added comprehensive tests for dynamic bot instance detection (new file)
- **BOT_CONNECTION_DETECTION_FIX.md**: This documentation (new file)

## Testing

### New Tests (test_bot_connection_detection.py)
All tests verify that WebServer dynamically detects bot connection status:

✅ **test_webserver_gets_current_bot_instance**
- Creates WebServer without passing bot instance
- Updates `main.bot_instance` from placeholder to connected bot
- Verifies WebServer sees the new bot with servers

✅ **test_webserver_detects_bot_reconnection**
- Simulates bot reconnection with different guilds
- Verifies WebServer dynamically sees the new guilds

✅ **test_webserver_handles_no_bot**
- Tests graceful handling when `main.bot_instance` is None
- Returns empty server list without crashing

### Existing Tests
All existing tests continue to pass:
- ✅ test_server_channels_fix.py
- ✅ test_manual_send_dropdowns.py

## Verification

To verify the fix works:

1. Run the bot: `python main.py`
2. Wait for "Bot is ready!" message in console
3. Open http://localhost:5000
4. Click **"Servers/Channels"** tab
   - ✅ Should show all Discord servers and channels (not "Bot Not Connected")
5. Click **"Manual Send"** tab
   - ✅ Should show server dropdown with all servers
   - ✅ Selecting a server should populate channels dropdown

## Before & After

### Before Fix ❌
- Console: "Bot is ready! Logged in as..."
- UI Servers/Channels tab: "⚠️ Bot Not Connected to Discord"
- UI Manual Send tab: "No servers found. Make sure the bot is running..."
- Reality: Bot IS connected, but UI can't see it

### After Fix ✅
- Console: "Bot is ready! Logged in as..."
- UI Servers/Channels tab: Shows list of servers with channel counts
- UI Manual Send tab: Shows server dropdown with all servers
- Reality: UI correctly detects bot connection status

## Impact

This fix ensures that:
1. ✅ The web interface accurately reflects bot connection status
2. ✅ Manual Send feature works when bot is connected
3. ✅ Servers/Channels configuration works when bot is connected
4. ✅ Bot reconnection is automatically detected by the web interface
5. ✅ No need to refresh the page - dynamic detection works on tab switch
