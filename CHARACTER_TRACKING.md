# Character Name Tracking Feature

## Overview

The Discord bot now supports character name tracking, allowing users to identify themselves as characters in roleplay scenarios. This feature makes it easier for the AI to understand multi-character conversations.

## How to Use

### Basic Format

Use the format `CharacterName: message` when chatting with the bot:

```
!chat Alice: "Hello, how are you today?"
!chat Bob: *waves* "Hi everyone!"
!chat Charlie: "I'm doing great, thanks!"
```

### Message Formatting Guidelines

The bot supports three types of content in messages:

1. **Spoken Dialogue** - Use `"quotes"` for words spoken by the character:
   ```
   !chat Alice: "Hello! How can I help you?"
   ```

2. **Actions** - Use `*asterisks*` for actions performed by the character:
   ```
   !chat Bob: *walks into the room*
   !chat Sarah: *waves enthusiastically*
   ```

3. **Descriptive Text** - Text without quotes or asterisks is descriptive or contextual:
   ```
   !chat Tom: Looks around the room carefully
   ```

### Combining Formats

You can combine dialogue, actions, and descriptions in a single message:

```
!chat Sarah: *enters the room* "Good morning everyone!" She smiles warmly
!chat Tom: *looks up from his book* "Oh, hello Sarah!" *closes the book*
!chat Alice: Notices the newcomers "Welcome! Please, have a seat." *gestures to the chairs*
```

### How It Works

1. **Parsing**: The bot automatically detects character names before colons
2. **Tracking**: All character names are tracked per channel
3. **Context**: The AI is informed about which characters are in the conversation
4. **Prevention**: The AI is explicitly instructed NOT to pretend to be these characters
5. **Persistence**: Character names and conversations persist across bot restarts by reading channel history

### Context Persistence

The bot now automatically loads recent channel history when starting a conversation. This means:

- **Character names are remembered** even after bot restarts
- **Conversation context persists** across sessions
- **Past `!chat` messages are included** in the AI's context

For example:
```
Session 1:
!chat Alice: "Hello everyone!"
!chat Bob: "Hi Alice!"

[Bot restarts]

Session 2:
!chat Alice: "Bob, remember what we discussed?"
Bot: [Remembers both Alice and Bob from channel history]
```

Use `!reload_history` to manually refresh the context from channel messages. See [Context Management Guide](CONTEXT_MANAGEMENT.md) for details.

### System Prompt Enhancement

When character names are detected, the system prompt is enhanced:

```
Base: "You are a helpful AI assistant."

Enhanced: "You are a helpful AI assistant.

IMPORTANT: In this conversation, users will identify themselves as characters 
by prefixing their messages with 'CharacterName:'. The following character 
names are being used by users: Alice, Bob, Charlie. You should NEVER pretend 
to be these characters or respond as if you are them. You are a separate 
entity having a conversation with these characters.

FORMAT GUIDELINES:
- Text in "quotes" represents spoken dialogue by the character
- Text in *asterisks* represents actions performed by the character
- Text without quotes or asterisks is descriptive text or additional context"
```

## Example Conversation

```
User: !chat Alice: "Hello! Is anyone here?"
Bot: Hello Alice! Yes, I'm here. How can I help you today?

User: !chat Bob: *walks in* "Hey Alice! I just arrived."
Bot: Welcome, Bob! I see you've just joined Alice. How are you both doing?

User: !chat Alice: *turns to Bob* "We're planning an adventure, care to help us prepare?"
Bot: Of course! I'd be happy to help you and Bob prepare for your adventure. 
     What kind of adventure are you planning?

User: !chat Bob: Pulls out a map "We're thinking of exploring the ancient ruins to the north."
Bot: That sounds exciting! Exploring ancient ruins can be quite an adventure. 
     What supplies do you think you'll need for this journey?
```

## Commands

- `!clear` - Clears conversation history AND tracked character names
- `!help_bot` - Shows help including character name feature documentation

## Technical Details

### Character Name Parsing

The bot uses regex pattern matching to identify character names:
- Pattern: `^([^:]+?)\s*:\s*(.+)$`
- Supports spaces around the colon
- Extracts character name and message separately

### Storage

- Character names are stored per channel in `bot.character_names[channel_id]`
- Names are preserved until `!clear` is called
- Each channel maintains its own list of characters

### Conversation Format

Messages are stored in conversation history with the character name prefix:
```python
{"role": "user", "content": "Alice: Hello, how are you?"}
{"role": "assistant", "content": "Hello Alice! How can I help you?"}
```

## Testing

Run the test script to see the feature in action:

```bash
python /tmp/test_character_tracking.py
```

This demonstrates:
- Character name parsing
- Name tracking across messages
- System prompt enhancement
- Formatted message storage
