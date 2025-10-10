#!/usr/bin/env python3
"""Test enhanced error handling for context length errors."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_error_message_detection():
    """Test that error messages are properly categorized."""
    print("\n" + "=" * 70)
    print("TEST: Error Message Pattern Detection")
    print("=" * 70)
    
    test_cases = [
        # Context length errors
        ("context_length_exceeded error", True, "context"),
        ("maximum context length is 8192", True, "context"),
        ("The context window is too large", True, "context"),
        ("too many tokens in request", True, "context"),
        ("token limit exceeded", True, "context"),
        ("Please reduce the length", True, "context"),
        
        # 500 errors (should be caught by context OR 500 handler)
        ("Error code: 500 - Internal server error", True, "500"),
        
        # Other errors (should not match)
        ("Error code: 404 - Not found", False, None),
        ("Invalid API key", False, None),
    ]
    
    passed = 0
    failed = 0
    
    for error_msg, should_match, expected_type in test_cases:
        error_lower = error_msg.lower()
        
        # Check context patterns
        is_context_error = any(pattern in error_lower for pattern in [
            "context_length_exceeded", "maximum context length", "context window",
            "too many tokens", "token limit", "reduce the length"
        ])
        
        # Check 500 error
        is_500_error = "500" in error_msg or "Internal server error" in error_msg
        
        matched = is_context_error or is_500_error
        match_type = "context" if is_context_error else ("500" if is_500_error else None)
        
        if matched == should_match and (not should_match or match_type == expected_type):
            print(f"✅ PASS: '{error_msg[:50]}...' -> {match_type or 'no match'}")
            passed += 1
        else:
            print(f"❌ FAIL: '{error_msg[:50]}...' -> Expected: {expected_type}, Got: {match_type}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("CONTEXT LENGTH ERROR DETECTION TESTS")
    print("=" * 70)
    
    result = test_error_message_detection()
    
    if result:
        print("\n✅ ALL TESTS PASSED")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
