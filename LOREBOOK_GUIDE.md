# Lorebook Guide

## Overview

The Lorebook feature allows you to add world-building and lore information that the AI can use for context during conversations. This is similar to how SillyTavern uses lorebooks to provide consistent world information across roleplay sessions.

## Key Concepts

- **Entry Key**: A unique identifier for the lorebook entry (e.g., "Kingdom of Aldoria", "Magic System")
- **Content**: The actual lore or information about the entry
- **Keywords**: Optional list of words that trigger this entry to be included when mentioned
- **Always Active**: If enabled, the entry is always included in the AI's context

## Using Discord Commands

### Add or Update Entry

```
!lorebook_add "Kingdom of Aldoria" A vast kingdom ruled by King Aldric... [keywords: kingdom, aldoria, king] [always_active]
```

**Format Options:**
- Basic: `!lorebook_add <key> <content>`
- With keywords: Add `[keywords: word1, word2, word3]` at the end of content
- Always active: Add `[always_active]` at the end of content

### View All Entries

```
!lorebook_list
```

### View Specific Entry

```
!lorebook_view "Kingdom of Aldoria"
```

### Delete Entry

```
!lorebook_delete "Kingdom of Aldoria"
```

## Using the Web Interface

1. Navigate to `http://localhost:5000`
2. Click on the **Lorebook** tab
3. Fill in the entry details:
   - **Entry Key**: Unique identifier
   - **Content**: The lore information
   - **Keywords**: Comma-separated keywords (optional)
   - **Always Active**: Check if this should always be included
4. Click **Save Entry**

### Import/Export

- **Export**: Click "Export All" to download all entries as JSON
- **Import**: Click "Import" and paste JSON data
  - Check "Merge with existing" to add to current entries
  - Uncheck to replace all entries

## How It Works

### Keyword Matching

When you send a message, the lorebook system checks if any keywords are mentioned:

```
!chat I want to learn magic in the kingdom
```

If you have entries with keywords `magic` or `kingdom`, they will be included in the AI's context.

### Always Active Entries

Entries marked as "always active" are included in every conversation, regardless of keywords. This is useful for:
- Core world rules (magic systems, physics)
- Important background information
- Setting tone and atmosphere

## Examples

### Example 1: Fantasy World

```
!lorebook_add "Magic System" Magic requires mana crystals and only those with the Gift can use it [keywords: magic, spell, mana] [always_active]
!lorebook_add "Kingdom of Aldoria" Ruled by King Aldric, capital has a crystal tower [keywords: kingdom, aldoria, king, capital]
!lorebook_add "The Dark Forest" Dangerous forest on the northern border, home to monsters [keywords: forest, north, monsters, dark]
```

### Example 2: Sci-Fi Setting

```
!lorebook_add "FTL Travel" Faster-than-light travel uses jump gates between systems [keywords: ftl, travel, jump, gate] [always_active]
!lorebook_add "Earth Alliance" Federation of human colonies, headquarters on Mars [keywords: alliance, earth, federation, colonies]
!lorebook_add "Xenon Empire" Alien empire known for advanced technology [keywords: xenon, alien, empire]
```

### Example 3: Modern Setting

```
!lorebook_add "The Organization" Secret agency protecting humanity from supernatural threats [keywords: organization, agency, secret] [always_active]
!lorebook_add "Chicago Office" Main headquarters in downtown Chicago [keywords: chicago, office, headquarters]
```

## Best Practices

1. **Use Descriptive Keys**: Make entry keys clear and specific
2. **Be Concise**: Keep content focused and relevant
3. **Choose Keywords Wisely**: Pick words that will naturally appear in conversations
4. **Use Always Active Sparingly**: Only for essential world information
5. **Organize Related Entries**: Group related lore together

## Integration with Other Features

### Works With User Characters

Lorebook works alongside user character descriptions:

```
!update Alice: A brave warrior from Aldoria
!lorebook_add "Kingdom of Aldoria" A vast kingdom...
!chat Alice: "I'm returning to my homeland!" *heads toward the kingdom*
```

The AI will have both Alice's description and the kingdom's lore.

### Works With Character Cards

You can combine AI character cards with lorebook:

```
!character sherlock  # Load Sherlock character
!lorebook_add "Victorian London" Description of the setting...
!chat "What do you know about the recent murders?"
```

## Storage

All lorebook entries are stored in:
```
lorebook/lorebook.json
```

This file is automatically created and updated. You can back it up or share it with others.

## Troubleshooting

### Entry Not Appearing

1. Check keywords are spelled correctly
2. Verify keywords appear in your message
3. Try marking as "always active" for testing

### Too Much Context

If responses seem cluttered:
1. Remove unnecessary "always active" entries
2. Use more specific keywords
3. Keep content concise

### Import Issues

- Ensure JSON format is correct
- Check for duplicate keys
- Verify content doesn't have special characters that break JSON

## Questions?

For more information, see the main README.md or use `!help_bot` in Discord.
