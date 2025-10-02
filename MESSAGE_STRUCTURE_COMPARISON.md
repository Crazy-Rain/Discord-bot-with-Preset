# Message Structure Comparison

## Before (Old System)

**Single System Message:**
```
ROLE: system
CONTENT:
  - System prompt
  - Character description
  - Character personality
  - Character scenario
  - User character descriptions
  - Lorebook entries
  - Format guidelines
  (All combined into one large system message)

ROLE: user
CONTENT: "Hello!"

ROLE: assistant
CONTENT: "Hi there!"
```

## After (SillyTavern-Style System)

**Properly Separated Messages:**
```
1. ROLE: system
   CONTENT:
     - System prompt from preset
     - Character description (if character_position = "system" or "both")
     - User character descriptions
     - Lorebook entries
     - Format guidelines

2. ROLE: assistant  (from first_mes)
   CONTENT: "*glances over with a playful smirk* Well, well. You look interesting."

3. ROLE: user  (from mes_example)
   CONTENT: "What brings you here?"

4. ROLE: assistant  (from mes_example)
   CONTENT: "*leans back* Oh, the usual. Good drinks, better company, maybe some treasure."

5. ROLE: user  (from mes_example)
   CONTENT: "You seem dangerous."

6. ROLE: assistant  (from mes_example)
   CONTENT: "*laughs* Flattery will get you everywhere, darling."

7. ROLE: user  (conversation history)
   CONTENT: "I need your help with something."

8. ROLE: assistant  (conversation history)
   CONTENT: "*sits up with interest* Now you've got my attention. What do you need?"

9. ROLE: user  (current message)
   CONTENT: "Can you help me find a treasure map?"
```

## Key Benefits

1. **Better Context Understanding**: AI can distinguish between instructions (system), examples (user/assistant pairs), and actual conversation

2. **Example-Based Learning**: The AI learns the character's voice and behavior from the example dialogues

3. **Cleaner System Message**: System prompt stays focused on instructions, not character personality

4. **Optimal for Uncensored Characters**: By separating instructions from examples, the AI is less likely to refuse requests when in character

5. **SillyTavern Compatibility**: Character cards with `first_mes` and `mes_example` work exactly as expected

## Configuration

In your preset JSON:
```json
{
  "prompt_format": "sillytavern",
  "character_position": "both",
  "include_examples": true,
  "example_separator": "<START>"
}
```

In your character card JSON:
```json
{
  "name": "Aria",
  "first_mes": "*opening message*",
  "mes_example": "<START>\n{{user}}: message\n{{char}}: response\n<START>\n{{user}}: message\n{{char}}: response"
}
```
