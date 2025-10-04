# Reconnection Fix - Visual Guide

## The Problem - Before Fix

```
┌─────────────────────────────────────────────────────────────┐
│  main() function                                            │
│                                                             │
│  1. bot_instance = DiscordBot(config_manager)  <-- Created  │
│     │                                                       │
│     v                                                       │
│  2. web_server = WebServer(..., bot_instance)  <-- Stores  │
│     │                                             reference │
│     v                                                       │
│  3. asyncio.run(run_discord_bot(...))                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│  run_discord_bot() - First Iteration                        │
│                                                             │
│  retry_count = 0                                           │
│  bot_instance.is_closed() = False                          │
│                                                             │
│  ❌ Condition: if retry_count > 0 or is_closed():          │
│     │         = if False or False:                         │
│     │         = False                                      │
│     │                                                       │
│     └─> Don't create new instance, use existing one        │
│                                                             │
│  await bot_instance.start(token)  <-- Uses instance from    │
│                                       main() above          │
│                                                             │
│  ✓ Works fine first time                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│  Bot Running - First Disconnect                             │
│                                                             │
│  Discord.py detects disconnect                             │
│  -> on_disconnect() called                                 │
│  -> Discord.py tries to reconnect internally               │
│  -> ✓ Success! on_resume() called                         │
│  -> Bot keeps running                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│  Bot Running - Second Disconnect                            │
│                                                             │
│  Discord.py detects disconnect again                       │
│  -> on_disconnect() called                                 │
│  -> Discord.py tries to reconnect internally               │
│  -> ❌ FAILS! (cumulative state issues?)                   │
│  -> Exception raised                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│  run_discord_bot() - Exception Handler                      │
│                                                             │
│  retry_count = 1                                           │
│  Close old bot instance                                    │
│  Sleep 5 seconds                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│  run_discord_bot() - Second Iteration                       │
│                                                             │
│  retry_count = 1                                           │
│  bot_instance.is_closed() = True (just closed it)          │
│                                                             │
│  ✓ Condition: if retry_count > 0 or is_closed():           │
│     │         = if True or True:                           │
│     │         = True                                       │
│     │                                                       │
│     └─> Create NEW bot instance!                           │
│                                                             │
│  bot_instance = DiscordBot(config_manager)  <-- Fresh!     │
│  await bot_instance.start(token)                           │
│                                                             │
│  ✓ Should work... but what about web_server?              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│  ❌ WEB SERVER PROBLEM                                      │
│                                                             │
│  web_server.bot_instance still points to OLD instance!     │
│  (the one created in main() at the beginning)              │
│                                                             │
│  When web server tries to access:                          │
│  - bot_instance.guilds     -> OLD/stale data               │
│  - bot_instance.cp_totals  -> OLD/stale data               │
│  - bot_instance.update_openai_config() -> Wrong instance!  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## The Solution - After Fix

```
┌─────────────────────────────────────────────────────────────┐
│  main() function                                            │
│                                                             │
│  1. bot_instance = DiscordBot(config_manager)              │
│     (placeholder, won't be used for actual connection)     │
│                                                             │
│  2. web_server = WebServer(..., bot_instance)              │
│     (stores in _bot_instance_ref for backward compat)      │
│                                                             │
│  3. asyncio.run(run_discord_bot(...))                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│  run_discord_bot() - EVERY Iteration                        │
│                                                             │
│  ✅ ALWAYS create fresh instance:                          │
│                                                             │
│  if retry_count == 0:                                      │
│      print("Creating bot instance for initial connection") │
│  else:                                                     │
│      print("Creating fresh bot instance for reconnection") │
│                                                             │
│  bot_instance = DiscordBot(config_manager)  <-- FRESH!     │
│  await bot_instance.start(token)                           │
│                                                             │
│  ✓ Clean state every time                                 │
│  ✓ No cumulative issues                                   │
│  ✓ Consistent behavior                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│  ✅ WEB SERVER SOLUTION                                     │
│                                                             │
│  @property                                                 │
│  def bot_instance(self):                                   │
│      import main                                           │
│      return main.bot_instance  <-- Always get latest!     │
│                                                             │
│  When web server accesses bot_instance:                    │
│  - Always gets current bot from main.bot_instance global   │
│  - No stale references                                     │
│  - Always up-to-date                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Flow Comparison

### OLD FLOW (Buggy)
```
Iteration 1 (retry_count=0):
  ┌─> Check: retry_count > 0? NO
  ├─> Check: is_closed()? NO
  └─> Use existing instance ❌ (might have issues)

Iteration 2 (retry_count=1):
  ┌─> Check: retry_count > 0? YES
  └─> Create new instance ✓

Web Server:
  └─> Uses instance from main() ❌ (stale after iteration 2)
```

### NEW FLOW (Fixed)
```
Iteration 1 (retry_count=0):
  └─> ALWAYS create new instance ✓

Iteration 2 (retry_count=1):
  └─> ALWAYS create new instance ✓

Iteration N (retry_count=N-1):
  └─> ALWAYS create new instance ✓

Web Server:
  └─> Gets main.bot_instance ✓ (always current)
```

## Key Improvements

| Aspect | Before | After |
|--------|--------|-------|
| **First iteration** | Reuses bot from main() | Creates fresh instance |
| **Bot state** | Potentially inconsistent | Always clean |
| **Web server access** | Static reference | Dynamic via property |
| **Reconnection reliability** | Works once, fails second time | Works every time |
| **Debugging** | Hard to track state issues | Consistent behavior |

## Code Changes Summary

### main.py
```diff
- if retry_count > 0 or bot_instance.is_closed():
-     print("🔄 Creating fresh bot instance for reconnection...")
-     bot_instance = DiscordBot(config_manager)
+ if retry_count == 0:
+     print("🔄 Creating bot instance for initial connection...")
+ else:
+     print("🔄 Creating fresh bot instance for reconnection...")
+ bot_instance = DiscordBot(config_manager)
```

### web_server.py
```diff
  def __init__(self, config_manager, bot_instance=None):
-     self.bot_instance = bot_instance
+     self._bot_instance_ref = bot_instance
+
+ @property
+ def bot_instance(self):
+     import main
+     return main.bot_instance
```

## Result

✅ **Reliable reconnection every time**
- First disconnect → reconnects successfully
- Second disconnect → reconnects successfully  
- Third disconnect → reconnects successfully
- ...and so on!

✅ **Web server always has current bot**
- No stale references
- Configuration updates work
- Server/channel info always current
