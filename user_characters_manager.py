"""User character manager for handling user character descriptions."""
import json
import os
from typing import Dict, Any, List, Optional

class UserCharactersManager:
    def __init__(self, user_chars_dir: str = "user_characters"):
        self.user_chars_dir = user_chars_dir
        self.ensure_user_chars_dir()
        self.user_characters: Dict[str, Dict[str, str]] = {}
        self.load_all_user_characters()
    
    def ensure_user_chars_dir(self) -> None:
        """Ensure user characters directory exists."""
        if not os.path.exists(self.user_chars_dir):
            os.makedirs(self.user_chars_dir)
    
    def load_all_user_characters(self) -> None:
        """Load all user characters from storage."""
        storage_path = os.path.join(self.user_chars_dir, "user_characters.json")
        if os.path.exists(storage_path):
            with open(storage_path, "r") as f:
                self.user_characters = json.load(f)
        else:
            self.user_characters = {}
    
    def save_all_user_characters(self) -> None:
        """Save all user characters to storage."""
        storage_path = os.path.join(self.user_chars_dir, "user_characters.json")
        with open(storage_path, "w") as f:
            json.dump(self.user_characters, f, indent=2)
    
    def add_or_update_character(self, name: str, description: str, sheet: str = "", sheet_enabled: bool = False) -> None:
        """Add or update a user character."""
        # Preserve existing sheet data if not provided
        existing_char = self.user_characters.get(name, {})
        self.user_characters[name] = {
            "name": name,
            "description": description,
            "sheet": sheet if sheet is not None else existing_char.get("sheet", ""),
            "sheet_enabled": sheet_enabled if sheet is not None else existing_char.get("sheet_enabled", False)
        }
        self.save_all_user_characters()
    
    def get_character(self, name: str) -> Optional[Dict[str, str]]:
        """Get a user character by name."""
        return self.user_characters.get(name)
    
    def delete_character(self, name: str) -> bool:
        """Delete a user character."""
        if name in self.user_characters:
            del self.user_characters[name]
            self.save_all_user_characters()
            return True
        return False
    
    def list_characters(self) -> List[str]:
        """List all user character names."""
        return list(self.user_characters.keys())
    
    def get_all_characters(self) -> Dict[str, Dict[str, str]]:
        """Get all user characters."""
        return self.user_characters.copy()
    
    def export_characters(self) -> str:
        """Export all user characters as JSON string."""
        return json.dumps(self.user_characters, indent=2)
    
    def import_characters(self, characters_json: str) -> None:
        """Import user characters from JSON string."""
        imported = json.loads(characters_json)
        self.user_characters.update(imported)
        self.save_all_user_characters()
    
    def update_character_sheet(self, name: str, sheet: str) -> bool:
        """Update a character's sheet.
        
        Args:
            name: Character name
            sheet: Character sheet content
            
        Returns:
            True if successful, False if character doesn't exist
        """
        if name not in self.user_characters:
            return False
        
        self.user_characters[name]['sheet'] = sheet
        self.save_all_user_characters()
        return True
    
    def set_sheet_enabled(self, name: str, enabled: bool) -> bool:
        """Enable or disable a character's sheet.
        
        Args:
            name: Character name
            enabled: Whether to enable the sheet
            
        Returns:
            True if successful, False if character doesn't exist
        """
        if name not in self.user_characters:
            return False
        
        self.user_characters[name]['sheet_enabled'] = enabled
        self.save_all_user_characters()
        return True
    
    def get_system_prompt_section(self, character_names: List[str]) -> str:
        """Generate system prompt section for specific user characters.
        
        Args:
            character_names: List of character names to include in the prompt
            
        Returns:
            Formatted system prompt section with user character descriptions
        """
        if not character_names:
            return ""
        
        # Filter to only include characters that have descriptions
        described_chars = [name for name in character_names if name in self.user_characters]
        
        if not described_chars:
            return ""
        
        sections = []
        for name in described_chars:
            char_data = self.user_characters[name]
            section = f"""[{name} Description]
Name: {name}
Description: {char_data['description']}"""
            
            # Add character sheet if enabled
            if char_data.get('sheet_enabled', False) and char_data.get('sheet', '').strip():
                section += f"""
[sheet]
This is a sheet of {name}'s Abilities and Perks. Always take them into account when considering what {name} is able to do.
{char_data['sheet']}
[/sheet]"""
            
            section += f"""
Note: This is a User Character, for referencing when {name} is doing something, In scene, or needing to be referenced in some manner. Do not Act, or Write for this Character, they are only for the Human to Act/Write/Play as.
[/{name} Description]"""
            sections.append(section)
        
        if sections:
            return "\n\n" + "\n\n".join(sections)
        
        return ""
