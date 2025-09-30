# User Character Descriptions Guide

This guide explains how to use the User Character Descriptions feature to enhance your roleplay experiences with the Discord bot.

## Overview

User Character Descriptions allow you to save detailed information about your roleplay characters. When you use a character name in chat, the AI will automatically reference their saved description to provide better, more contextualized responses.

## Key Concepts

- **Character Name**: The name used when chatting (e.g., `!chat Alice: "Hello!"`)
- **Character Description**: Physical appearance, personality traits, background, etc.
- **System Prompt Integration**: Descriptions are automatically added to the AI's context
- **Persistence**: All descriptions are saved between sessions

## Using Discord Commands

### 1. Add or Update a Character Description

```
!update Alice: A brave warrior with long red hair and green eyes, wearing silver armor. Known for her courage and compassion.
```

The format is: `!update <Character Name>: <Description>`

### 2. List All Saved Characters

```
!user_chars
```

This will show all character names you've saved.

### 3. View a Specific Character

```
!user_char Alice
```

This displays Alice's full description.

### 4. Delete a Character

```
!delete_user_char Alice
```

This removes Alice's description from the saved characters.

## Using the Web Interface

1. Navigate to `http://localhost:5000`
2. Click on the "User Characters" tab
3. Enter the character name and description
4. Click "Save User Character"

### Import/Export

You can import and export all your character descriptions as JSON:

**Export**: Click "Export All" to download a JSON file with all your characters

**Import**: Click "Import" and paste JSON data in this format:
```json
{
  "Alice": {
    "name": "Alice",
    "description": "A brave warrior with long red hair and green eyes, wearing silver armor. Known for her courage and compassion."
  },
  "Bob": {
    "name": "Bob",
    "description": "A skilled archer with short brown hair and a quiet demeanor. Fiercely loyal to his friends."
  }
}
```

## Complete Usage Example

### Step 1: Save Character Descriptions

```
!update Alice: A brave warrior with long red hair and green eyes, wearing silver armor. Known for her courage and compassion.
!update Bob: A skilled archer with short brown hair and a quiet demeanor. Fiercely loyal to his friends.
```

### Step 2: Use Characters in Roleplay

```
!chat Alice: "Bob, look over there!" *points toward the forest*
```

The AI will receive context about Alice (appearance, personality) automatically.

```
!chat Bob: *nods* "I see movement in the trees."
```

The AI will also have Bob's description in context.

### Step 3: AI Response

The AI will respond understanding both characters' appearances and traits:

```
The distant rustling in the forest grows louder. Given Alice's brave nature and 
Bob's keen archer skills, they're well-positioned to investigate...
```

## How It Works Behind the Scenes

When you use a character name in chat:

1. The bot checks if that character has a saved description
2. If found, it adds this section to the AI's system prompt:

```
[Alice Description]
Name: Alice
Description: A brave warrior with long red hair and green eyes, wearing silver armor. 
Known for her courage and compassion.
Note: This is a User Character, for referencing when Alice is doing something, In scene, 
or needing to be referenced in some manner. Do not Act, or Write for this Character, they 
are only for the Human to Act/Write/Play as.
[/Alice Description]
```

3. The AI uses this information to provide context-aware responses
4. The AI is explicitly instructed NOT to act as or write for these characters

## Best Practices

### Good Descriptions

✅ **Include physical appearance**:
```
Long red hair, green eyes, wearing silver armor
```

✅ **Include personality traits**:
```
Known for her courage and compassion
```

✅ **Include relevant background**:
```
A veteran of many battles, respected by her peers
```

### Tips for Better Roleplay

1. **Be Specific**: More detail helps the AI understand your character better
2. **Update as Needed**: Use `!update` to modify descriptions as your character develops
3. **Multiple Characters**: Save all characters in your roleplay party for consistency
4. **Use Formatting**: The bot supports `"quotes"` for dialogue and `*asterisks*` for actions

## Example Roleplay Session

```
# Setup characters
!update Elena: A young mage with purple robes and silver hair. Curious and eager to learn magic.
!update Marcus: A grizzled mercenary with scars across his face. Cynical but protective.

# Start roleplay
!chat Elena: "Marcus, I sense powerful magic ahead!" *clutches her staff nervously*

Bot: The ancient ruins loom before you. Marcus's battle-hardened instincts 
kick in as Elena's magical sensitivity picks up on the arcane energy...

!chat Marcus: *draws his sword* "Stay close, kid. Let me check it out first."

Bot: Marcus advances cautiously, his years of experience showing in every 
calculated step. Elena's silver hair glows faintly as she prepares a protective spell...
```

## File Storage

All user character descriptions are saved in:
```
user_characters/user_characters.json
```

This file is automatically created and updated when you add or modify characters. You can back it up or share it with others.

## Troubleshooting

### Character not appearing in AI's context

- Make sure you saved the character with `!update`
- Check that you're using the exact same name in `!chat`
- Use `!user_chars` to verify the character is saved

### Description not updating

- Use `!update` again with the same name to overwrite
- The new description will be used immediately in future chats
- You may need to use `!clear` to reset the conversation

### Can't find saved characters

- Check if the file exists: `user_characters/user_characters.json`
- Use the web interface to view and manage characters
- Export your characters regularly as backup

## Advanced Usage

### Combining with Character Cards

You can use User Character Descriptions alongside AI Character Cards:

- **AI Character Card**: Defines the AI's personality (e.g., "Sherlock")
- **User Characters**: Define the human players' characters (e.g., "Alice", "Bob")

```
!character sherlock  # Load AI character
!update Alice: A brave warrior...  # Define your character
!chat Alice: "Mr. Holmes, I need your help!"
```

The AI (as Sherlock) will know Alice's description when responding.

## Questions?

For more information, see the main README.md or use `!help_bot` in Discord.
