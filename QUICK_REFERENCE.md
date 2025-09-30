# User Characters Quick Reference

## What is This?
Save descriptions of your roleplay characters so the AI knows their appearance and traits!

## Quick Commands

### Discord Bot Commands
```bash
# Save a character description
!update Alice: A brave warrior with long red hair and green eyes, wearing silver armor.

# List all saved characters
!user_chars

# View a specific character
!user_char Alice

# Delete a character
!delete_user_char Alice
```

### Using Characters in Chat
```bash
# Just use the character name before your message
!chat Alice: "Hello everyone!" *waves*

# The AI will automatically know Alice's description!
```

## Web Interface

1. Go to `http://localhost:5000`
2. Click **"User Characters"** tab
3. Enter name and description
4. Click **"Save User Character"**

### Import/Export
- **Export**: Click "Export All" to download JSON backup
- **Import**: Click "Import", paste JSON, click "Import"

## How It Works

1. You save a character: `!update Alice: A brave warrior...`
2. You chat as that character: `!chat Alice: "Hello!"`
3. The AI gets Alice's description automatically
4. The AI can reference Alice's appearance and traits in responses
5. The AI knows NOT to act as Alice (only you can!)

## Example Workflow

```bash
# Step 1: Save characters
!update Alice: A brave warrior with long red hair and green eyes.
!update Bob: A skilled archer with short brown hair.

# Step 2: Start roleplay
!chat Alice: "Bob, look over there!" *points to the forest*
# AI knows Alice has red hair, green eyes, is brave

!chat Bob: *nods quietly* "I see it."
# AI knows Bob has brown hair, is quiet

# The AI will reference these traits in its responses!
```

## Tips

✅ **Be descriptive**: Include appearance, personality, background  
✅ **Update anytime**: Use `!update` again to change description  
✅ **Export regularly**: Backup your characters with Export  
✅ **Use formatting**: `"quotes"` for dialogue, `*asterisks*` for actions  

## Need More Help?

See **USER_CHARACTERS_GUIDE.md** for detailed examples and advanced usage!
