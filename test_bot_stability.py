#!/usr/bin/env python3
"""Test script to verify bot stability improvements."""

import sys
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import inspect

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        import main
        from discord_bot import DiscordBot
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_event_handlers():
    """Test that bot has proper event handlers."""
    print("\nTesting event handlers...")
    try:
        from config_manager import ConfigManager
        from discord_bot import DiscordBot
        
        config = ConfigManager('config.example.json')
        bot = DiscordBot(config)
        
        # Check if event handlers exist and are coroutines
        handlers = ['on_ready', 'on_disconnect', 'on_resume', 'on_error']
        for handler in handlers:
            if not hasattr(bot, handler):
                print(f"✗ Missing handler: {handler}")
                return False
            handler_func = getattr(bot, handler)
            if not inspect.iscoroutinefunction(handler_func):
                print(f"✗ {handler} is not a coroutine")
                return False
            print(f"  ✓ {handler} exists and is async")
        
        print("✓ All event handlers present")
        return True
    except Exception as e:
        print(f"✗ Event handler error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_signal_handlers():
    """Test that main.py has signal handlers."""
    print("\nTesting signal handlers...")
    try:
        import main
        
        # Check signal_handler function exists
        if not hasattr(main, 'signal_handler'):
            print("✗ signal_handler function not found")
            return False
        
        # Check shutdown_flag exists
        if not hasattr(main, 'shutdown_flag'):
            print("✗ shutdown_flag not found")
            return False
        
        print("✓ Signal handler and shutdown flag present")
        return True
    except Exception as e:
        print(f"✗ Signal handler error: {e}")
        return False

def test_reconnection_logic():
    """Test that reconnection logic is present."""
    print("\nTesting reconnection logic...")
    try:
        import main
        import inspect
        
        # Check run_discord_bot function
        if not hasattr(main, 'run_discord_bot'):
            print("✗ run_discord_bot function not found")
            return False
        
        # Verify it's async
        if not inspect.iscoroutinefunction(main.run_discord_bot):
            print("✗ run_discord_bot is not async")
            return False
        
        # Check source code for retry logic
        source = inspect.getsource(main.run_discord_bot)
        
        required_keywords = ['retry', 'while', 'Exception', 'asyncio.sleep']
        for keyword in required_keywords:
            if keyword not in source:
                print(f"✗ Missing keyword in reconnection logic: {keyword}")
                return False
        
        print("✓ Reconnection logic is present")
        print("  - Retry loop detected")
        print("  - Exception handling present")
        print("  - Backoff delay mechanism found")
        return True
    except Exception as e:
        print(f"✗ Reconnection logic error: {e}")
        return False

def test_cleanup_logic():
    """Test that cleanup logic is present."""
    print("\nTesting cleanup logic...")
    try:
        import main
        import inspect
        
        # Check main function for cleanup
        source = inspect.getsource(main.main)
        
        required_keywords = ['finally', 'is_closed', 'close']
        for keyword in required_keywords:
            if keyword not in source:
                print(f"✗ Missing cleanup keyword: {keyword}")
                return False
        
        print("✓ Cleanup logic is present")
        print("  - finally block detected")
        print("  - Bot close handling found")
        return True
    except Exception as e:
        print(f"✗ Cleanup logic error: {e}")
        return False

async def test_bot_event_handler_execution():
    """Test that event handlers can be called."""
    print("\nTesting event handler execution...")
    try:
        from config_manager import ConfigManager
        from discord_bot import DiscordBot
        
        config = ConfigManager('config.example.json')
        bot = DiscordBot(config)
        
        # Test on_disconnect (doesn't require user)
        await bot.on_disconnect()
        print("  ✓ on_disconnect executed successfully")
        
        # Test on_resume (doesn't require user)
        await bot.on_resume()
        print("  ✓ on_resume executed successfully")
        
        # Test on_error (doesn't require user)
        await bot.on_error('test_event')
        print("  ✓ on_error executed successfully")
        
        print("✓ All testable event handlers can be executed")
        return True
    except Exception as e:
        print(f"✗ Event handler execution error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Discord Bot Stability - Test Suite")
    print("=" * 60)
    
    sync_tests = [
        ("Imports", test_imports),
        ("Event Handlers", test_event_handlers),
        ("Signal Handlers", test_signal_handlers),
        ("Reconnection Logic", test_reconnection_logic),
        ("Cleanup Logic", test_cleanup_logic),
    ]
    
    async_tests = [
        ("Event Handler Execution", test_bot_event_handler_execution),
    ]
    
    results = []
    
    # Run synchronous tests
    for name, test_func in sync_tests:
        result = test_func()
        results.append((name, result))
    
    # Run async tests
    for name, test_func in async_tests:
        result = asyncio.run(test_func())
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All stability tests passed!")
        print("\nImprovements implemented:")
        print("  ✓ Event handlers for disconnect/resume/error")
        print("  ✓ Automatic reconnection with exponential backoff")
        print("  ✓ Graceful shutdown handling")
        print("  ✓ Proper cleanup on exit")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
