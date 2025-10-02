# Swipe Button Feature - Implementation Guide

## Overview

The Discord bot now includes interactive buttons on every AI response, allowing users to navigate between alternative responses, generate new alternatives, and delete messages without needing to use text commands.

**✨ NEW: Swipe buttons now EDIT the existing message instead of posting new ones!** This keeps the channel clean and makes navigation more intuitive.

## Features

### Interactive Buttons

Every response from the bot now includes five buttons:

1. **◀ Swipe Left** - Navigate to the previous alternative response (edits the message)
2. **🔄 Swipe** - Generate a new alternative response (edits the message)
3. **Swipe Right ▶** - Navigate to the next alternative response (edits the message)
4. **🗑️ Delete** - Delete the message
5. **✅ Done** - Finish swiping and remove the buttons (keeps the current response)

### Button Behavior

- **Swipe Left/Right**: Cycles through existing alternatives with wrap-around (when at the first alternative, left goes to the last, and vice versa). **Edits the message to show the selected alternative.**
- **Swipe**: Generates a new alternative response using the AI, adds it to the list of alternatives. **Edits the message to show the new alternative.**
- **Delete**: Removes the message from the channel
- **Done**: Removes the buttons from the message, keeping the currently displayed response. This cleans up the UI when you're satisfied with a response.

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
     [◀ Swipe Left] [🔄 Swipe] [Swipe Right ▶] [🗑️ Delete] [✅ Done]

User: *clicks Swipe button*

Bot: [Same message EDITED to show different joke]
     [◀ Swipe Left] [🔄 Swipe] [Swipe Right ▶] [🗑️ Delete] [✅ Done]
     *Alternative 2/2* (shown as ephemeral message)

User: *clicks Swipe Left*

Bot: [Same message EDITED to show first joke again]
     [◀ Swipe Left] [🔄 Swipe] [Swipe Right ▶] [🗑️ Delete] [✅ Done]
     *Alternative 1/2*

User: *clicks Done button*

Bot: [Same message with buttons removed]
     [First joke remains visible]
```

**Note:** Unlike the old behavior, the message is edited in-place rather than posting new messages. This keeps the channel clean and makes it easy to see which message you're swiping through.

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
        # Navigate to previous alternative - EDITS the message
        
    @discord.ui.button(label="🔄 Swipe", style=discord.ButtonStyle.primary)
    async def swipe_button(self, interaction, button):
        # Generate new alternative - EDITS the message
        
    @discord.ui.button(label="Swipe Right ▶", style=discord.ButtonStyle.secondary)
    async def swipe_right_button(self, interaction, button):
        # Navigate to next alternative - EDITS the message
        
    @discord.ui.button(label="🗑️ Delete", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction, button):
        # Delete the message
    
    @discord.ui.button(label="✅ Done", style=discord.ButtonStyle.success)
    async def done_button(self, interaction, button):
        # Remove buttons - EDITS the message to remove view
```

### Helper Functions

```python
async def edit_long_message(message, content: str, view: discord.ui.View = None):
    """Edit a message with long content using embeds."""
    # Edits the message in-place

async def edit_as_character(message, content: str, character_data: Dict, view: discord.ui.View = None):
    """Edit a webhook message as a character."""
    # Edits webhook messages using webhook.edit_message()
```

## Benefits

1. **Better UX**: No need to type commands for navigation
2. **Faster**: One click instead of typing a command
3. **Cleaner Channel**: Messages are edited in-place instead of posting new ones - no chat spam!
4. **Easier to Follow**: See alternatives change in real-time on the same message
5. **Discovery**: New users can see available actions without reading docs
6. **Mobile-Friendly**: Easier to use on mobile devices
7. **Done Button**: Clean up the UI by removing buttons when you're satisfied

## Backward Compatibility

✅ **Fully backward compatible**
- All existing commands still work
- No breaking changes to the API
- Works with existing character cards
- Works with existing presets
- Optional feature (buttons just enhance the UX)

## Testing

Run the test suites to verify functionality:

```bash
python test_swipe_buttons.py
python test_swipe_edit_functionality.py
```

All tests should pass:
- ✓ Imports
- ✓ View structure
- ✓ Button callbacks (including Done button)
- ✓ Function signatures
- ✓ send_as_character signature
- ✓ Button labels and styles
- ✓ Edit functionality (new)
- ✓ Message editing instead of sending (new)
- ✓ Done button removes view (new)

## Limitations

1. **Discord Limits**: Discord has a limit of 25 components per message (we use 5)
2. **Webhook Messages**: Delete button may have limited permissions on webhook messages
3. **Message History**: Buttons don't persist in message history after bot restart (functionality remains)
4. **Long Messages**: When editing very long messages (>4096 chars), only the first page is shown in the edited version with a note

## Future Enhancements

Potential future additions:
- Button to show current alternative count in the message itself
- Button to jump to first/last alternative
- Settings button for per-message configuration
- Reaction-based alternative to buttons for backwards compatibility
- Support for full multi-page editing of very long messages

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
- `test_swipe_buttons.py` - Test suite for button structure
- `test_swipe_edit_functionality.py` - Test suite for edit functionality (new)
- `RECENT_ENHANCEMENTS.md` - Previous swipe command documentation

## Changelog

### Version 2.0 - Message Editing Update
- **Breaking Change**: Swipe buttons now EDIT messages instead of posting new ones
- Added **Done** button (✅) to remove buttons while keeping the message
- Added `edit_long_message()` helper function
- Added `edit_as_character()` method for webhook message editing
- Updated `send_as_character()` to return message objects
- Updated `send_long_message_with_view()` to return message objects
- Improved channel cleanliness - no more duplicate messages when swiping
- All swipe operations now happen on the same message

### Version 1.0 - Initial Release
- Interactive buttons on every AI response
- Four buttons: Swipe Left, Swipe, Swipe Right, Delete
- Full backward compatibility with text commands

## Support

For issues or questions:
1. Check the test results
2. Review bot logs for errors
3. Verify Discord.py version
4. Check bot permissions in Discord
