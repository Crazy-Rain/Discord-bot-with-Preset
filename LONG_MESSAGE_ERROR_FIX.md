# Long Message Error Fix - Summary

## Issue Reported

User (@Crazy-Rain) reported that sending fairly long messages with the `!chat` command causes an error. The suspicion was that there might be an accidental character/word limit.

## Root Cause

The error was **not** due to a character limit in the bot itself. Instead, it was caused by:

1. **Context Window Limit**: When a user sends a long message, the total context sent to the AI includes:
   - User's message
   - Conversation history (loaded via auto context limit, default 50 messages)
   - System prompts
   - Lorebook entries (if active)
   
2. **Poor Error Messages**: When this total exceeded the model's context window, the API returned errors that weren't clearly explaining the issue or how to fix it.

## Fix Applied

Enhanced error handling in `openai_client.py` to:

### 1. Detect Context Length Errors

Added pattern matching for context length errors:
- "context_length_exceeded"
- "maximum context length"
- "context window"
- "too many tokens"
- "token limit"
- "reduce the length"

### 2. Provide Actionable Solutions

When context length is exceeded, users now see:
```
Message too long - exceeded context window limit.
The combined length of your message, conversation history, and system prompts exceeded the model's token limit.
Please try:
1. Sending a shorter message
2. Using !clear to clear conversation history
3. Reducing the auto context limit with !setcontext (current messages loaded from history)
```

### 3. Updated 500 Error Messages

Updated the 500 error handler to include message length as a possible cause:
```
API server error (500). Possible causes:
1. Your API endpoint is not accessible or incorrect
2. The model name is invalid for your API provider
3. Your proxy (if using one) has a configuration issue
4. Your message may be too long (try a shorter message or use !clear to reset history)
```

## Solutions for Users

When encountering this error, users can:

1. **Send a shorter message** - Break long messages into smaller parts
2. **Clear conversation history** - Use `!clear` to reset the context
3. **Reduce auto context limit** - Use `!setcontext 50` (or lower) to load fewer messages from history
4. **Check model limits** - Ensure the model being used supports the context size needed

## No Artificial Limits

The bot itself has **NO artificial character or word limits**. The only limit is the model's context window, which varies by:
- Model type (e.g., GPT-3.5 has 4k-16k, GPT-4 has 8k-32k, Claude has 100k-200k)
- API provider configuration
- Proxy settings (if using one)

## Test Coverage

Added `test_context_error_handling.py` with tests for:
- Context length error pattern detection (9/9 tests passing)
- Error message categorization
- Pattern matching accuracy

## Commit

Fixed in commit: **e51170a**

## Related Features

- `!clear` - Clear conversation history
- `!setcontext <number>` - Set auto context limit (50-5000)
- `!reload_history [limit]` - Manually reload history
- See `AUTO_CONTEXT_LIMIT.md` for more details on context management
