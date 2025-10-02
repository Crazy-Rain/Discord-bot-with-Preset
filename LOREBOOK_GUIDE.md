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
- **Linked Character**: Optional character link - lorebook only activates when that specific character is loaded
- **Global Lorebook**: A lorebook with no character link - always active when enabled

### Character-Linked vs Global Lorebooks

**NEW FEATURE**: You can now link lorebooks to specific AI characters!

- **Global Lorebooks**: No character link (default). Active whenever they are enabled, regardless of which character is loaded.
- **Character-Linked Lorebooks**: Linked to a specific character. Only active when that character is loaded and being used by the AI.

**Use Cases:**
- Create a "Base World Rules" lorebook that's always active (global)
- Create character-specific lorebooks like "Luna's Backstory" that only activate when Luna is the active character
- Combine both types: global world lore + character-specific details

**Example:**
```
Global Lorebook: "Fantasy World Rules"
  - Magic System (always active)
  - Currency System (always active)

Character-Linked: "Luna" → "Luna's Lore"
  - Luna's secret past
  - Luna's special abilities
  - People only Luna knows

Character-Linked: "Sherlock" → "Sherlock's Lore"
  - Sherlock's deductive techniques
  - Victorian London details specific to Sherlock
```

When Luna is active: You get Fantasy World Rules + Luna's Lore
When Sherlock is active: You get Fantasy World Rules + Sherlock's Lore
When no character is loaded: You only get Fantasy World Rules

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
4. Enter a name (e.g., "Fantasy World", "Sci-Fi Setting", "Luna's Backstory")
5. Optionally add a description
6. **NEW**: Optionally link to a character (or leave as "Global" for always-active)
7. Click **Create**

**Character Linking:**
- Select "Global (no character link)" to create a lorebook that works with any character
- Select a specific character name to link the lorebook to that character
- Character-linked lorebooks only activate when that character is loaded via `!character <name>`

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

### Editing Lorebook Metadata

**NEW**: You can now edit a lorebook's description and character link!

1. Select the lorebook from the dropdown
2. Click **Edit Metadata** button
3. Update the description and/or character link
4. Click **Save**

This allows you to:
- Change a global lorebook to be character-linked
- Change a character-linked lorebook to be global
- Move a lorebook from one character to another
- Update the description

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
  "linked_character": null,
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

**For Character-Linked Lorebooks:**
```json
{
  "name": "Luna's Lore",
  "description": "Luna-specific backstory and abilities",
  "enabled": true,
  "linked_character": "Luna",
  "entries": {
    "Luna's Powers": {
      "key": "Luna's Powers",
      "content": "Luna can control moonlight and has telepathy",
      "keywords": ["luna", "power", "ability"],
      "activation_type": "constant"
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
1. Create "Base Rules" lorebook with always-active world rules (global)
2. Create "Current Arc" lorebook with story-specific lore (global)
3. Enable both to combine their entries
4. Disable "Current Arc" when moving to a new story

### Using Character-Linked Lorebooks

**NEW**: Link lorebooks to specific characters for character-specific lore!

**Scenario 1: Multiple Characters with Unique Backgrounds**

```
1. Create global lorebook: "Sci-Fi Universe"
   - Link: Global
   - Contains: FTL travel rules, alien species, technology

2. Create character lorebook: "Captain Sarah's History"
   - Link: Captain Sarah
   - Contains: Sarah's military service, her ship's crew, personal relationships

3. Create character lorebook: "Dr. Chen's Research"
   - Link: Dr. Chen  
   - Contains: Chen's scientific discoveries, lab location, research team
```

When you load Captain Sarah (`!character "Captain Sarah"`):
- Sci-Fi Universe lore is active
- Captain Sarah's History is active
- Dr. Chen's Research is NOT active

When you load Dr. Chen (`!character "Dr. Chen"`):
- Sci-Fi Universe lore is active
- Dr. Chen's Research is active
- Captain Sarah's History is NOT active

**Scenario 2: Character Evolution**

Create separate lorebooks for different story arcs of the same character:

```
Global: "Kingdom of Aldoria" (world rules)
Character-linked to "Luna": "Luna - Early Days" (her childhood, training)
Character-linked to "Luna": "Luna - Queen Era" (her reign, responsibilities)
```

Enable "Luna - Early Days" for flashback scenes, switch to "Luna - Queen Era" for present-day.

**Benefits:**
- Keep character-specific lore organized and separate
- Avoid lore conflicts between different characters
- Reduce token usage - only load relevant lore for active character
- Easily share character lorebooks with character cards

## Best Practices

1. **Organize by Setting**: Create separate lorebooks for different worlds or campaigns
2. **Use Descriptive Names**: Name lorebooks clearly (e.g., "Cyberpunk 2077 World" vs "Lorebook 1")
3. **One Setting at a Time**: For focused roleplay, enable only the relevant lorebook(s)
4. **Use Constant Activation Sparingly**: Only use "Constant" activation for essential world rules and core setting information
5. **Disable When Not Needed**: Disable lorebooks you're not currently using to reduce context clutter
6. **Export for Backup**: Regularly export your lorebooks as JSON files for backup
7. **Share Lorebooks**: Share your exported lorebook JSON files with others
8. **Use Character Linking**: Link character-specific lore to characters to keep things organized and automatic
9. **Combine Global + Character**: Use global lorebooks for world rules, character-linked for personal details
10. **Character Packages**: When sharing a character card, also share their linked lorebook for the complete experience

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

**Lorebook Structure:**
Each lorebook in `lorebooks.json` contains:
- `name`: Lorebook name
- `description`: Optional description
- `enabled`: Whether the lorebook is active
- `linked_character`: Optional character name (null for global lorebooks)
- `entries`: Dictionary of lorebook entries

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
