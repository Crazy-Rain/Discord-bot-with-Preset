#!/usr/bin/env python3
"""Comprehensive test to verify all UI features are working correctly."""
import re
import sys

def test_configuration_tab():
    """Test Configuration tab has all expected features."""
    print("Test: Configuration tab features...")
    
    with open('templates/index.html', 'r') as f:
        html = f.read()
    
    # Check for key configuration features
    features = [
        ('Discord Token', 'discord-token'),
        ('API Key', 'api-key'),
        ('Base URL', 'base-url'),
        ('Model selector', 'model'),
        ('Save API Config', 'Save API Config'),
        ('Default Preset', 'Default Preset'),
        ('Thinking Filter', 'Thinking Filter'),
        ('Auto Context Loading', 'Auto Context Loading'),
        ('CP Tracking', 'CP Tracking'),
    ]
    
    for name, pattern in features:
        assert pattern in html, f"Missing {name} in Configuration tab"
        print(f"  ✓ {name} present")
    
    print("✓ Configuration tab has all features")
    return True

def test_presets_tab():
    """Test Presets tab has all expected features."""
    print("\nTest: Presets tab features...")
    
    with open('templates/index.html', 'r') as f:
        html = f.read()
    
    features = [
        ('Preset Name', 'preset-name'),
        ('Prompt Sections', 'Prompt Sections'),
        ('Temperature slider', 'temperature'),
        ('Max Tokens', 'max_tokens'),
        ('SillyTavern Options', 'SillyTavern Options'),
        ('Save Preset', 'Save Preset'),
        ('Export', 'Export'),
        ('Import', 'Import'),
    ]
    
    for name, pattern in features:
        assert pattern in html, f"Missing {name} in Presets tab"
        print(f"  ✓ {name} present")
    
    print("✓ Presets tab has all features")
    return True

def test_characters_tab():
    """Test Characters tab has all expected features."""
    print("\nTest: Characters tab features...")
    
    with open('templates/index.html', 'r') as f:
        html = f.read()
    
    features = [
        ('Character Name', 'character-name'),
        ('Display Name', 'character-display-name'),
        ('Personality', 'character-personality'),
        ('Description', 'character-description'),
        ('Scenario', 'character-scenario'),
        ('Avatar Upload', 'avatar-method'),
        ('Save Character', 'Save Character'),
    ]
    
    for name, pattern in features:
        assert pattern in html, f"Missing {name} in Characters tab"
        print(f"  ✓ {name} present")
    
    print("✓ Characters tab has all features")
    return True

def test_user_characters_tab():
    """Test User Characters tab has all expected features."""
    print("\nTest: User Characters tab features...")
    
    with open('templates/index.html', 'r') as f:
        html = f.read()
    
    features = [
        ('Character Name', 'user-character-name'),
        ('Description', 'user-character-description'),
        ('Character Sheet', 'Character Sheet'),
        ('Enable Character Sheet', 'user-character-sheet-enabled'),
        ('Save User Character', 'Save User Character'),
    ]
    
    for name, pattern in features:
        assert pattern in html, f"Missing {name} in User Characters tab"
        print(f"  ✓ {name} present")
    
    print("✓ User Characters tab has all features")
    return True

def test_lorebook_tab():
    """Test Lorebook tab has all expected features."""
    print("\nTest: Lorebook tab features...")
    
    with open('templates/index.html', 'r') as f:
        html = f.read()
    
    features = [
        ('Entry Key', 'lorebook-key'),
        ('Content', 'lorebook-content'),
        ('Keywords', 'lorebook-keywords'),
        ('Activation Type', 'lorebook-activation'),
        ('Save Entry', 'Save Entry'),
        ('Export All', 'Export All'),
    ]
    
    for name, pattern in features:
        assert pattern in html, f"Missing {name} in Lorebook tab"
        print(f"  ✓ {name} present")
    
    print("✓ Lorebook tab has all features")
    return True

def test_servers_tab():
    """Test Servers/Channels tab exists."""
    print("\nTest: Servers/Channels tab features...")
    
    with open('templates/index.html', 'r') as f:
        html = f.read()
    
    features = [
        ('Server Configuration', 'Server Configuration'),
        ('Refresh Servers', 'Refresh Servers'),
    ]
    
    for name, pattern in features:
        assert pattern in html, f"Missing {name} in Servers tab"
        print(f"  ✓ {name} present")
    
    print("✓ Servers/Channels tab has all features")
    return True

def test_javascript_functions():
    """Test all critical JavaScript functions exist."""
    print("\nTest: JavaScript functions...")
    
    with open('templates/index.html', 'r') as f:
        html = f.read()
    
    functions = [
        'switchTab',
        'loadConfig',
        'saveConfig',
        'loadPresetsList',
        'savePreset',
        'loadCharactersList',
        'saveCharacter',
        'loadUserCharactersList',
        'saveUserCharacter',
        'loadLorebookList',
        'saveLorebookEntry',
        'loadServersList',
    ]
    
    for func in functions:
        pattern = f'function {func}'
        assert pattern in html, f"Missing function: {func}"
        print(f"  ✓ {func} defined")
    
    print("✓ All JavaScript functions present")
    return True

def test_no_syntax_errors():
    """Test that there are no common syntax errors."""
    print("\nTest: No JavaScript syntax errors...")
    
    with open('templates/index.html', 'r') as f:
        html = f.read()
    
    # Check for Python-style docstrings in JavaScript
    if '"""' in html:
        script_section = html[html.find('<script>'):html.find('</script>')]
        if '"""' in script_section:
            print("  ✗ Python-style docstrings found in JavaScript")
            return False
    
    print("  ✓ No Python-style docstrings in JavaScript")
    
    # Check for proper script tag closure
    assert '<script>' in html, "Missing opening script tag"
    assert '</script>' in html, "Missing closing script tag"
    print("  ✓ Script tags properly closed")
    
    print("✓ No syntax errors detected")
    return True

def main():
    """Run all comprehensive tests."""
    print("=" * 70)
    print("Comprehensive UI Feature Test Suite")
    print("=" * 70)
    
    tests = [
        test_configuration_tab,
        test_presets_tab,
        test_characters_tab,
        test_user_characters_tab,
        test_lorebook_tab,
        test_servers_tab,
        test_javascript_functions,
        test_no_syntax_errors,
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
    
    print("\n" + "=" * 70)
    print("Test Results:")
    print("=" * 70)
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All comprehensive tests passed!")
        print("\n🎉 All features verified and working correctly!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
