# Multiple Lorebooks - Quick Start Guide

## What's New?

You can now create and manage multiple lorebook collections, each with its own set of entries. This allows you to:
- Organize lore by setting (Fantasy, Sci-Fi, Modern, etc.)
- Quickly switch between different worlds/campaigns
- Enable/disable entire lorebooks without deleting them
- Share complete lorebook collections as single files

## Quick Example

### Step 1: Import Sample Lorebooks

1. Go to `http://localhost:5000` → **Lorebook** tab
2. Click **Import**
3. Open `lorebook/fantasy_aldoria.json` in a text editor
4. Copy the entire contents and paste into the import dialog
5. Click **Import**
6. Repeat for `lorebook/murder_drones_lore.json`

### Step 2: View Your Lorebooks

In the "Manage Lorebooks" section, you'll see:
- **Fantasy World - Aldoria** ● Enabled - 5 entries
- **Murder Drones Lore** ● Enabled - 4 entries

### Step 3: Switch Between Lorebooks

Use the "Active Lorebook" dropdown to select which one you want to work with:
- Select "Fantasy World - Aldoria" to see/edit fantasy entries
- Select "Murder Drones Lore" to see/edit sci-fi entries

### Step 4: Enable/Disable Lorebooks

- Check/uncheck the **Enabled** checkbox to toggle a lorebook
- Disabled lorebooks won't affect AI responses
- Perfect for temporarily switching settings without losing data

## Common Use Cases

### Use Case 1: Multiple Campaign Settings

You're running two D&D campaigns:
1. Create "Campaign: Lost Mines" lorebook with that campaign's lore
2. Create "Campaign: Dragon Heist" lorebook with different lore
3. Enable only the one you're currently playing
4. Both campaigns keep their lore separate and organized

### Use Case 2: Base Rules + Story Arcs

1. Create "World Rules" lorebook (always active: magic system, physics, etc.)
2. Create "Arc 1: The Awakening" lorebook (current story arc lore)
3. Create "Arc 2: The War" lorebook (next story arc, disabled for now)
4. Keep "World Rules" always enabled
5. Switch between arc lorebooks as your story progresses

### Use Case 3: Shared Lorebooks

1. Create a lorebook for your setting
2. Export it using "Export This Lorebook"
3. Share the JSON file with friends
4. They can import it and have the exact same lore

## File Format

### Structured Format (Recommended)

```json
{
  "name": "My Fantasy World",
  "description": "A medieval fantasy setting",
  "enabled": true,
  "entries": {
    "Magic System": {
      "key": "Magic System",
      "content": "Magic requires mana crystals...",
      "keywords": ["magic", "spell"],
      "always_active": true
    },
    "Capital City": {
      "key": "Capital City", 
      "content": "The capital is called...",
      "keywords": ["capital", "city"],
      "always_active": false
    }
  }
}
```

This creates a complete lorebook that can be enabled/disabled as a unit.

### Legacy Format (Still Supported)

```json
{
  "Magic System": {
    "key": "Magic System",
    "content": "...",
    "keywords": ["magic"],
    "always_active": true
  }
}
```

This imports entries into the "Default" lorebook.

## Tips

- **Name lorebooks clearly**: "Cyberpunk 2077" not "Lorebook 1"
- **Use descriptions**: Helps remember what each lorebook is for
- **Export regularly**: Backup your lorebooks as JSON files
- **One setting at a time**: For focused roleplay, enable only relevant lorebooks
- **Share with community**: Export and share your lorebooks with others!

## Questions?

See the full [LOREBOOK_GUIDE.md](LOREBOOK_GUIDE.md) for detailed documentation.
