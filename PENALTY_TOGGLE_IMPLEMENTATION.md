# Penalty Toggle Implementation

## Overview
Added enable/disable toggle checkboxes for Frequency Penalty and Presence Penalty parameters to address compatibility issues with models that don't support these parameters (e.g., Google's Gemini 2.5).

## Problem Statement
Google's Gemini 2.5 and some other models don't support frequency_penalty and presence_penalty parameters. When these parameters are sent in API requests, the models throw errors like "Penalty is not enabled for models/gemini-pro-latest".

## Solution
Added checkbox toggles that allow users to enable or disable each penalty parameter independently. When disabled, the penalties are not included in the API request, preventing compatibility errors.

## Changes Made

### 1. UI Changes (templates/index.html)

#### Configuration Tab - Default Preset Section
- Added checkbox for Frequency Penalty with explanatory text
- Added checkbox for Presence Penalty with explanatory text
- Both checkboxes are checked by default (backward compatible)

#### Presets Tab
- Added checkbox for Frequency Penalty with explanatory text
- Added checkbox for Presence Penalty with explanatory text  
- Both checkboxes are checked by default (backward compatible)

#### JavaScript Functions Updated
- **saveConfig()**: Now saves `frequency_penalty_enabled` and `presence_penalty_enabled` flags
- **loadConfig()**: Now loads and sets checkbox states, defaults to `true` if not present
- **savePreset()**: Now saves `frequency_penalty_enabled` and `presence_penalty_enabled` flags
- **selectPreset()**: Now loads and sets checkbox states, defaults to `true` if not present

### 2. Backend Changes (openai_client.py)

#### Modified chat_completion() Method
- Added optional parameters: `frequency_penalty_enabled` and `presence_penalty_enabled`
- Both default to `True` for backward compatibility
- Builds request parameters dynamically - only includes penalties if their corresponding enabled flag is `True`

```python
# Only include penalties if they are enabled
if frequency_penalty_enabled:
    request_params["frequency_penalty"] = frequency_penalty
if presence_penalty_enabled:
    request_params["presence_penalty"] = presence_penalty
```

### 3. Discord Bot Changes (discord_bot.py)

Updated all three calls to `chat_completion()` to pass the enabled states from the preset:
- Swipe functionality (line ~217)
- Regular chat command (line ~1017)
- Edit functionality (line ~1621)

Each call now includes:
```python
frequency_penalty_enabled=preset.get("frequency_penalty_enabled", True),
presence_penalty_enabled=preset.get("presence_penalty_enabled", True)
```

## Backward Compatibility

- Default value for both enabled flags is `True`
- Existing presets without these flags will work normally (penalties will be sent)
- The `.get("frequency_penalty_enabled", True)` pattern ensures old configurations continue to work

## Usage

### For Users
1. When using models that don't support penalties (like Gemini):
   - Uncheck the "Frequency Penalty" checkbox
   - Uncheck the "Presence Penalty" checkbox
   - Save the configuration or preset

2. When using models that support penalties (like GPT models):
   - Keep both checkboxes checked
   - Adjust the slider values as needed
   - Save the configuration or preset

### Testing
The implementation has been tested to ensure:
- ✓ Checkboxes appear in both Configuration and Presets tabs
- ✓ Checkbox states are saved correctly
- ✓ Checkbox states are loaded correctly
- ✓ Penalties are excluded from API requests when disabled
- ✓ Backward compatibility with existing configurations

## Screenshots

### Configuration Tab
![Configuration Tab with Penalty Toggles](https://github.com/user-attachments/assets/74f9f9c1-46f7-44a9-a948-73c39e1a63ee)

### Presets Tab
![Presets Tab with Penalty Toggles](https://github.com/user-attachments/assets/4bc4285e-9efa-47cc-b3df-9ca1e3d08f5e)

## Files Modified
1. `templates/index.html` - Added checkboxes and updated JavaScript functions
2. `openai_client.py` - Modified chat_completion() to conditionally include penalties
3. `discord_bot.py` - Updated all chat_completion() calls to pass enabled states

## Benefits
- ✅ Prevents API errors when using models that don't support penalties
- ✅ Maintains full functionality for models that do support penalties
- ✅ User-friendly toggle interface with explanatory text
- ✅ Fully backward compatible with existing configurations
- ✅ Works consistently across Configuration and Presets tabs
