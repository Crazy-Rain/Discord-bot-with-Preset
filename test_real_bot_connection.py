#!/usr/bin/env python3
"""
Real-world bot connection test.
This test helps diagnose actual Discord connection issues.
"""

import asyncio
import sys
import time
from config_manager import ConfigManager
from discord_bot import DiscordBot

async def test_real_bot_connection():
    """Test actual bot connection and guild detection."""
    print("=" * 70)
    print("REAL BOT CONNECTION TEST")
    print("=" * 70)
    
    config_manager = ConfigManager()
    token = config_manager.get("discord_token")
    
    if not token or token == "YOUR_DISCORD_BOT_TOKEN":
        print("\n❌ No Discord token configured!")
        print("Please configure your Discord bot token in config.json")
        return False
    
    print(f"\n✅ Discord token found: {token[:10]}...")
    
    # Create bot instance
    print("\n1. Creating bot instance...")
    bot = DiscordBot(config_manager)
    print(f"   Bot instance created: {id(bot)}")
    print(f"   Initial guilds count: {len(bot.guilds)}")
    
    # Add a test event to see when guilds are populated
    guild_ready_event = asyncio.Event()
    
    @bot.event
    async def on_ready():
        """Override on_ready to track when guilds are populated."""
        print(f"\n2. on_ready event fired!")
        print(f"   Bot user: {bot.user}")
        print(f"   Guilds count: {len(bot.guilds)}")
        if len(bot.guilds) > 0:
            print("   Guilds:")
            for guild in bot.guilds:
                channel_count = len(guild.text_channels) if hasattr(guild, 'text_channels') else 0
                print(f"      - {guild.name} (ID: {guild.id}, {channel_count} text channels)")
        else:
            print("   ⚠️  No guilds found!")
            print("   Make sure the bot is added to at least one server.")
        guild_ready_event.set()
    
    # Start bot with timeout
    print("\n3. Connecting to Discord...")
    try:
        # Create a task to run the bot
        bot_task = asyncio.create_task(bot.start(token))
        
        # Wait for on_ready or timeout
        try:
            await asyncio.wait_for(guild_ready_event.wait(), timeout=30)
            print("\n4. ✅ Bot connected successfully!")
            
            # Give it a moment to ensure guilds are fully loaded
            await asyncio.sleep(2)
            
            # Check guilds one more time
            print("\n5. Final guild check:")
            print(f"   Guilds count: {len(bot.guilds)}")
            if len(bot.guilds) == 0:
                print("   ❌ ISSUE: Bot is connected but has no guilds!")
                print("   Possible causes:")
                print("   - Bot is not added to any servers")
                print("   - Guilds intent is not enabled in Discord Developer Portal")
                print("   - There's a delay in guild caching")
            else:
                print("   ✅ Bot has guilds!")
            
            # Close bot
            print("\n6. Closing bot connection...")
            await bot.close()
            
        except asyncio.TimeoutError:
            print("\n❌ Timeout waiting for bot to connect!")
            print("   The bot may be having connection issues.")
            await bot.close()
            return False
            
    except Exception as e:
        print(f"\n❌ Error connecting bot: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
    return True

if __name__ == "__main__":
    result = asyncio.run(test_real_bot_connection())
    sys.exit(0 if result else 1)
