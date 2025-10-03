"""Configuration manager for Discord bot."""
import json
import os
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if not os.path.exists(self.config_path):
            # Copy example config if config doesn't exist
            if os.path.exists("config.example.json"):
                with open("config.example.json", "r") as f:
                    example_config = json.load(f)
                with open(self.config_path, "w") as f:
                    json.dump(example_config, f, indent=2)
                print(f"Created {self.config_path} from example. Please update with your settings.")
                return example_config
            else:
                raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, "r") as f:
            return json.load(f)
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values."""
        self.config.update(updates)
        self.save_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
    
    def save_api_config(self, name: str, api_key: str, base_url: str, model: str) -> None:
        """Save an API configuration with a given name."""
        if 'saved_api_configs' not in self.config:
            self.config['saved_api_configs'] = {}
        
        self.config['saved_api_configs'][name] = {
            'api_key': api_key,
            'base_url': base_url,
            'model': model
        }
        self.save_config()
    
    def get_api_configs(self) -> Dict[str, Any]:
        """Get all saved API configurations."""
        return self.config.get('saved_api_configs', {})
    
    def get_api_config(self, name: str) -> Dict[str, Any]:
        """Get a specific saved API configuration."""
        configs = self.get_api_configs()
        return configs.get(name, {})
    
    def delete_api_config(self, name: str) -> bool:
        """Delete a saved API configuration."""
        if 'saved_api_configs' in self.config and name in self.config['saved_api_configs']:
            del self.config['saved_api_configs'][name]
            self.save_config()
            return True
        return False
