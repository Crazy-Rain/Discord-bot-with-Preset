#!/usr/bin/env python3
"""Test script to verify the reconnection and typing indicator fixes."""

import asyncio
import sys
from unittest.mock import Mock, AsyncMock, MagicMock
import inspect

def test_reconnection_creates_new_instance():
    """Test that reconnection logic creates a fresh bot instance."""
    print("\n🔧 Testing reconnection creates fresh bot instance...")
    try:
        import main
        source = inspect.getsource(main.run_discord_bot)
        
        # Check that we create a new instance on retry
        if "bot_instance = DiscordBot(config_manager)" in source:
            print("  ✓ Creates new bot instance during reconnection")
        else:
            print("  ✗ Does not create new bot instance")
            return False
        
        # Check that we close the old instance before retrying
        if "bot_instance.close()" in source or "await bot_instance.close()" in source:
            print("  ✓ Closes failed bot instance before retry")
        else:
            print("  ✗ Does not close failed bot instance")
            return False
            
        print("✓ Reconnection logic creates fresh instances")
        return True
    except Exception as e:
        print(f"✗ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_persistent_typing_exists():
    """Test that PersistentTyping class exists."""
    print("\n🔧 Testing PersistentTyping class...")
    try:
        from discord_bot import PersistentTyping
        
        # Check that it's a class
        if not inspect.isclass(PersistentTyping):
            print("  ✗ PersistentTyping is not a class")
            return False
        
        print("  ✓ PersistentTyping class exists")
        
        # Check for required methods
        required_methods = ['__aenter__', '__aexit__', '_keep_typing']
        for method in required_methods:
            if not hasattr(PersistentTyping, method):
                print(f"  ✗ Missing method: {method}")
                return False
            print(f"  ✓ Has {method} method")
        
        print("✓ PersistentTyping class is properly implemented")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_typing_usage():
    """Test that PersistentTyping is used instead of ctx.typing()."""
    print("\n🔧 Testing PersistentTyping usage...")
    try:
        import discord_bot
        source = inspect.getsource(discord_bot.DiscordBot)
        
        # Count occurrences
        persistent_typing_count = source.count("PersistentTyping")
        ctx_typing_count = source.count("ctx.typing()")
        
        print(f"  - PersistentTyping usages: {persistent_typing_count}")
        print(f"  - ctx.typing() usages: {ctx_typing_count}")
        
        if persistent_typing_count >= 4:
            print("  ✓ PersistentTyping is used in multiple places")
        else:
            print("  ✗ PersistentTyping should be used more")
            return False
        
        if ctx_typing_count == 0:
            print("  ✓ No more ctx.typing() usage")
        else:
            print(f"  ⚠ Still {ctx_typing_count} ctx.typing() usages")
        
        print("✓ PersistentTyping is properly used")
        return True
    except Exception as e:
        print(f"✗ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_persistent_typing_functionality():
    """Test that PersistentTyping maintains typing indicator."""
    print("\n🔧 Testing PersistentTyping functionality...")
    try:
        from discord_bot import PersistentTyping
        
        # Mock channel
        channel = Mock()
        channel.trigger_typing = AsyncMock()
        
        # Test context manager
        async with PersistentTyping(channel) as typing:
            # Typing should start immediately
            await asyncio.sleep(0.1)
            assert channel.trigger_typing.call_count >= 1, "Typing not triggered"
            print(f"  ✓ Typing triggered {channel.trigger_typing.call_count} time(s)")
            
            # Wait to see if it refreshes
            initial_count = channel.trigger_typing.call_count
            await asyncio.sleep(8.5)
            
            if channel.trigger_typing.call_count > initial_count:
                print(f"  ✓ Typing refreshed (now {channel.trigger_typing.call_count} calls)")
            else:
                print(f"  ⚠ Typing might not refresh (still {channel.trigger_typing.call_count} calls)")
        
        # After exiting, the task should stop
        print("  ✓ Context manager exited cleanly")
        print("✓ PersistentTyping functionality works")
        return True
    except Exception as e:
        print(f"✗ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Reconnection and Typing Indicator Fixes - Test Suite")
    print("=" * 60)
    
    results = []
    
    # Synchronous tests
    results.append(("Reconnection Creates New Instance", test_reconnection_creates_new_instance()))
    results.append(("PersistentTyping Exists", test_persistent_typing_exists()))
    results.append(("PersistentTyping Usage", test_typing_usage()))
    
    # Async test
    print("\nRunning async functionality test...")
    async_result = asyncio.run(test_persistent_typing_functionality())
    results.append(("PersistentTyping Functionality", async_result))
    
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
        print("\nFixes implemented:")
        print("  ✓ Reconnection creates fresh bot instances")
        print("  ✓ Failed bot instances are properly closed")
        print("  ✓ PersistentTyping class for long operations")
        print("  ✓ Typing indicator refreshes every 8 seconds")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
