# Reconnection Fix - Always Create Fresh Bot Instances

## Problem

The Discord bot's reconnection logic had a subtle bug that caused it to fail on the second reconnection attempt:

1. **First disconnect** → Discord.py's internal reconnection handled it → worked fine
2. **Second disconnect** → Reconnection logic triggered BUT reused a bot instance that was already started → failed

The issue was in this condition:
```python
if retry_count > 0 or bot_instance.is_closed():
    bot_instance = DiscordBot(config_manager)
```

On the **first iteration** (retry_count=0), if the bot instance was not closed, it would reuse the existing instance. While this worked the first time, it could cause issues if:
- The bot instance was in an inconsistent state
- Discord.py's internal reconnection counter was cumulative
- The bot instance had been partially initialized

## Solution

**Always create a fresh bot instance on every connection attempt**, regardless of retry_count:

```python
# Always create a fresh bot instance for each connection attempt
if retry_count == 0:
    print("🔄 Creating bot instance for initial connection...")
else:
    print("🔄 Creating fresh bot instance for reconnection...")
bot_instance = DiscordBot(config_manager)
```

This ensures:
- ✅ Clean state for every connection attempt
- ✅ No cumulative issues from Discord.py's internal reconnection
- ✅ Consistent behavior on 1st, 2nd, 3rd... Nth reconnection

## Web Server Integration

The web server needs access to the current bot instance to:
- Update OpenAI configuration
- Access channel/server information
- Modify bot settings

### Previous Implementation (Broken)
```python
# main.py
bot_instance = DiscordBot(config_manager)  # Created once
web_server = WebServer(config_manager, bot_instance)  # Stored reference

# In run_discord_bot():
bot_instance = DiscordBot(config_manager)  # NEW instance created
# But web_server still has reference to OLD instance!
```

### New Implementation (Fixed)
```python
# web_server.py
@property
def bot_instance(self):
    """Get the current bot instance from main module."""
    import main
    return main.bot_instance
```

Now the web server **always gets the latest bot instance** from the global variable in main.py.

## Changes Made

### 1. `main.py` - Always create fresh bot instance
- Removed conditional `if retry_count > 0 or bot_instance.is_closed()`
- Now creates fresh instance on EVERY iteration
- Added clearer logging for initial vs reconnection attempts

### 2. `web_server.py` - Use global bot instance
- Changed `bot_instance` from instance variable to property
- Property dynamically fetches `main.bot_instance`
- Web server always has access to the latest bot instance

### 3. `test_reconnection_fix.py` - Validation test
- Verifies fresh instance is created on every iteration
- Confirms web server uses global bot instance property
- Ensures old buggy conditional is removed

## Testing

Run the validation test:
```bash
python3 test_reconnection_fix.py
```

Expected output:
```
✅ All tests passed!

Fix implemented:
  ✓ Always creates fresh bot instances on every connection attempt
  ✓ Web server accesses global bot_instance to get latest instance
  ✓ No more stale bot instance references

This ensures:
  • First disconnect -> fresh bot created -> reconnects successfully
  • Second disconnect -> fresh bot created -> reconnects successfully
  • N-th disconnect -> fresh bot created -> reconnects successfully
```

## Impact

### For Users
- **More Reliable Reconnection**: Bot will reconnect successfully every time, not just once
- **Better Stability**: No more "stuck" bot that won't reconnect after second disconnect
- **Peace of Mind**: The message "⚠️ Bot disconnected from Discord. Attempting to reconnect..." will actually result in successful reconnection

### For Developers
- **Cleaner Architecture**: Web server properly accesses current bot instance
- **No State Issues**: Fresh bot instance ensures no cumulative state problems
- **Easier Debugging**: Consistent behavior makes issues easier to track

## Files Modified

- `main.py` - Reconnection logic (9 lines changed)
- `web_server.py` - Bot instance access pattern (8 lines changed)
- `test_reconnection_fix.py` - Validation test (new file, 175 lines)
- `RECONNECTION_FIX.md` - Documentation (new file)

## Backward Compatibility

✅ **Fully backward compatible** - No breaking changes:
- Web server API unchanged (still accepts bot_instance parameter)
- All existing functionality preserved
- Bot behavior improved, not changed
- No configuration changes needed
