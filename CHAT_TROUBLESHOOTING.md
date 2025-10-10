# Chat Command Troubleshooting Guide

This guide helps diagnose and fix issues with the `!chat` command not responding.

## Quick Diagnosis

If you're not getting responses from `!chat CharacterName: message`, check the console logs for these debug messages:

### Expected Log Flow

```
[CHAT] Received message in channel 123456: CharacterName: Hello...
[CHAT] Parsed - Character: CharacterName, Message: Hello...
[CHAT] Built 5 messages for API call
[CHAT] Calling OpenAI API...
[CHAT] Received response: This is the AI response...
[CHAT] Sending via webhook as character: CharacterName
[CHAT] Message sent successfully, IDs: [789012]
```

### Common Issues

#### 1. No Response at All

**Symptom**: Command is received but nothing happens

**Check for**:
```
[CHAT] Error occurred: ...
```

**Common Causes**:
- API key not configured
- API endpoint unreachable
- Invalid model name
- Network issues

**Solution**: Check config.json and verify API settings

#### 2. Webhook Send Failure

**Symptom**: You see this in logs:
```
[WEBHOOK] Error sending webhook message: ...
[CHAT] Webhook send failed for channel 123456, falling back to regular message
```

**Common Causes**:
- Bot lacks "Manage Webhooks" permission in the channel
- Invalid character avatar URL (not https://)
- Discord webhook service temporarily down

**Solution**: 
1. The bot automatically falls back to regular messages
2. Grant "Manage Webhooks" permission to the bot
3. Check character avatar URLs are valid HTTPS URLs
4. Response will still be sent, just without character avatar

#### 3. Character Name Not Parsed

**Symptom**: 
```
[CHAT] Parsed - Character: None, Message: CharacterName: Hello...
```

**Cause**: Incorrect message format

**Solution**: Ensure format is exactly: `CharacterName: message`
- There must be a colon (`:`) after the character name
- Space after colon is optional
- Character name cannot contain colons

## Debug Mode

To see full debug output, the bot now logs:

1. **Message Reception**: `[CHAT] Received message in channel...`
2. **Parsing**: `[CHAT] Parsed - Character:...`
3. **Message Building**: `[CHAT] Built X messages for API`
4. **API Call**: `[CHAT] Calling OpenAI API...`
5. **API Response**: `[CHAT] Received response:...`
6. **Send Method**: `[CHAT] Sending via webhook/regular embed...`
7. **Send Result**: `[CHAT] Message sent successfully, IDs:...`
8. **Errors**: Full stack traces for debugging

## Webhook Fallback

The bot now automatically falls back to regular messages if webhook sending fails:

```python
# Webhook send attempted
last_msg, msg_ids = await self.send_as_character(...)

# If failed, automatically retry with regular message
if not last_msg or not msg_ids:
    print(f"[CHAT] Webhook send failed, falling back to regular message")
    last_msg, msg_ids = await send_long_message_with_view(...)
```

This ensures you **always** get a response, even if the character display fails.

## Testing Without Discord

Run the test suite to verify core functionality:

```bash
python3 test_chat_fix.py
```

This tests:
- Character name parsing
- Message building
- Fallback logic
- API integration (mocked)

## Common Error Messages

### "API key is not configured"

**Fix**: Update config.json with valid API key:
```json
{
  "openai_config": {
    "api_key": "your-actual-api-key",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4"
  }
}
```

### "API authentication failed"

**Fix**: Verify API key is correct and has necessary permissions

### "Error: 'NoneType' object..."

**Fix**: This usually means a webhook operation failed. Check:
1. Bot has "Manage Webhooks" permission
2. Character avatar URL is valid HTTPS
3. Console logs for `[WEBHOOK]` errors

## Permissions Required

The bot needs these Discord permissions:
- **Send Messages** - To respond in channels
- **Embed Links** - To send formatted responses
- **Manage Webhooks** - To send as character (optional, falls back if missing)
- **Read Message History** - To load context from previous messages

## Still Having Issues?

1. Check console output for `[CHAT]` and `[WEBHOOK]` logs
2. Run `python3 test_chat_fix.py` to verify core functionality
3. Verify API configuration in config.json
4. Check Discord bot permissions
5. Try without a character loaded first: `!chat Hello` (no character name)
6. If webhook fails, the bot falls back automatically - you should still get a response

## Report Issues

If the problem persists, provide:
1. Full console output including `[CHAT]` logs
2. The exact command you used
3. Whether a character is loaded for the channel
4. Error messages from the console
