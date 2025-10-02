# Quick Start Guide: SillyTavern-Style Presets

This guide shows you how to use the new SillyTavern-style preset system.

## Step 1: Load a SillyTavern-Style Preset

```discord
!preset sillytavern_style
```
or
```discord
!preset uncensored_roleplay
```

**Response:**
```
Loaded preset: sillytavern_style
```

## Step 2: Load a Character with Examples

```discord
!character aria
```

**Response:**
```
✨ Loaded character Aria for this channel!
The bot will now respond with Aria's avatar and name using webhooks.
```

## Step 3: Start Chatting

```discord
!chat Hello! Who are you?
```

**What Happens Behind the Scenes:**

The bot builds messages like this:

```
Message 1 [system]:
  "Write {{char}}'s next reply in a fictional chat between {{char}} and {{user}}...
   You are Aria. A charming rogue with a silver tongue and a mysterious past..."

Message 2 [assistant]:
  "*A woman with striking red hair and emerald eyes glances over at you from 
   across the tavern. She raises her glass with a playful smirk* Well, well. 
   You look like someone who knows how to have a good time..."

Message 3 [user]:
  "What brings you to this tavern?"

Message 4 [assistant]:
  "*leans back in her chair, studying you with an amused expression* Oh, you 
   know... the usual. Good drinks, better company, and maybe a lead on some 
   treasure. *grins mischievously*"

Message 5 [user]:
  "You seem like you can handle yourself in a fight."

Message 6 [assistant]:
  "*laughs and pats the hilt of her rapier* Flattery will get you everywhere, 
   darling. *winks*"

Message 7 [user]:
  "Hello! Who are you?"
```

**Response from Aria:**
```
*sets down her drink and gives you an appraising look* 

The name's Aria, darling. *extends a hand with a confident smile* Adventurer, 
treasure hunter, and occasional troublemaker - though I prefer to think of 
myself as a professional problem solver. 

*leans in slightly, her emerald eyes sparkling with mischief* 

And who might you be? You've got that look about you - like someone who's 
either looking for adventure, or trying to escape from one. Which is it?
```

## Step 4: Continue the Conversation

The character will maintain consistency because:
1. The system prompt guides the style
2. The example dialogues teach the character's voice
3. The conversation history maintains context

## Creating Your Own SillyTavern-Style Content

### Custom Preset

Create `presets/my_preset.json`:

```json
{
  "temperature": 0.85,
  "max_tokens": 4000,
  "max_response_length": 2000,
  "top_p": 0.95,
  "frequency_penalty": 0.1,
  "presence_penalty": 0.1,
  "system_prompt": "Write {{char}}'s next reply. Be creative and stay in character.",
  "prompt_format": "sillytavern",
  "character_position": "both",
  "include_examples": true,
  "example_separator": "<START>"
}
```

### Custom Character

Create `character_cards/my_character.json`:

```json
{
  "name": "Zara",
  "personality": "Mysterious, intelligent, sarcastic",
  "description": "A cyberpunk hacker with purple hair and augmented reality implants.",
  "scenario": "You meet Zara in a neon-lit underground club.",
  "first_mes": "*adjusts her AR visor and smirks* New face. You a corp or a runner?",
  "mes_example": "<START>\n{{user}}: What do you do?\n{{char}}: *taps her temple* I see what others don't. Data flows like water in this city, and I know how to swim. *grins*\n<START>\n{{user}}: Can you help me?\n{{char}}: *leans back* Depends. What's in it for me? And more importantly... *narrows eyes* ...who sent you?",
  "system_prompt": "",
  "avatar_url": ""
}
```

### Using Your Custom Content

```discord
!preset my_preset
!character zara
!chat Hey, I need your help with something
```

## Tips for Best Results

1. **Temperature**: 
   - 0.7-0.9 for balanced character responses
   - 0.9-1.1 for very creative/varied responses

2. **character_position**:
   - `"system"` - Character in system prompt only (lighter)
   - `"examples"` - Character learned from examples only
   - `"both"` - Maximum character presence (recommended)

3. **Example Dialogues**:
   - Include 2-4 example exchanges
   - Show different facets of the character
   - Use actions (*like this*) and dialogue ("like this")
   - Keep examples concise but characteristic

4. **System Prompt**:
   - Use `{{char}}` and `{{user}}` placeholders
   - Specify response style and length
   - Include any special instructions
   - Keep it clear and direct

## Troubleshooting

**Character not staying in character?**
- Try `character_position: "both"`
- Add more example dialogues
- Adjust system prompt to emphasize character behavior

**Responses too short?**
- Increase `max_response_length`
- Adjust system prompt: "Write detailed responses..."
- Increase `temperature` slightly

**Responses too repetitive?**
- Increase `frequency_penalty` (0.2-0.5)
- Increase `presence_penalty` (0.2-0.5)
- Add more varied example dialogues

**AI refusing requests?**
- Use `uncensored_roleplay` preset
- Ensure system prompt emphasizes staying in character
- Try `character_position: "both"` to strengthen character
- Increase `temperature` for more creative responses

## Advanced: Importing SillyTavern Characters

If you have a character card from SillyTavern with `first_mes` and `mes_example`:

1. Save the JSON file in `character_cards/` directory
2. Use `!character <name>` to load it
3. Use a SillyTavern-style preset
4. The character will work exactly as expected!

## Learn More

- **Full Documentation**: `SILLYTAVERN_PRESETS_GUIDE.md`
- **Technical Details**: `IMPLEMENTATION_SUMMARY_SILLYTAVERN.md`
- **Message Structure**: `MESSAGE_STRUCTURE_COMPARISON.md`
