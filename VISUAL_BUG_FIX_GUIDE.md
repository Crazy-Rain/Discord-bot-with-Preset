# Visual Bug Fix Explanation

## Issue 1: Config Update Bug

### ❌ BEFORE (Buggy Behavior)

```python
# User's config in config.json
{
    "openai_config": {
        "api_key": "sk-secret-key-12345",
        "base_url": "https://api.openai.com/v1", 
        "model": "gpt-3.5-turbo"
    }
}

# User loads a saved config with different proxy
# Web interface shows:
API Key: ***HIDDEN***  (not in update data)
Base URL: https://new-proxy.com/v1  ✏️ (in update data)
Model: gpt-4  ✏️ (in update data)

# Update sent to server:
{
    "openai_config": {
        "base_url": "https://new-proxy.com/v1",
        "model": "gpt-4"
        # api_key missing because it was hidden
    }
}

# OLD CODE (BUGGY):
config.update(update_data)  # Shallow update!

# Result in config.json:
{
    "openai_config": {
        "base_url": "https://new-proxy.com/v1",
        "model": "gpt-4"
        # ❌ API key is GONE!
    }
}

# Next API call fails: "No API key provided"
```

### ✅ AFTER (Fixed Behavior)

```python
# User's config in config.json
{
    "openai_config": {
        "api_key": "sk-secret-key-12345",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-3.5-turbo"
    }
}

# User loads a saved config with different proxy
# Web interface shows:
API Key: ***HIDDEN***  (not in update data)
Base URL: https://new-proxy.com/v1  ✏️ (in update data)
Model: gpt-4  ✏️ (in update data)

# Update sent to server:
{
    "openai_config": {
        "base_url": "https://new-proxy.com/v1",
        "model": "gpt-4"
        # api_key missing because it was hidden
    }
}

# NEW CODE (FIXED):
deep_update(config, update_data)  # Recursive merge!

# Result in config.json:
{
    "openai_config": {
        "api_key": "sk-secret-key-12345",  # ✅ PRESERVED!
        "base_url": "https://new-proxy.com/v1",  # ✅ Updated
        "model": "gpt-4"  # ✅ Updated
    }
}

# Next API call succeeds with new proxy and preserved key!
```

---

## The Fix: Deep Update Algorithm

```python
def deep_update(target: dict, updates: dict):
    """Recursively merge updates into target, preserving existing values."""
    for key, value in updates.items():
        if key in target and isinstance(target[key], dict) and isinstance(value, dict):
            # Both are dicts - recurse to merge
            deep_update(target[key], value)
        else:
            # Replace value
            target[key] = value
```

### Example Walkthrough

```python
# Initial state
target = {
    "openai_config": {
        "api_key": "sk-secret",
        "base_url": "url1",
        "model": "model1"
    }
}

# Update to apply
updates = {
    "openai_config": {
        "base_url": "url2",
        "model": "model2"
    }
}

# Deep update process:
# 1. Check "openai_config" key
#    - target["openai_config"] is dict ✓
#    - updates["openai_config"] is dict ✓
#    - RECURSE into nested dict

# 2. Inside nested dict:
#    - Process "base_url": replace url1 → url2
#    - Process "model": replace model1 → model2
#    - "api_key" not in updates, so it's preserved!

# Final result:
{
    "openai_config": {
        "api_key": "sk-secret",  # ✅ Preserved
        "base_url": "url2",       # ✅ Updated
        "model": "model2"         # ✅ Updated
    }
}
```

---

## Issue 2: Lorebook Debug Logging

### ❌ BEFORE (No Visibility)

```
User: "My lorebooks aren't working!"
Console: [no output]
Developer: "I can't see what's happening..."
```

### ✅ AFTER (Full Visibility)

```
User: "My lorebooks aren't working!"
Console:
[LOREBOOK] Getting lorebook entries for character: Luna
[LOREBOOK] Total lorebooks: 3
[LOREBOOK] Skipping disabled lorebook: Old Lore
[LOREBOOK] Skipping lorebook 'Alice Lore' (linked_chars: ['Alice'], current: Luna)
[LOREBOOK] Including lorebook 'Luna Lore' (linked_chars: ['Luna'])
[LOREBOOK]   Added constant entry: Luna's Past
[LOREBOOK]   Total entries from 'Luna Lore': 1
[LOREBOOK] Total entries to include: 1
```

**Diagnosis**: Immediately clear that:
- "Old Lore" is disabled (user needs to enable it)
- "Alice Lore" is skipped (wrong character)
- "Luna Lore" is working correctly

---

## Impact

### Before Fix
- ❌ Changing proxy deleted API key
- ❌ Bot couldn't make API calls after config update
- ❌ Users had to manually re-enter API keys
- ❌ No visibility into lorebook issues

### After Fix
- ✅ Config updates preserve all fields
- ✅ Bot works immediately after config change
- ✅ Users never lose their API keys
- ✅ Full visibility into lorebook behavior
- ✅ Easy troubleshooting with console logs

---

## Testing

Both issues verified with:
- ✅ 5 unit tests
- ✅ 3 real-world scenario tests
- ✅ All existing tests passing
- ✅ Comprehensive documentation
