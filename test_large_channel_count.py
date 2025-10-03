#!/usr/bin/env python3
"""Test channel listing with large number of channels (4000+)."""
import sys
sys.path.insert(0, '/home/runner/work/Discord-bot-with-Preset/Discord-bot-with-Preset')

from web_server import WebServer
from config_manager import ConfigManager
import json
import time

class MockChannel:
    """Mock Discord Channel object."""
    def __init__(self, channel_id, name):
        self.id = channel_id
        self.name = name

class MockGuild:
    """Mock Discord Guild with many channels."""
    def __init__(self, guild_id, name, num_channels=4000):
        self.id = guild_id
        self.name = name
        # Create a large number of channels
        self.text_channels = [
            MockChannel(f"{guild_id}{str(i).zfill(6)}", f"channel-{i}")
            for i in range(num_channels)
        ]

class MockBot:
    """Mock Discord Bot instance."""
    def __init__(self):
        # Create a guild with 4000 channels
        self.guilds = [MockGuild(123456, "Large Server", 4000)]

def test_large_channel_count():
    """Test API with 4000 channels."""
    print("\n=== Testing with 4000 Channels ===\n")
    
    # Create web server
    config_manager = ConfigManager("config.example.json")
    bot = MockBot()
    web_server = WebServer(config_manager, bot)
    
    with web_server.app.test_client() as client:
        # Test /api/servers endpoint
        print("1. Testing /api/servers endpoint...")
        start = time.time()
        response = client.get('/api/servers')
        elapsed = time.time() - start
        data = json.loads(response.data)
        
        print(f"   ✓ Response time: {elapsed:.3f}s")
        print(f"   ✓ Server count: {len(data['servers'])}")
        print(f"   ✓ Channel count: {data['servers'][0]['channel_count']}")
        
        # Test /api/servers/<id>/channels endpoint
        print("\n2. Testing /api/servers/<id>/channels endpoint...")
        start = time.time()
        response = client.get('/api/servers/123456/channels')
        elapsed = time.time() - start
        data = json.loads(response.data)
        
        print(f"   ✓ Response time: {elapsed:.3f}s")
        print(f"   ✓ Channels returned: {len(data['channels'])}")
        
        # Check response size
        response_size = len(response.data)
        print(f"   ✓ Response size: {response_size / 1024:.1f} KB ({response_size / (1024*1024):.2f} MB)")
        
        # Performance analysis
        print("\n3. Performance Analysis:")
        if elapsed > 2.0:
            print(f"   ⚠️  Response time is {elapsed:.1f}s - this may cause timeout issues")
        else:
            print(f"   ✓ Response time is acceptable: {elapsed:.3f}s")
        
        if response_size > 1024 * 1024:  # 1 MB
            print(f"   ⚠️  Response size is {response_size / (1024*1024):.2f} MB - this is quite large")
        else:
            print(f"   ✓ Response size is acceptable: {response_size / 1024:.1f} KB")
        
        print("\n4. Recommendation:")
        if elapsed > 1.0 or response_size > 512 * 1024:
            print("   ⚠️  With 4000 channels, pagination is RECOMMENDED to improve performance")
            print("   Suggested: Implement pagination with 100 channels per page")
        else:
            print("   ✓ Current implementation can handle 4000 channels")

if __name__ == "__main__":
    try:
        test_large_channel_count()
        print("\n=== Test Complete ===\n")
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
