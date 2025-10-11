#!/usr/bin/env python3
"""
Quick verification script for bot guild detection.
Run this to verify everything is configured correctly.
"""

import sys
import json
from config_manager import ConfigManager

def check_config():
    """Check if Discord token is configured."""
    print("=" * 70)
    print("1. CHECKING CONFIGURATION")
    print("=" * 70)
    
    config = ConfigManager()
    token = config.get("discord_token")
    
    if not token or token == "YOUR_DISCORD_BOT_TOKEN":
        print("❌ Discord token not configured")
        print("\n📋 To fix:")
        print("   1. Open config.json")
        print("   2. Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual bot token")
        print("   3. Save the file")
        print("   4. Run this script again")
        return False
    
    print(f"✅ Discord token configured: {token[:10]}...")
    return True

def check_bot_instance():
    """Check if bot instance can be accessed."""
    print("\n" + "=" * 70)
    print("2. CHECKING BOT INSTANCE")
    print("=" * 70)
    
    try:
        import main
        if hasattr(main, 'bot_instance'):
            bot = main.bot_instance
            if bot is None:
                print("⚠️  Bot instance is None (bot not started yet)")
                print("\n📋 This is normal if:")
                print("   - You haven't run 'python main.py' yet")
                print("   - The bot hasn't finished connecting")
                return True
            else:
                if hasattr(bot, 'user') and bot.user:
                    print(f"✅ Bot instance exists and is connected as: {bot.user}")
                else:
                    print("⚠️  Bot instance exists but user is None (not connected yet)")
                
                if hasattr(bot, 'guilds'):
                    guild_count = len(bot.guilds)
                    print(f"   Guilds: {guild_count}")
                    if guild_count > 0:
                        for guild in bot.guilds[:5]:  # Show first 5
                            print(f"      - {guild.name}")
                return True
        else:
            print("❌ main.bot_instance does not exist")
            return False
    except ImportError:
        print("⚠️  Cannot import main module (not running)")
        print("\n📋 This is normal if the bot is not currently running")
        return True

def check_web_server():
    """Check if web server can access bot."""
    print("\n" + "=" * 70)
    print("3. CHECKING WEB SERVER")
    print("=" * 70)
    
    try:
        from web_server import WebServer
        config = ConfigManager()
        
        web = WebServer(config)
        bot = web.bot_instance
        
        if bot is None:
            print("⚠️  WebServer.bot_instance is None")
            print("\n📋 This means:")
            print("   - Bot hasn't started yet, OR")
            print("   - Bot is starting but hasn't connected")
            print("\n✅ To fix:")
            print("   - Start the bot: python main.py")
            print("   - Wait for 'Bot is ready!' message")
            print("   - Then the web server will see it")
            return True
        else:
            print("✅ WebServer can access bot instance")
            if hasattr(bot, 'guilds'):
                print(f"   Guilds accessible: {len(bot.guilds)}")
            return True
            
    except Exception as e:
        print(f"❌ Error checking web server: {e}")
        return False

def check_health_endpoint():
    """Check health endpoint."""
    print("\n" + "=" * 70)
    print("4. CHECKING HEALTH ENDPOINT")
    print("=" * 70)
    
    try:
        from web_server import WebServer
        config = ConfigManager()
        
        web = WebServer(config)
        
        with web.app.test_client() as client:
            response = client.get('/api/health')
            data = response.get_json()
            
            print("Health Status:")
            print(f"   Web Server: {data.get('web_server', 'unknown')}")
            print(f"   Bot Connected: {data.get('bot_connected', False)}")
            print(f"   Guild Count: {data.get('guild_count', 0)}")
            
            issues = data.get('issues', [])
            if issues:
                print("\n⚠️  Issues found:")
                for issue in issues:
                    print(f"   - {issue}")
            else:
                print("\n✅ No issues found")
            
            return len(issues) == 0
            
    except Exception as e:
        print(f"❌ Error checking health endpoint: {e}")
        import traceback
        traceback.print_exc()
        return False

def print_next_steps():
    """Print next steps."""
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    
    print("\n1. START THE BOT:")
    print("   python main.py")
    
    print("\n2. WAIT FOR THIS MESSAGE:")
    print("   'Bot is ready! Logged in as YourBot#1234'")
    print("   '✅ Bot is in X server(s):'")
    
    print("\n3. IF YOU SEE 'Bot connected but not in any servers':")
    print("   - Bot needs to be added to a Discord server")
    print("   - Go to: https://discord.com/developers/applications")
    print("   - Select your bot → OAuth2 → URL Generator")
    print("   - Check 'bot' scope → Copy URL → Add to server")
    
    print("\n4. OPEN WEB INTERFACE:")
    print("   http://localhost:5000")
    
    print("\n5. CHECK MANUAL SEND TAB:")
    print("   - Should show servers in dropdown")
    print("   - If not, refresh the page")
    
    print("\n6. IF STILL NOT WORKING:")
    print("   python diagnose_guild_detection.py")

def main():
    """Run all checks."""
    print("=" * 70)
    print("BOT GUILD DETECTION - QUICK VERIFICATION")
    print("=" * 70)
    print("\nThis script verifies your bot setup is correct.\n")
    
    results = []
    
    # Run checks
    results.append(check_config())
    results.append(check_bot_instance())
    results.append(check_web_server())
    results.append(check_health_endpoint())
    
    # Print summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if all(results):
        print("\n✅ ALL CHECKS PASSED!")
        print("\nYour configuration looks good. If you're seeing 'NO SERVERS':")
        print("1. Make sure the bot is running: python main.py")
        print("2. Wait for 'Bot is ready!' message")
        print("3. Make sure bot is added to at least one Discord server")
        print("4. Refresh the web interface")
    else:
        print("\n⚠️  SOME CHECKS FAILED")
        print("\nPlease address the issues above.")
    
    print_next_steps()
    
    print("\n" + "=" * 70)
    print("For more help, see:")
    print("  - QUICK_FIX_NO_SERVERS.md")
    print("  - TROUBLESHOOTING_NO_SERVERS.md")
    print("=" * 70)
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
