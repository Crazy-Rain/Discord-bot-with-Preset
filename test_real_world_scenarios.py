#!/usr/bin/env python3
"""
Real-world scenario tests for config and lorebook fixes.
These tests simulate actual user workflows.
"""

import sys
import json
import tempfile
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_manager import ConfigManager
from discord_bot import DiscordBot
from lorebook_manager import LorebookManager

def scenario_1_user_changes_proxy():
    """
    Scenario: User wants to switch from OpenAI to a local proxy.
    Steps:
    1. Bot is running with OpenAI API
    2. User loads a saved config for local proxy  
    3. User clicks Save Configuration
    4. Next message should use the new proxy
    """
    print("\n" + "=" * 70)
    print("SCENARIO 1: User Changes Proxy via Web Interface")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_data = {
            'openai_config': {
                'api_key': 'sk-openai-key-123',
                'base_url': 'https://api.openai.com/v1',
                'model': 'gpt-3.5-turbo'
            },
            'saved_api_configs': {
                'Local Ollama': {
                    'api_key': 'ollama',
                    'base_url': 'http://localhost:11434/v1',
                    'model': 'llama2'
                }
            }
        }
        json.dump(config_data, f, indent=2)
        temp_config_path = f.name
    
    try:
        # Step 1: Bot starts with OpenAI
        print("\n1. Bot starts with OpenAI API...")
        config_manager = ConfigManager(temp_config_path)
        bot = DiscordBot(config_manager)
        print(f"   Current URL: {bot.openai_client.client.base_url}")
        
        # Step 2: User loads "Local Ollama" config (fills form fields)
        print("\n2. User loads 'Local Ollama' config in web interface...")
        saved_config = config_manager.get_api_config('Local Ollama')
        print(f"   Loaded config: {saved_config}")
        
        # Step 3: User clicks Save (API key is hidden, so it's deleted from update)
        print("\n3. User clicks 'Save Configuration'...")
        update_data = {
            'openai_config': {
                # api_key is '***HIDDEN***' so it's deleted
                'base_url': saved_config['base_url'],
                'model': saved_config['model']
            }
        }
        
        # Simulate web server logic
        openai_config_changed = False
        new_base_url = None
        new_model = None
        
        if 'openai_config' in update_data:
            if 'base_url' in update_data['openai_config']:
                current_base_url = config_manager.get('openai_config.base_url')
                if update_data['openai_config']['base_url'] != current_base_url:
                    openai_config_changed = True
                    new_base_url = update_data['openai_config']['base_url']
            
            if 'model' in update_data['openai_config']:
                current_model = config_manager.get('openai_config.model')
                if update_data['openai_config']['model'] != current_model:
                    openai_config_changed = True
                    new_model = update_data['openai_config']['model']
        
        config_manager.update_config(update_data)
        
        # Verify API key preserved
        api_key = config_manager.get('openai_config.api_key')
        if api_key != 'sk-openai-key-123':
            print(f"   ❌ FAIL: API key lost! Got: {api_key}")
            return False
        print(f"   ✓ API key preserved: {api_key}")
        
        # Apply to bot
        if openai_config_changed:
            if new_base_url is None:
                new_base_url = config_manager.get('openai_config.base_url')
            if new_model is None:
                new_model = config_manager.get('openai_config.model')
            
            bot.update_openai_config(
                api_key=config_manager.get('openai_config.api_key'),
                base_url=new_base_url,
                model=new_model
            )
        
        # Step 4: Verify next message uses new proxy
        print("\n4. User sends message in Discord...")
        client = bot.get_openai_client_for_channel(channel_id=12345)
        print(f"   Message will be sent to: {client.client.base_url}")
        print(f"   Using model: {client.model}")
        
        if 'localhost:11434' in str(client.client.base_url):
            print("\n✅ SUCCESS: Bot switched to local proxy!")
            return True
        else:
            print(f"\n❌ FAIL: Still using old proxy: {client.client.base_url}")
            return False
            
    finally:
        os.unlink(temp_config_path)

