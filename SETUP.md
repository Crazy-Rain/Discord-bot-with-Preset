# Setup Instructions

## Step-by-Step Setup Guide

### 1. Get a Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under "Token", click "Reset Token" and copy it
6. Enable these Privileged Gateway Intents:
   - MESSAGE CONTENT INTENT (required for reading messages)
   - SERVER MEMBERS INTENT (optional)

### 2. Invite Bot to Your Server

1. Go to "OAuth2" > "URL Generator"
2. Select scopes:
   - `bot`
   - `applications.commands`
3. Select bot permissions:
   - Read Messages/View Channels
   - Send Messages
   - Read Message History
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

### 3. Get OpenAI API Key (or alternative)

#### Option A: OpenAI
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Go to API Keys section
4. Create new API key and copy it

#### Option B: Local LLM (LM Studio)
1. Download [LM Studio](https://lmstudio.ai/)
2. Download a model (e.g., Mistral, Llama 2)
3. Start the local server (default: `http://localhost:1234/v1`)
4. Use any string as API key (not validated locally)

#### Option C: Other OpenAI-Compatible APIs
- Ollama with compatibility layer
- Text Generation WebUI
- KoboldAI
- Any other compatible endpoint

### 4. Configure the Bot

1. Copy `config.example.json` to `config.json`:
   ```bash
   cp config.example.json config.json
   ```

2. Edit `config.json` with your details:
   ```json
   {
     "discord_token": "YOUR_DISCORD_BOT_TOKEN_HERE",
     "openai_config": {
       "api_key": "YOUR_API_KEY_HERE",
       "base_url": "https://api.openai.com/v1",
       "model": "gpt-3.5-turbo"
     }
   }
   ```

   For LM Studio:
   ```json
   {
     "discord_token": "YOUR_DISCORD_BOT_TOKEN_HERE",
     "openai_config": {
       "api_key": "lm-studio",
       "base_url": "http://localhost:1234/v1",
       "model": "local-model"
     }
   }
   ```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Bot

```bash
python main.py
```

The bot will:
- Start the web configuration interface on `http://localhost:5000`
- Connect to Discord with your bot token
- Be ready to receive commands!

### 7. Test the Bot

In your Discord server:
```
!help_bot
!chat Hello, how are you?
!presets
!preset creative
!characters
!character sherlock
```

### 8. Configure via Web Interface

1. Open `http://localhost:5000` in your browser
2. Navigate through tabs:
   - **Configuration**: Edit bot and API settings
   - **Presets**: Create and manage conversation presets
   - **Characters**: Create and manage character cards

## Troubleshooting

### "Error: Discord token not configured!"
- Make sure you copied `config.example.json` to `config.json`
- Ensure your Discord token is correctly set in `config.json`
- Token should not have quotes or extra spaces

### "Error calling OpenAI API"
- Check your API key is valid
- Verify the base URL is correct and accessible
- Ensure the model name exists on your endpoint
- For local LLMs, make sure the server is running

### Bot doesn't respond to commands
- Ensure bot has "Read Messages" and "Send Messages" permissions
- Make sure MESSAGE CONTENT INTENT is enabled in Discord Developer Portal
- Check the bot is online (green status) in Discord

### Web interface won't load
- Check if port 5000 is already in use
- Try a different port by editing `web_server.port` in `config.json`
- Verify firewall isn't blocking the port

## Advanced Configuration

### Using Environment Variables

You can also use environment variables instead of `config.json`:

```bash
export DISCORD_TOKEN="your_token_here"
export OPENAI_API_KEY="your_key_here"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-3.5-turbo"
```

### Running in Production

For production deployment:

1. Use a process manager like `systemd`, `supervisor`, or `pm2`
2. Set up proper logging
3. Use environment variables for sensitive data
4. Configure reverse proxy (nginx) for web interface
5. Enable HTTPS for security

### Docker Deployment (Future)

A Dockerfile will be provided in future updates for easier deployment.
