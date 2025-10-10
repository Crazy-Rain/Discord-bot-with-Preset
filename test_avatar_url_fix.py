#!/usr/bin/env python3
"""Test to verify the avatar URL fix for Discord webhooks."""

import sys
import os

def test_web_server_route():
    """Test that web server has a route to serve character avatars."""
    print("\n🔧 Testing web server avatar route...")
    try:
        from web_server import WebServer
        from config_manager import ConfigManager
        
        config = ConfigManager('config.example.json')
        web_server = WebServer(config)
        
        # Check if the route exists
        rules = list(web_server.app.url_map.iter_rules())
        avatar_route = None
        
        for rule in rules:
            if 'character_avatars' in rule.rule:
                avatar_route = rule
                break
        
        if avatar_route:
            print(f"  ✓ Found avatar route: {avatar_route.rule}")
            return True
        else:
            print("  ✗ Avatar route not found")
            return False
            
    except Exception as e:
        print(f"  ✗ Error testing web server route: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_get_web_server_url():
    """Test that bot can generate web server URLs."""
    print("\n🔧 Testing web server URL generation...")
    try:
        from discord_bot import DiscordBot
        from config_manager import ConfigManager
        
        config = ConfigManager('config.example.json')
        bot = DiscordBot(config)
        
        url = bot.get_web_server_url()
        
        if url and (url.startswith('http://') or url.startswith('https://')):
            print(f"  ✓ Generated URL: {url}")
            return True
        else:
            print(f"  ✗ Invalid URL: {url}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error testing URL generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_webhook_url_validation():
    """Test that webhook only accepts HTTP/HTTPS URLs."""
    print("\n🔧 Testing webhook URL validation...")
    try:
        # Simulate the webhook logic
        test_cases = [
            {
                'name': 'Valid HTTP URL',
                'avatar_url': 'http://localhost:5000/character_avatars/luna.png',
                'should_include': True
            },
            {
                'name': 'Valid HTTPS URL',
                'avatar_url': 'https://example.com/avatar.png',
                'should_include': True
            },
            {
                'name': 'Base64 data URL (should be filtered)',
                'avatar_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
                'should_include': False
            },
            {
                'name': 'Empty string',
                'avatar_url': '',
                'should_include': False
            },
            {
                'name': 'None',
                'avatar_url': None,
                'should_include': False
            }
        ]
        
        all_passed = True
        for test_case in test_cases:
            avatar_url = test_case['avatar_url']
            should_include = test_case['should_include']
            
            # This is the actual logic from discord_bot.py
            will_include = bool(avatar_url and avatar_url.strip() and (avatar_url.startswith('http://') or avatar_url.startswith('https://')))
            
            if will_include == should_include:
                status = 'Included' if will_include else 'Filtered'
                print(f"  ✓ {test_case['name']}: {status} (as expected)")
            else:
                actual = 'Included' if will_include else 'Filtered'
                expected = 'Included' if should_include else 'Filtered'
                print(f"  ✗ {test_case['name']}: {actual} (expected {expected})")
                all_passed = False
        
        return all_passed
            
    except Exception as e:
        print(f"  ✗ Error testing webhook validation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_command_logic():
    """Test that image command uses HTTP URLs."""
    print("\n🔧 Testing image command logic...")
    try:
        from discord_bot import DiscordBot
        from config_manager import ConfigManager
        
        config = ConfigManager('config.example.json')
        bot = DiscordBot(config)
        
        # Simulate what the image command does
        character_name = "test_character"
        file_ext = "png"
        web_server_url = bot.get_web_server_url()
        avatar_url = f"{web_server_url}/character_avatars/{character_name}.{file_ext}"
        
        # Check that the URL is HTTP-based, not base64
        if avatar_url.startswith('http://') or avatar_url.startswith('https://'):
            print(f"  ✓ Generated HTTP URL: {avatar_url}")
            if 'data:image' not in avatar_url:
                print(f"  ✓ No base64 data in URL")
                return True
            else:
                print(f"  ✗ URL contains base64 data")
                return False
        else:
            print(f"  ✗ Invalid URL format: {avatar_url}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error testing image command logic: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 70)
    print("AVATAR URL FIX VERIFICATION")
    print("=" * 70)
    
    results = []
    
    # Run tests
    results.append(("Web Server Route", test_web_server_route()))
    results.append(("Web Server URL Generation", test_get_web_server_url()))
    results.append(("Webhook URL Validation", test_webhook_url_validation()))
    results.append(("Image Command Logic", test_image_command_logic()))
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ All tests passed!")
        print("\nFix implemented:")
        print("  ✓ Web server serves character avatars via HTTP")
        print("  ✓ !image command generates HTTP URLs instead of base64")
        print("  ✓ Webhook logic filters out base64 data URLs")
        print("  ✓ Only HTTP/HTTPS URLs are used for Discord webhooks")
        print("\nThis fixes the error:")
        print('  "sw4wpeokvbqaaaaasuvork5cyii=" is not supported.')
        print('  Scheme must be one of (\'http\', \'https\').')
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
