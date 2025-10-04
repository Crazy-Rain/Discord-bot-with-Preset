# Server/Channel Display Fix

## Issue
The Servers/Channels tab in the web interface was showing "No servers connected. Make sure the bot is running and connected to Discord." even though:
- The console showed "Bot is ready! Logged in as..." 
- The console showed "Loading X channel configuration(s)..."
- The bot was clearly connected to Discord

## Root Cause
There was a **duplicate bot instance creation** bug in `main.py`:

1. **Line 89**: `bot_instance = DiscordBot(config_manager)` - First bot instance created
2. **Line 97**: Web server thread starts with reference to first bot instance
3. **Line 29 (OLD CODE)**: `bot_instance = DiscordBot(config_manager)` - **SECOND bot instance created!**
4. The second bot instance connected to Discord and received guilds
5. The web server had a reference to the **first bot instance** which never connected

This meant:
- The connected bot had guilds ✓
- The web server's bot reference had NO guilds ✗
- The `/api/servers` endpoint returned an empty list

## Fix
Removed the duplicate bot creation on line 29 of `run_discord_bot()`:

```python
# BEFORE (BUGGY)
async def run_discord_bot(config_manager: ConfigManager):
    global bot_instance, shutdown_flag
    bot_instance = DiscordBot(config_manager)  # ← Creates duplicate bot!
    token = config_manager.get("discord_token")
    ...

# AFTER (FIXED)
async def run_discord_bot(config_manager: ConfigManager):
    global bot_instance, shutdown_flag
    # Use existing bot_instance created in main()
    token = config_manager.get("discord_token")
    ...
```

## How It Works Now
1. `main()` creates a single `bot_instance` (line 89)
2. Web server thread starts and gets reference to this bot instance
3. `run_discord_bot()` uses the **same** bot instance (not creating a new one)
4. When bot connects to Discord, guilds are populated
5. Web server sees the guilds immediately through its bot reference
6. `/api/servers` returns the correct server list

## Testing
The fix was verified with:
1. Unit tests showing web server sees the same bot instance
2. Integration tests simulating the complete flow
3. Existing test suite continues to pass

## Verification
To verify the fix works:
1. Set up `config.json` with a valid Discord token
2. Run `python main.py`
3. Wait for "Bot is ready! Logged in as..." message
4. Open http://localhost:5000
5. Click "Servers/Channels" tab
6. ✅ You should see all Discord servers and channels listed

## Files Changed
- `main.py`: Removed duplicate bot instance creation in `run_discord_bot()`
