# SillyTavern Preset UI Fix

## Issue
SillyTavern presets could not be properly imported into the Bot Config Page because the web UI was missing form fields for SillyTavern-specific options.

## Root Cause
The HTML template (`templates/index.html`) had form fields for basic preset options (temperature, max_tokens, etc.) but was missing the 4 SillyTavern-specific fields:

1. `prompt_format` - Controls message formatting style
2. `character_position` - Where to inject character info
3. `include_examples` - Whether to include example dialogues
4. `example_separator` - Separator for parsing examples

## Solution
Added a new "SillyTavern Options" section to the preset form with all 4 missing fields.

## Changes Made

### 1. Added HTML Form Fields
```html
<h3>SillyTavern Options</h3>
<p>Optional settings for SillyTavern-style character card integration and prompt formatting.</p>

<!-- Prompt Format dropdown -->
<select id="preset-prompt-format">
    <option value="default">Default</option>
    <option value="sillytavern">SillyTavern</option>
</select>

<!-- Character Position dropdown -->
<select id="preset-character-position">
    <option value="system">System Message</option>
    <option value="examples">Example Dialogues</option>
    <option value="both">Both</option>
</select>

<!-- Include Examples checkbox -->
<input type="checkbox" id="preset-include-examples" checked>

<!-- Example Separator text input -->
<input type="text" id="preset-example-separator" value="<START>">
```

### 2. Updated savePreset() JavaScript Function
```javascript
const preset = {
    // ... existing fields ...
    prompt_format: document.getElementById('preset-prompt-format').value,
    character_position: document.getElementById('preset-character-position').value,
    include_examples: document.getElementById('preset-include-examples').checked,
    example_separator: document.getElementById('preset-example-separator').value
};
```

### 3. Updated selectPreset() JavaScript Function
```javascript
document.getElementById('preset-prompt-format').value = preset.prompt_format || 'default';
document.getElementById('preset-character-position').value = preset.character_position || 'system';
document.getElementById('preset-include-examples').checked = preset.include_examples !== false;
document.getElementById('preset-example-separator').value = preset.example_separator || '<START>';
```

## Testing

### Test 1: Load Existing SillyTavern Preset
✅ Loaded `sillytavern_style.json` preset
✅ All fields populated correctly:
- Prompt Format: "SillyTavern"
- Character Position: "Both"
- Include Examples: ✓ checked
- Example Separator: "<START>"

### Test 2: Import SillyTavern Preset via JSON
✅ Imported preset with SillyTavern fields:
```json
{
  "temperature": 0.9,
  "prompt_format": "sillytavern",
  "character_position": "examples",
  "include_examples": true,
  "example_separator": "***"
}
```
✅ Preset saved correctly to file
✅ All fields loaded properly when preset selected

### Test 3: Backward Compatibility
✅ Old presets without SillyTavern fields still work
✅ Default values applied when fields missing
✅ No breaking changes to existing functionality

## Field Descriptions

### Prompt Format
- **Default**: Standard message formatting
- **SillyTavern**: Proper role separation for character cards
- Use "SillyTavern" for optimal character roleplay

### Character Position
- **System Message**: Character info in system message only
- **Example Dialogues**: Character info in examples only
- **Both**: Character info in both locations
- "Both" recommended for best character consistency

### Include Example Dialogues
- When checked: Includes `first_mes` and `mes_example` from character cards
- When unchecked: Only uses character description
- Should be checked for full SillyTavern compatibility

### Example Separator
- Default: `<START>`
- Used to split dialogue examples in character card's `mes_example` field
- Change if your character cards use different separator

## Benefits

1. **Full SillyTavern Compatibility**: Users can now import SillyTavern presets and see all fields
2. **Visual Editing**: All preset options visible and editable in the web UI
3. **Better Documentation**: Field descriptions help users understand options
4. **No Breaking Changes**: Fully backward compatible with existing presets

## Screenshots

![SillyTavern Options in Preset Form](https://github.com/user-attachments/assets/7d68c8ef-823f-4c53-94f0-75bfbb2228ee)

## Related Documentation
- [SILLYTAVERN_PRESETS_GUIDE.md](SILLYTAVERN_PRESETS_GUIDE.md) - Full guide to SillyTavern presets
- [MESSAGE_STRUCTURE_COMPARISON.md](MESSAGE_STRUCTURE_COMPARISON.md) - Message structure details
- [IMPLEMENTATION_SUMMARY_SILLYTAVERN.md](IMPLEMENTATION_SUMMARY_SILLYTAVERN.md) - Implementation overview
