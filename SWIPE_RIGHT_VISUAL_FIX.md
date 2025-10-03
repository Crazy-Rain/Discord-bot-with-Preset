# Multi-Embed Message Fix - Visual Comparison

## The Problem

When using the `!swipe_right` command with multi-page responses (messages that span multiple Discord embeds), only the first page was being tracked and updated. This meant:

❌ **Before the fix:**
```
User uses !swipe_right command
│
├─ Response has 3 pages (3 separate embed messages)
│
└─ Button handlers can't find all messages
    └─ Only first page updates on next swipe
        └─ Pages 2 and 3 show old content
```

## The Code Bug

### Before (Broken):
```python
# In !swipe_right command (line ~1734)
webhook_sent = await self.send_as_character(
    ctx.channel, 
    response, 
    character_data,
    view=view
)
if not webhook_sent:  # ❌ WRONG! webhook_sent is a tuple (last_msg, msg_ids)
    # Fallback to normal message if webhook fails - use embeds
    await send_long_message(ctx, response, view=view)  # ❌ WRONG! Doesn't return IDs
# ❌ view.message_ids is NEVER updated!
```

**Problems:**
1. `send_as_character()` returns `(last_msg, msg_ids)` tuple, not a boolean
2. Checking `if not webhook_sent:` doesn't work - tuple `(None, [])` is truthy!
3. Fallback used deprecated `send_long_message()` which doesn't return message IDs
4. `view.message_ids` was never set, so button handlers couldn't find the messages

### After (Fixed):
```python
# In !swipe_right command (line ~1734)
last_msg, msg_ids = await self.send_as_character(  # ✅ Unpack tuple
    ctx.channel, 
    response, 
    character_data,
    view=view
)
if not last_msg:  # ✅ Check the message, not the tuple
    # Fallback to normal message if webhook fails - use embeds
    last_msg, msg_ids = await send_long_message_with_view(ctx.channel, response, view=view)  # ✅ Returns IDs
# Update view with message IDs for multi-page swipe support
if msg_ids:
    view.message_ids = msg_ids  # ✅ Always update!
```

**Fixes:**
1. ✅ Properly unpacks the tuple returned by `send_as_character()`
2. ✅ Checks `if not last_msg:` to test if webhook succeeded
3. ✅ Uses `send_long_message_with_view()` in fallback, which returns `(last_msg, msg_ids)`
4. ✅ Always updates `view.message_ids` so button handlers can find all pages

## The Result

✅ **After the fix:**
```
User uses !swipe_right command
│
├─ Response has 3 pages (3 separate embed messages)
│
├─ All 3 message IDs are tracked in view.message_ids = [101, 102, 103]
│
└─ Button handlers can find all messages
    └─ Next swipe deletes ALL 3 old messages
        └─ Sends ALL pages of new response
            └─ All pages show current content ✅
```

## How Multi-Page Swipe Works

### Message Creation:
```python
# When response is > 4096 chars, it's split into multiple embeds
chunks = smart_split_text(response, max_length=4096)

# Each chunk becomes a separate message
for i, chunk in enumerate(chunks):
    embed = discord.Embed(description=chunk)
    msg = await channel.send(embed=embed)
    message_ids.append(msg.id)  # Track ALL message IDs
```

### Button Handler Using Tracked IDs:
```python
# In SwipeButtonView.swipe_left_button (or right, or generate)
last_msg, new_ids = await self.bot.replace_as_character(
    channel, 
    self.message_ids,  # Use ALL tracked message IDs
    filtered_response, 
    character_data, 
    view=self
)
self.message_ids = new_ids  # Update for next swipe
```

### Replace Function:
```python
# replace_as_character deletes old, sends new
async def replace_as_character(..., old_message_ids, ...):
    # Delete ALL old pages
    for msg_id in old_message_ids:
        await webhook.delete_message(msg_id)
    
    # Send ALL new pages
    return await send_as_character(...)  # Returns (last_msg, new_ids)
```

## Files Changed

- **discord_bot.py** - 6 lines changed in `!swipe_right` command
  - Changed variable assignment from `webhook_sent =` to `last_msg, msg_ids =`
  - Changed condition from `if not webhook_sent:` to `if not last_msg:`
  - Changed fallback from `send_long_message()` to `send_long_message_with_view()`
  - Added `view.message_ids = msg_ids` update
  - Removed duplicate `view = SwipeButtonView(...)` in else branch

- **SWIPE_RIGHT_FIX.md** - New documentation file

## Testing

All tests pass:
- ✅ All `send_as_character()` calls properly unpack tuples
- ✅ No deprecated `send_long_message()` usage
- ✅ `view.message_ids` is updated in all swipe commands
- ✅ All three swipe commands handle message IDs consistently
- ✅ Existing embed splitting tests still pass
- ✅ No syntax errors

## Impact

This fix ensures that multi-page (multi-embed) responses work correctly:
1. All pages are tracked when first sent
2. All pages are deleted when swiping to a different response
3. All pages of the new response are sent
4. No orphaned messages left behind
5. Button handlers work correctly for multi-page responses
6. Webhook and non-webhook modes work identically
