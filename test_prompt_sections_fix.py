#!/usr/bin/env python3
"""Test that the frontend handles prompt_sections structure correctly."""
import re

def test_loadDefaultConfig_handles_prompt_sections():
    """Test that loadDefaultConfig handles the new prompt_sections structure."""
    print("Test: loadDefaultConfig handles prompt_sections structure...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Extract the loadDefaultConfig function
    func_match = re.search(r'async function loadDefaultConfig\(\).*?(?=\n        async function|\n        function|\Z)', html_content, re.DOTALL)
    if not func_match:
        raise AssertionError("Could not find loadDefaultConfig function")
    
    func_content = func_match.group(0)
    
    # Check that it handles prompt_sections
    if 'prompt_sections' not in func_content:
        raise AssertionError("loadDefaultConfig should check for prompt_sections structure")
    
    # Check that it still has backward compatibility with system_prompt
    if 'system_prompt' not in func_content:
        raise AssertionError("loadDefaultConfig should maintain backward compatibility with system_prompt")
    
    # Check for safe element access
    if 'getElementById(\'default-preset-display\')' in func_content:
        # Should check if element exists before using it
        if 'if (defaultPresetEl)' not in func_content:
            raise AssertionError("loadDefaultConfig should check if defaultPresetEl exists before using it")
    
    if 'getElementById(\'default-api-display\')' in func_content:
        # Should check if element exists before using it
        if 'if (defaultApiEl)' not in func_content:
            raise AssertionError("loadDefaultConfig should check if defaultApiEl exists before using it")
    
    print("✓ loadDefaultConfig handles prompt_sections and has safe element access")

def test_loadServersList_error_handling():
    """Test that loadServersList handles loadDefaultConfig errors gracefully."""
    print("Test: loadServersList handles loadDefaultConfig errors gracefully...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Extract the loadServersList function
    func_match = re.search(r'async function loadServersList\(\).*?(?=\n        async function|\n        function|\Z)', html_content, re.DOTALL)
    if not func_match:
        raise AssertionError("Could not find loadServersList function")
    
    func_content = func_match.group(0)
    
    # Check that loadDefaultConfig is wrapped in try-catch
    # Pattern: try { await loadDefaultConfig(); } catch (error) { ... }
    pattern = r'try\s*\{\s*await loadDefaultConfig\(\);?\s*\}\s*catch\s*\('
    
    if not re.search(pattern, func_content):
        raise AssertionError("loadServersList should wrap loadDefaultConfig in try-catch to prevent errors from blocking server loading")
    
    # Make sure the main server loading logic is outside the inner try-catch
    # and proceeds even if loadDefaultConfig fails
    if 'await fetch(\'/api/servers\')' not in func_content:
        raise AssertionError("loadServersList should still fetch servers")
    
    print("✓ loadServersList handles loadDefaultConfig errors gracefully")

def test_error_handling_in_catch_block():
    """Test that error handling in catch block is safe."""
    print("Test: Error handling in catch block is safe...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Extract the loadDefaultConfig function
    func_match = re.search(r'async function loadDefaultConfig\(\).*?(?=\n        async function|\n        function|\Z)', html_content, re.DOTALL)
    if not func_match:
        raise AssertionError("Could not find loadDefaultConfig function")
    
    func_content = func_match.group(0)
    
    # Find the catch block
    catch_match = re.search(r'catch\s*\([^)]+\)\s*\{([^}]+)\}', func_content, re.DOTALL)
    if not catch_match:
        raise AssertionError("loadDefaultConfig should have a catch block")
    
    catch_content = catch_match.group(1)
    
    # Check that elements are safely accessed in the catch block
    if 'getElementById' in catch_content:
        # Should check if elements exist before setting innerHTML
        if 'if (' not in catch_content:
            raise AssertionError("Catch block should check if elements exist before accessing them")
    
    print("✓ Error handling in catch block is safe")

if __name__ == "__main__":
    try:
        print("\n=== Testing Prompt Sections Fix ===\n")
        test_loadDefaultConfig_handles_prompt_sections()
        test_loadServersList_error_handling()
        test_error_handling_in_catch_block()
        print("\n=== All Tests Passed! ===\n")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)
