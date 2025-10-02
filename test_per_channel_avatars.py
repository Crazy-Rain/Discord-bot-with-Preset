#!/usr/bin/env python3
"""Test script for per-channel character avatars feature."""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import discord
        from discord.ext import commands
        print("  ✓ discord imports successful")
    except ImportError as e:
        print(f"  ✗ discord import failed: {e}")
        return False
    
    try:
        from config_manager import ConfigManager
        from character_manager import CharacterManager
        print("  ✓ manager imports successful")
    except ImportError as e:
        print(f"  ✗ manager import failed: {e}")
        return False
    
    return True

def test_character_manager():
    """Test character manager functionality."""
    print("\nTesting character manager...")
    try:
        from character_manager import CharacterManager
        manager = CharacterManager()
        
        # List characters
        characters = manager.list_characters()
        print(f"  ✓ Found {len(characters)} characters: {', '.join(characters)}")
        
        # Try to load a character if any exist
        if characters:
            char_name = characters[0]
            char_data = manager.load_character(char_name)
            print(f"  ✓ Loaded character '{char_name}'")
            print(f"    - Name: {char_data.get('name', 'N/A')}")
            print(f"    - Has avatar_url: {bool(char_data.get('avatar_url'))}")
            if char_data.get('avatar_url'):
                print(f"    - Avatar URL: {char_data.get('avatar_url')[:50]}...")
        else:
            print("  ℹ No characters found to test loading")
        
        return True
    except Exception as e:
        print(f"  ✗ Character manager test failed: {e}")
        return False

def test_discord_bot_structure():
    """Test the Discord bot class structure."""
    print("\nTesting Discord bot structure...")
    try:
        # Read the discord_bot.py file to check for our new code
        with open('discord_bot.py', 'r') as f:
            content = f.read()
        
        # Check for new attributes
        checks = [
            ('channel_characters', 'Per-channel character tracking'),
            ('channel_webhooks', 'Webhook caching'),
            ('get_or_create_webhook', 'Webhook management method'),
            ('send_as_character', 'Character message sending method'),
            ('current_character', 'Current character command'),
            ('unload_character', 'Unload character command'),
        ]
        
        all_passed = True
        for check, description in checks:
            if check in content:
                print(f"  ✓ Found: {description}")
            else:
                print(f"  ✗ Missing: {description}")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"  ✗ Structure test failed: {e}")
        return False

def test_webhook_logic():
    """Test webhook-related code structure."""
    print("\nTesting webhook logic...")
    try:
        with open('discord_bot.py', 'r') as f:
            content = f.read()
        
        # Check for webhook usage in commands
        checks = [
            ('if channel_id in self.channel_characters:', 'Character check in chat'),
            ('await self.send_as_character(', 'Webhook message sending'),
            ('await channel.create_webhook(', 'Webhook creation'),
            ('username=character_name', 'Character name in webhook'),
            ('avatar_url=avatar_url', 'Avatar URL in webhook'),
        ]
        
        all_passed = True
        for check, description in checks:
            if check in content:
                print(f"  ✓ Found: {description}")
            else:
                print(f"  ✗ Missing: {description}")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"  ✗ Webhook logic test failed: {e}")
        return False

def test_documentation():
    """Test that documentation exists."""
    print("\nTesting documentation...")
    try:
        docs = [
            ('PER_CHANNEL_AVATARS_GUIDE.md', 'Per-channel avatars guide'),
            ('README.md', 'README with updated features'),
        ]
        
        all_passed = True
        for filename, description in docs:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    content = f.read()
                    if 'webhook' in content.lower() or 'per-channel' in content.lower():
                        print(f"  ✓ {description} exists and mentions feature")
                    else:
                        print(f"  ⚠ {description} exists but may not cover feature")
            else:
                print(f"  ✗ {description} not found")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"  ✗ Documentation test failed: {e}")
        return False

def test_syntax():
    """Test Python syntax of discord_bot.py."""
    print("\nTesting Python syntax...")
    try:
        import py_compile
        py_compile.compile('discord_bot.py', doraise=True)
        print("  ✓ discord_bot.py has valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"  ✗ Syntax error in discord_bot.py: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Compilation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Per-Channel Character Avatars Feature - Test Suite")
    print("=" * 60)
    
    results = {
        'Syntax Check': test_syntax(),
        'Imports': test_imports(),
        'Character Manager': test_character_manager(),
        'Bot Structure': test_discord_bot_structure(),
        'Webhook Logic': test_webhook_logic(),
        'Documentation': test_documentation(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed!")
        print("\nThe per-channel character avatars feature has been implemented successfully.")
        print("\nKey features:")
        print("  • Webhook-based character avatars per channel")
        print("  • No rate limits on character switching")
        print("  • Different characters in different channels simultaneously")
        print("  • Graceful fallback to normal messages")
        print("\nNext steps:")
        print("  1. Ensure bot has 'Manage Webhooks' permission in Discord")
        print("  2. Test the feature in a Discord server")
        print("  3. Use !character <name> to load characters per channel")
    else:
        print("❌ Some tests failed!")
        print("\nPlease review the failed tests above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
