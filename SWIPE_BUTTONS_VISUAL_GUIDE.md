# Swipe Buttons - Visual Guide

## Button Interface Overview

Every AI response now includes interactive buttons for easy navigation and control.

## Visual Layout

```
┌──────────────────────────────────────────────────────────────┐
│  🤖 Bot Response                                              │
│──────────────────────────────────────────────────────────────│
│                                                               │
│  [Embed with AI-generated response]                          │
│                                                               │
│  In the vast cosmos, a lone explorer drifted through the     │
│  void, searching for signs of life among the stars...        │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│  [◀ Swipe Left]  [🔄 Swipe]  [Swipe Right ▶]  [🗑️ Delete]    │
└──────────────────────────────────────────────────────────────┘
```

## Button Details

### Button 1: ◀ Swipe Left
- **Style**: Secondary (Gray)
- **Function**: Navigate to previous alternative
- **Behavior**: Cycles backwards through alternatives with wrap-around
- **Feedback**: Shows "Alternative X/Y" as ephemeral message

### Button 2: 🔄 Swipe
- **Style**: Primary (Blue)
- **Function**: Generate new alternative response
- **Behavior**: Creates a new AI response and adds it to alternatives
- **Feedback**: Shows "Alternative X/Y" as ephemeral message

### Button 3: Swipe Right ▶
- **Style**: Secondary (Gray)
- **Function**: Navigate to next alternative
- **Behavior**: Cycles forward through alternatives with wrap-around
- **Feedback**: Shows "Alternative X/Y" as ephemeral message

### Button 4: 🗑️ Delete
- **Style**: Danger (Red)
- **Function**: Delete the message
- **Behavior**: Removes the message from the channel
- **Feedback**: Message disappears

## User Flow Examples

### Example 1: Generating Alternatives

```
Step 1: Initial Chat
┌────────────────────────────────────────┐
│ User: !chat Tell me a joke             │
└────────────────────────────────────────┘

Step 2: Bot Response with Buttons
┌────────────────────────────────────────┐
│ 🤖 Bot                                  │
│ Why did the programmer quit his job?   │
│ Because he didn't get arrays!          │
│                                        │
│ [◀ Swipe Left] [🔄 Swipe]              │
│ [Swipe Right ▶] [🗑️ Delete]            │
└────────────────────────────────────────┘

Step 3: User Clicks "🔄 Swipe"
┌────────────────────────────────────────┐
│ 🤖 Bot                                  │
│ What do you call a programmer from     │
│ Finland? Nerdic!                       │
│                                        │
│ [◀ Swipe Left] [🔄 Swipe]              │
│ [Swipe Right ▶] [🗑️ Delete]            │
└────────────────────────────────────────┘
│ ℹ️ Alternative 2/2 (only you can see)  │
└────────────────────────────────────────┘

Step 4: User Clicks "◀ Swipe Left"
┌────────────────────────────────────────┐
│ 🤖 Bot                                  │
│ Why did the programmer quit his job?   │
│ Because he didn't get arrays!          │
│                                        │
│ [◀ Swipe Left] [🔄 Swipe]              │
│ [Swipe Right ▶] [🗑️ Delete]            │
└────────────────────────────────────────┘
│ ℹ️ Alternative 1/2 (only you can see)  │
└────────────────────────────────────────┘
```

### Example 2: With Character Avatar

```
Step 1: Load Character
┌────────────────────────────────────────┐
│ User: !character luna                  │
│ Bot: ✨ Loaded character Luna!         │
└────────────────────────────────────────┘

Step 2: Chat with Character
┌────────────────────────────────────────┐
│ User: !chat How are you today?         │
└────────────────────────────────────────┘

Step 3: Character Response (via Webhook)
┌────────────────────────────────────────┐
│ 🌙 Luna (with avatar)                  │
│ I'm doing wonderfully, thank you for   │
│ asking! The stars are especially       │
│ bright tonight. How about you?         │
│                                        │
│ [◀ Swipe Left] [🔄 Swipe]              │
│ [Swipe Right ▶] [🗑️ Delete]            │
└────────────────────────────────────────┘
```

