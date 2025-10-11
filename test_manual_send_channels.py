#!/usr/bin/env python3
"""Test for the manual_send/channels API endpoint fix."""
import sys
import json
from unittest.mock import Mock, MagicMock
from web_server import WebServer
from config_manager import ConfigManager

class MockGuild:
    """Mock Discord Guild object."""
    def __init__(self, guild_id, name, has_text_channels=True, text_channels_is_none=False):
        self.id = guild_id
        self.name = name
        if not has_text_channels:
            # Simulate missing text_channels attribute
            pass
        elif text_channels_is_none:
            self.text_channels = None
        else:
            # Create mock text channels
            self.text_channels = [
                MockChannel(f"{guild_id}001", "general"),
                MockChannel(f"{guild_id}002", "random"),
            ]

class MockChannel:
    """Mock Discord Channel object."""
    def __init__(self, channel_id, name):
        self.id = channel_id
        self.name = name

class MockBot:
    """Mock Discord Bot instance."""
    def __init__(self, guilds):
        self.guilds = guilds

def test_manual_send_channels_normal():
    """Test that normal guilds return channels correctly."""
    print("Test: Manual send channels with normal guild...")
    
    # Create mock bot with normal guild
    guild = MockGuild(123456, "Test Server")
    bot = MockBot([guild])
    
    # Create web server
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, bot)
    
    # Test the endpoint
    with web_server.app.test_client() as client:
        response = client.get('/api/manual_send/channels')
        data = json.loads(response.data)
        
        assert 'channels' in data, "Response should have 'channels' key"
        assert len(data['channels']) == 2, f"Should have 2 channels, got {len(data['channels'])}"
        
        # Check channel structure
        channel = data['channels'][0]
        assert 'id' in channel, "Channel should have 'id' field"
        assert 'name' in channel, "Channel should have 'name' field"
        assert 'server_name' in channel, "Channel should have 'server_name' field"
        assert 'server_id' in channel, "Channel should have 'server_id' field"
        
        assert channel['server_name'] == 'Test Server', f"Server name should be 'Test Server', got {channel['server_name']}"
        
    print("✓ Manual send channels with normal guild works correctly")

def test_manual_send_channels_with_none_text_channels():
    """Test that guilds with None text_channels return empty list."""
    print("Test: Manual send channels with None text_channels...")
    
    # Create mock bot with guild where text_channels is None
    guild = MockGuild(123457, "Broken Server", text_channels_is_none=True)
    bot = MockBot([guild])
    
    # Create web server
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, bot)
    
    # Test the endpoint
    with web_server.app.test_client() as client:
        response = client.get('/api/manual_send/channels')
        data = json.loads(response.data)
        
        assert 'channels' in data, "Response should have 'channels' key"
        assert len(data['channels']) == 0, f"Should have 0 channels when text_channels is None, got {len(data['channels'])}"
        
    print("✓ Manual send channels with None text_channels handled gracefully")

def test_manual_send_channels_without_text_channels_attribute():
    """Test that guilds without text_channels attribute return empty list."""
    print("Test: Manual send channels without text_channels attribute...")
    
    # Create mock bot with guild missing text_channels attribute
    guild = MockGuild(123458, "Incomplete Server", has_text_channels=False)
    bot = MockBot([guild])
    
    # Create web server
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, bot)
    
    # Test the endpoint
    with web_server.app.test_client() as client:
        response = client.get('/api/manual_send/channels')
        data = json.loads(response.data)
        
        assert 'channels' in data, "Response should have 'channels' key"
        assert len(data['channels']) == 0, f"Should have 0 channels when text_channels doesn't exist, got {len(data['channels'])}"
        
    print("✓ Manual send channels without text_channels attribute handled gracefully")

def test_manual_send_channels_no_bot():
    """Test that endpoint returns empty list when bot_instance is None."""
    print("Test: Manual send channels with no bot instance...")
    
    # Create web server with no bot instance
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, None)
    
    # Test the endpoint
    with web_server.app.test_client() as client:
        response = client.get('/api/manual_send/channels')
        data = json.loads(response.data)
        
        assert 'channels' in data, "Response should have 'channels' key"
        assert len(data['channels']) == 0, f"Should have 0 channels when bot_instance is None, got {len(data['channels'])}"
        
    print("✓ Manual send channels with no bot instance returns empty list")

def test_manual_send_channels_multiple_guilds():
    """Test with multiple guilds, some broken and some working."""
    print("Test: Manual send channels with multiple guilds...")
    
    # Create mock bot with multiple guilds in different states
    guilds = [
        MockGuild(123456, "Normal Server 1"),  # Normal - 2 channels
        MockGuild(123457, "Broken Server", text_channels_is_none=True),  # None text_channels - 0 channels
        MockGuild(123458, "Normal Server 2"),  # Normal - 2 channels
    ]
    bot = MockBot(guilds)
    
    # Create web server
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, bot)
    
    # Test the endpoint
    with web_server.app.test_client() as client:
        response = client.get('/api/manual_send/channels')
        data = json.loads(response.data)
        
        assert 'channels' in data, "Response should have 'channels' key"
        # Should have 4 channels total (2 from first guild + 0 from broken + 2 from third)
        assert len(data['channels']) == 4, f"Should have 4 channels total, got {len(data['channels'])}"
        
        # Check that channels from different servers are included
        server_names = [ch['server_name'] for ch in data['channels']]
        assert 'Normal Server 1' in server_names, "Should include channels from Normal Server 1"
        assert 'Normal Server 2' in server_names, "Should include channels from Normal Server 2"
        assert 'Broken Server' not in server_names, "Should not include channels from Broken Server"
        
    print("✓ Manual send channels with multiple guilds handled correctly")

if __name__ == "__main__":
    try:
        print("\n=== Testing Manual Send Channels API Fix ===\n")
        test_manual_send_channels_normal()
        test_manual_send_channels_with_none_text_channels()
        test_manual_send_channels_without_text_channels_attribute()
        test_manual_send_channels_no_bot()
        test_manual_send_channels_multiple_guilds()
        print("\n=== All Tests Passed! ===\n")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
