#!/usr/bin/env python3
"""Test for the server/channels API endpoint fix."""
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

def test_normal_guild():
    """Test that normal guilds work correctly."""
    print("Test: Normal guild with text_channels...")
    
    # Create mock bot with normal guild
    guild = MockGuild(123456, "Test Server")
    bot = MockBot([guild])
    
    # Create web server
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, bot)
    
    # Test the endpoint
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        
        assert 'servers' in data, "Response should have 'servers' key"
        assert len(data['servers']) == 1, "Should have 1 server"
        
        server = data['servers'][0]
        assert server['id'] == '123456', f"Server ID should be '123456', got {server['id']}"
        assert server['name'] == 'Test Server', f"Server name should be 'Test Server', got {server['name']}"
        assert server['channel_count'] == 2, f"Should have 2 channels, got {server.get('channel_count')}"
        
    print("✓ Normal guild works correctly")

def test_guild_with_none_text_channels():
    """Test that guilds with None text_channels are handled gracefully."""
    print("Test: Guild with text_channels = None...")
    
    # Create mock bot with guild where text_channels is None
    guild = MockGuild(123457, "Broken Server", text_channels_is_none=True)
    bot = MockBot([guild])
    
    # Create web server
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, bot)
    
    # Test the endpoint
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        
        assert 'servers' in data, "Response should have 'servers' key"
        assert len(data['servers']) == 1, "Should have 1 server"
        
        server = data['servers'][0]
        assert server['channel_count'] == 0, f"Should have 0 channels when text_channels is None, got {server.get('channel_count')}"
        
    print("✓ Guild with None text_channels handled gracefully")

def test_guild_without_text_channels_attribute():
    """Test that guilds without text_channels attribute are handled gracefully."""
    print("Test: Guild without text_channels attribute...")
    
    # Create mock bot with guild missing text_channels attribute
    guild = MockGuild(123458, "Incomplete Server", has_text_channels=False)
    bot = MockBot([guild])
    
    # Create web server
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, bot)
    
    # Test the endpoint
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        
        assert 'servers' in data, "Response should have 'servers' key"
        assert len(data['servers']) == 1, "Should have 1 server"
        
        server = data['servers'][0]
        assert server['channel_count'] == 0, f"Should have 0 channels when text_channels doesn't exist, got {server.get('channel_count')}"
        
    print("✓ Guild without text_channels attribute handled gracefully")

def test_multiple_guilds_mixed():
    """Test with multiple guilds, some broken and some working."""
    print("Test: Multiple guilds with mixed conditions...")
    
    # Create mock bot with multiple guilds in different states
    guilds = [
        MockGuild(123456, "Normal Server"),  # Normal
        MockGuild(123457, "Broken Server", text_channels_is_none=True),  # None text_channels
        MockGuild(123458, "Another Normal Server"),  # Normal
    ]
    bot = MockBot(guilds)
    
    # Create web server
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, bot)
    
    # Test the endpoint
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        
        assert 'servers' in data, "Response should have 'servers' key"
        assert len(data['servers']) == 3, f"Should have 3 servers, got {len(data['servers'])}"
        
        # Check that all servers are included with correct channel counts
        channel_counts = [s['channel_count'] for s in data['servers']]
        assert channel_counts == [2, 0, 2], f"Channel counts should be [2, 0, 2], got {channel_counts}"
        
    print("✓ Multiple guilds with mixed conditions handled correctly")

def test_server_channels_endpoint():
    """Test the /api/servers/<server_id>/channels endpoint."""
    print("Test: Server channels endpoint...")
    
    # Create mock bot
    guild = MockGuild(123456, "Test Server")
    bot = MockBot([guild])
    
    # Create web server
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, bot)
    
    # Test the endpoint
    with web_server.app.test_client() as client:
        response = client.get('/api/servers/123456/channels')
        data = json.loads(response.data)
        
        assert 'channels' in data, "Response should have 'channels' key"
        assert len(data['channels']) == 2, f"Should have 2 channels, got {len(data['channels'])}"
        
    print("✓ Server channels endpoint works correctly")

def test_server_channels_with_none_text_channels():
    """Test the channels endpoint with None text_channels."""
    print("Test: Server channels endpoint with None text_channels...")
    
    # Create mock bot with guild where text_channels is None
    guild = MockGuild(123457, "Broken Server", text_channels_is_none=True)
    bot = MockBot([guild])
    
    # Create web server
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, bot)
    
    # Test the endpoint
    with web_server.app.test_client() as client:
        response = client.get('/api/servers/123457/channels')
        data = json.loads(response.data)
        
        assert 'channels' in data, "Response should have 'channels' key"
        assert len(data['channels']) == 0, f"Should have 0 channels when text_channels is None, got {len(data['channels'])}"
        
    print("✓ Server channels endpoint handles None text_channels gracefully")

if __name__ == "__main__":
    try:
        print("\n=== Testing Server/Channels API Fix ===\n")
        test_normal_guild()
        test_guild_with_none_text_channels()
        test_guild_without_text_channels_attribute()
        test_multiple_guilds_mixed()
        test_server_channels_endpoint()
        test_server_channels_with_none_text_channels()
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
