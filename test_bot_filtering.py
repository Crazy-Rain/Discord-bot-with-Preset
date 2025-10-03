#!/usr/bin/env python3
"""Test script to verify bot filtering functionality."""

import sys
from config_manager import ConfigManager
from discord_bot import DiscordBot

def test_bot_filter():
    """Test that the bot applies the filter correctly."""
    print("="*60)
    print("Testing Bot Thinking Filter Integration")
    print("="*60)
    
    # Load config
    config = ConfigManager('config.json')
    
    # Create bot instance
    bot = DiscordBot(config)
    
    # Test filter with enabled=true
    print("\nTest 1: Filter enabled")
    test_response = "Hello! <think>Let me think about this carefully...</think> Here's my answer."
    full, filtered = bot.filter_thinking_tags(test_response)
    
    print(f"Input: {test_response}")
    print(f"Full: {full}")
    print(f"Filtered: {filtered}")
    
    if filtered == "Hello!  Here's my answer.":
        print("✓ PASSED - Thinking tags filtered correctly")
    else:
        print(f"✗ FAILED - Expected 'Hello!  Here's my answer.' but got '{filtered}'")
        return False
    
    # Test multiple tags
    print("\nTest 2: Multiple thinking blocks")
    test_response2 = "Start <think>thought 1</think> middle <think>thought 2</think> end"
    full2, filtered2 = bot.filter_thinking_tags(test_response2)
    
    print(f"Input: {test_response2}")
    print(f"Filtered: {filtered2}")
    
    if filtered2 == "Start  middle  end":
        print("✓ PASSED - Multiple tags filtered correctly")
    else:
        print(f"✗ FAILED - Expected 'Start  middle  end' but got '{filtered2}'")
        return False
    
    # Test with filter disabled
    print("\nTest 3: Filter disabled")
    # Temporarily disable filter
    config.config['thinking_filter']['enabled'] = False
    full3, filtered3 = bot.filter_thinking_tags(test_response)
    
    print(f"Input: {test_response}")
    print(f"Filtered: {filtered3}")
    
    if filtered3 == test_response:
        print("✓ PASSED - Content unchanged when filter disabled")
    else:
        print(f"✗ FAILED - Content should be unchanged but got '{filtered3}'")
        return False
    
    # Test with different tags
    print("\nTest 4: Different custom tags")
    config.config['thinking_filter']['enabled'] = True
    config.config['thinking_filter']['start_tag'] = "<reasoning>"
    config.config['thinking_filter']['end_tag'] = "</reasoning>"
    
    test_response4 = "Text <reasoning>my reasoning here</reasoning> more text"
    full4, filtered4 = bot.filter_thinking_tags(test_response4)
    
    print(f"Input: {test_response4}")
    print(f"Filtered: {filtered4}")
    
    if filtered4 == "Text  more text":
        print("✓ PASSED - Custom tags filtered correctly")
    else:
        print(f"✗ FAILED - Expected 'Text  more text' but got '{filtered4}'")
        return False
    
    print("\n" + "="*60)
    print("✓ ALL BOT FILTER TESTS PASSED")
    print("="*60)
    return True

if __name__ == "__main__":
    try:
        if test_bot_filter():
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
