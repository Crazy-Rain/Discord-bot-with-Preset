# Quick Fix: Invalid Token Error

## Problem
Getting "Invalid Token" error even though your API key works in SillyTavern or other tools?

## Solution ✅
This has been fixed! The bot now automatically handles:

### What Gets Cleaned:
- ✅ **Whitespace**: Removes spaces, tabs, newlines
- ✅ **Bearer Prefix**: Removes "Bearer " prefix (case-insensitive)

### Examples:
All of these now work correctly:

```
❌ Before: "Bearer sk-abc123"     → ❌ Invalid Token error
✅ After:  "Bearer sk-abc123"     → ✅ Cleaned to "sk-abc123" - works!

❌ Before: "  sk-abc123  "        → ❌ Might fail
✅ After:  "  sk-abc123  "        → ✅ Cleaned to "sk-abc123" - works!

❌ Before: "bearer sk-abc123"     → ❌ Invalid Token error
✅ After:  "bearer sk-abc123"     → ✅ Cleaned to "sk-abc123" - works!
```

## How to Update Your API Key

### Via Web Interface (Recommended):
1. Go to http://localhost:5000
2. Click **Configuration** tab
3. Enter your API key (with or without "Bearer")
4. Click **Save Configuration**
5. ✅ It will be automatically cleaned!

### Via config.json:
```json
{
  "openai_config": {
    "api_key": "your-key-here",
    "base_url": "https://your-proxy.com/v1",
    "model": "gpt-3.5-turbo"
  }
}
```

Don't include "Bearer " - but if you do, it will be removed automatically.

## Why This Happens

The OpenAI SDK automatically adds "Bearer " to create the authorization header:
```
Your key:      sk-abc123
SDK creates:   Authorization: Bearer sk-abc123  ✅ Correct
```

If you include "Bearer " in your key:
```
Your key:      Bearer sk-abc123
Old behavior:  Authorization: Bearer Bearer sk-abc123  ❌ Invalid!
New behavior:  Cleaned to sk-abc123, then creates: Authorization: Bearer sk-abc123  ✅ Works!
```

## Still Having Issues?

If you're still getting "Invalid Token" errors:

1. **Verify your key is correct**:
   - Copy it exactly from your proxy/service provider
   - Check for typos

2. **Verify your base URL**:
   - Should end with `/v1`
   - Example: `https://anas-proxy.xyz/v1`

3. **Verify your proxy is accessible**:
   - Test with curl or in SillyTavern first
   - Make sure the service is online

4. **Check your model name**:
   - Use the "Fetch Models" button to see available models
   - Make sure you're using a valid model name

## Technical Details

For developers and advanced users, see:
- [API_KEY_BEARER_FIX.md](API_KEY_BEARER_FIX.md) - Full technical documentation
- [INVALID_TOKEN_ERROR_FIX.md](INVALID_TOKEN_ERROR_FIX.md) - Previous error handling fix

## Tests

Verify the fix is working:
```bash
python3 test_api_key_bearer_fix.py
python3 test_web_api_key_cleaning.py
python3 test_bearer_prefix_integration.py
```

All should show: ✅ All Tests Passed!
