#!/usr/bin/env python3
"""Test that the web interface loads correctly with the fix."""
import sys
import json
from unittest.mock import Mock, MagicMock
from web_server import WebServer
from config_manager import ConfigManager

# Mock Discord guild and bot
class MockGuild:
    def __init__(self, guild_id, name):
        self.id = guild_id
        self.name = name
        self.text_channels = [
            type('obj', (object,), {'id': f'{guild_id}001', 'name': 'general'}),
            type('obj', (object,), {'id': f'{guild_id}002', 'name': 'random'}),
        ]

class MockBot:
    def __init__(self):
        self.guilds = [
            MockGuild(123456, "Test Server 1"),
            MockGuild(789012, "Test Server 2"),
        ]

def test_web_interface():
    """Test that the web interface returns the correct structure."""
    print("Test: Web interface endpoints work correctly...")
    
    # Create config manager
    config_manager = ConfigManager("config.example.json")
    
    # Create mock bot
    bot = MockBot()
    
    # Create web server
    web_server = WebServer(config_manager, bot)
    
    with web_server.app.test_client() as client:
        # Test /api/config endpoint
        print("  - Testing /api/config endpoint...")
        response = client.get('/api/config')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        config = json.loads(response.data)
        print(f"    ✓ Config loaded successfully")
        
        # Check that it has the expected structure
        assert 'default_preset' in config, "Config should have default_preset"
        assert 'openai_config' in config, "Config should have openai_config"
        
        # Check if it has prompt_sections (new structure)
        if 'prompt_sections' in config['default_preset']:
            print(f"    ✓ Config has new prompt_sections structure")
            assert len(config['default_preset']['prompt_sections']) > 0, "Should have at least one prompt section"
        elif 'system_prompt' in config['default_preset']:
            print(f"    ✓ Config has old system_prompt structure (backward compatible)")
        else:
            print(f"    ! Warning: Config has neither prompt_sections nor system_prompt")
        
        # Test /api/servers endpoint
        print("  - Testing /api/servers endpoint...")
        response = client.get('/api/servers')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = json.loads(response.data)
        assert 'servers' in data, "Response should have 'servers' key"
        assert len(data['servers']) == 2, f"Should have 2 servers, got {len(data['servers'])}"
        
        # Check server structure
        for server in data['servers']:
            assert 'id' in server, "Server should have 'id'"
            assert 'name' in server, "Server should have 'name'"
            assert 'channel_count' in server, "Server should have 'channel_count'"
            print(f"    ✓ Server '{server['name']}' has {server['channel_count']} channels")
        
        print("  ✓ All web interface endpoints work correctly")

def test_frontend_loads():
    """Test that the frontend HTML loads correctly."""
    print("Test: Frontend HTML loads...")
    
    config_manager = ConfigManager("config.example.json")
    bot = MockBot()
    web_server = WebServer(config_manager, bot)
    
    with web_server.app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        html_content = response.data.decode('utf-8')
        
        # Check for key elements
        assert 'loadDefaultConfig' in html_content, "HTML should contain loadDefaultConfig function"
        assert 'loadServersList' in html_content, "HTML should contain loadServersList function"
        assert 'default-preset-display' in html_content, "HTML should contain default-preset-display element"
        assert 'default-api-display' in html_content, "HTML should contain default-api-display element"
        assert 'servers-list' in html_content, "HTML should contain servers-list element"
        
        # Check for the fix - should handle prompt_sections
        assert 'prompt_sections' in html_content, "HTML should check for prompt_sections"
        
        # Check for error handling
        assert 'try {' in html_content and 'catch' in html_content, "HTML should have error handling"
        
        print("  ✓ Frontend HTML loads correctly with all necessary elements")

if __name__ == "__main__":
    try:
        print("\n=== Testing Web Interface with Fix ===\n")
        test_web_interface()
        test_frontend_loads()
        print("\n=== All Web Interface Tests Passed! ===\n")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
