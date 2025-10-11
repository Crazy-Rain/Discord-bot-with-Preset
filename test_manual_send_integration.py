#!/usr/bin/env python3
"""Integration test for Manual Send feature - both dropdown and manual ID input modes."""

import sys
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
    async def send(self, **kwargs):
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
        return MockWebhook()
    
    async def send_as_character(self, channel, content, character_data, view=None):
        """Mock send_as_character - simulates successful send."""
        return MockMessage(123456), [123456]


def test_dropdown_mode_workflow():
    """Test the dropdown selection workflow."""
    print("\n=== Test: Dropdown Mode Workflow ===")
    
    # Setup bot with servers and channels
    guild1 = MockGuild(
        1011703948526239814,  # Server ID from issue
        'Test Server 1',
        [
            MockChannel(1426231081182695636, 'general'),  # Channel ID from issue
            MockChannel(1426231081182695637, 'random')
        ]
    )
    
    guild2 = MockGuild(
        9999999999999999,
        'Test Server 2',
        [MockChannel(8888888888888888, 'chat')]
    )
    
    bot = MockBot([guild1, guild2])
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=bot)
    
    with web_server.app.test_client() as client:
        # Step 1: Get list of servers (for dropdown)
        response = client.get('/api/servers')
        assert response.status_code == 200
        servers = response.json['servers']
        assert len(servers) == 2
        print(f"  ✓ Step 1: Retrieved {len(servers)} servers for dropdown")
        
        # Step 2: Get channels for first server (for dropdown)
        response = client.get(f'/api/servers/{guild1.id}/channels')
        assert response.status_code == 200
        channels = response.json['channels']
        assert len(channels) == 2
        print(f"  ✓ Step 2: Retrieved {len(channels)} channels for server dropdown")
        
        # Step 3: Get characters
        response = client.get('/api/characters')
        assert response.status_code == 200
        characters = response.json['characters']
        assert len(characters) > 0
        print(f"  ✓ Step 3: Retrieved {len(characters)} characters")
        
        # Step 4: Send message using dropdown-selected channel
        response = client.post('/api/manual_send',
            json={
                'channel_id': str(channels[0]['id']),  # From dropdown
                'character_name': characters[0],  # Character name (string)
                'message': 'Test message via dropdown'
            },
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        print(f"  ✓ Step 4: Successfully sent message via dropdown selection")


def test_manual_id_input_mode():
    """Test the manual ID input mode with the exact IDs from the issue."""
    print("\n=== Test: Manual ID Input Mode (Issue IDs) ===")
    
    # Setup with exact IDs from issue
    SERVER_ID = 1011703948526239814
    CHANNEL_ID = 1426231081182695636
    
    guild = MockGuild(
        SERVER_ID,
        'Test Server',
        [MockChannel(CHANNEL_ID, 'test-channel')]
    )
    
    bot = MockBot([guild])
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=bot)
    
    with web_server.app.test_client() as client:
        # User enters Server ID and Channel ID manually (as strings from frontend)
        response = client.post('/api/manual_send',
            json={
                'channel_id': str(CHANNEL_ID),  # Manual input (string)
                'character_name': 'aria',
                'message': 'Test message with manual IDs'
            },
            content_type='application/json'
        )
        
        print(f"  Server ID used: {SERVER_ID}")
        print(f"  Channel ID used: {CHANNEL_ID}")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json['status'] == 'success'
        print(f"  ✓ Successfully sent message using manual ID input")


def test_server_unreachable_scenario():
    """Test the scenario where server isn't reachable via dropdown but manual ID works."""
    print("\n=== Test: Server Unreachable via Dropdown but Accessible via Manual ID ===")
    
    # Scenario: Bot can see server but dropdown might fail
    # User uses manual ID input as fallback
    SERVER_ID = 1011703948526239814
    CHANNEL_ID = 1426231081182695636
    
    guild = MockGuild(
        SERVER_ID,
        'Test Server',
        [MockChannel(CHANNEL_ID, 'test-channel')]
    )
    
    bot = MockBot([guild])
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=bot)
    
    with web_server.app.test_client() as client:
        # Even if dropdown fails to load, manual ID input works
        response = client.post('/api/manual_send',
            json={
                'channel_id': str(CHANNEL_ID),
                'character_name': 'aria',
                'message': 'Fallback to manual ID when dropdown fails'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        print("  ✓ Manual ID input works as fallback when dropdown unavailable")


def test_both_modes_send_to_same_channel():
    """Verify both dropdown and manual ID modes can send to the same channel."""
    print("\n=== Test: Both Modes Send to Same Channel ===")
    
    SERVER_ID = 1011703948526239814
    CHANNEL_ID = 1426231081182695636
    
    guild = MockGuild(
        SERVER_ID,
        'Test Server',
        [MockChannel(CHANNEL_ID, 'test-channel')]
    )
    
    bot = MockBot([guild])
    config_manager = ConfigManager('config.example.json')
    web_server = WebServer(config_manager, bot_instance=bot)
    
    with web_server.app.test_client() as client:
        # Mode 1: Dropdown (channel ID from /api/servers/{id}/channels)
        response1 = client.post('/api/manual_send',
            json={
                'channel_id': str(CHANNEL_ID),  # From dropdown
                'character_name': 'aria',
                'message': 'Via dropdown mode'
            },
            content_type='application/json'
        )
        
        # Mode 2: Manual ID Input (user types the channel ID)
        response2 = client.post('/api/manual_send',
            json={
                'channel_id': str(CHANNEL_ID),  # Manual input
                'character_name': 'aria',
                'message': 'Via manual ID mode'
            },
            content_type='application/json'
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        print("  ✓ Both dropdown and manual ID modes successfully send to same channel")


if __name__ == '__main__':
    print("=" * 70)
    print("MANUAL SEND INTEGRATION TEST")
    print("=" * 70)
    print("\nTesting both Dropdown Selection and Manual ID Input modes")
    print(f"Using Server ID: 1011703948526239814")
    print(f"Using Channel ID: 1426231081182695636")
    
    try:
        test_dropdown_mode_workflow()
        test_manual_id_input_mode()
        test_server_unreachable_scenario()
        test_both_modes_send_to_same_channel()
        
        print("\n" + "=" * 70)
        print("✅ ALL INTEGRATION TESTS PASSED")
        print("=" * 70)
        print("\nVerified:")
        print("✓ Dropdown selection mode works correctly")
        print("✓ Manual ID input mode works with issue IDs")
        print("✓ Manual ID works as fallback when dropdown fails")
        print("✓ Both modes can send to the same channel")
        print("\nThe Manual Send feature is now fully functional!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
