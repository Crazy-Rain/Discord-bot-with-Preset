#!/usr/bin/env python3
"""Test script for manual send and context optimization features."""

import sys
from config_manager import ConfigManager
from discord_bot import DiscordBot

def test_token_estimation():
    """Test token estimation and message trimming."""
    print("="*60)
    print("Testing Token Estimation and Message Trimming")
    print("="*60)
    
    config = ConfigManager('config.json')
    bot = DiscordBot(config)
    
    # Test token estimation
    test_text = "This is a test message with some content."
    tokens = bot.estimate_tokens(test_text)
    print(f"\nTest 1: Token Estimation")
    print(f"Text: '{test_text}'")
    print(f"Estimated tokens: {tokens}")
    print(f"Characters: {len(test_text)}")
    print(f"Ratio: ~{len(test_text)/tokens:.1f} chars/token")
    
    # Test message trimming
    print(f"\nTest 2: Message Trimming")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello" * 100},
        {"role": "assistant", "content": "Hi there" * 100},
        {"role": "user", "content": "How are you?" * 100},
        {"role": "assistant", "content": "I'm doing well" * 100},
        {"role": "user", "content": "What's the weather?"},
    ]
    
    original_count = len(messages)
    original_tokens = sum(bot.estimate_tokens(msg['content']) for msg in messages)
    print(f"Original messages: {original_count}")
    print(f"Original tokens: {original_tokens}")
    
    # Trim to 200 tokens
    max_tokens = 200
    trimmed = bot.trim_messages_to_fit(messages, max_tokens)
    trimmed_count = len(trimmed)
    trimmed_tokens = sum(bot.estimate_tokens(msg['content']) for msg in trimmed)
    
    print(f"Max tokens: {max_tokens}")
    print(f"Trimmed messages: {trimmed_count}")
    print(f"Trimmed tokens: {trimmed_tokens}")
    
    # Verify system message is preserved
    system_preserved = any(msg['role'] == 'system' for msg in trimmed)
    if system_preserved:
        print("✓ PASSED - System message preserved")
    else:
        print("✗ FAILED - System message not preserved")
        return False
    
    # Verify we're under the limit
    if trimmed_tokens <= max_tokens:
        print("✓ PASSED - Token limit respected")
    else:
        print(f"✗ FAILED - Exceeded token limit ({trimmed_tokens} > {max_tokens})")
        return False
    
    # Verify messages are in order
    last_msg = trimmed[-1]['content']
    if last_msg == "What's the weather?":
        print("✓ PASSED - Most recent message preserved")
    else:
        print(f"✗ FAILED - Most recent message not preserved: {last_msg}")
        return False
    
    print("\n" + "="*60)
    print("✓ ALL TOKEN TESTS PASSED")
    print("="*60)
    return True

def test_preset_simplification():
    """Test that preset logic uses global default only."""
    print("\n" + "="*60)
    print("Testing Preset Simplification")
    print("="*60)
    
    config = ConfigManager('config.json')
    bot = DiscordBot(config)
    
    # Test get_preset_for_channel always returns default
    channel_id = 12345
    server_id = 67890
    
    preset1 = bot.get_preset_for_channel(channel_id)
    preset2 = bot.get_preset_for_channel(channel_id, server_id)
    preset3 = bot.preset_manager.get_current_preset()
    
    print(f"\nTest: Preset Consistency")
    print(f"Preset for channel {channel_id}: {type(preset1)}")
    print(f"Preset for channel {channel_id} with server {server_id}: {type(preset2)}")
    print(f"Default preset: {type(preset3)}")
    
    if preset1 == preset3 and preset2 == preset3:
        print("✓ PASSED - All presets return the default preset")
    else:
        print("✗ FAILED - Presets are not consistent")
        return False
    
    print("\n" + "="*60)
    print("✓ PRESET SIMPLIFICATION TEST PASSED")
    print("="*60)
    return True

if __name__ == "__main__":
    try:
        success = True
        success = test_token_estimation() and success
        success = test_preset_simplification() and success
        
        if success:
            print("\n" + "="*60)
            print("✓✓✓ ALL TESTS PASSED ✓✓✓")
            print("="*60)
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
