# Per-Channel Character Avatars - Visual Guide

## How It Works: Visual Explanation

### Traditional Bot Avatar (Old Method)

```
┌─────────────────────────────────────────────────────────┐
│                    Discord Server                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  #channel-1              #channel-2        #channel-3   │
│  ┌──────────┐            ┌──────────┐     ┌──────────┐ │
│  │          │            │          │     │          │ │
│  │ [BOT]    │            │ [BOT]    │     │ [BOT]    │ │
│  │ ┌────┐   │            │ ┌────┐   │     │ ┌────┐   │ │
│  │ │ 🤖 │   │            │ │ 🤖 │   │     │ │ 🤖 │   │ │
│  │ └────┘   │            │ └────┘   │     │ └────┘   │ │
│  │ Same     │            │ Same     │     │ Same     │ │
│  │ Avatar   │            │ Avatar   │     │ Avatar   │ │
│  │ Everywhere│           │ Everywhere│    │ Everywhere│ │
│  └──────────┘            └──────────┘     └──────────┘ │
│                                                          │
│  Problem: Can only change 2 times per hour              │
│           Same avatar in all channels                   │
└─────────────────────────────────────────────────────────┘
```

### Per-Channel Webhooks (New Method)

```
┌─────────────────────────────────────────────────────────┐
│                    Discord Server                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  #fantasy-rp             #scifi-rp         #mystery-rp  │
│  ┌──────────┐            ┌──────────┐     ┌──────────┐ │
│  │          │            │          │     │          │ │
│  │ Luna     │            │ AI-2077  │     │ Sherlock │ │
│  │ ┌────┐   │            │ ┌────┐   │     │ ┌────┐   │ │
│  │ │ 🌙 │   │            │ │ 🤖 │   │     │ │ 🔍 │   │ │
│  │ └────┘   │            │ └────┘   │     │ └────┘   │ │
│  │ "Hello!" │            │ "Beep"   │     │ "Watson?"│ │
│  │ -Luna    │            │ -AI-2077 │     │ -Sherlock│ │
│  └──────────┘            └──────────┘     └──────────┘ │
│                                                          │
│  Solution: Different character per channel              │
│            No rate limits, unlimited switches           │
└─────────────────────────────────────────────────────────┘
```

## Architecture Diagram

```
┌────────────────────────────────────────────────────────────┐
│                      Discord Bot                           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  User Commands         Bot Logic           Discord API    │
│  ═════════════         ═════════           ════════════    │
│                                                            │
│  !character luna       Load Character      Create/Get     │
│       │                     │              Webhook        │
│       │                     │                  │          │
│       └────────────────────>│                  │          │
│                              │                  │          │
│                              │<─────────────────┘          │
│                              │                             │
│                       Store in Memory:                     │
│                       channel_characters[channel_id] = {   │
│                         "name": "Luna",                    │
│                         "avatar_url": "https://..."        │
│                       }                                    │
│                              │                             │
│  !chat message              │                             │
│       │                     │                             │
│       └────────────────────>│                             │
│                              │                             │
│                        Check if character                  │
│                        loaded for channel?                 │
│                              │                             │
│                        ┌─────┴─────┐                      │
│                        │           │                      │
│                     Yes│           │No                    │
│                        │           │                      │
│                        v           v                      │
│                  Use Webhook   Normal Message             │
│                  with avatar   from bot                   │
│                  and name                                 │
│                        │           │                      │
│                        └─────┬─────┘                      │
│                              │                             │
│                              v                             │
│                      Message Appears                       │
│                      in Channel                           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Data Flow Example

### Step 1: Load Character

```
User types: !character luna

┌──────────┐      ┌──────────┐      ┌──────────────┐
│  User    │─────>│   Bot    │─────>│ Memory       │
└──────────┘      └──────────┘      └──────────────┘
                       │                 Store:
                       │                 channel_characters[123] = {
                       │                   name: "Luna",
                       v                   avatar_url: "https://..."
                  ┌──────────┐          }
                  │ Webhook  │
                  │ Manager  │
                  └──────────┘
                       │
                       v
              Create/Get Webhook
              for channel #123
```

### Step 2: Chat with Character

```
User types: !chat Hello Luna!

┌──────────┐      ┌──────────┐      ┌──────────────┐
│  User    │─────>│   Bot    │      │ OpenAI API   │
└──────────┘      └──────────┘      └──────────────┘
                       │                    ^
                       │                    │
                       │ Send prompt        │
                       └────────────────────┘
                       │
                       │ Receive response
                       v
                  ┌──────────┐
                  │ Check    │
                  │Character?│
                  └──────────┘
                       │
                  Yes  │
                       v
              ┌──────────────────┐
              │ Send via Webhook │
              │ with Luna's      │
              │ name & avatar    │
              └──────────────────┘
                       │
                       v
              ┌──────────────────┐
              │ Message appears  │
              │ as "Luna" with   │
              │ Luna's avatar    │
              └──────────────────┘
```

## Multi-Channel Scenario

```
Time: 10:00 AM

Server: Roleplay Hub
├── #fantasy-rp
│   └── Character: Luna (fairy)
│       Avatar: 🧚
│
├── #scifi-rp
│   └── Character: AI-2077 (robot)
│       Avatar: 🤖
│
└── #mystery-rp
    └── Character: Sherlock (detective)
        Avatar: 🔍

All three channels active simultaneously!
No conflicts, no rate limits!

User Actions:
─────────────

