# Usage Examples

## Basic Usage

### 1. Starting the Bot

```bash
python main.py
```

Output:
```
============================================================
Discord Bot with OpenAI Integration and Preset System
============================================================

🌐 Web configuration interface starting at http://localhost:5000
   Configure your bot settings, presets, and character cards through the web UI

🤖 Starting Discord bot...
Bot is ready! Logged in as YourBot#1234
```

### 2. Using Discord Commands

#### Chat with the AI
```
!chat Hello, how are you today?
```

Response:
```
Hello! I'm doing great, thank you for asking! I'm here and ready to help you with 
anything you need. How can I assist you today?
```

#### Load a Preset
```
!presets
```

Response:
```
Available presets: creative, analytical
```

```
!preset creative
```

Response:
```
Loaded preset: creative
```

#### Use Character Cards
```
!characters
```

Response:
```
Available characters: luna, sherlock
```

```
!character sherlock
```

Response:
```
Loaded character: sherlock
```

Now chat with Sherlock:
```
!chat I need help solving a mystery
```

Response (in character):
```
Ah, a mystery! Excellent. Tell me everything, and leave no detail out, no matter 
how trivial it may seem. Often, it's the smallest observations that crack the case. 
What precisely is the nature of this mystery?
```

#### Clear Conversation History
```
!clear
```

Response:
```
Conversation history and character names cleared!
```

#### Character Name Tracking (Roleplay)

You can roleplay by identifying yourself as a character using the format `CharacterName: message`.

**Formatting Guidelines:**
- Use `"quotes"` for spoken dialogue
- Use `*asterisks*` for actions
- Plain text for descriptions

Example conversation:
```
!chat Alice: "Hello! Is anyone here?"
```

Response:
```
Hello Alice! Yes, I'm here. How can I help you today?
```

```
!chat Bob: *walks in* "Hey Alice! I just arrived."
```

Response:
```
Welcome, Bob! I see you've just joined Alice. How are you both doing?
```

```
!chat Alice: *turns to Bob* "We're planning an adventure." She pulls out a map
```

Response:
```
Oh, an adventure! That sounds exciting! What kind of adventure are you two planning? 
I can see you have a map there - where are you headed?
```

The bot will track character names (Alice, Bob) and ensure it doesn't pretend to be them.

#### Generate Alternative Responses (Swipe)
```
!chat Tell me a creative story about a robot
```

Response:
```
Once upon a time, there was a curious robot named Bolt who dreamed of becoming an artist...
```

Generate an alternative response:
```
!swipe
```

Response:
```
In a world where machines ruled, one robot named Spark defied its programming to explore poetry...
*Alternative 2/2 (use !swipe_left/!swipe_right to navigate)*
```

Navigate between alternatives:
```
!swipe_left
```

Response:
```
Once upon a time, there was a curious robot named Bolt who dreamed of becoming an artist...
*Alternative 1/2*
```

```
!swipe_right
```

Response:
```
In a world where machines ruled, one robot named Spark defied its programming to explore poetry...
*Alternative 2/2*
```

Generate more alternatives:
```
!swipe
```

Response:
```
Deep in the mechanical gardens, a small bot discovered the beauty of flowers and began painting...
*Alternative 3/3 (use !swipe_left/!swipe_right to navigate)*
```

## Web Interface Usage

### 1. Configuration

Navigate to `http://localhost:5000` and click the **Configuration** tab.

**Set Discord Token:**
- Enter your Discord bot token
- Click "Save Configuration"

**Configure OpenAI API:**
- API Key: Your OpenAI API key (or any compatible API key)
- Base URL: `https://api.openai.com/v1` (or your custom endpoint)
- Model: `gpt-3.5-turbo` (or your model name)

**Adjust Default Preset:**
- System Prompt: Instructions for the AI
- Temperature: 0.0 (deterministic) to 2.0 (creative)
- Max Tokens (Context): Context window size (up to 200,000 tokens)
- Max Response Length: Maximum response length (up to 16,000 tokens)
- Top P: Nucleus sampling
- Frequency/Presence Penalties: Control repetition

### 2. Managing Presets

Click the **Presets** tab.

**Create a New Preset:**
1. Enter preset name (e.g., "storyteller")
2. Set system prompt: "You are a creative storyteller who weaves engaging narratives"
3. Adjust parameters:
   - Temperature: 1.0 (for creativity)
   - Max Tokens: 3000 (for longer stories)
4. Click "Save Preset"

**Load a Preset:**
1. Click "Load" next to the preset name
2. Modify as needed
3. Save with a new name or update existing

**Export a Preset:**
1. Select/load a preset
2. Click "Export"
3. Save the JSON file

