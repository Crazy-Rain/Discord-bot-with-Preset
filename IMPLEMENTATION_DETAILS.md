# Multiple Lorebooks Feature - Implementation Summary

## Problem Statement

The user wanted to:
1. Use multiple lorebooks
2. Swap between lorebooks
3. Enable/disable individual lorebooks

Example provided: `@murder_drones_lore.json` as a reference for lorebook structure.

## Solution Implemented

### Architecture

The implementation adds a hierarchical structure while maintaining backward compatibility:

```
Old Structure:
lorebook/
  └── lorebook.json          # Flat dict of all entries

New Structure:
lorebook/
  ├── lorebooks.json         # Dict of lorebook collections (NEW)
  ├── lorebook.json          # Legacy flat format (auto-synced)
  ├── *.json                 # Sample lorebook files
  └── README.md              # Documentation
```

### Data Model

Each lorebook collection contains:
```python
{
  "name": str,              # Unique name
  "description": str,       # Optional description
  "enabled": bool,          # Toggle on/off
  "entries": {              # Dict of entries
    "Entry Key": {
      "key": str,
      "content": str,
      "keywords": List[str],
      "always_active": bool
    }
  }
}
```

### Backend Changes (lorebook_manager.py)

**New Attributes:**
- `self.lorebooks`: Dict storing all lorebook collections
- `self.entries`: Maintained for backward compatibility (auto-synced from enabled lorebooks)

**New Methods:**
- `create_lorebook(name, description, enabled)` - Create new lorebook
- `delete_lorebook(name)` - Delete lorebook
- `list_lorebooks()` - List all lorebooks with metadata
- `get_lorebook(name)` - Get specific lorebook
- `update_lorebook_metadata(name, description, enabled)` - Update metadata
- `enable_lorebook(name)` - Enable a lorebook
- `disable_lorebook(name)` - Disable a lorebook
- `import_lorebook_file(data, merge)` - Import structured lorebook
- `export_lorebook_file(name)` - Export specific lorebook

**Updated Methods:**
- `add_or_update_entry()` - Now accepts `lorebook_name` parameter
- `get_entry()` - Can search in specific lorebook or all enabled
- `delete_entry()` - Can delete from specific lorebook or all
- `save_all_lorebooks()` - Saves to both new and legacy formats

### API Changes (web_server.py)

**New Endpoints:**
- `GET /api/lorebooks` - List all lorebooks
- `POST /api/lorebooks` - Create new lorebook
- `GET /api/lorebooks/<name>` - Get specific lorebook
- `POST /api/lorebooks/<name>` - Update lorebook metadata
- `DELETE /api/lorebooks/<name>` - Delete lorebook
- `GET /api/lorebooks/<name>/export` - Export lorebook as JSON
- `POST /api/lorebooks/<name>/toggle` - Quick enable/disable

**Updated Endpoints:**
- `POST /api/lorebook/<key>` - Now accepts `lorebook_name` in request body
- `POST /api/lorebook/import` - Handles both old and new formats

### UI Changes (templates/index.html)

**New Components:**
1. **Lorebook Selector** - Dropdown to select active lorebook
2. **Lorebook Management Section**:
   - Shows all lorebooks with status
   - Enable/disable toggle for current lorebook
   - Export/delete buttons for current lorebook
3. **Create Lorebook Dialog** - Form to create new lorebooks
4. **Enhanced Import** - Detects format automatically

**JavaScript Functions Added:**
- `loadLorebooksList()` - Load and display all lorebooks
- `onLorebookSelected()` - Handle lorebook selection
- `loadLorebookEntriesForCurrent()` - Load entries for selected lorebook
- `selectLorebook(name)` - Select lorebook programmatically
- `toggleCurrentLorebook()` - Toggle enabled status
- `showCreateLorebookDialog()` - Show create dialog
- `createLorebook()` - Create new lorebook
- `exportCurrentLorebook()` - Export selected lorebook
- `deleteCurrentLorebook()` - Delete selected lorebook

**Updated Functions:**
- `loadLorebookList()` - Now loads lorebooks first, then entries
- `saveLorebookEntry()` - Requires lorebook selection
- `editLorebookEntry()` - Loads from selected lorebook
- `deleteLorebookEntry()` - Deletes from selected lorebook
- `importLorebook()` - Handles both formats

### Sample Files

Two example lorebooks included:

1. **fantasy_aldoria.json** - Fantasy setting
   - Magic System, Kingdom of Aldoria, The Dark Forest, Mage Knights, The Great War
   
2. **murder_drones_lore.json** - Sci-fi setting
   - Copper-9, Worker Drones, Disassembly Drones, The Absolute Solver

### Documentation

**New Files:**
- `MULTIPLE_LOREBOOKS_GUIDE.md` - Quick start guide
- `lorebook/README.md` - Sample files documentation

**Updated Files:**
- `LOREBOOK_GUIDE.md` - Comprehensive documentation update
- `README.md` - Feature announcement

## Backward Compatibility

The implementation is fully backward compatible:

1. **Legacy Storage**: Old `lorebook.json` is auto-synced from enabled lorebooks
2. **Legacy Import**: Old format imports to "Default" lorebook
3. **Legacy API**: All old API endpoints still work
4. **Migration**: Existing entries auto-migrate to "Default" lorebook on first load

## Testing

All features tested and verified:
- ✅ Create/delete lorebooks
- ✅ Enable/disable lorebooks
- ✅ Import/export both formats
- ✅ Add/edit/delete entries
- ✅ Lorebook selection and switching
- ✅ Backward compatibility
- ✅ Sample file imports

## Usage Example

```python
from lorebook_manager import LorebookManager

lm = LorebookManager()

# Create lorebooks
lm.create_lorebook("Fantasy World", "High fantasy setting")
lm.create_lorebook("Sci-Fi", "Space opera setting")

# Add entries
lm.add_or_update_entry(
    "Magic System", 
    "Magic requires mana crystals...", 
    ["magic", "spell"],
    always_active=True,
    lorebook_name="Fantasy World"
)

# Toggle lorebooks
lm.disable_lorebook("Sci-Fi")  # Disable sci-fi lore
lm.enable_lorebook("Sci-Fi")   # Re-enable it

# Export/Import
json_str = lm.export_lorebook_file("Fantasy World")
# Share json_str with others
lm.import_lorebook_file(json.loads(json_str))
```

## Benefits

1. **Organization** - Separate lore by setting/campaign
2. **Flexibility** - Quick switching without data loss
3. **Sharing** - Export/import complete lorebook collections
4. **Compatibility** - Works with existing setups
5. **Scalability** - Manage unlimited lorebooks

## Files Changed

- `lorebook_manager.py` (+166 lines)
- `web_server.py` (+115 lines)
- `templates/index.html` (+318 lines)
- `LOREBOOK_GUIDE.md` (updated)
- `README.md` (updated)
- `MULTIPLE_LOREBOOKS_GUIDE.md` (new)
- `lorebook/README.md` (new)
- `lorebook/fantasy_aldoria.json` (new)
- `lorebook/murder_drones_lore.json` (new)

Total: ~600+ lines of new code, 4 new files, comprehensive documentation.
