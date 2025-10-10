# OpenAI-Compatible Proxy Guide

## Overview

This Discord bot supports any OpenAI-compatible API proxy or endpoint. This guide explains how to configure and use different proxies effectively.

## Supported Proxy Types

The bot works with any OpenAI-compatible proxy that follows the OpenAI API format. Common examples include:

- **OpenAI Direct**: `https://api.openai.com/v1`
- **Anas Proxy**: `https://anas-proxy.xyz/v1`
- **Local Ollama**: `http://localhost:11434/v1`
- **Claude via Proxy**: Various proxy services
- **Custom Proxies**: Any service implementing OpenAI API format

## Configuration

### Via Web Interface (Recommended)

1. Open the web interface at `http://localhost:5000`
2. Go to the **Configuration** tab
3. Under "OpenAI API Configuration", enter:
   - **API Key**: Your proxy's authentication token/key
   - **Base URL**: The proxy's API endpoint
   - **Model**: The model name supported by your proxy
4. Click **Save Configuration**

### Via Config File

Edit `config.json`:

```json
{
  "openai_config": {
    "api_key": "your-proxy-api-key",
    "base_url": "https://your-proxy.com/v1",
    "model": "gpt-3.5-turbo"
  }
}
```

## Important Notes

### URL Formatting

- **Always include the API path** (usually `/v1`)
  - ✅ Correct: `https://anas-proxy.xyz/v1`
  - ❌ Wrong: `https://anas-proxy.xyz`

- **Trailing slashes are optional** - the bot handles both:
  - ✅ `https://api.openai.com/v1`
  - ✅ `https://api.openai.com/v1/`

- **Whitespace is automatically removed**:
  - Input: ` https://proxy.com/v1 `
  - Stored: `https://proxy.com/v1`

### API Keys

- **Whitespace is automatically stripped**:
  - Input: ` sk-key-123 `
  - Stored: `sk-key-123`

- **Proxy-specific keys**: Each proxy has its own authentication:
  - OpenAI uses keys like `sk-...`
  - Other proxies may use different formats
  - Use the exact key provided by your proxy service

### Model Names

- **Must match your proxy's available models**
- Some proxies support OpenAI model names: `gpt-3.5-turbo`, `gpt-4`
- Others use custom names: `llama2`, `claude-2`, etc.
- Use the **Fetch Models** button in the web interface to see available models

## Common Proxy Configurations

### OpenAI (Direct)

```json
{
  "api_key": "sk-...",
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-3.5-turbo"
}
```

### Anas Proxy

```json
{
  "api_key": "your-anas-token",
  "base_url": "https://anas-proxy.xyz/v1",
  "model": "gpt-3.5-turbo"
}
```

### Local Ollama

```json
{
  "api_key": "ollama",
  "base_url": "http://localhost:11434/v1",
  "model": "llama2"
}
```

### Custom Proxy

```json
{
  "api_key": "your-custom-key",
  "base_url": "https://custom-proxy.com/api/v1",
  "model": "custom-model-name"
}
```

## Saving Multiple Proxy Configurations

You can save multiple proxy configurations and switch between them:

1. Configure your first proxy in the main settings
2. Scroll to "Saved API Configurations"
3. Enter a name (e.g., "OpenAI GPT-4")
4. Click **Save API Config**
5. Repeat for other proxies

To switch proxies:
1. Select from the dropdown
2. Click **Load Selected**
3. Click **Save Configuration**

## Per-Channel/Server Proxies

You can use different proxies for different Discord channels or servers:

1. Go to **Servers & Channels** tab
2. Find your server/channel
3. Select an API configuration from the dropdown
4. Click **Save**

Now that channel will use its own proxy while others use the default.

## Troubleshooting

### "Invalid Token" Error

**Cause**: Your API key is not valid for the proxy

**Solutions**:
1. Verify you're using the correct API key for that specific proxy
2. Check if the key has expired
3. Ensure there are no extra spaces (the bot strips them, but verify your source)
4. Test the same key in another client (e.g., SillyTavern, Postman)

### "API authentication failed"

**Cause**: Authentication issue with the proxy

**Solutions**:
1. Double-check the API key
2. Verify the base URL is correct (must include `/v1` or appropriate path)
3. Test the proxy directly with curl:
   ```bash
   curl -X POST https://your-proxy.com/v1/chat/completions \
     -H "Authorization: Bearer your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"test"}]}'
   ```

### Works in SillyTavern but not in Bot

**Possible causes**:
1. Different API keys being used
2. Different base URLs (check for trailing slashes, /v1 suffix)
3. Model name differences

**Solution**:
1. Open both configurations side-by-side
2. Copy the exact values from SillyTavern to the bot
3. Use the **Load** feature if you previously saved a working config

### Connection Refused / Timeout

**Cause**: Proxy is not accessible

**Solutions**:
1. Check if the proxy service is online
2. For local proxies (Ollama), ensure the service is running
3. Verify firewall settings
4. Check network connectivity

### Invalid Model Name

**Cause**: Model not supported by your proxy

**Solutions**:
1. Click **Fetch Models** button to see available models
2. Use a model from the list
3. Check your proxy's documentation

## Best Practices

1. **Test First**: Use the **Fetch Models** button to verify your proxy works before chatting
2. **Save Configs**: Save working configurations so you can easily restore them
3. **Use Descriptive Names**: Name saved configs clearly (e.g., "Anas-GPT4", "Local-Llama")
4. **Keep Backups**: Back up your `config.json` file
5. **Monitor Logs**: Check the bot console for detailed error messages

## Advanced Configuration

### Custom Headers

If your proxy requires custom headers, you may need to modify `openai_client.py`. The OpenAI Python library supports custom headers:

```python
client = OpenAI(
    api_key="your-key",
    base_url="https://your-proxy.com/v1",
    default_headers={"Custom-Header": "value"}
)
```

### Timeout Settings

To adjust API timeout, modify the OpenAI client initialization:

```python
client = OpenAI(
    api_key="your-key",
    base_url="https://your-proxy.com/v1",
    timeout=60.0  # seconds
)
```

### Retry Logic

The OpenAI library has built-in retry logic. To customize:

```python
from openai import OpenAI
import httpx

client = OpenAI(
    api_key="your-key",
    base_url="https://your-proxy.com/v1",
    max_retries=3
)
```

## Proxy Compatibility Checklist

When setting up a new proxy:

- [ ] Proxy supports OpenAI-compatible API format
- [ ] You have a valid API key/token
- [ ] Base URL includes the API path (e.g., `/v1`)
- [ ] You know the supported model names
- [ ] Proxy is accessible from your network
- [ ] API key has appropriate permissions

## Getting Help

If you're having trouble with a specific proxy:

1. Check the proxy's documentation
2. Test with curl or Postman first
3. Compare with a working SillyTavern configuration
4. Check the bot console for detailed error messages
5. Verify all settings are correct (no typos, correct URL format)

## Examples of Error Messages and Solutions

### Error: "API key is not configured"
- **Solution**: Enter a valid API key (not "YOUR_API_KEY" or empty)

### Error: "Failed to fetch models: 401"
- **Solution**: API key is invalid for this proxy

### Error: "Failed to fetch models: 404"
- **Solution**: Base URL is incorrect (likely missing `/v1`)

### Error: "Connection refused"
- **Solution**: Proxy is not running or not accessible

### Error: "Invalid response structure"
- **Solution**: Proxy is not OpenAI-compatible or has issues
