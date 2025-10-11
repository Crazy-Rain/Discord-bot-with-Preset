#!/usr/bin/env python3
"""Test that WebServer correctly detects bot connection status."""

import sys
import json
import importlib
from config_manager import ConfigManager
from web_server import WebServer

class MockGuild:
    """Mock Discord Guild."""
    def __init__(self, guild_id, name, text_channels_count=2):
        self.id = guild_id
        self.name = name
        self.text_channels = [
            type('Channel', (), {'id': i, 'name': f'channel-{i}'})()
            for i in range(text_channels_count)
        ]

class MockBot:
    """Mock Discord Bot."""
    def __init__(self, guilds=None):
        self.guilds = guilds or []
        self.user = type('User', (), {'name': 'TestBot'})()
        
    def is_closed(self):
        return False

def test_webserver_gets_current_bot_instance():
    """Test that WebServer gets the current bot instance dynamically."""
    print("\nTest: WebServer gets current bot instance dynamically...")
    
    # Create a mock main module
    import types
    main = types.ModuleType('main')
    sys.modules['main'] = main
    
    # Step 1: Create placeholder bot (like line 104 in main.py)
    placeholder_bot = MockBot([])
    main.bot_instance = placeholder_bot
    
    # Step 2: Create WebServer WITHOUT passing bot_instance
    # This is the fix - WebServer should get bot dynamically from main.bot_instance
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager)
    
    # Step 3: Verify WebServer sees the placeholder bot (no guilds yet)
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        assert data['servers'] == [], f"Should have no servers initially, got {data['servers']}"
        print("  ✓ WebServer sees placeholder bot with no servers")
    
    # Step 4: Simulate bot connection - create NEW bot instance with guilds
    # (like line 50 in main.py when reconnection creates fresh bot)
    connected_bot = MockBot([
        MockGuild(123456, "Test Server 1"),
        MockGuild(789012, "Test Server 2")
    ])
    main.bot_instance = connected_bot
    
    # Step 5: Verify WebServer NOW sees the connected bot with guilds
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        assert len(data['servers']) == 2, f"Should have 2 servers now, got {len(data['servers'])}"
        assert data['servers'][0]['name'] == "Test Server 1"
        assert data['servers'][1]['name'] == "Test Server 2"
        print("  ✓ WebServer dynamically sees new connected bot with 2 servers")
    
    # Cleanup
    del sys.modules['main']
    
    print("✓ WebServer correctly gets current bot instance dynamically")
    return True

def test_webserver_detects_bot_reconnection():
    """Test that WebServer detects when bot reconnects with different guilds."""
    print("\nTest: WebServer detects bot reconnection...")
    
    # Create a mock main module
    import types
    main = types.ModuleType('main')
    sys.modules['main'] = main
    
    # Initial connected bot
    initial_bot = MockBot([MockGuild(111111, "Initial Server")])
    main.bot_instance = initial_bot
    
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager)
    
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        assert len(data['servers']) == 1
        assert data['servers'][0]['name'] == "Initial Server"
        print("  ✓ WebServer sees initial bot with 1 server")
    
    # Simulate reconnection with different guilds
    reconnected_bot = MockBot([
        MockGuild(222222, "Reconnected Server 1"),
        MockGuild(333333, "Reconnected Server 2"),
        MockGuild(444444, "Reconnected Server 3")
    ])
    main.bot_instance = reconnected_bot
    
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        assert len(data['servers']) == 3
        assert data['servers'][0]['name'] == "Reconnected Server 1"
        assert data['servers'][1]['name'] == "Reconnected Server 2"
        assert data['servers'][2]['name'] == "Reconnected Server 3"
        print("  ✓ WebServer sees reconnected bot with 3 different servers")
    
    # Cleanup
    del sys.modules['main']
    
    print("✓ WebServer correctly detects bot reconnection")
    return True

def test_webserver_handles_no_bot():
    """Test that WebServer handles case when bot is None."""
    print("\nTest: WebServer handles no bot gracefully...")
    
    # Create a mock main module
    import types
    main = types.ModuleType('main')
    sys.modules['main'] = main
    
    # Set bot to None (before any bot is created)
    main.bot_instance = None
    
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager)
    
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        assert data['servers'] == []
        print("  ✓ WebServer returns empty list when bot is None")
    
    # Cleanup
    del sys.modules['main']
    
    print("✓ WebServer handles no bot gracefully")
    return True

def main():
    print("=" * 70)
    print("BOT CONNECTION DETECTION TEST")
    print("=" * 70)
    
    tests = [
        test_webserver_gets_current_bot_instance,
        test_webserver_detects_bot_reconnection,
        test_webserver_handles_no_bot,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except AssertionError as e:
            print(f"  ✗ Test failed: {e}")
            results.append(False)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 70)
    print("Test Results:")
    print("=" * 70)
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ ALL TESTS PASSED")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
