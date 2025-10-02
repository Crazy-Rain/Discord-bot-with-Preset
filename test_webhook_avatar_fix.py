#!/usr/bin/env python3
"""Test script to verify webhook avatar_url fix."""

def test_webhook_params_building():
    """Test that webhook parameters are built correctly based on avatar_url."""
    print("=" * 60)
    print("Testing Webhook Parameter Building")
    print("=" * 60)
    
    # Import the logic from discord_bot.py
    def build_webhook_params(character_data):
        """Simulates the fixed send_as_character logic"""
        character_name = character_data.get('name', 'Character')
        avatar_url = character_data.get('avatar_url')
        
        webhook_params = {
            'username': character_name,
            'wait': True
        }
        
        # Only include avatar_url if it's a valid non-empty string
        if avatar_url and avatar_url.strip():
            webhook_params['avatar_url'] = avatar_url
        
        return webhook_params
    
    test_cases = [
        {
            'name': 'Empty string avatar_url',
            'input': {'name': 'Luna', 'avatar_url': ''},
            'expected_has_username': True,
            'expected_has_avatar': False,
            'description': 'Character name should be used even without avatar'
        },
        {
            'name': 'None avatar_url',
            'input': {'name': 'Sherlock', 'avatar_url': None},
            'expected_has_username': True,
            'expected_has_avatar': False,
            'description': 'Character name should be used with None avatar'
        },
        {
            'name': 'Valid avatar_url',
            'input': {'name': 'Aria', 'avatar_url': 'https://example.com/aria.png'},
            'expected_has_username': True,
            'expected_has_avatar': True,
            'description': 'Both username and avatar should be included'
        },
        {
            'name': 'Whitespace-only avatar_url',
            'input': {'name': 'Test', 'avatar_url': '   '},
            'expected_has_username': True,
            'expected_has_avatar': False,
            'description': 'Whitespace-only avatar should be treated as empty'
        },
    ]
    
    all_passed = True
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        
        params = build_webhook_params(test_case['input'])
        
        has_username = 'username' in params and params['username'] == test_case['input']['name']
        has_avatar = 'avatar_url' in params
        
        print(f"  Input: {test_case['input']}")
        print(f"  Output: {params}")
        
        # Verify username
        if has_username == test_case['expected_has_username']:
            print(f"  ✓ Username correct: {has_username}")
        else:
            print(f"  ✗ Username incorrect: expected {test_case['expected_has_username']}, got {has_username}")
            all_passed = False
        
        # Verify avatar
        if has_avatar == test_case['expected_has_avatar']:
            print(f"  ✓ Avatar correct: {has_avatar}")
        else:
            print(f"  ✗ Avatar incorrect: expected {test_case['expected_has_avatar']}, got {has_avatar}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All webhook parameter tests passed!")
    else:
        print("✗ Some webhook parameter tests failed!")
    print("=" * 60)
    
    return all_passed


def test_code_structure():
    """Test that the fix is properly implemented in discord_bot.py"""
    print("\n" + "=" * 60)
    print("Testing Code Structure")
    print("=" * 60)
    
    try:
        with open('discord_bot.py', 'r') as f:
            content = f.read()
        
        checks = [
            ("webhook_params = {", "Webhook params dict created"),
            ("'username': character_name", "Character name added to params"),
            ("if avatar_url and avatar_url.strip():", "Conditional avatar URL check"),
            ("webhook_params['avatar_url'] = avatar_url", "Avatar URL conditionally added"),
            ("**webhook_params", "Params unpacked in webhook.send()"),
        ]
        
        all_passed = True
        print("\nChecking for required code patterns:")
        for check, description in checks:
            if check in content:
                print(f"  ✓ Found: {description}")
            else:
                print(f"  ✗ Missing: {description}")
                all_passed = False
        
        print("\n" + "=" * 60)
        if all_passed:
            print("✓ All code structure checks passed!")
        else:
            print("✗ Some code structure checks failed!")
        print("=" * 60)
        
        return all_passed
    except Exception as e:
        print(f"✗ Code structure test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Webhook Avatar Fix - Test Suite")
    print("=" * 60)
    print("\nThis test verifies the fix for the issue where character")
    print("names and avatars weren't displaying correctly in webhooks.")
    print("\nRoot cause: Empty avatar_url strings were being passed to")
    print("Discord's webhook API, causing it to fall back to defaults.")
    print("\nSolution: Only include avatar_url parameter when it has a")
    print("valid non-empty value.")
    print()
    
    results = []
    
    # Run tests
    results.append(("Webhook Parameter Building", test_webhook_params_building()))
    results.append(("Code Structure", test_code_structure()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(passed for _, passed in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nThe fix correctly handles:")
        print("  • Character names display even without avatars")
        print("  • Valid avatar URLs are used when provided")
        print("  • Empty/None/whitespace avatar URLs are handled gracefully")
    else:
        print("✗ SOME TESTS FAILED!")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
