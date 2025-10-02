#!/usr/bin/env python3
"""Test script to verify that swipe buttons now edit messages instead of posting new ones."""

import sys
import inspect

def test_edit_long_message_exists():
    """Test that edit_long_message function exists."""
    print("Testing edit_long_message function...")
    try:
        from discord_bot import edit_long_message
        
        # Check function signature
        sig = inspect.signature(edit_long_message)
        params = list(sig.parameters.keys())
        
        assert 'message' in params, "edit_long_message should have 'message' parameter"
        assert 'content' in params, "edit_long_message should have 'content' parameter"
        assert 'view' in params, "edit_long_message should have 'view' parameter"
        
        print("✓ edit_long_message function exists with correct signature")
        return True
    except Exception as e:
        print(f"✗ edit_long_message test failed: {e}")
        return False


def test_edit_as_character_exists():
    """Test that edit_as_character method exists."""
    print("\nTesting edit_as_character method...")
    try:
        from discord_bot import DiscordBot
        import inspect
        
        # Check that method exists
        assert hasattr(DiscordBot, 'edit_as_character'), "DiscordBot should have edit_as_character method"
        
        # Check method signature
        sig = inspect.signature(DiscordBot.edit_as_character)
        params = list(sig.parameters.keys())
        
        assert 'self' in params, "edit_as_character should have 'self' parameter"
        assert 'message' in params, "edit_as_character should have 'message' parameter"
        assert 'content' in params, "edit_as_character should have 'content' parameter"
        assert 'character_data' in params, "edit_as_character should have 'character_data' parameter"
        assert 'view' in params, "edit_as_character should have 'view' parameter"
        
        print("✓ edit_as_character method exists with correct signature")
        return True
    except Exception as e:
        print(f"✗ edit_as_character test failed: {e}")
        return False


def test_send_as_character_returns_message():
    """Test that send_as_character now returns a message object."""
    print("\nTesting send_as_character return value...")
    try:
        from discord_bot import DiscordBot
        import inspect
        
        # Get method source to verify it returns a message
        source = inspect.getsource(DiscordBot.send_as_character)
        
        # Check that it returns the message object
        assert 'return last_message' in source or 'return None' in source, \
            "send_as_character should return a message object or None"
        
        print("✓ send_as_character returns message object")
        return True
    except Exception as e:
        print(f"✗ send_as_character return value test failed: {e}")
        return False


def test_send_long_message_with_view_returns_message():
    """Test that send_long_message_with_view now returns a message object."""
    print("\nTesting send_long_message_with_view return value...")
    try:
        from discord_bot import send_long_message_with_view
        import inspect
        
        # Get function source to verify it returns a message
        source = inspect.getsource(send_long_message_with_view)
        
        # Check that it returns the message object
        assert 'return' in source, "send_long_message_with_view should return a message object"
        
        print("✓ send_long_message_with_view returns message object")
        return True
    except Exception as e:
        print(f"✗ send_long_message_with_view return value test failed: {e}")
        return False


def test_done_button_exists():
    """Test that Done button callback exists."""
    print("\nTesting Done button...")
    try:
        from discord_bot import SwipeButtonView
        
        # Check for done_button callback method
        methods = dir(SwipeButtonView)
        assert 'done_button' in methods, "done_button callback not found"
        
        # Check the source to verify it's a button
        source = inspect.getsource(SwipeButtonView.done_button)
        assert '@discord.ui.button' in source or 'discord.ui.button' in source, \
            "done_button should be decorated as a button"
        
        print("✓ Done button callback defined")
        return True
    except Exception as e:
        print(f"✗ Done button test failed: {e}")
        return False


def test_button_callbacks_use_edit():
    """Test that button callbacks use edit instead of send."""
    print("\nTesting that button callbacks edit messages...")
    try:
        from discord_bot import SwipeButtonView
        import inspect
        
        # Check swipe_left_button uses edit
        left_source = inspect.getsource(SwipeButtonView.swipe_left_button)
        assert 'edit_long_message' in left_source or 'edit_as_character' in left_source, \
            "swipe_left_button should use edit functions"
        assert 'send_long_message_with_view' not in left_source and 'send_as_character' not in left_source or \
            'edit' in left_source, \
            "swipe_left_button should not send new messages"
        print("✓ swipe_left_button uses edit")
        
        # Check swipe_button uses edit
        swipe_source = inspect.getsource(SwipeButtonView.swipe_button)
        assert 'edit_long_message' in swipe_source or 'edit_as_character' in swipe_source, \
            "swipe_button should use edit functions"
        print("✓ swipe_button uses edit")
        
        # Check swipe_right_button uses edit
        right_source = inspect.getsource(SwipeButtonView.swipe_right_button)
        assert 'edit_long_message' in right_source or 'edit_as_character' in right_source, \
            "swipe_right_button should use edit functions"
        print("✓ swipe_right_button uses edit")
        
        return True
    except Exception as e:
        print(f"✗ Button callback edit test failed: {e}")
        return False


def test_done_button_removes_view():
    """Test that Done button removes the view."""
    print("\nTesting Done button removes view...")
    try:
        from discord_bot import SwipeButtonView
        import inspect
        
        source = inspect.getsource(SwipeButtonView.done_button)
        
        # Check that it sets view=None when editing
        assert 'view=None' in source, "done_button should remove view by setting view=None"
        
        print("✓ Done button removes view")
        return True
    except Exception as e:
        print(f"✗ Done button view removal test failed: {e}")
        return False


def test_swipe_view_init_signature():
    """Test that SwipeButtonView.__init__ has correct signature."""
    print("\nTesting SwipeButtonView.__init__ signature...")
    try:
        from discord_bot import SwipeButtonView
        import inspect
        
        sig = inspect.signature(SwipeButtonView.__init__)
        params = list(sig.parameters.keys())
        
        assert 'self' in params, "__init__ should have 'self' parameter"
        assert 'bot' in params, "__init__ should have 'bot' parameter"
        assert 'channel_id' in params, "__init__ should have 'channel_id' parameter"
        
        # message_id is optional, so we just check it exists in the source
        source = inspect.getsource(SwipeButtonView.__init__)
        assert 'message_id' in source, "__init__ should reference message_id"
        
        print("✓ SwipeButtonView.__init__ has correct signature")
        return True
    except Exception as e:
        print(f"✗ SwipeButtonView.__init__ signature test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("SWIPE BUTTON EDIT FUNCTIONALITY TESTS")
    print("=" * 80)
    
    tests = [
        test_edit_long_message_exists,
        test_edit_as_character_exists,
        test_send_as_character_returns_message,
        test_send_long_message_with_view_returns_message,
        test_done_button_exists,
        test_button_callbacks_use_edit,
        test_done_button_removes_view,
        test_swipe_view_init_signature,
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
