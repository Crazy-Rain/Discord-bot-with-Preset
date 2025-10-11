#!/usr/bin/env python3
"""Test API key Bearer prefix handling fix."""
import sys
from openai_client import OpenAIClient

def test_api_key_cleaning():
    """Test that API keys with Bearer prefix are properly cleaned."""
    
    test_cases = [
        # (input_key, expected_stored_key, description)
        ("sk-abc123", "sk-abc123", "Normal API key"),
        ("  sk-abc123  ", "sk-abc123", "API key with spaces"),
        ("sk-abc123\n", "sk-abc123", "API key with newline"),
        ("Bearer sk-abc123", "sk-abc123", "API key with Bearer prefix"),
        ("  Bearer sk-abc123  ", "sk-abc123", "API key with Bearer prefix and spaces"),
        ("bearer sk-abc123", "sk-abc123", "API key with lowercase bearer prefix"),
        ("BEARER sk-abc123", "sk-abc123", "API key with uppercase bearer prefix"),
        ("Bearer  sk-abc123", "sk-abc123", "API key with Bearer and extra spaces"),
    ]
    
    print("\n=== Testing API Key Bearer Prefix Fix ===\n")
    print("Testing OpenAIClient._clean_api_key() method:")
    
    all_passed = True
    for input_key, expected, description in test_cases:
        result = OpenAIClient._clean_api_key(input_key)
        passed = result == expected
        status = "✓" if passed else "✗"
        
        print(f"  {status} {description:45} | Input: {repr(input_key):30} | Output: {repr(result):20}")
        
        if not passed:
            print(f"      FAILED: Expected {repr(expected)}")
            all_passed = False
    
    # Test that cleaned API keys work correctly in OpenAIClient
    print("\nTesting OpenAIClient initialization with various API key formats:")
    
    test_client_cases = [
        ("Bearer sk-test123", "sk-test123"),
        ("  Bearer sk-test123  ", "sk-test123"),
        ("sk-test123", "sk-test123"),
    ]
    
    for input_key, expected_stored in test_client_cases:
        try:
            client = OpenAIClient(api_key=input_key, base_url="https://api.openai.com/v1")
            if client.api_key == expected_stored:
                print(f"  ✓ Client initialized with {repr(input_key):30} -> Stored: {repr(client.api_key)}")
            else:
                print(f"  ✗ Client initialized with {repr(input_key):30} -> Stored: {repr(client.api_key)} (expected {repr(expected_stored)})")
                all_passed = False
        except Exception as e:
            print(f"  ✗ Failed to initialize client with {repr(input_key)}: {e}")
            all_passed = False
    
    if all_passed:
        print("\n=== All Tests Passed! ===\n")
    else:
        print("\n=== Some Tests Failed! ===\n")
    
    return all_passed

if __name__ == "__main__":
    success = test_api_key_cleaning()
    sys.exit(0 if success else 1)
