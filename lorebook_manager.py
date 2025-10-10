"""Lorebook manager for handling world-building and lore information."""
import json
import os
from typing import Dict, Any, List, Optional

class LorebookManager:
    def __init__(self, lorebook_dir: str = "lorebook"):
        self.lorebook_dir = lorebook_dir
        self.debug_logging = True  # Always enabled for diagnostics
        self.ensure_lorebook_dir()
        self.lorebooks: Dict[str, Dict[str, Any]] = {}
        self.entries: Dict[str, Dict[str, Any]] = {}  # Legacy flat entries for backward compatibility
        self.load_all_lorebooks()
    
    def ensure_lorebook_dir(self) -> None:
        """Ensure lorebook directory exists."""
        if not os.path.exists(self.lorebook_dir):
            os.makedirs(self.lorebook_dir)
    
    def load_all_lorebooks(self) -> None:
        """Load all lorebooks from storage."""
        # Load new multi-lorebook format
        lorebooks_path = os.path.join(self.lorebook_dir, "lorebooks.json")
        if os.path.exists(lorebooks_path):
            with open(lorebooks_path, "r") as f:
                self.lorebooks = json.load(f)
        else:
            self.lorebooks = {}
        
        # Load legacy single lorebook for backward compatibility
        legacy_path = os.path.join(self.lorebook_dir, "lorebook.json")
        if os.path.exists(legacy_path):
            with open(legacy_path, "r") as f:
                self.entries = json.load(f)
                
            # If we have legacy entries but no "Default" lorebook, migrate them
            if self.entries and "Default" not in self.lorebooks:
                self.lorebooks["Default"] = {
                    "name": "Default",
                    "description": "Default lorebook (migrated from legacy format)",
                    "enabled": True,
                    "entries": self.entries
                }
                self.save_all_lorebooks()
        else:
            self.entries = {}
        
        # Migrate always_active to activation_type in all lorebooks
        self._migrate_always_active_to_activation_type()
        
        # Migrate linked_character to linked_characters
        self._migrate_linked_character_to_list()
    
    def _migrate_always_active_to_activation_type(self) -> None:
        """Migrate old always_active boolean to new activation_type field."""
        needs_save = False
        
        for lorebook_name, lorebook in self.lorebooks.items():
            entries = lorebook.get("entries", {})
            for key, entry in entries.items():
                # If entry has always_active but not activation_type, migrate it
                if "always_active" in entry and "activation_type" not in entry:
                    always_active = entry.get("always_active", False)
                    entry["activation_type"] = "constant" if always_active else "normal"
                    # Keep always_active for backward compatibility but it's now deprecated
                    needs_save = True
                # If entry has neither, default to normal
                elif "activation_type" not in entry:
                    entry["activation_type"] = "normal"
                    needs_save = True
        
        if needs_save:
            self.save_all_lorebooks()
    
    def _migrate_linked_character_to_list(self) -> None:
        """Migrate old linked_character (single string) to new linked_characters (list)."""
        needs_save = False
        
        for lorebook_name, lorebook in self.lorebooks.items():
            # If lorebook has linked_character but not linked_characters, migrate it
            if "linked_character" in lorebook and "linked_characters" not in lorebook:
                linked_char = lorebook.get("linked_character")
                if linked_char:
                    lorebook["linked_characters"] = [linked_char]
                else:
                    lorebook["linked_characters"] = None
                # Remove old field
                del lorebook["linked_character"]
                needs_save = True
            # If lorebook has neither, set to None (global)
            elif "linked_characters" not in lorebook:
                lorebook["linked_characters"] = None
                needs_save = True
        
        if needs_save:
            self.save_all_lorebooks()
    
    def load_all_entries(self) -> None:
        """Load all lorebook entries from storage (legacy method for backward compatibility)."""
        self.load_all_lorebooks()
    
    def save_all_lorebooks(self) -> None:
        """Save all lorebooks to storage."""
        lorebooks_path = os.path.join(self.lorebook_dir, "lorebooks.json")
        with open(lorebooks_path, "w") as f:
            json.dump(self.lorebooks, f, indent=2)
        
        # Also update legacy format for backward compatibility
        # Merge all enabled lorebooks into flat entries (regardless of linked_character for legacy support)
        self.entries = {}
        for lorebook_name, lorebook in self.lorebooks.items():
            if lorebook.get("enabled", True):
                self.entries.update(lorebook.get("entries", {}))
        
        legacy_path = os.path.join(self.lorebook_dir, "lorebook.json")
        with open(legacy_path, "w") as f:
            json.dump(self.entries, f, indent=2)
    
    def save_all_entries(self) -> None:
        """Save all lorebook entries to storage (legacy method for backward compatibility)."""
        self.save_all_lorebooks()
    
    def add_or_update_entry(self, key: str, content: str, keywords: Optional[List[str]] = None, 
                           always_active: bool = False, activation_type: Optional[str] = None,
                           lorebook_name: str = "Default") -> None:
        """Add or update a lorebook entry.
        
        Args:
            key: Unique identifier for the entry
            content: The lore/information content
            keywords: List of keywords that trigger this entry (optional)
            always_active: DEPRECATED - use activation_type instead. If True, sets activation_type to "constant"
            activation_type: Type of activation - "constant" (always active), "normal" (keyword-based), or "vectorized" (semantic search)
            lorebook_name: Name of the lorebook to add the entry to (default: "Default")
        """
        if keywords is None:
            keywords = []
        
        # Ensure the lorebook exists
        if lorebook_name not in self.lorebooks:
            self.lorebooks[lorebook_name] = {
                "name": lorebook_name,
                "description": "",
                "enabled": True,
                "entries": {}
            }
        
        # Handle activation_type - convert from always_active if needed
        if activation_type is None:
            # Use always_active for backward compatibility
            activation_type = "constant" if always_active else "normal"
        
        # Add/update the entry
        entry = {
            "key": key,
            "content": content,
            "keywords": keywords,
            "activation_type": activation_type
        }
        self.lorebooks[lorebook_name]["entries"][key] = entry
        
        # Update flat entries for backward compatibility
        if self.lorebooks[lorebook_name].get("enabled", True):
            self.entries[key] = entry
        
        self.save_all_lorebooks()
    
    def get_entry(self, key: str, lorebook_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a lorebook entry by key.
        
        Args:
            key: Entry key to retrieve
            lorebook_name: Optional lorebook name to search in. If None, searches all enabled lorebooks.
        
        Returns:
            Entry dict if found, None otherwise
        """
        if lorebook_name:
            # Search in specific lorebook
            if lorebook_name in self.lorebooks:
                return self.lorebooks[lorebook_name].get("entries", {}).get(key)
            return None
        else:
            # Search in flat entries (all enabled lorebooks)
            return self.entries.get(key)
    
    def delete_entry(self, key: str, lorebook_name: Optional[str] = None) -> bool:
        """Delete a lorebook entry.
        
        Args:
            key: Entry key to delete
            lorebook_name: Optional lorebook name. If None, deletes from all lorebooks containing this key.
        
        Returns:
            True if entry was deleted, False otherwise
        """
        deleted = False
        
        if lorebook_name:
            # Delete from specific lorebook
            if lorebook_name in self.lorebooks:
                entries = self.lorebooks[lorebook_name].get("entries", {})
                if key in entries:
                    del entries[key]
                    deleted = True
        else:
            # Delete from all lorebooks
            for lorebook in self.lorebooks.values():
                entries = lorebook.get("entries", {})
                if key in entries:
                    del entries[key]
                    deleted = True
        
        if deleted:
            self.save_all_lorebooks()
        
        return deleted
    
    def list_entries(self) -> List[str]:
        """List all lorebook entry keys."""
        return list(self.entries.keys())
    
    def get_all_entries(self) -> Dict[str, Dict[str, Any]]:
        """Get all lorebook entries."""
        return self.entries.copy()
    
    def export_lorebook(self) -> str:
        """Export all lorebook entries as JSON string."""
        return json.dumps(self.entries, indent=2)
    
    def import_lorebook(self, lorebook_json: str, merge: bool = True) -> None:
        """Import lorebook entries from JSON string.
        
        Args:
            lorebook_json: JSON string containing lorebook entries
            merge: If True, merge with existing entries; if False, replace all
        """
        imported = json.loads(lorebook_json)
        if merge:
            self.entries.update(imported)
        else:
            self.entries = imported
        self.save_all_entries()
    
    def get_relevant_entries(self, text: str, include_always_active: bool = True) -> List[Dict[str, Any]]:
        """Get lorebook entries relevant to the given text.
        
        Args:
            text: Text to match against keywords
            include_always_active: Whether to include always-active/constant entries
            
        Returns:
            List of relevant lorebook entries
        """
        relevant = []
        text_lower = text.lower()
        
        for entry in self.entries.values():
            # Get activation type (with backward compatibility)
            activation_type = entry.get("activation_type")
            if activation_type is None:
                # Fall back to always_active for old entries
                activation_type = "constant" if entry.get("always_active", False) else "normal"
            
            # Include if it's constant (always active)
            if include_always_active and activation_type == "constant":
                relevant.append(entry)
                continue
            
            # For normal entries, include if any keyword is found in the text
            if activation_type == "normal":
                keywords = entry.get("keywords", [])
                if any(keyword.lower() in text_lower for keyword in keywords):
                    relevant.append(entry)
            
            # TODO: Implement vectorized/semantic search activation in the future
            # For now, treat "vectorized" the same as "normal"
            if activation_type == "vectorized":
                keywords = entry.get("keywords", [])
                if any(keyword.lower() in text_lower for keyword in keywords):
                    relevant.append(entry)
        
        return relevant
    
    def get_system_prompt_section(self, relevant_text: str = "", character_name: Optional[str] = None) -> str:
        """Generate system prompt section with lorebook entries.
        
        Args:
            relevant_text: Text to match against keywords for relevance
            character_name: Optional character name to filter character-linked lorebooks
            
        Returns:
            Formatted system prompt section with lorebook entries
        """
        # Get entries from enabled lorebooks that match the current context
        # Include global lorebooks (linked_characters is None) and character-specific lorebooks
        entries = []
        
        # Debug logging
        if self.debug_logging:
            print(f"[LOREBOOK] Getting lorebook entries for character: {character_name}")
            print(f"[LOREBOOK] Total lorebooks: {len(self.lorebooks)}")
        
        for lorebook_name, lorebook in self.lorebooks.items():
            # Skip disabled lorebooks
            if not lorebook.get("enabled", True):
                if self.debug_logging:
                    print(f"[LOREBOOK] Skipping disabled lorebook: {lorebook_name}")
                continue
            
            linked_chars = lorebook.get("linked_characters")
            lorebook_entries = lorebook.get("entries", {})
            
            # Track entries added from this lorebook
            entry_count = 0
            
            # Check if lorebook matches character filter for normal/vectorized entries
            # Global: linked_chars is None or empty list
            # Character-specific: character_name is in linked_chars list
            character_matches = not linked_chars or (character_name is not None and character_name in linked_chars)
            
            if self.debug_logging:
                print(f"[LOREBOOK] Processing lorebook '{lorebook_name}' (linked_chars: {linked_chars}, character_matches: {character_matches})")
            
            for entry in lorebook_entries.values():
                # Get activation type (with backward compatibility)
                activation_type = entry.get("activation_type")
                if activation_type is None:
                    # Fall back to always_active for old entries
                    activation_type = "constant" if entry.get("always_active", False) else "normal"
                
                # Constant entries are ALWAYS included from ALL enabled lorebooks
                # (character links don't apply to constant entries, matching SillyTavern behavior)
                if activation_type == "constant":
                    entries.append(entry)
                    entry_count += 1
                    if self.debug_logging:
                        print(f"[LOREBOOK]   Added constant entry: {entry['key']} (always included)")
                # For normal/vectorized entries, respect character filtering
                elif character_matches:
                    # Include if relevant text contains keywords
                    if relevant_text and activation_type in ["normal", "vectorized"]:
                        keywords = entry.get("keywords", [])
                        if any(keyword.lower() in relevant_text.lower() for keyword in keywords):
                            entries.append(entry)
                            entry_count += 1
                            if self.debug_logging:
                                print(f"[LOREBOOK]   Added keyword-matched entry: {entry['key']}")
            
            if self.debug_logging:
                print(f"[LOREBOOK]   Total entries from '{lorebook_name}': {entry_count}")
        
        if not entries:
            if self.debug_logging:
                print(f"[LOREBOOK] No entries found, returning empty string")
            return ""
        
        if self.debug_logging:
            print(f"[LOREBOOK] Total entries to include: {len(entries)}")
        
        sections = []
        sections.append("[Lorebook - World Information]")
        sections.append("The following information provides context about the world, characters, locations, and lore:")
        sections.append("")
        
        for entry in entries:
            sections.append(f"**{entry['key']}:**")
            sections.append(entry['content'])
            sections.append("")
        
        sections.append("[/Lorebook]")
        
        return "\n".join(sections)
    
    # Multiple Lorebook Management Methods
    
    def create_lorebook(self, name: str, description: str = "", enabled: bool = True, linked_character: Optional[str] = None, linked_characters: Optional[List[str]] = None) -> None:
        """Create a new lorebook.
        
        Args:
            name: Unique name for the lorebook
            description: Optional description
            enabled: Whether the lorebook is enabled by default
            linked_character: DEPRECATED - use linked_characters instead. Optional character name to link this lorebook to (None = global)
            linked_characters: Optional list of character names to link this lorebook to (None or empty list = global)
        """
        if name in self.lorebooks:
            raise ValueError(f"Lorebook '{name}' already exists")
        
        # Handle backward compatibility: if linked_character is provided, convert to list
        if linked_characters is None:
            if linked_character:
                linked_characters = [linked_character]
            else:
                linked_characters = None
        else:
            # Empty list should be treated as None (global)
            if not linked_characters:
                linked_characters = None
        
        self.lorebooks[name] = {
            "name": name,
            "description": description,
            "enabled": enabled,
            "linked_characters": linked_characters,
            "entries": {}
        }
        self.save_all_lorebooks()
    
    def delete_lorebook(self, name: str) -> bool:
        """Delete a lorebook.
        
        Args:
            name: Name of the lorebook to delete
        
        Returns:
            True if deleted, False if not found
        """
        if name in self.lorebooks:
            del self.lorebooks[name]
            self.save_all_lorebooks()
            return True
        return False
    
    def list_lorebooks(self) -> List[Dict[str, Any]]:
        """List all lorebooks with their metadata.
        
        Returns:
            List of lorebook info dicts
        """
        result = []
        for name, lorebook in self.lorebooks.items():
            linked_chars = lorebook.get("linked_characters")
            info = {
                "name": name,
                "description": lorebook.get("description", ""),
                "enabled": lorebook.get("enabled", True),
                "linked_characters": linked_chars,
                "entry_count": len(lorebook.get("entries", {}))
            }
            # Backward compatibility: also provide linked_character (first in list or None)
            info["linked_character"] = linked_chars[0] if linked_chars else None
            result.append(info)
        return result
    
    def get_lorebook(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific lorebook.
        
        Args:
            name: Name of the lorebook
        
        Returns:
            Lorebook dict if found, None otherwise
        """
        lorebook = self.lorebooks.get(name)
        if lorebook:
            # Create a copy to avoid modifying the original
            result = lorebook.copy()
            # Backward compatibility: also provide linked_character (first in list or None)
            linked_chars = result.get("linked_characters")
            result["linked_character"] = linked_chars[0] if linked_chars else None
            return result
        return None
    
    def update_lorebook_metadata(self, name: str, description: Optional[str] = None, 
                                 enabled: Optional[bool] = None, linked_character: Optional[str] = None,
                                 linked_characters: Optional[List[str]] = None) -> bool:
        """Update lorebook metadata.
        
        Args:
            name: Name of the lorebook
            description: Optional new description
            enabled: Optional new enabled status
            linked_character: DEPRECATED - use linked_characters instead. Optional character name to link this lorebook to (None = global, empty string to unlink)
            linked_characters: Optional list of character names to link this lorebook to (None or empty list = global)
        
        Returns:
            True if updated, False if lorebook not found
        """
        if name not in self.lorebooks:
            return False
        
        if description is not None:
            self.lorebooks[name]["description"] = description
        
        if enabled is not None:
            self.lorebooks[name]["enabled"] = enabled
        
        # Handle linked_characters (new preferred method)
        if linked_characters is not None:
            # Empty list means unlink (set to None for global)
            self.lorebooks[name]["linked_characters"] = linked_characters if linked_characters else None
        # Handle backward compatibility with linked_character (deprecated)
        elif linked_character is not None:
            # Empty string means unlink (set to None)
            if linked_character:
                self.lorebooks[name]["linked_characters"] = [linked_character]
            else:
                self.lorebooks[name]["linked_characters"] = None
        
        self.save_all_lorebooks()
        return True
    
    def enable_lorebook(self, name: str) -> bool:
        """Enable a lorebook.
        
        Args:
            name: Name of the lorebook to enable
        
        Returns:
            True if enabled, False if not found
        """
        return self.update_lorebook_metadata(name, enabled=True)
    
    def disable_lorebook(self, name: str) -> bool:
        """Disable a lorebook.
        
        Args:
            name: Name of the lorebook to disable
        
        Returns:
            True if disabled, False if not found
        """
        return self.update_lorebook_metadata(name, enabled=False)
    
    def import_lorebook_file(self, lorebook_data: Dict[str, Any], merge: bool = True) -> str:
        """Import a lorebook from a structured lorebook file.
        
        Args:
            lorebook_data: Dict containing lorebook structure with name, description, entries
            merge: If True, merge with existing; if False, replace
        
        Returns:
            Name of the imported lorebook
        """
        name = lorebook_data.get("name", "Imported Lorebook")
        description = lorebook_data.get("description", "")
        enabled = lorebook_data.get("enabled", True)
        
        # Handle both old and new format for character linking
        linked_characters = lorebook_data.get("linked_characters")
        if linked_characters is None and "linked_character" in lorebook_data:
            # Migrate old format
            linked_char = lorebook_data.get("linked_character")
            if linked_char:
                linked_characters = [linked_char]
        
        entries = lorebook_data.get("entries", {})
        
        # Migrate always_active to activation_type in imported entries
        for key, entry in entries.items():
            if "always_active" in entry and "activation_type" not in entry:
                always_active = entry.get("always_active", False)
                entry["activation_type"] = "constant" if always_active else "normal"
            elif "activation_type" not in entry:
                entry["activation_type"] = "normal"
        
        if merge and name in self.lorebooks:
            # Merge entries into existing lorebook
            self.lorebooks[name]["entries"].update(entries)
            if description:
                self.lorebooks[name]["description"] = description
            # Update linked_characters if provided in import
            if "linked_characters" in lorebook_data or "linked_character" in lorebook_data:
                self.lorebooks[name]["linked_characters"] = linked_characters
        else:
            # Create new or replace existing lorebook
            self.lorebooks[name] = {
                "name": name,
                "description": description,
                "enabled": enabled,
                "linked_characters": linked_characters,
                "entries": entries
            }
        
        self.save_all_lorebooks()
        return name
    
    def export_lorebook_file(self, name: str) -> str:
        """Export a specific lorebook as JSON string.
        
        Args:
            name: Name of the lorebook to export
        
        Returns:
            JSON string of the lorebook
        """
        if name not in self.lorebooks:
            raise ValueError(f"Lorebook '{name}' not found")
        
        lorebook = self.lorebooks[name].copy()
        # Backward compatibility: also include linked_character for old systems
        linked_chars = lorebook.get("linked_characters")
        lorebook["linked_character"] = linked_chars[0] if linked_chars else None
        
        return json.dumps(lorebook, indent=2)

