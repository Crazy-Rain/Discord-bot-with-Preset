#!/usr/bin/env python3
"""Test that manual send endpoint works correctly with the fix."""

import sys
import json
from web_server import WebServer
from config_manager import ConfigManager

# Mock classes
class MockUser:
    def __init__(self):
        self.name = 'TestBot'
    
    def __str__(self):
        return 'TestBot#1234'

class MockMessage:
    def __init__(self, msg_id):
        self.id = msg_id

class MockWebhook:
    def __init__(self):
        pass
    
    async def send(self, **kwargs):
        """Mock webhook send."""
        return MockMessage(999999)

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
        self.user = MockUser()
    
    def get_channel(self, channel_id):
        """Search for channel in all guilds."""
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.id == channel_id:
                    return channel
        return None
    
    async def get_or_create_webhook(self, channel):
        """Mock webhook creation."""
        return MockWebhook()
    
    async def send_as_character(self, channel, content, character_data, view=None):
        """Mock send_as_character method."""
        # Simulate successful message send
        return MockMessage(123456), [123456]


def test_manual_send_with_string_id():
    """Test manual send endpoint with string channel ID (as sent from frontend)."""
    print("\n=== Test: Manual Send with String Channel ID ===")
    
    # Create bot with the specified IDs from the issue
    guild = MockGuild(
        1011703948526239814,  # Server ID from issue
        'Test Server',
        [MockChannel(1426231081182695636, 'test-channel')]  # Channel ID from issue
    )
    
    bot = MockBot([guild])
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=bot)
    
    # Test the endpoint with string ID (as sent from frontend)
    with web_server.app.test_client() as client:
        response = client.post('/api/manual_send',
            json={
                'channel_id': '1426231081182695636',  # String format
                'character_name': 'aria',
                'message': 'Test message from manual send'
            },
            content_type='application/json'
        )
        
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json['status'] == 'success', f"Expected success, got {response.json}"
        print("  ✓ Test passed - manual send works with string channel ID")


def test_manual_send_with_int_id():
    """Test manual send endpoint with integer channel ID."""
    print("\n=== Test: Manual Send with Integer Channel ID ===")
    
    guild = MockGuild(
        1011703948526239814,
        'Test Server',
        [MockChannel(1426231081182695636, 'test-channel')]
    )
    
    bot = MockBot([guild])
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=bot)
    
    with web_server.app.test_client() as client:
        response = client.post('/api/manual_send',
            json={
                'channel_id': 1426231081182695636,  # Integer format
                'character_name': 'aria',
                'message': 'Test message'
            },
            content_type='application/json'
        )
        
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json['status'] == 'success', f"Expected success, got {response.json}"
        print("  ✓ Test passed - manual send works with integer channel ID")


def test_manual_send_channel_not_found():
    """Test manual send endpoint when channel doesn't exist."""
    print("\n=== Test: Manual Send with Non-existent Channel ===")
    
    guild = MockGuild(
        1011703948526239814,
        'Test Server',
        [MockChannel(1426231081182695636, 'test-channel')]
    )
    
    bot = MockBot([guild])
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=bot)
    
    with web_server.app.test_client() as client:
        response = client.post('/api/manual_send',
            json={
                'channel_id': '9999999999999999',  # Non-existent channel
                'character_name': 'aria',
                'message': 'Test message'
            },
            content_type='application/json'
        )
        
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json}")
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        assert 'not found' in response.json['message'].lower(), f"Expected 'not found' in message"
        print("  ✓ Test passed - correct error when channel not found")


def test_manual_send_missing_fields():
    """Test manual send endpoint with missing required fields."""
    print("\n=== Test: Manual Send with Missing Fields ===")
    
    guild = MockGuild(
        1011703948526239814,
        'Test Server',
        [MockChannel(1426231081182695636, 'test-channel')]
    )
    
    bot = MockBot([guild])
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=bot)
    
    with web_server.app.test_client() as client:
        # Test missing channel_id
        response = client.post('/api/manual_send',
            json={
                'character_name': 'aria',
                'message': 'Test message'
            },
            content_type='application/json'
        )
        
        print(f"  Status Code (missing channel_id): {response.status_code}")
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print("  ✓ Correctly rejects missing channel_id")
        
        # Test missing character_name
        response = client.post('/api/manual_send',
            json={
                'channel_id': '1426231081182695636',
                'message': 'Test message'
            },
            content_type='application/json'
        )
        
        print(f"  Status Code (missing character_name): {response.status_code}")
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print("  ✓ Correctly rejects missing character_name")
        
        # Test missing message
        response = client.post('/api/manual_send',
            json={
                'channel_id': '1426231081182695636',
                'character_name': 'aria'
            },
            content_type='application/json'
        )
        
        print(f"  Status Code (missing message): {response.status_code}")
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print("  ✓ Correctly rejects missing message")


def test_manual_send_no_bot():
    """Test manual send endpoint when bot is not running."""
    print("\n=== Test: Manual Send with No Bot Instance ===")
    
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=None)
    
    with web_server.app.test_client() as client:
        response = client.post('/api/manual_send',
            json={
                'channel_id': '1426231081182695636',
                'character_name': 'aria',
                'message': 'Test message'
            },
            content_type='application/json'
        )
        
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json}")
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert 'not running' in response.json['message'].lower(), f"Expected 'not running' in message"
        print("  ✓ Test passed - correct error when bot not running")


if __name__ == '__main__':
    print("=" * 70)
    print("MANUAL SEND FIX VERIFICATION TESTS")
    print("=" * 70)
    print("\nTesting fix for: POST /api/manual_send HTTP/1.1 400 error")
    print("Server ID: 1011703948526239814")
    print("Channel ID: 1426231081182695636")
    
    try:
        test_manual_send_with_string_id()
        test_manual_send_with_int_id()
        test_manual_send_channel_not_found()
        test_manual_send_missing_fields()
        test_manual_send_no_bot()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED - Manual Send Fix Verified")
        print("=" * 70)
        print("\nThe /api/manual_send endpoint now works correctly!")
        print("- Accepts both string and integer channel IDs")
        print("- Properly handles async send_as_character method")
        print("- Returns appropriate error codes for edge cases")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
