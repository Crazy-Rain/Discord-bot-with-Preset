#!/usr/bin/env python3
"""Test suite for Issue #XX: Config update and lorebook integration bugs."""

import sys
import json
import tempfile
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_manager import ConfigManager
from discord_bot import DiscordBot
from lorebook_manager import LorebookManager

def test_config_update_preserves_api_key():
    """
    Test that updating config via web interface preserves API key.
    
    Bug: config_manager.update_config() used shallow dict.update() which 
    replaced entire nested dicts, causing API key to be lost when hidden.
    
    Fix: Implemented deep_update() for recursive dict merging.
    """
    print("\n" + "=" * 70)
    print("TEST: Config Update Preserves API Key")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_data = {
            'discord_token': 'test-token',
            'openai_config': {
                'api_key': 'sk-original-key',
                'base_url': 'https://api.openai.com/v1',
                'model': 'gpt-3.5-turbo'
            }
        }
        json.dump(config_data, f, indent=2)
        temp_config_path = f.name
    
    try:
        config_manager = ConfigManager(temp_config_path)
        bot = DiscordBot(config_manager)
        
        # Simulate web update with hidden API key
        data = {
            'openai_config': {
                # api_key is missing because it was '***HIDDEN***' and deleted
                'base_url': 'https://new-proxy.com/v1',
                'model': 'gpt-4'
            }
        }
        
        config_manager.update_config(data)
        
        # Verify API key is preserved
        api_key = config_manager.get('openai_config.api_key')
        base_url = config_manager.get('openai_config.base_url')
        model = config_manager.get('openai_config.model')
        
        assert api_key == 'sk-original-key', f"API key lost! Expected 'sk-original-key', got '{api_key}'"
        assert base_url == 'https://new-proxy.com/v1', f"Base URL not updated! Got '{base_url}'"
        assert model == 'gpt-4', f"Model not updated! Got '{model}'"
        
        print("✅ PASS: Config update preserves API key")
        return True
        
    finally:
        os.unlink(temp_config_path)

def test_bot_receives_updated_config():
    """
    Test that bot's OpenAI client is updated when config changes.
    """
    print("\n" + "=" * 70)
    print("TEST: Bot Receives Updated Config")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_data = {
            'openai_config': {
                'api_key': 'sk-test-key',
                'base_url': 'https://api.openai.com/v1',
                'model': 'gpt-3.5-turbo'
            }
        }
        json.dump(config_data, f, indent=2)
        temp_config_path = f.name
    
    try:
        config_manager = ConfigManager(temp_config_path)
        bot = DiscordBot(config_manager)
        
        # Update config
        new_url = 'https://new-proxy.com/v1'
        new_model = 'gpt-4'
        bot.update_openai_config(base_url=new_url, model=new_model)
        
        # Verify bot client is updated
        client = bot.get_openai_client_for_channel(channel_id=12345)
        
        assert new_url.rstrip('/') in str(client.client.base_url), \
            f"Bot not using new URL! Got {client.client.base_url}"
        assert client.model == new_model, \
            f"Bot not using new model! Got {client.model}"
        
        print("✅ PASS: Bot receives updated config")
        return True
        
    finally:
        os.unlink(temp_config_path)

def test_lorebook_constant_entries():
    """
    Test that constant (always active) lorebook entries are included.
    """
    print("\n" + "=" * 70)
    print("TEST: Lorebook Constant Entries")
    print("=" * 70)
    
    lorebook_manager = LorebookManager()
    
    # Create a lorebook with constant entry
    lorebook_manager.create_lorebook(
        name="Test Lore",
        enabled=True,
        linked_characters=None
    )
    
    lorebook_manager.add_or_update_entry(
        key="Constant Entry",
        content="This should always be included.",
        activation_type="constant",
        lorebook_name="Test Lore"
    )
    
    # Get system prompt
    prompt = lorebook_manager.get_system_prompt_section(
        relevant_text="anything",
        character_name=None
    )
    
    assert "Constant Entry" in prompt, "Constant entry not included!"
    
    print("✅ PASS: Constant entries are included")
    return True

