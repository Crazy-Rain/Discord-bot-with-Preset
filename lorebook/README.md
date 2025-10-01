# Lorebook Sample Files

This directory contains example lorebook files that you can import into the Discord bot.

## How to Use

1. Navigate to `http://localhost:5000` in your browser
2. Click on the **Lorebook** tab
3. Click **Import** button
4. Copy the contents of one of these files and paste it into the import dialog
5. Click **Import** to add the lorebook to your collection

## Sample Files

### fantasy_aldoria.json
A high-fantasy medieval setting featuring:
- **Magic System**: Mana crystal-based magic with different types
- **Kingdom of Aldoria**: A prosperous kingdom with a crystal tower
- **The Dark Forest**: Dangerous northern forest with monsters
- **Mage Knights**: Elite warrior-mage combination
- **The Great War**: Historical conflict that shaped the world

**Best for**: Fantasy roleplay, D&D-style adventures, medieval settings

### murder_drones_lore.json
Based on the Murder Drones animated series:
- **Copper-9**: The frozen exoplanet setting
- **Worker Drones**: Sentient robots building their own society
- **Disassembly Drones**: The murder drones hunting workers
- **The Absolute Solver**: Mysterious reality-bending entity

**Best for**: Sci-fi horror, robot characters, Murder Drones fan content

## Creating Your Own Lorebooks

Each lorebook file follows this structure:

```json
{
  "name": "Your Lorebook Name",
  "description": "Brief description of the setting",
  "enabled": true,
  "entries": {
    "Entry Name": {
      "key": "Entry Name",
      "content": "The lore content goes here",
      "keywords": ["keyword1", "keyword2"],
      "always_active": false
    }
  }
}
```

### Tips for Creating Entries

- **Keywords**: Choose words that will naturally appear in conversations
- **Always Active**: Use sparingly - only for core world rules
- **Content**: Keep it concise but informative (2-4 sentences)
- **Entry Keys**: Use descriptive, unique names

## File Storage

- `lorebooks.json` - Main storage for all your lorebook collections
- `lorebook.json` - Legacy format (auto-generated, contains all enabled entries)
- `*.json` - Sample lorebook files (these are examples, not loaded automatically)

To use sample files, you must import them through the web interface.
