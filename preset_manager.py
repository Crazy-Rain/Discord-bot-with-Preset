"""Preset manager for handling chat presets."""
import json
import os
from typing import Dict, Any, List, Optional

class PresetManager:
    def __init__(self, presets_dir: str = "presets"):
        self.presets_dir = presets_dir
        self.ensure_presets_dir()
        self.current_preset = None
    
    def ensure_presets_dir(self) -> None:
        """Ensure presets directory exists."""
        if not os.path.exists(self.presets_dir):
            os.makedirs(self.presets_dir)
    
    def load_preset(self, preset_name: str) -> Dict[str, Any]:
        """Load a preset from file."""
        preset_path = os.path.join(self.presets_dir, f"{preset_name}.json")
        if not os.path.exists(preset_path):
            raise FileNotFoundError(f"Preset not found: {preset_name}")
        
        with open(preset_path, "r") as f:
            preset = json.load(f)
        
        self.current_preset = preset
        return preset
    
    def get_preset(self, preset_name: str) -> Dict[str, Any]:
        """Get a preset from file without setting it as current."""
        preset_path = os.path.join(self.presets_dir, f"{preset_name}.json")
        if not os.path.exists(preset_path):
            raise FileNotFoundError(f"Preset not found: {preset_name}")
        
        with open(preset_path, "r") as f:
            return json.load(f)
    
    def save_preset(self, preset_name: str, preset_data: Dict[str, Any]) -> None:
        """Save a preset to file."""
        preset_path = os.path.join(self.presets_dir, f"{preset_name}.json")
        with open(preset_path, "w") as f:
            json.dump(preset_data, f, indent=2)
    
    def list_presets(self) -> List[str]:
        """List all available presets."""
        if not os.path.exists(self.presets_dir):
            return []
        
        presets = []
        for file in os.listdir(self.presets_dir):
            if file.endswith(".json"):
                presets.append(file[:-5])  # Remove .json extension
        return presets
    
    def delete_preset(self, preset_name: str) -> None:
        """Delete a preset."""
        preset_path = os.path.join(self.presets_dir, f"{preset_name}.json")
        if os.path.exists(preset_path):
            os.remove(preset_path)
    
    def export_preset(self, preset_name: str) -> str:
        """Export preset as JSON string."""
        preset = self.load_preset(preset_name)
        return json.dumps(preset, indent=2)
    
    def import_preset(self, preset_name: str, preset_json: str) -> None:
        """Import preset from JSON string."""
        preset_data = json.loads(preset_json)
        self.save_preset(preset_name, preset_data)
    
    def get_current_preset(self) -> Dict[str, Any]:
        """Get the current active preset."""
        return self.current_preset or {}
    
    def format_character_for_prompt(self, character_data: Dict[str, Any], preset: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Format character card data according to preset's prompt formatting rules.
        Returns a dict with 'system_messages', 'example_messages' that can be used to build the message list.
        
        Args:
            character_data: Character card data
            preset: Current preset (uses self.current_preset if not provided)
        
        Returns:
            Dict with keys:
                - 'system_prompt': Main system prompt text
                - 'character_system': Character info as system message (if applicable)
                - 'example_dialogues': List of example message dicts with role/content
        """
        if preset is None:
            preset = self.current_preset or {}
        
        result = {
            'system_prompt': preset.get('system_prompt', ''),
            'character_system': '',
            'example_dialogues': []
        }
        
        if not character_data:
            return result
        
        # Get prompt format settings from preset
        prompt_format = preset.get('prompt_format', 'default')
        char_position = preset.get('character_position', 'system')  # 'system', 'examples', or 'both'
        include_examples = preset.get('include_examples', True)
        example_separator = preset.get('example_separator', '<START>')
        
        # Build character description
        name = character_data.get('name', 'Assistant')
        description = character_data.get('description', '')
        personality = character_data.get('personality', '')
        scenario = character_data.get('scenario', '')
        
        # Check if character has custom system_prompt
        if character_data.get('system_prompt'):
            result['system_prompt'] = character_data['system_prompt']
        
        # Build character info for system message
        if char_position in ['system', 'both'] and description:
            char_info = f"You are {name}."
            if description:
                char_info += f" {description}"
            if personality:
                char_info += f"\n\nPersonality: {personality}"
            if scenario:
                char_info += f"\n\nScenario: {scenario}"
            result['character_system'] = char_info
        
        # Parse example dialogues from character card
        if include_examples and char_position in ['examples', 'both']:
            # Check for mes_example field (SillyTavern format)
            mes_example = character_data.get('mes_example', '')
            if mes_example:
                # Parse <START> separated examples
                examples = mes_example.split(example_separator)
                for example in examples:
                    example = example.strip()
                    if not example:
                        continue
                    
                    # Parse example dialogue lines
                    lines = example.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Try to parse "User:" or "Assistant:" or character name format
                        if line.startswith('User:') or line.startswith('{{user}}:'):
                            content = line.split(':', 1)[1].strip()
                            result['example_dialogues'].append({
                                'role': 'user',
                                'content': content
                            })
                        elif line.startswith(f'{name}:') or line.startswith('Assistant:') or line.startswith('{{char}}:'):
                            content = line.split(':', 1)[1].strip()
                            result['example_dialogues'].append({
                                'role': 'assistant',
                                'content': content
                            })
                        else:
                            # Assume it's continuation of previous message or assistant message
                            if result['example_dialogues'] and result['example_dialogues'][-1]['role'] == 'assistant':
                                result['example_dialogues'][-1]['content'] += '\n' + line
                            else:
                                result['example_dialogues'].append({
                                    'role': 'assistant',
                                    'content': line
                                })
            
            # Check for first_mes field
            first_mes = character_data.get('first_mes', '')
            if first_mes:
                result['example_dialogues'].insert(0, {
                    'role': 'assistant',
                    'content': first_mes
                })
        
        return result
