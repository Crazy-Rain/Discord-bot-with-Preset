# Creation Points (CP) Tracking Feature

## Overview

The CP (Creation Points) Tracking system allows the bot to automatically track and manage Creation Points awarded during roleplay sessions. This feature is particularly useful for users who use a point-based achievement system in their Discord bot interactions.

## Features

### 1. Auto Context Limit Improvement
- **Changed slider step from 50 to 10** for more granular control
- Allows setting Auto Context Limit in increments of 10 instead of 50

### 2. CP Tracking Toggle
- **Enable/Disable CP Tracking**: Toggle in Bot Configuration tab
- When enabled, the AI receives instructions to note CP awards in responses
- System automatically tracks CP totals and response counts

### 3. Automatic CP Detection
- Parses AI responses for CP awards using pattern matching
- Recognizes formats like:
  - `+50 CP`
  - `+100 cp` (case insensitive)
  - `25 CP` (with or without +)
  - Multiple CP awards in single response

### 4. Response Counter
- Tracks number of responses since last 10-count milestone
- Increments on new responses (not on swipes)
- Displays as `[Count: X/10]` at end of each response

### 5. Automatic Bonus CP
- Configurable CP amount (default: 100) awarded when count reaches 10/10
- Count automatically resets to 1 after reaching 10
- Bonus amount can be customized in the configuration

### 6. Manual CP Total Management
- Edit current CP total directly in Bot Configuration
- Changes apply to the next response
- Useful for corrections or adjustments

### 7. Swipe Compatibility
- Swipes recalculate CP based on the alternative response
- Count doesn't increment when swiping (maintains current count)
- Each alternative's CP awards are properly tracked

## Configuration

### Web UI Settings

In the **Bot Configuration** tab, you'll find:

1. **Enable CP Tracking** (checkbox)
   - Toggles the entire CP tracking system
   - Shows/hides CP tracking settings

2. **CP Per 10 Responses** (number input)
   - Amount of CP to award automatically when count reaches 10/10
   - Default: 100
   - Can be any positive integer

3. **Current CP Total** (number input + Update button)
   - Displays current CP total across all channels
   - Can be manually edited
   - Click "Update CP Total" to save changes

### Config File Structure

```json
{
  "cp_tracking": {
    "enabled": true,
    "cp_per_count": 100,
    "cp_total": 0
  }
}
```

## Response Format

When CP tracking is enabled, responses are appended with:

```
[Your response content here]

[CP Total: 150]
[Count: 3/10]
```

### Example Response Flow

**Response 1:**
```
You completed the quest successfully! +25 CP

[CP Total: 25]
[Count: 1/10]
```

**Response 2-9:**
```
You explored the dungeon. +10 CP

[CP Total: 35]
[Count: 2/10]
```

**Response 10 (triggers bonus):**
```
You defeated the boss! +50 CP

[CP Total: 185]  # 35 + 50 + 100 (bonus)
[Count: 1/10]    # Reset to 1
```

## AI System Prompt

When CP tracking is enabled, the AI receives this additional instruction:

> IMPORTANT: At the end of your response, make a note of any Creation Points (CP) that would be awarded for achievements or actions carried out in your response. Use the format '+X CP' where X is the amount awarded.

## Implementation Details

### Per-Channel Tracking
- CP totals and counts are tracked separately for each Discord channel
- Allows multiple independent sessions in different channels

### Swipe Behavior
- When generating a new alternative (🔄 Swipe button):
  - Count doesn't increment
  - CP from the new response is added to the base total
  
- When navigating between alternatives (◀ ▶ buttons):
  - Count remains the same
  - CP total is recalculated based on the selected alternative

### Data Persistence
- CP settings are saved to `config.json`
- Manual CP total updates persist across bot restarts
- Per-channel totals are maintained in memory during bot runtime

## Use Cases

1. **Achievement System**: Award CP for completing quests, defeating enemies, or discovering secrets
2. **Progress Tracking**: Monitor character progression over multiple sessions
3. **Milestone Rewards**: Automatic bonus CP every 10 responses encourages engagement
4. **Manual Adjustments**: Correct mistakes or add special bonuses via the web UI

## API Endpoints

### Update CP Total
```
POST /api/cp_total
Content-Type: application/json

{
  "cp_total": 500
}
```

Updates the global CP total configuration and applies to all channels.

## Testing

The feature includes comprehensive test coverage for:
- CP extraction from various text patterns
- Count increments and resets
- Bonus CP application at count=10
- Swipe behavior (no count increment)
- Response formatting

Run tests with:
```bash
python test_cp_tracking.py
```

## Notes

- CP tracking is completely optional and can be disabled at any time
- When disabled, no CP information is appended to responses
- The AI won't receive CP-related instructions when disabled
- Works seamlessly with existing features like thinking filters, character cards, and lorebooks
