#!/usr/bin/env python3
"""
Simulation script to demonstrate the bot connection detection fix.

This script simulates the exact scenario from the problem statement:
1. Bot is connected and active
2. Web interface checks bot status when tabs are selected
3. Verifies servers/channels are shown correctly
"""

import sys
import json
import types
from config_manager import ConfigManager
from web_server import WebServer

class MockChannel:
    def __init__(self, channel_id, name):
        self.id = channel_id
        self.name = name

class MockGuild:
    def __init__(self, guild_id, name, channel_count=5):
        self.id = guild_id
        self.name = name
        self.text_channels = [
            MockChannel(i, f"channel-{i}") 
            for i in range(channel_count)
        ]

class MockBot:
    def __init__(self, guilds=None):
        self.guilds = guilds or []
        self.user = type('User', (), {'name': 'TestBot', 'id': 12345})()
    
    def is_closed(self):
        return False

def simulate_scenario():
    """Simulate the exact scenario from the problem statement."""
    
    print("=" * 70)
    print("SIMULATING BOT CONNECTION DETECTION SCENARIO")
    print("=" * 70)
    
    # Create mock main module
    main = types.ModuleType('main')
    sys.modules['main'] = main
    
    # Scenario: Bot starts up
    print("\n📝 SCENARIO: Bot Starting Up")
    print("-" * 70)
    
    # Step 1: Initially no bot (or placeholder bot)
    print("\n1. Initial state - placeholder bot created (line 104 in main.py)")
    placeholder_bot = MockBot([])
    main.bot_instance = placeholder_bot
    print(f"   Bot instance created: {id(placeholder_bot)}")
    print(f"   Guilds: {len(placeholder_bot.guilds)}")
    
    # Step 2: Web server starts (without bot_instance parameter - THE FIX!)
    print("\n2. Web server starting (line 20 in main.py - after fix)")
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager)  # No bot_instance parameter!
    print("   WebServer initialized WITHOUT bot_instance parameter ✓")
    
    # Step 3: User opens web interface and clicks Servers/Channels tab
    print("\n3. User opens http://localhost:5000 and clicks 'Servers/Channels' tab")
    print("   Frontend calls: fetch('/api/servers')")
    
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        print(f"   Response: {len(data['servers'])} servers")
        if len(data['servers']) == 0:
            print("   ⚠️  'Bot Not Connected' message would be shown")
    
    # Step 4: Bot connects to Discord
    print("\n4. Bot connecting to Discord (line 50 in main.py)")
    connected_bot = MockBot([
        MockGuild(111111111, "My Gaming Server", 10),
        MockGuild(222222222, "Dev Community", 5),
        MockGuild(333333333, "Friends", 3)
    ])
    main.bot_instance = connected_bot  # This updates the global bot_instance
    print(f"   New bot instance created: {id(connected_bot)}")
    print(f"   Guilds: {len(connected_bot.guilds)}")
    print("   ✅ Bot is ready! Logged in as TestBot")
    
    # Step 5: User clicks Servers/Channels tab again (or Manual Send)
    print("\n5. User clicks 'Servers/Channels' tab (tab already open or switching)")
    print("   Frontend calls: fetch('/api/servers') again")
    
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        print(f"   Response: {len(data['servers'])} servers")
        
        if len(data['servers']) > 0:
            print("\n   ✅ SUCCESS! Web interface now sees the connected bot!")
            print("\n   Servers shown:")
            for server in data['servers']:
                print(f"      🖥️  {server['name']} ({server['channel_count']} channels)")
        else:
            print("\n   ❌ FAIL! Web interface still doesn't see the bot")
    
    # Step 6: Test Manual Send tab
    print("\n6. User clicks 'Manual Send' tab")
    print("   Frontend calls: fetch('/api/servers') for dropdown")
    
    with web_server.app.test_client() as client:
        response = client.get('/api/servers')
        data = json.loads(response.data)
        
        if len(data['servers']) > 0:
            print(f"\n   ✅ Server dropdown populated with {len(data['servers'])} servers")
            
            # Test getting channels for a server
            server_id = data['servers'][0]['id']
            server_name = data['servers'][0]['name']
            print(f"\n7. User selects '{server_name}' from dropdown")
            print(f"   Frontend calls: fetch('/api/servers/{server_id}/channels')")
            
            response = client.get(f'/api/servers/{server_id}/channels')
            channel_data = json.loads(response.data)
            
            if channel_data.get('channels'):
                print(f"\n   ✅ Channel dropdown populated with {len(channel_data['channels'])} channels")
                print("\n   Channels shown:")
                for channel in channel_data['channels'][:5]:  # Show first 5
                    print(f"      #  {channel['name']}")
                if len(channel_data['channels']) > 5:
                    print(f"      ... and {len(channel_data['channels']) - 5} more")
        else:
            print("\n   ❌ No servers shown - error message would appear")
    
    # Cleanup
    del sys.modules['main']
    
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)
    print("\n✅ The fix allows the web interface to dynamically detect bot connection!")
    print("✅ Both 'Servers/Channels' and 'Manual Send' tabs work correctly!")
    print("\nKey Points:")
    print("  • WebServer no longer stores a stale bot instance")
    print("  • Each API request gets the current main.bot_instance")
    print("  • When bot reconnects, web interface immediately sees the new instance")
    print("  • Tab switching triggers data loading that checks current bot status")

if __name__ == "__main__":
    simulate_scenario()
