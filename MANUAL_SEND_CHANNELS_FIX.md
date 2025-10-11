# Manual Send Channels Dropdown Fix

## Problem Statement
The Manual Send feature had an empty channel dropdown with no options. Users were unable to select channels to send messages to.

## Root Cause Analysis
Two main issues were identified:

1. **bot_instance Property Issue**: The `bot_instance` property in `WebServer` class was trying to import the `main` module to get the current bot instance. This caused:
   - Import errors in test environments (discord.py not installed)
   - Ignored the `_bot_instance_ref` passed during initialization
   - Failed when the bot hadn't started yet

2. **Missing Safety Checks**: The `/api/manual_send/channels` endpoint directly accessed `guild.text_channels` without checking if:
   - The attribute exists (`hasattr`)
   - The value is not `None`
   - This could cause errors or empty results

## Changes Made

### 1. Fixed `bot_instance` Property (web_server.py)
```python
@property
def bot_instance(self):
    """Get the current bot instance from main module or use the passed instance."""
    # First, try to use the instance passed during initialization (for tests)
    if self._bot_instance_ref is not None:
        return self._bot_instance_ref
    
    # Otherwise, try to get the current instance from main module (for production)
    try:
        import main
        return main.bot_instance
    except (ImportError, AttributeError):
        # If main module can't be imported or doesn't have bot_instance, return None
        return None
```

**Benefits:**
- Works in test environments without discord.py
- Uses passed instance if available
- Gracefully handles missing main module
- Falls back to None instead of crashing

### 2. Added Safety Checks to `/api/manual_send/channels` Endpoint (web_server.py)
```python
@self.app.route('/api/manual_send/channels', methods=['GET'])
def get_manual_send_channels():
    """Get list of channels the bot has access to for manual sending."""
    if not self.bot_instance:
        return jsonify({"channels": []})
    
    channels = []
    for guild in self.bot_instance.guilds:
        try:
            # Safely access text_channels - handle cases where it might be None or missing
            text_channels = guild.text_channels if hasattr(guild, 'text_channels') and guild.text_channels is not None else []
            for channel in text_channels:
                channels.append({
                    'id': str(channel.id),
                    'name': channel.name,
                    'server_name': guild.name,
                    'server_id': str(guild.id)
                })
        except Exception as e:
            # If there's any error getting guild info, skip it but log the issue
            print(f"Error getting channels for guild {guild.id}: {e}")
            continue
    
    return jsonify({"channels": channels})
```

**Benefits:**
- Handles missing or None `text_channels` attribute
- Skips problematic guilds instead of crashing
- Logs errors for debugging
- Returns empty list when bot is not available

### 3. Enhanced UI with Two-Dropdown Approach (templates/index.html)

Implemented the suggested improvement: **Server selection first, then Channel selection**

**Before:**
- Single channel dropdown showing all channels from all servers (confusing and hard to parse)
- Format: "Server Name / Channel Name (ID: 12345)"

**After:**
- **Step 1:** Select Server dropdown shows all available servers with channel count
- **Step 2:** Select Channel dropdown dynamically loads channels for selected server
- Format: "# channel-name" (cleaner, Discord-style)

**New UI Elements:**
```html
<div class="form-group">
    <label>Select Server</label>
    <select id="manual-send-server" onchange="loadManualSendServerChannels()">
        <option value="">-- Select a server --</option>
    </select>
    <button onclick="loadManualSendServers()">🔄 Refresh Servers</button>
</div>

<div class="form-group">
    <label>Select Channel</label>
    <select id="manual-send-channel">
        <option value="">-- Select a server first --</option>
    </select>
</div>
```

**New JavaScript Functions:**
- `loadManualSendServers()` - Loads server list from `/api/servers`
- `loadManualSendServerChannels()` - Loads channels for selected server from `/api/servers/{id}/channels`
- `loadManualSendChannels()` - Kept for backward compatibility (calls loadManualSendServers)

### 4. Comprehensive Tests (test_manual_send_channels.py)

Added complete test coverage:
- ✅ Normal guilds with text_channels
- ✅ Guilds with `text_channels = None`
- ✅ Guilds without `text_channels` attribute
- ✅ No bot instance (returns empty list)
- ✅ Multiple guilds with mixed conditions

## Benefits

1. **More Reliable**: Handles edge cases gracefully
2. **Better UX**: Two-step dropdown is easier to use, especially with many servers
3. **Testable**: Works in test environments without Discord.py
4. **Performance**: Channels loaded on-demand instead of all at once
5. **Maintainable**: Clear error handling and logging

## Screenshots

### Initial State
![Initial State](https://github.com/user-attachments/assets/04974279-1f17-4da4-b59b-9ace29a6bddb)
- Server dropdown with available servers
- Channel dropdown shows "-- Select a server first --"

### After Selecting Server
![With Channels](https://github.com/user-attachments/assets/52181b44-4895-405e-950c-6fd86683d66b)
- Server selected showing channel count
- Channel dropdown populated with channels from that server
- Channels prefixed with "#" for clarity

## Testing

Run tests:
```bash
python3 test_manual_send_channels.py
python3 test_server_channels_fix.py
```

All tests pass ✅

## Backward Compatibility

- Legacy `/api/manual_send/channels` endpoint still works (returns all channels)
- Old `loadManualSendChannels()` function redirects to new implementation
- Existing code continues to function without changes
