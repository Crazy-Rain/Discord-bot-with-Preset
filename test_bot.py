#!/usr/bin/env python3
"""Test script to verify Discord bot functionality."""

import sys
import json

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from config_manager import ConfigManager
        from preset_manager import PresetManager
        from character_manager import CharacterManager
        from openai_client import OpenAIClient
        from discord_bot import DiscordBot
        from web_server import WebServer
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test configuration management."""
    print("\nTesting configuration...")
    try:
        from config_manager import ConfigManager
        config = ConfigManager('config.example.json')
        
        # Test getting values
        token = config.get('discord_token')
        api_key = config.get('openai_config.api_key')
        model = config.get('openai_config.model')
        
        print(f"✓ Discord token: {token[:20]}...")
        print(f"✓ API key: {api_key[:20]}...")
        print(f"✓ Model: {model}")
        return True
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False

def test_presets():
    """Test preset management."""
    print("\nTesting presets...")
    try:
        from preset_manager import PresetManager
        pm = PresetManager()
        
        # List presets
        presets = pm.list_presets()
        print(f"✓ Found {len(presets)} presets: {', '.join(presets)}")
        
        # Load a preset
        if presets:
            preset = pm.load_preset(presets[0])
            print(f"✓ Loaded preset '{presets[0]}':")
            print(f"  - Temperature: {preset.get('temperature')}")
            print(f"  - Max tokens: {preset.get('max_tokens')}")
            print(f"  - System prompt: {preset.get('system_prompt', '')[:50]}...")
        
        return True
    except Exception as e:
        print(f"✗ Preset error: {e}")
        return False

def test_characters():
    """Test character management."""
    print("\nTesting characters...")
    try:
        from character_manager import CharacterManager
        cm = CharacterManager()
        
        # List characters
        characters = cm.list_characters()
        print(f"✓ Found {len(characters)} characters: {', '.join(characters)}")
        
        # Load a character
        if characters:
            char = cm.load_character(characters[0])
            print(f"✓ Loaded character '{characters[0]}':")
            print(f"  - Name: {char.get('name')}")
            print(f"  - Personality: {char.get('personality', '')[:50]}...")
            
            # Get system prompt
            prompt = cm.get_character_system_prompt()
            print(f"✓ Generated system prompt ({len(prompt)} chars)")
            if len(prompt) > 0:
                print(f"  Preview: {prompt[:100]}...")
        
        return True
    except Exception as e:
        print(f"✗ Character error: {e}")
        return False

def test_openai_client():
    """Test OpenAI client initialization."""
    print("\nTesting OpenAI client...")
    try:
        from openai_client import OpenAIClient
        client = OpenAIClient(
            api_key="test-key",
            base_url="https://api.openai.com/v1",
            model="gpt-3.5-turbo"
        )
        print("✓ OpenAI client initialized successfully")
        print(f"  - Model: {client.model}")
        return True
    except Exception as e:
        print(f"✗ OpenAI client error: {e}")
        return False

def test_web_server():
    """Test web server initialization."""
    print("\nTesting web server...")
    try:
        from config_manager import ConfigManager
        from web_server import WebServer
        
        config = ConfigManager('config.example.json')
        server = WebServer(config)
        print("✓ Web server initialized successfully")
        print("  - Flask app created")
        print("  - Routes configured")
        return True
    except Exception as e:
        print(f"✗ Web server error: {e}")
        return False

def test_discord_bot():
    """Test Discord bot initialization."""
    print("\nTesting Discord bot...")
    try:
        from config_manager import ConfigManager
        from discord_bot import DiscordBot
        
        config = ConfigManager('config.example.json')
        bot = DiscordBot(config)
        print("✓ Discord bot initialized successfully")
        print(f"  - Prefix: {bot.command_prefix}")
        print(f"  - Intents configured")
        return True
    except Exception as e:
        print(f"✗ Discord bot error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Discord Bot with Presets - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Presets", test_presets),
        ("Characters", test_characters),
        ("OpenAI Client", test_openai_client),
        ("Web Server", test_web_server),
        ("Discord Bot", test_discord_bot),
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed!")
        print("\nTo run the bot:")
        print("  1. Copy config.example.json to config.json")
        print("  2. Update with your Discord token and API settings")
        print("  3. Run: python main.py")
        print("  4. Access web UI at http://localhost:5000")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
