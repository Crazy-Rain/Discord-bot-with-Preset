#!/usr/bin/env python3
"""
Diagnostic script to understand bot connection and guild detection issues.
This simulates the actual flow and checks for potential issues.
"""

import sys
import time
import types
from config_manager import ConfigManager
from web_server import WebServer

class MockChannel:
    """Mock Discord Channel."""
    def __init__(self, channel_id, name):
        self.id = channel_id
        self.name = name

class MockGuild:
    """Mock Discord Guild."""
    def __init__(self, guild_id, name, num_channels=3):
        self.id = guild_id
        self.name = name
        self.text_channels = [
            MockChannel(i, f"channel-{i}") for i in range(num_channels)
        ]

class MockBot:
    """Mock Discord Bot."""
    def __init__(self, guilds):
        self.guilds = guilds
        self.user = type('obj', (object,), {'name': 'TestBot'})()
    
    def is_closed(self):
        return False

def diagnose_connection_flow():
    """Diagnose the actual connection flow."""
    
    print("=" * 70)
    print("DIAGNOSTIC: Bot Connection and Guild Detection")
    print("=" * 70)
    
    # Create a mock main module to simulate the actual environment
    main = types.ModuleType('main')
    sys.modules['main'] = main
    
    # Step 1: Simulate initial bot placeholder (line 105 in main.py)
    print("\n1. Creating placeholder bot instance (line 105 in main.py)...")
    placeholder_bot = MockBot([])
    main.bot_instance = placeholder_bot
    print(f"   bot_instance ID: {id(placeholder_bot)}")
    print(f"   Guilds: {len(placeholder_bot.guilds)}")
    print(f"   Is this the instance web server will see? Let's check...")
    
    # Step 2: Web server starts (line 20 in main.py)
    print("\n2. Web server starting (line 20 in main.py)...")
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager)  # No bot_instance parameter!
    print(f"   WebServer._bot_instance_ref: {web_server._bot_instance_ref}")
    
    # Step 3: Check what bot instance the web server sees
    print("\n3. Checking what bot instance web server sees...")
    bot_from_property = web_server.bot_instance
    print(f"   bot_instance from property ID: {id(bot_from_property) if bot_from_property else 'None'}")
    print(f"   Is same as placeholder? {bot_from_property is placeholder_bot}")
    print(f"   Guilds from property: {len(bot_from_property.guilds) if bot_from_property else 0}")
    
    # Step 4: Simulate API call from web interface
    print("\n4. Simulating web interface API call GET /api/servers...")
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = response.get_json()
        print(f"   Response: {data}")
        print(f"   Number of servers: {len(data.get('servers', []))}")
        if len(data.get('servers', [])) == 0:
            print("   ⚠️  This would show 'NO SERVERS' in the UI")
    
    # Step 5: Simulate bot connection (line 51 in main.py)
    print("\n5. Bot connecting to Discord (line 51 in main.py)...")
    print("   Creating fresh bot instance for connection...")
    connected_bot = MockBot([
        MockGuild(123456789, "Test Server 1", 5),
        MockGuild(987654321, "Test Server 2", 3)
    ])
    main.bot_instance = connected_bot
    print(f"   New bot_instance ID: {id(connected_bot)}")
    print(f"   Guilds: {len(connected_bot.guilds)}")
    
    # Step 6: Simulate on_ready event
    print("\n6. Bot on_ready event fired (guilds populated)...")
    print(f"   Guilds in bot: {[g.name for g in connected_bot.guilds]}")
    
    # Step 7: Check what bot instance the web server sees NOW
    print("\n7. Checking what bot instance web server sees NOW...")
    bot_from_property = web_server.bot_instance
    print(f"   bot_instance from property ID: {id(bot_from_property) if bot_from_property else 'None'}")
    print(f"   Is same as connected bot? {bot_from_property is connected_bot}")
    print(f"   Guilds from property: {len(bot_from_property.guilds) if bot_from_property else 0}")
    
    # Step 8: Simulate API call from web interface AFTER connection
    print("\n8. Simulating web interface API call GET /api/servers AFTER connection...")
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = response.get_json()
        print(f"   Response: {data}")
        print(f"   Number of servers: {len(data.get('servers', []))}")
        if len(data.get('servers', [])) > 0:
            print("   ✅ Servers would be shown in the UI!")
            for server in data['servers']:
                print(f"      - {server['name']} ({server['channel_count']} channels)")
        else:
            print("   ❌ Still showing 'NO SERVERS' - ISSUE FOUND!")
    
    # Step 9: Check manual send channels endpoint
    print("\n9. Checking Manual Send channels endpoint...")
    with web_server.app.test_client() as client:
        response = client.get('/api/manual_send/channels')
        data = response.get_json()
        print(f"   Response: {len(data.get('channels', []))} channels")
        if len(data.get('channels', [])) > 0:
            print("   ✅ Channels dropdown would be populated!")
            for channel in data['channels'][:5]:  # Show first 5
                print(f"      - {channel['server_name']} / {channel['name']}")
        else:
            print("   ❌ Channels dropdown would be empty!")
    
    # Cleanup
    del sys.modules['main']
    
    print("\n" + "=" * 70)
    print("DIAGNOSIS COMPLETE")
    print("=" * 70)
    
    # Final analysis
    print("\nFINAL ANALYSIS:")
    print("-" * 70)
    if len(data.get('channels', [])) > 0:
        print("✅ The fix IS working correctly!")
        print("   Web server dynamically gets the current bot instance.")
        print("   Servers and channels are properly detected after connection.")
    else:
        print("❌ Issue detected!")
        print("   The web server is NOT getting the connected bot instance.")
        print("   This needs further investigation.")

if __name__ == "__main__":
    diagnose_connection_flow()
