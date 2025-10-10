# Google AI Proxy Error Fix

## Issue Reported

User (@Crazy-Rain) reported that sending messages with specific formatting causes errors:

**Example that triggers the error:**
```
!chat OOC: Pokes you

Pokes you Twice
```

The error message was:
```
Error code: 500 - {'error': 'Internal server error', 'proxy_note': "Error while executing proxy response middleware: googleAIBlockingResponseHandler (Cannot read properties of undefined (reading '0'))"}
```

## Root Cause

The error is caused by the **Google AI proxy middleware** (`googleAIBlockingResponseHandler`) failing to properly handle certain message patterns. Specifically:

1. **Content Filtering**: Messages with certain content or patterns may trigger Google AI's safety filters, causing the API to return a blocked/filtered response
2. **Response Parsing Issues**: When the response is blocked or has an unexpected format, the proxy tries to access `response.candidates[0]` but `response.candidates` is undefined, causing a JavaScript error
3. **Message Formatting**: Messages with multiple newlines, special formatting, or certain character combinations can trigger parsing issues in the proxy

## The Problem

The original error message:
- Showed a cryptic JavaScript error from the proxy
- Didn't explain why the error occurred
- Provided no guidance on how to fix it
- Made it seem like a bot bug rather than a proxy/filtering issue

## Fix Applied

Enhanced error detection in `openai_client.py` to specifically recognize Google AI proxy errors:

```python
# Detect Google AI proxy errors
elif "googleAIBlockingResponseHandler" in error_msg or "Cannot read properties of undefined" in error_msg:
    raise Exception(
        f"Google AI proxy error - likely content filtering or response parsing issue. "
        f"This often happens when:\n"
        f"1. Your message contains content that triggers safety filters\n"
        f"2. The message format (e.g., with newlines or special characters) causes parsing issues\n"
        f"3. The proxy cannot parse the API response correctly\n"
        f"Try:\n"
        f"- Rewording your message\n"
        f"- Removing extra line breaks or special formatting\n"
        f"- Using a different API endpoint/proxy if available\n"
        f"Original error: {error_msg}"
    )
```

## User Solutions

When encountering Google AI proxy errors:

### Option 1: Reword the Message
- Simplify the message structure
- Remove special formatting or characters
- Try a different phrasing

### Option 2: Remove Extra Formatting
- Avoid multiple consecutive newlines (empty lines)
- Simplify special character usage
- Keep messages in a single line or with minimal line breaks

### Option 3: Use Alternative API/Proxy
- If using a Google AI proxy, consider switching to a direct OpenAI API endpoint
- Use a different proxy service that doesn't have the same parsing issues
- Configure your API settings in the web interface (http://localhost:5000)

## Technical Details

### Why This Happens

Google AI (Gemini) has built-in safety filters that can block certain content. When content is blocked:
1. The API returns a response without the usual `candidates` array
2. The proxy middleware tries to access `response.candidates[0]`
3. Since `candidates` is undefined, JavaScript throws: "Cannot read properties of undefined (reading '0')"
4. The proxy wraps this in a 500 error

### Common Triggers

Messages that may trigger this error:
- Multiple consecutive newlines (empty lines)
- Certain character combinations
- Content that resembles harmful/inappropriate content (even if innocent)
- Roleplay scenarios that trigger safety filters (like "OOC: ..." patterns)
- Special formatting characters in specific positions

### Why It's Not a Bot Bug

This is **not a bug in the Discord bot**. The bot correctly:
- Parses the message
- Formats it for the API
- Sends it to the configured endpoint

The error occurs in the **Google AI proxy middleware** when it processes the response from the Google AI API.

## Prevention

To minimize these errors:

1. **Keep messages simple** - Avoid complex formatting
2. **Test your proxy** - Verify it works with various message formats
3. **Use direct endpoints** - When possible, connect directly to the API provider
4. **Monitor for patterns** - Note which message types trigger errors
5. **Have a backup** - Configure alternative API endpoints

## Example Error Flow

1. User sends: `!chat OOC: Pokes you\n\nPokes you Twice`
2. Bot parses and formats correctly
3. Bot sends to Google AI proxy
4. Google AI filters/blocks the response due to content/format
5. Proxy tries to access `response.candidates[0]`
6. Error: `Cannot read properties of undefined (reading '0')`
7. Proxy returns 500 error with this message
8. Bot now shows helpful Google AI proxy error message

## Commit

Fixed in commit: **[commit-hash]**