#fantasy-rp:
  User: !chat Tell me about magic
  Luna: 🧚 "Magic flows through our realm..."
  
#scifi-rp:
  User: !chat What's your purpose?
  AI-2077: 🤖 "I am programmed to assist..."

#mystery-rp:
  User: !chat Solve this case
  Sherlock: 🔍 "Elementary, my dear Watson..."

All happening at the same time!
```

## Switching Characters in One Channel

```
Timeline in #roleplay:

10:00 - Load Luna
  !character luna
  Bot: ✨ Loaded character Luna

10:01 - Chat as Luna
  !chat Hello!
  Luna: 🌙 "Hi there!"

10:02 - Switch to Sherlock  
  !character sherlock
  Bot: ✨ Loaded character Sherlock Holmes

10:03 - Chat as Sherlock
  !chat Investigate this
  Sherlock: 🔍 "I observe that..."

10:04 - Switch back to Luna
  !character luna
  Bot: ✨ Loaded character Luna

No waiting! No rate limits!
```

## Comparison Chart

```
Feature Comparison:
══════════════════════════════════════════════════════════

                    Global Avatar    Per-Channel Webhooks
                    ═════════════    ════════════════════

Rate Limit          2 per hour       Unlimited ✓
                    
Switch Speed        30 min wait      Instant ✓
                    
Multi-Character     ✗                ✓ 
                    
Per-Channel         ✗                ✓
                    
Name Display        Bot nickname     Character name ✓
                    
Avatar Display      Global           Per-channel ✓
                    
Permission Needed   None             Manage Webhooks
                    
API Calls           bot.user.edit()  Webhooks
```

## Webhook System Diagram

```
┌─────────────────────────────────────────────────┐
│          Webhook Cache System                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  channel_webhooks = {                           │
│    123: Webhook("Character Bot"),               │
│    456: Webhook("Character Bot"),               │
│    789: Webhook("Character Bot")                │
│  }                                              │
│                                                 │
│  When sending message:                          │
│  1. Check cache for channel's webhook           │
│  2. If exists and valid → Use it                │
│  3. If missing → Create new & cache             │
│  4. If invalid → Delete, create new & cache     │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Error Handling Flow

```
!character command
       │
       v
   Load character
       │
       v
   Store in channel_characters
       │
       v
   User sends !chat
       │
       v
   Character loaded? ──No──> Send normal message
       │                            │
      Yes                           │
       │                            │
       v                            │
   Get/Create webhook               │
       │                            │
       v                            │
   Webhook available? ──No──> Send normal message
       │                            │
      Yes                           │
       │                            │
       v                            │
   Send via webhook                 │
       │                            │
       v                            v
   Success! ───────────────────> Message sent!
```

## User Journey

```
New User Experience:
════════════════════

1. Setup Character Card
   ┌─────────────────────────┐
   │ Create luna.json with:  │
   │ - name: "Luna"          │
   │ - avatar_url: "..."     │
   └─────────────────────────┘
           │
           v

2. Load in Discord
   !character luna
           │
           v
   ┌─────────────────────────┐
   │ ✨ Loaded character     │
   │ Luna for this channel!  │
   └─────────────────────────┘
           │
           v

3. Start Chatting
   !chat Hello!
           │
           v
   ┌─────────────────────────┐
   │ Luna 🌙                 │
   │ "Hello! How can I help?"│
   └─────────────────────────┘
           │
           v

4. Switch Characters Anytime
   !character sherlock
   !chat Investigate this
           │
           v
   ┌─────────────────────────┐
   │ Sherlock Holmes 🔍      │
   │ "Elementary..."         │
   └─────────────────────────┘
```

## Permission Setup

```
Required Permission: Manage Webhooks
═════════════════════════════════════

Server Settings
    │
    └─> Roles
         │
         └─> Your Bot's Role
              │
              └─> Permissions
                   │
                   └─> ✓ Manage Webhooks

Without this permission:
├─> Character loading: ✓ Works
├─> Storing character data: ✓ Works
└─> Webhook messages: ✗ Falls back to normal messages
```

## Quick Start Visual Guide

```
Step-by-Step Setup:
═══════════════════

1. Add avatar_url to character card
   ┌───────────────────────────┐
   │ {                         │
   │   "name": "Luna",         │
   │   "avatar_url": "https://│
   │     imgur.com/luna.png"   │
   │ }                         │
   └───────────────────────────┘
          │
          v

2. Grant bot permissions
   ┌───────────────────────────┐
   │ Server Settings →         │
   │ Roles → Bot Role →        │
   │ ✓ Manage Webhooks         │
   └───────────────────────────┘
          │
          v

3. Load character in channel
   ┌───────────────────────────┐
   │ !character luna           │
   └───────────────────────────┘
          │
          v

4. Chat normally
   ┌───────────────────────────┐
   │ !chat Hello!              │
   └───────────────────────────┘
          │
          v

5. Enjoy character avatars! 🎉
   ┌───────────────────────────┐
   │ Luna 🌙                   │
   │ "Hi there!"               │
   └───────────────────────────┘
```

---

**Legend:**
- 🤖 = Bot avatar
- 🌙 = Luna's avatar
- 🤖 = AI-2077's avatar
- 🔍 = Sherlock's avatar
- ✓ = Feature available
- ✗ = Feature not available
- → = Next step
- ═ = Important section

**Color Coding (if viewed in markdown):**
- **Bold** = Commands or important terms
- `Code` = Actual commands to type
- > Quotes = User input examples
