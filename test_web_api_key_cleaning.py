#!/usr/bin/env python3
"""Test web server API key handling with Bearer prefix."""
import sys
import json
from web_server import WebServer
from config_manager import ConfigManager

def test_web_server_api_key_cleaning():
    """Test that web server properly cleans API keys with Bearer prefix."""
    
    print("\n=== Testing Web Server API Key Cleaning ===\n")
    
    # Create a test config
    config_manager = ConfigManager("config.example.json")
    web_server = WebServer(config_manager, None)
    
    test_cases = [
        {
            "input": {"openai_config": {"api_key": "Bearer sk-test123", "base_url": "https://api.openai.com/v1"}},
            "expected_key": "sk-test123",
            "description": "API key with Bearer prefix"
        },
        {
            "input": {"openai_config": {"api_key": "  Bearer sk-test123  ", "base_url": "https://api.openai.com/v1"}},
            "expected_key": "sk-test123",
            "description": "API key with Bearer prefix and spaces"
        },
        {
            "input": {"openai_config": {"api_key": "bearer sk-test123", "base_url": "https://api.openai.com/v1"}},
            "expected_key": "sk-test123",
            "description": "API key with lowercase bearer prefix"
        },
        {
            "input": {"openai_config": {"api_key": "sk-test123", "base_url": "https://api.openai.com/v1"}},
            "expected_key": "sk-test123",
            "description": "Normal API key without Bearer"
        },
    ]
    
    all_passed = True
    
    with web_server.app.test_client() as client:
        for test_case in test_cases:
            # Simulate POST to /api/config
            response = client.post(
                '/api/config',
                data=json.dumps(test_case["input"]),
                content_type='application/json'
            )
            
            # Check if request was successful
            if response.status_code == 200:
                # Verify the API key was cleaned properly
                stored_key = config_manager.get('openai_config.api_key')
                if stored_key == test_case["expected_key"]:
                    print(f"  ✓ {test_case['description']:45} -> Cleaned to: {repr(stored_key)}")
                else:
                    print(f"  ✗ {test_case['description']:45} -> Got {repr(stored_key)}, expected {repr(test_case['expected_key'])}")
                    all_passed = False
            else:
                print(f"  ✗ {test_case['description']:45} -> HTTP {response.status_code}: {response.data}")
                all_passed = False
    
    if all_passed:
        print("\n=== All Web Server Tests Passed! ===\n")
    else:
        print("\n=== Some Web Server Tests Failed! ===\n")
    
    return all_passed

if __name__ == "__main__":
    success = test_web_server_api_key_cleaning()
    sys.exit(0 if success else 1)
