"""Character card manager for handling character definitions."""
import json
import os
import base64
from typing import Dict, Any, List, Optional

class CharacterManager:
    def __init__(self, characters_dir: str = "character_cards"):
        self.characters_dir = characters_dir
        self.ensure_characters_dir()
        self.current_character = None
    
    def ensure_characters_dir(self) -> None:
        """Ensure characters directory exists."""
        if not os.path.exists(self.characters_dir):
            os.makedirs(self.characters_dir)
    
    def load_character(self, character_name: str) -> Dict[str, Any]:
        """Load a character card from file."""
        character_path = os.path.join(self.characters_dir, f"{character_name}.json")
        if not os.path.exists(character_path):
            raise FileNotFoundError(f"Character not found: {character_name}")
        
        with open(character_path, "r") as f:
            character = json.load(f)
        
        self.current_character = character
        return character
    
    def save_character(self, character_name: str, character_data: Dict[str, Any]) -> None:
        """Save a character card to file."""
        character_path = os.path.join(self.characters_dir, f"{character_name}.json")
        with open(character_path, "w") as f:
            json.dump(character_data, f, indent=2)
    
    def list_characters(self) -> List[str]:
        """List all available character cards."""
        if not os.path.exists(self.characters_dir):
            return []
        
        characters = []
        for file in os.listdir(self.characters_dir):
            if file.endswith(".json"):
                characters.append(file[:-5])  # Remove .json extension
        return characters
    
    def delete_character(self, character_name: str) -> None:
        """Delete a character card."""
        character_path = os.path.join(self.characters_dir, f"{character_name}.json")
        if os.path.exists(character_path):
            os.remove(character_path)
    
    def export_character(self, character_name: str) -> str:
        """Export character as JSON string."""
        character = self.load_character(character_name)
        return json.dumps(character, indent=2)
    
    def import_character(self, character_name: str, character_json: str) -> None:
        """Import character from JSON string."""
        character_data = json.loads(character_json)
        self.save_character(character_name, character_data)
    
    def get_current_character(self) -> Optional[Dict[str, Any]]:
        """Get the current active character."""
        return self.current_character
    
    def get_character_system_prompt(self) -> str:
        """Get system prompt from current character card."""
        if not self.current_character:
            return ""
        
        # Support multiple character card formats
        # Check if custom system_prompt is provided and not empty
        if "system_prompt" in self.current_character and self.current_character["system_prompt"]:
            return self.current_character["system_prompt"]
        elif "description" in self.current_character:
            name = self.current_character.get("name", "Assistant")
            desc = self.current_character["description"]
            personality = self.current_character.get("personality", "")
            scenario = self.current_character.get("scenario", "")
            
            prompt = f"You are {name}. {desc}"
            if personality:
                prompt += f"\n\nPersonality: {personality}"
            if scenario:
                prompt += f"\n\nScenario: {scenario}"
            return prompt
        
        return ""
