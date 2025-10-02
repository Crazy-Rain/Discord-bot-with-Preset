# Swipe Button Feature - Implementation Guide

## Overview

The Discord bot now includes interactive buttons on every AI response, allowing users to navigate between alternative responses, generate new alternatives, and delete messages without needing to use text commands.

## Features

### Interactive Buttons

Every response from the bot now includes four buttons:

1. **◀ Swipe Left** - Navigate to the previous alternative response
2. **🔄 Swipe** - Generate a new alternative response
3. **Swipe Right ▶** - Navigate to the next alternative response
4. **🗑️ Delete** - Delete the message

### Button Behavior

- **Swipe Left/Right**: Cycles through existing alternatives with wrap-around (when at the first alternative, left goes to the last, and vice versa)
- **Swipe**: Generates a new alternative response using the AI, adds it to the list of alternatives
- **Delete**: Removes the message from the channel

## Usage

### Basic Workflow

1. Send a message using `!chat`:
   ```
   !chat Tell me a story about space
   ```

2. The bot responds with an AI-generated message and buttons attached

3. Click any button to:
   - **Navigate**: Use left/right buttons to see different versions of the response
   - **Generate**: Click the Swipe button to create a new alternative
   - **Clean up**: Use the Delete button to remove unwanted messages

### Example

```
User: !chat Tell me a joke

Bot: [Response with joke]
     [◀ Swipe Left] [🔄 Swipe] [Swipe Right ▶] [🗑️ Delete]

User: *clicks Swipe button*

Bot: [Different joke]
     [◀ Swipe Left] [🔄 Swipe] [Swipe Right ▶] [🗑️ Delete]
     *Alternative 2/2* (shown as ephemeral message)

User: *clicks Swipe Left*

Bot: [First joke again]
     [◀ Swipe Left] [🔄 Swipe] [Swipe Right ▶] [🗑️ Delete]
     *Alternative 1/2*
```

## Command Compatibility

The new button functionality is fully compatible with existing text commands:

- `!chat <message>` - Still works, now with buttons
- `!swipe` - Still works, now with buttons
- `!swipe_left` - Still works, now with buttons
- `!swipe_right` - Still works, now with buttons

Both methods (buttons and commands) can be used interchangeably.

## Technical Implementation

### Components

1. **SwipeButtonView**: A `discord.ui.View` subclass containing four button callbacks
2. **Updated send_long_message**: Now accepts an optional `view` parameter
3. **Updated send_as_character**: Now accepts an optional `view` parameter for webhook messages
4. **Button Handlers**: Async callbacks that handle user interactions

### Key Features

- **Persistent Buttons**: Buttons remain functional across bot restarts (timeout=None)
- **Per-Channel State**: Each channel maintains its own alternative history
- **Webhook Support**: Buttons work with webhook messages (character avatars)
- **Long Message Support**: Buttons are attached to the last chunk when messages are split

### Code Structure

```python
class SwipeButtonView(discord.ui.View):
    """View with swipe navigation buttons."""
    
    @discord.ui.button(label="◀ Swipe Left", style=discord.ButtonStyle.secondary)
    async def swipe_left_button(self, interaction, button):
        # Navigate to previous alternative
        
    @discord.ui.button(label="🔄 Swipe", style=discord.ButtonStyle.primary)
    async def swipe_button(self, interaction, button):
        # Generate new alternative
        
    @discord.ui.button(label="Swipe Right ▶", style=discord.ButtonStyle.secondary)
    async def swipe_right_button(self, interaction, button):
        # Navigate to next alternative
        
    @discord.ui.button(label="🗑️ Delete", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction, button):
        # Delete the message
```

## Benefits

1. **Better UX**: No need to type commands for navigation
2. **Faster**: One click instead of typing a command
3. **Cleaner**: Delete button removes unwanted messages quickly
4. **Discovery**: New users can see available actions without reading docs
5. **Mobile-Friendly**: Easier to use on mobile devices

## Backward Compatibility

✅ **Fully backward compatible**
- All existing commands still work
- No breaking changes to the API
- Works with existing character cards
- Works with existing presets
- Optional feature (buttons just enhance the UX)

## Testing

Run the test suite to verify functionality:

```bash
python test_swipe_buttons.py
```

All tests should pass:
- ✓ Imports
- ✓ View structure
- ✓ Button callbacks
- ✓ Function signatures
- ✓ send_as_character signature
- ✓ Button labels and styles

## Limitations

1. **Discord Limits**: Discord has a limit of 25 components per message (we use 4)
2. **Webhook Messages**: Delete button may have limited permissions on webhook messages
3. **Message History**: Buttons don't persist in message history after bot restart (functionality remains)

## Future Enhancements

Potential future additions:
- Button to show current alternative count
- Button to jump to first/last alternative
- Settings button for per-message configuration
- Reaction-based alternative to buttons for backwards compatibility

## Troubleshooting

### Buttons Not Appearing

- Ensure discord.py >= 2.3.2 is installed
- Check that the bot has permission to send messages with components
- Verify the view is being passed to send functions

### Buttons Not Working

- Check bot logs for errors
- Ensure the bot has necessary permissions
- Verify the channel_id is correctly tracked

### Delete Button Not Working

- Some webhook messages may have restricted delete permissions
- Check bot permissions in the channel
- Fallback: Use Discord's native delete functionality

## Related Files

- `discord_bot.py` - Main implementation
- `test_swipe_buttons.py` - Test suite
- `RECENT_ENHANCEMENTS.md` - Previous swipe command documentation

## Support

For issues or questions:
1. Check the test results
2. Review bot logs for errors
3. Verify Discord.py version
4. Check bot permissions in Discord
