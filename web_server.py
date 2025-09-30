"""Web server for bot configuration."""
from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
from config_manager import ConfigManager
from preset_manager import PresetManager
from character_manager import CharacterManager

class WebServer:
    def __init__(self, config_manager: ConfigManager):
        self.app = Flask(__name__)
        self.config_manager = config_manager
        self.preset_manager = PresetManager()
        self.character_manager = CharacterManager()
        
        self.setup_routes()
    
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
                # Don't update hidden fields
                if 'discord_token' in data and data['discord_token'] == '***HIDDEN***':
                    del data['discord_token']
                if 'openai_config' in data and 'api_key' in data['openai_config']:
                    if data['openai_config']['api_key'] == '***HIDDEN***':
                        del data['openai_config']['api_key']
                
                self.config_manager.update_config(data)
                return jsonify({"status": "success", "message": "Configuration updated"})
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
    
    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        """Run the web server."""
        self.app.run(host=host, port=port, debug=debug)
