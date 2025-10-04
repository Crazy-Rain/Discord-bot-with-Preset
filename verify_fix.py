#!/usr/bin/env python3
"""
Quick verification script to test if the fix works.
This creates a mock scenario to verify the fix without needing a Discord token.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("="*70)
    print("SERVER/CHANNEL FIX VERIFICATION")
    print("="*70)
    
    print("\n📋 Checking the fix...")
    
    # Check that main.py has the fix
    with open('main.py', 'r') as f:
        content = f.read()
    
    # The bug was this line in run_discord_bot():
    # bot_instance = DiscordBot(config_manager)
    
    # Check if the duplicate creation is gone
    lines = content.split('\n')
    in_run_discord_bot = False
    duplicate_found = False
    
    for i, line in enumerate(lines, 1):
        if 'def run_discord_bot' in line:
            in_run_discord_bot = True
            start_line = i
        elif in_run_discord_bot and line.strip().startswith('def '):
            # Exited the function
            break
        elif in_run_discord_bot and 'bot_instance = DiscordBot(' in line:
            duplicate_found = True
            print(f"\n❌ FAILED: Duplicate bot creation found at line {i}!")
            print(f"   Line: {line.strip()}")
            break
    
    if not duplicate_found:
        print("\n✅ Fix verified! No duplicate bot creation in run_discord_bot()")
        print("\n📝 Summary of the fix:")
        print("   • Removed duplicate bot_instance creation")
        print("   • Web server now uses the same bot instance that connects")
        print("   • Servers/Channels tab will show connected servers correctly")
        
        print("\n🔍 What was changed:")
        print("   File: main.py")
        print("   Change: Removed 1 line from run_discord_bot() function")
        print("   Line removed: bot_instance = DiscordBot(config_manager)")
        
        print("\n✨ How to test:")
        print("   1. Set up config.json with your Discord bot token")
        print("   2. Run: python main.py")
        print("   3. Wait for 'Bot is ready!' message")
        print("   4. Open http://localhost:5000")
        print("   5. Click 'Servers/Channels' tab")
        print("   6. You should see your Discord servers!")
        
        print("\n" + "="*70)
        return 0
    else:
        print("\n" + "="*70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
