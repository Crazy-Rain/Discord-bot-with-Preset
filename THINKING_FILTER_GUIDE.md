# Thinking Filter Feature

This feature allows you to filter out "thinking" or "reasoning" content from AI responses before they are sent to Discord, while still preserving the full response in the conversation history and console logs.

## Overview

Some AI models include their reasoning process in responses using special tags (e.g., `<think>...</think>` or `<thinking>...</thinking>`). This feature allows you to:

1. **Configure custom tags** to identify thinking content
2. **Toggle filtering on/off** through the web UI
3. **Preview full responses** in the console before filtering
4. **Maintain full context** - the complete response (with thinking tags) is stored in conversation history

## Configuration

The thinking filter is configured in the **Configuration** tab of the web UI at `http://localhost:5000`.

### Settings

- **Enable Thinking Filter**: Checkbox to enable/disable the filter
- **Start Thinking Tag**: The opening tag that marks the beginning of thinking content (default: `<think>`)
- **End Thinking Tag**: The closing tag that marks the end of thinking content (default: `</think>`)
- **Console Preview**: A preview area showing how the filter works (full responses are logged to console when enabled)

### Example Configuration

```json
{
  "thinking_filter": {
    "enabled": true,
    "start_tag": "<think>",
    "end_tag": "</think>"
  }
}
```

## How It Works

### Before Filtering (Full Response)
```
Hello! <think>Let me analyze this question carefully. The user is asking about...</think> Here's my answer to your question.
```

### After Filtering (Sent to Discord)
```
Hello!  Here's my answer to your question.
```

### What Happens Behind the Scenes

1. **AI generates response** with thinking tags
2. **Full response logged to console** (when filtering is enabled)
3. **Filtered response sent to Discord** (thinking tags removed)
4. **Full response stored in history** (preserves complete context for future messages)

## Usage Examples

### Example 1: Default Tags
**Configuration:**
- Start Tag: `<think>`
- End Tag: `</think>`

**AI Response:**
```
<think>The user wants to know about Python. I should explain it clearly.</think>
Python is a high-level programming language known for its simplicity and readability.
```

**Discord Shows:**
```
Python is a high-level programming language known for its simplicity and readability.
```

### Example 2: Custom Tags
**Configuration:**
- Start Tag: `<reasoning>`
- End Tag: `</reasoning>`

**AI Response:**
```
Let me explain. <reasoning>This requires a detailed answer with examples.</reasoning>
The answer is: it depends on your use case.
```

**Discord Shows:**
```
Let me explain. 
The answer is: it depends on your use case.
```

### Example 3: Multiple Thinking Blocks
**AI Response:**
```
First point: <think>analyzing...</think> This is correct.
Second point: <think>checking logic...</think> This is also valid.
```

**Discord Shows:**
```
First point:  This is correct.
Second point:  This is also valid.
```

## Console Logging

When the thinking filter is enabled, the bot logs both versions of the response to the console:

```
============================================================
FULL RESPONSE (before filtering):
============================================================
Hello! <think>Let me think about this...</think> Here's my answer.
============================================================
FILTERED RESPONSE (sent to Discord):
============================================================
Hello!  Here's my answer.
============================================================
```

This helps you:
- Debug issues with filtering
- Verify the AI's reasoning process
- Understand how the AI arrived at its answers

## Benefits

1. **Cleaner Discord messages** - Users see only the final answer
2. **Preserved context** - Full responses are kept in conversation history
3. **Transparency** - Console logs show the AI's reasoning
4. **Flexibility** - Customizable tags work with different AI models
5. **Easy toggle** - Enable/disable without restarting the bot

## Compatibility

This feature works with:
- All AI models that use tagged thinking/reasoning
- All bot commands that generate responses (`!chat`, `!swipe`, swipe buttons)
- Webhook messages (character avatars)
- Multi-page messages (long responses)

## Configuration via Web UI

1. Navigate to `http://localhost:5000`
2. Click the **Configuration** tab
3. Scroll to the **Thinking Filter** section
4. Check **Enable Thinking Filter**
5. Set your **Start Thinking Tag** (e.g., `<think>`)
6. Set your **End Thinking Tag** (e.g., `</think>`)
7. Click **Save Configuration**

The changes take effect immediately - no bot restart required!

## Technical Details

### Filter Algorithm

The filter uses Python's `re.sub()` with the `DOTALL` flag to remove content:
- Matches: `start_tag + any content + end_tag`
- Non-greedy matching (stops at first closing tag)
- Case-sensitive matching
- Handles multiline thinking blocks
- Cleans up excessive whitespace after removal

### Where Filtering Applies

The filter is applied in these locations:
- `!chat` command (initial responses)
- `!swipe` command (alternative generation)
- Swipe button (🔄 Swipe)
- Swipe left/right navigation (◀ ▶)

### Storage

- **Conversation history**: Stores full responses (unfiltered)
- **Response alternatives**: Stores full responses (unfiltered)
- **Discord messages**: Shows filtered responses
- **Console logs**: Shows both full and filtered when enabled

## Troubleshooting

### Filter not working?
1. Check that **Enable Thinking Filter** is checked
2. Verify your tags match the AI's output exactly
3. Check the console logs to see the full response
4. Try saving and reloading the configuration

### AI not using thinking tags?
Some models need to be prompted to use thinking tags. Add this to your system prompt:
```
Use <think>...</think> tags to show your reasoning process before providing the final answer.
```

### Seeing extra spaces?
This is normal - the filter removes the entire tag block, which may leave spaces. The algorithm cleans up excessive whitespace but preserves paragraph structure.

## Related Features

- **Console Preview**: Shows what the full response looks like (in the web UI)
- **Swipe Functionality**: Works seamlessly with alternative responses
- **Character System**: Filtered responses work with character avatars
- **Multi-page Messages**: Long responses are filtered before splitting

## Future Enhancements

Potential future improvements:
- Multiple tag pairs (filter different types of content)
- Regex pattern support for more complex filtering
- UI preview showing before/after filtering in real-time
- Per-preset filter settings
- Statistics on how much content was filtered
