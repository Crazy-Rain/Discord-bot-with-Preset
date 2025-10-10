"""Web server for bot configuration."""
from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
import base64
from werkzeug.utils import secure_filename
from config_manager import ConfigManager
from preset_manager import PresetManager
from character_manager import CharacterManager
from user_characters_manager import UserCharactersManager
from lorebook_manager import LorebookManager

class WebServer:
    def __init__(self, config_manager: ConfigManager, bot_instance=None):
        self.app = Flask(__name__)
        self.config_manager = config_manager
        self._bot_instance_ref = bot_instance  # Keep for backward compatibility
        self.preset_manager = PresetManager()
        self.character_manager = CharacterManager()
        self.user_characters_manager = UserCharactersManager()
        self.lorebook_manager = LorebookManager()
        
        self.setup_routes()
    
    @property
    def bot_instance(self):
        """Get the current bot instance from main module."""
        import main
        return main.bot_instance
    
    def setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            """Serve main configuration page."""
            return render_template('index.html')
        
        @self.app.route('/api/config', methods=['GET'])
        def get_config():
            """Get current configuration."""
            config = self.config_manager.config.copy()
            # Don't expose sensitive data
            if 'discord_token' in config:
                config['discord_token'] = '***HIDDEN***'
            if 'openai_config' in config and 'api_key' in config['openai_config']:
                config['openai_config']['api_key'] = '***HIDDEN***'
            return jsonify(config)
        
        @self.app.route('/api/config', methods=['POST'])
        def update_config():
            """Update configuration."""
            try:
                data = request.json
                
                # Sanitize OpenAI config fields for proxy compatibility (strip whitespace)
                if 'openai_config' in data:
                    if 'api_key' in data['openai_config'] and data['openai_config']['api_key'] != '***HIDDEN***':
                        data['openai_config']['api_key'] = data['openai_config']['api_key'].strip()
                    if 'base_url' in data['openai_config']:
                        data['openai_config']['base_url'] = data['openai_config']['base_url'].strip()
                    if 'model' in data['openai_config']:
                        data['openai_config']['model'] = data['openai_config']['model'].strip()
                
                # Track if OpenAI config changed
                openai_config_changed = False
                new_api_key = None
                new_base_url = None
                new_model = None
                
                # Don't update hidden fields
                if 'discord_token' in data and data['discord_token'] == '***HIDDEN***':
                    del data['discord_token']
                if 'openai_config' in data and 'api_key' in data['openai_config']:
                    if data['openai_config']['api_key'] == '***HIDDEN***':
                        del data['openai_config']['api_key']
                    else:
                        # API key is being updated
                        openai_config_changed = True
                        new_api_key = data['openai_config']['api_key']
                
                # Check if base_url or model changed
                if 'openai_config' in data:
                    if 'base_url' in data['openai_config']:
                        current_base_url = self.config_manager.get('openai_config.base_url')
                        if data['openai_config']['base_url'] != current_base_url:
                            openai_config_changed = True
                            new_base_url = data['openai_config']['base_url']
                    
                    if 'model' in data['openai_config']:
                        current_model = self.config_manager.get('openai_config.model')
                        if data['openai_config']['model'] != current_model:
                            openai_config_changed = True
                            new_model = data['openai_config']['model']
                
                # Update config file
                self.config_manager.update_config(data)
                
                # Apply changes to running bot if available
                if openai_config_changed and self.bot_instance:
                    # Get all current values (use new if provided, otherwise get from config)
                    if new_api_key is None:
                        new_api_key = self.config_manager.get('openai_config.api_key')
                    if new_base_url is None:
                        new_base_url = self.config_manager.get('openai_config.base_url')
                    if new_model is None:
                        new_model = self.config_manager.get('openai_config.model')
                    
                    # Update the bot's OpenAI client
                    self.bot_instance.update_openai_config(
                        api_key=new_api_key,
                        base_url=new_base_url,
                        model=new_model
                    )
                    return jsonify({
                        "status": "success", 
                        "message": "Configuration updated and applied to running bot"
                    })
                
                # Update auto_context_limit in the running bot if it changed
                if 'auto_context_limit' in data and self.bot_instance:
                    new_limit = data['auto_context_limit']
                    # Validate and clamp the limit
                    new_limit = max(50, min(5000, new_limit))
                    self.bot_instance.auto_context_limit = new_limit
                
                return jsonify({"status": "success", "message": "Configuration updated"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/models', methods=['POST'])
        def fetch_models():
            """Fetch available models from the configured API endpoint."""
            try:
                data = request.json
                api_key = data.get('api_key', '').strip()  # Strip whitespace for proxy compatibility
                base_url = data.get('base_url', '').strip()  # Strip whitespace for proxy compatibility
                
                if not api_key or not base_url:
                    return jsonify({"status": "error", "message": "API key and base URL are required"}), 400
                
                # Create a temporary client to fetch models
                from openai_client import OpenAIClient
                temp_client = OpenAIClient(api_key=api_key, base_url=base_url)
                models = temp_client.list_models()
                
                return jsonify({"status": "success", "models": models})
            except ValueError as e:
                return jsonify({"status": "error", "message": str(e)}), 400
            except Exception as e:
                return jsonify({"status": "error", "message": f"Failed to fetch models: {str(e)}"}), 400
        
        @self.app.route('/api/api_configs', methods=['GET'])
        def list_api_configs():
            """List all saved API configurations."""
            configs = self.config_manager.get_api_configs()
            # Return configs with hidden API keys
            configs_list = []
            for name, config in configs.items():
                configs_list.append({
                    'name': name,
                    'base_url': config.get('base_url', ''),
                    'model': config.get('model', ''),
                    'api_key': '***HIDDEN***'
                })
            return jsonify({"configs": configs_list})
        
        @self.app.route('/api/api_configs/<config_name>', methods=['GET'])
        def get_api_config(config_name):
            """Get a specific API configuration."""
            config = self.config_manager.get_api_config(config_name)
            if not config:
                return jsonify({"error": "Configuration not found"}), 404
            # Hide the API key
            config_copy = config.copy()
            config_copy['api_key'] = '***HIDDEN***'
            return jsonify(config_copy)
        
        @self.app.route('/api/api_configs/<config_name>', methods=['POST'])
        def save_api_config(config_name):
            """Save an API configuration."""
            try:
                data = request.json
                api_key = data.get('api_key', '').strip() if data.get('api_key') else ''  # Strip whitespace for proxy compatibility
                base_url = data.get('base_url', '').strip() if data.get('base_url') else ''  # Strip whitespace for proxy compatibility
                model = data.get('model', '').strip() if data.get('model') else ''
                
                if not all([api_key, base_url, model]):
                    return jsonify({"status": "error", "message": "Missing required fields"}), 400
                
                # Don't update if api_key is hidden placeholder
                if api_key == '***HIDDEN***':
                    # Get existing config and keep its api_key
                    existing_config = self.config_manager.get_api_config(config_name)
                    if existing_config:
                        api_key = existing_config.get('api_key', '')
                    else:
                        return jsonify({"status": "error", "message": "Cannot create new config with hidden API key"}), 400
                
                self.config_manager.save_api_config(config_name, api_key, base_url, model)
                return jsonify({"status": "success", "message": f"API configuration '{config_name}' saved"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/api_configs/<config_name>', methods=['DELETE'])
        def delete_api_config(config_name):
            """Delete an API configuration."""
            try:
                if self.config_manager.delete_api_config(config_name):
                    return jsonify({"status": "success", "message": f"API configuration '{config_name}' deleted"})
                else:
                    return jsonify({"status": "error", "message": "Configuration not found"}), 404
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/api_configs/<config_name>/load', methods=['POST'])
        def load_api_config(config_name):
            """Load an API configuration to get the actual values (including API key)."""
            try:
                config = self.config_manager.get_api_config(config_name)
                if not config:
                    return jsonify({"status": "error", "message": "Configuration not found"}), 404
                
                # Return the full config including API key for loading into form
                return jsonify({
                    "status": "success",
                    "config": config
                })
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/presets', methods=['GET'])
        def list_presets():
            """List all presets."""
            presets = self.preset_manager.list_presets()
            return jsonify({"presets": presets})
        
        @self.app.route('/api/presets/<preset_name>', methods=['GET'])
        def get_preset(preset_name):
            """Get a specific preset."""
            try:
                preset = self.preset_manager.load_preset(preset_name)
                return jsonify(preset)
            except FileNotFoundError:
                return jsonify({"error": "Preset not found"}), 404
        
        @self.app.route('/api/presets/<preset_name>', methods=['POST'])
        def save_preset(preset_name):
            """Save a preset."""
            try:
                data = request.json
                self.preset_manager.save_preset(preset_name, data)
                return jsonify({"status": "success", "message": f"Preset '{preset_name}' saved"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/presets/<preset_name>', methods=['DELETE'])
        def delete_preset(preset_name):
            """Delete a preset."""
            try:
                self.preset_manager.delete_preset(preset_name)
                return jsonify({"status": "success", "message": f"Preset '{preset_name}' deleted"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/presets/<preset_name>/export', methods=['GET'])
        def export_preset(preset_name):
            """Export a preset as JSON."""
            try:
                preset_json = self.preset_manager.export_preset(preset_name)
                return jsonify({"preset": preset_json})
            except FileNotFoundError:
                return jsonify({"error": "Preset not found"}), 404
        
        @self.app.route('/api/presets/import', methods=['POST'])
        def import_preset():
            """Import a preset from JSON."""
            try:
                data = request.json
                preset_name = data.get('name')
                preset_json = data.get('preset')
                
                if not preset_name or not preset_json:
                    return jsonify({"status": "error", "message": "Missing name or preset data"}), 400
                
                self.preset_manager.import_preset(preset_name, preset_json)
                return jsonify({"status": "success", "message": f"Preset '{preset_name}' imported"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/characters', methods=['GET'])
        def list_characters():
            """List all character cards."""
            characters = self.character_manager.list_characters()
            return jsonify({"characters": characters})
        
        @self.app.route('/api/characters/<character_name>', methods=['GET'])
        def get_character(character_name):
            """Get a specific character card."""
            try:
                character = self.character_manager.load_character(character_name)
                return jsonify(character)
            except FileNotFoundError:
                return jsonify({"error": "Character not found"}), 404
        
        @self.app.route('/api/characters/<character_name>', methods=['POST'])
        def save_character(character_name):
            """Save a character card."""
            try:
                data = request.json
                self.character_manager.save_character(character_name, data)
                return jsonify({"status": "success", "message": f"Character '{character_name}' saved"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/characters/<character_name>', methods=['DELETE'])
        def delete_character(character_name):
            """Delete a character card."""
            try:
                self.character_manager.delete_character(character_name)
                return jsonify({"status": "success", "message": f"Character '{character_name}' deleted"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/characters/<character_name>/export', methods=['GET'])
        def export_character(character_name):
            """Export a character as JSON."""
            try:
                character_json = self.character_manager.export_character(character_name)
                return jsonify({"character": character_json})
            except FileNotFoundError:
                return jsonify({"error": "Character not found"}), 404
        
        @self.app.route('/api/characters/import', methods=['POST'])
        def import_character():
            """Import a character from JSON."""
            try:
                data = request.json
                character_name = data.get('name')
                character_json = data.get('character')
                
                if not character_name or not character_json:
                    return jsonify({"status": "error", "message": "Missing name or character data"}), 400
                
                self.character_manager.import_character(character_name, character_json)
                return jsonify({"status": "success", "message": f"Character '{character_name}' imported"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/characters/upload_avatar', methods=['POST'])
        def upload_avatar():
            """Upload an avatar image for a character."""
            try:
                if 'avatar' not in request.files:
                    return jsonify({"status": "error", "message": "No file provided"}), 400
                
                file = request.files['avatar']
                character_name = request.form.get('character_name')
                
                if not character_name:
                    return jsonify({"status": "error", "message": "Character name is required"}), 400
                
                if file.filename == '':
                    return jsonify({"status": "error", "message": "No file selected"}), 400
                
                # Validate file extension
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                if file_ext not in allowed_extensions:
                    return jsonify({"status": "error", "message": "Invalid file type. Only PNG, JPG, and GIF are allowed"}), 400
                
                # Create avatars directory if it doesn't exist
                avatars_dir = 'character_avatars'
                if not os.path.exists(avatars_dir):
                    os.makedirs(avatars_dir)
                
                # Save file with character name
                filename = f"{secure_filename(character_name)}.{file_ext}"
                filepath = os.path.join(avatars_dir, filename)
                file.save(filepath)
                
                # Convert to base64 data URL for storage
                with open(filepath, 'rb') as f:
                    image_data = f.read()
                    base64_data = base64.b64encode(image_data).decode('utf-8')
                    mime_type = f"image/{file_ext if file_ext != 'jpg' else 'jpeg'}"
                    data_url = f"data:{mime_type};base64,{base64_data}"
                
                return jsonify({
                    "status": "success", 
                    "message": "Avatar uploaded successfully",
                    "avatar_url": data_url,
                    "filename": filename
                })
            except Exception as e:
                return jsonify({"status": "error", "message": f"Error uploading avatar: {str(e)}"}), 400
        
        @self.app.route('/api/user_characters', methods=['GET'])
        def list_user_characters():
            """List all user characters."""
            characters = self.user_characters_manager.get_all_characters()
            return jsonify({"characters": characters})
        
        @self.app.route('/api/user_characters/<character_name>', methods=['GET'])
        def get_user_character(character_name):
            """Get a specific user character."""
            character = self.user_characters_manager.get_character(character_name)
            if character:
                return jsonify(character)
            return jsonify({"error": "User character not found"}), 404
        
        @self.app.route('/api/user_characters/<character_name>', methods=['POST'])
        def save_user_character(character_name):
            """Save a user character."""
            try:
                data = request.json
                description = data.get('description', '')
                sheet = data.get('sheet', '')
                sheet_enabled = data.get('sheet_enabled', False)
                self.user_characters_manager.add_or_update_character(
                    character_name, description, sheet, sheet_enabled
                )
                return jsonify({"status": "success", "message": f"User character '{character_name}' saved"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/user_characters/<character_name>', methods=['DELETE'])
        def delete_user_character(character_name):
            """Delete a user character."""
            try:
                if self.user_characters_manager.delete_character(character_name):
                    return jsonify({"status": "success", "message": f"User character '{character_name}' deleted"})
                return jsonify({"status": "error", "message": "User character not found"}), 404
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/user_characters/export', methods=['GET'])
        def export_user_characters():
            """Export all user characters as JSON."""
            try:
                characters_json = self.user_characters_manager.export_characters()
                return jsonify({"characters": characters_json})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/user_characters/import', methods=['POST'])
        def import_user_characters():
            """Import user characters from JSON."""
            try:
                data = request.json
                characters_json = data.get('characters')
                
                if not characters_json:
                    return jsonify({"status": "error", "message": "Missing characters data"}), 400
                
                self.user_characters_manager.import_characters(characters_json)
                return jsonify({"status": "success", "message": "User characters imported"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        # Lorebook API endpoints
        @self.app.route('/api/lorebook', methods=['GET'])
        def list_lorebook_entries():
            """List all lorebook entries."""
            entries = self.lorebook_manager.get_all_entries()
            return jsonify({"entries": entries})
        
        @self.app.route('/api/lorebook/<key>', methods=['GET'])
        def get_lorebook_entry(key):
            """Get a specific lorebook entry."""
            entry = self.lorebook_manager.get_entry(key)
            if entry:
                return jsonify(entry)
            return jsonify({"error": "Lorebook entry not found"}), 404
        
        @self.app.route('/api/lorebook/<key>', methods=['POST'])
        def save_lorebook_entry(key):
            """Save a lorebook entry."""
            try:
                data = request.json
                content = data.get('content', '')
                keywords = data.get('keywords', [])
                # Support both old always_active and new activation_type
                activation_type = data.get('activation_type')
                always_active = data.get('always_active', False)
                lorebook_name = data.get('lorebook_name', 'Default')
                
                self.lorebook_manager.add_or_update_entry(
                    key, content, keywords, 
                    always_active=always_active,
                    activation_type=activation_type,
                    lorebook_name=lorebook_name
                )
                return jsonify({"status": "success", "message": f"Lorebook entry '{key}' saved"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/lorebook/<key>', methods=['DELETE'])
        def delete_lorebook_entry(key):
            """Delete a lorebook entry."""
            try:
                data = request.json or {}
                lorebook_name = data.get('lorebook_name')
                
                if self.lorebook_manager.delete_entry(key, lorebook_name):
                    return jsonify({"status": "success", "message": f"Lorebook entry '{key}' deleted"})
                return jsonify({"status": "error", "message": "Lorebook entry not found"}), 404
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/lorebook/export', methods=['GET'])
        def export_lorebook():
            """Export all lorebook entries as JSON."""
            try:
                lorebook_json = self.lorebook_manager.export_lorebook()
                return jsonify({"lorebook": lorebook_json})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/lorebook/import', methods=['POST'])
        def import_lorebook():
            """Import lorebook entries from JSON."""
            try:
                data = request.json
                lorebook_json = data.get('lorebook')
                merge = data.get('merge', True)
                
                if not lorebook_json:
                    return jsonify({"status": "error", "message": "Missing lorebook data"}), 400
                
                # Try to parse as new structured format first
                try:
                    lorebook_data = json.loads(lorebook_json) if isinstance(lorebook_json, str) else lorebook_json
                    
                    # Check if it's a structured lorebook (has name and entries)
                    if isinstance(lorebook_data, dict) and "name" in lorebook_data and "entries" in lorebook_data:
                        # New format: import as a complete lorebook
                        name = self.lorebook_manager.import_lorebook_file(lorebook_data, merge)
                        return jsonify({"status": "success", "message": f"Lorebook '{name}' imported"})
                    else:
                        # Legacy format: flat entries dict - import to Default lorebook
                        self.lorebook_manager.import_lorebook(lorebook_json, merge)
                        return jsonify({"status": "success", "message": "Lorebook imported to Default"})
                except json.JSONDecodeError:
                    self.lorebook_manager.import_lorebook(lorebook_json, merge)
                    return jsonify({"status": "success", "message": "Lorebook imported"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        # Multiple Lorebooks API endpoints
        @self.app.route('/api/lorebooks', methods=['GET'])
        def list_lorebooks():
            """List all lorebooks."""
            try:
                lorebooks = self.lorebook_manager.list_lorebooks()
                return jsonify({"lorebooks": lorebooks})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/lorebooks/<name>', methods=['GET'])
        def get_lorebook(name):
            """Get a specific lorebook."""
            try:
                lorebook = self.lorebook_manager.get_lorebook(name)
                if lorebook:
                    return jsonify(lorebook)
                return jsonify({"error": "Lorebook not found"}), 404
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/lorebooks/<name>', methods=['POST'])
        def update_lorebook(name):
            """Update lorebook metadata."""
            try:
                data = request.json
                description = data.get('description')
                enabled = data.get('enabled')
                # Support both old single character and new multiple characters
                linked_character = data.get('linked_character') if 'linked_character' in data else None
                linked_characters = data.get('linked_characters') if 'linked_characters' in data else None
                
                if self.lorebook_manager.update_lorebook_metadata(
                    name, description, enabled, linked_character, linked_characters
                ):
                    return jsonify({"status": "success", "message": f"Lorebook '{name}' updated"})
                return jsonify({"status": "error", "message": "Lorebook not found"}), 404
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/lorebooks/<name>', methods=['DELETE'])
        def delete_lorebook(name):
            """Delete a lorebook."""
            try:
                if self.lorebook_manager.delete_lorebook(name):
                    return jsonify({"status": "success", "message": f"Lorebook '{name}' deleted"})
                return jsonify({"status": "error", "message": "Lorebook not found"}), 404
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/lorebooks', methods=['POST'])
        def create_lorebook():
            """Create a new lorebook."""
            try:
                data = request.json
                name = data.get('name')
                description = data.get('description', '')
                enabled = data.get('enabled', True)
                # Support both old single character and new multiple characters
                linked_character = data.get('linked_character')
                linked_characters = data.get('linked_characters')
                
                if not name:
                    return jsonify({"status": "error", "message": "Missing lorebook name"}), 400
                
                self.lorebook_manager.create_lorebook(
                    name, description, enabled, linked_character, linked_characters
                )
                return jsonify({"status": "success", "message": f"Lorebook '{name}' created"})
            except ValueError as e:
                return jsonify({"status": "error", "message": str(e)}), 400
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/lorebooks/<name>/export', methods=['GET'])
        def export_lorebook_file(name):
            """Export a specific lorebook as JSON."""
            try:
                lorebook_json = self.lorebook_manager.export_lorebook_file(name)
                return jsonify({"lorebook": lorebook_json})
            except ValueError as e:
                return jsonify({"error": str(e)}), 404
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/lorebooks/<name>/toggle', methods=['POST'])
        def toggle_lorebook(name):
            """Toggle a lorebook's enabled status."""
            try:
                lorebook = self.lorebook_manager.get_lorebook(name)
                if not lorebook:
                    return jsonify({"status": "error", "message": "Lorebook not found"}), 404
                
                current_status = lorebook.get("enabled", True)
                new_status = not current_status
                
                if self.lorebook_manager.update_lorebook_metadata(name, enabled=new_status):
                    return jsonify({
                        "status": "success", 
                        "message": f"Lorebook '{name}' {'enabled' if new_status else 'disabled'}",
                        "enabled": new_status
                    })
                return jsonify({"status": "error", "message": "Failed to toggle lorebook"}), 500
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/cp_total', methods=['POST'])
        def update_cp_total():
            """Update CP Total manually."""
            try:
                data = request.json
                cp_total = data.get('cp_total', 0)
                
                # Update CP total in config
                if 'cp_tracking' not in self.config_manager.config:
                    self.config_manager.config['cp_tracking'] = {}
                self.config_manager.config['cp_tracking']['cp_total'] = cp_total
                self.config_manager.save_config()
                
                # Update all channels in the bot if it's running
                if self.bot_instance:
                    for channel_id in self.bot_instance.cp_totals:
                        self.bot_instance.cp_totals[channel_id] = cp_total
                
                return jsonify({
                    "status": "success",
                    "message": f"CP Total updated to {cp_total}"
                })
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/servers', methods=['GET'])
        def get_servers():
            """Get list of servers the bot is connected to (without channels)."""
            if not self.bot_instance:
                return jsonify({"servers": []})
            
            servers = []
            for guild in self.bot_instance.guilds:
                try:
                    # Safely get text_channels count
                    channel_count = len(guild.text_channels) if hasattr(guild, 'text_channels') and guild.text_channels is not None else 0
                    
                    # Get server configuration
                    server_config = self.config_manager.get(f'server_configs.{guild.id}', {})
                    
                    servers.append({
                        'id': str(guild.id),
                        'name': guild.name,
                        'channel_count': channel_count,
                        'preset': server_config.get('preset', ''),
                        'api_config': server_config.get('api_config', ''),
                        'character': server_config.get('character', '')
                    })
                except Exception as e:
                    # If there's any error getting guild info, skip it but log the issue
                    print(f"Error getting info for guild {guild.id}: {e}")
                    continue
            
            return jsonify({"servers": servers})
        
        @self.app.route('/api/servers/<server_id>/channels', methods=['GET'])
        def get_server_channels(server_id):
            """Get channels for a specific server with pagination support."""
            if not self.bot_instance:
                return jsonify({"channels": [], "total": 0, "page": 1, "per_page": 100})
            
            # Get pagination parameters
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 100))
            search = request.args.get('search', '').lower()
            
            # Validate pagination parameters
            page = max(1, page)
            per_page = min(max(1, per_page), 500)  # Max 500 per page
            
            # Find the guild
            guild = None
            for g in self.bot_instance.guilds:
                if str(g.id) == server_id:
                    guild = g
                    break
            
            if not guild:
                return jsonify({"error": "Server not found"}), 404
            
            all_channels = []
            try:
                # Safely access text_channels
                text_channels = guild.text_channels if hasattr(guild, 'text_channels') and guild.text_channels is not None else []
                for channel in text_channels:
                    # Apply search filter if provided
                    if search and search not in channel.name.lower():
                        continue
                    
                    # Get current configuration for this channel
                    channel_config = self.config_manager.get(f'channel_configs.{channel.id}', {})
                    all_channels.append({
                        'id': str(channel.id),
                        'name': channel.name,
                        'preset': channel_config.get('preset', ''),
                        'api_config': channel_config.get('api_config', ''),
                        'character': channel_config.get('character', '')
                    })
            except Exception as e:
                # If there's any error getting channels, return empty list
                print(f"Error getting channels for guild {server_id}: {e}")
                return jsonify({"channels": [], "total": 0, "page": page, "per_page": per_page})
            
            # Calculate pagination
            total_channels = len(all_channels)
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            paginated_channels = all_channels[start_idx:end_idx]
            
            return jsonify({
                "channels": paginated_channels,
                "total": total_channels,
                "page": page,
                "per_page": per_page,
                "total_pages": (total_channels + per_page - 1) // per_page if per_page > 0 else 0
            })
        
        @self.app.route('/api/server_config/<server_id>', methods=['POST'])
        def save_server_config(server_id):
            """Save configuration for a specific server."""
            try:
                data = request.json
                preset = data.get('preset', '')
                api_config = data.get('api_config', '')
                character = data.get('character', '')
                
                # Save to config
                self.config_manager.set(f'server_configs.{server_id}.preset', preset)
                self.config_manager.set(f'server_configs.{server_id}.api_config', api_config)
                self.config_manager.set(f'server_configs.{server_id}.character', character)
                
                return jsonify({
                    "status": "success",
                    "message": f"Server configuration saved"
                })
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/channel_config/<channel_id>', methods=['POST'])
        def save_channel_config(channel_id):
            """Save configuration for a specific channel."""
            try:
                data = request.json
                preset = data.get('preset', '')
                api_config = data.get('api_config', '')
                character = data.get('character', '')
                
                # Save to config
                self.config_manager.set(f'channel_configs.{channel_id}.preset', preset)
                self.config_manager.set(f'channel_configs.{channel_id}.api_config', api_config)
                self.config_manager.set(f'channel_configs.{channel_id}.character', character)
                
                return jsonify({
                    "status": "success",
                    "message": f"Channel configuration saved"
                })
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/all_configs', methods=['GET'])
        def get_all_configs():
            """Get all server and channel configurations from config file (not just connected servers)."""
            try:
                server_configs = self.config_manager.get('server_configs', {})
                channel_configs = self.config_manager.get('channel_configs', {})
                
                # Format server configs
                servers = []
                for server_id, config in server_configs.items():
                    servers.append({
                        'id': server_id,
                        'name': f'Server {server_id}',  # We don't have the name unless bot is connected
                        'preset': config.get('preset', ''),
                        'api_config': config.get('api_config', ''),
                        'character': config.get('character', ''),
                        'from_config': True  # Flag to indicate this is from config, not Discord
                    })
                
                # Format channel configs
                channels = []
                for channel_id, config in channel_configs.items():
                    channels.append({
                        'id': channel_id,
                        'name': f'Channel {channel_id}',  # We don't have the name unless bot is connected
                        'preset': config.get('preset', ''),
                        'api_config': config.get('api_config', ''),
                        'character': config.get('character', ''),
                        'from_config': True  # Flag to indicate this is from config, not Discord
                    })
                
                return jsonify({
                    'servers': servers,
                    'channels': channels
                })
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/server_config/<server_id>', methods=['DELETE'])
        def delete_server_config(server_id):
            """Delete configuration for a specific server."""
            try:
                server_configs = self.config_manager.get('server_configs', {})
                if server_id in server_configs:
                    del server_configs[server_id]
                    self.config_manager.set('server_configs', server_configs)
                    return jsonify({
                        "status": "success",
                        "message": f"Server configuration deleted"
                    })
                else:
                    return jsonify({
                        "status": "error",
                        "message": f"Server {server_id} not found in configuration"
                    }), 404
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/api/channel_config/<channel_id>', methods=['DELETE'])
        def delete_channel_config(channel_id):
            """Delete configuration for a specific channel."""
            try:
                channel_configs = self.config_manager.get('channel_configs', {})
                if channel_id in channel_configs:
                    del channel_configs[channel_id]
                    self.config_manager.set('channel_configs', channel_configs)
                    return jsonify({
                        "status": "success",
                        "message": f"Channel configuration deleted"
                    })
                else:
                    return jsonify({
                        "status": "error",
                        "message": f"Channel {channel_id} not found in configuration"
                    }), 404
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400
        
        @self.app.route('/character_avatars/<filename>')
        def serve_character_avatar(filename):
            """Serve character avatar images."""
            avatars_dir = os.path.join(os.getcwd(), 'character_avatars')
            return send_from_directory(avatars_dir, filename)
    
    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        """Run the web server."""
        self.app.run(host=host, port=port, debug=debug, threaded=True, use_reloader=False)
