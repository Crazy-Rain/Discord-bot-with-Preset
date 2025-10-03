# Multi-Section Prompt Manager

## Overview

The preset system now supports SillyTavern-style multi-section prompts, allowing you to build complex prompts with multiple sections, each with a different role (System, User, or Assistant).

## Features

### 1. Multiple Prompt Sections
- Create as many prompt sections as needed
- Each section can have a different role:
  - **System**: Instructions and guidelines for the AI
  - **User**: Example user messages
  - **Assistant**: Example AI responses

### 2. Dynamic Section Management
- **Add Section**: Click "+ Add Section" button to create new sections
- **Delete Section**: Each section has a "Delete" button
- **Reorder Sections**: Use ▲▼ arrow buttons to move sections up or down
- Sections are processed in order from top to bottom

### 3. Role Assignment
- Each section has a dropdown to select its role
- Textarea placeholder updates to match selected role
- Sections can be any combination of roles

## Data Structure

### New Format (prompt_sections)
```json
{
  "prompt_sections": [
    {
      "id": "prompt-section-0",
      "role": "system",
      "content": "You are a helpful AI assistant",
      "order": 0,
      "enabled": true
    },
    {
      "id": "prompt-section-1",
      "role": "user",
      "content": "Example user message",
      "order": 1,
      "enabled": true
    },
    {
      "id": "prompt-section-2",
      "role": "assistant",
      "content": "Example assistant response",
      "order": 2,
      "enabled": true
    }
  ],
  "temperature": 0.7,
  ...
}
```

### Old Format (system_prompt) - Still Supported
```json
{
  "system_prompt": "You are a helpful AI assistant",
  "temperature": 0.7,
  ...
}
```

## Backward Compatibility

The system maintains full backward compatibility:

1. **Loading Old Presets**: Presets with only `system_prompt` are automatically converted to a single system section
2. **Saving New Presets**: New presets save as `prompt_sections` array
3. **Migration**: No manual migration needed - old presets work as-is

## How It Works

### Frontend (UI)
1. Preset form replaced single textarea with dynamic sections container
2. JavaScript functions manage adding/removing/reordering sections
3. `getPromptSections()` collects all sections into array when saving
4. `loadPromptSections()` populates UI from array when loading

### Backend (Message Building)
1. `build_chat_messages()` checks for `prompt_sections` in preset
2. If found, processes sections in order by `order` field
3. System sections get enhanced with character info, lorebook, etc.
4. User and Assistant sections are added as-is
5. If no `prompt_sections`, falls back to old `system_prompt` logic

## Use Cases

### 1. Few-Shot Learning
```json
{
  "prompt_sections": [
    {"role": "system", "content": "You are a helpful math tutor", "order": 0},
    {"role": "user", "content": "What is 2+2?", "order": 1},
    {"role": "assistant", "content": "2+2 equals 4", "order": 2},
    {"role": "user", "content": "What is 3+3?", "order": 3},
    {"role": "assistant", "content": "3+3 equals 6", "order": 4}
  ]
}
```

### 2. Character Voice Examples
```json
{
  "prompt_sections": [
    {"role": "system", "content": "You are a pirate captain", "order": 0},
    {"role": "user", "content": "What's your name?", "order": 1},
    {"role": "assistant", "content": "*adjusts tricorn hat* Arrr, they call me Captain Blackbeard!", "order": 2}
  ]
}
```

### 3. Complex Instructions
```json
{
  "prompt_sections": [
    {"role": "system", "content": "Primary instruction: Write creative stories", "order": 0},
    {"role": "system", "content": "Style guide: Use vivid imagery and metaphors", "order": 1},
    {"role": "system", "content": "Constraints: Keep responses under 200 words", "order": 2}
  ]
}
```

## Benefits

1. **Precise Control**: Define exact message sequence
2. **Role Separation**: Clear distinction between instructions and examples
3. **Better Learning**: AI learns from example exchanges
4. **SillyTavern Compatible**: Matches SillyTavern's prompt manager design
5. **Flexible**: Mix and match roles as needed

## Migration from Old Presets

No action needed! Old presets automatically convert when loaded:
- Single `system_prompt` → Single system section
- All other fields preserved
- Save to upgrade to new format
