# Manual Send 400 Error - Improved Error Handling

## Problem Statement
Users were experiencing `POST /api/manual_send HTTP/1.1" 400 -` errors when trying to use the Manual Send feature. The suggestion was to "remove the requirement to check if the bot is online" and ensure it uses the same "Tunnel" (webhook system) that the Response system uses.

## Root Cause Analysis

The issue had multiple potential causes:
1. **Data validation order**: Bot availability was checked BEFORE request data validation, leading to misleading error messages
2. **Limited exception handling**: The bot_instance property only caught ImportError and AttributeError
3. **Unclear error messages**: Errors didn't provide enough guidance for users to resolve issues

## Solution Implemented

### 1. Reordered Validation Logic
**Before:**
```python
@self.app.route('/api/manual_send', methods=['POST'])
def send_manual_message():
    if not self.bot_instance:
        return jsonify({"status": "error", "message": "Bot is not running"}), 400
    
    try:
        data = request.json
        # ... validate data
```

**After:**
```python
@self.app.route('/api/manual_send', methods=['POST'])
def send_manual_message():
    try:
        data = request.json
        # Validate required fields first (before checking bot)
        if not channel_id_raw or not character_name or not message:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
        # Convert channel_id to int after validation
        try:
            channel_id = int(channel_id_raw)
        except (ValueError, TypeError):
            return jsonify({"status": "error", "message": "Invalid channel_id format"}), 400
        
        # Now check if bot instance is available (after data validation)
        if not self.bot_instance:
            return jsonify({"status": "error", "message": "Bot is not running"}), 400
```

**Benefits:**
- Users get accurate error messages for data issues
- Bot check happens only after confirming request is valid
- Reduces confusion when data is malformed

### 2. Improved Bot Instance Property
**Before:**
```python
@property
def bot_instance(self):
    if self._bot_instance_ref is not None:
        return self._bot_instance_ref
    
    try:
        import main
        return main.bot_instance
    except (ImportError, AttributeError):
        return None
```

**After:**
```python
@property
def bot_instance(self):
    if self._bot_instance_ref is not None:
        return self._bot_instance_ref
    
    try:
        import main
        bot = getattr(main, 'bot_instance', None)
        return bot
    except Exception as e:
        # Catch all exceptions, not just ImportError/AttributeError
        print(f"[WebServer] Error accessing bot instance: {type(e).__name__}: {e}")
        return None
```

**Benefits:**
- Catches all exceptions, not just specific ones
- Uses `getattr` for safer attribute access
- Logs errors to help diagnose issues
- More robust against unexpected errors

### 3. Added Diagnostic Logging
```python
# Log when bot instance is not available
if not self.bot_instance:
    print(f"[MANUAL_SEND] Bot instance not available for channel {channel_id}")
    return jsonify(...)

# Log when channel is not found
if not channel:
    print(f"[MANUAL_SEND] Channel {channel_id} not found")
    if self.bot_instance:
        guilds_count = len(self.bot_instance.guilds) if hasattr(self.bot_instance, 'guilds') else 'unknown'
        print(f"[MANUAL_SEND] Bot is in {guilds_count} guilds")
    return jsonify(...)
```

**Benefits:**
- Helps identify which error is occurring
- Shows bot state (guild count) for debugging
- Makes troubleshooting easier

### 4. Better Error Messages
**Before:**
```python
return jsonify({
    "status": "error",
    "message": f"Channel {channel_id} not found or bot doesn't have access"
}), 404
```

**After:**
```python
return jsonify({
    "status": "error",
    "message": f"Channel {channel_id} not found. Make sure: 1) The bot is connected and in the server, 2) The channel ID is correct, 3) The bot has permission to view the channel."
}), 404
```

**Benefits:**
- Provides actionable steps to resolve the issue
- Guides users on what to check
- More helpful for troubleshooting

## Why We Can't Remove the Bot Check

The suggestion was to "remove the requirement to check if the bot is online". However, this isn't possible because:

1. **Need channel object**: Manual send requires converting `channel_id` (string/int) to a `discord.TextChannel` object
2. **Bot API required**: Only `bot.get_channel(channel_id)` can perform this conversion
3. **Webhook dependencies**: The webhook system needs the channel object to create/fetch webhooks

**The "Tunnel" (webhook) requires bot access to:**
- Get the channel object
- Check existing webhooks via `channel.webhooks()`
- Create new webhooks via `channel.create_webhook()`
- Send messages via webhook with character avatars

**What we DID do:**
- Made the bot check more robust
- Moved it to the right place in the validation flow
- Added better error handling and messages
- Improved diagnostics

## Testing

### Test Cases Covered
1. ✅ Data validation before bot check
   - Missing fields return correct error
   - Invalid format returns correct error
   - Bot check happens last
2. ✅ Bot instance property robustness
   - Handles missing main module
   - Handles missing bot_instance attribute
   - Doesn't crash on unexpected errors
3. ✅ Improved error messages
   - 404 provides helpful guidance
   - Messages are specific and actionable

### Backwards Compatibility
All existing tests still pass:
- `test_manual_send_fix.py` ✅
- `test_manual_send_integration.py` ✅
- `test_manual_send_dropdowns.py` ✅
- `test_manual_send_channels.py` ✅

## Files Modified
- `web_server.py`: Improved manual send endpoint and bot_instance property

## Files Created
- `test_manual_send_improvements.py`: Tests for the improvements

## Impact
- **Better UX**: Users get clearer, more actionable error messages
- **Easier debugging**: Logs help identify root cause of issues
- **More robust**: Handles edge cases and unexpected errors gracefully
- **Maintainable**: Code is better organized and documented

## Next Steps for Users
If still experiencing 400 errors:
1. Check server logs for diagnostic messages (e.g., `[MANUAL_SEND] ...`)
2. Verify the Discord bot is running and connected
3. Confirm the bot is in the target server
4. Ensure the bot has permission to view the channel
5. Check that channel ID is correct (can be found in Discord with Developer Mode enabled)