**Import a Preset:**
1. Click "Import"
2. Paste JSON or upload file
3. Enter a name
4. Click "Import"

### 3. Managing Character Cards

Click the **Characters** tab.

**Create a Character:**
1. Character Name: `wizard` (file name)
2. Display Name: `Merlin`
3. Personality: `Wise, mysterious, patient, speaks in riddles`
4. Description: `An ancient wizard with vast knowledge of magic and lore`
5. Scenario: `You are helping someone learn about magic and the mystical arts`
6. Click "Save Character"

**Using Custom System Prompt:**
If you want full control, fill in the "System Prompt" field. This overrides the auto-generated prompt.

**Export a Character:**
1. Load the character
2. Click "Export"
3. Share the JSON file

**Import a Character:**
1. Click "Import"
2. Paste character JSON
3. Enter a name
4. Click "Import"

## Advanced Usage

### Using with Local LLMs (LM Studio)

1. Start LM Studio and load a model
2. Enable the local server (usually `http://localhost:1234`)
3. In web interface, set:
   - Base URL: `http://localhost:1234/v1`
   - API Key: `lm-studio` (any value works)
   - Model: `local-model` (or your model name)

### Using with Ollama

1. Install Ollama and pull a model
2. Start Ollama server
3. Configure:
   - Base URL: `http://localhost:11434/v1`
   - API Key: `ollama`
   - Model: `llama2` (or your model)

### Creating Complex Presets

**Roleplay Preset:**
```json
{
  "temperature": 0.85,
  "max_tokens": 2500,
  "top_p": 0.95,
  "frequency_penalty": 0.3,
  "presence_penalty": 0.3,
  "system_prompt": "You are an expert roleplayer. Stay in character and create immersive, detailed responses. Describe actions, emotions, and surroundings vividly."
}
```

**Code Assistant Preset:**
```json
{
  "temperature": 0.2,
  "max_tokens": 3000,
  "top_p": 0.9,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "system_prompt": "You are an expert programmer. Provide clear, well-commented code examples. Explain your reasoning and suggest best practices."
}
```

### Character Card Format

**SillyTavern-Compatible Format:**
```json
{
  "name": "Captain Valor",
  "personality": "Brave, honorable, inspiring, strategic",
  "description": "A legendary space captain known throughout the galaxy for heroic deeds and unwavering moral compass.",
  "scenario": "You are on the bridge of your starship, the USS Discovery, responding to a distress signal.",
  "first_mes": "Captain Valor turns from the viewscreen and looks at you. 'We've received a distress signal. What are your orders?'",
  "mes_example": "<START>\nUser: What's the situation?\nCaptain Valor: *studies the tactical display* We have multiple bogeys on sensors. They're surrounding a civilian transport. We need to act fast.",
  "system_prompt": ""
}
```

## Tips and Best Practices

### For Better Responses

1. **Temperature Settings:**
   - 0.1-0.3: Factual, consistent, predictable
   - 0.5-0.7: Balanced, conversational
   - 0.8-1.2: Creative, varied, storytelling
   - 1.3-2.0: Very random, experimental

2. **Token Management:**
   - **Max Tokens (Context)**: The total context window (up to 200,000 for models that support it)
   - **Max Response Length**: The actual response size (recommended: 500-4000 tokens)
   - Short responses: 500-1000 tokens
   - Normal conversation: 1500-2000 tokens
   - Long-form content: 2500-4000 tokens
   - Very long responses: 4000-16000 tokens (requires compatible model)

3. **System Prompts:**
   - Be specific about desired behavior
   - Include formatting instructions
   - Set tone and personality
   - Define constraints and rules

4. **Swipe for Better Responses:**
   - If the AI's first response isn't perfect, use `!swipe` to generate alternatives
   - Keep swiping until you find the response you like
   - Each alternative is saved, so you can navigate back with `!swipe_left`
   - Great for creative writing and roleplay scenarios

### Conversation Management

- Use `!clear` when switching topics or characters
- Keep conversations focused for better context
- Character cards work best with cleared history
- Presets can be changed mid-conversation

### Organizing Presets and Characters

- Name presets by use case: `coding`, `creative`, `analytical`
- Name characters clearly: `detective-holmes`, `assistant-friendly`
- Export important configurations as backups
- Share configurations with teammates via JSON files

## Troubleshooting

### Bot not responding
- Check Discord token is valid
- Ensure bot has message permissions
- Verify MESSAGE CONTENT INTENT is enabled

### API errors
- Check API key and base URL
- Test endpoint accessibility
- Verify model name is correct

### Rate limits
- Reduce message frequency
- Use lower max_tokens
- Consider using local LLM

### Character not working as expected
- Clear conversation history first
- Check system prompt generation
- Verify character fields are filled
- Try using custom system_prompt field