def test_lorebook_character_filtering():
    """
    Test that character-linked lorebooks are filtered correctly.
    """
    print("\n" + "=" * 70)
    print("TEST: Lorebook Character Filtering")
    print("=" * 70)
    
    lorebook_manager = LorebookManager()
    
    # Create global lorebook
    lorebook_manager.create_lorebook(
        name="Global",
        enabled=True,
        linked_characters=None
    )
    lorebook_manager.add_or_update_entry(
        key="Global Entry",
        content="Global information.",
        activation_type="constant",
        lorebook_name="Global"
    )
    
    # Create character-linked lorebook
    lorebook_manager.create_lorebook(
        name="Luna Lore",
        enabled=True,
        linked_characters=["Luna"]
    )
    lorebook_manager.add_or_update_entry(
        key="Luna Entry",
        content="Luna's information.",
        activation_type="constant",
        lorebook_name="Luna Lore"
    )
    
    # Test with Luna character
    prompt_luna = lorebook_manager.get_system_prompt_section(
        relevant_text="test",
        character_name="Luna"
    )
    assert "Global Entry" in prompt_luna, "Global entry not included for Luna!"
    assert "Luna Entry" in prompt_luna, "Luna entry not included for Luna!"
    
    # Test with different character
    prompt_alice = lorebook_manager.get_system_prompt_section(
        relevant_text="test",
        character_name="Alice"
    )
    assert "Global Entry" in prompt_alice, "Global entry not included for Alice!"
    assert "Luna Entry" not in prompt_alice, "Luna entry incorrectly included for Alice!"
    
    print("✅ PASS: Character filtering works correctly")
    return True

def test_lorebook_enabled_disabled():
    """
    Test that disabled lorebooks are excluded.
    """
    print("\n" + "=" * 70)
    print("TEST: Lorebook Enabled/Disabled Filtering")
    print("=" * 70)
    
    lorebook_manager = LorebookManager()
    
    # Create enabled lorebook
    lorebook_manager.create_lorebook(
        name="Enabled",
        enabled=True
    )
    lorebook_manager.add_or_update_entry(
        key="Enabled Entry",
        content="This is enabled.",
        activation_type="constant",
        lorebook_name="Enabled"
    )
    
    # Create disabled lorebook
    lorebook_manager.create_lorebook(
        name="Disabled",
        enabled=False
    )
    lorebook_manager.add_or_update_entry(
        key="Disabled Entry",
        content="This is disabled.",
        activation_type="constant",
        lorebook_name="Disabled"
    )
    
    # Get system prompt
    prompt = lorebook_manager.get_system_prompt_section()
    
    assert "Enabled Entry" in prompt, "Enabled entry not included!"
    assert "Disabled Entry" not in prompt, "Disabled entry incorrectly included!"
    
    print("✅ PASS: Disabled lorebooks are excluded")
    return True

def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("ISSUE FIX VERIFICATION TESTS")
    print("=" * 70)
    
    # Clean up lorebook directory before tests
    import shutil
    lorebook_dir = os.path.join(os.path.dirname(__file__), 'lorebook')
    if os.path.exists(lorebook_dir):
        shutil.rmtree(lorebook_dir)
    
    tests = [
        ("Config Update Preserves API Key", test_config_update_preserves_api_key),
        ("Bot Receives Updated Config", test_bot_receives_updated_config),
        ("Lorebook Constant Entries", test_lorebook_constant_entries),
        ("Lorebook Character Filtering", test_lorebook_character_filtering),
        ("Lorebook Enabled/Disabled", test_lorebook_enabled_disabled),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            # Clean up lorebook between tests
            if os.path.exists(lorebook_dir):
                shutil.rmtree(lorebook_dir)
        except Exception as e:
            print(f"❌ FAIL: {test_name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    print(f"\n{'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
