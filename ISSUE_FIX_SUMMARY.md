# Issue Fix Summary

## Issues Addressed

### 1. OpenAI API 500 Error with Confusing Error Message

**Problem**: Users were getting confusing error messages when the OpenAI-compatible API returned a 500 server error:
```
Error: Error calling OpenAI-compatible API: Error code: 500 - {'error': 'Internal server error', 'proxy_note': "Error while executing proxy response middleware: googleAIBlockingResponseHandler (Cannot read properties of undefined (reading '0'))"}
```

**Root Cause**: The error message from the API proxy was being passed through without additional context, making it difficult for users to understand what went wrong and how to fix it.

**Fix Applied**:
1. Added defensive validation of the API response structure before accessing `response.choices[0]`
2. Added specific error handling for 500 server errors with helpful troubleshooting steps
3. Improved error messages to guide users on what to check

**Code Changes** (`openai_client.py`):
- Added checks for `response.choices` existence and content
- Added dedicated 500 error handler with actionable troubleshooting steps:
  - Check API endpoint is correct and accessible
  - Verify model name is valid for the API provider
  - Ensure proxy (if used) is configured correctly

### 2. Lorebook Constant Entries Not Being Pulled

**Problem**: Constant (always active) lorebook entries were being skipped even when the lorebook was linked to the current character or was a global lorebook.

**Root Cause**: The lorebook filtering logic had a bug when `character_name` was an empty string `""`:

```python
# OLD (buggy) code:
if not linked_chars or (character_name and character_name in linked_chars):
```

When `character_name` is an empty string:
- `character_name and character_name in linked_chars` evaluates to `False` (because empty string is falsy in Python)
- Even if the lorebook was linked to an empty string character, it would be skipped

**Fix Applied**:
Changed the condition to explicitly check for `None` instead of relying on truthiness:

```python
# NEW (fixed) code:
if not linked_chars or (character_name is not None and character_name in linked_chars):
```

This properly handles all three cases:
1. `character_name` is `None` → only include global lorebooks
2. `character_name` is empty string `""` → check if empty string is in `linked_chars`
3. `character_name` is non-empty string → check if it's in `linked_chars`

**Code Changes** (`lorebook_manager.py`):
- Updated the lorebook filtering condition in `get_system_prompt_section()` method
- Added clarifying comment about the three possible states of `character_name`

## Test Coverage

Created comprehensive test suite (`test_issue_fixes.py`) that verifies:

1. **Empty String Character with Global Lorebook**: Global lorebooks are included for empty string characters
2. **Empty String Character with Linked Lorebook**: Lorebooks linked to empty string characters work correctly
3. **Constant Entries Always Included**: Constant entries are properly filtered and included based on character matching
4. **Backward Compatibility**: Old `always_active` field still works (converted to `activation_type`)

All tests pass ✅

## Impact

These fixes ensure that:
1. Users get clear, actionable error messages when API calls fail
2. Lorebook constant entries are always included when they should be, regardless of character name format
3. The bot correctly handles edge cases like empty string character names
4. Backward compatibility is maintained with older lorebook formats

## Files Modified

1. `lorebook_manager.py` - Fixed character name filtering logic
2. `openai_client.py` - Enhanced error handling and validation
3. `test_issue_fixes.py` - Added comprehensive test coverage (new file)