### Example 3: Long Message Split

```
For messages over 4096 characters, buttons appear on the last chunk:

┌────────────────────────────────────────┐
│ 🤖 Bot                                  │
│ [Very long story - Part 1 of 3]        │
│ Page 1/3                               │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ 🤖 Bot                                  │
│ [Very long story - Part 2 of 3]        │
│ Page 2/3                               │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ 🤖 Bot                                  │
│ [Very long story - Part 3 of 3]        │
│ Page 3/3                               │
│                                        │
│ [◀ Swipe Left] [🔄 Swipe]              │
│ [Swipe Right ▶] [🗑️ Delete]            │
└────────────────────────────────────────┘
```

## Ephemeral Feedback Messages

When you click a button, you'll see a message that only you can see:

```
┌────────────────────────────────────────┐
│ ℹ️ Alternative 3/5 (only you can see)  │
└────────────────────────────────────────┘
```

This tells you:
- Which alternative you're viewing (3)
- How many alternatives exist (5)
- The message is private (ephemeral)

## Button States

### Active Button
```
[◀ Swipe Left]  - Clickable, normal appearance
```

### Disabled State
When there are no alternatives to navigate:
```
The buttons still appear but show feedback messages:
"No other alternatives available. Use the Swipe button to generate more."
```

## Color Coding

- **Gray Buttons** (Navigation): Safe, non-destructive actions
- **Blue Button** (Swipe): Primary action, generates new content
- **Red Button** (Delete): Destructive action, requires confirmation

## Mobile View

On mobile devices, buttons stack vertically for easier tapping:

```
┌──────────────────────┐
│ 🤖 Bot Response      │
│                      │
│ [Message content]    │
│                      │
│ [◀ Swipe Left]       │
│ [🔄 Swipe]           │
│ [Swipe Right ▶]      │
│ [🗑️ Delete]          │
└──────────────────────┘
```

## Comparison: Before vs After

### Before (Text Commands Only)
```
User: !chat Tell me a story
Bot: [Story about space]
User: !swipe
Bot: [Different story]
     *Alternative 2/2 (use !swipe_left/!swipe_right to navigate)*
User: !swipe_left
Bot: [Original story]
     *Alternative 1/2*
```

### After (With Buttons)
```
User: !chat Tell me a story
Bot: [Story about space]
     [◀ Swipe Left] [🔄 Swipe] [Swipe Right ▶] [🗑️ Delete]

User: *clicks Swipe button*
Bot: [Different story]
     [◀ Swipe Left] [🔄 Swipe] [Swipe Right ▶] [🗑️ Delete]
     ℹ️ Alternative 2/2 (only you can see)

User: *clicks Swipe Left*
Bot: [Original story]
     [◀ Swipe Left] [🔄 Swipe] [Swipe Right ▶] [🗑️ Delete]
     ℹ️ Alternative 1/2 (only you can see)
```

**Benefits:**
- ✅ 3 clicks vs 3 commands typed
- ✅ Cleaner interface
- ✅ Easier on mobile
- ✅ More discoverable
- ✅ Faster interaction

## Accessibility

- Button labels are clear and descriptive
- Emoji provide visual cues
- Ephemeral messages provide feedback
- Keyboard navigation supported
- Screen reader compatible

## Tips

1. **Quick Navigation**: Use Left/Right for exploring existing alternatives
2. **Generate More**: Click Swipe when you want new options
3. **Clean Up**: Use Delete to remove messages you don't want
4. **Try Multiple**: Generate several alternatives, then navigate to find the best

## Technical Notes

- Buttons use Discord's native UI components
- No additional latency or lag
- Works with both regular and webhook messages
- Persistent across message edits
- Compatible with Discord mobile and desktop apps

---

For more technical details, see [SWIPE_BUTTONS_GUIDE.md](SWIPE_BUTTONS_GUIDE.md)
