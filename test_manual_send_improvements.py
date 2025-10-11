#!/usr/bin/env python3
"""Test manual send improvements - validates error handling and data validation order."""

import sys
import json

# Mock classes to simulate Discord bot
class MockChannel:
    def __init__(self, channel_id, name):
        self.id = channel_id
        self.name = name

class MockGuild:
    def __init__(self, guild_id, name, channels):
        self.id = guild_id
        self.name = name
        self.text_channels = channels

class MockBot:
    def __init__(self, guilds):
        self.guilds = guilds
    
    def get_channel(self, channel_id):
        """Search for channel in all guilds."""
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.id == channel_id:
                    return channel
        return None
    
    async def send_as_character(self, channel, content, character_data, view=None):
        """Mock send_as_character method."""
        class MockMessage:
            id = 123456
        return MockMessage(), [123456]

class MockUser:
    name = 'TestBot'

def test_data_validation_before_bot_check():
    """Test that data validation happens before bot check."""
    print("\n=== Test: Data Validation Before Bot Check ===")
    
    from web_server import WebServer
    from config_manager import ConfigManager
    
    # Create web server with NO bot instance
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=None)
    
    with web_server.app.test_client() as client:
        # Test 1: Missing channel_id - should get 400 "Missing required fields"
        # NOT "Bot is not running"
        response = client.post('/api/manual_send',
            json={
                'character_name': 'aria',
                'message': 'Test message'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert 'missing' in response.json['message'].lower(), \
            f"Expected 'missing' error, got: {response.json['message']}"
        print(f"  ✓ Missing data returns correct error: {response.json['message']}")
        
        # Test 2: Invalid channel_id format - should get 400 "Invalid channel_id format"
        # NOT "Bot is not running"
        response = client.post('/api/manual_send',
            json={
                'channel_id': 'not_a_number',
                'character_name': 'aria',
                'message': 'Test message'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert 'invalid' in response.json['message'].lower(), \
            f"Expected 'invalid' error, got: {response.json['message']}"
        print(f"  ✓ Invalid format returns correct error: {response.json['message']}")
        
        # Test 3: Valid data but no bot - should get 400 "Bot is not running"
        response = client.post('/api/manual_send',
            json={
                'channel_id': '123456789',
                'character_name': 'aria',
                'message': 'Test message'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert 'not running' in response.json['message'].lower(), \
            f"Expected 'not running' error, got: {response.json['message']}"
        print(f"  ✓ Bot check happens after validation: {response.json['message']}")

def test_bot_instance_property_robustness():
    """Test that bot_instance property handles errors gracefully."""
    print("\n=== Test: Bot Instance Property Robustness ===")
    
    from web_server import WebServer
    from config_manager import ConfigManager
    
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=None)
    
    # The bot_instance property should return None if main.bot_instance doesn't exist
    # and should not crash
    bot = web_server.bot_instance
    print(f"  ✓ bot_instance property returns: {bot}")
    assert bot is None or hasattr(bot, 'get_channel'), \
        f"bot_instance should be None or a valid bot, got: {type(bot)}"

def test_improved_error_messages():
    """Test that error messages are helpful and specific."""
    print("\n=== Test: Improved Error Messages ===")
    
    from web_server import WebServer
    from config_manager import ConfigManager
    
    # Create bot with channel
    guild = MockGuild(1011703948526239814, 'Test Server',
                     [MockChannel(1426231081182695636, 'test-channel')])
    bot = MockBot([guild])
    
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=bot)
    
    with web_server.app.test_client() as client:
        # Test 404 error message for non-existent channel
        response = client.post('/api/manual_send',
            json={
                'channel_id': '9999999999',
                'character_name': 'aria',
                'message': 'Test'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        message = response.json['message']
        print(f"  ✓ 404 error message: {message}")
        
        # Check that message provides helpful guidance
        assert 'bot is connected' in message.lower() or 'channel id' in message.lower(), \
            "Error message should provide helpful guidance"

if __name__ == '__main__':
    print("=" * 70)
    print("MANUAL SEND IMPROVEMENTS TEST")
    print("=" * 70)
    print("\nTesting improvements to manual send error handling...")
    
    try:
        test_data_validation_before_bot_check()
        test_bot_instance_property_robustness()
        test_improved_error_messages()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED - Manual Send Improvements Verified")
        print("=" * 70)
        print("\nImprovements validated:")
        print("- Data validation happens before bot check ✓")
        print("- Bot instance property is robust ✓")
        print("- Error messages are helpful and specific ✓")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
