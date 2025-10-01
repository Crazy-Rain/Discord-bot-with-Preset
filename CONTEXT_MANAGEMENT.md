# Context and History Management

## Overview

The Discord bot now intelligently manages conversation context by reading the actual channel message history. This means conversations persist across bot restarts and the bot can pick up context from previous interactions in the channel.

## How It Works

### Automatic Context Loading

When you use `!chat` for the first time in a channel (or after the bot restarts), the bot automatically:

1. **Fetches recent channel messages** - Reads up to 50 recent messages from the Discord channel
2. **Parses `!chat` commands** - Extracts user messages that were sent via `!chat`
3. **Identifies bot responses** - Recognizes its own previous responses
4. **Tracks character names** - Finds all character names used in the format `CharacterName: message`
5. **Builds conversation history** - Creates a chronological conversation context

### What Gets Loaded

The bot loads:
- ✅ User messages sent with `!chat` (including character names and content)
- ✅ Bot responses (excluding meta messages like "Alternative X/Y")
- ✅ Character names found in messages
- ❌ Regular Discord messages (not sent via `!chat`)
- ❌ Messages from other bots
- ❌ Meta/system messages

### Example Scenario

**Before bot restart:**
```
User: !chat Alice: "Hello everyone!" *waves*
Bot: Hello Alice! Nice to see you here.
User: !chat Bob: "How's the weather today?"
Bot: The weather is lovely, Bob!
```

**After bot restart:**
```
User: !chat Alice: "Bob, did you enjoy the weather?"
Bot: [Remembers Alice and Bob from channel history]
     Yes, Alice! I recall Bob was asking about the weather earlier. 
     It was lovely today!
```

## Commands

### `!chat <message>`

Standard chat command. Now automatically loads channel history on first use.

```
!chat Alice: "Hello!"
!chat What's the capital of France?
```

**Behind the scenes:**
- If conversation is empty, loads recent channel history
- Extracts character names from history
- Maintains context from previous messages

### `!reload_history [limit]`

Manually reload conversation context from channel history.

**Usage:**
```
!reload_history          # Load last 50 messages
!reload_history 100      # Load last 100 messages (max)
!reload_history 20       # Load last 20 messages
```

**When to use:**
- After clearing conversation history
- To refresh context with recent messages
- To adjust the amount of context used
- When you want to ensure all recent messages are included

