"""Lorebook manager for handling world-building and lore information."""
import json
import os
from typing import Dict, Any, List, Optional

class LorebookManager:
    def __init__(self, lorebook_dir: str = "lorebook"):
        self.lorebook_dir = lorebook_dir
        self.ensure_lorebook_dir()
        self.entries: Dict[str, Dict[str, Any]] = {}
        self.load_all_entries()
    
    def ensure_lorebook_dir(self) -> None:
        """Ensure lorebook directory exists."""
        if not os.path.exists(self.lorebook_dir):
            os.makedirs(self.lorebook_dir)
    
    def load_all_entries(self) -> None:
        """Load all lorebook entries from storage."""
        storage_path = os.path.join(self.lorebook_dir, "lorebook.json")
        if os.path.exists(storage_path):
            with open(storage_path, "r") as f:
                self.entries = json.load(f)
        else:
            self.entries = {}
    
    def save_all_entries(self) -> None:
        """Save all lorebook entries to storage."""
        storage_path = os.path.join(self.lorebook_dir, "lorebook.json")
        with open(storage_path, "w") as f:
            json.dump(self.entries, f, indent=2)
    
    def add_or_update_entry(self, key: str, content: str, keywords: Optional[List[str]] = None, 
                           always_active: bool = False) -> None:
        """Add or update a lorebook entry.
        
        Args:
            key: Unique identifier for the entry
            content: The lore/information content
            keywords: List of keywords that trigger this entry (optional)
            always_active: If True, this entry is always included in context
        """
        if keywords is None:
            keywords = []
        
        self.entries[key] = {
            "key": key,
            "content": content,
            "keywords": keywords,
            "always_active": always_active
        }
        self.save_all_entries()
    
    def get_entry(self, key: str) -> Optional[Dict[str, Any]]:
        """Get a lorebook entry by key."""
        return self.entries.get(key)
    
    def delete_entry(self, key: str) -> bool:
        """Delete a lorebook entry."""
        if key in self.entries:
            del self.entries[key]
            self.save_all_entries()
            return True
        return False
    
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
            include_always_active: Whether to include always-active entries
            
        Returns:
            List of relevant lorebook entries
        """
        relevant = []
        text_lower = text.lower()
        
        for entry in self.entries.values():
            # Include if it's always active
            if include_always_active and entry.get("always_active", False):
                relevant.append(entry)
                continue
            
            # Include if any keyword is found in the text
            keywords = entry.get("keywords", [])
            if any(keyword.lower() in text_lower for keyword in keywords):
                relevant.append(entry)
        
        return relevant
    
    def get_system_prompt_section(self, relevant_text: str = "") -> str:
        """Generate system prompt section with lorebook entries.
        
        Args:
            relevant_text: Text to match against keywords for relevance
            
        Returns:
            Formatted system prompt section with lorebook entries
        """
        # Get relevant entries based on text, or all always-active entries if no text
        if relevant_text:
            entries = self.get_relevant_entries(relevant_text)
        else:
            entries = [e for e in self.entries.values() if e.get("always_active", False)]
        
        if not entries:
            return ""
        
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