def scenario_2_character_with_lorebooks():
    """
    Scenario: User wants to use a character with custom lorebooks.
    Steps:
    1. Create a character-linked lorebook
    2. Create a global lorebook
    3. Load the character
    4. Send a message
    5. Verify both lorebooks are used
    """
    print("\n" + "=" * 70)
    print("SCENARIO 2: Character with Multiple Lorebooks")
    print("=" * 70)
    
    # Step 1: Create lorebooks
    print("\n1. User creates lorebooks in web interface...")
    
    lorebook_manager = LorebookManager()
    
    # Global world lore
    lorebook_manager.create_lorebook(
        name="Fantasy World",
        description="Core world building",
        enabled=True,
        linked_characters=None
    )
    lorebook_manager.add_or_update_entry(
        key="Magic System",
        content="Magic is powered by ancient crystals that glow in moonlight.",
        keywords=["magic", "spell", "crystal"],
        activation_type="constant",
        lorebook_name="Fantasy World"
    )
    print("   ✓ Created 'Fantasy World' (global, constant)")
    
    # Character-specific lore
    lorebook_manager.create_lorebook(
        name="Luna Background",
        description="Luna's personal history",
        enabled=True,
        linked_characters=["Luna"]
    )
    lorebook_manager.add_or_update_entry(
        key="Luna's Origin",
        content="Luna is the last surviving moon elf from the Silver Kingdom.",
        keywords=["luna", "past", "origin"],
        activation_type="constant",
        lorebook_name="Luna Background"
    )
    print("   ✓ Created 'Luna Background' (linked to Luna, constant)")
    
    # Step 2: Setup bot with character
    print("\n2. User loads Luna character for Discord channel...")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_data = {
            'openai_config': {
                'api_key': 'test',
                'base_url': 'https://api.openai.com/v1',
                'model': 'gpt-3.5-turbo'
            }
        }
        json.dump(config_data, f, indent=2)
        temp_config_path = f.name
    
    try:
        config_manager = ConfigManager(temp_config_path)
        bot = DiscordBot(config_manager)
        bot.lorebook_manager = lorebook_manager  # Use our test lorebook manager
        
        # Simulate !character luna command
        bot.channel_characters[12345] = {"name": "Luna"}
        print("   ✓ Luna loaded for channel 12345")
        
        # Step 3: User sends message
        print("\n3. User sends message 'Tell me about magic'...")
        
        # Suppress debug logs for cleaner output
        import io
        import contextlib
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            messages = bot.build_chat_messages(
                channel_id=12345,
                user_message="Tell me about magic",
                character_name=None,
                server_id=None
            )
        
        # Find system message
        system_msg = next((m for m in messages if m['role'] == 'system'), None)
        if not system_msg:
            print("   ❌ FAIL: No system message found!")
            return False
        
        # Step 4: Verify lorebooks
        print("\n4. Checking if lorebooks are included...")
        
        has_magic = "Magic System" in system_msg['content']
        has_luna = "Luna's Origin" in system_msg['content']
        
        print(f"   Contains 'Magic System' (global): {has_magic}")
        print(f"   Contains 'Luna's Origin' (character): {has_luna}")
        
        if has_magic and has_luna:
            print("\n✅ SUCCESS: Both lorebooks included in AI prompt!")
            return True
        else:
            print("\n❌ FAIL: Lorebooks missing from prompt!")
            print(f"   System prompt preview: {system_msg['content'][:200]}...")
            return False
            
    finally:
        os.unlink(temp_config_path)

def scenario_3_disabled_lorebook():
    """
    Scenario: User has a lorebook but disabled it.
    It should NOT be included.
    """
    print("\n" + "=" * 70)
    print("SCENARIO 3: Disabled Lorebook Should Not Appear")
    print("=" * 70)
    
    lorebook_manager = LorebookManager()
    
    # Create enabled lorebook
    lorebook_manager.create_lorebook("Active", enabled=True)
    lorebook_manager.add_or_update_entry(
        "Active Entry", "This should appear.",
        activation_type="constant",
        lorebook_name="Active"
    )
    
    # Create disabled lorebook
    lorebook_manager.create_lorebook("Inactive", enabled=False)
    lorebook_manager.add_or_update_entry(
        "Inactive Entry", "This should NOT appear.",
        activation_type="constant",
        lorebook_name="Inactive"
    )
    
    print("   ✓ Created one enabled and one disabled lorebook")
    
    # Get prompt
    import io
    import contextlib
    
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        prompt = lorebook_manager.get_system_prompt_section()
    
    has_active = "Active Entry" in prompt
    has_inactive = "Inactive Entry" in prompt
    
    print(f"\n   Contains 'Active Entry': {has_active}")
    print(f"   Contains 'Inactive Entry': {has_inactive}")
    
    if has_active and not has_inactive:
        print("\n✅ SUCCESS: Only enabled lorebook included!")
        return True
    else:
        print("\n❌ FAIL: Disabled lorebook was included!")
        return False

def main():
    """Run all scenario tests."""
    print("\n" + "=" * 70)
    print("REAL-WORLD SCENARIO TESTS")
    print("=" * 70)
    
    # Clean up lorebook directory
    import shutil
    lorebook_dir = os.path.join(os.path.dirname(__file__), 'lorebook')
    if os.path.exists(lorebook_dir):
        shutil.rmtree(lorebook_dir)
    
    scenarios = [
        ("User Changes Proxy", scenario_1_user_changes_proxy),
        ("Character with Lorebooks", scenario_2_character_with_lorebooks),
        ("Disabled Lorebook", scenario_3_disabled_lorebook),
    ]
    
    results = []
    for name, func in scenarios:
        try:
            result = func()
            results.append((name, result))
            # Clean up between scenarios
            if os.path.exists(lorebook_dir):
                shutil.rmtree(lorebook_dir)
        except Exception as e:
            print(f"\n❌ ERROR in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("SCENARIO TEST SUMMARY")
    print("=" * 70)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(r for _, r in results)
    print(f"\n{'✅ ALL SCENARIOS PASSED' if all_passed else '❌ SOME SCENARIOS FAILED'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
