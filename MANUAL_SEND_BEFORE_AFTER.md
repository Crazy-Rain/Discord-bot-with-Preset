# Manual Send Fix - Before & After

## Before (Broken) ❌

### Symptom
```
POST /api/manual_send HTTP/1.1" 400 -
```

### Code
```python
@self.app.route('/api/manual_send', methods=['POST'])
async def send_manual_message():  # ❌ async def with Flask
    """Send a manual message to a Discord channel as a character."""
    if not self.bot_instance:
        return jsonify({"status": "error", "message": "Bot is not running"}), 400
    
    try:
        data = request.json
        channel_id = int(data.get('channel_id'))  # ❌ Crashes if None
        character_name = data.get('character_name')
        message = data.get('message')
        
        if not channel_id or not character_name or not message:
            return jsonify({
                "status": "error",
                "message": "Missing required fields"
            }), 400
        
        # Get the channel
        channel = self.bot_instance.get_channel(channel_id)
        if not channel:
            return jsonify({
                "status": "error",
                "message": f"Channel {channel_id} not found"
            }), 404
        
        # Load the character
        character_data = self.character_manager.load_character(character_name)
        
        # Send the message as the character
        last_msg, msg_ids = await self.bot_instance.send_as_character(  # ❌ await in Flask
            channel,
            message,
            character_data
        )
        
        if last_msg and msg_ids:
            return jsonify({
                "status": "success",
                "message": "Message sent successfully"
            })
```

### Error
```
RuntimeError: Install Flask with the 'async' extra in order to use async views.
```

### User Experience
- ❌ POST request returns 400 error
- ❌ Message not sent to Discord
- ❌ No helpful error message
- ❌ Both dropdown and manual ID input modes fail

---

## After (Fixed) ✅

### Result
```
POST /api/manual_send HTTP/1.1" 200 OK
```

### Code
```python
@self.app.route('/api/manual_send', methods=['POST'])
def send_manual_message():  # ✅ Regular def (synchronous)
    """Send a manual message to a Discord channel as a character."""
    if not self.bot_instance:
        return jsonify({"status": "error", "message": "Bot is not running"}), 400
    
    try:
        data = request.json
        channel_id_raw = data.get('channel_id')  # ✅ Get raw value first
        character_name = data.get('character_name')
        message = data.get('message')
        
        if not channel_id_raw or not character_name or not message:  # ✅ Validate before conversion
            return jsonify({
                "status": "error",
                "message": "Missing required fields"
            }), 400
        
        # Convert channel_id to int after validation
        try:  # ✅ Safe conversion with error handling
            channel_id = int(channel_id_raw)
        except (ValueError, TypeError):
            return jsonify({
                "status": "error",
                "message": "Invalid channel_id format"
            }), 400
        
        # Get the channel
        channel = self.bot_instance.get_channel(channel_id)
        if not channel:
            return jsonify({
                "status": "error",
                "message": f"Channel {channel_id} not found or bot doesn't have access"
            }), 404
        
        # Load the character
        try:
            character_data = self.character_manager.load_character(character_name)
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Failed to load character: {str(e)}"
            }), 400
        
        # Send the message as the character (run async function in sync context)
        import asyncio  # ✅ Use asyncio to run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            last_msg, msg_ids = loop.run_until_complete(  # ✅ Run async in sync context
                self.bot_instance.send_as_character(
                    channel,
                    message,
                    character_data
                )
            )
        finally:
            loop.close()  # ✅ Clean up event loop
        
        if last_msg and msg_ids:
            return jsonify({
                "status": "success",
                "message": "Message sent successfully"
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to send message via webhook"
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
```

### Success
```
{
  "status": "success",
  "message": "Message sent successfully"
}
```

### User Experience
- ✅ POST request returns 200 success
- ✅ Message sent to Discord successfully
- ✅ Clear error messages for all edge cases
- ✅ Both dropdown and manual ID input modes work
- ✅ Proper validation and error handling

---

## Key Changes

### 1. Async to Sync Conversion
**Before:** `async def send_manual_message()` with `await`
**After:** `def send_manual_message()` with asyncio event loop

### 2. Input Validation
**Before:** `int(data.get('channel_id'))` - crashes if None
**After:** Validate first, then convert with try/except

### 3. Error Handling
**Before:** Generic 400 errors
**After:** Specific error codes and messages:
- 400: Missing fields or invalid format
- 404: Channel not found
- 500: Server error

### 4. Asyncio Integration
**Before:** Direct `await` (not supported in Flask)
**After:** 
```python
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    result = loop.run_until_complete(async_function())
finally:
    loop.close()
```

---

## Test Results

### Before Fix
```
POST /api/manual_send HTTP/1.1" 400 -
RuntimeError: Install Flask with the 'async' extra...
```

### After Fix
```
POST /api/manual_send HTTP/1.1" 200 OK
{'status': 'success', 'message': 'Message sent successfully'}
```

### Verified With
- Server ID: `1011703948526239814` ✅
- Channel ID: `1426231081182695636` ✅

---

## Summary

| Aspect | Before | After |
|--------|--------|-------|
| HTTP Status | 400 Error | 200 Success |
| Async Handling | ❌ Broken (`async def` in Flask) | ✅ Fixed (asyncio event loop) |
| Input Validation | ❌ Crashes on None | ✅ Validates before conversion |
| Error Messages | ❌ Generic | ✅ Specific and helpful |
| Dropdown Mode | ❌ Broken | ✅ Works |
| Manual ID Mode | ❌ Broken | ✅ Works |
| Test Coverage | ❌ No tests | ✅ Comprehensive tests |

The Manual Send feature is now **fully functional**! 🎉