**What it does:**
1. Clears current conversation history
2. Fetches specified number of recent messages
3. Rebuilds conversation from channel history
4. Reports number of messages and character names found
5. Clears any swipe alternatives (they're no longer valid)

**Example output:**
```
Reloaded conversation history!
- Loaded 12 messages
- Found 3 character(s): Alice, Bob, Charlie
```

### `!clear`

Clears all conversation history and character names from memory. The next `!chat` command will automatically reload from channel history.

```
!clear
```

**Effect:**
- Clears conversation memory
- Clears character names
- Clears swipe alternatives
- Next `!chat` will reload from channel history

### `!swipe`

Generate alternative responses. Now works with loaded channel history.

```
User: !chat Tell me a joke
Bot: Why did the chicken cross the road?
User: !swipe
Bot: [Generates alternative joke using full context]
```

**Context handling:**
- Uses full conversation history (including loaded messages)
- Excludes only the last bot response being regenerated
- Maintains all character context
- Includes lorebook entries based on conversation

## Technical Details

### Message Limit

By default, the bot loads the last **50 messages** from the channel. This can be adjusted:
- `!reload_history 20` - Load 20 messages
- `!reload_history 100` - Load 100 messages (maximum)

### Message Filtering

The `load_channel_history()` method intelligently filters messages:

1. **User messages** - Must start with `!chat`
   - Extracts content after `!chat `
   - Parses character names (format: `CharacterName: message`)
   - Adds to conversation as user role

2. **Bot responses** - From this bot only
   - Must not start with `!` (commands)
   - Skips meta messages like `*Alternative X/Y*`
   - Adds to conversation as assistant role

3. **Ignored messages**
   - Messages from other bots
   - Regular Discord messages without `!chat`
   - Bot commands (starting with `!`)
   - Meta/system messages

### Chronological Order

Messages are loaded in **chronological order** (oldest first), ensuring the conversation flows naturally:

```
Oldest:  User: "Hello"      (loaded first)
         Bot: "Hi there"
         User: "How are you?"
Newest:  Bot: "I'm great!"  (loaded last)
```

### Character Name Tracking

Character names are automatically tracked from channel history:

```
!chat Alice: "Hello!"     # Alice added to tracked names
!chat Bob: "Hi!"          # Bob added to tracked names
!chat Charlie: "Hey!"     # Charlie added to tracked names
```

The bot then includes all tracked character names in its system prompt to maintain context about who is participating in the conversation.

### Integration with Other Features

The history loading works seamlessly with:

- **Character tracking** - Character names from history are tracked
- **User character descriptions** - Applied to characters found in history
- **Lorebook** - Entries triggered by keywords in loaded messages
- **Swipe functionality** - Alternatives use full conversation context
- **Presets** - All loaded context respects current preset settings

## Use Cases

### 1. Bot Restart Recovery

**Before:**
```
[Bot restarts]
User: !chat Alice: "Where were we?"
Bot: "I'm not sure, I don't have any previous context."
```

**After:**
```
[Bot restarts]
User: !chat Alice: "Where were we?"
Bot: "We were discussing the weather and your trip to the mountains, Alice!"
```

### 2. Roleplay Continuity

**Scenario:** Long roleplay session with multiple characters

```
Day 1:
!chat Alice: "Let's explore the forest" *grabs backpack*
!chat Bob: "I'll bring the map!"

[Bot goes offline]

Day 2:
!chat Alice: "Bob, do you still have that map?"
Bot: [Remembers Bob had the map from previous day]
```

### 3. Group Conversations

**Multiple users with character names:**

```
UserA: !chat Alice: "Hello everyone!"
UserB: !chat Bob: "Hi Alice!"
UserC: !chat Charlie: "Good to see you both!"

[New user joins]
UserD: !chat Diana: "What did I miss?"
Bot: [Provides context mentioning Alice, Bob, and Charlie]
```

### 4. Context Refresh

**After clearing or to get fresh context:**

```
!clear
!reload_history 30
!chat Continue our previous discussion
Bot: [Uses last 30 messages as context]
```

## Best Practices

### 1. Regular History Reloads

If you notice the bot missing recent context:
```
!reload_history
```

### 2. Adjust History Limit

For longer conversations, increase the limit:
```
!reload_history 100
```

For focused conversations, use fewer messages:
```
!reload_history 20
```

### 3. Clear When Starting New Topic

Start fresh when changing topics:
```
!clear
!chat Let's talk about something completely different
```

### 4. Character Name Consistency

Use consistent character names across sessions:
```
!chat Alice: "Hello"     ✅ Good
!chat alice: "Hello"     ⚠️ Different character (case-sensitive)
!chat Alice : "Hello"    ✅ Same as first (spaces are trimmed)
```

## Limitations

### Message History Limit

- Default: 50 messages
- Maximum: 100 messages
- Older messages beyond the limit are not loaded

### Only `!chat` Messages

Regular Discord messages without `!chat` are not included in context:
```
User: Hello there         # Not loaded (no !chat)
User: !chat Hello there   # Loaded ✅
```

### Token Limits

Very long conversations may still hit the model's token limit. The bot:
1. Limits conversation history to last 20 exchanges
2. Trims older messages when limit is reached
3. Respects model's max_tokens setting

### Bot Identification

The bot only recognizes its own previous responses by checking:
- Message author is this bot
- Message doesn't start with `!`
- Message isn't a meta message

If another bot was used previously, those messages won't be loaded.

## Troubleshooting

### Bot Not Remembering Context

1. Check if messages were sent with `!chat`:
   ```
   !chat Your message here   ✅
   Your message here         ❌
   ```

2. Reload history manually:
   ```
   !reload_history
   ```

3. Increase history limit:
   ```
   !reload_history 100
   ```

### Character Names Not Tracked

1. Verify format (colon after name):
   ```
   !chat Alice: "Hello"     ✅
   !chat Alice "Hello"      ❌
   ```

2. Reload history to pick up names:
   ```
   !reload_history
   ```

### Too Much Context

Limit the history loaded:
```
!reload_history 20        # Load only last 20 messages
```

Or start fresh:
```
!clear
```

### Context From Wrong Channel

Each channel has separate context. If you're in the wrong channel, switch to the correct one. The bot maintains separate conversation histories per channel.

## Technical Implementation

### Code Structure

**`load_channel_history()` method:**
- Fetches messages using `channel.history(limit=N)`
- Reverses messages to chronological order
- Parses `!chat` commands
- Filters bot responses
- Returns conversation list and character names

**Integration points:**
- `!chat` command - Auto-loads on empty conversation
- `!swipe` command - Auto-loads if needed
- `!reload_history` command - Manual trigger

**Storage:**
- `self.conversations[channel_id]` - Conversation history per channel
- `self.character_names[channel_id]` - Character names per channel
- `self.response_alternatives[channel_id]` - Swipe alternatives per channel

### Example Method Call

```python
# Load history from channel
history_messages, character_names = await self.load_channel_history(
    ctx.channel,
    limit=50
)

# Merge into conversation
self.conversations[channel_id] = history_messages
self.character_names[channel_id] = character_names
```

## Future Enhancements

Potential improvements for future versions:

1. **Configurable default limit** - Set default history limit in config
2. **Automatic pruning** - Remove old messages based on token count
3. **Channel archiving** - Save/restore full channel conversations
4. **Cross-channel context** - Optional context sharing between channels
5. **Smart context selection** - ML-based relevant message selection
6. **Token-aware loading** - Stop loading when approaching token limit

## Summary

The channel history context loading feature:

✅ **Persists conversations** across bot restarts
✅ **Tracks character names** from previous messages  
✅ **Maintains context** automatically
✅ **Works with swipe** functionality
✅ **Integrates** with lorebook and character descriptions
✅ **Provides manual control** via `!reload_history`
✅ **Filters intelligently** to include only relevant messages

This feature ensures the bot has full conversational context from the channel, making interactions more natural and continuous.
