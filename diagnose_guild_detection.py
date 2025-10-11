#!/usr/bin/env python3
"""
Comprehensive diagnostic tool for Discord bot guild detection issues.

This script tests various aspects of bot connectivity and guild caching
to help identify why the web interface might show "NO SERVERS".
"""

import sys
import asyncio
import time
from config_manager import ConfigManager

def test_configuration():
    """Test 1: Check configuration."""
    print("\n" + "=" * 70)
    print("TEST 1: Configuration Check")
    print("=" * 70)
    
    config_manager = ConfigManager()
    token = config_manager.get("discord_token")
    
    if not token or token == "YOUR_DISCORD_BOT_TOKEN":
        print("❌ FAIL: Discord token not configured")
        print("   Action: Configure your Discord bot token in config.json")
        return False
    
    print(f"✅ PASS: Discord token configured ({token[:10]}...)")
    return True

def test_bot_instance_import():
    """Test 2: Check if main.bot_instance is accessible."""
    print("\n" + "=" * 70)
    print("TEST 2: Bot Instance Import Test")
    print("=" * 70)
    
    try:
        import main
        print(f"✅ PASS: Successfully imported main module")
        
        if hasattr(main, 'bot_instance'):
            print(f"✅ PASS: main.bot_instance exists")
            bot = main.bot_instance
            if bot is not None:
                print(f"   Bot instance: {type(bot).__name__}")
                if hasattr(bot, 'guilds'):
                    print(f"   Guilds count: {len(bot.guilds)}")
                else:
                    print(f"   ⚠️  WARNING: Bot has no 'guilds' attribute")
            else:
                print(f"   ⚠️  WARNING: main.bot_instance is None")
            return True
        else:
            print(f"❌ FAIL: main module has no 'bot_instance' attribute")
            return False
            
    except ImportError as e:
        print(f"❌ FAIL: Cannot import main module - {e}")
        return False

