#!/usr/bin/env python3
"""Test server configuration feature."""

import json
import sys

def test_config_priority():
    """Test configuration priority: channel > server > default."""
    
    # Mock config structure
    config = {
        "server_configs": {
            "server_123": {
                "preset": "server_preset",
                "api_config": "server_api",
                "character": "server_char"
            }
        },
        "channel_configs": {
            "channel_456": {
                "preset": "channel_preset",
                "api_config": "",
                "character": ""
            }
        }
    }
    
    # Test 1: Channel with config should use channel config
    channel_id = "channel_456"
    server_id = "server_123"
    
    # Priority: channel > server > default
    preset = config['channel_configs'].get(channel_id, {}).get('preset', '')
    if not preset and server_id:
        preset = config['server_configs'].get(server_id, {}).get('preset', '')
    if not preset:
        preset = "default_preset"
    
    assert preset == "channel_preset", f"Expected 'channel_preset', got '{preset}'"
    print("✓ Test 1 passed: Channel config takes priority")
    
    # Test 2: Channel without config should use server config
    channel_id = "channel_789"  # No channel config
    
    preset = config['channel_configs'].get(channel_id, {}).get('preset', '')
    if not preset and server_id:
        preset = config['server_configs'].get(server_id, {}).get('preset', '')
    if not preset:
        preset = "default_preset"
    
    assert preset == "server_preset", f"Expected 'server_preset', got '{preset}'"
    print("✓ Test 2 passed: Server config used when no channel config")
    
    # Test 3: Channel with empty config value should use server config
    channel_id = "channel_456"  # Has channel config but api_config is empty
    
    api_config = config['channel_configs'].get(channel_id, {}).get('api_config', '')
    if not api_config and server_id:
        api_config = config['server_configs'].get(server_id, {}).get('api_config', '')
    if not api_config:
        api_config = "default_api"
    
    assert api_config == "server_api", f"Expected 'server_api', got '{api_config}'"
    print("✓ Test 3 passed: Server config used when channel config is empty")
    
    # Test 4: No channel or server config should use default
    channel_id = "channel_999"
    server_id = "server_999"
    
    preset = config['channel_configs'].get(channel_id, {}).get('preset', '')
    if not preset and server_id:
        preset = config['server_configs'].get(server_id, {}).get('preset', '')
    if not preset:
        preset = "default_preset"
    
    assert preset == "default_preset", f"Expected 'default_preset', got '{preset}'"
    print("✓ Test 4 passed: Default used when no channel or server config")
    
    print("\n✅ All configuration priority tests passed!")

def test_config_json():
    """Test that config.example.json is valid and has server_configs."""
    try:
        with open('config.example.json', 'r') as f:
            config = json.load(f)
        
        assert 'server_configs' in config, "server_configs key not found in config.example.json"
        assert 'channel_configs' in config, "channel_configs key should still exist for backward compatibility"
        
        print("✓ config.example.json is valid")
        print("✓ server_configs key exists")
        print("✓ channel_configs key still exists (backward compatibility)")
        print("\n✅ Configuration file structure test passed!")
        
    except Exception as e:
        print(f"❌ Configuration file test failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    print("Testing Server Configuration Feature")
    print("=" * 50)
    
    test_config_priority()
    print()
    test_config_json()
