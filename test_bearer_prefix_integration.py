#!/usr/bin/env python3
"""Integration test for Bearer prefix fix with actual OpenAI client usage."""
import sys
from openai_client import OpenAIClient

def test_bearer_prefix_integration():
    """Test that Bearer prefix removal works correctly in real scenarios."""
    
    print("\n=== Bearer Prefix Fix Integration Test ===\n")
    
    # Test 1: Verify client initialization with various key formats
    print("Test 1: Client initialization with different API key formats")
    test_keys = [
        ("Normal key", "sk-test123"),
        ("Bearer prefix", "Bearer sk-test123"),
        ("Lowercase bearer", "bearer sk-test123"),
        ("With spaces", "  Bearer sk-test123  "),
    ]
    
    all_passed = True
    for desc, key in test_keys:
        try:
            client = OpenAIClient(api_key=key, base_url="https://api.openai.com/v1", model="gpt-3.5-turbo")
            if client.api_key == "sk-test123":
                print(f"  ✓ {desc:20} -> Cleaned correctly to 'sk-test123'")
            else:
                print(f"  ✗ {desc:20} -> Got '{client.api_key}', expected 'sk-test123'")
                all_passed = False
        except Exception as e:
            print(f"  ✗ {desc:20} -> Error: {e}")
            all_passed = False
    
    # Test 2: Verify update_config also cleans keys
    print("\nTest 2: update_config method")
    try:
        client = OpenAIClient(api_key="sk-initial", base_url="https://api.openai.com/v1")
        client.update_config(api_key="Bearer sk-updated")
        if client.api_key == "sk-updated":
            print(f"  ✓ update_config removes Bearer prefix correctly")
        else:
            print(f"  ✗ update_config failed: got '{client.api_key}', expected 'sk-updated'")
            all_passed = False
    except Exception as e:
        print(f"  ✗ update_config error: {e}")
        all_passed = False
    
    # Test 3: Verify the static method directly
    print("\nTest 3: _clean_api_key static method")
    test_cases = [
        ("Bearer sk-abc", "sk-abc"),
        ("  Bearer  sk-abc  ", "sk-abc"),
        ("sk-abc", "sk-abc"),
        ("BEARER sk-abc", "sk-abc"),
    ]
    
    for input_key, expected in test_cases:
        result = OpenAIClient._clean_api_key(input_key)
        if result == expected:
            print(f"  ✓ {repr(input_key):30} -> {repr(result)}")
        else:
            print(f"  ✗ {repr(input_key):30} -> {repr(result)} (expected {repr(expected)})")
            all_passed = False
    
    # Test 4: Ensure normal keys are not affected
    print("\nTest 4: Normal keys remain unchanged")
    normal_keys = ["sk-abc123", "custom-key-xyz", "token-123"]
    for key in normal_keys:
        result = OpenAIClient._clean_api_key(key)
        if result == key:
            print(f"  ✓ {repr(key):30} unchanged")
        else:
            print(f"  ✗ {repr(key):30} changed to {repr(result)}")
            all_passed = False
    
    if all_passed:
        print("\n=== All Integration Tests Passed! ===\n")
    else:
        print("\n=== Some Integration Tests Failed! ===\n")
    
    return all_passed

if __name__ == "__main__":
    success = test_bearer_prefix_integration()
    sys.exit(0 if success else 1)
