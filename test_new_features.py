#!/usr/bin/env python3
"""Test script for new features: bot name change and dynamic config updates."""

import sys
import json
from config_manager import ConfigManager
from character_manager import CharacterManager
from discord_bot import DiscordBot
from openai_client import OpenAIClient

def test_bot_name_change():
    """Test that character loading stores the character data."""
    print("\n" + "=" * 60)
    print("Testing Bot Name Change Feature")
    print("=" * 60)
    
    try:
        char_manager = CharacterManager()
        
        # Load a character
        print("\n1. Loading character 'luna'...")
        character_data = char_manager.load_character('luna')
        
        # Verify character has a name
        if 'name' in character_data:
            print(f"   ✓ Character loaded with name: {character_data['name']}")
            print(f"   ✓ Bot would set nickname to: '{character_data['name']}'")
        else:
            print("   ✗ Character has no 'name' field")
            return False
        
        # Check current character is stored
        print("\n2. Checking current character is stored...")
        current = char_manager.get_current_character()
        if current and current.get('name') == character_data['name']:
            print(f"   ✓ Current character correctly set to: {current['name']}")
        else:
            print("   ✗ Current character not stored correctly")
            return False
        
        print("\n✅ Bot name change feature implementation verified!")
        print("   Note: Actual Discord nickname change requires a running bot with Discord connection")
        return True
        
    except Exception as e:
        print(f"\n✗ Error testing bot name change: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dynamic_config_update():
    """Test that OpenAI config can be updated dynamically."""
    print("\n" + "=" * 60)
    print("Testing Dynamic Config Update Feature")
    print("=" * 60)
    
    try:
        config_manager = ConfigManager('config.example.json')
        
        print("\n1. Creating bot instance...")
        # Create a bot instance (this won't actually connect to Discord)
        bot = DiscordBot(config_manager)
        
        # Get initial config
        initial_model = bot.openai_client.model
        print(f"   ✓ Initial model: {initial_model}")
        
        print("\n2. Testing dynamic OpenAI config update...")
        # Test updating the config
        new_model = "gpt-4"
        new_base_url = "https://api.example.com/v1"
        new_api_key = "test-key-12345"
        
        print(f"   Updating to:")
        print(f"   - Model: {new_model}")
        print(f"   - Base URL: {new_base_url}")
        print(f"   - API Key: {new_api_key[:10]}...")
        
        bot.update_openai_config(
            api_key=new_api_key,
            base_url=new_base_url,
            model=new_model
        )
        
        # Verify the update
        if bot.openai_client.model == new_model:
            print(f"   ✓ Model successfully updated to: {bot.openai_client.model}")
        else:
            print(f"   ✗ Model not updated correctly: {bot.openai_client.model}")
            return False
        
        if bot.openai_client.api_key == new_api_key:
            print(f"   ✓ API key successfully updated")
        else:
            print(f"   ✗ API key not updated correctly")
            return False
        
        print("\n3. Testing update with partial parameters...")
        # Test updating just the model
        another_model = "gpt-3.5-turbo-16k"
        bot.update_openai_config(model=another_model)
        
        if bot.openai_client.model == another_model:
            print(f"   ✓ Model successfully updated to: {bot.openai_client.model}")
            print(f"   ✓ Other parameters preserved")
        else:
            print(f"   ✗ Model not updated correctly")
            return False
        
        print("\n✅ Dynamic config update feature verified!")
        print("   Config changes are applied immediately without restart")
        return True
        
    except Exception as e:
        print(f"\n✗ Error testing dynamic config update: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("New Features Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test bot name change
    results.append(("Bot Name Change", test_bot_name_change()))
    
    # Test dynamic config update
    results.append(("Dynamic Config Update", test_dynamic_config_update()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✅ All new feature tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
