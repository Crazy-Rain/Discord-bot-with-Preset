# Lorebook Guide

## Overview

The Lorebook feature allows you to add world-building and lore information that the AI can use for context during conversations. This is similar to how SillyTavern uses lorebooks to provide consistent world information across roleplay sessions.

**NEW**: You can now manage multiple lorebooks, enable/disable them individually, and easily swap between different settings!

## Key Concepts

- **Lorebook**: A collection of related lore entries with a name and description
- **Entry Key**: A unique identifier for each lorebook entry (e.g., "Kingdom of Aldoria", "Magic System")
- **Content**: The actual lore or information about the entry
- **Keywords**: Optional list of words that trigger this entry to be included when mentioned
- **Activation Type**: How the entry is triggered (see below)
- **Enabled/Disabled**: Each lorebook can be toggled on or off to control which lore is active

### Activation Types

Lorebook entries now support three activation types:

1. **Normal (Keyword-triggered)**: Entry appears when any of its keywords are mentioned in the conversation
2. **Constant (Always Active)**: Entry is always included in the AI's context, regardless of keywords
3. **Vectorized (Semantic search)**: *Planned feature* - Will use semantic similarity to determine relevance. Currently works like Normal.

Choose the activation type based on how you want the entry to be used:
- Use **Constant** for fundamental world rules, magic systems, or core setting information
- Use **Normal** for locations, characters, or events that should only appear when relevant
- Use **Vectorized** for future semantic search capabilities (currently behaves like Normal)

## Managing Multiple Lorebooks

### Creating a Lorebook

**Via Web Interface:**
1. Navigate to `http://localhost:5000`
2. Click on the **Lorebook** tab
3. Click **New Lorebook** button
4. Enter a name (e.g., "Fantasy World", "Sci-Fi Setting")
5. Optionally add a description
6. Click **Create**

### Switching Between Lorebooks

Use the **Active Lorebook** dropdown to select which lorebook you want to work with. You can have multiple lorebooks created, but entries are organized within each lorebook.

### Enabling/Disabling Lorebooks

- Check or uncheck the **Enabled** checkbox next to a lorebook to toggle it
- Disabled lorebooks won't have their entries included in AI responses
- This allows you to quickly switch between different settings without deleting lorebooks

### Deleting a Lorebook

1. Select the lorebook from the dropdown
2. Click **Delete This Lorebook**
3. Confirm the deletion (this will remove all entries in that lorebook)

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
3. Select or create a lorebook using the **Active Lorebook** dropdown
4. Fill in the entry details:
   - **Entry Key**: Unique identifier
   - **Content**: The lore information
   - **Keywords**: Comma-separated keywords (optional)
   - **Activation Type**: Choose from Normal, Constant, or Vectorized
5. Click **Save Entry**

**Note**: The old "Always Active" checkbox has been replaced with the Activation Type dropdown. Existing entries with `always_active: true` will be automatically migrated to `activation_type: "constant"`.

### Import/Export

#### Exporting a Lorebook
- **Single Lorebook**: Select a lorebook and click "Export This Lorebook" to download it as JSON
- **All Entries**: Click "Export All" to download all entries from all enabled lorebooks

#### Importing a Lorebook

**New Structured Format** (Recommended):
```json
{
  "name": "My Fantasy World",
  "description": "A complete fantasy setting",
  "enabled": true,
  "entries": {
    "Entry Key": {
      "key": "Entry Key",
      "content": "...",
      "keywords": ["keyword1", "keyword2"],
      "activation_type": "normal"
    }
  }
}
```

**Legacy Format** (Still Supported):
```json
{
  "Entry Key": {
    "key": "Entry Key",
    "content": "...",
    "keywords": ["keyword1", "keyword2"],
    "always_active": false
  }
}
```

