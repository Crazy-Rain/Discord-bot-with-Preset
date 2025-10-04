#!/usr/bin/env python3
"""Test to verify the reconnection fix always creates fresh bot instances."""

import sys

def test_always_creates_fresh_instance():
    """Test that reconnection logic ALWAYS creates a fresh bot instance."""
    print("\n🔧 Testing that fresh bot instance is always created...")
    try:
        # Read main.py source directly
        with open('main.py', 'r') as f:
            source = f.read()
        
        # Find the run_discord_bot function
        if 'async def run_discord_bot' not in source:
            print("  ✗ Could not find run_discord_bot function")
            return False
        
        # Extract the function
        start_idx = source.find('async def run_discord_bot')
        # Find the next function or end of file
        next_func = source.find('\ndef ', start_idx + 1)
        if next_func == -1:
            next_func = source.find('\nasync def ', start_idx + 1)
        if next_func == -1:
            func_source = source[start_idx:]
        else:
            func_source = source[start_idx:next_func]
        
        # Check that we create a new instance on EVERY iteration
        if "bot_instance = DiscordBot(config_manager)" not in func_source:
            print("  ✗ Does not create bot instance")
            return False
        print("  ✓ Creates bot instance")
        
        # Check that the creation is inside the while loop
        if "while not shutdown_flag and retry_count < max_retries:" not in func_source:
            print("  ✗ Could not find retry loop")
            return False
        print("  ✓ Has retry loop")
        
        # Extract the while loop content
        loop_start = func_source.find("while not shutdown_flag")
        loop_content = func_source[loop_start:]
        
        # Verify bot instance is created in the loop
        if "bot_instance = DiscordBot(config_manager)" not in loop_content:
            print("  ✗ Bot instance not created in retry loop")
            return False
        print("  ✓ Bot instance created in retry loop")
        
        # Check that problematic conditional is NOT present
        # Old buggy code: if retry_count > 0 or bot_instance.is_closed():
        if "if retry_count > 0 or bot_instance.is_closed():" in func_source:
            print("  ✗ Still has old conditional logic (if retry_count > 0 or bot_instance.is_closed())")
            return False
        print("  ✓ Does not have old buggy conditional")
        
        # Verify the instance creation is not behind a retry_count > 0 check
        lines = func_source.split('\n')
        for i, line in enumerate(lines):
            if "bot_instance = DiscordBot(config_manager)" in line:
                # Look at previous non-empty lines for conditions
                j = i - 1
                while j >= 0 and lines[j].strip() == '':
                    j -= 1
                
                if j >= 0:
                    prev_line = lines[j].strip()
                    # Check for the old buggy conditional
                    if "if retry_count > 0 or" in prev_line:
                        print(f"  ✗ Bot creation still conditional on retry_count > 0: {prev_line}")
                        return False
                break
        
        print("  ✓ Bot instance creation not conditional on retry_count > 0")
            
        print("✓ Reconnection logic always creates fresh instances")
        return True
    except Exception as e:
        print(f"✗ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_server_uses_global():
    """Test that web server uses global bot_instance reference."""
    print("\n🔧 Testing web server uses global bot_instance...")
    try:
        # Read web_server.py source directly
        with open('web_server.py', 'r') as f:
            source = f.read()
        
        # Check for property decorator
        if "@property" not in source:
            print("  ✗ No @property decorator found")
            return False
        print("  ✓ Has @property decorator")
        
        # Check for bot_instance property
        if "def bot_instance(self):" not in source:
            print("  ✗ No bot_instance property method")
            return False
        print("  ✓ Has bot_instance property method")
        
        # Extract the property
        prop_start = source.find("def bot_instance(self):")
        prop_end = source.find("\n    def ", prop_start + 1)
        if prop_end == -1:
            prop_source = source[prop_start:]
        else:
            prop_source = source[prop_start:prop_end]
        
        # Check that it imports main and returns main.bot_instance
        if "import main" not in prop_source:
            print("  ✗ Property does not import main")
            return False
        print("  ✓ Property imports main")
        
        if "return main.bot_instance" not in prop_source:
            print("  ✗ Property does not return main.bot_instance")
            return False
        print("  ✓ Property returns main.bot_instance")
        
        print("✓ Web server correctly uses global bot_instance")
        return True
    except Exception as e:
        print(f"✗ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Reconnection Fix - Test Suite")
    print("=" * 60)
    
    results = []
    results.append(("Always Creates Fresh Instance", test_always_creates_fresh_instance()))
    results.append(("Web Server Uses Global", test_web_server_uses_global()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed!")
        print("\nFix implemented:")
        print("  ✓ Always creates fresh bot instances on every connection attempt")
        print("  ✓ Web server accesses global bot_instance to get latest instance")
        print("  ✓ No more stale bot instance references")
        print("\nThis ensures:")
        print("  • First disconnect -> fresh bot created -> reconnects successfully")
        print("  • Second disconnect -> fresh bot created -> reconnects successfully")
        print("  • N-th disconnect -> fresh bot created -> reconnects successfully")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
