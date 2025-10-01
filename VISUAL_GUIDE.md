# Multiple Lorebooks Feature - Visual Guide

## Web Interface Overview

### 1. Lorebook Management Section

When you open the Lorebook tab, you'll see:

```
┌─────────────────────────────────────────────────────────────┐
│ Manage Lorebooks                                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Active Lorebook: [Fantasy World - Aldoria ▼] [New Lorebook] │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Fantasy World - Aldoria                                 │  │
│ │ A high-fantasy medieval setting with magic and kingdoms │  │
│ │ ☑ Enabled                                               │  │
│ │                                                          │  │
│ │ [Export This Lorebook] [Delete This Lorebook]           │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ All Lorebooks:                                               │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ ● Enabled - Fantasy World - Aldoria: 5 entries  [Select]│  │
│ │   A high-fantasy medieval setting with magic...         │  │
│ ├────────────────────────────────────────────────────────┤  │
│ │ ● Enabled - Murder Drones Lore: 4 entries       [Select]│  │
│ │   Lore and world-building for Murder Drones...          │  │
│ └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2. Creating a New Lorebook

Click "New Lorebook" and you'll see:

```
┌─────────────────────────────────────────────────────────────┐
│ Create New Lorebook                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Lorebook Name                                                │
│ ┌──────────────────────────────────────────────────────┐    │
│ │ e.g., Fantasy World, Sci-Fi Setting                  │    │
│ └──────────────────────────────────────────────────────┘    │
│                                                              │
│ Description (optional)                                       │
│ ┌──────────────────────────────────────────────────────┐    │
│ │ Brief description of this lorebook                   │    │
│ └──────────────────────────────────────────────────────┘    │
│                                                              │
│ [Create] [Cancel]                                            │
└─────────────────────────────────────────────────────────────┘
```

### 3. Adding Entries to Selected Lorebook

```
┌─────────────────────────────────────────────────────────────┐
│ Add/Edit Entry                                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Entry Key (Unique identifier)                                │
│ ┌──────────────────────────────────────────────────────┐    │
│ │ e.g., Kingdom of Aldoria, Magic System               │    │
│ └──────────────────────────────────────────────────────┘    │
│                                                              │
│ Content (Lore information)                                   │
│ ┌──────────────────────────────────────────────────────┐    │
│ │ Describe the lore, world details, or information...  │    │
│ │                                                      │    │
│ │                                                      │    │
│ └──────────────────────────────────────────────────────┘    │
│                                                              │
│ Keywords (comma-separated, optional)                         │
│ ┌──────────────────────────────────────────────────────┐    │
│ │ e.g., kingdom, aldoria, magic                        │    │
│ └──────────────────────────────────────────────────────┘    │
│ Entry will appear when any keyword is mentioned             │
│                                                              │
│ ☐ Always Active (Include in all conversations)              │
│                                                              │
│ [Save Entry] [Clear Form] [Export All] [Import]             │
└─────────────────────────────────────────────────────────────┘
```

### 4. Viewing Entries in Current Lorebook

```
┌─────────────────────────────────────────────────────────────┐
│ Lorebook Entries                                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Magic System                                    [Edit] [Delete]
│ │ ● Always Active | Keywords: magic, spell, mana         │  │
│ │ Magic in this world requires mana crystals, which are  │  │
│ │ rare and valuable. Only those born with the Gift...    │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Kingdom of Aldoria                              [Edit] [Delete]
│ │ Keywords: aldoria, kingdom, king, capital              │  │
│ │ The largest and most prosperous kingdom in the realm,  │  │
│ │ ruled by King Aldric the Wise. The capital city...     │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ The Dark Forest                                 [Edit] [Delete]
│ │ Keywords: forest, dark, north, monsters, shadow        │  │
│ │ A dangerous forest on the northern border where few... │  │
│ └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 5. Import Dialog

Click "Import" to see:

