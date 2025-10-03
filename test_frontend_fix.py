#!/usr/bin/env python3
"""Test that the frontend handles missing channel_count gracefully."""
import re

def test_frontend_handles_missing_channel_count():
    """Test that the frontend JavaScript safely handles missing channel_count."""
    print("Test: Frontend handles missing channel_count...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Check that we're using a defensive pattern for channel_count
    # Look for: const channelCount = server.channel_count || 0;
    pattern = r'const\s+channelCount\s*=\s*server\.channel_count\s*\|\|\s*0'
    
    if not re.search(pattern, html_content):
        raise AssertionError("Frontend should use defensive pattern: const channelCount = server.channel_count || 0;")
    
    # Verify it's used in the template string
    if '${channelCount}' not in html_content:
        raise AssertionError("Frontend should use ${channelCount} instead of ${server.channel_count}")
    
    # Make sure we're not directly using server.channel_count in the template
    # (after the defensive assignment)
    loadServersList_func = re.search(r'async function loadServersList\(\).*?(?=async function|\Z)', html_content, re.DOTALL)
    if loadServersList_func:
        func_content = loadServersList_func.group(0)
        # Find the defensive assignment
        defensive_pattern = re.search(pattern, func_content)
        if defensive_pattern:
            # Check if server.channel_count is used AFTER the defensive assignment
            after_defensive = func_content[defensive_pattern.end():]
            if '${server.channel_count}' in after_defensive:
                raise AssertionError("Frontend should not use ${server.channel_count} directly after defensive assignment")
    
    print("✓ Frontend safely handles missing channel_count")

def test_no_references_to_server_channels():
    """Test that there are no references to server.channels (which would cause the error)."""
    print("Test: No references to server.channels...")
    
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Check that we're not trying to access server.channels anywhere
    if 'server.channels' in html_content:
        raise AssertionError("Frontend should not reference server.channels")
    
    if 'server[\'channels\']' in html_content or 'server["channels"]' in html_content:
        raise AssertionError("Frontend should not reference server['channels'] or server[\"channels\"]")
    
    print("✓ No references to server.channels found")

if __name__ == "__main__":
    try:
        print("\n=== Testing Frontend JavaScript Fix ===\n")
        test_frontend_handles_missing_channel_count()
        test_no_references_to_server_channels()
        print("\n=== All Frontend Tests Passed! ===\n")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)
