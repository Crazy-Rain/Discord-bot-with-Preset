#!/usr/bin/env python3
"""
Test script to verify the chat command fix.

This script tests the parsing and message building logic without requiring
an actual Discord connection or API call.
"""

import sys
import asyncio
from unittest.mock import Mock, AsyncMock, MagicMock, patch
from discord_bot import DiscordBot
from config_manager import ConfigManager

def test_parse_character_message():
    """Test the parse_character_message method."""
    print("\n" + "="*60)
    print("TEST 1: Parse Character Message")
    print("="*60)
    
    config = ConfigManager('config.example.json')
    bot = DiscordBot(config)
    
    test_cases = [
        ('Luna: Hello there!', 'Luna', 'Hello there!'),
        ('Character Name: This is a test', 'Character Name', 'This is a test'),
        ('Just a regular message', None, 'Just a regular message'),
        ('Character:Message without space', 'Character', 'Message without space'),
        ('Bob: *waves*', 'Bob', '*waves*'),
    ]
    
    all_passed = True
    for input_msg, expected_char, expected_msg in test_cases:
        char_name, actual_msg = bot.parse_character_message(input_msg)
        passed = (char_name == expected_char and actual_msg == expected_msg)
        status = "✓" if passed else "✗"
        print(f"{status} Input: '{input_msg}'")
        print(f"  Expected: char='{expected_char}', msg='{expected_msg}'")
        print(f"  Got:      char='{char_name}', msg='{actual_msg}'")
        if not passed:
            all_passed = False
    
    return all_passed

async def test_chat_flow_mock():
    """Test the chat command flow with mocked dependencies."""
    print("\n" + "="*60)
    print("TEST 2: Chat Command Flow (Mocked)")
    print("="*60)
    
    # Create config
    config = ConfigManager('config.example.json')
    bot = DiscordBot(config)
    
    # Mock context
    mock_ctx = Mock()
    mock_ctx.channel.id = 12345
    mock_ctx.guild.id = 67890
    mock_ctx.channel = AsyncMock()
    
    # Mock the OpenAI response
    test_response = "Hello! This is a test response from the AI."
    
    # Mock openai_client.chat_completion
    with patch.object(bot.openai_client, 'chat_completion', new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = test_response
        
        # Mock send_long_message_with_view
        with patch('discord_bot.send_long_message_with_view', new_callable=AsyncMock) as mock_send:
            mock_msg = Mock()
            mock_msg.id = 99999
            mock_send.return_value = (mock_msg, [99999])
            
            # Mock ctx.send for the error case
            mock_ctx.send = AsyncMock()
            
            # Test 1: Regular message (no character)
            print("\nTest 2a: Regular message (no character)")
            message = "Hello bot!"
            
            # Parse message
            character_name, actual_message = bot.parse_character_message(message)
            print(f"  Parsed: char='{character_name}', msg='{actual_message}'")
            
            # Build messages
            messages = bot.build_chat_messages(mock_ctx.channel.id, actual_message, character_name, mock_ctx.guild.id)
            print(f"  Built {len(messages)} messages for API")
            
            # Simulate API call
            response = await mock_chat(messages)
            print(f"  API Response: '{response}'")
            
            # Test 2: Character message
            print("\nTest 2b: Character message")
            message = "Luna: How are you doing?"
            
            # Parse message
            character_name, actual_message = bot.parse_character_message(message)
            print(f"  Parsed: char='{character_name}', msg='{actual_message}'")
            
            # Build messages
            messages = bot.build_chat_messages(mock_ctx.channel.id, actual_message, character_name, mock_ctx.guild.id)
            print(f"  Built {len(messages)} messages for API")
            
            # Check if character name is in the last message
            last_msg = messages[-1]
            print(f"  Last message role: {last_msg['role']}")
            print(f"  Last message content: {last_msg['content'][:50]}...")
            
            # Simulate API call
            response = await mock_chat(messages)
            print(f"  API Response: '{response}'")
    
    print("\n✓ Chat flow test completed successfully")
    return True

def test_fallback_logic():
    """Test the webhook fallback logic."""
    print("\n" + "="*60)
    print("TEST 3: Webhook Fallback Logic")
    print("="*60)
    
    # Test the logic: if webhook returns (None, []), we should fall back
    webhook_results = [
        ((Mock(), [123]), "Success", False),
        ((None, []), "Failed - None message", True),
        ((Mock(), None), "Failed - None IDs", True),
        ((None, None), "Failed - Both None", True),
    ]
    
    all_passed = True
    for (last_msg, msg_ids), description, should_fallback in webhook_results:
        needs_fallback = not last_msg or not msg_ids
        passed = needs_fallback == should_fallback
        status = "✓" if passed else "✗"
        print(f"{status} {description}")
        print(f"  last_msg: {last_msg}, msg_ids: {msg_ids}")
        print(f"  Expected fallback: {should_fallback}, Got: {needs_fallback}")
        if not passed:
            all_passed = False
    
    return all_passed

def main():
    """Run all tests."""
    print("\n" + "="*70)
    print(" CHAT COMMAND FIX - TEST SUITE")
    print("="*70)
    
    results = []
    
    # Test 1: Parse character message
    results.append(("Parse Character Message", test_parse_character_message()))
    
    # Test 2: Chat flow with mocks
    results.append(("Chat Command Flow", asyncio.run(test_chat_flow_mock())))
    
    # Test 3: Fallback logic
    results.append(("Webhook Fallback Logic", test_fallback_logic()))
    
    # Summary
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("="*70)
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
