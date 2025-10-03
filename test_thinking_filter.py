#!/usr/bin/env python3
"""Test script for thinking filter functionality."""

import sys
import json
from config_manager import ConfigManager

def test_filter():
    """Test thinking filter logic."""
    print("Testing Thinking Filter...")
    print("="*60)
    
    # Test cases
    test_cases = [
        {
            "name": "Simple thinking tags",
            "input": "Hello <think>This is my reasoning</think> world!",
            "expected": "Hello  world!",
            "config": {
                "enabled": True,
                "start_tag": "<think>",
                "end_tag": "</think>"
            }
        },
        {
            "name": "Multiple thinking tags",
            "input": "First <think>reason 1</think> middle <think>reason 2</think> last",
            "expected": "First  middle  last",
            "config": {
                "enabled": True,
                "start_tag": "<think>",
                "end_tag": "</think>"
            }
        },
        {
            "name": "Different tags",
            "input": "Text <thinking>my thoughts</thinking> more text",
            "expected": "Text  more text",
            "config": {
                "enabled": True,
                "start_tag": "<thinking>",
                "end_tag": "</thinking>"
            }
        },
        {
            "name": "Disabled filter",
            "input": "Hello <think>This should stay</think> world!",
            "expected": "Hello <think>This should stay</think> world!",
            "config": {
                "enabled": False,
                "start_tag": "<think>",
                "end_tag": "</think>"
            }
        },
        {
            "name": "Multiline thinking",
            "input": "Start\n<think>\nLine 1\nLine 2\nLine 3\n</think>\nEnd",
            "expected": "Start\n\nEnd",
            "config": {
                "enabled": True,
                "start_tag": "<think>",
                "end_tag": "</think>"
            }
        }
    ]
    
    # Import after defining test cases
    import re
    
    def filter_thinking_tags(text, config):
        """Simulate the filter function."""
        enabled = config.get("enabled", False)
        
        if not enabled:
            return text, text
        
        start_tag = config.get("start_tag", "<think>")
        end_tag = config.get("end_tag", "</think>")
        
        # Escape special regex characters in tags
        start_tag_escaped = re.escape(start_tag)
        end_tag_escaped = re.escape(end_tag)
        
        # Pattern to match start_tag...end_tag (non-greedy, case-sensitive)
        pattern = f"{start_tag_escaped}.*?{end_tag_escaped}"
        
        # Remove all occurrences of the pattern
        filtered_text = re.sub(pattern, "", text, flags=re.DOTALL)
        
        # Clean up any excessive whitespace left behind
        filtered_text = re.sub(r'\n\n\n+', '\n\n', filtered_text)
        filtered_text = filtered_text.strip()
        
        return text, filtered_text
    
    # Run tests
    passed = 0
    failed = 0
    
    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Input: {repr(test['input'])}")
        print(f"Config: {test['config']}")
        
        full, filtered = filter_thinking_tags(test['input'], test['config'])
        
        print(f"Expected: {repr(test['expected'])}")
        print(f"Got: {repr(filtered)}")
        
        if filtered == test['expected']:
            print("✓ PASSED")
            passed += 1
        else:
            print("✗ FAILED")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0

def test_config():
    """Test config loading with thinking filter."""
    print("\nTesting Config Manager...")
    print("="*60)
    
    try:
        config = ConfigManager('config.example.json')
        thinking_filter = config.get('thinking_filter', {})
        
        print(f"Thinking Filter Config:")
        print(f"  Enabled: {thinking_filter.get('enabled', False)}")
        print(f"  Start Tag: {thinking_filter.get('start_tag', '<think>')}")
        print(f"  End Tag: {thinking_filter.get('end_tag', '</think>')}")
        print("✓ Config loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Error loading config: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("THINKING FILTER TEST SUITE")
    print("="*60)
    
    filter_ok = test_filter()
    config_ok = test_config()
    
    print("\n" + "="*60)
    if filter_ok and config_ok:
        print("✓ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("✗ SOME TESTS FAILED")
        sys.exit(1)
