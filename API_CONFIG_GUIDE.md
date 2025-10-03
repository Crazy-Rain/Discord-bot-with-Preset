# API Configuration Save/Load Feature Guide

## Overview

The API Configuration Save/Load feature allows you to save and manage multiple API configurations for quick switching between different proxies, models, and API providers.

## Key Features

- **Save Multiple Configurations**: Store unlimited API configurations with custom names
- **Quick Switching**: Switch between configurations with a single click
- **Security**: API keys are hidden in the dropdown and list views for security
- **Separate Management**: API configurations are stored separately from Discord Bot Token and other settings

## How to Use

### Saving a Configuration

1. Navigate to the **Configuration** tab in the web interface
2. Under "OpenAI API Configuration", fill in:
   - **API Key**: Your OpenAI-compatible API key
   - **Base URL**: The API endpoint URL (e.g., `https://api.openai.com/v1`)
   - **Model**: The model name (e.g., `gpt-4`, `llama2`)
3. Scroll down to "Saved API Configurations"
4. Enter a **Configuration Name** (e.g., "OpenAI GPT-4", "Local Ollama", "Claude via Proxy")
5. Click **Save API Config**
6. Your configuration is now saved!

### Loading a Configuration

#### Method 1: Using the Dropdown
1. Select a configuration from the **Saved Configurations** dropdown
2. Click **Load Selected**
3. The API Key, Base URL, and Model fields will be populated

#### Method 2: Using the List
1. Find your configuration in the **Available API Configurations** list
2. Click the **Load** button next to it
3. The API Key, Base URL, and Model fields will be populated

### Deleting a Configuration

#### Method 1: Using the Dropdown
1. Select a configuration from the **Saved Configurations** dropdown
2. Click **Delete Selected**
3. Confirm the deletion

#### Method 2: Using the List
1. Find your configuration in the **Available API Configurations** list
2. Click the **Delete** button next to it
3. Confirm the deletion

## Use Cases

### Example 1: Multiple API Providers
Save different configurations for:
- "OpenAI GPT-4" → OpenAI's API
- "Anthropic Claude" → Anthropic's API via proxy
- "Local LLaMA" → Local Ollama instance

### Example 2: Different Models from Same Provider
Save configurations for different models:
- "OpenAI GPT-4" → `gpt-4` model
- "OpenAI GPT-3.5" → `gpt-3.5-turbo` model
- "OpenAI GPT-4 Turbo" → `gpt-4-turbo-preview` model

### Example 3: Development vs Production
Separate configurations for different environments:
- "Production API" → Live API with production credentials
- "Development API" → Test API with development credentials
- "Local Testing" → Local test server

## Security Notes

- **API keys are hidden** in the dropdown list (shown as "Base URL - Model Name")
- **API keys are hidden** in the configuration list (shown as `***HIDDEN***`)
- **API keys are revealed** only when loading a configuration into the input fields
- **API keys are stored** in the `config.json` file (ensure this file is in `.gitignore`)

## Configuration Storage

Saved API configurations are stored in `config.json` under the `saved_api_configs` key:

```json
{
  "saved_api_configs": {
    "OpenAI GPT-4": {
      "api_key": "sk-...",
      "base_url": "https://api.openai.com/v1",
      "model": "gpt-4"
    },
    "Local Ollama": {
      "api_key": "ollama",
      "base_url": "http://localhost:11434/v1",
      "model": "llama2"
    }
  }
}
```

## Tips

1. **Descriptive Names**: Use clear, descriptive names for your configurations
2. **Keep It Organized**: Delete unused configurations to keep your list clean
3. **Backup**: Back up your `config.json` file to save your configurations
4. **Testing**: Save a test configuration before using it with the bot

## Workflow Example

1. **Initial Setup**:
   - Save your primary API configuration (e.g., "OpenAI GPT-4")
   - Save a backup configuration (e.g., "OpenAI GPT-3.5")

2. **Daily Use**:
   - Load your primary configuration when starting the bot
   - Switch to backup if you hit rate limits

3. **Experimentation**:
   - Save a new configuration for testing (e.g., "Local Testing")
   - Load it without affecting your primary setup
   - Delete when done testing

## Troubleshooting

**Q: My saved configuration isn't loading**
- A: Make sure you clicked "Load Selected" after choosing from the dropdown

**Q: I don't see my saved configurations**
- A: Refresh the page or click the "Reload" button

**Q: Can I edit a saved configuration?**
- A: Yes, load it, modify the fields, and save it again with the same name

**Q: Where are my configurations stored?**
- A: They're stored in `config.json` in the root directory of the bot

**Q: Are my API keys secure?**
- A: API keys are hidden in the UI for display purposes, but they're stored in plain text in `config.json`. Keep this file secure and don't commit it to public repositories.
