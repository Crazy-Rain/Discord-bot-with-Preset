# Invalid Token Error Fix

## Latest Update: Bearer Prefix Fix (NEW)

**Issue**: Users were still getting "Invalid Token" errors even when their token worked in SillyTavern.

**Root Cause Found**: Users were accidentally including "Bearer " prefix in their API key (e.g., `Bearer sk-abc123`). The OpenAI SDK automatically adds `Bearer ` to create the authorization header, so this resulted in `Authorization: Bearer Bearer sk-abc123`, which is invalid.

**Fix Applied**: API keys are now automatically cleaned to remove:
- Whitespace (spaces, tabs, newlines)
- "Bearer " prefix (case-insensitive)

**See**: [API_KEY_BEARER_FIX.md](API_KEY_BEARER_FIX.md) for complete details.

---

## Previous Fix: Error Detection Enhancement

## Issue Reported

User (@Crazy-Rain) reported getting an "Invalid Token" error when using a proxy (https://anas-proxy.xyz/v1) that works fine in SillyTavern.

## Root Cause

The error detection in `openai_client.py` was too narrow and only checked for specific patterns:
- "401"
- "invalid_api_key"
- "Incorrect API key"

However, different proxies and API providers may return various error messages for authentication failures:
- "Invalid Token" (what the user encountered)
- "Invalid API key"
- "Unauthorized"
- "Authentication failed"
- etc.

## Fix Applied

Enhanced the authentication error detection to catch a broader range of error patterns:

```python
# OLD (narrow detection):
if "401" in error_msg or "invalid_api_key" in error_msg or "Incorrect API key" in error_msg:

# NEW (broad detection):
if any(pattern in error_msg.lower() for pattern in [
    "401", "invalid_api_key", "incorrect api key", "invalid api key", "invalid token", 
    "invalid_request_error", "authentication", "unauthorized"
]):
```

## Enhanced Error Message

The new error message now provides specific guidance for proxy users:

```
API authentication failed. Please verify your API key/token is correct.
You can update it via the web interface at http://localhost:5000.
Note: If using a proxy (like anas-proxy.xyz), ensure:
1. Your API key/token is valid for that specific proxy
2. The proxy URL is correct (should end with /v1)
3. The proxy service is currently accessible
Original error: [error details]
```

## Why This Happens

### Different Error Formats

Different API providers and proxies return authentication errors in various formats:

- **OpenAI**: "Incorrect API key provided"
- **Proxy services**: "Invalid Token", "Invalid API key"
- **Generic**: "401 Unauthorized", "Authentication failed"

### Proxy-Specific Tokens

When using a proxy service (like anas-proxy.xyz):
1. The proxy requires its own API key/token
2. This token is different from OpenAI's API keys
3. The proxy validates the token before forwarding requests
4. If the token is invalid for that specific proxy, you get an error

### Working in SillyTavern vs Discord Bot

If a proxy works in SillyTavern but not in the Discord bot, possible causes:

1. **Different tokens**: You might be using different API keys/tokens in each application
2. **Token format**: The bot or SillyTavern might be formatting the token differently
   - ⚠️ **Common issue**: Including "Bearer " prefix in the API key (now fixed - see [API_KEY_BEARER_FIX.md](API_KEY_BEARER_FIX.md))
3. **Configuration**: The base URL might be slightly different (trailing slashes, /v1 suffix, etc.)
4. **Token expiration**: The token might have expired between testing

## Solutions for Users

### Verify Proxy Configuration

1. **Check the API key/token**:
   - Open web interface: http://localhost:5000
   - Go to Configuration tab
   - Verify the API key matches what works in SillyTavern
   - Make sure there are no extra spaces or characters

2. **Check the base URL**:
   - Should be: `https://anas-proxy.xyz/v1` (with /v1 suffix)
   - Check for typos or extra characters
   - Ensure it matches SillyTavern's configuration

3. **Test the proxy directly**:
   - Use curl or Postman to test the proxy with your token
   - Verify the proxy service is accessible and accepting requests

### Common Issues

**Issue**: "Invalid Token" error
- **Cause**: Token is not valid for the proxy, OR token includes "Bearer " prefix
- **Solution**: 
  1. Copy the exact token from SillyTavern configuration
  2. Remove any "Bearer " prefix if present (now handled automatically)
  3. Ensure there are no extra spaces

**Issue**: Works in SillyTavern but not in bot
- **Cause**: Different configuration, token, or token format
- **Solution**: 
  1. Compare both configurations side-by-side
  2. Check if you accidentally included "Bearer " prefix (now handled automatically)
  3. Verify base URL and model match exactly

**Issue**: Intermittent errors
- **Cause**: Proxy service might be rate-limited or having issues
- **Solution**: Wait and retry, or contact proxy provider

### Example Configuration

For anas-proxy.xyz:
```json
{
  "openai_config": {
    "api_key": "your-proxy-token-here",
    "base_url": "https://anas-proxy.xyz/v1",
    "model": "gpt-3.5-turbo"
  }
}
```

## Pattern Detection

The enhanced error detection now catches these patterns (case-insensitive):

- ✅ "Invalid Token"
- ✅ "Invalid API key"
- ✅ "Incorrect API key"
- ✅ "401 Unauthorized"
- ✅ "Authentication failed"
- ✅ "invalid_api_key"
- ✅ "invalid_request_error"
- ✅ "Unauthorized access"

## Commit

Fixed in commit: **[commit-hash]**

## Related Issues

- Original 500 error fix
- Google AI proxy error fix
- Context length error fix