```
┌─────────────────────────────────────────────────────────────┐
│ Import Lorebook (JSON)                                       │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────┐    │
│ │ {                                                    │    │
│ │   "name": "My Lorebook",                            │    │
│ │   "description": "...",                              │    │
│ │   "enabled": true,                                   │    │
│ │   "entries": { ... }                                 │    │
│ │ }                                                     │    │
│ └──────────────────────────────────────────────────────┘    │
│                                                              │
│ ☑ Merge with existing entries (uncheck to replace all)      │
│                                                              │
│ [Import] [Cancel]                                            │
└─────────────────────────────────────────────────────────────┘
```

## Workflow Examples

### Example 1: Switching Between Settings

**Scenario**: You have both fantasy and sci-fi lorebooks

1. Select "Fantasy World - Aldoria" from dropdown
2. See 5 fantasy entries (magic, kingdoms, etc.)
3. Add new fantasy entry or edit existing
4. Select "Murder Drones Lore" from dropdown
5. See 4 sci-fi entries (planets, drones, etc.)
6. Work with sci-fi entries

### Example 2: Temporarily Disable a Lorebook

**Scenario**: You want to pause using sci-fi lore

1. Select "Murder Drones Lore"
2. Uncheck "Enabled" checkbox
3. Lorebook status changes to "✗ Disabled"
4. Sci-fi entries won't appear in AI responses
5. Check "Enabled" again to reactivate

### Example 3: Export and Share

**Scenario**: Share your fantasy world with a friend

1. Select "Fantasy World - Aldoria"
2. Click "Export This Lorebook"
3. File downloads as "Fantasy World - Aldoria.json"
4. Send file to friend
5. Friend clicks "Import" and pastes contents
6. Friend now has identical lorebook

### Example 4: Import Sample Lorebook

**Scenario**: Import the included Murder Drones example

1. Open `lorebook/murder_drones_lore.json` in text editor
2. Copy entire contents
3. Click "Import" in web UI
4. Paste JSON into dialog
5. Check "Merge with existing"
6. Click "Import"
7. "Murder Drones Lore" appears in lorebook list

## Color Coding

- **Green (● Enabled)**: Lorebook is active, entries will be used
- **Red (✗ Disabled)**: Lorebook is inactive, entries won't be used
- **Green Dot (●)**: "Always Active" entry, always included
- **No Dot**: Keyword-triggered entry

## Status Indicators

Each lorebook shows:
- Name
- Description
- Status (Enabled/Disabled) with color
- Entry count
- Quick actions (Select, Export, Delete)

Each entry shows:
- Entry key (name)
- Always Active status if applicable
- Keywords if defined
- Content preview (truncated)
- Edit and Delete buttons

## Benefits Visualized

```
Before (Single Lorebook):
┌─────────────────────┐
│ All entries mixed   │
│ - Fantasy entry 1   │
│ - Sci-fi entry 1    │
│ - Fantasy entry 2   │
│ - Sci-fi entry 2    │
│ Can't organize!     │
└─────────────────────┘

After (Multiple Lorebooks):
┌─────────────────────┐  ┌─────────────────────┐
│ Fantasy Lorebook    │  │ Sci-Fi Lorebook     │
│ ● Enabled           │  │ ✗ Disabled          │
│ - Fantasy entry 1   │  │ - Sci-fi entry 1    │
│ - Fantasy entry 2   │  │ - Sci-fi entry 2    │
│ - Fantasy entry 3   │  │ - Sci-fi entry 3    │
│                     │  │                     │
│ Clean & Organized!  │  │ Toggle anytime!     │
└─────────────────────┘  └─────────────────────┘
```

## Quick Reference

**To create a lorebook**: New Lorebook button
**To switch lorebooks**: Use dropdown selector
**To enable/disable**: Toggle checkbox
**To export**: Select lorebook → Export This Lorebook
**To import**: Import button → Paste JSON
**To delete**: Select lorebook → Delete This Lorebook
**To add entry**: Select lorebook → Fill form → Save Entry

This visual guide shows how the web interface makes managing multiple lorebooks intuitive and user-friendly!
