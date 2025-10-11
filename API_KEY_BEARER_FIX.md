# API Key Bearer Prefix Fix

## Issue

Users were experiencing "Invalid Token" errors even when their API key/token worked correctly in other tools like SillyTavern. Investigation revealed the root cause: **users were accidentally including the "Bearer " prefix in their API key**.

## Root Cause Analysis

### How OpenAI SDK Authentication Works

The OpenAI Python SDK (and most OpenAI-compatible APIs) use the following authentication format:

```
Authorization: Bearer <api_key>
```

The SDK automatically constructs this header by:
1. Taking the `api_key` parameter passed to the client
2. Prepending `Bearer ` to create the Authorization header

### The Problem

When users copy API keys from documentation, other tools, or curl commands, they sometimes include the "Bearer " prefix. For example:

- ❌ User enters: `Bearer sk-abc123xyz`
- ❌ SDK creates header: `Authorization: Bearer Bearer sk-abc123xyz`
- ❌ Server rejects: "Invalid Token" error

This is especially common when:
1. Copying from curl examples that show the full header
2. Copying from SillyTavern's UI where it might be displayed
3. Following documentation that shows the complete Authorization header format

### Why It Works in SillyTavern

SillyTavern likely handles this scenario by:
1. Detecting and removing the "Bearer " prefix before creating headers
2. Or constructing the header differently
3. This makes it more forgiving of user input errors

## The Fix

We've implemented comprehensive API key cleaning that:

1. **Strips whitespace**: Removes leading/trailing spaces, tabs, newlines
2. **Removes Bearer prefix**: Detects and removes "Bearer " prefix (case-insensitive)

### Implementation

#### In `openai_client.py`:

Added a static method `_clean_api_key()` that:
```python
@staticmethod
def _clean_api_key(api_key: str) -> str:
    """Clean API key by removing whitespace and Bearer prefix."""
    if not api_key:
        return api_key
    
    # Strip whitespace
    cleaned = api_key.strip()
    
    # Remove "Bearer " prefix if present (case-insensitive)
    if cleaned.lower().startswith("bearer "):
        cleaned = cleaned[7:].strip()
    
    return cleaned
```

This method is called in:
- `__init__()`: When creating a new client
- `update_config()`: When updating client configuration

#### In `web_server.py`:

Updated the `/api/config` endpoint to clean API keys:
```python
if 'api_key' in data['openai_config'] and data['openai_config']['api_key'] != '***HIDDEN***':
    # Clean API key: strip whitespace and remove Bearer prefix if present
    api_key = data['openai_config']['api_key'].strip()
    # Remove "Bearer " prefix (case-insensitive)
    if api_key.lower().startswith("bearer "):
        api_key = api_key[7:].strip()
    data['openai_config']['api_key'] = api_key
```

## Test Coverage

Created comprehensive tests to verify the fix:

### Test Cases Covered:
- ✅ Normal API key: `sk-abc123`
- ✅ API key with spaces: `  sk-abc123  `
- ✅ API key with newline: `sk-abc123\n`
- ✅ API key with Bearer prefix: `Bearer sk-abc123`
- ✅ API key with Bearer and spaces: `  Bearer sk-abc123  `
- ✅ Lowercase bearer: `bearer sk-abc123`
- ✅ Uppercase bearer: `BEARER sk-abc123`
- ✅ Bearer with extra spaces: `Bearer  sk-abc123`

All test cases now correctly clean to: `sk-abc123`

## User Impact

### Before Fix:
- ❌ `Bearer sk-abc123` → "Invalid Token" error
- ❌ Confusing because it works in SillyTavern
- ❌ No clear indication of the problem

### After Fix:
- ✅ `Bearer sk-abc123` → Automatically cleaned to `sk-abc123`
- ✅ Works consistently with SillyTavern
- ✅ More forgiving of common user input errors
- ✅ API key works regardless of format

## Migration Guide

### For Users:

No action required! The fix automatically handles:
- Existing API keys continue to work
- New API keys work with or without "Bearer " prefix
- Both web interface and config file entries are cleaned

### For Developers:

If you're using the OpenAIClient directly:
```python
from openai_client import OpenAIClient

# All these now work correctly:
client1 = OpenAIClient(api_key="sk-abc123", base_url="...")
client2 = OpenAIClient(api_key="Bearer sk-abc123", base_url="...")  # Cleaned automatically
client3 = OpenAIClient(api_key="  Bearer sk-abc123  ", base_url="...")  # Also cleaned
```

## Related Issues

This fix addresses the core authentication issue mentioned in:
- "Invalid Token" errors with proxies
- SillyTavern compatibility
- API key format confusion

## Backwards Compatibility

✅ **Fully backwards compatible**
- Existing API keys without "Bearer " prefix work unchanged
- No breaking changes to API or configuration format
- All existing functionality preserved

## Testing Commands

Run the test suite to verify the fix:

```bash
# Test OpenAIClient API key cleaning
python3 test_api_key_bearer_fix.py

# Test web server API key cleaning
python3 test_web_api_key_cleaning.py
```

Both tests should pass with all checks green (✓).