**Note**: When importing lorebooks with the old `always_active` field, it will be automatically converted:
- `always_active: true` → `activation_type: "constant"`
- `always_active: false` → `activation_type: "normal"`
{
  "Entry Key": {
    "key": "Entry Key",
    "content": "...",
    "keywords": ["keyword1", "keyword2"],
    "always_active": false
  }
}
```

Click "Import" and paste JSON data:
- Check "Merge with existing" to add to current entries
- Uncheck to replace all entries
- New format creates/updates the specified lorebook
- Legacy format imports to the "Default" lorebook

## How It Works

### Keyword Matching

When you send a message, the lorebook system checks if any keywords are mentioned:

```
!chat I want to learn magic in the kingdom
```

If you have entries with keywords `magic` or `kingdom`, they will be included in the AI's context.

### Constant (Always Active) Entries

Entries with activation type "Constant" are included in every conversation, regardless of keywords. This is useful for:
- Core world rules (magic systems, physics)
- Important background information
- Setting tone and atmosphere

### Vectorized Entries

The "Vectorized" activation type is planned for future semantic search capabilities. Currently, it behaves the same as "Normal" (keyword-triggered).

## Examples

### Example 1: Fantasy World Lorebook

You can import the included `lorebook/fantasy_aldoria.json` file which contains:
- Magic System (constant activation)
- Kingdom of Aldoria (normal activation)
- The Dark Forest (normal activation)
- Mage Knights (normal activation)
- The Great War (normal activation)

### Example 2: Sci-Fi Setting

Create a "Sci-Fi Universe" lorebook:

```
Entry: "FTL Travel"
Content: Faster-than-light travel uses jump gates between systems. Each gate requires massive energy and can only connect to paired gates.
Keywords: ftl, travel, jump, gate
Activation Type: Constant

Entry: "Earth Alliance"
Content: Federation of human colonies with headquarters on Mars. Founded after the First Contact War.
Keywords: alliance, earth, federation, colonies
Activation Type: Normal

Entry: "Xenon Empire"
Content: Advanced alien civilization known for biotechnology and crystal-based computing.
Keywords: xenon, alien, empire, biotechnology
Activation Type: Normal
```

### Example 3: Murder Drones Setting

You can import the included `lorebook/murder_drones_lore.json` file which contains lore for:
- Copper-9 (the planet)
- Worker Drones
- Disassembly Drones
- The Absolute Solver

### Using Multiple Lorebooks Together

You can enable multiple lorebooks at once:
1. Create "Base Rules" lorebook with always-active world rules
2. Create "Current Arc" lorebook with story-specific lore
3. Enable both to combine their entries
4. Disable "Current Arc" when moving to a new story

## Best Practices

1. **Organize by Setting**: Create separate lorebooks for different worlds or campaigns
2. **Use Descriptive Names**: Name lorebooks clearly (e.g., "Cyberpunk 2077 World" vs "Lorebook 1")
3. **One Setting at a Time**: For focused roleplay, enable only the relevant lorebook(s)
4. **Use Constant Activation Sparingly**: Only use "Constant" activation for essential world rules and core setting information
5. **Disable When Not Needed**: Disable lorebooks you're not currently using to reduce context clutter
6. **Export for Backup**: Regularly export your lorebooks as JSON files for backup
7. **Share Lorebooks**: Share your exported lorebook JSON files with others

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

Lorebooks are stored in two files:

```
lorebook/lorebooks.json    # Main storage with all lorebook collections
lorebook/lorebook.json      # Legacy flat format (auto-generated from enabled lorebooks)
```

The system maintains backward compatibility by automatically syncing enabled lorebook entries to the legacy format.

**Sample Lorebook Files:**
- `lorebook/fantasy_aldoria.json` - Fantasy setting example
- `lorebook/murder_drones_lore.json` - Sci-fi setting example

You can import these files directly through the web interface!

## Troubleshooting

### Entry Not Appearing

1. Check that the lorebook containing the entry is **enabled**
2. Verify keywords are spelled correctly
3. Check that keywords appear in your message
4. Try marking as "always active" for testing

### Too Much Context

If responses seem cluttered:
1. Disable lorebooks you're not currently using
2. Remove unnecessary "always active" entries
3. Use more specific keywords
4. Keep content concise

### Import Issues

- **New Format**: Ensure JSON has `name`, `description`, and `entries` fields
- **Legacy Format**: Ensure it's a flat dict of entries
- Check for duplicate keys within a lorebook
- Verify content doesn't have special characters that break JSON
- Use a JSON validator to check format

### Lorebook Not Saving

1. Ensure you've selected a lorebook in the dropdown
2. Create a new lorebook if none exist
3. Check browser console for errors

## Questions?

For more information, see the main README.md or use `!help_bot` in Discord.
