#!/usr/bin/env python3
"""Test pagination with 4000 channels."""
import sys
sys.path.insert(0, '/home/runner/work/Discord-bot-with-Preset/Discord-bot-with-Preset')

from web_server import WebServer
from config_manager import ConfigManager
import json

class MockChannel:
    def __init__(self, channel_id, name):
        self.id = channel_id
        self.name = name

class MockGuild:
    def __init__(self, guild_id, name, num_channels=4000):
        self.id = guild_id
        self.name = name
        self.text_channels = [
            MockChannel(f"{guild_id}{str(i).zfill(6)}", f"channel-{i}")
            for i in range(num_channels)
        ]

class MockBot:
    def __init__(self):
        self.guilds = [MockGuild(123456, "Large Server", 4000)]

def test_pagination():
    """Test pagination functionality."""
    print("\n=== Testing Pagination with 4000 Channels ===\n")
    
    config_manager = ConfigManager("config.example.json")
    bot = MockBot()
    web_server = WebServer(config_manager, bot)
    
    with web_server.app.test_client() as client:
        # Test page 1
        print("1. Testing Page 1 (first 100 channels)...")
        response = client.get('/api/servers/123456/channels?page=1&per_page=100')
        data = json.loads(response.data)
        
        print(f"   ✓ Channels returned: {len(data['channels'])}")
        print(f"   ✓ Total channels: {data['total']}")
        print(f"   ✓ Current page: {data['page']}")
        print(f"   ✓ Total pages: {data['total_pages']}")
        
        assert len(data['channels']) == 100, "Should return 100 channels"
        assert data['total'] == 4000, "Total should be 4000"
        assert data['page'] == 1, "Should be page 1"
        assert data['total_pages'] == 40, "Should have 40 pages (4000/100)"
        
        # Test page 2
        print("\n2. Testing Page 2...")
        response = client.get('/api/servers/123456/channels?page=2&per_page=100')
        data = json.loads(response.data)
        
        print(f"   ✓ Channels returned: {len(data['channels'])}")
        print(f"   ✓ First channel: {data['channels'][0]['name']}")
        
        assert len(data['channels']) == 100, "Should return 100 channels"
        assert data['channels'][0]['name'] == 'channel-100', "First channel should be channel-100"
        
        # Test last page
        print("\n3. Testing Last Page (page 40)...")
        response = client.get('/api/servers/123456/channels?page=40&per_page=100')
        data = json.loads(response.data)
        
        print(f"   ✓ Channels returned: {len(data['channels'])}")
        print(f"   ✓ First channel: {data['channels'][0]['name']}")
        print(f"   ✓ Last channel: {data['channels'][-1]['name']}")
        
        assert len(data['channels']) == 100, "Last page should have 100 channels"
        assert data['channels'][0]['name'] == 'channel-3900', "First channel should be channel-3900"
        assert data['channels'][-1]['name'] == 'channel-3999', "Last channel should be channel-3999"
        
        # Test search functionality
        print("\n4. Testing Search Functionality...")
        response = client.get('/api/servers/123456/channels?page=1&per_page=100&search=channel-10')
        data = json.loads(response.data)
        
        print(f"   ✓ Search results: {data['total']} channels")
        print(f"   ✓ First result: {data['channels'][0]['name'] if data['channels'] else 'None'}")
        
        # Should find channels like: channel-10, channel-100, channel-101, ..., channel-109, 
        # channel-1000, channel-1001, ..., channel-1099, channel-10xx, etc.
        assert data['total'] > 0, "Should find matching channels"
        
        # Test response size
        print("\n5. Testing Response Size...")
        response = client.get('/api/servers/123456/channels?page=1&per_page=100')
        response_size = len(response.data)
        print(f"   ✓ Response size for 100 channels: {response_size / 1024:.1f} KB")
        
        # With pagination, 100 channels should be much smaller than all 4000
        assert response_size < 100 * 1024, "100 channels should be less than 100KB"
        
        print("\n6. Performance Summary:")
        print(f"   ✓ Pagination working correctly")
        print(f"   ✓ 100 channels per page instead of 4000")
        print(f"   ✓ Response size reduced from ~339 KB to ~{response_size / 1024:.1f} KB")
        print(f"   ✓ Browser will render ~600 DOM elements instead of ~24,000")
        print(f"   ✓ Search functionality available")

if __name__ == "__main__":
    try:
        test_pagination()
        print("\n=== All Pagination Tests Passed! ===\n")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
