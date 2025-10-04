"""Mock test to demonstrate the new server configuration UI."""
import json

# Create a mock config showing the new structure
mock_config = {
    "discord_token": "MOCK_TOKEN",
    "openai_config": {
        "api_key": "mock_key",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4"
    },
    "server_configs": {
        "123456789": {
            "preset": "creative",
            "api_config": "openai_gpt4",
            "character": "luna"
        },
        "987654321": {
            "preset": "analytical",
            "api_config": "",
            "character": "sherlock"
        }
    },
    "channel_configs": {
        "555666777": {
            "preset": "roleplay",
            "api_config": "",
            "character": "aria"
        }
    }
}

# Show the configuration structure
print("=" * 60)
print("NEW CONFIGURATION STRUCTURE")
print("=" * 60)
print()
print("Server Configurations (set via Web UI):")
print("-" * 60)
for server_id, config in mock_config["server_configs"].items():
    print(f"  Server {server_id}:")
    print(f"    - Preset: {config['preset']}")
    print(f"    - API Config: {config['api_config'] or '(default)'}")
    print(f"    - Character: {config['character'] or '(none)'}")
    print()

print("Channel Configurations (set via Discord commands):")
print("-" * 60)
for channel_id, config in mock_config["channel_configs"].items():
    print(f"  Channel {channel_id}:")
    print(f"    - Preset: {config['preset']}")
    print(f"    - API Config: {config['api_config'] or '(default)'}")
    print(f"    - Character: {config['character'] or '(none)'}")
    print()

print("=" * 60)
print("CONFIGURATION PRIORITY LOGIC")
print("=" * 60)
print()
print("When determining configuration for a channel:")
print("  1. Check channel_configs (from Discord commands) - HIGHEST")
print("  2. Check server_configs (from Web UI) - MEDIUM")
print("  3. Use defaults - LOWEST")
print()
print("Example:")
print("  Channel 555666777 in Server 123456789:")
print("    - Has channel config → Uses 'roleplay' preset")
print("  Channel 888999000 in Server 123456789:")
print("    - No channel config → Uses server 'creative' preset")
print("  Channel 111222333 in Server 555555555:")
print("    - No channel or server config → Uses default preset")
print()
print("=" * 60)
