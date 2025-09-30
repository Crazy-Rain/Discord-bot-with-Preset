"""Preset manager for handling chat presets."""
import json
import os
from typing import Dict, Any, List

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
