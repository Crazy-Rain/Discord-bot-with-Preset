#!/usr/bin/env python3
"""Test Manual Send dropdown functionality."""

import sys
sys.path.insert(0, '/home/runner/work/Discord-bot-with-Preset/Discord-bot-with-Preset')

from web_server import WebServer
from config_manager import ConfigManager

# Create a mock bot instance
class MockGuild:
    def __init__(self, guild_id, name, channels):
        self.id = guild_id
        self.name = name
        self.text_channels = channels

class MockChannel:
    def __init__(self, channel_id, name):
        self.id = channel_id
        self.name = name

class MockBot:
    def __init__(self):
        self.guilds = [
            MockGuild(123, 'Test Server 1', [
                MockChannel(1001, 'general'),
                MockChannel(1002, 'random')
            ]),
            MockGuild(456, 'Test Server 2', [
                MockChannel(2001, 'announcements'),
                MockChannel(2002, 'chat')
            ])
        ]

def test_with_connected_bot():
    """Test endpoints when bot is connected."""
    print("\n=== Testing with CONNECTED bot ===")
    config_manager = ConfigManager()
    bot = MockBot()
    web_server = WebServer(config_manager, bot_instance=bot)
    
    with web_server.app.test_client() as client:
        # Test /api/servers
        response = client.get('/api/servers')
        data = response.json
        assert response.status_code == 200
        assert 'servers' in data
        assert len(data['servers']) == 2
        print(f"✓ /api/servers returns {len(data['servers'])} servers")
        
        # Test /api/servers/{id}/channels
        response = client.get('/api/servers/123/channels')
        data = response.json
        assert response.status_code == 200
        assert 'channels' in data
        assert len(data['channels']) == 2
        print(f"✓ /api/servers/123/channels returns {len(data['channels'])} channels")
        
        # Test /api/characters
        response = client.get('/api/characters')
        data = response.json
        assert response.status_code == 200
        assert 'characters' in data
        assert len(data['characters']) > 0
        print(f"✓ /api/characters returns {len(data['characters'])} characters")

def test_without_connected_bot():
    """Test endpoints when bot is NOT connected."""
    print("\n=== Testing with DISCONNECTED bot ===")
    config_manager = ConfigManager()
    web_server = WebServer(config_manager, bot_instance=None)
    
    with web_server.app.test_client() as client:
        # Test /api/servers returns empty list
        response = client.get('/api/servers')
        data = response.json
        assert response.status_code == 200
        assert 'servers' in data
        assert len(data['servers']) == 0
        print(f"✓ /api/servers returns empty list (bot not connected)")
        
        # Test /api/servers/{id}/channels returns empty list
        response = client.get('/api/servers/123/channels')
        data = response.json
        assert response.status_code == 200
        assert 'channels' in data
        assert len(data['channels']) == 0
        print(f"✓ /api/servers/123/channels returns empty list (bot not connected)")
        
        # Characters should still work (they're from files, not the bot)
        response = client.get('/api/characters')
        data = response.json
        assert response.status_code == 200
        assert 'characters' in data
        print(f"✓ /api/characters still returns {len(data['characters'])} characters")

def test_html_contains_functions():
    """Test that HTML contains the required JavaScript functions."""
    print("\n=== Testing HTML contains required functions ===")
    with open('templates/index.html', 'r') as f:
        html = f.read()
    
    # Check for required functions
    required_functions = [
        'loadManualSendServers',
        'loadManualSendServerChannels', 
        'loadManualSendCharacters'
    ]
    
    for func in required_functions:
        assert f'function {func}' in html, f"Missing function: {func}"
        print(f"✓ Found function: {func}")
    
    # Check for onchange handler
    assert 'onchange="loadManualSendServerChannels()"' in html
    print("✓ Server dropdown has onchange handler")
    
    # Check for tab switching logic
    assert "tabName === 'manual_send'" in html
    print("✓ Tab switching logic includes manual_send")
    
    # Check for error messaging
    assert 'No servers found. Make sure the bot is running and connected to Discord servers.' in html
    print("✓ Error message for no servers found")
    
    assert 'No channels found for this server.' in html
    print("✓ Error message for no channels found")

if __name__ == '__main__':
    print("=" * 70)
    print("MANUAL SEND DROPDOWN FUNCTIONALITY TESTS")
    print("=" * 70)
    
    try:
        test_with_connected_bot()
        test_without_connected_bot()
        test_html_contains_functions()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED")
        print("=" * 70)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
