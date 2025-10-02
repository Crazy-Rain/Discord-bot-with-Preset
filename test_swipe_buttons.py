#!/usr/bin/env python3
"""Test script to verify swipe button functionality."""

import sys
import discord
from discord.ui import View, Button

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from discord_bot import SwipeButtonView, send_long_message, send_long_message_with_view
        print("✓ SwipeButtonView class imported successfully")
        print("✓ send_long_message function imported successfully")
        print("✓ send_long_message_with_view function imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_view_structure():
    """Test that SwipeButtonView has the expected structure."""
    print("\nTesting View structure...")
    try:
        from discord_bot import SwipeButtonView
        from config_manager import ConfigManager
        from discord_bot import DiscordBot
        
        # Create a mock bot for testing
        config = ConfigManager('config.example.json')
        
        # Check that SwipeButtonView is a View subclass
        assert issubclass(SwipeButtonView, discord.ui.View), "SwipeButtonView should be a subclass of discord.ui.View"
        print("✓ SwipeButtonView is a discord.ui.View subclass")
        
        # Create an instance (we'll use a mock channel_id)
        # Note: This won't work fully without a real bot instance, but we can test structure
        print("✓ SwipeButtonView structure looks correct")
        
        return True
    except Exception as e:
        print(f"✗ View structure error: {e}")
        return False

def test_button_callbacks():
    """Test that button callbacks are defined."""
    print("\nTesting button callbacks...")
    try:
        from discord_bot import SwipeButtonView
        
        # Check for button callback methods
        methods = dir(SwipeButtonView)
        
        expected_methods = ['swipe_left_button', 'swipe_button', 'swipe_right_button', 'delete_button']
        for method in expected_methods:
            assert method in methods, f"{method} callback not found"
            print(f"✓ {method} callback defined")
        
        return True
    except Exception as e:
        print(f"✗ Button callback error: {e}")
        return False

def test_function_signatures():
    """Test that helper functions have correct signatures."""
    print("\nTesting function signatures...")
    try:
        from discord_bot import send_long_message, send_long_message_with_view
        import inspect
        
        # Check send_long_message signature
        sig = inspect.signature(send_long_message)
        params = list(sig.parameters.keys())
        assert 'ctx' in params, "send_long_message should have 'ctx' parameter"
        assert 'content' in params, "send_long_message should have 'content' parameter"
        assert 'view' in params, "send_long_message should have 'view' parameter"
        print("✓ send_long_message has correct signature")
        
        # Check send_long_message_with_view signature
        sig = inspect.signature(send_long_message_with_view)
        params = list(sig.parameters.keys())
        assert 'channel' in params, "send_long_message_with_view should have 'channel' parameter"
        assert 'content' in params, "send_long_message_with_view should have 'content' parameter"
        assert 'view' in params, "send_long_message_with_view should have 'view' parameter"
        print("✓ send_long_message_with_view has correct signature")
        
        return True
    except Exception as e:
        print(f"✗ Function signature error: {e}")
        return False

def test_send_as_character_signature():
    """Test that send_as_character method has view parameter."""
    print("\nTesting send_as_character signature...")
    try:
        from discord_bot import DiscordBot
        import inspect
        
        # Get the method signature
        sig = inspect.signature(DiscordBot.send_as_character)
        params = list(sig.parameters.keys())
        
        # Check for expected parameters
        assert 'self' in params, "send_as_character should have 'self' parameter"
        assert 'channel' in params, "send_as_character should have 'channel' parameter"
        assert 'content' in params, "send_as_character should have 'content' parameter"
        assert 'character_data' in params, "send_as_character should have 'character_data' parameter"
        assert 'view' in params, "send_as_character should have 'view' parameter"
        print("✓ send_as_character has correct signature with view parameter")
        
        return True
    except Exception as e:
        print(f"✗ send_as_character signature error: {e}")
        return False

def test_button_labels():
    """Test that buttons have correct labels and styles."""
    print("\nTesting button labels and styles...")
    try:
        from discord_bot import SwipeButtonView
        
        # Create a mock instance to inspect buttons
        # We can't create a real instance without a bot, but we can check the class definition
        import inspect
        source = inspect.getsource(SwipeButtonView)
        
        # Check for button labels
        assert '◀ Swipe Left' in source, "Swipe Left button label not found"
        assert '🔄 Swipe' in source, "Swipe button label not found"
        assert 'Swipe Right ▶' in source, "Swipe Right button label not found"
        assert '🗑️ Delete' in source, "Delete button label not found"
        print("✓ All button labels are correct")
        
        # Check for button styles
        assert 'ButtonStyle.secondary' in source, "Secondary button style not found"
        assert 'ButtonStyle.primary' in source, "Primary button style not found"
        assert 'ButtonStyle.danger' in source, "Danger button style not found"
        print("✓ All button styles are defined")
        
        return True
    except Exception as e:
        print(f"✗ Button labels/styles error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 80)
    print("SWIPE BUTTON FUNCTIONALITY TESTS")
    print("=" * 80)
    
    tests = [
        test_imports,
        test_view_structure,
        test_button_callbacks,
        test_function_signatures,
        test_send_as_character_signature,
        test_button_labels
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