def test_web_server_bot_access():
    """Test 3: Check if WebServer can access bot instance."""
    print("\n" + "=" * 70)
    print("TEST 3: WebServer Bot Access Test")
    print("=" * 70)
    
    try:
        from web_server import WebServer
        config_manager = ConfigManager()
        
        # Create WebServer without bot_instance parameter (the fix)
        web_server = WebServer(config_manager)
        print(f"✅ PASS: WebServer created successfully")
        
        # Check _bot_instance_ref
        print(f"   _bot_instance_ref: {web_server._bot_instance_ref}")
        
        # Check bot_instance property
        bot = web_server.bot_instance
        if bot is not None:
            print(f"✅ PASS: WebServer.bot_instance is not None")
            print(f"   Bot type: {type(bot).__name__}")
            if hasattr(bot, 'guilds'):
                guild_count = len(bot.guilds)
                print(f"   Guilds count: {guild_count}")
                if guild_count == 0:
                    print(f"   ⚠️  WARNING: Bot has 0 guilds")
                    print(f"   This could mean:")
                    print(f"   - Bot hasn't connected yet")
                    print(f"   - Bot is not added to any servers")
                    print(f"   - Guilds intent is not enabled in Discord Developer Portal")
            else:
                print(f"   ⚠️  WARNING: Bot has no 'guilds' attribute")
            return True
        else:
            print(f"⚠️  WARNING: WebServer.bot_instance is None")
            print(f"   This is expected before the bot connects")
            return True
            
    except Exception as e:
        print(f"❌ FAIL: Error testing WebServer - {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test 4: Test API endpoints."""
    print("\n" + "=" * 70)
    print("TEST 4: API Endpoints Test")
    print("=" * 70)
    
    try:
        from web_server import WebServer
        config_manager = ConfigManager()
        web_server = WebServer(config_manager)
        
        with web_server.app.test_client() as client:
            # Test /api/servers
            print("\n Testing GET /api/servers...")
            response = client.get('/api/servers')
            data = response.get_json()
            servers = data.get('servers', [])
            print(f"   Response status: {response.status_code}")
            print(f"   Servers count: {len(servers)}")
            
            if len(servers) == 0:
                print(f"   ⚠️  WARNING: No servers returned")
                print(f"   This is why the UI shows 'NO SERVERS'")
            else:
                print(f"   ✅ Servers found:")
                for server in servers[:5]:  # Show first 5
                    print(f"      - {server['name']} ({server['channel_count']} channels)")
            
            # Test /api/manual_send/channels
            print("\n   Testing GET /api/manual_send/channels...")
            response = client.get('/api/manual_send/channels')
            data = response.get_json()
            channels = data.get('channels', [])
            print(f"   Response status: {response.status_code}")
            print(f"   Channels count: {len(channels)}")
            
            if len(channels) == 0:
                print(f"   ⚠️  WARNING: No channels returned")
                print(f"   This is why the dropdown is empty")
            else:
                print(f"   ✅ Channels found:")
                for channel in channels[:5]:  # Show first 5
                    print(f"      - {channel['server_name']} / {channel['name']}")
            
        return True
            
    except Exception as e:
        print(f"❌ FAIL: Error testing API endpoints - {e}")
        import traceback
        traceback.print_exc()
        return False

def test_discord_intents():
    """Test 5: Check Discord intents configuration."""
    print("\n" + "=" * 70)
    print("TEST 5: Discord Intents Test")
    print("=" * 70)
    
    try:
        from discord_bot import DiscordBot
        from config_manager import ConfigManager
        
        config_manager = ConfigManager()
        bot = DiscordBot(config_manager)
        
        intents = bot.intents
        print(f"✅ Bot intents configured:")
        print(f"   guilds: {intents.guilds}")
        print(f"   members: {intents.members}")
        print(f"   messages: {intents.messages}")
        print(f"   message_content: {intents.message_content}")
        
        if not intents.guilds:
            print(f"\n❌ CRITICAL: Guilds intent is NOT enabled!")
            print(f"   This will prevent the bot from seeing servers.")
            print(f"   Action: Enable guilds intent in the code (should be default)")
            return False
        else:
            print(f"\n✅ PASS: Guilds intent is enabled in code")
            print(f"\nIMPORTANT: Also check Discord Developer Portal:")
            print(f"   1. Go to https://discord.com/developers/applications")
            print(f"   2. Select your bot application")
            print(f"   3. Go to 'Bot' section")
            print(f"   4. Under 'Privileged Gateway Intents':")
            print(f"      - 'SERVER MEMBERS INTENT' (optional for this issue)")
            print(f"      - 'MESSAGE CONTENT INTENT' should be ON")
            print(f"   5. NOTE: The 'guilds' intent is NOT privileged and is always available")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error checking intents - {e}")
        import traceback
        traceback.print_exc()
        return False

def print_recommendations():
    """Print recommendations for fixing the issue."""
    print("\n" + "=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    
    print("\nIf you're seeing 'NO SERVERS' in the web interface:")
    print("\n1. VERIFY BOT IS ADDED TO SERVERS:")
    print("   - Go to Discord and check if the bot is in at least one server")
    print("   - If not, use the OAuth2 URL to add it:")
    print("     https://discord.com/developers/applications")
    print("     → Your App → OAuth2 → URL Generator")
    print("     → Select 'bot' scope and required permissions")
    
    print("\n2. CHECK BOT HAS CONNECTED:")
    print("   - Look for 'Bot is ready! Logged in as...' in console")
    print("   - This message confirms the bot has connected")
    print("   - Guilds are populated when this message appears")
    
    print("\n3. TIMING ISSUE:")
    print("   - If you open the web interface TOO QUICKLY after starting")
    print("   - The bot might not have finished connecting")
    print("   - Try refreshing the page after bot shows as 'ready'")
    
    print("\n4. MODULE IMPORT ISSUE:")
    print("   - If using 'uv run' or similar tools")
    print("   - There might be module isolation issues")
    print("   - Try running with: python main.py")
    
    print("\n5. RESTART:")
    print("   - Stop the bot (Ctrl+C)")
    print("   - Start it again: python main.py")
    print("   - Wait for 'Bot is ready!' message")
    print("   - Open http://localhost:5000")
    print("   - Check Manual Send tab")

def main():
    """Run all diagnostic tests."""
    print("=" * 70)
    print("DISCORD BOT GUILD DETECTION - COMPREHENSIVE DIAGNOSTIC")
    print("=" * 70)
    print("\nThis tool will help diagnose why the web interface shows 'NO SERVERS'")
    print("even though the bot appears online in Discord.")
    
    results = []
    
    # Run tests
    results.append(("Configuration", test_configuration()))
    results.append(("Bot Instance Import", test_bot_instance_import()))
    results.append(("WebServer Bot Access", test_web_server_bot_access()))
    results.append(("API Endpoints", test_api_endpoints()))
    results.append(("Discord Intents", test_discord_intents()))
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    # Print recommendations
    print_recommendations()
    
    print("\n" + "=" * 70)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 70)
    
    # Return success if all tests passed
    return all(result for _, result in results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
