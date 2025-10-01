# Context Loading Feature - Problem Statement Response

## Original Problem Statement

> How does the bot handle Context, or Past responses? Does it only read it's own? It should probably be using any past !chat <charactername>: "words" *actions* actions from within the channel that it's responding to, right? Up until it runs out of it's Max Tokens/Context limit, anyway. Obviously, Swipe should ignore it's own past response, as it's regenerating that one. But it should also be making sure to keep track of it's own last responses in that channel too.

## Solution Implemented

### ✅ Channel History Loading

**What was the problem?**
- The bot only tracked messages it had seen since it started
- After restart, all conversation context was lost
- Past `!chat` messages in the channel weren't being used for context

**What's the solution?**
- Bot now reads the actual Discord channel message history
- Automatically loads recent `!chat` messages when conversation is empty
- Parses and includes past messages up to a configurable limit (default 50, max 100)

### ✅ Reading Past Messages

**Yes, the bot now reads past `!chat` messages from the channel:**

```python
# Automatically loads when conversation is empty
if not self.conversations[channel_id]:
    history_messages, character_names = await self.load_channel_history(
        ctx.channel, 
        limit=50
    )
```

**What gets loaded:**
- ✅ All `!chat CharacterName: "words" *actions*` messages
- ✅ Character names used in those messages  
- ✅ Bot's own responses to those messages
- ✅ Messages in chronological order (oldest first)
- ❌ Meta messages like "Alternative X/Y" (filtered out)
- ❌ Regular Discord messages without `!chat`

### ✅ Token/Context Limit Handling

**Respects limits:**
- Configurable message limit (default 50, max 100)
- Existing 20-message history limit still applies
- Max tokens from preset still enforced
- Old messages pruned when limit reached

```python
# Limit conversation history
if len(self.conversations[channel_id]) > 20:
    self.conversations[channel_id] = self.conversations[channel_id][-20:]
```

### ✅ Swipe Functionality

**Swipe correctly handles past responses:**

```python
# Add conversation history except the last assistant message
conv_without_last = self.conversations[channel_id][:-1]
messages.extend(conv_without_last)
```

**What happens:**
- ✅ Swipe excludes only its own last response (the one being regenerated)
- ✅ Keeps all other historical messages in context
- ✅ Uses full conversation history including loaded messages
- ✅ Maintains character names and context

### ✅ Tracking Own Responses

**Bot tracks its own responses:**
- Responses stored in conversation history
- Loaded from channel history on restart
- Identified by author ID matching bot's user ID
- Filtered to exclude commands and meta messages

## Usage Examples

### Automatic Context Loading

```
# Session 1
User: !chat Alice: "Hello everyone!"
Bot: Hello Alice! Welcome to the chat.
User: !chat Bob: "Hi Alice and Bot!"
Bot: Hello Bob! Nice to see you both here.

[Bot restarts]

# Session 2 - Context automatically loaded
User: !chat Alice: "Bob, remember what we discussed?"
Bot: Of course, Alice! Bob mentioned the weather earlier.
     [Bot loaded Bob and Alice from channel history]
```

### Manual History Reload

```
!reload_history          # Load last 50 messages
!reload_history 100      # Load last 100 messages  
!reload_history 20       # Load last 20 messages
```

**Output:**
```
Reloaded conversation history!
- Loaded 12 messages
- Found 3 character(s): Alice, Bob, Charlie
```

### Swipe with History

```
User: !chat Alice: "Tell me about space"
Bot: Space is vast and full of wonders...

User: !swipe
Bot: The cosmos stretches infinitely...
     [Uses all previous context except the last response]
     *Alternative 2/2 (use !swipe_left/!swipe_right to navigate)*
```

## Technical Implementation

### Key Methods

1. **`load_channel_history(channel, limit=50)`**
   - Fetches messages from Discord channel
   - Parses `!chat` commands
   - Returns conversation history + character names

2. **`!chat` command integration**
   - Checks if conversation is empty
   - Loads history automatically if needed
   - Merges character names

3. **`!swipe` command integration**
   - Also loads history if needed
   - Uses enhanced system prompt
   - Excludes only last response

### Message Filtering Logic

```python
# User messages: Must start with !chat
if message.content.startswith("!chat "):
    chat_message = message.content[6:].strip()
    character_name, actual_message = self.parse_character_message(chat_message)
    # Add to conversation...

# Bot responses: From this bot, not commands, not meta
elif message.author.id == self.user.id and not message.content.startswith("!"):
    if message.content.startswith("*Alternative "):
        continue  # Skip meta messages
    # Add to conversation...
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `!chat <message>` | Chat with AI (auto-loads history on first use) |
| `!reload_history [limit]` | Manually reload context from channel (default 50, max 100) |
| `!clear` | Clear conversation (next chat will reload from history) |
| `!swipe` | Generate alternative (uses full context) |
| `!swipe_left` | Previous alternative |
| `!swipe_right` | Next alternative |

## Configuration

No configuration needed - works automatically!

**Defaults:**
- 50 messages loaded on first use
- 100 message maximum limit
- 20 message conversation history limit
- Chronological order (oldest first)

**Customization:**
```
!reload_history 30    # Custom limit
```

## Benefits

✅ **Conversation persistence** - Context survives bot restarts
✅ **Character continuity** - Character names remembered from history
✅ **Automatic operation** - No user action needed
✅ **Manual control** - `!reload_history` for custom refreshes
✅ **Swipe compatibility** - Works seamlessly with alternatives
✅ **Smart filtering** - Only relevant messages included
✅ **Configurable limits** - Adjust to your needs

## Documentation

For more details, see:
- **[CONTEXT_MANAGEMENT.md](CONTEXT_MANAGEMENT.md)** - Complete guide
- **[CHARACTER_TRACKING.md](CHARACTER_TRACKING.md)** - Character name feature
- **[README.md](README.md)** - Overview and commands

## Summary

**Question:** Does the bot read past `!chat` messages from the channel?
**Answer:** ✅ Yes! The bot now automatically loads recent channel history.

**Question:** Does it track character names from past messages?
**Answer:** ✅ Yes! Character names are extracted and tracked.

**Question:** Does swipe respect the context correctly?
**Answer:** ✅ Yes! Swipe uses full context but excludes only its last response.

**Question:** Does it respect token/context limits?
**Answer:** ✅ Yes! Configurable message limits with max 100 messages.

**Question:** Does it track its own responses?
**Answer:** ✅ Yes! Bot responses are loaded from channel history.

**The feature is fully implemented and working!** 🎉
