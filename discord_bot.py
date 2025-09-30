"""Discord bot with OpenAI integration and preset support."""
import discord
from discord.ext import commands
from typing import Dict, List, Optional
from config_manager import ConfigManager
from preset_manager import PresetManager
from character_manager import CharacterManager
from openai_client import OpenAIClient

class DiscordBot(commands.Bot):
    def __init__(self, config: ConfigManager):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        
        self.config_manager = config
        self.preset_manager = PresetManager()
        self.character_manager = CharacterManager()
        
        # Initialize OpenAI client
        openai_config = config.get("openai_config", {})
        self.openai_client = OpenAIClient(
            api_key=openai_config.get("api_key", ""),
            base_url=openai_config.get("base_url", "https://api.openai.com/v1"),
            model=openai_config.get("model", "gpt-3.5-turbo")
        )
        
        # Load default preset
        default_preset = config.get("default_preset", {})
        if default_preset:
            self.preset_manager.current_preset = default_preset
        
        # Conversation history per channel
        self.conversations: Dict[int, List[Dict[str, str]]] = {}
        
        # Add commands
        self.add_bot_commands()
    
    def add_bot_commands(self):
        """Add bot commands."""
        
        @self.command(name="chat", help="Chat with the AI")
        async def chat(ctx, *, message: str):
            """Chat with the AI using current preset and character."""
            channel_id = ctx.channel.id
            
            # Initialize conversation history if needed
            if channel_id not in self.conversations:
                self.conversations[channel_id] = []
            
            # Get system prompt
            system_prompt = self.get_system_prompt()
            
            # Build messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history
            messages.extend(self.conversations[channel_id])
            
            # Add user message
            messages.append({"role": "user", "content": message})
            
            # Get preset parameters
            preset = self.preset_manager.get_current_preset()
            
            try:
                async with ctx.typing():
                    # Generate response
                    response = await self.openai_client.chat_completion(
                        messages=messages,
                        temperature=preset.get("temperature", 0.7),
                        max_tokens=preset.get("max_tokens", 2000),
                        top_p=preset.get("top_p", 1.0),
                        frequency_penalty=preset.get("frequency_penalty", 0.0),
                        presence_penalty=preset.get("presence_penalty", 0.0)
                    )
                
                # Update conversation history
                self.conversations[channel_id].append({"role": "user", "content": message})
                self.conversations[channel_id].append({"role": "assistant", "content": response})
                
                # Limit conversation history
                if len(self.conversations[channel_id]) > 20:
                    self.conversations[channel_id] = self.conversations[channel_id][-20:]
                
                # Send response (split if too long)
                if len(response) > 2000:
                    for i in range(0, len(response), 2000):
                        await ctx.send(response[i:i+2000])
                else:
                    await ctx.send(response)
            
            except Exception as e:
                await ctx.send(f"Error: {str(e)}")
        
        @self.command(name="clear", help="Clear conversation history")
        async def clear(ctx):
            """Clear conversation history for this channel."""
            channel_id = ctx.channel.id
            if channel_id in self.conversations:
                self.conversations[channel_id] = []
            await ctx.send("Conversation history cleared!")
        
        @self.command(name="preset", help="Load a preset")
        async def preset(ctx, preset_name: str):
            """Load a preset by name."""
            try:
                self.preset_manager.load_preset(preset_name)
                await ctx.send(f"Loaded preset: {preset_name}")
            except FileNotFoundError:
                await ctx.send(f"Preset not found: {preset_name}")
        
        @self.command(name="presets", help="List available presets")
        async def presets(ctx):
            """List all available presets."""
            preset_list = self.preset_manager.list_presets()
            if preset_list:
                await ctx.send(f"Available presets: {', '.join(preset_list)}")
            else:
                await ctx.send("No presets available.")
        
        @self.command(name="character", help="Load a character card")
        async def character(ctx, character_name: str):
            """Load a character card by name."""
            try:
                self.character_manager.load_character(character_name)
                await ctx.send(f"Loaded character: {character_name}")
                # Clear conversation when switching characters
                channel_id = ctx.channel.id
                if channel_id in self.conversations:
                    self.conversations[channel_id] = []
            except FileNotFoundError:
                await ctx.send(f"Character not found: {character_name}")
        
        @self.command(name="characters", help="List available characters")
        async def characters(ctx):
            """List all available character cards."""
            char_list = self.character_manager.list_characters()
            if char_list:
                await ctx.send(f"Available characters: {', '.join(char_list)}")
            else:
                await ctx.send("No characters available.")
        
        @self.command(name="help_bot", help="Show bot help")
        async def help_bot(ctx):
            """Show bot help information."""
            help_text = """
**Discord Bot Commands:**
`!chat <message>` - Chat with the AI
`!clear` - Clear conversation history
`!preset <name>` - Load a preset
`!presets` - List available presets
`!character <name>` - Load a character card
`!characters` - List available characters
`!help_bot` - Show this help message

**Configuration:**
Visit http://localhost:5000 to configure the bot via web interface.
"""
            await ctx.send(help_text)
    
    def get_system_prompt(self) -> str:
        """Get the system prompt from character or preset."""
        # Character takes precedence
        char_prompt = self.character_manager.get_character_system_prompt()
        if char_prompt:
            return char_prompt
        
        # Fall back to preset
        preset = self.preset_manager.get_current_preset()
        return preset.get("system_prompt", "You are a helpful AI assistant.")
    
    async def on_ready(self):
        """Called when bot is ready."""
        print(f"Bot is ready! Logged in as {self.user}")
