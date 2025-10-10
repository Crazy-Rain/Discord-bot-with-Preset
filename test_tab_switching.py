#!/usr/bin/env python3
"""Test script to verify tab switching functionality."""
import re
import sys

def test_switchTab_function_signature():
    """Test that switchTab function has correct signature."""
    print("Test: switchTab function signature...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Find the switchTab function definition
    pattern = r'function\s+switchTab\s*\([^)]*\)\s*{'
    match = re.search(pattern, html_content)
    
    assert match, "switchTab function not found"
    
    # Extract the function signature
    signature = match.group(0)
    print(f"  Found signature: {signature}")
    
    # The function should accept at least tabName parameter
    # It should also handle event properly
    assert 'switchTab' in signature, "Function name not found"
    
    # Check if the function uses event.target
    func_start = match.start()
    # Find the end of the function (next function or end of script)
    next_func = re.search(r'\n\s*function\s+', html_content[func_start + len(signature):])
    if next_func:
        func_body = html_content[func_start:func_start + len(signature) + next_func.start()]
    else:
        func_body = html_content[func_start:func_start + 500]  # Get enough of the function
    
    if 'event.target' in func_body or 'event.' in func_body:
        print("  ⚠ Function uses 'event' object")
        # Check if event is a parameter
        if 'event' not in signature and 'Event' not in signature:
            print("  ✗ Function uses 'event' but doesn't accept it as parameter")
            return False
    
    print("✓ switchTab function signature is valid")
    return True

def test_tab_onclick_handlers():
    """Test that tab buttons have proper onclick handlers."""
    print("\nTest: Tab button onclick handlers...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Find all tab buttons
    tab_pattern = r'<button\s+class="tab[^"]*"\s+onclick="switchTab\(\'(\w+)\'\)"[^>]*>'
    tabs = re.findall(tab_pattern, html_content)
    
    assert len(tabs) > 0, "No tab buttons found"
    print(f"  Found {len(tabs)} tab buttons: {', '.join(tabs)}")
    
    # Expected tabs
    expected_tabs = ['config', 'presets', 'characters', 'user_characters', 'lorebook', 'servers']
    for expected in expected_tabs:
        assert expected in tabs, f"Missing tab: {expected}"
    
    print("✓ All tab buttons have proper onclick handlers")
    return True

def test_tab_content_elements():
    """Test that all tab content elements exist."""
    print("\nTest: Tab content elements...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Expected tab content IDs
    expected_tabs = ['config', 'presets', 'characters', 'user_characters', 'lorebook', 'servers']
    
    for tab_id in expected_tabs:
        pattern = f'<div\\s+id="{tab_id}"\\s+class="tab-content[^"]*"'
        assert re.search(pattern, html_content), f"Missing tab content element: {tab_id}"
        print(f"  ✓ Found tab content: {tab_id}")
    
    print("✓ All tab content elements exist")
    return True

def test_active_tab_classes():
    """Test that CSS classes for active tabs are defined."""
    print("\nTest: Active tab CSS classes...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Check for tab active class
    assert re.search(r'\.tab\.active\s*{', html_content), "Missing .tab.active CSS class"
    print("  ✓ Found .tab.active CSS class")
    
    # Check for tab-content active class  
    assert re.search(r'\.tab-content\.active\s*{', html_content), "Missing .tab-content.active CSS class"
    print("  ✓ Found .tab-content.active CSS class")
    
    print("✓ Active tab CSS classes are defined")
    return True

def test_switchTab_event_handling():
    """Test that switchTab properly handles event parameter."""
    print("\nTest: switchTab event handling...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Find switchTab function
    func_match = re.search(r'function\s+switchTab\s*\([^)]*\)\s*{([^}]*(?:{[^}]*}[^}]*)*)}', html_content, re.DOTALL)
    
    assert func_match, "switchTab function not found"
    
    func_body = func_match.group(0)
    
    # Check if function uses event
    uses_event = 'event.' in func_body
    
    if uses_event:
        # If it uses event, it should either:
        # 1. Accept event as parameter, OR
        # 2. Use event from inline onclick (which passes it implicitly)
        
        # Check the function signature
        sig_match = re.search(r'function\s+switchTab\s*\(([^)]*)\)', func_body)
        params = sig_match.group(1) if sig_match else ""
        
        # For inline onclick handlers, 'event' is available as a global
        # But it's better practice to pass it explicitly or use this
        if 'event' not in params.lower():
            print("  ⚠ Function uses 'event' without explicit parameter")
            print("  Note: This may fail in strict mode or modern browsers")
            return False
    
    print("✓ switchTab event handling is correct")
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("Tab Switching Functionality Tests")
    print("=" * 60)
    
    tests = [
        test_tab_onclick_handlers,
        test_tab_content_elements,
        test_active_tab_classes,
        test_switchTab_function_signature,
        test_switchTab_event_handling,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except AssertionError as e:
            print(f"  ✗ Test failed: {e}")
            results.append(False)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    passed = sum(1 for r in results if r)
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
