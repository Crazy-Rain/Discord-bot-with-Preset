#!/usr/bin/env python3
"""
Quick verification script to check if bot connection detection is working correctly.

This script checks if the WebServer is properly configured to dynamically
detect bot connection status.
"""

import sys
import os

def check_fix():
    """Check if the bot connection detection fix is in place."""
    
    print("=" * 70)
    print("BOT CONNECTION DETECTION FIX VERIFICATION")
    print("=" * 70)
    print()
    
    # Check main.py for the fix
    main_file = 'main.py'
    if not os.path.exists(main_file):
        print(f"❌ ERROR: {main_file} not found!")
        return False
    
    with open(main_file, 'r') as f:
        content = f.read()
    
    # Check for the INCORRECT pattern (the bug)
    if 'WebServer(config_manager, bot_instance)' in content:
        print("❌ BUG DETECTED!")
        print()
        print("Found: WebServer(config_manager, bot_instance)")
        print("This will cause the bot connection detection issue.")
        print()
        print("The WebServer should be initialized WITHOUT the bot_instance parameter:")
        print("  WebServer(config_manager)")
        print()
        return False
    
    # Check for the CORRECT pattern (the fix)
    if 'WebServer(config_manager)' in content:
        # Make sure it's in run_web_server function
        if 'def run_web_server' in content:
            # Extract the function
            start = content.find('def run_web_server')
            end = content.find('\ndef ', start + 1)
            if end == -1:
                end = len(content)
            func_content = content[start:end]
            
            if 'WebServer(config_manager)' in func_content:
                print("✅ FIX VERIFIED!")
                print()
                print("WebServer is correctly initialized without bot_instance parameter.")
                print("This allows dynamic bot connection detection.")
                print()
                print("Location: run_web_server() function in main.py")
                print("Pattern found: WebServer(config_manager)")
                print()
                
                # Show the actual line
                for i, line in enumerate(func_content.split('\n'), 1):
                    if 'WebServer(config_manager)' in line:
                        print(f"Line content: {line.strip()}")
                        break
                
                print()
                print("✅ Bot connection detection should work correctly!")
                print()
                print("Expected behavior:")
                print("  • Servers/Channels tab shows servers when bot is connected")
                print("  • Manual Send tab shows server dropdown when bot is connected")
                print("  • Bot reconnection is automatically detected")
                print()
                return True
    
    print("⚠️  UNCLEAR STATUS")
    print()
    print("Could not find the expected WebServer initialization pattern.")
    print("Please check main.py manually.")
    print()
    return None

def check_tests():
    """Check if the tests exist."""
    print("-" * 70)
    print("CHECKING TEST FILES")
    print("-" * 70)
    print()
    
    test_files = [
        'test_bot_connection_detection.py',
        'test_server_channels_fix.py',
        'test_manual_send_dropdowns.py'
    ]
    
    all_exist = True
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"✅ {test_file} exists")
        else:
            print(f"❌ {test_file} missing")
            all_exist = False
    
    print()
    if all_exist:
        print("✅ All test files present")
        print()
        print("To run tests:")
        print("  python3 test_bot_connection_detection.py")
        print("  python3 test_server_channels_fix.py")
        print("  python3 test_manual_send_dropdowns.py")
    else:
        print("⚠️  Some test files are missing")
    
    print()
    return all_exist

def main():
    """Main verification function."""
    fix_ok = check_fix()
    tests_ok = check_tests()
    
    print("=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print()
    
    if fix_ok:
        print("✅ Fix is in place")
    elif fix_ok is False:
        print("❌ Fix is NOT in place - bug exists!")
    else:
        print("⚠️  Could not verify fix status")
    
    if tests_ok:
        print("✅ Test files are present")
    else:
        print("⚠️  Some test files are missing")
    
    print()
    
    if fix_ok:
        print("✨ Bot connection detection should work correctly!")
        print()
        print("To verify manually:")
        print("  1. Run: python main.py")
        print("  2. Wait for 'Bot is ready!' message")
        print("  3. Open: http://localhost:5000")
        print("  4. Click 'Servers/Channels' tab → should show servers")
        print("  5. Click 'Manual Send' tab → should show server dropdown")
        print()
        return 0
    else:
        print("⚠️  The bot connection detection fix may not be working correctly.")
        print()
        print("To apply the fix:")
        print("  1. Open main.py")
        print("  2. Find: def run_web_server(config_manager: ConfigManager):")
        print("  3. Change: web_server = WebServer(config_manager, bot_instance)")
        print("  4. To:     web_server = WebServer(config_manager)")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
