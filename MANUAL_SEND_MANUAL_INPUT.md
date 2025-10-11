# Manual Send - Manual ID Input Feature

## Overview
Added a new **Manual ID Input** mode to the Manual Send feature, allowing users to directly enter Server ID and Channel ID instead of relying on dropdown selection.

## Why This Feature?
The previous dropdown-only approach had limitations:
- Required the bot to be connected and have access to servers
- Didn't work if the bot couldn't see certain servers/channels
- No way to target specific channels when dropdowns failed to load

## New Feature: Manual ID Input Mode

### How It Works
Users can now choose between two input modes:

#### 1. **Dropdown Selection** (Default)
- Works as before
- Select server from dropdown → Select channel from dropdown
- Requires bot to be connected

#### 2. **Manual ID Input** (NEW)
- Enter Server ID directly
- Enter Channel ID directly
- Works even if dropdowns fail to load
- Useful for debugging and direct targeting

### UI Screenshots

**Dropdown Mode (Default):**
![Dropdown Mode](https://github.com/user-attachments/assets/caf26751-cf0e-46e0-a186-4cdad33c160b)

**Manual ID Input Mode (NEW):**
![Manual Input Mode](https://github.com/user-attachments/assets/aff6c370-d1bd-40ac-ae76-c5b209f26f1b)

## How to Use

### Method 1: Dropdown Selection (Existing)
1. Go to Manual Send tab
2. Keep "Dropdown Selection" radio button selected
3. Select server from dropdown
4. Select channel from dropdown
5. Select character and enter message
6. Click "Send Message"

### Method 2: Manual ID Input (NEW)
1. Go to Manual Send tab
2. Click "Manual ID Input" radio button
3. Enter Server ID (e.g., `123456789012345678`)
4. Enter Channel ID (e.g., `987654321098765432`)
5. Select character and enter message
6. Click "Send Message"

### How to Get Discord IDs

**Prerequisite:** Enable Developer Mode in Discord
- Desktop: User Settings → App Settings → Advanced → Enable Developer Mode
- Mobile: Similar path in Discord settings

**To Copy Server ID:**
1. Right-click on server icon
2. Click "Copy Server ID"
3. Paste into "Server ID" field

**To Copy Channel ID:**
1. Right-click on channel name
2. Click "Copy Channel ID"
3. Paste into "Channel ID" field

## Technical Implementation

### Files Modified
- `templates/index.html` - Added UI toggle and manual input fields

### Code Changes

#### UI Addition
```html
<!-- Mode Toggle -->
<div class="form-group">
    <label>Input Mode</label>
    <div>
        <label>
            <input type="radio" name="manual-send-mode" value="dropdown" checked onchange="toggleManualSendMode()"> 
            Dropdown Selection
        </label>
        <label>
            <input type="radio" name="manual-send-mode" value="manual" onchange="toggleManualSendMode()"> 
            Manual ID Input
        </label>
    </div>
</div>

<!-- Manual Input Mode -->
<div id="manual-send-manual-mode" style="display: none;">
    <div class="form-group">
        <label>Server ID</label>
        <input type="text" id="manual-send-server-id" placeholder="Enter Discord Server ID">
        <small>Right-click on server → Copy Server ID (Developer Mode must be enabled)</small>
    </div>
    
    <div class="form-group">
        <label>Channel ID</label>
        <input type="text" id="manual-send-channel-id" placeholder="Enter Discord Channel ID">
        <small>Right-click on channel → Copy Channel ID (Developer Mode must be enabled)</small>
    </div>
</div>
```

#### JavaScript Functions
```javascript
function toggleManualSendMode() {
    const mode = document.querySelector('input[name="manual-send-mode"]:checked').value;
    const dropdownMode = document.getElementById('manual-send-dropdown-mode');
    const manualMode = document.getElementById('manual-send-manual-mode');
    
    if (mode === 'dropdown') {
        dropdownMode.style.display = 'block';
        manualMode.style.display = 'none';
    } else {
        dropdownMode.style.display = 'none';
        manualMode.style.display = 'block';
    }
}

async function sendManualMessage() {
    const mode = document.querySelector('input[name="manual-send-mode"]:checked').value;
    let channelId;
    
    // Get channel ID based on mode
    if (mode === 'dropdown') {
        channelId = document.getElementById('manual-send-channel').value;
    } else {
        channelId = document.getElementById('manual-send-channel-id').value.trim();
    }
    
    // ... rest of the function
}
```

## Backend Compatibility
The backend `/api/manual_send` endpoint already accepts `channel_id` as a parameter, so no backend changes were needed. The endpoint works with both:
- Channel ID from dropdown selection
- Channel ID from manual input

## Testing
Feature tested and verified:
- ✅ Mode toggle works correctly
- ✅ Manual input fields show/hide based on selection
- ✅ Channel ID is correctly extracted from manual input
- ✅ Dropdown mode continues to work as before
- ✅ User guidance displayed properly
- ✅ Backend endpoint compatible with both modes

## Use Cases

### When to Use Dropdown Mode
- Normal usage when bot is connected
- When you want to browse available servers/channels
- Quick selection from visible options

### When to Use Manual Input Mode
- Dropdowns fail to load
- Bot can't see the server/channel but has permissions
- Debugging specific channel issues
- Direct targeting when you know the exact IDs
- Bot connection issues preventing dropdown population

## Backward Compatibility
- ✅ Existing dropdown functionality preserved
- ✅ Default mode is still dropdown selection
- ✅ No breaking changes to existing workflows
- ✅ Backend API unchanged

## Future Enhancements
Possible improvements:
- Save recently used Server/Channel ID combinations
- Validate ID format before submission
- Auto-populate Server ID when channel is selected in dropdown mode
- Bookmark frequently used channels

## Related Documentation
- [MANUAL_SEND_CHANNELS_FIX.md](MANUAL_SEND_CHANNELS_FIX.md) - Previous dropdown improvements
- Discord Developer Portal - For more info on Developer Mode
