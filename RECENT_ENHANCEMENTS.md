# Recent Enhancements - Quick Reference Guide

This guide covers the new features added to the Discord bot based on user feedback.

## 🔧 Web Server Fix

**Issue**: The web server was not loading properly at localhost.

**Solution**: Added threading support to the Flask server.

**Technical Details**:
- Added `threaded=True` to allow concurrent request handling
- Added `use_reloader=False` to prevent duplicate server instances

**Impact**: The web UI now works correctly at http://localhost:5000

---

## 📊 Extended Token Limits

**Issue**: Max tokens were limited to 4,000, insufficient for large context windows.

**Solution**: Increased the maximum context tokens to 200,000.

### New Configuration Fields

```json
{
  "max_tokens": 100000,          // Context window (up to 200,000)
  "max_response_length": 2000    // Actual response size (up to 16,000)
}
```

### Why Two Fields?

- **max_tokens (Context)**: The total context window the model can see (conversation history + new response)
- **max_response_length**: The maximum length for the AI's response only

This separation allows you to:
- Use models with 100K+ token context windows
- Keep responses at a reasonable length (e.g., 2000 tokens)
- Fit more conversation history without generating huge responses

### Web UI Sliders

**Configuration Tab & Presets Tab**:
- **Max Tokens (Context)**: 100 to 200,000 tokens (step: 1,000)
- **Max Response Length**: 100 to 16,000 tokens (step: 100)

---

## 🔄 Swipe Functionality

**Issue**: Need ability to generate and navigate alternative AI responses, similar to SillyTavern.

**Solution**: Implemented full swipe functionality with three new commands.

### Commands

#### `!swipe`
Generate an alternative response to the last message.

```
User: !chat Tell me a story about space
Bot: In the vast cosmos, a lone explorer...

User: !swipe
Bot: Among the stars, a brave astronaut...
     *Alternative 2/2 (use !swipe_left/!swipe_right to navigate)*
```

#### `!swipe_left`
Navigate to the previous alternative response (wraps around).

```
User: !swipe_left
Bot: In the vast cosmos, a lone explorer...
     *Alternative 1/2*
```

#### `!swipe_right`
Navigate to the next alternative response (wraps around).

```
User: !swipe_right
Bot: Among the stars, a brave astronaut...
     *Alternative 2/2*
```

### How It Works

1. When you use `!chat`, the bot generates a response and stores it
2. Use `!swipe` to generate alternative responses to the same message
3. Each swipe creates a new alternative and switches to it
4. Use `!swipe_left` and `!swipe_right` to navigate between alternatives
5. The bot remembers up to 10 exchanges with their alternatives
6. All alternatives are cleared when you use `!clear`

### Use Cases

- **Creative Writing**: Generate multiple story directions
- **Roleplay**: Find the perfect character response
- **Problem Solving**: Explore different approaches
- **Tone Adjustment**: Get variations with different tones

---

## 📝 Configuration Examples

### For Long Context + Short Responses
Perfect for having long conversations with concise replies:

```json
{
  "temperature": 0.7,
  "max_tokens": 128000,        // Large context (Claude 2.1, GPT-4 Turbo)
  "max_response_length": 1000,  // Short, focused responses
  "system_prompt": "You are a helpful assistant. Be concise."
}
```

### For Creative Writing
Generate longer, more detailed creative content:

```json
{
  "temperature": 0.9,
  "max_tokens": 8000,           // Moderate context
  "max_response_length": 4000,  // Longer creative responses
  "frequency_penalty": 0.5,
  "system_prompt": "You are a creative writer..."
}
```

### For Code Generation
Use large context for code understanding:

```json
{
  "temperature": 0.3,
  "max_tokens": 100000,          // Very large for code review
  "max_response_length": 2000,   // Reasonable code snippets
  "system_prompt": "You are an expert programmer..."
}
```

---

## 🧪 Testing Your Setup

### Test Web Server
1. Start the bot: `python main.py`
2. Navigate to http://localhost:5000
3. You should see the configuration interface
4. Check both sliders are visible in Configuration tab

### Test Extended Tokens
1. Go to Configuration or Presets tab
2. Move the "Max Tokens (Context)" slider
3. It should go up to 200,000
4. Save and verify in config/preset file

### Test Swipe Functionality
```
!chat What's a good recipe for cookies?
!swipe
!swipe
!swipe_left
!swipe_right
```

You should see different responses and navigation working.

---

## 🔄 Backward Compatibility

All changes are backward compatible:

- **Old presets**: Will use `max_tokens` as before
- **New presets**: Can use both `max_tokens` and `max_response_length`
- **Web UI**: Handles both old and new configurations
- **Commands**: All existing commands work as before

---

## 💡 Tips & Best Practices

### Token Management
1. Start with defaults (2000/2000) and adjust as needed
2. Increase context for longer conversations
3. Keep response length reasonable for Discord's limits
4. Monitor your API usage/costs

### Swipe Usage
1. Generate 2-3 alternatives before choosing
2. Use with creative/roleplay scenarios
3. Clear alternatives when switching topics
4. Remember: each swipe uses API tokens

### Model Compatibility
- **OpenAI GPT-4 Turbo**: Supports 128K context
- **Claude 2.1**: Supports 200K context  
- **Local models**: Check your model's limits
- **GPT-3.5-Turbo**: 16K max context

---

## 📚 Additional Resources

- **README.md**: Complete feature documentation
- **EXAMPLES.md**: Detailed usage examples
- **SETUP.md**: Initial setup instructions
- **PROJECT_SUMMARY.md**: Technical implementation details

---

## 🐛 Troubleshooting

### Web server not loading
- Check if port 5000 is available
- Try accessing http://127.0.0.1:5000 instead
- Look for error messages in console

### Swipe not working
- Make sure you've used `!chat` first
- Check that the bot is responding normally
- Try `!clear` and start a new conversation

### Large tokens not working
- Verify your model supports large contexts
- Check API provider documentation
- Monitor for token limit errors

### Response too long
- Reduce `max_response_length` value
- Discord has a 2000 character limit per message
- The bot auto-splits long responses

---

**Questions or Issues?** Check the main documentation or create an issue on GitHub.
